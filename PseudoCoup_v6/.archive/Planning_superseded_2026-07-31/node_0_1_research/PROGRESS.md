---
id: pcv6.research.progress
status: living
---

# PROGRESS — research queue

- R1 intentions-data verification — **done** 2026-07-28 (clean;
  `<WORKSPACE_DIR>/PseudoCoup_v6/Research/r1_intentions_validation/REPORT.md`).
- R2 compiler-source census — **done** 2026-07-28: all five
  subjects parse clean (zero ERROR nodes), censuses deterministic;
  milestone-1 worklist = 91 named kinds; report at
  `<WORKSPACE_DIR>/PseudoCoup_v6/Research/r2_compiler_source_census/REPORT.md`.
  Subject files (paths relative to `<WORKSPACE_DIR>/PseudoCoup_v5/`);
  the generated-Rust and support-family subjects belonged to a
  retired reference backend's assembler crate, since removed as
  mis-aimed (2026-07-30) along with the ingestor work they fed:
  - generated Rust: `Research/rust_routing/sources/encoder/asm/assembler.rs`
  - support family: the same crate's `rex.rs`, `custom.rs`, …
  - rustc front half: `Research/rust_routing/sources/rust/compiler/rustc_codegen_ssa/src/mir/rvalue.rs`
  - LLVM encoder: `Research/llvm_trace/sources/llvm-project/llvm/lib/Target/X86/MCTargetDesc/X86MCCodeEmitter.cpp`
- R3 harvest verification — **done** 2026-07-28 (all sources
  healthy, zero source failures;
  `<WORKSPACE_DIR>/PseudoCoup_v6/Research/r3_harvest_verification/REPORT.md`).
- R5 slice + insertion mechanism survey — **done** 2026-07-28:
  produced the automation-boundary finding (seams declared by
  hand, downstream mechanical) that shapes T5 and T6;
  `<WORKSPACE_DIR>/PseudoCoup_v6/Research/r5_slice_mechanism_survey/REPORT.md`.
- R4 runtime-ledger/walker survey — **done** 2026-07-28
  (`<WORKSPACE_DIR>/PseudoCoup_v6/Research/r4_runtime_ledger_survey/REPORT.md`).
