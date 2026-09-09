#!/usr/bin/env bash
# t83 lane 9 -- ZERO REGRESSION for the bound.  Three shards already
# in term66_store are re-transcribed under the 6 GB address-space
# bound, into scratch, and compared record for record against what is
# stored.  If the bound changes a record it is not a bound and the
# lane refuses.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/1] three stored shards re-transcribed under the bound"
python3 term66_bounded.py 6144 100000 --check \
  canon40_wrapped_go.json \
  canon40_interp.json \
  canon40_regen_store/op_units2_c_c0001.json
echo "exit $?"
