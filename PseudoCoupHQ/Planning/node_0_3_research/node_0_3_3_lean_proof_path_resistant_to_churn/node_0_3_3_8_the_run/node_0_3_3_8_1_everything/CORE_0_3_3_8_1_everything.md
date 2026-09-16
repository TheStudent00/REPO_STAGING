---
id: hq.research.lean_proof_path_resistant_to_churn.the_run.everything
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: everything
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_8_the_run/node_0_3_3_8_1_everything/CORE_0_3_3_8_1_everything.md
super_node:
    name: the_run
    path: ../CORE_0_3_3_8_the_run.md
sub_nodes: []
---

# CORE 0_3_3_8_1 — everything

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.the_run.everything
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

The whole run:

1. the four languages' corpora (c and go are lowered for riscv64 already;
   cpp and rust through the same route)
2. pass A over all four: `operator_for` per language
3. pass B over every readable definition (50 kinds as of 2026-09-14; the
   readers for vector loops, floats, control registers and atomics are
   `sail_model.strip`'s open items and grow the count without touching
   anything here)
4. the eye table, then the proofs
5. the report: per language, per arch-opcode, per arch-unit, with
   populations, in a DevComms log
