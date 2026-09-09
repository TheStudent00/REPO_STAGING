#!/usr/bin/env bash
# ap1_l18_verify_243e.sh -- task ap1: the conventions verifier over this
# task's DevComms log, FIFTH and closing pass: over the log with section
# 14's own fourth-pass row written into it, so the tally the log prints
# is checked against the log as it finally stands rather than against
# the version that was verified before that row existed.
#
# The row and the paragraph beside it are prose and carry no command, so
# what this pass measures is that writing them moved nothing but the
# line numbers and one UNVERIFIABLE count.
#
# The obligation the law states is the DIFFERS column: zero, and a log
# fixed rather than a verifier.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_243_task_ap1_autopoly_first_full_loop.md
