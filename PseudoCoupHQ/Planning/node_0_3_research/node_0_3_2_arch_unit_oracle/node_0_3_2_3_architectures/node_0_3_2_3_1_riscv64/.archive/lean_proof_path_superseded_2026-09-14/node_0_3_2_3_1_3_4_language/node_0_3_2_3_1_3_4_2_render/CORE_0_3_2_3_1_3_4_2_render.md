---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language.render
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: render
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_4_language/node_0_3_2_3_1_3_4_2_render/CORE_0_3_2_3_1_3_4_2_render.md
super_node:
    name: language
    path: ../CORE_0_3_2_3_1_3_4_language.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_4_2 — render

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language.render
- **level:** 7
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [language](../CORE_0_3_2_3_1_3_4_language.md)

## sub_nodes

*(none yet)*

## definition

`render(language, definition) -> source`

Input: an arch-opcode's definition as a `LeanExpr`. Output: source text in this language whose compiled body should compute it.

Steps, in order:

1. walk the definition's expression
2. at each primitive at width w, write the operator that `operator_for[(primitive, w)]` holds, in the language's own spelling from that unit's source
3. where no entry exists, call `compose_at_width` for that primitive
4. wrap the two guards of a definition (`if` cases) as the language's conditional, so that a trapping branch is a branch (the guarded render of log 268)
5. return the source; the source is one candidate, never a search
