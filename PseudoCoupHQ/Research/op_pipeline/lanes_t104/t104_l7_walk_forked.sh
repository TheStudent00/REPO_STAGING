#!/usr/bin/env bash
# t104 lane 7 -- THE RE-NORMALIZATION WALK, one forked sub-process per
# unit.
#
# Lane 3 walked in a single process and stopped making progress inside
# canon40_regen_store/op_units2_c_c0004.json after 8 minutes at a flat
# 137 MB resident -- solver time, not memory.  That is the same
# obstacle task 97 met and answered by forking one sub-process per unit
# (log_202 section 2), so this lane uses that mechanism, with the owner's two
# passes: pass 1 at 1,536 MB and 60 s per unit, pass 2 over whatever
# pass 1 flagged at 6,144 MB and 600 s.  A unit that does not finish in
# pass 2 is named as a shortfall, never approximated.
#
# term66_store/ is never opened for writing.  The audit columns go to
# t104_audit.json, so no record in the new store grows a field.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[0/1] term66_store shards before the walk"
ls term66_store/*.json | wc -l
python3 PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_walk.py 1536 60 6144 600
echo "exit $?"
