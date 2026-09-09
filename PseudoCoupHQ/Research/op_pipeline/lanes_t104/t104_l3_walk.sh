#!/usr/bin/env bash
# t104 lane 3 -- THE RE-NORMALIZATION WALK.
#
# Every record in term66_store/ is rebuilt into the new store
# term104_store/ with its layer-5 text printed again by `term.py` as it
# stands.  term66_store/ is never opened for writing.  The audit
# columns -- which records' text changed, whether the layer-4 object's
# own s-expression hashes the same before and after printing, and the
# census of declaration kinds actually present in the proved terms --
# go to t104_audit.json beside the store, so no record grows a field.
#
# MEMORY: one shard at a time; task 79's comparable walk peaked at
# 83 MB resident.  Hard cap 6 GB, named abort ABORT_MEMORY_T104.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[0/1] term66_store shard count and record count before the walk"
ls term66_store/*.json | wc -l
python3 /projects/PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_walk.py
echo "exit $?"
