#!/bin/bash
# L1 lane 12 —
#   [1/2] the renderer preservation theorem, second build. The width
#         arguments of extract and concat are now written out (Lean could not
#         infer them from an underscore), the bit-vector facts the hard cases
#         rest on are stated as their own named theorems, and every remaining
#         `sorry` is counted rather than left in the build noise.
#   [2/2] the operators the term walk emits, counted over EVERY printed
#         layer-5 text in the_pool5.json, each marked with the Render.lean
#         constructor that covers it or the reason the subset stops short.
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"

echo '[1/2] the renderer preservation theorem, build 2'
cd "$LEANDIR/archproof" || exit 1
time lean Archproof/Render.lean > /work/render2_out.txt 2>&1
echo "--- lean exit $?"
echo '--- errors only, LITERAL'
grep -n 'error' /work/render2_out.txt | head -60
echo "--- declarations using sorry: $(grep -c "declaration uses 'sorry'" /work/render2_out.txt)"
echo "--- error lines: $(grep -c 'error:' /work/render2_out.txt)"
echo '--- which declarations use sorry'
grep -B1 "declaration uses 'sorry'" /work/render2_out.txt | head -40

echo '[2/2] the operators the term walk emits, over the whole pool'
python3 "$LEANDIR/edges_L1.py" emitted
echo "--- emitted exit $?"
