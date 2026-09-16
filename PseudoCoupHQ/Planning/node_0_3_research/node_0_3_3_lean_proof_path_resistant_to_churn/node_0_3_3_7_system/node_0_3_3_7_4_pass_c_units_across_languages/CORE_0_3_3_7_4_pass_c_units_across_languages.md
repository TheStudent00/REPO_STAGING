---
id: hq.research.lean_proof_path_resistant_to_churn.system.pass_c_units_across_languages
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: pass_c_units_across_languages
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_7_system/node_0_3_3_7_4_pass_c_units_across_languages/CORE_0_3_3_7_4_pass_c_units_across_languages.md
super_node:
    name: system
    path: ../CORE_0_3_3_7_system.md
sub_nodes: []
---

# CORE 0_3_3_7_4 — pass_c_units_across_languages

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.system.pass_c_units_across_languages
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

`pass_c_units_across_languages(languages)`

The Hub's claim: a unit of one language against the units of another.

Steps, in order:

1. for every pair of languages, for every unit of the first's
   `compiler_corpus`, for every unit of the second's: if
   `LeanExpr.equals(unit_i.lean, unit_j.lean)` proves, record the pair
2. the same candidate filter as pass A (evaluation at sample inputs)
   keeps the pair count down; the proof is the only thing that adds
3. the result is the owner's last loop of 2026-09-13: every language's
   operators expressed in every other's, with a proof on each edge
