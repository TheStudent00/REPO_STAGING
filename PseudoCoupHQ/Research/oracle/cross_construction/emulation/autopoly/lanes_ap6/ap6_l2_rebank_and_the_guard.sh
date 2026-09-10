#!/bin/bash
# ap6_l2_rebank_and_the_guard.sh -- task ap6, lane 2.
#
# WHAT THIS LANE DOES: builds the bank again, so that every certificate
# carries the two things this task adds -- the SETTER CELL, which is now
# part of a certificate's key, and the CODE VERSION of the machinery
# that produced the run.  Then it reads the bank's own four tables so
# that they can be set beside `DevComms/log_253`'s, which is how the
# effect of the key's change on the counts is measured rather than
# assumed.
#
# NOTHING IS DELETED: `certificates.jsonl` is derived from the stores
# and is rebuilt from them; every store, every source folder and every
# lane log stays where it is.
#
# MEMORY: bound 6 GB resident on the one collecting process, named abort
# ABORT_MEMORY_AP6, checked after every store; lane 1b's sample peaked
# at 60,704 kB.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
OP=PseudoCoupHQ/Research/op_pipeline
total=7

i=1
echo "[$i/$total] BUILD: every run of every pass -> certificates.jsonl"
python3 "$A/bank.py" build
echo

i=2
echo "[$i/$total] the certificates banked per kind, and per pass"
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
echo "[$i/$total] the certificates that carry a SETTER CELL -- the"
echo "          pair-level certificates, before this task's own pass"
python3 - "$A" <<'PY'
import json, sys
here = sys.argv[1]
counted = {}
pairs = set()
per_pass = {}
total = 0
handle = open(here + "/certificates.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    total = total + 1
    if not cert.get("setter"):
        continue
    counted[cert["kind"]] = counted.get(cert["kind"], 0) + 1
    name = cert["produced_by"]["pass"]
    per_pass[name] = per_pass.get(name, 0) + 1
    pairs.add((cert["cell"]["mnem"], cert["cell"]["shape"],
               cert["cell"]["key_width"], cert["setter"]["mnem"],
               cert["setter"]["shape"], cert["setter"]["key_width"]))
handle.close()
print("| what | count |")
print("|---|---|")
print("| certificates on the bank | %d |" % total)
print("| of them, PAIR-LEVEL (a setter cell on the key) | %d |"
      % sum(counted.values()))
print("| distinct (consumer cell, setter cell) pairs | %d |" % len(pairs))
print("")
print("| kind | pair-level certificates |")
print("|---|---|")
for kind in sorted(counted):
    print("| `%s` | %d |" % (kind, counted[kind]))
print("")
print("| pass | pair-level certificates |")
print("|---|---|")
for name in sorted(per_pass):
    print("| `%s` | %d |" % (name, per_pass[name]))
PY
echo

i=6
echo "[$i/$total] THE SPELLING GUARD over the json"
python3 "$OP/check_no_spelling_keys.py" "$A/certificates.json"
echo "  guard exit: $?"
echo

i=7
echo "[$i/$total] THE SPELLING GUARD over the jsonl, materialised under"
echo "          /tmp inside the instance and never in the repository"
mkdir -p /tmp/ap6_guard
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
out = "/tmp/ap6_guard/certificates_as_json.json"
json.dump(held, open(out, "w"))
print("  certificates.jsonl -> %s (%d record(s))" % (out, len(held)))
PY
python3 "$OP/check_no_spelling_keys.py" \
    /tmp/ap6_guard/certificates_as_json.json
echo "  guard exit: $?"
echo
echo "lane done"
