---
id: hq.research.arch_unit_oracle.simplification.emulator_arch_units.attest
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: attest
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_0_emulator_arch_units/node_0_3_2_4_0_1_attest/CORE_0_3_2_4_0_1_attest.md
super_node:
    name: emulator_arch_units
    path: ../CORE_0_3_2_4_0_emulator_arch_units.md
sub_nodes: []
---

# CORE 0_3_2_4_0_1 — attest

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.emulator_arch_units.attest
- **level:** 5
- **status:** draft
- **designation:** code (function)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [emulator_arch_units](../CORE_0_3_2_4_0_emulator_arch_units.md)

## sub_nodes

*(none yet)*

## definition

`attest(body)`
- one row in the canon store: the body, its term text, `origin: emulation`, the cell, the tier, the certificate id. The guard runs over the store afterwards.
