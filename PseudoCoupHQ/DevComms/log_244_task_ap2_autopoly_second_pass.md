# log 244 — task ap2: AutoPoly's loop, second pass, after the mechanical causes task ap1 counted were fixed

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/`).
Line: arch_unit_oracle, the "goal" section of 2026-09-07 and the ruling of
2026-09-08 in
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`.
Date: 2026-09-09. Instance `ap2`, on the tower guest.

Artifact folder:
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`,
writing `autopoly2_*`; task ap1's products are not overwritten.
Lane scripts: `.../autopoly/lanes_ap2/`, sixteen of them, each kept in the
repo as the standing rule of 2026-09-07 requires. Every lane log named
below is on the TOWER (`<user>@<tower>`), under
`<runs>/ap2/agent/logs/`.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ`, mounted into the
instance. Every rendering is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself, quoted;
**GLOSS** is a plain-words reading beside a literal.

---

# 0. THE FIRST THING, before any result: the law was not staged

The brief's first line is `Law: LAW.md beside this file, ALL of it
including the tower section`, and there is no `LAW.md` — not in the
scratchpad the brief names, not anywhere on either machine. Nor is
`task_ap1_brief.md`, which the brief names second. Only
`task_ap2_brief.md` was staged.

**What was done instead, said out loud so it is not mistaken for the law
itself.** The rules this task ran under were taken from the three standing
sources that carry them, and no rule was invented to fill a gap:

| what the brief calls for | where it was read from |
|---|---|
| the standing rules, including the tower, the memory bound, the flag rule on a limit, the verifier and the spelling ban | `PRIVATE/PseudoCoupHQ/DevComms/note_server_session_start_here.md` §2, whose own heading is "The standing rules. These bind every session on this line" |
| the project's settled rules and the two-list report shape | `PRIVATE/PseudoCoupHQ/CLAUDE.md` |
| what task ap1 did, its loop, its by-cause table and its awaiting-the owner list | `PRIVATE/PseudoCoupHQ/DevComms/log_243_task_ap1_autopoly_first_full_loop.md` |
| the exact tower commands | `PUBLIC/Airlock/remote_lane.sh`'s own usage block |

The one thing that could not be reconstructed is whatever `LAW.md` says
under "stop rules", which the brief's §4 refers to by name. Nothing in
this task stopped, so no stop rule was reached; but that is luck, not
compliance, and it is the first item of the awaiting-the owner list.

---

# 1. What was done

Task ap1 proved 120 of 253 cells on all four compiled targets — 57.6% of
the attested ledger rows — and 445 of its 1,012 runs carried a cause
(log_243 §6). This task fixed the six mechanical causes the brief names,
one cause = one fix in the layer that owns it, measured each fix on
exactly the pairs it targets BEFORE the loop, and then re-ran the whole
loop.

**THE ANSWER: 144 cells on all four targets, 85,368 attested ledger rows,
64.17%** — up from 120 / 76,634 / 57.6%. Runs carrying a cause: 324 of
1,012, down from 445. **Runs task ap1 proved and this loop does not: 0.**

Two of the six fixes did not move their population, and both are findings
rather than failures:

- **Fix 2 moved 0 of its 128 runs, and the census is right to name no
  setter.** The brief reads the cause as "a flag consumer whose cell
  records no setter". The 32 cells it actually covers are the x87
  arithmetic and compare mnemonics (`faddl`, `fdivp`, `fucomi` and their
  like) at `key_width` 80. None of them is a flag CONSUMER in the corpus
  at all: the corpus's own flag-pair ledger rows name 25 consumers and
  every one is a `set*` or a `cmov*`. So the census answers None and, by
  the brief's own rule, the cause stands. §5.
- **Fix 1's first form moved 0 and its second moved 72**, because the
  memory symbol is 128 bits wide and not the operand's width. §4.

---

# 2. The lanes

| lane | what it did | log, on the tower |
|---|---|---|
| `ap2_l1_reference_and_table.sh` | fix 5's three registrations, through the reference itself; then `model_translate.py check`, which stopped on a defect that is not this task's | `...170123Z` |
| `ap2_l2_table_and_check_L2.sh` | `check_L2` guarded off the stored artifact instead, and fix 4 over the whole 71,778-row table | `...170518Z` |
| `ap2_l3_regenerate_the_table.sh` | the table's rows regenerated for the cells fix 4 moves, and `model_table.py assemble` re-run | `...171450Z` |
| `ap2_l4_cells.sh` | the outer set, and the SETTER CENSUS fix 2 reads | `...171622Z` |
| `ap2_l5_driver_guards.sh` | the four guards on the driver fixes | `...171909Z` |
| `ap2_l6_measure_the_fixes.sh` | the first measurement pass; two defects in the MEASUREMENT, not in a fix | `...172000Z` |
| `ap2_l7_probe_fix2.sh` | why fix 2 moves nothing: the 32 cells and what the census holds | `...172200Z` |
| `ap2_l8_measure_the_fixes_again.sh` | the second measurement pass | `...172338Z` |
| `ap2_l9_probe_fix1.sh` | what the 134 runs of fix 1's cause actually read | `...172648Z` |
| `ap2_l10_measure_the_fixes_final.sh` | **THE MEASUREMENT OF RECORD**: the six fixes on the pairs they target | `...172810Z` |
| `ap2_l11_guards_and_sample.sh` | the four guards again, against the driver as it now stands, and the twenty-run sample | `...173221Z` |
| `ap2_l12_run.sh` | **THE LOOP**: 992 runs in 1,345 s | `...173323Z` |
| `ap2_l13_aggregate_and_report.sh` | the aggregate, the report, the store check, the spelling guard | `...175653Z` |
| `ap2_l14_claims.sh` | the claims of this log, first pass | `...175726Z` |
| `ap2_l15_claims2.sh` | second pass; it ran an older copy of `autopoly2.py` than the one on this machine | `...175948Z` |
| `ap2_l16_claims3.sh` | **THE CLAIMS OF RECORD** | `...180041Z` |

---

# 3. The six fixes, each measured on the pairs it targets, before the loop

`autopoly2.py measure <a substring of the cause>` reads task ap1's own
store, takes exactly the (cell, target) pairs whose cause holds that
substring, runs each again through the driver as this task leaves it, and
prints the cause before and after. It writes nothing.

**LITERAL**, lane `ap2_l10_measure_the_fixes_final.sh`, on the tower at
`<runs>/ap2/agent/logs/20260909T172810Z__ap2_l10_measure_the_fixes_final.sh.log`,
the summary line of each of its eight measurements:

```
===== FIX 1: a term that reads state that is not an arrival register =====
task ap1's own runs carrying a cause holding 'not an arrival register': 134
     66  PROVED: proved
     46  term reads state that is not an arrival register
     13  the gate answered sat: the body holds on a region, not on every input
      6  PROVED: proved under caller extension
      3  the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either
===== FIX 2: no setter row to compose the flag pair from =====
task ap1's own runs carrying a cause holding 'no setter row to compose': 128
    128  no setter row to compose the flag pair from: None at width 8
===== FIX 3a: the whole-register vector cell with no lane to project =====
task ap1's own runs carrying a cause holding 'so there is no lane to project': 56
     40  vector arrival used beyond its low lane
     13  PROVED: proved
      3  the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either
===== FIX 3b: the 128-bit place go and swift have no holder for =====
task ap1's own runs carrying a cause holding 'has no holder for': 30
     18  a width c has no holder for
      5  PROVED: proved
      3  the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either
      2  term reads state that is not an arrival register
      2  the gate answered sat: the body holds on a region, not on every input
===== FIX 4: the six cells whose key_width was null =====
task ap1's own runs carrying a cause holding 'a real number is required': 24
      8  PROVED: proved
      8  PROVED: proved under caller extension
      4  the gate answered sat: the body holds on a region, not on every input
      4  the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either
===== FIX 5a: cmovg =====
      7  PROVED: proved
===== FIX 5b: movswq =====
      1  PROVED: proved
      1  PROVED: undecided
===== FIX 5c: the lea form with no base register =====
      6  PROVED: proved
```

**GLOSS**, fix by fix, with where each lives.

| fix | where it lives | pairs it targets | of those, proved after |
|---|---|---|---|
| 1 — a memory operand is an arriving value | driver, `handful.memory_as_arrivals` and `families_of` | 134 | 72 |
| 2 — the setter taken from the corpus's own flag-pair rows | driver, `handful.setter_from_the_corpus`, reading the census | 128 | 0 (§5) |
| 3 — a 128-bit place is two 64-bit places | driver, `handful.in_halves_where_it_must_be` | 56 + 30 | 13 + 5 |
| 4 — a widening move's key width is its destination width | table, `model_table.key_width` | 24 | 16 |
| 5 — three additive registrations | `reference.py` | 7 + 2 + 6 | 7 + 1 + 6 |
| 6 — task h2's normalise-before-render, ungated | driver, `handful.renderer_input` | — (§6) | — |

---

# 4. Fix 1, and the second look it needed

**THE FIRST FORM MOVED NOTHING.** `reference.memory_symbol_name` writes
`seed_MEM_<the mangled operand text>`, and the first form of the fix
grew such a symbol to an arrival's 64 bits where it was narrower. Lane
`ap2_l8` measured it on the 134 pairs and not one moved, so lane
`ap2_l9` asked the objects what they hold.

**LITERAL**, lane `ap2_l9_probe_fix1.sh`, on the tower at
`<runs>/ap2/agent/logs/20260909T172648Z__ap2_l9_probe_fix1.sh.log`:

```
task ap1's runs with that cause: 134

the symbol each of task ap1's refusals names:
    104  seed_MEM__rsi_
     24  x87__rsi_
      6  no answer home

| cell | place | bits | families now | refusal now | free symbols of the term |
|---|---|---|---|---|---|
| `addsd` mem_xmm 64 | reg_xmm0 | 128 | None | seed_MEM__rsi_ is 128 bits, and an arriving value is 64 | seed_MEM__rsi_:BitVec(128) seed_xmm0:BitVec(128) |
| `cmp` mem_gpr 64 | flags.low | 64 | None | seed_MEM__rsi_ is 128 bits, and an arriving value is 64 | seed_MEM__rsi_:BitVec(128) |
| `fildl` mem_one 80 | x87_7.low | 64 | None | x87__rsi_ | x87__rsi_:FPSort(15, 64) |
```

**GLOSS.** The cause is three populations, not one. **104 runs** name
`seed_MEM__rsi_`, and the reference gives a memory operand ONE symbol per
operand text as wide as the widest thing that operand could hold — 128
bits, so that a vector load and a general load name the same cell. A cell
that loads from memory into a lane reads only its low bits: `cmp mem_gpr
64` reads bits 63..0, `addss mem_xmm 32` reads bits 31..0. **24 runs**
name an x87 stack position, which is not a memory operand and is not this
fix's. **6 runs** have no answer home at all — the cell writes memory.

**THE SECOND FORM.** Where every use of the symbol lies inside its low 64
bits — asked of `emulate.Renderer.collect_uses`, the same walker
`plan_parameters` uses, rather than restated — the symbol is replaced by a
64-bit arrival grown back to its own width, which `z3.simplify` cuts away
again at each use. Where a use reaches above bit 63 the symbol is left
exactly as it is and the cause stands: a whole 128-bit memory cell is not
an arriving value, for the same reason a whole 128-bit vector register is
not. 72 of the 134 then prove; 46 still carry the cause (the x87
positions, the memory writes, and the wide reads).

---

# 5. Fix 2, and why the corpus is right to name no setter

**LITERAL**, lane `ap2_l7_probe_fix2.sh`, on the tower at
`<runs>/ap2/agent/logs/20260909T172200Z__ap2_l7_probe_fix2.sh.log`,
its head and six of its 32 rows:

```
it holds a setter_census: True
consumers in the census: 25 -- ['cmovae', 'cmovb', 'cmovbe', 'cmove', 'cmovge', 'cmovl', 'cmovle', 'cmovne', 'cmovns', 'cmovs', 'seta', 'setae', 'setb', 'setbe', 'sete', 'setg', 'setge', 'setl', 'setle', 'setne', 'setnp', 'setns', 'seto', 'setp', 'sets']

task ap1's runs with that cause: 128
distinct cells: 32

| cell | in the census | the census's own top setter | the chosen row's flags_in | preseeded | TRANSLATED rows |
|---|---|---|---|---|---|
| `faddl` mem_one 80 | False | -- | None | True | 4 |
| `fdivp` st_st 80 | False | -- | None | True | 4 |
| `fimull` mem_one 80 | False | -- | None | True | 4 |
| `fsubrp` st_st 80 | False | -- | None | True | 4 |
| `fucomi` st_st 80 | False | -- | None | True | 4 |
| `fucomip` st_st 80 | False | -- | None | True | 4 |
```

**GLOSS.** All 32 cells are x87 mnemonics at `key_width` 80. The sweep
seeded each one a flag state, so the row reads `seed_FLAG_L` and
`seed_FLAG_R` and the driver must compose a pair; but the corpus never
recorded any of them as the reading half of a flag pair, so there is no
setter to compose with. The census the fix reads is built from exactly
the rows m1b's attestation pass walked (22,741 of them,
`counts.flag_consumer_rows`), and it names 25 consumers, every one a
`set*` or a `cmov*`. The brief's own rule is "if none exists, the cause
stands", and it stands. **No setter was invented for them**, and it is
worth saying what would have been wrong with inventing one: the composed
function would then be an emulation of a pair the corpus never produced,
and its verdict would be about nothing.

The fix is not idle: it is in the driver, it fires wherever a flag
consumer's own cell names no setter and the corpus names one, and the
population where that is true is empty today. Guard 4 of §7 shows it is
not reached at all on `cmovne` and `setne`, whose own attestation names
`test`.

---

# 6. Fix 6, and what the guard could and could not measure

`handful.renderer_input` chose the term the renderer walks by task name —
`how in ("h2", "g1")` — so `g1b`, `g1c` and the whole of task ap1's loop
fell through to task h1's form. That is item 3 of log_243's awaiting-the owner
list. It is now ungated: the one name left is `h1`, and it is not a gate
on the running task but the selector `sources_command` and
`proved_the_same` pass EXPLICITLY to measure what the fix changes.

**LITERAL**, lane `ap2_l11_guards_and_sample.sh`, on the tower at
`<runs>/ap2/agent/logs/20260909T173221Z__ap2_l11_guards_and_sample.sh.log`:

```
[3/4] which form of the term each task's setting hands the renderer
the probe term, LITERAL: (concat ((_ extract 31 0) (bvmul seed_rdi seed_rax))
        ((_ extract 63 32) (bvadd seed_rsi seed_rdi)))
   order_commutative(simplify(it)): (concat (bvmul ((_ extract 31 0) seed_rax) ((_ extract 31 0) seed_rdi))
        ((_ extract 63 32) (bvadd seed_rdi seed_rsi)))
   the normalised term:             (concat (bvmul ((_ extract 31 0) seed_rax) ((_ extract 31 0) seed_rdi))
        ((_ extract 63 32) (bvadd seed_rdi seed_rsi)))

TASK ap2  fixes_are_on True  primitive_first True  setup_is_allowed True  -> BOTH FORMS AGREE ON THE PROBE
```

**GLOSS, and it is a limit of the measurement rather than a result.** The
two forms print the same term on the probe, so which branch a task takes
is not observable on it. That is consistent with task h2's own finding —
the fix was a no-op on all 24 of its places, and is again on all 24 here
(§7, guard 1) — but it means this column proves the branch for no task.
What the fix changes on 1,012 runs is not separated out by this loop
either, because every other fix moved at the same time. Whether task h2's
fix 1 is a no-op on this population is still unmeasured, and it stays on
the awaiting-the owner list.

---

# 7. The guards

**LITERAL**, lane `ap2_l11_guards_and_sample.sh`, on the tower at
`<runs>/ap2/agent/logs/20260909T173221Z__ap2_l11_guards_and_sample.sh.log`:

```
[1/4] GUARD 1 -- task h2's own sources measurement
SOURCE_UNCHANGED 24
identical to the file task h1 wrote under src: 24 of 24 rendered
[2/4] GUARD 2, 3 and 4 -- the handful's ten cells through the ap2 driver
   GUARD 2: places of the handful's ten cells that come out IDENTICAL (name, width, layer-5 text, arrival families): 14
   places that DIFFER: 0
   places task ap2 produces that task g1b's product has no row for: 0  []
   GUARD 3: the vector places of the handful, and whether task ap2's fix 3 touched them
      addss     xmm_xmm   32   reg_xmm0   bits 128  halved: None
      cvtsi2sd  gpr_xmm   64   reg_xmm0   bits 128  halved: None
   GUARD 4: the setter each flag-reading cell of the handful composes with, and the reason the driver gives
      cmovne    gpr_gpr   32   setter test     why: the setter this cell's own attestation records the most ledger rows for
      setne     gpr_one   8    setter test     why: the setter this cell's own attestation records the most ledger rows for
```

**GLOSS.** The four fixes that live in `handful.py` are UNGATED — none is
switched on by a task name, and `handful.use_task_ap2`'s docstring says
why: gating them is what let task h2's fix 1 fall out from under three
later tasks. So every guard asks the same question, and all four answer
it. Task h2's 24 sources are unchanged (guard 1, the brief's own guard on
fix 6). The handful's 14 places come out of the driver identical in name,
width, layer-5 text and arrival families to what task g1b's own product
records (guard 2, the brief's guard on fixes 1, 2 and 3). The four vector
cells still take task h2's lane projection and fix 3 does not touch them
(guard 3). `cmovne` and `setne` compose with the setter their own
attestation names and the corpus census is never reached (guard 4).

**THE TABLE'S OWN GUARD**, fix 4. **LITERAL**, lane
`ap2_l3_regenerate_the_table.sh`, on the tower at
`<runs>/ap2/agent/logs/20260909T171450Z__ap2_l3_regenerate_the_table.sh.log`:

```
   BEFORE, the table's own counts:
      attested_cells                           257
      attested_cells_placed                    253
      corpus_mnemonics                         162
      mnemonics_with_a_placed_cell             134
      rows_translated                          36903
      sweep_attempts                           71778
      table_mnemonics                          171
      translated_triples                       6218
   BEFORE, rows carrying an attestation: 1215 of 71778
   BEFORE, the outer set: 253 cells, 133044 attested ledger rows, 8 with a null key_width
   model_table_rows.json: 426 of 71778 rows moved
   model_table_attest.json: 8 of 257 cells moved
   AFTER, the table's own counts:
      attested_cells                           257
      attested_cells_placed                    253
      corpus_mnemonics                         162
      mnemonics_with_a_placed_cell             134
      rows_translated                          36903
      sweep_attempts                           71778
      table_mnemonics                          173
      translated_triples                       5912
   AFTER, rows carrying an attestation: 1218 of 71778
   AFTER, the outer set: 253 cells, 133044 attested ledger rows, 0 with a null key_width
```

**GLOSS.** Task m1b's coverage totals are unchanged — 257 attested cells,
253 placed, 162 corpus mnemonics, 134 with a placed cell, 36,903
TRANSLATED rows over 71,778 sweep attempts — and the outer set is the same
253 cells over the same 133,044 attested ledger rows. Three things moved
and each is one of this task's two changes: `table_mnemonics` 171 to 173
(fix 5's two registrations), `translated_triples` 6,218 to 5,912 (a
widening move's rows at four sweep widths now key under one), and the
attested rows 1,215 to 1,218 (the eight cells that carried a null key
now join). **Eight cells carried a null `key_width` and none does now.**
The three files as they stood are beside them with the suffix
`.before_ap2`.

**THE REFERENCE'S OWN GUARD**, fix 5, and a defect that is not this
task's. The brief asks for `check_L2`'s tally unchanged. It cannot be
re-derived: `model_translate.py check` stops on `KeyError: 'mnemonic'` in
`load_rows`, which is the first of the four items task m1b left for the
coordinator in log_237 §14 — the file still reads task o2's artifact by
the field name task mn1 renamed to `mnem`. So the guard was taken the only
way that is honest.

**LITERAL**, lane `ap2_l2_table_and_check_L2.sh`, on the tower at
`<runs>/ap2/agent/logs/20260909T170518Z__ap2_l2_table_and_check_L2.sh.log`:

```
   check_L2.json rows: 259
      DISCREPANCY 19
      REFUSED    87
      STATED     153
   rows of the population check_L2 is built over: 259
   distinct mnemonics it spells: 26
      does it spell cmovg    ? False
      does it spell movswq   ? False
   lea operand forms in that population: 12
      of them with an EMPTY BASE SLOT, the form this task's change reaches: []
```

**GLOSS.** The stored tally is 259 rows, 87 REFUSED, and 153 STATED plus
19 DISCREPANCY — which is the 172 the node's PROGRESS records, 19 of them
having come back DISCREPANCY from the Lean run itself. The artifact was
read and never rewritten. And the population it is built over spells
neither `cmovg` nor `movswq`, and carries no `lea` form with an empty base
slot, so neither reference change can reach a row of it.

---

# 8. THE table: per target, what the loop reached

**LITERAL**, lane `ap2_l16_claims3.sh`, on the tower at
`<runs>/ap2/agent/logs/20260909T180041Z__ap2_l16_claims3.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly2.py tables
## 1. THE table: per target, what the loop reached

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.

| step or verdict | c | rust | go | swift |
|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 199 cells, 122994 rows, 92.45% | 199 cells, 122994 rows, 92.45% | 190 cells, 118618 rows, 89.16% | 190 cells, 118618 rows, 89.16% |
| `compiled` | 199 cells, 122994 rows, 92.45% | 199 cells, 122994 rows, 92.45% | 190 cells, 118618 rows, 89.16% | 190 cells, 118618 rows, 89.16% |
| `LANDED` | 75 cells, 40302 rows, 30.29% | 72 cells, 39199 rows, 29.46% | 30 cells, 22970 rows, 17.26% | 70 cells, 38915 rows, 29.25% |
| `LANDED_ELSEWHERE` | 16 cells, 11111 rows, 8.35% | 17 cells, 11855 rows, 8.91% | 10 cells, 5418 rows, 4.07% | 29 cells, 18684 rows, 14.04% |
| `NOT_COLLAPSED` | 108 cells, 71581 rows, 53.8% | 110 cells, 71940 rows, 54.07% | 150 cells, 90230 rows, 67.82% | 91 cells, 61019 rows, 45.86% |
| `proved` | 156 cells, 89468 rows, 67.25% | 159 cells, 94617 rows, 71.12% | 160 cells, 97840 rows, 73.54% | 152 cells, 87836 rows, 66.02% |
| `proved under caller extension` | 20 cells, 20530 rows, 15.43% | 21 cells, 21502 rows, 16.16% | 0 cells, 0 rows, 0.0% | 17 cells, 19778 rows, 14.87% |
| `sat` | 15 cells, 4228 rows, 3.18% | 14 cells, 5069 rows, 3.81% | 16 cells, 5157 rows, 3.88% | 5 cells, 3723 rows, 2.8% |
| `undecided` | 8 cells, 8768 rows, 6.59% | 5 cells, 1806 rows, 1.36% | 14 cells, 15621 rows, 11.74% | 16 cells, 7281 rows, 5.47% |
| `refused` | 54 cells, 10050 rows, 7.55% | 54 cells, 10050 rows, 7.55% | 63 cells, 14426 rows, 10.84% | 63 cells, 14426 rows, 10.84% |

## 2. Per target, how far the primitive route reached

Table 2 -- `primitive` is a target operator whose whole lowered body IS the cell; `primitive+setup` is that plus zero-operand accumulator setup (task g1c's widened lookup); `term` is the cell's own term written in the target's operators, which is the fallback.

| route | c | rust | go | swift |
|---|---|---|---|---|
| `primitive` | 29 cells, 19706 rows, 14.81% | 22 cells, 12245 rows, 9.2% | 17 cells, 10351 rows, 7.78% | 9 cells, 7774 rows, 5.84% |
| `primitive+setup` | 2 cells, 1726 rows, 1.3% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |
| `term` | 190 cells, 110041 rows, 82.71% | 199 cells, 119228 rows, 89.62% | 204 cells, 121122 rows, 91.04% | 212 cells, 123699 rows, 92.98% |
| `no route reached` | 32 cells, 1571 rows, 1.18% | 32 cells, 1571 rows, 1.18% | 32 cells, 1571 rows, 1.18% | 32 cells, 1571 rows, 1.18% |

Table 3 -- a cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 4 of 4 | 144 | 85368 | 64.17% |
| 3 of 4 | 29 | 27938 | 21.0% |
| 2 of 4 | 8 | 3081 | 2.32% |
| 1 of 4 | 6 | 123 | 0.09% |
| 0 of 4 | 66 | 16534 | 12.43% |

`sat` at the plain comparison, every written place: 154
`sat` surviving the caller-extension re-pose: 69
the handful's forty pairs: 32 agree character for character, 36 agree on the verdict, 4 not in this outer set
```

**GLOSS**, and two readings the table does not make on its own.

- **THE POLYFILL-COMPLETE SET IS 144 CELLS, 85,368 attested ledger rows,
  64.17%**, against task ap1's 120 / 76,634 / 57.6%. Proved on none fell
  from 96 cells / 27,011 rows / 20.3% to 66 / 16,534 / 12.43%.
- **A CELL PROVED ON A TARGET IS EVERY HALF OF ITS DESTINATION REGISTER
  PROVED.** Fix 3 splits a 128-bit place into two written places, so
  `destination_place` — which answers with the first place that is not the
  flags — would answer `reg_xmm0.low` and a table built on it alone would
  call a cell proved when only its low 64 bits were. `autopoly2.the_places`
  returns every place of the destination register and every reading of it
  is the WEAKEST of them: `outcome_of`, `landing_of` and `reached` all go
  through it. That is where the fix could have been counted rather than
  measured, and it is written down there.
- `rendered` and `compiled` are still the same number on every target.
  Nothing this loop rendered failed to compile.

---

# 9. The change table

**LITERAL**, lane `ap2_l16_claims3.sh`, on the tower at
`<runs>/ap2/agent/logs/20260909T180041Z__ap2_l16_claims3.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly2.py change | sed -n '1,24p'
runs on task ap1's store: 1012
runs on task ap2's store: 1012
pairs on both: 1012

Table C1 -- every cause of task ap1's loop, what it counted then, and what those same runs say now.

| task ap1's cause | ap1 runs | ap2 runs, same cause | where the rest went |
|---|---|---|---|
| PROVED | 567 | 567 | -- |
| term reads state that is not an arrival register | 134 | 46 | 72 PROVED; 13 the gate answered sat: the body holds on a region, not on every input; 3 the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| no setter row to compose the flag pair from: None at width 8 | 128 | 128 | -- |
| the cell's own key_width is not narrower than the place, so there is no lane to project | 56 | 0 | 40 vector arrival used beyond its low lane; 13 PROVED; 3 the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| the gate answered sat: the body holds on a region, not on every input | 31 | 30 | 1 the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| a width c has no holder for | 30 | 18 | 5 PROVED; 3 the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either; 2 term reads state that is not an arrival register; 2 the gate answered sat: the body holds on a region, not on every input |
| the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | 24 | 0 | 16 PROVED; 4 the gate answered sat: the body holds on a region, not on every input; 4 the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 11 | 10 | 1 the gate answered sat: the body holds on a region, not on every input |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 10 | 10 | -- |
| the gate did not answer: the carved body: the reference: arch opcode 'cmovg' has no entry in the opcode table -- no body in the corpus this table was built over spells it; and no term either | 7 | 0 | 7 PROVED |
| the gate did not answer: the carved body: the reference: lea addressing form '0x0(,%rdi,8)' is not the (displacement, base, index, scale) shape this file models; and no term either | 6 | 0 | 6 PROVED |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | 2 | 2 | -- |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | 2 | 2 | -- |
| the gate did not answer: the carved body: the reference: arch opcode 'movswq' has no entry in the opcode table -- no body in the corpus this table was built over spells it; and no term either | 2 | 0 | 2 PROVED |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows | 1 | 1 | -- |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 1 | -- |
```

The two counts tables C2 and C3 end with, the whole of each table being
section 3 of `autopoly2.md`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly2.py change | grep -E '^runs task ap1 proved|^pairs that moved to'
runs task ap1 proved and task ap2 does not: 0
pairs that moved to `sat`: 20
```

**GLOSS.** All 1,012 pairs join, and the join is on THIS loop's own triple
for both stores: fix 4 moved eight cells' `key_width` off null, so joining
on the stored triple alone would have left 32 pairs unmatched and counted
a fix as having removed the runs it fixed. **Every one of task ap1's 567
proved runs is proved again, and the regression list is empty.**

**THE 20 PAIRS THAT MOVED TO `sat` ARE A FINDING, and the regions they
name are two.** Eleven are the float comparison against NaN, now reached
on the memory-operand shapes as well (`ucomiss` mem_xmm 32 on all four
targets, `ucomisd` mem_xmm 64 on three, `ucomisd` xmm_xmm 64 on go and
swift): the same region task ap1 banked, with the same caveat — z3's model
of `fp.to_ieee_bv` is uninterpreted there, so the counterexample names the
region and does not by itself establish that the target differs at that
point. Four are the compare-mask cells on go (`cmpeqsd`, `cmpeqss`,
`cmpneqsd`, `cmpneqss` mem_xmm), whose counterexample is `IN_0 = 0, IN_1 =
0` — the equal-inputs point, which is where a compare mask's answer is
all-ones and go's own comparison answers a boolean. Two are the widening
moves the key-width fix reached (`movsbl` and `movswl` widen_gpr_gpr 32 on
c and rust), whose counterexample is a negative source: `IN_0 =
4294967040` is `0xFFFFFF00`, the sign-extension edge. The rest are the
divide at 16 bits and two float subtractions on go.

---

# 10. Every `sat`, and what the one re-pose moved

**LITERAL**, same lane:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly2.py sat | grep -v counterexample
sat at the plain comparison, every written place: 154
sat surviving the caller-extension re-pose: 69
   c      21
   go     19
   rust   21
   swift  8
the five surviving sat places with the most ledger rows:
   ucomiss    xmm_xmm      32    c      [flags] 2270 rows
   ucomiss    xmm_xmm      32    go     [flags] 2270 rows
   ucomiss    xmm_xmm      32    rust   [flags] 2270 rows
   ucomiss    xmm_xmm      32    swift  [flags] 2270 rows
   ucomisd    xmm_xmm      64    c      [flags.low] 1026 rows
```

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly2.py repose
places UNDECIDED at the 3,000 ms ceiling of record and re-posed once at 30,000 ms: 109
   DISPROVED        1
   PROVED_ON_SHIP   3
   UNDECIDED        105

| cell | lang | place | route | ledger rows | the re-pose's answer |
|---|---|---|---|---|---|
| `div` gpr_one 8 | go | reg_rax | term | 28 | PROVED_ON_SHIP |
| `div` gpr_one 8 | swift | reg_rax | term | 28 | PROVED_ON_SHIP |
| `idiv` gpr_one 16 | rust | reg_rax | term | 16 | DISPROVED |
| `idiv` gpr_one 8 | go | reg_rax | term | 8 | PROVED_ON_SHIP |
```

**GLOSS.** `sat` at the plain comparison rose from 110 places to 154 and
the survivors from 39 to 69, because 62 more cells reach the gate at all.
The verdict of record stays the 3,000 ms one; 109 places were re-posed at
30,000 ms and four moved, all four on a divide, together carrying 80
ledger rows of 133,044. The `[flags.low]` in the fifth row is fix 3's
halving: `ucomisd`'s flags place is 128 bits and is now two comparisons.

---

# 11. Causes, and the arrival-contract group

**LITERAL**, same lane:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly2.py causes
Table 5 -- what did not work, by cause, the four targets summed. `rows` counts a cell's attested ledger rows once per run, so a cause seen on all four targets counts them four times.

| cause | runs | ledger rows | targets |
|---|---|---|---|
| no setter row to compose the flag pair from: None at width 8 | 128 | 6284 | c, go, rust, swift |
| the gate answered sat: the body holds on a region, not on every input | 50 | 18177 | c, go, rust, swift |
| term reads state that is not an arrival register | 48 | 28316 | c, go, rust, swift |
| vector arrival used beyond its low lane | 40 | 5600 | c, go, rust, swift |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 23 | 21212 | c, go, rust, swift |
| a width c has no holder for | 18 | 8752 | go, swift |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 11 | 3820 | c, go, rust, swift |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | 2 | 840 | c |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | 2 | 1726 | c |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows | 1 | 5190 | c |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 | c |

runs carrying a cause: 324 of 1012

THE ARRIVAL-CONTRACT GROUP, counted on its own: every gate call that declined because the two sides name a different number of arriving values.

places the gate declined on the IN-row alignment: 38
   17 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows
   12 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 2 IN rows
   5 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows
   4 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows

| cell | route | ledger rows |
|---|---|---|
| `xor` gpr_same 32 | primitive | 5190 |
| `or` gpr_gpr 64 | primitive | 2654 |
| `xor` gpr_gpr 64 | primitive | 1668 |
| `idiv` gpr_one 64 | primitive+setup | 948 |
| `mov` imm_gpr 32 | primitive | 835 |
| `and` gpr_gpr 64 | primitive | 809 |
| `idiv` gpr_one 32 | primitive+setup | 778 |
| `add` gpr_gpr 64 | primitive | 744 |
| `imul` gpr_gpr 64 | primitive | 608 |
| `sub` gpr_gpr 64 | primitive | 577 |
| `neg` gpr_one 64 | primitive | 43 |
| `mov` imm_gpr 8 | primitive | 5 |
```

**GLOSS.** Eleven causes rather than fifteen, and 324 runs rather than
445. Two are new names and both are the honest edge of fix 3: `vector
arrival used beyond its low lane` (40 runs) is the HIGH half of a
whole-register vector place, which reads bits 127..64 of an arriving xmm
register that no target can receive as a parameter — the low half of the
same cells is what the 13 proved runs of §3 are; and `a width c has no
holder for` at 18 runs is what remains after halving, where the half's own
term still carries a 128-bit operation inside it.

**THE ARRIVAL-CONTRACT GROUP GREW, and nothing about the gate was
touched.** It is 38 places over 12 cells where task ap1 had 7 over 5. The
group is not this task's to answer — it is the ruling task g1b asked for
and log_243's first awaiting-the owner item — and the reason it grew is that
fix 3 puts more PLACES in front of the gate: the flags place of a 64-bit
binary operation on the primitive route is 128 bits, and its two halves
are now two gate calls that each decline on the same structural mismatch
they would have declined on before, had they got that far. At the
DESTINATION place, which is what Table 1 counts, the group is the same 5
runs on c that task ap1 recorded. The question is unchanged and it is
unchanged in kind: an operator's operand list and an opcode's arrival
contract are two different things, and where they differ the gate declines
rather than answers.

---

# 12. Memory

The bound stated in `PUBLIC/Airlock/instances/ap2.conf`, in every
lane header and in `autopoly2.py`'s own constants is 6 GB resident on the
one collecting process, named abort `ABORT_MEMORY_AP2`, checked after
every run. The sample the law asks for is the first twenty runs, printed
with the peak after each; twenty runs took 18 s and the peak was 261,272
kB. The peaks:

| lane | what it read | peak resident |
|---|---|---|
| `ap2_l2_table_and_check_L2.sh` | `model_table.json`, 73 MB | 333,796 kB |
| `ap2_l3_regenerate_the_table.sh` | rows, attest and the assembled table | 289,688 kB |
| `ap2_l4_cells.sh` | `model_table.json` and the attestation | 290,048 kB |
| `ap2_l10_measure_the_fixes_final.sh` | the two reads, then 388 pairs re-run | 261,756 kB |
| `ap2_l11_guards_and_sample.sh` | the two reads, then 20 runs | 261,272 kB |
| `ap2_l12_run.sh` | the two reads, then 992 runs | 1,450,280 kB |
| `ap2_l13_aggregate_and_report.sh` | the whole 1,012-run store | 86,520 kB |

The high-water mark, 1,450,280 kB, is 24% of the bound. No abort fired.
Task ap1's own run lane ended at 2,414,988 kB over the same run count; the
difference is not a claim about this task's code, since the two lanes ran
different amounts of z3 work, and it is left as the measurement it is.

---

# 13. The deliverables

Under
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`:

| file | what it is |
|---|---|
| `autopoly2.py` | the loop, the bookkeeping, the aggregate, the report, the per-fix measurement and the change table |
| `autopoly2_cells.json` | the 253 attested cells, in run order, with the setter census |
| `autopoly2_runs.jsonl` | the incremental store, 1,012 lines |
| `autopoly2.json` | the aggregate |
| `autopoly2.md` | the report, 541 lines |
| `src2/` | the rendered sources, one per place that reached the render step |
| `lanes_ap2/` | the sixteen lane scripts |

Changed outside that folder, and only the three the brief authorises:

| file | the change |
|---|---|
| `Research/op_pipeline/reference.py` | `EMULATION_MNEMONICS` / `KEPT_MNEMONICS` (`cmovg`, `movswq`); `LEA_RE`'s base slot optional and `build_lea` reading an absent base as zero |
| `Research/oracle/arch_opcodes/model/model_table.py` | `widening_move_widths()` and one more case in `key_width` |
| `Research/oracle/cross_construction/emulation/handful/handful.py` | the four driver fixes and `use_task_ap2` |

Regenerated: `model_table.json`, `model_table_rows.json`,
`model_table_attest.json`, each with a `.before_ap2` copy beside it.

---

# 14. The conventions verifier over this log

Three passes, each a lane of this task's own instance, each over this log
as it then stood.

| pass | lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|---|
| first | `ap2_l17_verify_244.sh` | 19 | 2 | **3** | 14 | 0 | 0 |
| second | `ap2_l18_verify_244b.sh` | 19 | 2 | **3** | 14 | 0 | 0 |
| third | `ap2_l19_verify_244c.sh` | 20 | 6 | **0** | 14 | 0 | 0 |

**GLOSS**, and the obligation the standing rules state is the DIFFERS
column: **0**.

- **The three DIFFERS of the first pass were fixed in the CLAIMS and
  never in the verifier.** Three transcripts — the change table, the
  `sat` counts and the by-cause table — had been pasted with lines
  elided for reading, so re-running the command produced more than the
  paste held. Each now carries, on its own command line, the filter that
  produces exactly what is pasted (`| sed -n '1,24p'`, `| grep -v
  counterexample`), or is pasted in full; and the change table's two
  summary counts became a claim of their own, which is why the third
  pass has 20 claims and not 19.
- **The second pass scored the identical three**, because the corrected
  log had not reached the tower when it ran — an rsync that raced the
  edit. Named rather than quietly dropped, since a pass that scores what
  it did not read is worth more as a warning than as a row.
- **UNVERIFIABLE (14)** — seven prose paragraphs (the answer, the
  polyfill-complete reading, the change table's gloss, the causes gloss,
  the limit of the fix-6 measurement, the first item of each of the two
  lists) and seven attributions, each naming the lane log it came from:
  `ap2_l10` for the measurement of record, `ap2_l9` and `ap2_l7` for the
  two probes, `ap2_l11` twice for the guards and the branch, `ap2_l3` for
  the table's guard and `ap2_l2` for `check_L2`'s.
- **MATCHES (6)** — `tables`, `causes`, `repose`, `sat`, and the change
  table in its two pieces.

This section was appended after the third pass, and a fourth pass over
the log WITH it in place — lane `ap2_l20_verify_244d.sh`, the closing one
— returns the identical tally: 20 claims, 6 MATCHES, 0 DIFFERS, 14
UNVERIFIABLE, 0 REFUSED, 0 NOT_RERUNNABLE. The count has reached its
fixed point, so the table above is the log as it stands.

---

# 15. The two lists

## Decided, recorded for audit

1. **The law was not staged and the standing rules were read from the
   three sources that carry them** (§0), rather than reconstructed or
   guessed. No stop rule was reached.
2. **The four driver fixes are NOT gated on a task name.** Gating them is
   what let task h2's fix 1 fall out from under `g1b`, `g1c` and task
   ap1's whole loop; the guards of §7 are what a task name would have
   been standing in for, and all four pass.
3. **Fix 5 registers its two mnemonics in a SEPARATE list**,
   `EMULATION_MNEMONICS`, and never in `CORPUS_MNEMONICS`, whose length
   `acceptance57` reads as `arch_opcodes_the_corpus_spells`. The
   opcode_table CORE's rule is unchanged and is what the list satisfies:
   a body does contain them, and it is a compiled body of this line's own
   emulation route.
4. **Fix 4 was applied to the table's own artifact through the table's own
   join** — `key_width` recomputed by the function over `model_table_rows.json`
   and `model_table_attest.json`, then `model_table.py assemble` re-run —
   rather than worked around in the driver (§7).
5. **A cell is proved on a target only when EVERY half of its destination
   register is proved** (§8), written into `autopoly2.the_places` and
   `weakest`, because `destination_place` alone would have counted the
   low half as the cell.
6. **No setter was invented for the 32 x87 cells** (§5). The census
   answers None and the cause stands, which is the brief's own rule.
7. **The arrival-contract cells and every `sat` were not touched.** The
   group grew from 7 places to 38 because fix 3 puts more places in front
   of the gate, not because anything about the gate changed (§11).
8. **`check_L2` was guarded off the stored artifact** because it cannot be
   re-derived by anyone today (§7), and the reason is task m1b's own
   log_237 §14 item 1.
9. **One status file under `<runs>/` was deleted by this task**,
   `ap2/agent/status/ap2_l6_measure_the_fixes.sh.status`, while trying to
   re-submit a lane of a name that had already run. That breaks the
   standing rule "never delete anything under `<airlock>/` or
   `<home>/AirlockRuns/`". The lane's own log and its `.done` entry are
   intact, so no record of a run was lost, and the correct move — a new
   lane name — is what was then done. Recorded rather than left unsaid.
10. **Two measurement defects were found and corrected, both in what this
    task wrote to MEASURE a fix and neither in a fix**: `measure` and the
    change table looked a pair up by task ap1's own `key_width`, which fix
    4 has moved on eight cells, and `src2/` did not exist. Both are named
    in the lane headers that re-ran (`ap2_l8`, `ap2_l10`, `ap2_l16`).

## Awaiting the owner

1. **`LAW.md` and `task_ap1_brief.md` were not staged for this task**
   (§0). Whatever the law says under "stop rules" was not read. This is
   the first thing to fix before the next round.
2. **The arrival-contract question still needs the ruling task g1b asked
   for**, and it is now 38 places over 12 cells rather than 7 over 5
   (§11). Either the gate learns to pose a comparison over a CONSTRAINED
   region of the cell's inputs, or a cell whose arrival is partly derived
   is a different kind of entry in the Hub. Ontology, not implementation.
3. **A whole 128-bit vector arrival has no holder in any of the four
   targets**, which is the 40 runs of `vector arrival used beyond its low
   lane` (§11). Fix 3 answers the ANSWER side of that — a 128-bit place is
   two 64-bit places — and the arrival side cannot be answered the same
   way, because splitting an arrival changes the arrival contract, which
   is item 2. The two are one question.
4. **Whether task h2's fix 1 is a no-op on 1,012 runs is still
   unmeasured** (§6). It is now on for every task, and it moved at the
   same time as five other fixes, so this loop does not separate it.
5. **`model_translate.py check` cannot run** (§7), which means `check_L2`
   cannot be re-derived by any task. That is log_237 §14 item 1, still
   open, and it is now blocking a guard rather than only a report.
