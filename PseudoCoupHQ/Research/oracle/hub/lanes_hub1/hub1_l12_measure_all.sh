#!/usr/bin/env bash
# hub1_l12_measure_all.sh -- task hub1, lane 12: the section-3 measure over
# the WHOLE population of corpus go units that name one cell, after lane
# hub1_l11's sample of 12 measured the cost (54 s for 36 runs, peak
# 101,328 kB against the 6 GB bound). It overwrites measure.json, which the
# sample lane wrote. Then the tables. Memory bound 6 GB, named abort
# ABORT_MEMORY_HUB1.
set -uo pipefail
echo "[1/3] the whole population"
cd PseudoCoupHQ/Research/oracle/hub
python3 hub.py measure
echo "[2/3] the tables"
python3 hub.py tables
echo "[3/3] the spelling guard over every json this task writes"
for f in dictionary.json oracle_test.json measure.json; do
    python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
        PseudoCoupHQ/Research/oracle/hub/$f
done
