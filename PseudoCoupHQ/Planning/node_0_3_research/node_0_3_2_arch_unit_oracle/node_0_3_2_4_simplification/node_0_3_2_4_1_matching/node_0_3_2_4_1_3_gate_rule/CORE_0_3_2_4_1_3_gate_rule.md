---
id: hq.research.arch_unit_oracle.simplification.matching.gate_rule
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: gate_rule
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_1_matching/node_0_3_2_4_1_3_gate_rule/CORE_0_3_2_4_1_3_gate_rule.md
super_node:
    name: matching
    path: ../CORE_0_3_2_4_1_matching.md
sub_nodes: []
---

# CORE 0_3_2_4_1_3 — gate_rule

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.matching.gate_rule
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

`gate_rule(E, i, j, t, u)`
- if `Term.normalize(t) == Term.normalize(u.term)`: IDENTICAL; else z3 at 3,000 ms: PROVED / DISPROVED / UNDECIDED. A rule is written only for IDENTICAL or PROVED, with its certificate.
