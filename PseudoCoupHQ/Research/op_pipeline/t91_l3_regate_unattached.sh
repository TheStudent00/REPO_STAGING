#!/usr/bin/env bash
# t91_l3_regate_unattached.sh -- TASK 91, lane 3: the whole canon38
# population (30,436 units) put to the ONE reference in configuration
# 'no_attached_callees', run label 'fix'.
#
# WHY A 'control' LABEL EXISTS.  gate.SOLVER_MILLISECONDS is a WALL
# CLOCK, so re-running UNCHANGED code can move a verdict.  A control
# run is the identical code over the identical population, and the
# movement between the two runs of one configuration is the wall-clock
# movement -- separated, and never folded into the movement the
# reference caused.
#
# THE MEMORY BOUND: one source document per shard process; 461 MB
# measured peak for one process (lane 1's sample); cap 6000 MB per
# process, abort named T91_MEMORY_ABORT, checked after every source
# document; four shards at once against the instance's 10g.
#
# Product: t91_regate_store_no_attached_callees_fix/ in the project tree.
set -uo pipefail

cd /projects/PseudoCoupHQ/Research/op_pipeline || exit 2

for i in 0 1 2 3; do
  python3 t91_regate_run.py --configuration=no_attached_callees \
      --label=fix --shard=$i/4 > /tmp/t91_l3_shard_$i.log 2>&1 &
done
wait

status=0
for i in 0 1 2 3; do
  echo "=================== shard $i/4 ==================="
  tail -6 /tmp/t91_l3_shard_$i.log
  if ! grep -q "finished" /tmp/t91_l3_shard_$i.log; then
    echo "SHARD $i DID NOT FINISH -- full log follows"
    cat /tmp/t91_l3_shard_$i.log
    status=4
  fi
done

echo ""
echo "store contents:"
ls t91_regate_store_no_attached_callees_fix | wc -l
exit $status
