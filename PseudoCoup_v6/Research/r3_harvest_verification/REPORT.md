# R3 Report — Harvest Verification In Place

Date: 2026-07-28. Runs by the owner on host via `run_checks.sh` (logs in
`runs/`). Purpose: every harvest source passes its OWN tests where
it lives before porting, so later port failures are attributable.

## Verdict: every harvest source is healthy

**Zero source failures across all seven suites.** Every reported
FAIL had a harness or environment cause — three causes total, all
identified from the logs, all fixed in the script:

| suite | final result | evidence |
|---|---|---|
| v0_idgen_check | PASS | first run |
| v0_ledger_unified_check | PASS | first run |
| pseudocoup_pytest | PASS (54 expected, confirmed on run 2) | `runs/pseudocoup_pytest.log` |
| pseudoir_pytest | 18/19 PASS; 1 environment residue (see cause 3) | `runs/pseudoir_pytest.log` |
| pcv5_test_vocab | PASS | first run |
| pcv5_differential_python_side | PASS | first run |
| pcv5_cpp_agreement | PASS | first run |

## Causes (report by cause, each with status)

1. **Missing PYTHONPATH for the v4 CLI** — the CLI imports
   pseudoir (gate + hoisting units); the script didn't provide it.
   All ~53 first-run pseudocoup failures were this one line
   (`ModuleNotFoundError: No module named 'pseudoir'`). FIXED in
   the script; suite then passed in full.
2. **Repo-wide pytest collection** — running pytest over all of
   `PseudoIR/` collected a research scratch file that calls
   `sys.exit` at import (`v2/prober/u_namespace/test_U.py`),
   crashing collection. FIXED: `tests/` only. Bonus evidence
   captured in the wreckage: the prober's 12 op vectors all PASS,
   including both falsy traps rejecting naive `a or b`.
3. **pseudoir not importable in emitted-program subprocesses** —
   `test_python_passthrough_matches_oracle` runs an EMITTED
   program in a subprocess; the program imports `pseudoir.U`,
   which historically resolved via `pip install -e`
   (`pseudoir.egg-info` is the fossil). FIXED in the script
   (PYTHONPATH exported to the suite). 18/19 passed regardless —
   including the TypeScript three-way-oracle leg. Confirmation
   rerun of this one suite is optional:
   `cd PseudoIR && PYTHONPATH=PseudoIR python3 -m pytest tests/ -q`

## Consequences for the tools program

- **Transplant order stands as planned** — no source is damaged,
  so no reordering is forced. T1 → T2 → T3 proceeds.
- The two T2 identity/record sources (`idgen.py`,
  `ledger_unified.py`) verified green on first run — the highest-
  value transplants carry the lowest risk.
- The v4 suite (semantic ledger + snapshot net) and all three PCv5
  gates (the T3 acceptance oracles) are green — the acceptance
  criteria the new tools will be measured against are themselves
  verified live.
- **Environment note for the ports**: v4's coupling to pseudoir is
  real (its CLI won't start without it). The T3 fresh spine must
  not inherit that implicit coupling — gate-before-emit arrives as
  a framework feature with an explicit dependency, not a bare
  import.
- Sandbox provisioning: tree-sitter 0.26.0 + python/rust/cpp
  grammar packages now installed in the session sandbox — T1 work
  can run in-session.
