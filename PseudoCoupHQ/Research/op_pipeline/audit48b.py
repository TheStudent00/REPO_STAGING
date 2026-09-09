#!/usr/bin/env python3
"""audit48b.py -- every number the report states, computed here with its
breakdown, so no figure in the log is typed by hand.

  * per population: units, terms built, terms proved, terms disproved
    (and therefore WITHDRAWN -- a term that does not prove is not a
    row), terms undecided on both routes;
  * the consistency check: no unit is PROVED on one route and DISPROVED
    on the other;
  * layer 3 against layer 5: identity, and the distinct-text counts
    that carry the normalizer's purpose;
  * the census headline.

No operator token appears in this file.
"""

import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def documents():
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "layer4b_terms_%s.json" % lang)
        if os.path.exists(path):
            out.append(("original", path))
    path = os.path.join(HERE, "layer4b_interp.json")
    if os.path.exists(path):
        out.append(("interpreter", path))
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "layer4b_regen_store",
                                              "*.json"))):
        out.append(("regenerated", path))
    return out


def main():
    per = collections.defaultdict(collections.Counter)
    contradictions = []
    distinct3 = collections.defaultdict(set)
    distinct5 = collections.defaultdict(set)
    for population, path in documents():
        document = json.load(open(path))
        for name, record in document["units"].items():
            counter = per[population]
            counter["units"] += 1
            ship = record["gate_ship_verdict"]
            text = record["gate_textorder_verdict"]
            if not record.get("term_built"):
                counter["no term built"] += 1
                continue
            counter["term built"] += 1
            proved = "PROVED_EQUAL" in (ship, text)
            disproved = "DISPROVED" in (ship, text)
            if proved and disproved:
                contradictions.append((name, ship, text))
            if disproved:
                counter["term DISPROVED -- withdrawn"] += 1
            elif proved:
                counter["term proved on at least one route"] += 1
            else:
                counter["term undecided on both routes"] += 1
            if ship == "PROVED_EQUAL":
                counter["proved on route one (the ship simulation)"] += 1
            if text == "PROVED_EQUAL":
                counter["proved on route two (the text-order walk)"] += 1
            if record.get("layer5_equals_layer3"):
                counter["layer 5 identical to layer 3"] += 1
            if not disproved and proved:
                distinct3[population].add(record["layer3_wrapped_text"])
                distinct5[population].add(
                    record["layer5_normalized_text"])
    grand = collections.Counter()
    for population in sorted(per):
        print("POPULATION: %s" % population)
        for key in sorted(per[population]):
            print("  %-48s %7d" % (key, per[population][key]))
            grand[key] += per[population][key]
        print("  %-48s %7d"
              % ("distinct layer-3 texts, proved units only",
                 len(distinct3[population])))
        print("  %-48s %7d"
              % ("distinct layer-5 texts, proved units only",
                 len(distinct5[population])))
        print("")
    print("ALL THREE POPULATIONS")
    for key in sorted(grand):
        print("  %-48s %7d" % (key, grand[key]))
    print("")
    print("CONSISTENCY -- units proved on one route and disproved on "
          "the other: %d" % len(contradictions))
    for item in contradictions[:20]:
        print("  %s" % (item,))
    census_path = os.path.join(HERE, "name_census3.json")
    if os.path.exists(census_path):
        census = json.load(open(census_path))
        print("")
        print("THE CENSUS HEADLINE")
        print("  distinct producers with no term: %d"
              % len(census["entries"]))
        rows = sum(one["rows_blocked"] for one in census["entries"])
        print("  rows blocked:                    %d" % rows)
        units = set()
        for entry in census["entries"]:
            units.update(entry["units_blocked"])
        print("  units carrying at least one such row: %d" % len(units))


if __name__ == "__main__":
    main()
