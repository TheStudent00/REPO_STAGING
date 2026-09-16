---
id: hq.research.lean_proof_path_resistant_to_churn.sail_model
level: 3
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model
designation: code (class)
node:
    name: sail_model
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_0_sail_model/CORE_0_3_3_0_sail_model.md
super_node:
    name: lean_proof_path_resistant_to_churn
    path: ../CORE_0_3_3_lean_proof_path_resistant_to_churn.md
sub_nodes:
    - name: definitions
      path: node_0_3_3_0_0_definitions/CORE_0_3_3_0_0_definitions.md
    - name: key_of
      path: node_0_3_3_0_1_key_of/CORE_0_3_3_0_1_key_of.md
    - name: strip
      path: node_0_3_3_0_2_strip/CORE_0_3_3_0_2_strip.md
    - name: emit_lane
      path: node_0_3_3_0_3_emit_lane/CORE_0_3_3_0_3_emit_lane.md
---

# CORE 0_3_3_0 — sail_model

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.sail_model
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model

## super_node

- [lean_proof_path_resistant_to_churn](../CORE_0_3_3_lean_proof_path_resistant_to_churn.md)

## sub_nodes

- [definitions](node_0_3_3_0_0_definitions/CORE_0_3_3_0_0_definitions.md) — `definitions(model) -> list[ArchOpcode]`.
- [key_of](node_0_3_3_0_1_key_of/CORE_0_3_3_0_1_key_of.md) — `key_of(clause) -> key`.
- [strip](node_0_3_3_0_2_strip/CORE_0_3_3_0_2_strip.md) — `strip(execute_clause) -> LeanExpr`.
- [emit_lane](node_0_3_3_0_3_emit_lane/CORE_0_3_3_0_3_emit_lane.md) — The tower lane that runs the sail compiler's Lean backend over the model and caches the tree by commit.

## definition

The ratified Sail RISC-V model as the one source of every definition,
read by the sail compiler's Lean backend, never by a person. Holds the
model's git commit as the cache key and produces the list of
arch-opcodes with their definitions.

- built: `sail --lean` over the leaf modules the compilers target, on
  the tower (about 45 minutes and 17 GB per run, measured 2026-09-13,
  log 274 §3), once per commit; the output tree is the cache.
- the model lives at `SOURCES/sail-riscv` on the laptop and
  at `/sources/sail-riscv` in a lane; the image's own configured clone
  `/opt/sail-riscv-src` carries the generated config files the emit
  needs.

## design

```
class SailModel
	attributes:
		commit
		modules            # leaf module names, e.g. I_insts M_insts postlude main
		lean_tree          # the emitted Lean, keyed by commit
	methods:
		definitions
		key_of
		strip
```
