#!/bin/bash
# task o11, lane 10: the report -- rust_results.json and
# rust_report.md, from the run json written by lanes 6 to 9.
set -u
R=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the report"
cd "$R" && python3 rust_render.py report
echo "[2/2] the guard over the results json"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_results.json"
echo "lane o11_l10 done"
