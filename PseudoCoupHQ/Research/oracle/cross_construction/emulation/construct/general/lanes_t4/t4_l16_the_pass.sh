#!/bin/bash
# t4_l16_the_pass.sh -- task t4, lane 16: THE MEASUREMENT ITSELF -- the
# loop run with this tier in place of task t2's eight schemas, over
# every (cell, target) the bank holds no proved certificate for.
#
# The preflight (lane 9 step [6/7]) reads: 2,159 keys the bank
# certifies, 4,080 keys with no such certificate, 0 held back by the
# code version -- the tier's own bytes are this pass's loop version, so
# every uncertified key is attempted because the machinery HAS moved --
# and 665 (cell, target) runs to execute.
#
# THE STORE IS WRITTEN LINE BY LINE (`autopoly.append_run`) and the run
# skips what is already on it, so this lane is resumable: a lane that
# runs out of wall clock leaves every line it wrote and the next lane
# carries on from there.
#
#   [1/3] the tier on one cell first: `adc gpr_gpr 64` on go, which
#         lanes 6, 7, 8, 9 and 10 all lost to the canonical form's
#         printed size before the form was declined wherever the render
#         constructed anything
#   [2/3] the pass
#   [3/3] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4, checked
# after every store line; the render's own bound is 4 GB resident and
# the solver's is 4 GB.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=3

i=1
echo "[$i/$total] the tier on adc gpr_gpr 64 -> go"
timeout 600 python3 "$G/general.py" tier adc gpr_gpr 64 go
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the pass"
timeout 18000 python3 "$G/general.py" run
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
