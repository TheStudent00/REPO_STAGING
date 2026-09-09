#!/usr/bin/env bash
# t97 lane 2 -- WHICH token fired on the 11 units lane 1 flagged, and
# whether the ceiling changes the record under the fork-per-unit
# arrangement.  Writes nothing into the store.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/2] c/regen_1859 -- the unit task 83 traced (log_189 section 2.5)"
python3 probe97b_flag_reason.py canon40_regen_store/op_units2_c_c0004.json \
  c/regen_1859 1536 3072 6144
echo "exit $?"
echo
echo "[2/2] c/regen_1869 -- a second of the eleven"
python3 probe97b_flag_reason.py canon40_regen_store/op_units2_c_c0004.json \
  c/regen_1869 1536 3072 6144
echo "exit $?"
