#!/bin/bash
# L2 lane 5 — the five opcodes again (named definitions, quoted setters), then
# the whole sweep: every mnemonic the reference's opcode table holds, at every
# operand shape model_translate.py spells, written into Archproof/Model.lean.
set -u

TOTAL=3
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/$TOTAL] the five opcodes, end to end"
python3 model_translate.py five
echo "--- exit $?"

echo "[2/$TOTAL] the sweep"
python3 -c "
import resource, sys, time
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline/lean')
import model_translate as M
start = time.time()
M.model_command(M.HERE, M.os.path.join(M.HERE, 'archproof', 'Archproof'))
print('sweep wall %.1f s' % (time.time() - start))
print('sweep peak RSS %d kB'
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
"
echo "--- exit $?"

echo "[3/$TOTAL] Model.lean: its size, and lake build of it alone"
wc -l archproof/Archproof/Model.lean
head -40 archproof/Archproof/Model.lean
cd archproof || exit 1
cat > Archproof.lean <<'LEAN'
import Archproof.Basic
import Archproof.Model
import Archproof.Render
LEAN
time lake build Archproof.Model 2>&1 | tail -30
echo "--- lake build exit $?"
