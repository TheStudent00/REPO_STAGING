---
id: hq.research.lean_proof_path_resistant_to_churn.system
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: system
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_7_system/CORE_0_3_3_7_system.md
super_node:
    name: lean_proof_path_resistant_to_churn
    path: ../CORE_0_3_3_lean_proof_path_resistant_to_churn.md
sub_nodes:
    - name: run
      path: node_0_3_3_7_0_run/CORE_0_3_3_7_0_run.md
    - name: pass_a_find
      path: node_0_3_3_7_1_pass_a_find/CORE_0_3_3_7_1_pass_a_find.md
    - name: pass_b_build
      path: node_0_3_3_7_2_pass_b_build/CORE_0_3_3_7_2_pass_b_build.md
    - name: eye_check
      path: node_0_3_3_7_3_eye_check/CORE_0_3_3_7_3_eye_check.md
    - name: pass_c_units_across_languages
      path: node_0_3_3_7_4_pass_c_units_across_languages/CORE_0_3_3_7_4_pass_c_units_across_languages.md
---

# CORE 0_3_3_7 — system

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.system
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path_resistant_to_churn](../CORE_0_3_3_lean_proof_path_resistant_to_churn.md)

## sub_nodes

- [run](node_0_3_3_7_0_run/CORE_0_3_3_7_0_run.md) — `run(model, languages) -> Dictionary`.
- [pass_a_find](node_0_3_3_7_1_pass_a_find/CORE_0_3_3_7_1_pass_a_find.md) — `pass_a_find(defs, languages)`.
- [pass_b_build](node_0_3_3_7_2_pass_b_build/CORE_0_3_3_7_2_pass_b_build.md) — `pass_b_build(defs, languages)`.
- [eye_check](node_0_3_3_7_3_eye_check/CORE_0_3_3_7_3_eye_check.md) — `eye_check(rows) -> table.md`.
- [pass_c_units_across_languages](node_0_3_3_7_4_pass_c_units_across_languages/CORE_0_3_3_7_4_pass_c_units_across_languages.md) — `pass_c_units_across_languages(languages)`.

## definition

the owner's three passes over the model and the languages, as one method
producing the dictionary, with the eye table he ordered on 2026-09-14:
written by every run, read by him on the handful before the whole run
starts, so a run is never a day in before a departure from the plan
shows. Every method here is a rule over its
inputs; none names an opcode, a compiler version or a language release.

```python
defs = model.definitions()                       # once per model commit
for lang in languages:
    for unit in lang.compiler_corpus:            # EVERY compiler-operator, function-wrapped and lowered
        unit.lean = unit.meaning(defs)           # Sail's decoder, Sail's definitions, chained
pass_a_find(defs, languages)                     # found entries; every operator_for, by proof
pass_b_build(defs, languages)                    # render from operator_for; compile; meaning; the eye row; the proof
pass_c_units_across_languages(languages)
```

The superseded node's `system` had the same passes; its run drifted:
pass A never filled `operator_for`, and pass B rendered from a
hand-written table. Neither was copied.

## design

```
class System
	attributes:
		model            # SailModel
		languages        # list[Language]
		dictionary       # Dictionary
	methods:
		run
		pass_a_find
		pass_b_build
		eye_check
		pass_c_units_across_languages
```
