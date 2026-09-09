#!/bin/bash
# L1 lane 15 — the renderer preservation theorem, build 3. The C model now
# carries a shift by a plain integer count beside the shift by a computed
# holder, because C's shift operand IS an int after the usual promotions, not
# a value of the shifted type; that is what makes the slice and the append
# renderable at all. Every remaining `sorry` is counted and named.
set -u
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"
echo '[1/1] Render.lean, build 3'
cd "$LEANDIR/archproof" || exit 1
time lean Archproof/Render.lean > /work/render4_out.txt 2>&1
echo "--- lean exit $?"
grep -v 'linter.unusedSimpArgs\|Hint: Omit it\|^$\|Note: This linter' /work/render4_out.txt | head -140
echo "--- declarations using sorry: $(grep -c "declaration uses 'sorry'" /work/render4_out.txt)"
echo "--- error lines: $(grep -c 'error:' /work/render4_out.txt)"
