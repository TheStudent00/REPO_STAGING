---
id: hq.research.compiler_graph.pool.families
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), finding
node:
    name: families
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_7_pool/node_0_3_1_7_5_families/CORE_0_3_1_7_5_families.md
super_node:
    name: pool
    path: ../CORE_0_3_1_7_pool.md
sub_nodes: []
---

# CORE 0_3_1_7_5 — families

## metadata

- **id:** hq.research.compiler_graph.pool.families
- **level:** 4
- **status:** draft
- **designation:** code (method), finding
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [pool](../CORE_0_3_1_7_pool.md)

## sub_nodes

*(none yet)*

## definition

The dominant-operator rule applied over the pool's entries, producing
groups of language-operators that behave as one operation across
languages. A node is a triple: a language, one of that language's
grammar operators, and its arity. An edge runs only BETWEEN languages
and is weighted by how many pool entries the two nodes share. Each node
keeps its single strongest counterpart per foreign language, and the
edge survives only when the choice is MUTUAL. The connected components
of what survives are the families. The rule is imported from
`dom_ops.py` unchanged, so it cannot drift here; the current build is
36 families over 197 nodes.

## design

```
Pool.families
	methods:
		build_nodes
			"""
			pool entries -> nodes (language,
			grammar-operator, arity)
			"""
		build_edges
			"""
			nodes -> cross-language edges,
			weighted by shared entry count
			"""
		best_per_language
			"""
			each node keeps its single strongest
			counterpart per foreign language
			"""
		mutual_edges
			"""
			keep an edge only when both ends
			chose each other
			"""
		components
			"""
			connected components of the mutual
			graph -> the families
			"""
```

The build, from `the_families3_run.log`:

| quantity | value |
|---|---|
| pool entries read | 2,247 |
| pool units read | 30,436 |
| nodes | 197 |
| cross-language edges, raw | 867 |
| edges surviving the mutual filter | 305 |
| families | 36 |

Two instances: `F0009`, the bitwise-not family, six nodes across c,
cpp, go, rust and swift — five spellings, one family. `F0001`, the
addition family, 17 nodes across c, cpp, cpython, go, java, php, ruby,
rust and swift — nine languages.

## settled rules

- **The dom_op rule is IMPORTED from `dom_ops.py`, never restated**,
  so it cannot drift between builds. Decision: log_148 §6.1; log_154
  §7.1; carried in [pool](../CORE_0_3_1_7_pool.md).
- **A node is (language, grammar-operator, ARITY).** Decision:
  log_154 §7.1.
- **The operator token is a `label` display field read by nothing.**
  Decision: THE SPELLING BAN; log_154 §7.1.
- **Family sets are compared by NODE SET, not by family name**, so a
  renumbering is not read as a change. Decision: log_154 §7.2.

## realization (what exists on disk, 2026-09-03)

Home: `PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| the rule | `dom_ops.py` (imported unchanged) | done |
| current build | `build_the_families3.py`, `the_families3.json`, `the_families3_run.log` — 36 families / 197 nodes | done (log_154 §7) |
| previous build | `build_the_families2.py`, `the_families2.json` | superseded record |
| continuity checked by node set | log_148 §6.2, log_154 §7.2 | done |
| round-13 build | `pool65_run.py`, `the_families5.json`, `pool65_run.log` — 34 families / 197 nodes, 1,334 raw edges, 345 mutual | done (task 65, log_169) |
