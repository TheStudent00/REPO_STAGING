---
id: hq.research.arch_unit_oracle.hub_compiler.joiner
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: joiner
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_1_hub_compiler/node_0_3_2_1_2_joiner/CORE_0_3_2_1_2_joiner.md
super_node:
    name: hub_compiler
    path: ../CORE_0_3_2_1_hub_compiler.md
sub_nodes: []
---

# CORE 0_3_2_1_2 — joiner

## metadata

- **id:** hq.research.arch_unit_oracle.hub_compiler.joiner
- **level:** 4
- **status:** draft
- **designation:** code (function)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [hub_compiler](../CORE_0_3_2_1_hub_compiler.md)

## sub_nodes

*(none yet)*

## definition

The emitter of the row traffic between entries: a post-order walk of
the tree in which a sub-node's entry stores its answer into a memory
row (the canonical form's epilogue) and the super-node's entry loads
that row as an operand (its prelude); one row per tree edge; the
prelude and epilogue are the canonical form's own
([canonical_form](../../../node_0_3_1_operator_equivalence/node_0_3_1_2_canonical_form/CORE_0_3_1_2_canonical_form.md)).
The join is the same on every edge, which is what makes the lowering
a map over operator nodes. Not started.
