---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.emit_measured
level: 6
status: draft
settled_by: the owner
supersedes: null
designation: finding
node:
    name: emit_measured
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_9_emit_measured/CORE_0_3_2_3_1_3_9_emit_measured.md
super_node:
    name: lean_proof_path
    path: ../CORE_0_3_2_3_1_3_lean_proof_path.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_9 — emit_measured

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.emit_measured
- **level:** 6
- **status:** draft
- **designation:** finding
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path](../CORE_0_3_2_3_1_3_lean_proof_path.md)

## sub_nodes

*(none yet)*

## definition

What the sail compiler's Lean backend produced and cost on 2026-09-13,
the five lanes of log 274 §3: refused without network on the laptop
(the C emulator's build fetches a dependency); stopped by the OS at 6 GB;
flat at 16.5 GB for 22 minutes at 16 GB; 47.5 minutes and 17.0 GB on the
tower for the wrong (group) module names with no instruction clause
emitted; 45.5 minutes and 62,893 lines for the leaf names
`I_insts M_insts postlude main`, with `execute_DIV` at
`InstsEnd.lean:4362`.

- the literal of `execute_DIV` and of `mult_to_bits_half` as Lean wrote
  them are in log 274 §2.3; the tree is at
  `<runs>/sail0/agent/out/lean/`.
- the two facts a future lane needs: module names are leaf names,
  resolved first with `sail --list-files`; the emit is fixed in cost and
  cached by commit.
