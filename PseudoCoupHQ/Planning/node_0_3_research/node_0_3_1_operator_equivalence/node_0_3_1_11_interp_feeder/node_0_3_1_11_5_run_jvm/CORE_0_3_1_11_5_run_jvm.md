---
id: hq.research.interp_feeder.run_jvm
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: work
node:
    name: run_jvm
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder/node_0_3_1_11_5_run_jvm/CORE_0_3_1_11_5_run_jvm.md
super_node:
    name: interp_feeder
    path: ../CORE_0_3_1_11_interp_feeder.md
sub_nodes: []
---

# CORE 0_3_1_11_5 — run_jvm

## metadata

- **id:** hq.research.interp_feeder.run_jvm
- **level:** 4
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [interp_feeder](../CORE_0_3_1_11_interp_feeder.md)

## sub_nodes

*(none yet)*

## definition

The java route, the one where the unit does not exist in any binary
until run time: the probe method is warmed until HotSpot's C2 tier
compiles it, the emitted machine code is dumped, and the method's
body is carved as the unit. Two java units exist (`java/op_1` for
`+`, `java/op_2` for `/`); both are refused by the canonical form at
the seventh block kind because their frames reach 0x538 past the
0x100 `AREA_SPAN` of the own-address block (the owner's ruling pending,
log_204 §4.4). Kotlin will use this route after `kotlinc`.
