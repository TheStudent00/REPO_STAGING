---
id: pcv6.tools.t3_transpiler.progress
status: living
---

# PROGRESS — T3 transpiler

- plan — **settled** 2026-07-28 (fresh spine; ingress-first;
  gates as framework features).
- ingress framework — **done** 2026-07-28 (acceptance 6/6; see
  its node PROGRESS).
- rust ingestor (increment 1) and the rust support-layer ingestor
  (increment 3) were built pointing at a retired reference backend
  instead of at the settled LLVM/rustc-LLVM direction. Both were
  **removed as mis-aimed** (2026-07-30); their outputs and tests are
  gone, and no claim from that work is carried forward. The forward
  path for Rust ingestion is LLVM/rustc-LLVM.
- LLVM C++ encoder ingestor — **increment 2 done** 2026-07-28:
  byte-identical to PCv5's `llvm_encoder_gen.py`; PCv5's agreement
  suite re-run against our build ALL PASS. First LLVM-facing tool,
  and the one increment of this node that stands as forward work.
- emission — **deferred** by design.
