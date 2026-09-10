#!/bin/bash
# bank1_l7_delta_report_and_rebank.sh -- task bank1, lane 7.
#
# WHAT THIS LANE DOES: the delta pass's own cost line and its audit,
# then the delta pass BANKED -- `bank.py build` again with
# `bank1_delta_runs.jsonl` now on disk -- and the three readings over
# the grown bank, which is the monotone growth the reshaped loop is
# for.  Then the guard over every json and jsonl again.
#
# THE COST LINE the delta pass wrote is computed against the bank AS IT
# STOOD BEFORE THIS PASS and is not recomputed here; re-banking changes
# what the NEXT pass would attempt, not what this one did.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BANK1; the
# delta pass peaked at 996,780 kB (15.8% of the bound).
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
OP=PseudoCoupHQ/Research/op_pipeline
total=8

i=1
echo "[$i/$total] the delta pass's cost line"
python3 "$A/autopoly.py" --bank report
echo

i=2
echo "[$i/$total] the audit, every triple"
python3 "$A/autopoly.py" --bank audit
echo

i=3
echo "[$i/$total] the delta pass's own tally"
python3 "$A/autopoly.py" --bank tally
echo

i=4
echo "[$i/$total] THE BANK, with the delta pass banked"
python3 "$A/bank.py" build
echo

i=5
echo "[$i/$total] the certificates banked per kind, after the delta"
python3 "$A/bank.py" kinds
echo

i=6
echo "[$i/$total] THE THREE READINGS, after the delta"
python3 "$A/bank.py" readings
echo

i=7
echo "[$i/$total] THE SPELLING GUARD over every json this task writes"
python3 "$OP/check_no_spelling_keys.py" "$A/certificates.json"
echo "  certificates.json guard exit: $?"
python3 "$OP/check_no_spelling_keys.py" "$A/bank1_delta.json"
echo "  bank1_delta.json guard exit: $?"
echo

i=8
echo "[$i/$total] THE SPELLING GUARD over every jsonl this task writes"
mkdir -p /tmp/bank1_guard
python3 - "$A" <<'PY'
import json, sys
here = sys.argv[1]
for name in ["certificates.jsonl", "bank1_delta_runs.jsonl"]:
    held = []
    handle = open(here + "/" + name)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        held.append(json.loads(text))
    handle.close()
    out = "/tmp/bank1_guard/" + name.replace(".jsonl", "_as_json.json")
    json.dump(held, open(out, "w"))
    print("  %s -> %s (%d record(s))" % (name, out, len(held)))
PY
python3 "$OP/check_no_spelling_keys.py" \
    /tmp/bank1_guard/certificates_as_json.json
echo "  certificates.jsonl guard exit: $?"
python3 "$OP/check_no_spelling_keys.py" \
    /tmp/bank1_guard/bank1_delta_runs_as_json.json
echo "  bank1_delta_runs.jsonl guard exit: $?"
echo
echo "lane done"
