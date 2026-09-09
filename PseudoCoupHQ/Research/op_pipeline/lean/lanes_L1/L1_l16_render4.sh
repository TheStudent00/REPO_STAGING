#!/bin/bash
# L1 lane 16 — the renderer preservation theorem, build 4. Build 3 carried a
# duplicated lemma block from a bad patch, and its case proofs named the
# theorem's outer width where they meant the case's own; both are corrected.
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"
echo '[1/1] Render.lean, build 4'
cd "$LEANDIR/archproof" || exit 1
time lean Archproof/Render.lean > /work/render5_out.txt 2>&1
echo "--- lean exit $?"
grep -v 'linter.unusedSimpArgs\|Hint: Omit it\|^$\|Note: This linter\|̵' /work/render5_out.txt | head -120
echo "--- declarations using sorry: $(grep -c "declaration uses 'sorry'" /work/render5_out.txt)"
echo "--- error lines: $(grep -c 'error:' /work/render5_out.txt)"
