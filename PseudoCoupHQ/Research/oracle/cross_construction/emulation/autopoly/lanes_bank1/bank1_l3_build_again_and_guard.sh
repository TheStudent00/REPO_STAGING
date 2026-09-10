#!/bin/bash
# bank1_l3_build_again_and_guard.sh -- task bank1, lane 3.
#
# WHY THIS LANE EXISTS, said out loud: lane 2's build read `rendered`
# before `refusal_cause` on the interpreted route, so task ex2's
# thirty-eight nullary runs ("the runner did not answer", log_250 SS9)
# were banked `undecided` where task ex2's own account calls them
# refused -- 418 refused against ex2's 456.  `bank.interpreted_certificate`
# now decides on the refusal cause first, and this lane banks again and
# guards the result.  Lane 2's own log is the record of the first
# reading and nothing of it is deleted.
#
# THE GUARD runs over every json AND every jsonl this task writes.  The
# guard reads json documents, so each jsonl is materialised as a json
# array UNDER /tmp INSIDE THE INSTANCE -- never in the repo -- and the
# guard walks that.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BANK1; lane 2
# peaked at 41,288 kB.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
OP=PseudoCoupHQ/Research/op_pipeline
total=7

i=1
echo "[$i/$total] BUILD, again: every run of every pass -> certificates.jsonl"
python3 "$A/bank.py" build
echo

i=2
echo "[$i/$total] the certificates banked per kind"
python3 "$A/bank.py" kinds
echo

i=3
echo "[$i/$total] THE THREE READINGS"
python3 "$A/bank.py" readings
echo

i=4
echo "[$i/$total] the pairs proved by some pass and not by the last"
python3 "$A/bank.py" restored
echo

i=5
echo "[$i/$total] the stores this task did not bank, audited"
python3 "$A/bank.py" backups
echo

i=6
echo "[$i/$total] THE SPELLING GUARD over every json this task writes"
python3 "$OP/check_no_spelling_keys.py" "$A/certificates.json"
echo "  guard exit: $?"
echo

i=7
echo "[$i/$total] THE SPELLING GUARD over every jsonl this task writes"
mkdir -p /tmp/bank1_guard
python3 - "$A" <<'PY'
import json, sys
here = sys.argv[1]
for name in ["certificates.jsonl"]:
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
echo "  guard exit: $?"
echo
echo "grep -c exempt over the files this task adds:"
grep -c exempt "$A/bank.py" "$A/autopoly.py" \
    "$A/lanes_bank1/bank1_l1_preflight_and_sample.sh" \
    "$A/lanes_bank1/bank1_l2_build_the_bank.sh" \
    "$A/lanes_bank1/bank1_l3_build_again_and_guard.sh"
echo
echo "lane done"
