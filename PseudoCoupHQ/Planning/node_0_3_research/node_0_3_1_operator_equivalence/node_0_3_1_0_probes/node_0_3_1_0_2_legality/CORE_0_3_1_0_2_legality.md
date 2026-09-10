---
id: hq.research.compiler_graph.probes.legality
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: legality
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_0_probes/node_0_3_1_0_2_legality/CORE_0_3_1_0_2_legality.md
super_node:
    name: probes
    path: ../CORE_0_3_1_0_probes.md
sub_nodes: []
---

# CORE 0_3_1_0_2 — legality

## metadata

- **id:** hq.research.compiler_graph.probes.legality
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [probes](../CORE_0_3_1_0_probes.md)

## sub_nodes

*(none yet)*

## definition

The reader of a compiler's OWN legality rules — the conditions under
which that compiler refuses an operator on a pair of operand types —
recorded with the file and line of the compiler source each rule was
read from. Given an operator and its operand types it predicts accept
or refuse before any probe is compiled. It is a cost saver, because a
predicted refusal need not be built, and a second witness, because a
prediction that disagrees with the compiler is a defect worth reading.
It is never the oracle: compile-or-refuse decides.

## design

```
probes.legality
	attributes:
		rules
			"""
			one entry per rule read out of a
			compiler's source: language, the
			operator arity it governs, the
			operand condition, and the source
			file + line it was read from
			"""
	methods:
		read_rules
			"""
			compiler source -> rules; each rule
			carries its file and line so the
			claim can be re-read
			"""
		predict
			"""
			(operator, operand_types) -> accept
			or refuse; the prediction is
			compared against the compiler's own
			answer, never substituted for it
			"""
```

## settled rules

- **Compile-or-refuse is the acceptance oracle; the legality reader
  only predicts.** Decision: [probes](../CORE_0_3_1_0_probes.md)
  settled rules, ratified pipeline step 1.
- **Every rule carries the compiler source file and line it was read
  from**, so a prediction can be checked against the compiler rather
  than trusted. Decision: this CORE, 2026-09-03, refining the
  "second witness" line of [probes](../CORE_0_3_1_0_probes.md).
- **A disagreement between prediction and compiler is a defect to be
  read, not a tie to be broken** in the predictor's favour. Decision:
  this CORE, 2026-09-03.

## realization (what exists on disk, 2026-09-03)

Home: `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| read_rules | `legality_rules.py` | done |
| rules | `legality_rules.json` | done |
| predict, applied to the grid | `legality_filter3.py` (with `legality_filter.py`, `legality_filter2.py` before it) | done |
| the saving measured | `legality_reduction3.json` (with `legality_reduction.json`, `legality_reduction2.json`) | done |
| prediction against compiler | `legality_validation2.json`, `legality_quirks.json` | done |
