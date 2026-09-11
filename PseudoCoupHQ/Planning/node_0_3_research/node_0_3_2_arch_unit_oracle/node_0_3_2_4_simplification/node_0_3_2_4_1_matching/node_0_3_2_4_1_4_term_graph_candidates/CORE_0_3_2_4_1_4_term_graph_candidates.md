---
id: hq.research.arch_unit_oracle.simplification.matching.term_graph_candidates
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: term_graph_candidates
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_1_matching/node_0_3_2_4_1_4_term_graph_candidates/CORE_0_3_2_4_1_4_term_graph_candidates.md
super_node:
    name: matching
    path: ../CORE_0_3_2_4_1_matching.md
sub_nodes: []
---

# CORE 0_3_2_4_1_4 — term_graph_candidates

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.matching.term_graph_candidates
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

`term_graph_candidates(E) -> sub-graphs`
- the second candidate source: connected sub-graphs of the body's data-flow term instead of text ranges, so a computation the compiler interleaved with another is still one candidate. Same fingerprint, same gate.
