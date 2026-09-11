---
id: hq.research.arch_unit_oracle.simplification.guarantees
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: rule
node:
    name: guarantees
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_6_guarantees/CORE_0_3_2_4_6_guarantees.md
super_node:
    name: simplification
    path: ../CORE_0_3_2_4_simplification.md
sub_nodes: []
---

# CORE 0_3_2_4_6 — guarantees

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.guarantees
- **level:** 4
- **status:** draft
- **designation:** rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [simplification](../CORE_0_3_2_4_simplification.md)

## sub_nodes

*(none yet)*

## definition

What each number in this node is allowed to claim. A result is
reported with its guarantee named, never as a bare count.

- matching: SOUND. Every rule is true. Nothing is said about rules not found.
- equality saturation: COMPLETE OVER THE RULE SET. Every form the rules
  generate is reached; forms outside the rules' span are not.
- synthesis: SHORTEST AT BOUND k. At each k, either a wiring is found or
  none exists at k; nothing is said beyond k_max.
- learned proposal: NO GUARANTEE OF ITS OWN. It orders candidates; z3's
  verdict is the only acceptance.
- the backstop: EXISTENCE. Every term is reachable by some combination,
  because the units include the gates.
