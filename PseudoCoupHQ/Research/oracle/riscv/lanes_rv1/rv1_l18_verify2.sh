#!/usr/bin/env bash
# rv1 lane 18 -- the law's final lane: the conventions/claims verifier over
# this task's DevComms log, run from this task's own instance, plus the
# spelling guard once more over every json and the `grep -c exempt` count
# over every file this task added.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
LOG=PseudoCoupHQ/DevComms/log_258_task_rv1_riscv_as_a_second_architecture.md
export HOME=/work
total=3

echo "[1/$total] the verifier"
python3 $OP/check_conventions_log_claims.py --verify --timeout 20 $LOG
echo "verifier rc=$?"

echo "[2/$total] the spelling guard, once more"
python3 $OP/check_no_spelling_keys.py $RV/units.json $RV/carved.json \
  $RV/claim.json $RV/level0_points.json $RV/level0_points_zicond.json \
  $RV/sail_smoke.json $RV/surface.json
echo "guard rc=$?"

echo "[3/$total] the count the law asks for, over every file this task added"
for f in $RV/*.py $RV/*.json $RV/*.md $RV/lanes_rv1/*.sh; do
  printf '%8s  %s\n' "$(grep -c exempt "$f")" "$f"
done

python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
