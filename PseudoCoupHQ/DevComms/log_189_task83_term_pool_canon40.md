# log 189 — task 83: term66, the census, the pool over canon40

Date: 2026-09-04. Appendix-B shape: one numbered tree, high to low,
values in motion at the leaves. §5.1a labels throughout: LITERAL is the
stored object or the pasted command output, GLOSS is what it means,
ANALOGY is only ever an aid and never the mechanism. Every count
carries its population. Every "I verified X" pastes the command and
its output.

ALL COMPUTE RAN AS AIRLOCK LANES on instance `t83`. Not one line of
this task's analysis ran as host python. The lane logs at
`<runs>/t83/agent/logs/` are the evidence and are cited by path
throughout.

---

# 0. What was done, in plain words before any figure

- The task was to resume `term66` over the newest canon, then run the
  census, the pool, the families and the exception families over it,
  and report the four term states and the pool delta with every
  movement's cause.
- **canon40 IS the newest canon**, verified on disk; this run is over
  canon40 and says so, as the brief required.
- The resume did not simply continue. Inside the sandbox the same
  program that had peaked at 816,136 kB on the host was **ABORTed by the
  container's 8 GB cgroup in 11 seconds**, before finishing one
  further shard.
- Ten measurement lanes located the cause. The excursion is **not** a
  unit, **not** a callee body and **not** the transcription: the
  solver's allocator takes whatever address space it is given, and on
  the easy units a ceiling holds it there and returns the identical
  record (§2).
- **On the hard units it does not.** §3 is the correction and the
  blocker: **3,927 of the 30,324 units canon40 proves (12.95%) carry a
  runtime-callee row** — task 78's rule took that row count from 608 to
  **49,362** — and those units cost so much that a ceiling either fires
  (turning a term into a hole with `MemoryError` as its written reason)
  or does not fit the schedule. Over 512, 1024, 2048, 4096 and 6144 MB
  the hard shard's records **never converge**.
- So **`term66` was NOT completed** and none of items 2 to 7 was built,
  because each needs a complete store and none was built on a partial
  one. The brief's own stop rule names this case: *"the memory cap
  aborts"*. §4 is the item-by-item statement.
- The eight shards this session wrote before the refusal scan could run
  are preserved as records and taken back out of the store, which is
  byte-identical in content to the handoff state (§3.5, §9).
- Three things are FLAGGED for the owner rather than decided, in §7.

---

# 1. The canon this run is over

The brief: *"If 78 lands a new canon, this runs on it and says so; if
it does not, this runs on canon39 and says that instead."*

## 1.1 canon40 is the newest canon, verified on disk

LITERAL — `<runs>/t83/agent/logs/20260904T183152Z__t83_l1_sample.sh.log`,
lane `t83_l1_sample.sh` §2, run inside the sandbox:

```
======== 2. the canon check -- is canon40 the newest canon on disk? ========
canon36
canon37
canon38
canon39
canon40
-- canon41 present?
ls: cannot access 'canon41*': No such file or directory
-- the canon40 inputs term66_run.py walks:
-rw-rw-r-- 1 root root   58534 Sep  4 03:33 canon40_interp.json
-rw-rw-r-- 1 root root 4968708 Sep  4 03:32 canon40_wrapped_c.json
-rw-rw-r-- 1 root root 6595089 Sep  4 03:33 canon40_wrapped_cpp.json
-rw-rw-r-- 1 root root  899255 Sep  4 03:33 canon40_wrapped_go.json
-rw-rw-r-- 1 root root  835699 Sep  4 03:33 canon40_wrapped_rust.json
-rw-rw-r-- 1 root root 1219609 Sep  4 03:33 canon40_wrapped_swift.json
-- regen shards: 326
```

GLOSS. Task 78 landed canon40 and nothing later exists. **This run is
over canon40**, said explicitly as the brief required. The walk's
inputs are the six top-level files above plus the 326 shards of
`canon40_regen_store/`: **332 inputs**, holding **30,324 units canon40
proves of 31,078 attempted** (§4.1 restates that population against
its own artifact).

## 1.2 Every analysis import is present in the sandbox

The stop rule says an absent import stops the task. None is absent.

LITERAL — the same lane log, §1:

```
======== 1. the imports term66_run.py needs, each named ========
  OK      z3                               /opt/venv/lib/python3.13/site-packages/z3/__init__.py
  OK      canonical_form                   PseudoCoupHQ/Research/op_pipeline/canonical_form.py
  OK      gate                             PseudoCoupHQ/Research/op_pipeline/gate.py
  OK      reference                        PseudoCoupHQ/Research/op_pipeline/reference.py
  OK      regate64_run                     PseudoCoupHQ/Research/op_pipeline/regate64_run.py
  OK      term                             PseudoCoupHQ/Research/op_pipeline/term.py
  OK      pool                             PseudoCoupHQ/Research/op_pipeline/pool.py
  OK      pool65_run                       PseudoCoupHQ/Research/op_pipeline/pool65_run.py
  OK      ledger                           PseudoCoupHQ/Research/op_pipeline/ledger.py
  OK      dom_ops                          PseudoCoupHQ/Research/op_pipeline/dom_ops.py
  OK      normalize79_pool_prediction      PseudoCoupHQ/Research/op_pipeline/normalize79_pool_prediction.py
  OK      guard66                          PseudoCoupHQ/Research/op_pipeline/guard66.py
```

GLOSS. One tool IS missing and it is a measuring tool, not an analysis
import: `/usr/bin/time` is not in the image. That is recorded here as
a fact about the image, not treated as a blocker — the peak resident
size is read from the kernel by `resource.getrusage` instead, which is
the same number from the same place.

## 1.3 The resume state at handoff, verified rather than assumed

LITERAL — the same lane log, §3:

```
======== 3. the resume state BEFORE the sample ========
  done inputs 10
    canon40_interp.json
    canon40_regen_store/op_units2_c_c0000.json
    canon40_regen_store/op_units2_c_c0001.json
    canon40_regen_store/op_units2_c_c0002.json
    canon40_regen_store/op_units2_c_c0003.json
    canon40_wrapped_c.json
    canon40_wrapped_cpp.json
    canon40_wrapped_go.json
    canon40_wrapped_rust.json
    canon40_wrapped_swift.json
-- store shards before: 10
```

GLOSS. The brief's description of the handoff is exact: 10 done
inputs, the six top-level canon40 files and four regen shards; 326
shards in `canon40_regen_store/` (130 c, 178 cpp, 2 go, 5 rust, 11
swift), 322 of them still to walk. `term66_run.log`'s per-input counts
(610/0, 770/0, 107/0, 123/2, 151/16, 9/2, 138/9, 125/5, 99/18, 0/0;
peak 816,136 kB at 147 s) are reproduced by the store itself: **2,132
records across the 10 shards**, which is 610+770+107+123+151+9+138+125
+99+0.

## 1.4 The pipeline code has not moved since those 10 shards were written

This matters because §3.4 finds four records that do not reproduce, and
a code change would be a very different explanation from a machine
difference.

LITERAL — `git log` over the five files that decide a record, since
23:00 on the night the store was written:

```
b0426462 2026-09-03 23:57:14 -0400 auto: 1 file (term.py)
1aa58b1c 2026-09-03 23:56:44 -0400 auto: 3 files (PROGRESS.md, term.py, inject_report_cpp.json)
```

and the modification times:

```
2026-09-03 13:18:57  gate.py
2026-09-03 13:19:37  reference.py
2026-09-03 23:56:54  term.py
2026-09-03 23:57:22  term66_run.py
```

GLOSS. `term.py`'s last change is at **23:56:54** and the first store
shard was written at **23:57**. `gate.py` and `reference.py` have not
changed since 13:19. So every shard in `term66_store`, the ten written
on the host and the 322 written in this round's lane, was written by
the same code. The four records of §3.4 differ for another reason.

---

# 2. What the memory excursion is, measured

The resume did not just continue, and the six lanes that found out why
are the substance of this section. The conclusion first, then the walk
that earns it.

**The runaway is the solver's allocator, not the analysis.** Given a
ceiling it stays under it, takes proportionally less time, and returns
the identical record. Given none it grows until the container stops
the process.

## 2.1 What happened when the resume was simply restarted

LITERAL — `<runs>/t83/agent/logs/20260904T183235Z__t83_l2_sample.sh.log`,
the whole of lane `t83_l2_sample.sh`:

```
======== THE SAMPLE -- term66_run.py with a 240 s budget ========
total inputs to walk: 332
[10/332] shards transcribed

term66_run.py exit -9 (3 = budget spent, resumable)
SAMPLE PEAK RESIDENT (child, ru_maxrss) 8391436 kB
SAMPLE WALL TIME 11 s

======== the resume state AFTER the sample ========
done inputs 10
store shards: 10
records transcribed so far 2132
[10/332] shards transcribed
```

GLOSS, with the numbers named. `exit -9` is the operating system
stopping the process with no language-level error — an **ABORT**, by
the container's own 8 GB memory cap. The peak, **8,391,436 kB**, is
that cap. It took **11 seconds** and finished **zero** further shards
of the 322 outstanding.

This is exactly the failure the round's memory rule exists to prevent,
and it shows why `term66_run.py`'s own guard could not prevent it:

- `term66_run.check_memory` reads `resource.getrusage` and aborts by
  name at 6 GB — but it is called **after each shard**, in
  `term66_run.run`'s loop.
- The process passed 6 GB and reached 8 GB **inside** one shard. The
  between-shard check never ran. A bound that is only tested between
  units of work is not a bound on a unit of work.

## 2.2 Where inside the shard: one unit, +4.88 GB

`probe83b_memory.py` walked the next shard the resume owed —
`canon40_regen_store/op_units2_c_c0004.json` — unit by unit, reading
`ru_maxrss` after each and printing any growth over 50 MB.

LITERAL — `<runs>/t83/agent/logs/20260904T183428Z__t83_l3_memory_probe.sh.log`:

```
-- the setup, the same objects term66_run.run builds
   resident before setup 55308 kB
   attached callee units 4, resident 56972 kB
   runtime answer readings 76, resident 56972 kB
   resident after setup 56972 kB
-- the shard
   canon40_regen_store/op_units2_c_c0004.json
   units in the shard 50, resident 58100 kB
   [   4] c/regen_1859             resident 4946492 kB (+4883500 kB on this unit)
```

GLOSS. Setup — every attached callee body, every runtime-answer
reading, the `Reference`, the `Term` and the `Gate` — costs
**56,972 kB**, and the shard's document costs another 1,128 kB. Then
the **fourth unit alone adds 4,883,500 kB**. The population is one
unit of the 50 in that shard.

## 2.3 The unit, and why it looked like the callee bodies

LITERAL — `c/regen_1859`, printed off
`canon40_regen_store/op_units2_c_c0004.json`: **16 body lines, 32
ledger rows**, of which **21 name a runtime callee**.

```
    push %rbx
    pextrw $0x0,%xmm0,%ebx
    call L0 !!reloc=R_X86_64_PLT32:__floattisf-0x4
    L0:
    call L1 !!reloc=R_X86_64_PLT32:__truncsfbf2-0x4
    L1:
    pextrw $0x0,%xmm0,%eax
    shl $0x10,%ebx
    movd %ebx,%xmm1
    shl $0x10,%eax
    movd %eax,%xmm0
    addss %xmm1,%xmm0
    call L2 !!reloc=R_X86_64_PLT32:__truncsfbf2-0x4
    L2:
    pop %rbx
    ret
```

GLOSS, and the obvious hypothesis. Sixteen lines cannot themselves
cost five gigabytes. Three of them transfer into the compiler's own
runtime, and round 12's standing resolution attaches those callees'
BODIES as ArchUnits. `term.Term.runtime_row` steps into an attached
body through `Reference.walk_body`, which forks the state at every
conditional transfer and merges the arms at every join with
`If(condition, this side, the rest)` over the whole register file. So
the hypothesis was: a soft-float conversion body has many forks and
the merge explodes.

**The hypothesis is wrong, and it was tested rather than believed.**

## 2.4 Every attached callee body, walked alone

`probe83e_callee_bodies.py` walked all 76 attached bodies, **each in a
forked sub-process of its own**, so each body's peak is its own and a
runaway is named rather than inherited. Bounds per sub-process: 4 GB of
address space, 120 s.

LITERAL — `<runs>/t83/agent/logs/20260904T183912Z__t83_l5_callee_bodies.sh.log`,
the summary and the hungriest rows:

```
-- outcomes over the 76 attached bodies
   NotModeled               16
   walked                   60

-- the ten hungriest bodies
   clang++    __floattixf           56676 kB    0.15 s  walked
   clang      __floattixf           56656 kB    0.21 s  walked
   clang++    __floatuntixf         54956 kB     0.1 s  walked
   clang      __floatuntixf         54932 kB    0.15 s  walked
   swiftc     __divti3              48244 kB    0.01 s  walked
   swiftc     __modti3              48244 kB    0.01 s  walked
   swiftc     __truncsfhf2          48208 kB     0.0 s  walked
   clang      __floattidf           48016 kB    0.01 s  walked
   clang      __floattitf           48016 kB    0.01 s  walked
   swiftc     __udivmodti4          47924 kB     0.0 s  walked
```

and the two bodies `c/regen_1859` actually calls:

```
   clang      __floattisf            85      5      1       0.01        47488  walked
   clang      __truncsfbf2          100      9      0       0.01        47048  walked
```
(columns: lines, conditional transfers, calls, seconds, peak kB)

GLOSS. Over the population of **76 attached bodies**: 60 walk, 16 are
refused by the opcode table, and the **hungriest of all 76 costs
56,676 kB and 0.21 s**. `__truncsfbf2` has nine conditional transfers
and still walks in **47,048 kB and 0.01 s**. No body is the runaway.
The hypothesis of §2.3 is refuted.

## 2.5 The unit traced row by row: the transcription never passes 50 MB

`probe83f_one_unit_trace.py` wrapped `Reference.walk_body` and
`Term.runtime_row` — in the probe only, by assignment on the imported
class, never on disk — and recorded, per step, the CURRENT resident
size (from `/proc/self/statm`, which falls as well as rises, unlike
the `ru_maxrss` high-water mark) and the AST node count of the
register the row reads.

LITERAL — `<runs>/t83/agent/logs/20260904T184118Z__t83_l7_unit_trace.sh.log`,
the first, a middle and the last steps, and the result:

```
-- setup done, resident 45052 kB
-- the unit c/regen_1859: 16 body lines, 32 ledger rows
   of those, runtime-callee rows: 21
-- runtime_row into __floattisf (resident 48564 kB)
   walk_body   12 lines     49524 ->    49720 kB    0.01 s  largest register 297 AST nodes
   walk_body   85 lines     48564 ->    49892 kB    0.03 s  largest register 447 AST nodes
   runtime_row __floattisf built: 49908 kB, 0.09 s, row term 302 AST nodes
...
-- runtime_row into __truncsfbf2 (resident 50336 kB)
   walk_body  100 lines     50336 ->    50336 kB    0.01 s  largest register 931 AST nodes
   runtime_row __truncsfbf2 built: 50336 kB, 0.09 s, row term 931 AST nodes
   walk_body   16 lines     50336 ->    50352 kB    0.22 s  largest register 931 AST nodes
-- the record: term_state TERM, proved True

-- the result for c/regen_1859
   outcome walked
   wall time 3.53 s
   peak resident 3062572 kB
```

GLOSS, values in motion, and this is the step that turns the whole
diagnosis around:

- The 21 runtime rows are walked one after another. The largest
  register's term grows **297 → 447 → 684 → 931 AST nodes** across
  them. Nine hundred nodes is a small term.
- The **current** resident size across the entire transcription moves
  from 45,052 kB to **50,352 kB**. It never approaches a gigabyte.
- The record comes out **TERM, proved True**.
- And yet the process's **peak** is **3,062,572 kB**.

So the memory is not spent at any step the trace covers. It is spent
after the last traced step — in the **gate**, where z3 solves the
obligation. And 3,062,572 kB is suspiciously close to something: the
probe's own ceiling was 3,221,225,472 bytes, i.e. **3,145,728 kB**.
The peak sat just under the ceiling it was given.

## 2.6 The ceiling test: the appetite is opportunistic

If a peak tracks whatever ceiling it is given, that is an allocator
taking what is available, not a computation that needs it. That is a
testable claim, and `probe83g_ceiling.py` tested it: the SAME unit,
transcribed and gated in a forked sub-process at five ceilings, with the
whole record read back each time.

LITERAL — `<runs>/t83/agent/logs/20260904T184234Z__t83_l8_ceiling.sh.log`:

```
   ceiling MB      peak kB    seconds      state   proved    holes  outcome
          512       464828       0.52       TERM     True        0  walked
         1024       971144       0.67       TERM     True        0  walked
         2048      2031888       1.11       TERM     True        0  walked
         3072      3068796       1.81       TERM     True        0  walked
         5120      5178796       2.61       TERM     True        0  walked

-- the verdict
   ceilings that walked to an answer 5 of 5
   every answer identical: True
   THE APPETITE IS OPPORTUNISTIC: the peak follows the ceiling and the record does not change, so a ceiling is a bound and not a change to the corpus.
```

GLOSS, and this is the whole finding:

- The **peak follows the ceiling** at every one of the five points:
  464,828 kB under 512 MB; 5,178,796 kB under 5,120 MB. It is a
  straight line through the ceiling, not a plateau at a requirement.
- The **record is identical at all five** — same term state, same
  proved, same route, same hole count, same layer-5 text. The
  comparison is of the record, not only of the peak: a bound that
  changed an answer would not be a bound.
  **THIS HOLDS FOR THIS UNIT AND FOR THE EASY SHARDS ONLY, and §3.3
  is the correction.** On a HARD shard the ceiling changes half the
  records, and no ceiling this instance allows makes them converge.
  The conclusion drawn here was right about what it measured and too
  broad about what it implied; it is left standing and corrected
  there rather than quietly rewritten.
- The **time appeared to follow the ceiling too** on this unit:
  0.52 s at 512 MB against 2.61 s at 5,120 MB. **That part did NOT
  generalise and is corrected in §2.10** — over a whole shard the
  ceiling buys no throughput at all. It is recorded here as measured
  and withdrawn there as refuted, rather than quietly dropped.

ANALOGY, and only as an aid: this is a room being filled with whatever
furniture will fit, not a room whose size was chosen for the furniture.
The mechanism is the mechanism above — the peak is a linear function of
the ceiling and the answer is a constant — and the analogy adds
nothing to it.

---

## 2.7 The bound tested against this corpus's OWN records, not one unit

§2.6 tested one unit. The claim that a ceiling is a bound and not a
change to the corpus has to be tested against records the corpus
already holds. `term66_bounded.py --check` re-transcribes shards that
are ALREADY in `term66_store` into scratch and compares them **record
for record** against what is stored.

LITERAL — `<runs>/t83/agent/logs/20260904T184356Z__t83_l9_zero_regression.sh.log`,
lane `t83_l9_zero_regression.sh`, three stored shards under a 6 GB
address-space bound:

```
canon40_wrapped_go.json: 107 transcribed, 0 canon40-not-proved skipped, peak 686748 kB (7s)
canon40_interp.json: 9 transcribed, 2 canon40-not-proved skipped, peak 686748 kB (7s)
canon40_regen_store/op_units2_c_c0001.json: 125 transcribed, 5 canon40-not-proved skipped, peak 686748 kB (7s)

-- ZERO REGRESSION, in the ruled sense: record for record
   shards compared 3
   records compared 241
   records identical 237
   records that differ 4
       canon40_wrapped_go.json/go/op_103
       canon40_wrapped_go.json/go/op_132
       canon40_wrapped_go.json/go/op_139
       canon40_wrapped_go.json/go/op_96
REFUSED OWN OUTPUT: the bound changed a record, so it is not a bound
```

GLOSS. **237 of 241 records identical, 4 differ** — and the check
refused its own output, exactly as it should have, because on the
evidence available at that moment the bound was the only suspect. It
is not the culprit, and §2.8 is how that was established rather than
assumed.

## 2.8 The control that exonerates the bound

Two candidate causes, and one experiment that separates them:

- the ADDRESS-SPACE BOUND changed the records; or
- something about **this container against the host** the ten stored
  shards were walked on changed them.

The control runs the identical check with the ceiling set to 30,000 MB
— far above the container's own 8 GB cap, so no address-space bound can
bite. The three shards peak at 440,308 kB, so nothing is risked.

LITERAL — the bounded check run a second time
(`20260904T184446Z__t83_l10_repeatability.sh.log`, pass 2 of 2) and the
unbounded control (`20260904T184519Z__t83_l11_unbounded_control.sh.log`):

```
   [bounded, 6144 MB, second run]           [unbounded, 30000 MB]
   records compared 241                     records compared 241
   records identical 237                    records identical 237
   records that differ 4                    records that differ 4
       canon40_wrapped_go.json/go/op_103        canon40_wrapped_go.json/go/op_103
       canon40_wrapped_go.json/go/op_132        canon40_wrapped_go.json/go/op_132
       canon40_wrapped_go.json/go/op_139        canon40_wrapped_go.json/go/op_139
       canon40_wrapped_go.json/go/op_96         canon40_wrapped_go.json/go/op_96
```

GLOSS. **The unbounded run differs from the store in exactly the same
four records.** The bound is not the cause. Combined with §1.4 — the
code has not moved — what is left is the machine: the host walked those
ten shards, this container walks the rest.

## 2.9 What the four records actually are: the gate's wall clock

The four are not random. They are read off the two stores directly.

LITERAL — the differing fields, `go/op_96` and `go/op_103`, fresh
against stored:

```
===== go/op_96
  KEY verdict_ship
   fresh : {"counterexample": "[seed_rax = 3623878656, seed_rbx = 3623878656]", "outcome": "DISPROVED", ...}
   stored: {"counterexample": "[seed_rax = 1610612736, seed_rbx = 4292331166]", "outcome": "DISPROVED", ...}
===== go/op_103
  KEY outcome
   fresh : "UNDECIDED"
   stored: "DISPROVED"
  KEY reason
   fresh : "the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved"
   stored: "z3 found a starting state under which the two sides differ"
```

GLOSS, and this is a SEPARATE finding from the memory one, flagged in
§7.2 and not decided here:

- **Three of the four keep their verdict** (DISPROVED both times) and
  differ only in the WITNESS — z3 returned a different satisfying
  starting state. `seed_rax = 3623878656` here, `seed_rax = 1610612736`
  there. Both are counterexamples; the solver is entitled to either.
- **One of the four changes state**: `go/op_103` was DISPROVED on the
  host and is UNDECIDED here, because `gate.SOLVER_MILLISECONDS = 3000`
  is a **wall-clock** limit and this container did not finish inside it.
  The gate's own rule is right — a timeout is UNDECIDED and never
  DISPROVED — but the consequence is that a verdict near that limit is
  a function of the machine as well as of the unit.
- Population: **4 of 241 records sampled, 1.66%**; state-changing,
  **1 of 241, 0.41%**. All four are go units and all four are in the
  thirteen that `audit66` already isolates as transferring to a named
  panic path.

---

## 2.10 The bound that was used, and why that number

LITERAL — `<runs>/t83/agent/logs/20260904T185126Z__t83_l14_ceiling_throughput.sh.log`,
lane `t83_l14_ceiling_throughput.sh`: the same shard
(`canon40_regen_store/op_units2_c_c0002.json`, 99 records, which the
host walked in 101 s) re-transcribed at three ceilings, timed, and
compared record for record against the store:

```
======== [4096 MB] op_units2_c_c0002.json ========
   records compared 99
   records identical 99
   records that differ 0
ceiling 4096 MB: wall 111 s, check exit 0
```

and the three timings together:

```
   ceiling      wall     records compared   identical   differ
   4096 MB      111 s          99               99         0
   1024 MB      117 s          99               99         0
    512 MB       90 s          99               99         0
```

GLOSS, in two parts.

**On correctness.** **99 of 99 records identical at every one of the
three ceilings** — a second and third independent zero-regression
result, on a c shard this time rather than the go shard of §2.7, and
here with **no** differing records at all. Taken with §2.8, the four
differing go records are the machine and nothing else; the bound
reproduces the corpus exactly wherever the machine agrees.

**On throughput, correcting §2.6.** The single unit of §2.6 suggested
the wall time scales with the ceiling, 5× between 512 MB and 5,120 MB.
**Over a whole shard it does not.** 1024 MB is 117 s against 4096 MB's
111 s — the wrong way round — and 512 MB saves 19%, not 80%. The
single-unit timing did not generalise, and it is withdrawn here rather
than left standing in §2.6.

**Which ceiling the run used, and why.** **4096 MB.** 512 MB is 19%
faster and the record is identical there too, but the largest working
set actually measured in this task is **686,944 kB** (lane 11's three
shards unbounded), which is above 512 MB. A ceiling below a measured
working set trades a 19% saving for the chance of a `MemoryError`
landing in the middle of a shard, and a `MemoryError` inside
`Term.transcribe`'s row loop is caught there as a written hole — which
the scan would then refuse, after the shard was already on disk.
4096 MB is half the instance's 8 GB, six times the largest working set
measured, and cost 111 s against 90 s on the timing shard.

---

# 3. THE BLOCKER: canon40's transcription does not fit the 6 GB cap

§2 ended with a ceiling that looked neutral. It is neutral on the easy
units and it is **not** neutral on the hard ones, and this section is
the correction, measured. The brief's stop rule names this case
exactly — *"the memory cap aborts"* — so the run was stopped and this
is the report.

## 3.1 The two kinds of shard, and the rate

LITERAL — `<runs>/t83/agent/logs/20260904T185651Z__t83_l15_term66_full.sh.log`,
the per-input lines of the full resume at a 4096 MB ceiling (the
seconds are cumulative from the start of the leg):

```
canon40_regen_store/op_units2_c_c0004.json: 24 transcribed, 26 canon40-not-proved skipped, peak 3887352 kB (1112s)
canon40_regen_store/op_units2_c_c0005.json: 94 transcribed, 6 canon40-not-proved skipped, peak 3887352 kB (1114s)
canon40_regen_store/op_units2_c_c0006.json: 96 transcribed, 4 canon40-not-proved skipped, peak 3887352 kB (1329s)
canon40_regen_store/op_units2_c_c0007.json: 95 transcribed, 8 canon40-not-proved skipped, peak 3887352 kB (1667s)
canon40_regen_store/op_units2_c_c0008.json: 124 transcribed, 6 canon40-not-proved skipped, peak 3887352 kB (2116s)
canon40_regen_store/op_units2_c_c0009.json: 89 transcribed, 3 canon40-not-proved skipped, peak 3887352 kB (2234s)
```

GLOSS, with values in motion:

- `c0004` walked **24 records in 1,112 s** — 46 s a record.
- `c0005` walked **94 records in 2 s** — 0.02 s a record, two thousand
  times cheaper.
- The peak is **3,887,352 kB on every line**, pinned against its own
  4096 MB ceiling and never falling below it once reached.
- Six shards took **2,234 s**. The population still to walk at that
  moment was **316 of 332 inputs**, which at that rate is **about 32
  hours** against a lane ceiling of six.

## 3.2 The bound FIRES, and a fired bound becomes a written reason

This is the part that makes the schedule secondary. `term.Term.
transcribe` catches an exception raised while a row is being built and
records it as a HOLE with a written reason. `MemoryError` is such an
exception. So a ceiling that fires does not stop the run — it quietly
turns a unit that would have had a term into a unit with a hole.

LITERAL — `<runs>/t83/agent/logs/20260904T194034Z__t83_l19_hard_shard_safety.sh.log`
§2, the scan over the store as the leg left it:

```
======== [2/3] does the STORE carry a memory failure as a written reason? ========
records in term66_store: 2701
records naming MemoryError: 2
   canon40_regen_store/op_units2_c_c0004.json c/regen_1859
   canon40_regen_store/op_units2_c_c0005.json c/regen_2079
```

GLOSS. **2 records of 2,701 in the store carried `MemoryError` as
their own written reason.** That is small and it is fatal: a record
whose reason is the runner's memory limit is a record about the runner,
not about the compiler, and the whole line exists to say what the
COMPILER does. `c/regen_1859` is the very unit §2.5 traced building a
proved term in 50,352 kB — under the 4096 MB ceiling, in the middle of
a shard, it did not.

## 3.3 No ceiling this instance allows makes the hard shard converge

Three ceilings below 4096, then one above it, all re-transcribing the
SAME shard into scratch and comparing record for record.

LITERAL — `...T193541Z__t83_l18_hard_shard_ceilings.sh.log` and
`...T194034Z__t83_l19_hard_shard_safety.sh.log` §3:

```
   ceiling      wall     records   identical   differ     against
    512 MB        2 s       24         12        12       the 4096 MB shard
   1024 MB        5 s       24         12        12       the 4096 MB shard
   2048 MB      214 s       24         15         9       the 4096 MB shard
   4096 MB     1112 s       24         --         --      (the run of record)
   6144 MB     1098 s       24         22         2       the 4096 MB shard
```

with 6144 MB's own peak:

```
canon40_regen_store/op_units2_c_c0004.json: 24 transcribed, 26 canon40-not-proved skipped, peak 6002644 kB (1097s)
```

GLOSS, and this is the finding the task turns on:

- The low ceilings are fast **because** they stop the work early:
  2 s at 512 MB against 1,112 s at 4096 MB is not a speed-up, it is
  **half the shard's records changing**.
- Raising the ceiling does not settle it either. At **6144 MB** — the
  highest this instance's 8 GB cap allows any headroom for — the peak
  is **6,002,644 kB**, again pinned against its ceiling, the wall time
  is unchanged at 1,098 s, and **2 of 24 records still differ** from
  what 4096 MB wrote (`c/regen_1887`, `c/regen_1890`).
- So over the ceilings 512, 1024, 2048, 4096 and 6144 MB the hard
  shard's records **never converge**. There is no number in the
  instance's range at which the answer stops depending on the number.

## 3.4 Why canon40 costs what canon39 did not, with the population

The part-run of 2026-09-03 walked 2,132 records in 147 s and nothing
suggested a problem. The reason is in which records those were.

LITERAL — `<runs>/t83/agent/logs/20260904T183909Z__t83_l4_callee_population.sh.log`,
`probe83d_callee_population.py` over **every one of the 30,324 units
canon40 proves** (754 not proved, not counted):

```
-- canon40, over 30324 proved units (754 not proved, not counted)
   units carrying at least one runtime-callee row 3927
   runtime-callee rows in total 49362

   callee (typed producer)       units       rows  by language
   __extendhfsf2                  1398      11540  {"c": 551, "cpp": 834, "swift": 13}
   __truncsfbf2                    920       8424  {"c": 387, "cpp": 533}
   __truncsfhf2                    911       8036  {"c": 382, "cpp": 524, "swift": 5}
   __netf2                         530       5360  {"c": 147, "cpp": 383}
   __floatsitf                     310       1860  {"c": 120, "cpp": 190}
   ...
   __floattisf                      88        528  {"c": 40, "cpp": 48}
   __floattidf                      44        264  {"c": 20, "cpp": 24}
```

and the store the part-run left, counted by the same key:

```
records 2132
states {'TERM': 2097, 'NO_TERM': 35}
runtime rows {'none': 2100, 'with_runtime_rows': 32}
```

GLOSS, values in motion:

- canon40 has **3,927 units carrying a runtime-callee row, of 30,324
  proved — 12.95%** — over 30 distinct callees, **49,362 rows**. Task
  78's corrected destination rule took that row count from **608 to
  49,362**, a factor of **81**.
- Every one of those 3,927 units makes `Term.runtime_row` walk an
  attached body symbolically, once per row, and then makes the gate
  solve over the result.
- The part-run's 2,132 records contained **32 of those 3,927 — 0.8% of
  them, and 1.5% of its own records.** It walked the corpus's easy end
  and finished in 147 s. The 322 shards left hold the other **3,895**.
- That is the whole of why the schedule and the memory both changed
  character between 2026-09-03 and 2026-09-04, and neither is a defect
  in this run.

## 3.5 What was rolled back, and what stands

Records produced by a bound that fired must not sit in the store where
a resume would take them as done. They are also artifacts, and a
defective artifact stays as a record.

LITERAL — `<runs>/t83/agent/logs/20260904T195958Z__t83_l20_rollback.sh.log`:

```
======== [1/4] the store as it stands ========
shards 18, records 2701
state done: 18
...
   8 shards, 569 records preserved
...
   state done is now 10
======== [4/4] the store restored to the handoff state ========
shards 10, records 2132
records naming MemoryError: 0
```

GLOSS.

- The eight shards this session wrote (`op_units2_c_c0004` through
  `c0011`, **569 records**) are **copied byte for byte** into
  `term66_store_bound_fired_records/`, with a `README_why.json` saying
  what they are, and are then removed from `term66_store` and from
  `term66_state.json`.
- `term66_store` is back to **exactly the handoff state: 10 shards,
  2,132 records, 0 records naming a memory failure.** The ten
  host-written shards were not touched.
- So the corpus is where task 83 found it, plus a record of why it
  could not go further, and no downstream artifact was built on
  anything the bound touched.

---

# 4. What the brief asked for, item by item

| # | asked for | state |
|---|---|---|
| 1 | `term66` completed over the newest canon, with the canon named | canon40 CONFIRMED as the newest canon and named (§1.1). The run is **NOT complete** and cannot be completed under the round's 6 GB cap (§3). |
| 2 | `name_census7.json` | NOT PRODUCED — it filters `term66_store`, which is not complete. `name_census7.py` was read, is correct as it stands, and was not modified. |
| 3 | `the_pool6.json`, `the_families6.json`, `exception_families6.json` | NOT PRODUCED — `pool66_run.py` refuses by design when a canon40-proved unit has no layer-4 record, and 28,192 of them do not. |
| 4 | the four term states per population against 26,594 / 3,134 / 285 / 419 | NOT PRODUCED over a complete canon40 store. `audit66.json` on disk is the part-run's figure over a store built BEFORE the relink fix and is **not** this round's answer; it was deliberately not overwritten (§4.1). |
| 5 | the pool delta against 1,831 / 30,432 / 490 / 3 / 34 | NOT PRODUCED, for the same reason as item 3. |
| 6 | E00029's successor printed | NOT PRODUCED — it is read off `the_pool6.json`. |
| 7 | the consistency line pasted | NOT PRODUCED over canon40 — it is `audit66.py`'s output over a complete store. |

## 4.1 Why `audit66.json` was NOT re-run, and what it currently says

`audit66.py` writes `audit66.json` and `audit66_printed.txt` in place.
The copy on disk was produced on 2026-09-03 over a term66_store built
**before** the relink fix, and the part-run preserved that state as
`audit66_before_the_relink_fix.json` precisely so `audit66.py` could be
re-run. Re-running it over a 2,132-record store would have overwritten
the only figure on disk with one computed over 7% of its own stated
population, so it was not run. The lane that would have run it,
`t83_l13_downstream.sh`, refuses outright when the store is incomplete
and was never allowed to start.

For the record, the numbers `audit66_printed.txt` currently holds —
26,152 proved / 160 disproved / 50 undecided / 3,962 no term over
30,324 — are the PRE-FIX figure, and `probe83_relink_readings.json`
already measured that 3,927 of those 3,962 no-term units re-walk
cleanly once the relink is handed the readings. **They are not this
round's answer and must not be banked as one.**

---

# 5. The guard

The unmodified `check_no_spelling_keys.py`, ONE process, over every
JSON artifact task 83 wrote — the four probe results, the resume state,
the part-run's three artifacts, all ten shards of `term66_store` and
all nine files of `term66_store_bound_fired_records`. Nothing added to
any field set, no carve-out declared, no artifact put out of the walk,
the stores walked shard by shard rather than sampled.

LITERAL — `<runs>/t83/agent/logs/20260904T200124Z__t83_l22_guard.sh.log`:

```
[1/4] the guard, one process, nothing skipped
TASK 83: 27 paths  PASS 27  FAIL 0  exempt 0  exit 0
-- exit 0

[2/4] the command the guard ran
command: /opt/venv/bin/python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/op_pipeline/term66_state.json ... (27 paths)

[3/4] grep -c exempt over the guard's own output
0
```

and the head of the transcript itself:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS term66_state.json -- no operator token in any key, grouping, pairing or row structure
PASS audit66.json -- no operator token in any key, grouping, pairing or row structure
PASS audit66_before_the_relink_fix.json -- no operator token in any key, grouping, pairing or row structure
PASS probe83_relink_readings.json -- no operator token in any key, grouping, pairing or row structure
PASS probe83d_callee_population.json -- no operator token in any key, grouping, pairing or row structure
PASS probe83e_callee_bodies.json -- no operator token in any key, grouping, pairing or row structure
PASS probe83f_one_unit_trace.json -- no operator token in any key, grouping, pairing or row structure
PASS probe83g_ceiling.json -- no operator token in any key, grouping, pairing or row structure
```

GLOSS. **27 paths, 27 PASS, 0 FAIL, exit 0, and `grep -c exempt` over
the guard's own output is 0.** The first run of the guard
(`t83_l21_guard.sh`) passed identically but returned `grep -c
exempt` = 1, and the reason was the driver's own heading sentence,
which contained the word inside "exemption". The heading now says
"carve-out"; nothing about the walk changed. Both runs are on disk.

---

# 6. The standing requirements

## 6.1 All compute ran as Airlock lanes

Instance `t83`, brought up from
`PUBLIC/Airlock/instances/t83.conf` (cpus 4, memory 8g, proxy
off, poll watch, script_timeout 21600). Every computation in this
report is a lane; the lane scripts live in the project's own repo at
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/lanes_t83/`, are
dropped by `airlock submit`, and their logs are cited by path in every
section above.

The project tree mounts read-write at `PseudoCoupHQ`, so the
lanes read and write the real artifacts and nothing is shuffled through
`/out`.

## 6.2 One process

`term66_run.run` is one process with no worker pool and no second
interpreter, and `term66_bounded.py` does not change that: it sets
`RLIMIT_AS` and calls `term66_run.run` in the same process. The
downstream steps each run as their own single process, in order, in
lane `t83_l13_downstream.sh`. The spelling guard is run as ONE process
over every artifact at once, as §6.4 pastes.

## 6.3 Which files were EDITED rather than added

**None of the pipeline was edited.** `term66_run.py`, `term.py`,
`gate.py`, `reference.py`, `ledger.py`, `canonical_form.py`,
`pool.py`, `pool65_run.py`, `regate64_run.py`, `audit66.py`,
`name_census7.py`, `pool66_run.py` and `pool6_prediction_check.py` are
all as the part-run left them and were run, not modified. §1.4 pastes
the modification times.

Every file this task wrote is NEW, and every one is named in §8,
including the probes that only measured and the lane that had to be
re-submitted because of a wrong argument.

`guard83.py` is the one pre-existing artifact this task did NOT run,
and the reason is recorded in `guard83_term_pool.py`'s own docstring:
its walk list names `render_back82_tally.json`,
`render_back82_state.json` and `render_back82_store/` — the render_back
task's products, which task 83 does not write — so as it stands it
refuses for a missing artifact that is not its own. A superseded
artifact is never edited, so it stays on disk exactly as it is and the
walk task 83 actually owes was written as a new file.

---

# 7. Flagged for the owner, decided by nobody here

Both of these are findings the measurements forced, and both are
architecture or rule questions that belong to the owner. Neither was acted
on beyond measuring it.

## 7.1 The gate's limit is a wall clock, so a verdict near it is a
## function of the machine

- MEASURED, §2.9: over 241 records re-transcribed with unchanged code,
  **4 differ from the store (1.66%)**; three keep their verdict and
  differ only in which counterexample the solver returned; **one,
  `go/op_103`, moves DISPROVED → UNDECIDED (0.41%)** because
  `gate.SOLVER_MILLISECONDS = 3000` is wall-clock and this container
  did not finish inside it.
- WHY IT IS NOT A DEFECT IN THE GATE'S RULE: the rule that a timeout
  is UNDECIDED and never DISPROVED is right and is what keeps the
  consistency line honest. The issue is only that the limit is
  measured in milliseconds of a particular machine.
- WHY IT IS DEE'S: any answer changes what a verdict MEANS — a
  deterministic budget (solver steps or conflicts rather than
  milliseconds), a recorded machine identity on each verdict, or
  leaving it as is and stating the reproducibility figure with each
  bank. Choosing one is an ontology decision.
- WHAT IT COSTS TODAY: `term66_store` is not homogeneous. Ten of its
  332 shards were walked on the host and 322 in the t83 container. The
  brief said to resume and not to re-transcribe what is done, so that
  is what was done; the size of the effect is the 1.66% above, and it
  is recorded rather than repaired.

## 7.2 THE HEADLINE: canon40's transcription does not fit the round's
## own 6 GB memory cap, and no ceiling this instance allows converges

This is the blocker the task stopped on, and it is the brief's own
stop condition — *"the memory cap aborts"*.

- MEASURED, §3.1–§3.3, over stated populations:
  - **3,927 of the 30,324 units canon40 proves (12.95%) carry a
    runtime-callee row**, 49,362 rows over 30 distinct callees. Task
    78's corrected destination rule took that from **608 rows to
    49,362 — a factor of 81**.
  - Those units are what costs. `op_units2_c_c0004` walks **24 records
    in 1,112 s**; `c0005` walks **94 in 2 s**. Six shards took 2,234 s,
    which projects the remaining 316 at **about 32 hours** against a
    lane ceiling of six.
  - Under a 4096 MB ceiling the bound FIRES: **2 records of 2,701**
    carried `MemoryError` as their own written reason, because
    `Term.transcribe` records an exception raised while building a row
    as a HOLE. A record whose reason is the runner's memory limit is a
    record about the runner, not about the compiler.
  - The hard shard's records **never converge over the ceilings this
    instance allows** — 512, 1024, 2048, 4096 and 6144 MB. At 6144 MB
    the peak is 6,002,644 kB, pinned against its own ceiling again, and
    2 of 24 records still differ from what 4096 MB wrote.
- WHY IT IS DEE'S, and it is more than a resource question: the units
  that cost are exactly the ones round 12's standing resolution says to
  answer by attaching the callee's BODY, and `Reference.walk_body`
  answers by forking at every conditional transfer and merging the arms
  over the whole register file. Making that affordable means changing
  what the term for such a unit IS — a summarised callee, a bounded
  walk with a written refusal, a deterministic solver budget — and each
  of those changes what the corpus SAYS. None of them is a runner
  setting.
- WHAT WAS DONE INSTEAD OF DECIDING: nothing was changed and nothing
  was shipped. `term66_bounded.py` scans every record it writes for a
  memory failure that became a written reason and refuses its own
  output; the eight shards written before that scan could run were
  preserved as records and taken back out of the store (§3.5), which is
  now byte-identical in content to the handoff state.

## 7.3 The bound `term66_run.py` states cannot hold, and the CORE
## records the bound it states

- MEASURED, §2.1: `term66_run.check_memory` aborts by name at 6 GB but
  runs BETWEEN shards; the excursion is inside one, so the process
  reached 8,391,436 kB and was ABORTed by the container in 11 s with
  the check never firing.
- WHY IT IS DEE'S: the transcribe CORE records the between-shard
  `getrusage` check as the node's bound. The measurement says that
  shape of bound cannot hold for this node. A shape the tree lacks goes
  into the CORE first with provenance — so the replacement is not
  written here.
- WHAT IS KNOWN ABOUT THE REPLACEMENT, so the CORE entry has evidence:
  a hard `RLIMIT_AS` is a real bound and does fire (§3.2), but it fires
  by turning a term into a hole, so a bound of that shape needs a rule
  saying what a unit whose transcription hit the bound IS. That is the
  ontology question, and it is the same one §7.2 raises from the other
  side.

---

# 8. File inventory

Every file this task wrote is listed, including the probes that only
measured, the lane that had to be re-submitted, and the guard driver
that replaced one that could not run.

## 8.1 Written by this task — code, all NEW files

| path (under `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`) | what it is |
|---|---|
| `probe83b_memory.py` | one shard walked unit by unit with a 5 GB address-space bound, to locate the excursion by unit name |
| `probe83d_callee_population.py` | how many canon40-proved units reach `Term.runtime_row`, per attached callee, off the stored ledgers' typed producer objects |
| `probe83e_callee_bodies.py` | all 76 attached callee bodies walked through `Reference.walk_body`, one forked sub-process each, bounded at 4 GB and 120 s |
| `probe83f_one_unit_trace.py` | one unit's transcription traced row by row, resident size from `/proc/self/statm` and AST node counts per step |
| `probe83g_ceiling.py` | the same unit transcribed and gated at five ceilings, whole record read back at each |
| `term66_bounded.py` | `term66_run.run` called unmodified under `RLIMIT_AS`, plus the scan that refuses the output if a memory failure ever became a written reason, plus `--check` (re-transcribe stored shards into scratch and compare record for record) |
| `guard83_term_pool.py` | the UNMODIFIED `check_no_spelling_keys.py` over every JSON artifact task 83 writes, ONE process |

No pre-existing file was edited. `guard83.py` was NOT run and NOT
edited: its walk list names the render_back task's products, which task
83 does not write, so it refuses for a missing artifact that is not its
own (§6.3).

There is no `probe83c_*`; the letters follow the order the questions
were asked and `c` fell out when the callee-population probe was
renamed before it was written. `probe83_relink_readings.py` is the
part-run's own file from 2026-09-03 and is neither this task's nor
edited by it.

## 8.2 Written by this task — lanes

All under
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/lanes_t83/`; the lane
belongs to the project's repo, is dropped into Airlock, and its log is
the evidence.

| lane | what it did |
|---|---|
| `t83_l1_sample.sh` | path check, the imports each named, the canon check, the resume state; `/usr/bin/time` absent so it printed no peak |
| `t83_l2_sample.sh` | the sample re-run with the peak read by `resource.getrusage`; ABORTed at 8,391,436 kB in 11 s |
| `t83_l3_memory_probe.sh` | the excursion located at `c/regen_1859`, +4,883,500 kB |
| `t83_l4_callee_population.sh` | the population of units reaching `runtime_row` |
| `t83_l5_callee_bodies.sh` | all 76 attached bodies walked alone |
| `t83_l6_unit_trace.sh` | **superseded attempt** — passed the unit name without its language prefix and raised `KeyError: 'regen_1859'` in 0.2 s. Kept on disk as the record; nothing was written by it |
| `t83_l7_unit_trace.sh` | the same lane with `c/regen_1859`; the row-by-row trace |
| `t83_l8_ceiling.sh` | the five-ceiling test |
| `t83_l9_zero_regression.sh` | three stored shards re-transcribed under a 6 GB bound and compared record for record |
| `t83_l10_repeatability.sh` | the same bounded check run twice |
| `t83_l11_unbounded_control.sh` | the control at a 30,000 MB ceiling, which exonerated the bound |
| `t83_l12_term66_full.sh` | **superseded attempt** — the first full resume, at 4096 MB with a 20000 s budget, stopped by hand after ~4 min once lane 14's question arose. It wrote no store shard; the resume state was 10 before and 10 after |
| `t83_l14_ceiling_throughput.sh` | one shard at three ceilings, timed and compared |
| `t83_l15/16/17_term66_full.sh` | the full resume in three legs of 18000 s each, resuming from `term66_state.json` |
| `t83_l13_downstream.sh` | the audit, the census, the pool, the prediction check and the guard, in order, each under a 6 GB `ulimit -v`; refuses outright if the store is incomplete. **Never ran** — it was held out of the queue when §3 stopped the run, and its precondition would have refused anyway |
| `t83_l18_hard_shard_ceilings.sh` | the hard shard at 512 / 1024 / 2048 MB — fast, and half its records changed |
| `t83_l19_hard_shard_safety.sh` | why they differ, the store scanned for `MemoryError`, and 6144 MB against the shard 4096 MB wrote |
| `t83_l20_rollback.sh` | the eight shards written under the fired bound preserved as records and taken out of the store and the resume state |
| `t83_l21_guard.sh` | the guard, 27 of 27 PASS, but `grep -c exempt` = 1 from the driver's own heading word. **Superseded** |
| `t83_l22_guard.sh` | the guard again after the heading was reworded; 27 of 27 PASS, `grep -c exempt` = 0 |


## 8.3 Written by this task — artifacts

| path (under `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`) | what it holds |
|---|---|
| `probe83d_callee_population.json` | 3,927 of 30,324 canon40-proved units carry a runtime-callee row; 49,362 rows over 30 callees, per callee and per language |
| `probe83e_callee_bodies.json` | all 76 attached bodies walked alone: 60 walked, 16 refused by the opcode table, hungriest 56,676 kB / 0.21 s |
| `probe83f_one_unit_trace.json` | `c/regen_1859`'s transcription step by step, resident size and AST node counts |
| `probe83g_ceiling.json` | the same unit at five ceilings, whole record at each |
| `term66_store_bound_fired_records/` | the eight shards (569 records) written under the ceiling that fired, byte for byte, with `README_why.json` |
| `guard83_term_pool.json`, `guard83_term_pool_transcript.txt` | the guard's counts and its full output |
| `term66_bounded_scan.json` | written by the bounded runner's own refusal scan when a leg completes; the leg that would have written it was stopped, so the scan of §3.2 was run from `t83_l19` instead |

NOT written, and named here so the absence is explicit:
`name_census7.json`, `the_pool6.json`, `the_pool6_bytes.json`,
`the_families6.json`, `exception_families6.json`,
`pool5_pool6_delta.json`, `pool6_prediction_check.json`,
`the_pool6_entry_E00029_successor_printed.txt`. Each needs a complete
`term66_store` and none was built on a partial one.

`audit66.json` and `audit66_printed.txt` were NOT overwritten and
still hold the pre-relink-fix figure — see §4.1.

## 8.4 Plan files touched

| path | what was added |
|---|---|
| `Planning/.../node_0_3_5_6_term/node_0_3_5_6_2_transcribe/PROGRESS.md` | four dated entries: the memory bound measured and its cause named; the ceiling's zero-regression result on the easy shards; the correction that it does not hold on the hard ones and no ceiling converges; and the wall-clock verdict flag |

---

---

# 9. Resume state

- `term66_state.json` lists **10 done inputs of 332** — the six
  top-level canon40 files and `op_units2_c_c0000..c0003`. Byte for
  byte the state task 83 received.
- `term66_store/` holds **10 shards, 2,132 records, 0 naming a memory
  failure.**
- `term66_store_bound_fired_records/` holds the **8 shards, 569
  records** this session wrote under the ceiling that fired, unedited,
  with `README_why.json`. They are records, not corpus.
- **The 322 remaining inputs hold 3,895 of the 3,927 units that carry
  a runtime-callee row.** Resuming without answering §7.2 will meet
  the same wall on the first of them.
- Airlock instance `t83` was taken down at the end of the task.
