---
id: pir.rust_llvm_transpile
level: 4
status: draft
settled_by: the owner
supersedes: null
nodes: []
---

# CORE 0_2_0_0_0 — transpile

## metadata

- **id:** pir.rust_llvm_transpile
- **level:** 4
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

*(none yet)*

## definition

getting rustc's source into hub source

the rust ingestor. the live work is the rustc front-half `rvalue.rs`
BinOp routing plus recording semantic roles.

## support

- [SUPPORT_rust_ingestor.md](SUPPORT_rust_ingestor.md) — carries its
  own record of which scope items were struck and why, and one step
  still marked unresolved
