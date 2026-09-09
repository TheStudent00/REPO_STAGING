#!/bin/bash
# task o11, lane 9: the per-opcode question again, after one field
# move. Lane 8's guard run FAILED rust_peropcode.json at 33 places,
# all of them `landed_mnem`: the guard exempts a field named exactly
# `mnem` as a machine form and nothing else, so the landed mnemonic now
# sits as `landed.mnem`. The guard itself is untouched.
set -u
R=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the per-opcode question"
cd "$R" && python3 rust_render.py peropcode
echo "[2/2] the guard over the per-opcode json"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_peropcode.json"
echo "lane o11_l9 done"
