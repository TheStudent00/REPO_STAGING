#!/bin/bash
# L1 lane 24 — the closing measurements, on an instance whose /tmp was raised
# from 1g to 4g and memory from 8g to 12g because the 16-bit division's proof
# certificate was truncated at exactly the 1 GiB /tmp cap.
#   [1/5] the axioms the preservation theorem rests on, now that the module
#         has an object file for `#print axioms` to read
#   [2/5] the division ladder at bv_decide's default 10 s SAT ceiling
#   [3/5] the division ladder at a 600 s SAT ceiling
#   [4/5] the 16-bit case with the elaborator's heartbeat limit off as well,
#         which is where the certificate size showed up
#   [5/5] the spelling guard again, over every json this task wrote
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
PIPE=/projects/PseudoCoupHQ/Research/op_pipeline
export HOME=/work/L1home
mkdir -p "$HOME"

echo '[1/5] the axioms the preservation theorem rests on'
cd "$LEANDIR/archproof" || exit 1
lake build > /dev/null 2>&1
cat > /work/axioms.lean <<'LEAN'
import Archproof.Render
#print axioms Archproof.render_preserves
#print axioms Archproof.append_as_shift_or
#print axioms Archproof.sshiftRight_out_of_range
#print axioms Archproof.shiftInRange_says
LEAN
lake env lean /work/axioms.lean
echo "--- axioms exit $?"

echo '[2/5] the division ladder at the default 10 s SAT ceiling'
python3 "$LEANDIR/run_edges_L1.py" divide 2>&1 | head -12

echo '[3/5] the division ladder at a 600 s SAT ceiling'
python3 "$LEANDIR/run_edges_L1.py" divide_more 600 2>&1 | head -12

echo '[4/5] the 16-bit case with the heartbeat limit off as well, 4g /tmp'
df -h /tmp | tail -1
python3 - <<'PY'
import resource, subprocess, time
t0 = time.time()
p = subprocess.Popen(["lean", "Edges/divide_identity_16_nolimit.lean"],
                     cwd="/projects/PseudoCoupHQ/Research/op_pipeline/lean/archproof",
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out, _ = p.communicate()
print("exit %s  wall %.1f s  child peak %.1f MB"
      % (p.returncode, time.time() - t0,
         resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024.0))
print(out.decode("utf-8", "replace").strip() or "(no output: the theorem was accepted)")
PY
df -h /tmp | tail -1

echo '[5/5] the spelling guard, unmodified, over every json this task wrote'
cd "$PIPE" || exit 1
python3 "$PIPE/check_no_spelling_keys.py" \
  "$LEANDIR/L1_edges_selected.json" "$LEANDIR/L1_ten_edges.json" \
  "$LEANDIR/L1_three_undecided.json" "$LEANDIR/L1_divide_ladder.json" \
  "$LEANDIR/L1_divide_ladder_t600.json"
echo "--- guard exit $?"
grep -c exempt \
  "$LEANDIR/L1_edges_selected.json" "$LEANDIR/L1_ten_edges.json" \
  "$LEANDIR/L1_three_undecided.json" "$LEANDIR/L1_divide_ladder.json" \
  "$LEANDIR/L1_divide_ladder_t600.json" \
  "$LEANDIR/edges_L1.py" "$LEANDIR/term_to_lean.py" "$LEANDIR/run_edges_L1.py" \
  "$LEANDIR/archproof/Archproof/Render.lean"
