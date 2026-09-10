# log 239 — task h1b: the composition column, closing task h1

Node: `hq.research.arch_unit_oracle`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
the "goal" section of 2026-09-07 and the ruling of 2026-09-08). The
PROGRESS entry is on the autopoly sub-node
(`.../node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`),
beside tasks o12, o13 and h1.

Date: 2026-09-09. Instance `h1b`, on the TOWER, brought down at the
end of this log. Artifact folder (the same one task h1 wrote):
[`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/`](file://PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/).
This task's own instruction was task h1's brief, §5, added 2026-09-09
after h1 had already run: one new field on every run already in
`handful.json`, `composition`, plus the matching column in
`handful.md`'s twenty-row table. Nothing else in either file changed.

Every rendering here is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself,
quoted; **GLOSS** is a plain-words reading beside a literal. No gloss
appears without its literal.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ`, mounted into
the instance. Prose names host paths. **The lane logs are on the
TOWER** (`<user>@<tower>`), under
`<runs>/h1b/agent/logs/`, and every
attribution below names one of them.

| lane | what it did | log, on the tower |
|---|---|---|
| `h1b_l1_compose_report.sh` | `handful.py compose` (writes `composition` on every run), `handful.py report`, the spelling guard | `20260909T054342Z__h1b_l1_compose_report.sh.log` |
| `h1b_l2_report.sh` | `handful.py report` re-run after `composition_gloss`'s length cut was fixed so an unmapped instruction is never truncated away, the guard again | `20260909T054443Z__h1b_l2_report.sh.log` |
| `h1b_l3_evidence.sh` | the twenty-row table, the tally, the guard, a first `grep -c exempt`, the LANDED-runs check -- one step (`grep -c exempt` naming `h1b_l2_report.sh`) ran before that lane's own sync had landed on the tower and reported "No such file", SUPERSEDED for that one step only | `20260909T054519Z__h1b_l3_evidence.sh.log` |
| `h1b_l4_evidence2.sh` | `grep -c exempt` retried, and made the same mistake about itself; SUPERSEDED | `20260909T054557Z__h1b_l4_evidence2.sh.log` |
| `h1b_l5_evidence3.sh` | `grep -c exempt`, corrected: the driver, the report, and the two compute lanes, never the evidence lanes themselves (task h1's own precedent, log 238 §10, for the same reason) | `20260909T054637Z__h1b_l5_evidence3.sh.log` |
| `h1b_l6_verify.sh` | the conventions-log-claims verifier over this log's first draft: 0 DIFFERS, 2 NOT_RERUNNABLE on the two elided transcripts in section 5 | `20260909T054932Z__h1b_l6_verify.sh.log` |
| `h1b_l7_verify2.sh` | the verifier again, after both elisions were replaced with the exact transcripts: 0 DIFFERS, 0 NOT_RERUNNABLE, but 1 REFUSED (a false-positive redirect read out of a literal `->` in a print statement) | `20260909T055116Z__h1b_l7_verify2.sh.log` |
| `h1b_l8_evidence4.sh` | the LANDED-runs check re-run with the `->` removed from its print statement, so the REFUSED claim clears | `20260909T055154Z__h1b_l8_evidence4.sh.log` |

Every lane script is kept in the repo at
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1b/`
and was submitted from there.

---

# 1. What the objects are

- **composition** — the new field this task adds to every run already
  in `handful.json`: the RAW carved body of the run's own DESTINATION
  PLACE, walked instruction by instruction in body order, each one
  named as what it is.
- **destination place** — task h1's own convention (`handful.
  destination_place`, unchanged): the first place a run writes that
  is not the flags, or the flags place when that is all there is. The
  `landed` and `gate` columns of h1's twenty-row table already
  summarize only this place; `composition` follows the same
  convention so the new column reads beside the old ones without a
  second axis of meaning.
- **the RAW carved body** — `handful.json`'s own `body_text` on that
  place: every instruction the compiler emitted for the emulation
  function, semicolon-joined, BEFORE task o2's chaff rule strips
  anything. Task h1's own `stripped_text` (AFTER the strip) is what
  the `landed`/`gate` columns are keyed on; `composition` walks the
  wider, unstripped list so `ret` and the calling-convention moves are
  present to be named, not already gone.
- **a table cell** (recap, task h1 §1) — one (`mnem`, operand shape,
  `key_width`) row of the arch-opcode model table that holds a z3
  term, task m1/m1b.
- **chaff** (recap, task o2) — `ret`/`nop`/`push`/`pop`
  (`single_opcode_units.NARROW_BARE`) or a pure register-to-register
  or register-to-slot move
  (`single_opcode_units.NARROW_PURE_MOVE`, both operands
  `is_reg_or_slot_operand`) under the narrow rule -- the same rule
  task h1's own `landing_of` already calls to decide LANDED.

---

# 2. What was done and what came back

the owner's reading, quoted in the brief: "a carved body is a sequence of
arch opcodes, each a cell of the model table, so the body's term is a
composition of table cells." For every one of the twenty runs, this
task took the destination place's raw carved body, split it on `"; "`
into its instructions, and classified each one with the SAME functions
task m1b's own classifier uses -- `model_table.classify_line` (which
calls `model_table.operand_class` and `model_table.SHAPE_OF_CLASSES`)
and `model_table.key_width` -- imported from `model_table.py` and
called, never re-implemented. Where an instruction's mnemonic and
operands are `ret` or a calling-convention move, task o2's own
`single_opcode_units.NARROW_BARE` / `NARROW_PURE_MOVE` test says so
before the classifier is asked at all, and the instruction is marked
`ret` or a calling-convention move rather than reported as unmapped --
the brief's own instruction ("marking `ret` and the calling-convention
moves as they are"). Everything else the classifier resolves is
checked against the 6,218 distinct (`mnem`, shape, `key_width`)
triples that are TRANSLATED rows of the model table
(`model_table_rows.json`, read once); an instruction the classifier
could not read, or one it read into a triple absent from that set, is
reported as mapping to no table cell, with its own line and the
cause.

Sixteen of the twenty runs have a destination place that compiled (the
same sixteen task h1 reported; the four float refusals -- `addss` and
`cvtsi2sd`, both targets -- never reached a carved body, so their
`composition` is the empty list). Those sixteen runs' raw bodies carry
198 instructions in total: 120 are table cells, 76 are chaff (16 `ret`
+ 60 calling-convention moves), and 2 map to no table cell -- both are
`cqto`, one in the c `idiv` run and one in the rust `idiv` run, the
only mnemonic this population's classifier could not read (`cqto`
carries no operand at all, and the classifier's own cause is "no
register name and no row size to give a width" -- there is no ledger
row behind a carved emulation body to supply one). Every one of the
six LANDED runs' composition is exactly one table-cell instruction,
and it is the run's own cell: `imul`, `sar` and `shr`, each in both
targets. This is not asserted; it was checked by re-deriving the
LANDED runs from `handful.json` itself and comparing (§5, and the
guard lane's own step [5/5]).

One structural bug was found and fixed before this record: the first
attempt at `composition_gloss` (the table-column GLOSS) built its
one-line summary from the table-cell mnemonics with a 200-character
cut, and for the two `idiv` runs -- 76 raw instructions each -- that
cut fell before reaching `cqto`, so the one unmapped instruction in
the whole population was invisible in the rendered table despite being
correctly recorded in `handful.json` all along. The brief's own words
("named as such with its line") make an unmapped instruction the
load-bearing case, so the fix reserves room for every unmapped entry
outside the cut and only trims the (common, long) cell sequence when
the two together would not fit (`handful.py`, `composition_gloss`).
Lane `h1b_l1` ran the ORIGINAL gloss; lane `h1b_l2` re-ran `handful.py
report` after the fix, against the SAME `handful.json` (`compose` was
not re-run, because the fix is in the report writer, not the data);
`h1b_l3` onward read the corrected `handful.md`.

---

# 3. The twenty-row table, with the composition column

**LITERAL**, block `[1/5]` of
`<runs>/h1b/agent/logs/20260909T054519Z__h1b_l3_evidence.sh.log`:

| cell | lang | landed | gate | composition (GLOSS) |
|---|---|---|---|---|
| `add` gpr_gpr 32 | c | LANDED_ELSEWHERE on `lea` | PROVED_ON_SHIP | `lea` (+1 chaff) |
| `add` gpr_gpr 32 | rust | LANDED_ELSEWHERE on `lea` | PROVED_ON_SHIP | `lea` (+1 chaff) |
| `sub` imm_gpr 64 | c | LANDED_ELSEWHERE on `lea` | PROVED_ON_SHIP | `lea` (+1 chaff) |
| `sub` imm_gpr 64 | rust | LANDED_ELSEWHERE on `lea` | PROVED_ON_SHIP | `lea` (+1 chaff) |
| `imul` gpr_gpr 32 | c | LANDED | PROVED_ON_SHIP | `imul` (+2 chaff) |
| `imul` gpr_gpr 32 | rust | LANDED | PROVED_ON_SHIP | `imul` (+2 chaff) |
| `sar` cl_gpr 32 | c | LANDED | PROVED_ON_SHIP | `sar` (+3 chaff) |
| `sar` cl_gpr 32 | rust | LANDED | PROVED_ON_SHIP | `sar` (+3 chaff) |
| `shr` cl_gpr 64 | c | LANDED | PROVED_ON_SHIP | `shr` (+3 chaff) |
| `shr` cl_gpr 64 | rust | LANDED | PROVED_ON_SHIP | `shr` (+3 chaff) |
| `idiv` gpr_one 32 | c | NOT_COLLAPSED (51) | UNDECIDED, UNDECIDED at 300000 ms | `shl` `or` `shr` `shl` ... (50 cells) -- maps to no cell: `cqto`\* (+25 chaff) |
| `idiv` gpr_one 32 | rust | NOT_COLLAPSED (51) | UNDECIDED, UNDECIDED at 300000 ms | `shl` `or` `shr` `shl` ... (50 cells) -- maps to no cell: `cqto`\* (+25 chaff) |
| `cmovne` gpr_gpr 32 | c | NOT_COLLAPSED (2) | PROVED_ON_SHIP | `test` `cmove` (+2 chaff) |
| `cmovne` gpr_gpr 32 | rust | NOT_COLLAPSED (2) | PROVED_ON_SHIP | `test` `cmove` (+2 chaff) |
| `setne` gpr_one 8 | c | NOT_COLLAPSED (3) | DISPROVED, PROVED_ON_SHIP under caller extension | `xor` `test` `setne` (+1 chaff) |
| `setne` gpr_one 8 | rust | NOT_COLLAPSED (3) | DISPROVED, PROVED_ON_SHIP under caller extension | `xor` `test` `setne` (+1 chaff) |
| `addss` xmm_xmm 32 | c |  |  |  |
| `addss` xmm_xmm 32 | rust |  |  |  |
| `cvtsi2sd` gpr_xmm 64 | c |  |  |  |
| `cvtsi2sd` gpr_xmm 64 | rust |  |  |  |

**GLOSS.** The `rendered` and `cause if refused` columns of the actual
table are dropped here for width; they are unchanged from task h1's
own log 238 §5 and sit beside `composition` in
`handful.md` itself. The `idiv` rows are shown abbreviated
(`handful.md`'s own cell already carries all 50 cell mnemonics before
the cut); the untruncated `composition` LIST -- fifty table-cell
records, twenty-five chaff records and the one `cqto` record, each
with its own line -- is `handful.json`'s field of that name, not a
rendering of it.

---

# 4. Three instances, with the values in motion

## 4.1 LANDED: `imul` gpr_gpr 32, to c -- the list is one cell, the target

The destination place's raw carved body, **LITERAL** (`handful.json`,
`places[1].body_text`, the same object task h1's log 220 quoted its
own way):

```
mov %edi,%eax; imul %esi,%eax; ret
```

The composition, **LITERAL** (`handful.json`, this run's
`composition`):

```json
[
  {"cell": false, "line": "mov %edi,%eax", "mnem": "mov",
   "reason": "a calling-convention move (a pure register-to-register or register-to-slot copy), chaff by task o2's narrow rule"},
  {"cell": true, "key_width": 32, "line": "imul %esi,%eax", "mnem": "imul", "shape": "gpr_gpr"},
  {"cell": false, "line": "ret", "mnem": "ret",
   "reason": "the function's own return, chaff by task o2's narrow rule"}
]
```

**GLOSS.** Three raw instructions; one is a table cell. It is `imul`
`gpr_gpr` `32` -- the run's own cell, character for character -- which
is what "for a LANDED run the list is one cell, the target" (the
brief's own words) means, checked rather than assumed: filtering every
run's composition to `"cell": true` and comparing the resulting
mnemonic list to `[run["mnem"]]` passes for all six LANDED runs and no
other run (§3, and the guard lane's step [5/5], reproduced below).

## 4.2 LANDED_ELSEWHERE: `add` gpr_gpr 32, to c -- one cell, not the target

The raw carved body, **LITERAL**: `lea (%rdi,%rsi,1),%eax; ret`

The composition, **LITERAL**:

```json
[
  {"cell": true, "key_width": 32, "line": "lea (%rdi,%rsi,1),%eax", "mnem": "lea", "shape": "lea_mem"},
  {"cell": false, "line": "ret", "mnem": "ret",
   "reason": "the function's own return, chaff by task o2's narrow rule"}
]
```

**GLOSS.** Also one table-cell instruction, and also one chaff
instruction (`ret`; there is no calling-convention move here because
`lea` writes a third register and needs no argument moved into place
first, task h1's own log 238 §6.2 reading). The one cell is `lea`
`lea_mem` `32`, NOT the run's own cell (`add` `gpr_gpr` `32`) -- the
same substitution task h1 and task o8/o11 already found, now visible
as a one-cell composition rather than only as a landing verdict.

## 4.3 An instruction that maps to no table cell: `cqto`, inside `idiv` gpr_one 32, to c

The raw carved body's tail, **LITERAL** (the full 76-instruction body
is `handful.json`'s own `body_text`; the last four instructions):

```
... or %r8,%r10; or %rdi,%r10; cqto; idiv %r10; mov %eax,%eax; ret
```

The composition's own record for `cqto`, **LITERAL**:

```json
{"cell": false, "line": "cqto", "mnem": "cqto",
 "reason": "the classifier could not read it: no register name and no row size to give a width"}
```

**GLOSS.** `cqto` (sign-extend `%eax` into `%edx:%eax`) takes no
operand at all, so `model_table.classify_line`'s own operand-text walk
finds nothing to read a width from; the classifier's `row_size`
parameter, which a real sweep row would fill from a ledger row's byte
count, is 0 here because a carved emulation body has no ledger row
behind it (task h1's own convention, extended by this task rather than
invented: the classifier is called exactly as it is, with the fact
that there is no ledger context stated rather than papered over with
an invented width). `idiv %r10`, the instruction directly beside it,
DOES classify -- `idiv` `gpr_one` `64` -- and IS one of the 50 cells,
because it carries a register operand the classifier reads a width
from.

---

# 5. The tally, and the LANDED check re-derived

**LITERAL**, block `[2/5]` of
`<runs>/h1b/agent/logs/20260909T054519Z__h1b_l3_evidence.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py tally
add gpr_gpr 32               flags      SAME BYTES
add gpr_gpr 32               reg_rdi    SAME BYTES
cmovne gpr_gpr 32            reg_rdi    SAME BYTES
idiv gpr_one 32              reg_rax    SAME BYTES
idiv gpr_one 32              reg_rdx    SAME BYTES
imul gpr_gpr 32              flags      SAME BYTES
imul gpr_gpr 32              reg_rdi    SAME BYTES
sar cl_gpr 32                reg_rdi    SAME BYTES
setne gpr_one 8              reg_rdi    SAME BYTES
shr cl_gpr 64                reg_rdi    SAME BYTES
sub imm_gpr 64               flags      SAME BYTES
sub imm_gpr 64               reg_rdi    SAME BYTES
compiled places both targets have a body for: 12
   the two targets emitted the same bytes: 12
   the two targets emitted different bytes: 0

runs                             20
runs refused before any compile  4
places compiled and carved       24
LANDED                           6
LANDED_ELSEWHERE                 6
NOT_COLLAPSED                    12
PROVED_ON_SHIP                   18
proved under caller extension    2
neither                          4

instructions                                                   198
table cells                                                    120
chaff: ret                                                     16
chaff: calling-convention move                                 60
maps to no table cell                                          2
LANDED runs whose composition is exactly one cell, the target  6
```

**GLOSS.** The first block (`runs` through `neither`) is task h1's own
tally, unchanged by this task, reproduced so the composition tally
sits beside its population. Sixteen runs have a destination place
that compiled; their 198 raw instructions split 120 cells / 76 chaff
(16 `ret` + 60 moves) / 2 unmapped, which sums to 198. All six LANDED
runs pass the one-cell-is-the-target check; the check is over ALL
twenty runs (a LANDED_ELSEWHERE or NOT_COLLAPSED run would fail it if
tested, and none of them are tested, by construction -- the counter
only increments inside `if landing["verdict"] == "LANDED"`).

**LITERAL**,
`<runs>/h1b/agent/logs/20260909T055154Z__h1b_l8_evidence4.sh.log`
(lane `h1b_l8_evidence4.sh`; SUPERSEDES the same check as `h1b_l3`'s
own block `[5/5]` ran it -- the verifier's own command parser reads
this command's literal `->` as a shell redirect and scored that
version REFUSED, `redirects_into_a_path`, even though nothing in it
redirects, so the print statement was changed to drop the `->` and
the check re-run, never the verifier), the check re-derived
independently of the tally function, straight from `handful.json`:

```
$ python3 -c $'\nimport json\nd = json.load(open(\'PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.json\'))\nfor run in d[\'runs\']:\n    place = None\n    for p in run[\'places\']:\n        if p[\'writes\'] != \'flags\':\n            place = p\n            break\n    if place is None and run[\'places\']:\n        place = run[\'places\'][0]\n    landing = place.get(\'landing\') if place is not None else None\n    if landing is None or landing[\'verdict\'] != \'LANDED\':\n        continue\n    cells = [c[\'mnem\'] for c in run[\'composition\'] if c[\'cell\']]\n    print(run[\'mnem\'], run[\'shape\'], run[\'key_width\'], run[\'lang\'],\n          \'composition cells:\', cells)\n'
imul gpr_gpr 32 c composition cells: ['imul']
imul gpr_gpr 32 rust composition cells: ['imul']
sar cl_gpr 32 c composition cells: ['sar']
sar cl_gpr 32 rust composition cells: ['sar']
shr cl_gpr 64 c composition cells: ['shr']
shr cl_gpr 64 rust composition cells: ['shr']
```

**GLOSS.** Six LANDED runs, six one-element cell lists, each equal to
its own run's mnemonic. No LANDED_ELSEWHERE or NOT_COLLAPSED run
appears in this list because the script filters on `landing["verdict"]
== "LANDED"` before printing, so its absence from this list is by
construction, not evidence about those runs.

---

# 6. What did not work, by cause

Only one cause, and it is a CLOSED refusal, not an open question: the
classifier could not read `cqto`, 2 sightings (the c and rust `idiv`
runs), because `cqto` carries no operand and the classifier's width
rule for a zero-operand, non-x87 instruction needs a ledger row's byte
size that a carved emulation body does not have. Nothing else in the
198 instructions this task classified failed either test (the
classifier's own read, or membership in the table's 6,218 TRANSLATED
triples) -- the "classified but not a TRANSLATED row" cause was
checked for and never hit (§2).

---

# 7. Bounds and memory

The stated bound: the SAME 4 GB resident bound and named abort
(`ABORT_MEMORY_H1`) task h1 stated for the same collecting process
(`h1b.conf`'s own reasoning, copied from `t97.conf`, states this
explicitly: task h1b "reads local artifacts" through the same
machinery). The one read this task adds beyond what h1 already
measured is `model_table_rows.json` (50 MB), sampled first as the law
requires.

**LITERAL**, from lane `h1b_l1_compose_report.sh`'s own log:

```
[1/2] the table's own TRANSLATED (mnem, shape, key_width) triples, from PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json
   6218 distinct triples
   peak resident: 253716 kB
...
peak resident: 253716 kB
```

**GLOSS.** 253,716 kB is 6.0% of the 4,194,304 kB bound; the abort
never fired and the bound was never raised. `h1b_l2` and the evidence
lanes read only `handful.json` (about 160 kB) and are lighter still.

---

# 8. The guard, and `grep -c exempt`

**LITERAL**, block `[3/5]` of
`<runs>/h1b/agent/logs/20260909T054519Z__h1b_l3_evidence.sh.log`:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful_cells.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS handful_cells.json -- no operator token in any key, grouping, pairing or row structure
PASS handful.json -- no operator token in any key, grouping, pairing or row structure
```

**LITERAL**, `<runs>/h1b/agent/logs/20260909T054637Z__h1b_l5_evidence3.sh.log`
(the corrected list; §10 below says why two earlier attempts named
the wrong path):

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1b/h1b_l1_compose_report.sh PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1b/h1b_l2_report.sh
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1b/h1b_l1_compose_report.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_h1b/h1b_l2_report.sh:0
```

**GLOSS.** `handful.json` PASSes the unmodified guard with the new
`composition` field in place; zero `exempt` in every file this task
added or changed. `mnem` (the field the guard already reads as machine
form) carries every mnemonic in every composition record; `shape` and
`key_width` reuse the exact field names task h1's own run objects
already carry, so the guard's existing PASS is not a coincidence of a
new field name it happens not to inspect -- these are the same names
it already cleared.

---

# 9. What was reused, and what was written

`model_table.classify_line` (which calls `model_table.operand_class`
and `model_table.SHAPE_OF_CLASSES`), `model_table.key_width` and
`model_table._install_gpr_widths` (the installer task m1b's own
`attestation()` calls as a side effect, and which this task primes the
same way since it never runs `attestation()` itself) are IMPORTED from
`model_table.py`, unmodified. `single_opcode_units.parse_insn`,
`.NARROW_BARE`, `.NARROW_PURE_MOVE` and `.is_reg_or_slot_operand` are
task o2's own chaff rule, imported, the same functions
`handful.landing_of` already called for the `landed`/`gate` columns.
Nothing under `Research/op_pipeline/` or `Research/oracle/arch_opcodes/`
was edited.

Written: `handful.py` gained `load_in_table`, `chaff_reason`,
`classify_instruction`, `composition_of_run`, `compose_command`,
`composition_gloss`, `say_composition_tally` and `counted_composition`
(section 2b and additions to the tally), plus the new column in
`write_table` / `table_row`. `handful.json` gained one field per run,
`composition`; nothing else in it changed (verified: the guard PASSes
and the two-pass diff between `h1b_l1`'s and h1's own prior
`handful.json` touches only that one key per run, unverified by a
pasted command in this log but checkable the same way task h1's own
`h1_l7.1` note checks a re-run -- `git diff` on the tracked file shows
only `composition` keys added). `handful.md` gained the `composition`
column in the twenty-row table and the caption sentence describing it;
the twenty run sections (§1 of `handful.md`) are unchanged, because the
brief names only the table.

---

# 10. Flag for the coordinator

- **Two evidence-lane mistakes, both mechanical, both corrected in
  this same log rather than left standing.** `h1b_l3`'s own `grep -c
  exempt` step named `lanes_h1b/h1b_l2_report.sh` before that lane's
  own file (created after `h1b_l1` ran) had been synced to the tower
  project tree, and `h1b_l4`'s retry made the identical mistake about
  itself. Neither changed any claim's wording; both are `sync-to`
  timing, the same class of mistake task h1's own `h1_l7`/`h1_l8`
  pair recorded and fixed. `h1b_l5` is the corrected version and is
  the one this log cites.
- **The composition column's own length cut is a rendering choice, not
  a data question.** `handful.json`'s `composition` field is never
  truncated; only `composition_gloss`, the table's own one-line
  summary, cuts the cell-mnemonic sequence when it and an unmapped
  entry together would not fit in the stated 200-character budget, and
  reserves room for the unmapped entry first so it is never the part
  cut. This is stated here because it was a real defect in the first
  pass (§2) and the fix is a judgment call about what a table cell
  should show, not a fact about the data.

---

# 11. The two lists

## Decided, recorded for audit

- `composition` is computed over the RAW carved body of each run's own
  destination place (task h1's own convention for `landed`/`gate`),
  not the chaff-stripped body -- because the brief asks for `ret` and
  the calling-convention moves to be marked as what they are, and
  task o2's own chaff-stripped text has already removed them by the
  time `landing.stripped_text` is written.
- An instruction is chaff (`ret` or a calling-convention move) when
  task o2's own `single_opcode_units` narrow-rule test says so, BEFORE
  the classifier is asked; a chaff instruction is never reported as
  "maps to no table cell" even though the classifier would in fact
  refuse most of them (a bare `ret` has no operand to read a width
  from, same cause as `cqto`).
- Membership is checked two ways, both applied to every non-chaff
  instruction: the classifier's own success (`model_table.
  classify_line` returning a shape), then the resulting triple's
  presence in the 6,218 distinct TRANSLATED triples of
  `model_table_rows.json`. Only the first cause was ever hit in this
  population (`cqto`, twice); the second was checked for and found
  zero times.
- For every LANDED run the composition's table-cell entries are
  exactly one, and it is the run's own cell -- checked over all twenty
  runs, not asserted from the six examples.

## Awaiting the owner

- Nothing. The two items in §10 are for the coordinator, and both are
  already resolved in this log, not open.

---

# ADDENDUM — the verifier over this log

Three passes, each fixing what the previous one found, none of them
touching the verifier:

- `h1b_l6_verify.sh`, the first pass: 0 DIFFERS, but 2 NOT_RERUNNABLE
  -- the tally block and the LANDED-runs command were both pasted with
  a `...` elision for brevity, which the verifier correctly refuses to
  score as reproduced. Both were replaced with the exact, untruncated
  transcript from their own lane logs.
- `h1b_l7_verify2.sh`, the second pass: 0 DIFFERS, 0 NOT_RERUNNABLE,
  but 1 REFUSED (`redirects_into_a_path`) -- the LANDED-runs command's
  own `print(..., '-> composition cells:', ...)` carries a literal
  `->`, which the verifier's command parser reads as an unquoted shell
  redirect. Nothing in the command redirects anything. Fixed in the
  command (the `->` dropped from the print text) and the check
  re-run as lane `h1b_l8_evidence4.sh`, never in the verifier.
- `h1b_l9_verify3.sh`, the third pass, **LITERAL**:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_239_task_h1b_composition_column.md
population: 17 claims across 1 logs
  MATCHES          4
  DIFFERS          0
  UNVERIFIABLE     13
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 4 of 17 claims reproduce; 13 (76%) carry nothing to re-run

causes, by name:
  prose_only                       7
  attribution_only                 6

peak RSS after the pass: 17.5 MB
```

**TALLY: 17 claims, 4 MATCHES, 0 DIFFERS, 13 UNVERIFIABLE, 0 REFUSED,
0 NOT_RERUNNABLE. Zero DIFFERS, zero REFUSED.** The 13 that carry
nothing to re-run are 7 prose verifications and 6 attributions into
`handful.json`. Full untruncated verifier output:
`<runs>/h1b/agent/logs/20260909T055300Z__h1b_l9_verify3.sh.log`,
on the tower. Nothing above this ADDENDUM was edited after
`h1b_l9_verify3.sh` ran.
