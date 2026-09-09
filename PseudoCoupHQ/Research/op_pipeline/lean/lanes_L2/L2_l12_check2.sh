#!/bin/bash
# L2 lane 12 -- re-run of lane 10's `check` command, needed because lane 11
# found a bug: the THEOREM template (model_translate.py) imported only
# Archproof.Model, so every fallback to `bv_decide` failed with "please
# include import Std.Tactic.BVDecide" -- a LEAN_REFUSED that was really the
# translator's own file missing an import, not a reading of the two models.
# Fixed in model_translate.py (THEOREM string now also imports
# Std.Tactic.BVDecide, matching every other bv_decide theorem already in
# this project: Render.lean, Api.lean, Smoke.lean, every Edges/*.lean).
# check_L2.json's rows that lane 11 rewrote from STATED to LEAN_REFUSED must
# be reset to STATED before lane 13 (the fixed run) will retry them, so this
# lane regenerates check_L2.json from scratch rather than patching it --
# check_command is deterministic and idempotent, so this is the same 172
# STATED / 87 REFUSED split lane 10 found, freshly stated with no prior
# outcome carried over.
set -u

TOTAL=1
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/$TOTAL] model_translate.py check (re-run after the THEOREM import fix)"
python3 -c "
import resource, sys, time
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline/lean')
import model_translate as M
start = time.time()
M.check_command()
print('check wall %.1f s' % (time.time() - start))
print('check peak RSS %d kB'
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
"
echo "--- exit $?"
