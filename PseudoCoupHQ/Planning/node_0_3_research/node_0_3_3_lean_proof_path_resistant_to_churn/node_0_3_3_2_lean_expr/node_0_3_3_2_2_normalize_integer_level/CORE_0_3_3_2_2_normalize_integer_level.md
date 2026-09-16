---
id: hq.research.lean_proof_path_resistant_to_churn.lean_expr.normalize_integer_level
level: 4
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.normalize_integer_level
designation: code (method)
node:
    name: normalize_integer_level
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_2_lean_expr/node_0_3_3_2_2_normalize_integer_level/CORE_0_3_3_2_2_normalize_integer_level.md
super_node:
    name: lean_expr
    path: ../CORE_0_3_3_2_lean_expr.md
sub_nodes: []
---

# CORE 0_3_3_2_2 — normalize_integer_level

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.lean_expr.normalize_integer_level
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.normalize_integer_level

## super_node

- [lean_expr](../CORE_0_3_3_2_lean_expr.md)

## sub_nodes

*(none yet)*

## definition

`normalize_integer_level(expr) -> LeanExpr`

Input: an expression at the integer level. Output: its polynomial normal form, with the guards (`if`) kept as cases.

Steps, in order:

1. push the truncation outward where the library allows
2. normalize each arithmetic subterm with `ring` (commutative-ring normal form)
3. return the form; two expressions with equal forms are equal by `ring`, no search

Why it exists: log 273 §3.6 named the multiply-high cause as a sum at the root of one side and an extract at the root of the other, a 64-bit multiplier identity no bit-blast decides; at the integer level both are one polynomial.
