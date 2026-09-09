#!/bin/bash
# task o11, lane 4: the last division question.
# Lane 3 removed rustc's zero-divisor check at every unsigned width but
# not the signed-extreme check. This lane tries the remaining spellings
# of that same fact: an unreachable branch, two separate hints, and the
# division done at double width where the extreme cannot arise.
set -u
R=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the fourth probe set"
cd "$R" && python3 rust_facts.py probe4
echo "[2/2] the guard over the json this lane wrote"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_facts4.json"
echo "lane o11_l4 done"
