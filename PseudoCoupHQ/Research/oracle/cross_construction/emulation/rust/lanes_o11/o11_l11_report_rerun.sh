#!/bin/bash
# task o11, lane 11: the report again, after two presentation fixes.
# (1) a `|` inside a cell -- task o1's pair key `rust|c` -- split the
# population table's first column, so cells are now escaped.
# (2) the byte-identity example was the shortest possible body, a bare
# `ret`; the picker now prefers one the gate also proved, else the
# longest emulated body.
set -u
R=PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the report"
cd "$R" && python3 rust_render.py report
echo "[2/2] the guard over the results json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_results.json"
echo "lane o11_l11 done"
