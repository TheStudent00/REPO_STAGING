---
id: hq.research.arch_unit_oracle.cross_construction.single_opcode_units
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: single_opcode_units
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_2_single_opcode_units/CORE_0_3_2_2_2_single_opcode_units.md
super_node:
    name: cross_construction
    path: ../CORE_0_3_2_2_cross_construction.md
sub_nodes: []
---

# CORE 0_3_2_2_2 — single_opcode_units

## metadata

- **id:** hq.research.arch_unit_oracle.cross_construction.single_opcode_units
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

The two lists the owner asked for on 2026-09-05 as the precondition for
construction: per language, the compiler-operators that lower to a
single arch opcode (chaff = `ret` and plain register moves), and the
distinct arch opcodes across all of the language's arch-units.
`single_opcode_units.py`, `unique_opcodes.py` and their json/md under
`PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/` (folder
name provisional). Task o2, log_208. Result per compiled language:
c 20 of 27 operators, cpp 26 of 32, rust 14 of 21, go 10 of 20,
swift 12 of 26 have at least one single-opcode unit, most only on
some operand types, comparisons never; 60–130 distinct opcodes per
language. This is the measurement that froze the super-node: one
language's single-opcode units cannot build another's. The
interpreted languages' rows count only their eleven carved units and
say nothing about those languages. Done.
