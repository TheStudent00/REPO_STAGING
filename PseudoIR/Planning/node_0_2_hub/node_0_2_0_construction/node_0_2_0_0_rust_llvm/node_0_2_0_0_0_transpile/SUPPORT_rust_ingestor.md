---
id: pir.rust_llvm_transpile.support.rust_ingestor
status: projected
---

# SUPPORT — rust ingestor

projected 2026-07-30 from the previous plan, now archived at
`PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_2_transpiler/node_0_0_2_1_rust_ingestor/CORE_0_0_2_1_rust_ingestor.md  (279 words)
source: node_0_0_tools/node_0_0_2_transpiler/node_0_0_2_1_rust_ingestor/node_0_0_2_1_0_deepening/CORE_0_0_2_1_0_deepening.md  (274 words)
verdict: substitute
changed: both sources already carry their own 2026-07-30
self-corrections striking the items that pointed at the retired
backend's generated assembler crate and its hand-written encoding
support files; those strikethroughs and superseded notes are carried
here intact as the record of what went wrong, not silently dropped.
The surviving forward work in both — the rustc front-half `rvalue.rs`
BinOp routing plus semantic-role recording — is carried as the live
plan. One addition beyond faithful carrying: deepening step 2
("ledger population at assembler scale") is marked [UNRESOLVED]
below, with a note that the equivalent LLVM-side file to measure
against is not yet identified — that scale figure was measured
against the retired backend's generated files, which no longer
anchor this campaign's ground truth.

---

## from rust_ingestor

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

- `node_0_0_2_1_0_deepening` (previous plan)
  — beyond structural reproduction: the rvalue.rs front half
  (+19 node kinds; SHARED with the Rust/LLVM application's front
  half — build once, two consumers), ledger population at
  assembler scale, semantic types. *(planning added 2026-07-29)*

## from deepening

# CORE 0_0_2_1_0 — Rust Ingestor Deepening

The rust ingestor's increment 1 (structural CST reproduction of a
generated-vocabulary artifact) pointed at a retired reference backend
instead of the settled LLVM/rustc-LLVM direction and was removed as
mis-aimed (2026-07-30); no claim from it carries forward. The open
steps below remain the forward plan, independent of that removal:

## Steps

1. **rvalue.rs front half** — the same file the Rust/LLVM
   application's front-half node needs (node_0_3_0); the ingestor
   must handle the +19 node kinds R2 measured beyond the
   generated+support set (closures, for/range, tuple/or-patterns,
   `let_chain`, `compound_assignment_expr`, lifetimes). This is
   where the ingestor stops reproducing a closed generated grammar
   and starts handling real hand-written Rust breadth.
2. **Ledger population at assembler scale** — the ingestor
   currently reproduces vocabulary; making it POPULATE the ledger
   over the 1.27M-node generated file needs the growth node's
   scale decision (node_0_0_1_3). Coupled: do not populate
   assembler-scale until the storage strategy is chosen.
   **[UNRESOLVED]** — the 1.27M-node figure was measured against
   the retired backend's generated files, which no longer anchor
   this campaign; the equivalent LLVM-side file to measure ledger
   population against is not yet identified.
3. **Semantic types, not just structure** — increment 1 records
   structure; the sliced regions need their semantic role recorded
   (which the T6 extraction consumes). Bridges into intent capture
   (node_0_4_1) for the application side.

## Acceptance

- rvalue.rs parses and ingests with the census gate green (the
  +19 kinds handled or baseline-justified, leftover fails).
- The front-half slice (node_0_3_0) extracts through this ingestor
  and matches `rustc --emit=llvm-ir`.

## Dependency note

Step 1 is the critical unblock for the Rust/LLVM application's
front half — the two nodes share the rvalue.rs work. Build it once,
in the ingestor, and the application node consumes it. Recorded so
the work is not duplicated across the two lines.

## where that sub-node went

- deepening — carried in this file, above, under its own `## from`
  heading.
