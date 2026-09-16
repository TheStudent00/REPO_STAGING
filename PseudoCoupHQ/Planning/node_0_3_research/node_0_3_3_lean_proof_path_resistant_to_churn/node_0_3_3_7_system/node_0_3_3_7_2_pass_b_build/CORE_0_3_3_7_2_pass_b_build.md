---
id: hq.research.lean_proof_path_resistant_to_churn.system.pass_b_build
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: pass_b_build
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_7_system/node_0_3_3_7_2_pass_b_build/CORE_0_3_3_7_2_pass_b_build.md
super_node:
    name: system
    path: ../CORE_0_3_3_7_system.md
sub_nodes: []
---

# CORE 0_3_3_7_2 — pass_b_build

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.system.pass_b_build
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

`pass_b_build(defs, languages)`

Steps, in order:

1. for every definition, for every language: skip when the dictionary
   already holds (language, definition)
2. `source = language.render(definition)`; a refusal is a row naming the
   primitive and widths
3. `unit = language.compile(source)`; a refusal is a row with the
   compiler's line
4. `unit.lean = unit.meaning(defs)`; a refusal is a row with the
   construct named (a branch shape, a call, a word Sail's decoder gives
   no constructor for)
5. `eye_check.row(definition, language, source, unit)` — the row is
   written whatever happens next
6. if `LeanExpr.equals(definition, unit.lean)` proves, add
   `Emulation(op, lang, unit, proof)` marked built; else a row

Nothing here chooses; `render` reads `operator_for`, the compiler
lowers, Sail reads it back, Lean decides.
