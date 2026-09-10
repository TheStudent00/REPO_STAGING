#!/bin/bash
# bank1_l13_verify_253.sh -- task bank1, lane 13.
#
# THE FINAL LANE THE LAW REQUIRES: the conventions verifier re-runs
# every command the log carries above a fenced block and sorts each
# claim into matches / differs / unverifiable.  The obligation is ZERO
# DIFFERS, and the fix for a DIFFERS is the log or the claim, never the
# verifier.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

OP=PseudoCoupHQ/Research/op_pipeline
L=PseudoCoupHQ/DevComms/log_253_task_bank1_the_bank.md
total=1

i=1
echo "[$i/$total] the conventions verifier over log 253"
python3 "$OP/check_conventions_log_claims.py" --verify --timeout 20 "$L"
echo "  verifier exit: $?"
echo
echo "lane done"
