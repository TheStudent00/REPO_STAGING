---
id: hq.research.lean_proof_path_resistant_to_churn.the_run.churn_tests
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: churn_tests
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_8_the_run/node_0_3_3_8_2_churn_tests/CORE_0_3_3_8_2_churn_tests.md
super_node:
    name: the_run
    path: ../CORE_0_3_3_8_the_run.md
sub_nodes: []
---

# CORE 0_3_3_8_2 — churn_tests

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.the_run.churn_tests
- **level:** 4
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [the_run](../CORE_0_3_3_8_the_run.md)

## sub_nodes

*(none yet)*

## definition

The two reruns and the one mechanical check that show nothing here is
hand-written for an opcode, a compiler or a language release:

1. a second compiler version for one language: rerun; nothing edited;
   the two dictionaries diffed, the difference explained by the
   compiler's changed output only
2. a second model commit: rerun; the cache misses, `definitions()`
   re-emits, everything downstream regenerates; nothing edited
3. the mechanical check, run on every commit of the module: the
   spelling-ban checker
   `PRIVATE/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py`
   over every file the run writes, and a grep of the module's code for a
   mnemonic, a compiler version string or a language release — zero
   hits, except the one invocation line per language in
   `Language.compile`
