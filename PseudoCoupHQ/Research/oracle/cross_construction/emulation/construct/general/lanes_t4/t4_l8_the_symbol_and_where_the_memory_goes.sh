#!/bin/bash
# t4_l8_the_symbol_and_where_the_memory_goes.sh -- task t4, lane 8: the
# go symbol spelling corrected, and the 128-bit divide's cost located.
#
# Lane 7 gave both causes as rows.  THE FIRST is corrected here: go's
# linked executable spells a package function `main.<name>` and this
# task's render returned the bare name, so every go source it wrote
# built and then carved to nothing.  THE SECOND is not yet located --
# the render's own resident bound did not fire, so the memory is not in
# the construction's rounds nor in its statements, and this lane prints
# the resident reading on either side of each route to say which one it
# is in.
#
#   [1/5] `adc gpr_gpr 64` on go -- the same cell lane 6 and 7 ran
#   [2/5] `mul gpr_one 64` on go -- 13,438 statements through go
#   [3/5] `shl cl_gpr 64` on swift -- a barrel shift through swift
#   [4/5] `div gpr_one 64` on c -- the resident reading per route
#   [5/5] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4; the render's
# own bound is 4 GB resident, read off /proc/self/statm.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=5

i=1
echo "[$i/$total] adc gpr_gpr 64 -> go"
timeout 900 python3 "$G/general.py" tier adc gpr_gpr 64 go
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] mul gpr_one 64 -> go"
timeout 1800 python3 "$G/general.py" tier mul gpr_one 64 go
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] shl cl_gpr 64 -> swift"
timeout 1800 python3 "$G/general.py" tier shl cl_gpr 64 swift
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] div gpr_one 64 -> c, the resident reading per route"
timeout 3000 python3 "$G/general.py" tier div gpr_one 64 c
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
