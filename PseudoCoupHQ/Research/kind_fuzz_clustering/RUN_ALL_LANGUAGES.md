# RUN_ALL_LANGUAGES — the cartesian probe run, without an agent

Written 2026-08-22 (log_062). This is for **the owner alone**, at a terminal,
with no agent session open. Every path below is absolute. Nothing here
folds anything, scores anything or rules anything — it runs probes and
leaves raw lane output on disk.

Vocabulary: the outcome where the operating system stops a lane is
**ABORT**.

---

## 0 — what is already waiting

| lane | who queued it | state |
|---|---|---|
| `ct_go_l1.sh` | log_061 | queued in `<WORKSPACE_DIR>/Airlock/agent/drop/`, never ran |
| `ct_python_l1.sh` | log_061 | queued, never ran |
| `kfz_pygo_ping.sh` | log_061 | queued, never ran |

`<WORKSPACE_DIR>/Airlock/agent/batch.json` already carries the
batch **`pygo-emitters-log061`**. Everything below **joins that batch**
rather than replacing it, so the three lanes above keep their
denominator. Do not pass `--new-batch` unless you mean to throw that
manifest away.

---

## 1 — restart the container (only you can do this)

Nothing has ever run in the Airlock tree: the daemon that is up is not
bound to these folders. `daemon/watcher.py` sweeps the drop folder
**once, at startup**, and is inotify-driven after that, so a restart is
what picks the queue up.

```
bash <WORKSPACE_DIR>/Airlock/down.sh && bash <WORKSPACE_DIR>/Airlock/up.sh
```

While it is down, one unrelated fault is worth clearing — the proxy
default-denies everything because there is no allowlist file:

```
cp <WORKSPACE_DIR>/Airlock/proxy/allowlist.txt.example <WORKSPACE_DIR>/Airlock/proxy/allowlist.txt
```

**None of these lanes needs the network.** Nothing downloads, nothing
resolves a hostname; `GOPROXY=off` and `GOTOOLCHAIN=local` are set in
go's lane and the other lanes fetch nothing at all. The allowlist is
housekeeping, not a prerequisite.

Then check the sandbox is healthy:

```
python3 <WORKSPACE_DIR>/Airlock/airlock doctor
bash <WORKSPACE_DIR>/Airlock/selftest.sh
```

---

## 2 — the one command

```
bash <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/run_all_languages.sh
```

That script submits all eight level-1 lanes, waits for them, generates
the level-2 lanes from what level 1 measured, submits those, and waits
for them. It never starts or stops podman and never runs a probe
itself. It prints what it is doing and stops on the first refusal.

Leave it running in a terminal. If you would rather drive it by hand,
section 4 is the same thing, one command per line.

---

## 3 — how to watch it

```
python3 <WORKSPACE_DIR>/Airlock/airlock status
python3 <WORKSPACE_DIR>/Airlock/airlock watch
bash <WORKSPACE_DIR>/Airlock/progress.sh -w
```

`airlock status` shows the batch summary, the queue, the running lane
with its latest progress line, and the most recent finished lanes.
`progress.sh` is the only view that lists live processes inside
`sandbox-runner`.

**Every lane prints a `[n/total]` progress line.** The compiled lanes
print one per chunk; the php lane prints one every 15 seconds off its
worker part files. If `progress.sh` says "no progress line in its log
yet" for more than a couple of minutes on a compiled lane, that lane is
inside a single long compile — kotlin's is the slow one.

---

## 4 — the same run, by hand

### 4a — phase 1, every level-1 lane

Run these **in this order**. Each is one line.

```
python3 <WORKSPACE_DIR>/Airlock/airlock submit <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/ct_php_l1.sh        --batch pygo-emitters-log061 --weight 37544
python3 <WORKSPACE_DIR>/Airlock/airlock submit <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/ct_typescript_l1.sh --batch pygo-emitters-log061 --weight 16238
python3 <WORKSPACE_DIR>/Airlock/airlock submit <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/ct_java_l1.sh       --batch pygo-emitters-log061 --weight 89430
python3 <WORKSPACE_DIR>/Airlock/airlock submit <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/ct_kotlin_l1.sh     --batch pygo-emitters-log061 --weight 25486
python3 <WORKSPACE_DIR>/Airlock/airlock submit <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/ct_cpp_l1.sh        --batch pygo-emitters-log061 --weight 96934
python3 <WORKSPACE_DIR>/Airlock/airlock submit <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/ct_swift_l1.sh      --batch pygo-emitters-log061 --weight 10054
python3 <WORKSPACE_DIR>/Airlock/airlock submit <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/ct_dart_l1.sh       --batch pygo-emitters-log061 --weight 46305
python3 <WORKSPACE_DIR>/Airlock/airlock submit <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/ct_csharp_l1.sh     --batch pygo-emitters-log061 --weight 45011
```

Wait until `airlock status` shows all eight `done`. The daemon runs
lanes **serially**, one at a time, so this is one queue and not eight.

### 4b — phase 2, generate the level-2 lanes

**This step needs phase 1's output and cannot be done earlier.** A
level-2 cell exists only where `op(y, y)` typechecks, and `y`'s type is
read out of the level-1 lane output — the same rule rust has followed
since log_052 and go since log_061. Until `ct_<lang>_l1.txt` exists in
`<WORKSPACE_DIR>/Airlock/agent/out/`, the generator refuses to
emit that language's level-2 lane and says so by name.

```
cd <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering
python3 <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/l3_cart_gen.py --eight l2 --no-drop
```

It prints, per language, the cell count, the probe count, the projected
wall clock and **how many shards it cut the family into**. Shard counts
are derived from the projection, not chosen by hand: anything past
40 minutes is cut until no single lane projects past it.

### 4c — phase 2, submit them

The generator prints the exact file names. Submit each one the same
way, using the probe count it printed as `--weight`:

```
python3 <WORKSPACE_DIR>/Airlock/airlock submit <WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/<lane>.sh --batch pygo-emitters-log061 --weight <probe count>
```

`ct_php_l2.sh` is already generated and can go in this phase too
(weight **1448096**). It is deliberately **not** submitted with phase 1,
so that every level-1 lane finishes before any level-2 lane starts.

---

## 5 — expected wall clock

Level-1 numbers are projections from **log_032's measured
milliseconds-per-probe**, taken from smoke lanes inside this same
container image; rust appears in both that instrument and log_052's
cartesian run and the two agree, which is what makes the table usable.
php is projected at log_052's measured interpreted rate (4,003
probes/s), because it is route C like ruby.

| lane | probes | rate used | projected wall |
|---|---|---|---|
| `ct_php_l1.sh` | 37,544 | 4,003 probes/s | 0m 09s |
| `ct_typescript_l1.sh` | 16,238 | 0.24 ms/probe | 0m 03s |
| `ct_java_l1.sh` | 89,430 | 0.60 ms/probe | 0m 53s |
| `ct_kotlin_l1.sh` | 25,486 | 5.60 ms/probe | 2m 22s |
| `ct_cpp_l1.sh` | 96,934 | 1.63 ms/probe | 2m 38s |
| `ct_swift_l1.sh` | 10,054 | 3.02 ms/probe | 0m 30s |
| `ct_dart_l1.sh` | 46,305 | 0.72 ms/probe | 0m 33s |
| `ct_csharp_l1.sh` | 45,011 | 0.76 ms/probe | 0m 34s |
| **phase 1 total** | **367,002** | | **about 8 minutes** |

Level 2, as an **upper bound** — the real cell set is whatever survives
the type rule in 4b, so these can only come down:

| family | probes (upper bound) | projected wall (upper bound) | shards (upper bound) |
|---|---|---|---|
| php | 1,448,096 | 6m 01s | 1 |
| typescript | 584,976 | 2m 20s | 1 |
| java | 2,020,148 | 20m 12s | 1 |
| kotlin | 650,541 | 60m 43s | 2 |
| c++ | 2,686,491 | 72m 58s | 2 |
| swift | 316,340 | 15m 55s | 1 |
| dart | 1,678,096 | 20m 08s | 1 |
| c# | 1,023,776 | 12m 58s | 1 |
| **phase 2 total** | **10,408,464** | **under 3 hours** | |

So the whole thing is **around three hours of compute**, comfortably
inside a fifteen-hour window, and every individual lane is inside the
daemon's 3,600-second per-lane ceiling.

---

## 6 — what to do if a lane ABORTs

`airlock status` renders **ABORT** when the operating system stopped a
lane on the wall-clock ceiling (`SCRIPT_TIMEOUT`, default 3,600 s). The
daemon's own raw token stays in the status file and is named alongside
it.

**First, nothing is lost.** Every lane writes its answers to `/out` as
they arrive, so an ABORTed lane still leaves everything it measured in
`<WORKSPACE_DIR>/Airlock/agent/out/`. The php lane additionally
writes one part file per worker (`ct_php_l2.w0.txt` …) as answers
arrive.

| symptom | what it means | what to do |
|---|---|---|
| a lane ABORTs at almost exactly 3,600 s | it ran past the ceiling | re-emit that family with more shards: `python3 …/l3_cart_gen.py --eight l2 --no-drop` after raising `SHARD_TARGET_S` in `l3_cart_gen.py` (it is 2400.0), or submit the family one shard at a time |
| a lane exits **4** in the first seconds, printing `REFUSING TO START: <tool> is not runnable` | that language's toolchain is not reachable inside the container | the lane names the exact path it tried and where that toolchain lives. Four of them (kotlin, swift, dart, c#) live in the `sandbox-persist` podman volume at `/persist`, not in the image — if `/persist` is empty, the volume was removed and the toolchain has to be reinstalled before that language can run. **Skip that lane and run the rest**; the languages are independent |
| a lane exits **3**, printing `only N MB free on /work` | `/work` is a 4 GB tmpfs and something did not sweep | restart the container (step 1); every lane sweeps its own root at the end |
| a compiled lane prints `chunk of N refused; the compiler named M probe(s)` | normal. The compiler refused specific probes (swift's constant folder refuses an overflow its type checker accepted) | nothing. Those probes are recorded `BUILDFAIL`, which folds to **REFUSE**, and the rest of the chunk runs |
| a compiled lane prints `bisecting` | the compiler refused and named no line | nothing. It costs `log2(chunk)` rebuilds and still lands on the single probe |
| many `ABORT:rc…` lines inside one lane's output | probes that stopped the process uncatchably (a c++ `SIGFPE`, a swift trap) | nothing. The START-INDEX discipline means each one cost **one probe**, not a chunk |
| the queue does not move at all and `agent/status/` stays empty | the daemon is not bound to these folders | step 1 again — down, then up |

An ABORTed or skipped lane does **not** invalidate the others. Each
language is a separate column and a partial run is still a whole set of
columns.

---

## 7 — where everything is

| what | where |
|---|---|
| the emitters | `<WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/l3_cart_gen.py` |
| the value sets and holders | `<WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/l3_cart_values.py` |
| the generated lanes | `<WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/ct_*.sh` |
| the batch manifests written at generation time | `<WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/lanes/batch_eight-l1-log062.json`, `…/batch_eight-l2-php-log062.json` |
| the live manifest Airlock reads | `<WORKSPACE_DIR>/Airlock/agent/batch.json` |
| queued lanes | `<WORKSPACE_DIR>/Airlock/agent/drop/` |
| statuses | `<WORKSPACE_DIR>/Airlock/agent/status/` |
| logs | `<WORKSPACE_DIR>/Airlock/agent/logs/` |
| **raw lane output** | `<WORKSPACE_DIR>/Airlock/agent/out/ct_<lang>_l<n>*.txt` |
| the record of this work | `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_062_remaining_language_emitters.md` |

The two `batch_*.json` files beside the lanes are a **record of what was
generated**, in Airlock's own manifest byte-shape. The manifest Airlock
actually reads is the one `airlock submit` maintains at
`<WORKSPACE_DIR>/Airlock/agent/batch.json`; you do not need to
copy anything.

---

## 8 — after the run

Nothing here folds. The raw answers sit in
`<WORKSPACE_DIR>/Airlock/agent/out/` in the same line shape rust
and go already use (`pid|type|ENCODING`), which is what
`l3_cart_read.read_rust` reads. Whether and how these eight columns join
`matrices_cart_v2/`, the compatibility gate, containment and the mode
partition is **structural and is yours to rule** — log_062 section
"awaiting the owner" says so and does not decide it.
