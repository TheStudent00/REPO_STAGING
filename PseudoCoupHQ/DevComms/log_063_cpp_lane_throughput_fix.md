# log 063 — the cpp lane throughput fix, 2026-08-22

`ct_cpp_l1.sh` had done 8,000 of 96,934 probes in the wall clock available,
against log_062's own 1.63 ms/probe projection. This log finds the real
cause, fixes it in `l3_cart_gen.py` for every STATIC8 language (not just
cpp), regenerates the seven affected lanes, and hands the owner one restart
sequence.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

---

## 1 — the cause, with its evidence

**It is not a rate. `run_binary`'s read loop has no timeout at all, and
one probe stopped writing output.** The lane's own log,
`Airlock/agent/logs/20260822T184954Z__ct_cpp_l1.sh.log`, ends here and has
not advanced since:

```
[progress] cpp L1 chunk 4/49 [8000/96934]   8.3%  build 1.53s  run 10.88s  elapsed 17s  ETA 191s
   .. chunk of 2000 refused; the compiler named 32 probe(s), dropping them and rebuilding (attempt 1)
```

Two things in that line matter. First, chunk 4's `run` time is **10.88s**
against **0.00s** for chunks 1–3 — an 18x jump that is the leading edge of
whatever went wrong. Second, and decisively: chunk 5 never printed
**anything** — not its progress line, not even the "chunk refused"
message every earlier chunk produced within a second or two. The only
code between two print statements that can block silently that long is
`compile_chunk`'s `subprocess.run(..., timeout=3000)` or `run_binary`'s
execution loop — and the wall clock has now run well past 3000s with no
`TimeoutExpired` traceback in the log and `agent/status/ct_cpp_l1.sh.status`
still reading `state=running`, which rules out the compile path (that
timeout would have fired and crashed the driver by now). That leaves
`run_binary`.

`grep -n "STALL\b" agent/drop/ct_cpp_l1.sh` before this fix returned
**exactly one line** — the assignment `STALL = T.get("stall_s", 120.0)`.
Nothing else in the file ever reads it. `run_binary`'s read loop was
`for line in pr.stdout: ...` followed by `pr.wait()`, both **unconditional
blocking calls with no timeout of any kind**. And `emit_static8`'s own
`payload` dict, which becomes `table.json`, never set a `"stall_s"` key at
all — so even the dead 120.0 default was never reaching anywhere real.
This is confirmed by reading `l3_cart_gen.py` directly, not inferred: the
STATIC8 driver template (the one baked into all seven of cpp / java /
kotlin / swift / dart / csharp / typescript's lanes) had the ruby driver's
stall *variable* copied over without the ruby driver's stall *mechanism*
(the queue + thread + `q.get(timeout=...)` pattern at `l3_cart_gen.py`
~line 1211–1308, proven in production since log_052).

Rust and go's `run_binary` have the identical unconditional-block shape
and are not touched here: their operand set is plain machine arithmetic
that panics or traps rather than looping, so nothing in the run of record
has ever produced a hang there. Something in the cpp chunk that started
run 5 did not behave that way — what specifically hung is **not**
determined (no toolchain access in this sandbox to reproduce it inside the
container), but it does not need to be: the fix is to bound the wait
regardless of cause, exactly as ruby's stall budget already does for a
different failure mode (`**` against BigDecimal, log_052 §2).

**"2,270 ms/probe" is not a rate.** It is `elapsed_wall / probes_done`
with the elapsed wall clock dominated by one indefinite wait. The
340x-slower framing measures the stall, not the compiler.

**Ruled out, per the brief, and confirmed rather than re-litigated:** the
log's one `g++ (Ubuntu 15.2.0...)` line is the version banner printed once
at start, not a per-probe compile count — the real evidence for
"batch-into-few-files" is the log's own `chunking: 96934 probes -> 49
chunk files` line, which is real per-chunk batching and was never the
problem.

---

## 2 — the fix, in `l3_cart_gen.py`, shared by all seven STATIC8 languages

Both changes live in the ONE driver template (`STATIC8_DRIVER`) and the
ONE emitter function (`emit_static8`) that all seven languages share, so
fixing them there fixes cpp, java, kotlin, swift, dart, csharp and
typescript at once. php is untouched — it is route C, already carries its
own working stall discipline (`PHP_STALL_S = 2.0`, log_062), and was never
at risk of this failure mode.

**a. The execution-side stall watchdog, now real.** `run_binary` pumps the
subprocess's stdout through a background thread into a `queue.Queue`, and
reads it with `q.get(timeout=STARTUP-or-STALL)` — the identical mechanism
ruby's driver has used since log_052. A gap with no line for `STARTUP`
seconds before the first line, or `STALL` seconds after, is now a STALL:
the process is `pr.kill()`-ed (the OUTCOME recorded is `ABORT`, per the
vocabulary), and the START-INDEX discipline that already handled an
uncatchable crash now handles a stall the same way — it costs **one
probe**, never the lane's whole remaining budget.

`STATIC8_STARTUP_S = 60.0`, `STATIC8_STALL_S = 15.0`. Both are **chosen,
not measured** — no java, kotlin, swift, dart or csharp toolchain exists
in this sandbox to time a cold start against — but both sit at a wide,
stated margin over every number this line has actually recorded: STALL is
roughly 1,400x the 5.4 ms/probe the one anomalous cpp chunk (chunk 4, run
10.88s / 2,000 probes) showed, and STARTUP is well past any JVM/.NET cold
start this project's own logs have measured. **Verified working, not just
written**: a standalone harness reproducing `run_binary` exactly, run
against a hand-compiled binary where probe 3 of 5 calls `sleep(999)`,
recovers in 2.00s (test STALL=2s) with `p2|-|ABORT:stalled>2s` recorded
and probes 4–5 completing normally — see §4.

**b. cpp's chunk cap, raised from 2,000 to 8,000, and MEASURED.** g++
compiling this lane's own dispatch shape (a flat function-pointer table,
no method-size limit — that limit is java/kotlin/csharp's, not cpp's) was
timed at six sizes on the host toolchain (g++ 11.4, not the container's
15.2, but the question is the shape of the curve, not the exact
container number):

| probes/file | compile wall |
|---|---|
| 500 | 0.35 s |
| 1,000 | 0.45 s |
| 2,000 | 0.69 s |
| 4,000 | 1.24 s |
| 8,000 | 2.37 s |
| 16,000 | 4.78 s |
| 32,000 | 9.75 s |

Near-linear throughout — the per-probe cost actually **falls** as the file
grows (0.70 ms/probe at 500, 0.30 ms/probe at 32,000), because g++'s own
fixed start-up cost is what's being amortised. No knee, no blow-up,
anywhere in this range. 8,000 was chosen over something more aggressive
as a conservative middle: it cuts cpp's file count from 49 to 13 (a 4x
reduction in g++ invocations, each carrying its own fixed start-up) while
sitting 4x under the largest size actually timed.

**The other six STATIC8 languages' chunk caps are UNCHANGED.** No
toolchain for java, kotlin, swift, dart, csharp or typescript exists in
this sandbox, and `l3_exec.CHUNK`'s own comment names two real,
language-specific risks that make guessing dangerous rather than merely
lazy: **swift's type checker is superlinear in file size**, and **java /
kotlin / csharp carry a 64 KB method-size limit** that their two-level
dispatch tables are already sized against. Raising those caps without a
toolchain to measure against would be exactly the "guessing" the brief
rules out.

**What did NOT change:** the bits-based float payload, the START-INDEX
restart discipline for a genuine crash, the `[n/total]` progress line
(now with a `stall %.2fs` field added, not replaced), the outcome
vocabulary, the probe design, the X sets, the canonical form, the
probe-index rule. `handle()`'s return tuple grew by one field (`stall_s`)
to carry the new number through to `__TIMING__`; every call site was
updated to match, and `python3 -m py_compile l3_cart_gen.py
l3_cart_values.py` is clean.

---

## 3 — validation done without podman

| what | result |
|---|---|
| `python3 -m py_compile l3_cart_gen.py l3_cart_values.py` | clean |
| `sh -n` on all 8 regenerated STATIC8+php lanes | all parse |
| embedded python driver of all 7 STATIC8 lanes, extracted and `compile()`-checked | all OK |
| `table.json` decoded from each of the 7 regenerated lanes | `stall_s: 15.0`, `startup_s: 60.0` present in all 7; `chunk: 8000` for cpp, all six others unchanged from `l3_exec.CHUNK` |
| **cpp smoke lane (54 probes, 3 cells), run end to end on the host with real g++ 11.4** | `54 answers, 0 raises, 0 aborts, 0 buildfail`, matching log_062's own container-side result; `__TIMING__` line shows `stall_s=0.000` on the clean run |
| **the stall watchdog itself, run end to end** | a standalone extract of the new `run_binary`, against a 5-probe binary where probe 3 calls `sleep(999)`: recovers in 2.00s (test STALL=2s) instead of hanging, `ABORT:stalled>2s` recorded for the stuck probe, probes 4–5 complete normally afterward |
| `airlock submit --dry-run` on the 7 regenerated lanes, current batch | **REFUSED, as expected** — a lane of the same name is still queued (the stale, pre-fix copy) in `agent/drop`; this is the same-name guard working correctly, not a defect, and is why the owner's sequence removes the stale copies before resubmitting |

Not validated by execution: java, kotlin, swift, dart, csharp, typescript
end to end (no toolchain in this sandbox) — same limitation log_062
already recorded for these six. Their generated sources were re-read
after the edit and are structurally identical to before except for the
two new `table.json` fields and the shared driver's `run_binary` body.

---

## 4 — the stall-recovery proof, verbatim

```
   .. probe p2 stalled (stalled>2s); killed and restarting at probe 3
elapsed: 2.00s (would be INFINITE with the old code -- probe p2 sleeps 999s)
restarts: 1 stall_s: 2.0
  p0|i|1
  p1|i|2
  p2|-|ABORT:stalled>2s
  p3|i|4
  p4|i|5
```

This is the exact failure mode diagnosed in §1, reproduced on purpose and
recovered from. Under the pre-fix code this same binary hangs `python3`
forever at `pr.wait()`.

---

## 5 — new projections

`MS_PER_PROBE` (log_032's own measured instrument) is untouched — it is
an average-case rate, and the regression this log fixes was a worst-case
pathology that average never modeled, so the printed per-language ms/probe
projection is unchanged from log_062. What changes is the two things a
flat rate cannot show: cpp's file count, and every language's worst-case
exposure to a single stuck probe.

| lane | probes (weight) | rate used | projected wall (unchanged) | chunk files, old to new | worst case, one stall, old to new |
|---|---|---|---|---|---|
| `ct_php_l1.sh` | 37,544 | 4,003 probes/s | 0m 09s | n/a (route C) | already bounded (`PHP_STALL_S=2.0`) |
| `ct_typescript_l1.sh` | 16,238 | 0.24 ms/probe | 0m 03s | 4 → 4 | infinite → 75s |
| `ct_java_l1.sh` | 89,430 | 0.60 ms/probe | 0m 53s | 45 → 45 | infinite → 75s |
| `ct_kotlin_l1.sh` | 25,486 | 5.60 ms/probe | 2m 22s | 13 → 13 | infinite → 75s |
| `ct_cpp_l1.sh` | 96,934 | 1.63 ms/probe | 2m 38s | **49 → 13** | infinite → 75s |
| `ct_swift_l1.sh` | 10,054 | 3.02 ms/probe | 0m 30s | 26 → 26 | infinite → 75s |
| `ct_dart_l1.sh` | 46,305 | 0.72 ms/probe | 0m 33s | 16 → 16 | infinite → 75s |
| `ct_csharp_l1.sh` | 45,011 | 0.76 ms/probe | 0m 34s | 23 → 23 | infinite → 75s |

"Worst case, one stall" is `STARTUP + STALL` = 60s + 15s = 75s — the most
a single stuck probe can now cost any of the seven, against the
**unbounded** wait it could cost before. cpp's file-count cut (49 → 13)
is the only per-language throughput change beyond the shared watchdog;
the other six's chunk caps are unchanged, for the reason in §2b.

---

## decided, recorded for audit

- **The cause is a missing execution-side timeout, not a slow compiler.**
  `run_binary`'s read loop blocked unconditionally; `STALL` was read from
  config and never used; `table.json` never set `stall_s` at all. Fixed
  once, in the shared driver and the shared emitter, so all seven STATIC8
  languages get it, not just cpp.
- The fix is **verified working** against a genuine, deliberately induced
  hang (§4), and the regenerated cpp smoke lane still produces the exact
  answers log_062's container run produced (§3), so the fix does not
  change correctness.
- **cpp's chunk cap is raised from 2,000 to 8,000, measured** on the host
  g++ (near-linear to 32,000 probes/file, no blow-up found — table in
  §2b). The other six languages' chunk caps are **unchanged** — no
  toolchain to measure them against, and `l3_exec.CHUNK`'s own comment
  names real per-language risks (swift's superlinear checker, the 64 KB
  method limit) that make guessing them dangerous.
- Every correctness property named in the brief is preserved unedited:
  BITS floats, START-INDEX restart, `[n/total]` progress (now with a
  stall field), the outcome vocabulary, the probe design, the X sets, the
  canonical form, the probe-index rule.
- **Weights are unchanged.** Chunk size and the stall budget are
  mechanical/performance concerns; they do not change which cells are
  accepted or how many probes a cell contributes. `ct_cpp_l1.sh` is still
  96,934, every other lane is still its log_062 number.
- Did not run any lane, did not start or stop podman or any container,
  did not touch `agent/drop` while `ct_cpp_l1.sh` was recorded as
  `state=running` in `agent/status`.
- `airlock submit --dry-run` on the regenerated lanes correctly REFUSED
  while the stale pre-fix copies still sit in `agent/drop` under the same
  names — that is the same-name guard working as designed, not a defect,
  and is why the sequence below removes them first.
- Regenerated lane sources: `Research/kind_fuzz_clustering/lanes/ct_{cpp,
  java,kotlin,swift,dart,csharp,typescript,php}_l1.sh`, and a fresh
  informational manifest `lanes/batch_fixed-static8-log063.json` (8
  lanes, weight 367,002) written by `l3_cart_gen.py`'s own `--manifest`
  flag — separate from, and not a substitute for, the `agent/batch.json`
  Airlock's own `batch.sh`/`airlock submit` maintain.

## awaiting the owner

1. **Stop the frozen container, replace the seven lane files, restart,
   and resubmit the whole batch under a fresh label.** One sequence,
   given in the chat message this log is attached to. `SCRIPT_TIMEOUT`
   (3600s) should have already stopped `ct_cpp_l1.sh` on its own and
   rendered it `ABORT` — it has not, roughly 2,800s past that ceiling as
   of this writing, which means the daemon is not currently enforcing it
   in this session and a manual `down.sh` is genuinely required, not
   optional.
2. **What actually hung inside cpp's chunk 5 is not identified.** The
   fix bounds the cost of not knowing (75s worst case instead of
   infinite) rather than requiring the answer. If it recurs after this
   fix, the `ABORT:stalled>Ns` line it now produces names the exact probe
   id, which is the starting point log_062 didn't have.
3. **The six unmeasured chunk caps** (java, kotlin, swift, dart, csharp,
   typescript) are a candidate for the same treatment cpp just got, once
   a toolchain exists in this sandbox to measure them against rather than
   guess.
