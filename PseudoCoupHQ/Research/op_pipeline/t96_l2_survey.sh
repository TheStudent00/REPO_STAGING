#!/bin/bash
# TASK 96 round 19, lane 2.  The measurement that decides AREA_ORIGIN.
# Nothing is written.
set -x
cd PseudoCoupHQ/Research/op_pipeline

echo "[1/2] the displacements every body spells from an arriving base"
python3 - <<'PY'
import json
import resource
import t96_arriving_area as AREA

d = json.load(open("t94_recarve.json"))
pairs = []
for r in d["records"]:
    rc = r.get("recarved") or {}
    pairs.append((r["unit"], rc.get("body_verbatim")))
out = AREA.survey(pairs)
for row in out["records"]:
    if row.get("body", 0) is None:
        print("%-58s no body" % row["unit"])
        continue
    print("%-58s %d areas" % (row["unit"], len(row["areas"])))
    for a in row["areas"]:
        print("      %-6s %6s .. %-6s  sightings %2d   first: %s"
              % (a["base"], a["smallest_displacement"],
                 a["largest_displacement"], a["sightings"],
                 a["first_sighting"]))
print()
print("smallest displacement in the population: %s"
      % out["smallest_displacement_in_the_population"])
print("largest  displacement in the population: %s"
      % out["largest_displacement_in_the_population"])
print("the origin this implies: 0x%x" % out["the_origin_this_implies"])
print("the origin in force    : 0x%x" % out["the_origin_in_force"])
print("the extent span        : 0x%x" % out["the_extent_span"])
print("peak resident size kB: %d"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[2/2] the recorded arrival contract families, for comparison"
python3 - <<'PY'
import json
d = json.load(open("t94_recarve.json"))
for r in d["records"]:
    c = r.get("arrival_contract") or {}
    fam = []
    for key in ("a", "b", "c", "d"):
        if c.get(key):
            fam.append(c[key])
    print("%-58s contract %-14s result %s/%s"
          % (r["unit"], ",".join(fam) or "(none)",
             c.get("result"), c.get("result_width")))
PY
echo done
