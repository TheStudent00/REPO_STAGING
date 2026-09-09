#!/usr/bin/env bash
# t86_l5_guards.sh -- TASK 86, lane 5: EVERY GATE, in one place.
#
#   1. check_no_spelling_keys.py, UNMODIFIED, in ONE process over every
#      artifact task 86 produced, with `grep -c exempt` on each;
#   2. check_dashboard_py_no_spelling.py over the python page;
#   3. check_dashboard_js_no_spelling.py over the JavaScript route,
#      which this task did not touch;
#   4. the JavaScript route and Ourobrowser proved untouched -- both the
#      working tree and the whole span of task 86's commits, because the
#      repository's own daemon commits every 30 s and a working-tree
#      diff alone would prove nothing here;
#   5. the vocabulary grep: `round`, `bank`, `lap` over the new code.
#
# Node: hq.research.compiler_graph.dashboard
set -uo pipefail
cd /projects/PseudoCoupHQ/Research/op_pipeline || exit 2

#: the commit that landed task 85 -- everything after it on these paths
#: is task 86.
BASE=b86366cd38c72e557064e44d8d062d83f7610e5d

echo "[1/5] the data guard, unmodified, ONE process, every artifact"
git -C /projects/PseudoCoupHQ status --porcelain -- \
    Research/op_pipeline/check_no_spelling_keys.py
echo "  sha256: $(sha256sum check_no_spelling_keys.py | cut -d' ' -f1)"
echo "  git diff over the guard itself, from the task-85 commit to HEAD:"
git -C /projects/PseudoCoupHQ diff --stat "$BASE"..HEAD -- \
    Research/op_pipeline/check_no_spelling_keys.py
echo "  (nothing above means the guard is byte-identical)"
echo
echo "  grep -c exempt over every artifact:"
for f in t86_vcs_scale.json t86_sample.json t86_sample2.json \
         t86_all_panes.json; do
    echo "    $f: $(grep -c exempt "$f")"
done
echo
python3 check_no_spelling_keys.py \
    t86_vcs_scale.json t86_sample.json t86_sample2.json t86_all_panes.json
echo "  exit $?"
echo

echo "[2/5] check_dashboard_py_no_spelling.py over the python page"
python3 check_dashboard_py_no_spelling.py dashboard_ouro.py viewer_build.py
echo "  exit $?"
echo

echo "[3/5] check_dashboard_js_no_spelling.py over the JavaScript route"
python3 check_dashboard_js_no_spelling.py
echo "  exit $?"
echo

echo "[4/5] the JavaScript route, untouched"
echo "-- git diff (working tree) over dashboard.html and every dashboard_pane*.js"
git -C /projects/PseudoCoupHQ diff -- \
    Research/op_pipeline/dashboard.html \
    Research/op_pipeline/dashboard_pane1.js \
    Research/op_pipeline/dashboard_pane23.js \
    Research/op_pipeline/dashboard_pane4.js \
    Research/op_pipeline/dashboard_pane5.js \
    Research/op_pipeline/dashboard_pane6.js \
    Research/op_pipeline/dashboard_join.js \
    Research/op_pipeline/dashboard_loader.js | tee /tmp/jsdiff.txt | wc -l
echo "-- git diff $BASE..HEAD over the same paths (the daemon commits every 30 s,"
echo "   so this is the diff that actually proves it)"
git -C /projects/PseudoCoupHQ diff "$BASE"..HEAD -- \
    Research/op_pipeline/dashboard.html \
    Research/op_pipeline/dashboard_pane1.js \
    Research/op_pipeline/dashboard_pane23.js \
    Research/op_pipeline/dashboard_pane4.js \
    Research/op_pipeline/dashboard_pane5.js \
    Research/op_pipeline/dashboard_pane6.js \
    Research/op_pipeline/dashboard_join.js \
    Research/op_pipeline/dashboard_loader.js | tee /tmp/jsdiff2.txt | wc -l
echo "-- the files those globs actually match, so the list is not a claim:"
ls -1 dashboard.html dashboard_pane*.js dashboard_join.js dashboard_loader.js
echo

echo "[5/5] the vocabulary grep over the changed page"
echo "-- grep -nEi 'round|bank|lap' dashboard_ouro.py dashboard_ouro.html"
grep -nEi 'round|bank|lap' dashboard_ouro.py dashboard_ouro.html || \
    echo "  (no match)"
echo
echo "-- the same, with the CSS property and the retired-defect sentence removed"
grep -nEi 'round|bank|lap' dashboard_ouro.py dashboard_ouro.html \
  | grep -vE 'background|collapse' | grep -v 'grep=banked' || \
    echo "  (no match)"
