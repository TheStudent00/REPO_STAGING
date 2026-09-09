#!/bin/bash
# L2 lane 10 -- the brief's deliverable 2, step 1: state each of the 259
# single-opcode rows as a theorem (or refuse it by cause), writing the
# ModelCheck_<lang>_<row> .lean files and check_L2.json.  This is
# model_translate.py's own `check` command; it does not run `lean` itself --
# that is lane 11.  Memory bound: model_translate.check_command's own
# MEMORY_CEILING_KB (6 GB), named abort ABORT_MEMORY_L2, already inside the
# command; this lane also prints its own peak RSS as a second reading.
set -u

TOTAL=1
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/$TOTAL] model_translate.py check"
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
