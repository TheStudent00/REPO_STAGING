---
id: pcv6.tools.t3_transpiler.rust_ingestor.deepening
level: 4
status: draft
settled_by: the owner
supersedes: null
---

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
