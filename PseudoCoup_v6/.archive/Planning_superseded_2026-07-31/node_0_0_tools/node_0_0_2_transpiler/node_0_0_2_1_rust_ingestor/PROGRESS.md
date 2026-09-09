---
id: pcv6.tools.t3_transpiler.rust_ingestor.progress
status: living
---

# PROGRESS — T3 rust ingestor

- plan — **settled** 2026-07-28.
- **UNBLOCKED** 2026-07-28: R2 done — all sources parse clean
  under T1's grammars; milestone-1 node table sized at 91 named
  kinds (`~/Programming/PseudoCoup_v6/Research/r2_compiler_source_census/REPORT.md`).
- Two increments of this node (a generated-vocabulary ingestor and its
  statement-level CST deepening) were built pointing at a retired
  reference backend instead of the settled LLVM/rustc-LLVM direction.
  Both were **removed as mis-aimed** (2026-07-30); their outputs, gates,
  and acceptance oracles are gone, and no claim from that work is
  carried forward.
- **increment 2 (LLVM C++ encoder) — done** 2026-07-28:
  `~/Programming/PseudoCoup_v6/Tools/transpiler/ingest_llvm_encoder.py`
  + `render_cpp.py` (verbatim-copied rendering/assembly layer).
  Structure (functions, enum, class body) from tree-sitter,
  replacing the regex/brace-scanning extractors. **Acceptance met:
  output BYTE-IDENTICAL to PCv5's `llvm_encoder_gen.py`**, and
  PCv5's own agreement suite re-run against OUR build: ALL PASS
  (modRM 256/256, REX 131,072/131,072, SIB 256/256, all five cut
  arms refuse). Census gate: R2-frozen 94-kind partition.
  This is the first LLVM-facing tool in PCv6, and the one increment
  of this node that stands as forward work.
- open: the forward path for Rust-side ingestion is LLVM/rustc-LLVM;
  a rust_codegen_llvm-facing ingestor increment has not yet been
  built.
