#!/bin/bash
# task o13, lane 7: the report the brief names -- `mode.py report`
# reads mode_population.json / mode_facts.json / mode_run_c.json /
# mode_run_rust.json (the 3,000 ms verdict of record) and writes
# mode_results.json and mode_report.md.
set -u
M=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode
G=/projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the report"
cd "$M" && python3 mode.py report
echo "[2/2] the guard over the json this lane wrote"
python3 "$G" "$M/mode_results.json"
echo "lane o13_l7 done"
