---
id: hq.research.arch_unit_oracle.cross_construction.length_two
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: length_two
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_1_length_two/CORE_0_3_2_2_1_length_two.md
super_node:
    name: cross_construction
    path: ../CORE_0_3_2_2_cross_construction.md
sub_nodes: []
---

# CORE 0_3_2_2_1 — length_two

## metadata

- **id:** hq.research.arch_unit_oracle.cross_construction.length_two
- **level:** 4
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [cross_construction](../CORE_0_3_2_2_cross_construction.md)

## sub_nodes

*(none yet)*

## definition

The depth-2 composition search at the term level: y's layer-5 term
matched at the root against x's terms with variables as holes, each
hole bound to a variable, a literal, or another x term whose holes
bind only to variables or literals. `cross2_length_two.py`, with its
own parser of the layer-5 print form (round-trip checked over 1,267
distinct texts; 22 fail on one cause, the `*` spacing ambiguity,
excluded not patched). Task o1, log_207: under 3.1% of the entries
length one missed, in any cell. No gate proof was run. Done; frozen.
