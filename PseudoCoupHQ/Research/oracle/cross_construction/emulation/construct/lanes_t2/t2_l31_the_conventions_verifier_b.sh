#!/bin/bash
# t2_l31_the_conventions_verifier_b.sh -- task t2, lane 31: lane 28 again, after five reproducing commands were put in the log: the
# conventions verifier over this task's log, run FROM this task's own
# instance as the law requires.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

V=PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py
L=PseudoCoupHQ/DevComms/log_257_task_t2_the_second_tier_constructs_what_a_target_lacks.md
total=1

i=1
echo "[$i/$total] THE CONVENTIONS VERIFIER"
python3 "$V" --verify --timeout 20 "$L"
echo
echo "lane done"
