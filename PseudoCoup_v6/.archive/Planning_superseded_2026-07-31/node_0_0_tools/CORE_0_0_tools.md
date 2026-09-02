---
id: pcv6.tools
level: 1
status: settled
settled_by: the owner
supersedes: pcv6.planning.tools_program_flat
decision: ../../AgentMemory/02_decisions.md
---

# CORE 0_0 — Tools Program

The initial PCv6 work is constructing the tools (the owner, 2026-07-28).
Standing rules: every tool ships with a falsifiable acceptance
test; oracle assets live beside the tool they check; harvested code
carries a provenance header; tool files are named verb-object with
a one-sentence-purpose docstring first line.

Build order (dependencies): **T1 → T2 → T3 → T4 ∥ T5 → T6.**
Research entries [R2, R3](../node_0_1_research/CORE_0_1_research.md)
run before/alongside T2–T3. Tools graduate into `Tools/` only on
passing acceptance.

## Nodes (one per tool)

- [node_0_0_0_tree_sitter_base](node_0_0_0_tree_sitter_base/CORE_0_0_0_tree_sitter_base.md)
  — T1: grammars vendored+pinned, parser factory, coverage
  recorder. Everything parses through this; nothing else
  constructs a parser.
- [node_0_0_1_ledger](node_0_0_1_ledger/CORE_0_0_1_ledger.md)
  — T2: the one-record, three-axis, id-keyed ledger. **Deep
  detail below this node.**
- [node_0_0_2_transpiler](node_0_0_2_transpiler/CORE_0_0_2_transpiler.md)
  — T3: fresh-spine ingress framework + Rust ingestor first.
  **Deep detail below this node.**
- [node_0_0_3_polyfill](node_0_0_3_polyfill/CORE_0_0_3_polyfill.md)
  — T4: the uniform-law wrapper layer.
- [node_0_0_4_intentions](node_0_0_4_intentions/CORE_0_0_4_intentions.md)
  — T5: dominance as validated, slicer-consumable data (R1's four
  gaps are its work list).
- [node_0_0_5_slicer](node_0_0_5_slicer/CORE_0_0_5_slicer.md)
  — T6: intentions-driven extraction + insertion; built last;
  automation lives here.
