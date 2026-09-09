#!/usr/bin/env bash
# t86_l8_guards_final.sh -- TASK 86, lane 8: EVERY GATE, against the
# FINAL code.  Lanes 5 and 6 ran before the window shifts were added and
# stand as the record of that; this is the run of record.
set -uo pipefail
cd PseudoCoupHQ/Research/op_pipeline || exit 2

BASE=b86366cd38c72e557064e44d8d062d83f7610e5d

echo "[1/6] the data guard is UNMODIFIED"
echo "  sha256: $(sha256sum check_no_spelling_keys.py | cut -d' ' -f1)"
git -C PseudoCoupHQ diff --stat "$BASE"..HEAD -- \
    Research/op_pipeline/check_no_spelling_keys.py
echo "  (no diff line above = byte-identical since the task-85 commit)"
echo
echo "[2/6] grep -c exempt over every artifact task 86 produced"
for f in t86_vcs_scale.json t86_sample.json t86_sample2.json \
         t86_all_panes.json t86_all_panes2.json; do
    echo "    $f: $(grep -c exempt "$f")"
done
echo
echo "[3/6] check_no_spelling_keys.py, ONE process, all five artifacts"
python3 check_no_spelling_keys.py \
    t86_vcs_scale.json t86_sample.json t86_sample2.json \
    t86_all_panes.json t86_all_panes2.json
echo "  exit $?"
echo
echo "[4/6] check_dashboard_py_no_spelling.py over the python page"
python3 check_dashboard_py_no_spelling.py dashboard_ouro.py viewer_build.py \
    2>&1 | grep -E "^(PASS|FAIL|operator inventory)"
echo "  exit ${PIPESTATUS[0]}"
echo
echo "[5/6] check_dashboard_js_no_spelling.py over the JavaScript route"
python3 check_dashboard_js_no_spelling.py \
    dashboard_join.js dashboard_loader.js dashboard_pane1.js \
    dashboard_pane23.js dashboard_pane4.js dashboard_pane5.js \
    dashboard_pane6.js 2>&1 | grep -E "^(PASS|FAIL|operator inventory)"
echo "  exit ${PIPESTATUS[0]}"
echo
echo "[6/6] the JavaScript route untouched, and the vocabulary grep"
echo "-- git diff (working tree), lines:"
git -C PseudoCoupHQ diff -- \
    Research/op_pipeline/dashboard.html \
    Research/op_pipeline/dashboard_pane1.js \
    Research/op_pipeline/dashboard_pane23.js \
    Research/op_pipeline/dashboard_pane4.js \
    Research/op_pipeline/dashboard_pane5.js \
    Research/op_pipeline/dashboard_pane6.js | wc -l
echo "-- git diff $BASE..HEAD, lines (the daemon commits every 30 s, so"
echo "   this is the diff that proves it):"
git -C PseudoCoupHQ diff "$BASE"..HEAD -- \
    Research/op_pipeline/dashboard.html \
    Research/op_pipeline/dashboard_pane1.js \
    Research/op_pipeline/dashboard_pane23.js \
    Research/op_pipeline/dashboard_pane4.js \
    Research/op_pipeline/dashboard_pane5.js \
    Research/op_pipeline/dashboard_pane6.js | wc -l
echo "-- grep -nEi 'round|bank|lap' over the changed page, everything:"
grep -nEi 'round|bank|lap' dashboard_ouro.py dashboard_ouro.html
echo "-- the same, minus the CSS property and the sentence that names the"
echo "   retired defect:"
grep -nEi 'round|bank|lap' dashboard_ouro.py dashboard_ouro.html \
  | grep -vE 'background|collapse' | grep -v 'grep=banked' || echo "  (no match)"
