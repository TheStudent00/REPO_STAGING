#!/bin/bash
# bb2_l11_the_alarms_by_the_banks_own_kind.sh -- task bb2, lane 11: the
# alarm count read the way the BANK reads a place, and the three
# readings and the routes re-printed for the record.
#
# THE THIRD DEFECT OF THIS TASK'S OWN, found by lane 10's own output.
# Lane 10 counted 294 alarms off the gate's RAW outcome.  A gate that
# answers DISPROVED and whose caller-extension re-pose then proves is
# banked `proved_under_caller_extension` -- a proof on the region the
# caller guarantees, which is task o7's rule and every pass's -- and
# the counterexamples lane 10 printed are exactly that shape
# (`[IN_1 = 4294901760, IN_0 = 0]`: the bits ABOVE the place's own
# width).  An alarm is a place the bank would record `sat`, and
# `bank.kind_of_place` is the reading.
#
#   [1/3] the alarms, by the bank's own kind
#   [2/3] the three routes and this route's outcomes, for the record
#   [3/3] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
total=3

i=1
echo "[$i/$total] the alarms, by the bank's own kind"
timeout 1800 python3 "$G/bb2_run.py" alarms
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the three routes and this route's outcomes"
timeout 1800 python3 "$G/bb2_run.py" table
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
