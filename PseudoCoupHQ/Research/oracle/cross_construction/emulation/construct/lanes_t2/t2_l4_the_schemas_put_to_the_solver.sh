#!/bin/bash
# t2_l4_the_schemas_put_to_the_solver.sh -- task t2, lane 4: every
# schema in `construct/schemas.py` asked, on its own, whether the term
# it builds out of limbs of the word computes the same mapping as the
# operation it replaces.
#
# This runs BEFORE the tier touches a cell.  A schema that is wrong is
# wrong here, in one row naming the z3 declaration kind and the width,
# and not two hundred runs later inside a verdict about a cell.
#
#   [1/4] the narrow widths, whole, divider included -- these a solver
#         answers outright, so a defect is a counterexample
#   [2/4] the widths the pipeline meets (65, 96, 128 over a 64-bit
#         word), divider excluded
#   [3/4] the divider at widths a solver can still reach
#   [4/4] the divider's own SIZE against its width, which is the number
#         the tier refuses on
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2, checked
# after every row.  CEILING: 30,000 ms per obligation, the brief's hard
# one.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=4

i=1
echo "[$i/$total] THE NARROW WIDTHS, whole, divider included"
python3 "$C/check_schemas.py" narrow
echo

i=2
echo "[$i/$total] THE WIDTHS THIS PIPELINE MEETS, divider excluded"
python3 "$C/check_schemas.py" wide
echo

i=3
echo "[$i/$total] THE DIVIDER, at widths a solver can still reach"
python3 "$C/check_schemas.py" divider
echo

i=4
echo "[$i/$total] THE DIVIDER'S SIZE AGAINST ITS WIDTH"
python3 "$C/check_schemas.py" size
echo
echo "lane done"
