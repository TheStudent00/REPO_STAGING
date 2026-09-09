#!/usr/bin/env bash
# t104 lane 8 -- WHY the operand-order acceptance flags a unit, and
# whether ordering the operands BEFORE the first simplification closes
# it.
#
# For every unit the acceptance flagged, this lane asks the solver
# whether the operand-permuted term is the same computation (so a flag
# caused by an unsound perturbation is separated from a flag caused by
# the normalizer), and prints the text pair as `term.py` prints it
# today beside the text pair with the candidate applied.  It edits
# nothing.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/1] the flagged units, cause and candidate"
python3 PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_order_probe.py 3072 300
echo "exit $?"
