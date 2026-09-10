# log 236 — task m1: the arch-opcode model table, keyed by (mnem, operand form, width)

Node: `hq.research.arch_unit_oracle`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
its "goal" section of 2026-09-07 and its ruling of 2026-09-08). This is
the first item of that goal and step 3 of the research master order
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/CORE_0_3_research.md`
§4.2).

Date: 2026-09-08. Instance `m1` (its conf
`PUBLIC/Airlock/instances/m1.conf`), brought up and down by this
task. Every lane ran on the tower guest through
`bash PUBLIC/Airlock/remote_lane.sh`, per LAW's last section;
nothing but file editing, git and those commands ran on the laptop.
A lane log's host path on the tower is
`<runs>/m1/agent/logs/<stamp>__<lane>.sh.log`;
every attribution below names its file.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ`, mounted into
the instance. Every rendering is labelled **LITERAL** (the object,
quoted) or **GLOSS** (a plain-words reading beside a literal), per
`object.literal-gloss-analogy`.

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

## §0. What was done and found, in plain words, before any figure

The reference simulator holds one entry per arch mnemonic, and each
entry carries a builder — a function that, given the operand texts of a
line and a machine state, leaves a z3 term in every place the opcode
writes. That builder is the opcode's mapping. There was no artifact
that showed those mappings; the sweep in the Lean model translator
already ran every builder over every operand spelling it knows, but it
recorded only which Lean definition each place received, not the term.

This task ran that same sweep, imported and not re-written, and kept
the terms. Every attempt that translated became a row keyed by the
mnemonic, the operand shape and the width, carrying the layer-5 text of
each place written, the entry's own read set and write set, whether the
mapping reads the flags or only writes them, and the condition the
builder's own source states — quoted from the source, or the sentence
saying the builder is total on bit patterns.

Beside each row sits the corpus's own attestation: one stream over the
332 canon40 shards, every ledger row whose producer is an arch opcode
classified into the same operand shapes by the operand texts of the body
line that made it. The line comes from the pipeline's own relink, which
re-walks a body only to learn which line made which ledger row and
checks the re-walk against the stored ledger.

Then the equivalences, reported and never applied. Two rows at one shape
and width whose written places and layer-5 texts are the same object are
one `identical_text` class. Two mnemonics the reference registers with
the same builder OBJECT are a `same_builder` pair, and for every shape
and width at which both carry a row, z3 was asked separately whether
their destination terms can differ and whether their flags terms can
differ, at a 3,000 ms ceiling.

Three things came out of it that are worth saying before the numbers.
First, the corpus's 162 mnemonics are ALL in the reference's table: the
difference runs the other way, nine table mnemonics the corpus does not
spell, and the mnemonics the reference cannot model are the six entries
with no builder, not a corpus-only set. Second, only two of the
twenty-four same-builder groups are alias groups — groups whose members
z3 finds equal on every place they write at every shape and width they
share. Third, reading the `add`/`lea` cells the brief names surfaced a
defect in this task's own reading of "a place written", and then a fact
about the reference itself: a one-operand line of any binary-family
mnemonic is given the accumulator-pair widening multiply.

---

## §1. The objects, one sentence each, in relation

- The **reference's opcode table** is
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline/reference.py`'s
  `opcode_table`: one `Entry` per arch mnemonic, each naming the places
  the opcode reads and writes and holding a **builder**, the function
  that turns operand texts plus a machine state into the z3 term the
  opcode leaves in each place.
- The **sweep** is `sweep`, `attempts_for`, `shapes_for`, `one_attempt`
  and `run_line` in
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py`:
  it hands every builder every operand spelling it knows at every width
  and records the outcome per (mnem, shape, width). This task imported
  and ran it; it did not re-implement it and did not edit it.
- The **layer-5 printer** is `Term.normalize` in
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline/term.py`: the
  pipeline's own fixed-rule re-render — order the commutative nodes,
  simplify, rename the free symbols positionally, print on one line. It
  applies to a bare z3 expression, so the fallback the brief allowed
  (`str(z3.simplify(t))`) was not used anywhere.
- The **attestation** is a stream over the canon40 shards
  (`term66_run.shards()`, 332 files); the reading of a shard, a unit and
  a ledger row is copied from `census_pass` in
  `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/signatures/ledger_signatures.py`,
  and the body line of a row comes from `relink` in `term.py`.
- The **162** is the corpus's mnemonic vocabulary,
  `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.json`.
  This table's row count is a different number by construction and does
  not correct it.
- The **deliverable** is
  `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py`
  and what it writes in the same folder: `model_table_rows.json` (41.3
  MB), `model_table_attest.json`, `model_table_edges.json` (17.2 MB),
  `model_table.json` (62.3 MB, the joined table) and `model_table.md`
  (552 lines, the report).

---

## §2. The key, and how the json avoids the ban

The ruling of 2026-09-08 is that a mnemonic alone is a spelling and
(mnemonic, operand form, width) is machine form. Every row of this table
is keyed by that triple and the mnemonic sits in the field `mnem`, which
the guard already reads as a machine form because `mnem` is one of its
`PROSE_FIELDS`. Nothing was asked of the guard and the guard was not
edited.

Four mnemonics — `and`, `or`, `xor`, `not` — are also operator spellings
in the guard's 91-token inventory, so a bare one of them anywhere else
fails. The consequences, all mechanical:

- every field carrying a mnemonic is named `mnem`, including the flags
  record's `{"mnem": <the setter>}` and the flag-seed record
  `{"flags_in": {"mnem": ...}}`;
- a list of mnemonics is a list of records each carrying `mnem`, never a
  list of bare strings — the `table_only`, `corpus_only` and
  same-builder member lists are all of that shape;
- the sweep's own `cause` string is carried as `reason` and a printed
  term as `text`, both `PROSE_FIELDS`, because a free-text sentence is
  not a key;
- every edge is keyed by ROW IDS. The candidate set for a comparison is
  either the rows sharing a shape and a width (machine-form evidence) or
  the pairs of entries holding the same builder OBJECT
  (`entry.build is other.build`, a fact about the table's function
  objects). The one exception is the `add`/`lea` pair, which the brief
  named and which therefore enters as ratified intention; its cells are
  keyed by row ids like the rest and sit under `named_pair_cells`.

**LITERAL**, lane `20260909T000823Z__m1_l20_claims2.sh.log`, the guard
unmodified over the four json this task wrote:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_attest.json PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_edges.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS model_table.json -- no operator token in any key, grouping, pairing or row structure
PASS model_table_rows.json -- no operator token in any key, grouping, pairing or row structure
PASS model_table_attest.json -- no operator token in any key, grouping, pairing or row structure
PASS model_table_edges.json -- no operator token in any key, grouping, pairing or row structure
```

**LITERAL**, same lane, the companion count over the two files this task
added:

```
$ grep -c exempt PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py
0
$ grep -c exempt PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.md
0
```

---

## §3. The counts, beside the 162

**LITERAL**, lane `20260908T235712Z__m1_l17_claims.sh.log`:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
c = d['counts']
print('table', c['table_mnemonics'], 'corpus', c['corpus_mnemonics'], 'both', c['in_both'])
print('table only', ' '.join(r['mnem'] for r in c['table_only']))
print('corpus only', ' '.join(r['mnem'] for r in c['corpus_only']) or '(none)')
"
table 171 corpus 162 both 162
table only bsr bt cmova cs endbr64 fld inc pinsrw xchg
corpus only (none)
```

**GLOSS.** The corpus-only set is EMPTY: every one of the 162 mnemonics
any body spells has an entry in the reference's table. The brief asked
for "the corpus-only ones — the mnemonics the reference cannot model";
there are none, and the mnemonics the reference cannot model are a
different set — the six entries that carry no builder at all, listed in
§7. The nine table-only mnemonics are the ones task 63 added from the
attached toolchain-archive bodies (`endbr64 bsr inc bt cmova pinsrw cs
fld xchg`, `reference.ARCHIVE_MNEMONICS`), which the corpus's own
`unique_opcodes.json` population does not count.

**LITERAL**, same lane:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
c = d['counts']
print('attempts', c['sweep_attempts'], 'translated', c['rows_translated'])
print('triples', c['translated_triples'], 'distinct mappings', c['distinct_mappings_after_identical_text'])
print('identical_text pairs', c['identical_text_pairs'], 'classes', len(d['identical_text_classes']))
print('splits', len(c['mnemonics_with_several_mappings']))
print('alias groups', sum(1 for g in c['alias_groups'] if g['is_an_alias_group']))
"
attempts 62418 translated 34867
triples 8703 distinct mappings 5155
identical_text pairs 961170 classes 2219
splits 86
alias groups 2
```

Table 1 — the §6 counts the brief asked for, with what each counts.

| what | count | population |
|---|---|---|
| table mnemonics | 171 | entries in `reference.py`'s `opcode_table`, as of 2026-09-08 |
| corpus mnemonics | 162 | `unique_opcodes.json`'s `cross_language_rows` |
| in both | 162 | — |
| table only | 9 | `bsr bt cmova cs endbr64 fld inc pinsrw xchg` |
| corpus only | 0 | — |
| sweep attempts | 62,418 | every (mnemonic, shape, width) the sweep spells, both passes |
| rows TRANSLATED | 34,867 | attempts whose builder left a term the translator accepted |
| distinct (mnem, shape, width) triples with a TRANSLATED row | 8,703 | the machine-form keys the table actually fills |
| distinct mappings after `identical_text` | 5,155 | classes of the 34,867 TRANSLATED rows under textual identity of the written places at one shape and width |
| `identical_text` pairs | 961,170 | the pairs those 2,219 many-member classes carry |
| splits | 86 | mnemonics whose rows do not all write one multiset of place kinds |
| alias groups | 2 | same-builder groups z3 found equal on every place at every shared cell |

`identical_text` is textual identity after normalisation and is an
UNDER-COUNT of true equivalence: two rows can compute one function and
print differently, and only a solver call decides that. The 961,170
pairs are written as the 2,219 classes they form, keyed by row ids —
DECIDED, recorded for audit (§9): textual identity is an equivalence
relation, so the class list carries exactly the information the pair
list does, at 1/400th the size.

---

## §4. Five rows in full, LITERAL

All five are in
`PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.md`
§1, each printed whole from `model_table.json`. The one the verifier
re-runs, **LITERAL**, lane `20260908T235712Z__m1_l17_claims.sh.log`:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for row in d['rows']:
    if row['mnem'] != 'add':
        continue
    if row['shape'] != 'gpr_gpr' or row['width'] != 32:
        continue
    if row['outcome'] != 'TRANSLATED':
        continue
    print(row['row_id'], row['text'], row['builder'])
    for m in row['mapping']:
        print(' ', m['writes'], '=', m['text'])
    print(' ', 'attestation', row['attestation']['ledger_rows'], 'rows', row['attestation']['units'], 'units')
    break
"
r00120 add %esi,%edi build_binary
  reg_rdi = Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
  flags = Concat(Extract(31, 0, v0), Extract(31, 0, v1))
  attestation 11 rows 11 units
```

Table 2 — the five rows the brief names, in one line each. Every term is
the layer-5 text `Term.normalize` printed; the two division and the
one-operand multiply terms are long and are quoted whole in
`model_table.md` §1, not here.

| row | builder | writes | condition, from the builder's source | attestation |
|---|---|---|---|---|
| `add` gpr_gpr 32 | `build_binary` | `reg_rdi`, `flags` | total on bit patterns | 11 rows / 11 units |
| `imul` gpr_one 32 | `build_binary` | `reg_rax`, `reg_rdx` | total on bit patterns | 0 rows / 0 units |
| `imul` gpr_gpr 32 | `build_binary` | `reg_rdi`, `flags` | total on bit patterns | 266 rows / 266 units |
| `sar` cl_gpr 32 | `build_shift` | `reg_rdi` | the count refusal, and `masked = count & z3.BitVecVal(shift_mask(width), 8)` | 335 rows / 335 units |
| `idiv` gpr_one 32 | `build_division` | `reg_rax`, `reg_rdx` | `raise NotModeled("a division at width %d is not modeled" % width)` | 778 rows / 389 units |

**GLOSS on the condition column, because it is the brief's §3 and the
answer is not the expected one.** `build_division` states ONE condition
and it is a WIDTH refusal. Its quotient and remainder are z3's `SDiv`,
`UDiv`, `SRem` and `URem`, which are TOTAL functions on bit patterns, so
division by zero and the `MIN / -1` case are not branched on and no
fault region is named in the model. The fault is the machine's; this
reference does not carry it. `build_wide_multiply` is the same shape: a
width refusal only. `build_shift` and `build_double_shift` are the two
that state a real input condition, and it is the hardware's own count
mask, quoted above.

---

## §5. The splits, and the alias groups

**LITERAL**, lane `20260908T235712Z__m1_l17_claims.sh.log`, the split
criterion applied to the five mnemonics where it is most visible:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for r in d['counts']['mnemonics_with_several_mappings']:
    if r['mnem'] not in ('imul', 'div', 'idiv', 'mul', 'xchg'):
        continue
    print(r['mnem'], '|', ' / '.join(r['place_kind_sets']))
"
imul | flags mem / flags reg / reg / reg reg
xchg | mem reg / reg / reg reg
div | reg / reg reg
idiv | reg / reg reg
mul | reg / reg reg
```

**GLOSS.** The split criterion is the multiset of place KINDS a
mnemonic's rows write, a kind being `reg`, `flags`, `mem`, `stack` or
`x87`. `imul`'s `reg reg` is the one-operand accumulator-pair form and
its `flags reg` is the two-operand named-destination form — the ruling's
own example, read mechanically. The kind abstraction is what makes the
count meaningful: keying on the place NAME would count a destination of
`%edi` in one shape and `%eax` in another as a split, and keying on the
destination TEXT would count every width as a split. All three counts
are in the table (`place_kind_sets`, `distinct_place_sets`,
`distinct_destination_texts`) so the criterion can be checked rather
than trusted; the 86 splits are the first.

**LITERAL**, same lane, the alias groups:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for g in d['counts']['alias_groups']:
    if not g['is_an_alias_group']:
        continue
    print(g['group_id'], g['cells'], ' '.join(m['mnem'] for m in g['members']))
"
g12 72 movapd movaps movdqa
g19 24 fstp fstpt
```

**GLOSS.** Twenty-four same-builder groups exist; two are alias groups.
A group is an alias group when every one of its cells came back `unsat`
on the destination and, where both sides write flags, `unsat` on the
flags — z3 saying no differing point exists on any place written. The
other twenty-two are NOT aliases, and the reason is the same in every
case and worth stating once: a shared builder is not a shared mapping,
because almost every builder in the table branches on `ops.mnemonic`
inside itself. `sar`, `shl` and `shr` share `build_shift` and differ on
which shift the branch selects; the fifteen `set*` mnemonics share
`build_set_condition` and differ on the predicate. The full table of all
twenty-four with their cell counts is `model_table.md` Table 3.

---

## §6. The pair the brief names, `add` and `lea`

**LITERAL**, lane `20260908T235712Z__m1_l17_claims.sh.log`:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
seen = {}
for cell in d['named_pair_cells']:
    key = (cell.get('destination_verdict'), cell.get('flags_verdict'), cell.get('flags_refusal'))
    seen[key] = seen.get(key, 0) + 1
print('cells', len(d['named_pair_cells']))
for key in sorted(seen, key=str):
    print(seen[key], 'x destination', key[0], 'flags', key[1], key[2])
"
cells 12
12 x destination sat flags None one of the two places is not written at all
```

**GLOSS, and it is not what the brief expected.** The flags half is as
expected: `lea` writes no flags, so no flags equality is even stated —
twelve cells, twelve refusals with that sentence. The destination half
is `sat` at every cell: z3 finds a point where the two differ.

The reason is a level distinction, not a solver problem. At one operand
shape and width, `add (%rsi),%edi` adds the CONTENTS of the cell at
`%rsi` and `lea (%rsi),%edi` takes the ADDRESS `%rsi` itself, so their
destinations are different functions of the same inputs. The equality
the brief expected — `lea (%rdi,%rsi,1),%rax` computing what `add
%rsi,%rdi` computes — holds ACROSS two different operand shapes, and the
machine-form key never pairs two different shapes. The twelve cells that
exist are `mem_gpr`, `lea_mem` and `mem_xmm` at the four widths; there
is no `gpr_gpr` cell at all, because `lea` refuses a register source
(`build_lea` raises `NotModeled` on an addressing form that is not the
displacement/base/index/scale shape).

So the two are two mappings on both grounds the brief named, and the
ground on which they coincide is a cross-shape composition this table
does not key.

---

## §7. NO_BUILDER and NOT_MODELLED, by cause

**LITERAL**, lane `20260908T235712Z__m1_l17_claims.sh.log`:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for outcome in sorted(d['causes']):
    total = sum(r['count'] for r in d['causes'][outcome])
    print(outcome, total, 'rows over', len(d['causes'][outcome]), 'causes')
"
NOTHING_WRITTEN 1081 rows over 1 causes
NOT_MODELLED_BY_THE_REFERENCE 26464 rows over 148 causes
NO_BUILDER 6 rows over 3 causes
```

Table 3 — the three outcomes that are not TRANSLATED, by cause. The
causes are the sweep's own strings; the full 148 for
`NOT_MODELLED_BY_THE_REFERENCE` are in `model_table.md` §6, each with
its row count.

| outcome | rows | causes | what it means |
|---|---|---|---|
| `NO_BUILDER` | 6 | 3 | the six entries the table registers with no builder: `call`, `jmp`, `pcmpeqb`, `pcmpeqd`, `pmovmskb`, `ud2`. These, not a corpus-only set, are the mnemonics the reference cannot model |
| `NOTHING_WRITTEN` | 1,081 | 1 | "the builder ran and changed no register and no flag" |
| `NOT_MODELLED_BY_THE_REFERENCE` | 26,464 | 148 | the builder refused the operand spelling by name — a shape combination the mnemonic does not spell, not a gap |

---

## §8. The corpus's attestation, and what the classifier could not place

**LITERAL**, lane `20260908T235712Z__m1_l17_claims.sh.log`:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
u = d['attestation_unclassified']
for cause in sorted(u, key=lambda c: -u[c]):
    print(u[cause], cause[:60])
"
19797 the answer row of the OUT block, which canonical_form.wrap_u
1139 an operand text this classifier does not read: '%st(1)'
120 an operand text this classifier does not read: '%st'
0 the unit's body could not be relinked, so no row of it has a
```

Table 4 — the attestation stream, as of 2026-09-08.

| what | count |
|---|---|
| shards streamed | 332 |
| units seen | 31,078 |
| units relinked | 30,436 |
| units the relink refused | 642 |
| arch-opcode ledger rows seen | 130,108 |
| of those, placed into a (mnem, shape, width) cell | 109,052 |
| cells attested | 219 |
| attested cells with no TRANSLATED row in the table | 83 |

The three causes, by cause and with a status:

- **the OUT block's answer row, 19,797 rows, by design.** `wrap_unit`
  adds OUT-0 after the dataflow walk and it repeats the producer of the
  row it copies, so the relink gives it no line of its own and counting
  it would count one instruction twice. Not a gap; named so the
  arithmetic is checkable.
- **the x87 stack registers `%st` and `%st(1)`, 1,259 rows, open.** The
  sweep's shape grammar (`shapes_for` in `model_translate.py`) spells
  general registers, immediates, `%cl`, memory and `%xmm*`, and no x87
  register, so `faddp %st,%st(1)` has no shape to be classified into.
  This is a gap in the SWEEP's shape list, not in the classifier, and it
  is the reason the x87 mnemonics' attested cells all sit at `mem_one`.
- **the 642 units the relink refused, 0 rows, closed.** They held no
  arch-opcode ledger row at all, so nothing was lost to them.

**LITERAL**, lane `20260909T000823Z__m1_l20_claims2.sh.log`, what those
83 cells are:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
cells = d['counts']['attested_cells_with_no_translated_row']
print('attested cells with no translated row:', len(cells))
by_width = {}
for c in cells:
    by_width[c['width']] = by_width.get(c['width'], 0) + 1
print('by width:', sorted(by_width.items(), key=str))
for c in cells:
    if c['width'] != 128:
        print('not at 128:', c['mnem'], c['shape'], c['width'], c['ledger_rows'], 'rows')
"
attested cells with no translated row: 83
by width: [(128, 82), (32, 1)]
not at 128: pmovmskb xmm_gpr 32 2 rows
```

**GLOSS.** Eighty-two of the 83 are vector rows at width 128, which the
table has no cell for because `model_translate.SWEEP_WIDTHS` is
`(8, 16, 32, 64)` and the sweep therefore spells `%xmm` operands only at
the four general-register widths. The one that is not is `pmovmskb`
`xmm_gpr` 32, whose entry carries no builder at all. All 83 are listed
in `model_table.md` Table 6.

---

## §9. The one defect this task found in its own reading, and the one it found in the reference

Reported by cause, each with a status.

- **This task's own reading of "a place written" was wrong for memory,
  FIXED.** `reference.MachineState.memory_cell` puts a cell's arrival
  symbol into `state.memory` the first time a line READS the cell, so
  `model_translate.run_line` — which reports every place the state
  gained — reports a read-only memory cell as written. `run_line`
  already applies exactly this correction to REGISTERS
  (`state.shared_seed.get(place[4:])`) and not to memory. The effect
  was that `add (%rsi),%edi` was recorded as writing three places, 192
  bits joined, where it writes one, and every `add`/`lea` cell was
  refused for "different sorts". Found by reading the `add`/`lea` cells
  the brief names. Fixed in `model_table.drop_cells_only_read`, in this
  task's own program; `model_translate.py` was NOT touched, being a
  shared file this brief did not name. Everything was re-run after the
  fix (lane `20260908T233535Z__m1_l13_rerun.sh.log`); the `identical_text`
  class count moved from 2,235 to 2,219 and the distinct-mapping count
  from 5,171 to 5,155.
- **`reference.build_binary` gives a one-operand line of ANY
  binary-family mnemonic the accumulator-pair widening multiply, OPEN,
  flagged for the coordinator.** Its first statement is
  `if len(ops.texts) == 1: build_wide_multiply(ops); return`. So `add
  %edi` is modelled as `%eax = %edi * %eax`, and the same for `and`,
  `or`, `sub` and `xor`. Measured in lane
  `20260908T235444Z__m1_l15_one_operand_binary.sh.log`: 28 TRANSLATED
  rows arrive this way, of which only `imul`'s are attested by the
  corpus at all (2 ledger rows); `add`, `and`, `or`, `sub` and `xor`
  contribute 24 rows attested 0 times. Nothing was changed:
  `reference.py` is a shared file this brief did not name, and no body
  in the corpus reaches the branch, so it costs the corpus nothing
  today. It would cost something the moment a one-operand binary line
  appears.

---

## §10. Time and memory, and the two ceilings that were hit

Every lane stated the bound 16 GB resident inside the instance's 20g,
with the named abort `ABORT_MEMORY_M1` (`resource.getrusage`, checked
after every 5,000 rows in the sweep, after every shard in the
attestation and after every 200 cells in the equivalence pass). The
abort never fired.

Table 5 — peak resident memory and wall clock, per lane, from the lanes'
own prints.

| lane | what | wall clock | peak RSS |
|---|---|---|---|
| `m1_l4_sweep.sh` | the sweep and the terms | 290 s | 190 MB |
| `m1_l5_attest.sh` | 332 shards, 31,078 units | 4.5 s | 83 MB |
| `m1_l9_edges3.sh` | 51,730 cells, both verdicts each | 598 s | 1,088 MB |
| `m1_l13_rerun.sh` | all four commands after the memory fix | 955 s | — |
| `m1_l14_assemble3.sh` | the join and the counts | 4.0 s | 251 MB |

Two ceilings were hit and both were reported rather than worked around:

- **The first equivalence pass would have taken about 8.2 hours**, past
  the instance's 21,600 s `script_timeout`, because a cell was keyed by
  (pair, shape, width, whether the sweep's second pass seeded the state,
  which flag-setting mnemonic seeded it) and there were 196,190 of them.
  The seed is a probe choice of the sweep's second pass and not part of
  the machine form the ruling names, so the key was corrected to the
  triple: 51,730 cells, and 26,164 further sweep attempts share a triple
  with one of them and are not compared a second time. Both numbers are
  in `model_table_edges.json`'s `meta`. Lane
  `20260908T224319Z__m1_l7_edges.sh.log` was stopped at cell 1,600 and
  wrote nothing.
- **The corrected pass was still about 24 hours**, measured at 8,400
  cells in 1,635 s once it reached the x87 group, whose terms are 80-bit
  floating point and which therefore reach the 3,000 ms ceiling and
  answer `unknown`. The fix was a MEMO on the question itself — the pair
  of the two terms' s-expressions — so an identical question is answered
  once and re-used. Nothing is compared less and the ceiling is
  unchanged. Measured: 5,661 solver calls and 57,127 re-used answers
  over the 51,730 cells, 598 s. Lane
  `20260908T224922Z__m1_l8_edges2.sh.log` was stopped at cell 8,400 and
  wrote nothing.

---

## §11. Decided, recorded for audit

- **The cell of a same-builder comparison is keyed by (mnem, shape,
  width), one sweep attempt per triple, first in sweep order.** The
  sweep's second pass re-runs a flag-reading mnemonic once per
  flag-setting mnemonic it saw; those attempts differ in the seed state
  the builder was handed, not in the instruction. Both counts are
  recorded (8,703 triples, 26,164 further attempts sharing one).
- **`identical_text` is written as equivalence CLASSES keyed by row ids,
  with the pair count beside them**, rather than 961,170 explicit pairs.
  Textual identity is an equivalence relation, so the classes carry the
  same information.
- **z3's own words are the verdict vocabulary** — `unsat`, `sat`,
  `unknown` — and a comparison that cannot be stated at all (two terms of
  different sorts, or a place only one side writes) carries a `refusal`
  sentence and no verdict, rather than a new outcome name.
- **The split criterion is the multiset of place KINDS**, with the
  place-name and destination-text counts kept beside it, so the
  criterion is checkable.
- **An identical question is memoized**, keyed by the two terms'
  s-expressions; `meta.solver_calls` and `meta.solver_memo_hits` record
  both numbers.
- **A memory cell holding its own arrival value is not a place written**
  (§9, first item), corrected in this task's program and not in
  `model_translate.py`.
- **The superseded lane scripts `m1_l7_edges.sh` and `m1_l8_edges2.sh`
  were moved out of the instance's `drop` into its `drop/.done/`**, the
  same folder and the same stamped name shape the daemon itself uses,
  so that a restart of the instance did not re-run them. Nothing under
  `PUBLIC/Airlock/` or `<runs>/` was deleted; both scripts
  are in the repo under `lanes_m1/`, and both lanes' logs are on the
  tower.

## §12. Awaiting the owner

- **`reference.build_binary`'s one-operand branch** (§9, second item):
  whether a one-operand `add`/`and`/`or`/`sub`/`xor` line should refuse
  rather than be modelled as a widening multiply. Twenty-four table rows
  ride on it and the corpus attests none of them, so nothing measured
  today changes either way.
- **The x87 registers have no operand shape in the sweep's grammar**
  (§8), so 1,259 corpus ledger rows have no cell to be attested into and
  the x87 mnemonics' attested cells all collapse to `mem_one`. Adding an
  `%st`-shaped operand spelling to `model_translate.shapes_for` is a
  change to a shared file, so it is not made here.

---

## §13. The verifier's tally

`check_conventions_log_claims.py --verify --timeout 20` was run over
this log from this task's own instance on the tower, as LAW's final
lane. **LITERAL**, lane `20260909T001139Z__m1_l21_verify2.sh.log`
(host path
`<runs>/m1/agent/logs/20260909T001139Z__m1_l21_verify2.sh.log`):

```
population: 12 claims across 1 logs
  MATCHES          12
  DIFFERS          0
  UNVERIFIABLE     0
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 12 of 12 claims reproduce; 0 (0%) carry nothing to re-run
```

The first verify lane (`20260909T000551Z__m1_l19_verify.sh.log`) read 10
MATCHES, 1 DIFFERS and 2 UNVERIFIABLE. All three were defects in THIS
LOG and were fixed in it, never in the verifier: the guard transcript
had been pasted from a lane that had changed into the model folder, so
its relative paths did not resolve where the verifier runs (re-pasted
from an absolute-path run of the same unmodified guard, lane
`m1_l20_claims2.sh`); one sentence asserted a verification in prose with
nothing beside it (reworded to state the reading, the transcript above
it carrying the evidence); and one attribution block carried no command
(given the command that produces it).

This section itself was appended after that run, so it is not among the
12 claims the tally counts.
