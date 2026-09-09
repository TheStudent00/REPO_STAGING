---
id: hq.research.interp_feeder.parse_interp
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: code (function)
node:
    name: parse_interp
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder/node_0_3_1_11_1_parse_interp/CORE_0_3_1_11_1_parse_interp.md
super_node:
    name: interp_feeder
    path: ../CORE_0_3_1_11_interp_feeder.md
sub_nodes: []
---

# CORE 0_3_1_11_1 — parse_interp

## metadata

- **id:** hq.research.interp_feeder.parse_interp
- **level:** 4
- **status:** draft
- **designation:** code (function)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [interp_feeder](../CORE_0_3_1_11_interp_feeder.md)

## sub_nodes

*(none yet)*

## definition

The reader of one interpreter pilot's dump: `parse_interp_log(path)`
loads the JSON an interpreter or JIT pilot wrote (for java,
`interp_jvm.json`: per unit an id, a label, the objdump lines and hex
bytes of the emitted code, and the operand types the pilot probed).
It reads; it interprets nothing. What each pilot writes is that
pilot's own schema, which is why the next step exists.
