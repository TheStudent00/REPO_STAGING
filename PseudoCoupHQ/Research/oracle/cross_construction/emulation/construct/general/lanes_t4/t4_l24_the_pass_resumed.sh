#!/bin/bash
# t4_l24_the_pass_resumed.sh -- task t4, lane 24: the pass carried on
# from where lane 23 left it, with both bounds enforced by INTERRUPTING
# THE SOLVER rather than by raising.
#
# LANE 23's TWO FINDINGS, and they are about the ENFORCEMENT and not
# about the bounds, which do not move.  A signal handler that raises
# lands in whatever Python frame is running, and on this pass that is
# constantly z3's own `AstRef.__del__`: Python IGNORES an exception
# raised in a `__del__`, so the bound fires and is thrown away -- the
# lane printed "Exception ignored in: AstRef.__del__ ...
# TheGateRanLong: 5 s" -- and raising through the solver's own C frames
# ended its attempt 1 with a `Segmentation fault`, exit 139, at run 109
# of 654.  `Context.interrupt` is z3's own way to stop a solver: the
# running `check` returns `unknown`, every later one returns quickly,
# the call comes back by itself, and nothing is raised anywhere.
#
# LANE 23's STORE IS KEPT AND CARRIED ON, not moved aside: its 851
# lines were written under the SAME two bounds (one gate call 5 s, one
# run 900 s) and only the way the bound is applied has changed, so the
# store is one measurement and the pass resumes into it.
#
# (Lane 23's third attempt added nothing and stopped, because the stop
# file it had removed was put back by a later mirror of the artifact
# folder.  That file is gone from the folder now.)
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
if [ -f "$G/STOP_THE_PASS" ]; then
    echo "  a stop file is present and is removed:"
    cat "$G/STOP_THE_PASS"
    rm -f "$G/STOP_THE_PASS"
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
