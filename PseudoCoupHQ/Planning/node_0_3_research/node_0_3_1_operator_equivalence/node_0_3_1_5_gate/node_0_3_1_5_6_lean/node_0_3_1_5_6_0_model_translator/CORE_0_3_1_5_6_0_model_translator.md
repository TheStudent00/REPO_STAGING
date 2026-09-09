---
id: hq.research.compiler_graph.gate.lean.model_translator
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: model_translator
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/node_0_3_1_5_6_0_model_translator/CORE_0_3_1_5_6_0_model_translator.md
super_node:
    name: lean
    path: ../CORE_0_3_1_5_6_lean.md
sub_nodes: []
---

# CORE 0_3_1_5_6_0 — model_translator

## metadata

- **id:** hq.research.compiler_graph.gate.lean.model_translator
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

The translator from the reference simulator's opcode semantics (the
opcode table `reference.py` and the term walk use, VEX semantics via
pyvex) to Lean definitions, so that level 0 of the proof system — the
mapping model of every arch opcode, flags and partial region included
— is DERIVED from the one source the gate already uses and never
written a second time. Checked by the single-opcode units: each is
the model's operation definitionally (`rfl`) or a named discrepancy
between the two readings. First in the lean node's order (ruled
2026-09-07); task L2. Not started.
