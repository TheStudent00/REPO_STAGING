---
id: hq.research.lean_proof_path_resistant_to_churn.lean_expr.decide_fixed_width
level: 4
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.decide_fixed_width
designation: code (method)
node:
    name: decide_fixed_width
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_2_lean_expr/node_0_3_3_2_3_decide_fixed_width/CORE_0_3_3_2_3_decide_fixed_width.md
super_node:
    name: lean_expr
    path: ../CORE_0_3_3_2_lean_expr.md
sub_nodes: []
---

# CORE 0_3_3_2_3 — decide_fixed_width

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.lean_expr.decide_fixed_width
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.decide_fixed_width

## super_node

- [lean_expr](../CORE_0_3_3_2_lean_expr.md)

## sub_nodes

*(none yet)*

## definition

`decide_fixed_width(equation, budget) -> Proof | Differ | Undecided`

Input: an equation between fixed-width expressions. Output: a checked proof, a counterexample, or undecided.

Steps, in order:

1. call Lean's bit-vector prover (`bv_decide`: bit-blast to a circuit, SAT, certificate checked) with the budget
2. on a counterexample, return it as the differing input
3. on timeout, undecided with the width and the operation kinds present

Measured limit (log 262): it times out at 16-bit multiply; multiply and divide are routed around it by `normalize_integer_level` first and by the once-proved theorems last.
