---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.the_run
level: 6
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: the_run
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_8_the_run/CORE_0_3_2_3_1_3_8_the_run.md
super_node:
    name: lean_proof_path
    path: ../CORE_0_3_2_3_1_3_lean_proof_path.md
sub_nodes:
    - name: handful
      path: node_0_3_2_3_1_3_8_0_handful/CORE_0_3_2_3_1_3_8_0_handful.md
    - name: everything
      path: node_0_3_2_3_1_3_8_1_everything/CORE_0_3_2_3_1_3_8_1_everything.md
    - name: churn_tests
      path: node_0_3_2_3_1_3_8_2_churn_tests/CORE_0_3_2_3_1_3_8_2_churn_tests.md
    - name: speed_measured
      path: node_0_3_2_3_1_3_8_3_speed_measured/CORE_0_3_2_3_1_3_8_3_speed_measured.md
---

# CORE 0_3_2_3_1_3_8 — the_run

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.the_run
- **level:** 6
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path](../CORE_0_3_2_3_1_3_lean_proof_path.md)

## sub_nodes

- [handful](node_0_3_2_3_1_3_8_0_handful/CORE_0_3_2_3_1_3_8_0_handful.md) — Ten units and one model commit, to see the path working end to end before any population: the rv1 handful (log 258) of carved riscv64 units, `definitions()` from the cached emit of 2026-09-13 (or a fresh one), `meaning` on the ten, `equals` against their definitions, with `mulh` on c among them so that the integer-level normalization is tried where log 273 measured the wall.
- [everything](node_0_3_2_3_1_3_8_1_everything/CORE_0_3_2_3_1_3_8_1_everything.md) — Every arch-opcode the selected modules define, every language, passes A and B, one process, on the tower: the table "of N" per language beside log 273's union of routes (c 243, c++ 243, rust 247, go 243 of 255; 251 on some language, 235 on all four), every refusal by cause, and the speed measured per stage.
- [churn_tests](node_0_3_2_3_1_3_8_2_churn_tests/CORE_0_3_2_3_1_3_8_2_churn_tests.md) — The two tests the owner's criterion is: the regeneration test (delete the dictionary and the cached emit; run; both are back, byte-identical or the diff named) and the churn test (run again against a different compiler version, or a different model commit, and read what moved and why, with nobody editing anything in between).
- [speed_measured](node_0_3_2_3_1_3_8_3_speed_measured/CORE_0_3_2_3_1_3_8_3_speed_measured.md) — What the run costs per stage, measured, beside the expectations of log 274 §7.1: the emit once per commit (45 min, 17 GB, measured); `meaning` per unit; `equals` per pair by stage; a full pass A over 255 cells by four languages.

## definition

Running the system, in the owner's order: a handful first to see that it is
making sense, then everything, then the two tests that show it resists
churn. All compute on the tower through the lane protocol; the artifact
folder is `Research/oracle/riscv/leanpath/`.

- built: three lanes of increasing population, each reported with every
  table row "of N" and every refusal literal.
