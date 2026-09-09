---
id: hq.research.arch_unit_oracle.compiler_units
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: compiler_units
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_0_compiler_units/CORE_0_3_2_0_compiler_units.md
super_node:
    name: arch_unit_oracle
    path: ../CORE_0_3_2_arch_unit_oracle.md
sub_nodes:
    - name: operators_used
      path: node_0_3_2_0_0_operators_used/CORE_0_3_2_0_0_operators_used.md
    - name: variants_by_search
      path: node_0_3_2_0_1_variants_by_search/CORE_0_3_2_0_1_variants_by_search.md
    - name: lowering_route_cut
      path: node_0_3_2_0_2_lowering_route_cut/CORE_0_3_2_0_2_lowering_route_cut.md
---

# CORE 0_3_2_0 — compiler_units

## metadata

- **id:** hq.research.arch_unit_oracle.compiler_units
- **level:** 3
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit_oracle](../CORE_0_3_2_arch_unit_oracle.md)

## sub_nodes

- [operators_used](node_0_3_2_0_0_operators_used/CORE_0_3_2_0_0_operators_used.md) — The census of which grammar operators OCCUR in a compiler's own source, set against the operators the language offers and the subset the corpus has lowered: `compiler_operators_used.py` under `~/Programming/PseudoCoupHQ/Research/oracle/compiler_units/`, a tree-sitter walk over every source file counting operator nodes (strings and comments excluded), measured against the inventory of the language the compiler is WRITTEN in.
- [variants_by_search](node_0_3_2_0_1_variants_by_search/CORE_0_3_2_0_1_variants_by_search.md) — The operator VARIANTS (operator × written operand types) at every lowered-operator site in a compiler's source, resolved by search alone: `operator_variants_by_search.py`, importing operators_used's walk, resolving each operand to a literal kind, a cast, an identifier whose explicitly typed declaration is found in the same file, or a nested operator whose operands resolve and agree; everything else unresolved with one named reason.
- [lowering_route_cut](node_0_3_2_0_2_lowering_route_cut/CORE_0_3_2_0_2_lowering_route_cut.md) — Step 1 of the master order: the variant records of variants_by_search cut to the LOWERING ROUTE — the emitter definitions task 95 found (57 in go, 251 in clang, `arch-opcode-nodes`, log_200) and the functions task 81's diaries recorded per operator probe — so the operators a compiler's routing uses are counted apart from its whole source.

## definition

The operators a compiler's OWN SOURCE uses, each taken as an
arch-unit, set against the operators that compiler OFFERS to the
programs it compiles — the existing corpus — so that the difference
between what a compiler offers and what it uses is measured.

Corrected by the owner, 2026-09-05, verbatim: "im interested in the
compiler-operators used by the compiler. as opposed to taking entire
compiler functions and extracting the entire lowered form of that
function. it is something we can explore also but the objective im
looking for the operators used in the compiler. one of the reasons
is that im looking to see the difference between what the compiler
offers in operators (the original arch-unit research that has formed
a corpus of results already) and what operators the compiler itself
uses."

## the two populations, named

- **Offered:** the arch-units of the main line's corpus — 31,078
  units over nine languages as of 2026-09-05, one per (operator,
  operand types) the language exposes, generated as probes and
  compiled by that language's compiler.
- **Used:** every operator SITE in the compiler's own source, with
  the operand types at that site, taken as an arch-unit — the
  machine code that compiler's build emits for that operator on
  those types.

## how a used site becomes an arch-unit, without slicing a function

- The compiler's source is already parsed: the compiler graph
  (`~/Programming/PseudoCoupGraphs`) holds tree-sitter nodes for go
  and clang's source, rust and swift structurally. An operator site
  is a tree-sitter node of an operator kind with its operand nodes;
  the operand types come from the declarations the graph's read
  edges reach.
- The unit for a site is produced the way every unit is produced:
  a generated probe of that (operator, operand types), compiled by
  the compiler that compiles the compiler, carved by the
  function-body rule. No function of the compiler is sliced; the
  site tells us WHICH probe to make.
- A site whose (operator, operand types) the probe corpus already
  covers maps to an existing unit and its pool entry. A site it does
  not cover is a new probe — and each such site is a finding in
  itself: an operator the compiler uses that its offered corpus
  did not include.

## the spelling ban, applied here

The offered-versus-used comparison is made through the POOL: a used
site maps to its unit, the unit to its pool entry, and two sites are
the same computation only if they land in the same entry. The
operator token is carried as a label on the site and never keys the
comparison.

## whole-function lowering, kept as a later option

Taking an entire compiler function and extracting its lowered form
is a second study the owner named as possible. It is not this sub-node's
objective and is not started; if opened it becomes its own sub-node.

## artifacts

`~/Programming/PseudoCoupHQ/Research/oracle/compiler_units/`. Reads
`Research/op_pipeline/` and `~/Programming/PseudoCoupGraphs/`; writes
neither.
