---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.primitives
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: primitives
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_2_lean_expr/node_0_3_2_3_1_3_2_4_primitives/CORE_0_3_2_3_1_3_2_4_primitives.md
super_node:
    name: lean_expr
    path: ../CORE_0_3_2_3_1_3_2_lean_expr.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_2_4 — primitives

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.primitives
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

`primitives(expr) -> set[SailPrimitive]`

Input: an expression. Output: the atoms it is made of, each with its width: `Int.tdiv`, `BitVec.toInt`, `to_bits_truncate`, integer `+ - * ^`, comparisons, `extractLsb`, `if`.

Steps, in order:

1. walk the expression tree
2. collect each operation node with the widths of its operands
3. return the set; the swap table (`Language.operator_for`) is keyed by these
