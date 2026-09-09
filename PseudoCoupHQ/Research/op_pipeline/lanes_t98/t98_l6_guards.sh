#!/usr/bin/env bash
# t98 lane 6 -- THE GUARDS.
#
#  1. `check_no_spelling_keys.py`, UNMODIFIED, in ONE process, over
#     EVERY artifact pane 5 reads: the pool, the term audit, the census,
#     every document of the canonical-form generation the pane walks,
#     and every shard of the term store it walks.  Its own transcript is
#     the evidence, and `grep -c exempt` over that transcript is printed.
#  2. `check_dashboard_py_no_spelling.py` over the python page code this
#     task touched -- the renderer, the new stats module, and the three
#     programs written for this task.
#  3. The guards' own files are proved unmodified by `git diff`.
#
# THE MEMORY BOUND: `ulimit -v 6291456` (6 GB of address space).
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "======== [1/4] the guards themselves, unmodified ========"
git -C /projects/PseudoCoupHQ diff --stat -- \
  Research/op_pipeline/check_no_spelling_keys.py \
  Research/op_pipeline/check_dashboard_py_no_spelling.py \
  Research/op_pipeline/check_dashboard_js_no_spelling.py
echo "(no lines above means no line of any guard changed)"
echo "sha256 of the data guard:"
sha256sum check_no_spelling_keys.py

echo
echo "======== [2/4] check_no_spelling_keys.py, ONE process, every artifact pane 5 reads ========"
ARTIFACTS=$(ls the_pool5.json audit65.json name_census6.json \
  canon40_wrapped_*.json canon40_interp.json \
  canon40_regen_store/*.json term66_store/*.json)
echo "artifacts handed to the guard: $(echo "$ARTIFACTS" | wc -l)"
( ulimit -v 6291456 ; python3 check_no_spelling_keys.py $ARTIFACTS ) \
  > t98_spelling_guard_transcript.txt 2>&1
echo "-- guard exit $?"
echo "transcript lines: $(wc -l < t98_spelling_guard_transcript.txt)"
echo "PASS lines:       $(grep -c '^PASS' t98_spelling_guard_transcript.txt)"
echo "FAIL lines:       $(grep -c '^FAIL' t98_spelling_guard_transcript.txt)"
echo "grep -c exempt:   $(grep -c exempt t98_spelling_guard_transcript.txt)"
echo "first line:"
head -1 t98_spelling_guard_transcript.txt
echo "last line:"
tail -1 t98_spelling_guard_transcript.txt

echo
echo "======== [3/4] check_dashboard_py_no_spelling.py over the python page code ========"
( ulimit -v 6291456 ; python3 check_dashboard_py_no_spelling.py \
    dashboard_ouro.py dashboard_stats.py \
    t98_probe_shapes.py t98_settle.py t98_render_check.py )
echo "-- exit $?"

echo
echo "======== [4/4] the javascript route is untouched ========"
git -C /projects/PseudoCoupHQ diff --stat -- \
  Research/op_pipeline/dashboard.html \
  Research/op_pipeline/dashboard_pane1.js \
  Research/op_pipeline/dashboard_pane23.js \
  Research/op_pipeline/dashboard_pane4.js \
  Research/op_pipeline/dashboard_pane5.js \
  Research/op_pipeline/dashboard_pane6.js \
  Research/op_pipeline/dashboard_join.js \
  Research/op_pipeline/dashboard_loader.js
echo "(no lines above means the javascript route changed by 0 lines)"
