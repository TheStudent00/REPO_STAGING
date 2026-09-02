---
id: pcv6.research
level: 1
status: settled
settled_by: the owner
supersedes: pcv6.planning.research_queue_flat
---

# CORE 0_1 — Research Queue

Every entry: what is being determined, by what experiment, with
what acceptance criterion, feeding which decision. Each entry gets
its own subfolder under `../../Research/` when it starts; reports
separate measured fact from characterization.

- **R1 — intentions-data verification: COMPLETE (2026-07-28).**
  Verdict: clean; four prose-only gaps enumerated →
  [T5's work list](../node_0_0_tools/node_0_0_4_intentions/CORE_0_0_4_intentions.md).
  Report: [../../Research/r1_intentions_validation/REPORT.md](../../Research/r1_intentions_validation/REPORT.md).
- **R2 — tree-sitter census of the compiler sources: QUEUED.**
  Parse the exact files the Rust ingestor will ingest (a retired
  reference backend's assembler crate + support family — since
  removed as mis-aimed, see the tools PROGRESS; rustc rvalue.rs;
  C++ files when the LLVM back-half starts) with T1's grammars; total-partition
  census; leftover = the ingestor's worklist. Acceptance:
  deterministic per-file census tables + a stated handled/stub
  split. Feeds: T3 sizing, T4 wrapper inventory. Depends on T1's
  grammar vendoring.
- **R3 — harvest verification in place: COMPLETE (2026-07-28).**
  Every harvest source passed its own tests where it lives; zero
  source failures (three harness/environment causes found and
  fixed in the run script). Transplant order stands. Report:
  [../../Research/r3_harvest_verification/REPORT.md](../../Research/r3_harvest_verification/REPORT.md).
- **R4 — runtime-ledger/walker survey: COMPLETE (2026-07-28).**
  Found the WFL walker suite + the node-identity design decision;
  consequence folded into
  [T2's keying spec](../node_0_0_tools/node_0_0_1_ledger/node_0_0_1_1_keying/CORE_0_0_1_1_keying.md).
  Report: [../../Research/r4_runtime_ledger_survey/REPORT.md](../../Research/r4_runtime_ledger_survey/REPORT.md).
