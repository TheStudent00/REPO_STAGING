#!/bin/bash
# bb2_l2_the_six_cell_sample_and_the_interpreted_cost.sh -- task bb2,
# lane 2: the six largest circuits of the population taken ALL THE WAY
# THROUGH on all five compiled targets, with the sizes and the seconds
# pasted; and what one interpreted gate run costs, so this task's
# interpreted work ceiling is a number read off a run.
#
# The six are chosen by CIRCUIT SIZE off lane 1's own sizes file --
# machine-form evidence, measured, never a reading of a name.  Lane 1
# says the largest is `idiv gpr_one 32` at 74,786 gates and the
# twentieth is `sbb gpr_gpr 64` at 2,638.
#
#   [1/4] the sample: the six largest cells, every place, every target
#   [2/4] one SMALL interpreted run, timed, on the slowest runner
#   [3/4] one LARGE interpreted run, timed, on the slowest runner
#   [4/4] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BB2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
total=4

i=1
echo "[$i/$total] the six largest circuits, every place, every target"
timeout 14400 python3 "$G/bb2_run.py" sample 6
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] one SMALL interpreted gate run, timed"
timeout 1200 python3 "$G/bb2_run.py" interp_one add gpr_gpr 32 cpython
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] one LARGER interpreted gate run, timed"
timeout 1200 python3 "$G/bb2_run.py" interp_one add gpr_gpr 64 cpython
echo "  exit: $?"
timeout 1200 python3 "$G/bb2_run.py" interp_one imul gpr_gpr 32 cpython
echo "  exit: $?"
timeout 1200 python3 "$G/bb2_run.py" interp_one add gpr_gpr 64 java
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
