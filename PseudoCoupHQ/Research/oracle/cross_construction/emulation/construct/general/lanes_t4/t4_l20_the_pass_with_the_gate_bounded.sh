#!/bin/bash
# t4_l20_the_pass_with_the_gate_bounded.sh -- task t4, lane 20: THE
# MEASUREMENT ITSELF, run again with one gate call bounded by the wall
# clock and with a place whose gate was never asked carrying no gate
# record.
#
# LANE 16's TWO FINDINGS. First, the pass reached run 62 of 665 in about
# ten minutes and ended there on `KeyError: 'check'` inside
# `handful.verdict_of_run`, which reads a place's gate record
# unconditionally: a place that rendered and compiled and whose gate was
# never asked has none. That place is now recorded with `not_gated` and
# its cause, which is what `bank.kind_of_place` already reads as
# `refused` -- "never reached the gate at all", in its own words -- and
# the progress line answers for it instead of raising. Second, `adc
# gpr_gpr 64` on go did not come back from the gate inside 600 s, twice,
# so one gate call is now bounded at 120 s by `signal.alarm`, which
# raises in the Python frame and therefore bounds HOW MANY solver calls
# are asked rather than one of them -- one of them is already bounded at
# the gate's own 3,000 ms.
#
# LANE 16's STORE IS KEPT AND NOT READ. Its 61 runs were produced by the
# code before both changes, so it is moved aside as
# `t4_general_runs.jsonl.before_the_gate_carried_its_own_record` and
# this lane's pass starts from nothing. Nothing is deleted.
#
#   [1/4] the store lane 16 wrote, moved aside
#   [2/4] `adc gpr_gpr 64` on go, the cell that ran long twice
#   [3/4] the pass, repeated until it stops adding lines
#   [4/4] peak resident
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
total=4

i=1
echo "[$i/$total] the store lane 16 wrote, moved aside"
if [ -f "$A/t4_general_runs.jsonl" ]; then
    wc -l "$A/t4_general_runs.jsonl"
    mv "$A/t4_general_runs.jsonl" \
       "$A/t4_general_runs.jsonl.before_the_gate_carried_its_own_record"
    echo "  moved to t4_general_runs.jsonl.before_the_gate_carried_its_own_record"
else
    echo "  no store to move"
fi

i=2
echo ""
echo "[$i/$total] adc gpr_gpr 64 -> go, the cell that ran long twice"
timeout 900 python3 "$G/general.py" tier adc gpr_gpr 64 go
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the pass, repeated until it stops adding lines"
for k in 1 2 3 4 5 6; do
    before=0
    if [ -f "$A/t4_general_runs.jsonl" ]; then
        before=$(wc -l < "$A/t4_general_runs.jsonl")
    fi
    echo "  --- attempt $k, store lines before: $before ---"
    timeout 5400 python3 "$G/general.py" run
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

i=4
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
