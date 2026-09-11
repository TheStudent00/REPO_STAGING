---
id: hq.research.arch_unit_oracle.simplification.synthesis.cegis
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: cegis
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_3_synthesis/node_0_3_2_4_3_1_cegis/CORE_0_3_2_4_3_1_cegis.md
super_node:
    name: synthesis
    path: ../CORE_0_3_2_4_3_synthesis.md
sub_nodes: []
---

# CORE 0_3_2_4_3_1 — cegis

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.synthesis.cegis
- **level:** 5
- **status:** draft
- **designation:** code (function)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [synthesis](../CORE_0_3_2_4_3_synthesis.md)

## sub_nodes

*(none yet)*

## definition

`cegis(term, components, k, budget) -> wiring | None`
- the counterexample-guided loop: propose a wiring on the points so far, verify for all inputs, add the counterexample, repeat; Gulwani's 2011 shape.
