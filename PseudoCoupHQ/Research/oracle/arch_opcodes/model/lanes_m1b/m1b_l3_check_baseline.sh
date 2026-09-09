#!/usr/bin/env bash
# m1b_l3_check_baseline.sh -- task m1b: the BASELINE reading of the
# check the brief asks to hold unchanged.
#
# WHAT IS CHECKED, one sentence: `model_translate.check_command` states
# each of task o2's 259 single-opcode rows as a theorem against the
# model the sweep builds, or refuses it by cause, and the tally of
# those outcomes is what must not move when task m1b adds three
# operand shapes to the sweep -- because adding shapes changes which
# model definitions exist and what they are numbered.
#
# This lane runs BEFORE the change, on the tower's unmodified copy of
# `model_translate.py`, so the comparison is against a reading this
# task took, not against a stored file another task's `run` pass has
# since rewritten (the stored `check_L2.json` carries `run`'s
# outcomes, not `check`'s).
#
# WHERE IT WRITES: `model_translate.HERE` is pointed at a scratch
# directory under /work, so this lane writes NOTHING into
# `Research/op_pipeline/lean` -- neither `check_L2.json` nor the
# ModelCheck_*.lean files, which are that folder's own artifacts and
# not this task's to overwrite.
#
# MEMORY BOUND: 16 GB resident inside the m1b instance's 20g, named
# abort ABORT_MEMORY_M1B; the command's own ceiling
# (model_translate.MEMORY_CEILING_KB, 6 GB) is left as it is. Peak RSS
# printed at the end.
set -euo pipefail
export HOME=/work/m1bhome
mkdir -p "$HOME" /work/m1b_check_baseline/archproof/Archproof
echo "[1/2] task m1b: the shapes the sweep spells today"
cd /projects/PseudoCoupHQ/Research/op_pipeline/lean
python3 -c "
import sys
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline')
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline/lean')
import model_translate as MT
names = [s[0] for s in MT.shapes_for(32)]
print('   shapes_for(32): %d -- %s' % (len(names), ' '.join(names)))
print('   attempts_for(\'add\'): %d' % len(MT.attempts_for('add')))
"
echo "[2/2] task m1b: model_translate.check_command, redirected"
python3 - <<'PY'
import resource
import sys
import time

sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline/lean")
import model_translate as MT

ABORT_MEMORY_M1B_KB = 16 * 1024 * 1024
MT.HERE = "/work/m1b_check_baseline"
started = time.time()
MT.check_command()
print("   check wall %.1f s" % (time.time() - started))
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("   peak RSS: %d kB" % peak)
if peak > ABORT_MEMORY_M1B_KB:
    raise SystemExit("ABORT_MEMORY_M1B: %d kB" % peak)
PY
echo "[2/2] done"
