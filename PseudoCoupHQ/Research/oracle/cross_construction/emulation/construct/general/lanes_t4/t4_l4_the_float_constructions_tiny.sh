#!/bin/bash
# t4_l4_the_float_constructions_tiny.sh -- task t4, lane 4: the constructions
# put to z3 at TINY widths, before any of them touches a cell.
#
# The obligation, one sentence: for one operation kind at one width `n`
# over one word `W`, is the construction the operation it replaces at
# every input?  z3 answers PROVED, DISPROVED or UNDECIDED, and a
# DISPROVED row is a defect in this task's own file which is fixed with
# the row shown, never worked around.
#
#   [1/3] the smoke: three (width, word) pairs a solver answers at once
#   [2/3] the float constructions at a TINY format (3 exponent bits, 4
#         significand bits), which is where a solver can decide a
#         softfloat at all
#   [3/3] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=3

i=1
echo "[$i/$total] THE CONSTRUCTIONS AT THE WIDTHS A SOLVER ANSWERS"
python3 "$G/check_constructions.py" narrow
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] THE FLOAT CONSTRUCTIONS AT A TINY FORMAT"
python3 "$G/check_constructions.py" float tiny
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
