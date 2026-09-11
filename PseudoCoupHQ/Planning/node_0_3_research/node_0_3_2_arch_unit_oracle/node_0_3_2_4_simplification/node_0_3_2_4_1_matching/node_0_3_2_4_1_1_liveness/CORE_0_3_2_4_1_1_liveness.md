---
id: hq.research.arch_unit_oracle.simplification.matching.liveness
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: liveness
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_1_matching/node_0_3_2_4_1_1_liveness/CORE_0_3_2_4_1_1_liveness.md
super_node:
    name: matching
    path: ../CORE_0_3_2_4_1_matching.md
sub_nodes: []
---

# CORE 0_3_2_4_1_1 — liveness

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.matching.liveness
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

`liveness(E, i, j) -> live_interface`
- one backward pass per i gives, for every j, what the segment reads from before i and what it writes that is read after j (registers and flags). Keeps the matching at N² overall.
