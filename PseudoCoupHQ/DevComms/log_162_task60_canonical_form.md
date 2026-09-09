# log 162 — TASK 60: `canonical_form.py`, and the IN-i ordering fix over all 31,078

Date: 2026-09-03. Node `hq.research.compiler_graph.canonical_form`
(0_3_5_2) and its four realized sub-nodes `prelude`, `epilogue`,
`labels`, `refuse`. Round 12, log_158's task 60.

---

# 0. The lap in plain words, before any figure

Round 11 rendered every arch unit into the memory-wrapped form and
recorded the result as `canon38_*`. That render had one internal
disagreement, which log_153 §9 printed and deliberately did not fix:
the prelude loaded a unit's VECTOR arrivals first, while the ledger's
own wiring and the recorded bindings numbered `IN-i` by the ARRIVAL
CONTRACT's order. For a unit with both kinds of arrival the two orders
name different rows, so `IN-0` meant one thing to the prelude and
another to everything downstream.

The CORE settled it on 2026-09-03: the contract's order is the order,
and vector-first is a defect. This task did three things.

1. **Counted the damage before touching it.** The defect can only bite
   a unit whose contract names BOTH a vector and a general arrival.
   That is 5,818 of the 31,078 units.
2. **Wrote the node's own module.** `canonical_form.py`, class
   `CanonicalForm`, with the prelude emitting in contract order. It
   imports `ledger.py` (task 59) and `gate.py` (task 58) and imports
   nothing from `ledger47/48.py`, `gate48.py` or any `canon37/38_*`
   driver.
3. **Re-rendered and re-gated all three populations** into `canon39_*`,
   assembled the same 2,728-unit sample with the real assembler, and
   ran the unmodified spelling guard over every file written.

---

# 1. The verdict, with its population

## 1.1 The one-line state

Over the WHOLE corpus of 31,078 arch units (original 1,779 +
interpreter 11 + regenerated 29,288), canon39 wraps and proves
**30,432** and refuses **646**, against canon38's 30,436 / 642. The
only movement is 4 units, all with the same named cause.

## 1.2 Per population, canon39 against canon38

| population | of | canon38 proved | canon39 proved | canon38 refused | canon39 refused |
|---|---:|---:|---:|---:|---:|
| original (compiled corpus) | 1,779 | 1,763 | **1,763** | 16 | **16** |
| interpreter | 11 | 9 | **9** | 2 | **2** |
| regenerated | 29,288 | 28,664 | **28,660** | 624 | **628** |
| **all three** | **31,078** | **30,436** | **30,432** | **642** | **646** |

## 1.3 The proved 30,432 by which route carried them

Route: `gate.py`'s `Gate.prove_wrapped`, the wrapped text's `OUT-0`
against the value the unit's own SHIP body leaves in its own answer
home, for every value of every input row.

| population | PROVED_ON_SHIP | PROVED_BY_CONSTRUCTION |
|---|---:|---:|
| original | 1,068 | 695 |
| interpreter | 9 | 0 |
| regenerated | 21,353 | 7,307 |
| **all three** | **22,430** | **8,002** |

`PROVED_BY_CONSTRUCTION` is the structural route (C1–C6), reached ONLY
where the reference has no model for a mnemonic the body spells — never
as a cheaper first choice.

## 1.4 What this lap does NOT report, said rather than left blank

**No term-level figures are owed by this render.** log_158 asks for
them "if `Gate` yields them". `Gate.prove_wrapped` gates the WRAPPED
TEXT; the two term routes (`prove_term_against_ship`,
`prove_term_against_text`) need a transcribed term, and the term is
`term.py`, node 0_3_5_6, which is **task 61** and does not exist yet.
Task 58's term figures (25,179 proved / 0 withdrawn / 3,970 undecided /
1,287 no term, over 30,436) are terms transcribed off **canon38**;
re-transcribing them over canon39 is task 61's first act, and the 5,818
units whose rows were renumbered are exactly the ones whose terms will
move. Quoting task 58's figures here as if they were canon39's would be
a false claim, so they are not quoted.

---

# 2. The module, and what is in it

## 2.1 The class, against the CORE's `## design`

`PseudoCoupHQ/Research/op_pipeline/canonical_form.py`.

| the CORE says | the file has |
|---|---|
| attribute `block_order` | `CanonicalForm.block_order` — the eight blocks IN, CONST, TEMP, OWN, STACK, X87, GUARD, OUT |
| attribute `wrapped_text` | `CanonicalForm.wrapped_text`, and the same string on every returned record |
| method `wrap` | `CanonicalForm.wrap` — calls prelude, labels, epilogue; the body is never touched |
| method `assemble` | `CanonicalForm.assemble` + `render_for_assembler` / `write_batch` / `disassemble` / `relocations` |
| method `refuse` | `CanonicalForm.refuse`, delegating to the sub-node class |
| sub-node `prelude` | class `Prelude` — `emit`, `emit_general_row`, `emit_vector_row` |
| sub-node `epilogue` | class `Epilogue` — `emit`, `pick_pointer`, `place` |
| sub-node `labels` | class `Labels` — `rewrite`, `locate_targets`, `rewrite_external` |
| sub-node `refuse` | class `Refuse` — `causes`, `classify`, `record` |

## 2.2 What is DELEGATED rather than copied, said out loud

The epilogue and the label rewrite are unchanged by this task. Their
one text lives in `ledger.py` (`Ledger.build_epilogue`,
`positional_labels`), which itself carries a header saying it copied
them unchanged from the superseded record. Copying them a SECOND time
into `canonical_form.py` would put two texts of one rule on disk, and a
rule with two texts drifts. So `Epilogue` and `Labels` here are the
node's SHAPE — the CORE's named methods — and each method calls that
one text. The shape is this node's; the logic is the one logic.

The prelude is NOT delegated, because the prelude is the thing this
task changed and it is a sub-node of THIS node.

## 2.3 `Refuse`, and the fourth cause

`Refuse.causes` names six reasons a unit cannot be wrapped. Four of
them fire over this corpus (§6). A refusal is written onto the unit's
own record — `outcome: REFUSED`, `refusal_cause`, `refusal` — so a
refused unit travels with its population rather than being absent.

## 2.4 Where the arch-unit facts come from

Reading a unit's body, its arrival contract and its answer home is node
0_3_5_1 `arch_unit`, not this node, and that reading was done and
recorded in round 11. `canonical_form.py` therefore reads those facts
out of the canon38 **data files** — `canon38_wrapped_<lang>.json`,
`canon38_interp.json`, `canon38_regen_store/*.json` — and re-renders
every unit from them. A data file is a record; reading it is not
importing a superseded module. The fields read are exactly
`body_text`, `body_bytes`, `body_source`, `arrival_families`,
`entry_contract`, `result_family`, `result_width`, `lang`, `n`,
`population`, and `operator` (a display label, read by nothing).

Everything downstream of those facts — the prelude, the labels, the
dataflow walk, the epilogue, the ledger, the verdict — is recomputed.

---

# 3. THE COUNT THE CORE OWED: how many units the defect affects

A unit is affected exactly when its arrival contract names BOTH a
vector family and a general one; for any other unit the vector-first
order and the contract order are the same order.

LITERAL — `canonical_form.py --defect-census`, computed from canon38:

```
population totals      {"interpreter": 11, "original": 1779, "regenerated": 29288}
affected by the defect {"original": 474, "regenerated": 5344}
affected, per language:
  original     c         196
  original     cpp       264
  original     go         12
  original     rust        2
  regenerated  c        2220
  regenerated  cpp      3104
  regenerated  go         12
  regenerated  rust        2
  regenerated  swift       6
affected total 5818 of 31078
```

GLOSS: **5,818 of 31,078**. The interpreter population is untouched —
none of its 11 units has a vector arrival alongside a general one. The
remaining 25,260 units split into 1,244 with only vector arrivals and
24,016 with only general ones (or none), and for both of those the two
orders coincide.

The affected units were, in canon38, ALL PROVED — 474 of 474 in the
original population and 5,344 of 5,344 in the regenerated one. So the
defect never showed as a refusal or a disproof at layer 3; it showed as
`IN-i` meaning two different things to two different readers, which is
what log_153 §9 caught at layer 4.

---

# 4. `c/op_105`, before and after, literally

This is the instance log_153 §9 printed and the instance
`CORE_0_3_5_2_2_prelude.md` names.

LITERAL — `canonical_form.py --show-op-105`:

```
LITERAL -- c/op_105, body: cvtsi2ss %edi,%xmm1; addss %xmm1,%xmm0; ret
LITERAL -- arrival_families      ['rdi', 'xmm0', 'xmm1']

LITERAL -- canon38 prelude_resolved   ['movdqu IN-0,%xmm0', 'movdqu IN-1,%xmm1', 'mov IN-2,%rdi']
LITERAL -- canon38 prelude            ['mov ledger+0x00(%rip),%r11', 'movdqu 0x0(%r11),%xmm0', 'mov ledger+0x00(%rip),%r11', 'movdqu 0x10(%r11),%xmm1', 'mov ledger+0x00(%rip),%rdi', 'mov 0x20(%rdi),%rdi']
LITERAL -- canon38 bindings           [{"bound_to_the_same_symbol_as": "%rdi", "row": "IN-0", "size": 16}, {"bound_to_the_same_symbol_as": "%xmm0", "row": "IN-1", "size": 16}, {"bound_to_the_same_symbol_as": "%xmm1", "row": "IN-2", "size": 8}]

LITERAL -- canon39 prelude_resolved   ['mov IN-0,%rdi', 'movdqu IN-1,%xmm0', 'movdqu IN-2,%xmm1']
LITERAL -- canon39 prelude            ['mov ledger+0x00(%rip),%rdi', 'mov 0x0(%rdi),%rdi', 'mov ledger+0x00(%rip),%r11', 'movdqu 0x10(%r11),%xmm0', 'mov ledger+0x00(%rip),%r11', 'movdqu 0x20(%r11),%xmm1']
LITERAL -- canon39 bindings           [{"bound_to_the_same_symbol_as": "%rdi", "row": "IN-0", "size": 8}, {"bound_to_the_same_symbol_as": "%xmm0", "row": "IN-1", "size": 16}, {"bound_to_the_same_symbol_as": "%xmm1", "row": "IN-2", "size": 16}]

LITERAL -- canon39 wrapped_text_resolved  mov IN-0,%rdi; movdqu IN-1,%xmm0; movdqu IN-2,%xmm1; cvtsi2ss %edi,%xmm1; addss %xmm1,%xmm0; movq %xmm0,OUT-0; ret
```

GLOSS, three things changed and one thing did not.

1. **The order.** canon38 loaded `%xmm0` first and `%rdi` last;
   canon39 loads `%rdi` first, because `%rdi` is what the arrival
   contract names at position 0.
2. **The row numbering follows.** `IN-0` is now `%rdi`'s row, which is
   what `walk_dataflow` and the bindings ALREADY believed. The prelude
   and the wiring now say the same thing, so the disagreement log_153
   §9 recorded is gone rather than merely documented.
3. **The row SIZES are now right.** canon38's binding record said
   `IN-0` is `%rdi` at size 16 — it took the family from the contract
   and the size from the vector row the prelude had put at that
   position. canon39 says `IN-0` is `%rdi` at size 8 and `IN-1` /
   `IN-2` are 16, which is what the values actually are. This is the
   same disagreement seen from the other end.
4. **The body did not change.** `cvtsi2ss %edi,%xmm1; addss
   %xmm1,%xmm0; ret` is character-for-character what it was, in its
   own order. Ruling 1 holds.

---

# 5. Why the reorder is safe, and the measurement that shows it

## 5.1 The argument

A vector row cannot be loaded through its own destination — a 16-byte
row does not fit a general pointer register — so a vector load needs
one general scratch. That scratch is picked ONCE, before any line is
emitted, against the set of GENERAL ARRIVAL FAMILIES plus the
never-rename set. So it is never a register that any load in this
prelude fills with an arrival value, whichever order the loads run in.
A general load uses its own destination as its own pointer and touches
nothing else. Therefore no load in the prelude can destroy another
load's result, and the order is free.

This is structural check C2, and `gate.py` runs it per unit.

## 5.2 The measurement, over the proved population

Computed over the 30,432 units canon39 proves, comparing each unit's
`wrapped_text` against the same unit's canon38 `wrapped_text`:

| | units |
|---|---:|
| wrapped text CHANGED | **5,818** |
| wrapped text unchanged | 24,614 |
| sum | 30,432 |

GLOSS: the 5,818 changed texts are exactly the 5,818 units §3 counted
as affected. Not one unaffected unit's text moved, and not one affected
unit's text stayed put. That is the strongest available statement that
the change is the change that was intended and nothing else: the fix
reaches every unit the defect reached, and no other unit at all.

And every one of the 5,818 is still proved (§6 table: the affected
count by canon39 outcome is 474 original + 5,344 regenerated, all
`WRAPPED_TEXT_PROVED`).

---

# 6. Zero regressions, in the ruled sense

`Gate.zero_regression` joins the two rounds on the unit name, and the
cause of every lost proof is COMPUTED over that unit's own canon39
record, not asserted.

LITERAL — `canonical_form.py --zero-regression`:

```
population before 31078  after 31078
states before {"proved": 30436, "refused": 642}
states after  {"proved": 30432, "refused": 646}
refusal causes before {"never returns": 424, "no answer home": 216, "no canonical text": 2}
refusal causes after  {"never returns": 424, "no answer home": 216, "no canonical text": 2, "no runtime callee body": 4}
kept 30432  lost 4  gained 0  moved 0  missing 0
regressions without a named cause = 0
  4 unit(s): REFUSED, cause 'no runtime callee body': no archive for toolchain 'swiftc' on this machine, so the callee's body cannot come from the compiler that built the caller
    sightings: swift/regen_315, swift/regen_321, swift/regen_327
```

GLOSS.

- **kept 30,432; lost 4; gained 0; missing 0.** Every unit canon38
  proved except four is proved again, and no unit went missing from the
  new run.
- **regressions without a named cause = 0.** That is the ruled sense of
  zero regressions.
- **The three recorded refusal causes are unchanged in count** — never
  returns 424 (16 original + 408 regenerated), no answer home 216, no
  canonical text 2. `CORE_0_3_5_2_7_refuse.md`'s settled rule "the
  refusals must be the same refusals across a rebuild" holds for all
  three.

## 6.1 The four losses, named

The fourth cause is not a defect of this render. log_158 requires it:
"the 4 swift callers without an attached callee are refused by name
with log_161's reason." Those four units are
`swift/regen_315`, `swift/regen_321`, `swift/regen_327`,
`swift/regen_333`; each one's answer arrives through a call into its
own compiler's runtime (`__divti3`, `__udivti3`, `__modti3`,
`__umodti3` respectively), and log_161 §4.1.1 established that swift's
runtime archive is on NEITHER side of the container wall on this
machine, so the callee's body cannot be read. canon38 counted them as
proved by the structural route while their answer was in fact unknown;
canon39 refuses them by name instead. That is a loss of four proofs and
a gain of four honest refusals.

## 6.2 The 304 that DID attach

The other side of the same ruling. Over canon39, 304 units carry an
answer row produced by `{"kind": "runtime_callee", "callee": ...}` —
c 136, cpp 164, rust 4 — which is exactly log_161's attachment count.
Across all canon39 rows the producer kinds are:

| producer kind | rows |
|---|---:|
| `arch_opcode` | 130,364 |
| `non_opcode_phrase` | 81,816 |
| `flag_pair` | 33,657 |
| `runtime_callee` | 608 |

Every producer is a typed object, never a bare string. No record
carries a `role` key, and no field is whitelisted anywhere in
`canonical_form.py`.

---

# 7. Assemble: the same 2,728-unit sample, real assembler

Sample rule, unchanged from canon38 so the two are comparable: every
proved unit of the original and interpreter populations, plus a fixed
stride of 30 over the proved regenerated population, the stride
recorded on the artifact.

LITERAL — `canonical_form.py --assemble`:

```
offered 2728  assembled 2728  failed 0  ledger relocations 8948
```

| | canon38 | canon39 |
|---|---:|---:|
| offered | 2,728 | **2,728** |
| assembled | 2,728 | **2,728** |
| failed | 0 | **0** |
| `R_X86_64_PC32` ledger relocations | 8,946 | **8,948** |

GLOSS on the relocation count: it is 2 higher because the sample is not
byte-identical in membership. The regenerated stride is taken over the
PROVED list, and canon39's proved regenerated list is 4 units shorter
than canon38's (§6.1), so the stride lands on a slightly different set
of units past those four, and those units spell a slightly different
number of ledger references. The offered and assembled counts are
unchanged because the whole-population part of the sample grew by
nothing and the stride still yields 956 regenerated units.

LITERAL — the head of `canon39_assemble_transcripts.txt`, which is
`objdump -d` on the object file `as --64` produced:

```
==== c/op_0   (from /tmp/canon39_assemble_work/batch_0000.s)
0000000000000000 <u_c_op_0>:
   0:	48 8b 3d 00 00 00 00 	mov    0x0(%rip),%rdi        # 7 <u_c_op_0+0x7>
   7:	48 8b 3f             	mov    (%rdi),%rdi
   a:	31 c0                	xor    %eax,%eax
   c:	85 ff                	test   %edi,%edi
   e:	0f 94 c0             	sete   %al
  11:	4c 8b 1d 00 00 00 00 	mov    0x0(%rip),%r11        # 18 <u_c_op_0+0x18>
  18:	41 88 03             	mov    %al,(%r11)
  1b:	c3                   	ret
```

GLOSS: lines 0 and 7 are the prelude's two-step load (ledger entry into
`%rdi`, then the row through `%rdi`); lines a–e are `c/op_0`'s own body
untouched; lines 11 and 18 are the epilogue's two-step store into
`OUT-0`; then the body's own `ret`. The two `0x0(%rip)` operands are
the R_X86_64_PC32 relocations against the ledger symbol — the symbol
appears in the object file only as a relocation, never as an absolute.

---

# 8. The guard: unmodified, ONE process, over every canon39 file

`guard60.py` runs `check_no_spelling_keys.py` as a SEPARATE process
with its own interpreter. It adds nothing to any field set, declares no
exemption, and edits no guard file.

WHAT WAS WALKED: all 335 JSON artifacts task 60 writes — the five
`canon39_wrapped_<lang>.json`, `canon39_interp.json`, all 326 shards of
`canon39_regen_store/`, `canon39_regen_state.json`,
`canon39_assemble.json`, `canon39_zero_regression.json`. None skipped.

LITERAL — the run:

```
$ /tmp/reconnect_venv/bin/python3 guard60.py
TASK 60: 335 paths  PASS 335  FAIL 0  exempt 0  exit 0
EXIT=0
```

LITERAL — the head and tail of `guard60_transcript.txt`:

```
guard60.py -- every artifact task 60 writes, unmodified guard, ONE process.  Nothing was added to any field set, and no artifact was declared out of the walk.
$ python3 check_no_spelling_keys.py <335 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
PASS canon39_wrapped_c.json -- no operator token in any key, grouping, pairing or row structure
PASS canon39_wrapped_cpp.json -- no operator token in any key, grouping, pairing or row structure
...
PASS op_units2_swift_c0010.json -- no operator token in any key, grouping, pairing or row structure

GUARD EXIT CODE = 0
```

LITERAL — the exemption count and the untouched-guard check:

```
$ grep -c exempt guard60_transcript.txt
0

$ git status --porcelain check_no_spelling_keys.py ledger.py gate.py reference.py
(no output — none of the four is modified)
```

GLOSS: `grep -c exempt` = 0, guard exit code 0, and the guard file
itself plus the three modules this task consumes are unmodified in the
working tree. The operator token travels once per unit as a display
label on the member and is read by nothing; the selection of what to
render is the corpus files on disk.

---

# 9. Decided and recorded for audit / awaiting the owner

## 9.1 Decided, recorded for audit

1. **`Epilogue` and `Labels` delegate to `ledger.py` rather than
   copying it.** Reason in §2.2: one rule, one text. If the tree wants
   those texts physically inside `canonical_form.py`, that is a
   one-line change of policy and a move, not a redesign.
2. **The arch-unit facts are read from canon38's DATA files.** Reason
   in §2.4: reading the corpus is node 0_3_5_1's job and was already
   done; a data file is a record, not a module. No `canon*` code is
   imported by `canonical_form.py`.
3. **The stride-30 sample is taken over each round's own proved list**,
   so canon39's sample differs from canon38's by the four units of
   §6.1. Keeping canon38's exact membership would have meant sampling a
   list this round does not hold.

## 9.2 Awaiting the owner

Nothing. No question is open that a CORE or AgentMemory does not
already answer.

---

# 10. The complete file inventory

## 10.1 Code written this task (two files, both new; nothing reused was edited)

| file | what it is |
|---|---|
| `PseudoCoupHQ/Research/op_pipeline/canonical_form.py` | the node's module: `CanonicalForm`, `Prelude`, `Epilogue`, `Labels`, `Refuse`, and the drivers for the three populations, the assembler, the defect census, the `c/op_105` print and the zero-regression comparison |
| `PseudoCoupHQ/Research/op_pipeline/guard60.py` | the unmodified guard over every canon39 artifact, one process |

## 10.2 Data written this task

| file | what it holds |
|---|---|
| `canon39_wrapped_c.json` | 610 original c units |
| `canon39_wrapped_cpp.json` | 770 original cpp units |
| `canon39_wrapped_go.json` | 107 original go units |
| `canon39_wrapped_rust.json` | 125 original rust units |
| `canon39_wrapped_swift.json` | 167 original swift units |
| `canon39_interp.json` | 11 interpreter units |
| `canon39_regen_store/` | 326 shards, 29,288 regenerated units |
| `canon39_regen_state.json` | the resume record: shards done, running tally |
| `canon39_assemble.json` | 2,728 offered / 2,728 assembled / 8,948 ledger relocations |
| `canon39_zero_regression.json` | the before-and-after against canon38, with the cause of every loss |
| `guard60.json` | the guard's own summary |

## 10.3 Transcripts and logs written this task

| file | what it holds |
|---|---|
| `canon39_wrapped_run.log` | the original population's run |
| `canon39_interp_run.log` | the interpreter population's run |
| `canon39_regen_run.log` | the regenerated population's 326 shards |
| `canon39_assemble_run.log` | the assembler's run |
| `canon39_assemble_transcripts.txt` | verbatim `objdump -d` blocks |
| `guard60_transcript.txt` | the guard's verbatim output, 335 paths |

## 10.4 PROGRESS and CORE files touched (five nodes)

All under
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_2_canonical_form/`.

| file | what changed |
|---|---|
| `PROGRESS.md` | four entries: the module, the render + zero regression, the assemble, the guard |
| `CORE_0_3_5_2_canonical_form.md` | the realization's "next lap" paragraph replaced by the 2026-09-03 lap's table |
| `node_0_3_5_2_2_prelude/PROGRESS.md` | three entries: the owed count (5,818), the contract-order emit, the reorder verified harmless |
| `node_0_3_5_2_2_prelude/CORE_0_3_5_2_2_prelude.md` | realization row for the emit order: planned → done |
| `node_0_3_5_2_3_epilogue/PROGRESS.md` | two entries: the class, the re-run |
| `node_0_3_5_2_3_epilogue/CORE_0_3_5_2_3_epilogue.md` | realization row added for `canonical_form.Epilogue` |
| `node_0_3_5_2_4_labels/PROGRESS.md` | two entries: the class, the re-run and assemble |
| `node_0_3_5_2_4_labels/CORE_0_3_5_2_4_labels.md` | realization row added for `canonical_form.Labels` |
| `node_0_3_5_2_7_refuse/PROGRESS.md` | two entries: the class, the fourth cause |
| `node_0_3_5_2_7_refuse/CORE_0_3_5_2_7_refuse.md` | realization rows for `canonical_form.Refuse` and the fourth cause |

## 10.5 Read, never written

`ledger.py`, `gate.py`, `reference.py`, `check_no_spelling_keys.py`
(all four confirmed unmodified in §8); `canon38_wrapped_<lang>.json`,
`canon38_interp.json`, `canon38_regen_store/*.json`,
`runtime_callee_units.json`, `runtime_callee_attachments.json` — data
records; the five CORE files of this node's sub-tree; log_146, log_152,
log_153, log_158, log_159, log_160, log_161.

---

# 11. Resume state

**There is none owed. All three populations finished in-session.**

The mechanics exist and were exercised, so a future lap can resume:

- `canonical_form.py --population original` skips units already in
  `canon39_wrapped_<lang>.json` and checkpoints every 200 units;
  `--fresh` starts over.
- `canonical_form.py --population regenerated` records finished shards
  in `canon39_regen_state.json` (`shards_done`, running `tally`) and
  writes it after every shard; a re-run resumes at the first shard not
  listed. It currently reads `shards_done` = all 326.
- `canonical_form.py --population interpreter` is one pass over 11
  units.

Commands, in the order they were run:

```
/tmp/reconnect_venv/bin/python3 canonical_form.py --defect-census
/tmp/reconnect_venv/bin/python3 canonical_form.py --show-op-105
/tmp/reconnect_venv/bin/python3 canonical_form.py --population original
/tmp/reconnect_venv/bin/python3 canonical_form.py --population interpreter
/tmp/reconnect_venv/bin/python3 canonical_form.py --population regenerated
/tmp/reconnect_venv/bin/python3 canonical_form.py --zero-regression
/tmp/reconnect_venv/bin/python3 canonical_form.py --assemble
/tmp/reconnect_venv/bin/python3 guard60.py
```

## 11.1 What task 61 inherits

`canon39_*` is the layer-3 record: 30,432 proved wrapped texts and 646
named refusals over 31,078. The 5,818 units whose IN rows were
renumbered are named by the field
`prelude_order_was_affected_by_the_vector_first_defect` on every canon39
record, so `term.py` can re-transcribe them and report the term-level
movement against task 58's canon38 figures without re-deriving the set.
