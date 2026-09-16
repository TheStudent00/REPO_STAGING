---
id: hq.research.lean_proof_path_resistant_to_churn.the_run.retire_drifted_code
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: retire_drifted_code
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_8_the_run/node_0_3_3_8_4_retire_drifted_code/CORE_0_3_3_8_4_retire_drifted_code.md
super_node:
    name: the_run
    path: ../CORE_0_3_3_8_the_run.md
sub_nodes: []
---

# CORE 0_3_3_8_4 — retire_drifted_code

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.the_run.retire_drifted_code
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

What the superseded run built on a hand-written table, archived with
the reason, never reused. Nothing is deleted; each goes under an
`.archive/` beside where it lived, with a one-line file saying why.

| what | where | why it is retired |
|---|---|---|
| `construct.py`, `propose_all.py`, `construct_table.py`, the `construct` command | `Research/oracle/riscv/leanpath/leanpath/` | rendered emulations through t4's `render_general.py`, a hand-written table from term nodes to operators, in place of `operator_for` |
| `construct_all/` and lane `lp3_l48_construct_lower_and_compose.sh` | `Research/oracle/riscv/leanpath/` | the 1,040 emulations and their walk, built on that table |
| the z3 evaluation half of `lean_to_z3.py` | same | z3 was only the old renderer's input form; the parser half is kept for `render` |

Kept, because they were right: `strip.py` (definitions), `walk.py`
(compile, carve, decode, compose, the meanings), `equals.py` (the Lean
proofs).
