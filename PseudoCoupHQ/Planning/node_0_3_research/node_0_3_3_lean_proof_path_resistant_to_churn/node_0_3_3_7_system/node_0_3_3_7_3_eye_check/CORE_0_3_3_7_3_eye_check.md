---
id: hq.research.lean_proof_path_resistant_to_churn.system.eye_check
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: eye_check
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_7_system/node_0_3_3_7_3_eye_check/CORE_0_3_3_7_3_eye_check.md
super_node:
    name: system
    path: ../CORE_0_3_3_7_system.md
sub_nodes: []
---

# CORE 0_3_3_7_3 — eye_check

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.system.eye_check
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

`eye_check(rows) -> table.md`

the owner, 2026-09-14: "dont do all the proofs first. do the construction
first so that we theoretically have everything built out of the proven
pieces. we will prove things after we verify by eye that things look
right."

One row per (definition, language), with four columns side by side:

- D — Sail's definition of the arch-opcode, its Lean text
- E — the rendered source, and the names of the corpus units it was
  built from
- U — the compiled words, shown as instructions
- L — the meaning composed back through Sail's own decoder and
  definitions

What it is for (the owner, 2026-09-14, later the same evening): "check by
eye is just meant to make sure things look correct and give us an idea
of what to expect with the rest of the run so we dont get 24 hours into
a run only to find out that you havent followed the plan." So: every
run writes the table; the owner reads it on the handful, before `everything`
starts; it is not a gate on the proofs, which run right after the
meaning is read back. Written as a markdown table (raw blocks wrap;
markdown tables scroll) into the run's directory, and carried into a
DevComms log with the walkthrough first.
