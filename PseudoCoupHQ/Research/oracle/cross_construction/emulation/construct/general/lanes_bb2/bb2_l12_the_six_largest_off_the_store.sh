#!/bin/bash
# bb2_l12_the_six_largest_off_the_store.sh -- task bb2, lane 12: the
# six-cell sample finished.  Lane 4 ran it as its own command and was
# cut inside it -- swiftc did not come back from a 74,674-line source
# and its own 600-second bound raised out of the run -- and the pass
# then ran every one of those cells on every target with the bound
# firing recorded as a row.  These are the same rows, off the store.
#
#   [1/2] the six largest cells, every place, every target
#   [2/2] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
total=2

i=1
echo "[$i/$total] the six largest cells, off the pass's own store"
timeout 1800 python3 "$G/bb2_run.py" largest 6
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
