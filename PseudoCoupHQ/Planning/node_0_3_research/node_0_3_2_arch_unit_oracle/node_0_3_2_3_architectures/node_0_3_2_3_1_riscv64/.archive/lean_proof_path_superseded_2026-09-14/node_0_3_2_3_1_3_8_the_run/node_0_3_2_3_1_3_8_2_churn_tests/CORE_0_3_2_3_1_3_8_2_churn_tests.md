---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.the_run.churn_tests
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: churn_tests
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_8_the_run/node_0_3_2_3_1_3_8_2_churn_tests/CORE_0_3_2_3_1_3_8_2_churn_tests.md
super_node:
    name: the_run
    path: ../CORE_0_3_2_3_1_3_8_the_run.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_8_2 — churn_tests

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.the_run.churn_tests
- **level:** 7
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [the_run](../CORE_0_3_2_3_1_3_8_the_run.md)

## sub_nodes

*(none yet)*

## definition

The two tests the owner's criterion is: the regeneration test (delete the
dictionary and the cached emit; run; both are back, byte-identical or
the diff named) and the churn test (run again against a different
compiler version, or a different model commit, and read what moved and
why, with nobody editing anything in between).

- a person editing any row anywhere in the path fails both.
