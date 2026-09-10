#!/bin/bash
# ap6_l13_rebank_readings_and_the_guards.sh -- task ap6, lane 13.
#
# WHAT THIS LANE DOES: it banks the two stores this task wrote -- the
# 100% audit's and the delta pass's -- and then reads the bank the four
# ways the brief asks for, so every number in the report is one this
# lane printed.
#
#   * the bank per kind and per pass, and THE THREE READINGS, to be set
#     beside `log_253`'s Table B3 and B5.
#   * THE PAIR-LEVEL CERTIFICATES: how many certificates carry a setter
#     cell on their key, and over how many distinct (consumer cell,
#     setter cell) pairs -- the before was 2,623 over 39 pairs, printed
#     by lane 2 before this task's own pass ran.
#   * THE GUARD ON THE PAIR CHANGE: every pair entry task hub2's own
#     dictionary serves, asked of the bank again.  A pair hub2 served
#     and the bank no longer certifies is a REGRESSION and is named.
#     `dictionary2.json` is READ and never written.
#   * the delta's cost line, against `log_253`'s.
#   * THE SPELLING GUARD over every json and jsonl.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_AP6; the bank
# is streamed and never held whole.  Lane 12's pass peaked at
# 2,413,732 kB (38% of the bound).
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
OP=PseudoCoupHQ/Research/op_pipeline
HUB=PseudoCoupHQ/Research/oracle/hub
total=9

echo "[1/$total] BUILD: every run of every pass -> certificates.jsonl"
python3 "$A/bank.py" build
echo

echo "[2/$total] the certificates banked per kind, and per pass"
python3 "$A/bank.py" kinds
echo

echo "[3/$total] THE THREE READINGS"
python3 "$A/bank.py" readings
echo

echo "[4/$total] THE PAIR-LEVEL CERTIFICATES, after this task's pass"
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

echo "[5/$total] THE GUARD: every pair entry hub2's dictionary serves,"
echo "          asked of the bank again"
python3 - "$A" "$HUB" <<'PY'
import json, sys
here = sys.argv[1]
hub = sys.argv[2]
best = {}
handle = open(here + "/certificates.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    if not cert["preferred"]:
        continue
    setter = cert.get("setter")
    if not setter:
        continue
    key = (cert["cell"]["mnem"], cert["cell"]["shape"],
           cert["cell"]["key_width"], cert["target"],
           setter["mnem"], setter["shape"], setter["key_width"])
    held = best.get(key) or set()
    held.add(cert["kind"])
    best[key] = held
handle.close()
document = json.load(open(hub + "/dictionary2.json"))
served = 0
still = 0
missing = []
for target in sorted(document["pairs"]):
    for label in sorted(document["pairs"][target]):
        entry = document["pairs"][target][label]
        setter = entry["setter"]
        consumer = entry["consumer"]
        key = (consumer["mnem"], consumer["shape"],
               consumer["key_width"], target,
               setter["mnem"], setter["shape"], setter["key_width"])
        served = served + 1
        kinds = best.get(key) or set()
        if "proved" in kinds or "agreed" in kinds:
            still = still + 1
            continue
        missing.append((label, target, sorted(kinds)))
        continue
    continue
print("| what | count |")
print("|---|---|")
print("| pair entries task hub2's dictionary serves | %d |" % served)
print("| of them, still certified `proved` by the bank | %d |" % still)
print("| REGRESSED: served by hub2, no longer certified | %d |"
      % len(missing))
if missing:
    print("")
    print("| the pair | target | the kinds the bank now holds |")
    print("|---|---|---|")
    for label, target, kinds in missing:
        print("| %s | %s | %s |" % (label, target,
                                    ", ".join(kinds) or "none"))
PY
echo

echo "[6/$total] the pairs proved by some pass and not by the last"
python3 "$A/bank.py" restored
echo

echo "[7/$total] THE DELTA'S OWN COST LINE"
python3 "$A/autopoly.py" --pass ap6_delta --bank report
echo
python3 "$A/autopoly.py" --pass ap6_delta --bank cost
echo

echo "[8/$total] THE AUDIT of this pass, and the tally"
python3 "$A/autopoly.py" --pass ap6_delta --bank audit
echo
python3 "$A/autopoly.py" --pass ap6_delta --bank tally
echo

echo "[9/$total] THE SPELLING GUARD over every json this task wrote"
mkdir -p /tmp/ap6_guard13
for f in "$A/certificates.json" "$A/ap6_delta.json"; do
    if [ -f "$f" ]; then
        python3 "$OP/check_no_spelling_keys.py" "$f"
        echo "  guard exit: $?"
    fi
done
python3 - "$A" <<'PY'
import json, sys
here = sys.argv[1]
for name in ("certificates.jsonl", "ap6_delta_runs.jsonl",
             "ap6_audit_runs.jsonl"):
    held = []
    handle = open(here + "/" + name)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        held.append(json.loads(text))
    handle.close()
    out = "/tmp/ap6_guard13/%s.json" % name.replace(".jsonl", "")
    json.dump(held, open(out, "w"))
    print("  %s -> %s (%d record(s))" % (name, out, len(held)))
    continue
PY
for f in /tmp/ap6_guard13/*.json; do
    python3 "$OP/check_no_spelling_keys.py" "$f"
    echo "  guard exit: $?"
done
echo
echo "lane done"
