---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model.key_of
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: key_of
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_0_sail_model/node_0_3_2_3_1_3_0_1_key_of/CORE_0_3_2_3_1_3_0_1_key_of.md
super_node:
    name: sail_model
    path: ../CORE_0_3_2_3_1_3_0_sail_model.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_0_1 — key_of

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model.key_of
- **level:** 7
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [sail_model](../CORE_0_3_2_3_1_3_0_sail_model.md)

## sub_nodes

*(none yet)*

## definition

`key_of(clause) -> key`

Input: one instruction's `mapping clause assembly` as Lean wrote it. Output: (mnemonic, operand form, width), the machine-form key the spelling guard exempts as machine form.

Steps, in order:

1. read the mnemonic as the assembly clause's literal string, with its width suffix rule (`maybe_u`, `w`) applied by the clause itself
2. read the operand form from the clause's parameter kinds (register, register, register; register, immediate; ...)
3. read the width from `xlen` as instantiated in the emit (64) or the clause's own narrower width
4. return the triple; nothing else about the instruction is read
