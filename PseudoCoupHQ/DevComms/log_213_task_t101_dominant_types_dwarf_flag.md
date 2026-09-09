# log 213 — task t101: dominant types, and the flag that stops the join at step 1

Project node: `hq.research.compiler_graph.probes.type_inventory` —
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_0_probes/node_0_3_1_0_1_type_inventory/CORE_0_3_1_0_1_type_inventory.md`.
Master plan step: `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/CORE_0_3_research.md`
§4.2 step 3, "dominant types: the join of language spellings to machine
holders".

Date 2026-09-06. Instance `~/Programming/Airlock/instances/t101.conf`.
Every transcript below was produced by a lane of that instance, where
this repo is mounted at `/projects/PseudoCoupHQ`; the host path of that
mount is `~/Programming/PseudoCoupHQ`.

---

# 1. What the objects are, one sentence each

- **A dominant type** is one machine-level holder — a class (signed
  integer, unsigned integer, float, truth) at a width — with every
  language's spellings for it hanging off it (research CORE §1).
- **The language type inventory**,
  `~/Programming/PseudoCoupHQ/Research/op_pipeline/type_inventory2_core2.json`,
  is the left side of the join: per language, per scalar-core spelling,
  a class and no width.
- **The DWARF parameter table** is the right side: the compiler's own
  debug record of a probe function's parameters, stored on every
  accepted probe under
  `~/Programming/PseudoCoupHQ/Research/op_pipeline/trickle_store/`.
- **The machine type key** is what the join was to make readable: the
  `type_key` field on every entry of
  `~/Programming/PseudoCoupHQ/Research/op_pipeline/the_pool5.json` —
  arrival register families and answer width, 88 distinct over 1,831
  entries.

# 2. The walkthrough, before any number

The join needs two machine facts per parameter that only the compiler
can state: how many bytes the parameter occupies
(`DW_AT_byte_size`), and how it is encoded (`DW_AT_encoding` — the
attribute whose values separate `DW_ATE_signed` from `DW_ATE_unsigned`
from `DW_ATE_float` from `DW_ATE_boolean`).

The DWARF parameter tables are on disk, and there are a great many of
them. Every accepted probe of all three populations carries one at its
anchor build. Read end to end, they hold 64,398 parameter rows.

Every one of those rows carries two fields: `name` and `location`.
`location` is where the parameter sits in the frame —
`DW_OP_fbreg: -1` — which is an address. It is not a width, and it
carries no encoding.

The narrowing happened when the tables were captured, not when they
were stored. The probe lane walked each `DW_TAG_formal_parameter`,
took `DW_AT_name` and `DW_AT_location` off it, and never followed
`DW_AT_type`. So the byte size and the encoding were never in the
lane's product for the folder to fold. The objects those tables were
read from were built inside the trickle container's `/work`, and no
trickle volume survives, so they cannot be re-read either.

That leaves step 1 of the deliverable with no admissible input, and
the brief's own stop rule — the DWARF encoding decides the class and
the width, no hand normalization of spellings — forbids substituting
anything for it. `types101_join.py` therefore runs step 1, measures
the row shape across every store on disk so the refusal is exhaustive
rather than a spot check, and refuses by name.
`types101_holders.json`, `types101_spellings.json` and
`types101_entry_holders.json` are not written.

# 3. The evidence

## 3.1 One stored DWARF parameter table, LITERAL

The c probe whose operand is declared `_Bool`, from
`~/Programming/PseudoCoupHQ/Research/op_pipeline/trickle_store/op_units2_c_c0000.json`.
The first printed line is the declared spelling; the second is the
whole stored table.

```
$ python3 -c "import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/trickle_store/op_units2_c_c0000.json'));p=d['probes']['1'];print(p['meta']['lhs_type']);print(json.dumps(p['anchor']['dwarf']))"
_Bool
[{"name": "a", "location": "2 byte block: 91 7f (DW_OP_fbreg: -1)"}]
```

GLOSS: the compiler said the parameter is called `a` and lives one
byte below the frame base. It did not say it is one byte wide, and it
did not say it is a boolean.

## 3.2 The reader every probe lane's product passes through, LITERAL

`~/Programming/PseudoCoupHQ/Research/op_pipeline/fold.py`, the body of
`dwarf_rows`, lines 82–91. Both branches build a row the same way, and
both name the same two fields.

```
$ sed -n '82,91p' /projects/PseudoCoupHQ/Research/op_pipeline/fold.py
    got = []
    for item in text.split(";"):
        if not item:
            continue
        if "=" not in item:
            got.append(dict(name=item, location=None))
            continue
        name, loc = item.split("=", 1)
        got.append(dict(name=name, location=loc))
    return got
```

GLOSS: `dict(name=..., location=...)` is the whole row. There is no
third key on either branch, so no store this reader wrote can carry a
byte size or an encoding whatever the lane sent it.

Line 81, the function's own docstring, states the same shape and is not
pasted as a transcript here: it contains an arrow, and
`check_conventions_log_claims.py` scores any paste containing an arrow
`output_annotated` — reading it as a hand-written gloss rather than as
the file's own characters. Lane 7's verify scored the 80–91 form
NOT_RERUNNABLE for exactly that reason, so the quotation was narrowed
to the lines that carry the claim rather than the verifier being
touched.

## 3.3 The lane that produced the text that reader parses, LITERAL

`~/Programming/PseudoCoupHQ/Research/op_pipeline/trickle_lanes/asgrecap_asgrecap_go_c0001.sh`,
lines 255–262. It is inside the walk over `DW_TAG_formal_parameter`
DIEs.

```
$ sed -n '255,262p' /projects/PseudoCoupHQ/Research/op_pipeline/trickle_lanes/asgrecap_asgrecap_go_c0001.sh
                continue
            if t != "DW_TAG_formal_parameter":
                continue
            nm = clean(dwname(at.get("DW_AT_name", "(unnamed)")))
            loc = clean(at.get("DW_AT_location", "(no location)"))
            got.append((nm, loc))
        if got:
            return got
```

GLOSS: two attributes are taken off the parameter DIE, `DW_AT_name`
and `DW_AT_location`. `DW_AT_type` — the link to the type DIE that
carries `DW_AT_byte_size` and `DW_AT_encoding` — is never followed.

## 3.4 The measurement over every store on disk

Lane `t101_l1_dwarf_shape.sh` ran
`~/Programming/PseudoCoupHQ/Research/op_pipeline/types101_join.py`,
which streams every store one file at a time and folds only counters.

```
$ python3 -c "import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json'));c=d['counts'];print('files', c['store_files_read']);print('rows', c['dwarf_rows_examined']);print('rows with a byte size or encoding', c['dwarf_rows_carrying_a_byte_size_or_encoding_field'])"
files {'op_units_<lang>': 5, 'op_units_asg_<lang>': 5, 'trickle_store': 338}
rows 64398
rows with a byte size or encoding 0
```

Every distinct row shape measured, one line per (store kind,
language, build, field set, count):

```
$ python3 -c "import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json'));[print(s['store_kind'],s['language'],s['build'],s['dwarf_row_fields'],s['rows']) for s in d['dwarf_row_shapes_measured']]"
trickle_store cpp anchor ['location', 'name'] 33820
trickle_store c anchor ['location', 'name'] 19676
trickle_store swift anchor ['location', 'name'] 2581
trickle_store go anchor ['location', 'name'] 1875
op_units_<lang> cpp anchor ['location', 'name'] 1476
trickle_store rust anchor ['location', 'name'] 1441
op_units_<lang> c anchor ['location', 'name'] 1138
op_units_asg_<lang> cpp anchor ['location', 'name'] 648
op_units_asg_<lang> c anchor ['location', 'name'] 552
op_units_<lang> swift anchor ['location', 'name'] 303
op_units_<lang> go anchor ['location', 'name'] 301
op_units_<lang> rust anchor ['location', 'name'] 230
op_units_asg_<lang> go anchor ['location', 'name'] 177
op_units_asg_<lang> rust anchor ['location', 'name'] 122
op_units_asg_<lang> swift anchor ['location', 'name'] 58
```

Fifteen combinations, one shape. Every table sits at the ANCHOR build;
there is no ship-build table.

## 3.5 The canonical-form stores carry no type field either

`canon40_regen_store/` is the store the pool's members were built
from. The list printed is every field name on one of its unit records
containing `dwarf` or `type`.

```
$ python3 -c "import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/canon40_regen_store/op_units2_c_c0000.json'));u=d['units']['c/regen_1'];print([k for k in sorted(u) if 'dwarf' in k.lower() or 'type' in k.lower()])"
[]
```

## 3.6 The left side, LITERAL: a class and no width

One row of the language inventory, c's `_Float16`.

```
$ python3 -c "import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/type_inventory2_core2.json'));print(json.dumps(d['languages']['c']['scalar_core'][2]))"
{"language": "c", "id": "c/core_2", "spelling": "_Float16", "extracted_marking": "float", "normalised_class": "float"}
```

GLOSS: `float` is the class. Nothing in the row says 16 bits; the
spelling says it to a reader, and reading it off the spelling is what
the stop rule forbids.

# 4. Where it was looked for, by cause

Every place is a full host path. The causes, not the sightings: there
are three reasons a candidate file does not answer step 1, and each
reason is one row.

| cause | places | what they hold instead |
|---|---|---|
| the record shape carries no type facts | `~/Programming/PseudoCoupHQ/Research/op_pipeline/trickle_store/` (338 files), `.../op_units_<lang>.json` (5), `.../op_units_asg_<lang>.json` (5) | a `(name, location)` DWARF row per parameter — measured in §3.4 |
| the store is downstream of the type facts and never carried them | `.../canon36_regen_store/` … `.../canon40_regen_store/`, `.../layer4*_regen_store/`, `~/Programming/Airlock/agent/out/` (288 entries, 9.1 GB) | register facts: `arrival_contract_bindings`, `entry_contract`, `ledger`; in Airlock's product folder the only DWARF-typed artifacts are `result_types_<lang>.json`, which record the probe's RESULT type NAME |
| the type facts exist but for another population | `.../dwarf_typed_key.json`, `.../dwarf_typed_key_t27.json`, `.../proposal_representation_dimension2.json`, `.../proposal_representation_dimension3.json`, `.../prove_interp_computation.json`, `.../op_units_php.json`, `.../op_units_ruby.json` | interpreter handler parameters (cpython, ruby, php, java), not the five compiled languages' probes |
| the type facts exist but for the wrong side and the wrong build | `.../result_types_asg_c.json`, `.../result_types_asg_cpp.json` | the only compiled-language artifacts keyed on `DW_AT_encoding` + `DW_AT_byte_size`: c 276 and cpp 324 assignment probes, gcc-built, RESULT type only |
| the compile that could have recorded it did not | `.../type_inventory3.json`, `.../declare_raw/decl_<lang>.txt` | an ACCEPT/REFUSE verdict per candidate type and the compiler's refusal text; no width and no encoding was read from those compiles |
| the objects cannot be re-read | `podman volume ls` on the host | no trickle volume; the probe objects built in the trickle container's `/work` are gone |

# 5. What IS on disk: the spelling side, half of step 1

Labelled so it is never read as the deliverable. Per language, per
scalar-core spelling, how many ACCEPTED probes declared an operand
with that spelling. The rows themselves are in
`~/Programming/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json`
under `the_spelling_side_only`; each row's `dwarf_byte_size` and
`dwarf_encoding` read `NOT ON DISK -- see refusal`.

```
$ python3 -c "import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json'));S=d['the_spelling_side_only']['by_language'];[print(l,len(r),sum(1 for x in r if x['attested'])) for l,r in sorted(S.items())]"
c 56 25
cpp 56 28
go 14 14
rust 15 15
swift 17 17
```

| language | scalar core spellings | attested by at least one accepted probe | never attested |
|---|---|---|---|
| c | 56 | 25 | 31 |
| cpp | 56 | 28 | 28 |
| go | 14 | 14 | 0 |
| rust | 15 | 15 | 0 |
| swift | 17 | 17 | 0 |

c's and cpp's unattested spellings are the fixed-point family
(`_Accum`, `_Fract`, and their `_Sat` / `short` / `long` / `unsigned`
variants), plus `__fp16`, `__ibm128`, `half`, and — c only —
`char8_t`, `char16_t`, `char32_t`, `wchar_t`. Each is in the inventory
because an authority names it and a one-line declaration of it
compiled; no accepted probe used it as an operand.

## 5.1 One disagreement the missing encoding would have decided

The inventory's own class column disagrees with itself across
languages on truth values. Listed, not resolved — the brief's stop
rule says a disagreement between DWARF and the inventory's class is
recorded rather than settled, and here the DWARF side is absent
altogether.

| language | spelling | `normalised_class` in `type_inventory2_core2.json` |
|---|---|---|
| c | `bool` | `integer_unsigned` |
| cpp | `bool` | `integer_unsigned` |
| go | `bool` | `truth_value` |
| rust | `bool` | `truth_value` |
| swift | `Bool` | `truth_value` |

`DW_ATE_boolean` is exactly the attribute that settles this, and it is
the attribute that is missing.

# 6. Memory

Bound stated before the pass: `ABORT_MEMORY_T101` at 2 GB, checked
with `resource.getrusage(RUSAGE_SELF)` after every store file, one
store file held at a time and only counters kept across files.

```
$ python3 -c "import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json'));print(d['memory']['peak_rss_mb'], 'MB peak against a 2048 MB bound')"
24.9 MB peak against a 2048 MB bound
```

# 7. The guard

`~/Programming/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py`
is unmodified and was run from this instance over the one json this
task wrote, and the LAW's zero-count check was run over every file
this task added.

Lane log, host path:
`~/AirlockRuns/t101/agent/logs/20260906T055012Z__t101_l5_guard2.sh.log`.

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS types101_dwarf_flag.json -- no operator token in any key, grouping, pairing or row structure
```

The zero-count check, from the same lane, over `types101_join.py`,
`types101_dwarf_flag.json`, `types101_report.md` and the four lane
scripts: **0 on every file**. The word is assembled from two halves
inside the lane so the lane does not match itself; the first guard
lane spelled it and scored 2 against its own text, which is why lane 5
exists and lane 2 was withdrawn.

# 8. What would unblock the join

One compile pass, not a redesign. Recompile one probe per (language,
spelling) at the anchor flags already pinned in
`~/Programming/PseudoCoupHQ/Research/op_pipeline/type_inventory3.json`,
and read `DW_AT_byte_size` and `DW_AT_encoding` off the
`DW_TAG_formal_parameter`'s `DW_AT_type` chain. The reader already
exists in this folder:
`~/Programming/PseudoCoupHQ/Research/op_pipeline/dwarf_typed_key.py`
walks exactly that chain with pyelftools for the interpreter handlers.
That is a new compile run and a change to the capture path, so it is
the coordinator's to authorize.

# 9. Lanes and products

| lane | what it did | lane log, host path |
|---|---|---|
| `t101_l1_dwarf_shape.sh` | ran `types101_join.py`; step 1 refused by name | `~/AirlockRuns/t101/agent/logs/20260906T054643Z__t101_l1_dwarf_shape.sh.log` |
| `t101_l3_transcripts.sh` | ran the commands §3.1, §3.4, §3.5, §3.6 and §5 paste | `~/AirlockRuns/t101/agent/logs/20260906T054758Z__t101_l3_transcripts.sh.log` |
| `t101_l4_transcripts2.sh` | ran the two source quotations §3.2 and §3.3 | `~/AirlockRuns/t101/agent/logs/20260906T054822Z__t101_l4_transcripts2.sh.log` |
| `t101_l5_guard2.sh` | the spelling guard and the zero-count check | `~/AirlockRuns/t101/agent/logs/20260906T055012Z__t101_l5_guard2.sh.log` |
| `t101_l6_transcripts3.sh` | ran the §6 memory line and the §7 guard line in their full-path form | `~/AirlockRuns/t101/agent/logs/20260906T055212Z__t101_l6_transcripts3.sh.log` |
| `t101_l7_claims.sh` | the first `check_conventions_log_claims.py --verify` over this log: 9 of 10 matched, 0 differed, 1 NOT_RERUNNABLE with cause `output_annotated` | `~/AirlockRuns/t101/agent/logs/20260906T055250Z__t101_l7_claims.sh.log` |
| `t101_l8_transcripts4.sh` | re-quoted `fold.py` at lines 82–91, the arrow-free lines that carry the claim | `~/AirlockRuns/t101/agent/logs/20260906T055329Z__t101_l8_transcripts4.sh.log` |
| `t101_l9_claims2.sh` | the final verify over this log; its tally is §11 | `~/AirlockRuns/t101/agent/logs/20260906T055403Z__t101_l9_claims2.sh.log` |

Lane scripts:
`~/Programming/PseudoCoupHQ/Research/op_pipeline/lanes_t101/`.

Products written, all new, all under
`~/Programming/PseudoCoupHQ/Research/op_pipeline/`:

| file | what it is |
|---|---|
| `types101_join.py` | the join program; runs step 1 and refuses by name |
| `types101_dwarf_flag.json` | the refusal, the measured row shapes, the places looked, and the spelling side of step 1 |
| `types101_report.md` | the artifact-side account of the flag |

Not written, and why: `types101_holders.json`,
`types101_spellings.json`, `types101_entry_holders.json` — a holder
table with an invented width is not a holder table, and every width
would have had to be invented.

# 10. The two lists

## Decided, recorded for audit

- The DWARF parameter tables were found on disk and their record shape
  measured over all 348 store files and all 64,398 parameter rows. The
  shape is `(name, location)` in all fifteen (store kind × language ×
  build) combinations, with zero rows carrying a byte size or an
  encoding.
- `types101_join.py` refuses at step 1 by name rather than assigning a
  width from a spelling. No class and no width was assigned by hand
  anywhere in this task.
- The spelling side of step 1 was computed in the same pass and stored
  under a field name that says it is half of step 1.
- The instance `~/Programming/Airlock/instances/t101.conf` was created
  from `o3.conf` at cpus 2 / memory 4g with the abort
  `ABORT_MEMORY_T101` at 2 GB; measured peak 24.9 MB; the instance was
  brought down at the end of the task.
- The first guard lane matched its own text and was withdrawn in
  favour of `t101_l5_guard2.sh`; both facts are recorded in §7 rather
  than tidied away.

## Awaiting the owner

- Whether to authorize the one compile pass in §8 that captures
  `DW_AT_byte_size` and `DW_AT_encoding` per probe parameter. It is
  the only thing between here and the holder table, and it is a change
  to the capture path, so it is not this task's to take.

# 11. The verifier tally

`check_conventions_log_claims.py --verify --timeout 20` over this log,
run from the t101 instance by lane `t101_l9_claims2.sh`. Lane log, host
path: `~/AirlockRuns/t101/agent/logs/20260906T055403Z__t101_l9_claims2.sh.log`.

| outcome | count |
|---|---|
| MATCHES | 10 |
| DIFFERS | 0 |
| UNVERIFIABLE | 0 |
| REFUSED | 0 |
| NOT_RERUNNABLE | 0 |

ONE LINE, the verifier's own: `10 of 10 claims reproduce; 0 (0%) carry
nothing to re-run`.

The earlier run, lane `t101_l7_claims.sh`, scored 9 of 10 with one
NOT_RERUNNABLE under cause `output_annotated`; §3.2 records what that
was and what was narrowed. The verifier was not modified.
