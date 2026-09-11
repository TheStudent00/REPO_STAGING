---
id: hq.research.arch_unit_oracle.simplification.synthesis
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: synthesis
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_3_synthesis/CORE_0_3_2_4_3_synthesis.md
super_node:
    name: simplification
    path: ../CORE_0_3_2_4_simplification.md
sub_nodes:
    - name: components
      path: node_0_3_2_4_3_0_components/CORE_0_3_2_4_3_0_components.md
    - name: cegis
      path: node_0_3_2_4_3_1_cegis/CORE_0_3_2_4_3_1_cegis.md
    - name: bound_table
      path: node_0_3_2_4_3_2_bound_table/CORE_0_3_2_4_3_2_bound_table.md
---

# CORE 0_3_2_4_3 — synthesis

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.synthesis
- **level:** 4
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [simplification](../CORE_0_3_2_4_simplification.md)

## sub_nodes

- [components](node_0_3_2_4_3_0_components/CORE_0_3_2_4_3_0_components.md) — `Components` - each unit as a component: its term, arity, widths, and the places it writes; the wiring variables z3 chooses over.
- [cegis](node_0_3_2_4_3_1_cegis/CORE_0_3_2_4_3_1_cegis.md) — `cegis(term, components, k, budget) -> wiring | None` - the counterexample-guided loop: propose a wiring on the points so far, verify for all inputs, add the counterexample, repeat; Gulwani's 2011 shape.
- [bound_table](node_0_3_2_4_3_2_bound_table/CORE_0_3_2_4_3_2_bound_table.md) — `bound_table(E, k_max, residue)` - per cell and language: the k at which it closed, or the residue at the budget, LITERAL; the measured boundary of completeness.

## definition

Task rm2: component-based synthesis. Ask z3 for a wiring of at most k
units equal to the whole term for every input; raise k until it
answers. Complete for straight-line, loop-free, memory-free bodies at
each k; exponential in k.

```
for k in 1, 2, 3, ... k_max:
    wiring = cegis(term_of(E), components(units_of(lang)), k, budget)
    if wiring: return wiring            # provably the shortest at or below k
bound_table.record(E, k_max, residue)   # what closed at which k, what did not
```
