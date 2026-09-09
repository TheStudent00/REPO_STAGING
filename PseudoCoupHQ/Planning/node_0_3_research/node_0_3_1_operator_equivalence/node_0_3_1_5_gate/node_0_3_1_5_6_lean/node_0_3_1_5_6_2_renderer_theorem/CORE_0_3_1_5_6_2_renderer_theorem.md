---
id: hq.research.compiler_graph.gate.lean.renderer_theorem
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: renderer_theorem
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/node_0_3_1_5_6_2_renderer_theorem/CORE_0_3_1_5_6_2_renderer_theorem.md
super_node:
    name: lean
    path: ../CORE_0_3_1_5_6_lean.md
sub_nodes: []
---

# CORE 0_3_1_5_6_2 — renderer_theorem

## metadata

- **id:** hq.research.compiler_graph.gate.lean.renderer_theorem
- **level:** 5
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean](../CORE_0_3_1_5_6_lean.md)

## sub_nodes

*(none yet)*

## definition

The preservation theorem: the term language as an inductive type with
an evaluator, the target language's expressions as a second type with
theirs, rendering as a function, and one theorem by structural
induction that evaluating the rendered expression equals evaluating
the term. PROVED for the integer subset (18 constructors) with C as
the target, no `sorry`, standard axioms only (task L1, log_227). The
C evaluator answers `Option`, so the theorem also states the rendered
C is always defined; the proof forced the correction that C's shift
count is an `int` after promotion. Next: comparisons and truth
connectives, then the rust expression type with the same induction,
then guarded division.
