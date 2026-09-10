#!/usr/bin/env bash
# rv1 lane 13 -- section 5 counted again with lane_gen's carve found inside
# its own DRIVER string, then the spelling guard run over every json this
# task wrote, then `grep -c exempt` over every file it added.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
total=4

echo "[1/$total] the surface"
python3 $RV/surface.py $RV $OP $RV/surface

echo "[2/$total] the spelling guard over every json"
python3 $OP/check_no_spelling_keys.py $RV/units.json $RV/carved.json \
  $RV/claim.json $RV/level0_points.json $RV/level0_points_zicond.json \
  $RV/sail_smoke.json $RV/surface.json
echo "guard rc=$?"

echo "[3/$total] grep -c exempt over every file this task added"
for f in $RV/*.py $RV/*.json $RV/lanes_rv1/*.sh; do
  printf '%8s  %s\n' "$(grep -c exempt "$f")" "$f"
done

echo "[4/$total] the whole surface json, for the record"
python3 -c "
import json
d = json.load(open('$RV/surface.json'))
print(json.dumps(d['x86_counterpart'], indent=1, sort_keys=True))
"
python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
