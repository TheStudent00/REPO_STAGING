#!/usr/bin/env bash
# h1_l10_verify2.sh -- task h1: the law's final lane. Every claim of
# log 238 re-run inside this instance and sorted into matches /
# differs / unverifiable.
# MEMORY: the verifier's own; the task's bound is 4 GB with the named
# abort ABORT_MEMORY_H1.
set -euo pipefail
echo "[1/1] task h1: check_conventions_log_claims.py --verify over log 238"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_238_task_h1_handful_of_find_emulation_runs.md
