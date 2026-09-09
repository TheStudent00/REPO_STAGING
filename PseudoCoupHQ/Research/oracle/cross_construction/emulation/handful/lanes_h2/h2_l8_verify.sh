#!/usr/bin/env bash
# h2_l8_verify.sh -- task h2: the conventions verifier over this task's
# own log, from this task's own instance, as the law requires.
#
# The verifier re-runs every command log 240 pastes and sorts each claim
# into matches / differs / unverifiable / refused. The verifier itself
# is never modified: where it disagrees, the log or the claim is fixed.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H2; the verifier
# prints its own peak RSS.
set -euo pipefail
echo "[1/2] task h2: the conventions verifier over log 240"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 /projects/PseudoCoupHQ/DevComms/log_240_task_h2_two_printing_fixes.md
echo "[2/2] done"
