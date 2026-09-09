#!/usr/bin/env bash
# ap1_l13_verify_243.sh -- task ap1: the conventions verifier over this
# task's DevComms log, run from this task's own instance as the law
# requires.
#
# The verifier re-runs every command the log pastes and sorts each claim
# into matches / differs / unverifiable. The obligation the law states
# is the DIFFERS column: zero, and a log fixed rather than a verifier.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1. The
# verifier runs the log's own commands, each of which reads at most the
# 5 MB aggregate.
set -euo pipefail
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_243_task_ap1_autopoly_first_full_loop.md
