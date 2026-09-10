#!/usr/bin/env bash
# hub2_l4_modes_and_exclusions_again.sh -- task hub2, lane 4.  Writes
# nothing.  Lane 3 read task o13's rows for a top-level `outcome` field
# they do not carry (the verdict is in `q3` and `q3_guarded`) and read
# the two populations' `entries` as a list where both are dicts; this
# lane asks the same two questions the way the objects are shaped.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
total=2

echo "[1/$total] task o13's mode store, read through q3 and q3_guarded"
python3 - <<'PY'
import json, os, collections, resource
EMU = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
mode = json.load(open(os.path.join(EMU, "mode", "mode_results.json")))
PROVED = ("PROVED", "PROVED_ON_SHIP")
for target in sorted(mode["runs"]):
    rows = mode["runs"][target]
    counter = collections.Counter()
    proved = []
    for row in rows:
        first = (row.get("q3") or {})
        guarded = (row.get("q3_guarded") or {})
        def word(check):
            outcome = check.get("outcome")
            if outcome in PROVED:
                return "proved"
            extension = (check.get("under_caller_extension") or {}).get("outcome")
            if extension in PROVED:
                return "proved under caller extension"
            return outcome
        one = word(first)
        two = word(guarded) if guarded else None
        counter[(one, two)] += 1
        if one in ("proved", "proved under caller extension") or \
           two in ("proved", "proved under caller extension"):
            proved.append(row)
    print("--- %s: %d rows" % (target, len(rows)))
    print("| the first posing | the guarded posing | rows |")
    print("|---|---|---|")
    for key in sorted(counter, key=lambda k: (str(k[0]), str(k[1]))):
        print("| %s | %s | %d |" % (key[0], key[1], counter[key]))
    print("entries the mode re-run leaves proved: %d"
          % len(set(r["entry_id"] for r in proved)))
    with_mode = [r for r in proved if r.get("mode")]
    print("of those, rows whose emulation carries a rendered mode: %d" % len(with_mode))
    if with_mode:
        row = with_mode[0]
        print("one such row's `mode`, LITERAL:")
        print(json.dumps(row["mode"], indent=1)[:1200])
        print("its entry %s, x unit %s, params %s"
              % (row["entry_id"], row["x_unit"],
                 [(p["name"], p["holder"], p["bits"], p["family"])
                  for p in row["params"]]))
    handle = open("/tmp/mode_%s.json" % target, "w")
    json.dump([r["entry_id"] for r in proved], handle)
    handle.close()
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[2/$total] why each entry is outside o7's and o11's populations"
python3 - <<'PY'
import json, os, resource
HQ = "PseudoCoupHQ"
EMU = os.path.join(HQ, "Research", "oracle", "cross_construction", "emulation")
OP = os.path.join(HQ, "Research", "op_pipeline")
want = ["E00302", "E00163", "E00310", "E00316", "E00025", "E00058"]
pool = json.load(open(os.path.join(OP, "the_pool5.json")))
facts = {}
for entry in pool["entries"]:
    if entry["entry_id"] not in want:
        continue
    languages = set()
    for member in entry["members"]:
        unit = member["unit"] if isinstance(member, dict) else member
        languages.add(unit.split("/")[0])
    facts[entry["entry_id"]] = {
        "languages": sorted(languages),
        "member_count": entry["member_count"],
        "layer5_normalized_texts": entry.get("layer5_normalized_texts"),
        "members_not_layer5_eligible": entry.get("members_not_layer5_eligible"),
    }
del pool
for name, path in [("o7 (c)", os.path.join(EMU, "emulation_population.json")),
                   ("o11 (rust)", os.path.join(EMU, "rust",
                                               "rust_population.json"))]:
    document = json.load(open(path))
    entries = document["entries"]
    print("===", name, "-- population of", len(entries), "entries")
    print("its filters, LITERAL:", json.dumps(document.get("filters")))
    key = sorted(entries.keys())[0]
    print("a population row, LITERAL:", json.dumps({key: entries[key]})[:600])
    for entry_id in want:
        inside = entry_id in entries
        fact = facts.get(entry_id) or {}
        texts = fact.get("layer5_normalized_texts")
        print("   %-8s in the population: %-5s   member languages %s   "
              "layer-5 texts %s"
              % (entry_id, inside, fact.get("languages"),
                 0 if not texts else len(texts)))
print("peak kB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
