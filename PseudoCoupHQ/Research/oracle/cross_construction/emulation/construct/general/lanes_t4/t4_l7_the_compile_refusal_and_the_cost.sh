#!/bin/bash
# t4_l7_the_compile_refusal_and_the_cost.sh -- task t4, lane 7: the two
# things lane 6 left unstated, each read off the run itself.
#
# Lane 6 (`t4_l6_the_tier_on_five_cells.sh`) printed `compiled: False`
# with no sentence beside it, and was stopped by the operating system
# with no language-level error on the 128-bit divide.  Neither is a
# result.  This lane makes both into rows:
#   [1/4] `adc gpr_gpr 64` on go -- THE COMPILE REFUSAL, LITERAL
#   [2/4] `mul gpr_one 64` on go -- the same, at 13,438 statements
#   [3/4] `div gpr_one 64` on c -- the 128-bit divide under the render's
#         own resident bound (4 GB, under the task's 6 GB), so the cost
#         is a refusal BY NAME with the round it reached rather than an
#         ABORT with nothing in it
#   [4/4] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4; the render's
# own bound is 4 GB resident, read off /proc/self/statm.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=4

i=1
echo "[$i/$total] adc gpr_gpr 64 -> go, with the compile refusal"
timeout 900 python3 "$G/general.py" tier adc gpr_gpr 64 go
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] mul gpr_one 64 -> go, with the compile refusal"
timeout 1800 python3 "$G/general.py" tier mul gpr_one 64 go
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] div gpr_one 64 -> c, under the render's own resident bound"
timeout 3000 python3 "$G/general.py" tier div gpr_one 64 c
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
