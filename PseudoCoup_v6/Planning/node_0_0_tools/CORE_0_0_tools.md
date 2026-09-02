---
id: pcv6.tools
level: 1
status: draft
settled_by: the owner
supersedes: null
nodes: [ledgerer, transpiler, polyfill]
---

# CORE 0_0 — tools

## metadata

- **id:** pcv6.tools
- **level:** 1
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

- [ledgerer](node_0_0_0_ledgerer/CORE_0_0_0_ledgerer.md) — the system that tracks all information needed of input script to preserve intentions.
- [transpiler](node_0_0_1_transpiler/CORE_0_0_1_transpiler.md) — maps from source language to target language while preserving intentions.
- [polyfill](node_0_0_2_polyfill/CORE_0_0_2_polyfill.md) — wrappers from transpilation that the required filling to match source behavior.

## definition

the things we build and run

## notes

order is dependency order. the transpiler uses the ledgerer. the
polyfill supplies wrappers the transpiler places.

the slicer left in the split — it is PseudoIR's, and PseudoIR split
it into two tools, slice and insert.

the transpiler is the artifact this project lends to PseudoIR.
