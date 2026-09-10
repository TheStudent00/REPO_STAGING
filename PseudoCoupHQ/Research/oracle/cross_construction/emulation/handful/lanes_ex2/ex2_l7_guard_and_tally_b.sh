#!/usr/bin/env bash
# ex2_l7_guard_and_tally_b.sh -- task ex2: the spelling guard over every
# json this task wrote, re-run over the report of record (the second
# pass, after the label-dot fix), and the tally.
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
echo "[2/3] no exemption anywhere in what this task added (its own text excluded)"
grep -c exempt "$A/expand2.py" \
  "$A/lanes_ex2/ex2_l1_preflight_and_smoke.sh" \
  "$A/lanes_ex2/ex2_l2_the_loop.sh" \
  "$A/lanes_ex2/ex2_l3_retry600.sh" \
  "$A/lanes_ex2/ex2_l4_aggregate_and_report.sh" \
  "$A/lanes_ex2/ex2_l6_aggregate_and_report_b.sh" || true

echo ""
echo "[3/3] the report as it stands, line count and the runs recorded"
wc -l "$A/expand2.md"
python3 - <<'PY'
import json
import os
runs = 0
with open("PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand2_runs.jsonl") as handle:
    for line in handle:
        if line.strip():
            runs = runs + 1
retries = 0
retry_path = ("PseudoCoupHQ/Research/oracle/cross_construction/"
              "emulation/autopoly/expand2_runs_retry600.jsonl")
if os.path.exists(retry_path):
    with open(retry_path) as handle:
        for line in handle:
            if line.strip():
                retries = retries + 1
disagreements = 0
with open("PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand2_runs.jsonl") as handle:
    for line in handle:
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("disagreements", 0) > 0:
            disagreements = disagreements + 1
print("runs recorded on expand2_runs.jsonl: %d" % runs)
print("runs recorded on expand2_runs_retry600.jsonl: %d" % retries)
print("runs with a disagreement, over the run of record: %d" % disagreements)
PY
echo "done"
