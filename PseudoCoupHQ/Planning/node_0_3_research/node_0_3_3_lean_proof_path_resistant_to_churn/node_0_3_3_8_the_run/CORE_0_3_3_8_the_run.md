---
id: hq.research.lean_proof_path_resistant_to_churn.the_run
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: the_run
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_8_the_run/CORE_0_3_3_8_the_run.md
super_node:
    name: lean_proof_path_resistant_to_churn
    path: ../CORE_0_3_3_lean_proof_path_resistant_to_churn.md
sub_nodes:
    - name: handful
      path: node_0_3_3_8_0_handful/CORE_0_3_3_8_0_handful.md
    - name: everything
      path: node_0_3_3_8_1_everything/CORE_0_3_3_8_1_everything.md
    - name: churn_tests
      path: node_0_3_3_8_2_churn_tests/CORE_0_3_3_8_2_churn_tests.md
    - name: speed_measured
      path: node_0_3_3_8_3_speed_measured/CORE_0_3_3_8_3_speed_measured.md
    - name: retire_drifted_code
      path: node_0_3_3_8_4_retire_drifted_code/CORE_0_3_3_8_4_retire_drifted_code.md
---

# CORE 0_3_3_8 — the_run

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.the_run
- **level:** 3
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path_resistant_to_churn](../CORE_0_3_3_lean_proof_path_resistant_to_churn.md)

## sub_nodes

- [handful](node_0_3_3_8_0_handful/CORE_0_3_3_8_0_handful.md) — The smallest run that exercises every method once:.
- [everything](node_0_3_3_8_1_everything/CORE_0_3_3_8_1_everything.md) — The whole run:.
- [churn_tests](node_0_3_3_8_2_churn_tests/CORE_0_3_3_8_2_churn_tests.md) — The two reruns and the one mechanical check that show nothing here is hand-written for an opcode, a compiler or a language release:.
- [speed_measured](node_0_3_3_8_3_speed_measured/CORE_0_3_3_8_3_speed_measured.md) — Wall time, measured, per language and per pass: the corpus compile, the meanings (Lean's decode per shard), pass A's proofs, pass B's render and proofs.
- [retire_drifted_code](node_0_3_3_8_4_retire_drifted_code/CORE_0_3_3_8_4_retire_drifted_code.md) — What the superseded run built on a hand-written table, archived with the reason, never reused.

## definition

Running the system, in the owner's order (2026-09-13): a handful first to see
that it is making sense, then everything; with the eye check before the
proofs (2026-09-14); then the churn tests and the speed measured. And
first of all, the retirement of the code that drifted.

The superseded node's `the_run` ran over printed emulations instead of
the compiler corpora and its churn tests never ran; nothing of it was
copied.
