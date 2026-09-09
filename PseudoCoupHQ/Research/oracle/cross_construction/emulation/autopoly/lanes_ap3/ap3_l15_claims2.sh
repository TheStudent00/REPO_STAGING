#!/usr/bin/env bash
# ap3_l15_claims2.sh -- task ap3, second pass (a lane name is used ONCE; nothing was removed): the fix-4 table of lane ap3_l14 pasted a WHOLE rendered source per side, several hundred characters of shared preamble around the one line that is the measurement, so `sources_that_differ` now prints the FIRST LINE the two differ on. Nothing else moved.: every table the log pastes, each from
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
