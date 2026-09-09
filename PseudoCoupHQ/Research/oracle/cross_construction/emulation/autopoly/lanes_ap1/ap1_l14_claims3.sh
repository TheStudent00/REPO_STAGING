#!/usr/bin/env bash
# ap1_l14_claims3.sh -- task ap1: the four claims the DevComms log
# carried as attributions to a lane log, turned into commands that
# re-run, and run once so the log pastes what the machine printed.
#
# WHY: the conventions verifier scored this task's first pass 5 MATCHES
# and 16 UNVERIFIABLE. Zero DIFFERS is the law's obligation and it was
# met, but four of those sixteen are facts a command can reproduce --
# the outer set, the store's identity with the aggregate, the `sat`
# counts, and which form of a term the renderer is handed. Each is now
# an entry point of `autopoly.py`.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py
echo "===== preflight ====="
python3 $A preflight
echo "===== store ====="
python3 $A store
echo "===== sat ====="
python3 $A sat
echo "===== branch ====="
python3 $A branch
