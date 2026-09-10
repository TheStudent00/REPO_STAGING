---
id: pir.research.support.research_queue
status: projected
---

# SUPPORT — research queue

projected 2026-07-30 from the previous plan, now archived at
`PRIVATE/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_1_research/CORE_0_1_research.md  (197 words)
verdict: substitute
changed: R2's entry named the retired backend's assembler crate as an
ingest target; the old file itself had already crossed that out and
repointed at rustc's own files plus LLVM C++ files. Carried here with
the retired backend left unnamed. [SUBSTITUTED]

---

# CORE 0_1 — Research Queue

Every entry: what is being determined, by what experiment, with
what acceptance criterion, feeding which decision. Each entry gets
its own subfolder under `../../Research/` when it starts; reports
separate measured fact from characterization.

- **R1 — intentions-data verification: COMPLETE (2026-07-28).**
  Verdict: clean; four prose-only gaps enumerated →
  `T5's work list` (previous plan).
  Report: `../../Research/r1_intentions_validation/REPORT.md` (`PRIVATE/PseudoCoup_v6/Research/r1_intentions_validation/REPORT.md`).
- **R2 — tree-sitter census of the compiler sources: QUEUED.**
  Parse the exact files the Rust ingestor will ingest (the retired
  backend's assembler crate + support family — since removed as
  mis-aimed, see the tools PROGRESS; rustc rvalue.rs; C++ files when
  the LLVM back-half starts) with T1's grammars; total-partition
  census; leftover = the ingestor's worklist. Acceptance:
  deterministic per-file census tables + a stated handled/stub
  split. Feeds: T3 sizing, T4 wrapper inventory. Depends on T1's
  grammar vendoring.
- **R3 — harvest verification in place: COMPLETE (2026-07-28).**
  Every harvest source passed its own tests where it lives; zero
  source failures (three harness/environment causes found and
  fixed in the run script). Transplant order stands. Report:
  `../../Research/r3_harvest_verification/REPORT.md` (`PRIVATE/PseudoCoup_v6/Research/r3_harvest_verification/REPORT.md`).
- **R4 — runtime-ledger/walker survey: COMPLETE (2026-07-28).**
  Found the WFL walker suite + the node-identity design decision;
  consequence folded into
  `T2's keying spec` (previous plan).
  Report: `../../Research/r4_runtime_ledger_survey/REPORT.md` (`PRIVATE/PseudoCoup_v6/Research/r4_runtime_ledger_survey/REPORT.md`).

## where those references went

- T5's work list — `PRIVATE/PseudoIR/Planning/node_0_1_research/node_0_1_0_intentions/SUPPORT_intentions_data_shape.md`
- T2's keying spec — moved to the other project with the ledgerer:
  `PRIVATE/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_ur_ast.md`
