---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.compose
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: compose
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_3_arch_unit/node_0_3_2_3_1_3_3_2_compose/CORE_0_3_2_3_1_3_3_2_compose.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_2_3_1_3_3_arch_unit.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_3_2 — compose

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.compose
- **level:** 7
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit](../CORE_0_3_2_3_1_3_3_arch_unit.md)

## sub_nodes

*(none yet)*

## definition

`compose(state, instruction, defs) -> state`

Input: the register file as expressions, one decoded instruction, the definitions. Output: the register file after it.

Steps, in order:

1. find the definition whose key the decoded constructor carries (the emitted `execute` dispatch does this by structure, not by name)
2. substitute the current register expressions for the definition's unknowns
3. write the resulting expression into the destination register
4. return the new state
