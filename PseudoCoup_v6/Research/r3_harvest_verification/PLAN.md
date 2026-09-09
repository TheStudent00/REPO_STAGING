# R3 — Harvest Verification In Place

Spec: [../../Planning/node_0_1_research/CORE_0_1_research.md](../../Planning/node_0_1_research/CORE_0_1_research.md).
Every component named in the harvest maps runs its OWN tests where
it lives, BEFORE porting — so a later port failure is attributable
to the port, not the source.

Run (host; sandbox was down at staging):

```bash
bash PseudoCoup_v6/Research/r3_harvest_verification/run_checks.sh
```

Logs land in `runs/` beside the script; the status table is
`runs/status.md` and is also printed. Toolchain-dependent suites
that fail on a missing command are reported `needs-host-toolchain`,
not FAIL. REPORT.md gets written from `runs/` after execution.

Covered sources: v0 `idgen.py --check` + `ledger_unified.py
--check` (T2 identity/record sources), `PseudoCoup/` pytest (T2
semantic payload + T3 snapshot-net source), PseudoIR pytest
(registry + gate + three-way oracle; TS leg needs node), PCv5
gates (`test_vocab.py`, differential python side,
`cpp_ingress/test_agreement.py` — T3/T4 sources).
