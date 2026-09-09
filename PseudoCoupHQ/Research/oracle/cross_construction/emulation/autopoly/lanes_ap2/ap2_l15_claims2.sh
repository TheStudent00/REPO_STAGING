#!/usr/bin/env bash
# ap2_l15_claims2.sh -- task ap2: the same claims as ap2_l14, after two defects in the CHANGE TABLE (not in a fix or a run) were corrected: it joined the two stores on task ap1's own key_width, which fix 4 has moved on eight cells, and its sat column printed the region and the counterexample twice.
# a command, printed by that command.
#
# Each entry point of `autopoly2.py` below prints exactly what the log
# pastes and nothing that moves between runs, which is what the
# conventions verifier re-runs.  `preflight` ends with the program's
# own `peak resident` line, a real measurement that moves by a few kB,
# so the pasted command carries the `grep -v` on the line itself --
# task ap1's own third-pass correction, kept.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

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
