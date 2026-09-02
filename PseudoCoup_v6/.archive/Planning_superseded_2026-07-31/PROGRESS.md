---
id: pcv6.planning.progress
status: living
---

# PROGRESS — node_0 (project)

- planning restructure to the node grammar — **done** 2026-07-28.
- tools program (node_0_0) — **partially built, one line removed**
  2026-07-30. Standing green at 128 tests: T1 tree_sitter_base (12),
  T2 ledger phase-1 (7), T3 ingress framework + LLVM C++ encoder
  ingestor (8), T4 polyfill (68), T5 intentions data (19), T6
  insertion (14). REMOVED as mis-aimed: T3's two Rust-side
  ingestors, T5's forms, T6's selection and extraction — all of
  them pointed at a retired backend rather than the settled
  LLVM/rustc-LLVM direction. See `node_0_0_tools/PROGRESS.md`.
- research (node_0_1) — R1–R4 complete. R5 removed with its
  subject.
- Hub (node_0_2), Rust/LLVM application (node_0_3), application
  ingress (node_0_4) — planning drafted 2026-07-29, unbuilt; all
  `status: draft` pending the owner's review.
- **next action**: write the first LLVM-facing slicing request form
  (the front half — rustc_codegen_ssa `rvalue.rs` BinOp routing
  into rustc_codegen_llvm's builder), then rebuild selection and
  extraction against it, verified against `rustc --emit=llvm-ir`.
  That is the critical path to the intermediate goal, and both its
  ends already exist: the LLVM encoder ingests, and insertion
  executes mounted bytes.
