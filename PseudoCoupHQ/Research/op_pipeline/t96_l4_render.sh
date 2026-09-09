#!/bin/bash
# TASK 96 round 19, lane 4.  Part A + Part B: render the eleven onto
# the canonical form, and again with the seventh block kind, and gate
# each against the unit's OWN ship body.
set -x
cd PseudoCoupHQ/Research/op_pipeline

echo "[1/3] render and gate"
python3 t96_onto_canonical_form.py 2>&1 | tail -40

echo "[2/3] the spelling guard, ONE process, over this task's artifact"
python3 check_no_spelling_keys.py t96_canonical.json
echo "spelling guard exit=$?"

echo "[3/3] grep -c exempt over this task's own artifacts"
grep -c exempt t96_canonical.json t96_onto_canonical_form.py t96_arriving_area.py
echo done
