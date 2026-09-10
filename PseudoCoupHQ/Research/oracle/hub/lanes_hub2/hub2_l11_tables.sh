#!/usr/bin/env bash
# hub2_l11_tables.sh -- task hub2, lane 11: oracle_test2.md, task hub1's
# own numbers read beside this task's from its own artifacts
# (oracle_test.json, measure.json), which are READ and never edited.
set -uo pipefail
echo "[1/1] the tables"
cd PseudoCoupHQ/Research/oracle/hub
python3 hub2.py tables
