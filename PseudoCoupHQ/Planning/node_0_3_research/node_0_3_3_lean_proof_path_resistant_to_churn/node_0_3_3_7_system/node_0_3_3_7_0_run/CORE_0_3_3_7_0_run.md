---
id: hq.research.lean_proof_path_resistant_to_churn.system.run
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: run
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_7_system/node_0_3_3_7_0_run/CORE_0_3_3_7_0_run.md
super_node:
    name: system
    path: ../CORE_0_3_3_7_system.md
sub_nodes: []
---

# CORE 0_3_3_7_0 — run

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.system.run
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

`run(model, languages) -> Dictionary`

Steps, in order:

1. `defs = model.definitions()` — once per model commit; the cache is
   keyed by (model commit, sail commit) and misses on either changing
2. for every language, for every unit of its `compiler_corpus`:
   `unit.lean = unit.meaning(defs)`
3. `pass_a_find(defs, languages)` — fills the dictionary's found entries
   and every language's `operator_for`
4. `pass_b_build(defs, languages)` — renders from `operator_for`,
   compiles, reads meanings, writes the eye row and proves, row by row
5. `pass_c_units_across_languages(languages)`
6. return the dictionary

Every run writes its own directory: the definitions used, each
language's corpus and refusals, `operator_for.json`, the eye table, the
proofs, the dictionary. A rerun on a new compiler or a new model commit
writes a new directory; nothing is edited.
