---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language
level: 6
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: language
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_4_language/CORE_0_3_2_3_1_3_4_language.md
super_node:
    name: lean_proof_path
    path: ../CORE_0_3_2_3_1_3_lean_proof_path.md
sub_nodes:
    - name: compile
      path: node_0_3_2_3_1_3_4_0_compile/CORE_0_3_2_3_1_3_4_0_compile.md
    - name: operator_for
      path: node_0_3_2_3_1_3_4_1_operator_for/CORE_0_3_2_3_1_3_4_1_operator_for.md
    - name: render
      path: node_0_3_2_3_1_3_4_2_render/CORE_0_3_2_3_1_3_4_2_render.md
    - name: compose_at_width
      path: node_0_3_2_3_1_3_4_3_compose_at_width/CORE_0_3_2_3_1_3_4_3_compose_at_width.md
---

# CORE 0_3_2_3_1_3_4 — language

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.language
- **level:** 6
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path](../CORE_0_3_2_3_1_3_lean_proof_path.md)

## sub_nodes

- [compile](node_0_3_2_3_1_3_4_0_compile/CORE_0_3_2_3_1_3_4_0_compile.md) — `compile(language, source) -> ArchUnit`.
- [operator_for](node_0_3_2_3_1_3_4_1_operator_for/CORE_0_3_2_3_1_3_4_1_operator_for.md) — The swap table: for this language, the compiled unit that computes each Sail primitive at each width, proved by pass A.
- [render](node_0_3_2_3_1_3_4_2_render/CORE_0_3_2_3_1_3_4_2_render.md) — `render(language, definition) -> source`.
- [compose_at_width](node_0_3_2_3_1_3_4_3_compose_at_width/CORE_0_3_2_3_1_3_4_3_compose_at_width.md) — `compose_at_width(language, primitive, width) -> source fragment`.

## definition

One language PCHQ covers, with its compiler at ship flags, its corpus
of compiled units, and the swap table `operator_for` that pass A fills:
which of its own units computes each Sail primitive at each width. The
only thing written per language is how to invoke its compiler and cut a
body out, which is plumbing.

- built: from the census; the corpus is every unit the compiler
  produced for the census operators at the census type pairs.

## design

```
class Language
	attributes:
		name
		toolchain          # compiler command at ship flags, target riscv64
		corpus             # list of ArchUnit
		operator_for       # SailPrimitive -> ArchUnit, filled by pass A
	methods:
		compile
		render
		compose_at_width
```
