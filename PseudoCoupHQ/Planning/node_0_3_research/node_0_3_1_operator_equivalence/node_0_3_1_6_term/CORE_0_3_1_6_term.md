---
id: hq.research.compiler_graph.term
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: term
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_6_term/CORE_0_3_1_6_term.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: z3_term
      designation: code (attribute)
      realize: false
    - name: normalized_text
      designation: code (attribute)
      realize: false
    - name: transcribe
      path: node_0_3_1_6_2_transcribe/CORE_0_3_1_6_2_transcribe.md
    - name: normalize
      path: node_0_3_1_6_3_normalize/CORE_0_3_1_6_3_normalize.md
    - name: census
      path: node_0_3_1_6_4_census/CORE_0_3_1_6_4_census.md
    - name: render_back
      path: node_0_3_1_6_5_render_back/CORE_0_3_1_6_5_render_back.md
---

# CORE 0_3_1_6 — term

## metadata

- **id:** hq.research.compiler_graph.term
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- z3_term — code (attribute) *(realize: false)*
- normalized_text — code (attribute) *(realize: false)*
- [transcribe](node_0_3_1_6_2_transcribe/CORE_0_3_1_6_2_transcribe.md) — The walk that turns a unit's ledger into a z3 expression, starting at OUT-0 — the answer row — and descending through each row's operands until it reaches the IN rows, which become free symbols bound to the arrival registers.
- [normalize](node_0_3_1_6_3_normalize/CORE_0_3_1_6_3_normalize.md) — The one fixed printing rule that turns a z3 term into a single line of characters, so that two units computing the same thing print the same string.
- [census](node_0_3_1_6_4_census/CORE_0_3_1_6_4_census.md) — The filter over ledgers that lists every row whose producer has no term builder — that is, the list of what the pipeline cannot yet model.
- [render_back](node_0_3_1_6_5_render_back/CORE_0_3_1_6_5_render_back.md) — The return path from a z3 term back to arch text — turning a term into machine code again — which the standing rule about transforms requires.

## definition

A unit's computation as a z3 expression, read off its ledger from
OUT-0 downward (layer 4), and that expression printed by one fixed
rule so that two units computing the same thing print the same
characters (layer 5). The census is the filter over ledgers for rows
whose producer has no term; it is the list of what is not yet
modelled, keyed by arch opcode, never by a lifter name or an operator
token.

## design

```
class Term
	attributes:
		z3_term
		normalized_text
			"""
			layer 5: simplified once, free
			symbols renamed positionally v0, v1,
			…, printed on one line. A comparison
			key, computed beside the runnable
			text, never instead of it
			"""
	methods:
		transcribe
			"""
			sub-node: Ledger -> z3_term. Walk
			from OUT-0: producer -> term builder
			from Reference.opcode_table,
			operands -> sub-terms; stops at IN
			rows (free symbols bound to the
			arrival registers)
			"""
		normalize
			"""
			sub-node: z3_term -> normalized_text
			"""
		census
			"""
			sub-node: over a population of
			ledgers, the rows whose producer has
			no builder — producer, rows blocked,
			units, languages, and the written
			reason
			"""
		render_back
			"""
			sub-node: z3_term -> arch text; the
			return path the accumulate ruling
			requires for any transform. NOT built
			"""
```

## settled rules

- **Layer 4 is a transcription of the ledger** — no second pass over
  instructions, no sequence mining. Decision: "THE MEMORY-WRAPPED
  FORM" (4).
- **The census is a filter**, never a survey; its keys are arch
  opcodes of the blocked unit's own body. Decision: same; log_147
  §3.3.
- **Meanings come from one table** shared with the reference, so
  route two tests wiring and route one tests meaning. Decision:
  [reference](../node_0_3_1_4_reference/CORE_0_3_1_4_reference.md),
  2026-09-03.
- **A term that does not prove is withdrawn**, not kept as a weaker
  key. Decision: log_147 §1.2; the pool honours it as
  `layer5_merge_eligible`.
- **Any transform must have a return path.** `render_back` is owed;
  until it exists, layer 3 is the only runnable record and layer 5 is
  a key beside it. Decision: log_075 ("tools may transform only with
  a return path"); log_147 §8.1 names the debt.

## realization (what exists on disk, 2026-09-03)

| part | current file | status |
|---|---|---|
| transcribe | `layer4.py` (producer table + walk), drivers `census48b.py` → `layer4b_*`, `layer4c` drivers over canon38 | done: 29,149 terms over 30,436 units (log_153) |
| normalize | `layer5.py` | done; `v0 + v1` for c/op_109 and go/op_319 |
| census | `name_census3.py` / `name_census4.json`: 54 producers, 1,719 rows, 1,668 units | done; superseded `name_census.json` (lifter-keyed), `name_census2.json` (bare producers) |
| render_back | `term.py` section 5 — `RenderBack`, reached through `Term.render_back`; drivers `render_back_E00029.py`, `render_back_run.py`, `render_back_tally.py` | done: 5,909 rendered / 5,873 proved of 26,040 proved terms (log_170) |
| meanings table | `layer4.py`'s table + `vex_names.py` + `condition_table.py` | to be unified with the reference's `opcode_table` |
| round-12 run | `term61_run.py`, `term61_store/` | superseded record |
| round-13 run | `term65_run.py`, `term65_store/`, `term65_state.json`, `term65_run.log` — 30,432 records on task 64's verdicts | done (task 65, log_169) |
| round-13 four states | `audit65.py`, `audit65.json`, `audit65_printed.txt` — 26,594 / 3,134 / 285 / 419, consistency 0 | done (task 65, log_169) |
