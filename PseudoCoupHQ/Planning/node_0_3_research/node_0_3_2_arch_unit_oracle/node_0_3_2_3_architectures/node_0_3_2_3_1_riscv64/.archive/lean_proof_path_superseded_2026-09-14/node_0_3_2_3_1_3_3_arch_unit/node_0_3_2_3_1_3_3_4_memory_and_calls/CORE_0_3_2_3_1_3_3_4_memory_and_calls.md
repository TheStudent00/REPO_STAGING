---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.memory_and_calls
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: memory_and_calls
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_3_arch_unit/node_0_3_2_3_1_3_3_4_memory_and_calls/CORE_0_3_2_3_1_3_3_4_memory_and_calls.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_2_3_1_3_3_arch_unit.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_3_4 — memory_and_calls

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.memory_and_calls
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

`memory_and_calls(state, instruction, defs) -> state`

Input: the state at a load, store, or call. Output: the state after it.

Steps, in order:

1. a store writes its value expression to a named memory cell keyed by its address expression
2. a load reads the named cell if one matches, else an unknown named for the address
3. a call to a symbol outside the unit attaches the callee's body from the toolchain archive and walks it inline (the standing rule); a call that cannot be attached is a refusal with the symbol
4. return the new state
