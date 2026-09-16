---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.system
level: 6
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: system
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_7_system/CORE_0_3_2_3_1_3_7_system.md
super_node:
    name: lean_proof_path
    path: ../CORE_0_3_2_3_1_3_lean_proof_path.md
sub_nodes:
    - name: run
      path: node_0_3_2_3_1_3_7_0_run/CORE_0_3_2_3_1_3_7_0_run.md
    - name: pass_a_find
      path: node_0_3_2_3_1_3_7_1_pass_a_find/CORE_0_3_2_3_1_3_7_1_pass_a_find.md
    - name: pass_b_build
      path: node_0_3_2_3_1_3_7_2_pass_b_build/CORE_0_3_2_3_1_3_7_2_pass_b_build.md
    - name: pass_c_units_across_languages
      path: node_0_3_2_3_1_3_7_3_pass_c_units_across_languages/CORE_0_3_2_3_1_3_7_3_pass_c_units_across_languages.md
---

# CORE 0_3_2_3_1_3_7 — system

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.system
- **level:** 6
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path](../CORE_0_3_2_3_1_3_lean_proof_path.md)

## sub_nodes

- [run](node_0_3_2_3_1_3_7_0_run/CORE_0_3_2_3_1_3_7_0_run.md) — `run(model, langs) -> Dictionary`.
- [pass_a_find](node_0_3_2_3_1_3_7_1_pass_a_find/CORE_0_3_2_3_1_3_7_1_pass_a_find.md) — `pass_a_find(defs, langs, dictionary)`.
- [pass_b_build](node_0_3_2_3_1_3_7_2_pass_b_build/CORE_0_3_2_3_1_3_7_2_pass_b_build.md) — `pass_b_build(defs, langs, dictionary)`.
- [pass_c_units_across_languages](node_0_3_2_3_1_3_7_3_pass_c_units_across_languages/CORE_0_3_2_3_1_3_7_3_pass_c_units_across_languages.md) — `pass_c_units_across_languages(langs, dictionary)`.

## definition

The three passes over the model and the languages, in one method,
producing the dictionary; the loop the owner wrote on 2026-09-13, as code.
Nothing in it names an opcode; the population is every definition the
model gives and every unit the compilers gave.

- built: `run`, calling the three passes in order; each pass is its own
  method so a pass can be re-run alone.

## design

```
class System
	attributes:
		model
		langs
		dictionary
	methods:
		run
		pass_a_find
		pass_b_build
		pass_c_units_across_languages
```
