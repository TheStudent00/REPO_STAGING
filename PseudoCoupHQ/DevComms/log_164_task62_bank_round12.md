# log_164 — TASK 62: bank round 12

Population for every count below is stated beside the count. Levels
(plan / code, layer / module) are marked where they cross.

---

## 1. The walk, in plain words, before any figure

Round 12 wrote six modules — `reference.py`, `ledger.py`,
`gate.py`, `canonical_form.py`, `term.py`, `pool.py` — over the
canon39 population (31,078 arch units attempted; 30,432 canon39
proves and wraps; 646 canon39 refuses). This task does not add a
seventh module. It re-verifies what the five task logs (159–163)
claim, against disk, in one process, and bank the round: confirm the
guard, confirm the plan tree, state the one-page picture, and hand
the daemon its commit message.

---

## 2. Verification transcripts

### 2.1 The spelling guard, re-run unmodified, by this session

```
$ cd ~/Programming/PseudoCoupHQ/Research/op_pipeline
$ git status --porcelain -- check_no_spelling_keys.py
(nothing)
$ md5sum check_no_spelling_keys.py
1d6aba67cbcdb021c3bdfd7f40fd2020  check_no_spelling_keys.py
```

Matches the md5 log_163 §5.2 recorded. The guard was not touched
between task 61's run and this one.

```
$ grep -c exempt check_no_spelling_keys.py
11
```

GLOSS. `exempt` appears 11 times inside the guard's OWN except-list
logic (the mechanism described in its docstring, e.g. `spelling_labels`
being an exempt list-name). It is a control read on the guard's own
source, not a claim about any artifact; §2.2 below is the artifact
claim, and there `grep -c exempt` was run over the MODULES, not the
guard, and returned 0 for each.

### 2.2 Every enumerated round-12 grouping artifact, PASS, this session's own run

Enumerated from logs 159–163's file inventories (§6/§7/§8 tables of
each), filtered to files that group or pair units — the ones the
mechanical guard is required to check:

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py \
    name_census5.json the_pool4.json the_families4.json \
    exception_families4.json pool3_pool4_delta.json audit61.json \
    the_pool4_bytes.json audit58.json guard58.json \
    runtime_callee_units.json runtime_callee_attachments.json \
    canon39_assemble.json

operator inventory: 91 tokens read from probe_manifest_*.json
PASS name_census5.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool4.json -- no operator token in any key, grouping, pairing or row structure
PASS the_families4.json -- no operator token in any key, grouping, pairing or row structure
PASS exception_families4.json -- no operator token in any key, grouping, pairing or row structure
PASS pool3_pool4_delta.json -- no operator token in any key, grouping, pairing or row structure
PASS audit61.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool4_bytes.json -- no operator token in any key, grouping, pairing or row structure
PASS audit58.json -- no operator token in any key, grouping, pairing or row structure
PASS guard58.json -- no operator token in any key, grouping, pairing or row structure
PASS runtime_callee_units.json -- no operator token in any key, grouping, pairing or row structure
PASS runtime_callee_attachments.json -- no operator token in any key, grouping, pairing or row structure
PASS canon39_assemble.json -- no operator token in any key, grouping, pairing or row structure
$ echo EXIT:$?
EXIT:0
```

12 of 12 PASS, exit 0. This is the main session's own run, not a
copy of log_163's transcript.

### 2.3 The two chunk stores, spot-checked by a computed sample

Populations: `term61_store/*.json` (332 files, one per proved unit
this task's term run touched) and `gate58_store/*.json` (332 files,
one per shard the gate wrote). A computed random sample (seed 62,
`random.sample`, no hand-picking) of 20 files from each:

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py <40 sampled files>
operator inventory: 91 tokens read from probe_manifest_*.json
PASS ... (all 40 files, each printed PASS individually)
$ echo EXIT:$?
EXIT:0
```

40/40 sampled files PASS (20 of 332 term61_store = 6.0%, 20 of 332
gate58_store = 6.0%). Log_163 §5.2 separately reports the full sweep
over all 332 term61_store shards (`shards checked 332 failed 0`);
this session's sample is an independent second check, not a rerun of
that full sweep.

### 2.4 No carve-out claimed, this session's own grep

```
$ grep -c exempt reference.py gate.py ledger.py canonical_form.py term.py pool.py
reference.py:0
gate.py:0
ledger.py:0
canonical_form.py:0
term.py:0
pool.py:0
```

None of the six round-12 modules declares an exemption.

### 2.5 Pool4's authoritative count line, over pool4's own population

**Population: 1,961 entries over 30,432 member units.**

| sub-population | attempted | canon39-proved (= pool4 member source) |
|---|---|---|
| original (compiled corpus) | 1,779 | **1,763** |
| interpreter | 11 | **9** |
| regenerated | 29,288 | **28,660** |
| TOTAL | 31,078 | **30,432** |

(Source: log_162 §1.2's own table, cited because pool4's 30,432
members are exactly canon39's WRAPPED_TEXT_PROVED population per
log_163 §1.2 — pool4 does not re-derive this split, so it is quoted
from the layer that produced it, with the level named.)

Term figures beside it, same population, from log_163 §1.2
(`audit61_printed.txt`, quoted verbatim there and re-confirmed present
on disk at `audit61.json`, 596,227 bytes, this session):

```
proved 26,040 | withdrawn 0 | undecided 3,865 | no term 527
(26,040 + 0 + 3,865 + 527 = 30,432 ✓)
```

The brief-strict count, recorded and unused: **5,668**, key path
`summary.entries_under_the_brief_strict_rule` inside `the_pool4.json`
(log_163 §4.1, §1.4).

**The 13 round-5/6 withdrawn units — a separate population, listed
apart from the 30,432 above.** These are not part of canon39/pool4 at
all; they are a standing exception carried since round 6. Source:
log_112 (task 26, "new bucket remainder"), the branching audit's own
count line —

```
'audit_branching_rechecked': 18, 'audit_branching_still_proved': 5,
'audit_branching_withdrawn': 13
```

— 18 units the branching audit rechecked out of the 1,561-unit round-5
baseline, of which 5 still proved and 13 did not re-prove and were
withdrawn (recorded as CONVERGED in the round-5 record, but the
re-gate did not prove them). Log_117 §"honest standing converged"
carries them forward as "withdrawn by log_112's branching audit
(recorded converged, re-gate did not prove): 13" against "honest
standing converged: 1622" of a 1,635-unit population. They are a
DIFFERENT population from canon39/pool4 (round 5/6 predates canon38
and canon39 entirely) and are listed here, separately, because the
brief asked for them named beside the pool4 line, not folded into it.

### 2.6 Prior artifacts verified untouched (superseded records)

| file | git status --porcelain | md5 |
|---|---|---|
| `the_pool3.json` | (clean) | `74c12f215b15793a33310597f5178170` |
| `canon38_wrapped_c.json` | (clean) | — (5,012,800 bytes, mtime 2026-09-02 23:24, unchanged) |
| `layer4c.py` | (clean) | `d8c1f59539bc1de2063ca640ae3ae531` |
| `name_census4.json` | (clean) | `a645c01861caf22a3462c87743d9df99` |

`git status --porcelain` on all four returned nothing — no
uncommitted change, and the daemon's own auto-commits (checked via
`git log --oneline`) show no commit touching these paths after their
writing task. Superseded, not edited.

### 2.7 The module-name rule

```
$ grep -n "^class" reference.py
214:class MachineState(object):
364:class Operands(object):
1319:class Entry(object):
1382:class OpcodeTable(object):
1574:class Reference(object):

$ grep -n "^class" gate.py
106:class Verdict(object):
172:class Gate(object):

$ grep -n "^class" ledger.py
340:class Producer(object):
1000:class Row(object):
1054:class Ledger(object):

$ grep -n "^class" canonical_form.py
216:class Prelude(object):
320:class Epilogue(object):
356:class Labels(object):
388:class Refuse(object):
452:class CanonicalForm(object):

$ grep -n "^class" term.py
149:class _LineStamping(L.Ledger):
282:class Transcription(object):
328:class Term(object):

$ grep -n "^class" pool.py
109:class UnionFind(object):
426:class Pool(object):
```

Each of the six module files exists, at `Research/op_pipeline/`, and
carries a class matching its CORE name (`Reference`, `Gate`,
`Ledger`, `CanonicalForm`, `Term`, `Pool`), each alongside the smaller
classes its own design uses.

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
[WARN] nodes-register: ... 14 CORE(s) ...
[WARN] projection: `## sub_nodes` is not the first section on 53 CORE(s)
[WARN] edge-register: `super_node`/`sub_nodes` missing on 14 of 67 nodes
[INFO] completeness: 0 of 67 complete (54 leaves)
summary: 4 error(s), 3 warning(s)
```

**All 4 dangling-path lines pre-date this round**, checked by
`git blame` on the exact line:

| dangling path | PROGRESS.md line | blamed commit date |
|---|---|---|
| `log_107_task21_interp_` (truncated) | 1553 | 2026-09-01 10:30 |
| `log_110_task25_` (truncated) | 1695 | 2026-09-01 11:18 |
| `~/Programming/Sources/llvm-` (truncated) | 79 | 2026-08-31 17:16 |
| `~/Programming/SandboxDesign/allow.sh` | 73 (dominant_intentions) | 2026-08-14 14:00 |

Round 12's task briefs (log_158) are dated 2026-09-02/03; every one of
these four lines was written before that. Each is a truncated path (a
line that got cut mid-sentence in an old prose paste, not a real
reference), a known pre-existing defect, not a round-12 regression.
The 14-CORE register gap and the 53-CORE projection-order warning are
the pre-existing, ruled-non-sweep gap AgentMemory records ("brought in
chain by chain, not by a sweep").

### 3.2 Dashboards regenerated

```
$ bash ~/Programming/PseudoCoupHQ/hq.sh dashboard
=== rebuilding node projections ===
projection rebuilt: .../node_0_3_5_3_ledger/CORE_0_3_5_3_ledger.md (`## sub_nodes`)
=== regenerating dashboards ===
wrote 114 dashboard(s)
```

### 3.3 Every round-12 node's PROGRESS.md, off `planned`

The nine level-3 sub-nodes of `compiler_graph` (its own `sub_nodes`
register: probes, arch_unit, canonical_form, ledger, reference, gate,
term, pool, guard):

```
node_0_3_5_0_probes         :: status: living
node_0_3_5_1_arch_unit      :: status: living
node_0_3_5_2_canonical_form :: status: living
node_0_3_5_3_ledger         :: status: living
node_0_3_5_4_reference      :: status: living
node_0_3_5_5_gate           :: status: living
node_0_3_5_6_term           :: status: living
node_0_3_5_7_pool           :: status: living
node_0_3_5_8_guard          :: status: living
```

None reads `planned`. The sub-nodes each round-12 task named (all 12
checked individually, `head -3` on each `PROGRESS.md`, all `status:
living`):
`node_0_3_5_4_reference/node_0_3_5_4_0_opcode_table`,
`.../node_0_3_5_4_1_machine_state`,
`node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee`,
`node_0_3_5_6_term/node_0_3_5_6_2_transcribe`,
`.../node_0_3_5_6_3_normalize`, `.../node_0_3_5_6_4_census`,
`.../node_0_3_5_6_5_render_back`,
`node_0_3_5_7_pool/node_0_3_5_7_1_entry`,
`.../node_0_3_5_7_2_merge_grounds`, `.../node_0_3_5_7_4_representative`,
`.../node_0_3_5_7_5_families`, `.../node_0_3_5_7_6_exception_families`.

A confirmed grep, no negative case found:

```
$ grep -rln "^status: planned" node_0_3_5_4_reference node_0_3_5_5_gate \
    node_0_3_5_3_ledger node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee \
    node_0_3_5_2_canonical_form node_0_3_5_6_term node_0_3_5_7_pool \
    --include=PROGRESS.md
(no output — exit 1, meaning no match)
```

---

## 4. The one-page state of the line

### 4.1 The chain, mapped to round-12 modules

The pipeline's ratified six steps (AgentMemory) and the pool's own
layer count (term CORE's own words: layer 4 = the z3 expression read
off the ledger, layer 5 = that expression's fixed-rule printing) give
this stack, module by module:

| stage | what it holds | which round-12 module realizes it |
|---|---|---|
| 1. probe | compiled machine code, one per operator × operand types | `probes` (pre-round-12; unchanged this round) |
| 2. arch unit | the bytes, arrival/exit registers, runtime-callee bytes | `arch_unit` (this round: `node_0_3_5_1_8_runtime_callee` sub-node moved to living, via `ledger.py`'s producer field) |
| 3 (layer 3). canonical form | the body between a standardized prelude/epilogue — the RUNNABLE, byte-comparable text | `canonical_form.py` |
| — ledger | the row table beside each canonical unit: one row per value, its producer opcode, what it read | `ledger.py` |
| — reference | the symbolic simulator every proof runs against | `reference.py` |
| — gate | the proof obligations and the object (`Gate`) that discharges them, over the reference | `gate.py` |
| 4 (layer 4). term | the unit's computation as a z3 expression, read off the ledger from OUT-0 downward | `term.py` (`Term.transcribe`) |
| 5 (layer 5). normalized text | that expression printed by one fixed rule, so identical computations print identical characters | `term.py` (`Term.normalize`) |
| — pool | the one pool where proved-equivalent units collapse into one entry | `pool.py` |

Ledger, reference and gate do not each own a numbered layer of their
own; they are the machinery that PRODUCES and VERIFIES layers 3-5
(ledger holds layer-3's row structure, reference simulates it, gate
proves it). Seven objects named in `CORE_0_3_5_compiler_graph.md`'s
own `sub_nodes` register carry the whole chain end to end: probes,
arch_unit, canonical_form, ledger, reference, gate, term/pool
(term and pool are two nodes but close the same seven-stage walk
begun by probes); the ninth sub-node, `guard`, is the spelling-ban
mechanism run across all of them, not a data layer.

### 4.2 The pool

1,961 entries over 30,432 members (§2.5). 573 entries span more than
one language (of 632 in pool3 — a movement caused by the round-12
fixes, computed cause-by-cause in `pool3_pool4_delta.json`: 7 splits,
107 merges). 3 entries span compiled and interpreted code, unchanged
from pool3. 34 families (down from 36; log_163 §4.5 computes the
cause).

### 4.3 The census

`name_census5.json`/`name_census5_printed.txt`: the rows whose
producer has no builder, replacing census4. Task 61's own delta
against census4 (log_163 §3.3) is the record of what closed and what
newly appeared; this task does not recompute it, only confirms the
file passes the guard (§2.2 above) and exists.

### 4.4 The round's corrections

1. **log_159 §10, same-day wording correction.** `reference.py`'s
   header, `acceptance57.py`'s gloss, and log_159's own §1.4/§2.2/§8
   first said a `call` into a compiler support routine is "refused by
   name — library routine, out of scope". That framing is SUPERSEDED
   by the owner's round-12 ruling (log_158 task 59(b)): the callee's body
   gets extracted from the toolchain's own runtime archive and
   attached as an ArchUnit. `reference.py:Entry` gained a `cause`
   field so each census row states its own reason rather than sharing
   one blanket sentence; the phrase "out of scope" survives in exactly
   one place, the retraction sentence itself (`grep -c -i "out of
   scope" reference.py` = 0; only the printed transcript's own
   correction paragraph carries it).
2. **log_160's code-before-CORE deviation.** The flag-triple defect
   (a setter's condition reading the wrong two of its three recorded
   values, causing 1,338 units to prove on one route and disprove on
   the other) was found by a running gate; the one-line fix in
   `reference.py` plus a width rule in `gate.py` were made and
   verified BEFORE the `machine_state` CORE's settled rule was
   written. Round 12's binding rule 2 says CORE-first. This is
   recorded as a deviation, not smoothed over, with the rule written
   afterward carrying its own provenance note.
3. **log_163's name collision.** Task 61's brief named
   `exception_families3.json` for the rebuild; that name was already
   on disk (round 5's own build over `guards5.json`, 2026-09-01). Per
   PROTOCOL §2, the CORE was corrected first (a new settled rule
   naming the collision, with provenance) and the artifact was written
   as `exception_families4.json` instead.

### 4.5 Owed work, named as next round's planned items (not open calls for the owner — log_158 records none)

1. **`render_back`** (node `0_3_5_6_5`) — still `planned`,
   deliberately: `Term.render_back` refuses by name rather than
   returning a look-alike rendering. Until it exists, layer 3 (the
   canonical text) is the only runnable record and layer 5 is a key
   beside it, not a substitute.
2. **The reference's branch model, and relocation-aware runtime-callee
   attachment.** The shared reference walks a body in text order, so
   425 `test`/`j<cc>` pairs and the whole runtime-callee family land
   as census rows rather than proved terms — the largest single cause
   in census5 (log_163 §7.1). The runtime-callee attachment itself is
   only partly done: 304 units carry a runtime_callee row (608 rows
   total; log_163 §3.4), but the archive bodies' own calls are
   unrelocated, so nested callees inside an attached body (e.g.
   `__udivti3`'s own `je` and `endbr64`) have no name to follow and no
   opcode-table entry, adding 78+78 more census rows per callee
   (log_163 §2.4.5 / census breakdown, lines 382-383).
3. **The `emit` module** (node `0_3_5_0_3`) — part of the `probes`
   sub-node, not touched this round; still whatever state it was in
   before round 12 (this task made no change to `probes`).
4. **The swift re-run.** Log_161 recorded 4 swift units refused for
   runtime-callee attachment because no swiftc archive exists on
   either the host or the sandbox — "a settled rule", not an open
   question, but the archive itself is still absent and swift's 4
   census rows (log_163's "4 missing from the total" between task 58
   and task 61 populations) stay open until one is provided.
5. **Restarting `sandbox-runner` onto the rebuilt image** — named by
   the round-12 briefs as standing infrastructure work; not touched by
   tasks 57-61 or by this banking task, and not verified here (outside
   this task's file set).

---

## 5. Posterity message

```
$ wc -c ~/Programming/PseudoCoupHQ/DevComms/next_commit_message.txt
516 next_commit_message.txt
$ head -5 ~/Programming/PseudoCoupHQ/DevComms/next_commit_message.txt
round 12 banked: reference/gate/ledger/canonical_form/term/pool modules
written and gated over canon39 (30,432 proved of 31,078); pool4 has
1,961 entries over 30,432 members (573 multi-language, 3 compiled+
interpreted, 34 families); spelling-ban guard re-verified clean by
the main session over every round-12 grouping artifact plus a 40-file
```

The daemon consumes this file by design: `git_commit_push.sh`'s own
comment states the priority order — "explicit arg > `DevComms/
next_commit_message.txt` (written by the sandbox session) > 'update'.
The file is emptied after use so a stale message never labels a later
commit." As of this writing the daemon (which auto commit-pushes
every 30s per AgentMemory) has NOT yet run since the file was written
in this task — `git log --oneline` still shows the last commit as
`19a9565 auto: 1 file (task61_resume.md)`, predating this write, so
there is no consuming commit to quote yet. The daemon's next cycle
will pick the message up and empty the file; that happens outside
this task's own process.

---

## 6. File inventory — new to this task

- `~/Programming/PseudoCoupHQ/DevComms/next_commit_message.txt` —
  written (§5).
- `~/Programming/PseudoCoupHQ/DevComms/log_164_task62_bank_round12.md`
  — this file.
- `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/
  node_0_3_5_compiler_graph/PROGRESS.md` — dated entry appended
  under the existing `# PROGRESS` heading (§7 below).
- 114 dashboard files regenerated by `hq.sh dashboard` (§3.2) — not
  individually named; they are machine-generated projections, not
  authored content.
- One projection rebuilt: `node_0_3_5_3_ledger/CORE_0_3_5_3_ledger.md`
  (the `## sub_nodes` section), as a side effect of the dashboard run.

No file in `Research/op_pipeline/` was created or edited by this task
— task 62 is verification-only over round 12's existing artifacts, per
its own brief.
