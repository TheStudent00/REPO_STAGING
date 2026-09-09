#!/bin/bash
# L1 lane 17 — the renderer preservation theorem, build 6. Three gaps build 4
# named are addressed: the append lemma's arithmetic step lacked the bound the
# bit index already carries; the slice case needed the equality taken on the
# number rather than on the holder; the append case at a zero-width left
# operand needed that width substituted before the bits line up.
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"
echo '[1/1] Render.lean, build 6'
cd "$LEANDIR/archproof" || exit 1
time lean Archproof/Render.lean > /work/render7_out.txt 2>&1
echo "--- lean exit $?"
grep -v 'linter.unusedSimpArgs\|Hint: Omit it\|^$\|Note: This linter\|̵' /work/render7_out.txt | head -120
echo "--- declarations using sorry: $(grep -c "declaration uses 'sorry'" /work/render7_out.txt)"
echo "--- error lines: $(grep -c 'error:' /work/render7_out.txt)"
