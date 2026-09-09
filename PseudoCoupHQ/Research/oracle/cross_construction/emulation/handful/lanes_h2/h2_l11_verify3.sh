#!/usr/bin/env bash
# h2_l11_verify3.sh -- task h2: the conventions verifier over this
# task's own log AGAIN, after every transcript in it was replaced with
# lane h2_l9_evidence.sh's own blocks, each carrying the command that
# produced it.
#
# WHY A THIRD PASS: lane h2_l10's pass found 2 DIFFERS, both about a
# pasted transcript rather than about any claim's wording -- one command
# prints its own peak resident kB, which differs on every run, and one
# paste had carried the lane log's own footer lines into the block. The
# first is now pasted WITHOUT its command and attributed to the lane
# that first ran it; the second had its footer removed. The verifier is
# not modified here or anywhere.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H2; the verifier
# prints its own peak RSS.
set -euo pipefail
echo "[1/2] task h2: the conventions verifier over log 240"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 /projects/PseudoCoupHQ/DevComms/log_240_task_h2_two_printing_fixes.md
echo "[2/2] done"
