#!/usr/bin/env bash
# t81 lane 15 — the SPELLING GUARD, unmodified, in ONE process, over
# every artifact this task produced; then the inventory those artifacts
# make, with sizes.
#
# THE GUARD IS NOT EDITED AND NOT WRAPPED. It is
# op_pipeline/check_no_spelling_keys.py, invoked with the artifact paths
# as its arguments exactly as task 75 invoked it. Its whole output is
# written to guard_task81.txt so `grep -c exempt` can be run against the
# file rather than against a retyping of it.
#
# ONE THING IS MEASURED HERE AND NOT ASSUMED: the guard holds one
# artifact in memory at a time (`check(path)` frees its payload before
# the next path), so its peak is set by the LARGEST file, which is
# coverage_extended.json at 1.27 GB of JSON. If that cannot be held
# inside this instance's 12 GB, the guard says so and the file is named
# in the report as the one artifact the guard could not read -- it is
# not dropped from the list to make the run pass.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
PIPELINE=PseudoCoupHQ/Research/op_pipeline
cd "$PIPELINE"

ARTIFACTS="
$REPO/t81/probes_cpp.json
$REPO/t81/diary_targets_cpp.json
$REPO/t81/inject_report_cpp2.json
$REPO/t81/instrumented_cpp.json
$REPO/t81/diary_state_cpp.json
$REPO/t81/diary_state_regen.json
$REPO/t81/probes_regen_slice.json
$REPO/t81/sample_probe_cost.json
$REPO/coverage_cpp_summary.json
$REPO/coverage_extended_summary.json
$REPO/super_ops_comparison_cpp.json
$REPO/super_ops_cpp.json
$REPO/coverage_c.json
$REPO/coverage_cpp.json
$REPO/coverage_c_and_cpp.json
$REPO/coverage_extended.json
"

say "[1/4] the artifacts, with their sizes"
for F in $ARTIFACTS ; do
  if [ -f "$F" ]; then
    printf '   %14d  %s\n' "$(stat -c %s "$F")" "${F#$REPO/}"
  else
    printf '   %14s  %s\n' ABSENT "${F#$REPO/}"
  fi
done
free -g | head -2

say "[2/4] EVERY artifact, ONE process, guard unmodified"
# shellcheck disable=SC2086
python3 "$PIPELINE/check_no_spelling_keys.py" $ARTIFACTS \
    > "$REPO/guard_task81.txt" 2>&1
RC=$?
echo "   guard exit=$RC"
cat "$REPO/guard_task81.txt"
echo "   grep -c exempt on that output:"
grep -c exempt "$REPO/guard_task81.txt" || true

say "[3/4] the one-process run's outcome, named"
if [ $RC -eq 0 ]; then
  echo "   the single process covered every artifact and passed"
else
  echo "   the single process did NOT pass or did not finish (exit $RC)."
  echo "   THIS IS A FLAG, not a thing to work around: an ABORT here is"
  echo "   the memory of a multi-gigabyte artifact, and a violation here"
  echo "   is a real violation. Neither is patched from this lane."
fi

say "[4/4] the guard file is unmodified"
git -C PseudoCoupHQ status --porcelain \
    Research/op_pipeline/check_no_spelling_keys.py
echo "   (no line above means the guard file is untouched)"
md5sum "$PIPELINE/check_no_spelling_keys.py"
echo "DONE t81_l15"
