---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language.compose_at_width
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: compose_at_width
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_4_language/node_0_3_2_3_1_3_4_3_compose_at_width/CORE_0_3_2_3_1_3_4_3_compose_at_width.md
super_node:
    name: language
    path: ../CORE_0_3_2_3_1_3_4_language.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_4_3 — compose_at_width

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language.compose_at_width
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

`compose_at_width(language, primitive, width) -> source fragment`

Input: a primitive the language has no operator for at this width. Output: the same function built from the language's operators at narrower widths.

Steps, in order:

1. pick the widest width w' < w the language has for this primitive kind
2. instantiate the construction for the kind (schoolbook product, shift-and-subtract quotient, add with carry) from w' pieces
3. return the fragment; the theorem that justifies it is the once-proved one for that kind, instantiated by `LeanExpr.equals`

Expected unused for our five compiled languages on rv64 (log 274 §5.4); present so that a language without a full-width product is still covered.
