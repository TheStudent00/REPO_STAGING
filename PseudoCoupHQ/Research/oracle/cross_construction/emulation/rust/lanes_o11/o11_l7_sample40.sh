#!/bin/bash
# task o11, lane 7: the sample of 40, across the three source
# languages, before the run of record -- the shake-out for the rust
# renderer's rules.
set -u
R=PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the sample"
cd "$R" && python3 rust_render.py sample 40
echo "[2/2] the guard over the sample json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_sample.json"
echo "lane o11_l7 done"
