---
id: hq.research.interp_feeder.invoke_normalizer
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: code (function)
node:
    name: invoke_normalizer
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder/node_0_3_1_11_3_invoke_normalizer/CORE_0_3_1_11_3_invoke_normalizer.md
super_node:
    name: interp_feeder
    path: ../CORE_0_3_1_11_interp_feeder.md
sub_nodes: []
---

# CORE 0_3_1_11_3 — invoke_normalizer

## metadata

- **id:** hq.research.interp_feeder.invoke_normalizer
- **level:** 4
- **status:** draft
- **designation:** code (function)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [interp_feeder](../CORE_0_3_1_11_interp_feeder.md)

## sub_nodes

*(none yet)*

## definition

The hand-off from the feeder's records to the canonical-form stage:
the written op_units records are given to the same normalizer the
compiled units go through (today `canon40_interp.py`, producing
`canon40_interp.json`). Nothing interpreter-specific happens after
this point except the seventh block kind, the arriving addressable
area, which the canonical form supplies for a handler's frame.
