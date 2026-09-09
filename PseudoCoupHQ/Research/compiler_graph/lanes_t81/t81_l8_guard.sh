#!/usr/bin/env bash
# t81 lane 8 — the SPELLING GUARD, unmodified, in ONE process, over
# every artifact this task produced; then the inventory those artifacts
# make, with sizes.
#
# THE GUARD IS NOT EDITED AND NOT WRAPPED. It is
# op_pipeline/check_no_spelling_keys.py, invoked with the artifact paths
# as its arguments exactly as task 75 invoked it. Its whole output is
# written to guard_task81.txt so `grep -c exempt` can be run against the
# file rather than against a retyping of it.
set -u
say() { echo; echo "======== $* ========"; }
REPO=/projects/PseudoCoupHQ/Research/compiler_graph
PIPELINE=/projects/PseudoCoupHQ/Research/op_pipeline
cd "$PIPELINE"

say "[1/4] the artifacts, with their sizes"
for F in \
    "$REPO/t81/probes_cpp.json" \
    "$REPO/t81/diary_targets_cpp.json" \
    "$REPO/t81/inject_report_cpp2.json" \
    "$REPO/t81/instrumented_cpp.json" \
    "$REPO/t81/diary_state_cpp.json" \
    "$REPO/t81/sample_probe_cost.json" \
    "$REPO/coverage_cpp_summary.json" \
    "$REPO/coverage_c.json" \
    "$REPO/coverage_cpp.json" \
    "$REPO/coverage_c_and_cpp.json" \
    "$REPO/super_ops_cpp.json" \
    "$REPO/super_ops_comparison_cpp.json" ; do
  if [ -f "$F" ]; then
    printf '   %14d  %s\n' "$(stat -c %s "$F")" "$(basename "$F")"
  else
    printf '   %14s  %s\n' ABSENT "$(basename "$F")"
  fi
done
free -g | head -2

say "[2/4] EVERY artifact, ONE process, guard unmodified"
python3 "$PIPELINE/check_no_spelling_keys.py" \
    "$REPO/t81/probes_cpp.json" \
    "$REPO/t81/diary_targets_cpp.json" \
    "$REPO/t81/inject_report_cpp2.json" \
    "$REPO/t81/instrumented_cpp.json" \
    "$REPO/t81/diary_state_cpp.json" \
    "$REPO/t81/sample_probe_cost.json" \
    "$REPO/coverage_cpp_summary.json" \
    "$REPO/super_ops_comparison_cpp.json" \
    "$REPO/super_ops_cpp.json" \
    "$REPO/coverage_c.json" \
    "$REPO/coverage_cpp.json" \
    "$REPO/coverage_c_and_cpp.json" \
    > "$REPO/guard_task81.txt" 2>&1
RC=$?
echo "   guard exit=$RC"
cat "$REPO/guard_task81.txt"
echo "   grep -c exempt on that output:"
grep -c exempt "$REPO/guard_task81.txt" || true

say "[3/4] the one-process run's outcome, named"
if [ $RC -eq 0 ]; then
  echo "   the single process covered all twelve artifacts and passed"
else
  echo "   the single process did NOT pass or did not finish (exit $RC)."
  echo "   THIS IS A FLAG, not a thing to work around: an ABORT here is"
  echo "   the memory of a multi-gigabyte artifact, and a violation here"
  echo "   is a real violation. Neither is patched from this lane."
fi

say "[4/4] the guard file is unmodified"
git -C /projects/PseudoCoupHQ status --porcelain \
    Research/op_pipeline/check_no_spelling_keys.py
echo "   (no line above means the guard file is untouched)"
md5sum "$PIPELINE/check_no_spelling_keys.py"
echo "DONE t81_l8"
