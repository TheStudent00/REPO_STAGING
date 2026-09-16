---
id: hq.research.lean_proof_path_resistant_to_churn.emulation
level: 3
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.emulation
designation: code (class)
node:
    name: emulation
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_5_emulation/CORE_0_3_3_5_emulation.md
super_node:
    name: lean_proof_path_resistant_to_churn
    path: ../CORE_0_3_3_lean_proof_path_resistant_to_churn.md
sub_nodes: []
---

# CORE 0_3_3_5 — emulation

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.emulation
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.emulation

## super_node

- [lean_proof_path_resistant_to_churn](../CORE_0_3_3_lean_proof_path_resistant_to_churn.md)

## sub_nodes

*(none yet)*

## definition

One proved answer: an arch-opcode, a language, the compiled unit that
computes the arch-opcode's definition, and the Lean theorem file that
proves it. The certificate of the earlier line, with the proof object
inside it.

- built: by pass A (found in the language's `compiler_corpus`) or pass B (rendered, compiled,
  proved); never without a checked proof.

## design

```
class Emulation
	attributes:
		opcode
		language
		unit
		proof              # the Lean theorem file, kernel-checked
		found_or_built     # which pass produced it
		definitions_commit # the model commit the definition came from
```
