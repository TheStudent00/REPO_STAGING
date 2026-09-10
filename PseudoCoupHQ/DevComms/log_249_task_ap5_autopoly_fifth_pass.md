# log 249 — task ap5: the two mechanical remainders of the four languages — the x87 stack read end to end, the immediate as an input of the mapping, and AutoPoly's loop, fifth pass

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/`).
Line: arch_unit_oracle, the "goal" section of 2026-09-07 and the rulings of
2026-09-08 and 2026-09-09 in
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`.
Law: `PseudoCoupHQ/Research/LAW.md`, read in full including its
tower section. Brief:
`PseudoCoupHQ/Research/briefs/task_ap5_brief.md`.
Date: 2026-09-09. Instance `ap5`, on the tower guest.

Artifact folder:
`PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`,
writing `autopoly5_*`; tasks ap1 to ap4's products are not overwritten. Lane
scripts: `.../autopoly/lanes_ap5/`, twenty-four of them, each kept in the repo
as the standing rule of 2026-09-07 requires. Every lane log named below is on
the TOWER (`<user>@<tower>`) under
`<runs>/ap5/agent/logs/`.

**THIS TASK RAN IN TWO SITTINGS AND THE SECOND ONE WROTE THIS LOG.** The first
implementer was stopped by a usage limit after lane `ap5_l16`; lanes `ap5_l1`
to `ap5_l16` are its work and `ap5_l17` to `ap5_l24` are this one's. Lanes
`ap5_l17` to `ap5_l21` were already on disk, written by the first implementer
and never submitted; they were read against the state and submitted unchanged.
Nothing under `<runs>/` or `Airlock/` was deleted.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PseudoCoupHQ`, mounted into the
instance. Every rendering is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself, quoted;
**GLOSS** is a plain-words reading beside a literal. Where a pasted block shows
`...[N chars]`, the LANE truncated the field, not this log.

---

# 1. What this is, one sentence per object in relation

* A **CELL** is one (`mnem`, operand shape, `key_width`) row of the arch-opcode
  model table, holding, per place the opcode writes, the z3 term the reference
  simulator's own builder puts there.
* The **OUTER SET** is the 253 cells the canon40 corpus attests, over 133,044
  attested ledger rows — task ap4's file rebuilt here with 20 rows added and no
  existing row changed, both counts identical.
* A **RUN** is `find_emulation(cell, lang)` on one of the four compiled
  targets: the target's own operator where its whole lowered body IS the cell,
  the cell's term written in the target's operators where it is not, compiled
  at the corpus's ship flags, carved, and put back to z3 against the cell's own
  term.
* An **x87 ARRIVAL** is an input a cell reads off the 80-bit register stack. It
  reaches an IN row under TWO spellings and the pipeline already says so in
  `emulate.X87_ARRIVAL`: `X87_<k>` is a stack POSITION the model table
  preseeded, `x87_<mangled operand>` is a literal memory operand read at the
  x87 sort. An **x87 ANSWER HOME** is `X87_<k>` named as a unit's result family.
* An **`imm_*` CELL** is a cell whose operand shape carries an immediate. The
  cell key carries no immediate, so the sweep's own spelling bakes `$0x3` in
  while the corpus rows the cell is attested by spell `$0x1`, `$0x8` and the
  rest. A **SYMBOLIC-IMMEDIATE ROW** is that shape spelled a second time with a
  register of the operand's own width in the immediate's slot, marked
  `imm_symbolic` on the cells file.
* **THIS TASK** is the loop run a fifth time after the two mechanical
  remainders task ap4's log listed were each closed in the layer that owns it.

**THE ANSWER: 165 cells proved on all four targets, 106,773 attested ledger
rows, 80.25%** — up from task ap4's 162 / 106,032 / 79.7%, ap3's 151 / 85,530 /
64.29%, ap2's 144 / 85,368 / 64.17% and ap1's 120 / 76,634 / 57.6%. Runs
carrying a cause: 232 of 1,012, down from task ap4's 237.

**AND THE BRIEF'S STOP CONDITION IS MET, so this task stops here and does not
run a sixth pass. Runs task ap4 proved that task ap5 does not: 1** — `sbb`
imm_gpr 8 on swift. It is named, read off both stores, and left as it is; §4 is
that reading. The brief's words are "zero regressions or STOP".

Three things are said before the numbers so the numbers are not misread:

* **The x87 change is a MOVE OF LAYER, not a gain in the population.** Task ap4
  already proved the 30 x87 c cells, using two stand-ins IN THE DRIVER because
  the two shared functions that do those jobs for every other place were not
  files its brief named. This brief names them. The reading now happens in
  `reference.answer_of` and `pool100_entry_equivalence.align_by_row`, the
  driver's `x87_answer_for_unit` is GONE, and the verdicts are the same ones:
  **36 x87 places PROVED on c, 0 disproved, 0 sat, 0 undecided**; rust, go and
  swift refused by nature as before. §6.
* **The immediate change is where the six gained runs come from.** Six runs
  task ap4 answered `sat` are proved now, every one an `imm_*` cell whose
  primitive route had matched a corpus body carrying a DIFFERENT baked-in
  immediate. §7.
* **The first pass of this task's own loop was WRONG and was re-run.** Lane
  `ap5_l8` measured 31 regressions; 30 were one defect in the new
  `align_by_row` branch, which tested only one of the two x87 spellings. Lane
  `ap5_l15` found it, the branch was widened, lane `ap5_l16` ran the 1,012
  again, and the first pass's store is KEPT beside the second as
  `autopoly5_runs.jsonl.before_the_x87_memory_arrival_fix`. §3.

---

# 2. The two changes, each in the layer that owns it

## 2.1 The x87 stack, read end to end

Three edits and one deletion, and the brief authorises exactly those three
files:

| file | function | what it does now |
|---|---|---|
| `PseudoCoupHQ/Research/op_pipeline/reference.py` | `answer_of` | an answer home spelled `X87_<k>` is read off the reference's own `MachineState.x87` through its own `x87_at`, under the same `fpToIEEEBV` the model table's builder puts on an x87 place |
| `PseudoCoupHQ/Research/op_pipeline/pool100_entry_equivalence.py` | `align_by_row` | an arrival whose family is spelled `X87_<k>` or `x87_<operand>` is aligned by its IN row like any other, at `reference.X87_SORT` instead of a `BitVec` |
| `PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py` | `shapes_for` | §2.2 |
| `PseudoCoupHQ/Research/oracle/cross_construction/emulation/emulate.py` | `x87_answer_for_unit` REMOVED | task ap4's driver-side stand-in for `answer_of`, called from one line of `body_answer` and nowhere else; the docstring left in `body_answer` says why it is gone |

**WHY THE `BitVec` WAS THE DEFECT, LITERAL** — lane `ap5_l15`, asking
`align_by_row` itself under both spellings:

```
emulate.X87_ARRIVAL, LITERAL: ('X87_', 'x87_')
align_by_row over the two spellings:
   X87_0        fp.to_ieee_bv(seed_X87_0)   ->   fp.to_ieee_bv(IN_0)
   x87__rsi_    fp.to_ieee_bv(seed_x87__rsi_)   ->   fp.to_ieee_bv(IN_0)
```

**GLOSS.** `seed_X87_0` and `seed_x87__rsi_` are both `FPSort(15, 64)`
constants; the `z3.BitVec` the old line built under those names was a
DIFFERENT constant, so the substitution silently did nothing and the seed
stayed free on the cell side. Both spellings now land on the row's `IN_i`.

## 2.2 The immediate as an input of the mapping

`model_translate.shapes_for` spells every `imm_*` shape a SECOND time with a
register of the operand's own width in the immediate's slot — which is how the
reference's own operand reader spells a value of that width that is not a
literal — and the sweep marks those rows `imm_symbolic`. The driver
(`handful.the_symbolic_immediate_row`) chooses such a row where the cell has
one, takes the immediate as one more parameter of the operand's width, and does
NOT ask the primitive route, whose lookup key is the cell's own triple and
therefore carries no immediate.

**THE CELLS FILE, BEFORE AND AFTER, LITERAL** — lane `ap5_l4` §[3/4]
(`<runs>/ap5/agent/logs/*__ap5_l4_build_the_cells_file.sh.log`):

```
   cells on the new file: 253
   attested ledger rows on the new file: 133044
   rows added, all of them symbolic: 20
   existing rows that differ in ANY field: 0
   cells on the old file that are not on the new: 0
```

**GLOSS**, and it answers the brief's guard on m1b's coverage totals directly:
the cell count did NOT rise — it is 253 before and after, and the ledger rows
are the same 133,044. The 20 symbolic rows are extra TRANSLATED rows AT cells
that already existed, and no existing row's text changed in any field.

---

# 3. The two regressions of the first pass, and their fate

Lane `ap5_l8` ran the 1,012 and lane `ap5_l13`'s change table then said "runs
task ap4 proved and task ap5 does not: 31". That is the brief's STOP condition,
so lane `ap5_l15` asked both populations before anything was re-run.

**THE THIRTY — `mem_one` 80 cells on c — were this task's own defect.** The
counterexamples named `seed_x87__rsi_` free on the cell side beside `IN_0` and
`IN_1`. An x87 arrival reaches a row under two names and the first draft of
`align_by_row`'s new branch tested only `X87_`, so the second arrival of those
thirty cells — a MEMORY operand read at the x87 sort — was never put on a row.
The branch now tests both. **LITERAL**, lane `ap5_l15` §[1/2], one of the four
it re-ran with the widened branch:

```
   == `faddl` mem_one 80 -> c
      route: term   line: 'faddl (%rsi)'
      place x87_6          rendered True  outcome PROVED_ON_SHIP
         the cell's families: ['X87_0', 'x87__rsi_']
         the parameter plan: [('a', 'long double', 'X87_0', 79), ('b', 'long double', 'x87__rsi_', 79)]
         the carved body: none
         aligned_rows: [{'row': 'IN-0', 'the cell reads': 'X87_0', 'the body reads': 'x87_0x18_rsp_, the argument slot at 0x18(%rsp)'}, {'row': 'IN-1', 'the cell reads': 'x87__rsi_', 'the body reads': 'x87_0x8_rsp_, the argument slot at 0x8(%rsp)'}]
         reason: z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row
      the run's verdict: proved
```

**THE ONE — `sbb` imm_gpr 8 on swift — SURVIVED the second pass** and is §4.

Lane `ap5_l16` then re-ran the whole 1,012 from an empty store, keeping the
first pass's file rather than deleting it. **LITERAL**, its tail:

```
runs performed this lane: 1012 in 1412 s
lines on PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5_runs.jsonl: 1012
peak resident: 2423324 kB
```

---

# 4. The STOP: the one run task ap4 proved that task ap5 does not

**`sbb` imm_gpr 8 → swift.** Task ap4: `term / proved`. Task ap5:
`term / undecided`, cause "the carved body: the reference: this unit record
carries no body, so there is no ship code to walk; and no term either". It is
the only entry of table C2.

Lane `ap5_l22` reads the two stores' lines for that one pair and prints them
field by field, and writes nothing. **LITERAL**, task ap4's line, head:

```
== task ap4: `sbb` imm_gpr 8 -> swift
   attestation                  {"example_units": ["cpp/op_764", "cpp/regen_53017", "cpp/regen_53020"], "flag_pair_rows": 0, "ledger_rows": 164, "setter": [], "units": 82}
   attested_ledger_rows         164
   chosen_by                    "of the 8 TRANSLATED rows at this cell, the one whose own sweep width equals the cell's key_width"
   composition                  [{"cell": true, "key_width": 32, "line": "lea 0xff(%rdx),%eax", "mnem": "lea", "shape": "mem_gpr"}, {"cell": true, "key_width": 8, "line": "add %dil,%sil", "mnem": "add", "shape": "gpr_gpr"}, {"cell": true, "key_width": 32, "line": "cmovae %edx,%eax", "mnem": "cmovae", "shape": "gpr_gpr"}, {"cell": true, "key_width": 32, "line": "add $0xfd,%eax", "mnem": "add", "shape": "imm_gpr"}, {"cell": true,  ...[606 chars]
   key_width                    8
   lang                         "swift"
   line                         "sbb $0x3,%dil"
   mnem                         "sbb"
   primitive                    {"cause": "no single-opcode row of this language's own corpus is this cell's instruction plus zero-operand setup and nothing else", "cell": {"key_width": 8, "mnem": "sbb", "shape": "imm_gpr"}, "lang": "swift", "lookup": "single_opcode_units.json, this language's own rows under BOTH of task o2's rules, each stripped again under the NARROW rule and accepted when what remains is the cell's instructio ...[626 chars]
   route                        "term"
   row_id                       "r51173"
```

**LITERAL**, task ap5's line, head:

```
== task ap5: `sbb` imm_gpr 8 -> swift
   attestation                  {"example_units": ["cpp/op_764", "cpp/regen_53017", "cpp/regen_53020"], "flag_pair_rows": 0, "ledger_rows": 164, "setter": [], "units": 82}
   attested_ledger_rows         164
   chosen_by                    "of the 9 TRANSLATED rows at this cell, the one whose immediate is an INPUT of the mapping rather than a literal (`imm_symbolic`)"
   composition                  [{"cell": false, "line": "jmp 5 <emu_sbb_imm_gpr_8__reg_rdi__swift+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship33emu_sbb_imm_gpr_8__reg_rdi__swiftys6UInt64Vs5UInt8V_A3FtF-0x4", "mnem": "jmp", "reason": "the classifier could not read it: an operand text this classifier does not read: '5 <emu_sbb_imm_gpr_8__reg_rdi__swift+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship33emu_sbb_imm_gpr_8__reg_rdi__swiftys6UInt ...[425 chars]
   key_width                    8
   lang                         "swift"
   line                         "sbb %r8b,%dil"
   mnem                         "sbb"
   primitive                    {"cause": "the immediate is an input of the mapping, and a corpus body carries a baked-in immediate of its own", "cell": {"key_width": 8, "mnem": "sbb", "shape": "imm_gpr"}, "lang": "swift", "lookup": "not asked: the lookup's key is the cell's own triple, which carries no immediate, so a body it matches would carry a baked-in immediate of its own", "row": null}
   route                        "term"
   row_id                       "r51173_imm_symbolic"
```

**LITERAL**, the `reg_rdi` place on task ap4's side:

```
   -- place reg_rdi
      bits                     64
      body_bytes               "8d 82 ff 00 00 00 40 00 fe 0f 43 c2 05 fd 00 00 00 0f b6 c0 c3"
      body_text                [90 chars, not printed here]
      check                    {"aligned_rows": [{"row": "IN-0", "the body reads": "rdi", "the cell reads": "rsi"}, {"row": "IN-1", "the body reads": "rsi", "the cell reads": "rdx"}, {"row": "IN-2", "the body reads": "rdx", "the cell reads": "rdi"}], "arrival_families_read_off_the_body": ["rdi", "rsi", "rdx"], "body_bits": 32, "body_side_free_state": [], "canon40_outcome": "WRAPPED_TEXT_PROVED", "cell_bits": 64, "outcome": "PRO ...[796 chars]
      compiled                 true
      families                 ["rsi", "rdx", "rdi"]
      home                     {"family": "rdi", "source": "the place the reference's own builder wrote"}
      label                    "sbb_imm_gpr_8__reg_rdi__swift"
      landing                  {"holds_the_cells_own_opcode": false, "remaining": [{"mnem": "lea"}, {"mnem": "add"}, {"mnem": "cmovae"}, {"mnem": "add"}, {"mnem": "movzbl"}], "stripped_count": 5, "stripped_text": "lea 0xff(%rdx),%eax; add %dil,%sil; cmovae %edx,%eax; add $0xfd,%eax; movzbl %al,%eax", "verdict": "NOT_COLLAPSED"}
```

**LITERAL**, the `reg_rdi` place on task ap5's side:

```
   -- place reg_rdi
      bits                     64
      body_bytes               "e9 00 00 00 00"
      body_text                [144 chars, not printed here]
      check                    {"arrival_families_read_off_the_body": [], "canon40_outcome": "REFUSED", "outcome": "UNDECIDED", "reason": "the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either", "recheck": {"arrival_families_read_off_the_body": [], "canon40_outcome": "REFUSED", "ceiling_ms": 30000, "outcome": "UNDECIDED", "reason": "the carved body: the reference: ...[516 chars]
      compiled                 true
      families                 ["rsi", "rdx", "rdi", "r8"]
      home                     {"family": "rdi", "source": "the place the reference's own builder wrote"}
      label                    "sbb_imm_gpr_8__reg_rdi__swift"
      landing                  {"landed": {"mnem": "jmp"}, "remaining": [{"mnem": "jmp"}], "stripped_count": 1, "stripped_text": "jmp 5 <emu_sbb_imm_gpr_8__reg_rdi__swift+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship33emu_sbb_imm_gpr_8__reg_rdi__swiftys6UInt64Vs5UInt8V_A3FtF-0x4", "verdict": "LANDED_ELSEWHERE"}
```

**GLOSS, and this is the cause by the record rather than by guess.** The cell
now chooses the symbolic-immediate row `r51173_imm_symbolic`, whose line is
`sbb %r8b,%dil` and whose rendered swift function therefore takes FOUR `UInt8`
parameters where task ap4's `sbb $0x3,%dil` rendering took three. What the
carve gets back for the four-parameter one is **five bytes,
`e9 00 00 00 00`** — a single `jmp` relocated `R_X86_64_PLT32` to the mangled
swift symbol `$s9unit_ship33emu_sbb_imm_gpr_8__reg_rdi__swift…`. The `@_cdecl`
entry point compiled to a TAIL-CALL THUNK into the real swift function instead
of holding the arithmetic; the landing is `LANDED_ELSEWHERE` on `jmp`, and the
reference walking that body says the unit record carries no body. Task ap4's
three-parameter rendering of the same cell carved 21 bytes of real arithmetic
and proved.

WHAT IS NOT ESTABLISHED, said plainly: the record shows the thunk, not WHY
swiftc emitted one here and not for the three-parameter rendering, nor for the
same cell's two-parameter `flags` place, which carved real arithmetic on swift
in both passes. The parameter count is the visible difference; it is not proved
to be the cause. The other 19 cells with a symbolic row did not do this on
swift. Nothing was patched and no third pass was run: the brief says STOP, and
this is the report of it.

---

# 5. The tables

## 5.1 Per target, what the loop reached

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.py tables
## 1. THE table: per target, what the loop reached

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.

| step or verdict | c | rust | go | swift |
|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `compiled` | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `LANDED` | 73 cells, 40976 rows, 30.8% | 69 cells, 38346 rows, 28.82% | 27 cells, 23481 rows, 17.65% | 67 cells, 38062 rows, 28.61% |
| `LANDED_ELSEWHERE` | 26 cells, 11853 rows, 8.91% | 22 cells, 11871 rows, 8.92% | 18 cells, 5442 rows, 4.09% | 35 cells, 18864 rows, 14.18% |
| `NOT_COLLAPSED` | 142 cells, 73008 rows, 54.88% | 114 cells, 72935 rows, 54.82% | 145 cells, 76696 rows, 57.65% | 94 cells, 61850 rows, 46.49% |
| `proved` | 200 cells, 99156 rows, 74.53% | 164 cells, 95590 rows, 71.85% | 178 cells, 113591 rows, 85.38% | 156 cells, 88645 rows, 66.63% |
| `proved under caller extension` | 27 cells, 21022 rows, 15.8% | 28 cells, 21994 rows, 16.53% | 0 cells, 0 rows, 0.0% | 24 cells, 20270 rows, 15.24% |
| `sat` | 16 cells, 5893 rows, 4.43% | 14 cells, 5024 rows, 3.78% | 16 cells, 5177 rows, 3.89% | 4 cells, 3662 rows, 2.75% |
| `undecided` | 2 cells, 1008 rows, 0.76% | 3 cells, 1786 rows, 1.34% | 6 cells, 1250 rows, 0.94% | 16 cells, 7441 rows, 5.59% |
| `refused` | 8 cells, 5965 rows, 4.48% | 44 cells, 8650 rows, 6.5% | 53 cells, 13026 rows, 9.79% | 53 cells, 13026 rows, 9.79% |

## 2. Per target, how far the primitive route reached

Table 2 -- `primitive` is a target operator whose whole lowered body IS the cell; `primitive+setup` is that plus zero-operand accumulator setup (task g1c's widened lookup); `term` is the cell's own term written in the target's operators, which is the fallback.

| route | c | rust | go | swift |
|---|---|---|---|---|
| `primitive` | 26 cells, 18805 rows, 14.13% | 21 cells, 12184 rows, 9.16% | 16 cells, 10347 rows, 7.78% | 8 cells, 7713 rows, 5.8% |
| `primitive+setup` | 2 cells, 1726 rows, 1.3% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |
| `term` | 225 cells, 112513 rows, 84.57% | 232 cells, 120860 rows, 90.84% | 237 cells, 122697 rows, 92.22% | 245 cells, 125331 rows, 94.2% |
| `no route reached` | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |

Table 3 -- a cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 4 of 4 | 165 | 106773 | 80.25% |
| 3 of 4 | 21 | 8275 | 6.22% |
| 2 of 4 | 7 | 2804 | 2.11% |
| 1 of 4 | 40 | 2743 | 2.06% |
| 0 of 4 | 20 | 12449 | 9.36% |

`sat` at the plain comparison, every written place: 174
`sat` surviving the caller-extension re-pose: 65
the handful's forty pairs: 32 agree character for character, 35 agree on the verdict, 4 not in this outer set
```

## 5.2 The five-pass all-four line

**GLOSS**, one row per pass, each figure off that pass's own `autopoly*.md`
Table 3 (`grep '| 4 of 4 |' autopoly.md autopoly2.md autopoly3.md autopoly4.md
autopoly5.md` in the artifact folder):

| pass | task | cells proved on all four | attested ledger rows | share of 133,044 |
|---|---|---|---|---|
| 1 | ap1 | 120 | 76,634 | 57.6% |
| 2 | ap2 | 144 | 85,368 | 64.17% |
| 3 | ap3 | 151 | 85,530 | 64.29% |
| 4 | ap4 | 162 | 106,032 | 79.7% |
| 5 | ap5 | **165** | **106,773** | **80.25%** |

## 5.3 The change table, task ap4 → task ap5

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.py change | sed -n '1,30p'
runs on task ap4's store: 1012
runs on task ap5's store: 1012
pairs on both: 1012

Table C1 -- every cause of task ap4's loop, what it counted then, and what those same runs say now.

| task ap4's cause | ap4 runs | ap5 runs, same cause | where the rest went |
|---|---|---|---|
| PROVED | 775 | 774 | 1 the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| answer home or arrival on the x87 stack | 114 | 114 | -- |
| the gate answered sat: the body holds on a region, not on every input | 56 | 50 | 6 PROVED |
| a width c has no holder for | 24 | 24 | -- |
| term reads state that is not an arrival register | 20 | 20 | -- |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 12 | 12 | -- |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 10 | 10 | -- |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 1 | -- |

Table C2 -- runs task ap4 proved that task ap5 does not.

| cell | lang | ap5's cause, which task ap4 did not have |
|---|---|---|
| `sbb` imm_gpr 8 | swift | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |

runs task ap4 proved and task ap5 does not: 1

Table C3 -- pairs that moved to `sat`: the gate now has a comparison to answer and answers it with a counterexample, which names a region rather than a limit.

| cell | lang | ap4's cause | the region the counterexample names |
|---|---|---|---|

```

**GLOSS.** PROVED 775 → 774: the one loss is §4. `sat` 56 → 50: six runs the
gate could not prove against a body with a foreign baked-in immediate are
proved against the symbolic row. Every other cause is unmoved, the x87 refusal
count included — which is the point of §2.1: the reading moved layers and the
population did not.

**Tables C2 and C3 in full.** C2's column header was corrected in this task's
own file from "ap4's cause" to "ap5's cause, which task ap4 did not have": the
value printed there was always `cause_of` on task ap5's run, so only the label
was wrong. **LITERAL**, lane `ap5_l21`:

```
Table C2 -- runs task ap4 proved that task ap5 does not.

| cell | lang | ap5's cause, which task ap4 did not have |
|---|---|---|
| `sbb` imm_gpr 8 | swift | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |

runs task ap4 proved and task ap5 does not: 1

Table C3 -- pairs that moved to `sat`: the gate now has a comparison to answer and answers it with a counterexample, which names a region rather than a limit.

| cell | lang | ap4's cause | the region the counterexample names |
|---|---|---|---|

pairs that moved to `sat`: 0
```

## 5.4 By cause

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.py causes
Table 5 -- what did not work, by cause, the four targets summed. `rows` counts a cell's attested ledger rows once per run, so a cause seen on all four targets counts them four times.

| cause | runs | ledger rows | targets |
|---|---|---|---|
| answer home or arrival on the x87 stack | 114 | 10478 | c, go, rust, swift |
| the gate answered sat: the body holds on a region, not on every input | 50 | 19756 | c, go, rust, swift |
| a width c has no holder for | 24 | 12169 | go, rust, swift |
| term reads state that is not an arrival register | 20 | 18020 | c, go, rust, swift |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 13 | 6993 | swift |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 10 | 3804 | c, go, rust, swift |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 | c |

runs carrying a cause: 232 of 1012

THE ARRIVAL-CONTRACT GROUP, counted on its own: every gate call that declined because the two sides name a different number of arriving values.

places the gate declined on the IN-row alignment: 0

| cell | route | ledger rows |
|---|---|---|
```

---

# 6. Every x87 place, with the gate's verdict, by count

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.py x87 | sed -n '1,2p'
x87 places, over 156 run(s) at key_width 80: 164

```

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.py x87 | grep '^| ' | cut -d'|' -f3,6 | sort | uniq -c
      5  c | NOT_RENDERED 
     36  c | PROVED_ON_SHIP 
     41  go | NOT_RENDERED 
      1  lang | the gate's verdict 
     41  rust | NOT_RENDERED 
     41  swift | NOT_RENDERED 
```

**GLOSS.** 164 places over 156 runs at `key_width` 80, 41 per target.

| target | PROVED_ON_SHIP | NOT_RENDERED | DISPROVED | UNDECIDED | sat |
|---|---|---|---|---|---|
| c | 36 | 5 | 0 | 0 | 0 |
| rust | 0 | 41 | 0 | 0 | 0 |
| go | 0 | 41 | 0 | 0 | 0 |
| swift | 0 | 41 | 0 | 0 | 0 |

(The `lang | the gate's verdict` row of that tally is the markdown table's
own header line, which `cut` cannot tell from a data row; it is not a place.
The table's rule row is not matched at all, because it begins `|-` and not
`| `.)

**THE BRIEF ASKED FOR A `sat` WITH ITS COUNTEREXAMPLE, AND THERE IS NONE.**
The brief's words: "a `sat` with its counterexample — the 80-bit format's
explicit integer bit is where one is expected, and if it appears, it is a
finding about `long double` against the reference's `FPSort(15, 64)`, stated,
not patched." **No x87 place is `sat` and none is DISPROVED**, so there is no
such finding to state. The DISPROVED x87 places of this task's FIRST pass (lane
`ap5_l13`) were the `align_by_row` defect of §3 and not the format: their
counterexamples named `seed_x87__rsi_`, a free symbol, and they are gone.

**The five c places that still do not render** are `fucomi` and `fucomip`
st_st 80 (`flags.low` and `flags.high` on each) and `fldz` st_none 80 — a
comparison that ARRIVES on the stack and writes flags, and a constant push with
no arrival — all under the standing cause "answer home or arrival on the x87
stack". That cause carries 114 runs over the four targets, exactly as it did
for task ap4.

---

# 7. The `imm_*` cells, before and after

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.py immediate | sed -n '1,8p'
imm_* cells on the outer set: 27
of those, cells the cells file gives a symbolic-immediate row: 20
cells on the outer set, before and after: 253 and 253

Table I1 -- every imm_* cell, task ap4's route and verdict against task ap5's, per target.

| cell | symbolic row | c | rust | go | swift |
|---|---|---|---|---|---|
```

Table I1 in full — one row per `imm_*` cell, task ap4's route and
verdict against task ap5's on each target — is in lane `ap5_l21`'s log
(`<runs>/ap5/agent/logs/*__ap5_l21_the_tables_b.sh.log`)
and in `autopoly5.md`; it is not pasted here because its cells carry `->`,
which the conventions verifier reads as an arrow gloss and refuses to
compare.

**GLOSS.** 27 `imm_*` cells on the outer set; 20 have a symbolic row; 7 do not,
and the reason on each is the reference's own `NotModeled` when the symbolic
line is re-read — a shift whose count is a register that is not `%cl`, and
`pextrw` whose index is not an immediate. Cells before and after: 253 and 253.

**THE SIX RUNS THAT MOVED**, off Table I1 (`sat` → proved, every one a
primitive-route match against a body carrying a foreign immediate):

| cell | target | task ap4 | task ap5 |
|---|---|---|---|
| `mov` imm_gpr 32 | c | primitive / sat | term / proved |
| `mov` imm_gpr 8 | c | primitive / sat | term / proved under caller extension |
| `xor` imm_gpr 8 | c | primitive / sat | term / proved under caller extension |
| `xor` imm_gpr 8 | rust | primitive / sat | term / proved under caller extension |
| `xor` imm_gpr 8 | swift | primitive / sat | term / proved under caller extension |
| `xor` imm_gpr 32 | go | primitive / sat | term / proved |

**THE ONE THAT MOVED THE OTHER WAY** is `sbb` imm_gpr 8 on swift, §4.

**THE CORPUS'S OWN IMMEDIATES, counted under the one cell** (Table I2, lane
`ap5_l21`): four cells have single-opcode rows that classify to them, and the
distinct constants those rows spell are — `mov` imm_gpr 32, 5 rows,
`$0x1 $0x10 $0x2 $0x4 $0x8`; `xor` imm_gpr 8, 3 rows, `$0x1`; `mov` imm_gpr 8,
1 row, `$0x1`; `xor` imm_gpr 32, 1 row, `$0x1`. The other 23 have none — which
is why the sweep's `$0x3` was never the corpus's own constant.

---

# 8. The four guards the brief names

## 8.1 `model_translate.py check` — 259 / 172 / 87

**LITERAL**, lane `ap5_l17`
(`<runs>/ap5/agent/logs/*__ap5_l17_guard_check_and_the_handful_b.sh.log`):

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
definitions after the check: 4148
   the re-derived check, kept as autopoly5_check_L2_rerun.json: rows 259
      REFUSED      87
      STATED       172
   RESTORED IDENTICAL: every file check_command wrote is back to its stored bytes (178 files)

[2/2] the h2 handful: sources_counts
NOT_RENDERED 4
ONE_SIDE_REFUSED 4
SOURCE_UNCHANGED 24
identical to the file task h1 wrote under src: 24 of 24 rendered
```

**GLOSS.** The brief's tally exactly: 259 rows, 172 STATED, 87 REFUSED. The
stored `check_L2.json` reads 153 STATED and 19 DISCREPANCY because it carries a
Lean run's verdicts a fresh `check` cannot know; every one of the 178 files
`check_command` can write was copied aside before and restored byte for byte
after. This is the SECOND pass of the guard — it ran once before the
`align_by_row` branch was widened (lane `ap5_l9`, same tally) and again over
the code as this task finally leaves it.

## 8.2 Task o8's four totals — 243 / 197 / 155 / 216

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/o8_regression.py totals
rows             243
LANDED           197
byte identical   155
proved           216
```

**GLOSS.** Task o8's own numbers from log 220, unchanged: nothing this task did
to `answer_of`, `align_by_row`, `shapes_for` or the driver moved what the
renderers write for the same 243 terms. Lane `ap5_l18` is the run of record and
`ap5_l10` the first pass, with the same four totals.

## 8.3 The h2 handful — 24 of 24

**LITERAL**, lane `ap5_l17` §[2/2], the last two lines above:
`SOURCE_UNCHANGED 24` and
`identical to the file task h1 wrote under src: 24 of 24 rendered`. The 4
`NOT_RENDERED` and 4 `ONE_SIDE_REFUSED` beside them are outside the 24 rendered
pairs and are task h1's own.

## 8.4 Task t100's proved-edge count — 12 of 12, and the branch's reach

**LITERAL**, lane `ap5_l19`
(`<runs>/ap5/agent/logs/*__ap5_l19_guard_t100_edges_c.sh.log`):

```
   THE PROVED-EDGE COUNT the brief names, by every field of an
   edge that states one:
      edges whose `edge_applies` says proved: 12 of 12
      edges whose `both_terms_proved_against_own_body` says proved: 12 of 12
      edges whose `proved` says proved: 0 of 12
      edges whose `state` says proved: 0 of 12
      edges whose `runner_word` says proved: 0 of 12
   peak resident at section 1: 285572 kB

[2/3] the branch's reach over the whole pool
   distinct arrival families over every edge: 5
   they are: rcx, rdi, rsi, xmm0, xmm1
   family readings that are an x87 family: 0
   peak resident at section 2: 285572 kB

[3/3] the aligner re-run, edge for edge
   edges whose substitution is identical before and after: 12
   edges with no input row at all (nothing to substitute): 0
   edges whose substitution DIFFERS: 0
```

**GLOSS.** Three readings, not one. The count the brief names is unchanged at
12 of 12 by both fields of `pool100_edges.json` that state one (`edge_applies`
and `both_terms_proved_against_own_body`; the three fields that state nothing
about proving read 0 of 12 and are shown so the reading is not cherry-picked).
The new branch is UNREACHABLE for the whole pool — the five arrival families
over every edge are `rcx rdi rsi xmm0 xmm1` and none is an x87 family. And the
aligner re-run, edge for edge against a reference implementation of the two
lines the function had before this task (written inside the lane, labelled as
such, never in the shared file), gives an identical substitution on all 12 and
differs on none.

---

# 9. The tally, the store, the spelling guard, and memory

**LITERAL**, lane `ap5_l20` §[6/6]:

```
[6/6] the tally
runs recorded: 1012 of 1012

| target | attempted | rendered | compiled | LANDED | proved | sat | undecided | refused |
|---|---|---|---|---|---|---|---|---|
| c | 253 | 245 | 245 | 73 | 200 | 16 | 2 | 8 |
| rust | 253 | 209 | 209 | 69 | 164 | 14 | 3 | 44 |
| go | 253 | 200 | 200 | 27 | 178 | 16 | 6 | 53 |
| swift | 253 | 200 | 200 | 67 | 156 | 4 | 16 | 53 |

peak resident: 88036 kB
```

**LITERAL**, the store and the aggregate compared run for run, lane
`ap5_l20` §[3/6]:

```
[3/6] the store and the aggregate compared run for run
lines on the store: 1012
runs on the aggregate: 1012
run for run identical: 1012
distinct (cell, target) pairs: 1012
```

```
$ wc -l PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5_runs.jsonl
1012 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5_runs.jsonl
```

**THE SPELLING GUARD**, over every json this task wrote:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS autopoly5.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5_cells.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS autopoly5_cells.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5_check_L2_rerun.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS autopoly5_check_L2_rerun.json -- no operator token in any key, grouping, pairing or row structure
```

**NO EXEMPTION** anywhere in what this task wrote:

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.py || true
0
```

`grep -c exempt` over `lanes_ap5/*.sh` returns 2 on exactly two lanes,
`ap5_l12` and `ap5_l20`, and both hits are those lanes' OWN
`echo "[5/6] no exemption…"` and `grep -c exempt …` lines. Every other lane
returns 0, and so does `autopoly5.py` above.

**MEMORY.** Bound 6 GB resident on the one collecting process, named abort
`ABORT_MEMORY_AP5`, checked after every run. The sample of 20 ran first (lane
`ap5_l7`, peak 262,480 kB). The loop of record peaked at **2,423,324 kB** —
2.31 GB, 38.5% of the bound — and never aborted. The reporting lanes peaked at
88,276 kB (the aggregate), 114,992 kB (`immediate`) and 104,512 kB (`change`);
the guards at 285,572 kB (`ap5_l19`) and 82,712 kB (`ap5_l18`'s collector). No
lane hit a time or memory limit, so nothing is re-run for room.

**THE `sat` POPULATION AND THE RE-POSE**, for continuity with task ap4:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.py sat | grep -v counterexample | sed -n '1,12p'
sat at the plain comparison, every written place: 174
sat surviving the caller-extension re-pose: 65
   c      21
   go     18
   rust   20
   swift  6
the five surviving sat places with the most ledger rows:
   ucomiss    xmm_xmm      32    c      [flags] 2270 rows
   ucomiss    xmm_xmm      32    go     [flags] 2270 rows
   ucomiss    xmm_xmm      32    rust   [flags] 2270 rows
   ucomiss    xmm_xmm      32    swift  [flags] 2270 rows
   ucomisd    xmm_xmm      64    c      [flags.low] 1026 rows
```

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.py repose | sed -n '1,6p'
places UNDECIDED at the 3,000 ms ceiling of record and re-posed once at 30,000 ms: 38
   DISPROVED        1
   PROVED_ON_SHIP   3
   UNDECIDED        34

| cell | lang | place | route | ledger rows | the re-pose's answer |
```

---

# 9b. The conventions verifier, two passes

**LITERAL**, the summaries of lanes `ap5_l25` and `ap5_l27`, both
`python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20`
over this file:

| pass | lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|---|
| 1 | `ap5_l25` | 37 | 11 | **0** | 23 | 1 | 2 |
| 2 | `ap5_l27` | 37 | 14 | **0** | 23 | 0 | 0 |
| 3 | `ap5_l28` | 38 | 14 | **0** | 24 | 0 | 0 |

**GLOSS**, and the obligation the law states is the DIFFERS column: **0 on
both passes**. The first pass's one REFUSED and two NOT_RERUNNABLE were
defects in the pasted COMMAND and not in the claim, and each was fixed in the
command, never in the verifier: `awk 'NF>5'` reads to the verifier as a
redirection into a file named `5`, so the same tally is taken through `cut` on
the table's own pipes; `cd X && python3 Y` names `cd`, which is not a program
in the image, so the script is given its own full path; and the `imm_*` paste
carried `->` inside the table's cells, which the verifier reads as an arrow
gloss, so the range was cut to the three counts the brief asks for and Table I1
in full is attributed to its lane instead. Lane `ap5_l26` re-ran the three
rewritten commands and this log carries that output.

The 23 UNVERIFIABLE are 13 attributions (a fenced block whose lead-in names the
lane log it came from, carrying no command) and 10 prose paragraphs. They carry
nothing to re-run BY DESIGN — a lane's own log is not re-runnable from another
instance — and each names the tower path of the log it quotes, as §8's headings
do.

Pass 3 is this section itself measured: lane `ap5_l28` ran the verifier
again over the file WITH the table above in it, and the one extra claim
it counts (38, not 37) is this section's own paste, which is an
attribution. The only thing added after pass 3 is the `ap5_l28` row of
the table and this paragraph, and they carry no command.

---

# 10. The two lists

## Decided, recorded for audit

1. **The three shared-file changes the brief authorised were made and no
   others**, and the counterpart deletion in the driver was kept:
   `reference.answer_of` reads an `X87_<k>` home, `align_by_row` aligns both
   x87 spellings, `model_translate.shapes_for` spells a second symbolic row per
   `imm_*` shape, and `emulate.x87_answer_for_unit` — task ap4's stand-in for
   the first of those — is removed. The four guards the brief names pass at
   their stated tallies (§8).
2. **The `align_by_row` branch tests BOTH x87 spellings**, `X87_<k>` and
   `x87_<operand>`, because `emulate.X87_ARRIVAL` already holds both. The first
   draft tested one; the loop's own change table caught it; the branch was
   widened and the whole loop re-run (§3). The first pass's store is kept on
   disk beside the second and nothing was deleted.
3. **The C2 column header in `autopoly5.py` was corrected** from "ap4's cause"
   to "ap5's cause, which task ap4 did not have". The value printed there was
   always `cause_of` on task ap5's run; only the label was wrong. It is a label
   in this task's own artifact file, not in a shared file.
4. **No sixth pass was run.** The brief's stop rule is "zero regressions or
   STOP" and one regression stands, so the loop of record is lane `ap5_l16`'s
   and the cell is reported rather than patched (§4).
5. **Lanes `ap5_l17` to `ap5_l21` were submitted as the first implementer wrote
   them**, after being read against the state on disk; `ap5_l22`, `ap5_l23` and
   `ap5_l24` are new. `ap5_l11` and `ap5_l23` stay on the record with their own
   defects and were replaced by NEW names, never edited in place, per the
   standing rule of 2026-09-07.

## Awaiting the owner

1. **`sbb` imm_gpr 8 on swift is one regression and it is not fixed.** The
   record says the `@_cdecl` entry for the four-parameter rendering compiled to
   a five-byte tail-call thunk, so the carve holds a `jmp` and no arithmetic
   (§4). Whether the symbolic-immediate row should be preferred at a cell where
   the target's compiler answers with a thunk — or whether the carve should
   follow a `jmp` relocation into the mangled symbol — is a decision about the
   pipeline, not an implementation detail, and it is left here.
