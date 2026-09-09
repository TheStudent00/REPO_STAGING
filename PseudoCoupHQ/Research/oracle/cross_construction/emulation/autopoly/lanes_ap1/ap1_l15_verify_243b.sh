#!/usr/bin/env bash
# ap1_l15_verify_243b.sh -- task ap1: the conventions verifier over this
# task's DevComms log, second pass, after five claims that had been
# attributions to a lane log were turned into commands that re-run.
#
# The obligation the law states is the DIFFERS column: zero, and a log
# fixed rather than a verifier. The first pass (lane
# `ap1_l13_verify_243.sh`) already returned zero; this pass measures
# what the five conversions moved.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_243_task_ap1_autopoly_first_full_loop.md
