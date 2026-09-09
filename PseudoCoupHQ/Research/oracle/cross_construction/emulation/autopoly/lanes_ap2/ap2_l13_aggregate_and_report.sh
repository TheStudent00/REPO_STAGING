#!/usr/bin/env bash
# ap2_l13_aggregate_and_report.sh -- task ap2: the 1,012-run store read
# once, every table computed off it, the report written, and the
# spelling guard over every json this task wrote.
#
# THE GUARD IS `Research/op_pipeline/check_no_spelling_keys.py`, the
# standing one, run over this task's own output and never modified.
# It refused task ap1's first aggregate for a joined cell key and was
# right; this task writes the record the same way task ap1 ended up
# writing it (`autopoly2.as_machine_form`, the triple in three fields
# with the mnemonic in `mnem`).
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP2.  Task
# ap1's aggregate lane peaked at 81,844 kB over the same-sized store.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/6] the aggregate"
python3 autopoly2.py aggregate

echo "[2/6] the report"
python3 autopoly2.py report

echo "[3/6] the store and the aggregate compared run for run"
python3 autopoly2.py store

echo "[4/6] the spelling guard, over every json this task wrote"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly2_cells.json \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly2.json

echo "[5/6] no exemption anywhere in what this task wrote"
grep -c exempt \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly2.py \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap2/ap2_l4_cells.sh \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap2/ap2_l12_run.sh || true

echo "[6/6] the tally"
python3 autopoly2.py tally
echo "done"
