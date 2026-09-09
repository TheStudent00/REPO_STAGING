---
id: hq.research.compiler_graph.gate.lean.certificates
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: certificates
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/node_0_3_1_5_6_1_certificates/CORE_0_3_1_5_6_1_certificates.md
super_node:
    name: lean
    path: ../CORE_0_3_1_5_6_lean.md
sub_nodes: []
---

# CORE 0_3_1_5_6_1 — certificates

## metadata

- **id:** hq.research.compiler_graph.gate.lean.certificates
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

Term equivalences re-proved in Lean with a checked certificate: the
pool's proved edges as theorems `∀ v0 v1, tA = tB` discharged by
`bv_decide` (bit-blasting with the SAT certificate verified in Lean),
translated from the layer-5 print form by `term_to_lean.py` with a
z3 round-trip check. Task L1 (log_227): 8 of 10 t100 edges proved in
~0.2 s each at ~450 MB; the two refused are floating point. Cost of
the fallback measured on division: 16 bits in 283 s / 12 GB, 32 and
64 undecided at 600 s. Lean's `/` and SMT-LIB's `bvudiv` differ at a
zero divisor, recorded.
