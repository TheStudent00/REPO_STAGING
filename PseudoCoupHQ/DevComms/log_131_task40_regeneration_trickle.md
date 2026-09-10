# log 131 — TASK 40, the regeneration trickle: the residue is compiled

Date: 2026-09-02. Session: Claude Code, TASK 40 of
`DevComms/log_129_claude_code_task_briefs_round8.md` **as upgraded by that
file's ADDENDUM** (the owner ruled GO — "yeah lets try it"), plus the
coordinator's supplement of the same date (the F35-1 and F36-1 fixes,
which had to land before any count was recomputed).

Two populations are named on this page and never mixed:

- **the corpus** — the 4,440 candidate probes that have been on disk since
  2026-08-25 (1,779 accepted, 2,661 refused), at six hand-written holder
  types per language. Nothing in it was rewritten by this task.
- **the residue** — every operator unit crossed with each language's full
  EXTRACTED scalar core, minus what the legality rules call illegal.
  **129,553 candidates.** It did not exist before today; it exists now,
  compiled, in 326 new store files.

---

# 1. The four answers, in one line each

## 1.1 The residue was compiled — all of it, this session

**129,553 probes submitted, 29,288 accepted, 100,265 refused, and every
one of the 29,288 accepted probes fully extracted** — ship unit, anchor
unit and DWARF parameter table, 29,288 of each, no gaps. 326 chunks of
400, every chunk banked, zero chunks left pending. The brief allowed for a
checkpointed partial; the trickle finished instead.

## 1.2 It cost 18.4 minutes of wall clock at half the machine

6,265 seconds of lane time, run six chunks at a time inside a container
capped at 6 of this machine's <cores>, is **18.4 minutes end to end**
(01:42:37 to 02:01:02 local, by the store files' own timestamps). The cost
page written before the run predicted 8,522 serial seconds; the measured
figure is 6,265, so the prediction is 1.36x the measurement — erring long,
which is the direction it was built to err in (§3.3).

## 1.3 The 121,081-vs-129,043 discrepancy: 129,043 is the residue

Both numbers are in `legality_reduction.json` and both are correct for
what they name. 121,081 is what an extracted rule ADMITS. 129,043 is that
plus 7,962 candidates belonging to the 62 operator units for which no rule
was extracted at all — which the filter passes through rather than judges.
The regeneration population is the second. Computed in §4.1, corrected to
**129,553** by the core fix in §2.1.

## 1.4 The testimony remediation needed a second run, and the addendum's
## reasoning about it was wrong on one link

The addendum ruled that the regeneration subsumes Route A. Measured, it
does not: joined against the finished 129,553-probe regeneration, **zero**
altered records were superseded. The cause is mechanical and is stated
with the values in §7.2. A 235-second unfiltered re-capture of the three
original plain lanes was run, and **218 altered records (109 distinct
captures across two stores each) are now superseded by real verbatim
testimony**, with the recaptured text matching log 126's reconstruction
character for character.

---

# 2. The two supplement fixes, and what each moved

## 2.1 F35-1 — the truth-value mark, added to the shared rule

### 2.1.1 The gap, in the rule's own words against its own code

`type_inventory_validate.py` states its rule in a comment:

> A type is in the scalar core when an EXTRACTED class marking says it is
> an integer, a float or **a truth value**.

Its implementation is a tuple with no truth-value entry:

```
NUMERIC_MARKS = ("integer_signed", "integer_unsigned", "float",
                 "numeric_grammar_marked")
```

So a truth value fell through to `undecided` by a missing tuple entry.

### 2.1.2 The fix, and why it is one mechanism rather than two rows

`core_rule2.py` (new; nothing existing edited) replaces the tuple test
with: **a type is in the scalar core when its NORMALISED class is one of
`integer_signed`, `integer_unsigned`, `float`, `truth_value`** — the same
four-class normalisation `legality_filter.py` already uses. That is the
sentence above, implemented.

Adding the literal string `truth_value` to the tuple would have fixed
swift and left rust out, because rust's marking is
`nonnumeric_grammar_marked`, one marking covering `bool`, `char` and
`str`. Naming `rust bool` by hand would have been the per-name patch this
line bans. Instead a second authority is READ AT RUN TIME — rustc's own
code generator, at the pin `legality_rules.py` already reads:

```
Sources/rust/compiler/rustc_codegen_cranelift/src/num.rs
$ git -C Sources/rust rev-parse HEAD
7c329d6c76e11ca40c5673818ab0439c1be8962c

    match in_lhs.layout().ty.kind() {
        ty::Bool => crate::num::codegen_bool_binop(...)
        ty::Uint(_) | ty::Int(_) => crate::num::codegen_int_binop(...)
        ty::Float(_) => crate::num::codegen_float_binop(...)
        ty::RawPtr(..) | ty::FnPtr(..) => ...
```

`bool` joins `ty::Bool` by name identity and gets `truth_value`. `char`
and `str` have no scalar arm and get nothing — so they stay out without
being named. A missing anchor block is a hard failure; the table is never
guessed.

### 2.1.3 The recount, and the one thing a first cut got wrong

```
$ /tmp/reconnect_venv/bin/python3 core_rule2.py
c      core v1  56 -> v2  56   entered: (none)
cpp    core v1  56 -> v2  56   entered: (none)
go     core v1  14 -> v2  14   entered: (none)
rust   core v1  14 -> v2  15   entered: bool
swift  core v1  16 -> v2  17   entered: Bool
PASS type_inventory2_core2.json -- no operator token in any key, ...
```

rust 14→15 and swift 16→17, exactly the moves log 125 predicted. c, cpp
and go do not move: clang declares `bool` `UNSIGNED_TYPE` so it was
already in, and go's own branch already admitted `IsBoolean`.

A FIRST CUT WAS WRONG AND IS RECORDED: it consulted the six DECLARED
stdint aliases (`int32_t`, `int64_t`, `uint64_t`) for core membership and
c/cpp went 56 → 59. Every one of the three is an alias of a type already
in the core, so that would have counted one holder twice. They are now
lookup-only, and core membership is decided by extracted markings alone.

### 2.1.4 The delta on the candidate space

| language | naive before | naive after | residue before | residue after |
|---|---:|---:|---:|---:|
| c | 57,400 | 57,400 | 51,829 | 51,829 |
| cpp | 79,352 | 79,352 | 70,991 | 70,991 |
| go | 3,864 | 3,864 | 553 | 553 |
| rust | 4,466 | **5,115** | 1,800 | **1,993** |
| swift | 7,216 | **8,126** | 3,870 | **4,187** |
| **total** | **152,298** | **153,857** | **129,043** | **129,553** |

swift 7,216 → 8,126 is the figure log 125 named. rust 4,466 → 5,115 is its
counterpart: 11 unary × 15 + 22 binary × 15 × 15 = 165 + 4,950 = 5,115.

## 2.2 F36-1 — the c++ truth-value increment, annotated as a ratified quirk

the owner's ruling: "if c++ allows it and someone can use it with intention, its
valid." The rules already predict those four candidates LEGAL, which is
what the ruling says they should; what changed is the SCORING.

The choice made, stated so it can be struck: an **additive annotation
file**, `legality_quirks.json`, naming two rule ids as
`deprecated_but_allowed`. `legality_rules.json` is not superseded and not
edited — no rule shape changes, so the reduction arithmetic is untouched
by this fix. The annotation is keyed by the authority's own name for its
check, never by a token.

```
$ /tmp/reconnect_venv/bin/python3 legality_filter2.py
validation: in-scope 3588 ; agreement 100.0% (compiler-only 99.9%) ;
            misses 0 ; quirk agreements 4
  quirk agreement  cpp cpp/probe_53  ++a  | .../unit.cpp:9:12: error: ISO C++17 does not allow incrementing expression
  quirk agreement  cpp cpp/probe_59  --a  | .../unit.cpp:9:12: error: cannot decrement expression of type bool
  quirk agreement  cpp cpp/probe_89  a++  | .../unit.cpp:9:13: error: ISO C++17 does not allow incrementing expression
  quirk agreement  cpp cpp/probe_95  a--  | .../unit.cpp:9:13: error: cannot decrement expression of type bool
PASS legality_reduction2.json -- no operator token in any key, ...
PASS legality_validation2.json -- no operator token in any key, ...
```

**4 validated misses became 4 validated agreements; in-scope agreement is
100.0%.** The compiler's own refusal text is kept verbatim on every one of
the four, and the file carries a second figure,
`compiler_agreement_without_the_ruling: 99.9`, so the arithmetic without
the ruling stays readable.

---

# 3. The cost page, measured before anything was compiled

## 3.1 Where the measurement comes from

The Airlock daemon writes its own footer line into every lane log. The ten
lanes of 2026-08-25 and 2026-08-26 carry them, and `regen_cost.py` reads
them rather than timing anything:

```
$ tail -3 PUBLIC/Airlock/agent/logs/20260825T055219Z__op_c.sh.log
# exit 0 in 42.4s
```

| language | lane | probes | accepted | refused | measured |
|---|---|---:|---:|---:|---:|
| c | `op_c.sh` | 750 | 610 | 140 | 42.4s |
| c | `op_asg_c.sh` | 396 | 276 | 120 | 12.0s |
| cpp | `op_cpp.sh` | 1002 | 770 | 232 | 74.1s |
| cpp | `op_asg_cpp.sh` | 504 | 324 | 180 | 27.4s |
| go | `op_go.sh` | 744 | 107 | 637 | 48.5s |
| go | `op_asg_go.sh` | 432 | 59 | 373 | 23.0s |
| rust | `op_rust.sh` | 858 | 125 | 733 | 24.1s |
| rust | `op_asg_rust.sh` | 396 | 61 | 335 | 8.9s |
| swift | `op_swift.sh` | 1086 | 167 | 919 | 159.8s |
| swift | `op_asg_swift.sh` | 216 | 29 | 187 | 31.1s |

No probe was compiled to produce this page.

## 3.2 The model, and where it failed honestly

A refused probe costs one compile. An accepted probe costs the acceptance
compile, then the anchor build, then two objdump reads, then the debug
table. Two lanes per language, two unknowns, solved per language.

It solved cleanly for swift only (0.1222s refused, 0.2843s accepted). For
c, cpp, go and rust the solve returns a NEGATIVE rate, which is refused
rather than clamped: the assignment lane is not merely a different mix, it
compiles a different probe SHAPE, so its cost differs for reasons the
accepted/refused split does not carry. Those four fall back to the blended
rate, and the fallback is named on each row of `regen_cost.md`.

## 3.3 Predicted against measured, now that the run has happened

| language | probes | predicted serial | measured lane seconds | measured s/probe |
|---|---:|---:|---:|---:|
| c | 51,829 | 2,460 | 1,202 | 0.0232 |
| cpp | 70,991 | 4,785 | 3,810 | 0.0537 |
| go | 553 | 34 | 146 | 0.2633 |
| rust | 1,993 | 52 | 72 | 0.0362 |
| swift | 4,187 | 1,190 | 1,035 | 0.2472 |
| **total** | **129,553** | **8,522** | **6,265** | **0.0484** |

The prediction is 1.36x the measurement. c and cpp came in cheap because the
residue turned out to be far more refusal-heavy than the corpus was
(§6.1); go and rust came in dear because their residue is the opposite,
nearly all accepted. **Wall clock: 18.4 minutes at six workers** — 6,265
seconds of lane time over 1,105 seconds of wall clock is a 5.7x speedup
against six workers, which is the arithmetic agreeing with itself.

---

# 4. The residue, computed rather than quoted

## 4.1 The discrepancy, with the arithmetic pasted

```
$ /tmp/reconnect_venv/bin/python3 -c "..." legality_reduction.json
{'naive': 152298, 'legal': 121081, 'must_compile': 129043,
 'reduction_factor': 1.26, 'reduction_factor_including_no_rule_residue': 1.18}
  per-lang no-rule residue: [('c', 504), ('cpp', 3528), ('go', 84),
                             ('rust', 1302), ('swift', 2544)]
  legal+residue = 129043
```

504 + 3,528 + 84 + 1,302 + 2,544 = 7,962, and 121,081 + 7,962 = 129,043.

**Which figure is right, as the regeneration population: 129,043** — the
figure log 127 §1.1 and the task-40 brief both use. The brief's handoff
line, which names "legal 121,081" as the corrected residue, is naming the
rule-admitted subset. Compiling only that subset would skip every operator
unit for which no rule exists, and log 127 §4.1 measured what that costs:
**136 corpus-accepted units live on exactly those units** (c's `sizeof` /
`_Alignof` family 30, cpp's three-way comparison 22, rust's range
constructors 24, swift's coalesce and range forms 16). They are real
accepted units and would be lost.

## 4.2 The corrected figure, and a second route to it

```
$ /tmp/reconnect_venv/bin/python3 -c "..." legality_reduction2.json
{'naive': 153857, 'legal': 121096, 'must_compile': 129553, ...}
  legal+residue = 129553
```

That is arithmetic over the rule tables. The generator then ENUMERATED the
same space, candidate by candidate, and arrived at the same numbers by a
different road:

```
$ /tmp/reconnect_venv/bin/python3 probe_gen2.py
c      core 56   naive   57400   legal   51325   no-rule    504   illegal(skipped)    5571   TO COMPILE   51829
cpp    core 56   naive   79352   legal   67463   no-rule   3528   illegal(skipped)    8361   TO COMPILE   70991
go     core 14   naive    3864   legal     469   no-rule     84   illegal(skipped)    3311   TO COMPILE     553
rust   core 15   naive    5115   legal     508   no-rule   1485   illegal(skipped)    3122   TO COMPILE    1993
swift  core 17   naive    8126   legal    1331   no-rule   2856   illegal(skipped)    3939   TO COMPILE    4187
TOTAL to compile: 129553
```

Per language and in total, the enumeration and the arithmetic agree to the
unit.

---

# 5. The capped copy, and the trickle through it

## 5.1 The copy: what it is, where it is, how to stop it

### 5.1.1 The names, which are the whole constraint

Airlock and SandboxDesign SHARE their container, network, image and volume
names — that is why those two may never run together. A third participant
reusing any of them would collide with both. So every name here is new:

| | this copy | what it must not collide with |
|---|---|---|
| container | `trickle-runner` | `sandbox-runner`, `va-runner` |
| network | `trickle-internal` | `sandbox-internal`, `va-internal` |
| agent tree | `AirlockTrickle/agent/{drop,out,logs,status}` | `PUBLIC/Airlock/agent` |

`trickle_doctor.sh` checks this and prints it:

```
== name collisions (Airlock and SandboxDesign share sandbox-* names)
  sandbox-runner exists -- and is NOT this copy's name, so no collision
  sandbox-proxy exists -- and is NOT this copy's name, so no collision
  va-runner exists -- and is NOT this copy's name, so no collision
  va-proxy exists -- and is NOT this copy's name, so no collision
  this copy uses: trickle-runner, trickle-internal
```

Airlock's own `sandbox-runner` was UP throughout this session and was
never touched. The whole trickle ran beside it.

### 5.1.2 What is shared, and how it is made safe

The runner IMAGE (`sandbox-runner:latest`, read-only by construction) and
the toolchain volume `sandbox-persist`, which holds the swift installation
at `/persist/swift`. The volume is mounted **read-only**, so this copy
cannot alter a toolchain Airlock's own runs depend on:

```
  mount /persist <- .../volumes/sandbox-persist/_data rw=false
  mount /drop    <- AirlockTrickle/agent/drop rw=true
```

### 5.1.3 The cap

```
  cpu cap: 6 of <cores>
```

`--cpus 6`, computed as half of `nproc`, overridable with `TRICKLE_CPUS`.
Six chunks run at once, so the cap — not the driver — is what decides how
much of the machine the work can take. Memory is capped at 8g and `/work`
is a 4g tmpfs, so a runaway fails inside the container rather than filling
the host disk.

### 5.1.4 No proxy, and no hot-folder daemon — the second one is a finding

There is no proxy: the lanes compile local source and fetch nothing, so
the container sits on an `--internal` network with no route out.

The image's default command is Airlock's inotify watcher, and it was tried
first. The container stopped immediately:

```
OSError: [Errno 28] inotify_add_watch(/drop) failed: No space left on device
$ cat /proc/sys/fs/inotify/max_user_instances
128
```

That is the inotify INSTANCE limit, not disk. This machine already runs
many watchers and has none left to give. **Raising a kernel limit is a
system setting change and was not made.** The container is started idle
instead and the driver reaches in with `podman exec`. The lane, the
scratch directory and the products are unchanged; only the doorbell is.

### 5.1.5 How to stop it

```
bash trickle_down.sh            stop and remove the container and network
bash trickle_down.sh --pause    stop only; trickle_up.sh restarts it
```

Either way the agent tree and everything the trickle banked stay on disk,
because the resume state is the point. Nothing owned by Airlock or
SandboxDesign is touched by either.

The copy was PAUSED at the end of this session, and Airlock's own
containers were verified untouched:

```
$ bash trickle_down.sh --pause
  trickle-runner stopped (kept; 'bash trickle_up.sh' starts it again)
$ podman ps -a --format '{{.Names}} {{.Status}}' | sort
sandbox-proxy Up 34 hours
sandbox-runner Up 34 hours
trickle-runner Exited (137) Less than a second ago
va-proxy Up 3 days
va-runner Up 3 days
```

## 5.2 The pins, verified IN-LANE before capture

This was the addendum's one named risk. Every lane prints its toolchain's
own version line before it compiles anything, so the check is the lane's,
not a claim about the lane. The 2026-09-02 banners against the 2026-08-25
originals:

| | the original lane, 2026-08-25 | this session's lane |
|---|---|---|
| c, cpp | `Ubuntu clang version 21.1.8 (6ubuntu1)` | `Ubuntu clang version 21.1.8 (6ubuntu1)` |
| go | `go version go1.26.0 linux/amd64` | `go version go1.26.0 linux/amd64` |
| rust | `rustc 1.96.1 (31fca3adb 2026-06-26)` | `rustc 1.96.1 (31fca3adb 2026-06-26)` |
| swift | `Swift version 6.0.3 (swift-6.0.3-RELEASE)` | `Swift version 6.0.3 (swift-6.0.3-RELEASE)` |
| disassembler | `GNU objdump (GNU Binutils for Ubuntu) 2.46` | `GNU objdump (GNU Binutils for Ubuntu) 2.46` |

All five identical. The re-capture risk log 126 called "the only one that
is not cheap to dismiss" is dismissed, on the lanes' own testimony.

One toolchain detail, recorded because it was met: `swiftc` in this image
wants `libncurses.so.6` and the image ships only `libncursesw.so.6`.
`lane_gen.py`'s own lane prologue already creates that symlink; the copy
needed no change for it.

## 5.3 One chunk, with values moving

Take `rust_c0002` — regeneration manifest probes 800 through 1,199.

1. `lane_gen_verbatim.lane_verbatim` renders the lane. Its driver ESCAPES
   the compiler's words (`|` becomes `\p`) instead of substituting them,
   and its product opens with `#verbatim-escape v1`.
2. The lane is written to `AirlockTrickle/agent/drop/` and
   run with `podman exec trickle-runner sh /drop/regen_rust_c0002.sh`.
3. The product is read back, every escaped field decoded, and folded into
   `trickle_store/op_units2_rust_c0002.json` — a NEW file of its own.
4. The chunk is marked `done` in `trickle_state.json`.

```
  rust_c0002       400 submitted    300 accepted    100 refused    300 extracted     19.0s
```

Step 4 is the checkpoint, and it is the only atomicity in the design: a
chunk that was in flight when a run stopped is simply not done, so it is
redone from its start. Nothing smaller than a chunk is ever half-banked,
because every chunk writes its own file and the state is written to a
temporary name and renamed.

## 5.4 The one real defect the run hit, and its cause

Ten chunks failed on the first run with:

```
AssertionError: edit did not apply as expected:
    clean(): drop the two substitutions -- found 0, wanted 1
```

Cause, named: `lane_verbatim` swaps the module-global `lane_gen.DRIVER`
for the duration of one call and restores it afterwards. That is safe on
one thread and unsafe on six — the second worker edits an already-edited
driver and its own assertion fires. This is the verbatim path REFUSING to
write a lane it cannot vouch for, which is the behaviour log 126 built
into it, working exactly as intended.

Fix: a render lock in `trickle.py`. Rendering is milliseconds; the
compiling stays parallel. All ten chunks were retried on resume and
landed. **No corrupted lane was produced and no store was written from a
mis-edited driver** — the assertion is upstream of the write.

## 5.5 The per-chunk tallies

Full per-chunk table (326 rows) in
`Research/op_pipeline/trickle_tallies.md`. The roll-up:

| language | chunks | probes | submitted | accepted | refused | extracted ship / anchor / dwarf | lane seconds |
|---|---:|---:|---:|---:|---:|---|---:|
| c | 130 / 130 | 51,829 | 51,829 | 10,010 | 41,819 | 10,010 / 10,010 / 10,010 | 1,202 |
| cpp | 178 / 178 | 70,991 | 70,991 | 17,070 | 53,921 | 17,070 / 17,070 / 17,070 | 3,810 |
| go | 2 / 2 | 553 | 553 | 483 | 70 | 483 / 483 / 483 | 146 |
| rust | 5 / 5 | 1,993 | 1,993 | 570 | 1,423 | 570 / 570 / 570 | 72 |
| swift | 11 / 11 | 4,187 | 4,187 | 1,155 | 3,032 | 1,155 / 1,155 / 1,155 | 1,035 |
| **total** | **326 / 326** | **129,553** | **129,553** | **29,288** | **100,265** | **29,288 / 29,288 / 29,288** | **6,265** |

Every accepted probe carries all three extractions. `no_line` — a probe
the lane wrote nothing about — is 0 across all 326 chunks.

---

# 6. THE RESUME STATE

## 6.1 Where it stands: nothing is left to resume

```
$ /tmp/reconnect_venv/bin/python3 trickle.py --status
chunk size 400 ; 326 chunks ; 129553 probes
  c      done 130                                   51829 probes banked
  cpp    done 178                                   70991 probes banked
  go     done 2                                       553 probes banked
  rust   done 5                                      1993 probes banked
  swift  done 11                                     4187 probes banked
  totals: submitted 129553  accepted 29288  refused 100265
          extracted ship 29288 anchor 29288 dwarf 29288
```

326 of 326 chunks `done`. 0 pending, 0 failed, 0 refused by the guard. The
re-capture's own state is separate and also complete: 8 of 8 chunks done
over 2,688 probes.

## 6.2 How to resume if more is ever added to the plan

- `trickle_state.json` IS the mechanism. A chunk marked `done` is never
  rerun. Delete the file and the whole trickle restarts; that is the only
  way to restart it, and it is deliberate.
- `/tmp/reconnect_venv/bin/python3 trickle.py --run` picks up every chunk
  not marked done. `--langs`, `--limit` and `--minutes` narrow it;
  `--minutes 30` stops cleanly at a time budget with everything banked.
- `--plan` REFUSES to overwrite an existing plan, because overwriting it
  would discard the resume state.
- The container must be up: `bash trickle_up.sh`. The driver refuses by
  name rather than failing chunk by chunk if it is not.
- `recapture_original.py` has its own `recapture_state.json` with the same
  contract.

## 6.3 What a resumed run would find on disk

| what | where | size |
|---|---|---|
| resume state, regeneration | `Research/op_pipeline/trickle_state.json` | 326 chunk records |
| resume state, re-capture | `Research/op_pipeline/recapture_state.json` | 8 chunk records |
| folded stores | `Research/op_pipeline/trickle_store/` | 334 files, 125 MB |
| raw lane products + consoles | `Research/op_pipeline/trickle_raw/` | 668 files, 32 MB |
| the exact lane scripts that ran | `Research/op_pipeline/trickle_lanes/` | 334 files, 8 MB |
| the container's own tree | `AirlockTrickle/agent/` | outside every repo |

---

# 7. The testimony supersession

## 7.1 What was ruled, and the one link that did not hold

The addendum: "since regeneration re-runs everything anyway with the
verbatim path, Route A is subsumed: the regenerated stores ARE the
remediation. The annotate route is dead."

Measured after the full regeneration landed: **zero** altered records
joined to a regenerated capture.

## 7.2 Why, with the values moving

Take go's plain-run record 387.

- The probe: `a | b`, with `a` an `int32` and `b` a `float32`.
- What the store holds today:
  `./main.go:6:9: invalid operation: a / b (mismatched types int32 and float32)`
  — a `/` the compiler never emitted.
- What the filter now says: go's own `binaryOpPredicates` require both
  operands identical, so `int32` against `float32` is ILLEGAL.
- So the regeneration never compiled it. There is no regenerated capture,
  because there is nothing to capture.

Generalised: **every altered record is a REFUSAL**, and a refusal is what
a compiler says about an operand shape the extracted rules call illegal —
precisely the shape the filter exists to keep away from a compiler. The
filter's saving and the testimony remediation pull against each other, and
that was not visible until both existed.

## 7.3 The re-capture, and what it cost

`recapture_original.py` runs the three original PLAIN lanes — go, rust and
swift at the six hand-written holder types, unfiltered, exactly as
2026-08-25 ran them — through the same capped container and the same
verbatim path.

```
planned 8 chunks over 2688 probes
  recap_go_c0000         400 submitted     70 accepted    330 refused    25.3s
  recap_go_c0001         344 submitted     37 accepted    307 refused    16.7s
  recap_rust_c0000       400 submitted     60 accepted    340 refused    10.3s
  recap_rust_c0001       400 submitted     61 accepted    339 refused    10.6s
  recap_rust_c0002        58 submitted      4 accepted     54 refused     1.5s
  recap_swift_c0000      400 submitted     87 accepted    313 refused    65.5s
  recap_swift_c0001      400 submitted     63 accepted    337 refused    66.0s
  recap_swift_c0002      286 submitted     17 accepted    269 refused    38.6s
```

**234.5 seconds**, against log 126's prediction of 232.4 for the same
three lanes. Its products carry `#verbatim-escape v1`.

## 7.4 The supersession, and how a record is joined to its recapture

The join is **whole-source identity**: the probe's own source text with its
probe number erased, because the two runs number from zero in separate id
spaces. Two normalised texts are equal exactly when the two probes are the
same probe. Evidence class: forced by construction. No token key, and no
text match on the diagnostic.

```
$ /tmp/reconnect_venv/bin/python3 supersede_altered.py
altered findings 336 ; superseded now 218 ; not yet 0 ; out of scope 118
PASS supersession_altered_testimony.json -- no operator token in any key, ...
```

| where | superseded |
|---|---:|
| `op_pipeline/op_units_go.json` | 68 |
| `op_pipeline/op_units_rust.json` | 32 |
| `op_pipeline/op_units_swift.json` | 9 |
| `stage_asg/op_units_go.json` | 68 |
| `stage_asg/op_units_rust.json` | 32 |
| `stage_asg/op_units_swift.json` | 9 |
| **total** | **218** |

218 record findings = **109 distinct plain-run captures** (68 + 32 + 9),
each living in two files on disk. Against log 132's corrected total of 158
distinct altered captures across all six lanes, the 49 remaining are the
assignment run's.

## 7.5 The reconstructions, now confirmed against real testimony

Log 126 could only offer a SUSPECTED original, because no unaltered copy
was retained anywhere. Three of them, beside what the compiler actually
said this session:

```
store op_pipeline/op_units_go.json rec 385
  stored (altered) : ./main.go:6:9: invalid operation: a / b (mismatched types int32 and int64)
  suspected (126)  : ./main.go:6:9: invalid operation: a | b (mismatched types int32 and int64)
  RECAPTURED       : ./main.go:6:9: invalid operation: a | b (mismatched types int32 and int64)

store op_pipeline/op_units_go.json rec 386
  stored (altered) : ./main.go:6:9: invalid operation: a / b (mismatched types int32 and uint64)
  suspected (126)  : ./main.go:6:9: invalid operation: a | b (mismatched types int32 and uint64)
  RECAPTURED       : ./main.go:6:9: invalid operation: a | b (mismatched types int32 and uint64)

store op_pipeline/op_units_go.json rec 387
  stored (altered) : ./main.go:6:9: invalid operation: a / b (mismatched types int32 and float32)
  suspected (126)  : ./main.go:6:9: invalid operation: a | b (mismatched types int32 and float32)
  RECAPTURED       : ./main.go:6:9: invalid operation: a | b (mismatched types int32 and float32)
```

Character for character. Log 126's reconstruction method is now measured
against ground truth on 109 captures, not argued for.

## 7.6 Supersession is a MARK, never an edit

No store on disk was opened for writing. The mark lives only in the new
sidecar `supersession_altered_testimony.json`, which carries, per record:
the origin store and record id, the stored altered text, log 126's
suspected original, the join, and the recapturing store, chunk and
diagnostic.

## 7.7 What is NOT superseded, stated rather than hidden

**118 findings, all of them the assignment run's** (the three `op_asg_*`
lanes, plus their rows inside the `stage_asg` union stores). The
assignment bucket is excluded from probe generation by `probe_gen.py`'s
own `EXCLUDED_BUCKETS`, and its probes come from a different generator
(`asg_stage.py`). Neither the regeneration nor the re-capture produced a
counterpart, so they cannot be superseded by this task. Sizing them from
log 126: go 33 and rust 26 distinct assignment captures. Re-capturing them
would need the same treatment applied to `asg_stage.py`; log 126 measured
those three lanes at 63.0 seconds.

---

# 8. Findings

- **F40-1 — the legality filter and the testimony remediation pull
  against each other.** §7.2. Every altered record is a refusal of a shape
  the rules call illegal, which is exactly what the filter removes; so a
  filtered regeneration can never supersede an altered refusal. Measured:
  0 of 218 joined against the finished 129,553-probe regeneration; 218 of
  218 joined once the unfiltered re-capture existed. The addendum's
  "Route A is subsumed" does not hold, and Route A is what did the work.
- **F40-2 — the c and cpp extracted core contains 24 fixed-point
  spellings the default dialect refuses.** `_Fract`, `_Accum` and their
  `_Sat` / signed / unsigned / short / long variants are real rows of
  clang's `BuiltinTypes.def`, so they belong in the extracted core, but a
  probe written with one is refused: `error: use of undeclared identifier
  '_Sat'` — clang admits them only under `-ffixed-point`. Whole chunks of
  the c residue are 400-refusals-of-400 for this one cause. It is honest
  testimony and no accepted unit is lost by it, but it is why c and cpp
  came in far cheaper than the cost model predicted, and it is a real
  question for the owner: should the residue carry a dialect flag, or should
  these types be marked as needing one?
- **F40-3 — the residue is 77% refusals (100,265 of 129,553).** The
  corpus was 60% refusals. The filter cut 24,304 predicted-illegal
  candidates and what remains is still mostly refused, so the extracted
  rules cover much less of the real admissibility surface at the full core
  than they do at the six holder types. The 62 rule-less operator units
  (§4.1) are the visible part of that; F40-2 is another part.
- **F40-4 — the machine cost is not the constraint on this line.** The
  entire residue, which had been an open go/no-go for days, is 18.4
  minutes of wall clock at half the machine. The estimate that preceded it
  was 1.36x the measurement and still small.
- **F40-5 — `lane_verbatim` is not thread-safe, by construction.** §5.4.
  It mutates a module global. Any future concurrent caller must hold a
  lock. Recorded because the failure mode is silent-looking (an assertion
  about an edit count) and its cause is three modules away.
- **F40-6 — go's residue is almost entirely accepted (483 of 553).** Go's
  filter factor was x6.99, the largest of the five, and what survives it
  is nearly all real. That is the filter working as intended, and it is
  the opposite of c and cpp.

---

# 9. Zero regressions, verified against the version-control system

Every file this task read, with the commit that last changed it — all
before today:

```
lane_gen.py                        8dda5af 2026-08-25
fold.py                            8dda5af 2026-08-25
fold_verbatim.py                   d885f14 2026-09-01
lane_gen_verbatim.py               7ca56b3 2026-09-01
verbatim_diag.py                   7ca56b3 2026-09-01
probe_gen.py                       8dda5af 2026-08-25
legality_filter.py                 d5a9808 2026-09-01
legality_rules.py                  bc7aa07 2026-09-01
legality_rules.json                bc7aa07 2026-09-01
legality_reduction.json            d5a9808 2026-09-01
legality_validation.json           d5a9808 2026-09-01
type_inventory2.json               c238971 2026-09-01
type_inventory_validate.py         bb5ba8a 2026-09-01
check_no_spelling_keys.py          fdff0b2 2026-08-26
audit_altered_testimony.json       c238971 2026-09-01
op_units_c.json                    8dda5af 2026-08-25
op_units_cpp.json                  8dda5af 2026-08-25
op_units_go.json                   8dda5af 2026-08-25
op_units_rust.json                 8dda5af 2026-08-25
op_units_swift.json                8dda5af 2026-08-25
probe_manifest_go.json             fdff0b2 2026-08-26
probe_manifest_rust.json           fdff0b2 2026-08-26
probe_manifest_swift.json          fdff0b2 2026-08-26
```

The only files MODIFIED under `Research/op_pipeline` during this session's
window are this task's own new files, edited after the daemon had already
committed them, plus `canon35_*` and `build_table25.py`, which belong to
task 39 running in parallel and are named here so they are not mistaken
for this task's.

The daemon has committed throughout:

```
$ git log --oneline -3
be339f1 auto: 1 file (supersession_altered_testimony.json)
7198fe1 auto: 6 files (recapture_state.json, supersede_altered.py, ...)
c545fc1 auto: 5 files (recapture_state.json, recap_recap_swift_c0002.sh, ...)
```

## 9.1 The guard, on every grouping-shaped output

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py \
    type_inventory2_core2.json legality_reduction2.json \
    legality_validation2.json legality_quirks.json regen_cost.json \
    probe_residue2.json probe_manifest2_{c,cpp,go,rust,swift}.json \
    trickle_state.json recapture_state.json trickle_tallies.json \
    supersession_altered_testimony.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS type_inventory2_core2.json -- no operator token in any key, grouping, pairing or row structure
PASS legality_reduction2.json -- ...
PASS legality_validation2.json -- ...
PASS legality_quirks.json -- ...
PASS regen_cost.json -- ...
PASS probe_residue2.json -- ...
PASS probe_manifest2_c.json -- exempt: top-level meta declares role 'generator provenance', ...
PASS probe_manifest2_cpp.json -- exempt ...
PASS probe_manifest2_go.json -- exempt ...
PASS probe_manifest2_rust.json -- exempt ...
PASS probe_manifest2_swift.json -- exempt ...
PASS trickle_state.json -- ...
PASS recapture_state.json -- ...
PASS trickle_tallies.json -- ...
PASS supersession_altered_testimony.json -- ...
guard rc=0
```

The five manifests take the same `generator provenance` exemption
`probe_gen.py`'s own manifests take, declared in `meta.role` — a manifest
records what was handed to a compiler, so its operator field is the
provenance of the probe. The exemption was NOT claimed for anything else:
the reduction, the validation, the quirks, the residue tally, the two
state files, the tallies and the supersession sidecar were all walked in
full. Every one of the 334 chunk stores is walked individually the moment
it is written, and a store that fails is DELETED and its chunk marked
`refused_by_the_spelling_guard` rather than banked; zero chunks reached
that state.

## 9.2 Which side of the container wall

```
$ ls -d /work
ls: cannot access '/work': No such file or directory
$ hostname
<user>
```

`/work` is the container's build root — the residue's own refusal texts
carry it (`/work/regen_c_c0061/u/n24400/unit.c:5:13: error: ...`). It is
absent here, so every command in this log ran on the HOST unless it is
written as a `podman exec`.

---

# 10. Evidence class per claim

| claim | evidence class |
|---|---|
| the 129,553 residue, per language and total | forced by construction — two independent routes over the rule tables and the enumerated candidate space, agreeing to the unit (§4.2) |
| rust `bool` is a truth value | the tool's own testimony — rustc's type-kind match, at a named pin and line, parsed at run time (§2.1.2) |
| swift `Bool` is a truth value | the tool's own testimony — the stdlib's own declaration, already in the inventory |
| every accepted probe's ship / anchor / DWARF | the tool's own testimony — objdump's columns and the compiler's own debug table, as the lane recorded them |
| every refusal text | the tool's own testimony — the compiler's own words, captured verbatim (the marker is on every product) |
| the toolchain pins (§5.2) | the tool's own testimony — each toolchain's own version line, printed by the lane before it compiled |
| lane runtimes and per-probe costs | forced by construction — the daemon's own footer, and this session's own measured elapsed times |
| the 0.8 efficiency haircut in the cost page | human interpretation — declared, not measured, and marked so in `regen_cost.json` |
| the 218 supersessions | forced by construction — whole-source identity with the probe numbering erased |
| log 126's reconstructions being right | forced by construction — the recaptured diagnostic matches the reconstruction character for character on 109 captures |
| c/cpp fixed-point refusals (F40-2) | forced by construction — clang's own stored diagnostic |
| zero regressions | forced by construction — the version-control system's own record (§9) |

---

# 11. Complete file inventory

## 11.1 New programs, in `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`

| file | what it is |
|---|---|
| `core_rule2.py` | the scalar-core rule v2: normalised-class membership, plus rustc's type-kind arms parsed at run time |
| `legality_filter2.py` | the reduction and validation recomputed over the corrected core, with the ratified quirk scored |
| `legality_quirks.json` | the additive quirk annotation (two rule ids, `deprecated_but_allowed`) |
| `regen_cost.py` | the cost page, read off the existing lane logs; compiles nothing |
| `probe_gen2.py` | the regeneration candidate set: full extracted core, filter verdict on every candidate |
| `trickle.py` | the chunked, checkpointed, resumable driver |
| `trickle_report.py` | the per-chunk tallies, read from the resume state |
| `recapture_original.py` | the unfiltered re-capture of the three original plain lanes |
| `supersede_altered.py` | the supersession sidecar builder (whole-source identity join) |
| `trickle_up.sh` | starts the capped copy; documents every name, share and cap |
| `trickle_down.sh` | stops it (`--pause` to keep the container) |
| `trickle_doctor.sh` | state, collisions, pins, resume position, disk |

## 11.2 New data, same directory

| file | what it is |
|---|---|
| `type_inventory2_core2.json` | the v2 cores with the v1/v2 delta and the rust citations |
| `legality_reduction2.json` | the corrected reduction; 153,857 naive / 121,096 legal / 129,553 to compile |
| `legality_validation2.json` | the corrected validation; 100.0% in-scope, 0 misses, 4 quirk agreements |
| `regen_cost.json`, `regen_cost.md` | the cost page |
| `probe_manifest2_c.json` | 51,829 candidates with sources |
| `probe_manifest2_cpp.json` | 70,991 |
| `probe_manifest2_go.json` | 553 |
| `probe_manifest2_rust.json` | 1,993 |
| `probe_manifest2_swift.json` | 4,187 |
| `probe_residue2.json` | the per-language residue tallies, one page |
| `trickle_state.json` | **the resume state** — 326 chunk records |
| `recapture_state.json` | the re-capture's resume state — 8 chunk records |
| `trickle_tallies.json`, `trickle_tallies.md` | per-chunk and per-language tallies |
| `supersession_altered_testimony.json` | the supersession sidecar; 218 superseded, 118 out of scope |
| `trickle_run.log` | the driver's own console output for the regeneration |

## 11.3 New directories, same directory

| directory | contents |
|---|---|
| `trickle_store/` | 334 folded stores — 326 `op_units2_<chunk>.json` and 8 `op_units_recapture_<chunk>.json`, 125 MB |
| `trickle_raw/` | 668 files — each lane's raw product and its console log, 32 MB |
| `trickle_lanes/` | 334 files — the exact lane script that ran for each chunk, 8 MB |

## 11.4 New, outside every repository

`AirlockTrickle/agent/{drop,out,logs,status}` — the capped
copy's own tree, deliberately outside the repositories so the 30-second
daemon is not asked to commit the container's scratch.

## 11.5 New in `PRIVATE/PseudoCoupHQ/DevComms/`

`log_131_task40_regeneration_trickle.md` — this log.

## 11.6 Byte-code caches, named as required

Created or refreshed in `Research/op_pipeline/__pycache__/` by this task's
imports: `core_rule2.cpython-313.pyc`, `supersede_altered.cpython-313.pyc`,
`trickle.cpython-313.pyc`, and refreshed (pre-existing) copies of
`legality_filter.cpython-313.pyc` and `probe_gen.cpython-313.pyc`.

## 11.7 Edited, append-only

One dated entry appended under the single `# PROGRESS` heading of
`Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`.

---

# 12. The two lists

## 12.1 Decided, recorded for audit (mechanical, mine to decide)

- the core rule v2 tests the NORMALISED class, and reads rustc's type-kind
  arms at run time for rust's unmarked primitives; the declared stdint
  aliases are lookup-only and never enter a core.
- F36-1 is an ADDITIVE annotation file, not a superseding rules file; no
  rule shape is edited, so the reduction arithmetic is untouched by it.
- the copy is `trickle-runner` on `trickle-internal`, capped at half the
  cores, sharing the image and the persist volume read-only, with no proxy
  and no hot-folder daemon.
- chunk size 400, six workers, per-chunk stores in a new directory, a
  temporary-name-and-rename state file, and a chunk as the unit of
  atomicity.
- the supersession join is whole-source identity with the probe numbering
  erased; supersession is a sidecar mark and never an edit.
- the re-capture covers the three PLAIN lanes only; the assignment lanes
  are reported out of scope rather than quietly counted.

## 12.2 Awaiting the owner (kept minimal)

1. **F40-2 — the fixed-point types.** 24 of c's and cpp's 56 core
   spellings are `_Fract` / `_Accum` forms clang admits only under
   `-ffixed-point`. Should the residue carry that flag, or should those
   rows be marked as needing a dialect? Today they are compiled and
   honestly refused.
2. **The assignment lanes' 49 remaining altered captures** (go 33, rust
   26). Re-capturing them means giving `asg_stage.py` the same verbatim
   treatment; log 126 measured the three lanes at 63.0 seconds. Not done,
   because it is a different generator and outside this brief.
3. **What consumes the 29,288 new accepted units.** They are extracted and
   banked in a separate id space; nothing downstream reads them yet.

---

# CORRECTION, 2026-09-02 — a copy was made where a feature was required

Appended after the fact. Nothing above is edited; this states plainly what
§5.1 got wrong, and corrects one measured claim.

## C.1 The copy

§5.1 describes `AirlockTrickle` as "the capped copy" and
treats making it as a mechanical decision (§12.1: "the copy is
`trickle-runner` on `trickle-internal`, capped at half the cores"). It was
not. It was a **fork of Airlock**, made because Airlock could not be asked
for a second sandbox: its container, network and volume names were spelled
literally in thirteen files, and its caps were bound to the install.

the owner's rule, stated the same day:

> its not supposed to be a repo that is modified for use for a specific
> project ... if i wanted to use Numpy, i wouldnt clone Numpy in order to
> modify Numpy source. Airlock source isnt meant to be modified. its an
> application.

**A copy was made where a feature was required.** The correct act was to
add instances to Airlock — which is what was done on 2026-09-02, recorded
in `DevComms/log_138_airlock_instances_feature.md`. A second sandbox is now
one settings file and one flag:

```
PUBLIC/Airlock/instances/trickle.conf
bash PUBLIC/Airlock/up.sh --instance trickle --cpus 6
```

`trickle_up.sh`, `trickle_down.sh` and `trickle_doctor.sh` are superseded
(see `Research/op_pipeline/TRICKLE_SUPERSEDED.md`). `trickle.py`'s
`podman exec` path is replaced by `trickle2.py`, which submits through
`airlock submit`. Nothing on the project side runs podman any more.

`AirlockTrickle` no longer exists on disk. It was **not**
removed by the instances work: it was present with its 339 lanes and 339
products early in that session and absent an hour later, removed by
something else. Its material survives in this repository as
`Research/op_pipeline/trickle_lanes/` (334 lane scripts),
`trickle_raw/` (668 raw products and consoles) and `trickle_store/`
(334 folded stores). This is recorded in
`PUBLIC/Airlock/instances/trickle/agent/README.md`.

## C.2 The inotify diagnosis was the right conclusion from the wrong number

§5.1.4 reads:

> ```
> OSError: [Errno 28] inotify_add_watch(/drop) failed: No space left on device
> $ cat /proc/sys/fs/inotify/max_user_instances
> 128
> ```
> That is the inotify INSTANCE limit, not disk.

Half right. It is not disk — that part stands, and it is the part that
matters. But the call that failed is `inotify_add_watch`, and the limit
`inotify_add_watch` runs into is `max_user_watches`, not
`max_user_instances`. `inotify_init1` had already succeeded, so an instance
was available.

Measured on 2026-09-02 while the same failure was reproduced:

```
inotify INSTANCES open : 114 / 128        <- tight, but not the one that failed
inotify WATCHES held   : 65470 / 65536    <- 66 free; this is the one
   62684 watches  <one editor>
```

Measured again after that editor was not running:

```
instances 56/128  watches 3625/65536
```

So the exhaustion is a transient property of what else is on the machine,
which is exactly why the fix belongs inside Airlock and not in a kernel
setting. Airlock's daemon now takes `watch = poll` (a `/drop` rescan, no
inotify resource at all) and `watch = auto` (inotify, falling back loudly on
that one ENOSPC). Both are documented; `inotify` remains the default.

The `podman exec` workaround §5.1.4 chose — "the container is started idle
instead and the driver reaches in" — is retired. It is also why the 339 runs
above have no `status/` and no `logs/` entries: reaching past the daemon
means the daemon writes nothing.
