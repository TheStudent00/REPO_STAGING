#!/usr/bin/env bash
# hub2_l3_modes_and_exclusions.sh -- task hub2, lane 3.  Writes nothing.
# Three questions lane 2 left open:
#   1. task o13's own store, read the way its own shape asks: which pool
#      entries the mode re-run proved, per target, and with which mode;
#   2. the exact filter that kept the pool entries the handful's holes
#      name out of task o7's and task o11's populations;
#   3. whether the go units that are ONE PAIR plus chaff overlap the 134
#      units task hub1 asked about (task o2's narrow rule, one cell).
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
total=3

echo "[1/$total] task o13's mode store"
python3 - <<'PY'
import json, os, collections, resource
EMU = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
mode = json.load(open(os.path.join(EMU, "mode", "mode_results.json")))
runs = mode["runs"]
print("`runs` is a dict of:", sorted(runs.keys()))
for target in sorted(runs):
    rows = runs[target]
    print("--- %s: %d rows; a row's own fields: %s"
          % (target, len(rows), sorted(rows[0].keys())))
    counter = collections.Counter()
    proved = []
    for row in rows:
        outcome = row.get("outcome") or row.get("verdict")
        counter[outcome] += 1
        if outcome in ("PROVED", "PROVED_ON_SHIP",
                       "PROVED_UNDER_CALLER_EXTENSION"):
            proved.append(row)
    print("| outcome | rows |")
    print("|---|---|")
    for key in sorted(counter, key=lambda k: str(k)):
        print("| %s | %d |" % (key, counter[key]))
    print("entries proved on the mode re-run: %d"
          % len(set(r.get("entry_id") for r in proved)))
    if proved:
        example = proved[0]
        print("one proved row, cut to 1800 characters:")
        print(json.dumps({k: v for k, v in example.items()
                          if k not in ("source", "mode_source")},
                         indent=1)[:1800])
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[2/$total] the filter that excluded each entry"
python3 - <<'PY'
import json, os, resource
EMU = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
want = ["E00302", "E00163", "E00310", "E00316", "E00025", "E00058"]
for name, path in [("o7 (c)", os.path.join(EMU, "emulation_population.json")),
                   ("o11 (rust)", os.path.join(EMU, "rust",
                                               "rust_population.json"))]:
    document = json.load(open(path))
    print("===", name, "-- `entries` is", type(document["entries"]).__name__,
          "of", len(document["entries"]))
    entries = document["entries"]
    if isinstance(entries, list) and entries and isinstance(entries[0], dict):
        print("an entry row's own fields:", sorted(entries[0].keys()))
        index = {}
        for row in entries:
            index[row.get("entry_id") or row.get("entry")] = row
    else:
        index = {}
        print("the first three:", entries[:3])
    print("its filters, LITERAL:", json.dumps(document.get("filters")))
    for entry_id in want:
        row = index.get(entry_id)
        if row is None:
            print("   %-8s NOT in the population's `entries`" % entry_id)
            continue
        print("   %-8s %s" % (entry_id, json.dumps(row)[:500]))
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[3/$total] do the pair units overlap task hub1's 134?"
python3 - <<'PY'
import json, os, resource
HQ = "PseudoCoupHQ"
ARCH = os.path.join(HQ, "Research", "oracle", "arch_opcodes")
single = json.load(open(os.path.join(ARCH, "single_opcode_units.json")))
narrow = set()
for group in single["single_opcode_groups"]["go"]["narrow"]:
    for member in group["members"]:
        narrow.add(member["unit"])
pairs = set(row["unit"] for row in json.load(open("/tmp/one_pair.json")))
print("task o2's narrow rule holds %d go units" % len(narrow))
print("one-pair-plus-chaff go units: %d" % len(pairs))
print("in both: %d" % len(narrow & pairs))
print("the dictionary of task hub1 asked about 134 of the narrow units "
      "(the ones naming exactly one cell)")
document = json.load(open(os.path.join(HQ, "Research", "oracle", "hub",
                                       "dictionary.json")))
asked = set(row["unit"] for row in document["go_units"])
print("task hub1's own 134: %d; in both with the pair units: %d"
      % (len(asked), len(asked & pairs)))
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
