#!/bin/bash
# rv4_l3_the_sample_again_after_the_two_defects.sh -- task rv4, lane 3: the
# sample re-run after the first round (lane `rv4_l2`) measured two defects
# in this task's own driver, and a wider cost probe so the round's own
# clock is spent on runs rather than on one term's printing.
#
# THE TWO DEFECTS THE FIRST ROUND MEASURED, both in `rv4_off.py` and
# neither in the machinery it calls:
#   1. `os.makedirs(src_dir)` raced: eight workers made the same directory
#      in the same moment and the loser ABORTED before its first pair
#      (`FileExistsError: [Errno 17] File exists`).
#   2. The identical-text shortcut was bounded by the DISTINCT NODE COUNT,
#      which bounds nothing about printing: z3's printer expands the shared
#      graph into a tree and recurses per level, so a deep term spent the
#      whole budget and then raised
#      `ctypes.ArgumentError: argument 1: RecursionError` -- thirty times
#      in worker 4 alone.  The shortcut is now bounded by PRINTED SIZE and
#      DEPTH as well, and a pair that raises is a refused row rather than
#      the end of a worker.
#
#   [1/3] the five-pair sample, the same five, after the fix
#   [2/3] the wider cost probe: twenty-four pairs spread over the
#         population, each with its own seconds
#   [3/3] peak resident
#
# MEMORY: bound 6 GB resident per worker, named abort ABORT_MEMORY_RV4.
#
# Node: hq.research.arch_unit_oracle.architectures.riscv64
# Brief: Research/briefs/task_rv4_brief.md
set -u

P=PseudoCoupHQ
RV=$P/Research/oracle/riscv
export HOME=/work
export GOCACHE=/work/rv4gocache GOPATH=/work/rv4gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv4work2
total=3

i=1
echo "[$i/$total] the five-pair sample, the same five, after the fix"
timeout 900 python3 "$RV/rv4_off.py" sample "$P" \
  "$RV/rv4_population.json" 5 "$RV/rv4_sample_again" \
  "$RV/src_rv4_sample" /work/rv4work2
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the wider cost probe: twenty-four pairs spread over the population"
timeout 1800 python3 "$RV/rv4_off.py" sample "$P" \
  "$RV/rv4_population.json" 24 "$RV/rv4_cost_probe" \
  "$RV/src_rv4_sample" /work/rv4work2
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
