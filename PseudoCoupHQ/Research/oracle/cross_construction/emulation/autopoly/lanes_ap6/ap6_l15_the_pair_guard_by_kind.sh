#!/bin/bash
# ap6_l15_the_pair_guard_by_kind.sh -- task ap6, lane 15: lane 14's pair
# guard again, against the kind each entry actually carries.
#
# WHY LANE 14's FIRST TABLE IS NOT THE ANSWER.  It asked whether the
# bank still certifies each of task hub2's 111 pair-level entries as
# `proved`, and named five that it does not.  But a dictionary entry
# records its OWN kind, and hub2 serves an entry proved under the
# caller's extension as well as one proved outright: the question the
# guard is for is whether an entry the dictionary serves is still
# carried by the bank AT THE KIND IT WAS SERVED AT, and that is what
# this lane asks.  A kind the bank no longer holds is the regression.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_AP6; the bank is
# streamed and never held whole.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
HUB=PseudoCoupHQ/Research/oracle/hub
total=1

echo "[1/$total] every pair entry hub2 serves, at its own kind"
python3 - "$A" "$HUB" <<'PY'
import json, sys, resource
here = sys.argv[1]
hub = sys.argv[2]
best = {}
handle = open(here + "/certificates.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    setter = cert.get("setter")
    if not setter:
        continue
    key = (cert["cell"]["mnem"], cert["cell"]["shape"],
           cert["cell"]["key_width"], cert["target"], cert["place"],
           setter["mnem"], setter["shape"], setter["key_width"])
    held = best.get(key) or set()
    held.add(cert["kind"])
    best[key] = held
    continue
handle.close()
document = json.load(open(hub + "/dictionary2.json"))
served = 0
still = 0
by_kind = {}
missing = []
for target in sorted(document["pairs"]):
    for label in sorted(document["pairs"][target]):
        entry = document["pairs"][target][label]
        setter = entry["setter_cell"]
        consumer = entry["consumer_cell"]
        key = (consumer["mnem"], consumer["shape"],
               consumer["key_width"], entry["lang"], entry["place"],
               setter["mnem"], setter["shape"], setter["key_width"])
        served = served + 1
        kind = entry["kind"]
        by_kind[kind] = (by_kind.get(kind) or 0) + 1
        kinds = best.get(key) or set()
        if kind in kinds:
            still = still + 1
            continue
        missing.append((label, entry["lang"], kind, sorted(kinds)))
        continue
    continue
print("| what | count |")
print("|---|---|")
print("| pair-level entries task hub2's dictionary serves | %d |" % served)
print("| of them, the bank still holds AT THE ENTRY'S OWN KIND | %d |"
      % still)
print("| REGRESSED: the bank no longer holds that kind | %d |"
      % len(missing))
print("")
print("| the kind the entry was served at | entries |")
print("|---|---|")
for kind in sorted(by_kind):
    print("| `%s` | %d |" % (kind, by_kind[kind]))
    continue
if missing:
    print("")
    print("| the pair | target | served at | the kinds the bank holds |")
    print("|---|---|---|---|")
    for label, target, kind, kinds in missing:
        print("| %s | %s | `%s` | %s |"
              % (label, target, kind, ", ".join(kinds) or "none"))
        continue
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo
echo "lane done"
