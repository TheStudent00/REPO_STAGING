#!/usr/bin/env bash
# t104 lane 5 -- THE 44, asked again.
#
# The 44 units whose layer-4 term is built and proved but whose
# normalizer did not converge at any ceiling task 97 tried (log_202
# section 4.3).  Each is run again in a forked sub-process of its own
# with RLIMIT_AS at 6,144 MB and 600 s, by term97_walk.one_unit_forked
# -- imported, not re-typed, so the answer is comparable to task 97's.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/1] the 44"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_the44.py 6144 600
echo "exit $?"
