---
id: hq.research.arch_unit_oracle.simplification.matching.walk
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: walk
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_1_matching/node_0_3_2_4_1_0_walk/CORE_0_3_2_4_1_0_walk.md
super_node:
    name: matching
    path: ../CORE_0_3_2_4_1_matching.md
sub_nodes: []
---

# CORE 0_3_2_4_1_0 — walk

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.matching.walk
- **level:** 5
- **status:** draft
- **designation:** code (function)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [matching](../CORE_0_3_2_4_1_matching.md)

## sub_nodes

*(none yet)*

## definition

`walk.step(state, instruction) -> state`
- one reference step on a symbolic state; the walk from i is shared by every j, so the whole body costs N² steps, never N³. A step's cost grows with the term it carries.
