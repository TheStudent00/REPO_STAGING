#!/usr/bin/env bash
# ap1_l10_claims.sh -- task ap1: every command the DevComms log pastes,
# run once, so what the log carries is what the machine printed and the
# conventions verifier re-runs it unchanged.
#
# Each of the three commands is one entry point of `autopoly.py` and
# prints no figure that moves between runs (no peak resident line, no
# wall clock), which is what makes the claim re-runnable.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py
echo "===== tables ====="
python3 $A tables
echo "===== causes ====="
python3 $A causes
echo "===== repose ====="
python3 $A repose
echo "===== reproduce ====="
python3 $A reproduce
