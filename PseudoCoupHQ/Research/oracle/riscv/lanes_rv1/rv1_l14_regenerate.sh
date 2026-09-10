#!/usr/bin/env bash
# rv1 lane 14 -- every artifact regenerated after the row field carrying the
# source operator token was renamed to the guard's own allowed name, then
# the spelling guard over every json again, then the surface counted over
# the final files.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
export GOCACHE=/work/rv1gocache GOPATH=/work/rv1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv1carve
total=5

echo "[1/$total] the ten units"
python3 $RV/pick_units.py $OP $RV/units.json

echo "[2/$total] compile for riscv64 and carve"
python3 $RV/riscv_carve.py $RV/units.json $RV/carved.json /work/rv1carve

echo "[3/$total] the claim"
python3 $RV/claim_check.py $OP $RV/units.json $RV/carved.json $RV/claim

echo "[4/$total] the surface"
python3 $RV/surface.py $RV $OP $RV/surface

echo "[5/$total] the spelling guard over every json"
python3 $OP/check_no_spelling_keys.py $RV/units.json $RV/carved.json \
  $RV/claim.json $RV/level0_points.json $RV/level0_points_zicond.json \
  $RV/sail_smoke.json $RV/surface.json
echo "guard rc=$?"

python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
