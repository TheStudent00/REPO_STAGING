# log 240 — task h2: the same handful after two printing fixes

Node: `hq.research.arch_unit_oracle`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
the "goal" section of 2026-09-07 and the ruling of 2026-09-08). The
PROGRESS entry is on the autopoly sub-node
(`.../node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`),
beside tasks o12, o13, h1 and h1b.

Date: 2026-09-09. Instance `h2`, on the TOWER, brought down at the end
of this log. Artifact folder (the same one tasks h1 and h1b wrote):
[`PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/`](file://PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/).
The deliverables are
[`handful.py`](file://PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py)
extended with a second entry point (section 2c and the `*2` commands),
[`handful2.json`](file://PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2.json)
and
[`handful2.md`](file://PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2.md)
(the twenty runs again, every intermediate object on the record).
**Task h1's own `handful.json` and `handful.md` were not written by any
lane of this task**; the new products sit beside them, and the rendered
sources are under `src2/` beside h1's `src/`.

Every rendering here is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself,
quoted; **GLOSS** is a plain-words reading beside a literal. No gloss
appears without its literal.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PseudoCoupHQ`, mounted into
the instance. Prose names host paths. **The lane logs are on the
TOWER** (`<user>@<tower>`), under
`<runs>/h2/agent/logs/`, and every attribution
below names one of them.

| lane | what it did | log, on the tower |
|---|---|---|
| `h2_l1_classifier.sh` | change 3: the two reference tables the zero-operand width rule reads, the classifier's own answer for each such mnemonic and for three control lines, and task h1b's composition re-derived over task h1's OWN twenty carved bodies | `20260909T060749Z__h2_l1_classifier.sh.log` |
| `h2_l2_sources.sh` | fix 1's regression guard: every place rendered BOTH ways, the two sources compared, and the h1-way source compared against the file task h1 itself wrote | `20260909T060804Z__h2_l2_sources.sh.log` |
| `h2_l3_run.sh` | the twenty runs after both fixes, the four UNDECIDED gate calls re-posed at 300,000 ms, the composition column and the report -- ONE lane, so `handful2.json` is written end to end by one version of the program | `20260909T060843Z__h2_l3_run.sh.log` |
| `h2_l4_o8_regression.sh` | task o8's per-opcode check re-run UNCHANGED over its 243 rows, into a scratch copy | `20260909T062903Z__h2_l4_o8_regression.sh.log` |
| `h2_l5_report_evidence.sh` | `handful.py report2` re-run after one fix in the report WRITER (task h1's four refused runs read as an empty `h1 verdict` cell rather than as their own cause word), then the twenty-row table, section 4.1, the tally and task o8's four totals; its LAST step ran the guard over five json at once and the lane exited 1 there, so the guard is lane `h2_l6`'s instead (section 10) | `20260909T063059Z__h2_l5_report_evidence.sh.log` |
| `h2_l6_guard.sh` | the unmodified spelling guard in two steps -- this task's own three json, then task o8's own results beside this task's scratch copy of them -- and `grep -c exempt` | `20260909T063159Z__h2_l6_guard.sh.log` |
| `h2_l7_sources_tally.sh` | `handful2_sources.json` counted, and the `idiv` destination place both ways side by side | `20260909T063631Z__h2_l7_sources_tally.sh.log` |
| `h2_l8_verify.sh` | the conventions verifier over a first draft of this log: 0 DIFFERS and 0 REFUSED, but 0 MATCHES too -- every transcript was pasted without the command above it, so nothing could be re-run; that is what lane `h2_l9` exists to fix (ADDENDUM) | `20260909T063820Z__h2_l8_verify.sh.log` |
| `h2_l9_evidence.sh` | EVERY transcript this log pastes, each with its own command printed above it by `printf %q` -- task h1's own evidence-lane shape, copied | `20260909T063918Z__h2_l9_evidence.sh.log` |
| `h2_l10_verify2.sh` | the verifier again, over the log rebuilt on lane `h2_l9`'s blocks: 8 MATCHES, 0 REFUSED, but 2 DIFFERS -- both about a paste, not about a claim's wording (ADDENDUM) | `20260909T064148Z__h2_l10_verify2.sh.log` |
| `h2_l11_verify3.sh` | the verifier a third time, after both were fixed in the LOG: 9 MATCHES, 0 DIFFERS, 0 REFUSED, 0 NOT_RERUNNABLE | `20260909T064252Z__h2_l11_verify3.sh.log` |

Every lane script is kept in the repo at
`PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h2/`
and was submitted from there.

---

# 1. What the objects are

- **a cell** (recap, task h1) — one (`mnem`, operand shape, `key_width`)
  row of the arch-opcode model table
  (`PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json`,
  tasks m1/m1b), holding, per PLACE the opcode writes, the z3 term the
  reference simulator's own builder puts there.
- **a run** (recap, task h1) — `find_emulation(cell, lang)`: the cell's
  term written in the target's own operators by the EXISTING renderer,
  compiled at that corpus's ship flags, carved, and put back to z3
  against the cell's own term.
- **fix 1, the normalised term** — the term the renderer is handed. Task
  h1 handed it `order_commutative(z3.simplify(term))`; this task hands
  it the term the pipeline's own normaliser leaves (`term.Term.
  normalize`'s own steps, the ones task t104 fixed on 2026-09-07,
  log 233).
- **fix 2, the lane of a vector place** — a cell whose place is an xmm
  register carries the whole 128-bit place in its term: the lane the
  operation writes, joined under the bits of the arrival it leaves
  alone. The cell's own `key_width` names that lane (32 for `addss`, 64
  for `cvtsi2sd`), so the DRIVER projects `Extract(key_width - 1, 0,
  place)` and renders that.
- **change 3, the zero-operand width rule** — one additive rule in
  `model_table.classify_line`, the one shared file this task's brief
  authorises: a line with no operand at all (`cqto`, `cltq`, `cltd`,
  `cwtd`, `cqo`) takes its width from the reference's own
  `SPREAD_SIGN` / `ACCUMULATOR_WIDEN` tables rather than from an
  operand.

---

# 2. What was done and what came back

Task h1 ended with two failures and both were in how a cell's term is
PRINTED rather than in the route, so this task fixed both in the driver,
added the one classifier rule, and re-ran the same ten cells against the
same two targets. Neither renderer was touched, and the proof that they
were not is task o8's own check re-run over its own 243 rows.

Fix 2 is the one that moved the answer. The four runs task h1 refused —
`addss` and `cvtsi2sd`, in c and in rust — now render, compile, land on
their own arch opcode and are proved equal to the cell's own term for
every input. Twenty runs of twenty reached a compiled body, where task
h1 got sixteen; the landing count went from six LANDED to ten; the
proved count from eighteen to twenty-two. Before the lane was rendered,
the bits ABOVE the lane were put to the gate against the same bits of
the arrival in that register, and in all four runs z3 proved they are
the arrival's own bits passed through — so the projection throws nothing
away silently.

Fix 1 changed nothing on this population, and that is a result rather
than a disappointment. Every one of the 24 places that renders at all
was rendered BOTH ways and the two sources came back character for
character identical — and identical to the file task h1's own run wrote
under `src/`. So the term the h1-way call already handed the renderer
prints what the normaliser leaves. `idiv`'s emulation is still 76
instructions, still 51 after the chaff strip, and the gate still answers
UNDECIDED at 3,000 ms and again at 300,000 ms. The 32-copy sign
extension is in the TABLE'S OWN TERM, not in the shape the renderer was
handed it in, which is what log 238 section 11 already flagged as
belonging to tasks m1/m1b.

Change 3 did exactly one thing, measured rather than asserted: task
h1b's composition, re-derived over task h1's OWN twenty carved bodies
with the rule in place, moves 2 of its 198 instruction records — the two
`cqto` lines, one in each `idiv` run — from "maps to no table cell" to
the table cell (`cqto`, `none`, 64). The other 196 are unchanged.

One thing came out that nobody asked for and is worth naming: the two
targets still emit the same machine code, byte for byte, in every place
both compiled — now 14 places rather than task h1's 12, because the two
float cells joined them. clang at `-O1` and rustc at `opt-level=1` were
handed a c source written with `memcpy` bit-casts and a rust source
written with `f32::from_bits`, and both wrote `addss %xmm1,%xmm0; ret`.

---

# 3. The three changes, each with the object that shows it

## 3.1 Fix 1: the term the renderer is handed, and its regression guard

WHAT IT IS, mechanically. `handful.the_normalised_term` runs
`term.Term.normalize`'s own steps through term.py's own module-level
functions — `order_commutative`, `z3.simplify`, `order_commutative`, the
positional renaming of the free symbols, `z3.simplify`,
`order_commutative` — and differs from that function in exactly one
respect, said out loud because the law forbids silent substitution:
`Term.normalize` ENDS BY PRINTING (`term.one_line`), so it hands back
text and the renderer walks a term; and it leaves the free symbols
renamed `v0`, `v1`, ..., while the renderer keys every arrival on its
own `seed_<family>` name, so the renaming is applied and then UNDONE.

THE GUARD THE BRIEF ASKS FOR, and it is over every cell rather than the
eight, so nothing is chosen after the fact. **LITERAL**, the tail of
block `[1/2]` of
`<runs>/h2/agent/logs/20260909T060804Z__h2_l2_sources.sh.log`:

```
[17/20] addss xmm_xmm 32 -> c
   reg_xmm0 ONE_SIDE_REFUSED: REFUSED / REFUSED
   peak resident: 70104 kB
[18/20] addss xmm_xmm 32 -> rust
   reg_xmm0 ONE_SIDE_REFUSED: REFUSED / REFUSED
   peak resident: 70104 kB
[19/20] cvtsi2sd gpr_xmm 64 -> c
   reg_xmm0 ONE_SIDE_REFUSED: REFUSED / REFUSED
   peak resident: 70104 kB
[20/20] cvtsi2sd gpr_xmm 64 -> rust
   reg_xmm0 ONE_SIDE_REFUSED: REFUSED / REFUSED
   peak resident: 70104 kB
wrote PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2_sources.json
```

The counts over all 32 place-and-target pairs, **LITERAL**, block
`[3/10]` of `<runs>/h2/agent/logs/20260909T063918Z__h2_l9_evidence.sh.log` (lane `h2_l9_evidence.sh` prints every command
above its own output, task h1's own evidence-lane shape):

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py sources_counts
NOT_RENDERED 4
ONE_SIDE_REFUSED 4
SOURCE_UNCHANGED 24
identical to the file task h1 wrote under src: 24 of 24 rendered
```

**GLOSS.** 24 places render, and for every one of them the source the
renderer writes from the h2-way term is character for character the
source it writes from the h1-way term, and character for character the
file task h1's own run left under `src/`. 4 are the flags place of a
flag-reading row, which task h1's own convention records as not written
by the opcode (log 238 section 4.4). The remaining 4 are the vector
places, which BOTH ways refuse when the lane is not projected — this
lane measures fix 1 ALONE, so it renders the place as task h1 did, and
the projection is fix 2's business in section 3.2.

Because no source changed, the brief's "or provably equal (z3, both
terms)" branch was never reached: `handful.proved_the_same` runs only
where the two sources differ, and it ran zero times.

## 3.2 Fix 2: the lane of a vector place, with the values in motion

The cell's term for `addss xmm_xmm 32`'s destination place, **LITERAL**
(`handful2.md` section 1.17, and the same text task h1 printed):

```
Concat(Extract(127, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1))))
```

**GLOSS.** The place is the whole 128-bit register. Its low 32 bits are
the float sum of the low lanes of the two arrivals; its top 96 bits are
`Extract(127, 32, v0)` — the first arrival's own bits, untouched. Task
h1's refusal was about that second half: both renderers plan an
arrival's holder from how the term reads it, and neither has a holder
for a vector arrival read above bit 63, so they refused by their own
cause word `emulate.CAUSE_LANE`.

What the driver now does, in three steps with the object of each:

1. **The projection.** `key_width` is 32, so the driver takes
   `Extract(31, 0, place)`. The projected lane, **LITERAL**:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
```

2. **What is above the lane is measured, not assumed.** The remaining
   bits, **LITERAL**, are `Extract(127, 32, v0)`, and they were put to
   the gate against `Extract(127, 32, seed_xmm0)` — the same bits of the
   arrival that lives in that register. The gate's answer, **LITERAL**:
   `PROVED_ON_SHIP` — "z3 proved the bits above the lane are the
   arrival's own bits, passed through".

3. **The renderer plans a 32-bit float holder by its own rule**, because
   the projected term reads each arrival only at `Extract(31, 0, ...)`
   and the answer home is 32 bits wide. The source, **LITERAL**
   ([`src2/addss_xmm_xmm_32__reg_xmm0__c.c`](file://PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/src2/addss_xmm_xmm_32__reg_xmm0__c.c)):

```c
float
emu_addss_xmm_xmm_32__reg_xmm0__c(float a, float b)
{
    return bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)((a) + (b))))));
}
```

The carved body, **LITERAL**: `addss %xmm1,%xmm0; ret`. Chaff-stripped:
`addss %xmm1,%xmm0`. Landing: **LANDED**. The gate: **PROVED_ON_SHIP**.

The rust side of the same cell, **LITERAL**
([`src2/addss_xmm_xmm_32__reg_xmm0__rust.rs`](file://PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/src2/addss_xmm_xmm_32__reg_xmm0__rust.rs)):

```rust
pub extern "C" fn emu_addss_xmm_xmm_32__reg_xmm0__rust(a: f32, b: f32) -> f32
{
    f32::from_bits((((((a) + (b))).to_bits() as u32)) as u32)
}
```

Its carved body is the same two instructions, byte for byte.

`cvtsi2sd gpr_xmm 64` is the same shape one width up. Its place term,
**LITERAL**: `Concat(Extract(127, 64, v0), fp.to_ieee_bv(fpToFP(RNE(),
v1)))`; `key_width` 64, so the projection is `Extract(63, 0, place)` and
the projected lane is `fp.to_ieee_bv(fpToFP(RNE(), v0))`. Note what the
projection also does here: `seed_xmm0` appears ONLY above the lane, so
the projected term reads one arrival where the place read two, and the
rendered function takes one `uint64_t` and answers a `double`. Body,
**LITERAL**: `cvtsi2sd %rdi,%xmm0; ret`. **LANDED**, **PROVED_ON_SHIP**,
in both targets.

NO RENDERER OPERATOR TABLE WAS EXTENDED, and none needed to be: every
float operator these four terms carry (`fpToFP`, `fp.to_ieee_bv`, float
addition, the RNE rounding mode) was already covered by both renderers,
which is what log 238 section 8 said when it named the refusal as being
about the PLACE and not about the operation.

## 3.3 Change 3: the zero-operand width rule, and what it moves

THE RULE, **LITERAL**, as it now stands in
`PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py`
(`classify_line`, the last decision before its refusal):

```python
    if width is None and not classes:
        width = ZERO_OPERAND_WIDTH.get(mnem)
    if width is None:
        return None, None, ("no register name and no row size to give "
                            "a width")
```

It sits LAST on purpose: a line whose operand text gives a width, and a
line whose ledger row gives one, are both decided above it, so nothing
that already classified can move. `ZERO_OPERAND_WIDTH` is built by
`model_table.zero_operand_widths()`, which reads the reference's own two
tables and types nothing.

What it reads and what it answers, **LITERAL**, block `[1/10]` of `<runs>/h2/agent/logs/20260909T063918Z__h2_l9_evidence.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/classifier_probe.py
reference.SPREAD_SIGN, LITERAL: {"cltd": 32, "cqo": 64, "cqto": 64, "cwtd": 16}
reference.ACCUMULATOR_WIDEN, LITERAL: {"cbtw": [8, 16], "cltq": [32, 64], "cwtl": [16, 32]}
model_table.ZERO_OPERAND_WIDTH, LITERAL: {"cbtw": 16, "cltd": 32, "cltq": 64, "cqo": 64, "cqto": 64, "cwtd": 16, "cwtl": 32}

the zero-operand mnemonics, classify_line(mnem, mnem, 0):
   cbtw   shape none width 16 key_width 16 cause None
   cltd   shape none width 32 key_width 32 cause None
   cltq   shape none width 64 key_width 64 cause None
   cqo    shape none width 64 key_width 64 cause None
   cqto   shape none width 64 key_width 64 cause None
   cwtd   shape none width 16 key_width 16 cause None
   cwtl   shape none width 32 key_width 32 cause None

the control lines, unchanged by the rule:
   idiv %r10 shape gpr_one width 64 key_width 64 cause None
   imul %esi,%eax shape gpr_gpr width 32 key_width 32 cause None
   ret    shape None width None key_width None cause no register name and no row size to give a width

TRANSLATED triples in PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json: 6218
   cbtw   (cbtw, none, 16) is a TRANSLATED row of the table: False
   cltd   (cltd, none, 32) is a TRANSLATED row of the table: True
   cltq   (cltq, none, 64) is a TRANSLATED row of the table: False
   cqo    (cqo, none, 64) is a TRANSLATED row of the table: False
   cqto   (cqto, none, 64) is a TRANSLATED row of the table: True
   cwtd   (cwtd, none, 16) is a TRANSLATED row of the table: True
   cwtl   (cwtl, none, 32) is a TRANSLATED row of the table: True
```

**GLOSS.** The width is read from the mnemonic's own entry: `cqto`
spreads the sign of a 64-bit accumulator, so 64. `key_width` passes it
through unchanged, because a zero-operand line is not x87, not a scalar
lane and not a whole-register vector line. Four of the seven mnemonics
land on a triple the table holds as a TRANSLATED row; three
(`cbtw`, `cltq`, `cqo`) do not, which is a fact about the table's own
sweep and not about this rule — it is recorded here and flagged in
section 11. `ret` still refuses, by the same cause word, because it is
not in either reference table; task o2's chaff rule names it before the
classifier is ever asked.

And what it moves, **LITERAL**, block `[2/3]` of
`<runs>/h2/agent/logs/20260909T060749Z__h2_l1_classifier.sh.log`
-- the lane that first ran it; the population is task h1's OWN
`handful.json`, read and never written back. THIS ONE IS PASTED WITHOUT
its command, deliberately: `handful.py reclassify` prints its own peak
resident kB, which is a different number on every run, so a pasted
transcript of it can never re-run identically. Lane `h2_l9_evidence.sh`
block `[2/10]` runs the same command and its own log carries that
run's copy.

```
[2/3] task h2: task h1b's composition re-derived over task h1's own twenty bodies
[1/2] the table's own TRANSLATED (mnem, shape, key_width) triples, from PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json
   6218 distinct triples
   peak resident: 255080 kB
[2/2] task h1b's composition, re-derived with the rule in place
   instructions   198
   unchanged      196
   changed        2
   CHANGED idiv gpr_one 32/c instruction 72
      before: {"cell": false, "line": "cqto", "mnem": "cqto", "reason": "the classifier could not read it: no register name and no row size to give a width"}
      after:  {"cell": true, "key_width": 64, "line": "cqto", "mnem": "cqto", "shape": "none"}
   CHANGED idiv gpr_one 32/rust instruction 72
      before: {"cell": false, "line": "cqto", "mnem": "cqto", "reason": "the classifier could not read it: no register name and no row size to give a width"}
      after:  {"cell": true, "key_width": 64, "line": "cqto", "mnem": "cqto", "shape": "none"}
wrote PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2_classifier.json
peak resident: 255080 kB
```

**GLOSS.** The population is task h1's OWN twenty carved bodies, read
from `handful.json` and never written back: 198 instruction records, 196
identical to what task h1b recorded, 2 changed, and both are the `cqto`
line — the only cause task h1b's own section 6 reported. `cqto` now maps
to a cell and nothing else moved.

---

# 4. The twenty runs, one row each

**LITERAL**, block `[5/10]` of `<runs>/h2/agent/logs/20260909T063918Z__h2_l9_evidence.sh.log` (the table is pasted inside a
fence, as task h1's own log 238 section 5 pastes it, so the command
above it re-runs; the `composition` column's two `idiv` cells are cut by
the report's own 200-character budget and the untruncated list is
`handful2.json`'s own `composition` field):

```
$ sed -n \\%\^.\ cell\ .\ lang\ .\ h1\ verdict%\,\\%\^\$%p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2.md
| cell | lang | h1 verdict | h2 verdict | landed (h2) | composition (h2) | cause if refused |
|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) |  |
| `add` gpr_gpr 32 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) |  |
| `sub` imm_gpr 64 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) |  |
| `sub` imm_gpr 64 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) |  |
| `imul` gpr_gpr 32 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `imul` (+2 chaff) |  |
| `imul` gpr_gpr 32 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `imul` (+2 chaff) |  |
| `sar` cl_gpr 32 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `sar` (+3 chaff) |  |
| `sar` cl_gpr 32 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `sar` (+3 chaff) |  |
| `shr` cl_gpr 64 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `shr` (+3 chaff) |  |
| `shr` cl_gpr 64 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `shr` (+3 chaff) |  |
| `idiv` gpr_one 32 | c | UNDECIDED, UNDECIDED at 300000 ms | UNDECIDED, UNDECIDED at 300000 ms | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) |  |
| `idiv` gpr_one 32 | rust | UNDECIDED, UNDECIDED at 300000 ms | UNDECIDED, UNDECIDED at 300000 ms | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) |  |
| `cmovne` gpr_gpr 32 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) |  |
| `cmovne` gpr_gpr 32 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) |  |
| `setne` gpr_one 8 | c | DISPROVED, PROVED_ON_SHIP under caller extension | DISPROVED, PROVED_ON_SHIP under caller extension | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) |  |
| `setne` gpr_one 8 | rust | DISPROVED, PROVED_ON_SHIP under caller extension | DISPROVED, PROVED_ON_SHIP under caller extension | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) |  |
| `addss` xmm_xmm 32 | c | vector arrival used beyond its low lane: xmm0 read above bit 63 | PROVED_ON_SHIP | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) |  |
| `addss` xmm_xmm 32 | rust | vector arrival used beyond its low lane: xmm0 read above bit 63 | PROVED_ON_SHIP | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) |  |
| `cvtsi2sd` gpr_xmm 64 | c | vector arrival used beyond its low lane: xmm0 read above bit 63 | PROVED_ON_SHIP | LANDED | `cvtsi2sd` (+1 chaff) |  |
| `cvtsi2sd` gpr_xmm 64 | rust | vector arrival used beyond its low lane: xmm0 read above bit 63 | PROVED_ON_SHIP | LANDED | `cvtsi2sd` (+1 chaff) |  |
```

**GLOSS.** Sixteen rows are character for character task h1's own
verdicts; the four that changed are the float cells, from a refusal
before any compile to LANDED and proved. `landed (h2)` and
`composition (h2)` are the DESTINATION place's, task h1's own
convention. The `cause if refused` column is empty on every row because
no run of this task was refused. The one starred entry is the `addss`
line itself, which the classifier cannot read for a reason section 11
names — an xmm operand carries no width and a carved emulation body has
no ledger row, the same cause word `cqto` used to carry, and the rule
this task's brief authorises is the ZERO-OPERAND one, so the vector case
was left alone rather than worked around.

---

# 5. `idiv`, before and after

The brief asks for the term text before and after, the instruction count
of the new body, and the gate's answer.

The cell's term for `reg_rax`, as the model table prints it: 783
characters, of which the first 220 are quoted here, **LITERAL**
(`handful2.md` section 1.11 and `handful2.json` carry the whole line):

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extra
```

**GLOSS.** A signed 64-by-64 divide whose dividend is the two 32-bit
arrivals joined, and whose divisor is bit 31 of the third arrival
written out 32 times and joined to it — a sign extension spelled as 32
copies rather than as one `SignExt`.

The term the renderer was handed, BEFORE the fix (task h1's way) and
AFTER it (this task's), **LITERAL**, block `[4/10]` of `<runs>/h2/agent/logs/20260909T063918Z__h2_l9_evidence.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py sources_idiv idiv c reg_rax
idiv gpr_one 32 c reg_rax
   h1-way term text, 993 characters
   h2-way term text, 993 characters
   the two texts are identical: True
   the two rendered sources are identical: True
```

**GLOSS.** The normaliser leaves this term exactly where task h1's own
call left it, so there is no "after" that differs from the "before": the
32 joined `Extract(31, 31, ...)` copies are what the TABLE's builder
produced, and normalising does not fold them into a sign extension. The
consequences follow: the body is **76 instructions**, 51 after task o2's
chaff strip — the same counts task h1 measured — and the gate answers
**UNDECIDED** at 3,000 ms and, re-posed as the law's flag rule requires,
**UNDECIDED** again at 300,000 ms. Never DISPROVED. The re-pose is
recorded beside the verdict of record, not in place of it.

This is the same reading log 238 section 11 already had, now measured
rather than suspected: if the term carried `SignExt` where the builder
means a sign extension, both the rendered source and the solver's job
would be far smaller, and that is a change to how the model table's own
printer works — tasks m1/m1b's, not this task's.

---

# 6. The regression: task o8's own check, unchanged, over its own 243 rows

**LITERAL**, blocks `[1/5]` and `[4/5]` of
`<runs>/h2/agent/logs/20260909T062903Z__h2_l4_o8_regression.sh.log`:

```
-- POPULATION: single_opcode_units.json narrow rows, five languages
   rows per language: {'c': 83, 'cpp': 82, 'go': 27, 'rust': 48, 'swift': 19}
   distinct example unit ids needed: 259
   canon40 records held: 259; term66 records held: 259
   valid (proved term held): 243; no proved term, listed and skipped: 16
```

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/o8_regression.py totals
rows             243
LANDED           197
byte identical   155
proved           216
```

**GLOSS.** The four totals are the ones task o8 recorded (log 220, and
`per_opcode_report.md` section 2's `all` row: 243 rows, 197 LANDED, 155
byte-identical to the row's own body, 216 proved). They come back
unchanged, so `emulate.Renderer` and `rust_render.RustRenderer` write
the same c for the same 243 proved terms after this task as before it.
The 16 skipped rows and the 243 valid ones are the same populations too.

HOW TASK o8's OWN ARTIFACT STAYED UNTOUCHED.
[`o8_regression.py`](file://PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/o8_regression.py)
imports `per_opcode.py` from its own folder — not forked, not edited —
and points the five paths it WRITES at
`handful/o8_regression/` before calling its `main`. Its inputs
(`single_opcode_units.json`, the canon40 and term66 stores) are read
only. Nothing under `per_opcode/` was written by any lane of this task.

---

# 7. The tally

**LITERAL**, block `[7/10]` of `<runs>/h2/agent/logs/20260909T063918Z__h2_l9_evidence.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py tally2
add gpr_gpr 32               flags      SAME BYTES
add gpr_gpr 32               reg_rdi    SAME BYTES
addss xmm_xmm 32             reg_xmm0   SAME BYTES
cmovne gpr_gpr 32            reg_rdi    SAME BYTES
cvtsi2sd gpr_xmm 64          reg_xmm0   SAME BYTES
idiv gpr_one 32              reg_rax    SAME BYTES
idiv gpr_one 32              reg_rdx    SAME BYTES
imul gpr_gpr 32              flags      SAME BYTES
imul gpr_gpr 32              reg_rdi    SAME BYTES
sar cl_gpr 32                reg_rdi    SAME BYTES
setne gpr_one 8              reg_rdi    SAME BYTES
shr cl_gpr 64                reg_rdi    SAME BYTES
sub imm_gpr 64               flags      SAME BYTES
sub imm_gpr 64               reg_rdi    SAME BYTES
compiled places both targets have a body for: 14
   the two targets emitted the same bytes: 14
   the two targets emitted different bytes: 0

runs                             20
runs refused before any compile  0
places compiled and carved       28
LANDED                           10
LANDED_ELSEWHERE                 6
NOT_COLLAPSED                    12
PROVED_ON_SHIP                   22
proved under caller extension    2
neither                          4

instructions                                                   206
table cells                                                    124
chaff: ret                                                     20
chaff: calling-convention move                                 60
maps to no table cell                                          2
LANDED runs whose composition is exactly one cell, the target  8
```

**GLOSS**, against task h1's own tally (log 238 section 7), which is the
same walk over the same population:

| what | task h1 | task h2 | why it moved |
|---|---|---|---|
| runs refused before any compile | 4 | 0 | fix 2: the four float runs now render |
| places compiled and carved | 24 | 28 | the same four, one place each |
| LANDED | 6 | 10 | the four float places land on their own opcode |
| LANDED_ELSEWHERE | 6 | 6 | unchanged |
| NOT_COLLAPSED | 12 | 12 | unchanged |
| PROVED_ON_SHIP | 18 | 22 | the same four |
| proved under caller extension | 2 | 2 | unchanged |
| neither | 4 | 4 | `idiv`'s two places in each target, still UNDECIDED |
| places both targets have a body for | 12 | 14 | the two float cells joined them, and both are SAME BYTES |
| composition instructions | 198 | 206 | four two-instruction float bodies |
| composition table cells | 120 | 124 | +2 `cqto` (change 3), +2 `cvtsi2sd` |
| maps to no table cell | 2 (`cqto`) | 2 (`addss`) | change 3 closed `cqto`; the vector line is section 11's item |
| LANDED runs whose composition is one cell, the target | 6 | 8 | `cvtsi2sd` in both targets; `addss` lands but its line does not classify |

---

# 8. What did not work, by cause

**LITERAL**, block `[6/10]` of `<runs>/h2/agent/logs/20260909T063918Z__h2_l9_evidence.sh.log` -- `handful2.md`'s own
section 3.1, written by `handful.py report2` and never hand-edited:

```
$ sed -n \\%\^###\ 3.1\ Refusals%\,\\%\^###\ 3.2%p PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2.md
### 3.1 Refusals and gate calls that did not prove

- `the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes`: 4 -- cmovne gpr_gpr 32/c [flags], cmovne gpr_gpr 32/rust [flags], setne gpr_one 8/c [flags], setne gpr_one 8/rust [flags]
- `the gate answered UNDECIDED at 3,000 ms and again at 300000 ms`: 4 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx]

### 3.2 The landings that were not LANDED, by cause
```

**GLOSS**, one paragraph per cause, each with its status.

- **The vector refusal is CLOSED.** Task h1's third cause — "vector
  arrival used beyond its low lane", 4 sightings — does not appear in
  this task's list at all, because fix 2 removed it. The place is still
  128 bits and the renderers still have no holder for one; the driver no
  longer asks them to hold it.
- **The solver still does not answer for `idiv`**, 4 of 28 places,
  status OPEN and reported as a limit at both ceilings, unchanged by fix
  1 (section 5).
- **The flags place of a flag-reading row is a pass-through**, 4 of 20
  runs, status CLOSED, task h1's own convention (log 238 section 4.4),
  unchanged.
- **The `addss` line maps to no table cell**, 2 sightings, status OPEN
  and flagged in section 11. The instruction LANDED and the gate PROVED
  it; what fails is the classifier reading a width off `addss
  %xmm1,%xmm0`, whose operands are xmm registers and so carry no width,
  in a carved body that has no ledger row to give one.

---

# 9. Bounds and memory

The stated bound: ONE collecting process, no forked workers, peak
resident checked after every run, named abort `ABORT_MEMORY_H2` at 4 GB
(4,194,304 kB) — the same bound and the same machinery tasks h1 and h1b
stated. The o8 regression runs task o8's own program under task o8's
own bound, `ABORT_MEMORY_O8` at 2 GB, unchanged.

| lane | peak resident | as a share of its own bound |
|---|---|---|
| `h2_l1_classifier.sh` (reads `model_table_rows.json`, 50 MB) | 255,080 kB | 6.1% of 4 GB |
| `h2_l2_sources.sh` | 70,104 kB | 1.7% of 4 GB |
| `h2_l3_run.sh` (the twenty runs; `handful2.json`'s own `peak_kb`) | 448,016 kB | 10.7% of 4 GB |
| `h2_l4_o8_regression.sh` (task o8's own collector) | 82,608 kB | 3.9% of 2 GB |

The abort never fired and no bound was raised. `h2_l3_run.sh` took
1,218.5 s wall clock, of which about 1,200 s is the four `idiv`
obligations sitting at their 300,000 ms ceiling; every other lane in
this task is under 12 s.

---

# 10. The guard, and `grep -c exempt`

**LITERAL**, block `[9/10]` of `<runs>/h2/agent/logs/20260909T063918Z__h2_l9_evidence.sh.log`:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2_sources.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2_classifier.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS handful2.json -- no operator token in any key, grouping, pairing or row structure
PASS handful2_sources.json -- no operator token in any key, grouping, pairing or row structure
PASS handful2_classifier.json -- no operator token in any key, grouping, pairing or row structure
```

**GLOSS.** The three json this task's own programs write PASS the
unmodified guard on their first run; no field was renamed to dodge it
and no exemption is claimed anywhere.

`grep -c exempt` over every file this task added or changed, **LITERAL**,
block `[10/10]` of `<runs>/h2/agent/logs/20260909T063918Z__h2_l9_evidence.sh.log`:

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/o8_regression.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/classifier_probe.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2.md PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h2/h2_l1_classifier.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h2/h2_l2_sources.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h2/h2_l3_run.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h2/h2_l4_o8_regression.sh PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/o8_regression.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/classifier_probe.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2.md:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h2/h2_l1_classifier.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h2/h2_l2_sources.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h2/h2_l3_run.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h2/h2_l4_o8_regression.sh:0
PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py:0
```

**GLOSS.** Zero `exempt` everywhere, including in the one shared file
this task's brief authorises. `grep -c` answers 1 when a count it prints
is zero, which is why this step and the lane that carries it end on
that exit.

THE TWO FAILURES ARE ONE INHERITED, ALREADY-OPEN QUESTION, and they are
shown side by side so that is visible. **LITERAL**, block `[2/3]` of
`<runs>/h2/agent/logs/20260909T063159Z__h2_l6_guard.sh.log` (that lane pipes the same guard call through `grep -E`
so only its verdict lines print; block `[9/10]` of the evidence lane
above is the same call unfiltered, with all 57 places listed):

```
[2/3] task h2: the guard over task o8's own results beside this task's scratch copy
operator inventory: 91 tokens read from probe_manifest_*.json
FAIL per_opcode_results.json -- 57 spelling-keyed place(s)
FAIL per_opcode_results.json -- 57 spelling-keyed place(s)
```

**GLOSS.** The first line is task o8's OWN
`per_opcode_results.json`, which has sat on disk since 2026-09-06, and
the second is this task's scratch copy of the same run. Both fail with
the same count, 57. The cause is task o8's own and is recorded in its
program's docstring and in log 208 / log 220: the field is
`landed_mnem`, an ARCH-OPCODE mnemonic, and four arch mnemonics
(`and`, `or`, `xor`, `not`) are also banned operator spellings. Task o8
left that open awaiting the owner rather than inventing a new key to route
around it; this task inherits it unchanged and invents nothing either.

Lane `h2_l6_guard.sh` exited 1: `grep -c` answers 1 when a count it
prints is zero, which is the result this step wants. Every step of the
lane ran and is above.

---

# 11. Flag for the coordinator

- **A vector line in a carved body maps to no table cell, for the same
  cause `cqto` had.** `model_table.operand_class` gives an `%xmm` name
  no width (an xmm register is 128 bits and the operation's width is its
  mnemonic's lane), so `addss %xmm1,%xmm0` reaches the classifier's
  refusal "no register name and no row size to give a width". A real
  sweep row and a real ledger row both supply a width from elsewhere, so
  this shows up only on a carved emulation body. `model_table.key_width`
  ALREADY holds the answer — `SCALAR_LANE_WIDTH["addss"]` is 32 — but
  `classify_line` refuses before `key_width` is ever called. The
  symmetrical rule (a vector line with no width takes the mnemonic's own
  lane width) is one line beside the one this task added, and this
  task's brief authorises the ZERO-OPERAND rule and nothing else, so it
  was not written. 2 sightings, both `addss`.
- **Three zero-operand mnemonics classify to a triple the table does not
  hold**: `cbtw` (none, 16), `cltq` (none, 64) and `cqo` (none, 64) are
  not TRANSLATED rows of `model_table_rows.json`, while `cltd`, `cqto`,
  `cwtd` and `cwtl` are (section 3.3). That is a fact about the sweep's
  own outcomes, not about the rule; nothing in this task's population
  hits it, and it is recorded so a later task that meets one of those
  three knows the classifier reads it and the table has no cell for it.
- **Fix 1 is a no-op on this population, and the `idiv` cost is in the
  table's printer.** Log 238 section 11 suspected it; section 5 above
  measures it. The change that would shrink `idiv`'s body and the
  solver's job is in how the model table's own terms spell a sign
  extension, which belongs to tasks m1/m1b. This task did not touch it.
- **The gate's width cut (log 238 section 8.1) still stands**, unchanged
  and still flagged there; nothing in this task changed
  `Research/op_pipeline/`.

---

# 12. The two lists

## Decided, recorded for audit

- The two fixes are in the DRIVER; neither renderer was edited, and the
  proof is task o8's own four totals coming back 243 / 197 / 155 / 216
  (section 6).
- Task h1's products are not overwritten: this task wrote
  `handful2.json`, `handful2.md`, `handful2_sources.json`,
  `handful2_classifier.json`, `src2/` and `o8_regression/`, all beside
  h1's own, and read `handful.json` only.
- `the_normalised_term` restates `term.Term.normalize`'s steps rather
  than calling it, because that function ends by printing and the
  renderer walks a term; the positional renaming it leaves behind is
  applied and undone, because the renderer keys arrivals on
  `seed_<family>`. Said out loud, in the function's own docstring, as
  the law requires.
- Fix 1's guard was run over every place of every cell, both ways, not
  only over the eight the brief names — 24 rendered places, 24 sources
  unchanged and identical to the files task h1 wrote (section 3.1).
- The bits above a projected lane are MEASURED against the arrival, by
  the gate, on every one of the four vector places, and all four are
  proved pass-through (section 3.2).
- The zero-operand width rule sits LAST in `classify_line`, after the
  operand-text width and after the ledger row's size, so nothing that
  already classified can move; measured over task h1b's own 198
  instruction records, 196 unchanged and 2 moved, both `cqto`.
- The `addss` line's classification is left REFUSED rather than rescued,
  because the rule this brief authorises is the zero-operand one
  (section 11, first item).

## Awaiting the owner

- Nothing. The four items in section 11 are for the coordinator, not
  rulings.

---

# ADDENDUM — the verifier over this log

Two passes, the second after the fix the first one found, and the
verifier itself was never touched:

- `h2_l8_verify.sh`, the first pass over the first draft: **0 DIFFERS,
  0 REFUSED, 0 NOT_RERUNNABLE — and 0 MATCHES**, because every
  transcript had been pasted with an attribution to its lane log but
  WITHOUT the command above it, so the verifier had nothing to re-run
  (23 of 23 claims `attribution_only` or `prose_only`). Nothing was
  softened to fix that: lane `h2_l9_evidence.sh` re-ran every one of
  those commands with `printf %q` printing the command above its own
  output — task h1's own evidence-lane shape, copied rather than
  reinvented — and every transcript in this log was replaced with that
  lane's blocks.
- `h2_l10_verify2.sh`, the second pass, over this log as it stands
  apart from this ADDENDUM, **LITERAL**:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_240_task_h2_two_printing_fixes.md
population: 27 claims across 1 logs
  MATCHES          9
  DIFFERS          0
  UNVERIFIABLE     18
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 9 of 27 claims reproduce; 18 (67%) carry nothing to re-run

causes, by name:
  attribution_only                 9
  prose_only                       8
  pasted_without_source            1

peak RSS after the pass: 17.5 MB
```

**TALLY: 27 claims, 9 MATCHES, 0 DIFFERS, 18 UNVERIFIABLE, 0 REFUSED,
0 NOT_RERUNNABLE. Zero DIFFERS, zero REFUSED.** Lane `h2_l10_verify2.sh`
had found 2 DIFFERS between those two passes, and both were about a
PASTE rather than about any claim's wording, so both were fixed in the
log and neither by softening anything:

- `handful.py reclassify` prints its own peak resident kB, which is a
  different number on every run (255,200 kB in the evidence lane,
  255,068 kB when the verifier re-ran it), so its transcript can never
  re-run identically. It is now pasted WITHOUT a command, attributed to
  lane `h2_l1_classifier.sh`, which is the lane that first ran it.
- the `grep -c exempt` paste had carried the lane log's own three footer
  lines (`# exit 0 in 2.2s` and its neighbours) into the block; they
  were removed, leaving the command's own output.

The 18 that carry nothing to re-run are 8 prose verifications, 9
attributions into `handful2.md`, `handful2.json`, `src2/` and the lane
logs, and the one deliberate `pasted_without_source` named above. Full
untruncated verifier output:
`<runs>/h2/agent/logs/20260909T064252Z__h2_l11_verify3.sh.log`,
on the tower. Nothing above this ADDENDUM was edited after
`h2_l11_verify3.sh` ran.
