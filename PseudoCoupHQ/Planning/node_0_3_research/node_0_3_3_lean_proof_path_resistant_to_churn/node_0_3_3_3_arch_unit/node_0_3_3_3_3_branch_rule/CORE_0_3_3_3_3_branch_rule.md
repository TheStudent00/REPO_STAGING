---
id: hq.research.lean_proof_path_resistant_to_churn.arch_unit.branch_rule
level: 4
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.branch_rule
designation: code (method)
node:
    name: branch_rule
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_3_arch_unit/node_0_3_3_3_3_branch_rule/CORE_0_3_3_3_3_branch_rule.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_3_3_arch_unit.md
sub_nodes: []
---

# CORE 0_3_3_3_3 — branch_rule

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.arch_unit.branch_rule
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.branch_rule

## super_node

- [arch_unit](../CORE_0_3_3_3_arch_unit.md)

## sub_nodes

*(none yet)*

## definition

`branch_rule(state, branch, defs) -> state`

Input: the state at a conditional branch. Output: the state after both sides, joined.

Steps, in order:

1. evaluate the branch condition as an expression over the state
2. walk the taken side and the fall-through side each to the join point
3. for every register that differs, write `if condition then taken else fallthrough`
4. return the joined state; a body with a back edge (a loop) is a refusal named `loop`, out of scope here

This is the branch-following walk the earlier line owed (a body with an `if` was read in text order).
