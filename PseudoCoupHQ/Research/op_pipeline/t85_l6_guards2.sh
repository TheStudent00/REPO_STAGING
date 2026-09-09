#!/usr/bin/env bash
# t85_l6_guards2.sh -- TASK 85, lane 6: THE GUARDS, RE-RUN after the python
# guard FAILED on a literal path separator in a membership test.
#
# THE SPELLING BAN, mechanically.  Every artifact task 85 produced is
# walked by the UNMODIFIED check_no_spelling_keys.py in ONE process; the
# python page code is walked by check_dashboard_py_no_spelling.py; and
# the JavaScript route -- which this task did not touch -- is walked by
# check_dashboard_js_no_spelling.py so that its passing is measured
# rather than assumed.
set -uo pipefail

OP=/projects/PseudoCoupHQ/Research/op_pipeline
cd "$OP" || exit 2
total=6

echo "[1/$total] the data guard is UNMODIFIED"
git -C /projects/PseudoCoupHQ status --porcelain -- \
    Research/op_pipeline/check_no_spelling_keys.py
echo "  (no line above means git sees no change to it)"
echo "  sha256: $(sha256sum check_no_spelling_keys.py | cut -d' ' -f1)"

echo
echo "[2/$total] grep -c exempt over the guard, and over every artifact"
echo "  check_no_spelling_keys.py: $(grep -c exempt check_no_spelling_keys.py)"
for f in t85_gitfacts.json t85_sample.json t85_all_moments.json \
         t85_all_moments2.json t85_one_moment_proof.json; do
    if [ -f "$f" ]; then
        echo "  $f: $(grep -c exempt "$f")"
    else
        echo "  $f: ABSENT"
    fi
done

echo
echo "[3/$total] check_no_spelling_keys.py, UNMODIFIED, ONE process, over"
echo "          every artifact task 85 produced"
python3 check_no_spelling_keys.py \
    t85_gitfacts.json t85_sample.json t85_all_moments.json \
    t85_all_moments2.json t85_one_moment_proof.json
echo "  exit $?"

echo
echo "[4/$total] check_dashboard_py_no_spelling.py over the python page code"
python3 check_dashboard_py_no_spelling.py dashboard_ouro.py viewer_build.py
echo "  exit $?"

echo
echo "[5/$total] check_dashboard_js_no_spelling.py over the JavaScript route"
echo "          this task did NOT touch"
python3 check_dashboard_js_no_spelling.py \
    dashboard_join.js dashboard_loader.js dashboard_pane23.js \
    dashboard_pane4.js dashboard_pane5.js dashboard_pane6.js
echo "  exit $?"

echo
echo "[6/$total] git diff over the JavaScript route -- must be empty"
git -C /projects/PseudoCoupHQ diff --stat -- \
    Research/op_pipeline/dashboard.html \
    Research/op_pipeline/dashboard_pane1.js \
    Research/op_pipeline/dashboard_pane23.js \
    Research/op_pipeline/dashboard_pane4.js \
    Research/op_pipeline/dashboard_pane5.js \
    Research/op_pipeline/dashboard_pane6.js
echo "  lines of diff: $(git -C /projects/PseudoCoupHQ diff -- \
    Research/op_pipeline/dashboard.html \
    Research/op_pipeline/dashboard_pane*.js | wc -l)"
