#!/usr/bin/env bash
# t83 lane 18 -- DOES A LOWER CEILING RESCUE THE HARD SHARDS?
#
# WHAT IS MEASURED SO FAR.  Under a 4096 MB ceiling the walk's peak
# sits at 3,887,352 kB -- pinned against the ceiling -- and the shards
# split into two kinds: op_units2_c_c0005 walked 94 records in 2 s,
# while op_units2_c_c0004 walked 24 records in 1112 s.  Six shards took
# 2234 s, which projects the remaining 316 at about 32 hours against a
# lane ceiling of six.
#
# THE HYPOTHESIS.  A heap held right at its ceiling collects
# constantly.  Lane 14 already saw the shape of this on an ordinary
# shard: 512 MB walked op_units2_c_c0002 in 90 s against 111 s at
# 4096 MB, with 99 of 99 records identical.  If the effect is much
# larger on a HARD shard, the ceiling is not only a memory bound but
# the schedule.
#
# THE TEST.  op_units2_c_c0004 is now in term66_store with a known
# cost of 1112 s at 4096 MB.  It is re-transcribed into SCRATCH under
# --check at three lower ceilings, so each run reports BOTH its wall
# time AND whether it reproduced the stored shard record for record.
# A ceiling that is faster but changes an answer is not a ceiling.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
i=0
for mb in 512 1024 2048; do
  i=$(( i + 1 ))
  echo
  echo "======== [$i/3] $mb MB -- op_units2_c_c0004.json (1112 s at 4096 MB) ========"
  rm -rf /work/t83_check_store /work/t83_check_state.json
  start=$(date +%s)
  python3 term66_bounded.py "$mb" 100000 --check \
    canon40_regen_store/op_units2_c_c0004.json
  rc=$?
  end=$(date +%s)
  echo "ceiling $mb MB: wall $(( end - start )) s, check exit $rc"
done
echo "[3/3] three ceilings timed on the hard shard"
exit 0
