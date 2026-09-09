#!/usr/bin/env bash
# ap1_l8_causes.sh -- task ap1: the by-cause totals over the whole loop,
# the four targets together, and the one group inside them that is a
# question rather than a limit.
#
# WHY THIS LANE: the report's section 3 is per target, which is what the
# brief asks for; the reply to the coordinator needs the same causes
# summed over all 1,012 runs, and the arrival-contract group -- the
# cause task g1b flagged on the divide alone -- counted, so whether it
# is one cell's problem or a general one is a measurement.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import json
import resource

AGG = ("/projects/PseudoCoupHQ/Research/oracle/cross_construction/"
       "emulation/autopoly/autopoly.json")
document = json.load(open(AGG))

# THE SAME CAUSES THE REPORT'S SECTION 3 PRINTS, summed over the four
# targets rather than split by target.
summed = {}
for lang in document["meta"]["targets"]:
    for name in document["causes"][lang]:
        held = document["causes"][lang][name]
        entry = summed.setdefault(name, {"runs": 0, "rows": 0,
                                         "langs": []})
        entry["runs"] = entry["runs"] + held["runs"]
        entry["rows"] = entry["rows"] + held["ledger_rows"]
        entry["langs"].append(lang)
print("| cause | runs | ledger rows counted once per run | targets |")
print("|---|---|---|---|")
ordered = sorted(summed, key=lambda name: (-summed[name]["runs"], name))
for name in ordered:
    held = summed[name]
    print("| %s | %d | %d | %s |"
          % (name.replace("|", "\\|"), held["runs"], held["rows"],
             ",".join(sorted(held["langs"]))))
total = 0
for name in summed:
    total = total + summed[name]["runs"]
print("")
print("runs carrying a cause: %d of %d" % (total, document["meta"]["runs"]))

# THE ARRIVAL-CONTRACT GROUP: every gate call that declined because the
# two sides name a different number of IN rows.  Task g1b found it on
# the divide in c; this counts it over the whole loop.
group = []
for run in document["runs"]:
    for place in (run.get("places") or []):
        check = place.get("check") or {}
        reason = "%s" % check.get("reason")
        if "the IN rows cannot be aligned" not in reason:
            continue
        group.append((run["mnem"], run["shape"], run["key_width"],
                      run["lang"], place["writes"], run["route"],
                      run["attested_ledger_rows"], reason))
print("")
print("places the gate declined on the IN-row alignment: %d" % len(group))
shapes = {}
for one in group:
    shapes.setdefault(one[7], 0)
    shapes[one[7]] = shapes[one[7]] + 1
for reason in sorted(shapes, key=lambda r: -shapes[r]):
    print("   %d places: %s" % (shapes[reason], reason))
print("")
print("the cells in that group, with their route and ledger rows:")
seen = set()
for one in group:
    key = (one[0], one[1], one[2], one[5])
    if key in seen:
        continue
    seen.add(key)
    print("   %-8s %-10s %-5s route %-16s %d rows"
          % (one[0], one[1], one[2], one[5], one[6]))
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
