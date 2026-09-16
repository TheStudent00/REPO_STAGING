---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.dictionary
level: 6
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: dictionary
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_6_dictionary/CORE_0_3_2_3_1_3_6_dictionary.md
super_node:
    name: lean_proof_path
    path: ../CORE_0_3_2_3_1_3_lean_proof_path.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_6 — dictionary

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.dictionary
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

The table keyed by (language, arch-opcode) whose entries are proved
emulations: the line's bank, regenerable from the model and the
compilers by running the system. Read by the Hub; written only by the
three passes.

- built: `System.run`; the regeneration test is that deleting it and
  running gives it back byte-identical or with the diff named.

## design

```
class Dictionary
	attributes:
		entries            # (Language, ArchOpcode) -> Emulation
		definitions_commit
	methods:
		add
		find
		report             # the table "of N" per language, three readings where they differ
```
