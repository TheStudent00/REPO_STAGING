#!/usr/bin/env bash
# ex2_l5_guard_and_tally.sh -- task ex2: the spelling guard over every
# json this task wrote, and the final tally of the report -- the same
# pattern task ex1's `ex1_l15_guard_report_and_the_tally.sh` used.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_EX2.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/3] the spelling guard, over every json this task wrote"
cd PseudoCoupHQ/Research/op_pipeline
for F in expand2_cells.json expand2.json; do
  python3 check_no_spelling_keys.py "$A/$F"
done

echo ""
echo "[2/3] no exemption anywhere in what this task added"
grep -c exempt "$A/expand2.py" "$A/lanes_ex2/"*.sh || true

echo ""
echo "[3/3] the report as it stands, line count and the runs recorded"
wc -l "$A/expand2.md"
python3 - <<'PY'
import json
runs = 0
with open("PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand2_runs.jsonl") as handle:
    for line in handle:
        if line.strip():
            runs = runs + 1
retries = 0
import os
retry_path = ("PseudoCoupHQ/Research/oracle/cross_construction/"
              "emulation/autopoly/expand2_runs_retry600.jsonl")
if os.path.exists(retry_path):
    with open(retry_path) as handle:
        for line in handle:
            if line.strip():
                retries = retries + 1
print("runs recorded on expand2_runs.jsonl: %d" % runs)
print("runs recorded on expand2_runs_retry600.jsonl: %d" % retries)
PY
echo "done"
