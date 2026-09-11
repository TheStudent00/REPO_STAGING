#!/bin/bash
# t4_l26_the_pass_past_what_it_cannot_finish.sh -- task t4, lane 26: the
# pass carried on past the one (cell, target) that stops it.
#
# LANES 23 AND 24 BOTH ENDED THE SAME WAY: `setg gpr_one 8` on rust did
# not come out inside an attempt's own wall clock, and because the lane
# repeats the pass and stops when an attempt adds no store line, every
# attempt started that run again, was cut inside it, and nothing after
# it was ever reached.  851 of the store's lines and 570 of the 654
# runs were already on the store; the remaining 84 were unreachable.
#
# THE MECHANISM, and it is written down rather than a list somebody
# chose: a run is WRITTEN DOWN before it starts (`t4_general_in_flight
# .json`) and rubbed out after it finishes.  What is left written down
# when an attempt is cut is exactly the run that was in flight, so the
# next attempt moves it to `t4_general_left_behind.json`, records it
# with its cause, and goes past it.  Nothing is deleted and nothing is
# chosen.
#
#   [1/3] what the store holds before
#   [2/3] the pass, repeated until it stops adding lines
#   [3/3] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
A=$P/Research/oracle/cross_construction/emulation/autopoly
total=3

i=1
echo "[$i/$total] what the store holds before"
wc -l "$A/t4_general_runs.jsonl" || true

i=2
echo ""
echo "[$i/$total] the pass, repeated until it stops adding lines"
for k in 1 2 3 4 5 6 7 8 9 10; do
    before=0
    if [ -f "$A/t4_general_runs.jsonl" ]; then
        before=$(wc -l < "$A/t4_general_runs.jsonl")
    fi
    echo "  --- attempt $k, store lines before: $before ---"
    timeout 2400 python3 "$G/general.py" run
    echo "  exit: $?"
    after=0
    if [ -f "$A/t4_general_runs.jsonl" ]; then
        after=$(wc -l < "$A/t4_general_runs.jsonl")
    fi
    echo "  --- attempt $k, store lines after: $after ---"
    if [ "$after" = "$before" ] && [ ! -f "$A/t4_general_in_flight.json" ]; then
        echo "  the attempt added nothing and left nothing in flight; the pass is done"
        break
    fi
done

i=3
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
