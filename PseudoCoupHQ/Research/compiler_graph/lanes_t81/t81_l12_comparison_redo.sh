#!/usr/bin/env bash
# t81 lane 12 — the both-ways comparison re-run after ONE character was
# corrected, and the go artifact proved byte-identical.
#
# WHAT LANE 7 FOUND. Re-running the go comparison with the new
# `--language` default produced an artifact identical to task 75's in
# every line but one: the `why_both` sentence read "9809" where the
# stored artifact reads "9,809", because the sentence is now COMPUTED
# from the artifact in hand and the format string had no thousands
# separator. That is a regression in shape, small but real, and it is
# fixed rather than excused. This lane re-runs both comparisons on the
# corrected program and diffs the go one against task 75's file.
set -u
say() { echo; echo "======== $* ========"; }
REPO=PseudoCoupHQ/Research/compiler_graph
cd "$REPO"

say "[1/3] the cpp comparison, re-run on the corrected program"
python3 t81/run_with_peak.py report_super_ops.py compare \
    --candidates super_ops_cpp.json \
    --output-side PseudoCoupHQ/Research/op_pipeline/super_ops3.json \
    --language cpp \
    --out super_ops_comparison_cpp.json 2>&1 | tail -20

say "[2/3] the go comparison, re-run with the DEFAULT language"
python3 t81/run_with_peak.py report_super_ops.py compare \
    --candidates super_ops_go.json \
    --output-side PseudoCoupHQ/Research/op_pipeline/super_ops3.json \
    --out /work/super_ops_comparison_go_again2.json 2>&1 | tail -10

say "[3/3] byte for byte against task 75's artifact"
if diff super_ops_comparison_go.json \
        /work/super_ops_comparison_go_again2.json ; then
  echo "   IDENTICAL -- zero regressions, proved rather than asserted"
else
  echo "   DIFFERS -- the lines above are the whole difference"
fi
echo "   the two sentences, LITERAL:"
grep -m1 '"why_both"' super_ops_comparison_go.json
grep -m1 '"why_both"' super_ops_comparison_cpp.json
echo "DONE t81_l12"
