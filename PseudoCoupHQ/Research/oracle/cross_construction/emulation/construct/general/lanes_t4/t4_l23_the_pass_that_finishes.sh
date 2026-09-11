#!/bin/bash
# t4_l23_the_pass_that_finishes.sh -- task t4, lane 23: THE
# MEASUREMENT, run with both of its bounds set from lane 20's own store
# rather than guessed.
#
# LANE 22's MEASUREMENT, and it is the last bound this pass states.
# Lane 22 ran with one gate call bounded at 30 s and was held for more
# than 44 minutes by ONE flag consumer -- a flag consumer carries one
# written place per setter cell, seventeen of them, and each place pays
# the whole bound twice -- with its attempt's own wall clock nearly
# spent.  A run longer than one attempt's budget stops the pass DEAD:
# every attempt starts it again and every attempt is cut inside it.
#
# TWO BOUNDS ARE RE-STATED, both off the pass's own store, and nothing
# else is changed.  ONE GATE CALL is bounded at 5 s, which is fifty
# times the slowest gate call that ANSWERED in 443 of them (0.099 s,
# median 0.011 s), so nothing that was going to answer is lost.  ONE
# WHOLE (cell, target) RUN is bounded at 900 s, and a run past it is
# left with its cause on the record while the pass goes on -- every
# store line it already wrote stays, because `autopoly.append_run`
# flushes each one.
#
# LANE 22's STORE IS KEPT AND NOT READ, as lane 16's and lane 20's were:
# its lines were written under the older bound, so it is moved aside as
# `t4_general_runs.jsonl.before_the_run_was_bounded` and this lane
# starts from nothing.  Nothing is deleted.
#
#   [1/3] the store lane 22 wrote, moved aside
#   [2/3] the pass, repeated until it stops adding lines
#   [3/3] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4, checked
# after every store line.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
A=$P/Research/oracle/cross_construction/emulation/autopoly
total=3

i=1
echo "[$i/$total] the stop file removed, and the store lane 22 wrote, moved aside"
if [ -f "$G/STOP_THE_PASS" ]; then
    cat "$G/STOP_THE_PASS"
    rm -f "$G/STOP_THE_PASS"
    echo "  the stop file is removed; the pass runs"
fi
if [ -f "$A/t4_general_runs.jsonl" ]; then
    wc -l "$A/t4_general_runs.jsonl"
    mv "$A/t4_general_runs.jsonl" \
       "$A/t4_general_runs.jsonl.before_the_run_was_bounded"
    echo "  moved to t4_general_runs.jsonl.before_the_run_was_bounded"
else
    echo "  no store to move"
fi

i=2
echo ""
echo "[$i/$total] the pass, repeated until it stops adding lines"
for k in 1 2 3 4 5 6 7 8; do
    before=0
    if [ -f "$A/t4_general_runs.jsonl" ]; then
        before=$(wc -l < "$A/t4_general_runs.jsonl")
    fi
    echo "  --- attempt $k, store lines before: $before ---"
    timeout 4800 python3 "$G/general.py" run
    echo "  exit: $?"
    after=0
    if [ -f "$A/t4_general_runs.jsonl" ]; then
        after=$(wc -l < "$A/t4_general_runs.jsonl")
    fi
    echo "  --- attempt $k, store lines after: $after ---"
    if [ "$after" = "$before" ]; then
        echo "  the attempt added nothing; the pass is done or stuck"
        break
    fi
done

i=3
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
