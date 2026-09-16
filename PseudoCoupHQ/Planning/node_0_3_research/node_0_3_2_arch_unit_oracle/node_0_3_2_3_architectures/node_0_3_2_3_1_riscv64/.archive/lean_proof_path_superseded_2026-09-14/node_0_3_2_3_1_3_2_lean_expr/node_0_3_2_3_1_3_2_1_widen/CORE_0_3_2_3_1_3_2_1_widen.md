---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.widen
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: widen
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_2_lean_expr/node_0_3_2_3_1_3_2_1_widen/CORE_0_3_2_3_1_3_2_1_widen.md
super_node:
    name: lean_expr
    path: ../CORE_0_3_2_3_1_3_2_lean_expr.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_2_1 — widen

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.widen
- **level:** 7
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_expr](../CORE_0_3_2_3_1_3_2_lean_expr.md)

## sub_nodes

*(none yet)*

## definition

`widen(expr) -> LeanExpr`

Input: an expression that computes with width-free integers and truncates at the end (the shape every Sail definition has). Output: the same function as fixed-width bit-vector operations, each at a width that provably loses nothing.

Steps, in order:

1. compute a bound for every node from its inputs' widths (a 64 by 64 product needs 128 bits; a signed quotient 65)
2. replace each integer operation by the bit-vector operation at that width, citing Lean's library fact for the replacement
3. keep the final `to_bits_truncate` as an extract of the low bits
4. return the fixed-width expression; the facts cited are the proof that nothing was lost

The rule is general; the facts are Lean's own, about its own `Int` and `BitVec`. No bridge is authored per primitive.
