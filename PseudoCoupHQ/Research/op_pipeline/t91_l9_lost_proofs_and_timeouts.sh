#!/usr/bin/env bash
# t91_l9_lost_proofs_and_timeouts.sh -- TASK 91, lane 9: the two things
# the run's own numbers demand before the report can be written.
#
#   [1/3] THE 245 LOST PROOFS given a computed cause: the superseded
#         simulator's answer and the ONE reference's answer put to the
#         solver on the SAME body, and the units grouped by the shapes
#         of their own machine text.
#   [2/3] EVERY UNIT THAT HIT THE WALL CLOCK re-run with forty times
#         the room (120,000 ms against 3,000 ms), per the owner's rule of
#         2026-09-04, with the report saying whether the answer changed.
#   [3/3] the audit re-run, because its cause detector was corrected:
#         the first version split a `call` line on a space and lost the
#         RELOCATION, which is where an unlinked transfer's callee name
#         lives, so 2,969 disproofs came out with no computed cause.
#
# THE MEMORY BOUND: one canon38 source document at a time, then one
# unit at a time; cap 6000 MB per process, abort T91_MEMORY_ABORT.
#
# Products: t91_lost_proofs.json, t91_timeouts.json, t91_audit.json,
#           and the three printed transcripts beside them.
set -uo pipefail

cd PseudoCoupHQ/Research/op_pipeline || exit 2

echo "[1/3] the 245 lost proofs"
python3 t91_lost_proofs.py 2>&1 | tee t91_lost_proofs_printed.txt
one=${PIPESTATUS[0]}

echo ""
echo "[2/3] every unit that hit the wall clock, re-run at 120000 ms"
python3 t91_timeouts.py 120000 2>&1 | tee t91_timeouts_printed.txt
two=${PIPESTATUS[0]}

echo ""
echo "[3/3] the audit re-run with the corrected cause detector"
python3 t91_audit.py 2>&1 | tee t91_audit_printed.txt
three=${PIPESTATUS[0]}

echo ""
echo "exit codes: lost_proofs=$one timeouts=$two audit=$three"
if [ "$one" -ne 0 ] || [ "$two" -ne 0 ] || [ "$three" -ne 0 ]; then
  exit 8
fi
