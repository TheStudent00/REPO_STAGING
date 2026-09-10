#!/bin/bash
# t2_l7_the_tier_on_one_cell_b.sh -- task t2, lane 7: lane 6 again, after this pass's source folder was put under construct/ where its store is: the second tier put
# through, end to end, on the (cell, target) pairs lane 3 showed the
# renderer refusing, one at a time and printed.
#
# The walkthrough before the pass, which is the order this line works
# in: an object looked at whole before a population of them is counted.
# Four shapes, each a different schema:
#   the 65-bit carry (the ripple adder), the 128-bit funnel shift (the
#   shifter), the 128-bit high product (the multiplier) and the 128-bit
#   divide (the divider, which is where the size ceiling bites).
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
# CEILINGS: the gate's own 3,000 ms; the equality's HARD 30,000 ms.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=5

i=1
echo "[$i/$total] the plan, and the word of each target"
python3 "$C/construct.py" preflight
echo

i=2
echo "[$i/$total] the ripple adder: a 65-bit carry on go"
python3 "$C/construct.py" tier sbb gpr_gpr 64 go
echo

i=3
echo "[$i/$total] the shifter: a 128-bit funnel shift on go"
python3 "$C/construct.py" tier shld cl_gpr_gpr 64 go
echo

i=4
echo "[$i/$total] the multiplier: a 128-bit high product on swift"
python3 "$C/construct.py" tier mul gpr_one 64 swift
echo

i=5
echo "[$i/$total] the divider: a 128-bit divide on go"
python3 "$C/construct.py" tier div gpr_one 64 go
echo
echo "lane done"
