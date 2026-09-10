#!/bin/bash
# t2_l26_the_readings_and_the_guards.sh -- task t2, lane 26: the three
# readings WITH this pass in them, and the spelling guard over every
# json this task wrote.
#
# WHY THE READINGS ARE RUN AGAIN.  `bank.py readings` reads the twelve
# passes its own file names, and this pass is registered from outside
# that file, so a reading run in its own process is the reading BEFORE
# this pass.  The registration has to be in the same process as the
# reading, and `construct.py readings` is that process.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2; every store
# is streamed.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
G=PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
total=4

i=1
echo "[$i/$total] THE THREE READINGS, with this pass registered"
python3 "$C/construct.py" readings
echo

i=2
echo "[$i/$total] THE SPELLING GUARD over the json this task wrote"
python3 "$G" "$C/construct.json" "$C/lean/lemmas_t2.json" \
    "$A/certificates.json"
echo "  guard exit: $?"
echo

i=3
echo "[$i/$total] THE SPELLING GUARD over the two jsonl stores, materialised as json"
mkdir -p /tmp/t2_guard
python3 - <<'PY'
import json, os
pairs = [
    ("PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/t2_construct_runs.jsonl",
     "/tmp/t2_guard/t2_construct_runs.json"),
    ("PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl",
     "/tmp/t2_guard/certificates.json"),
]
for source, target in pairs:
    rows = []
    handle = open(source)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        rows.append(json.loads(text))
        continue
    handle.close()
    out = open(target, "w")
    json.dump({"records": rows}, out)
    out.close()
    print("  %s -> %s (%d record(s))"
          % (os.path.basename(source), target, len(rows)))
    continue
PY
python3 "$G" /tmp/t2_guard/t2_construct_runs.json
echo "  guard exit: $?"
python3 "$G" /tmp/t2_guard/certificates.json
echo "  guard exit: $?"
echo

i=4
echo "[$i/$total] THE LAW'S OWN COUNT over the files this task added"
grep -rc exempt "$C"/*.py "$C"/lean/*.py "$C"/lanes_t2/*.sh | sort -t: -k2 -rn | head -5
echo "  the maximum above must be 0"
echo
echo "lane done"
