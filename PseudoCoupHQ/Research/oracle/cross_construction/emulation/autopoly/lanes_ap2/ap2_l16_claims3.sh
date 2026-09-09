#!/usr/bin/env bash
# ap2_l16_claims3.sh -- task ap2: the claims of ap2_l15, re-run once the two change-table corrections had actually reached the tower (the pass before it ran an older copy of autopoly2.py).
# a command, printed by that command.
#
# Each entry point of `autopoly2.py` below prints exactly what the log
# pastes and nothing that moves between runs, which is what the
# conventions verifier re-runs.  `preflight` ends with the program's
# own `peak resident` line, a real measurement that moves by a few kB,
# so the pasted command carries the `grep -v` on the line itself --
# task ap1's own third-pass correction, kept.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "===== tables ====="
python3 autopoly2.py tables

echo "===== causes ====="
python3 autopoly2.py causes

echo "===== repose ====="
python3 autopoly2.py repose

echo "===== sat ====="
python3 autopoly2.py sat

echo "===== change ====="
python3 autopoly2.py change

echo "===== reproduce ====="
python3 autopoly2.py reproduce

echo "===== preflight ====="
python3 autopoly2.py preflight | grep -v 'peak resident'
echo "done"
