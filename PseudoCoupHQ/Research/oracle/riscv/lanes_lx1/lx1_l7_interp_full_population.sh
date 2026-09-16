#!/bin/bash
# lx1_l7_interp_full_population.sh -- task lx1, lane 7: THE WHOLE
# POPULATION -- 255 RISC-V cells x the seven interpreted targets =
# 1,785 runs, first pass at 60 s per run (task ex2's own bound).
# Resumable: `rv_interp.py run` skips any (cell, lang) already on the
# store, so a lane stopped partway loses nothing and a re-submission
# of this same script finishes what is left. No network.
#
#   [1/2] the loop, repeated until an attempt adds no store line
#   [2/2] the counts so far
set -u

HQ=PseudoCoupHQ
RV="$HQ/Research/oracle/riscv"
PREFIX="$RV/lx1_interp_runs"
SRC="$RV/interp_src_lx1"
total=2

i=1
echo "[$i/$total] the loop, repeated until an attempt adds no store line"
before=0
if [ -f "$PREFIX.jsonl" ]; then before=$(wc -l < "$PREFIX.jsonl"); fi
for attempt in 1 2 3 4 5 6 7 8; do
  echo ""
  echo "  ---- attempt $attempt, store lines before: $before ----"
  timeout 18000 python3 "$RV/rv_interp.py" run "$RV/twins.json" \
    "$RV/model_table_rv.json" "$PREFIX" "$SRC" 60
  echo "  exit: $?"
  after=0
  if [ -f "$PREFIX.jsonl" ]; then after=$(wc -l < "$PREFIX.jsonl"); fi
  echo "  store lines after: $after"
  if [ "$after" -ge 1785 ]; then
    echo "  the whole population is on the store: the loop is done"
    break
  fi
  if [ "$after" = "$before" ]; then
    echo "  the attempt added no store line: the loop is done"
    break
  fi
  before=$after
done

i=2
echo ""
echo "[$i/$total] the counts so far"
wc -l "$PREFIX.jsonl"
python3 -c "
import json
counts = {}
for line in open('$PREFIX.jsonl'):
    row = json.loads(line)
    key = (row.get('lang'), row.get('outcome'))
    counts[key] = counts.get(key, 0) + 1
for key in sorted(counts):
    print(key, counts[key])
"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
