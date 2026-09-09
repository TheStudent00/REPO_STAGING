#!/usr/bin/env bash
# t93 lane 8 -- the planning tree checks, after this task's edits to two
# CORE files and two PROGRESS files. Nothing is written.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line. The candidate set for comparison comes from
# machine-form evidence or from ratified intention -- never from the
# token. The token appears exactly once per unit: as a display label on
# the member. MECHANICAL GUARD REQUIRED: every pipeline stage that groups
# or pairs units must run op_pipeline/check_no_spelling_keys.py and
# refuse its own output on failure.
set -u
echo "======== [1/1] check_plans.py over PseudoCoupHQ ========"
cd PseudoCoupHQ
python3 PlanPlan/framework/check_plans.py 2>&1 | tail -30
echo "   exit: $?"
echo
echo "======== lane 8 finished ========"
