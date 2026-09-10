#!/usr/bin/env bash
# ex2_l1_preflight_and_smoke.sh -- task ex2, step 1: the outer set and
# the cells file, nothing run; then the first two cells on all seven
# interpreted targets (14 runs), so a bug in the new driver is found on
# fourteen runs rather than on 1,771.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX2; each runner is a separate short-lived process handed
# the whole sample at once.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/2] preflight: the outer set and the cells file"
python3 expand2.py preflight

echo ""
echo "[2/2] the smoke: the first two cells on all seven targets (14 runs)"
python3 expand2.py run 14
echo "done"
