---
id: hq.research.lean_proof_path_resistant_to_churn.lean_expr.primitives
level: 4
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.primitives
designation: code (method)
node:
    name: primitives
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_2_lean_expr/node_0_3_3_2_4_primitives/CORE_0_3_3_2_4_primitives.md
super_node:
    name: lean_expr
    path: ../CORE_0_3_3_2_lean_expr.md
sub_nodes: []
---

# CORE 0_3_3_2_4 — primitives

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.lean_expr.primitives
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.primitives

## super_node

- [lean_expr](../CORE_0_3_3_2_lean_expr.md)

## sub_nodes

*(none yet)*

## definition

`primitives(expr) -> set[SailPrimitive]`

Input: an expression. Output: the atoms it is made of, each with its width: `Int.tdiv`, `BitVec.toInt`, `to_bits_truncate`, integer `+ - * ^`, comparisons, `extractLsb`, `if`.

Steps, in order:

1. walk the expression tree
2. collect each operation node with the widths of its operands
3. return the set; the swap table (`Language.operator_for`) is keyed by these

Widened on 2026-09-14 when `operator_for` was coded: the keys are every
SUBTERM of a definition over its register reads, atoms included (`(a +
b)`, `(a <<< 3)`, `(sign_extend (m := 64) (to_bits_truncate (l := 32)
...))`), reads renamed to the unknowns by the order of first occurrence
of their register. An atom alone would miss what a compiler-operator
actually computes (c's `<<` is `shift_bits_left a (extractLsb b 5 0)`,
not `shift_bits_left`). Still nothing typed: the subterms are read off
the definitions; Lean types them; a proof fills each key. Code:
`Research/oracle/riscv/leanpath/leanpath/operator_for.py`,
`candidates_of_definitions`. Measured: 136 subterms (62 unary, 74
binary) from the 42 certified straight forms.
