---
id: hq.research.compiler_graph.term.transcribe
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: transcribe
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_6_term/node_0_3_1_6_2_transcribe/CORE_0_3_1_6_2_transcribe.md
super_node:
    name: term
    path: ../CORE_0_3_1_6_term.md
sub_nodes: []
---

# CORE 0_3_1_6_2 — transcribe

## metadata

- **id:** hq.research.compiler_graph.term.transcribe
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [term](../CORE_0_3_1_6_term.md)

## sub_nodes

*(none yet)*

## definition

The walk that turns a unit's ledger into a z3 expression, starting at
OUT-0 — the answer row — and descending through each row's operands
until it reaches the IN rows, which become free symbols bound to the
arrival registers. It is a TRANSCRIPTION: it reads rows, never
instructions, so there is no second pass over the body and no sequence
mining. Each row's producer selects a term builder from the shared
opcode table, and each row's operands become the builder's arguments in
the arch text's own operand order. The width of a term is read off the
line that PRODUCED the value, not off the row, because a row does not
carry one.

## design

```
Term.transcribe
	methods:
		walk
			"""
			Ledger -> z3 term. Start at OUT-0;
			for each row take its producer's
			builder and recurse into its
			operands; stop at IN rows
			"""
		bind_inputs
			"""
			IN-i -> a free symbol standing for
			argument i, bound to arrival
			register i
			"""
		width_of
			"""
			row -> width, read off the line that
			produced the value (the relink),
			since the row itself carries none
			"""
		check_operand_slots
			"""
			replay each builder's arguments
			against the arch text's own operand
			order, so a slot swap is caught
			rather than assumed away
			"""
```

## settled rules

- **Layer 4 is a transcription of the ledger** — no second pass over
  instructions, no sequence mining. Decision: AgentMemory "THE
  MEMORY-WRAPPED FORM" (4); carried in [term](../CORE_0_3_1_6_term.md).
- **Meanings come from ONE table**, shared with the reference, so
  route two tests the ledger's wiring and route one tests meaning.
  Decision: [reference](../../node_0_3_1_4_reference/CORE_0_3_1_4_reference.md),
  2026-09-03.
- **The width comes from the producing line**, through the relink,
  not from the row. Decision: log_147 §2.3.
- **Operand slots are checked, not assumed.** Decision: log_147 §2.4.
- **A term that does not prove is withdrawn**, not kept as a weaker
  key. Decision: log_147 §1.2; the pool honours it as
  `layer5_merge_eligible`.
- **The walk follows the ledger's WIRING** where the wiring and the
  prelude disagree about which register IN-0 is. Decision: log_153 §9
  (`layer4c.py` follows the wiring, because the wiring is what it
  transcribes).

- **THE RELINK IS HANDED EVERY INPUT THE RENDER WAS HANDED** (added
  2026-09-03, task 83, after the measurement below). The relink
  re-runs the ledger walk only to learn which body line made each row,
  and then CHECKS the re-run against the stored ledger row for row.
  That check can only hold when the re-run is built from the same
  inputs the render was built from. So every argument
  `canonical_form.CanonicalForm.wrap` gives `ledger.Ledger` — today
  `runtime_routines`, `runtime_answers` (the register families each
  attached callee's own body changes) and `toolchain` (which archive
  that callee's body came from) — is given to the relink's ledger too,
  and the toolchain is the unit's own, read off its language exactly as
  `canonical_form.wrap_unit` reads it. The rule is stated as
  "every input", not as a list of three names, because the list is the
  ledger's and will grow again.
  - **THE MEASUREMENT THAT FORCED IT.** Task 78 gave `ledger.Ledger`
    `runtime_answers` and `toolchain`, and `Ledger.runtime_answer`
    refuses BY NAME when a transfer names an archive-defined routine
    whose reading was not handed in. `term.relink` built its ledger
    with neither. Over the 30,324 units canon40 proved, **3,927 of the
    3,962 that built no term carried that one refusal sentence** — the
    walk never reached the corpus at all. Handed the readings and the
    toolchain, **3,927 of 3,927 re-walk and their rebuilds match the
    stored canon40 ledger row for row**; 0 still refuse and 0 disagree.
    Evidence: `probe83_relink_readings_printed.txt`,
    `audit66_printed.txt`, log_189. Decision: this CORE, 2026-09-03,
    task 83, applying its own "the width comes from the producing
    line, through the relink" rule — a relink that refuses produces no
    width and no line.
  - **WHY IT IS RECORDED AS A DEFECT AND NOT AS A GAP.** The two
    readings were separated by measurement rather than by argument: a
    genuine gap would leave the re-walk disagreeing with the stored
    ledger, or would stop the walk inside the attached callee's body at
    a producer the one table has no builder for. Neither happened for
    any of the 3,927.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| walk and producer table | `layer4.py` | done |
| driver over canon38 | `layer4c.py`, with `layer4c_terms_<lang>.json`, `layer4c_interp.json`, `layer4c_regen_store/` | done: 29,149 terms over 30,436 units (log_153) |
| earlier drivers | `layer4_terms_<lang>.json`, `layer4b_terms_<lang>.json` | superseded records |
| resume state | `layer4c_state.json` | done |
| round-13 walk | `term65_run.py` over `reference.py` with the task-63 callee attachments; `term65_store/*.json` — 30,013 terms over 30,432 units, 0 disagreements with task 64 | done (task 65, log_169) |
| the relink's inputs | `term.py` — `_LineStamping.__init__`, `relink`, `Term.__init__`, `Term.transcribe` now carry `runtime_answers` and `toolchain` through to the ledger the re-walk builds | done (task 83, log_189) |
| the measurement that forced the fix | `probe83_relink_readings.py` / `.json` / `_printed.txt` — 3,927 of 3,927 re-walk, 0 refuse, 0 disagree | done (task 83) |
| round-15 walk | `term66_run.py` over canon40 with the same task-63 callee attachments; `term66_store/*.json`, `term66_run.log`, `term66_time.txt` | **NOT COMPLETE — CORRECTED 2026-09-04 (round-15 bank).** This row read "done" and was wrong: task 83 (log_189) STOPPED the walk under the round's own 6 GB memory cap. `term66_store` holds 10 of 332 inputs (2,132 records), byte-identical to the handoff state — the 8 shards written before the stop (569 records) were rolled back out of the store as `term66_store_bound_fired_records/`. BLOCKED because 3,927 of the 30,324 units canon40 proves carry a runtime-callee row (49,362 rows, task 78) and no memory ceiling this instance allows (512 MB to 6,144 MB tested) makes the hard shards' records converge — flagged for the owner in log_189 §7.2, not decided here. `name_census7.json`, `the_pool6.json`, `the_families6.json`, `exception_families6.json` were consequently **NOT PRODUCED**. |
