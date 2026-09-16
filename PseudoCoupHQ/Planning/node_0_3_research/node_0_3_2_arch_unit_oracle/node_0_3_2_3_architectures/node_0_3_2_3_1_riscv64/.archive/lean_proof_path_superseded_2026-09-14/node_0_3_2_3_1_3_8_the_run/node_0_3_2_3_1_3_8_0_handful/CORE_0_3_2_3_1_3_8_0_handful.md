---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.the_run.handful
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: handful
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_8_the_run/node_0_3_2_3_1_3_8_0_handful/CORE_0_3_2_3_1_3_8_0_handful.md
super_node:
    name: the_run
    path: ../CORE_0_3_2_3_1_3_8_the_run.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_8_0 — handful

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.the_run.handful
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

Ten units and one model commit, to see the path working end to end
before any population: the rv1 handful (log 258) of carved riscv64
units, `definitions()` from the cached emit of 2026-09-13 (or a fresh
one), `meaning` on the ten, `equals` against their definitions, with
`mulh` on c among them so that the integer-level normalization is tried
where log 273 measured the wall.

- the report: ten rows, each with the stage reached, seconds, and the
  proof file or the refusal; the expected outcome is `ring` closing
  `mulh` without a circuit, and it is recorded as measured either way.
