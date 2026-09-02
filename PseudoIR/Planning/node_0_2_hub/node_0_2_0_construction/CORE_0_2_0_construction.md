---
id: pir.construction
level: 2
status: draft
settled_by: the owner
supersedes: pcv6.construction
nodes: [rust_llvm]
---

# CORE 0_2_0 — construction

## metadata

- **id:** pir.construction
- **level:** 2
- **status:** draft
- **settled_by:** the owner
- **supersedes:** pcv6.construction

## super_node

*(none — tree root)*

## sub_nodes

- [rust_llvm](node_0_2_0_0_rust_llvm/CORE_0_2_0_0_rust_llvm.md) — rust, through llvm.

## definition

getting a language's semantics into the hub, one language at a time

## notes

one sub-node per language. each runs the same three tools —
transpile, then slice, then insert — over that language's compiler.

the tools are written once, in
[tools](../../node_0_0_tools/CORE_0_0_tools.md). what lives under a
language here is what is specific to that language.

the remaining 11 languages get sub-nodes when they are started, not
before.
