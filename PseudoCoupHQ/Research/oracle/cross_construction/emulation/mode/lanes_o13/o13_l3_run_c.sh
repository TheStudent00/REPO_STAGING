#!/bin/bash
# task o13, lane 3: re-render with the mode the 36 emulations task o7
# recorded DISPROVED (log_218), compile at the c corpus's own ship
# flags, carve, and gate against the x unit -- twice: task o7's own
# first posing, unchanged, and the guarded posing.
set -u
M=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode
G=/projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the c re-run"
cd "$M" && python3 mode.py run c
echo "[2/2] the guard over the json this lane wrote"
python3 "$G" "$M/mode_run_c.json"
echo "lane o13_l3 done"
