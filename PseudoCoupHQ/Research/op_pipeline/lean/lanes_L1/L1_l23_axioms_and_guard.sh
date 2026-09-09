#!/bin/bash
# L1 lane 23 —
#   [1/3] what the preservation theorem actually rests on. A build with no
#         errors is not the same claim as a proof with no holes: `#print
#         axioms` names every axiom the kernel used, and `sorryAx` appearing
#         there would mean a hole regardless of what the build said.
#   [2/3] the whole lake project builds, so nothing in it is stale
#   [3/3] the spelling guard, unmodified, over every json this task wrote
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
PIPE=/projects/PseudoCoupHQ/Research/op_pipeline
export HOME=/work/L1home
mkdir -p "$HOME"

echo '[1/3] the axioms the preservation theorem rests on'
cd "$LEANDIR/archproof" || exit 1
cat > /work/axioms.lean <<'LEAN'
import Archproof.Render
#print axioms Archproof.render_preserves
#print axioms Archproof.append_as_shift_or
#print axioms Archproof.sshiftRight_out_of_range
#print axioms Archproof.shiftInRange_says
LEAN
LEAN_PATH="$LEANDIR/archproof/.lake/build/lib/lean" lean /work/axioms.lean

echo '[2/3] lake build of the whole project'
cat > "$LEANDIR/archproof/Archproof.lean" <<'LEAN'
import Archproof.Basic
import Archproof.Smoke
import Archproof.Api
import Archproof.Render
LEAN
lake build 2>&1 | tail -20
echo "--- lake build exit $?"

echo '[3/3] the spelling guard, unmodified, over every json this task wrote'
cd "$PIPE" || exit 1
python3 "$PIPE/check_no_spelling_keys.py" \
  "$LEANDIR/L1_edges_selected.json" \
  "$LEANDIR/L1_ten_edges.json" \
  "$LEANDIR/L1_three_undecided.json" \
  "$LEANDIR/L1_divide_ladder.json" \
  "$LEANDIR/L1_divide_ladder_t600.json"
echo "--- guard exit $?"
echo '--- grep -c exempt over every file this task added'
grep -c exempt \
  "$LEANDIR/L1_edges_selected.json" "$LEANDIR/L1_ten_edges.json" \
  "$LEANDIR/L1_three_undecided.json" "$LEANDIR/L1_divide_ladder.json" \
  "$LEANDIR/L1_divide_ladder_t600.json" \
  "$LEANDIR/edges_L1.py" "$LEANDIR/term_to_lean.py" "$LEANDIR/run_edges_L1.py" \
  "$LEANDIR/archproof/Archproof/Render.lean"
