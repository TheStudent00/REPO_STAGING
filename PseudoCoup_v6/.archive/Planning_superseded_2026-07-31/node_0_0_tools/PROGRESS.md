---
id: pcv6.tools.progress
status: living
---

# PROGRESS — tools program

Stack acceptance as of 2026-07-28 (104 passed) included increments
since removed as mis-aimed (2026-07-30, see T3 below); that count no
longer reflects the current suite.

- T1 tree_sitter_base — **done**: graduated to
  `~/Programming/PseudoCoup_v6/Tools/tree_sitter_base/`,
  acceptance 12/12.
- T2 ledger — **phase-1 done**:
  `~/Programming/PseudoCoup_v6/Tools/ledger/`, acceptance 7/7;
  open points on its node PROGRESS (assembler-scale storage,
  declaration-kind growth, later slots).
- T3 transpiler — **framework done; one ingestor stands**: ingress
  framework; LLVM C++ encoder ingestor (byte-identical, agreement
  suite re-verified) — the first LLVM-facing tool. A Rust
  generated-vocabulary ingestor and a Rust support-layer ingestor
  were built pointing at a retired reference backend instead of the
  settled LLVM/rustc-LLVM direction and were removed as mis-aimed
  (2026-07-30). Emission deferred by design.
- T4 polyfill — **done**:
  `~/Programming/PseudoCoup_v6/Tools/polyfill/` (fixed-width
  wrapper layer + uniformity checker + differential grid vs an
  independently computed oracle). Five recorded deviations on its
  node PROGRESS — one needs the owner's ruling.
- T5 intentions — **planned**; work list ready (R1's four gaps).
  NOTE: its plan node is settled at CORE level only; it wants a
  depth layer before building.
- T6 slicer — **planned**; last, per dependency order; also wants
  a depth layer first.
