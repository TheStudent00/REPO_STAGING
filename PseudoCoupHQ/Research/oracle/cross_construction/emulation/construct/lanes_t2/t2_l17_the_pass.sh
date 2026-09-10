#!/bin/bash
# t2_l17_the_pass.sh -- task t2, lane 17: THE PASS.  Every (cell,
# target) the bank certifies no proof for, through BOTH routes.
#
# Lane 16's store is moved beside itself rather than deleted: it was
# written before the tier stopped writing a second store line for a run
# where every place declined, and a store that holds two shapes of
# record is a store nobody can read.  Nothing under this folder is ever
# removed.
#
# MEMORY: bound 6 GB resident, checked after EVERY store line, named
# abort ABORT_MEMORY_T2; lane 16's twenty-run sample peaked at 258,740
# kB, which is 4% of the bound.
# CEILINGS: the gate's own 3,000 ms, one re-pose at 30,000 ms, the
# equality's HARD 30,000 ms, and the constructed term's own size ceiling
# of 200,000 nodes written out.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=2

i=1
echo "[$i/$total] lane 16's store, moved beside itself"
if [ -f "$C/t2_construct_runs.jsonl" ]; then
    mv "$C/t2_construct_runs.jsonl" \
       "$C/t2_construct_runs.jsonl.before_the_tier_stopped_writing_a_declined_run"
    echo "  moved: $(wc -l < "$C/t2_construct_runs.jsonl.before_the_tier_stopped_writing_a_declined_run") line(s)"
else
    echo "  no store to move"
fi
echo

i=2
echo "[$i/$total] THE PASS"
python3 "$C/construct.py" run
echo
echo "lane done"
