#!/bin/bash
# task o13, lane 6: name the cause of the two rows the guarded posing
# still disproves, instead of guessing it.  For each, the two guarded
# answers and the two guard conditions are evaluated at the solver's
# own model, with the caller-extension rule applied -- the values in
# motion at the input the solver picked.
set -u
M=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode
G=/projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the two c rows the guarded posing still disproves"
cd "$M" && python3 mode.py diagnose c E01589 E01596
echo "[2/2] the guard over the json this lane wrote"
python3 "$G" "$M/mode_diagnose_c.json"
echo "lane o13_l6 done"
