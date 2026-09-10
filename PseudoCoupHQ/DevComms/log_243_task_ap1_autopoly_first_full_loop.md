# log 243 — task ap1: AutoPoly's first full loop, every attested cell of the model table on four compiled targets

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/`).
Line: arch_unit_oracle, the "goal" section of 2026-09-07 and the ruling of
2026-09-08 in
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`.
Date: 2026-09-09. Instance `ap1`, on the tower guest.

Artifact folder:
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`.
Lane scripts: `.../autopoly/lanes_ap1/`, nineteen of them, each kept in
the repo as the standing rule of 2026-09-07 requires. Every lane log named
below is on the TOWER, under
`<runs>/ap1/agent/logs/`, and says so.

---

# 1. What the objects are

- **A CELL** is one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table
  (`PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json`,
  tasks m1/m1b), which holds, per place the opcode writes, the z3 term the
  reference simulator's own builder puts there.
- **THE OUTER SET** is every cell that the canon40 corpus actually
  attests: a distinct triple with a `TRANSLATED` row whose
  `attestation.ledger_rows` is greater than zero. Task m1b measured it at
  253 (log_237 §8, `PRIVATE/PseudoCoupHQ/DevComms/log_237_task_m1b_model_table_join_closer.md`);
  this task counted it again from the table itself and got 253.
- **A RUN** is `find_emulation(cell, lang)` for one of the four compiled
  targets (c, rust, go, swift): the target's own operator where it has one
  whose whole lowered body IS the cell, the cell's term written in the
  target's operators where it has not; then compiled at the corpus's ship
  flags, carved, and put back to z3 against the cell's own term.
- **THE DRIVER** is
  `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py`
  as task g1b left it (log_242). It is imported and called; not one line
  of it was edited by this task.
- **THIS TASK'S OWN PROGRAM** is
  `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py`,
  the loop around that driver and the bookkeeping, and nothing that
  decides an answer.
- **THE ATTESTED LEDGER ROWS** of a cell are how many rows of the canon40
  corpus's ledger that triple produced (task m1's own census). They are
  the weight this report puts on a cell: a cell proved on four targets
  covering 10,000 ledger rows matters more than one covering 3. The whole
  outer set carries 133,044 of them, and that number is the denominator
  of every share below.

---

# 2. What was done and what came back

the owner's loop was run over its whole measured outer set for the first time.
One lane read the 73 MB model table once and wrote the 253 attested cells,
in descending order of attested ledger rows, into a two-megabyte file the
run lane reads. A second lane ran the first twenty of the thousand runs
and printed its peak memory after each one, which is the sample the law
asks for before a long run; twenty runs took thirteen seconds and the peak
was 260 megabytes against a stated bound of six gigabytes. A third lane
ran the aggregate, the report, the reproduction table and the spelling
guard over those twenty runs alone, before any long compute, and the guard
refused the aggregate — the reason is in section 10 and it was a real
defect in what this task wrote. It was fixed and the guard re-run before
the loop started.

The loop itself then ran all 1,012 pairs in nineteen minutes. Every run is
one line of json, written and flushed as it finishes, so a lane stopped by
the wall clock would have lost nothing; none was stopped. Of the 1,012,
567 ended with the gate proving the emulation equal to the cell and 445
carry a cause. The causes are twelve in number, not four hundred, and the
largest three are not failures of the route at all: a cell whose term
reads machine state that is not an arriving register (134 runs), a
flag-consuming cell whose setter has no row to compose the pair from (128
runs), and a vector cell whose whole 128-bit place is the operation's own
lane so there is nothing narrower to project (56 runs).

Two things came out of the loop that the handful of forty runs could not
have shown. The first is that the primitive route — the target's own
operator, where its whole lowered body IS the cell — reaches between 4%
and 12% of the cells depending on the target, and the term route carries
the rest; that ratio was invisible on ten cells. The second is that the
arrival-contract question task g1b flagged on the divide alone is not the
divide's question. It appears seven times, on five cells, and every one of
them is on the primitive route: an operator's operand list and an opcode's
arrival contract are two different things, and where they differ the gate
declines rather than answers. That is the same finding g1b banked, now
with its population.

The handful reproduces. Of its forty (cell, target) pairs, thirty-six come
out of this loop with the route, the landing and the gate verdict task g1b
recorded; the other four are one cell that is not in this outer set at
all, because the corpus never attested it. Nothing about the method was
touched to make that happen.

---

# 3. The outer set: how the 253 were taken, and the four cells that are not in it

**LITERAL**, lane `ap1_l1_cells.sh`, on the tower at
`<runs>/ap1/agent/logs/20260909T103531Z__ap1_l1_cells.sh.log`:

```
   parsing PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json
   peak after the parse: 290040 kB
   rows in the table: 71778
   the table's own counts: attested_cells 257 placed 253
   distinct (mnem, shape, key_width) triples in the table: 9747
   triples with a TRANSLATED row and ledger_rows > 0: 253
   task m1's own attested cell list holds 257 keys with ledger_rows > 0
   in mine and not in m1's: []
   in m1's and not in mine: [('pcmpeqb', 'mem_xmm', 128), ('pcmpeqb', 'xmm_xmm', 128), ('pcmpeqd', 'xmm_same', 128), ('pmovmskb', 'xmm_gpr', 128)]
```

**GLOSS**, beside it. The table holds 9,747 distinct triples; 253 of them
have both a `TRANSLATED` row and at least one attested ledger row, which
is this loop's outer set. Task m1's own attestation file names 257
attested cells, and the four this task does not run are the four m1b
already reported as having no `TRANSLATED` row: two `pcmpeqb` shapes, one
`pcmpeqd` and one `pmovmskb`. The two counts agree in both directions,
which is why they are printed in both directions rather than summarised.

**THE ORDER** is the attested ledger rows, descending, so a stopped lane
has already finished the cells that carry most of the corpus. The outer
set as the loop walks it, **LITERAL**, lane `ap1_l14_claims3.sh` on the
tower at `<runs>/ap1/agent/logs/20260909T112049Z__ap1_l14_claims3.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py preflight | grep -v 'peak resident'
cells on PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly_cells.json: 253
targets: c, rust, go, swift
pairs: 1012
attested ledger rows over the whole outer set: 133044

the first ten cells of the order, most attested first:
   setne      gpr_one        8      ledger_rows 10335
   mov        gpr_gpr        32     ledger_rows 10245
   mov        gpr_gpr        64     ledger_rows 7194
   xor        gpr_same       32     ledger_rows 5190
   cmp        gpr_gpr        64     ledger_rows 4011
   movslq     widen_gpr_gpr  None   ledger_rows 3728
   test       gpr_same       32     ledger_rows 3617
   push       gpr_one        64     ledger_rows 3408
   xorps      xmm_same       128    ledger_rows 3013
   cvtsi2ss   gpr_xmm        32     ledger_rows 2936

cells whose key_width is null: 8
   movslq widen_gpr_gpr None
   movzbl widen_gpr_gpr None
   movzwl widen_gpr_gpr None
   movswl widen_gpr_gpr None
   movsbl widen_gpr_gpr None
   movzbl widen_mem_gpr None
   movsbq widen_gpr_gpr None
   movzwl widen_mem_gpr None

runs already on PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly_runs.jsonl: 1012
```

**GLOSS**: 253 cells, 1,012 pairs, 133,044 attested ledger rows, and the
eight cells whose `key_width` is null — six of which are in this outer
set and are the six the driver cannot format a label for (§6).

**WHAT THE CELLS FILE HOLDS AND WHAT IT DROPS.** Each of the 253 entries
carries every model-table row at its triple, so the driver's own
`chosen_row` applies task g1b's two rules unchanged (the row whose own
`width` equals the cell's `key_width`; among flag-reading rows, the one
whose arriving flag state was written by the setter the cell's attestation
records most). One field of each row is dropped: `mapping`, the built term
per written place as text. The driver never reads it — `terms_of_row`
REBUILDS the terms by calling `model_table.places_of_attempt` on the row's
own `mnem` / `operands` / `preseeded` / `flags_in` / `width`, which is the
same call task m1b's edges pass makes. Dropping it is what keeps the file
at 1.9 MB rather than tens of megabytes. The lane prints a row's own field
list so the drop is visible rather than asserted.

---

# 4. The loop: 1,012 runs, the pace, and the ceilings

**LITERAL**, lane `ap1_l5_run.sh`, on the tower at
`<runs>/ap1/agent/logs/20260909T104708Z__ap1_l5_run.sh.log`,
its first lines and its last:

```
20 line(s) of the store were rewritten onto the machine-form cell key
pairs to run: 1012; already recorded: 20
the gate of record: 3000 ms; the one re-pose: 30000 ms
the table's own TRANSLATED triples, for the composition step: 6218
peak resident after the two reads: 260192 kB
[21/1012] movslq widen_gpr_gpr None -> c (ledger_rows 3728)
   - | REFUSED: the driver raised on this (cell, target) pair | 0 s | peak resident: 260192 kB
```

**LITERAL**, the same lane log, its last three lines:

```
runs performed this lane: 992 in 1139 s
lines on PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly_runs.jsonl: 1012
peak resident: 2414988 kB
```

**GLOSS.** The twenty runs the sample lane had already recorded were
skipped; the remaining 992 took nineteen minutes. The wall-clock pace, per
target, is a measurement and not an estimate — c 54 s over 253 runs, rust
207 s, swift 193 s, go 691 s, because `go build` gets a fresh build cache
per compile (`go_render.compile_and_carve` points `GOCACHE` inside its own
temporary directory, which is what the corpus's own lane generator does).

**THE TWO CEILINGS.** The gate of record is the pipeline's own 3,000 ms.
Every UNDECIDED is re-posed ONCE at 30,000 ms — the brief's own number,
not the handful's 300,000 ms, because this loop poses a thousand runs
rather than forty — and both answers are kept. What that re-pose moved is
section 8.

---

# 5. THE table: per target, what the loop reached

**LITERAL**, lane `ap1_l11_claims2.sh`, on the tower at
`<runs>/ap1/agent/logs/20260909T111309Z__ap1_l11_claims2.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py tables
## 1. THE table: per target, what the loop reached

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.

| step or verdict | c | rust | go | swift |
|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 167 cells, 112151 rows, 84.3% | 167 cells, 112151 rows, 84.3% | 153 cells, 99907 rows, 75.09% | 153 cells, 99907 rows, 75.09% |
| `compiled` | 167 cells, 112151 rows, 84.3% | 167 cells, 112151 rows, 84.3% | 153 cells, 99907 rows, 75.09% | 153 cells, 99907 rows, 75.09% |
| `LANDED` | 62 cells, 36632 rows, 27.53% | 59 cells, 35529 rows, 26.7% | 25 cells, 18849 rows, 14.17% | 57 cells, 35245 rows, 26.49% |
| `LANDED_ELSEWHERE` | 15 cells, 13524 rows, 10.17% | 16 cells, 14268 rows, 10.72% | 8 cells, 5004 rows, 3.76% | 22 cells, 14502 rows, 10.9% |
| `NOT_COLLAPSED` | 90 cells, 61995 rows, 46.6% | 92 cells, 62354 rows, 46.87% | 120 cells, 76054 rows, 57.16% | 74 cells, 50160 rows, 37.7% |
| `proved` | 129 cells, 77735 rows, 58.43% | 132 cells, 82884 rows, 62.3% | 136 cells, 87742 rows, 65.95% | 124 cells, 73007 rows, 54.87% |
| `proved under caller extension` | 15 cells, 19418 rows, 14.6% | 16 cells, 20390 rows, 15.33% | 0 cells, 0 rows, 0.0% | 13 cells, 18670 rows, 14.03% |
| `sat` | 10 cells, 3812 rows, 2.87% | 11 cells, 4685 rows, 3.52% | 8 cells, 3433 rows, 2.58% | 2 cells, 2331 rows, 1.75% |
| `undecided` | 13 cells, 11186 rows, 8.41% | 8 cells, 4192 rows, 3.15% | 9 cells, 8732 rows, 6.56% | 14 cells, 5899 rows, 4.43% |
| `refused` | 86 cells, 20893 rows, 15.7% | 86 cells, 20893 rows, 15.7% | 100 cells, 33137 rows, 24.91% | 100 cells, 33137 rows, 24.91% |

## 2. Per target, how far the primitive route reached

Table 2 -- `primitive` is a target operator whose whole lowered body IS the cell; `primitive+setup` is that plus zero-operand accumulator setup (task g1c's widened lookup); `term` is the cell's own term written in the target's operators, which is the fallback.

| route | c | rust | go | swift |
|---|---|---|---|---|
| `primitive` | 29 cells, 19706 rows, 14.81% | 22 cells, 12245 rows, 9.2% | 17 cells, 10351 rows, 7.78% | 9 cells, 7774 rows, 5.84% |
| `primitive+setup` | 2 cells, 1726 rows, 1.3% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |
| `term` | 184 cells, 105179 rows, 79.06% | 193 cells, 114366 rows, 85.96% | 198 cells, 116260 rows, 87.38% | 206 cells, 118837 rows, 89.32% |
| `no route reached` | 38 cells, 6433 rows, 4.84% | 38 cells, 6433 rows, 4.84% | 38 cells, 6433 rows, 4.84% | 38 cells, 6433 rows, 4.84% |

Table 3 -- a cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 4 of 4 | 120 | 76634 | 57.6% |
| 3 of 4 | 17 | 16985 | 12.77% |
| 2 of 4 | 14 | 9941 | 7.47% |
| 1 of 4 | 6 | 2473 | 1.86% |
| 0 of 4 | 96 | 27011 | 20.3% |

`sat` at the plain comparison, every written place: 110
`sat` surviving the caller-extension re-pose: 39
the handful's forty pairs: 32 agree character for character, 36 agree on the verdict, 4 not in this outer set
```

**GLOSS**, and three readings the table does not make on its own.

- **Every count is of the run's own DESTINATION PLACE**, which is
  `handful.destination_place` — the first place the cell writes that is
  not the flags, or the flags place when that is all the cell writes.
  That is the place tasks h1, h2, g1 and g1b's own tables already
  summarize, so a row here counts the same thing a row there did.
- **`rendered` and `compiled` are the same number on every target.**
  Nothing that this loop rendered failed to compile. Whatever stops a
  cell, it stops it before the compiler ever sees a source file.
- **The verdict of record is the 3,000 ms one.** Two runs that the
  30,000 ms re-pose then proved still sit in the `undecided` row of this
  table; section 8 names them.

---

# 6. Refusals and non-proofs, by cause, the four targets summed

The report's own section 3 splits this per target, which is what the brief
asks for. Summed over all 1,012 runs it is twelve causes and one of them
is a question rather than a limit.

**LITERAL**, same lane
(`<runs>/ap1/agent/logs/20260909T111309Z__ap1_l11_claims2.sh.log`):

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py causes
Table 5 -- what did not work, by cause, the four targets summed. `rows` counts a cell's attested ledger rows once per run, so a cause seen on all four targets counts them four times.

| cause | runs | ledger rows | targets |
|---|---|---|---|
| term reads state that is not an arrival register | 134 | 37874 | c, go, rust, swift |
| no setter row to compose the flag pair from: None at width 8 | 128 | 6284 | c, go, rust, swift |
| the cell's own key_width is not narrower than the place, so there is no lane to project | 56 | 19324 | c, go, rust, swift |
| the gate answered sat: the body holds on a region, not on every input | 31 | 14261 | c, go, rust, swift |
| a width c has no holder for | 30 | 25130 | go, swift |
| the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | 24 | 19448 | c, go, rust, swift |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 11 | 3820 | c, go, rust, swift |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 10 | 10534 | go, swift |
| the gate did not answer: the carved body: the reference: arch opcode 'cmovg' has no entry in the opcode table -- no body in the corpus this table was built over spells it; and no term either | 7 | 195 | c, rust, swift |
| the gate did not answer: the carved body: the reference: lea addressing form '0x0(,%rdi,8)' is not the (displacement, base, index, scale) shape this file models; and no term either | 6 | 7005 | c, rust, swift |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | 2 | 840 | c |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | 2 | 1726 | c |
| the gate did not answer: the carved body: the reference: arch opcode 'movswq' has no entry in the opcode table -- no body in the corpus this table was built over spells it; and no term either | 2 | 19 | go |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows | 1 | 5190 | c |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 | c |

runs carrying a cause: 445 of 1012

THE ARRIVAL-CONTRACT GROUP, counted on its own: every gate call that declined because the two sides name a different number of arriving values.

places the gate declined on the IN-row alignment: 7
   4 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows
   2 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows
   1 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows

| cell | route | ledger rows |
|---|---|---|
| `xor` gpr_same 32 | primitive | 5190 |
| `idiv` gpr_one 64 | primitive+setup | 948 |
| `mov` imm_gpr 32 | primitive | 835 |
| `idiv` gpr_one 32 | primitive+setup | 778 |
| `mov` imm_gpr 8 | primitive | 5 |
```

**GLOSS**, cause by cause, each with its status.

- **`term reads state that is not an arrival register` — 134 runs, OPEN,
  upstream.** The cell's term reads something the emulation has no way to
  receive as an argument: `push` gpr_one 64 reads and writes the stack
  pointer; `fldt` mem_one 80 reads an x87 stack position; `movss` mem_xmm
  32 reads memory. These are cells whose mapping is not a function of
  arriving values at all, and no renderer can be given one.
- **`no setter row to compose the flag pair from: None at width 8` — 128
  runs, OPEN.** A flag-reading cell's mapping is a function of the flags a
  setter wrote, so the driver composes the pair; where the cell's own
  attestation names no setter (the field is `None`), there is no pair to
  compose. Thirty-two cells, on all four targets.
- **`the cell's own key_width is not narrower than the place` — 56 runs,
  OPEN.** Task h2's fix 2 projects a vector cell's lane out of its
  128-bit place; a cell whose `key_width` IS 128 (`xorps` xmm_same 128,
  `movaps` xmm_xmm 128) has no narrower lane, so there is nothing to
  project and the driver says so.
- **`a width c has no holder for` — 30 runs, go and swift only, OPEN.**
  The flags place of a 64-bit comparison is a 128-bit value (the two
  operands concatenated), and neither the go nor the swift renderer has a
  128-bit integer holder. c and rust do (`unsigned __int128`, `i128`),
  which is why the same 15 cells are refused on two targets and not on
  the other two.
- **`the driver raised ... %d format: a real number is required, not
  NoneType` — 24 runs, 6 cells, OPEN and named in section 12.** Eight
  cells of the table carry `key_width: null`, and the driver formats a
  cell's label with `%d`. Six of the eight are attested and are in this
  outer set. Recorded as a result by cause, per the brief's own rule, and
  not worked around.
- **`the gate answered sat` — 31 runs, OPEN, and it is a FINDING rather
  than a limit.** Section 7.
- **The five remaining `the gate did not answer` causes — 27 runs,
  OPEN.** Four are the reference simulator declining to walk the carved
  body (an addressing form it does not model, an opcode with no entry, a
  body with no path that stays in the unit, a unit record with no body),
  one is the solver's clock at 3,000 ms, and one is the arrival-contract
  group below.
- **THE ARRIVAL-CONTRACT GROUP — 7 places, 5 cells, OPEN, and it is the
  one that needs a ruling.** Every one of the seven is on the primitive or
  primitive+setup route, and the reason is structural rather than a
  clock. An operator's operand list and an opcode's arrival contract are
  two different things, and the gate aligns them row by row:
  - `idiv` gpr_one at 32 and 64 reads THREE arriving values (the high
    half of the dividend, its low half, the divisor); the emulation `a %
    b` reads TWO and derives the third with `cltd`. This is task g1b's
    own finding (log_242 §7.4), now with a second width beside it.
  - `xor` gpr_same 32 reads ONE (a register exclusive-ORed with itself);
    the operator on two holders reads TWO. The mismatch runs the other
    way, and it carries 5,190 ledger rows — the largest single cell in
    the group.
  - `mov` imm_gpr at 32 and 8 reads ZERO arriving values (the source is
    an immediate); the operator reads ONE.
  Three shapes, one question: the gate has no way to say "this input is
  a function of that one" or "this input is a constant", so it declines
  rather than answers.

---

# 7. Every `sat` verdict: two counts, and the region each names

A `sat` is z3 finding a starting state under which the compiled body and
the cell's term answer differently — which is exactly where a target's
edge region differs from the opcode's. There are two counts and they are
two different things.

- **`sat` at the plain comparison: 110 places.** Every written place, the
  flags included, where z3 answered `sat` when the emulation's arriving
  values are whatever fits the register.
- **`sat` surviving the caller-extension re-pose: 39 places.** Task o7's
  own rule: pose the same comparison again with every narrow-holder input
  row zero-extended from its holder width to the register, which is what
  the target's own calling rule guarantees the caller did. c 13, rust 15,
  go 8, swift 3.
- **Table 1's `sat` row is 31**, because it counts only the destination
  place; the other eight of the 39 are on flags places.

**LITERAL**, lane `ap1_l14_claims3.sh` on the tower at `<runs>/ap1/agent/logs/20260909T112049Z__ap1_l14_claims3.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py sat
sat at the plain comparison, every written place: 110
sat surviving the caller-extension re-pose: 39
   c      13
   go     8
   rust   15
   swift  3
the five surviving sat places with the most ledger rows:
   ucomiss    xmm_xmm      32    c      [flags] 2270 rows
      counterexample: [IN_1 = 2139180370, IN_0 = 2139180354, fp.to_ieee_bv = [NaN -> 2139180370, else -> fp.to_ieee_bv(Var(0))]]
   ucomiss    xmm_xmm      32    go     [flags] 2270 rows
      counterexample: [IN_0 = 1048592389, IN_1 = 4294948858, fp.to_ieee_bv = [NaN -> 4294965242, else -> fp.to_ieee_bv(Var(0))]]
   ucomiss    xmm_xmm      32    rust   [flags] 2270 rows
      counterexample: [IN_0 = 2139096064, IN_1 = 2692742014, fp.to_ieee_bv = [NaN -> 2139620352, else -> fp.to_ieee_bv(Var(0))]]
   ucomiss    xmm_xmm      32    swift  [flags] 2270 rows
      counterexample: [IN_0 = 2222718846, IN_1 = 2139357249, fp.to_ieee_bv = [NaN -> 2139357185, else -> fp.to_ieee_bv(Var(0))]]
   ucomisd    xmm_xmm      64    c      [flags] 1026 rows
      counterexample: [IN_1 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]]
```

**GLOSS.** The top four are the same cell on all four targets, and z3's
counterexample names the same region on each: the model of
`fp.to_ieee_bv` it built maps `NaN` to a specific bit pattern, and the
counterexample sits on it. `ucomiss` compares two floats and writes the
flags; a comparison against a NaN is the float comparison's edge region,
and every one of the four targets differs from the opcode's mapping
there. That is the owner's edge-region model made measurable on the largest
cell it reaches — with the caveat, stated because it changes what the
counterexample proves: z3's model of `fp.to_ieee_bv` is a model of an
uninterpreted function, so the counterexample names the region, and
whether the target actually differs at that point is a further question
about the float model (the proof-system item of the research CORE's §4.2
order, item 4).

The whole list of 110, each with its counterexample and whether it
survives the re-pose, is section 5 of
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.md`.

---

# 8. Cells proved on all four targets, and what the one re-pose moved

**THE POLYFILL-COMPLETE SET IS 120 CELLS, 76,634 attested ledger rows,
57.6% of the outer set** (Table 3 in section 5). Three of four: 17 cells,
12.77%. Two: 14, 7.47%. One: 6, 1.86%. None: 96 cells, 27,011 rows,
20.3%. The 120 in full, and the 96 in full with the cause on each of the
four targets, are sections 4.1 and 4.2 of
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.md`.

**THE RE-POSE.** The law's rule on a time limit is that it is a FLAG:
re-run with more room and report whether the answer changed.

**LITERAL**, lane `ap1_l11_claims2.sh`, on the tower at
`<runs>/ap1/agent/logs/20260909T111309Z__ap1_l11_claims2.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py repose
places UNDECIDED at the 3,000 ms ceiling of record and re-posed once at 30,000 ms: 56
   DISPROVED        1
   PROVED_ON_SHIP   2
   UNDECIDED        53

| cell | lang | place | route | ledger rows | the re-pose's answer |
|---|---|---|---|---|---|
| `div` gpr_one 8 | go | reg_rax | term | 28 | PROVED_ON_SHIP |
| `div` gpr_one 8 | swift | reg_rax | term | 28 | PROVED_ON_SHIP |
| `idiv` gpr_one 16 | c | reg_rax | term | 16 | DISPROVED |
```

**GLOSS.** Fifty-six places were re-posed and three moved: two proved and
one disproved, all three on a divide, together carrying 72 ledger rows of
133,044. The verdict of record stays the 3,000 ms one, so those three are
still counted as `undecided` in Table 1; the answer at ten times the
ceiling sits beside it, which is what the law asks for. Fifty-three did
not move, and 7 of those 53 are the arrival-contract group of section 6,
which no ceiling can move because the reason is structural.

---

# 9. The handful, reproduced

**LITERAL**, eight rows copied verbatim out of the forty that lane
`ap1_l11_claims2.sh` printed, on the tower at
`<runs>/ap1/agent/logs/20260909T111309Z__ap1_l11_claims2.sh.log`
under its `===== reproduce =====` heading. The whole forty-row table is
section 6 of
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.md`,
and the three counts under it are the last line of the `tables` transcript
in section 5 of this log, which re-runs.

Table 1 of this log — one row per reading the forty carry:

| cell | lang | this loop: route / landed / gate | the handful: route / landed / gate | agrees | agrees on the verdict |
|---|---|---|---|---|---|
| `add` gpr_gpr 32 | go | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `sub` imm_gpr 64 | c | -- | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | **no** | **no** |
| `imul` gpr_gpr 32 | c | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `sar` cl_gpr 32 | go | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | yes | yes |
| `idiv` gpr_one 32 | c | primitive+setup / NOT_COLLAPSED (2) / UNDECIDED, UNDECIDED at 30000 ms | primitive+setup / NOT_COLLAPSED (2) / UNDECIDED, UNDECIDED at 300000 ms | **no** | yes |
| `setne` gpr_one 8 | c | term / NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | term / NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | yes | yes |
| `addss` xmm_xmm 32 | swift | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |
| `cvtsi2sd` gpr_xmm 64 | go | term / NOT_COLLAPSED (4) / PROVED_ON_SHIP | term / NOT_COLLAPSED (4) / PROVED_ON_SHIP | yes | yes |

**GLOSS**, and the two counts are the answer. **Thirty-two of forty agree
character for character; thirty-six agree on the verdict.** The two
numbers differ by exactly the four `idiv` rows, whose only difference is
the number of milliseconds the one re-pose was given — 30,000 here against
the handful's 300,000, which is this brief's own instruction. Both answers
are UNDECIDED at both ceilings.

**THE FOUR PAIRS THIS LOOP DID NOT RUN ARE ONE CELL**, `sub` imm_gpr 64,
and the reason is that it is not in the outer set. **LITERAL**, lane
`ap1_l7_report_evidence.sh`, on the tower at
`<runs>/ap1/agent/logs/20260909T110920Z__ap1_l7_report_evidence.sh.log`
— every `sub` cell task m1's own attestation file holds:

```
sub cl_gpr     key_width 8     ledger_rows 253 units 253
sub gpr_gpr    key_width 16    ledger_rows 2 units 2
sub gpr_gpr    key_width 32    ledger_rows 340 units 340
sub gpr_gpr    key_width 64    ledger_rows 577 units 576
sub gpr_gpr    key_width 8     ledger_rows 19 units 19
```

**GLOSS.** There is no `sub imm_gpr` cell at any width: the corpus never
produced a subtract with an immediate operand, because a compiler emits an
ADD of a negative immediate instead — which is precisely what task g1b
measured on that cell (`sub` imm_gpr 64 on go: LANDED_ELSEWHERE on `add`).
Task h1's brief named the cell and the table has a `TRANSLATED` row for
it; what it has no attestation for. So the loop's outer set does not carry
it, and that is a fact about the corpus rather than a gap in this run.

---

# 10. The one defect this task found in what it wrote, and how it was fixed

The aggregate written from the first twenty runs was refused by the
spelling guard. **LITERAL**, lane `ap1_l3_aggregate_probe.sh`, on the
tower at
`<runs>/ap1/agent/logs/20260909T104313Z__ap1_l3_aggregate_probe.sh.log`:

```
FAIL autopoly.json -- 24 spelling-keyed place(s)
     $.across_targets.on_none_with_causes[5].cell
         operator token 'or' on a structure field -- this is a grouping/row key, not a per-unit label
     $.across_targets.on_none_with_causes[15].cell
         operator token 'xor' on a structure field -- this is a grouping/row key, not a per-unit label
     $.across_targets.on_none_with_causes[16].cell
         operator token 'and' on a structure field -- this is a grouping/row key, not a per-unit label
```

**GLOSS.** The aggregate carried a field `cell` holding the triple joined
into one string — `and|gpr_gpr|32` — which is a row key carrying an
operator token, and the guard's rule 1 names exactly that shape. The guard
was right. The record is now written the guard's way: the triple in three
fields, the mnemonic in `mnem`, which the ruling of 2026-09-08 states is
the machine form and which the guard already reads as one. Nothing about
the match changed — the driver still compares triple with triple in
memory — and what changed is how the store spells a key it writes down.

A second pass found a second shape of the same defect: the driver's own
`primitive_lookup` records a matched row's cell as a LIST, `["xor",
"gpr_same", 32]`, and the guard refuses a list element that is a bare
operator token. The handful's ten cells carried no mnemonic that collides
with an operator spelling, so that shape had never met the guard; this
loop's 253 do. It is fixed in `autopoly.as_machine_form`, one function
applied once at the one place a record becomes a line on a file, and NOT
in `handful.py`, which this task does not edit.

**LITERAL**, the final state, lane `ap1_l12_guard_and_branch.sh`, on the
tower at
`<runs>/ap1/agent/logs/20260909T111412Z__ap1_l12_guard_and_branch.sh.log`:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly_cells.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS autopoly_cells.json -- no operator token in any key, grouping, pairing or row structure
PASS autopoly.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap1/ap1_l1_cells.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap1/ap1_l5_run.sh
PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap1/ap1_l1_cells.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap1/ap1_l5_run.sh:0
```

**THE STORE AND THE AGGREGATE HOLD THE SAME RUNS**, checked rather than
assumed. **LITERAL**, lane `ap1_l14_claims3.sh` on the tower at `<runs>/ap1/agent/logs/20260909T112049Z__ap1_l14_claims3.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py store
lines on the store: 1012
runs on the aggregate: 1012
run for run identical: 1012
distinct (cell, target) pairs: 1012
```

**GLOSS**, and this is why the guard over `autopoly.json` covers the
incremental store too: every line of `autopoly_runs.jsonl` is a run of
`autopoly.json`, character for character, so guarding the one guards the
other.

---

# 11. One fact about the imported driver, found while reading it, reported and not changed

`handful.renderer_input` decides which form of a cell's term the renderer
is handed, and it names two tasks by name. **LITERAL**, lane
`ap1_l14_claims3.sh` on the tower at `<runs>/ap1/agent/logs/20260909T112049Z__ap1_l14_claims3.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py branch
def renderer_input(term, how):
    """the term the renderer is handed, by task.

    `h1`: `order_commutative(z3.simplify(term))`, which is what task h1
    handed it and what task h1's own products are a rendering of.
    `h2` and `g1`: the normalised term, task h2's fix 1, which task g1
    inherits rather than re-deciding."""
    if how in ("h2", "g1"):
        return the_normalised_term(term)
    return T.order_commutative(z3.simplify(term))

TASK h1   fixes_are_on False primitive_first False setup_is_allowed False -> order_commutative(simplify(term)), task h1's own
TASK h2   fixes_are_on True  primitive_first False setup_is_allowed False -> the normalised term (task h2's fix 1)
TASK g1   fixes_are_on True  primitive_first True  setup_is_allowed False -> the normalised term (task h2's fix 1)
TASK g1b  fixes_are_on True  primitive_first True  setup_is_allowed False -> order_commutative(simplify(term)), task h1's own
TASK g1c  fixes_are_on True  primitive_first True  setup_is_allowed True  -> order_commutative(simplify(term)), task h1's own
```

**GLOSS.** `fixes_are_on()` answers True for `g1b` and `g1c`, so task h2's
FIX 2 (the vector lane projection) is on for them and for this loop. FIX 1
is not: `renderer_input`'s list names `h2` and `g1` and not their two
closers, so tasks g1b, g1c and this task all render from
`order_commutative(simplify(term))` — task h1's own form — rather than
from the normalised term. Task h2 measured that fix as a NO-OP on its own
population: all 24 rendered places produced a source character for
character identical both ways (log_240, and
`PRIVATE/PseudoCoupHQ/DevComms/log_240_task_h2_two_printing_fixes.md`).
So this is a fact about what ran, not a claim that a result is wrong, and
it is REPORTED rather than fixed: this brief's own instruction is the
driver as task g1b left it, unchanged, and changing which term the
renderer is handed mid-loop would be exactly the process substitution the
standing rule forbids. It is in the awaiting-the owner list.

---

# 12. Memory

The bound stated in `PUBLIC/Airlock/instances/ap1.conf`, in
`autopoly.py`'s own docstring and in every lane header is 6 GB resident on
the one collecting process, named abort `ABORT_MEMORY_AP1`, checked after
every run. The peaks the programs printed:

| lane | what it read | peak resident |
|---|---|---|
| `ap1_l1_cells.sh` | `model_table.json`, 73 MB, once | 290,040 kB |
| `ap1_l2_preflight_sample.sh` | the cells file and `model_table_rows.json`, then 20 runs | 260,016 kB |
| `ap1_l5_run.sh` | the same two reads, then 992 runs | 2,414,988 kB |
| `ap1_l6_aggregate.sh` | the whole 1,012-run store | 81,844 kB |
| `ap1_l7_report_evidence.sh` | the store and the aggregate together | 43,436 kB |

The high-water mark, 2,414,988 kB, is 38% of the bound. No abort fired.
The growth inside the run lane is worth naming since it is the only figure
that moves with the run count: 260 MB after the two reads, 2.4 GB by the
thousandth run, and it grows because the z3 context accumulates terms
across runs. A lane stopped on that bound would have lost nothing — the
store is per-run — and a resumed lane starts again at 260 MB, which is
what the incremental store was for.

---

# 13. The deliverables

Under
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`:

| file | what it is |
|---|---|
| `autopoly.py` | the loop over the table, the bookkeeping, the aggregate and the report writer |
| `autopoly_cells.json` | the 253 attested cells, in run order, with every model-table row at each triple and the setter rows a flag pair needs |
| `autopoly_runs.jsonl` | the incremental store: one json object per run, 1,012 lines, 4.0 MB |
| `autopoly.json` | the aggregate: the five tables, the by-cause lists, every `sat`, the handful comparison, and the 1,012 runs themselves, 5.1 MB |
| `autopoly.md` | the report, 512 lines, the six sections the brief names |
| `src/` | the 1,012 rendered sources, one per run that reached the render step |
| `lanes_ap1/` | the nineteen lane scripts, kept in the repo as the standing rule requires |

---

# 14. The conventions verifier over this log

Four passes, each a lane of this task's own instance, each over this log
as it then stood.

| pass | lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|---|
| first | `ap1_l13_verify_243.sh` | 21 | 5 | 0 | 16 | 0 | 0 |
| second | `ap1_l15_verify_243b.sh` | 21 | 6 | **1** | 12 | 0 | 2 |
| third | `ap1_l16_verify_243c.sh` | 21 | 7 | **0** | 12 | 0 | 2 |
| fourth | `ap1_l17_verify_243d.sh` | 22 | 7 | **0** | 13 | 0 | 2 |

**GLOSS**, and the obligation the law states is the DIFFERS column: **0**.
Every claim that carries a command and can be re-run reproduces.

- **What moved between the first pass and the second.** Five claims that
  were attributions to a lane log — the outer set, the store's identity
  with the aggregate, the `sat` counts, the driver's `renderer_input`, and
  the run lane's own last lines — were turned into commands that re-run,
  each a new entry point of `autopoly.py` printing exactly what the lane
  had printed. UNVERIFIABLE fell from 16 to 12.
- **The one DIFFERS, and it was fixed in the CLAIM and never in the
  verifier.** The `preflight` transcript ended with the program's own
  `peak resident` line, a real measurement that moves by a few kB between
  runs. The pasted command now carries `| grep -v 'peak resident'` on the
  line itself, so what is printed is what ran, and the memory figures are
  in section 12 where they belong. That is the third pass.
- **NOT_RERUNNABLE (2), both for the cause `output_annotated`.** The `sat`
  transcript in section 7 and the `branch` transcript in section 11. The
  verifier reads `->` in a paste as a hand-written gloss; here the arrow
  is real output, from z3's own model printing (`NaN -> 2139180370`) and
  from the program's own per-task table. A heuristic misfire on genuine
  output, left as it is rather than worked around by rewording the
  program.
- **UNVERIFIABLE (12)** — six prose paragraphs (section 1's objects,
  section 2's walkthrough, the three glosses that read a table, and the
  first item of each of the two lists, which the protocol requires) and
  six attributions, each naming the lane log it came from: `ap1_l1_cells.sh`
  for the outer-set cross-check, `ap1_l5_run.sh` for the loop's own first
  and last lines, `ap1_l3_aggregate_probe.sh` for the guard's refusal
  (which cannot re-run, being a historical output of a program since
  fixed), and the `sub` attestation read.
- **MATCHES (7)** — `preflight`, `tables`, `causes`, `repose`, `store`,
  the spelling guard, and the `grep -c exempt` count.

This section was appended after the third pass, and the fourth pass is the
one over the log with it in place. Appending it added exactly one
UNVERIFIABLE prose claim (21 claims to 22, UNVERIFIABLE 12 to 13) and
moved the line numbers, and changed nothing else — which is what a
section of prose about a verifier should change. The row for that pass is
in the table above, written after it ran, and a fifth pass over the log
WITH that row in it — lane `ap1_l18_verify_243e.sh`, the closing one —
returns the identical tally: 22 claims, 7 MATCHES, 0 DIFFERS, 13
UNVERIFIABLE, 0 REFUSED, 2 NOT_RERUNNABLE. The count has reached its
fixed point, so the table above is the log as it stands.

---

# 15. The two lists

## Decided, recorded for audit

1. **The outer set is the 253 attested cells, counted from the table
   itself and cross-checked against task m1's own attestation file in both
   directions** (§3), rather than taken from log_237's number.
2. **The cells file drops each row's `mapping` field and nothing else**,
   because the driver rebuilds every term by calling
   `model_table.places_of_attempt` on the row's own fields and never reads
   that field; the lane prints a row's field list so the drop is visible
   (§3).
3. **`handful.py` was not edited.** `handful.TASK` is set to `g1c`, which
   is task g1b's closer's own setting, and every path the driver writes
   through is repointed into this task's folder so no lane of this task
   could write task g1b's products (`autopoly.use_task_ap1`).
4. **A run the route cannot handle is recorded as a result by cause**, the
   exception LITERAL with the line it came from, and the loop goes on —
   the brief's own rule. Twenty-four runs, six cells, all of them the
   `key_width: null` shape (§6).
5. **The re-pose is ONE, at 30,000 ms, inside the run** rather than in a
   second pass over the file, so a line on the store is a finished run
   (§8).
6. **The verdict of record is the 3,000 ms one**, and the three places the
   re-pose moved are still counted as `undecided` in Table 1 with the
   re-pose's answer beside them (§8).
7. **The guard's refusal of the joined cell key was taken as correct and
   the record was rewritten its way**, in two shapes, both fixed in this
   task's own code and neither in `handful.py` (§10).
8. **Two comparisons are reported for the handful**, character for
   character and on the verdict, because the two differ by exactly the
   re-pose's own millisecond number and reporting only the first would
   read as a disagreement that is not one (§9).

## Awaiting the owner

1. **The arrival-contract question is general, and it needs the ruling
   task g1b asked for.** Seven places, five cells, every one on the
   primitive route: `idiv` at two widths reads three arriving values where
   the operator reads two; `xor` gpr_same 32 reads one where the operator
   reads two, and it carries 5,190 ledger rows; `mov` imm_gpr at two
   widths reads zero where the operator reads one. The gate aligns inputs
   IN row by IN row and cannot express "this input is derived from that
   one" or "this input is a constant", so it declines. Either the gate
   learns to pose a comparison over a CONSTRAINED region of the cell's
   inputs, or a cell whose arrival is partly derived is a different kind of
   entry in the Hub. Ontology, not implementation (§6).
2. **Eight cells of the model table carry `key_width: null`, six of them
   attested**, and the driver formats a label with `%d`. Whether the fix
   is in the table (a `widen_gpr_gpr` cell's key width is the DESTINATION
   width, which the shape name already implies) or in the driver is a
   question about what `key_width` means for a widening move, which is
   m1b's ontology and not this task's (§6).
3. **Task h2's FIX 1 is off for every task after `g1`.**
   `handful.renderer_input` names `h2` and `g1` and not `g1b`, `g1c` or
   this task, so those three render from task h1's form of the term. Task
   h2 measured the fix as a no-op on its own twenty runs; whether it is a
   no-op on 1,012 is unmeasured. Reported and not changed, because the
   brief's instruction is the driver unchanged (§11).
4. **The largest `sat` group is the float comparison against NaN on all
   four targets**, and what the counterexample proves depends on the float
   model: z3's `fp.to_ieee_bv` is uninterpreted there, so the
   counterexample names the region and does not yet establish that the
   target differs at that point. That is the proof-system item of the
   research CORE's §4.2 order (item 4), reached from this side (§7).
