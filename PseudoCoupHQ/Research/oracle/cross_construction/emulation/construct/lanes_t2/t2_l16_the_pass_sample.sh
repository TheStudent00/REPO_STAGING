#!/bin/bash
# t2_l16_the_pass_sample.sh -- task t2, lane 16: the plan, and the
# memory sample the law asks for before a pass runs.
#
# The pass walks every (cell, target) the bank certifies no proof for
# and puts each through BOTH routes: the native one, exactly as task ap6
# left it, and the second tier, whose places are written as a SECOND run
# carrying `route = constructed`.
#
# MEMORY: bound 6 GB resident, checked after EVERY store line, named
# abort ABORT_MEMORY_T2.  This lane is the sample: the first 20 store
# lines, with the peak pasted.
# CEILINGS: the gate's own 3,000 ms, one re-pose at 30,000 ms, and the
# equality's HARD 30,000 ms.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=2

i=1
echo "[$i/$total] THE PLAN"
python3 "$C/construct.py" preflight
echo

i=2
echo "[$i/$total] THE MEMORY SAMPLE: the first 20 store lines"
python3 "$C/construct.py" run 20
echo
echo "lane done"
