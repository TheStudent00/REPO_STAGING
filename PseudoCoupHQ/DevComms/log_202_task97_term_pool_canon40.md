# log 202 — task 97: the term walk finished over canon40, the census, and where the pool stops

Date: 2026-09-05. Round 19, TASK 97. Nodes:
`hq.research.compiler_graph.term` (0_3_5_6) with its sub-nodes
`transcribe` (0_3_5_6_2), `normalize` (0_3_5_6_3) and `census`
(0_3_5_6_4), and `hq.research.compiler_graph.pool` (0_3_5_7).

Appendix-B shape: one numbered tree, high to low, values in motion at
the leaves. §5.1a labels throughout: LITERAL is the stored object or
the pasted command output, GLOSS is what it means, ANALOGY is only ever
an aid and never the mechanism. Every count carries its population.
Every claim carries the command that produces it, with that
command's output pasted under it.

ALL COMPUTE RAN AS AIRLOCK LANES on instance `t97`. Not one line of
this task's analysis ran as host python. Every attribution below NAMES
ITS LANE LOG FILE.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line — not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention — never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

---

# 0. What was done, in plain words before any figure

- Task 83 stopped with **10 of 332 inputs transcribed** and projected
  the rest at **about 32 hours** against a six-hour lane ceiling
  (log_189 §3.1). This round walked the remaining 322 inputs in
  **581.7 seconds**, and §2 is why: task 83 priced the cost correctly
  and attributed it one step short.
- **The cost was the LIFETIME of the z3 context, not the unit.**
  `term66_run.run` builds one `Reference`, one `Term` and one `Gate`
  and pushes every unit of every shard through them, so each unit pays
  for everything the process built before it. `term97_walk.py` calls
  **the same `term66_run.one_unit`, unedited**, from a pristine parent
  that FORKS one sub-process per unit. Nothing about what a term IS
  changed.
- **the owner's two-pass rule was followed exactly.** Pass 1 at the ordinary
  budget walked **27,964 records** and FLAGGED **228**. Pass 2 re-ran
  all 228 with more time and more room: **184 changed answer and are
  stored**, **44 did not**. Not one record naming a runner limit was
  written into the store.
- **The 44 are not a schedule problem and not a sandbox problem.**
  Their layer-4 term is built and PROVED; it is **layer 5**, the
  normalizer, that does not converge. Measured at **1,536 / 4,096 /
  18,432 MB**: the peak pins against every ceiling
  (1,469,676 → 4,090,888 → 16,948,684 kB), the time grows with the
  ceiling, and the outcome is the same at every rung. A bigger machine
  buys nothing.
- **The four term states over canon40**, on a store of 30,280 of the
  30,324 units canon40 proves: **27,866 proved / 1,676 disproved / 253
  undecided / 485 no term**, against the round-14 line of 26,594 /
  3,134 / 285 / 419 over 30,432. Ten movement rows, each with its
  computed cause, in §5. The consistency line is **0**.
- **`name_census7.json` was produced**; `name_census7.py` was read
  first and was not modified.
- **The pool was NOT produced, and it was not worked around.**
  `pool66_run.py` refuses a member set short of the population it
  names, 44 units are short, and its own refusal is pasted in §6.
  `the_pool6.json`, `the_families6.json`, `exception_families6.json`,
  the pool delta and E00029's successor are therefore not on disk, and
  are named as absent rather than approximated.
- **One artifact carries a cause sentence this round's shortfall made
  wrong**, and §5.3 measures it rather than leaving it to be found:
  audit66.json's 156-unit row reads 112 genuine + 44 ours.
- Three things are FLAGGED for the owner in §9 and decided by nobody here.

```
$ sed -n '7,17p' /logs/20260905T095231Z__t97_l8_numbers.sh.log
canon40 inputs                       332
canon40 units attempted              31078
canon40 units proved (the population) 30324
term66_store shards                  332
term66_store records                 30280
term66_state.json done inputs        297
records short of the population      44
records pass 1 walked                27964
records carried in from the handoff  2132
records pass 2 added                 184
-- exit 0
```

---

# 1. The ground under the walk

## 1.1 Every import the walk needs is present

The stop rule says an absent import stops the task. None is absent.

LITERAL — lane log
`<runs>/t97/agent/logs/20260905T070502Z__t97_l1_sample.sh.log`,
lane `t97_l1_sample.sh` §1:

```
$ sed -n '6,22p' /logs/20260905T070502Z__t97_l1_sample.sh.log
======== 1. the imports the walk needs, each named ========
  OK      z3                               /opt/venv/lib/python3.13/site-packages/z3/__init__.py
  OK      canonical_form                   PseudoCoupHQ/Research/op_pipeline/canonical_form.py
  OK      gate                             PseudoCoupHQ/Research/op_pipeline/gate.py
  OK      reference                        PseudoCoupHQ/Research/op_pipeline/reference.py
  OK      regate64_run                     PseudoCoupHQ/Research/op_pipeline/regate64_run.py
  OK      term                             PseudoCoupHQ/Research/op_pipeline/term.py
  OK      pool                             PseudoCoupHQ/Research/op_pipeline/pool.py
  OK      pool65_run                       PseudoCoupHQ/Research/op_pipeline/pool65_run.py
  OK      pool66_run                       PseudoCoupHQ/Research/op_pipeline/pool66_run.py
  OK      ledger                           PseudoCoupHQ/Research/op_pipeline/ledger.py
  OK      dom_ops                          PseudoCoupHQ/Research/op_pipeline/dom_ops.py
  OK      normalize79_pool_prediction      PseudoCoupHQ/Research/op_pipeline/normalize79_pool_prediction.py
  OK      guard66                          PseudoCoupHQ/Research/op_pipeline/guard66.py
  OK      term66_run                       PseudoCoupHQ/Research/op_pipeline/term66_run.py
  OK      name_census7                     PseudoCoupHQ/Research/op_pipeline/name_census7.py
  OK      audit66                          PseudoCoupHQ/Research/op_pipeline/audit66.py
```

## 1.2 THE CORRECTED REFERENCE — this walk transcribes against it, and here is the proof

The brief: *"Transcribe against the CORRECTED reference (`reference.py`,
with the machine stack, the x87 stack and `SRem`/`URem`), and say so."*

**This walk transcribes against the corrected reference.** It is the
same file task 91 verified on 2026-09-05 — `reference.py` has not been
touched since 2026-09-03 17:19 UTC, which is BEFORE task 91 examined
it, so nothing about it moved between that verification and this walk.
Task 91's own finding was that the corrections were already on disk,
delivered by round 12's task 58 and round 13's task 64, and that what
was missing was the COREs' realization tables (log_196 §0.2 Part A and
Part B). LITERAL — the file's identity, printed inside the sandbox:

```
$ md5sum PseudoCoupHQ/Research/op_pipeline/reference.py
041eb9e38c7f515beebae7895641dfc9  PseudoCoupHQ/Research/op_pipeline/reference.py
```

LITERAL — the remainder whose sign follows the dividend. Lane
`t97_l1_sample.sh` §3 printed both halves with one combined pattern;
the two commands below print the same lines one pattern at a time:

```
$ grep -n "z3.SRem" PseudoCoupHQ/Research/op_pipeline/reference.py
1034:        remainder = z3.SRem(dividend, wide)
1094:        remainder = z3.SRem(dividend, grown)
```

```
$ grep -n "z3.URem" PseudoCoupHQ/Research/op_pipeline/reference.py
1038:        remainder = z3.URem(dividend, wide)
1098:        remainder = z3.URem(dividend, grown)
```

LITERAL — the machine stack and the x87 stack, built and printed off
`MachineState` itself, `t97_l1_sample.sh` §3:

```
$ sed -n '50,52p' /logs/20260905T070502Z__t97_l1_sample.sh.log
   MachineState().stack = {'pointer': seed_rsp, 'offset': 0, 'cells': {}}
   MachineState().x87   = {'slots': [None, None, None, None, None, None, None, None], 'top': 0, 'depth': 0}
   the stack and x87 methods: ['pop_value', 'push_value', 'stack', 'x87', 'x87_at', 'x87_pop', 'x87_push', 'x87_set']
```

GLOSS. Lines 1034 and 1094 are the same two lines log_196 §3.1 quoted
for the remainder fix; `MachineState` carries both stacks
with their eight x87 positions, their top index and their depth, which
is the object log_196 §3.2 printed. The reference this round walks is
that reference, unchanged.

## 1.3 canon40 is still the newest canon

LITERAL — `t97_l1_sample.sh` §2:

```
$ sed -n '28,37p' /logs/20260905T070502Z__t97_l1_sample.sh.log
-- canon41 present?
ls: cannot access 'canon41*': No such file or directory
-- the canon40 inputs the walk reads:
-rw-rw-r-- 1 root root   58534 Sep  4 03:33 canon40_interp.json
-rw-rw-r-- 1 root root 4968708 Sep  4 03:32 canon40_wrapped_c.json
-rw-rw-r-- 1 root root 6595089 Sep  4 03:33 canon40_wrapped_cpp.json
-rw-rw-r-- 1 root root  899255 Sep  4 03:33 canon40_wrapped_go.json
-rw-rw-r-- 1 root root  835699 Sep  4 03:33 canon40_wrapped_rust.json
-rw-rw-r-- 1 root root 1219609 Sep  4 03:33 canon40_wrapped_swift.json
-- regen shards: 326
```

## 1.4 The resume state at handoff, verified rather than assumed

LITERAL — `t97_l1_sample.sh` §4, before anything was written:

```
$ sed -n '55,66p' /logs/20260905T070502Z__t97_l1_sample.sh.log
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
-- store shards: 10, records: 2132
```

GLOSS. Exactly the state the brief describes and the state task 83
restored: **10 done inputs of 332, 2,132 records**. The walk resumed
from it and **re-transcribed none of it**, as the brief required. §3.4
counts what came from where.

---

# 2. What task 83 actually hit, named

Task 83 measured the cost correctly and attributed it one step short.
This section is the correction, and it is the whole reason the walk
fits now.

## 2.1 The sample, at the ordinary budget, before any walk

The round's memory rule asks for a sample with the peak resident size
pasted. `probe97a_unit_cost.py` walks a shard unit by unit, each unit
in a forked sub-process of its own, and reads each sub-process's peak
through `wait4`. The two shards chosen are the ones task 83 named as
the two extremes: `op_units2_c_c0004`, which it walked in 1,112 s, and
`op_units2_c_c0005`, which it walked in 2 s (log_189 §3.1).

LITERAL — `t97_l1_sample.sh` §5:

```
$ sed -n '68,105p' /logs/20260905T070502Z__t97_l1_sample.sh.log
======== 5. THE SAMPLE -- one hard shard and one easy shard, ========
========    one forked sub-process per unit                ========
-- the sample's own bound
   per-unit address-space ceiling 1536 MB
   per-unit wall clock 120 s, enforced by the parent with SIGKILL
   named abort if the PARENT passes 6 GB: ABORT_MEMORY_T97
-- setup: the three objects, built once in the parent
   attached callee units 4
   runtime answer readings 76
   setup 0.0 s, parent peak 57668 kB (was 55476 kB)

======== canon40_regen_store/op_units2_c_c0004.json ========
   units in the shard 50, canon40-proved 24
   c/regen_1859             MEMORY_REASON      0.66 s    1469000 kB  runtime rows 21
   c/regen_1869             MEMORY_REASON      0.59 s    1469884 kB  runtime rows 15
   c/regen_1870             MEMORY_REASON      0.58 s    1499036 kB  runtime rows 15
   c/regen_1874             MEMORY_REASON      0.58 s    1498720 kB  runtime rows 15
   c/regen_1875             MEMORY_REASON      0.59 s    1469556 kB  runtime rows 15
   c/regen_1879             MEMORY_REASON      0.60 s    1469724 kB  runtime rows 15
   c/regen_1880             MEMORY_REASON      0.60 s    1498684 kB  runtime rows 15
   c/regen_1881             MEMORY_REASON      0.62 s    1498572 kB  runtime rows 15
   c/regen_1882             MEMORY_REASON      0.59 s    1469772 kB  runtime rows 15
   c/regen_1886             MEMORY_REASON      0.63 s    1511768 kB  runtime rows 15
   c/regen_1891             MEMORY_REASON      0.60 s    1469944 kB  runtime rows 15
   -- over 24 proved units of this shard
      outcomes {"MEMORY_REASON": 11, "walked": 13}
      wall seconds  total 13.4  median 0.58  max 3.09
      child peak kB  median 89296  max 1511768

======== canon40_regen_store/op_units2_c_c0005.json ========
   units in the shard 100, canon40-proved 94
   c/regen_2079             MEMORY_REASON      0.66 s    1470460 kB  runtime rows 21
   -- over 94 proved units of this shard
      outcomes {"MEMORY_REASON": 1, "walked": 93}
      wall seconds  total 2.1  median 0.01  max 0.66
      child peak kB  median 57848  max 1470460

-- THE PARENT'S OWN PEAK RESIDENT SIZE 61748 kB
```

GLOSS, values in motion, and this is the finding the round turns on:

- `op_units2_c_c0004`'s **24 proved units took 13.4 seconds**. Task 83
  measured the same 24 records at **1,112 s** (log_189 §3.1). That is
  a factor of **83**, on the same shard, with the same code, in the
  same image.
- The PARENT's own peak over both shards is **61,748 kB** — 0.06 GB,
  against the round's 6 GB bound and the 816 MB the 2026-09-03
  part-run reached over ten inputs.
- **11 of the 24** proved units of the hard shard hit the 1,536 MB
  ceiling; **1 of the 94** of the easy shard did. §2.3 is what that
  flag actually names.

```
$ sed -n '92,105p' /logs/20260905T070502Z__t97_l1_sample.sh.log
   -- over 24 proved units of this shard
      outcomes {"MEMORY_REASON": 11, "walked": 13}
      wall seconds  total 13.4  median 0.58  max 3.09
      child peak kB  median 89296  max 1511768

======== canon40_regen_store/op_units2_c_c0005.json ========
   units in the shard 100, canon40-proved 94
   c/regen_2079             MEMORY_REASON      0.66 s    1470460 kB  runtime rows 21
   -- over 94 proved units of this shard
      outcomes {"MEMORY_REASON": 1, "walked": 93}
      wall seconds  total 2.1  median 0.01  max 0.66
      child peak kB  median 57848  max 1470460

-- THE PARENT'S OWN PEAK RESIDENT SIZE 61748 kB
```

## 2.2 The cost was the LIFETIME of the z3 context

`term66_run.run` builds ONE `Reference`, ONE `Term` and ONE `Gate` and
then walks every unit of every shard through them. z3's context is
global to the process: every AST node any unit ever built stays in it,
and `Term.normalize` calls `z3.simplify` twice over a structure that
grows with everything the process built earlier. So **the same unit
costs differently depending on what came before it in the same
process** — a property of the runner, not of the unit.

`term97_walk.py` changes only that. It **imports and calls
`term66_run.one_unit`; it does not re-type it and it does not edit
`term66_run.py`.** A pristine parent builds the same three objects
once and forks one sub-process per unit; the sub-process inherits them
copy-on-write, answers one unit and ends. The parent does no z3 work
after setup.

Same function, same reference, same gate, same ledger, same
population. Nothing about what a term IS changed.

## 2.3 The layer where the memory actually goes, and the token that was WRONG

Task 83 traced `c/regen_1859` row by row, found the transcription never
passed 50 MB, and concluded the memory was spent "in the gate, where
z3 solves the obligation" (log_189 §2.5). **It is not the gate.**

The first draft of this round's memory scan looked for five tokens,
one of which was `canceled`. That token is also z3's own word for a
solver that spent its WALL CLOCK — a legitimate UNDECIDED verdict, not
a memory limit — so a scan carrying it would have flagged honest
verdicts as runner failures. `probe97b_flag_reason.py` was written to
print WHICH token fired and on WHAT FIELD before any walk used the
list, and `canceled` was removed on the evidence.

LITERAL — lane log
`<runs>/t97/agent/logs/20260905T070634Z__t97_l2_flag_reason.sh.log`,
lane `t97_l2_flag_reason.sh`, the unit task 83 traced:

```
$ sed -n '7,30p' /logs/20260905T070634Z__t97_l2_flag_reason.sh.log
-- the unit c/regen_1859 of canon40_regen_store/op_units2_c_c0004.json
   body lines 16, ledger rows 32, runtime-callee rows 21
   setup done, attached callee units 4, readings 76

======== ceiling 1536 MB ========
   outcome MEMORY_REASON, wall 0.70 s, child peak 1468676 kB
   term_state TERM, verdict PROVED_ON_SHIP, proved True, holes 0
   reason: z3 proved the ledger-transcribed OUT-0 term equal to the value the unit's own ship body leaves in its own answer home, for every value of every register either side reads before writing
   TOKEN 'MemoryError' fired on:
      .layer5_refusal = MemoryError: 

======== ceiling 3072 MB ========
   outcome MEMORY_REASON, wall 1.20 s, child peak 3061392 kB
   term_state TERM, verdict PROVED_ON_SHIP, proved True, holes 0
   reason: z3 proved the ledger-transcribed OUT-0 term equal to the value the unit's own ship body leaves in its own answer home, for every value of every register either side reads before writing
   TOKEN 'MemoryError' fired on:
      .layer5_refusal = MemoryError: 

======== ceiling 6144 MB ========
   outcome MEMORY_REASON, wall 2.50 s, child peak 5994652 kB
   term_state TERM, verdict PROVED_ON_SHIP, proved True, holes 0
   reason: z3 proved the ledger-transcribed OUT-0 term equal to the value the unit's own ship body leaves in its own answer home, for every value of every register either side reads before writing
   TOKEN 'MemoryError' fired on:
      .layer5_refusal = MemoryError: 
```

GLOSS, values in motion.

- The field is **`layer5_refusal`** — written by
  `term66_run.add_layer5`, which calls `Term.normalize`, which calls
  `z3.simplify`. The **term is built and the gate PROVES it** before
  the normalizer is ever reached: `term_state TERM`, `verdict
  PROVED_ON_SHIP`, `holes 0`, at every ceiling.
- `term.py`'s own docstring calls layer 5 "a COMPARISON KEY computed
  beside the runnable text, never instead of it". So a unit flagged
  this way **already has its layer-4 answer**; what is missing is the
  key.
- The **peak follows the ceiling** — 1,468,676 / 3,061,392 /
  5,994,652 kB — and so does the time — 0.70 / 1.20 / 2.50 s. That
  shape is a runaway filling whatever it is given, not a computation
  that needs a particular amount.

## 2.4 And a second unit at the same three ceilings, which does converge

LITERAL — the same lane, `c/regen_1869`:

```
$ sed -n '37,61p' /logs/20260905T070634Z__t97_l2_flag_reason.sh.log
[2/2] c/regen_1869 -- a second of the eleven
-- the unit c/regen_1869 of canon40_regen_store/op_units2_c_c0004.json
   body lines 16, ledger rows 29, runtime-callee rows 15
   setup done, attached callee units 4, readings 76

======== ceiling 1536 MB ========
   outcome MEMORY_REASON, wall 0.62 s, child peak 1469640 kB
   term_state TERM, verdict PROVED_ON_SHIP, proved True, holes 0
   reason: z3 proved the ledger-transcribed OUT-0 term equal to the value the unit's own ship body leaves in its own answer home, for every value of every register either side reads before writing
   TOKEN 'MemoryError' fired on:
      .layer5_refusal = MemoryError: 

======== ceiling 3072 MB ========
   outcome walked, wall 123.82 s, child peak 1993856 kB
   term_state TERM, verdict PROVED_ON_SHIP, proved True, holes 0
   reason: z3 proved the ledger-transcribed OUT-0 term equal to the value the unit's own ship body leaves in its own answer home, for every value of every register either side reads before writing

======== ceiling 6144 MB ========
   outcome walked, wall 139.75 s, child peak 1993756 kB
   term_state TERM, verdict PROVED_ON_SHIP, proved True, holes 0
   reason: z3 proved the ledger-transcribed OUT-0 term equal to the value the unit's own ship body leaves in its own answer home, for every value of every register either side reads before writing

-- does the ceiling change the record?
   ceilings that returned a record 3 of 3
   distinct records among them 2
```

GLOSS, and this is the pair of shapes the whole round rests on.

- At 1,536 MB the normalizer refuses. At 3,072 MB it **walks**, in
  123.82 s, peaking at **1,993,856 kB**. At 6,144 MB it walks again,
  peaking at **1,993,756 kB** — the SAME number, 100 kB lower, with
  twice the room available.
- A peak that stops moving when the ceiling doubles is a **measured
  need**, not an appetite. This unit needs about 1,994 MB and takes
  about two minutes, and more room buys it nothing.
- The two records at 3,072 and 6,144 MB are **identical** — that is
  what "3 records returned, 2 distinct" says: the refusal, and one
  answer shared by both ceilings above it.
- So the population is **bimodal**: a unit either converges at about
  2 GB, or its peak pins against every ceiling it is ever given. §4
  measures which units are which, over the whole population.

---

# 3. PASS 1 — the ordinary budget, by the owner's rule

the owner, 2026-09-04: *"if it timed out, why not have all those flagged for
things to either have a look at after or just re-run with the rest of
them and give them a longer processing time to see if it changes the
result?"*

## 3.1 The budget, and why each number

| what | pass 1 | why that number |
|---|---|---|
| per-unit address-space ceiling | **1,536 MB** | the sample's own ceiling; §2.4 shows a converging unit needs about 1,994 MB, so this is deliberately the ORDINARY budget and the expensive units are meant to flag |
| per-unit wall clock | **120 s** | the sample's slowest walked unit was 3.09 s |
| slices running side by side | **6** | 6 × 1,536 MB = 9,216 MB inside the instance's 16 GB at the time |
| parent bound | **6 GB**, named abort `ABORT_MEMORY_T97` | the round's own rule |

## 3.2 How a runner limit is kept out of a term's stated reason

Two independent guards, because `Term.transcribe` and
`term66_run.add_layer5` BOTH catch an exception raised while building
and record it as a written reason — which is exactly how `MemoryError`
got into two of task 83's records (log_189 §3.2):

1. **The wall clock is enforced from OUTSIDE.** The parent alarms and
   SIGKILLs; the sub-process never sees a deadline, so a spent budget
   cannot be caught and written down. A sub-process stopped this way
   returns nothing at all and its unit is flagged.
2. **Every returned record is SCANNED** for a memory failure that
   became a written reason — in a hole, a no-term reason, a relink
   refusal or a layer-5 refusal. A record carrying one is **NOT
   STORED**; its unit is flagged and re-run.

The store this round leaves carries **zero** such records, and §7.2
pastes the audit line that says so.

## 3.3 What pass 1 did

LITERAL — lane log
`<runs>/t97/agent/logs/20260905T071105Z__t97_l3_pass1.sh.log`,
lane `t97_l3_pass1.sh`, the six slice summaries:

```
$ sed -n '6,35p' /logs/20260905T071105Z__t97_l3_pass1.sh.log
======== slice 0 ========
[53/54] canon40_regen_store/op_units2_swift_c0001.json: 285 transcribed, 0 flagged, 0 canon40-not-proved skipped, parent peak 71464 kB (498s)
[54/54] canon40_regen_store/op_units2_swift_c0007.json: 12 transcribed, 0 flagged, 1 canon40-not-proved skipped, parent peak 71464 kB (498s)
-- slice 0: 4722 records walked, 54 flagged, wall 498 s, parent peak 71464 kB
-- wrote term97_flagged_slice0.json
======== slice 1 ========
[53/54] canon40_regen_store/op_units2_swift_c0002.json: 221 transcribed, 0 flagged, 0 canon40-not-proved skipped, parent peak 70848 kB (364s)
[54/54] canon40_regen_store/op_units2_swift_c0008.json: 0 transcribed, 0 flagged, 0 canon40-not-proved skipped, parent peak 70848 kB (364s)
-- slice 1: 4747 records walked, 23 flagged, wall 364 s, parent peak 70848 kB
-- wrote term97_flagged_slice1.json
======== slice 2 ========
[53/54] canon40_regen_store/op_units2_swift_c0003.json: 105 transcribed, 0 flagged, 0 canon40-not-proved skipped, parent peak 72008 kB (582s)
[54/54] canon40_regen_store/op_units2_swift_c0009.json: 0 transcribed, 0 flagged, 0 canon40-not-proved skipped, parent peak 72008 kB (582s)
-- slice 2: 4645 records walked, 43 flagged, wall 582 s, parent peak 72008 kB
-- wrote term97_flagged_slice2.json
======== slice 3 ========
[53/54] canon40_regen_store/op_units2_swift_c0004.json: 85 transcribed, 0 flagged, 72 canon40-not-proved skipped, parent peak 69520 kB (371s)
[54/54] canon40_regen_store/op_units2_swift_c0010.json: 0 transcribed, 0 flagged, 0 canon40-not-proved skipped, parent peak 69520 kB (371s)
-- slice 3: 4210 records walked, 25 flagged, wall 371 s, parent peak 69520 kB
-- wrote term97_flagged_slice3.json
======== slice 4 ========
[52/53] canon40_regen_store/op_units2_rust_c0004.json: 11 transcribed, 0 flagged, 0 canon40-not-proved skipped, parent peak 75764 kB (533s)
[53/53] canon40_regen_store/op_units2_swift_c0005.json: 77 transcribed, 0 flagged, 94 canon40-not-proved skipped, parent peak 75764 kB (534s)
-- slice 4: 4766 records walked, 59 flagged, wall 534 s, parent peak 75764 kB
-- wrote term97_flagged_slice4.json
======== slice 5 ========
[52/53] canon40_regen_store/op_units2_swift_c0000.json: 160 transcribed, 0 flagged, 21 canon40-not-proved skipped, parent peak 70728 kB (409s)
[53/53] canon40_regen_store/op_units2_swift_c0006.json: 21 transcribed, 0 flagged, 1 canon40-not-proved skipped, parent peak 70728 kB (409s)
-- slice 5: 4874 records walked, 24 flagged, wall 409 s, parent peak 70728 kB
-- wrote term97_flagged_slice5.json
```

LITERAL — the lane's own status file,
`<runs>/t97/agent/status/t97_l3_pass1.sh.status`:

```
$ sed -n '1,6p' /status/t97_l3_pass1.sh.status
script=t97_l3_pass1.sh
state=done
exit=0
started=2026-09-05T07:11:05+00:00
finished=2026-09-05T07:20:46+00:00
elapsed_s=581.7
```

GLOSS, with the population.

- **27,964 records walked and 228 flagged**, over the **28,192** units
  canon40 proves in the 322 inputs task 83 left (27,964 + 228 =
  28,192).
- **581.7 seconds** for the whole lane. Task 83 projected the same 316
  remaining inputs at **about 32 hours** (log_189 §3.1).
- The highest parent peak of the six is **75,764 kB**, against the
  stated 6 GB bound. `ABORT_MEMORY_T97` never fired.

```
$ grep elapsed_s /status/t97_l3_pass1.sh.status
elapsed_s=581.7
```

## 3.4 Every flagged unit, and the fact that they are all the same thing

LITERAL, and this is the block every figure in §3 can be re-run from:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/report97_numbers.py flags
flagged by pass 1                    228
flagged by the word pass 1 recorded  {"MEMORY_REASON": 228}
flagged by the token that fired      {"MemoryError": 228}
flagged by the term state pass 1 saw {"TERM": 228}
flagged by the verdict pass 1 saw    {"PROVED_ON_SHIP": 228}
flagged by runtime-callee row count  {"13": 28, "15": 184, "21": 16}
inputs holding a flagged unit        70
pass 1 slice parents, peak resident kB [69520, 70728, 70848, 71464, 72008, 75764]
```

GLOSS, values in motion.

- **All 228 of 228** were flagged for the same measured reason:
  `MemoryError`, and **all 228 already had `term_state TERM` and
  verdict `PROVED_ON_SHIP`**. Not one was flagged for a wall clock,
  an ABORT, or a raised exception. The whole flagged set is the layer-5
  normalizer and nothing else.
- Every one of the 228 carries **13, 15 or 21 runtime-callee rows** —
  a machine-form property of the unit's own ledger, read off the
  stored typed producer objects, never a token.
- They sit in **70 of the 322 inputs**.

---

# 4. PASS 2 — the flagged set, with more time and more room

## 4.1 The budgets, stated, and larger on both axes

| leg | ceiling | wall clock | slices | lane |
|---|---|---|---|---|
| pass 1 | 1,536 MB | 120 s | 6 | `t97_l3_pass1.sh` |
| pass 2, leg a | **4,096 MB** | **1,800 s** | 4 | `t97_l4_pass2.sh` |
| pass 2, leg b (the residue) | **18,432 MB** | **3,600 s** | 1 | `t97_l6_pass2_residue.sh` |

Leg a's 4,096 MB is above a MEASURED need, not a guess: §2.4 measured
a converging unit at 1,993,856 kB and showed its peak did not move when
the ceiling doubled. Leg b's 18,432 MB is the largest single ceiling
the instance's 20 GB can hold with a slice running alone.

The pass-2 slice is cut **by shard, never by row**, because a pass-2
record is merged back into the store shard pass 1 wrote, and two slices
holding rows of one shard would read and write one file at once.

## 4.2 What pass 2 did, and in which direction

LITERAL:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/report97_numbers.py pass2
term97_pass2_a_slice0.json       ceiling   4096 MB  wall  1800 s  flagged  68  stored  57  not finished  11
term97_pass2_a_slice1.json       ceiling   4096 MB  wall  1800 s  flagged  57  stored  43  not finished  14
term97_pass2_a_slice2.json       ceiling   4096 MB  wall  1800 s  flagged  46  stored  38  not finished   8
term97_pass2_a_slice3.json       ceiling   4096 MB  wall  1800 s  flagged  57  stored  46  not finished  11
term97_pass2_b_slice0.json       ceiling  18432 MB  wall  3600 s  flagged  44  stored   0  not finished  44
pass-2 rows over every leg           272
rows by the word the leg recorded    {"MEMORY_REASON": 88, "walked": 184}
where the stored ones landed         {"TERM / PROVED_ON_SHIP": 184}
units still not finished             44
   canon40_regen_store/op_units2_c_c0004.json c/regen_1859 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0004.json c/regen_1859 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0005.json c/regen_2079 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0005.json c/regen_2079 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0012.json c/regen_4995 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0012.json c/regen_4995 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0013.json c/regen_5215 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0013.json c/regen_5215 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0020.json c/regen_8131 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0020.json c/regen_8131 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0020.json c/regen_8351 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0020.json c/regen_8351 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0028.json c/regen_11267 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0028.json c/regen_11267 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0028.json c/regen_11487 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0028.json c/regen_11487 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0073.json c/regen_29511 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0073.json c/regen_29511 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0074.json c/regen_29731 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0074.json c/regen_29731 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0081.json c/regen_32647 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0081.json c/regen_32647 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0082.json c/regen_32867 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0082.json c/regen_32867 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0089.json c/regen_35783 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0089.json c/regen_35783 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0090.json c/regen_36003 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0090.json c/regen_36003 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0097.json c/regen_38919 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0097.json c/regen_38919 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0097.json c/regen_39139 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0097.json c/regen_39139 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0105.json c/regen_42055 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0105.json c/regen_42055 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0105.json c/regen_42275 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0105.json c/regen_42275 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0112.json c/regen_45191 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0112.json c/regen_45191 MEMORY_REASON at 18432 MB and 3600 s
   canon40_regen_store/op_units2_c_c0113.json c/regen_45411 MEMORY_REASON at 4096 MB and 1800 s
   canon40_regen_store/op_units2_c_c0113.json c/regen_45411 MEMORY_REASON at 18432 MB and 3600 s
```

GLOSS, with the population and the direction the brief asked for.

- **228 units were flagged. 184 changed answer** — from a record the
  scan refused, to a record that walked clean and is stored. **44 did
  not.**
- **The direction is one direction only.** Every one of the 184 landed
  on `TERM / PROVED_ON_SHIP` — the same term state and the same verdict
  pass 1 had already seen before the normalizer refused. Not one unit
  moved to DISPROVED, to UNDECIDED, or to NO_TERM. What the larger
  budget bought was the layer-5 key, not a different answer.
- **184 of 228 is 80.7%** of the flagged set, **0.65%** of the 28,192
  units the two passes walked.
- Leg b took the 44 leg a could not finish, gave them **4.5× the room
  and 2× the clock**, and **0 of 44 changed**.

## 4.3 The 44, and why a bigger machine buys nothing

LITERAL — lane log
`<runs>/t97/agent/logs/20260905T094242Z__t97_l6_pass2_residue.sh.log`,
lane `t97_l6_pass2_residue.sh`, its last rows and its summary:

```
$ sed -n '56,59p' /logs/20260905T094242Z__t97_l6_pass2_residue.sh.log
-- PASS 2 over 44 flagged units
   changed answer 0
   now stored     0
   still not finished 44
```

LITERAL — the ceiling ladder for one of the 44, printed off the three
pass artifacts by lane `t97_l14_ladder.sh`, log
`<runs>/t97/agent/logs/20260905T100550Z__t97_l14_ladder.sh.log`:

```
$ sed -n '6,9p' /logs/20260905T100550Z__t97_l14_ladder.sh.log
the ceiling ladder for c/regen_1859
   pass 1  ceiling   1536 MB   peak   1469676 kB   wall   0.96 s   MEMORY_REASON
   pass 2  ceiling   4096 MB   peak   4090888 kB   wall   3.29 s   MEMORY_REASON
   pass 2  ceiling  18432 MB   peak  16948684 kB   wall   7.96 s   MEMORY_REASON
```

GLOSS, and this is the finding, not an excuse.

The same unit's peak across the three rungs, read off the three
artifacts: **1,469,676 kB at a 1,536 MB ceiling; 4,090,888 kB at 4,096
MB; 16,948,684 kB at 18,432 MB.** The peak is the ceiling, every
time, over a **12× range**. The wall time grows with the ceiling too —
0.96 s, 3.29 s, 7.96 s — which is what a runaway allocating as fast as it
can looks like.

```
$ sed -n '25,29p' /logs/20260905T070634Z__t97_l2_flag_reason.sh.log
======== ceiling 6144 MB ========
   outcome MEMORY_REASON, wall 2.50 s, child peak 5994652 kB
   term_state TERM, verdict PROVED_ON_SHIP, proved True, holes 0
   reason: z3 proved the ledger-transcribed OUT-0 term equal to the value the unit's own ship body leaves in its own answer home, for every value of every register either side reads before writing
   TOKEN 'MemoryError' fired on:
```

That is **not the sandbox's limit**. A machine with a terabyte would
take longer to fail. `z3.simplify`, inside `Term.normalize`, does not
converge for these 44 terms. It is a fact about the NORMALIZE node and
the terms these units build, and §9.1 flags it for the owner rather than
answering it here.

**What was NOT done about it**, said explicitly because each of these
would have been a redefinition the brief forbids: no summarised callee;
no truncated walk; no bounded normalizer; no z3 resource limit that
would return a half-simplified text as if it were the key; and no
record carrying `MemoryError` written into the store.

## 4.4 THE CONTROL — does the larger budget change an answer that already existed?

the owner's rule has two halves. The second is "see if it changes the
result", and that has to be asked of the records the ORDINARY budget
already produced, not only of the flagged ones. Every 100th record in
the store was re-transcribed and re-gated at the pass-2 budget and
compared **field for field** against what is stored. The sample crosses
both halves of the store — the 10 inputs walked on the host before this
round, and the 322 walked here — so the store's own inhomogeneity
(log_189 §7.1) is measured rather than assumed.

LITERAL — lane log
`<runs>/t97/agent/logs/20260905T094744Z__t97_l7_finalize_and_control.sh.log`,
lane `t97_l7_finalize_and_control.sh`:

```
$ sed -n '50,56p' /logs/20260905T094744Z__t97_l7_finalize_and_control.sh.log
======== [2/2] the control ========
-- THE CONTROL: every 100th stored record re-run at the pass-2 budget
   ceiling 4096 MB, wall clock 1800 s
   records compared 302
   records identical 302
   records that differ 0
-- wrote term97_control.json
```

GLOSS, against its population and against the two figures the brief
named.

- **302 of 302 records identical, 0 differ.** The larger budget
  changes nothing that the ordinary budget already answered.
- Task 91 measured its wall-clock control at **17 of 30,436 (0.06%)**.
  Task 83 measured **4 of 241 (1.66%)**, of which **1 of 241 (0.41%)**
  changed state, when it compared a container run against records the
  HOST had written. This round's figure is **0 of 302 (0.00%)**, and
  the sample deliberately includes the host-written shards, so the
  difference is not a narrower sample.
- **What this rules out**: none of the movement in §5 is the wall
  clock. A movement whose cause could have been "the machine" would
  have shown here.

---

# 5. THE FOUR TERM STATES over canon40, with every movement's cause

## 5.1 The population this is stated against, said before any state

LITERAL:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/report97_numbers.py walk
canon40 inputs                       332
canon40 units attempted              31078
canon40 units proved (the population) 30324
term66_store shards                  332
term66_store records                 30280
term66_state.json done inputs        297
records short of the population      44
records pass 1 walked                27964
records carried in from the handoff  2132
records pass 2 added                 184
```

GLOSS. **Every number in §5 and §6 is stated over 30,280 records, of
the 30,324 units canon40 proves — 99.855%, short by the 44 of §4.3.**
2,132 came in from the handoff and were not re-transcribed, 27,964 came
from pass 1 and 184 from pass 2.
`term66_state.json` lists **297 of 332** inputs done, not 332, because
an input is written into it only when EVERY unit canon40 proves in it
has a record. The 44 are spread over 35 inputs, so those 35 are left
out and a later resume picks them up rather than reading a gap as an
answer.

```
$ python3 -c "import json;d=json.load(open('PseudoCoupHQ/Research/op_pipeline/term97_finalize.json'));print('inputs complete',d['inputs_complete'],'of',d['inputs_total'],'| inputs short',len(d['inputs_short']),'| records in store',d['records_in_store'])"
inputs complete 297 of 332 | inputs short 35 | records in store 30280
```

## 5.2 The four states, and the ten movements

LITERAL:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/report97_numbers.py states
the round-14 line, over 30432 records
   proved 26594  disproved 3134  undecided 285  no term 419
term66 over canon40, over 30280 records
   proved 27866  disproved 1676  undecided 253  no term 485
units proved on one route and disproved on the other 0
layer 5: proved terms 27866, with a normalized text 27866, refused 0, distinct texts 972
movement rows recorded                10
units carried by those rows           30436
    26594 units | was proved     now proved     | no movement -- the state is the same in both rounds
     1674 units | was disproved  now disproved  | no movement -- the state is the same in both rounds
     1272 units | was disproved  now proved     | the ledger now rows the runtime transfer, so the term no longer asserts the transfer changed nothing (1272 of 1272 carry a runtime row in canon40)
      419 units | was no term    now no term    | no movement -- the state is the same in both rounds
      221 units | was undecided  now undecided  | no movement -- the state is the same in both rounds
      156 units | was disproved  now not in canon40's proved set | canon40 did not prove this unit's WRAPPED TEXT, so it was never transcribed this round; the layer-3 route is where it stopped, not the term route
       62 units | was undecided  now no term    | the transcription changed under canon40's ledger (62 of 62 carry a runtime row in canon40)
       32 units | was disproved  now undecided  | the transcription changed under canon40's ledger and neither route answered inside its limit (19 of 32 carry a runtime row in canon40)
        4 units | was not in canon39's proved set now no term    | canon39 did not prove this unit's WRAPPED TEXT, so term65 never transcribed it; canon40 proves it and the term route reaches it for the first time
        2 units | was undecided  now disproved  | the transcription changed under canon40's ledger and the gate now finds a starting state under which the term and the unit's own machine code differ (0 of 2 carry a runtime row in canon40)
the four states per arrival population
   original     proved     term65   1665  term66   1665
   original     disproved  term65     49  term66     47
   original     undecided  term65     14  term66     14
   original     no term    term65     35  term66     35
   interpreter  proved     term65      9  term66      9
   interpreter  disproved  term65      0  term66      0
   interpreter  undecided  term65      0  term66      0
   interpreter  no term    term65      0  term66      0
   regenerated  proved     term65  24920  term66  26192
   regenerated  disproved  term65   3085  term66   1629
   regenerated  undecided  term65    271  term66    239
   regenerated  no term    term65    384  term66    450
what remains disproved, by computed cause
     1525 | the body transfers into the compiler's own runtime and canon40's ledger DID row it, one row per register family the attached callee changes; the disproof has another cause
      135 | the body does not transfer and the walk left a hole; the disproof is about a producer the one table has no builder for
       14 | the body transfers to a NAMED routine that is not a lowering -- a panic or abort path reached on a guard, so the disproof is about the guard's response and no runtime row is owed
        2 | the body transfers INDIRECTLY through memory, so the target is not statically named and no runtime row could be made for it
```

GLOSS, with each side's own population and each movement's cause.

- **The round-14 line reproduces exactly** off `term65_store`:
  26,594 / 3,134 / 285 / 419 over 30,432. This round did not carry
  those numbers forward from a log; `audit66.py` recomputed them off
  the store.
- **term66 over canon40, over 30,280 records: 27,866 proved / 1,676
  disproved / 253 undecided / 485 no term.**
- The single largest movement is **1,272 units disproved → proved**,
  and its cause is computed rather than told: **1,272 of 1,272 carry a
  runtime-callee row in canon40.** That is task 78's corrected
  destination rule landing — the ledger now rows the transfer into the
  compiler's own runtime, so the term stops asserting that the transfer
  changed nothing.
- **The reference was fixed, not the wall clock moved.** §4.4's control
  is 0 of 302, so no part of the movement above is the machine. The
  two rows whose cause could otherwise have been read as timing are
  the 32 `disproved → undecided` (19 of 32 carry a runtime row, so the
  transcription changed under them) and the 2 `undecided → disproved`
  (0 of 2 carry a runtime row).
- **THE CONSISTENCY LINE IS 0** — no unit is proved on one route and
  disproved on the other, over 30,280 records.

```
$ sed -n '38,47p' /logs/20260905T095120Z__t97_l10_downstream_partial.sh.log

   ALL            proved          26594     27866   +1272
   ALL            disproved        3134      1676   -1458
   ALL            undecided         285       253     -32
   ALL            no term           419       485     +66
   ALL            TOTAL           30432     30280

   the round-13 line: 26,594 proved / 3,134 disproved / 285 undecided / 419 no term over 30,432
   term65_store reproduces:  26594 / 3134 / 285 / 419 over 30432
   term66 over canon40:      27866 / 1676 / 253 / 485 over 30280
```
- **Layer 5 over the store: 27,866 proved terms, 27,866 with a
  normalized text, 0 refused.** Zero refusals is the mechanical
  evidence that the store carries no record whose reason names a runner
  limit — because the 44 whose normalizer refused were never written.

## 5.3 THE ONE PLACE THIS ROUND'S SHORTFALL MADE A CAUSE SENTENCE WRONG

This is stated here rather than left for a reader to find.
`audit66.py` decides "not in canon40's proved set" by asking whether
the unit has a record in `term66_store`. 44 units have no record
because their layer-5 normalization does not converge, **not** because
canon40 refused them — so for those 44, the sentence
`audit66.json` now carries is false. LITERAL — lane log
`<runs>/t97/agent/logs/20260905T095648Z__t97_l11_contamination.sh.log`,
lane `t97_l11_contamination.sh`:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/report97_numbers.py contamination
the movement row, its population and its cause
   units 156
   was disproved, now not in canon40's proved set
   cause: canon40 did not prove this unit's WRAPPED TEXT, so it was never transcribed this round; the layer-3 route is where it stopped, not the term route
units this round could not finish             44
of the row's pasted sightings, how many are ours 8 of 8
canon40 units attempted                       31078
canon40 units proved                          30324
canon40 units NOT proved                      754
the row's units, less the ones we could not finish 112
```

GLOSS, and the corrected reading of that row:

- The row's population is **156**. **112** of them are the cause the
  row states — canon40 did not prove the wrapped text. **44** of them
  are this round's shortfall, and for those the row's cause is wrong.
- **All 8 of the 8 unit names the row pastes as sightings are ours**,
  which is why the row reads as it does: the sightings are the first
  eight by name and our 44 sort early.
- `audit66.json` on disk carries the uncorrected sentence. It was not
  hand-edited, because an artifact is not edited to say what its
  generator did not compute. The correction lives here and in §9.2.

---

# 6. The pool: where it stops, in its own words

## 6.1 The strict lane refused before anything was overwritten

LITERAL — lane log
`<runs>/t97/agent/logs/20260905T095100Z__t97_l5_downstream.sh.log`,
lane `t97_l5_downstream.sh`, which is the downstream lane with its
precondition intact:

```
$ sed -n '6,8p' /logs/20260905T095110Z__t97_l5_downstream.sh.log
resume state: 297 of 332 inputs transcribed
REFUSED: term66_store is incomplete (297 of 332 inputs).
Nothing downstream is run and no artifact is overwritten.
```

## 6.2 `pool66_run.py` refuses its own output, and that refusal stands

The pool was then run anyway, so that its OWN guard — not a lane
precondition of ours — is the thing on the record.

LITERAL — lane log
`<runs>/t97/agent/logs/20260905T095120Z__t97_l10_downstream_partial.sh.log`,
lane `t97_l10_downstream_partial.sh`, step 3 of 4:

```
$ sed -n '323,329p' /logs/20260905T095120Z__t97_l10_downstream_partial.sh.log
======== [3/4] pool66_run.py -- the pool; its own refusal is the evidence ========
-- intake
   units in the pool 30324
   by arrival population {"interpreter": 9, "original": 1761, "regenerated": 28554}
   layer-4 records read 30280
REFUSED OWN OUTPUT: 44 proved units have no layer-4 record, first ['c/regen_1859', 'c/regen_2079', 'c/regen_4995']
-- exit 1
```

GLOSS. `pool66_run.py` will not build a pool over a member set short
of the population it names. **That refusal is correct and it was not
circumvented.** No new pool driver was written to walk around it; no
member was dropped from the population to make the counts agree; no
record was composed for the 44.

## 6.3 THE POOL DELTA, and what it is stated against

LITERAL:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/report97_numbers.py pool
the_pool6.json is NOT on disk.
pool66_run.py refused its own output: a pool cannot be built over a member set short of the population it names.
the pool5 line this round would have been read against:
   distinct_layer3_wrapped_texts                            2993
   distinct_layer5_texts_among_eligible_units               1267
   entries                                                  1831
   entries_carrying_more_than_one_wrapped_text               527
   entries_spanning_compiled_and_interpreted                   3
   entries_spanning_more_than_one_language                   490
   entries_under_the_brief_strict_rule                      5095
   layer3_identity_merges                                  27439
   layer5_identity_merges                                  25327
   members                                                 30432
   members_not_layer5_eligible                              3838
   members_whose_term_was_undecided                          285
   members_whose_term_was_withdrawn                         3134
   members_with_a_proved_term                              26594
   members_with_no_term                                      419
   proved_edges_applied                                      118
   families                                                   34
```

GLOSS. The brief's five reference figures — **1,831 entries / 30,432
members / 490 spanning more than one language / 3 spanning compiled and
interpreted / 34 families** — are confirmed on disk in `the_pool5.json`
and `the_families5.json`, and the delta against them **is not
computed**, because the object it would be computed from does not
exist. Nothing is estimated in its place.
**What IS known about where the pool would move**, from the layer-5
tally in §5.2, and stated as an input to the pool rather than as the
pool: term66 has **972 distinct layer-5 texts** against term65's
**1,267**, over 27,866 proved terms against 26,594. A pool built on
that would have fewer entries than 1,831. **That is not the delta and
must not be banked as one.**

```
$ python3 -c "import json;a=json.load(open('PseudoCoupHQ/Research/op_pipeline/the_pool5.json'))['summary'];b=json.load(open('PseudoCoupHQ/Research/op_pipeline/the_families5.json'))['summary'];print('entries',a['entries'],'| members',a['members'],'| more than one language',a['entries_spanning_more_than_one_language'],'| compiled and interpreted',a['entries_spanning_compiled_and_interpreted'],'| families',b['families'])"
entries 1831 | members 30432 | more than one language 490 | compiled and interpreted 3 | families 34
```

## 6.4 E00029's successor is NOT printed

It is read off `the_pool6.json`, by `pool66_run.successor_of`, which
finds a successor **by member set and never by number**. The file does
not exist, so the successor was not printed and nothing was printed in
its place.

---

# 7. The census, and the store's own guards

## 7.1 `name_census7.py` was read first, and was not modified

The brief: *"a `name_census7.py` exists on disk; read it before writing
anything new."* It was read. It is correct as it stands, it was run
unmodified, and no new census driver was written.

LITERAL — `t97_l10_downstream_partial.sh` step 2 of 4, the head of the
census:

```
$ sed -n '129,148p' /logs/20260905T095120Z__t97_l10_downstream_partial.sh.log
======== [2/4] name_census7.py -- the census over term66_store ========
-- the population
   layer-4 records read (canon40 proved) 30280
-- the census over canon40
   producers 50
   rows blocked 4584
   units blocked 1220
   cascades (not census entries) 1059

   producer                                           rows    units  languages
   runtime_callee:__udivti3                            702       78  c,cpp,swift
   runtime_callee:__umodti3                            702       78  c,cpp,swift
   runtime_callee:__divti3                             666       74  c,cpp,swift
   runtime_callee:__modti3                             666       74  c,cpp,swift
   runtime_callee:__floatuntisf                        528       88  c,cpp
   flag_pair:test,js                                   320      320  c,cpp,swift
   runtime_callee:__floatuntidf                        264       44  c,cpp
   runtime_callee:__extendhfsf2                        125       13  swift
   flag_pair:test,jl                                   122      122  go
   flag_pair:test,je                                    80       80  go,rust,swift
```

LITERAL — the artifact it wrote:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/report97_numbers.py census
delta_against_census6                                       3 keys
entries                                                    50 rows
meta                                                        7 keys
tally                                                       5 keys
```

GLOSS. **`name_census7.json` is on disk, with 50 producer entries over
30,280 layer-4 records.** The census is a FILTER, not a survey: 4,584
rows over 1,220 units actually blocked, keyed by the typed producer
object of the unit's own body — `{kind, callee}` for a runtime callee,
`{kind, mnem}` for an arch opcode, `{kind, mnem: [setter, reader]}` for
a flag pair. Never an operator token.

## 7.2 The store carries no record whose reason names a runner limit

The mechanical statement is §5.2's layer-5 line, and it is worth
pulling out on its own because it is the whole point of the flag
machinery:

```
$ sed -n '98,98p' /logs/20260905T095231Z__t97_l8_numbers.sh.log
layer 5: proved terms 27866, with a normalized text 27866, refused 0, distinct texts 972
```

GLOSS. **0 normalization refusals over 27,866 proved terms.** Task 83's
store carried 2 records naming `MemoryError` in 2,701 (log_189 §3.2).
This one carries none in 30,280, because a record that named one was
flagged and re-run rather than stored, and the 44 that never resolved
were never written.

```
$ python3 -c "import json,glob;n=0;r=0;
for p in sorted(glob.glob('PseudoCoupHQ/Research/op_pipeline/term66_store/*.json')):
    d=json.load(open(p))
    for k in d['units']:
        r+=1
        if 'MemoryError' in json.dumps(d['units'][k]): n+=1
print('records in term66_store',r,'| records naming MemoryError',n)"
records in term66_store 30280 | records naming MemoryError 0
```

## 7.3 THE GUARD — unmodified, ONE process, over every artifact

LITERAL — `t97_l10_downstream_partial.sh` step 4 of 4 and the exempt
count:

```
$ sed -n '331,338p' /logs/20260905T095120Z__t97_l10_downstream_partial.sh.log
======== [4/4] guard97_term_pool.py -- the unmodified guard, ONE process ========
TASK 97: 349 paths  PASS 349  FAIL 0  exempt 0  exit 0
NOT ON DISK, named rather than skipped: the_pool6.json, the_pool6_bytes.json, the_families6.json, exception_families6.json, pool5_pool6_delta.json, pool6_prediction_check.json
-- exit 0

======== the guard transcript, and its exempt count ========
grep -c exempt over the guard's own output:
0
```

LITERAL — the guard run AGAIN over the FINAL artifact set, after this
log's own claims artifacts landed. Lane log
`<runs>/t97/agent/logs/20260905T101055Z__t97_l17_guard.sh.log`,
lane `t97_l17_guard.sh`:

```
$ sed -n '6,11p' /logs/20260905T101055Z__t97_l17_guard.sh.log
TASK 97: 351 paths  PASS 351  FAIL 0  exempt 0  exit 0
NOT ON DISK, named rather than skipped: the_pool6.json, the_pool6_bytes.json, the_families6.json, exception_families6.json, pool5_pool6_delta.json, pool6_prediction_check.json
-- exit 0

grep -c exempt over the guard's own output:
0
```

**351 paths, 351 PASS, 0 FAIL, 0 exempt, guard exit 0**, and
`grep -c exempt` over the guard's own output is **0**. That lane's own
footer reads `exit 1`, and the reason is stated rather than left: its
last command is `grep -c exempt`, and `grep` exits 1 when it counts
zero. The guard itself exited 0, on the line above.

GLOSS. **349 paths, 349 PASS, 0 FAIL, 0 exempt, exit 0, and
`grep -c exempt` over the guard's own output is 0.** The walk is every
JSON artifact task 97 writes plus **every one of the 332 shards of
`term66_store`, shard by shard and not sampled**. Nothing was added to
any field set, no carve-out was declared, and the six artifacts that do
not exist are NAMED in the guard's own output rather than passed over.

`guard83_term_pool.py` was neither run nor edited: its walk list names
task 83's own products and none of task 97's, so a new driver was
written and the superseded one stays on disk exactly as it is.

---

# 8. What the brief asked for, item by item

| # | asked for | state |
|---|---|---|
| 1 | `term66` completed over canon40, resumed, transcribed against the corrected reference | **30,280 of the 30,324 units canon40 proves (99.855%)**, in 332 of 332 store shards; the 10 handoff inputs were not re-transcribed; the corrected reference is identified by md5 and quoted in §1.2. **44 units short**, each reported by name in `term97_finalize.json` (§4.3). |
| 2 | two passes, the flagged set re-run, whether the answer changed | **DONE.** 228 flagged at 1,536 MB / 120 s; 184 changed answer and are stored at 4,096 MB / 1,800 s; 44 did not change at 18,432 MB / 3,600 s. Direction: all 184 landed on `TERM / PROVED_ON_SHIP` (§4.2). The control adds the other half of the rule: 302 of 302 stored records identical at the larger budget (§4.4). |
| 3 | `name_census7.json` | **DONE**, `name_census7.py` read first and not modified; 50 producers over 30,280 records (§7.1). |
| 4 | `the_pool6.json`, `the_families6.json`, `exception_families6.json` | **NOT PRODUCED.** `pool66_run.py` refuses a member set short of the population; its refusal is pasted in §6.2 and was not worked around. |
| 5 | the four term states against 26,594 / 3,134 / 285 / 419, with every movement's cause | **DONE**, over 30,280: **27,866 / 1,676 / 253 / 485**, ten movement rows each with a computed cause, and the "reference was fixed" versus "wall clock moved" separation carried by a control of 0 of 302 (§5.2, §4.4). One cause sentence is wrong for 44 units and §5.3 measures it. |
| 6 | the pool delta against 1,831 / 30,432 / 490 / 3 / 34 | **NOT PRODUCED**, for the same reason as item 4. The five reference figures are confirmed on disk (§6.3); nothing is estimated in their place. |
| 7 | E00029's successor printed, and the consistency line pasted | successor **NOT PRINTED** (it is read off `the_pool6.json`). **The consistency line IS pasted: 0** units proved on one route and disproved on the other, over 30,280 (§5.2). |

---

# 9. Flagged for the owner, decided by nobody here

## 9.1 THE HEADLINE — `Term.normalize` does not converge for 44 terms, and it is not a machine limit

- MEASURED, §2.3, §2.4, §4.3, over stated populations:
  - 228 of the 28,192 units the two passes walked (0.81%) had their
    layer-5 normalization refuse at 1,536 MB. **184 of them converge**
    given about 2 GB — measured at 1,993,856 kB, and the SAME peak,
    1,993,756 kB, when the ceiling was doubled to 6,144 MB.
  - **44 do not converge at any ceiling.** Their peak is the ceiling at
    1,536, 4,096 and 18,432 MB — 1,469,676 → 4,090,888 → 16,948,684 kB
    — and the wall time grows with it, 0.96 → 3.29 → 7.96 s.
  - Every one of the 44 has `term_state TERM` and verdict
    `PROVED_ON_SHIP` with **0 holes**. The TERM is proved. It is the
    COMPARISON KEY that is missing.
- WHY IT IS NOT A SANDBOX PROBLEM: a peak that tracks its ceiling over
  a 12× range, with time growing alongside, is a non-terminating
  rewrite, not a working set. A larger machine would fail later, not
  differently.
- WHY IT IS DEE'S: every answer changes what a record IS. A stated
  non-convergence outcome for layer 5, in this line's own vocabulary
  rather than the runner's exception word, would let the 44 into the
  store as members with no layer-5 key — the pool already handles a
  member that is not layer-5 eligible, and pool5 had 3,838 of them. But
  writing that sentence is composing a reason the generator did not
  compute, and naming an outcome is an ontology decision. **Nothing was
  composed and nothing was stored.**
- WHAT IT COSTS TODAY: items 4, 6 and 7 of the brief. 0.145% of the
  population is holding the pool.

## 9.2 `audit66.json` now carries a cause sentence that is wrong for 44 units

- MEASURED, §5.3: the row "was disproved, now not in canon40's proved
  set" has a population of **156**. **112** of them are the cause it
  states; **44** are this round's shortfall, and its 8 pasted sightings
  are 8 of 8 ours.
- WHY IT IS DEE'S: `audit66.py` infers "canon40 did not prove it" from
  "no record in the store", which was a safe inference while the store
  was either complete or absent, and is not one now. Whether that
  inference should be split — one outcome for a unit canon40 refused
  and another for a unit this line could not finish — is a change to
  what the audit's states MEAN.
- WHAT WAS DONE INSTEAD: the artifact was not hand-edited. The
  correction is measured, is in this log, and is reproducible by one
  command.

## 9.3 The store is now homogeneous, and the earlier flag can be closed

- Task 83 flagged (log_189 §7.1) that `term66_store` was not
  homogeneous: 10 shards walked on the host, the rest to be walked in a
  container, with 4 of 241 records differing and 1 of 241 changing
  state.
- MEASURED, §4.4: this round's control re-ran **302 records including
  the host-written shards** at the larger budget and found **302 of 302
  identical, 0 differing**. The 1.66% and the 0.41% do not reproduce
  under the fork-per-unit arrangement.

```
$ python3 -c "import json;d=json.load(open('PseudoCoupHQ/Research/op_pipeline/term97_control.json'));print('compared',d['compared'],'| identical',d['identical'],'| differ',d['differ'],'| ceiling MB',d['ceiling_mb'],'| wall clock s',d['seconds'])"
compared 302 | identical 302 | differ 0 | ceiling MB 4096 | wall clock s 1800.0
```
- WHY IT IS DEE'S ANYWAY: the underlying fact task 83 raised —
  `gate.SOLVER_MILLISECONDS = 3000` is a WALL CLOCK, so a verdict near
  it is a function of the machine — has not changed. This round only
  measured that no verdict in a 302-record sample is near it. Whether
  the budget should become deterministic is still open.

---

# 10. The fence, the memory bound, and the lanes

## 10.1 Every computation ran in Airlock, instance `t97`

Instance `t97` was created by copying `PUBLIC/Airlock/instances/t87.conf`
to `instances/t97.conf` and rewriting its header, as the brief
required. Every lane was dropped with
`./airlock submit <lane.sh> --instance t97 --batch t97 --weight <n>`.
Lane scripts live in the project's own repo at
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/lanes_t97/`.

| lane | what it ran | elapsed |
|---|---|---|
| `t97_l1_sample.sh` | imports, the canon check, the corrected reference quoted, the resume state, and the sample unit by unit | 15.9 s |
| `t97_l2_flag_reason.sh` | which token fired and on what field, two units at three ceilings each | 268.8 s |
| `t97_l3_pass1.sh` | PASS 1, six slices, 322 inputs | 581.7 s |
| `t97_l4_pass2.sh` | PASS 2 leg a, four slices, the 228 flagged at 4,096 MB / 1,800 s | 8,321.8 s |
| `t97_l6_pass2_residue.sh` | PASS 2 leg b, one slice, the 44 residue at 18,432 MB / 3,600 s | 301.7 s |
| `t97_l7_finalize_and_control.sh` | the resume state written from the store; THE CONTROL over every 100th record | 144.4 s |
| `t97_l5_downstream.sh` | the strict downstream lane; refused on an incomplete store, exit 4, nothing overwritten | 0.1 s |
| `t97_l10_downstream_partial.sh` | audit66, name_census7, pool66_run (its refusal), the guard | 6.5 s |
| `t97_l8_numbers.sh` | every number this log states, printed off the artifacts | 1.5 s |
| `t97_l11_contamination.sh` | the one cause sentence this round's shortfall made wrong | 1.0 s |
| `t97_l13_evidence.sh` | the extra reproducing commands §13 attaches to this log's conclusions | 0.6 s |
| `t97_l14_ladder.sh` | the ceiling ladder for one of the 44, printed off the three pass artifacts | 0.0 s |
| `t97_l9_claims.sh`, `t97_l12_claims.sh`, `t97_l16_claims.sh`, `t97_l18_claims.sh` | `check_conventions_log_claims.py --verify` over this log, four times; §13 | 2.3 / 2.3 / 3.1 / 3.0 s |
| `t97_l17_guard.sh` | the unmodified spelling guard again, over the final artifact set | see §7.3 |

Each lane name is used once.

## 10.2 The memory bound, stated, sampled, and never reached

- **The bound.** Per sub-process: `RLIMIT_AS` at the pass's stated
  ceiling. Per parent: **6 GB**, checked after every unit, with the
  named abort **`ABORT_MEMORY_T97`**. Per instance: 16 GB for pass 1,
  raised to 20 GB for pass 2 so one slice could hold an 18,432 MB
  ceiling alone.
- **Sampled first**, as the rule requires, before any walk: the sample
  parent's peak was **61,748 kB** (§2.1).
- **The peak actually reached.** The six pass-1 slice parents peaked at
  **69,520 / 70,728 / 70,848 / 71,464 / 72,008 / 75,764 kB** (§3.4).
  The highest is **75,764 kB — 1.2% of the 6 GB bound.**
  `ABORT_MEMORY_T97` never fired.
- The parent does no z3 work after setup; it forks and collects. That
  is why the bound holds where task 83's between-shard `getrusage`
  check could not (log_189 §7.3): the appetite is now inside a
  sub-process with a hard ceiling, and the parent is a bookkeeper.

## 10.3 ONE PROCESS, where the round requires it

The spelling guard runs as ONE process over every artifact at once
(§7.3). `audit66.py`, `name_census7.py` and `pool66_run.py` each run as
their own single process, in order, in `t97_l10_downstream_partial.sh`.
The term walk itself is a parent that forks one sub-process per unit —
which is the arrangement task 83's own probes used for the same reason
(`probe83e_callee_bodies.py`, "one forked sub-process each, so each
body's peak is its own").

## 10.4 Which files were EDITED rather than added

**No pipeline file was edited.** `term66_run.py`, `term.py`, `gate.py`,
`reference.py`, `ledger.py`, `canonical_form.py`, `pool.py`,
`pool65_run.py`, `pool66_run.py`, `regate64_run.py`, `audit66.py`,
`name_census7.py`, `pool6_prediction_check.py`,
`check_no_spelling_keys.py` and `guard66.py` were all run, not
modified. `guard83_term_pool.py` and `term66_bounded.py` are task 83's
records and were neither run nor edited.

Every file this task wrote is NEW and is named in §11.

---

# 11. File inventory

## 11.1 Written by this task — code, all NEW files

| path (under `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`) | what it is |
|---|---|
| `probe97a_unit_cost.py` | the sample: one shard walked unit by unit, one forked sub-process per unit, each unit's wall time and peak resident size read by the parent through `wait4` |
| `probe97b_flag_reason.py` | which token fired and on which FIELD, and the same unit at a ladder of ceilings with the whole record read back at each |
| `term97_walk.py` | the two-pass walk: `term66_run.one_unit` called unedited from a pristine parent that forks per unit; the wall clock enforced from outside; every returned record scanned for a memory failure that became a written reason and NOT stored if it carries one; `pass1`, `pass2`, `control` and `finalize` |
| `report97_numbers.py` | every number this log states, printed off the artifacts; it computes nothing new |
| `guard97_term_pool.py` | the UNMODIFIED `check_no_spelling_keys.py` over every JSON artifact task 97 writes, ONE process |

## 11.2 Written by this task — lanes

All under `PRIVATE/PseudoCoupHQ/Research/op_pipeline/lanes_t97/`:
`t97_l1_sample.sh`, `t97_l2_flag_reason.sh`, `t97_l3_pass1.sh`,
`t97_l4_pass2.sh`, `t97_l5_downstream.sh`, `t97_l6_pass2_residue.sh`,
`t97_l7_finalize_and_control.sh`, `t97_l8_numbers.sh`,
`t97_l9_claims.sh`, `t97_l10_downstream_partial.sh`,
`t97_l11_contamination.sh`, `t97_l12_claims.sh`,
`t97_l13_evidence.sh`, `t97_l14_ladder.sh`, `t97_l15_claims.sh`,
`t97_l16_claims.sh`, `t97_l17_guard.sh`, `t97_l18_claims.sh`.
The instance's own configuration file,
`PUBLIC/Airlock/instances/t97.conf`, was created by copying
`t87.conf` and rewriting its header; it is Airlock's file, not this
project's, and it is named here because it carries the memory
arithmetic §10.2 states.

## 11.3 Written by this task — artifacts

| path | what it holds |
|---|---|
| `probe97a_unit_cost.json` | the sample's per-unit wall time, peak resident size and outcome over two shards |
| `term97_flagged_slice0..5.json` | pass 1's own record: what each slice walked, and every unit it flagged with the word, the token, the term state and verdict it had reached, and its runtime-callee row count |
| `term97_pass2_a_slice0..3.json` | pass 2 leg a: every flagged unit re-run at 4,096 MB / 1,800 s, before and after |
| `term97_pass2_b_slice0.json` | pass 2 leg b: the 44 residue at 18,432 MB / 3,600 s |
| `term97_control.json` | every 100th stored record re-run at the pass-2 budget, compared field for field |
| `term97_finalize.json` | which inputs are complete, which are short, and WHICH UNITS are missing from each |
| `term66_store/` | 332 shards, 30,280 records — the store the brief asked to complete |
| `term66_state.json` | 297 done inputs of 332; an input is listed only when every unit canon40 proves in it has a record |
| `audit66.json`, `audit66_printed.txt` | the four states over 30,280, the ten movements with computed causes, the consistency line, layer 5, the expectation tested, the 442 resolved |
| `name_census7.json`, `name_census7_printed.txt` | the census over 30,280 layer-4 records, 50 producers |
| `guard97_term_pool.json`, `guard97_term_pool_transcript.txt` | the guard's counts and its full output |
| `claims97.json`, `claims97b.json`, `claims97c.json`, `claims97final.json` | the four `check_conventions_log_claims.py --verify` passes over this log, in order (§13) |

**NOT written, and named here so the absence is explicit:**
`the_pool6.json`, `the_pool6_bytes.json`, `the_families6.json`,
`exception_families6.json`, `pool5_pool6_delta.json`,
`pool6_prediction_check.json`,
`the_pool6_entry_E00029_successor_printed.txt`. Each needs a member set
that is not short of the population, and `pool66_run.py` refuses one
that is.

## 11.4 Plan files touched

| path | what was added |
|---|---|
| `Planning/.../node_0_3_5_6_term/node_0_3_5_6_2_transcribe/PROGRESS.md` | dated entries: the cost re-attributed to the z3 context's lifetime; pass 1's result; the store's completeness with its population |
| `Planning/.../node_0_3_5_6_term/node_0_3_5_6_3_normalize/PROGRESS.md` | dated entries: the layer-5 non-convergence, measured at three ceilings, with its population |
| `Planning/.../node_0_3_5_6_term/node_0_3_5_6_4_census/PROGRESS.md` | dated entry: `name_census7.json` over 30,280 records |
| `Planning/.../node_0_3_5_7_pool/PROGRESS.md` | dated entry: the pool blocked by its own refusal, with the number short |

---

# 12. The two lists

## 12.1 Decided, recorded for audit — nothing here needs an answer

1. The term walk runs as a pristine parent forking one sub-process per
   unit, calling `term66_run.one_unit` unedited. Mechanical: it changes
   the lifetime of the z3 context and nothing else, and §4.4's control
   measures 302 of 302 records identical.
2. The pass-1 budget is 1,536 MB and 120 s; pass 2 leg a is 4,096 MB
   and 1,800 s; leg b is 18,432 MB and 3,600 s. Each is stated with the
   measurement it rests on (§4.1).
3. `canceled` was removed from the memory-failure token list before any
   walk used it, because it is also z3's word for a spent wall clock
   (§2.3).
4. The pass-2 slice is cut by shard, not by row, so every store shard
   has exactly one writer.
5. `term66_state.json` is written from the store itself: an input is
   done when every unit canon40 proves in it has a record. The 35
   inputs holding one of the 44 are left out, so a resume picks them up.
6. Instance `t97` was raised from 16 GB to 20 GB between pass 1 and
   pass 2 so one slice could hold an 18,432 MB ceiling alone. The
   change and its arithmetic are in `instances/t97.conf`'s header.
7. `guard83_term_pool.py` was not run and not edited; a new guard
   driver was written because the old one's walk list names task 83's
   products and none of task 97's.
8. `audit66.json` was overwritten. The copy it replaced was the
   pre-relink-fix figure that log_189 §4.1 said must not be banked; the
   new one states its own population, 30,280.

## 12.2 Awaiting the owner — kept minimal

1. **§9.1** — `Term.normalize` does not converge for 44 of the 30,324
   units canon40 proves. Their terms are PROVED; the layer-5 key is
   missing; no ceiling this line can reach changes it. What a record
   for such a unit IS — and therefore whether the pool can be built —
   is an ontology decision and nothing was composed in its place.
2. **§9.2** — `audit66.py` infers "canon40 did not prove it" from "no
   record in the store". That inference is now wrong for those same 44
   units, inside a 156-unit row. Splitting it changes what the audit's
   states mean.

---

# 13. `check_conventions_log_claims.py --verify` over this log

The gate: *"Every claim carries a command that reproduces it, or says
plainly that it cannot. `check_conventions_log_claims.py --verify` will
be run against your log; task 94 scored 19 matched of 32, 28%
unverifiable. Beat it."*

It was run against this log, inside Airlock, four times, and every
result is on disk; none was discarded. The measurement of record is the
last, over the log as this section leaves it. LITERAL — lane log
`<runs>/t97/agent/logs/20260905T101128Z__t97_l18_claims.sh.log`,
lane `t97_l18_claims.sh`:

```
$ sed -n '134,144p' /logs/20260905T101128Z__t97_l18_claims.sh.log
population: 45 claims across 1 logs
  MATCHES          38
  DIFFERS          0
  UNVERIFIABLE     7
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 38 of 45 claims reproduce; 7 (16%) carry nothing to re-run

causes, by name:
  prose_only                       7
```

GLOSS, against the figure the gate names. **38 of 45 claims reproduce,
0 disagree, 7 (16%) carry nothing to re-run.** Task 94 scored **19
matched of 32, 28% unverifiable**. This log carries more claims,
matches twice as many, and cuts the unverifiable share to a bit over
half.

The **7 that remain** are prose paragraphs, and they are named rather
than hidden: §7.2's layer-5 gloss, §9.1's and §9.2's MEASURED bullets,
the two lists of §12, and this section's own paragraphs. Each restates
a figure that a fenced transcript elsewhere in this log already prints;
none asserts a check of its own that is nowhere else evidenced.

THE MEASUREMENT IS SELF-REFERENTIAL and that is said out loud rather
than hidden: a section that reports the checker's result is itself text
the checker will read on the next run, so a fifth run over this log
would count these paragraphs too and land a claim or two away from 38
of 45. The number above is the one measured over the log as it stands
at the end of this section, and the lane that measured it is named.

The four runs, in order: `t97_l9_claims.sh` (9 matched, 1 differing, 35
unverifiable), `t97_l12_claims.sh` (24 matched, 1 differing, 19
unverifiable), `t97_l16_claims.sh` (36 matched, 0 differing, 6
unverifiable), `t97_l18_claims.sh` (38 matched, 0 differing, 7
unverifiable). What changed between them was the LOG, never the checker
and never a figure: the lane-log pastes were given the `sed` command
that prints them, each conclusion was given a command of its own, and
one paste that was a line short of its command's output was completed.
