#!/bin/bash
# t4_l22_the_pass_at_the_measured_bound.sh -- task t4, lane 22: THE
# MEASUREMENT, run with both of its bounds set from lane 20's own store
# rather than guessed.
#
# LANE 20's TWO MEASUREMENTS, off the 712 store lines its first 93 runs
# wrote.
#
# FIRST, the gate's own time. Of the 443 gate calls that ANSWERED, the
# slowest took 0.099 s and the median 0.011 s. The calls that run long
# do not run a little long: they run past any bound this task could
# state. So one gate call is bounded at 30 s -- three hundred times the
# slowest answer on record, and the brief's own hard ceiling for the
# equality, so the two bounds are one number.
#
# SECOND, the cost of running both policies at every place. A flag
# consumer carries one written place per setter cell -- `setl gpr_one 8`
# has seventeen -- and where the gate runs long each of them costs its
# whole bound twice over: that one (cell, target) took 2,046 s. The
# brief's rule is "whoever gets there first", so `all_constructed` is
# now attempted only at a place `native_first` did not PROVE, which is
# exactly where the GUARANTEE is the question.
#
# LANE 20's STORE IS KEPT AND NOT READ, as lane 16's was: its lines were
# written under a 120 s bound with both policies always run, so it is
# moved aside as `t4_general_runs.jsonl.before_the_bounds_were_measured`
# and this lane starts from nothing. Nothing is deleted.
#
#   [1/3] the store lane 20 wrote, moved aside
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
echo "[$i/$total] the stop file removed, and the store lane 20 wrote, moved aside"
if [ -f "$G/STOP_THE_PASS" ]; then
    cat "$G/STOP_THE_PASS"
    rm -f "$G/STOP_THE_PASS"
    echo "  the stop file is removed; the pass runs"
fi
if [ -f "$A/t4_general_runs.jsonl" ]; then
    wc -l "$A/t4_general_runs.jsonl"
    mv "$A/t4_general_runs.jsonl" \
       "$A/t4_general_runs.jsonl.before_the_bounds_were_measured"
    echo "  moved to t4_general_runs.jsonl.before_the_bounds_were_measured"
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
