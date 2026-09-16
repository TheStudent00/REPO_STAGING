---
id: hq.research.lean_proof_path_resistant_to_churn.arch_unit.meaning
level: 4
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.meaning
designation: code (method)
node:
    name: meaning
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_3_arch_unit/node_0_3_3_3_0_meaning/CORE_0_3_3_3_0_meaning.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_3_3_arch_unit.md
sub_nodes: []
---

# CORE 0_3_3_3_0 — meaning

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.arch_unit.meaning
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.meaning

## super_node

- [arch_unit](../CORE_0_3_3_3_arch_unit.md)

## sub_nodes

*(none yet)*

## definition

`meaning(unit, defs) -> LeanExpr`

Input: a unit and the definitions. Output: the expression the answering register holds, over the argument registers left unknown.

Steps, in order:

1. decode every word with `decode`
2. start a register file of unknowns named for the ABI argument registers
3. walk the instructions in address order with `compose`; at a branch apply `branch_rule`; at a load, store or call apply `memory_and_calls`
4. return the answering register's expression; a walk that is refused returns the refusal with the construct named
