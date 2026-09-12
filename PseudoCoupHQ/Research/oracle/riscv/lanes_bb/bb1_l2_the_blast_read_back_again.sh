#!/bin/bash
# bb1 lane 2 -- the blast read back AGAIN, with the arrivals handed to z3
# already decomposed into bits this file names, which is what lane 1 showed
# was needed: z3 5.1.0 abstracts a bit-vector arrival into fresh booleans
# `k!<n>` whose meaning is in the goal's model converter and not in the
# formula. The circuit is put BACK to z3 and proved equal to the term it
# came from wherever it is small enough to pose.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
OP=$P/Research/op_pipeline
export HOME=/work
export PYTHONPATH="$OP:$G"
total=2
i=1

echo "[$i/$total] the image's z3"; i=$((i+1))
python3 -c "import z3; print('z3', z3.get_version_string())"

echo "[$i/$total] the blasted goal, LITERAL, and the circuit sizes"
timeout 1500 python3 "$G/bitblast.py" probe
echo "  exit: $?"
echo "lane bb1_l2 done"
