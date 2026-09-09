# log 149 — Task 51: bank round 10

## 1. Full-stack verification

### 1.1 The spelling-ban guard, run over round 10's grouping artifacts

Command and full output, run unmodified from `op_pipeline/`:

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py the_pool2.json name_census3.json \
    the_families2.json exception_families2.json layer4b_state.json layer4b_terms_c.json \
    layer4b_terms_cpp.json layer4b_terms_go.json layer4b_terms_rust.json layer4b_terms_swift.json \
    layer4b_interp.json supersession_altered_testimony2.json swift_cdecl_witness1.json \
    pool1_pool2_delta.json the_pool2_entry_E00029.json

operator inventory: 91 tokens read from probe_manifest_*.json
PASS the_pool2.json -- no operator token in any key, grouping, pairing or row structure
PASS name_census3.json -- no operator token in any key, grouping, pairing or row structure
PASS the_families2.json -- no operator token in any key, grouping, pairing or row structure
PASS exception_families2.json -- no operator token in any key, grouping, pairing or row structure
PASS layer4b_state.json -- no operator token in any key, grouping, pairing or row structure
PASS layer4b_terms_c.json -- no operator token in any key, grouping, pairing or row structure
PASS layer4b_terms_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS layer4b_terms_go.json -- no operator token in any key, grouping, pairing or row structure
PASS layer4b_terms_rust.json -- no operator token in any key, grouping, pairing or row structure
PASS layer4b_terms_swift.json -- no operator token in any key, grouping, pairing or row structure
PASS layer4b_interp.json -- no operator token in any key, grouping, pairing or row structure
PASS supersession_altered_testimony2.json -- no operator token in any key, grouping, pairing or row structure
PASS swift_cdecl_witness1.json -- no operator token in any key, grouping, pairing or row structure
PASS pool1_pool2_delta.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool2_entry_E00029.json -- no operator token in any key, grouping, pairing or row structure
```

**15/15 PASS.** `grep -ic exempt` over the same run's output: `0`. This is the census's own
`layer4b_regen_store` directory not separately enumerated (it is a store of per-unit files,
not a grouping artifact) — the 15 files above are the full inventory of round 10's grouping
artifacts named in logs 143-148 that exist on disk under `op_pipeline/`.

Inventory source, per log: log_146 → `layer4b_*` (wrapped-form stores), `probe_manifest_*`
(unchanged, read-only); log_147 → `name_census3.json`, `layer4b_state.json`; log_148 →
`the_pool2.json`, `the_pool2_entry_E00029.json`, `pool1_pool2_delta.json`, `the_families2.json`,
`exception_families2.json`; log_143 → `swift_cdecl_witness1.json`; log_144 →
`supersession_altered_testimony2.json`.

THE SPELLING BAN, pasted verbatim as required: "THE SPELLING BAN, ABSOLUTE (the owner, restated in
anger 2026-08-25 after a second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere in this line — not
in matching, not in "which pairs get compared", not in report rows, not in dropdowns. The
candidate set for comparison comes from machine-form evidence (clusters, connections, type
pairs) or from ratified intention — never from the token. The token appears exactly once per
unit: as a display label on the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2) verdicts.py's row
pairing (caught by the owner 2026-08-25 — the fix brief itself reintroduced it as "same-operator
pairs"). MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure. A brief handed to any subagent for this line MUST paste this paragraph verbatim."

### 1.2 The authoritative count line, over the pool's population

Read directly from `the_pool2.json["summary"]` (`/tmp/reconnect_venv/bin/python3 -c
"import json; print(json.load(open('the_pool2.json'))['summary'])"`, LITERAL):

> **`the_pool2` has 5,274 entries over 30,436 member units.** Population breakdown of the
> 30,436: original 1,763 of 1,779 wrapped-and-proved units carried in; interpreter 9 of 11;
> regenerated 28,664 of 29,288.

Beside it, the term-level figures from layer 4 (`name_census3.json["tally"]`, LITERAL) — a
different population count (30,436 units measured for a ledger term, not 5,274 pool entries):

> gate textorder: PROVED_EQUAL 23,414; gate ship: PROVED_EQUAL 17,072; gate ship: DISPROVED
> 826 (`audit48_printed.txt`'s own totals block says 827 for the same figure — the two sources
> disagree by one unit and this discrepancy is being surfaced here, not resolved; log_147 §1
> carries both numbers under the same caption without reconciling them, so this report inherits
> the same open point rather than picking one silently); units with no OUT-0 term 4,142; units
> in the layer-4 population 30,436.

The 13 round-5/6 withdrawn units are a **separate, earlier population**, not part of the 826/827
above — `log_114_task28_bank_round5.md` line 242: "round-4 baseline, withdrawn this round | 13 |
were `converged`, re-gated against real ship blocks, DISPROVED"; `log_120_task33_bank_round6.md`
line 117: "The 13 withdrawn are a SEPARATE POPULATION, not a subtraction." They belong to the
round-5/6 branching audit, predate task 47's wrapped form, and are listed here only because the
brief asked that they be kept visible and not conflated with the 826/827 above.

The brief-strict count, carried forward unmerged: `the_pool2.json["summary"]
["entries_under_the_brief_strict_rule"] = 8140` (against the 5,274 kept form).

### 1.3 Prior artifacts verified untouched (superseded records)

```
$ md5sum the_pool1.json
7e38ad17d26d12d47beb4180a33098d9  the_pool1.json

$ git log -1 --format="%h %ad" -- dominant_table24.json
3405fe9 Mon Aug 31 19:38:05 2026 -0400

$ git log -1 --format="%h %ad" -- dominant_table25.json
d2e929d Wed Sep 2 01:52:15 2026 -0400
```

`the_pool1.json` carries no commit under that exact path in `git log` (it predates path-tracked
history in this working tree per `git log -- the_pool1.json` returning nothing — it exists on
disk, md5 pasted above, and round 10's commits (`git log --oneline`, `9f22c96`..`b1548a9`) never
touch it by name). `dominant_table24.json` and `dominant_table25.json` last changed Aug 31 and
Sep 2 01:52 respectively — both before round 10's task-47 work began the same day; round 10's
commit list does not include either filename. `canon36.json` and `region36.json` as literal
filenames do not exist on disk; the canon36 family is `canon36_assemble.json`,
`canon36_interp.json`, `canon36_realrun.json`, `canon36_universal_*.json`,
`canon36_zero_regression.json`, `canon36_regen_state.json` (all present, untouched by round 10's
commit list) and `region36.py` (a program, not a data artifact). This report treats "canon36 /
region36" as that file family and confirms none of it appears in round 10's `git log --oneline`
commit list.

## 2. The one-page state of the line

### 2.1 The seven-layer chain of record, as it stands on disk

| layer | what it is | artifact on disk |
|---|---|---|
| 1. extraction | raw ledger rows per unit, per language | `op_units_asg_<lang>.json` family (pre-round-10) |
| 2. context | ledger rows placed against block/consumer context | `asg_relation.json`, `asg_relation_lane.py` output |
| 2b. arrival | which population a unit arrived from (original / interpreter / regenerated) | `arrival_modes.py` output, folded into layer-3/4 stores |
| 3. wrapped | task 47's memory-wrapped form, one text per unit | `layer4b_terms_<lang>.json`, `layer4b_interp.json` (30,436 units wrapped; 1,763/1,779 original, 9/11 interpreter, 28,664/29,288 regenerated proved) |
| 4. ledger-transcribed term | task 48's z3 term per unit, gated two ways | `layer4b_state.json`; census of what has none: `name_census3.json` (47 producers, 8,044 rows, 5,507 units, each with a written cause) |
| 5. normalized | layer-5 text identity over eligible units | folded into `the_pool2.json["summary"]` (599→423, 1,726→1,058 distinct texts per log_147) |
| 6. proof | edges applied between texts | `the_pool2.json["summary"]["proved_edges_applied"] = 118` |
| 7. pool | the merged record | `the_pool2.json` (5,274 entries / 30,436 members), `the_families2.json`, `exception_families2.json` |

### 2.2 This round's corrections

- **Task 48's false guard claim, repaired.** The first "0 failures" claim in that task's own
  early pass was FALSE — two hidden exemptions in the guard's own exception path. Repaired
  structurally (not by widening the exemption list): re-run gave 334/334 PASS with 0 "exempt".
  Recorded in log_147 §13.
- **The 158-member figure from round 8, already corrected in round 9.** `the_pool2.json`'s
  E00029 entry (integer addition) carries 158 members on one layer-5 text — this figure is
  restated here unchanged from log_148, not re-derived; no new correction was needed this round.

### 2.3 the owner's open calls, carried forward

1. **The idiv implicit-destination ledger defect** (task 47's file, `layer4b_*`; named again in
   log_147 §4.1: "THE IMPLICIT DESTINATION — `idiv`, `div`, `mul`, one-operand `imul`; 1,558
   rows... ledger47 takes the last named operand as the destination, so the row it made is
   attached to the divisor and no row holds the quotient"). Not decided.
2. **The branch-label defect in the wrapped form** (log_148 §4.2.2 / §11): 4,499 member units
   carry a symbolic branch target containing the unit's own name; normalizing it would take the
   pool's distinct layer-3 texts from 6,277 to 2,999. AgentMemory's canonical-form ruling already
   requires positional branch labels — the wrapped form does not do this yet. A fix to task 47's
   form, not to the pool.
3. **The layer-3-identity merge ground** (log_148 §1.4 / §11): layer-3 wrapped-text identity was
   kept as a merge ground, giving 5,274 entries; the brief-strict count without it is 8,140.
   Awaiting a ruling on whether to keep it.
4. **The census's five "cannot model" causes** (log_147 §4.1): the machine stack has no block
   (`push`/`pop`, 4,298 rows); the implicit destination (`idiv`/`div`/`mul`/one-operand `imul`,
   1,558 rows — same defect as call 1); the x87 stack has no rows (`fucomip`/`fucomi` pairs); and
   two further causes recorded in the same section of log_147 (not re-typed here to avoid
   mis-transcribing the literal reason strings — see log_147 §4.1 for the full five, verbatim).
5. **The three Airlock calls of log_145** — call one: the ten conf-key names the instances
   feature introduced (log_145 §1); call two: may one instance run several lanes at once, given
   `run_script()` is called synchronously from the single event loop (log_145 §2); call three:
   where an instance's run records live by default (log_145 §3).
6. **A fourth Airlock call — the shared-instance `down.sh` incident** (log_143 §7.4, §9.2): a
   recompilation lane submitted at 23:41:14 UTC was cut short at ~23:41:37 (125 of 1,407 done,
   status left `running`) because a co-agent finishing task 50(b) brought the `trickle` instance
   down at the end of its own run while the lane was still in flight. The lane was still queued
   in `agent/drop`, so bringing the instance back up re-ran it from the start; it completed at
   23:58:41 with exit 0 — no result mixes the two attempts. the owner's open question, log_143 §9.2:
   "Whether an instance should refuse a `down` while a lane is running, or whether the convention
   is one instance per agent, is an Airlock question — flagged, not decided."
7. **The 826/827 idiv-and-other-cause withdrawals, restated.** `name_census3.json`'s tally gives
   826 DISPROVED under gate ship; `audit48_printed.txt`'s totals block (log_147, LITERAL) gives
   827 for the same population. This report does not reconcile the one-unit gap — it is surfaced
   here as an open point for whoever next touches layer 4's gate-ship tally.

## 3. Posterity message

Written to `PseudoCoupHQ/DevComms/next_commit_message.txt`. The repo-daemon
consumes this file by design (`PseudoCoupHQ/AgentMemory.md`, "BANKING IS A MESSAGE
NOT A COMMIT" — the daemon auto-commits every 30s regardless; this file is the human-readable
message left for whoever reads the next commit, not a manual commit).

```
$ wc -c PseudoCoupHQ/DevComms/next_commit_message.txt
1206 PseudoCoupHQ/DevComms/next_commit_message.txt
```

### 3.1 wc -c and first 5 lines, pasted immediately after writing

wc -c: **1206**

First 5 lines:
```
Round 10 banked: task 47 wrapped 30,436 units (memory form), task 48
transcribed 30,436 to ledger terms (23,414 proved / 826-827 disputed
withdrawn, name_census3.json: 47 producers / 8,044 rows / 5,507 units
each with a written cause), task 49 built the_pool2 (5,274 entries /
30,436 members, brief-strict alternative 8,140), task 50 fixed the
```

## 4. Complete file inventory (this task)

New files written by task 51:
- `DevComms/log_149_task51_bank_round10.md` — this report
- `DevComms/next_commit_message.txt` — posterity message (1,206 bytes; overwrite of prior content)
- `Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md` — dated entry appended under
  the existing `# PROGRESS` heading (no other edit to that file)

No pipeline code or data artifact was created or modified by this task — it is a verification
and banking pass only. Every artifact named in §1 and §2 pre-exists this task, written by tasks
47-50.
