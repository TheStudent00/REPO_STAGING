# log 262 — task t4: the general construction tier, one construction per operation kind, measured against the eight-schema tier

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`).
It also touches the proof system's Lean node
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/PROGRESS.md`)
and both architecture nodes
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_0_x86_64/PROGRESS.md`,
`.../node_0_3_2_3_1_riscv64/PROGRESS.md`).

Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it.
It follows task t2 (`PRIVATE/PseudoCoupHQ/DevComms/log_257_task_t2_the_second_tier_constructs_what_a_target_lacks.md`),
which wrote EIGHT schemas for eight shapes; this task writes the METHOD.

Date: 2026-09-10 into 2026-09-11. Instance `t4`
(`PUBLIC/Airlock/instances/t4.conf`). Every lane ran on the
tower guest through `bash PUBLIC/Airlock/remote_lane.sh`;
nothing but file editing, git and those commands ran on the laptop. A lane
log's host path on the tower is
`<runs>/t4/agent/logs/<stamp>__<lane>.sh.log`, and
every attribution below names its file. Paths inside a pasted command are
the ones the lane sees: `PseudoCoupHQ` IS
`PRIVATE/PseudoCoupHQ`. Every rendering is labelled
**LITERAL** (the object, quoted) or **GLOSS** (a plain-words reading beside
a literal).

THIS TASK WAS PICKED UP MID-FLIGHT. The first implementer wrote the
constructions and ran five smoke lanes and was then cut off by an
authentication error; section 1 below is its measurement, unchanged, and
everything from section 2 on is this one's.

THE SPELLING BAN, pasted verbatim as required:

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

---

## §0. What this is, in plain words, before any figure

the owner asked, on 2026-09-10: "why isn't everything proven at least via the
method I've described with the primitives". The method is that a language
with `& | ^ ~`, a conditional and variables has every gate a processor is
built from, so every opcode's mapping is CONSTRUCTIBLE from them — and
whoever gets there first wins, the language's own operator when it has one
and the construction when it does not. Task t2 built eight hand-written
patterns for eight shapes. That is a set of patterns, not the method. This
task builds the method: ONE construction per OPERATION KIND — one node kind
of a term, named by z3's own declaration kind and never by a source token —
general in the width `n` and in the target's widest word `W`, proved once
per kind, and composed over the whole term by a render that gives every
node its own named local variable.

Three things were built and one was measured.

**Built, first: the constructions.** `build.py` is one function per kind
over the primitive set and nothing else — the adder by carry-lookahead in
log₂n rounds, the multiplier by shift-and-add in n rounds, divide and
remainder by restoring division in n rounds, the shifts by a barrel of
log₂n stages, the comparisons by the borrow of a subtraction, the signed
kinds by their unsigned kind and a sign fix, and the float kinds by the
softfloat algorithms over the integer ones. There is no case per opcode
name anywhere in it; every branch is on a z3 declaration kind or on a
width.

**Built, second: a way to STATE a construction as a theorem.** Task t2
recorded this as owed, in its own words
(`construct/lean/OWED.md` §3): a theorem's statement is the term WRITTEN
OUT, a printed term names no intermediate, and restoring division reads
its own previous remainder three times per step — so the statement grows
like 3^width, and the divider's lemma was not even stateable.
`lean_general.py` is that translation: it walks the z3 node and writes one
Lean `let` per DISTINCT node. The size it makes possible is the whole
point, and it is measured rather than argued — the multiplier at 8 bits is
190 distinct nodes and at or above 200,000 nodes WRITTEN OUT.

**Built, third: the general render.** `render_general.py` writes any term
into any target as a sequence of named intermediates, one local per node,
offering each node to the target's own renderer first and the construction
where the renderer refuses. That is task t3's item, done here because this
task could not proceed without it.

**Measured: where each obligation stops.** The table that answers the owner's
question is section 4: every place without a proof sits in a row with a
named cause, and the causes are few and specific.

---

## §1. The first implementer's five lanes, unchanged

These are the lanes the first implementer ran before it was cut off. They
are its measurement and are reported here as it left them.

### §1.1 Lane 1 — the stores this task reads, and the vocabulary

Lane log (tower):
`<runs>/t4/agent/logs/20260910T222246Z__t4_l1_the_vocabulary_and_the_stores.sh.log`,
`state=done exit=0` in 10.3 s.

Table 1.1 — the sha256 of every store this task reads, recorded before
anything ran. **LITERAL**, step [1/6].

```
40df3b55455f8d7a6e35ef04b7219701b957af65ad08f4d81fd550d911525e72  PseudoCoupHQ/Research/op_pipeline/reference.py
dae7048aebcbfc0be2de40cd17f36342880eae7be4bd89f992ed10d62d383429  PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json
f146dcba5893bac47bf00b2f0a97f7944fd19d86f3db22749b69b6b7599dfcd8  PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json
8b27c79cccc7d77e24cdb821a6e4c7de55bbd64be47494b67dd95c3d200ceda1  PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5_cells.json
bfd80360c0afdb4e6d2d227d6ea399f9781fcd0671dc121d676c18e02c2d49b8  PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl
29471177fa252ed8493297aa8f4d73886dc2d46f3a82f6d9dfe92d194609d17a  PseudoCoupHQ/Research/oracle/cross_construction/emulation/emulate.py
42125df2c847eb305a965e7dcea0c3516629b6eb1ede72a9833b94c944d60141  PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py
4153c9430c5c0a353315a83cf954813547a2c79c8ccf183bb771515e85efdab7  PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/schemas.py
c0b0ad39bb5051f3683a19f98cee4dda88e1755a0e979693821382653185542e  PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/construct.py
9c7f211689f079e774219febb6704b59cb3afde2213ac2e1f0982e87d0f508f0  PseudoCoupHQ/Research/oracle/riscv/model_table_rv.json
6b9e57ec07a2daef1f546f52f5da6d5c67acc28e15926dce8fd933ee46aa6b87  PseudoCoupHQ/Research/oracle/riscv/riscv_reference.py
3ebdad9e3313c8663d9ac8cf0701ffb47801ce53dcc7e31a2c10701ad1dd473e  PseudoCoupHQ/Research/oracle/riscv/twins.json
c4415a562f77c8817f117b27d3f437992d96b419c4617620b4d1f8fe41e588e6  PseudoCoupHQ/Research/oracle/riscv/attest_rv.json
4b41ab0de691e01b6d4ac6c27b80f5f536eb6071f76320c5dfd86f1df97c063c  PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl
```

**WHICH REFERENCE THIS IS, and it matters because task ref2 closed while
this task ran.** `40df3b55…` IS the CORRECTED `reference.py` — the one
task ref2 left after its four corrections
(`PRIVATE/PseudoCoupHQ/DevComms/log_261_task_ref2_correcting_level0.md`),
under which level 0 disagrees with the independent reading at NONE of
1,779 written places. The laptop's copy of the same file hashes
`2aac0220275572f21f36a92ea5cdddf51e6ed863758dc0060ff4b2705f49e56c` and
differs from the tower's in FOUR LINES, all of them documentation paths
rewritten by the repository move of 2026-09-10 16:00 EDT; the diff is in
section 8.1 and nothing it changes is executed. So every term this task
read is the corrected machine's, and no store was switched mid-pass.

**WHICH STORES ARE THE OLD ONES, said plainly.** `model_table.json`
(`dae7048a…`) and `model_table_rows.json` (`f146dcba…`) are the tables as
they stood BEFORE ref2 re-derived them; ref2 wrote the re-derived rows
BESIDE them as
`Research/oracle/arch_opcodes/level0/model_table_rows_ref2_c4.json`
(sha256 `43433ae26c2b231f41eff3d5dfa14a4fb588a32d96391c61ad451df9ddfd221e`)
and `…/model_table_attest_ref2_c4.json`
(`7b8021a9a95d793e157db44f0f1ed136322ff271bcbfbec16690d7ff589ac337`).
The driver's outer set for this pass is `autopoly5_cells.json`, whose
terms are rebuilt from the reference at run time, so the pass computes on
the CORRECTED reference throughout; the two old table files are read by
`model_table.py` for row bookkeeping only. The bank's delta on the
re-derived rows is the next pass and is named in section 9.

Table 1.2 — the x86 cells' node vocabulary, step [2/6]. 253 asked cells,
1,199 written places walked. **LITERAL**, the first ten rows of the
lane's own table:

| the kind, as z3 declares it | nodes | the widths it occurs at |
|---|---|---|
| seed (an arrival) | 2386 | 64(1897), 79(72), 128(417) |
| extract | 2208 | 1(386), 2(8), 8(733), 15(2), 16(55), 32(593), 48(18), 56(216), 64(183), 96(14) |
| numeral | 1130 | 1(194), 8(605), 16(3), 32(165), 48(1), 56(1), 62(8), 63(4), 64(148), 96(1) |
| concat | 631 | 16(218), 32(12), 64(362), 94(2), 128(37) |
| = | 435 | 1(435) |
| if | 405 | 8(196), 32(96), 64(113) |
| bvand | 288 | 8(149), 16(1), 32(85), 64(53) |
| bvsub | 227 | 8(84), 9(40), 16(1), 32(23), 33(20), 64(33), 65(26) |
| zero_extend | 208 | 9(25), 16(5), 32(15), 33(4), 64(139), 65(10), 128(10) |
| sign_extend | 180 | 9(78), 16(3), 32(5), 33(38), 64(4), 65(50), 128(2) |

The whole table is
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/vocabulary_x86.json`;
the RISC-V one (255 cells, 255 written places) is `vocabulary_riscv64.json`
beside it.

Table 1.3 — the word each target has, off that target's own renderer
table, step [4/6]. **LITERAL**.

| target | the word, off its own renderer table |
|---|---|
| c | 128 |
| cpp | 128 |
| rust | 128 |
| go | 64 |
| swift | 64 |

Table 1.4 — the bank's population, step [5/6]. 24,758 certificates, 3,075
distinct (cell, target) pairs. **LITERAL**, the five compiled targets:

| target | preferred certificates by kind |
|---|---|
| c | proved 452; proved_under_caller_extension 49; refused 604; sat 184; undecided 11 |
| cpp | proved 440; proved_under_caller_extension 48; refused 526; sat 182; undecided 3 |
| go | proved 443; refused 657; sat 178; undecided 22 |
| rust | proved 412; proved_under_caller_extension 53; refused 639; sat 183; undecided 13 |
| swift | proved 412; proved_under_caller_extension 46; refused 653; sat 168; undecided 21 |

### §1.2 Lanes 2 to 5 — every construction put to z3 on its own

Each lane asked z3, for one operation kind at one width over one word,
whether the construction and z3's OWN operator can differ on any input, at
the brief's hard 30-second ceiling. A DISPROVED row is a defect in this
task's own construction and was fixed with the row shown.

Table 1.5 — the four lanes, their populations and their outcomes.

| lane | tower log | what it posed | outcome counts |
|---|---|---|---|
| `t4_l2_the_constructions_smoke.sh` | `20260910T224257Z__t4_l2_…log`, exit 0 in 4.2 s | the integer kinds at (4,4), (6,4), (8,8); the float kinds at (3,4) and (4,5) | integers PROVED 102; floats DISPROVED 4, PROVED 20, REFUSED 12 |
| `t4_l3_the_constructions_smoke_again.sh` | `20260910T224531Z__t4_l3_…log`, exit 0 in 4.1 s | the same, after the float sign and absolute-value constructions were corrected | integers PROVED 102; floats PROVED 24, REFUSED 12 |
| `t4_l4_the_float_constructions_tiny.sh` | `20260910T224617Z__t4_l4_…log`, exit 0 in 503.7 s | the integer kinds at eight (width, word) pairs up to (16,16); the float kinds at (3,4) and (4,5) with the rounding mode admitted | integers PROVED 258, UNDECIDED 14; floats PROVED 29, DISPROVED 7 |
| `t4_l5_the_float_constructions_after_the_correction.sh` | `20260910T225801Z__t4_l5_…log`, exit 0 in 236.0 s | the float kinds at (3,4), (4,5) and at the half format (5,11) | tiny PROVED 36; half PROVED 16, UNDECIDED 2 |

**GLOSS on what those four lanes bought.** The float constructions were
wrong three times and right the fourth, and each wrongness was a
counterexample z3 handed back, never a guess: first the sign and absolute
value at every format, then the rounding mode (the file states the
constructions at round-to-nearest-ties-to-even and refused any other
rather than pretending), then multiply, divide and both integer-to-float
conversions. After the fourth lane every float kind at the two tiny
formats and at the half format is PROVED except multiply and divide at the
half format, which z3 leaves UNDECIDED.

Table 1.6 — the fourteen integer rows lane 4 left UNDECIDED, which is the
first appearance of the wall this whole task meets. **LITERAL**, lane 4
step [1/3], the six at (16,16):

| kind | shape | word | outcome | nodes | seconds |
|---|---|---|---|---|---|
| multiply | bvmul_w16 | 16 | UNDECIDED | 454 | 30.051 |
| divide unsigned | bvudiv_w16 | 16 | UNDECIDED | 1699 | 30.497 |
| remainder unsigned | bvurem_w16 | 16 | UNDECIDED | 1657 | 30.579 |
| divide signed | bvsdiv_w16 | 16 | UNDECIDED | 1785 | 30.526 |
| remainder signed | bvsrem_w16 | 16 | UNDECIDED | 1742 | 30.605 |
| modulo signed | bvsmod_w16 | 16 | UNDECIDED | 1781 | 30.948 |

---

## §2. The objects this task added, one sentence each, in relation

- **A construction** is one function of `build.py`: one operation kind at
  width `n` over a word `W`, written as a sequence of steps over limbs
  using `& | ^ ~`, shifts by CONSTANTS, `Extract`, `Concat`, a conditional
  and variables, and nothing else.
  (`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/build.py`)
- **The general render** is `render_general.render`: one term written into
  one target as a sequence of NAMED INTERMEDIATES, one local variable per
  distinct node, each node offered to the target's own renderer first and
  answered by a construction where the renderer refuses.
  (`.../general/render_general.py`)
- **The two policies** are `native_first` — the brief's own rule, the
  language's own operator wherever it has one — and `all_constructed`,
  where the construction answers every node whose kind has one. The second
  is the GUARANTEE's own measurement; both are attempted per place and
  whichever proves is the one kept.
- **The Lean printer** is `lean_general.py`: the same walk, writing one
  `let` per distinct node in Lean instead of in a target language, so a
  construction can be STATED as a theorem at all.
- **The lemma runner** is `run_lemmas_t4.py`: one `lean` process per
  theorem, one theorem per SHAPE of each kind at each (width, word) the
  census names. (`.../general/run_lemmas_t4.py`)
- **The census** is `kind_census.json`: every (operation kind, width) the
  x86 and riscv64 stores actually use, counted — the brief's own
  definition of `operation kind`, read off the stores rather than
  recalled.
- **The proof table** is `construction_proofs.json`: one row per
  (kind, width, word) saying which form proved that construction — `lemma`
  where a Lean theorem closed, `sat` where every z3 shape of it proved,
  and no form otherwise with the outcome that stopped it named.
- **The tier** is `general.py`: the driver's one call, running the native
  route as task ap6 left it and then the general tier under both policies,
  with TWO obligations per place — the GATE (does the carved body equal
  the term the render wrote?) and the EQUALITY (is that term the CELL's
  own?).

---

## §3. The four defects this task found in its own machinery, each with its measurement

Every one of the four was found by a lane and fixed with the lane's own
output in hand. None was worked around.

### §3.1 The go symbol was spelled without its package

**THE SYMPTOM.** Every go source the general render wrote BUILT and then
carved to nothing. Lane `t4_l7_the_compile_refusal_and_the_cost.sh` step
[1/4], **LITERAL**:

```
THE COMPILE REFUSED, LITERAL: objdump found no symbol emu_adc_gpr_gpr_64__reg_rdi__go__all_constructed
the source written: src_t4_general/adc_gpr_gpr_64__reg_rdi__go__all_constructed.go
```

**THE CAUSE.** `go_render.GoRenderer.render` returns its symbol as
`"main.%s" % symbol` because go's linked executable spells a package
function that way, and every other target's renderer returns the bare
name. `render_general.assemble` returned the bare name for go too.

**THE FIX AND ITS EVIDENCE.** One line. Lane
`t4_l8_the_symbol_and_where_the_memory_goes.sh` step [2/5] then carved
11,487 instructions out of the same cell.

### §3.2 The canonical form printed a term that names no intermediate

**THE SYMPTOM.** `adc gpr_gpr 64` on go was lost to a wall clock in five
lanes running (6, 7, 8, 9, 10), at 900 s each, with the process holding
82 MB and burning CPU.

**THE CAUSE.** The equality's first form compares two texts under the
pipeline's own normaliser, and `term.one_line` ends by writing the term
out — a step read three times is written three times. A constructed term
is nothing but such steps.

**THE FIX.** The printed form is attempted only where the render
CONSTRUCTED NOTHING, and then only under task t2's own written-out ceiling
of 200,000 nodes (`construct.UNFOLDED_CEILING`). Where the render
constructed something the question is whether each construction is the
operation it replaced, which the kind lemma answers; a construction and an
operation never print the same text.

### §3.3 The gate is what runs out, and it is measured rather than assumed

**THE MEASUREMENT.** Lane `t4_l9_the_census_and_the_stages.sh` steps [2/7]
and [3/7] take one cell through the tier one stage at a time. **LITERAL**:

```
  place reg_rax, 64 bits
    the cell's term: 7 distinct nodes
    all_constructed: rendered 19592 statements (19592 before the dead were dropped), 0 native nodes, 4 constructed nodes, in 2.1 s; resident 88832 kB
      the term the render wrote: 19728 distinct nodes
      the source: 2828751 bytes, 19603 lines
      compiled and carved: 20109 instructions in 6.1 s; resident 90088 kB
```

**GLOSS.** The render is cheap (2.1 s, 88 MB) and the compile is cheap
(6.1 s, 90 MB). It is the GATE — lifting a body of twenty thousand
instructions through the reference and posing it — that grows past the
instance's memory. So the tier states a ceiling on the carved body it
offers the gate, 4,000 instructions, and a body above it is recorded as
CONSTRUCTED, COMPILED and CARVED with its instruction count and its
landing, and NOT GATED, with the count on the row. That is the gate's cost
and it is a row with a named cause.

### §3.4 The fallback statement was bounded by the wrong number

**THE SYMPTOM.** The lemma runner was stopped by the operating system at
the multiplier at 16 bits, three lanes running (11, 12, 13), exit 137,
taking the ten theorems that had already closed with it.

**THE CAUSE, located.** Lane `t4_l13_the_lemmas_with_the_shell_bound.sh`
step [1/4] ran `lean` on that very file under `ulimit -v 4194304`.
**LITERAL**:

```
construction_multiply_w16_u64__bvmul_w16.lean:441:2: error: The SAT solver timed out while solving the problem.
```

So the `lean` process was never what grew. What grew was this task's own
process: a theorem whose `let` form Lean refuses is then offered WRITTEN
OUT, and the ceiling on that was read off the DISTINCT node count instead
of the written-out one.

**THE TWO NUMBERS, side by side.** Lane
`t4_l14_the_lemmas_with_the_unfolded_ceiling.sh` step [1/4], **LITERAL** —
and this table is the whole reason `lean_general.py` exists:

| the construction | word | distinct nodes | nodes WRITTEN OUT (ceiling 200000) |
|---|---|---|---|
| add at 8 | 64 | 25 | 152 |
| multiply at 8 | 64 | 190 | 200000 (at or above the ceiling) |
| divide unsigned at 8 | 64 | 339 | 200000 (at or above the ceiling) |
| shift left at 8 | 64 | 60 | 392 |
| add at 16 | 64 | 31 | 360 |
| multiply at 16 | 64 | 454 | 200000 (at or above the ceiling) |
| divide unsigned at 16 | 64 | 742 | 200000 (at or above the ceiling) |
| shift left at 16 | 64 | 74 | 864 |
| add at 32 | 64 | 37 | 840 |
| multiply at 32 | 64 | 1062 | 200000 (at or above the ceiling) |
| divide unsigned at 32 | 64 | 1625 | 200000 (at or above the ceiling) |
| shift left at 32 | 64 | 88 | 1872 |
| add at 64 | 64 | 43 | 1928 |
| multiply at 64 | 64 | 2438 | 200000 (at or above the ceiling) |
| divide unsigned at 64 | 64 | 8839 | 200000 (at or above the ceiling) |
| shift left at 64 | 64 | 102 | 4016 |

---

## §4. The census, and the lemma per operation kind

### §4.1 The census — the brief's own definition of `operation kind`

Lane `t4_l9_the_census_and_the_stages.sh` step [1/7] (tower log
`<runs>/t4/agent/logs/20260911T014118Z__t4_l9_the_census_and_the_stages.sh.log`)
walks every written place of both architectures' stores and counts every
node that HAS a construction, at the width its proof row is keyed by:
1,199 x86 written places and 255 RISC-V ones, **98 distinct (operation
kind, width)**. The whole table is
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/kind_census.json`.

Those 98 become **113 (kind, width, word) instances**: a width at or
under 64 is posed ONCE, because `build.unit_for` gives a value of `n`
bits a unit of `n` where `n <= W`, so at those widths the construction
over a word of 64 and over a word of 128 is the same term node for
node; above 64 the two differ and both are posed. Spread over the words
they cover, the instances are 196 rows.

### §4.2 The lemma per kind — 132 of 196 instances closed by Lean

Reproducing command, from the instance:
`python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/run_lemmas_t4.py prove 90 1 2`
(and `... 2 2`). Lane
`t4_l14_the_lemmas_with_the_unfolded_ceiling.sh`, tower log
`<runs>/t4/agent/logs/20260911T022917Z__t4_l14_the_lemmas_with_the_unfolded_ceiling.sh.log`,
`state=done exit=0` in 622.8 s. Toolchain, **LITERAL**: `Lean (version
4.24.0, x86_64-unknown-linux-gnu, commit
797c613eb9b6d4ec95db23e3e00af9ac6657f24b, Release)`. The budget is 90 s
per theorem and is this task's own; one `lean` process per theorem,
bounded at 4 GB of address space by the shell that starts it.

Table 4.1 — the 196 (kind, width, word) instances by the outcome of the
theorem stated over them. 263 theorems were run, one per SHAPE of each
instance, and an instance is PROVED_BY_LEAN only where every shape of it
is.

| the instance's outcome | instances |
|---|---|
| PROVED_BY_LEAN | 132 |
| LEAN_REFUSED | 40 |
| REFUSED_BEFORE_LEAN | 24 |

Table 4.2 — which OPERATION KINDS those are. Every integer kind the
census names is proved by a Lean lemma at every width the two stores
use, except multiply and the four divide/remainder kinds; the float
kinds are not stated in Lean at all.

| operation kind | instances with a closed Lean lemma | instances without | why not, where not |
|---|---|---|---|
| add | 14 | 0 | -- |
| subtract | 14 | 0 | -- |
| negate | 8 | 0 | -- |
| bitwise over the word | 10 | 0 | -- |
| complement | 8 | 0 | -- |
| compare unsigned | 6 | 0 | -- |
| compare signed | 2 | 0 | -- |
| equality | 8 | 0 | -- |
| conditional | 6 | 0 | -- |
| shift left | 8 | 0 | -- |
| shift right logical | 10 | 0 | -- |
| shift right arithmetic | 8 | 0 | -- |
| wiring: widen, narrow, spread the sign, join | 30 | 0 | -- |
| multiply | 0 | 8 | `bv_decide`'s SAT solver times out |
| divide unsigned | 0 | 8 | the same |
| remainder unsigned | 0 | 8 | the same |
| divide signed | 0 | 8 | the same |
| remainder signed | 0 | 8 | the same |
| float arithmetic | 0 | 6 | no Lean form: `BitVec` carries no float operation |
| float compare | 0 | 4 | the same |
| float class | 0 | 4 | the same |
| float convert | 0 | 4 | the same |
| float wiring | 0 | 6 | the same |

**THE STATEMENT THAT COULD NOT BE MADE BEFORE, and it is task t2's own
owed item.** Every one of those 132 is stated with ONE `let` PER NODE.
`construct/lean/OWED.md` §3 records what was owed: "a way to STATE it —
a translation to Lean that names intermediates (`let`), which
`op_pipeline/lean/term_to_lean.py` does not do today". The barrel
shifter at 128 bits over a word of 128 closes in 3.301 s with 102
bindings; the adder at 65 bits over a word of 64 closes in 1.219 s with
122 bindings; the subtractor at 65 over 64 in 1.523 s with 129. Written
out, the same terms are past every ceiling — section 3.4's table.

**WHAT IS STILL OWED** is the GENERAL statement, one theorem per kind
over `BitVec w` for every `w`, and it is owed for the same reason task
t2 recorded: `bv_decide` decides a goal at a FIXED width and cannot be
handed a variable one. `OWED.md` carries it and this task does not
close it.

### §4.3 z3 as the fallback, at the instances no lemma closed

The brief's own order — "where a lemma does not close in the task's
budget, the instantiation is proved by z3 at every width the store
uses" — so z3 is asked only at the 39 instances no theorem closed.
Reproducing command:
`python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/check_constructions.py store_rest <i> 5`.
Lane `t4_l21_the_constructions_one_process_each_again.sh`, tower log
`<runs>/t4/agent/logs/20260911T050033Z__t4_l21_the_constructions_one_process_each_again.sh.log`.

**EACH OBLIGATION IS POSED IN A PROCESS OF ITS OWN, and the reason is
measured.** z3's `memory_max_size` raises once and then refuses
everything after it in the same process. Lane
`t4_l15_the_constructions_z3_fallback.sh` posed a whole part in one
process, and after the divider at 32 bits exhausted the bound every
later row in that part came back UNDECIDED in about zero seconds —
`fp_neg` at 79 bits among them, and that same obligation at the tiny
formats is PROVED in lane 5. Those rows say the solver could not decide
when what happened is that the solver was already out of memory. Lane
15's four part files are kept on disk and named in
`collect_proofs.SET_ASIDE` with that reason; lane 21's are what the
proof table reads.

Table 4.3 — the proof table, `construction_proofs.json`, 196 rows.

| the form of record | instances |
|---|---|
| lemma (a Lean theorem closed) | 132 |
| sat (every z3 shape of it PROVED) | 8 |
| none | 56 |

The 8 z3 rows are `float compare` at 64 over both words and `float
wiring` at 32 over both words, and `compare signed` and `wiring` at
widths lane 10's own slice had already posed.

---

## §5. The measurement

Reproducing commands, from the instance:

```
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/general.py run
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/general_report.py report
```

The pass's own store is
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/t4_general_runs.jsonl`:
**970 store lines, of which 304 are general-tier runs.** The report is
`.../construct/general/general.md` and `.../general_measurement.json`.
The lane of record is
`t4_l28_the_measurement_of_record_after_the_guard.sh`, tower log
`<runs>/t4/agent/logs/20260911T185712Z__t4_l28_the_measurement_of_record_after_the_guard.sh.log`.

**WHAT THE PASS DID NOT REACH, named and counted.** The preflight
(lane 9 step [6/7]) reads 2,159 keys the bank certifies, 4,080 keys
with no certificate, 0 held back by the code version, and 654 (cell,
target) runs to execute. Four of those runs are on
`t4_general_left_behind.json`, **LITERAL**:

```
[["setg", "gpr_one", 8, "rust"],
 ["imul", "gpr_gpr", 64, "c"],
 ["setge", "gpr_one", 8, "c"],
 ["setge", "gpr_one", 8, "cpp"]]
```

and the pass was stopped by this task after them, with the remaining
runs of the same shape unreached. The shape is one and the cause is
one: a FLAG CONSUMER carries one written place per SETTER cell —
seventeen of them for `setl`, `setg`, `setge` and their kin — and each
of those places pays the native route's own compile and gate and then
this tier's two policies, which is about 2,000 s per (cell, target).
That is longer than one attempt's own wall clock, so the lane's repeat
enters it, is cut inside it, and starts it again. The left-behind
mechanism takes the pass past one such run per attempt, which is
progress at one run per forty minutes; the measurement does not need
every one of them, because each is a row with a named cause and the
cause is the same for all of them.

### §5.1 Per operation kind: constructed, and how each is proved

Table 5.1 — THE TABLE THAT ANSWERS "why isn't everything proven". One
row per (operation kind, width, target) the render CONSTRUCTED a node
at. `places constructed` counts the written places; `proved` is the
gate answering PROVED_ON_SHIP with the equality discharged.

| operation kind | width | target | places constructed | nodes | proved | by lemma | by z3 | undecided | refused |
|---|---|---|---|---|---|---|---|---|---|
| add | 64 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| add | 64 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| add | 65 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| add | 65 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| multiply | 64 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| multiply | 64 | swift | 1 | 2 | 0 | 0 | 0 | 0 | 1 |
| divide unsigned | 128 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| remainder unsigned | 128 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| divide signed | 128 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| remainder signed | 128 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| bitwise over the word | 8 | c | 12 | 12 | 12 | 12 | 0 | 0 | 0 |
| bitwise over the word | 8 | cpp | 12 | 12 | 12 | 12 | 0 | 0 | 0 |
| bitwise over the word | 8 | rust | 12 | 12 | 12 | 12 | 0 | 0 | 0 |
| complement | 8 | c | 6 | 18 | 6 | 6 | 0 | 0 | 0 |
| complement | 8 | cpp | 6 | 18 | 6 | 6 | 0 | 0 | 0 |
| complement | 8 | rust | 6 | 18 | 6 | 6 | 0 | 0 | 0 |
| equality | 1 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| equality | 1 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| equality | 8 | c | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| equality | 8 | cpp | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| equality | 8 | rust | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| conditional | 8 | c | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| conditional | 8 | cpp | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| conditional | 8 | rust | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| conditional | 64 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| conditional | 64 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 1 | go | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 1 | swift | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 8 | c | 20 | 32 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 8 | cpp | 20 | 32 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 8 | rust | 20 | 32 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 56 | c | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 56 | cpp | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 56 | rust | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 64 | c | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 64 | cpp | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 64 | go | 4 | 4 | 0 | 0 | 0 | 0 | 4 |
| wiring: widen, narrow, spread the sign, join | 64 | rust | 20 | 20 | 20 | 20 | 0 | 0 | 0 |
| wiring: widen, narrow, spread the sign, join | 65 | go | 1 | 2 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 65 | swift | 1 | 2 | 0 | 0 | 0 | 0 | 1 |
| wiring: widen, narrow, spread the sign, join | 128 | go | 4 | 8 | 0 | 0 | 0 | 0 | 4 |

**GLOSS, and it is the owner's answer.** 246 of the 268 constructed places are
PROVED, and every one of the 246 is proved **by the kind's own Lean
lemma** — the solver never decided a single one of them. The 22 that
are not sit in four causes and no fifth, and section 5.2 is the causes.

Table 5.2 — the cause on every row that is not proved, **LITERAL**.

| operation kind | width | target | the cause | places |
|---|---|---|---|---|
| add | 64 | go | no cause | 1 |
| add | 64 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| add | 65 | go | no cause | 1 |
| add | 65 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| multiply | 64 | go | no cause | 1 |
| multiply | 64 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| divide unsigned | 128 | go | the carved body is larger than the number of instructions this task's gate is offered | 1 |
| remainder unsigned | 128 | go | the carved body is larger than the number of instructions this task's gate is offered | 1 |
| divide signed | 128 | go | the carved body is larger than the number of instructions this task's gate is offered | 1 |
| remainder signed | 128 | go | the carved body is larger than the number of instructions this task's gate is offered | 1 |
| equality | 1 | go | no cause | 1 |
| equality | 1 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| conditional | 64 | go | no cause | 1 |
| conditional | 64 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| wiring: widen, narrow, spread the sign, join | 1 | go | no cause | 1 |
| wiring: widen, narrow, spread the sign, join | 1 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| wiring: widen, narrow, spread the sign, join | 64 | go | the carved body is larger than the number of instructions this task's gate is offered | 4 |
| wiring: widen, narrow, spread the sign, join | 65 | go | no cause | 1 |
| wiring: widen, narrow, spread the sign, join | 65 | swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged by any of the three forms | 1 |
| wiring: widen, narrow, spread the sign, join | 128 | go | the carved body is larger than the number of instructions this task's gate is offered | 4 |

Table 5.3 — the EQUALITY's form over every place the tier rendered, per
target. The kind lemma is the form of record for every constructed
place that proved; the canonical form is the places the render wrote
the cell's own term at.

| target | the equality's form | its outcome | places |
|---|---|---|---|
| c | canonical | PROVED | 74 |
| cpp | canonical | PROVED | 71 |
| rust | canonical | PROVED | 59 |
| swift | canonical | PROVED | 53 |
| c | kind | PROVED | 20 |
| cpp | kind | PROVED | 20 |
| rust | kind | PROVED | 20 |
| go | canonical | PROVED | 13 |
| go | (none) | (none) | 5 |
| swift | (none) | UNDECIDED | 1 |

Table 5.4 — where the tier DECLINED to render at all, by cause,
**LITERAL**. Both causes are about the native route and neither is
about a construction.

| target | the cause | places |
|---|---|---|
| c | the native route did not reach this place's term at all, so the tier has nothing to render | 72 |
| cpp | the native route did not reach this place's term at all, so the tier has nothing to render | 72 |
| rust | the native route did not reach this place's term at all, so the tier has nothing to render | 58 |
| swift | the native route did not reach this place's term at all, so the tier has nothing to render | 37 |
| c | the native route proved this place, so there is nothing the general tier can add | 9 |
| cpp | the native route proved this place, so there is nothing the general tier can add | 9 |
| swift | the native route proved this place, so there is nothing the general tier can add | 9 |
| rust | the native route proved this place, so there is nothing the general tier can add | 7 |
| go | the native route proved this place, so there is nothing the general tier can add | 7 |

### §5.2 The gate's own outcome over every rendered place

Table 5.5 — **LITERAL**, per target.

| target | the gate's own outcome | places |
|---|---|---|
| c | DISPROVED | 58 |
| cpp | DISPROVED | 58 |
| rust | DISPROVED | 47 |
| c | PROVED_ON_SHIP | 28 |
| cpp | PROVED_ON_SHIP | 28 |
| rust | PROVED_ON_SHIP | 28 |
| swift | UNDECIDED | 27 |
| swift | DISPROVED | 16 |
| swift | PROVED_ON_SHIP | 10 |
| go | PROVED_ON_SHIP | 8 |
| c | UNDECIDED | 8 |
| cpp | UNDECIDED | 5 |
| go | UNDECIDED | 5 |
| go | the carved body is larger than the number of instructions this task's gate is offered | 4 |
| rust | UNDECIDED | 4 |
| go | no verdict | 1 |
| swift | the carved body is proved equal to the term the render wrote, and that term's equality with the CELL's own is not discharged | 1 |

---

## §6. The three readings and the collapse column

### §6.1 The three readings, beside task t2's

Reproducing command, from the instance:
`python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/general.py readings`.
The bank was rebuilt first with BOTH the construct tier's pass and this
one registered — neither is in `bank.PASSES`'s own file and each
registers itself from outside, so a rebuild with only one registered
would write a bank with the other's proofs missing. 14 passes, 8,179
keys, **26,177 certificates**.

Table 6.1 — cells on all four compiled targets (c, rust, go, swift),
under each reading, out of the 205 the population counts over.

| reading | task t2 left it at | this task leaves it at | moved |
|---|---|---|---|
| strict | 96 | **96** | 0 |
| destination-only | 154 | **154** | 0 |
| corpus-needed | 141 | **141** | 0 |

Table 6.2 — the bank's own pair counts, where the movement is.

| reading | task t2 left it at | this task leaves it at | moved |
|---|---|---|---|
| strict | 2,007 | **2,015** | +8 |
| destination-only | 2,265 | **2,273** | +8 |
| corpus-needed | 2,221 | **2,229** | +8 |

and this pass's own contribution, off the bank: `t4_general` 21 strict /
79 destination-only / 64 corpus-needed, over 93 pairs and 12 cells on
all four.

**GLOSS, said plainly.** The tier proved 246 constructed places and
banked eight more (cell, target) pairs than the bank held before, and
the three readings over CELLS did not move at all. The reason is the
shape of what is left, not the tier: a cell counts in those three
readings only when all four targets have it, and what the tier reaches
is places on targets that were already the ones holding out — the
eight new pairs land on cells where another target is still refused at
the ARRIVAL or the ANSWER HOME, which is a question about the arrival
contract and not about any operation. Section 5.4's decline table is
that population: 239 places over the five targets where the native
route never reached the term at all.

### §6.2 The collapse column

the owner's compiler question on the general tier: did the compiler turn the
constructed source back into the one instruction the cell names?

Table 6.3 — per constructed certificate, **LITERAL**.

| target | landing | places | instructions, summed | instructions, mean |
|---|---|---|---|---|
| c | LANDED | 6 | 17 | 2.8 |
| c | LANDED_ELSEWHERE | 3 | 6 | 2.0 |
| c | NOT_COLLAPSED | 85 | 1116 | 13.1 |
| cpp | LANDED | 6 | 17 | 2.8 |
| cpp | LANDED_ELSEWHERE | 2 | 4 | 2.0 |
| cpp | NOT_COLLAPSED | 83 | 1108 | 13.3 |
| go | IDENTITY | 2 | 2 | 1.0 |
| go | LANDED | 5 | 10 | 2.0 |
| go | LANDED_ELSEWHERE | 2 | 4 | 2.0 |
| go | NO LANDING RECORDED | 1 | 0 | 0.0 |
| go | NOT_COLLAPSED | 8 | 154395 | 19299.4 |
| rust | LANDED | 6 | 17 | 2.8 |
| rust | LANDED_ELSEWHERE | 2 | 4 | 2.0 |
| rust | NOT_COLLAPSED | 71 | 1118 | 15.7 |
| swift | LANDED | 4 | 11 | 2.8 |
| swift | LANDED_ELSEWHERE | 28 | 31 | 1.1 |
| swift | NOT_COLLAPSED | 22 | 130 | 5.9 |

**GLOSS.** LANDED 27, LANDED_ELSEWHERE 37, IDENTITY 2, NOT_COLLAPSED
269, one place with no landing recorded. The compiler collapses a
construction back to the instruction it stands for in 27 places of 336
and does not in 269; and the go column is where the shape of the answer
is visible — eight NOT_COLLAPSED places carrying 154,395 instructions
between them, a mean of 19,299, because those are the 128-bit divides
and remainders written out of `& | ^ ~` on a target whose widest word
is 64.

**THE CARVED BODY OF ONE OF THEM, LITERAL**, so the claim is on the
page: `adc gpr_gpr 64` on go, the adder at 65 bits constructed into 185
named intermediates and compiled to 132 instructions, from lane
`t4_l20` step [2/4] — and there is no `add` anywhere in it:

```
mov %rbx,%rdx; xor %rax,%rbx; lea (%rbx,%rbx,1),%rsi; and %rbx,%rsi;
mov %rsi,%r8; shl $0x2,%rsi; and %r8,%rsi; mov %rsi,%r9; shl $0x4,%rsi;
and %r9,%rsi; mov %rsi,%r10; shl $0x8,%rsi; and %r10,%rsi; mov %rsi,%r11;
shl $0x10,%rsi; and %r11,%rsi; and %rax,%rdx; lea (%rdx,%rdx,1),%r12;
and %rbx,%r12; or %r12,%rdx; ... ; lea (%rdx,%rdx,1),%rcx; xor %rcx,%rax; ret
```

### §6.3 The size of the constructed sources

Table 6.4 — statements written, per target and policy.

| target | policy | places | statements, summed | statements, mean | the largest | instructions, summed |
|---|---|---|---|---|---|---|
| c | all_constructed | 20 | 362 | 18.1 | 21 | 290 |
| c | native_first | 74 | 671 | 9.1 | 22 | 849 |
| cpp | all_constructed | 20 | 362 | 18.1 | 21 | 290 |
| cpp | native_first | 71 | 667 | 9.4 | 22 | 839 |
| go | native_first | 18 | 112156 | 6230.9 | 27642 | 154411 |
| rust | all_constructed | 20 | 362 | 18.1 | 21 | 290 |
| rust | native_first | 59 | 429 | 7.3 | 19 | 849 |
| swift | all_constructed | 1 | 4727 | 4727.0 | 4727 | 1 |
| swift | native_first | 53 | 491 | 9.3 | 31 | 171 |

Table 6.5 — the largest by (kind, width, target), which is where the
cost is.

| operation kind | width | target | places | statements, summed | the largest |
|---|---|---|---|---|---|
| divide signed | 128 | go | 1 | 27642 | 27642 |
| remainder signed | 128 | go | 1 | 27461 | 27461 |
| divide unsigned | 128 | go | 1 | 27322 | 27322 |
| remainder unsigned | 128 | go | 1 | 27142 | 27142 |
| add | 64 | swift | 1 | 4727 | 4727 |
| add | 65 | swift | 1 | 4727 | 4727 |
| multiply | 64 | swift | 1 | 4727 | 4727 |
| add | 64 | go | 1 | 2553 | 2553 |
| add | 65 | go | 1 | 2553 | 2553 |
| multiply | 64 | go | 1 | 2553 | 2553 |

### §6.4 The gate's cost where it runs out

Table 6.6 — every (kind, width, word) with NO proof of record, with the
seconds the attempt actually took. The ceiling asked for is the brief's
hard 30 seconds and was never raised; z3's own `timeout` is checked
between propagations and NOT during bit-blasting, so a wide multiply or
divide overshoots it, and what the row records is the seconds actually
spent before the solver's 4 GB memory bound answered.

| operation kind | width | word | outcome | the form actually used | seconds |
|---|---|---|---|---|---|
| multiply | 16 | 64 | UNDECIDED | none | 30.051 |
| multiply | 32 | 64 | UNDECIDED | none | 30.423 |
| multiply | 64 | 64 | UNDECIDED | none | 32.461 |
| multiply | 128 | 64 | UNDECIDED | none | 129.975 |
| multiply | 128 | 128 | UNDECIDED | none | 439.573 |
| divide unsigned | 16 | 64 | UNDECIDED | none | 31.137 |
| divide unsigned | 32 | 64 | UNDECIDED | none | 106.638 |
| divide unsigned | 64 | 64 | UNDECIDED | none | 1542.784 |
| divide unsigned | 128 | 64 | UNDECIDED | none | 1474.09 |
| divide unsigned | 128 | 128 | UNDECIDED | none | 1556.813 |
| remainder unsigned | 16 | 64 | UNDECIDED | none | 30.996 |
| remainder unsigned | 32 | 64 | UNDECIDED | none | 261.364 |
| remainder unsigned | 64 | 64 | UNDECIDED | none | 1047.892 |
| remainder unsigned | 128 | 64 | UNDECIDED | none | 937.37 |
| remainder unsigned | 128 | 128 | UNDECIDED | none | 1345.92 |
| divide signed | 16 | 64 | UNDECIDED | none | 30.857 |
| divide signed | 32 | 64 | UNDECIDED | none | 97.601 |
| divide signed | 64 | 64 | LEAN_REFUSED, z3 not reached | none | 0.0 |
| divide signed | 128 | 64 | LEAN_REFUSED, z3 not reached | none | 0.0 |
| remainder signed | 16 | 64 | UNDECIDED | none | 30.935 |
| remainder signed | 32 | 64 | UNDECIDED | none | 221.306 |
| remainder signed | 64 | 64 | LEAN_REFUSED, z3 not reached | none | 0.0 |
| remainder signed | 128 | 64 | LEAN_REFUSED, z3 not reached | none | 0.0 |
| float arithmetic | 32 | 64 | UNDECIDED | none | 2977.221 |
| float arithmetic | 64 | 64 | UNDECIDED | none | 1790.416 |
| float arithmetic | 79 | 64 | REFUSED_BEFORE_LEAN, z3 not reached | none | 0.0 |
| float compare | 32 | 64 | REFUSED_BEFORE_LEAN, z3 not reached | none | 0.0 |
| float class | 64 | 64 | REFUSED_BEFORE_LEAN, z3 not reached | none | 0.0 |
| float convert | 32 | 64 | REFUSED_BEFORE_LEAN, z3 not reached | none | 0.0 |
| float convert | 64 | 64 | REFUSED_BEFORE_LEAN, z3 not reached | none | 0.0 |
| float wiring | 79 | 64 | REFUSED_BEFORE_LEAN, z3 not reached | none | 0.0 |

(The rows at word 128 for widths at or under 64 are the same
obligations and the same seconds, per section 4.1's sharing rule, and
are elided here; `construction_proofs.json` carries all 196.)

Table 6.7 — places CONSTRUCTED, COMPILED and CARVED and NOT GATED,
because the carved body is above the 4,000 instructions this task's
gate is offered.

| target | places |
|---|---|
| go | 4 |
| swift | 1 |

---

## §7. The second architecture

Reproducing command, from the instance:

```
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/rv_general.py run \
  PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/op_pipeline \
  PseudoCoupHQ/Research/oracle/cross_construction/emulation \
  PseudoCoupHQ/Research/oracle/riscv/twins.json \
  PseudoCoupHQ/Research/oracle/riscv/model_table_rv.json \
  <prefix> <src> <work>
```

Lane `t4_l17_the_tier_on_riscv64.sh`, tower log
`<runs>/t4/agent/logs/20260911T062706Z__t4_l17_the_tier_on_riscv64.sh.log`,
`state=done exit=0` in 168.1 s. The x86 reference it imported is
`PseudoCoupHQ/Research/op_pipeline/reference.py`, sha256
`40df3b55455f8d7a6e35ef04b7219701b957af65ad08f4d81fd550d911525e72` —
the CORRECTED one; task rv2's own lane read the pre-correction reference
out of `level0/ref2_originals`, so the two runs are not read as one.

Population: the 94 RISC-V cells `twins.json` leaves untwinned, 188 runs
on c and go under both policies.

Table 7.1 — the census of those 188 runs.

| kind | runs |
|---|---|
| proved | 144 |
| refused | 23 |
| undecided | 13 |
| sat | 8 |

Table 7.2 — the count, beside task rv3's 117 of 255.

| what | cells | share of the 255 |
|---|---|---|
| RISC-V cells `twins.json` holds | 255 | 100% |
| reached by an INHERITED proved certificate, rv3 | 35 | 13.7% |
| PROVED by task rv2's own loop | 82 | 32.2% |
| union, rv3's headline | 117 | 45.9% |
| PROVED by THIS task's general tier | 84 | 32.9% |
| **union, the inheritance with rv2's loop and this tier** | **119** | **46.7%** |

Table 7.3 — the two cells ONLY the general tier reaches, and it is the
point of the whole task: they are divisions.

| cell | what it is |
|---|---|
| `divw` `gpr_gpr_gpr` 32 | a 32-bit signed divide |
| `remw` `gpr_gpr_gpr` 32 | a 32-bit signed remainder |

---

## §8. Discipline

### §8.1 The two spellings of the corrected reference

The tower's `reference.py` (sha256 `40df3b55…`, 121,685 bytes) and the
laptop's (`2aac0220…`, 121,725 bytes) differ in FOUR LINES, every one of
them a documentation path the repository move of 2026-09-10 16:00 EDT
rewrote. **LITERAL**, one of the four:

```
-(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/.../CORE_0_3_5_4_reference.md`).
+(`PseudoCoupHQ/Planning/node_0_3_research/.../CORE_0_3_5_4_reference.md`).
```

Nothing that is executed differs, and both carry all four of task ref2's
corrections.

### §8.2 The spelling guard

Lane `t4_l28_the_measurement_of_record_after_the_guard.sh` step [6/8],
23 files, **guard rc=0**, every one PASS. Reproducing command, from the
instance:
`python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py <the 23 files>`.

**THE GUARD REFUSED THREE FILES FIRST, and it was right all three
times** (lane `t4_l27` step [6/8]). `vocabulary_x86.json` and
`vocabulary_riscv64.json` carried the z3 DECLARATION NAME on a field
called `kind`, and four of those names — `=`, `and`, `not`, `or` — are
operator tokens on a structure field; the name now sits in the field
`mnem`, which the ruling of 2026-09-08 states is machine form and which
the guard exempts, and which is the same remedy task ref2 applied to
three of its own files. `general_measurement.json` carried `--` as the
landing of a place that has none, and `--` is a range in swift and in
ruby; a place with no landing recorded now says so in words. Nothing
about the guard was changed.

`grep -c exempt` over every file this task added: 0 on all eleven
(`build.py`, `check_constructions.py`, `collect_proofs.py`,
`general.py`, `general_report.py`, `lean_general.py`,
`render_general.py`, `run_lemmas_t4.py`, `rv_general.py`,
`sizes_probe.py`, `softfloat.py`).

### §8.3 Memory

Bound 6 GB resident, named abort `ABORT_MEMORY_T4`, checked after every
store line. Peak resident by lane: the census 68,868 kB; the lemmas
64,508 kB; the z3 fallback 4,173,812 kB (one obligation at the solver's
own 4 GB bound); the pass 1,358,192 kB; the RISC-V leg 231,632 kB; the
report 26,784 kB. The render's own bound is 4 GB resident read off
`/proc/self/statm`; the solver's is 4 GB (`memory_max_size`); one
`lean` process is bounded at 4 GB of address space by the shell that
starts it.

### §8.4 The three ABORTS this task met, each named

1. `Killed`, exit 137, on the 128-bit divide through c (lanes 6, 7, 8):
   located in lane 9 to the GATE, not the render or the compile, and
   answered with a stated ceiling on the carved body the gate is
   offered.
2. `Aborted (core dumped)`, exit 134, on the z3 fallback (lane 15 parts
   1 and 2): z3 raises at `memory_max_size` and its C++ side calls
   `terminate` if nothing catches it. Caught, it is an UNDECIDED row
   with the solver's own sentence on it.
3. `Segmentation fault`, exit 139, at run 109 of 654 (lane 23 attempt
   1): a signal handler that RAISES lands in whatever Python frame is
   running, and through z3's C frames that ends the process.
   `Context.interrupt` is z3's own way to stop a solver and nothing is
   raised anywhere.

---

## §8.5 The six commands this log can be checked against, re-run

Lane `t4_l30_the_transcripts.sh`, tower log
`<runs>/t4/agent/logs/<stamp>__t4_l30_the_transcripts.sh.log`.
Every line below is the command and the output it printed, in the form
the conventions verifier re-runs.

```
$ sha256sum PseudoCoupHQ/Research/op_pipeline/reference.py
40df3b55455f8d7a6e35ef04b7219701b957af65ad08f4d81fd550d911525e72  PseudoCoupHQ/Research/op_pipeline/reference.py
```

```
$ wc -l PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/t4_general_runs.jsonl
970 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/t4_general_runs.jsonl
```

```
$ python3 -c "import json;d=json.load(open(\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/construction_proofs.json\"));print(d[\"meta\"][\"forms\"])"
{'lemma': 132, 'none': 56, 'sat': 8}
```

```
$ python3 -c "import json;d=json.load(open(\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/kind_census.json\"));print(len(d[\"rows\"]))"
98
```

```
$ python3 -c "import json,collections;rows=[];[rows.extend(json.load(open(p))[\"rows\"]) for p in [\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/lemmas_t4_1_of_2.json\",\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/lemmas_t4_2_of_2.json\"]];print(sorted(collections.Counter(r[\"outcome\"] for r in rows).items()))"
[('LEAN_REFUSED', 40), ('PROVED_BY_LEAN', 132), ('REFUSED_BEFORE_LEAN', 24)]
```

```
$ python3 -c "import json,collections;rows=[json.loads(l) for l in open(\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/rv_general.jsonl\")];print(sorted(collections.Counter(r[\"kind\"] for r in rows).items()))"
[('proved', 144), ('refused', 23), ('sat', 8), ('undecided', 13)]
```

---

## §8.6 The conventions verifier, this log's own tally

Reproducing command, from the instance:
`python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_262_t4_the_general_construction_tier.md`.
Lane `t4_l31_the_verifier_again.sh`. **LITERAL**:

```
population: 26 claims across 1 logs
  MATCHES          6
  DIFFERS          0
  UNVERIFIABLE     20
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 6 of 26 claims reproduce; 20 (77%) carry nothing to re-run

causes, by name:
  prose_only                       11
  attribution_only                 7
  pasted_without_source            2
```

Zero DIFFERS. The first run of the verifier (lane `t4_l29`) found 20 of
20 UNVERIFIABLE and zero MATCHES; the six commands of section 8.5 were
then run in a lane of their own and their output pasted as a shell
transcript, which is what the verifier can re-run. The 20 that remain
are prose and attributions to lane logs, each of which names its lane
and its step.

---

## §9. The two lists

### Decided, recorded for audit

1. **The construction is keyed by the z3 declaration kind and by
   nothing else.** `build.py` has no case per opcode name anywhere in
   it; every branch is on a declaration kind or on a width. The census,
   the proof table, the lemma runner and the report are all keyed
   (kind, width, word) or (kind, width, target).
2. **A width at or under 64 is posed once.** `build.unit_for` makes the
   construction over a word of 64 and over a word of 128 the same term
   node for node at those widths; the row records the words it covers
   and the reason.
3. **The canonical form is not attempted where the render constructed
   anything.** A construction and the operation it replaces never print
   the same text, and printing one is the 3^width cost task t2's
   `OWED.md` is about.
4. **One gate call is bounded at 5 s and one (cell, target) run at
   900 s**, both by interrupting the solver and never by raising, both
   numbers off the pass's own store: of 443 gate calls that ANSWERED,
   the slowest took 0.099 s and the median 0.011 s.
5. **The carved body the gate is offered is bounded at 4,000
   instructions.** A body above it is CONSTRUCTED, COMPILED and CARVED
   with its count and its landing, and NOT GATED, with the count on the
   row.
6. **Lane 15's four part files are kept and not read**, named in
   `collect_proofs.SET_ASIDE` with the measured reason.
7. **Three stores of earlier attempts are kept beside the store of
   record** (`.before_the_gate_carried_its_own_record`,
   `.before_the_bounds_were_measured`, `.before_the_run_was_bounded`),
   each named for the bound that moved.
8. **The pass's loop version is this tier's own bytes**, set from
   outside the driver the way `autopoly.configure` sets its paths, so
   every uncertified key is attempted because the machinery HAS moved.

### Awaiting the owner

1. **The general lemma, one theorem per kind over `BitVec w` for every
   `w`.** `bv_decide` decides at a FIXED width; the general statement
   needs an induction over the limb count in `BitVec.toNat`
   arithmetic. It is stated in `construct/lean/OWED.md` and is a
   different piece of work. The 132 instances closed here are its
   instances at every width the two stores use.
2. **The flag-consumer shape.** A cell that reads flags carries one
   written place per SETTER cell — seventeen for `setl` and its kin —
   and one (cell, target) of that shape costs about 2,000 s through the
   native route and this tier together. Four are named in
   `t4_general_left_behind.json` and the rest of that shape is
   unreached. Whether the pass should carry every setter of a flag
   consumer through the general tier, or one, is a question about what
   the measurement is over and not about any construction.
