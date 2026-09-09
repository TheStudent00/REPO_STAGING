#!/bin/bash
# TASK 96 round 19, lane 3.  The survey re-run with `lea` excluded and
# copies of a base followed.  Nothing is written.
set -x
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "[1/1] the arriving areas each body evidences"
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
        print("      %-6s %6s .. %-6s  n=%-2d inside_extent=%-5s "
              "indexed=%-5s also=%s"
              % (a["base"], a["smallest_displacement"],
                 a["largest_displacement"], a["sightings"],
                 a["inside_the_extent"],
                 a["reached_through_an_index_register"],
                 ",".join(a["also_named_by"]) or "-"))
        print("           first: %s" % a["first_sighting"])
print()
print("smallest displacement: %s"
      % out["smallest_displacement_in_the_population"])
print("largest  displacement: %s"
      % out["largest_displacement_in_the_population"])
print("origin implied: 0x%x   origin in force: 0x%x   span: 0x%x"
      % (out["the_origin_this_implies"], out["the_origin_in_force"],
         out["the_extent_span"]))
print("peak resident size kB: %d"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo done
