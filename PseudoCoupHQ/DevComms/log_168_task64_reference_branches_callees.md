# log 168 — task 64: the reference follows branches and steps into callees

Date: 2026-09-03. Round 13, TASK 64 of
`~/Programming/PseudoCoupHQ/DevComms/log_166_claude_code_task_briefs_round13.md`.
Node: `hq.research.compiler_graph.reference` (0_3_5_4), with its
sub-nodes `opcode_table` and `machine_state`, plus
`ledger.destination_rules` (0_3_5_3_3) and `gate` (0_3_5_5) for the
re-gate.
Appendix-B shape; §5.1a LITERAL / GLOSS labels throughout; every number
carries its population.

---

# 0. What was done, in plain words before any figure

A compiled body is not a list. It BRANCHES — one instruction decides
which of two later stretches runs — and it CALLS — it hands its value
to a routine the compiler shipped with itself and takes an answer back.
The reference simulator did neither. It read a body down the page and
stopped at the first `j<cc>` and at every `call`, and 3,865 of canon39's
30,432 units were undecided for exactly that reason.

Three things happened.

- **The reference now walks a body as its own graph.** It cuts the body
  into blocks at the labels the body defines, follows both sides of
  each conditional transfer, and puts the two states back together at
  the join as `If(condition, this side, the other)` per register, per
  memory cell, per stack slot. A side that transfers OUT of the unit —
  go's panic path, rust's `panic_const` — is unreachable, contributes
  nothing, and leaves its condition on the guard row.
- **The reference now steps into an attached callee.** At a `call`
  whose callee task 63 attached, it walks that routine's own body —
  itself a graph — and returns through the register that body writes
  its answer into. Put to numbers rather than asserted: walked over
  concrete half floats, `clang/__extendhfsf2` returns the IEEE-correct
  32-bit float every time, subnormals included.
- **All 30,432 canon39 terms were re-gated on both routes.** Proved
  goes 26,040 → 26,594. The four named causes of log_160 §1.7 all
  decide, but NOT all of them decide the way the brief's expectation
  guessed: the rip-relative bucket proves outright, the conditional
  transfers mostly prove, and the runtime-callee bucket mostly
  **disproves** — because the reference now models the callee and the
  round-12 LEDGER does not. §5 is that finding.

Two defects were found by measurement and are named rather than
smoothed: one in `gate.prove_term_against_text` (fixed here, §6) and
one in `destination_rules` rule 4 (written into the CORE here, its
realization a round-14 canon rebuild, §5.3).

---

# 1. The tree was corrected first, before any code

Round 12/13's binding rule 2 and PROTOCOL §2: a shape the tree lacks
goes into the tree first, with provenance. Eleven settled rules were
written into four COREs before a line of code was changed, and each
node's PROGRESS records the writing at the moment it happened.

| CORE | what was added |
|---|---|
| `node_0_3_5_4_reference` | five rules: a body is walked as its own control-flow graph, blocks cut at the positional labels, reverse postorder, a CYCLE refused by name; a transfer whose target is not a label this body defines leaves the unit, so that side is unreachable and its condition is a guard row; what a merge does to each kind of state and where it refuses; a `call` with an attached callee is not a transfer (the callee's own arrival contract in, its answer register out, `xmm0` when its body writes `xmm0` and `rax` otherwise, computed off the body); a rip-relative ADDRESS computation is the body's next `ripconst_<k>`. The `## design` block gained `blocks_of`, `walk_body`, `merge`, `guard_rows`. |
| `node_0_3_5_4_1_machine_state` | three rules: a state is mergeable and the merge REFUSES rather than guesses; a rip-relative address reads the same positional counter a rip-relative load reads; a sub-32-bit write into the accumulator pair PRESERVES the register's upper bits, which `full64` does not. |
| `node_0_3_5_4_0_opcode_table` | two rules: a conditional transfer is an entry with the SAME condition builder `set<cc>` and `cmov<cc>` carry, not a census row; 8- and 16-bit division and widening multiply are entries whose destination is a pair of bytes or words inside ONE register family. |
| `node_0_3_5_3_3_destination_rules` | the `## design` table's rows QUALIFIED BY OPERAND WIDTH — six new rows for widths 8 and 16 — and one settled rule saying why the narrow widths are two parts of one register. |

**One thing was written into a CORE AFTER the measurement that
produced it, and it is recorded as such** (§5.3): the defect in
`destination_rules` rule 4. It could not have been written first,
because it was not known until the re-gate ran; it is a finding of the
run, and its PROGRESS line says so.

**Nothing was put to the owner.** Every choice above is answered by a CORE or
by AgentMemory.

---

# 2. `go/op_174` — a branch to a panic path, with values in motion

## 2.1 The unit

`go/op_174` is go's left shift on 64-bit integers. Go checks that the
shift count is not negative and stops the program if it is.

LITERAL — `acceptance64_printed.txt` part 1, the unit's own stored
`body_verbatim` (`canon39_wrapped_go.json`):

```
     0  push %rbp
     1  mov %rsp,%rbp
     2  test %ebx,%ebx
     3  jl L0
     4  mov %ebx,%ecx
     5  shl %cl,%rax
     6  cmp $0x40,%ecx
     7  sbb %rdx,%rdx
     8  and %rdx,%rax
     9  pop %rbp
    10  ret
    11  L0:
    12  call x_runtime_panicshift
    13  nop
```

## 2.2 The graph the reference reads off that text

LITERAL — the same transcript:

```
    label -> instruction index: {"L0": 11}
    block 0  instructions 0..3   terminator 'jl L0'   taken: block 2 | not taken: block 1
    block 1  instructions 4..10  terminator 'ret'     returns
    block 2  instructions 11..12 terminator 'nop'     always: OUT OF THE UNIT
```

GLOSS: the body is cut into three straight-line runs. Block 0 ends at
the conditional transfer. `L0` is a label THIS BODY DEFINES, so the
taken side is an edge inside the unit, to block 2. Block 2 transfers to
`x_runtime_panicshift`, a name no builtins archive on this machine
defines, so block 2 leaves the unit — it is go's own runtime reacting
to a condition, not the compiler computing an answer, which is the
distinction log_167 §4.2 drew over the whole population.

## 2.3 The guard row the unreachable side leaves

LITERAL — the same transcript:

```
    line      call x_runtime_panicshift
    went to   runtime_panicshift
    condition And(True, 0 > Extract(31, 0, seed_rbx) & Extract(31, 0, seed_rbx))
```

GLOSS: `jl` after `test %ebx,%ebx` reads "the shift count is negative"
— `test` leaves the triple `("test", ebx & ebx, 0)` and `jl` reads
`0 > that`. Under that condition go stops the program; under its
negation the shift runs. The condition is kept as data, which is what a
guard row is for, and it is the reason the reference's answer and the
LEDGER's answer are comparable at all: the ledger's OUT-0 term is the
normal-path term (AgentMemory, "SEED = the normal-path computation
graph"), so an unreachable side has to contribute nothing on both
sides.

## 2.4 The answer, and the verdict

LITERAL — the same transcript:

```
~(~(seed_rax << Concat(0, Extract(5, 0, seed_rbx))) |
  ~(18446744073709551615*
    If(Or(Not(Extract(31, 7, seed_rbx) == 0),
          ULE(64, Extract(6, 0, seed_rbx))),
       0,
       1)))

outcome PROVED_ON_SHIP
```

and what round 12 recorded for the same unit
(`term61_store/canon39_wrapped_go.json`):

```
outcome UNDECIDED
reason  the reference: arch opcode 'jl' is a census row, not a silent
        gap: a transfer or trap, and this reference walks a body in
        text order
```

GLOSS: `shl %cl,%rax` shifts, and `cmp $0x40` + `sbb %rdx,%rdx` +
`and %rdx,%rax` is go's branch-free mask that turns the answer into
zero when the count is 64 or more (x86 would have shifted by count mod
64). The term says exactly that, and z3 proves it equal to the
ledger's.

---

# 3. `c/op_282` — a body with no graph, unchanged

LITERAL — `acceptance64_printed.txt` part 2:

```
     0  xor %eax,%eax
     1  or %esi,%edi
     2  setne %al
     3  ret

`Reference.answer_of`, simplified:
    If(Extract(31, 0, seed_rdi) | Extract(31, 0, seed_rsi) == 0, 0, 1)
the gate, route one: PROVED_ON_SHIP

round 12's record for the same unit:
    outcome                PROVED_ON_SHIP
    layer5_normalized_text If(Extract(31, 0, v0) | Extract(31, 0, v1) == 0, 0, 1)

this run's normalized text:
    If(Extract(31, 0, v0) | Extract(31, 0, v1) == 0, 0, 1)
    character-for-character identical to round 12's: True
```

GLOSS: this body has no label, no conditional transfer and no `call`,
so its graph is one block and the walk over it is the loop round 12
ran. The verdict and the text are the same ones, character for
character.

**That is one unit. §7 is the same claim over the whole population.**

---

# 4. Stepping into a callee: the entry, the return, and whether it is right

## 4.1 The entry and the return, printed

LITERAL — `acceptance64_printed.txt` part 3, on `c/regen_1056`
(`canon39_regen_store/op_units2_c_c0002.json`), whose answer home is
`%xmm0`:

```
     0  push %rbx
     1  mov %edi,%ebx
     2  call L0 !!reloc=R_X86_64_PLT32:__extendhfsf2-0x4
     3  L0:
     4  cvtsi2ss %ebx,%xmm1
     5  addss %xmm1,%xmm0
     6  call L1 !!reloc=R_X86_64_PLT32:__truncsfhf2-0x4
     7  L1:
     8  pop %rbx
     9  ret

  THE ENTRY, at line `call L0`:
    the transfer's own text names 'L0'; the RELOCATION names '__extendhfsf2'
    the callee arch unit entered: runtime/clang/__extendhfsf2
      archive        /usr/lib/llvm-21/lib/clang/21/lib/linux/libclang_rt.builtins-x86_64.a
      member         extendhfsf2.c.o
      instructions   40
      ITS OWN arrival contract (the families its text reads before it
      writes them): %xmm0, %rax
      the caller's registers already hold those values, so nothing
      about a calling rule is assumed
    THE RETURN: the answer register computed off the callee's own body
      is %xmm0
    the callee's body is itself a graph: 8 blocks, 3 of them ending in
      a conditional transfer
```

GLOSS. The transfer's own text says `call L0`, the very next
instruction, because the object file is not linked; the name survives
only in the relocation, which `ledger.transfer_callee` reads (log_161's
finding, log_167 §3.2). The walk does NOT assume a calling rule: the
callee's arrival contract is the set of families ITS OWN TEXT reads
before it writes them, and the caller's registers already hold those
values, so the shared machine state IS the hand-over. The answer
register is computed off the callee's body — `%xmm0` when the body
writes `%xmm0`, `%rax` otherwise — rather than declared, because the
callee record states no answer home and inventing one would be an
unruled rule.

## 4.2 Is the walk of that body RIGHT? Numbers through it

The callee's own body has five conditional transfers over forty
instructions. If the fork, the merge or the unreachable-side rule were
wrong, the number coming out would be wrong. So concrete halves were
put through it and the bits read back.

LITERAL — `acceptance64_printed.txt` part 3b:

```
  half in    what it is             float out    read as
  0x3C00     1.0                    0x3F800000   1.0
  0xC000     -2.0                   0xC0000000   -2.0
  0x0001     the smallest subnormal 0x33800000   5.960464477539063e-08
  0x7C00     +infinity              0x7F800000   inf
  0x3555     the nearest half to 1/3 0x3EAAA000  0.333251953125

  and the inverse routine `clang/__truncsfhf2` (101 instructions, 18
  blocks), narrowing them back:
    1.0    -> 0x3C00
    -2.5   -> 0xC100
    0.0    -> 0x0000
```

GLOSS: every one is the IEEE-correct widening. `0x0001` is the case the
body's `bsr` / `shl` branch exists for — the smallest half subnormal is
2^-24, which is 5.960464477539063e-08, and that is what came out.
Evidence class: forced by construction. The machine's own body was run
over values whose right answers are fixed by IEEE 754, and only a
correct fork, merge and unreachable-side rule produce them.

## 4.3 The one thing the brief asked for that did not happen, said plainly

The brief asked that one `__extendhfsf2` caller "prove THROUGH its
callee". **No canon39 unit's proof currently RESTS on its callee's
answer, and this is why.**

LITERAL — `acceptance64_printed.txt` part 3, the two callers side by
side:

```
UNIT cpp/regen_12920   its answer home: %rax, 64 bits
  the gate, route one: PROVED_ON_SHIP
  `Reference.answer_of` for the caller, simplified: seed_rax

UNIT c/regen_1056      its answer home: %xmm0, 32 bits
  the gate, route one: DISPROVED
  `Reference.answer_of` ...: Concat(Extract(31, 16, fp.to_ieee_bv(...
```

GLOSS. `cpp/regen_12920` is the unit the brief names. Its body is
`push %rax` … `pop %rax`, and canon39 records its answer home as
`%rax`, so its OUT-0 is the caller-saved register the body pushed and
popped — the callee's answer sits BESIDE the answer, not in it. The
walk does enter both callees (§4.1 prints the entries), and the unit
proves, but the proof does not rest on them. `c/regen_1056`'s answer
home IS `%xmm0`, so the callee's answer IS the unit's answer, and there
route one DISPROVES — because the reference now models the callee and
the ledger does not. That is §5.3, and it is the round's central
finding.

---

# 5. The re-gate: all 30,432 terms, both routes

## 5.1 The four states, per population

LITERAL — `audit64_printed.txt`:

```
population     state         task 61    task 64     move
original       proved           1671       1665       -6
original       disproved           0         49      +49
original       undecided          57         14      -43
original       no term            35         35       +0
interpreter    proved              9          9       +0
interpreter    disproved           0          0       +0
interpreter    undecided           0          0       +0
interpreter    no term             0          0       +0
regenerated    proved          24360      24920     +560
regenerated    disproved           0       3085    +3085
regenerated    undecided        3808        271    -3537
regenerated    no term           492        384     -108
ALL            proved          26040      26594     +554
ALL            TOTAL           30432      30432

the round-12 baseline the brief names: 26,040 proved / 0 disproved /
3,865 undecided / 527 no term over 30,432
recomputed here from `term61_store`: 26040 / 0 / 3865 / 527 over 30432
```

GLOSS, and the populations named: 30,432 is canon39's WRAPPED_TEXT_PROVED
count, split 1,763 original / 9 interpreter / 28,660 regenerated. The
brief's population line for the original set is 1,763; that is 1,671
proved + 57 undecided + 35 no term = 1,763, so the split holds. The
whole-population line is **26,594 proved / 3,134 disproved / 285
undecided / 419 no term**.

## 5.2 Every movement, with its computed cause

LITERAL — `audit64_printed.txt`, "THE TRANSITION" and "EVERY MOVEMENT,
BY COMPUTED CAUSE", both joined on the unit name:

```
task 61    task 64       units
proved     proved        25793
undecided  disproved      2893
undecided  proved          708
no term    no term         419
undecided  undecided       264
proved     disproved       233
no term    proved           93
proved     undecided        14
no term    disproved         8
no term    undecided         7

-- undecided -> disproved  (2893 units)
     2860 | the unit's own stored canon39 ledger carries NO row for its
          | transfer into the compiler's own runtime, so its term
          | asserts the transfer changed nothing; the reference now
          | walks that callee's body, and the two disagree
       33 | z3 found a starting state under which the two sides differ

-- undecided -> proved  (708 units)
      442 | the reference now enters the attached runtime callee's body
          | and returns through its answer register
      234 | the reference now follows this body's own branches and
          | merges them at the join
       32 | the reference now models something this body spells that it
          | refused before (the narrow division and widening multiply,
          | or a rip-relative address)

-- proved -> disproved  (233 units)
      233 | A PROOF WAS LOST: z3 found a starting state under which the
          | two sides differ

-- no term -> proved  (93 units)
       78 | the reference now models something this body spells that it
          | refused before
       15 | the reference now follows this body's own branches

-- proved -> undecided  (14 units)
       14 | A PROOF WAS LOST: the solver did not answer inside its
          | 3000 ms limit

-- no term -> undecided  (7 units)
        3 | this opcode reads the signed-overflow bit and no
          | flag-setting arch opcode precedes it in this body
        2 | arch opcode 'pcmpeqd' is a census row
        2 | the solver did not answer inside its 3000 ms limit

in task 64 and not task 61: 0
in task 61 and not task 64: 0
```

The two causes that are COMPUTED rather than read off a record are
computed off the unit's own artifacts: "the reference now follows this
body's own branches" fires when the unit's own text carries a
conditional transfer; "the stored ledger has no row for the transfer
into the compiler's own runtime" fires when the unit's own text carries
a `call` whose callee one of this machine's builtins archives DEFINES
and the unit's OWN STORED LEDGER carries no row whose producer names
that callee.

## 5.3 THE FINDING: `destination_rules` rule 4 is wrong, and 2,862 units say so

LITERAL — `CORE_0_3_5_3_3_destination_rules.md`, `## design` rule 4 as
it stands:

```
4. A transfer into the compiler's OWN runtime writes the accumulator,
   and the row it writes is produced by
   {"kind": "runtime_callee", "callee": ...}.
```

GLOSS of what is wrong with it, in two parts.

- **"the accumulator" is wrong for a routine that answers in `%xmm0`.**
  `__extendhfsf2`, `__truncsfbf2`, `__truncsfhf2`, `__floatsitf` and
  every other float lowering leave their answer in `%xmm0`. The rule
  makes a row on `%rax` and leaves the caller's `%xmm0` lineage
  untouched, so the ledger's term for the value after the transfer is
  the value BEFORE it.
- **One row is wrong even when the register is right.** The callee's
  body writes several places; the rule records one.

MEASURED, over canon39's 30,432: **2,862 units carry a transfer into a
routine one of this machine's archives defines AND no ledger row naming
it** (2,860 of the undecided→disproved plus 2 of the no-term→disproved).
Their stored term therefore asserts the transfer changed nothing. With
the reference now walking that callee's body, z3 disproves every one of
them — and the disproof is right: the term is not the unit's answer.

Why canon39's ledgers are like that, computed rather than guessed:
`canonical_form.runtime_routine_names()` reads
`runtime_callee_units.json`, task 59's file, and canon39 was built with
the four-name division family it holds. Task 63 found the real
population is 36 names and wrote `canon39_callee_units.json`; that file
did not exist when canon39's ledgers were written.

**The general fix is one thing in one place**, and it is NOT this
task's node: the runtime set handed to `ledger.Ledger` must be the
archive index's own answer (`runtime_callee.is_runtime_routine`), and
the row it makes must be the callee's ANSWER REGISTER computed off its
body. Realizing it means REBUILDING canon39 — `term.relink` checks its
re-run against the stored ledger row for row, so simply widening the
set here would refuse every one of those 2,862 units instead of
repairing them. Written into the destination_rules CORE as a settled
correction with its provenance, and into that node's PROGRESS as
**planned, round 14**.

**Recorded honestly:** this correction was written into the CORE AFTER
the measurement that produced it, which is the reverse of the binding
rule's order. It could not have gone first — it was not known until the
re-gate ran — and it is a finding of the run rather than a shape the
work needed in advance.

## 5.4 The brief's expectation, tested rather than assumed

LITERAL — `audit64_printed.txt`, "THE FOUR NAMED CAUSES OF log_160
SECTION 1.7, TESTED". The bucket is each unit's OWN recorded reason in
`term61_store`:

```
task 61's undecided, by its own reason        units   what task 64 made of them
runtime callee not yet attached                3359   {'proved': 410, 'disproved': 2716, 'undecided': 233}
a conditional transfer                          474   {'proved': 266, 'disproved': 177, 'undecided': 31}
a rip-relative address computation               32   {'proved': 32}
a narrow division or widening multiply            0   {}
another reason                                    0   {}
```

GLOSS, against the brief's "3,419 + 499 + 32 + 20 decide":

- **The populations are not the brief's, and this is why.** The brief
  quotes log_160 §1.7, which counted canon38's 30,436. Over canon39's
  30,432 the same buckets are 3,359 / 474 / 32 / **0**. The narrow
  division and widening multiply bucket is EMPTY on canon39: those 20
  units were canon38's, and canon39 either refused them or they build
  no term. The form is modelled anyway, because the CORE rules it and
  because five units stopped just past it (§5.5).
- **They do decide.** 3,865 undecided becomes 285 — 93% of the bucket
  moved. The rip-relative bucket decides completely and positively:
  32 of 32 prove.
- **They do not all decide POSITIVELY, and that was not knowable in
  advance.** 2,716 of the runtime-callee bucket and 177 of the
  conditional-transfer bucket are disproved, for the one cause of §5.3.

## 5.5 Five units stopped just past the division, on `%ah`

`%ah` is bits 15..8 of the `%rax` family — not the low byte and not a
family of its own. `canon.FAMILY_OF` holds no entry for it, because no
canonical text names one; a body that divides at width 8 does, because
the machine puts the remainder there.

LITERAL — `regression64.json`, before the fix:

```
c/regen_15263   was: REFUSE:a division at width 8 is not modeled
                now: REFUSE:operand '%ah' is neither an immediate, a
                     register nor a memory operand this file reads
```

and the four others (`cpp/regen_14486`, `cpp/regen_14502`,
`cpp/regen_15238`, `cpp/regen_15254`) say the same. Fixed at first
observation, in the shared layer (`Operands.is_high_byte`,
`HIGH_BYTE_OF`), not reported twice. After the fix all five build a
term and prove.

## 5.6 The consistency line

LITERAL — `audit64_printed.txt`:

```
units proved on one route and disproved on the other: 0
```

It was **230** before §6's fix.

## 5.7 Zero regression, and the 247 that moved

LITERAL — `audit64_printed.txt`:

```
units PROVED in task 61 and not proved in task 64: 247
   c/op_117: z3 found a starting state under which the two sides differ
   c/op_153: the solver did not answer inside its 3000 ms limit, so the
             verdict is undecided and never disproved
   ...
```

Two causes, both named, and one of them proved:

- **233 units lost their proof to a z3 COUNTEREXAMPLE against the
  unit's own ship body.** That is the strongest class of cause the line
  has: not "the tool refused", but "here is a starting state under
  which the term and the machine differ". §6 is what those proofs were
  resting on.
- **14 units lost their proof to the SOLVER'S OWN TIME LIMIT**, 3,000
  ms, which the gate CORE fixes and records on every verdict precisely
  so an UNDECIDED can be re-read later. A timeout is a named cause but
  not by itself a proved one, so §8 re-read all fourteen at a longer
  limit: **at 120,000 ms every one of them is DISPROVED**. The clock was
  not hiding a proof. So all 247 losses carry a proved cause, and the
  round is **zero regressions in the ruled sense**.

---

# 6. The second defect: route two was walking two alternatives as one

## 6.1 What it did

`Gate.prove_term_against_text` walks a body in TEXT ORDER with the
ledger's own meanings — that is its point, it tests the ledger's WIRING
rather than the meanings. It skipped a conditional transfer silently.

LITERAL — `gate.py` as it stood:

```
            if mnemonic.startswith("j") and not is_flag_reader(mnemonic):
                continue
            if mnemonic in ("call", "ud2", "nop", "hlt") or \
                    mnemonic.startswith("j"):
                ...
                continue
```

## 6.2 What that cost, measured

LITERAL — the worked case, `c/op_117`, printed this session:

```
   0 test %rdi,%rdi
   1 js L0
   2 cvtsi2ss %rdi,%xmm1
   3 addss %xmm1,%xmm0
   4 ret
   5 L0:
   6 mov %rdi,%rax
   7 shr $1,%rax
   8 and $0x1,%edi
   9 or %rax,%rdi
  10 cvtsi2ss %rdi,%xmm1
  11 addss %xmm1,%xmm1
  12 addss %xmm1,%xmm0
  13 ret

  REF (route one) : If(0 <= seed_rdi, <convert directly>, <halve, convert, double>)
  TERM            : <convert directly> + <halve, convert, double>
  route one: DISPROVED   counterexample: [seed_xmm0 = 1596703311,
                                          seed_rdi = 7734352952421377967]
  route two: PROVED_ON_SHIP
```

GLOSS: this is the halve-convert-double idiom AgentMemory names — the
compiler's own lowering of unsigned-to-float, where `js` chooses
between converting the value directly and halving it first. The two
stretches are ALTERNATIVES. Route two read them as one after the other
and ADDED BOTH ANSWERS TOGETHER, and called the ledger's term (which
does the same) proved.

MEASURED over canon39's 30,432, before the fix: **230 units route two
called PROVED while route one DISPROVED with a counterexample**. Every
one of the 230 has a conditional transfer whose target is a label the
same body defines, and none has a `call`. That is exactly the
contradiction the gate CORE names: "a unit proved on one and disproved
on the other is a defect to be found, not a tie to be broken."

## 6.3 The fix, and what it is careful about

LITERAL — `gate.transfers_inside_the_unit`, and the walk's new refusal:

```
    raise NotWalkable(
        "this body transfers to %r, a label it defines itself, so the "
        "page order is not the run order and a text-order walk has no "
        "one answer to reach" % line)
```

GLOSS: route two refuses BY NAME when a transfer's target is a label
the same body defines. When the target is NOT defined there, the
transfer leaves the unit and the fall-through is the only reachable
path — so the walk continues exactly as before, and agrees with the
reference's own unreachable-side rule by construction. Route two keeps
using `layer4`'s table, so the two routes stay independent evidence.

After the fix the consistency line is 0, and the 230 are DISPROVED —
which they were on the only route that reads the body correctly.

---

# 7. The regression check: unchanged where it should be, over the WHOLE population

The brief asks for "a computed sample where behaviour SHOULD be
unchanged". The population is computed and it is not a sample: every
canon39 proved unit whose own text has no label, no conditional
transfer, no `jmp`, no `call` and no `ud2`. Such a body's graph is one
block, and the walk over one block is the loop the module ran before.

LITERAL — `regression64_printed.txt`:

```
population: ALL 30,432 canon39 proved units, split by what the unit's
OWN TEXT spells -- no sample
the module before this task: d3de348:Research/op_pipeline/reference.py

                                   straight line  carries a graph
identical                                  25827                0
refusal became a term                        110              539
refused both times, wording moved              0             3956
term became a refusal                          0                0
CHANGED ANSWER                                 0                0
total                                      25937             4495

THE CHECK: a body with no label, no conditional transfer, no `jmp`, no
`call` and no `ud2` must answer identically.  Units where it did not: 0
```

GLOSS: both versions of `reference.py` are loaded side by side — the
working tree's and the one git holds at `d3de348`, the last commit
before this task's first edit — and each is asked for the same unit's
answer term. Over the 25,937 straight-line units, 25,827 answer
character-for-character the same, 110 turn a refusal into a term (the
rip-relative address and the narrow division), and **0 change an answer
and 0 turn a term into a refusal**. In the other column, where the
answer is expected to change, 539 turn a refusal into a term and 3,956
refuse both times with the wording moved.

Evidence class: this one is exhaustive over its population, not
sampled, so it proves rather than merely refutes — about the module,
under the assumption that a body with none of those five things has one
block, which the graph builder's own code makes true by construction.

---

# 8. The 14 proofs lost to the solver's own clock

LITERAL — `timeout64_printed.txt`:

```
population: the units task 61 proved and this round's re-gate left
UNDECIDED because the solver ran out of time -- 14 of the 30,432.
   c/op_153   c/op_225   c/op_230   c/regen_13067   c/regen_13235
   c/regen_6795   c/regen_6963   c/regen_8834   cpp/op_153
   cpp/op_225   cpp/regen_11958   cpp/regen_11961   cpp/regen_13058
   cpp/regen_13226

at a 30000 ms limit (170 s of wall clock over the 14):
   {'DISPROVED': 10, 'UNDECIDED': 4}

at a 120000 ms limit (198 s of wall clock over the 14):
   {'DISPROVED': 14}
```

GLOSS, and it settles the one open question §5.7 left. The 3,000 ms
limit was not hiding a proof. Given ten times the limit, ten of the
fourteen turn out DISPROVED; given forty times it, **all fourteen do**.
So every one of the 247 units that lost a proof this round lost it to a
z3 COUNTEREXAMPLE against the unit's own ship body — a named, PROVED
cause, which is what the zero-regression rule asks for. **Zero
regressions in the ruled sense.**

`regate64_store` keeps its 3,000 ms verdicts and the round's counts are
the counts one fixed limit produced; this is a re-reading beside the
run, which is what the gate CORE records the limit on every verdict
for. Raising the default is NOT done here — it would change what every
other number in this report means.

---

# 9. The guard, the tree, and the standing requirements

## 9.1 The unmodified guard, one process

LITERAL — `guard64_transcript.txt`:

```
guard64.py -- every artifact task 64 writes, unmodified guard, ONE
process.  Nothing was added to any field set, and no artifact was
declared out of the walk.
$ python3 check_no_spelling_keys.py <334 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
PASS audit64.json -- no operator token in any key, grouping, pairing or row structure
PASS regression64.json -- ...
PASS canon39_interp.json -- ...          (the 332 shards of regate64_store)
...
PASS canon39_wrapped_swift.json -- ...

GUARD EXIT CODE = 0
```

```
$ python3 guard64.py
TASK 64: 334 paths  PASS 334  FAIL 0  exempt 0  exit 0

$ cd ~/Programming/PseudoCoupHQ/Research/op_pipeline && grep -c exempt guard64_transcript.txt
0
```

GLOSS: 334 paths — `audit64.json`, `regression64.json` and every one of
the 332 shards of `regate64_store`, which carry one record per unit and
are therefore a row structure the ban applies to exactly as it applies
to the summaries. Nothing was added to any field set, no artifact was
declared out of the walk, and no exemption was declared.

## 9.2 The tree

LITERAL — `python3 ~/Programming/PlanPlan/framework/check_plans.py ~/Programming/PseudoCoupHQ/Planning`:

```
[ERROR] dangling-path: ~/Programming/PseudoCoupHQ/DevComms/log_107_task21_interp_ does not exist
[ERROR] dangling-path: ~/Programming/PseudoCoupHQ/DevComms/log_110_task25_ does not exist
[ERROR] dangling-path: ~/Programming/SandboxDesign/allow.sh does not exist
[ERROR] dangling-path: ~/Programming/Sources/llvm- does not exist
summary: 4 error(s), 3 warning(s)
```

GLOSS: all four are truncated paths in files this task did not touch,
and all four predate it — they are the same four log_167 §7.2 reported.
Dashboards were regenerated.

## 9.3 Which files were edited rather than added

The brief allows extending `reference.py`, `ledger.py`
(`DESTINATION_RULES`) and `gate.py`. Three live modules were edited and
one of them is not on that list; the reasoning is stated rather than
assumed.

- `reference.py` — allowed, and edited: the graph (`Body`, `Block`),
  the merge (`MachineState.fork`, `merge_two`, `merge_flags`,
  `choose`), the walk (`walk_body`, `walk_block`, `hand_on`,
  `merge_incoming`, `record_guard`), the callee step
  (`enter_callee`, `answer_register_of`, `callees_for`), the
  conditional-transfer builder, the rip-relative address, the narrow
  division and widening multiply (`build_narrow_division`,
  `build_narrow_wide_multiply`, `place_bits`), and the high-byte
  registers.
- `gate.py` — allowed, and edited at one place:
  `transfers_inside_the_unit` and the refusal §6.3 quotes.
- `ledger.py` — READ, not edited. `transfer_callee` is called to read a
  callee's name out of a relocation. Its `DESTINATION_RULES` table is
  unchanged: its rows already fire at any operand count and name the
  accumulator and the data register, and WHICH BITS of those the two
  narrow widths use is the reference's rule, not a second table. The
  defect §5.3 names is written into that node's CORE, not into its
  code, because realizing it needs a canon rebuild.
- `term.py` — EDITED, and it is NOT on the brief's list. One loop:
  `Term.runtime_row` walked an attached callee's body a line at a time
  through `Reference.step`, which stops at the first transfer, so a
  callee with branches was refused. It now calls `Reference.walk_body`,
  the one walk the reference CORE names, plus one new method
  `callees_beside` so a nested callee (`__divti3` reaches
  `__udivmodti4`) is found in the same archive. The ground: this is the
  general fix in the shared layer for a cause that shows in both gate
  routes, and putting it anywhere else would have been a second walk
  beside the one the CORE names. It is flagged here for task 65, whose
  node `term` owns that file.
- Nothing under `canon*`, `layer4*`, `ledger47`/`ledger48`, `gate48` or
  `textwalk48` was touched.

LITERAL:

```
$ git -C ~/Programming/PseudoCoupHQ diff --stat Research/op_pipeline/check_no_spelling_keys.py
(no output -- the checker is unmodified)
```

## 9.4 One process

`regate64_run.py` runs in ONE process, resumable through
`regate64_state.json`; there is no pool of workers and no second
interpreter. The same is true of `audit64.py`, `regression64.py`,
`acceptance64.py` and `timeout64.py`.

---

# 10. File inventory

## 10.1 Written by this task

Under `~/Programming/PseudoCoupHQ/Research/op_pipeline/`:

| file | what it is |
|---|---|
| `regate64_run.py` | the re-gate of all 30,432 canon39 terms, both routes, one process, resumable |
| `regate64_store/` | its 332 shards, one record per unit |
| `regate64_state.json`, `regate64_run.log` | the resume file and the run's own log |
| `audit64.py` | the re-gate read against round 12's, every movement with its computed cause |
| `audit64.json`, `audit64_printed.txt` | its product and its transcript |
| `acceptance64.py` | the four acceptance parts, printed with values |
| `acceptance64_printed.txt` | its transcript |
| `regression64.py` | both versions of `reference.py` asked the same question over the whole population |
| `regression64.json`, `regression64_printed.txt`, `regression64_run.log` | its product, transcript and log |
| `timeout64.py` | the 14 proofs lost to the solver's clock, re-read at longer limits |
| `timeout64.json`, `timeout64_printed.txt`, `timeout64_run.log` | its product, transcript and log |
| `guard64.py` | the unmodified guard, one process, over every artifact this task writes |
| `guard64.json`, `guard64_transcript.txt` | the guard's counts and its transcript |

## 10.2 Edited

- `~/Programming/PseudoCoupHQ/Research/op_pipeline/reference.py`
- `~/Programming/PseudoCoupHQ/Research/op_pipeline/gate.py`
- `~/Programming/PseudoCoupHQ/Research/op_pipeline/term.py` (one loop
  and one new method — §9.3)

## 10.3 Plan files touched

COREs:

- `.../node_0_3_5_4_reference/CORE_0_3_5_4_reference.md`
- `.../node_0_3_5_4_reference/node_0_3_5_4_0_opcode_table/CORE_0_3_5_4_0_opcode_table.md`
- `.../node_0_3_5_4_reference/node_0_3_5_4_1_machine_state/CORE_0_3_5_4_1_machine_state.md`
- `.../node_0_3_5_3_ledger/node_0_3_5_3_3_destination_rules/CORE_0_3_5_3_3_destination_rules.md`

PROGRESS files:

- `.../node_0_3_5_4_reference/PROGRESS.md`
- `.../node_0_3_5_4_reference/node_0_3_5_4_0_opcode_table/PROGRESS.md`
- `.../node_0_3_5_4_reference/node_0_3_5_4_1_machine_state/PROGRESS.md`
- `.../node_0_3_5_3_ledger/node_0_3_5_3_3_destination_rules/PROGRESS.md`
- `.../node_0_3_5_5_gate/PROGRESS.md`

All under
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/`.
Plus the DASHBOARD.md files regenerated by
`python3 ~/Programming/PlanPlan/framework/generate_dashboards.py ~/Programming/PseudoCoupHQ/Planning`.

---

# 11. Resume state

**The population finished in-session; there is nothing to resume.**
`regate64_state.json` lists all 332 shards as done and
`regate64_run.log`'s last line reads `all 332 shards re-gated`. Running
`regate64_run.py` again does nothing but re-read the state file. To
re-run from scratch, delete `regate64_store/` and
`regate64_state.json`; the run takes about ten minutes in one process
and writes a shard at a time, so a stopped run continues where it
stopped.

---

# 12. What task 65 receives

- `regate64_store/` — 30,432 re-gated records, the four states as §5.1
  counts them, each with its verdict, its route, its reason and (for a
  branch-bearing body) its guard rows.
- **26,594 proved terms**, up from 26,040, and **3,134 disproved**,
  which were 0. Task 65's pool is built over the proved set, so it
  gains 554 members and loses the 247 §5.7 names.
- **One thing to know:** 2,862 of the 3,134 disproofs share ONE cause,
  §5.3's — canon39's ledgers were built with a four-name runtime set
  and the archive index names 36. A canon rebuild with the wider set
  is what turns those disproofs into proofs, and it is round 14's, not
  task 65's. Until it happens the pool should be read as covering the
  units whose bodies do not transfer into the compiler's own runtime.
- `term.py` gained one loop and one method (§9.3), in the file task
  65's node owns.
