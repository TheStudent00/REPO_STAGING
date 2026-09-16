---
id: hq.research.lean_proof_path_resistant_to_churn.arch_opcode
level: 3
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_opcode
designation: code (class)
node:
    name: arch_opcode
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_1_arch_opcode/CORE_0_3_3_1_arch_opcode.md
super_node:
    name: lean_proof_path_resistant_to_churn
    path: ../CORE_0_3_3_lean_proof_path_resistant_to_churn.md
sub_nodes: []
---

# CORE 0_3_3_1 — arch_opcode

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.arch_opcode
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_opcode

## super_node

- [lean_proof_path_resistant_to_churn](../CORE_0_3_3_lean_proof_path_resistant_to_churn.md)

## sub_nodes

*(none yet)*

## definition

One machine instruction the compiler can write, keyed by mnemonic,
operand form and width, with its definition as a Lean expression taken
from the model. The identity of a cell is its key and its definition;
the mnemonic appears only as the display label the spelling ban allows.

- built: by `SailModel.definitions`, one per `execute` clause; never by
  hand.

## design

```
class ArchOpcode
	attributes:
		key                # (mnemonic, operand form, width)
		definition         # LeanExpr, the execute clause stripped
		source_clause      # the Lean text, for the audit trail
```
