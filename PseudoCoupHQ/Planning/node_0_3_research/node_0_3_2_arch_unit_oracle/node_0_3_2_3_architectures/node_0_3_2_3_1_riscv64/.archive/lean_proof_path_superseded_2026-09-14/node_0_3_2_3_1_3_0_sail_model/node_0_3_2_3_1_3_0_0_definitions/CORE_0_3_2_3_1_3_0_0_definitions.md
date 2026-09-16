---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model.definitions
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: definitions
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_0_sail_model/node_0_3_2_3_1_3_0_0_definitions/CORE_0_3_2_3_1_3_0_0_definitions.md
super_node:
    name: sail_model
    path: ../CORE_0_3_2_3_1_3_0_sail_model.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_0_0 — definitions

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model.definitions
- **level:** 7
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [sail_model](../CORE_0_3_2_3_1_3_0_sail_model.md)

## sub_nodes

*(none yet)*

## definition

`definitions(model) -> list[ArchOpcode]`

Input: the model at a commit. Output: one `ArchOpcode` per `execute` clause in the selected modules.

Steps, in order:

1. if the Lean tree for this commit exists, read it; else run the emit lane and cache it
2. for every `def execute_<NAME>` in the tree, build an `ArchOpcode`: key from `key_of`, definition from `strip`
3. return the list; a clause that `strip` refuses is a row with a named refusal, never dropped

No case for any name. The emit lane is `emit_lane` below.
