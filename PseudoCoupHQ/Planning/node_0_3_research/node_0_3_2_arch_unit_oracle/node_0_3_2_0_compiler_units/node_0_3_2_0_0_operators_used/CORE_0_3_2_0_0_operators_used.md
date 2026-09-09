---
id: hq.research.arch_unit_oracle.compiler_units.operators_used
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: operators_used
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_0_compiler_units/node_0_3_2_0_0_operators_used/CORE_0_3_2_0_0_operators_used.md
super_node:
    name: compiler_units
    path: ../CORE_0_3_2_0_compiler_units.md
sub_nodes: []
---

# CORE 0_3_2_0_0 — operators_used

## metadata

- **id:** hq.research.arch_unit_oracle.compiler_units.operators_used
- **level:** 4
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [compiler_units](../CORE_0_3_2_0_compiler_units.md)

## sub_nodes

*(none yet)*

## definition

The census of which grammar operators OCCUR in a compiler's own
source, set against the operators the language offers and the subset
the corpus has lowered: `compiler_operators_used.py` under
`PseudoCoupHQ/Research/oracle/compiler_units/`, a
tree-sitter walk over every source file counting operator nodes
(strings and comments excluded), measured against the inventory of
the language the compiler is WRITTEN in. Task o3, log_209; six rows
(clang/llvm, go compiler, go stdlib, rustc, swiftc, swift stdlib).
Finding: every compiler uses essentially every scalar operator the
corpus lowered; the gap runs the other way (assignment, member, cast
operators used and never lowered). Sparse checkouts for llvm and
rust are reported as sparse in the row. Done.
