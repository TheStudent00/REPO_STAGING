---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model.emit_lane
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: emit_lane
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_0_sail_model/node_0_3_2_3_1_3_0_3_emit_lane/CORE_0_3_2_3_1_3_0_3_emit_lane.md
super_node:
    name: sail_model
    path: ../CORE_0_3_2_3_1_3_0_sail_model.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_0_3 — emit_lane

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model.emit_lane
- **level:** 7
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [sail_model](../CORE_0_3_2_3_1_3_0_sail_model.md)

## sub_nodes

*(none yet)*

## definition

The tower lane that runs the sail compiler's Lean backend over the
model and caches the tree by commit. Measured 2026-09-13 (log 274 §3):
45.5 minutes, about 17 GB resident, 62,893 lines of Lean for
`I_insts M_insts postlude main`; a 6 GB instance is stopped by the OS.

- built: the invocation in log 274 §3, verbatim; instance memory 20g on
  the tower; module names are LEAF names, checked first with
  `sail --list-files <modules> riscv.sail_project`, which resolves in
  seconds and must list `base_insts.sail` and `mext_insts.sail`.
- the lane's product is the cache; deleting it and re-running must
  reproduce it (the regeneration test).
