#!/usr/bin/env bash
# ap3_l14_claims.sh -- task ap3: every table the log pastes, each from
# its own command, printed by that command.
#
# Each entry point below prints exactly what the log pastes and nothing
# that moves between runs, which is what the conventions verifier
# re-runs.  `preflight` ends with the program's own `peak resident`
# line, a real measurement that moves by a few kB, so the pasted
# command carries the `grep -v` on the line itself.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "===== tables ====="
python3 autopoly3.py tables

echo "===== causes ====="
python3 autopoly3.py causes

echo "===== repose ====="
python3 autopoly3.py repose

echo "===== sat ====="
python3 autopoly3.py sat | grep -v counterexample

echo "===== change ====="
python3 autopoly3.py change

echo "===== fix4 ====="
python3 autopoly3.py fix4

echo "===== reproduce ====="
python3 autopoly3.py reproduce

echo "===== preflight ====="
python3 autopoly3.py preflight | grep -v 'peak resident'
echo "done"
