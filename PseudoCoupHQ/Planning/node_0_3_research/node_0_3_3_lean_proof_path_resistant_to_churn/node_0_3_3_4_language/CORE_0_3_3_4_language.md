---
id: hq.research.lean_proof_path_resistant_to_churn.language
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: language
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_4_language/CORE_0_3_3_4_language.md
super_node:
    name: lean_proof_path_resistant_to_churn
    path: ../CORE_0_3_3_lean_proof_path_resistant_to_churn.md
sub_nodes:
    - name: compile
      path: node_0_3_3_4_0_compile/CORE_0_3_3_4_0_compile.md
    - name: compiler_corpus
      path: node_0_3_3_4_1_compiler_corpus/CORE_0_3_3_4_1_compiler_corpus.md
    - name: operator_for
      path: node_0_3_3_4_2_operator_for/CORE_0_3_3_4_2_operator_for.md
    - name: render
      path: node_0_3_3_4_3_render/CORE_0_3_3_4_3_render.md
    - name: compose_at_width
      path: node_0_3_3_4_4_compose_at_width/CORE_0_3_3_4_4_compose_at_width.md
---

# CORE 0_3_3_4 — language

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.language
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path_resistant_to_churn](../CORE_0_3_3_lean_proof_path_resistant_to_churn.md)

## sub_nodes

- [compile](node_0_3_3_4_0_compile/CORE_0_3_3_4_0_compile.md) — `compile(language, source, symbol) -> ArchUnit | Refusal`.
- [compiler_corpus](node_0_3_3_4_1_compiler_corpus/CORE_0_3_3_4_1_compiler_corpus.md) — `compiler_corpus : list[ArchUnit]`.
- [operator_for](node_0_3_3_4_2_operator_for/CORE_0_3_3_4_2_operator_for.md) — `operator_for : dict[(SailPrimitive, widths) -> list[ArchUnit]]`.
- [render](node_0_3_3_4_3_render/CORE_0_3_3_4_3_render.md) — `render(language, definition) -> source | Refusal`.
- [compose_at_width](node_0_3_3_4_4_compose_at_width/CORE_0_3_3_4_4_compose_at_width.md) — `compose_at_width(language, primitive, widths) -> source | None`.

## definition

One language the line covers: the line that invokes its compiler at
ship flags for riscv64 (plumbing), its `compiler_corpus` (EVERY
compiler-operator of the language, function-wrapped and lowered: the owner's
arch-units), and its swap table `operator_for`, which only
`System.pass_a_find`'s proofs fill. `render` writes an emulation from
`operator_for` and nothing else; where the table has no entry at the
definition's width, `compose_at_width` builds one from entries at the
language's widest word under a once-proved theorem, or refuses.

the owner, 2026-09-14, on the name: "id rather it say lang.compiler_corpus
... meaning the *corpus* is EVERY COMPILER-OPERATOR."

What a person writes, once, per language: the invocation line of its
compiler and the spelling of a function and a call in it (plumbing).
What is never written: which operator means which primitive. That is
`operator_for`, an output of a proof.

Churn: a new compiler version is a rerun; a new operator in the
language's grammar grows the probe set and is a rerun; nothing here is
edited for either.

The superseded node's `language` had the same shape and its code
drifted into a hand-written table (t4's renderer) in place of
`operator_for`; that code is retired by `the_run.retire_drifted_code`
and was not copied here.

## design

```
class Language
	attributes:
		name
		compiler            # the invocation at ship flags for riscv64: one line, plumbing
		compiler_corpus     # EVERY compiler-operator, function-wrapped and lowered: list[ArchUnit]
		operator_for        # dict[(SailPrimitive, widths) -> list[ArchUnit]]; filled by System.pass_a_find, never by hand
	methods:
		compile
		render
		compose_at_width
```
