#!/bin/bash
# task o11, lane 22: the law's `grep -c exempt` over every file this
# task added, on the record.
set -u
R=PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
echo "[1/1] grep -c exempt"
echo "\$ grep -c exempt $R/rust_render.py $R/rust_report.py $R/rust_facts.py $R/lanes_o11/*.sh"
grep -c exempt "$R/rust_render.py" "$R/rust_report.py" "$R/rust_facts.py" "$R"/lanes_o11/*.sh
echo "lane o11_l22 done"
