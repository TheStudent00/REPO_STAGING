#!/bin/bash
# task o13, lane 4: re-render with the mode the 59 emulations task o11
# recorded DISPROVED (log_226), compile at the rust corpus's own ship
# flags, carve, and gate against the x unit -- twice: task o7's own
# first posing, unchanged, and the guarded posing.
set -u
M=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode
G=/projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the rust re-run"
cd "$M" && python3 mode.py run rust
echo "[2/2] the guard over the json this lane wrote"
python3 "$G" "$M/mode_run_rust.json"
echo "lane o13_l4 done"
