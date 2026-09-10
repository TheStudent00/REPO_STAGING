#!/usr/bin/env bash
# rv3 lane 6 -- LEVEL 0 FOR THE FIVE NEW ROWS, re-run with the float
# unit enabled in the harness's prologue (lane rv3_l5 showed the model
# trapping without it, which is the model being right).  THIS IS A CHECK
# AT POINTS, NOT AN EQUALITY.  Sample first, then the brief's cap.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
export HOME=/work
mkdir -p /work/rv3sail2_sample /work/rv3sail2
total=2

echo "[1/$total] the sample: the five rows at 200 points each"
python3 "$RV/sail_points.py" "$RV/level0_points_rv3_sample" \
  /work/rv3sail2_sample --points 200 \
  --only add.uw,bseti,c.mul,c.zext.w,fsgnjn.d
echo "sample rc=$?"

echo "[2/$total] the five rows at the brief's cap of 20,000 points each"
python3 "$RV/sail_points.py" "$RV/level0_points_rv3" /work/rv3sail2 \
  --points 20000 --only add.uw,bseti,c.mul,c.zext.w,fsgnjn.d
echo "full rc=$?"

echo "-- the per-row tally, LITERAL"
python3 -c "
import json
d = json.load(open('$RV/level0_points_rv3.json'))
for r in d['rows']:
    print('%-10s %-24s variants %4d points %6d agree %6d disagree %5d'
          % (r['mnem'], r['outcome'], r['variants'], r['points'],
             r['agree'], r['disagree']))
print('points', sum(r['points'] for r in d['rows']),
      'agree', sum(r['agree'] for r in d['rows']),
      'disagree', sum(r['disagree'] for r in d['rows']))
"
echo "lane rv3_l6 done"
