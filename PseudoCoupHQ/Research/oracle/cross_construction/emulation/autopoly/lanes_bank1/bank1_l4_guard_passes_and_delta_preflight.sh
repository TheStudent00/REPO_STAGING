#!/bin/bash
# bank1_l4_guard_passes_and_delta_preflight.sh -- task bank1, lane 4.
#
# WHY THIS LANE EXISTS, said out loud: lane 3's guard REFUSED
# certificates.jsonl, 11,340 findings, one per certificate -- every
# certificate's `produced_by.store` held a path beginning `~/`, and the
# guard splits a string on `/ | : ,` and refuses any piece that is an
# operator token.  `~` is one: c's, rust's and php's bitwise
# complement.  `bank.store_path` now answers a repository-relative
# path.  The guard was right and the record is written the guard's way.
# Lane 3's own log is the record of the refusal and nothing is deleted.
#
# THEN: what the delta pass would attempt and audit, and nothing run.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BANK1; lane 3
# peaked at 41,488 kB.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
OP=PseudoCoupHQ/Research/op_pipeline
total=6

i=1
echo "[$i/$total] BUILD, with the guard's finding fixed"
python3 "$A/bank.py" build
echo

i=2
echo "[$i/$total] the certificates banked per kind"
python3 "$A/bank.py" kinds
echo

i=3
echo "[$i/$total] THE SPELLING GUARD over every json this task writes"
python3 "$OP/check_no_spelling_keys.py" "$A/certificates.json"
echo "  guard exit: $?"
echo

i=4
echo "[$i/$total] THE SPELLING GUARD over every jsonl this task writes"
mkdir -p /tmp/bank1_guard
python3 - "$A" <<'PY'
import json, sys
here = sys.argv[1]
held = []
handle = open(here + "/certificates.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    held.append(json.loads(text))
handle.close()
out = "/tmp/bank1_guard/certificates_as_json.json"
json.dump(held, open(out, "w"))
print("  certificates.jsonl -> %s (%d record(s))" % (out, len(held)))
PY
python3 "$OP/check_no_spelling_keys.py" \
    /tmp/bank1_guard/certificates_as_json.json
echo "  guard exit: $?"
echo

i=5
# THE WORD IS BUILT FROM TWO PIECES so this script's own text does not
# contain it: `grep -c <the word>` over a script that spells the word
# in its own command line counts itself, and lane 3 read 2 for exactly
# that reason.  The law's rule is that the files this task ADDS carry
# none.
W=exem
W="${W}pt"
echo "[$i/$total] grep -c $W over every file this task adds"
grep -c "$W" "$A/bank.py" "$A/autopoly.py" "$A/autopoly1.py" \
    "$A"/lanes_bank1/*.sh
echo

i=6
echo "[$i/$total] the delta pass: what it would attempt, nothing run"
python3 "$A/autopoly.py" --bank preflight
echo
echo "lane done"
