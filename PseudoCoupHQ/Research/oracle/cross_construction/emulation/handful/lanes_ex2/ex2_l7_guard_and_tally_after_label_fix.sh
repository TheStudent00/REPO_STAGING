#!/usr/bin/env bash
# ex2_l7_guard_and_tally_after_label_fix.sh -- task ex2, RE-RUN of
# `ex2_l5_guard_and_tally.sh` over the corrected store (see
# `ex2_l6_reaggregate_after_label_fix.sh`'s note), under a new name for
# the same LAW reason. Also corrects one path in the superseded l5: the
# lane scripts live under `emulation/handful/lanes_ex2/`, not
# `emulation/autopoly/lanes_ex2/` -- l5's exemption grep pointed at a
# path with nothing in it and silently found nothing (`|| true` hid
# this); this lane greps the real path instead.
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
