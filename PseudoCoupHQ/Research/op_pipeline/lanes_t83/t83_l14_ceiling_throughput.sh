#!/usr/bin/env bash
# t83 lane 14 -- DOES THE CEILING SET THE SPEED?  probe83g measured one
# unit at five ceilings and the wall time rose monotonically with the
# ceiling: 0.52 s at 512 MB, 0.67 at 1024, 1.11 at 2048, 1.81 at 3072,
# 2.61 at 5120, with the record identical at all five.  If that holds
# over a whole shard, the ceiling is worth choosing carefully: the
# first full-run attempt spent four minutes on ONE shard at 4096 MB,
# which extrapolates past the lane's own six-hour ceiling.
#
# THE SHARD: op_units2_c_c0002.json, 99 records, which the host walked
# in 101 s (term66_run.log).  It is re-transcribed into SCRATCH under
# --check, three times, at three ceilings.  --check compares against
# the stored shard, so this lane also re-tests that the ceiling
# changes no record, on a c shard this time rather than a go one.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
for mb in 4096 1024 512; do
  echo
  echo "======== [$mb MB] op_units2_c_c0002.json ========"
  rm -rf /work/t83_check_store /work/t83_check_state.json
  start=$(date +%s)
  python3 term66_bounded.py "$mb" 100000 --check \
    canon40_regen_store/op_units2_c_c0002.json
  rc=$?
  end=$(date +%s)
  echo "ceiling $mb MB: wall $(( end - start )) s, check exit $rc"
done
echo "[1/1] three ceilings timed"
exit 0
