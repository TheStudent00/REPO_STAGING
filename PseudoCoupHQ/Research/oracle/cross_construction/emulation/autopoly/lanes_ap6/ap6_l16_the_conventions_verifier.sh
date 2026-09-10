#!/bin/bash
# ap6_l16_the_conventions_verifier.sh -- task ap6, lane 16.
#
# WHAT THIS LANE DOES: it re-runs every command `log_255` pasted, from
# this task's own instance, and prints the tally.  The law asks for zero
# DIFFERS; a DIFFERS is fixed in the log or in the claim and never in
# the verifier.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_AP6.  The
# verifier runs each command with its own 20 s ceiling.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

OP=PseudoCoupHQ/Research/op_pipeline
LOG=PseudoCoupHQ/DevComms/log_255_task_ap6_one_versioned_driver.md
total=1

echo "[1/$total] the conventions verifier over log_255"
python3 "$OP/check_conventions_log_claims.py" --verify --timeout 20 "$LOG"
echo
echo "lane done"
