---
id: hq.research.lean_proof_path_resistant_to_churn.system.pass_a_find
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: pass_a_find
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_7_system/node_0_3_3_7_1_pass_a_find/CORE_0_3_3_7_1_pass_a_find.md
super_node:
    name: system
    path: ../CORE_0_3_3_7_system.md
sub_nodes: []
---

# CORE 0_3_3_7_1 — pass_a_find

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.system.pass_a_find
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [system](../CORE_0_3_3_7_system.md)

## sub_nodes

*(none yet)*

## definition

`pass_a_find(defs, languages)`

Input: the definitions; the languages, whose corpus units carry
meanings. Output: dictionary entries marked found; every language's
`operator_for`.

Steps, in order:

1. for every language, for every unit of `compiler_corpus`, for every
   definition: if `LeanExpr.equals(definition, unit.lean)` proves, add an
   `Emulation(op, lang, unit, proof)` marked found
2. for every language, for every unit, for every primitive with widths
   over all definitions (`LeanExpr.primitives`): if
   `LeanExpr.equals(primitive(unknowns), unit.lean)` proves, append the
   unit to `lang.operator_for[(primitive, widths)]`
3. record every Differ and Undecided as a row with its stage

Cost: pairs are filtered first by `equals`'s evaluation at sample
inputs, which only removes candidates and never adds one; the proof is
the only thing that adds. Measured 2026-09-14 on the earlier run over the 1,960 lowered
emulations of log 278 (not this node's set, not arch-units): 1,209
certified, 846 proof attempts, 114 equal. On this node's set (c's
compiler corpus, lane l53, 2026-09-15): see PROGRESS.

This is "whoever gets there first" by proof over what the compiler
already emitted, with no render. `operator_for` is its output, an input
to nothing a person fills.
