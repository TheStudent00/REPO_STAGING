---
id: hq.research.arch_unit_oracle.hub_compiler.front_end
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: front_end
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_1_hub_compiler/node_0_3_2_1_0_front_end/CORE_0_3_2_1_0_front_end.md
super_node:
    name: hub_compiler
    path: ../CORE_0_3_2_1_hub_compiler.md
sub_nodes: []
---

# CORE 0_3_2_1_0 — front_end

## metadata

- **id:** hq.research.arch_unit_oracle.hub_compiler.front_end
- **level:** 4
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [hub_compiler](../CORE_0_3_2_1_hub_compiler.md)

## sub_nodes

*(none yet)*

## definition

The reader of the file to be lowered: tree-sitter parses it; the
tree's nesting is the data flow (a sub-node's value is an operand of
its super-node); at each operator node the front end must also know
the operand TYPES, which the tree does not carry. the owner's ruling
2026-09-05: tree-sitter, with the ledgerer (PCv5 `ts_to_ur`,
`ur_to_ledger`) where it applies. The typing route is the open
ruling in [research](../../../CORE_0_3_research.md) §5; task o4
measured what search alone gives. Not started.
