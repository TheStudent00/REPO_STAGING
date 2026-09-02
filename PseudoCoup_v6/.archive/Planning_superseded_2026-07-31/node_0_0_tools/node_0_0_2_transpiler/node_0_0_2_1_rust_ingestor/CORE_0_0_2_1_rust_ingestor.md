---
id: pcv6.tools.t3_transpiler.rust_ingestor
level: 3
status: settled
settled_by: the owner
supersedes: null
---

# CORE 0_0_2_1 — Rust Ingestor (first milestone)

**SUPERSEDED IN PART (2026-07-30):** the scope below originally
pointed the generated-Rust and hand-written-support-grammar
increments at a retired reference backend instead of the settled
LLVM/rustc-LLVM direction. That work was removed as mis-aimed; its
artifacts, gates, and acceptance numbers no longer exist in this
repo and are not carried forward as accomplishments. Item 3 (the
rustc front-half files, `rvalue.rs` BinOp routing) and the LLVM C++
ingestor built as a co-node both stand. The forward direction for
the retired items is LLVM/rustc-LLVM, to be re-scoped when taken up.

The compiler-source ingress rebuilt on tree-sitter, replacing
PCv5's bespoke parsers (settled: tree-sitter everywhere; the
bespoke parsers are archived expedience).

- **Scope, in order of the R2 census** (items 1-2 superseded, see
  above):
  1. ~~generated Rust (a retired reference backend's assembler
     crate — the closed 12-node-kind grammar)~~;
  2. ~~hand-written Rust support grammar (arithmetic, `match`,
     struct literals — the same crate's `rex.rs`/`mem.rs` family)~~;
  3. the rustc front-half files the intermediate goal needs
     (`rvalue.rs` BinOp routing).
- **Dependency**: R2 (tree-sitter census of these exact files)
  sizes the node table before any porting; measure first.
- **Polyfill interface**: arithmetic nodes route through T4's
  wrappers under the uniform law; the census's arithmetic-node
  inventory is T4's requirements list.
- Provenance rule: transplanted logic keeps source headers; the
  C++ ingestor follows the same pattern as a later co-node when the
  LLVM back-half work starts.

## Sub-nodes

- [node_0_0_2_1_0_deepening](node_0_0_2_1_0_deepening/CORE_0_0_2_1_0_deepening.md)
  — beyond structural reproduction: the rvalue.rs front half
  (+19 node kinds; SHARED with the Rust/LLVM application's front
  half — build once, two consumers), ledger population at
  assembler scale, semantic types. *(planning added 2026-07-29)*
