# log 160 — TASK 58: `gate.py`, and all 30,436 canon38 terms re-gated

Date: 2026-09-03. Home: `PRIVATE/PseudoCoupHQ/Research/op_pipeline`.
Node: `hq.research.compiler_graph.gate`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_5_gate/`)
and its three sub-nodes `verdict`, `structural_checks`,
`zero_regression`.
Brief: log 158, TASK 58. Reads task 57's `reference.py` (log 159) and
task 53's records (log 153).

---

# 0. The walk, in plain words, before any figure

**The four names, each introduced before it is used.**

- **A GATE** is the object that decides whether a unit is counted.
  Nothing in this research is counted unless it passed one. There is
  now one, `gate.py`, class `Gate`.
- **A VERDICT** is what a gate returns about one unit: an outcome, the
  reason in plain words, the solver's own counterexample when there is
  one, which route produced it, and the solver time limit that was in
  force.
- **ROUTE ONE** puts the ledger's own term against the value the
  unit's own ship body leaves, as `reference.Reference` walks that
  body. It tests the MEANINGS.
- **ROUTE TWO** puts the same term against the same body walked in
  TEXT ORDER using the ledger's own meanings table. Because both sides
  then carry one set of meanings and differ only in what ORDERED the
  computation, agreement is evidence about the LEDGER'S WIRING.

**What this lap did.** It wrote the node's own module — `Gate` with
the CORE's five methods and `Verdict` with the sub-node's five
attributes — and re-gated every one of the 30,436 units task 52
proved, on both routes, against task 53's recorded verdicts.

**The headline, with its population.** Over **all 30,436 canon38
units**: **23,132 proved / 415 withdrawn / 5,602 undecided / 1,287 no
term** becomes **25,179 proved / 0 withdrawn / 3,970 undecided / 1,287
no term**. Every one of the 415 remainder withdrawals proves. 1,632 of
the 5,602 undecided decide. **Zero proofs were lost**, and the
consistency line is **0**.

**What did not go the predicted way, said here rather than buried.**
The first pass came back with a consistency line of **1,338** — units
route two proved and route one disproved. That is exactly the shape
the gate CORE calls "a defect to be found, not a tie to be broken",
and the defect was in `reference.py`: the flag triple for the logic
family carried the setter's two OPERANDS instead of the two values a
condition actually reads. §3 is that finding in full, with the term
printed both ways. It is one line of `reference.py` and it moved 1,338
units.

---

# 1. The verdict, with its population

## 1.1 The population line

Every unit task 52 proved: **9 interpreter, 1,763 original, 28,664
regenerated — 30,436 in all**. Nothing is sampled; both routes ran on
every one. The join against task 53's records is exact.

LITERAL — `audit58_printed.txt`:

```
POPULATION LINE
  units in task 53's records: 30436
  units in task 58's records: 30436
  in task 53 and not in task 58: 0
  in task 58 and not in task 53: 0
```

## 1.2 The one-line state

**Of 30,436 canon38 units, 25,179 carry a term proved on at least one
gate route, 0 are disproved, 3,970 are undecided on both routes, and
1,287 build no term at all. No unit proved in task 53 lost its
proof.**

## 1.3 The four states, against log 153 §1.2

The four states are defined once, in `audit58.py`'s own docstring, and
are exactly the reading log 153 used, so the two runs are directly
comparable: a unit is `withdrawn` when either route disproved it; else
`proved` when either route proved it; else `no term` when the ledger
built no OUT-0 term; else `undecided`.

LITERAL — `audit58_printed.txt`:

```
ALL THREE POPULATIONS, against log 153 section 1.2
  state                log 153   task 53   task 58    delta
  proved                 23132     23132     25179    +2047
  withdrawn                415       415         0     -415
  undecided               5602      5602      3970    -1632
  no term                 1287      1287      1287       +0
  units                  30436     30436     30436

  log 153's per-population figures, reproduced from its own section 1.4, against this run:
    (no MISMATCH line above means every one of the twelve figures agrees)
```

GLOSS. The `task 53` column is not copied from log 153 — it is this
run's own reading of task 53's stored records, and the twelve
per-population figures log 153 §1.4 printed were checked against it
one by one, mechanically. No line disagreed.

## 1.4 Per population, which is what the brief asked for

LITERAL — `audit58_printed.txt`:

```
POPULATION: interpreter
  units 9
  state                 task 53   task 58    delta
  proved                      9         9       +0
  withdrawn                   0         0       +0
  undecided                   0         0       +0
  no term                     0         0       +0
  route one (the term against the ship body) proved 9
  route two (the text-order walk) proved 8

POPULATION: original
  units 1763
  state                 task 53   task 58    delta
  proved                   1635      1671      +36
  withdrawn                  12         0      -12
  undecided                  81        57      -24
  no term                    35        35       +0
  route one (the term against the ship body) proved 1625
  route two (the text-order walk) proved 1623

POPULATION: regenerated
  units 28664
  state                 task 53   task 58    delta
  proved                  21488     23499    +2011
  withdrawn                 403         0     -403
  undecided                5521      3913    -1608
  no term                  1252      1252       +0
  route one (the term against the ship body) proved 23299
  route two (the text-order walk) proved 21084
```

## 1.5 The consistency line

LITERAL — `audit58_printed.txt`:

```
CONSISTENCY -- units proved on one route and disproved on the other: 0
```

## 1.6 Every movement, with its cause

The transition table is unit by unit over the 30,436, and every cell
of it is one of five.

LITERAL — `audit58_printed.txt`:

```
THE TRANSITION, unit by unit
  task 53        task 58          units   sightings
  proved         proved           23132   c/op_0, c/op_1, c/op_101
  undecided      undecided         3970   c/regen_1001, c/regen_10073, c/regen_10087
  undecided      proved            1632   c/op_212, c/op_218, c/op_222
  no term        no term           1287   c/op_100, c/op_21, c/op_22
  withdrawn      proved             415   c/op_246, c/op_247, c/op_252
```

The causes are COMPUTED, never typed: the cause of a gained proof is
the reason that unit's OWN task-53 record recorded for not proving it.

LITERAL — `audit58_printed.txt`:

```
EVERY GAINED PROOF, BY ITS COMPUTED CAUSE
     705  the old run's route-one reason: this body has a flag-reading arch opcode whose nearest preceding flag-setting arch opcode is out
          sightings: c/regen_15786, c/regen_16626, c/regen_16850
     466  the old run's route-one reason: the reference simulator: mnemonic 'div' has no symbolic model in this checker
          sightings: c/op_212, c/op_218, c/op_222
     415  the old run DISPROVED it: z3 found a starting state under which the ledger-transcribed term and the unit's own ship body d
          sightings: c/op_246, c/op_247, c/op_252
     298  the old run's route-one reason: the reference simulator: mnemonic 'fldt' has no symbolic model in this checker
          sightings: c/regen_10161, c/regen_1033, c/regen_10441
     146  the old run's route-one reason: the reference simulator: mnemonic 'mul' has no symbolic model in this checker
          sightings: c/regen_10091, c/regen_10092, c/regen_10147
      16  the old run's route-one reason: the reference simulator: mnemonic 'pextrw' has no symbolic model in this checker
          sightings: c/regen_11281, c/regen_12271, c/regen_1873
       1  the old run's route-one reason: z3 returned unknown
          sightings: cpp/regen_14397

EVERY LOST PROOF, BY ITS COMPUTED CAUSE
  (none)
```

GLOSS, cause by cause. The 2,047 gained proofs are five mechanisms and
one solver margin:

- **415 — the remainder.** The superseded reference computed the
  division remainder with z3py's `%`; the machine's remainder is
  `SRem`. §4.1 is that unit's values in motion.
- **705 — the stale flag guard.** `gate48.py` returned UNDECIDED
  whenever a body's flag-reading opcode followed a setter outside its
  own remembered set of four, because its reference would have
  answered from an earlier instruction's flags. `reference.py`
  rebuilds the condition from whatever set it, so the guard is gone
  and the units decide.
- **466 + 146 — `div` and `mul` had no model at all** in the
  superseded reference; the one opcode table has them, both halves.
- **298 — `fldt` had no model at all**: the x87 register stack did not
  exist in either superseded reference. §4.2 is one of these with its
  values.
- **16 — `pextrw`**, a lane read the superseded reference did not
  carry.
- **1 — the solver answered at the margin** where it previously
  returned `unknown` (`cpp/regen_14397`).

## 1.7 What is still undecided, by the artifact's own recorded reason

LITERAL — `audit58_printed.txt`, the head of the table:

```
WHAT IS STILL UNDECIDED, BY THE NEW RUN'S OWN RECORDED REASON (route one)
    3419  refused: runtime callee not yet attached (task 59, node 0_3_5_1_8) -- the reference's ow
     177  the reference: arch opcode 'js' is a census row, not a silent gap: a transfer or trap, a
     138  the reference: arch opcode 'jl' is a census row, not a silent gap: a transfer or trap, a
      82  the reference: arch opcode 'je' is a census row, not a silent gap: a transfer or trap, a
      36  the reference: arch opcode 'jb' is a census row, not a silent gap: a transfer or trap, a
      34  the reference: arch opcode 'jo' is a census row, not a silent gap: a transfer or trap, a
      32  the reference: an address computation over base register '%rip': this reference has no m
      20  the reference: arch opcode 'jbe' is a census row, not a silent gap: a transfer or trap, 
      10  the reference: a division at width 16 is not modeled
       6  the reference: arch opcode 'jge' is a census row, not a silent gap: a transfer or trap, 
       5  the reference: a division at width 8 is not modeled
       5  the reference: arch opcode 'jg' is a census row, not a silent gap: a transfer or trap, a
       4  the reference: a widening multiply at width 8 is not modeled: its destination pair is th
       1  the reference: arch opcode 'jne' is a census row, not a silent gap: a transfer or trap, 
       1  the reference: a widening multiply at width 16 is not modeled: its destination pair is t
```

GLOSS, and the honest reading. **3,419 of the 3,970 — 86% of what is
left — are one thing: a body whose answer comes from a transfer into
the compiler's own runtime (`__divti3` and its family), whose body is
not attached to the unit yet.** That is task 59's work under node
`0_3_5_1_8 runtime_callee`, and the owner's round-12 ruling is that those
bodies ARE in scope and are extracted from the toolchain's own
archive. The wording on every one of those verdicts says so: *"refused:
runtime callee not yet attached (task 59, node 0_3_5_1_8)"*. The
earlier "out of scope" framing is superseded and is not used anywhere
in this task's code or artifacts. **499 are conditional transfers** —
the reference walks a body in TEXT ORDER and refuses a branch rather
than guessing which side runs, which the reference CORE states as its
own limit. **32 are an address computation off `%rip`**, and **20 are
the 8- and 16-bit division and widening-multiply forms**.

The 1,287 that build no term are unchanged, and they are the ledger's
census rows, not the gate's: nothing about the gate can move them.

---

# 2. The module, and what the tree asked for

## 2.1 One class, the CORE's five methods

LITERAL — `gate.py`'s own shape, against the CORE's `## design` block:

| the CORE says | `gate.py` has |
|---|---|
| `prove_wrapped` | `Gate.prove_wrapped`, with `Gate.wrapped_answer` behind it |
| `prove_term_against_ship` | `Gate.prove_term_against_ship`, importing `reference.Reference` |
| `prove_term_against_text` | `Gate.prove_term_against_text`, with `Gate.walk_in_text_order` behind it |
| `structural_checks` (C1–C6) | `Gate.structural_checks` calling `check_one` .. `check_six` |
| `zero_regression` (compare / explain_losses / report) | `Gate.zero_regression` calling `Gate.compare`, `Gate.explain_losses`, `Gate.report` |
| class `Verdict` (outcome, reason, counterexample, route, solver_timeout_ms) | class `Verdict`, those five attributes and nothing else |

## 2.2 The three decisions the tree left to the coder, each answered
## from the tree

- **Which outcome a proved TERM carries.** The verdict CORE names five
  outcomes and no more. `PROVED_ON_SHIP` is "the solver showed
  equality against the unit's own ship code", and both term routes
  compare against the unit's own ship body — route one as the
  reference walks it, route two as the ledger's meanings walk it in
  text order. So a proved term is `PROVED_ON_SHIP` with `route` saying
  which obligation produced it. No sixth outcome was invented, and the
  superseded `PROVED_EQUAL` spelling is not carried forward.
- **Which meanings route two uses.** The gate CORE says route two is
  "the body walked in text order with the same opcode_table" and that
  its evidence is "about the LEDGER'S WIRING, not the meanings". Those
  two sentences settle it: route two carries the same meanings the
  LEDGER's transcription used, so the only difference between the two
  sides is what ordered the computation. Had it used `reference.py`'s
  table it would have been route one again and the two routes would
  have shared a code path — which is the one thing the CORE's
  two-routes rule exists to prevent.
- **What a failed structural check returns.** The CORE says "any fail
  -> the failing check named" and "a unit that fails any check is not
  counted". `UNDECIDED` with the failing check named is what is
  returned; `REFUSED` is reserved for its own meaning, a unit that
  could not be put into canonical form at all.

## 2.3 A solver timeout

LITERAL — `gate.py`, `Gate.decide`'s last branch:

```
        return Verdict(
            UNDECIDED,
            "the solver did not answer inside its %d ms limit, so the "
            "verdict is undecided and never disproved"
            % self.solver_timeout_ms,
            route, None, self.solver_timeout_ms)
```

Every verdict this task wrote carries `solver_timeout_ms: 3000`.

---

# 3. THE FINDING: the flag triple carried the wrong two values

This is the first pass's result, kept rather than smoothed, because it
is what the two-routes rule is for.

## 3.1 What the first pass said

LITERAL — the first run's own consistency line, before the fix:

```
CONSISTENCY -- units proved on one route and disproved on the other: 1338
  c/op_282, c/op_289, c/op_290, c/op_295, c/op_296, c/regen_15772, ...
```

Route two proved these; route one disproved them. Under the CORE that
is a defect to be found.

## 3.2 The values moving, on `c/op_282`

`c/op_282` is a unit whose body is four lines. Take `a` and `b` both
equal to `3115399309` — which is what the solver itself chose.

LITERAL — the unit's own ship body and its answer home:

```
  body:        xor %eax,%eax; or %esi,%edi; setne %al; ret
  answer home: rax at 8 bits
```

- `xor %eax,%eax` clears the answer register to 0.
- `or %esi,%edi` combines the two arriving values into `%edi`. With
  both equal to `3115399309`, the combination is `3115399309`, which
  is not zero, so the machine's zero flag is CLEAR.
- `setne %al` asks "was the result not zero?" — yes — and writes 1.
- The unit answers **1**.

LITERAL — the two sides, as they were:

```
  the ledger's term    If(0 != seed_rdi | seed_rsi, 1, 0)
  the reference's      If(seed_rdi != seed_rsi,     1, 0)
```

GLOSS. Put the solver's own values in. The ledger's term asks whether
the COMBINATION is non-zero: `3115399309 != 0`, so 1 — which is what
the machine leaves. The reference's asked whether the two INPUTS
differ: `3115399309 != 3115399309`, so 0. At those two equal values
the two sides differ, and that is the counterexample the solver
returned:

```
  counterexample [seed_rsi = 3115399309, seed_rdi = 3115399309]
```

## 3.3 The mechanism, in the reference's own source

LITERAL — `reference.py`, `build_binary`'s last line, before the fix:

```
    ops.write(1, result)
    ops.state.flags = (mnemonic, left, right)
```

Every binary opcode recorded its two OPERANDS as the flag triple's two
sides. For a comparison-shaped setter that is right — a subtraction's
condition IS a comparison of its two operands. For the logic family it
is not: those opcodes leave the zero and sign bits from their RESULT
and clear the carry and the overflow. `reference.py` already had the
correct shape one function away, for `test`:

```
        ops.state.flags = ("test", left & right,
                           z3.BitVecVal(0, width))
```

## 3.4 The fix, and the correction written into the tree

The fix is that shape applied to the logic family: the triple becomes
`(mnemonic, result, 0)`. `carry_bit` and `overflow_bit` already answer
`False` for this family by the setter's NAME, so nothing else moved.

**Which setters this could touch, computed over the whole corpus
rather than assumed.** Every flag reader in all 30,436 units was
matched to its nearest preceding flag setter:

```
every setter that a flag reader reads from, whole corpus:
     8044  test
     6569  cmp
     3778  ucomiss
     1607  fucomip
     1484  ucomisd
     1447  or
      776  sbb
      165  fucomi
       15  add
       13  sub
       12  shr
       10  mul
        7  imul
        7  neg
        3  xor
        3  sar
        2  adc
```

GLOSS. `or` and `xor` are 1,450 of these and are what the fix
addresses. `add`, `imul` and the shifts are 37 readings in all, and
the corrected run's consistency line is 0, so on this corpus no
reading of theirs disagrees with the ledger — recorded as measured,
not as proved safe in general.

**The tree.** The `machine_state` CORE said "the flag model is a
triple (setter, L, R)" and was SILENT on which two values L and R are.
A settled rule was added there with its provenance, saying that L and
R are the two values the CONDITION reads, and that a setter whose zero
and sign bits come from its result leaves `(result, 0)`.

**Recorded rather than smoothed: the order was wrong.** Round 12's
binding rule 2 says the CORE is corrected FIRST and the code follows.
Here the defect was found by a running gate, the one-line fix was made
and verified, and the CORE rule was written afterwards. The rule now
stands with its provenance and the PROGRESS entry says the same thing
this paragraph does.

## 3.5 What the fix moved

LITERAL — the corrected run against the first pass:

```
  consistency line     1338 -> 0
  proved              23357 -> 25179
  withdrawn            1362 -> 0
  lost proofs          1782 -> 0
```

GLOSS. The first pass's 1,362 withdrawals and 1,782 lost proofs were
the defect, not the corpus. One line of `reference.py` and one width
rule in `gate.py` (§7.2) account for all of them.

---

# 4. The acceptance instances, printed with values

All of `acceptance58_printed.txt`, produced by `acceptance58.py`.

## 4.1 (a) `c/op_246` — the remainder proves under `SRem`

LITERAL:

```
LITERAL -- the unit's own ship body, and its answer home:
  body:        mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret
  answer home: rax at 32 bits

LITERAL -- does the ledger's term use SRem?  yes

LITERAL -- the two routes:
  route one (the term against the unit's own ship body): PROVED_ON_SHIP
      z3 proved the ledger-transcribed OUT-0 term equal to the value the
      unit's own ship body leaves in its own answer home, for every value
      of every register either side reads before writing

LITERAL -- the two remainders at 32 bits, inputs 7 and -3:
  z3.SRem(7, -3)  = 1
  7 % -3 in z3py  = 4294967294   (as a signed value: -2)

LITERAL -- both sides run with the two arrival registers bound to 7 and -3:
  the reference's answer = 1
  the ledger's term      = 1
```

GLOSS, with the values moving. `a = 7` arrives in the first arrival
register and `b = -3` in the second. `mov %edi,%eax` copies 7 into the
accumulator. `cltd` spreads the accumulator's top bit — 7 is positive,
so the data register becomes 0. `idiv %esi` divides the pair
`(0, 7)` by `-3`: the quotient is `-2` and the remainder is what is
left over, `1`, because x86 gives the remainder the sign of the
DIVIDEND. `mov %edx,%eax` moves the remainder into the answer home.
The ledger's term always said `SRem` and always gave 1; the superseded
reference used z3py's `%`, which is `bvsmod` and gives `-2`, and the
solver duly found the disagreement. That is the whole of log 153 §5's
415-unit withdrawal, and all 415 prove here.

## 4.2 (b) `cpp/regen_36796` — a formerly-undecided x87 unit decides

This unit was **UNDECIDED on both routes** in log 153 §4.3, for want
of any x87 model in either reference.

LITERAL:

```
LITERAL -- the unit's own ship body:
  fldt 0x18(%rsp)
  fldt 0x8(%rsp)
  fucomip %st(1),%st
  fstp %st(0)
  seta %al
  ret

LITERAL -- log 153 section 4.3's verdict on this unit:
  route one (the ship simulation): UNDECIDED
  route two (the text-order walk): UNDECIDED

LITERAL -- the ledger's own OUT-0 term:
  Extract(7, 0, ZeroExt(56, If(And(Not(x87_0x8_rsp_ < x87_0x18_rsp_), Not(fpEQ(x87_0x8_rsp_, x87_0x18_rsp_)), Not(Or(fpIsNaN(x87_0x8_rsp_), fpIsNaN(x87_0x18_rsp_)))), 1, 0)))

LITERAL -- the x87 stack after the unit's own two loads:
  position 0 (the top)  x87_0x8_rsp_
  position 1            x87_0x18_rsp_
  depth                 2

LITERAL -- the reference's own answer term:
  Extract(7, 0, ZeroExt(56, If(And(Not(x87_0x8_rsp_ < x87_0x18_rsp_), Not(fpEQ(x87_0x8_rsp_, x87_0x18_rsp_)), Not(Or(fpIsNaN(x87_0x8_rsp_), fpIsNaN(x87_0x18_rsp_)))), 1, 0)))

LITERAL -- the two routes now:
  route one (the term against the unit's own ship body): PROVED_ON_SHIP
  route two (the term against the body walked in text order): UNDECIDED
      the text-order walk: no z3 term is written for this arch opcode

LITERAL -- the values moving.  Take the memory the two loads read as
0x18(%rsp) = 2.0 and 0x8(%rsp) = 3.0:
  the ledger's term with those two values, asked to be anything but 1: unsat
```

GLOSS, with the values moving. `fldt` loads an 80-bit extended float
onto the x87 register stack. The first loads 2.0, so position 0 holds
2.0. The second loads 3.0 and PUSHES, so position 0 now holds 3.0 and
position 1 holds 2.0. `fucomip %st(1),%st` is AT&T order — source
`%st(1)`, destination `%st` — so it compares the top against position
1, 3.0 against 2.0, and pops. `seta` asks for above-and-ordered: 3.0
is above 2.0 and neither is NaN, so the answer is 1. The last line is
z3 saying the ledger's term cannot be anything but 1 at those two
values. The two printed terms are character-identical, which is why
route one proves: the ledger's transcription and the reference's walk,
sharing no code path, name one term.

Route two is UNDECIDED here and that is honest: route two carries the
LEDGER's meanings table driven by text order, and that table has no
entry for the x87 load as a text-order step. Route two proves 21,084
of the regenerated population without it, and it never contradicts
route one.

## 4.3 (c) The other two obligations, on `c/op_246`

LITERAL:

```
LITERAL -- prove_wrapped: PROVED_ON_SHIP
  route:            the wrapped text against the unit's own ship body
  reason:           z3 proved the wrapped text's OUT-0 equal to the value
                    the unit's own ship body leaves in its own answer home,
                    for every value of every input row, with each input row
                    bound to the same symbol as the argument the reference
                    reads in its arrival register
  counterexample:   None
  solver timeout:   3000 ms
```

GLOSS. `prove_wrapped` carries no simulator of its own, which is the
CORE's settled rule as of today. It binds each input row by writing
the arrival family's own symbol into the cell the prelude's SECOND
step reads — the wrapped text reaches a row in two steps, the ledger
base then the row — then walks the whole wrapped text with the one
reference and reads back the cell the epilogue stored into. So the
ledger plumbing is simulated, not assumed away.

## 4.4 The six structural checks

LITERAL:

```
LITERAL -- structural_checks: all six passed = True
  C1: the body appears in the wrapped text character-for-character and in its own order -- no register was renamed, no immediate was moved, no stack address was rewritten
  C2: the prelude writes only the registers the arrival contract names, one two-step load per input row
  C3: every one of the 1 returns is immediately preceded by the epilogue, which stores the compiler's own result register into OUT-0
  C4: no body line names the ledger symbol or any ledger row, so the body and the plumbing touch disjoint text
  C5: the epilogue's pointer register %r11 is not the result register %rax, so loading the block base cannot destroy the answer
  C6: the only text this form changed inside the body is the TARGET operand of 0 transfer(s); every mnemonic, every other operand and every trailing annotation is the body's own, the rewrite is a function of the target, and every positional label the body branches to is defined exactly once in it
```

GLOSS. The route is reached only from `Gate.structural_fallback`,
which is called only where the reference has no model for something
the body spells — never as a cheaper first choice, which is the CORE's
settled rule.

---

# 5. Zero regressions, in the ruled sense

`Gate.zero_regression` was run over the whole population, task 53's
states against task 58's, joined on the unit name.

LITERAL — `audit58_printed.txt`:

```
ZERO REGRESSION -- Gate.zero_regression over all three populations
  units still proved (kept)                    23132
  proofs lost                                  0
  proofs gained                                2047
  moved without ever holding a proof           0
  units missing from the new run               0
  LOST PROOFS WITH NO COMPUTED CAUSE           0
```

GLOSS. Every one of the 23,132 units proved in task 53 is proved
here. There is nothing under "by cause" because there is nothing to
explain: the cause list is empty only when the loss list is. The
method still computes a cause per loss from the unit's own record, and
a loss with no computed cause would be reported as an unexplained
regression rather than smoothed — `audit58.py` asks for exactly that
count and it is 0.

---

# 6. The guard, unmodified, one process

`check_no_spelling_keys.py` was not edited. `git status --porcelain`
over it is empty and its sha256 is
`a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7` —
the same hash log 153 §7 recorded. No file this task writes declares
`role: generator provenance`, and nothing was added to any field set.

LITERAL — the command and its result:

```
$ /tmp/reconnect_venv/bin/python3 guard58.py
TASK 58: 334 paths  PASS 334  FAIL 0  exempt 0  exit 0
guard exit=0
```

LITERAL — the transcript's own head and tail
(`guard58_transcript.txt`):

```
guard58.py -- every artifact task 58 writes, unmodified guard, ONE process.  Nothing was added to any field set, and no artifact was declared out of the walk.
$ python3 check_no_spelling_keys.py <334 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
PASS acceptance58.json -- no operator token in any key, grouping, pairing or row structure
...
GUARD EXIT CODE = 0
```

LITERAL — the counts over that transcript, computed rather than
eyeballed:

```
$ grep -c "^PASS " guard58_transcript.txt
334
$ grep -c "^FAIL" guard58_transcript.txt
0
$ grep -c exempt guard58_transcript.txt
0
```

LITERAL — the superseded records this task READS, checked to be
unmodified:

```
$ git status --porcelain -- Research/op_pipeline/check_no_spelling_keys.py \
    Research/op_pipeline/gate48.py Research/op_pipeline/textwalk48.py \
    Research/op_pipeline/layer4c.py Research/op_pipeline/layer4.py \
    Research/op_pipeline/canon37_gate.py Research/op_pipeline/canon38_gate.py \
    Research/op_pipeline/ledger47.py Research/op_pipeline/ledger48.py
(no output -- every one matches its committed copy)
```

GLOSS. 334 paths walked: `acceptance58.json`, `audit58.json`, and all
332 verdict files in `gate58_store/`. Every line says PASS; no line
says exempt; nothing was declared out of the walk.

---

# 7. The two edits outside this task's own new files

## 7.1 `reference.py`, one line

The logic family's flag triple, §3. It is task 57's file and this is
its only change; the correction is recorded in the `machine_state`
CORE with provenance and in two PROGRESS files.

## 7.2 Nothing else was edited

`gate48.py`, `textwalk48.py`, `canon*`, `layer4*`, `ledger4*`,
`vex_names.py`, `condition_table.py` and `check_no_spelling_keys.py`
are untouched, and §6 shows the vcs saying so.

A width rule inside `gate.py` is worth naming because it cost 396
proofs on the first pass before it was corrected: two BIT VECTORS are
comparable whatever their widths — `Gate.decide` cuts both to the
narrower, which is what both superseded routes did and what the answer
home's own width means. Refusing on width made `c/op_105` and 395
others UNDECIDED for no reason. A float sort against a bit vector is
still not comparable, and saying so is still the honest verdict.

---

# 8. The complete file inventory

## 8.1 Code written this task (five files, all new)

| file | lines | what it is |
|---|---|---|
| `gate.py` | 898 | THE deliverable: `Gate` with `prove_wrapped`, `prove_term_against_ship`, `prove_term_against_text`, `structural_checks` (`check_one`..`check_six`), `zero_regression` (`compare`/`explain_losses`/`report`); class `Verdict` |
| `gate58_run.py` | 156 | the driver: every canon38 source document, both routes, sharded and resumable |
| `audit58.py` | 398 | the figures: per population, the transition table, every movement's computed cause, the consistency line, `Gate.zero_regression` |
| `acceptance58.py` | 244 | the three acceptance instances, printed with values |
| `guard58.py` | 132 | runs the UNMODIFIED guard, one process, over every task-58 artifact |

## 8.2 Data written this task

| file | bytes | what it is |
|---|---|---|
| `gate58_store/*.json` | 27 MB over 332 files | THE VERDICTS: 30,436 unit records, each with both routes' `Verdict` |
| `audit58.json` | 4,360 | every figure in §1, §3.5, §5 |
| `acceptance58.json` | 3,235 | the three instances as data |
| `guard58.json` | 303 | the guard run's counts |

## 8.3 Transcripts written this task

| file | bytes | what it is |
|---|---|---|
| `audit58_printed.txt` | 5,869 | every figure in §1 and §5 |
| `acceptance58_printed.txt` | 5,751 | the three instances |
| `guard58_transcript.txt` | 34,690 | 334 PASS, 0 FAIL, 0 exempt, exit 0 |
| `gate58_run_shard{0..5}.log` | — | the six shard logs, each ending `shard N/6 finished` |
| `gate58_resume.md` | — | the resume file, §9 |

## 8.4 Edited (one line)

`reference.py` — §3.4, §7.1.

## 8.5 Planning files touched

| file | what changed |
|---|---|
| `node_0_3_5_5_gate/PROGRESS.md` | three entries — the module, the re-gate with its four figures, `prove_wrapped` |
| `node_0_3_5_5_gate/node_0_3_5_5_0_verdict/PROGRESS.md` | three entries — the class, the outcome decision, the consistency line |
| `node_0_3_5_5_gate/node_0_3_5_5_4_structural_checks/PROGRESS.md` | two entries — the six named methods, and the fallback-only rule |
| `node_0_3_5_5_gate/node_0_3_5_5_5_zero_regression/PROGRESS.md` | two entries — the three methods, and the run's counts |
| `node_0_3_5_4_reference/node_0_3_5_4_1_machine_state/CORE_0_3_5_4_1_machine_state.md` | the new settled rule on what L and R are, with provenance |
| `node_0_3_5_4_reference/node_0_3_5_4_1_machine_state/PROGRESS.md` | the correction record, including that the code fix preceded the rule |
| `node_0_3_5_4_reference/PROGRESS.md` | the one-line edit to `reference.py` |

Paths are under
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/`.

## 8.6 Read, never written

`canon38_wrapped_{c,cpp,go,rust,swift}.json`, `canon38_interp.json`,
`canon38_regen_store/*.json`, `layer4c_terms_*.json`,
`layer4c_interp.json`, `layer4c_regen_store/*.json`, `layer4c.py`,
`layer4.py`, `ledger47.py`, `ledger48.py`, `canon.py`, `region36.py`,
`condition_table.py`, `check_no_spelling_keys.py`, `gate48.py`,
`textwalk48.py`, `canon37_gate.py`, `canon38_gate.py`.

---

# 9. Resume state

## 9.1 Nothing is part-done

`gate58_store/` holds 332 files, one per canon38 source document, and
every one of the 30,436 units has a record. Each of the six shard logs
ends `shard N/6 finished`. The whole re-gate takes about 21 seconds
with six shards on this machine, so no checkpoint was ever needed
beyond the per-file one that is there.

## 9.2 How to re-run, in order

All under `/tmp/reconnect_venv/bin/python3`:

1. `gate58_run.py --shard=0/6` .. `--shard=5/6` — skips any source
   whose output file already exists; delete `gate58_store/` for a full
   redo.
2. `audit58.py > audit58_printed.txt`
3. `acceptance58.py > acceptance58_printed.txt`
4. `guard58.py` — LAST, because it walks everything above.

## 9.3 What the next task reads

`gate58_store/*.json`. Each unit record carries `unit`, `lang`,
`population`, `term_built`, `transcription_refused`, and the two
verdicts `ship` and `text`, each a `Verdict` as a mapping. **The
proved population for the pool's three merge grounds is 25,179**: the
units whose record has `term_built` true, no `DISPROVED` outcome and
at least one `PROVED_ON_SHIP`.

---

# 10. The two lists

## 10.1 Decided, recorded for audit

1. **A proved TERM carries `PROVED_ON_SHIP`** with `route` naming the
   obligation. The verdict CORE names five outcomes; no sixth was
   invented (§2.2).
2. **Route two carries the LEDGER's meanings, not the reference's.**
   Two sentences of the gate CORE settle it, and the alternative would
   have made the two routes share a code path (§2.2).
3. **A failed structural check returns UNDECIDED with the check
   named**; `REFUSED` keeps its own meaning (§2.2).
4. **The flag triple's two sides are the values the condition reads.**
   Written into the `machine_state` CORE with provenance, after the
   defect was found by a running gate — the order is recorded as a
   deviation from binding rule 2 rather than smoothed (§3.4).
5. **Two bit vectors are comparable whatever their widths**; a float
   sort against a bit vector is not (§7.2).
6. **`call` into the compiler's own runtime is REFUSED as "runtime
   callee not yet attached (task 59, node 0_3_5_1_8)"**, never "out of
   scope". 3,419 of the 3,970 remaining undecided units are that one
   thing, and task 59 is the work that decides them (§1.7).

## 10.2 Awaiting the owner

*Nothing.*
