# log 196 — task 91: the one reference, and the two populations re-gated

Date: 2026-09-05. Round 17, TASK 91. Nodes:
`hq.research.compiler_graph.reference` (0_3_5_4) with its sub-nodes
`opcode_table` (0_3_5_4_0) and `machine_state` (0_3_5_4_1), and
`hq.research.compiler_graph.gate.verdict` (0_3_5_5_0).
Appendix-B shape; §5.1a LITERAL / GLOSS / ANALOGY labels throughout;
every number carries the population it is stated against.

**STATE PAGE NOTE, one line as required:** round 17's briefs were
written by the Claude Code coordinator, not by the owner — nothing in this
task's brief is a the owner ruling except the paragraphs it quotes.

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

## 0.1 The three names this report uses, each introduced before it is used

- **THE REFERENCE** is the one symbolic simulator of the machine. It
  takes a compiled unit's own shipped instructions, walks them over
  registers, flags, memory, the machine stack and the x87 stack that
  hold z3 terms rather than numbers, and returns the term the body
  leaves in its answer place. Its file is
  `~/Programming/PseudoCoupHQ/Research/op_pipeline/reference.py`.
- **THE LEDGER** is the stored provenance table for one unit: one row
  per value the unit's machine code produces, saying what produced it
  and which rows it read. `OUT-0` holds the answer. The stored ledgers
  this task reads are canon38's, as task 52 wrote them.
- **THE GATE** puts the two side by side. Route one asks the solver
  whether the ledger's `OUT-0` term equals the REFERENCE's answer for
  the same body, for every value of every input. Route two asks whether
  it equals the same body walked in text order with the LEDGER's own
  meanings. Its file is `gate.py`.

## 0.2 What the brief sent this task to do, and what was already true

The brief has three parts. Two of them were already on disk when this
task opened, delivered by round 12's task 58 and round 13's task 64,
and the COREs' realization tables had not been brought forward with
them. That is the first finding, and it is stated here rather than
buried, because a task that re-does delivered work is the failure this
line has a memory note about.

- **PART A — one simulator, not four.** Already done. `reference.py`
  is the one; `canon9`, `canon10` and `canon12` each carry one
  `# SUPERSEDED 2026-09-03 by reference.py` header line and nothing
  else changed; `gate.py` imports no behaviour checker at all. This
  task VERIFIED it in an Airlock lane and corrected the reference
  CORE's realization table, which still described the four.
- **PART B — the two defects.** Already fixed. The remainder is
  `SRem`/`URem` in `reference.py`; `MachineState` carries both the
  machine stack and the x87 stack. This task verified both with values
  in motion, and answered the one question the brief left open — the
  x87 CONTROL WORD — by census rather than by silence.
- **PART C — re-gate the two populations and report the movement.**
  NOT done before this task for these two populations under the
  reference as it stands today. This is the work of this log. Task 58
  re-gated canon38 under an EARLIER state of `reference.py` (before it
  walked branches or entered callees), and task 64 re-gated canon39 —
  a different ledger. Neither answers "what do log 153's own 415 and
  5,602 do under the reference as it is now", which is what §4 does.

## 0.3 The headline, with its population

Over log 153's own 30,436 units, ledger held at canon38, transcription
held at `layer4c`, only the reference moved:

- the **415** withdrawn disproofs: **415 prove**, 0 disprove, 0 stay
  undecided. Identical in all four runs;
- the **5,602** undecided, with the attached callee bodies in force:
  **2,356 prove**, **2,969 disprove**, **277 stay undecided**. Without
  them: 1,915 prove, 54 disprove, 3,633 stay undecided. §4.3 says why
  both are reported;
- **245** of the 23,132 units log 153 records as proved do not prove
  now. Every one of them is a proof that stood only on route two, of
  exactly the shape log_168 §6 named as a defect in that route — a
  correction, not a loss, and §5 proves it rather than asserting it.

---

# 1. The fence, the memory bound, and the lanes

## 1.1 Every computation ran in Airlock, instance `t91`

Eleven lanes, each name used once, each dropped through
`airlock submit … --instance t91 --batch t91`. Logs in
`~/AirlockRuns/t91/agent/logs/`; the elapsed column is each lane's own
`agent/status/<lane>.status` file.

| lane | what it ran | elapsed |
|---|---|---|
| `t91_l1_populations_and_sample.sh` | the two populations named unit by unit; a 200-unit sample of the re-gate, both configurations | 20.9 s |
| `t91_l2_regate_attached.sh` | the whole 30,436 re-gated, callees attached, run label `fix` | 154.8 s |
| `t91_l3_regate_unattached.sh` | the whole 30,436, no attached callees, `fix` | 82.8 s |
| `t91_l4_regate_attached_control.sh` | the same code again, callees attached, `control` | 165.7 s |
| `t91_l5_regate_unattached_control.sh` | the same code again, no attached callees, `control` | 90.1 s |
| `t91_l6_reference_evidence.sh` | Part A and Part B evidence, including the x87 control-word census | 3.0 s |
| `t91_l7_audit.sh` | the report over the four stores | 2.1 s |
| `t91_l9_lost_proofs_and_timeouts.sh` | the 245 lost proofs given a cause; every wall-clock unit re-run at 120,000 ms; the audit re-run with the corrected cause detector | 633.8 s |
| `t91_l10_guards.sh` | the spelling-key check, one process, over every artifact | 1.1 s |
| `t91_l11_lost_proof_routes.sh` | the 245 re-read for which route carried the proof that fell | 1.1 s |
| `t91_l12_guards_final.sh` | the spelling-key check again, after the last artifact was rewritten | 1.2 s |

There is no lane 8: `t91_l8_guards.sh` was written and then rewritten as
`t91_l10_guards.sh` before it was ever dropped, because the guard has to
run after the artifacts it checks. A lane name is used once, so the
number was retired rather than reused.

## 1.2 The memory bound, sampled first

STATED BEFORE THE RUN: one canon38 source document is held per
process, its units transcribed one at a time; nothing is kept across
units. Cap **6,000 MB per process**, abort named `T91_MEMORY_ABORT`,
checked after every source document.

MEASURED on the sample first (lane 1, 200 units, both
configurations):

```
    no_attached_callees: 200 units in 10.1s -- 0.050 s/unit, peak 461 MB
    attached_callees: 200 units in 10.0s -- 0.050 s/unit, peak 463 MB
SAMPLE PEAK RESIDENT SIZE: 463.0 MB, cap 6000 MB
```

MEASURED on the full pass (lane 2, four shards at once, 30,436 units):
the highest of the four shard peaks was **757.8 MB**, so the lane's own
ceiling was about 2.6 GB against the instance's 10 g. The abort was
never reached and nothing being measured was changed to fit.

---

# 2. PART A — one simulator, not four

## 2.1 The claim, and the artifact it is read off

LITERAL — lane 6's own output, the header line each superseded file
carries (`t91_l6_reference_evidence.sh`, section A1):

```
--- canon9_behaviour_check.py line 2 ---
# SUPERSEDED 2026-09-03 by reference.py (node 0_3_5_4 reference): one Reference, one MachineState, one opcode_table; this file is a record and is not edited further.
--- canon10_behaviour_check.py line 2 ---
# SUPERSEDED 2026-09-03 by reference.py (node 0_3_5_4 reference): one Reference, one MachineState, one opcode_table; this file is a record and is not edited further.
--- canon12_behaviour_check.py line 2 ---
# SUPERSEDED 2026-09-03 by reference.py (node 0_3_5_4 reference): one Reference, one MachineState, one opcode_table; this file is a record and is not edited further.
```

LITERAL — the same lane, section A2 and A2b: every module `gate.py`
imports, and the count of behaviour checkers among them:

```
84:import canon                                                      # noqa: E402
85:import ledger47 as L47                                            # noqa: E402
86:import ledger48 as L48                                            # noqa: E402
87:import region36 as R36                                            # noqa: E402
88:import layer4                                                     # noqa: E402
89:import reference as REF                                           # noqa: E402
90:import z3                                                         # noqa: E402

== A2b: does gate.py import any canon behaviour checker? ==
0
```

GLOSS: the fourth simulator the brief names — the one inside
`gate48.py` — was `gate48.reference_answer` calling
`canon10_behaviour_check.Sim10`. `gate48.py` is itself a superseded
record; the live gate is `gate.py`, and the count above is the
mechanical statement that it reaches exactly one simulator.

## 2.2 What this task changed here

Nothing in the code. The reference CORE's realization table still read
"`canon9_behaviour_check.py` (Sim9), extended by `canon10` — what
`gate48.py` calls | in use; **wrong remainder** (`%`), no stack, no
x87" and "machine_state.stack / x87 | nothing | **planned**". That
table is now what the disk says, with the evidence path on each row,
and each node's PROGRESS records the correction and its date.

---

# 3. PART B — the two defects, with values in motion

## 3.1 The remainder

### 3.1.1 The mechanism, stated before the numbers

x86's `idiv` leaves a remainder whose sign follows the DIVIDEND. z3py's
`%` on a bit vector is `bvsmod`, whose remainder follows the DIVISOR.
They differ exactly when the two sides have opposite signs, which is
where log 153's 415 disproofs all sat.

### 3.1.2 The two values, moving

LITERAL — lane 6, section B1, run in the same interpreter the pipeline
uses:

```
    LITERAL -- z3.SRem(7, -3) at 32 bits = 1  (signed 1)
    LITERAL -- the z3 operator on the same two = 4294967294  (signed -2)
```

GLOSS, with the values walked: divide 7 by −3. The quotient truncates
toward zero, so it is −2, and −2 × −3 = 6, leaving 7 − 6 = **1**. That
is what the machine leaves, and it is what `SRem` gives. `bvsmod`
answers −2 because it makes the remainder take the divisor's sign,
which the machine does not do.

### 3.1.3 The mechanism in the reference's own source

LITERAL — lane 6, section B1, every division line in `reference.py`:

```
      1034:         remainder = z3.SRem(dividend, wide)
      1037:         quotient = z3.UDiv(dividend, wide)
      1038:         remainder = z3.URem(dividend, wide)
      1094:         remainder = z3.SRem(dividend, grown)
      1097:         quotient = z3.UDiv(dividend, grown)
      1098:         remainder = z3.URem(dividend, grown)
```

The z3 operator appears in neither builder. Line 1034 is the 32- and
64-bit division; line 1094 is the 8- and 16-bit one task 64 added.

## 3.2 The machine stack and the x87 stack

LITERAL — lane 6, section B2:

```
    LITERAL -- MachineState().stack = {'pointer': seed_rsp, 'offset': 0, 'cells': {}}
    LITERAL -- MachineState().x87   = {'slots': [None, None, None, None, None, None, None, None], 'top': 0, 'depth': 0}
    LITERAL -- the stack and x87 methods: pop_value, push_value, x87_at, x87_pop, x87_push, x87_set
```

GLOSS, the machine stack with values in motion. `push %rbp` moves the
offset from 0 to −8, moves the pointer term from `seed_rsp` to
`seed_rsp - 8`, and writes the 64-bit term `seed_rbp` into the cell
keyed −8. `pop %rbp` reads the cell keyed −8 — `seed_rbp` — puts it
back in the register family, and moves the offset back to 0. A pop at
an offset this body never wrote is REFUSED by name, because the value
would have come from outside the unit and inventing it would be
inventing a fact.

GLOSS, the x87 stack with values in motion, on the unit log 153 §4.3
printed as undecided on both routes. Take `0x18(%rsp) = 2.0` and
`0x8(%rsp) = 3.0`. The first `fldt` pushes `2.0`: `top` moves from 0 to
7 and slot 7 holds it, `depth` is 1. The second `fldt` pushes `3.0`:
`top` moves to 6, `depth` is 2, so `%st` is `3.0` and `%st(1)` is
`2.0`. `fucomip %st(1),%st` compares `3.0` against `2.0` and pops.
`seta` asks "above and ordered", which is true, so the answer is 1.

### 3.2.1 That same unit, walked through the ONE reference today

LITERAL — lane 6, section B4:

```
  cpp/regen_36796
    LITERAL -- body: fldt 0x18(%rsp); fldt 0x8(%rsp); fucomip %st(1),%st; fstp %st(0); seta %al; ret
    LITERAL -- the ONE reference's answer: If(And(Not(x87_0x8_rsp_ < x87_0x18_rsp_),
       Not(fpEQ(x87_0x8_rsp_, x87_0x18_rsp_)),
       Not(Or(fpIsNaN(x87_0x8_rsp_), fpIsNaN(x87_0x18_rsp_)))),
   1,
   0)
    LITERAL -- the ledger's OUT-0 term:    If(And(Not(x87_0x8_rsp_ < x87_0x18_rsp_),
       Not(fpEQ(x87_0x8_rsp_, x87_0x18_rsp_)),
       Not(Or(fpIsNaN(x87_0x8_rsp_), fpIsNaN(x87_0x18_rsp_)))),
   1,
   0)
    route one (the term against the ship body): PROVED_ON_SHIP
```

GLOSS: log 153 printed the ledger's term for this unit and could put no
reference beside it. The two terms above are the same term, and the
solver says so for every input, including every NaN.

### 3.2.2 A machine-stack unit, the same way

LITERAL — lane 6, section B5:

```
  go/op_110
    LITERAL -- body: push %rbp; mov %rsp,%rbp; test %rbx,%rbx; je L0; xor %edx,%edx; div %rbx; pop %rbp; ret; L0:; call x_runtime_panicdivide; nop
    LITERAL -- the ONE reference's answer: Extract(31,
        0,
        bvudiv_i(Concat(0, seed_rax), Concat(0, seed_rbx)))
    LITERAL -- the ledger's OUT-0 term:    Extract(31,
        0,
        bvudiv_i(Concat(0, seed_rax), Concat(0, seed_rbx)))
    route one (the term against the ship body): PROVED_ON_SHIP
```

GLOSS: this is the unit log 153 §4.3 quoted as `the reference
simulator: mnemonic 'je' has no symbolic model in this checker`. Three
of the reference's rules meet in it: the `push`/`pop` pair round-trips
through the machine stack; the `je L0` forks and the side that reaches
`call x_runtime_panicdivide` leaves the unit, so it is unreachable and
contributes nothing; what is left is the normal path, which is the
unsigned division.

## 3.3 The x87 control word — the one question the brief left open

The brief says to build "its own control word where a unit's answer
depends on it". The opcode_table CORE's standing rule is that no entry
is invented for an opcode no body contains, so the question is a
census, not a design decision.

LITERAL — lane 6, section B3:

```
    bodies walked (canon38 and canon40 together): 62156
    bodies spelling any x87 arch opcode:          2810
    control-word arch opcodes found:              {"fldz": ["c/regen_34", "c/regen_15786", "c/regen_15842", "c/regen_16626", "c/regen_16682"]}
```

GLOSS, and one correction to my own search list, said rather than
smoothed. Twelve opcodes read or write the x87 control word (`fldcw`,
`fnstcw`, `fstcw`, `fldenv`, `fnstenv`, `fstenv`, `fnsave`, `frstor`,
`finit`, `fninit`, `fnclex`, `fclex`); **none of the twelve appears in
any of the 62,156 bodies**. `fldz` was in the list I searched for and
should not have been — it pushes the constant zero and touches no
control word — so the honest reading of the line above is: the census
found the twelve at zero, and separately noticed that `fldz` is spelled
by some bodies, which is a load and not a control-word access. **No
control word is modelled, and no unit's answer in this corpus depends
on one.**

---

# 4. PART C — the re-gate, and the movement

## 4.1 What was held still, so the movement means something

One thing moved. LITERAL — `t91_regate_run.py`'s own header:

```
WHAT MOVES AND WHAT IS HELD STILL, said before any figure.  Exactly one
thing moves: the reference.  The population is canon38's, the ledger is
canon38's as stored, the transcription is `layer4c.transcribe` (task
53's own superseded record, READ and never edited), and the obligations
are `gate.Gate`'s.
```

## 4.2 The starting populations, recomputed rather than retyped

The 415 and the 5,602 are not copied from log 153's prose. They are
recomputed from the artifacts `audit53.py` computed them from, with
`audit53`'s own four-way rule.

LITERAL — lane 1, `t91_populations.py`:

```
THE FOUR BUCKETS, against log 153 section 1.2
  state           log 153       here    delta
  proved            23132      23132       +0
  withdrawn           415        415       +0
  undecided          5602       5602       +0
  no term            1287       1287       +0
  units             30436      30436       +0

  contradictions (proved on one route, disproved on the other): 0
```

## 4.3 The two configurations, and why both are reported

The reference has one behaviour with a switch on it that the tree
itself names: a `call` whose callee is ATTACHED is not a transfer, and
a `call` whose callee is not attached IS one. Both are run, because
which one is in force changes 2,900 verdicts and folding them together
would hide that.

- **`attached_callees`** — the reference holds task 63's 76 attached
  callee bodies (clang 32, clang++ 32, rustc 5, swiftc 7) and walks
  into them.
- **`no_attached_callees`** — it holds none, so a `call` leaves the
  unit. This is the configuration task 58 ran.

## 4.4 THE 415 WITHDRAWN DISPROOFS — the three-way split

LITERAL — `t91_audit_printed.txt`, configuration `attached_callees`,
run `fix` (the figures are identical in all four runs):

```
  STARTING POPULATION: the 415 units log 153 records as withdrawn
    proved            415   100.0% of the 415
    withdrawn           0     0.0% of the 415
    undecided           0     0.0% of the 415
    no term             0     0.0% of the 415

    -- withdrawn -> proved  (415 units), by computed cause
          415 | the ONE reference's remainder is the machine's: SRem/URem, whose sign follows the dividend, in the place of the z3 operator whose sign follows the divisor (log 153 section 5)
              sightings: c/op_246, c/op_247, c/op_252
```

**Nothing in this population stayed put.** 415 of 415 moved, all in one
direction, on one cause.

## 4.5 THE 5,602 UNDECIDED — the three-way split

LITERAL — `t91_audit_printed.txt`, configuration `attached_callees`,
run `fix`:

```
  STARTING POPULATION: the 5602 units log 153 records as undecided
    proved           2356    42.1% of the 5602
    withdrawn        2969    53.0% of the 5602
    undecided         277     4.9% of the 5602
    no term             0     0.0% of the 5602
```

And the same population under `no_attached_callees`:

```
    proved           1915    34.2% of the 5602
    withdrawn          54     1.0% of the 5602
    undecided        3633    64.9% of the 5602
```

GLOSS: the difference between the two is the `call`. With the callee
bodies attached the reference reaches an answer for **3,356 more** of
these 5,602 bodies (3,633 undecided falls to 277); **441** of them
agree with the ledger and prove, and **2,915** disagree with it and
disprove. §4.6 says whose defect that disagreement is, computed rather
than guessed.

## 4.6 The 2,969 disproofs, by computed cause

LITERAL — `t91_audit_printed.txt`, configuration `attached_callees`,
run `fix`:

```
    -- undecided -> withdrawn  (2969 units), by computed cause
         2916 | the unit's own stored canon38 ledger carries NO row for its transfer into the compiler's own runtime, so its term asserts the transfer changed nothing; the reference now walks that callee's body, and the two disagree
              sightings: c/regen_10087, c/regen_10143, c/regen_10486
           53 | the new run's own recorded reason: z3 found a starting state under which the two sides differ
              sightings: c/regen_12973, cpp/regen_11824, cpp/regen_11844
```

And the proofs gained, for the same population:

```
    -- undecided -> proved  (2356 units), by computed cause
         1674 | the reference now models something this body spells that it refused before (the machine stack, the x87 stack, the narrow division and widening multiply, or a rip-relative address)
              sightings: c/op_212, c/op_218, c/op_222
          443 | the reference now enters the attached runtime callee's body and returns through its answer register
              sightings: c/regen_1001, c/regen_10073, c/regen_10129
          239 | the reference now follows this body's own branches and merges them at the join
              sightings: go/op_110, go/op_146, go/op_168
```

GLOSS, with the mechanism rather than the label. **2,916 of the 2,969
disproofs are the LEDGER's gap, not the reference's.** A canon38 ledger
was written before the runtime callee was attached, so where a body
hands its value to a routine the compiler shipped — `__divti3` and its
family — the ledger has NO row for the hand-over. Its `OUT-0` term
therefore reads as though the transfer changed nothing. The reference
now walks the callee's own body, so the two sides disagree, and the
solver says where. That is the gate working: a disagreement between a
correct reference and an incomplete ledger is exactly what route one is
for. The repair is the ledger's, not this node's — round 14's canon
rebuild is where it lands, and log_168 §5.3 already wrote the rule into
`destination_rules`.

**A correction to my own first pass, recorded rather than smoothed.**
The first run of `t91_audit.py` left all 2,969 with no computed cause,
because its `call_targets` split the line on a space and threw away the
RELOCATION — and an unlinked `call` disassembles as a transfer to an
address inside the unit, so the relocation is the only place the
routine's name survives. It now calls `ledger.transfer_callee`, the
same resolver the reference itself uses. The corrected run is what is
quoted above; the defective first pass is named here and its numbers
are not used anywhere.

## 4.7 The 277 that did not move, each with its reason

LITERAL — `t91_audit_printed.txt`:

```
    -- undecided -> undecided  (277 units), by computed cause
          132 | did not move; the run's own reason: the reference: the two sides of a branch leave the machine stack at different depths (-8 against -16)
              sightings: c/regen_11268, c/regen_11543, c/regen_11554
          122 | did not move; the run's own reason: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read
              sightings: c/regen_10483, c/regen_10484, c/regen_1075
           10 | did not move; the run's own reason: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved
              sightings: c/regen_10464, c/regen_10485, c/regen_12383
            7 | did not move; the run's own reason: the reference: this opcode reads the signed-overflow bit and no flag-setting arch opcode precedes it in this body
              sightings: swift/op_128, swift/regen_303, swift/regen_304
            6 | did not move; the run's own reason: the reference: this opcode reads the signed-overflow bit and the flag-setting arch opcode 'imul' has no overflow model in this file
              sightings: swift/op_114, swift/op_121, swift/regen_298
```

GLOSS, cause by cause, because a verdict that does not move is a
statement about the reference and is worth as much as one that does:

- **132 — the merge refuses on a stack-depth disagreement.** The
  machine_state CORE rules that the two sides of a branch must leave
  the machine stack at one depth and that a disagreement is REFUSED by
  name rather than guessed. These bodies push on one side and not the
  other, so the reference stops. It is the modelled stack working as
  ruled, not the stack missing.
- **122 — every path leaves the unit.** The reference CORE rules that a
  transfer out makes its side unreachable, and that a body all of whose
  sides transfer out leaves no answer. These are those bodies.
- **10 — the solver's wall clock.** Flagged and re-run with forty times
  the room; §6 reports what changed.
- **13 — the signed-overflow bit**, in two shapes: no flag-setting
  opcode precedes the read at all (7), and the setter is a widening
  multiply whose overflow this file does not model (6). Both are named
  census rows, not silent gaps.

## 4.8 The whole population, four states, per run

LITERAL — `t91_audit_printed.txt`:

```
THE FOUR STATES -- configuration 'attached_callees', run 'fix'
  state           log 153       here     delta
  proved            23132      25658     +2526
  withdrawn           415       3198     +2783
  undecided          5602        293     -5309
  no term            1287       1287        +0
  units             30436      30436        +0

THE FOUR STATES -- configuration 'no_attached_callees', run 'fix'
  state           log 153       here     delta
  proved            23132      25217     +2085
  withdrawn           415        283      -132
  undecided          5602       3649     -1953
  no term            1287       1287        +0
  units             30436      30436        +0
```

**Total movement, against the 30,436, counted unit by unit rather than
read off the column deltas.** With the callees attached: 415 leave
WITHDRAWN, 5,325 leave UNDECIDED (2,356 to proved, 2,969 to withdrawn),
245 leave PROVED — **5,985 verdicts move and 24,451 do not** (19.7%
against 80.3%). Without them: 415 + 1,969 + 245 = **2,629 move and
27,807 do not**. The 1,287 units that build no term at all move in
neither, and the reason is that the ledger builds them no term — a
statement about the ledger, which this task did not touch.

## 4.9 The consistency line

LITERAL — `t91_audit_printed.txt`:

```
  attached_callees       fix       units proved on one route and disproved on the other: 0
  attached_callees       control   units proved on one route and disproved on the other: 0
  no_attached_callees    fix       units proved on one route and disproved on the other: 0
  no_attached_callees    control   units proved on one route and disproved on the other: 0
```

---

# 5. Zero regression: the 245, and their cause

## 5.1 The count, and why it is not zero

LITERAL — `t91_audit_printed.txt`:

```
ZERO REGRESSION -- the 23,132 units log 153 records as proved

  configuration 'attached_callees', run 'fix'
    units still proved (kept)             22887
    proofs lost                             245
          229 | withdrawn -- z3 found a starting state under which the two sides differ
              sightings: c/op_117, c/op_122, c/op_158
           16 | undecided -- the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved
              sightings: c/op_153, c/op_225, c/op_230
```

The same 245 in all four runs. The zero_regression CORE's rule is not
"nothing may fall" — it is "no unit loses PROVED without a named cause,
CHECKED over the unit's own artifact", and it says in as many words
that "a withdrawn proof that was WRONG is a correction, not a loss to
be avoided". So the whole question is what these 245 were.

## 5.2 The shape they all share, measured before anything is claimed

LITERAL — `t91_lost_proofs_printed.txt`:

```
THE 245 LOST PROOFS, BY THE SHAPE OF THEIR OWN TEXT
    135 | carries a positional label and carries a conditional transfer
    110 | carries a positional label and carries a conditional transfer and carries an unconditional transfer or a trap
```

**All 245 carry a positional label and a conditional transfer.** Not
234, not most: all of them.

## 5.3 Which of log 153's two routes carried the proof that fell

LITERAL — the same file:

```
WHICH OF log 153's TWO ROUTES CARRIED THE PROOF THAT FELL
    245 | route two alone proved it in log 153

THE TWO REFERENCES ON THE SAME BODY
    245 | the SUPERSEDED simulator refuses this body; the ONE reference answers it
          sightings: c/op_117, c/op_122, c/op_153
```

GLOSS: route one never proved one of them. The superseded simulator
refuses a conditional transfer outright, so in log 153 every one of
these 245 was carried by ROUTE TWO — the text-order walk — alone.

## 5.4 What route two says about them now, in its own words

LITERAL — the same file, the largest group:

```
    129 | route one DISPROVED / route two UNDECIDED -- route two's own words: the text-order walk: this body transfers to 'js L0', a label it defines itself, so the page order is not the run order and a text-order walk has no one answer to reach
```

with eleven more groups of the same sentence over a different transfer,
summing to 245.

## 5.5 The mechanism, with values in motion

`c/op_117` is the instance log_168 §6.2 worked, and it comes out of
this task's own run first in the sightings.

LITERAL — `t91_lost_proofs_printed.txt`:

```
  c/op_117
    LITERAL -- body: test %rdi,%rdi; js L0; cvtsi2ss %rdi,%xmm1; addss %xmm1,%xmm0; ret; L0:; mov %rdi,%rax; shr $1,%rax; and $0x1,%edi; or %rax,%rdi; cvtsi2ss %rdi,%xmm1; addss %xmm1,%xmm1; addss %xmm1,%xmm0; ret
    LITERAL -- the SUPERSEDED simulator's answer: None
    LITERAL -- the ONE reference's answer:        If(0 <= seed_rdi,
   fp.to_ieee_bv(fpToFP(Extract(31, 0, seed_xmm0)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), seed_rdi)))),
   fp.to_ieee_bv(fpToFP(Extract(31, 0, seed_xmm0)) + fpToFP(fp.to_ieee_bv(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Concat(0, Extract(63, 1, seed_rdi) | Concat(0, Extract(0, 0, seed_rdi)))))) + fpToFP(fp.to_
```

GLOSS, with values moving. This is the compiler's own way of turning an
unsigned 64-bit integer into a float, because the machine's convert
instruction reads its operand as signed.

- Take `%rdi = 5`. `test %rdi,%rdi` leaves the sign bit clear, so
  `js L0` is not taken. The straight path converts 5 directly and adds
  it to `%xmm0`. The answer is `xmm0 + 5.0`.
- Take `%rdi = 2^63 + 4`, which the machine reads as a negative number.
  `js L0` IS taken. `shr $1` halves it to `2^62 + 2`; `and $0x1,%edi`
  keeps the bit that halving dropped, here 0; `or` puts it back;
  `cvtsi2ss` converts `2^62 + 2`, which is positive and converts
  correctly; `addss %xmm1,%xmm1` doubles it back. The answer is
  `xmm0 + (2^63 + 4).0`.
- **The two stretches are ALTERNATIVES.** Exactly one of them runs.
  The ONE reference says so: its answer is an `If` on the sign bit.
- The old route two walked the page from top to bottom and ran BOTH,
  so it added the two answers together — and the ledger's term does the
  same thing, so the two agreed and route two called it proved. Two
  walks sharing one error, which is the same failure log_153 §4.2 found
  in the flag link.

## 5.6 The ruling this falls under

Under the zero_regression CORE, these are **245 lost proofs with a
named, mechanically-checked cause**, and the cause is that the proofs
were wrong. Route two was fixed in task 64 (`gate.transfers_inside_the_
unit`, log_168 §6.3) and now refuses these bodies by name; route one can
now read them and disproves them against the ledger's term. Zero
regressions holds in the ruled sense. Nothing here is absorbed: the 245
are named, their shape is measured, and the units are in
`t91_lost_proofs.json`.

---

# 6. The wall clock: the control, and the flagged re-run

## 6.1 Why a control run exists at all

`gate.SOLVER_MILLISECONDS` is 3,000 ms of WALL CLOCK, so the same
question asked twice can get two answers. A verdict that changes
between two runs may be that and not the fix, so the two are separated
by measurement: each configuration was run twice, `fix` and `control`,
over identical code and an identical population.

## 6.2 What unchanged code did on its own

LITERAL — `t91_audit_printed.txt`:

```
  configuration 'attached_callees': 17 of 30436 units answer differently when the SAME code is run twice (0.06%)
          9 | undecided in the fix run, withdrawn in the control run
            sightings: c/regen_10464, c/regen_10485, c/regen_12383
          8 | withdrawn in the fix run, undecided in the control run
            sightings: c/regen_10486, c/regen_10502, c/regen_10509

  configuration 'no_attached_callees': 8 of 30436 units answer differently when the SAME code is run twice (0.03%)
          7 | withdrawn in the fix run, undecided in the control run
            sightings: c/regen_2559, c/regen_5695, cpp/regen_5689
          1 | undecided in the fix run, withdrawn in the control run
            sightings: c/op_225
```

GLOSS: **0.06% and 0.03%**, against the 1.66% the brief cites from an
earlier measurement. Every one of the 25 sits between UNDECIDED and
DISPROVED — never between PROVED and anything, which is what the
verdict CORE's "a solver timeout is UNDECIDED, never DISPROVED"
protects. Set against the movement this task measured (5,985 units with
the callees attached), the wall clock accounts for 0.3% of it.

## 6.3 the owner's rule applied: flagged, re-run with more room, reported

the owner, 2026-09-04, verbatim: "if it timed out, why not have all those
flagged for things to either have a look at after or just re-run with
the rest of them and give them a longer processing time to see if it
changes the result?"

LITERAL — `t91_timeouts_printed.txt`:

```
units flagged for more room: 39
     39 | its own verdict named the 3000 ms wall clock
     22 | unchanged code answered it two ways
bodies found in canon38:     39
the ceiling in force:        120000 ms (the runs used 3000 ms)
```

```
WHAT MORE ROOM CHANGED, per configuration
     26 | attached_callees: undecided at 3000 ms -> withdrawn at 120000 ms
     13 | attached_callees: withdrawn at 3000 ms -> withdrawn at 120000 ms
     14 | no_attached_callees: undecided at 3000 ms -> undecided at 120000 ms
     17 | no_attached_callees: undecided at 3000 ms -> withdrawn at 120000 ms
      8 | no_attached_callees: withdrawn at 3000 ms -> withdrawn at 120000 ms

verdicts that changed with more room: 43 of 78
```

GLOSS, and it is a real finding rather than a formality. The 78 rows
are 39 flagged units put to each of the two configurations.

- **43 of the 78 turn from UNDECIDED into DISPROVED** with more room —
  26 with the callees attached, 17 without.
- **None of the 78 turns into a proof.** Not one.
- **Nothing that was DISPROVED at 3,000 ms became anything else at
  120,000 ms**: 21 of 21 stayed disproved (13 attached, 8 not).
- **14 stay UNDECIDED even at 120,000 ms**, all of them in the
  no-attached-callees configuration; with the callees attached every
  one of the 39 decides.

So the 3,000 ms ceiling UNDER-counts disproofs rather than
over-counting them, which is the safe direction for a research that
counts proofs — nothing was ever called proved on a timeout — but it
does mean the undecided column carries verdicts that are really
disproofs. The 14 that never decide are the honest remainder and are
named unit by unit in `t91_timeouts.json`.

Peak resident size on that lane: **1,042.5 MB**, cap 6,000 MB, abort
`T91_MEMORY_ABORT` never reached.

---

# 7. The mechanical guard

LITERAL — `t91_l12_guards_final.sh`'s own output, one process over
every artifact this task wrote:

```
artifacts handed to the check, in ONE process:
  named files:      6
  store documents:  1328

check_no_spelling_keys.py exit code: 0

PASS lines:  1334
FAIL lines:  0
exempt count (must be 0): 0

--- the first and last lines of the check's own output ---
operator inventory: 91 tokens read from probe_manifest_*.json
PASS t91_audit.json -- no operator token in any key, grouping, pairing or row structure
PASS t91_lost_proofs.json -- no operator token in any key, grouping, pairing or row structure
```

`check_no_spelling_keys.py` is unmodified; 1,334 artifacts passed; the
provenance exemption is claimed by nothing (`grep -c exempt` = **0**).

---

# 8. Every artifact this task wrote

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| artifact | what it is |
|---|---|
| `t91_populations.py`, `t91_populations.json` | log 153's four buckets recomputed unit by unit from `layer4c*`, with `audit53`'s own rule |
| `t91_regate_run.py` | the re-gate driver: canon38 ledger, `layer4c` transcription, `gate.Gate`, `reference.Reference`, sharded and resumable |
| `t91_regate_store_attached_callees_fix/` (332 files) | the re-gate, callees attached |
| `t91_regate_store_attached_callees_control/` (332) | the same code again, for the wall-clock control |
| `t91_regate_store_no_attached_callees_fix/` (332) | the re-gate, no attached callees |
| `t91_regate_store_no_attached_callees_control/` (332) | its control |
| `t91_audit.py`, `t91_audit.json`, `t91_audit_printed.txt` | the report of §4, §5.1, §6.2 |
| `t91_lost_proofs.py`, `t91_lost_proofs.json`, `t91_lost_proofs_printed.txt` | §5's diagnosis of the 245 |
| `t91_timeouts.py`, `t91_timeouts.json`, `t91_timeouts_printed.txt` | §6.3's flagged re-run at 120,000 ms |
| `t91_sample.json` | lane 1's 200-unit sample, with seconds per unit and peak resident size |
| `t91_reference_evidence.json` | §2 and §3's evidence, including the x87 control-word census |
| `t91_guard_printed.txt`, `t91_guard_final_printed.txt` | the spelling-key check's own output |
| the eleven `t91_l*.sh` lane scripts | the Airlock lanes of §1.1, each name used once |

Planning tree, all under
`Planning/node_0_3_research/node_0_3_5_compiler_graph/`:

| file | what changed |
|---|---|
| `node_0_3_5_4_reference/CORE_…md` | realization table rewritten to what is on disk; the x87 control word ruled out by census, with its numbers |
| `node_0_3_5_4_reference/PROGRESS.md` | two dated entries (2026-09-05) |
| `node_0_3_5_4_0_opcode_table/CORE_…md` | realization table: the two **planned** rows closed with their evidence |
| `node_0_3_5_4_0_opcode_table/PROGRESS.md` | one dated entry |
| `node_0_3_5_4_1_machine_state/CORE_…md` | realization table: `stack` and `x87` closed; a control-word row added; what the gaps cost re-measured |
| `node_0_3_5_4_1_machine_state/PROGRESS.md` | one dated entry |
| `node_0_3_5_5_0_verdict/CORE_…md` | realization table: the two **planned** re-gates replaced by their results; a wall-clock row added |
| `node_0_3_5_5_0_verdict/PROGRESS.md` | two dated entries |
| `node_0_3_5_5_5_zero_regression/CORE_…md` | a FOURTH named cause added to the list of named causes: the alternative stretches added together, 245 units |
| `node_0_3_5_5_5_zero_regression/PROGRESS.md` | one dated entry |

No file that this task read as a record was edited: `canon38*`,
`layer4c*`, `gate48.py`, `textwalk48.py`, `canon9/10/12_behaviour_
check.py`, `audit53.py`, `gate58_run.py` and `regate64_run.py` are all
untouched.

---

# 9. The two lists

## 9.1 Decided, recorded for audit — no reply needed

1. **The re-gate holds the ledger still and moves only the reference.**
   canon38 as stored, `layer4c` as the record it is, `gate.Gate`'s
   obligations unchanged. Otherwise a movement could not be attributed.
2. **Both callee configurations are run and both are reported.** The
   tree names both behaviours as the reference's own; which is in force
   moves 2,915 verdicts, so folding them together would hide that.
3. **The starting populations are recomputed, never retyped.** 23,132 /
   415 / 5,602 / 1,287 reproduced exactly from the artifacts
   `audit53.py` used, with its own rule.
4. **The four COREs' realization tables were corrected to what is on
   disk.** They described a state of the world tasks 57, 58 and 64 had
   already left behind; that is a record being brought forward, not a
   shape being added, so no ruling was needed.
5. **The x87 control word is not modelled**, because the census says no
   body in the corpus spells any opcode that reads or writes it, and
   the opcode_table CORE forbids inventing an entry for an opcode no
   body contains.
6. **My own first audit pass had a defect and it is named**, not
   smoothed: the cause detector lost the relocation on a `call` line
   and left 2,969 disproofs unattributed. Fixed and re-run; the
   defective pass's numbers appear nowhere.

## 9.2 Awaiting the owner

1. **The 2,916 disproofs are the LEDGER's gap and their repair is not
   this node's.** canon38 holds no row for a transfer into the
   compiler's own runtime. Round 14's canon rebuild is where it lands
   (`destination_rules`, log_168 §5.3). Nothing here is blocked on it;
   it is named so the figure is not mistaken for a reference defect.
2. **The solver's 3,000 ms ceiling under-counts disproofs.** At 120,000
   ms, 43 of 78 flagged verdicts turn from UNDECIDED into DISPROVED and
   none turns into a proof. Whether the pipeline's ceiling should move
   is a decision about what the research measures, not a mechanical
   detail, so it is put here rather than taken.
