#!/usr/bin/env bash
# ap1_l17_verify_243d.sh -- task ap1: the conventions verifier over this
# task's DevComms log, FOURTH pass, over the log as it now stands with
# its own section 14 (the verifier's three earlier passes, their tally,
# and each non-matching outcome named with its cause) appended.
#
# That section adds prose and one table and no command, so what this
# pass measures is that appending it moved nothing but the line numbers
# and the UNVERIFIABLE count.
#
# The obligation the law states is the DIFFERS column: zero, and a log
# fixed rather than a verifier.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_243_task_ap1_autopoly_first_full_loop.md
