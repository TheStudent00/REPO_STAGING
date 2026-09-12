#!/bin/bash
# bb2_l1_the_stores_the_sizes_and_the_swift_probe.sh -- task bb2, lane 1:
# what this task reads, what the circuits cost before anything is
# compiled, and the probe for a Swift SDK for riscv64 linux.
#
# The sizes command blasts every written place of every attested x86
# cell -- 253 cells, the places the driver reaches -- and compiles
# NOTHING and gates NOTHING.  It is the cheap half of the task and it
# runs first, because it is what says where the expensive end is, and
# the expensive end is then what lane 2's sample takes all the way
# through.
#
#   [1/6] the sha256 of every store this task reads
#   [2/6] the files this task adds, read back by python so a syntax
#         error is a lane step and not a pass ABORTED at run 400
#   [3/6] the preflight: the bank's delta beside this pass's whole
#         population
#   [4/6] the sizes, every place, nothing compiled
#   [5/6] THE PROBE, LITERAL: is there a Swift SDK for riscv64 linux
#   [6/6] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BB2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
A="$HQ/Research/oracle/cross_construction/emulation/autopoly"
total=6

i=1
echo "[$i/$total] the sha256 of every store this task reads"
sha256sum \
  "$HQ/Research/op_pipeline/reference.py" \
  "$A/autopoly5_cells.json" \
  "$A/certificates.jsonl" \
  "$A/bank.py" \
  "$A/autopoly.py" \
  "$HQ/Research/oracle/cross_construction/emulation/handful/handful.py" \
  "$HQ/Research/oracle/cross_construction/emulation/handful/handful_frozen.py" \
  "$HQ/Research/oracle/cross_construction/emulation/interp/interp_check.py" \
  "$HQ/Research/oracle/cross_construction/emulation/interp/interp_render.py" \
  "$HQ/Research/oracle/cross_construction/emulation/interp/dialects.py" \
  "$G/general.py" "$G/render_general.py" "$G/bitblast.py" "$G/bb2_run.py"
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the two files this task adds or extends, read back"
python3 -c "import py_compile,sys
for one in ['$G/bb2_run.py','$G/bitblast.py']:
    py_compile.compile(one, doraise=True)
    print('  compiles: %s' % one)
"
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the preflight"
timeout 900 python3 "$G/bb2_run.py" preflight
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] the sizes: every written place blasted, nothing compiled"
timeout 7200 python3 "$G/bb2_run.py" sizes
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] THE PROBE: a Swift SDK for riscv64 linux, LITERAL"
timeout 1200 python3 "$G/bb2_run.py" swift_riscv
echo "  exit: $?"

i=6
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
