#!/usr/bin/env bash
# t83 lane 8 -- is the solver's appetite a requirement or an
# opportunistic allocation?  The same unit at five ceilings, with the
# whole record read back at each, so a ceiling is only called a bound
# if the answer does not move.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 probe83g_ceiling.py canon40_regen_store/op_units2_c_c0004.json c/regen_1859 512 1024 2048 3072 5120
echo "exit $?"
