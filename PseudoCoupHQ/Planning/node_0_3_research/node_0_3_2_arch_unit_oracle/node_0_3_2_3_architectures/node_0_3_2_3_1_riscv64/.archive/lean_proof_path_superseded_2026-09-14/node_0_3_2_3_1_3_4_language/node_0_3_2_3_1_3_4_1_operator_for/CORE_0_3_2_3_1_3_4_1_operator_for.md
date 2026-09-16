---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language.operator_for
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (attribute)
node:
    name: operator_for
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_4_language/node_0_3_2_3_1_3_4_1_operator_for/CORE_0_3_2_3_1_3_4_1_operator_for.md
super_node:
    name: language
    path: ../CORE_0_3_2_3_1_3_4_language.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_4_1 — operator_for

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language.operator_for
- **level:** 7
- **status:** draft
- **designation:** code (attribute)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [language](../CORE_0_3_2_3_1_3_4_language.md)

## sub_nodes

*(none yet)*

## definition

The swap table: for this language, the compiled unit that computes each
Sail primitive at each width, proved by pass A. the owner's
`lang_x_arch_unit_lean_primitives`. Filled by proof, never by hand; an
input to `render`, an output of `System.pass_a_find`.

- a missing entry at a width is what sends `render` to
  `compose_at_width`; it is never filled in by a guess.
