#!/bin/bash
# t4_l6_the_tier_on_five_cells.sh -- task t4, lane 6: the general tier
# end to end on five cells, printed, before any pass is run.
#
# Each is chosen for what it exercises, and each is a cell the bank
# holds NO proof for on that target:
#   [1/6] `adc gpr_gpr 64` on go -- a 65-bit node over a 64-bit word:
#         task t2's own walkthrough cell, so the two tiers can be read
#         side by side
#   [2/6] `div gpr_one 64` on c -- an unsigned divide at 128 bits: the
#         shape task t2 could not RENDER at any real width, because the
#         old renderer wrote a term whose steps read their own previous
#         step three times once per read
#   [3/6] `mul gpr_one 64` on go -- the high half of a product
#   [4/6] `shld cl_gpr_gpr 64` on swift -- a shift by a symbolic count
#   [5/6] `divsd xmm_xmm 64` on go -- a float divide
#   [6/6] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=6

i=1
echo "[$i/$total] adc gpr_gpr 64 -> go"
timeout 900 python3 "$G/general.py" tier adc gpr_gpr 64 go
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] div gpr_one 64 -> c"
timeout 1800 python3 "$G/general.py" tier div gpr_one 64 c
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] mul gpr_one 64 -> go"
timeout 1800 python3 "$G/general.py" tier mul gpr_one 64 go
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] shld cl_gpr_gpr 64 -> swift"
timeout 900 python3 "$G/general.py" tier shld cl_gpr_gpr 64 swift
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] divsd xmm_xmm 64 -> go"
timeout 1800 python3 "$G/general.py" tier divsd xmm_xmm 64 go
echo "  exit: $?"

i=6
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
