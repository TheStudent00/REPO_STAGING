# log_171 — TASK 67: bank round 13

Population for every count below is stated beside the count.
Levels (plan / code, layer / module) are marked where they cross.

---

## 1. The walk, in plain words, before any figure

Round 13 wrote no new module of its own; it extended round 12's six
(`reference.py`'s branch-fork/merge and callee-entry, `gate.py`'s
re-gate over canon39, `term.py`'s `render_back`) and rebuilt the
pool/census layer on top (`term65`, `the_pool5.json`,
`name_census6.json`). This task does not add code. It re-verifies
what the four task logs (167-170) claim, against disk, in one
process, and banks the round: confirm the guard, confirm the plan
tree, state the one-page picture, and hand the daemon its commit
message.

---

## 2. Verification transcripts

### 2.1 The spelling guard, re-run unmodified, by this session

```
$ cd ~/Programming/PseudoCoupHQ/Research/op_pipeline
$ md5sum check_no_spelling_keys.py
1d6aba67cbcdb021c3bdfd7f40fd2020  check_no_spelling_keys.py
$ grep -c exempt check_no_spelling_keys.py
11
```

Same md5 as log_164 §2.1 recorded for round 12 — the guard file
itself has not changed across rounds 12 and 13.

```
$ grep -c exempt reference.py gate.py ledger.py canonical_form.py term.py pool.py
reference.py:0
gate.py:0
ledger.py:0
canonical_form.py:0
term.py:0
pool.py:0
```

No module declares an exemption.

### 2.2 Every enumerated round-13 grouping artifact, PASS, this session's own run

Enumerated from logs 167-170's own file inventories, filtered to
files that group or pair units:

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py \
    name_census6.json the_pool5.json the_families5.json \
    exception_families5.json pool4_pool5_delta.json the_pool5_bytes.json \
    canon39_callee_units.json canon39_callee_attachments.json \
    canon39_callee_swift_lane.json canon39_zero_regression.json \
    canon39_assemble.json render_back_E00029.json

operator inventory: 91 tokens read from probe_manifest_*.json
PASS name_census6.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool5.json -- no operator token in any key, grouping, pairing or row structure
PASS the_families5.json -- no operator token in any key, grouping, pairing or row structure
PASS exception_families5.json -- no operator token in any key, grouping, pairing or row structure
PASS pool4_pool5_delta.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool5_bytes.json -- no operator token in any key, grouping, pairing or row structure
PASS canon39_callee_units.json -- no operator token in any key, grouping, pairing or row structure
PASS canon39_callee_attachments.json -- no operator token in any key, grouping, pairing or row structure
PASS canon39_callee_swift_lane.json -- no operator token in any key, grouping, pairing or row structure
PASS canon39_zero_regression.json -- no operator token in any key, grouping, pairing or row structure
PASS canon39_assemble.json -- no operator token in any key, grouping, pairing or row structure
PASS render_back_E00029.json -- no operator token in any key, grouping, pairing or row structure
$ echo EXIT:$?
EXIT:0
```

12 of 12 PASS, exit 0. This session's own run, not a copy of a
prior transcript.

### 2.3 A chunk store, spot-checked by a computed sample

Population: `term65_store/*.json` (332 files, one per shard the
round-13 term run wrote — same shard count as round 12's
`term61_store`, confirmed §2.6 below unchanged). A computed random
sample (seed 63, `random.sample`, no hand-picking) of 20 of 332
(6.0%):

```
$ python3 -c "
import random, os
random.seed(63)
files = sorted(os.listdir('term65_store'))
sample = random.sample(files, 20)
print('\n'.join('term65_store/'+f for f in sample))
"
term65_store/canon39_regen_store__op_units2_cpp_c0096.json
term65_store/canon39_regen_store__op_units2_cpp_c0019.json
term65_store/canon39_regen_store__op_units2_c_c0128.json
... (20 named)

$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py <the 20 files>
operator inventory: 91 tokens read from probe_manifest_*.json
PASS term65_store/canon39_regen_store__op_units2_cpp_c0096.json -- ...
... (all 20 printed PASS individually)
$ echo EXIT:$?
EXIT:0
```

20/20 sampled files PASS.

### 2.4 No carve-out claimed, this session's own grep

```
$ grep -c exempt reference.py gate.py ledger.py canonical_form.py term.py pool.py
(all 0 — same command/output as §2.1, cited once)
```

### 2.5 The authoritative count line, over pool5's own population

**Population: 1,831 entries over 30,432 member units.**

```
$ python3 -c "
import json
p=json.load(open('the_pool5.json'))
print(p['summary'])
"
{
  "distinct_layer3_wrapped_texts": 2993,
  "distinct_layer5_texts_among_eligible_units": 1267,
  "entries": 1831,
  "entries_carrying_more_than_one_wrapped_text": 527,
  "entries_spanning_compiled_and_interpreted": 3,
  "entries_spanning_more_than_one_language": 490,
  "entries_under_the_brief_strict_rule": 5095,
  "layer3_identity_merges": 27439,
  "layer5_identity_merges": 25327,
  "members": 30432,
  "members_not_layer5_eligible": 3838,
  "members_whose_term_was_undecided": 285,
  "members_whose_term_was_withdrawn": 3134,
  "members_with_a_proved_term": 26594,
  "members_with_no_term": 419,
  "proved_edges_applied": 118
}
```

Matches the brief's own figures exactly: 1,831 / 30,432; term
figures 26,594 proved / 3,134 withdrawn / 285 undecided / 419 no
term (26,594 + 3,134 + 285 + 419 = 30,432 ✓); brief-strict 5,095
(key `summary.entries_under_the_brief_strict_rule` inside
`the_pool5.json`, same path convention as pool4's log_164 §2.5);
490 multi-language, 3 compiled+interpreted.

Sub-population split (source: log_162/164's own table, quoted
because pool5's 30,432 members are the same canon39
WRAPPED_TEXT_PROVED population as pool4's — round 13 did not
re-run canon39 assembly):

| sub-population | attempted | canon39-proved (= pool5 member source) |
|---|---|---|
| original (compiled corpus) | 1,779 | **1,763** |
| interpreter | 11 | **9** |
| regenerated | 29,288 | **28,660** |
| TOTAL | 31,078 | **30,432** |

**The 13 round-5/6 withdrawn units — a separate population, listed
apart from the 30,432 above**, unchanged from log_164 §2.5: 18 units
the round-6 branching audit rechecked out of the 1,561-unit round-5
baseline, of which 5 still proved and 13 did not re-prove
(`audit_branching_withdrawn: 13`, log_112). This is a DIFFERENT
population from canon39/pool5 (round 5/6 predates canon38/canon39)
and is named here separately per the brief, not folded into the
30,432 line.

### 2.6 Prior artifacts verified untouched

```
$ git status --porcelain -- the_pool4.json name_census5.json canon39_regen_state.json term61_run.py
(nothing)
$ md5sum the_pool4.json name_census5.json canon39_regen_state.json term61_run.py
16797058af13a3b5fed3c93d3491b0c8  the_pool4.json
6fe86e5739715bd5d96c152681190167  name_census5.json
3d32fff4b24e682c1f98c1a4089cfb5f  canon39_regen_state.json
65a2fe665fcfaec526d32033c9ed873d  term61_run.py
$ ls term61_store | wc -l
332
```

`git status --porcelain` on all four returned nothing. The round-12
census (`name_census5.json`), pool (`the_pool4.json`), canon39 state
and term61 store are superseded by round 13's outputs, not edited.

### 2.7 The module-name rule

```
$ grep -n "^class" reference.py gate.py ledger.py canonical_form.py term.py pool.py
gate.py:106:class Verdict(object):
gate.py:185:class Gate(object):
reference.py:227:class MachineState(object):
reference.py:432:class Operands(object):
reference.py:2320:class Reference(object):
pool.py:109:class UnionFind(object):
pool.py:426:class Pool(object):
ledger.py:340:class Producer(object):
ledger.py:1054:class Ledger(object):
term.py:331:class Term(object):
term.py:1246:class RenderBack(object):
canonical_form.py:452:class CanonicalForm(object):
(plus smaller classes each file also defines, e.g. NotWalkable,
Block, Body, Entry, OpcodeTable, Refusal, Row, NoTerm,
RelinkDisagreement, Transcription, NoTemplate, Rendering, Prelude,
Epilogue, Labels, Refuse)
```

Each of the six module files carries a class matching its CORE
name. `term.py` additionally carries `RenderBack`, the class task 66
added (`node_0_3_5_6_5_render_back`).

---

## 3. The plan tree

### 3.1 `check_plans.py`, this session's own run

```
$ python3 ~/Programming/PlanPlan/framework/check_plans.py ~/Programming/PseudoCoupHQ/Planning
[ERROR] dangling-path: ~/Programming/PseudoCoupHQ/DevComms/log_107_task21_interp_ does not exist
    - .../node_0_3_5_compiler_graph/PROGRESS.md:1553
[ERROR] dangling-path: ~/Programming/PseudoCoupHQ/DevComms/log_110_task25_ does not exist
    - .../node_0_3_5_compiler_graph/PROGRESS.md:1695
[ERROR] dangling-path: ~/Programming/SandboxDesign/allow.sh does not exist
    - .../node_0_3_1_dominant_intentions/PROGRESS.md:73
    - .../node_0_3_4_data_representation/PROGRESS.md:75
[ERROR] dangling-path: ~/Programming/Sources/llvm- does not exist
    - .../node_0_3_5_compiler_graph/PROGRESS.md:79
[WARN] nodes-register: 14 CORE(s) with no readable register
[WARN] projection: `## sub_nodes` not the first section on 53 CORE(s)
[WARN] edge-register: `super_node`/`sub_nodes` missing on 14 of 67 nodes
[INFO] completeness: 0 of 67 complete (54 leaves)
summary: 4 error(s), 3 warning(s)
```

Same four dangling-path lines, same line numbers, as log_164 §3.1
reported for round 12 — nothing new. **All 4 pre-date this round**,
checked by `git blame` on the exact line, this session:

```
$ git blame -L 1553,1553 .../node_0_3_5_compiler_graph/PROGRESS.md
9842d19f (TheStudent00 2026-09-01 10:30:40 -0400 1553) `.../log_107_task21_interp_
$ git blame -L 1695,1695 .../node_0_3_5_compiler_graph/PROGRESS.md
78581903 (TheStudent00 2026-09-01 11:18:40 -0400 1695) Full record: `.../log_110_task25_
$ git blame -L 79,79 .../node_0_3_5_compiler_graph/PROGRESS.md
92b50c2b (TheStudent00 2026-08-31 17:16:50 -0400 79)   c/op_501). Source was on disk (~/Programming/Sources/llvm-
$ git blame -L 73,73 .../node_0_3_1_dominant_intentions/PROGRESS.md
ab2326b2 (TheStudent00 2026-08-14 14:00:05 -0400 73)   awaiting the owner's `bash ~/Programming/SandboxDesign/allow.sh sync`
```

| dangling path | blamed date |
|---|---|
| `log_107_task21_interp_` | 2026-09-01 |
| `log_110_task25_` | 2026-09-01 |
| `~/Programming/Sources/llvm-` | 2026-08-31 |
| `~/Programming/SandboxDesign/allow.sh` | 2026-08-14 |

Round 13's briefs (log_166) are dated 2026-09-03; all four lines
were written before that — pre-existing defects, not round-13
regressions. The 14-CORE register gap and 53-CORE projection-order
warning are the same pre-existing, ruled-non-sweep gap AgentMemory
already records (chain by chain, not by a sweep).

### 3.2 Dashboards regenerated

```
$ bash ~/Programming/PseudoCoupHQ/hq.sh dashboard
=== rebuilding node projections ===
projection rebuilt: .../node_0_3_5_6_term/CORE_0_3_5_6_term.md (`## sub_nodes`)
=== regenerating dashboards ===
wrote 114 dashboard(s)
```

### 3.3 Every round-13 node's PROGRESS.md, off `planned`

```
$ head -3 node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/PROGRESS.md
status: living
$ head -3 node_0_3_5_4_reference/PROGRESS.md
status: living
$ head -3 node_0_3_5_6_term/PROGRESS.md
status: living
$ head -3 node_0_3_5_6_term/node_0_3_5_6_5_render_back/PROGRESS.md
status: living
$ head -3 node_0_3_5_7_pool/PROGRESS.md
status: living
$ head -3 node_0_3_5_8_guard/PROGRESS.md
status: living

$ grep -rln "^status: planned" node_0_3_5_1_arch_unit node_0_3_5_4_reference \
    node_0_3_5_6_term node_0_3_5_7_pool --include=PROGRESS.md
(no output — exit 1, meaning no match)
```

`node_0_3_5_6_5_render_back`, `planned` at round-12 handoff (log_164
§4.5 named it as owed work), is now `living` — task 66 moved it.

---

## 4. The one-page state of the line

### 4.1 The seven-layer chain, mapped to modules

| stage | what it holds | module |
|---|---|---|
| 1. probe | compiled machine code, one per operator × operand types | `probes` (untouched this round) |
| 2. arch unit | bytes, arrival/exit registers, runtime-callee bytes | `arch_unit` (this round: callee attachment generalized to every builtins-archive name, task 63) |
| 3 (layer 3). canonical form | the body between a standardized prelude/epilogue, byte-comparable | `canonical_form.py` (unchanged this round) |
| — ledger | one row per value, its producer opcode, what it read | `ledger.py` (unchanged this round) |
| — reference | the symbolic simulator proofs run against | `reference.py` (this round: forks/merges at `j<cc>`, steps into attached callees, task 64) |
| — gate | the proof obligations, discharged over the reference | `gate.py` (this round: re-gate over all 30,432 canon39 units, task 64) |
| 4 (layer 4). term | the unit's computation as a z3 expression | `term.py:Term.transcribe` (rebuilt as `term65`, task 65) |
| 5 (layer 5). normalized text | that expression printed by one fixed rule | `term.py:Term.normalize` (rebuilt as `term65`, task 65) |
| — render_back | layer 4/5 term → arch text, gate-proved against ship code | `term.py:RenderBack` (NEW this round, task 66) |
| — pool | the one pool where proved-equivalent units collapse | `pool.py` (rebuilt as `pool5`, task 65) |

### 4.2 The pool

1,831 entries over 30,432 members (§2.5). 490 span more than one
language. 3 span compiled and interpreted code. 34 families (log_169
counts this as unchanged from pool4's 34 — no cause computed this
task beyond confirming the number on disk, §2.5 above).

### 4.3 The census

`name_census6.json`/`name_census6_printed.txt` replaces census5 as
this round's producer census. This task confirms the file passes the
guard (§2.2) and exists; the delta against census5 is log_169's own
record (49/1,637 cited in the brief), not recomputed here.

### 4.4 This round's corrections

1. **log_168's `prove_term_against_text` fix.** Task 64 found and
   removed 230 false proofs the reference's flag-triple defect had
   produced; consistency reads 0 after the fix, over 25,937
   straight-line units, with 0 changed answers on that population.
2. **The layer-5 order-dependence finding, CORE-corrected.** Task 65
   found 1,479 of 26,594 texts are not a function of the unit alone
   — they vary with `z3.simplify`'s internal argument order. Recorded
   as a CORE correction (log_169), not smoothed over; the fix itself
   is PLANNED for round 14, per §4.5 below.
3. **Code-before-CORE deviations, recorded in 168/169.** Both task
   64 and task 65 record places their code changed before the
   settled rule was written, per the pattern log_164 §4.4 item 2
   established for round 12 — deviations are named, not hidden, with
   the rule written afterward carrying its own provenance note.
4. **The destination-rule-4 finding, CORE-corrected but not yet
   fixed.** Task 64 found destination rule 4 answers wrong for float
   lowerings that return in `%xmm0` (2,862 units); 0 changed answers
   were found over the 25,937-unit straight-line population that
   rule 4 does not touch, so nothing already proved was disturbed.
   The fix is PLANNED for round 14 (§4.5).

### 4.5 Owed work, named as next round's planned items (no open calls for the owner — log_166 records none)

1. **Destination rule 4 for float lowerings answering in `%xmm0`**
   (2,862 units) — found wrong by task 64, fix not yet made.
2. **The archive's runtime set + canon rebuild** implied by the
   destination-rule-4 fix, over the same 2,862-unit population.
3. **Layer-5 order-dependence** (1,479 of 26,594 texts) — the
   `z3.simplify` argument-order finding from task 65; fix PLANNED.
4. **`render_back`'s `if` template** — task 66 closed E00029 (158/158
   proved, rendered) and the whole proved-term population (5,909
   rendered / 5,873 proved / 20,131 refused by 17 causes), with `if`
   the single largest refusal cause at 13,027 units; only 105
   rendered so far against 1,905 layer-3 texts on that cause.
5. **The go/rust panic-path callees** (196 units) — task 63 found
   these call-bearing units not attached to any builtins archive;
   go/rust panic paths are not covered by the current archive index.
6. **The `emit` module** (probes sub-node) — not touched this round,
   same standing item log_164 §4.5 named for round 12.
7. **The swift re-run** — task 63 ran the swift extraction as a lane
   on `trickle`; whether that closes the standing swift gap named in
   log_164 §4.5 is not re-verified by this banking task (outside its
   file set); named here so it is not silently dropped.
8. **Restarting `sandbox-runner` onto the rebuilt image** — standing
   infrastructure work, named again unchanged from log_164 §4.5;
   not touched by tasks 63-66 or by this banking task.

---

## 5. Posterity message

```
$ wc -c ~/Programming/PseudoCoupHQ/DevComms/next_commit_message.txt
1007 next_commit_message.txt
$ head -5 ~/Programming/PseudoCoupHQ/DevComms/next_commit_message.txt
round 13 banked: runtime-callee attachment generalized to every
builtins-archive name (task 63), the reference now forks/merges
branches and steps into callees with re-gate over all 30,432
canon39 units (task 64), term/pool/census rebuilt as term65/pool5/
census6 (task 65), Term.render_back closes the layer-5 rendering
```

The daemon consumes this file by design: `git_commit_push.sh`'s own
comment states the priority order — "explicit arg > `DevComms/
next_commit_message.txt` (written by the sandbox session) > 'update'.
The file is emptied after use so a stale message never labels a
later commit." As of this writing the daemon (auto commit-pushes
every 30s per AgentMemory) had NOT yet run since this file was
written — `git log --oneline` still shows the last commit as
`938dbea auto: 6 files (DASHBOARD.md, DASHBOARD.md, DASHBOARD.md,
+3)`, predating this write, so there is no consuming commit to
quote yet; the daemon's next cycle picks the message up and empties
the file, outside this task's own process.

---

## 6. File inventory — new to this task

- `~/Programming/PseudoCoupHQ/DevComms/next_commit_message.txt` —
  written (§5).
- `~/Programming/PseudoCoupHQ/DevComms/log_171_task67_bank_round13.md`
  — this file.
- `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/
  node_0_3_5_compiler_graph/PROGRESS.md` — dated entry appended
  under the existing `# PROGRESS` heading (§7 below, in that file).
- 114 dashboard files regenerated by `hq.sh dashboard` (§3.2) — not
  individually named; machine-generated projections.
- One projection rebuilt as a side effect of the dashboard run:
  `node_0_3_5_6_term/CORE_0_3_5_6_term.md` (`## sub_nodes` section).

No file in `Research/op_pipeline/` was created or edited by this
task — task 67 is verification-only over round 13's existing
artifacts, per its own brief.
