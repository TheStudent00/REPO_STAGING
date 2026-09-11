---
id: hq.research.arch_unit_oracle.simplification.matching.fingerprint_index
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: fingerprint_index
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_1_matching/node_0_3_2_4_1_2_fingerprint_index/CORE_0_3_2_4_1_2_fingerprint_index.md
super_node:
    name: matching
    path: ../CORE_0_3_2_4_1_matching.md
sub_nodes: []
---

# CORE 0_3_2_4_1_2 — fingerprint_index

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.matching.fingerprint_index
- **level:** 5
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [matching](../CORE_0_3_2_4_1_matching.md)

## sub_nodes

*(none yet)*

## definition

`FingerprintIndex`
- every unit's term evaluated at k concrete points, edge values first, keyed by the k-tuple; `lookup(fingerprint)` returns the units that agree at every point. The z3 call count is the collision count, and is reported beside the segment count.
