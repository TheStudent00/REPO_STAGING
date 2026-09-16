---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.equals
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: equals
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_2_lean_expr/node_0_3_2_3_1_3_2_0_equals/CORE_0_3_2_3_1_3_2_0_equals.md
super_node:
    name: lean_expr
    path: ../CORE_0_3_2_3_1_3_2_lean_expr.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_2_0 — equals

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.equals
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

`equals(left, right, budget) -> Proof | Differ | Undecided`

Input: two `LeanExpr` over the same unknowns and a time budget. Output: a checked Lean proof of equality, a counterexample, or undecided with the stage it stopped at.

Steps, in order:

1. integer level first: `normalize_integer_level` on both; if the normal forms coincide, the proof is by `ring` and no circuit is built
2. else widen both (`widen`) and hand the fixed-width equation to `decide_fixed_width` under the budget
3. else, if either side is a construction the once-proved theorems cover, instantiate that theorem at this width
4. else undecided, with the stage named; never a hand edit, never a case keyed by a name

The order is the design: the cheap exact algebra before any search, the search before any authored theorem.
