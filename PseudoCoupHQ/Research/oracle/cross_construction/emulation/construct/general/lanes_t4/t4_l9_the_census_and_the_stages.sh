#!/bin/bash
# t4_l9_the_census_and_the_stages.sh -- task t4, lane 9: the operation
# kinds the two stores actually use, and the tier's cost located stage
# by stage.
#
# Lane 8 corrected the go symbol and left two things open: the adder and
# the multiplier through go were stopped by the lane's own wall clock,
# and the 128-bit divide through c was stopped by the operating system
# AFTER the native route -- so the cost is in the general tier and the
# render's own resident bound did not fire, which says it is not in the
# construction's rounds.  This lane stops at each stage and prints what
# was built.
#
#   [1/7] the census: every (operation kind, width) the x86 and riscv64
#         stores use, counted -- the brief's own definition of
#         `operation kind`, read off the stores rather than recalled
#   [2/7] `div gpr_one 64` on c, RENDER ONLY
#   [3/7] `div gpr_one 64` on c, render and COMPILE, no gate
#   [4/7] `mul gpr_one 64` on go, render and compile, no gate
#   [5/7] `adc gpr_gpr 64` on go, the whole tier, with the canonical
#         form now bounded by node count
#   [6/7] the preflight: what the pass would attempt
#   [7/7] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4; the render's
# own bound is 4 GB resident, read off /proc/self/statm.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=7

i=1
echo "[$i/$total] THE CENSUS: every (operation kind, width) the two stores use"
timeout 1200 python3 "$G/check_constructions.py" census
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] div gpr_one 64 -> c, RENDER ONLY"
timeout 900 python3 "$G/general.py" probe div gpr_one 64 c render
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] div gpr_one 64 -> c, render and COMPILE, no gate"
timeout 1800 python3 "$G/general.py" probe div gpr_one 64 c compile
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] mul gpr_one 64 -> go, render and COMPILE, no gate"
timeout 1800 python3 "$G/general.py" probe mul gpr_one 64 go compile
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] adc gpr_gpr 64 -> go, the whole tier"
timeout 900 python3 "$G/general.py" tier adc gpr_gpr 64 go
echo "  exit: $?"

i=6
echo ""
echo "[$i/$total] the preflight: what the pass would attempt"
timeout 1800 python3 "$G/general.py" preflight
echo "  exit: $?"

i=7
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
