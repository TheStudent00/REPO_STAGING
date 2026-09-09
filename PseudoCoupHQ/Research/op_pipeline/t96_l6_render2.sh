#!/bin/bash
# TASK 96 round 19, lane 6.  The render and the analysis re-run with
# the walk that follows a base advanced by a constant (php's bytecode
# pointer) and the shared obtained-memory count.
set -x
cd PseudoCoupHQ/Research/op_pipeline

echo "[1/6] survey, with the constant advance followed"
python3 - <<'PY'
import json
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
        print("      %-6s %6s .. %-6s n=%-2d inside=%-5s indexed=%-5s"
              % (a["base"], a["smallest_displacement"],
                 a["largest_displacement"], a["sightings"],
                 a["inside_the_extent"],
                 a["reached_through_an_index_register"]))
        if a["advanced_by"]:
            print("           advanced by: %s"
                  % "; ".join(a["advanced_by"]))
print("smallest %s  largest %s  origin implied 0x%x"
      % (out["smallest_displacement_in_the_population"],
         out["largest_displacement_in_the_population"],
         out["the_origin_this_implies"]))
PY

echo "[2/6] render and gate"
python3 t96_onto_canonical_form.py 2>&1 | tail -30

echo "[3/6] the analysis"
python3 t96_analysis.py 2>&1 | tail -8

echo "[4/6] the three shortfalls, per unit"
python3 - <<'PY'
import json
d = json.load(open("t96_canonical.json"))
for r in d["records"]:
    s = r["the_three_shortfalls"]
    a = s["the_r15_collision"]
    b = s["memory_obtained_at_run_time"]
    c = s["an_input_block_holds_a_pointer"]
    print("%-58s r15: body_names=%-5s form_claims=%-5s gone=%-5s | "
          "obtained: n=%-2d gone=%-5s | pointer: areas=%d gone=%-5s "
          "n/a=%s"
          % (r["unit"], a["the_body_names_r15"],
             a["the_form_claims_r15"], a["gone"],
             b["sightings"], b["gone"], c["arriving_areas_found"],
             c["gone"], c["not_applicable"]))
PY

echo "[5/6] the spelling guard, ONE process, over every artifact this task wrote"
python3 check_no_spelling_keys.py t96_canonical.json t96_analysis.json
echo "spelling guard exit=$?"

echo "[6/6] grep -c exempt over this task's own artifacts"
grep -c exempt t96_canonical.json t96_analysis.json t96_wrapped_texts.txt \
  t96_onto_canonical_form.py t96_arriving_area.py t96_analysis.py
echo done
