#!/bin/bash
# t4_l29_the_verifier.sh -- task t4, lane 29: the log's own claims put to
# the conventions verifier, which is the law's last lane.
#
#   [1/2] `check_conventions_log_claims.py --verify --timeout 20` over
#         this task's log
#   [2/2] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

P=PseudoCoupHQ
total=2

i=1
echo "[$i/$total] the verifier over log_262"
timeout 3600 python3 "$P/Research/op_pipeline/check_conventions_log_claims.py" \
  --verify --timeout 20 \
  "$P/DevComms/log_262_t4_the_general_construction_tier.md"
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
