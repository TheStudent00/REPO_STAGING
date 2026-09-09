---
id: hq.research.interp_feeder.feeder_config
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: code (class)
node:
    name: feeder_config
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder/node_0_3_1_11_0_feeder_config/CORE_0_3_1_11_0_feeder_config.md
super_node:
    name: interp_feeder
    path: ../CORE_0_3_1_11_interp_feeder.md
sub_nodes: []
---

# CORE 0_3_1_11_0 — feeder_config

## metadata

- **id:** hq.research.interp_feeder.feeder_config
- **level:** 4
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [interp_feeder](../CORE_0_3_1_11_interp_feeder.md)

## sub_nodes

*(none yet)*

## definition

The configuration object of the feeder: which interpreter dump files
are read and which directory the op_units-shaped records are written
to. `FeederConfig(target_files, output_directory)` in
`PseudoCoupHQ/Research/op_pipeline/interp_feeder.py`.
It holds no logic; a run is one config plus the functions below.
