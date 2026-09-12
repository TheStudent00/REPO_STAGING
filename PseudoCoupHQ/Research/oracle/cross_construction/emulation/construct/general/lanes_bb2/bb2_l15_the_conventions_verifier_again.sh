#!/bin/bash
# bb2_l15_the_conventions_verifier_again.sh -- task bb2, lane 15: the
# conventions verifier over this task's own log after the two DIFFERS
# lane 13 read were fixed IN THE LOG (§10.3).  This tally is the one of
# record.
#
#   [1/2] the verifier, whole output
#   [2/2] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
OP="$HQ/Research/op_pipeline"
LOG="$HQ/DevComms/log_269_bb2_the_bit_blast_route_on_x86_and_the_interpreted_seven.md"
total=2

i=1
echo "[$i/$total] the conventions verifier over $LOG"
timeout 7200 python3 "$OP/check_conventions_log_claims.py" --verify --timeout 20 "$LOG"
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
