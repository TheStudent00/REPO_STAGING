---
id: hq.research.arch_unit_oracle.simplification.emulator_arch_units.extract
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: extract
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_0_emulator_arch_units/node_0_3_2_4_0_0_extract/CORE_0_3_2_4_0_0_extract.md
super_node:
    name: emulator_arch_units
    path: ../CORE_0_3_2_4_0_emulator_arch_units.md
sub_nodes: []
---

# CORE 0_3_2_4_0_0 — extract

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.emulator_arch_units.extract
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

`extract(certificate) -> (body, term)`
- compile at the certificate's flags, carve at the symbol, walk through the reference. Refuses by name when the compiler or the carve refuses; never substitutes a body.
