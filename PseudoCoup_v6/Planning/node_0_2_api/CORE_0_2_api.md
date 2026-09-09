---
id: pcv6.api
level: 1
status: draft
settled_by: the owner
supersedes: pcv6.application
nodes: [examples]
---

# CORE 0_2 — api

## metadata

- **id:** pcv6.api
- **level:** 1
- **status:** draft
- **settled_by:** the owner
- **supersedes:** pcv6.application

## super_node

*(none — tree root)*

## sub_nodes

- [examples](node_0_2_0_examples/CORE_0_2_0_examples.md) — worked uses of the api.

## definition

the callable surface. what a caller imports and invokes to do the work

## components

- surface: what is imported, what is called, what comes back
- drive: how one call runs the ledgerer, transpiler, polyfill and
  slicer in order

## notes

not interface sugar. calling it does the work; there is no separate
real entry point underneath that this merely covers. usable from an
ordinary python script.

the api depends on what PseudoIR put into the hub. both the hub and
the construction that fills it are planned in the other project, at
`PseudoIR/Planning`.

## support

- [SUPPORT_converting_programs.md](SUPPORT_converting_programs.md) —
  converting ordinary programs, and one ingestor per language
