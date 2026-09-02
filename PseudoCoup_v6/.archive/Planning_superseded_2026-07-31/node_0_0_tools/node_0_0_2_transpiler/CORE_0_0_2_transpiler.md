---
id: pcv6.tools.t3_transpiler
level: 2
status: settled
settled_by: the owner
supersedes: null
decision: ../../../AgentMemory/02_decisions.md
---

# CORE 0_0_2 — T3: Transpiler

The generalized ingress framework (tree-sitter tree → UR-AST +
ledger population) with per-language ingestors as thin
specializations; emission framework later. Settled (the owner-aligned
2026-07-28): **fresh spine in PCv6 mining the lineage** (no
wholesale port; every transplant carries provenance + its
acceptance test); coverage gate and gate-before-emit are framework
features; ledger writes id-keyed from the start; **first milestone
is ingress only** (Rust→hub).

Harvest map: [transpiler survey](../../../../PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md).
Lowering logic enters the hub by TRANSPILING THE COMPILER AND
SLICING, never by table mining (closed decision).

## Nodes

- [node_0_0_2_0_ingress_framework](node_0_0_2_0_ingress_framework/CORE_0_0_2_0_ingress_framework.md)
  — the general pipeline and the ingestor contract.
- [node_0_0_2_1_rust_ingestor](node_0_0_2_1_rust_ingestor/CORE_0_0_2_1_rust_ingestor.md)
  — first milestone: the compiler-source ingress rebuilt on
  tree-sitter, verified against PCv5's own artifacts.
- [node_0_0_2_2_emission](node_0_0_2_2_emission/CORE_0_0_2_2_emission.md)
  — deferred: the emission framework's settled constraints, held
  until ingress stands.
