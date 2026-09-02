---
id: pir.tools
level: 1
status: draft
settled_by: the owner
supersedes: pcv6.slicer
nodes: [transpile, slice, insert]
---

# CORE 0_0 — tools

## metadata

- **id:** pir.tools
- **level:** 1
- **status:** draft
- **settled_by:** the owner
- **supersedes:** pcv6.slicer

## super_node

*(none — tree root)*

## sub_nodes

- [transpile](node_0_0_0_transpile/CORE_0_0_0_transpile.md) — convert the source compiler into hub python.
- [slice](node_0_0_1_slice/CORE_0_0_1_slice.md) — extract the intention-bearing logic out of the transpiled compiler.
- [insert](node_0_0_2_insert/CORE_0_0_2_insert.md) — mount the slice into the hub.

## definition

the things we build and run. one per stage.

## notes

order is the order the work runs in. every intention traverses all
three.

these replace the single `slicer` tool the previous plan carried.
that tool was defined as extract AND insert, which put two stages
under one name and left the first stage in another project.

`transpile` is where PseudoIR borrows PseudoCoup's transpiler. it is
the only place this project reaches into the other one.

## support

- [SUPPORT_slicer.md](SUPPORT_slicer.md) — the previous plan's single
  slicer tool, covering what is now slice and insert
