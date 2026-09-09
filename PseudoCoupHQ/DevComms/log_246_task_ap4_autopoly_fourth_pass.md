# log 246 — task ap4: closing the four languages — the contract for a value that is not in a register, and AutoPoly's loop, fourth pass

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/`).
Line: arch_unit_oracle, the "goal" section of 2026-09-07 and the rulings
of 2026-09-08 and 2026-09-09 in
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`.
Law: `PseudoCoupHQ/Research/LAW.md`, read in full including
its tower section.
Date: 2026-09-09. Instance `ap4`, on the tower guest.

Artifact folder:
`PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`,
writing `autopoly4_*`; tasks ap1's, ap2's and ap3's products are not
overwritten. Lane scripts: `.../autopoly/lanes_ap4/`, fifteen of them,
each kept in the repo as the standing rule of 2026-09-07 requires. Every
lane log named below is on the TOWER (`<user>@<tower>`) under
`<runs>/ap4/agent/logs/`.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PseudoCoupHQ`, mounted into
the instance. Every rendering is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself, quoted;
**GLOSS** is a plain-words reading beside a literal.

---

# 1. What this is, one sentence per object in relation

* A **CELL** is one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table, holding, per place the opcode writes, the z3
  term the reference simulator's own builder puts there.
* The **OUTER SET** is the 253 cells the canon40 corpus attests, over
  133,044 attested ledger rows — task ap3's file copied here and its
  counts re-measured, identical.
* A **RUN** is `find_emulation(cell, lang)` on one of the four compiled
  targets: the target's own operator where its whole lowered body IS the
  cell, the cell's term written in the target's operators where it is
  not, compiled at the corpus's ship flags, carved, and put back to z3
  against the cell's own term.
* An **ARRIVAL CONTRACT** is the list of IN rows one side names. The
  gate aligns two of them position by position; where they name
  different numbers of rows it used to decline.
* **THIS TASK** is that loop run a fourth time, after the ONE question
  tasks ap1 to ap3 left — a value the machine holds somewhere other than
  a fresh register — was answered as the owner's ruling of 2026-09-09 states
  it: "the contract may state a place by a CONSTRAINT, not only by a
  register name. One extension, in the layer that owns each half."

**THE ANSWER: 162 cells proved on all four targets, 106,032 attested
ledger rows, 79.7%** — up from task ap3's 151 / 85,530 / 64.29%, task
ap2's 144 / 85,368 / 64.17% and task ap1's 120 / 76,634 / 57.6%. Cells
proved on NO target fell from 56 to 20, and their ledger rows from
15,134 to 12,449. Runs carrying a cause: 237 of 1,012, down from 293.
**Runs task ap3 proved and this loop does not: 0.** The
arrival-contract group, 38 places open since task g1b, is **0**.

Two things are said before the numbers so the numbers are not misread:

* **The 38 declined places were TWO populations, not one**, and the
  probes are what said so. Seven are what the brief describes — a cell
  whose arrivals really are a function of the emulation's — and the
  other **31 are a HALF of the flags place on the primitive route**,
  which the driver's own rule already refuses when the place is not
  halved. §5.
* **Change 2 lands and proves.** The 30 x87 c rows render, compile,
  carve to the x87 opcode, wrap on the canonical form and are proved;
  rust, go and swift stay refused by nature. But the ledger's new
  epilogue was only half of it: the reference cannot READ an answer left
  on the x87 stack and the shared aligner cannot align an FP arrival, so
  the other half is in the driver. §6.

---

# 2. The lanes

| lane | what it did | log, on the tower |
|---|---|---|
| `ap4_l1_probe_the_three_populations.sh` | the cells file re-measured; the 38 declined places by cell; the empty bodies; it stopped on its own format string in its last section | `...211159Z` |
| `ap4_l2_probe_the_two_sides_and_the_x87_form.sh` | the two sides of every declined place, and the x87 form the canonical form refuses | `...211451Z` |
| `ap4_l3_probe_the_seven_the_flags_halves_and_the_empty_bodies.sh` | **THE PROBE THAT SPLIT THE POPULATION**: 7 not a flags place, 31 a half of one; every `flags.*` place by route and verdict; every `ret`-only body | `...212014Z` |
| `ap4_l4_probe_the_cell_line_and_the_full_body_walk.sh` | the cell's own line off the table's row, and the reference walked over the WHOLE attested body rather than the narrow-stripped one | `...212318Z` |
| `ap4_l5_probe_change2_end_to_end.sh` | change 2's ledger half asked end to end, and the unchanged branches text for text | `...212944Z` |
| `ap4_l6_probe_the_x87_answer_and_its_arrivals.sh` | the answer term the driver now reads off the x87 stack, and every free symbol of it with its sort | `...213305Z` |
| `ap4_l9_measure_the_three_changes.sh` | the measurement, first pass; **it caught two defects of its own** (`measure` read this task's own store as the BEFORE, and the lane's echo line held backticks) | `...214155Z` |
| `ap4_l7_guard_check_and_the_handful.sh` | **GUARDS 1 AND 3**: `check_L2` re-derived and every file restored; the h2 handful | `...214159Z` |
| `ap4_l8_guard_o8.sh` | **GUARD 2**: task o8's 243 rows re-run | `...214450Z` |
| `ap4_l10_measure_the_three_changes_b.sh` | **THE MEASUREMENT OF RECORD**, and the PIN that fixed change 2's argument order | `...214504Z` |
| `ap4_l11_preflight_and_the_sample.sh` | the outer set, and the twenty-run memory sample | `...214706Z` |
| `ap4_l12_run_the_loop.sh` | **THE LOOP**: 1,012 runs in 1,431 s | `...214747Z` |
| `ap4_l13_aggregate_and_report.sh` | the aggregate, the report, the store check, the spelling guard, the tally | `...221230Z` |
| `ap4_l14_the_tables.sh` | **THE TABLES OF RECORD**: per target, routes, all-four, causes, change, region, identity, `sat`, re-pose | `...221258Z` |
| `ap4_l15_two_readings.sh` | two counts the tables do not make on their own | `...221444Z` |

---

# 3. What was changed, and in which layer

| file | the change | the layer it belongs to |
|---|---|---|
| `Research/op_pipeline/ledger.py` | CHANGE 2, the shared half the brief authorises: `is_x87_family`, an x87 branch in `build_epilogue` (`fstpt OUT-0`) and one in `build_prelude` (`fldt IN-k`, emitted last and in reverse so the first x87 arrival ends at st(0)) | the canonical form's own ledger |
| `.../emulation/emulate.py` | CHANGE 2's driver half: `X87_ANSWER_FAMILY`, the answer home in `recorded_facts` when the ledger's own reading of the body says a value is left on the x87 stack, and `x87_answer_for_unit` | the driver |
| `.../emulation/handful/handful.py` | CHANGE 1 (`derived_arrivals`, `the_region`, `the_sign_spread`, `attested_of`), CHANGE 2's alignment (`x87_arrivals`, `x87_aligned`), CHANGE 3 (`the_body_is_empty`, `the_identity`, `landing_of`'s `IDENTITY`, `composition_of_run`), and `is_the_flags_place` | the driver |

`canonical_form.py` was NOT changed: its refusal text `no answer home`
is still exactly right for a unit that leaves its answer nowhere, and an
x87 unit no longer reaches it. Nothing else under `Research/op_pipeline`
moved; §7 is the proof.

---

# 4. THE PROBES, which came before every line of every change

## 4.1 The 38 declined places are two populations

**LITERAL**, lane `ap4_l3_probe_the_seven_the_flags_halves_and_the_empty_bodies.sh`,
on the tower at
`<runs>/ap4/agent/logs/20260909T212014Z__ap4_l3_probe_the_seven_the_flags_halves_and_the_empty_bodies.sh.log`:

```
[1/3] THE PLACES THAT ARE NOT A HALF OF A FLAGS PLACE
   declined places: 38
   of those, a half of a flags place: 31
   of those, not a flags place at all: 7
```

**GLOSS.** Every one of the 38 is on the PRIMITIVE route, where the two
arrival contracts are different things: the cell's arrivals are the
registers its own opcode reads, and the emulation's are the registers
the corpus probe's own parameters arrive in. Thirty-one of them are
`flags.low` or `flags.high` — a half of the flags place, which task ap2's
fix 3 created and whose name slipped past the driver's own test
`place["writes"] == "flags"`.

## 4.2 The relation, read off the reference rather than named

**LITERAL**, lane `ap4_l4_probe_the_cell_line_and_the_full_body_walk.sh`,
on the tower at
`<runs>/ap4/agent/logs/20260909T212318Z__ap4_l4_probe_the_cell_line_and_the_full_body_walk.sh.log`:

```
== `idiv` gpr_one 64   row r07432
   row[text      ] = 'idiv %rdi'
   row[operands  ] = ['%rdi']

== `idiv` gpr_one 64   the matched body, LITERAL: mov %rdi,%rax; cqto; idiv %rsi; mov %rdx,%rax; ret
   [0] mov %rdi,%rax                  (mov, gpr_gpr, 64)
   [1] cqto                           (cqto, none, 64)
   [2] idiv %rsi                      (idiv, gpr_one, 64)   <== the cell
   [3] mov %rdx,%rax                  (mov, gpr_gpr, 64)
   [4] ret                            (ret, None, None)
   the registers the reference leaves at the cell's own instruction:
      %rax   = seed_rdi
      %rdi   = seed_rdi
      %rdx   = seed_rdi >> 63
   the body instruction's operands: ['%rsi']
```

**GLOSS, and this is the whole of change 1.** The cell's line is `idiv
%rdi` and the body's is `idiv %rsi`, so the cell's operand register at
position 0 is the body's `%rsi`. The two implicit registers the cell also
reads are matched by their own names, and the reference's own walk of the
attested body says what each holds when the opcode runs: `%rax` is the
emulation's first argument, and `%rdx` is that argument's sign spread,
which is what `cqto` leaves. Nothing here names a relation — it reads
one, and §5.2 shows z3 being asked to confirm it before it is printed.

**The same lane over the narrow-STRIPPED body left `%rax = seed_rax`**,
because task o2's narrow rule counts `mov %rdi,%rax` as chaff and strips
away the very instruction that carries the argument in. Lane `ap4_l3`
walked the stripped body and lane `ap4_l4` walked the whole one; the
change walks the whole one, and the first form is recorded as having
been wrong rather than quietly replaced.

## 4.3 The x87 answer, and its arrivals

**LITERAL**, lane `ap4_l6_probe_the_x87_answer_and_its_arrivals.sh`, on
the tower at
`<runs>/ap4/agent/logs/20260909T213305Z__ap4_l6_probe_the_x87_answer_and_its_arrivals.sh.log`:

```
== [3] `fmulp` st_st 80 -> c, place `x87_7`
   the cell's arrivals: ['X87_1', 'X87_0']
   the cell's term, LITERAL: fp.to_ieee_bv(v0 * v1)
   the parameter plan: [('a', 'long double', 'X87_1', 'fp', 79), ('b', 'long double', 'X87_0', 'fp', 79)]
   the carved body, LITERAL: fldt 0x18(%rsp); fldt 0x8(%rsp); fmulp %st,%st(1); ret
   canonical_form outcome: 'WRAPPED_TEXT_PROVED'
   the wrapped text resolved, LITERAL: fldt 0x18(%rsp); fldt 0x8(%rsp); fmulp %st,%st(1); fstpt OUT-0; ret
   the body's answer, LITERAL: fp.to_ieee_bv(x87_0x18_rsp_ * x87_0x8_rsp_)
   its sort: BitVec(79)  its size: 79
   its free symbols:
      x87_0x18_rsp_                sort FPSort(15, 64)
      x87_0x8_rsp_                 sort FPSort(15, 64)
```

**GLOSS.** With the ledger's new epilogue in, the unit wraps
(`WRAPPED_TEXT_PROVED` where task ap3 had `REFUSED / no answer home`),
and the driver's own reading gives an answer of the same shape and the
same width as the cell's term — `fp.to_ieee_bv` of an x87 value, 79
bits. What is left is that the body's two arrivals are named after the
STACK SLOTS it loads them from, and the cell's after the stack positions
the model table preseeds. Matching them is §6.3.

---

# 5. CHANGE 1 — the derived arrival, and the flags half

## 5.1 The two halves of one population

**THE SEVEN**, which are the brief's own: `idiv` gpr_one 32 and 64 on c
(two places each — the quotient and the remainder), `xor` gpr_same 32 on
c, and `mov` imm_gpr 8 and 32 on c. Their cells read 3, 1 and 0 arrivals
where their emulations read 2, 2 and 1.

**THE THIRTY-ONE** are `flags.low` / `flags.high` of `add`, `sub`,
`imul`, `and`, `or`, `xor` gpr_gpr 64 and `neg` gpr_one 64, on the
targets whose corpus has a primitive for them. The driver already
refuses a flags place on the primitive route by name, and that refusal
is true about the objects here too: an operator answers with the value it
hands back, and a flags place is a second place the opcode writes. The
test was `place["writes"] == "flags"`; it is now
`is_the_flags_place(place["writes"])`, which reads the name before the
dot. **LITERAL**, `handful.py`:

```python
def is_the_flags_place(writes):
    if not writes:
        return False
    return writes.split(".")[0] == "flags"
```

**WHAT THAT MOVES, measured rather than asserted.** Lane `ap4_l3` counted
every `flags.*` place of task ap3's store by route and verdict: 31
UNDECIDED on the primitive route (these), and 12 PROVED_ON_SHIP on it
(`and`, `or`, `xor` gpr_gpr 64's `flags.high`, on all four targets),
whose term happens to equal the operator's own answer. Those 12 places
are now refused with the rest. **No run changes verdict**, because a
run's verdict is its DESTINATION place — `handful.destination_place`, the
first place that is not the flags — and none of these is one. The change
table's `runs task ap3 proved and task ap4 does not: 0` is that stated
over the whole loop.

## 5.2 The substitution and the region

The cell's arrivals are substituted by what the reference's walk of the
attested body leaves in them, both sides are then aligned on the
EMULATION's rows, and the REGION that substitution names is asked of z3
before it is printed. **LITERAL**, `handful.the_region`'s own rule:

```python
            if other < index:
                if proved_equal(became[index], became[other]):
                    said.append("IN-%d = IN-%d" % (index, other))
                    break
            spread = the_sign_spread(became[other], key_width)
            if spread is None:
                continue
            if proved_equal(became[index], spread):
                said.append("IN-%d = SignExt(IN-%d)" % (index, other))
                break
```

**THE REGION LIST, and it is the brief's own deliverable. LITERAL**, lane
`ap4_l14_the_tables.sh`, on the tower at
`<runs>/ap4/agent/logs/20260909T221258Z__ap4_l14_the_tables.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly4.py region | sed -n '1,16p'
places task ap4's change 1 substituted: 7
distinct runs: 5

| cell | lang | place | the region | the gate's verdict |
|---|---|---|---|---|
| `xor` gpr_same 32 | c | `reg_rdi` | no constraint: every one of the cell's IN rows is free over the emulation's own arrivals | PROVED_ON_SHIP |
| `idiv` gpr_one 64 | c | `reg_rax` | on the region IN-0 = SignExt(IN-1) | DISPROVED |
| `idiv` gpr_one 64 | c | `reg_rdx` | on the region IN-0 = SignExt(IN-1) | PROVED_ON_SHIP |
| `mov` imm_gpr 32 | c | `reg_rdi` | no constraint: every one of the cell's IN rows is free over the emulation's own arrivals | DISPROVED |
| `idiv` gpr_one 32 | c | `reg_rax` | on the region IN-0 = SignExt(IN-1) | DISPROVED |
| `idiv` gpr_one 32 | c | `reg_rdx` | on the region IN-0 = SignExt(IN-1) | PROVED_ON_SHIP |
| `mov` imm_gpr 8 | c | `reg_rdi` | no constraint: every one of the cell's IN rows is free over the emulation's own arrivals | DISPROVED |

the region list, by verdict:
      4  DISPROVED
      3  PROVED_ON_SHIP
```

**GLOSS, place by place, because three of the four `DISPROVED` say
something and one says something else.**

* **`IN-0 = SignExt(IN-1)` is the owner's own sentence**, generated rather
  than transcribed: IN-0 is the cell's `rdx` row and IN-1 its `rax` row,
  and z3 proved that what the attested body leaves in `rdx` is the sign
  spread of what it leaves in `rax`. That is `cqto`, read off the
  reference.
* **The `idiv` REMAINDER place proves and the QUOTIENT place does not**,
  on both widths. The matched corpus row is the `%` probe — its body ends
  `mov %rdx,%rax`, so the operator's answer IS the remainder. Comparing
  it against the cell's quotient place is a true difference and z3 names
  it: for `idiv` gpr_one 64, `[IN_1 = 9223372036854775808, IN_0 =
  9223372036854775808]`, both the most negative 64-bit value, where the
  quotient is 1 and the remainder is 0. This is what `run_primitive`'s
  own docstring says the two places are for: "how a cell that writes two
  places (`idiv`'s quotient and its remainder) shows which of them the
  operator answers."
* **`mov` imm_gpr 8 and 32 disprove with an EMPTY counterexample**, and
  that is a finding about the cell key rather than about the code. The
  cell's own line is `mov $0x3,%dil` / `mov $0x3,%edi` and the corpus
  rows the lookup matches are `mov $0x1,%al` and `mov $0x8,%eax`. Both
  sides are constants, they are different constants, and there are no
  free variables for z3 to name. The cell key (`mnem`, operand shape,
  `key_width`) does not carry the immediate, so an `imm_*` cell is not
  one mapping; §11 carries that as the one thing that is not this task's
  to decide.
* **`xor` gpr_same 32 carries no constraint and proves.** The cell reads
  one arrival and the emulation two; the matched body is `xor %eax,%eax`
  and the reference leaves `seed_rax` in `%rax` there, which is not one
  of the emulation's arrivals. It is left FREE on the cell side, which
  makes the obligation stronger and not weaker, and the run record says
  so in `cell_side_free_state`. **LITERAL**, the same command:
  `` IN-0 (rdi) becomes seed_rax ``.

---

# 6. CHANGE 2 — the x87 stack, as loads and stores at the edges

## 6.1 The ledger, which is the shared half the brief authorises

**LITERAL**, `PseudoCoupHQ/Research/op_pipeline/ledger.py`,
`build_epilogue`:

```python
        if is_x87_family(result_family):
            row = self.add(
                "OUT", X87_ROW_BYTES, X87_ROW_TYPE, producer, operands,
                note="the answer, taken off the x87 register stack; "
                     "`fstpt` writes %d bytes of this %d-byte row and "
                     "the runner reads it when the unit returns"
                     % (X87_STORE_BYTES, X87_ROW_BYTES))
            scratch = pick_scratch(set(canon.NEVER_RENAME))
            pointer = register_text(scratch, 64)
            literal = []
            literal.append("mov %s,%s"
                           % (ledger_entry_text("OUT"), pointer))
            literal.append("fstpt 0x%x(%s)" % (row.offset, pointer))
            resolved = ["fstpt %s" % row.name()]
            return literal, resolved, row, scratch
```

The row is 16 bytes because that is the size THIS ledger already gives an
x87 row in `walk_dataflow` (`"X87", 16, "x87 stack value"`); the store
writes ten, which is the x86-64 extended format, and the row's own note
says so.

**BOTH EDGES, LITERAL**, lane `ap4_l5_probe_change2_end_to_end.sh`, on
the tower at
`<runs>/ap4/agent/logs/20260909T212944Z__ap4_l5_probe_change2_end_to_end.sh.log`:

```
[3/4] THE PRELUDE, handed x87 ARRIVALS
   prelude, LITERAL:          ['mov ledger+0x00(%rip),%r11', 'fldt 0x10(%r11)', 'mov ledger+0x00(%rip),%r11', 'fldt 0x0(%r11)']
   prelude resolved, LITERAL: ['fldt IN-1', 'fldt IN-0']
   epilogue, LITERAL:         ['mov ledger+0x38(%rip),%r11', 'fstpt 0x0(%r11)']
   epilogue resolved:         ['fstpt OUT-0']
   the wrapped text, LITERAL: mov ledger+0x00(%rip),%r11; fldt 0x10(%r11); mov ledger+0x00(%rip),%r11; fldt 0x0(%r11); faddp %st,%st(1); mov ledger+0x38(%rip),%r11; fstpt 0x0(%r11); ret
```

**GLOSS.** `fldt IN-1` before `fldt IN-0`, so that after the prelude the
FIRST x87 arrival is at st(0) — the order
`model_translate.preseeded_state` seeds (`seed_X87_1` pushed, then
`seed_X87_0`) and the order the c calling rule leaves an answer in. The
row order is untouched: IN-i is still arrival i.

**THE UNCHANGED BRANCHES, text for text**, lane `ap4_l5_probe_change2_end_to_end.sh`, on the tower at `<runs>/ap4/agent/logs/20260909T212944Z__ap4_l5_probe_change2_end_to_end.sh.log`:

```
[4/4] THE GUARD: the unchanged branches, text for text
   -- a general answer
      prelude resolved:  ['mov IN-0,%rdi', 'mov IN-1,%rsi']
      epilogue resolved: ['mov %rax,OUT-0']
   -- a vector answer
      prelude resolved:  ['movdqu IN-0,%xmm0', 'movdqu IN-1,%xmm1']
      epilogue resolved: ['movq %xmm0,OUT-0']
   -- a narrow general answer
      prelude resolved:  ['mov IN-0,%rdi']
      epilogue resolved: ['mov %eax,OUT-0']
```

## 6.2 What the ledger alone could not do, said out loud

With the ledger change alone the unit wraps and then STOPS, and the two
places it stops are both outside what the brief authorises to change:

* `reference.answer_of` reads a REGISTER family and cuts bits out of it,
  so an answer on the x87 stack raises. **LITERAL**, lane `ap4_l5`:
  `` answer_for_unit refused: the reference raised Z3Exception: b'invalid extract application' ``,
  and the transcribed term is `none`.
* `pool100_entry_equivalence.align_by_row` substitutes a BITVECTOR
  `seed_<family>` per IN row, and an x87 arrival is an FP value at
  `reference.X87_SORT`.

Neither `reference.py` nor `pool100_entry_equivalence.py` is a file this
brief names, so neither was touched. Both readings are done in the
DRIVER instead, which is the ruling's own "one extension, in the layer
that owns each half": `emulate.x87_answer_for_unit` walks the body with
the reference's own `simulate`, reads the reference's own
`MachineState.x87`, and applies the same `fp.to_ieee_bv` the model
table's builder puts on an x87 place; `handful.x87_aligned` builds the
rows.

## 6.3 The PIN: which argument slot is which

The alignment needs to know which `long double` argument sits at which
stack displacement, and that was MEASURED rather than read out of the
System V document. **LITERAL**, lane
`ap4_l10_measure_the_three_changes_b.sh`, on the tower at
`<runs>/ap4/agent/logs/20260909T214504Z__ap4_l10_measure_the_three_changes_b.sh.log`:

```
[0/4] THE PIN: the stack slot of each long double argument
   a_minus_b  return a - b;    -> fldt 0x18(%rsp); fldt 0x8(%rsp); fsubp %st,%st(1); ret
   b_minus_a  return b - a;    -> fldt 0x8(%rsp); fldt 0x18(%rsp); fsubp %st,%st(1); ret
   a_over_b   return a / b;    -> fldt 0x18(%rsp); fldt 0x8(%rsp); fdivp %st,%st(1); ret
   b_over_a   return b / a;    -> fldt 0x8(%rsp); fldt 0x18(%rsp); fdivp %st,%st(1); ret
```

**GLOSS.** Under
the reference's own model of `fsubp` and `fdivp`, `a - b` and `a / b`
both carve to the loads in the order `0x18` then `0x8`, so the FIRST
`long double` argument is the one at the HIGHER displacement. Both sides
of the comparison are read by that same reference, so the correspondence
is the one the two objects share; `x87_aligned` sorts the slots
descending and says why in its own comment.

## 6.4 What it reached

**LITERAL**, lane `ap4_l15_two_readings.sh`, on the tower at
`<runs>/ap4/agent/logs/20260909T221444Z__ap4_l15_two_readings.sh.log`:

```
[1/2] `answer home or arrival on the x87 stack`, by target
   runs: 114 over 39 distinct cells
      c      3
      go     37
      rust   37
      swift  37
   the cells on c, which are the ones NOT refused by nature:
      `fucomip` st_st 80  place `flags.low`  this term reads an x87 value's bits, and c's `long double` and z3's FPSort(15, 64) do not spell them the same
      `fldz` st_none 80  place `x87_7`  an x87 answer home reached with a bv root of 79 bits
      `fucomi` st_st 80  place `flags.low`  this term reads an x87 value's bits, and c's `long double` and z3's FPSort(15, 64) do not spell them the same
```

**GLOSS.** 111 of the 114 are rust, go and swift, which have no 80-bit
floating holder at all — refused BY NATURE, which is the brief's own
rule. The three on c are task ap3's own refusals and remain true: two x87
compares whose flags place reads an x87 value's BITS (the explicit
integer bit makes `long double` and `FPSort(15, 64)` different
spellings), and `fldz`, whose term's root is a 79-bit bitvector rather
than a float. **Every one of the 30 x87 ARITHMETIC c rows now proves**
(§8's change table: the 55 that moved to PROVED).

---

# 7. THE THREE GUARDS, which is how change 2 is proved harmless

## Guard 1 — `check_L2`: 259 / 172 / 87

**LITERAL**, lane `ap4_l7_guard_check_and_the_handful.sh`, on the tower at
`<runs>/ap4/agent/logs/20260909T214159Z__ap4_l7_guard_check_and_the_handful.sh.log`:

```
[1/2] model_translate.py check -- the tally the brief names
   files check_command can write, copied aside: 178
   the stored tally, off the artifact as it stands
      check_L2.json rows: 259
         DISCREPANCY  19
         REFUSED      87
         STATED       153
rows: 259
  REFUSED                  87
  STATED                   172
definitions after the check: 4006
   the re-derived check, kept as autopoly4_check_L2_rerun.json: rows 259
      REFUSED      87
      STATED       172
   RESTORED IDENTICAL: every file check_command wrote is back to its stored bytes (178 files)
```

**GLOSS.** Exactly the brief's expectation — 259 rows, 87 REFUSED, 172
STATED, and 153 + 19 = 172, the 19 being what the LEAN RUN of record
turned from STATED into DISCREPANCY. `check_command` OVERWRITES
`lean/check_L2.json` and rewrites 177 `.lean` files; all 178 were copied
aside before, copied back after, and compared by sha256.

## Guard 2 — task o8's 243 rows: 243 / 197 / 155 / 216

**LITERAL**, lane `ap4_l8_guard_o8.sh`, on the tower at
`<runs>/ap4/agent/logs/20260909T214450Z__ap4_l8_guard_o8.sh.log`:

```
[3/3] the four totals
rows             243
LANDED           197
byte identical   155
proved           216
```

**GLOSS.** Task o8's own four totals of log 220, unchanged to the row.
Every product went into `handful/o8_regression/`, which is that
program's own scratch; nothing under `per_opcode/` was written.

## Guard 3 — the h2 handful, unchanged

**LITERAL**, lane `ap4_l7`, same log:

```
[2/2] the h2 handful: sources_counts
NOT_RENDERED 4
ONE_SIDE_REFUSED 4
SOURCE_UNCHANGED 24
identical to the file task h1 wrote under src: 24 of 24 rendered
```

---

# 8. THE table: per target, what the loop reached

**LITERAL**, lane `ap4_l14_the_tables.sh`, on the tower at
`<runs>/ap4/agent/logs/20260909T221258Z__ap4_l14_the_tables.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly4.py tables
## 1. THE table: per target, what the loop reached

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.

| step or verdict | c | rust | go | swift |
|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `compiled` | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `LANDED` | 76 cells, 41829 rows, 31.44% | 72 cells, 39199 rows, 29.46% | 30 cells, 22970 rows, 17.26% | 70 cells, 38915 rows, 29.25% |
| `LANDED_ELSEWHERE` | 27 cells, 11867 rows, 8.92% | 23 cells, 11885 rows, 8.93% | 16 cells, 5448 rows, 4.09% | 35 cells, 18714 rows, 14.07% |
| `NOT_COLLAPSED` | 138 cells, 72141 rows, 54.22% | 110 cells, 72068 rows, 54.17% | 146 cells, 77229 rows, 58.05% | 91 cells, 61147 rows, 45.96% |
| `proved` | 204 cells, 98747 rows, 74.22% | 170 cells, 96021 rows, 72.17% | 177 cells, 113587 rows, 85.38% | 163 cells, 89240 rows, 67.08% |
| `proved under caller extension` | 20 cells, 20530 rows, 15.43% | 21 cells, 21502 rows, 16.16% | 0 cells, 0 rows, 0.0% | 17 cells, 19778 rows, 14.87% |
| `sat` | 19 cells, 6794 rows, 5.11% | 15 cells, 5085 rows, 3.82% | 17 cells, 5181 rows, 3.89% | 5 cells, 3723 rows, 2.8% |
| `undecided` | 2 cells, 1008 rows, 0.76% | 3 cells, 1786 rows, 1.34% | 6 cells, 1250 rows, 0.94% | 15 cells, 7277 rows, 5.47% |
| `refused` | 8 cells, 5965 rows, 4.48% | 44 cells, 8650 rows, 6.5% | 53 cells, 13026 rows, 9.79% | 53 cells, 13026 rows, 9.79% |

## 2. Per target, how far the primitive route reached

Table 2 -- `primitive` is a target operator whose whole lowered body IS the cell; `primitive+setup` is that plus zero-operand accumulator setup (task g1c's widened lookup); `term` is the cell's own term written in the target's operators, which is the fallback.

| route | c | rust | go | swift |
|---|---|---|---|---|
| `primitive` | 29 cells, 19706 rows, 14.81% | 22 cells, 12245 rows, 9.2% | 17 cells, 10351 rows, 7.78% | 9 cells, 7774 rows, 5.84% |
| `primitive+setup` | 2 cells, 1726 rows, 1.3% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |
| `term` | 222 cells, 111612 rows, 83.89% | 231 cells, 120799 rows, 90.8% | 236 cells, 122693 rows, 92.22% | 244 cells, 125270 rows, 94.16% |
| `no route reached` | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |

Table 3 -- a cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 4 of 4 | 162 | 106032 | 79.7% |
| 3 of 4 | 23 | 8955 | 6.73% |
| 2 of 4 | 7 | 2804 | 2.11% |
| 1 of 4 | 41 | 2804 | 2.11% |
| 0 of 4 | 20 | 12449 | 9.36% |

`sat` at the plain comparison, every written place: 155
`sat` surviving the caller-extension re-pose: 70
the handful's forty pairs: 32 agree character for character, 35 agree on the verdict, 4 not in this outer set
```

**GLOSS**, four readings the table does not make on its own.

* **THE POLYFILL-COMPLETE SET IS 162 CELLS, 106,032 attested ledger
  rows, 79.7%.** Across the four passes: 120 / 76,634 / 57.6% (ap1) →
  144 / 85,368 / 64.17% (ap2) → 151 / 85,530 / 64.29% (ap3) → **162 /
  106,032 / 79.7%** (ap4). The jump in ROWS is larger than the jump in
  cells because change 3 reached `mov gpr_gpr 64`, `cmp gpr_gpr 64` and
  the other heavily attested cells on go.
* **`1 of 4` rose from 9 cells to 41**, and that is change 2 doing
  exactly what the brief said it would: the x87 arithmetic cells prove on
  c and are refused by nature on the other three, so they are NOT
  comparable target for target and each counts as one.
* **c's `undecided` fell from 48 cells to 2 and its `refused` stayed
  8.** The two that remain are the two x87 compares.
* **The two buckets `2 of 4` and `1 of 4` carry the same 2,804 ledger
  rows.** That is arithmetic and not a copy: the five buckets sum to 253
  cells and to 133,044 rows exactly.

---

# 9. The change table, and the two lists it carries

**LITERAL**, lane `ap4_l14`, same log:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly4.py change | sed -n '1,19p'
runs on task ap3's store: 1012
runs on task ap4's store: 1012
pairs on both: 1012

Table C1 -- every cause of task ap3's loop, what it counted then, and what those same runs say now.

| task ap3's cause | ap3 runs | ap4 runs, same cause | where the rest went |
|---|---|---|---|
| PROVED | 719 | 719 | -- |
| answer home or arrival on the x87 stack | 114 | 114 | -- |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 68 | 12 | 55 PROVED; 1 the gate answered sat: the body holds on a region, not on every input |
| the gate answered sat: the body holds on a region, not on every input | 50 | 50 | -- |
| a width c has no holder for | 24 | 24 | -- |
| term reads state that is not an arrival register | 20 | 20 | -- |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 11 | 10 | 1 the gate answered sat: the body holds on a region, not on every input |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | 2 | 0 | 2 the gate answered sat: the body holds on a region, not on every input |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | 2 | 0 | 2 the gate answered sat: the body holds on a region, not on every input |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows | 1 | 0 | 1 PROVED |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 1 | -- |
```

and the two summary counts, same command:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly4.py change | grep -E '^runs task ap3 proved|^pairs that moved to'
runs task ap3 proved and task ap4 does not: 0
pairs that moved to `sat`: 6
```

**GLOSS.** All 1,012 pairs join and every one of task ap3's 719 proved
runs is proved again; the regression list is empty, which is the brief's
own STOP condition and it did not fire. Three causes are gone entirely —
all three spellings of `the IN rows cannot be aligned`, which is the
arrival-contract group. The 56 runs that left `this unit record carries
no body` are change 3's empty bodies and change 2's x87 c bodies.

**THE SIX PAIRS THAT MOVED TO `sat`**, each a finding and none a
regression. **LITERAL**, the same command:

```
| cell | lang | ap3's cause | the region the counterexample names |
|---|---|---|---|
| `idiv` gpr_one 16 | c | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | holds on a region, not on every input; z3's counterexample: [IN_2 = 3825412232, IN_0 = 9398, IN_1 = 14977] |
| `idiv` gpr_one 32 | c | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | holds on a region, not on every input; z3's counterexample: [IN_0 = 2148532224, IN_1 = 0] |
| `idiv` gpr_one 64 | c | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | holds on a region, not on every input; z3's counterexample: [IN_1 = 9223372036854775808, IN_0 = 9223372036854775808] |
| `mov` imm_gpr 32 | c | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | holds on a region, not on every input; z3's counterexample: [] |
| `mov` imm_gpr 8 | c | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | holds on a region, not on every input; z3's counterexample: [] |
| `ucomisd` mem_xmm 64 | go | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
```

Four of the six are the derived-arrival places read in §5.2. `idiv`
gpr_one 16 on c is the 3,000 ms ceiling reaching an answer this time,
with nothing about the gate touched. `ucomisd` mem_xmm 64 on go is change
3's one non-proof, and its counterexample names NaN — `fp.to_ieee_bv` is
underspecified there and z3 chose the two sides differently.

---

# 10. CHANGE 3 — the identity, and the by-cause table

**LITERAL**, lane `ap4_l14`, same log:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly4.py identity | grep -A 4 'the identity list, by verdict:'
the identity list, by verdict:
     33  PROVED_ON_SHIP
      1  DISPROVED

runs whose `composition` is empty because the body carried no instruction: 31
```

**GLOSS.** 34 places over 26 runs: `mov`, `cmp`, `test`, `sbb`, `adc`,
`lea`, `add` on go, where the argument arrives in the register the answer
leaves from; and `movaps`, `movapd`, `movdqa`, `punpcklqdq` on c, rust
and swift, where a vector register copy is elided. Every one carries
`landing = IDENTITY` and `composition = []`, which are the brief's own
words and neither is a new outcome name.

**WHAT THE TEST IS, and it is deliberately not `strip_chaff`. LITERAL**,
`handful.py`:

```python
RETURN_ONLY = frozenset(["ret", "retq", "repz", "endbr64", "nop",
                         "nopw", "nopl", "hlt"])
```

Task o2's narrow rule counts a register-to-register `mov` as chaff, so
`mov %rdi,%rax; ret` strips to nothing — and that body is not empty: it
moves an arrival into the answer register, which is the identity under
c's calling rule and is not under go's. The test here is the literal one.

**THE BY-CAUSE TABLE. LITERAL**, the same lane:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly4.py causes | sed -n '1,14p'
Table 5 -- what did not work, by cause, the four targets summed. `rows` counts a cell's attested ledger rows once per run, so a cause seen on all four targets counts them four times.

| cause | runs | ledger rows | targets |
|---|---|---|---|
| answer home or arrival on the x87 stack | 114 | 10478 | c, go, rust, swift |
| the gate answered sat: the body holds on a region, not on every input | 56 | 20783 | c, go, rust, swift |
| a width c has no holder for | 24 | 12169 | go, rust, swift |
| term reads state that is not an arrival register | 20 | 18020 | c, go, rust, swift |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 12 | 6829 | swift |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 10 | 3804 | c, go, rust, swift |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 | c |

runs carrying a cause: 237 of 1012
```

**GLOSS.** Seven causes rather than ten, and 237 runs rather than 293.
The `this unit record carries no body` cause is now ONE thing rather than
three summed: 12 swift runs whose carved body is a tail `jmp` to a PLT
relocation, listed in full by lane `ap4_l15`. **LITERAL**, that lane:

```
   `movslq` widen_gpr_gpr 64 / swift  body: jmp 5 <emu_movslq_widen_gpr_gpr_64__reg_rdi__swift+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship021emu_movslq_widen
```

---

# 11. Every `sat`, and the one re-pose

**LITERAL**, lane `ap4_l14`, same log:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly4.py sat | grep -v counterexample
sat at the plain comparison, every written place: 155
sat surviving the caller-extension re-pose: 70
   c      23
   go     19
   rust   21
   swift  7
the five surviving sat places with the most ledger rows:
   ucomiss    xmm_xmm      32    c      [flags] 2270 rows
   ucomiss    xmm_xmm      32    go     [flags] 2270 rows
   ucomiss    xmm_xmm      32    rust   [flags] 2270 rows
   ucomiss    xmm_xmm      32    swift  [flags] 2270 rows
   ucomisd    xmm_xmm      64    c      [flags.low] 1026 rows
```

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly4.py repose
places UNDECIDED at the 3,000 ms ceiling of record and re-posed once at 30,000 ms: 38
   DISPROVED        1
   PROVED_ON_SHIP   3
   UNDECIDED        34

| cell | lang | place | route | ledger rows | the re-pose's answer |
|---|---|---|---|---|---|
| `div` gpr_one 16 | swift | reg_rdx | term | 36 | DISPROVED |
| `div` gpr_one 8 | go | reg_rax | term | 28 | PROVED_ON_SHIP |
| `div` gpr_one 8 | swift | reg_rax | term | 28 | PROVED_ON_SHIP |
| `idiv` gpr_one 8 | go | reg_rax | term | 8 | PROVED_ON_SHIP |
```

**GLOSS.** `sat` is 155 places at the plain comparison against task ap3's
152, and 70 survivors against 67; the three new ones are the region
places of §5.2. The re-pose is a FLAG followed literally: 38 places were
re-posed at 30,000 ms (task ap3 had 147, because most of those are now
decided), four moved, and the verdict OF RECORD stays the 3,000 ms one in
every case.

---

# 12. Memory

The bound stated in `Airlock/instances/ap4.conf`, in every
lane header and in `autopoly4.py`'s own constants is 6 GB resident on the
one collecting process, named abort `ABORT_MEMORY_AP4`, checked after
every run. The sample the law asks for is the first twenty runs, printed
with the peak after each; twenty runs took 19 s and the peak was 262,184
kB.

| lane | what it read | peak resident |
|---|---|---|
| `ap4_l2_probe_the_two_sides_and_the_x87_form.sh` | the cells file and task ap3's store | 81,596 kB |
| `ap4_l3_probe_the_seven_the_flags_halves_and_the_empty_bodies.sh` | the same, and every declined place | 82,820 kB |
| `ap4_l4_probe_the_cell_line_and_the_full_body_walk.sh` | the same, and five reference walks | 82,200 kB |
| `ap4_l5_probe_change2_end_to_end.sh` | one wrap and four ledger calls | 83,140 kB |
| `ap4_l6_probe_the_x87_answer_and_its_arrivals.sh` | five x87 c bodies wrapped and answered | 82,640 kB |
| `ap4_l10_measure_the_three_changes_b.sh` | the two reads, then 187 measured pairs | 261,944 kB |
| `ap4_l11_preflight_and_the_sample.sh` | the two reads, then 20 runs | 262,184 kB |
| `ap4_l12_run_the_loop.sh` | the two reads, then 1,012 runs | 2,427,092 kB |
| `ap4_l13_aggregate_and_report.sh` | the whole 1,012-run store | 87,536 kB |
| `ap4_l14_the_tables.sh` | both 1,012-run stores | 104,216 kB |
| `ap4_l15_two_readings.sh` | the 1,012-run store | 76,800 kB |

The high-water mark, 2,427,092 kB, is 39% of the bound. No abort fired.
Task ap3's own run lane ended at 2,419,276 kB over the same run count.
Lanes `ap4_l7` and `ap4_l8` print no peak of their own: their work is
`model_translate.py check` and `o8_regression.py` in separate processes,
each with its own bound (task o8's is `ABORT_MEMORY_O8`, 2 GB, and its
own collector printed `collector peak 82468 kB`).

---

# 13. The deliverables

Under
`PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`:

| file | what it is |
|---|---|
| `autopoly4.py` | the loop, the bookkeeping, the aggregate, the report, the change table, and the two lists this task adds (`region`, `identity`) |
| `autopoly4_cells.json` | the 253 attested cells, task ap3's file copied and its counts re-measured |
| `autopoly4_runs.jsonl` | the incremental store of the loop of record, 1,012 lines |
| `autopoly4.json` | the aggregate |
| `autopoly4.md` | the report, 505 lines |
| `autopoly4_check_L2_rerun.json` | the `check` re-derived, kept here rather than over the stored artifact |
| `src4/` | the rendered sources of the loop |
| `lanes_ap4/` | the fifteen lane scripts |

Changed outside that folder: the three files of §3. Nothing else under
`Research/` moved.

---

# 14. The guard and the tally

**LITERAL**, lane `ap4_l13_aggregate_and_report.sh`, on the tower at
`<runs>/ap4/agent/logs/20260909T221230Z__ap4_l13_aggregate_and_report.sh.log`:

```
[3/6] the store and the aggregate compared run for run
lines on the store: 1012
runs on the aggregate: 1012
run for run identical: 1012
distinct (cell, target) pairs: 1012

[4/6] the spelling guard, over every json this task wrote
operator inventory: 91 tokens read from probe_manifest_*.json
PASS autopoly4_cells.json -- no operator token in any key, grouping, pairing or row structure
operator inventory: 91 tokens read from probe_manifest_*.json
PASS autopoly4.json -- no operator token in any key, grouping, pairing or row structure
operator inventory: 91 tokens read from probe_manifest_*.json
PASS autopoly4_check_L2_rerun.json -- no operator token in any key, grouping, pairing or row structure
```

and the tally, **LITERAL**, the same lane:

```
[6/6] the tally
runs recorded: 1012 of 1012

| target | attempted | rendered | compiled | LANDED | proved | sat | undecided | refused |
|---|---|---|---|---|---|---|---|---|
| c | 253 | 245 | 245 | 76 | 204 | 19 | 2 | 8 |
| rust | 253 | 209 | 209 | 72 | 170 | 15 | 3 | 44 |
| go | 253 | 200 | 200 | 30 | 177 | 17 | 6 | 53 |
| swift | 253 | 200 | 200 | 70 | 163 | 5 | 15 | 53 |
```

**`grep -c exempt` over what this task added is 0 everywhere except one
file, and that file is the lane that runs the grep.** Its two matches
are its own two lines, exactly as task ap3's were.

---

# 15. The two lists

## Decided, recorded for audit

1. **The 38 declined places were two populations and the probe is what
   said so** (§4.1, §5.1). Seven are the derived arrival the brief
   describes; 31 are a HALF of the flags place on the primitive route,
   which the driver's own rule already refused when the place was not
   halved. The generalisation is one function, `is_the_flags_place`, and
   it moves 12 PROVED places to refused and no RUN at all, because a
   run's verdict is its destination place.
2. **The relation between two arrival contracts is READ, never named**
   (§4.2): the reference simulator steps the emulation's own attested
   body, and what it leaves in each register at the cell's own
   instruction is the substitution. Anything that does not step, or a
   symbol that is not one of the emulation's arrivals, is a refusal by
   name.
3. **A region is printed only where z3 proved it** (§5.2,
   `proved_equal`). The two relations tested are the corpus's own setup:
   equality, and the sign spread the `SPREAD_SIGN` / `ACCUMULATOR_WIDEN`
   instructions leave.
4. **A cell arrival the substitution cannot place is left FREE rather
   than guessed** (`xor` gpr_same 32, §5.2). That makes the obligation
   stronger, not weaker, and the run record names the symbol.
5. **Change 2 is two halves and the log says which is which** (§6.2).
   The ledger's is the epilogue and the prelude, which is what the brief
   authorises. `reference.answer_of` and
   `pool100_entry_equivalence.align_by_row` cannot read or align an x87
   value and are files this brief does not name, so BOTH readings are
   done in the driver instead, over the reference's own state and the
   reference's own x87 stack.
6. **The argument-slot order is a MEASURED fact of this toolchain**
   (§6.3), pinned by compiling `a - b` and `b - a` at the corpus's own
   ship flags, not a reading of the System V document.
7. **`canonical_form.py` was not changed.** Its `no answer home` text is
   still exactly right for a unit that leaves its answer nowhere, and an
   x87 unit no longer reaches it.
8. **The three changes are UNGATED on a task name**, for the reason
   `use_task_ap2`'s docstring gave and `use_task_ap3` repeated. The
   three guards of §7 are what a task name would have been standing in
   for, and all three pass.
9. **An empty body is tested literally and not by `strip_chaff`**
   (§10), because the narrow rule strips a register-to-register `mov`
   that is the identity in one calling rule and not in another.
10. **The `idiv` quotient place disproves and its remainder place
    proves** (§5.2), which is what the pipeline's own two-place design
    is for: the matched corpus row is the `%` probe, so the operator
    answers the remainder.
11. **Nothing was deleted under `<runs>/` or
    `Airlock/`** on either machine. One lane name
    collided and took a new name (`ap4_l10_measure_the_three_changes_b.sh`
    after `ap4_l9`'s two defects, which are recorded in §2 rather than
    hidden); `check_command`'s 178 files were copied aside and copied
    back, compared by sha256.

## Awaiting the owner

1. **The cell key does not carry an immediate, so an `imm_*` cell is not
   one mapping** (§5.2). `mov` imm_gpr 8 and 32 disprove with an empty
   counterexample because the cell's own line is `mov $0x3,%dil` /
   `mov $0x3,%edi` and the corpus rows the lookup matches are
   `mov $0x1,%al` and `mov $0x8,%eax`. Whether the operand form should
   name the immediate is an ontology question about what a cell IS, and
   it is the only one this task met.
2. **cpp is a fifth compiled language the corpus already holds rows
   for**, and adding it changes what "proved on all four" counts, which
   is structural. Carried unchanged from log_245's list.

---

# 16. The conventions verifier over this log

Three passes, each a lane of this task's own instance, each over this log
as it then stood.

| pass | lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|---|
| first | `ap4_l16_verify_246.sh` | 34 | 5 | **3** | 26 | 0 | 0 |
| second | `ap4_l17_verify_246b.sh` | 34 | 7 | **0** | 26 | 1 | 0 |
| third | `ap4_l18_verify_246c.sh` | 34 | 8 | **0** | 26 | 0 | 0 |

**GLOSS**, and the obligation the law states is the DIFFERS column: **0**
on the pass of record.

* **The three DIFFERS of the first pass were all fixed in the CLAIM and
  none in the verifier**, and all three were one mistake of mine: a
  pasted command cut with `head -N`, which closes the pipe under a
  program that goes on printing and puts a `BrokenPipeError` traceback
  into the output the verifier then re-produces. Two are now cut with
  `sed -n '1,Np'`, which reads the whole stream; the third pasted
  `identity | tail -8`, whose last line is a peak-resident figure that
  moves between runs, and it now cuts the four lines that do not move.
* **The one REFUSED of the second pass was also fixed in the claim.**
  That third cut was first written as `sed -n '/.../,/.../p'`, and the
  verifier reads the range expression as a file path it cannot reach —
  the same heuristic misfire task ap3 met (log_245 §17). It is now
  `grep -A 4`, which is what task ap3 used for the same reason.
* **MATCHES (8)** — `tables`, `causes`, `repose`, `sat`, `region`,
  `identity`, and `change` in its two pieces.
* **UNVERIFIABLE (26)** — eight prose paragraphs (the answer, the two
  findings said before the numbers, the flags-half measurement, the
  region reading, the x87 reading, the change table's gloss and the two
  list items) and eighteen attributions, each naming the lane log it
  came from.

This section was appended after the third pass, and a fourth pass over
the log WITH it in place — lane `ap4_l19_verify_246d.sh`, the closing one
— is what the table's third row is checked against.
