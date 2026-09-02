# R1 — Intentions-Data Verification

Spec: `Planning/02_research_queue.md` R1. This folder holds the
runs and the report. Status: PLANNED — sandbox shell was down at
founding (2026-07-28); commands staged below, runnable in-session
when the shell returns, or by the owner on host.

Subject artifacts (provenance: PseudoCoup_v5):
- `<WORKSPACE_DIR>/PseudoCoup_v5/Designing/pc_verdicts.json`
- `<WORKSPACE_DIR>/PseudoCoup_v5/Designing/build_verdicts.py`
- `<WORKSPACE_DIR>/PseudoCoup_v5/Designing/intention_tables_gen.py`
- markdown sources: `minimum_intention_set.md`,
  `intention_row_satisfiers.md`, `two_layer_program.md`,
  `BEJ_expansion.md` (same folder)
- probe ground truth: `<WORKSPACE_DIR>/PseudoCoup_v5/Research/
  basis_audit/results.md` + run scripts

## How to run

Checks 1–2 are a script in this folder:

```bash
bash <WORKSPACE_DIR>/PseudoCoup_v6/Research/r1_intentions_validation/run_checks.sh
```

No chmod needed (invoked via `bash`). It regenerates both
artifacts in the PCv5 tree, byte-diffs them against git HEAD,
restores the tree, dumps the JSON's field sizes, and writes all
logs to `runs/` in this folder. Verified invocation: both
generators run bare (`build_verdicts.py` docstring: "Rerun after
any data change: python3 build_verdicts.py";
`intention_tables_gen.py`: "Edit the data below, rerun, commit
both files").

Checks 3 (agreement with basis_audit + divergence suite) and 4
(dominance-as-data audit) get their own scripts here once 1–2
pass.

## Report

`REPORT.md` (not yet written): four checks PASS/FAIL with exact
diffs/cells for any FAIL, plus the list of dominance/satisfier
facts that exist only in prose and need lifting into data for the
slicer (T6).
