#!/bin/bash
# L1 lane 11 —
#   [1/2] the renderer's preservation theorem, first build. Whatever does not
#         close is a `sorry`, and the count of them is printed rather than
#         left in the build noise.
#   [2/2] the division ladder again with bv_decide's own SAT ceiling raised
#         from its 10 s default to 600 s, because a tool limit is a flag: the
#         answer is reported at both ceilings, never at the first alone.
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"

echo '[1/2] the renderer preservation theorem'
cat > "$LEANDIR/archproof/Archproof.lean" <<'LEAN'
import Archproof.Basic
import Archproof.Smoke
import Archproof.Api
import Archproof.Render
LEAN
cd "$LEANDIR/archproof" || exit 1
time lean Archproof/Render.lean > /work/render_out.txt 2>&1
echo "--- lean exit $?"
echo '--- Render.lean output, LITERAL'
cat /work/render_out.txt
echo "--- declarations using sorry: $(grep -c "declaration uses 'sorry'" /work/render_out.txt)"
echo "--- errors: $(grep -c 'error:' /work/render_out.txt)"

echo '[2/2] the division ladder at a 600 s SAT ceiling'
python3 "$LEANDIR/run_edges_L1.py" divide_more 600
echo "--- divide_more exit $?"
