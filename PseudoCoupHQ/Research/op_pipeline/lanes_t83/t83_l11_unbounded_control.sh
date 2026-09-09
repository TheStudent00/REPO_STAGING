#!/usr/bin/env bash
# t83 lane 11 -- THE CONTROL.  Lane 9 and lane 10 both found the same
# four go records differing from the store under the 6 GB bound.  The
# control asks the only question that separates the two candidate
# causes: run the SAME three shards with the ceiling set far above the
# container's own 8 GB cgroup, so no address-space bound can bite, and
# see whether the same four still differ.
#
#   same four differ  -> the bound is not the cause; the difference is
#                        between this container and the host the
#                        stored shards were walked on
#   none differ       -> the bound is the cause and must not be used
#
# The three shards peaked at 440,308 kB under the bound, so running
# them unbounded risks nothing.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
rm -rf /work/t83_check_store /work/t83_check_state.json
echo "[1/1] the same three shards, ceiling 30000 MB (above the 8 GB cgroup: no bound bites)"
python3 term66_bounded.py 30000 100000 --check \
  canon40_wrapped_go.json \
  canon40_interp.json \
  canon40_regen_store/op_units2_c_c0001.json
echo "exit $?"
