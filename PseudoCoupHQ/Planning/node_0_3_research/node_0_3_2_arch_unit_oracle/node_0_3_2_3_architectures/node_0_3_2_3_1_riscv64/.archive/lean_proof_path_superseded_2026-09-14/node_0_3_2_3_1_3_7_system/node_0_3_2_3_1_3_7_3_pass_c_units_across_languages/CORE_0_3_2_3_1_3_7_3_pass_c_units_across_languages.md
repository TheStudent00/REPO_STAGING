---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.system.pass_c_units_across_languages
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: pass_c_units_across_languages
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_7_system/node_0_3_2_3_1_3_7_3_pass_c_units_across_languages/CORE_0_3_2_3_1_3_7_3_pass_c_units_across_languages.md
super_node:
    name: system
    path: ../CORE_0_3_2_3_1_3_7_system.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_7_3 — pass_c_units_across_languages

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.system.pass_c_units_across_languages
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

`pass_c_units_across_languages(langs, dictionary)`

Input: the languages with meanings. Output: for every source operator at a type pair, whether its units in two languages compute the same function (the claim of the riscv64 node, and the Hub's ground).

Steps, in order:

1. for every pair of languages, for every operator and type pair both compiled: `equals(unit_i.lean, unit_j.lean)`
2. record proved, differ with the input, or undecided
3. the Hub composes over the dictionary from pass A and B; this pass is its check

Planned after passes A and B land on the handful; not in the first run.
