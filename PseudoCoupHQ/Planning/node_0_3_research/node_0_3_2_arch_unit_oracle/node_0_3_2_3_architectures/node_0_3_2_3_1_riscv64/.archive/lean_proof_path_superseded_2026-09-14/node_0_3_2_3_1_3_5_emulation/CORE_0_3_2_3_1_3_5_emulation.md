---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.emulation
level: 6
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: emulation
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_5_emulation/CORE_0_3_2_3_1_3_5_emulation.md
super_node:
    name: lean_proof_path
    path: ../CORE_0_3_2_3_1_3_lean_proof_path.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_5 — emulation

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.emulation
- **level:** 6
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path](../CORE_0_3_2_3_1_3_lean_proof_path.md)

## sub_nodes

*(none yet)*

## definition

One proved answer: an arch-opcode, a language, the compiled unit that
computes the arch-opcode's definition, and the Lean theorem file that
proves it. The certificate of the earlier line, with the proof object
inside it.

- built: by pass A (found in the corpus) or pass B (rendered, compiled,
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
