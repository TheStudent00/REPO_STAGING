---
id: hq.research.interp_feeder.format_canon
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: code (function)
node:
    name: format_canon
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder/node_0_3_1_11_2_format_canon/CORE_0_3_1_11_2_format_canon.md
super_node:
    name: interp_feeder
    path: ../CORE_0_3_1_11_interp_feeder.md
sub_nodes: []
---

# CORE 0_3_1_11_2 — format_canon

## metadata

- **id:** hq.research.interp_feeder.format_canon
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

The mapping from a pilot's own dump schema onto the op_units record
the compiled probes have: `format_jvm(interp_data)` turns each dump
unit into a probe record with the operator label, the instruction
list (the last tab field of each objdump line), the bytes, and the
holder representations of the operands (`int32` → `i32`). One such
function per dump schema; java's is the one written. Everything
downstream reads the op_units shape and never the dump.
