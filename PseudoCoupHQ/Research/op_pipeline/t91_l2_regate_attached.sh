#!/usr/bin/env bash
# t91_l2_regate_attached.sh -- TASK 91, lane 2: the WHOLE canon38
# population re-gated through the ONE reference with the attached
# runtime callee bodies -- the reference exactly as it stands.
#
# POPULATION: all 30,436 units log 153 section 1.2 counts.  Not the
# 6,017 of the two moving buckets alone: the 23,132 already-proved
# units are re-gated too, because "zero regressions" is a measurement
# over them and not an assertion about them.
#
# THE MEMORY BOUND, stated before the run.
#   what is held:  one canon38 source document per shard process, its
#                  units transcribed one at a time.
#   measured:      461 MB peak resident size for one process over the
#                  200-unit sample of lane 1 (t91_sample.json).
#   cap:           6000 MB per process, abort named T91_MEMORY_ABORT,
#                  checked after every source document.
#   four shards run at once, so the lane's own ceiling is four times
#   one process; the sample says that is about 1.9 GB against the
#   instance's 10g.
#
# TIME: the sample measured 0.050 s/unit with one route short-circuited.
# This run puts BOTH routes to every unit, so the estimate is about
# 50 minutes for one process over 30,436 units and about 15 minutes
# over four shards.  The lane ceiling is 6 hours.
#
# Product: t91_regate_store_attached_callees_fix/ in the project tree.
set -uo pipefail

cd PseudoCoupHQ/Research/op_pipeline || exit 2

for i in 0 1 2 3; do
  python3 t91_regate_run.py --configuration=attached_callees \
      --label=fix --shard=$i/4 > /tmp/t91_l2_shard_$i.log 2>&1 &
done
wait

status=0
for i in 0 1 2 3; do
  echo "=================== shard $i/4 ==================="
  tail -6 /tmp/t91_l2_shard_$i.log
  if ! grep -q "finished" /tmp/t91_l2_shard_$i.log; then
    echo "SHARD $i DID NOT FINISH -- full log follows"
    cat /tmp/t91_l2_shard_$i.log
    status=4
  fi
done

echo ""
echo "store contents:"
ls t91_regate_store_attached_callees_fix | wc -l
exit $status
