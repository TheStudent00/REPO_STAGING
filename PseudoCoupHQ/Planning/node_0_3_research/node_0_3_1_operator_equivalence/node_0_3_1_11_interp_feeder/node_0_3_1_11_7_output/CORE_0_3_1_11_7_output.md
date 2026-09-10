---
id: hq.research.interp_feeder.output
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: grouping
node:
    name: output
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder/node_0_3_1_11_7_output/CORE_0_3_1_11_7_output.md
super_node:
    name: interp_feeder
    path: ../CORE_0_3_1_11_interp_feeder.md
sub_nodes: []
---

# CORE 0_3_1_11_7 — output

## metadata

- **id:** hq.research.interp_feeder.output
- **level:** 4
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [interp_feeder](../CORE_0_3_1_11_interp_feeder.md)

## sub_nodes

*(none yet)*

## definition

The records the feeder writes and where: per pilot,
`canon_interp_units_{java,cpython}.json` and
`canon_interp_units_ruby_php.json`; after the normalizer,
`canon40_interp.json` (eleven units, ten with bodies), all under
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/`. From there the
units are ordinary members of the term store and the pool.
