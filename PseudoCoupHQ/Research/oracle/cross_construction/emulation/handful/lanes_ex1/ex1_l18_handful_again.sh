#!/usr/bin/env bash
# ex1_l18_handful_again.sh -- task ex1: the handful table re-run on its
# own, because the verifier's first pass over log 248 found the pasted
# copy DIFFERS from what re-running produces.  The claim is fixed in
# the LOG, never in the verifier, and this lane's output is what the
# log will carry.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 expand1.py handful
echo "done"
