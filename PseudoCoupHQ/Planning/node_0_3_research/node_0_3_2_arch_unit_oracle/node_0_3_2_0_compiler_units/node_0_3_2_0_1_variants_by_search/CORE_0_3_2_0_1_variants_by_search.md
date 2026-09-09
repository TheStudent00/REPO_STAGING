---
id: hq.research.arch_unit_oracle.compiler_units.variants_by_search
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: variants_by_search
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_0_compiler_units/node_0_3_2_0_1_variants_by_search/CORE_0_3_2_0_1_variants_by_search.md
super_node:
    name: compiler_units
    path: ../CORE_0_3_2_0_compiler_units.md
sub_nodes: []
---

# CORE 0_3_2_0_1 — variants_by_search

## metadata

- **id:** hq.research.arch_unit_oracle.compiler_units.variants_by_search
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

The operator VARIANTS (operator × written operand types) at every
lowered-operator site in a compiler's source, resolved by search
alone: `operator_variants_by_search.py`, importing operators_used's
walk, resolving each operand to a literal kind, a cast, an identifier
whose explicitly typed declaration is found in the same file, or a
nested operator whose operands resolve and agree; everything else
unresolved with one named reason. Task o4, log_210 (§7 the
nested-operand extension). Result: fully resolved 6–22% of sites per
row; the leftover is call results, member access, inferred bindings
and other-file declarations — the compiler's own type checker, which
search cannot replace. Done; the leftover is the typing question in
[research](../../../CORE_0_3_research.md) §5.
