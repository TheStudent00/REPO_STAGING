#!/usr/bin/env bash
# ex2_l9_guard_and_tally_final.sh -- task ex2, FINAL guard + tally, over
# the store as `ex2_l8_reaggregate_after_hyphen_fix.sh` left it. Same
# content as `ex2_l7_guard_and_tally_after_label_fix.sh` (which already
# corrected l5's lane-path mistake), new name because l7 already ran.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_EX2.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
LANES=PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/lanes_ex2

echo "[1/3] the spelling guard, over every json this task wrote"
cd PseudoCoupHQ/Research/op_pipeline
for F in expand2_cells.json expand2.json; do
  python3 check_no_spelling_keys.py "$A/$F"
done

echo ""
echo "[2/3] no exemption anywhere in what this task added"
grep -c exempt "$A/expand2.py" "$LANES"/*.sh || true

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
