#!/bin/bash
# bb1 lane 1 -- what z3's bit-blast tactic actually hands back, printed, and
# the circuit this task reads out of it put BACK to z3 and proved equal to
# the term it came from, wherever the circuit is small enough to pose.
# Nothing is compiled here: this lane is about the reading, not the render.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
OP=$P/Research/op_pipeline
export HOME=/work
export PYTHONPATH="$OP:$G"
total=2

echo "[1/$total] the image's z3"
python3 -c "import z3; print('z3', z3.get_version_string())"

echo "[2/$total] the blasted goal, LITERAL, and the circuit sizes"
timeout 1500 python3 "$G/bitblast.py" probe
echo "  exit: $?"
echo "lane bb1_l1 done"
