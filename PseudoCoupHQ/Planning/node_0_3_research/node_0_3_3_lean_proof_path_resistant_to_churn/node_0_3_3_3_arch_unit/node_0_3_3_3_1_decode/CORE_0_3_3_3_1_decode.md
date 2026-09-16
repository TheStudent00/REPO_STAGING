---
id: hq.research.lean_proof_path_resistant_to_churn.arch_unit.decode
level: 4
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.decode
designation: code (method)
node:
    name: decode
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_3_arch_unit/node_0_3_3_3_1_decode/CORE_0_3_3_3_1_decode.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_3_3_arch_unit.md
sub_nodes: []
---

# CORE 0_3_3_3_1 — decode

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.arch_unit.decode
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit.decode

## super_node

- [arch_unit](../CORE_0_3_3_3_arch_unit.md)

## sub_nodes

*(none yet)*

## definition

`decode(word) -> instruction`

Input: one 32-bit or 16-bit encoded word. Output: the Sail `instruction` value (constructor and operands), as Sail's own decoder gives it.

Steps, in order:

1. apply the emitted `encdec_backwards` (or the compressed form) to the word
2. return the constructor and its operands; an undecodable word is a refusal, never a guess

The decoder is the model's own; the disassembler's text is kept only as the display label.
