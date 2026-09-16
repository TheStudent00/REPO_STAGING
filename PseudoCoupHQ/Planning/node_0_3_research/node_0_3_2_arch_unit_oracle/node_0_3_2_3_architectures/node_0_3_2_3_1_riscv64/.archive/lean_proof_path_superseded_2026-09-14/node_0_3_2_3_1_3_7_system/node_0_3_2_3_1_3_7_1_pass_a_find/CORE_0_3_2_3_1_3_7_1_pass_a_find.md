---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.system.pass_a_find
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: pass_a_find
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_7_system/node_0_3_2_3_1_3_7_1_pass_a_find/CORE_0_3_2_3_1_3_7_1_pass_a_find.md
super_node:
    name: system
    path: ../CORE_0_3_2_3_1_3_7_system.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_7_1 — pass_a_find

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.system.pass_a_find
- **level:** 7
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [system](../CORE_0_3_2_3_1_3_7_system.md)

## sub_nodes

*(none yet)*

## definition

`pass_a_find(defs, langs, dictionary)`

Input: the definitions, the languages with meanings computed. Output: the dictionary entries the corpus already holds, and each language's swap table.

Steps, in order:

1. for every language, for every unit, for every definition: if `equals(definition, unit.lean)` proves, add an `Emulation` marked found
2. for every primitive of every definition: if `equals(primitive, unit.lean)` proves, set `operator_for[(primitive, width)] = unit`
3. record every `Differ` and `Undecided` as a row with its stage

This is "whoever gets there first" done by proof over what the compiler already emitted, with no render.
