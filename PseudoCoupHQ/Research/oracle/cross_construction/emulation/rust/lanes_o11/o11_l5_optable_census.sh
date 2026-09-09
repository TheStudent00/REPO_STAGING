#!/bin/bash
# task o11, lane 5: the coverage table and the population census.
# The coverage table comes FIRST, before any run, as the brief
# requires: the term language's operators against the two targets.
set -u
R=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/3] the coverage table"
cd "$R" && python3 rust_render.py optable
echo "[2/3] the census"
cd "$R" && python3 rust_render.py census
echo "[3/3] the guard over both json"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/coverage_table.json"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_population.json"
echo "lane o11_l5 done"
