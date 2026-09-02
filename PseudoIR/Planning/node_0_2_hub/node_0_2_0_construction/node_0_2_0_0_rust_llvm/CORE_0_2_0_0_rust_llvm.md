---
id: pir.rust_llvm
level: 3
status: draft
settled_by: the owner
supersedes: null
nodes: [transpile, slice, insert]
---

# CORE 0_2_0_0 — rust llvm

## metadata

- **id:** pir.rust_llvm
- **level:** 3
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

- [transpile](node_0_2_0_0_0_transpile/CORE_0_2_0_0_0_transpile.md) — getting rustc's source into hub source.
- [slice](node_0_2_0_0_1_slice/CORE_0_2_0_0_1_slice.md) — cutting rust's semantics out of the transpiled compiler.
- [insert](node_0_2_0_0_2_insert/CORE_0_2_0_0_2_insert.md) — mounting rust's slice so the hub computes rust's semantics.

## definition

rust, through llvm. the intermediate goal, and the first language put
into the hub.

## notes

the three sub-nodes are this language's work at each stage. the
stages themselves are tools, written once at
[tools](../../../node_0_0_tools/CORE_0_0_tools.md). nothing here
restates how a tool works; what is here is what rustc and llvm
specifically demand of it.

## support

- [SUPPORT_framing.md](SUPPORT_framing.md) — the campaign framing
  from the previous plan. its cross-check oracle was the retired
  backend; ground truth is now real rustc and llvm output
