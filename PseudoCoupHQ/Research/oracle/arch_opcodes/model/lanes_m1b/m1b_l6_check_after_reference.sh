#!/usr/bin/env bash
# m1b_l6_check_after_reference.sh -- task m1b: the same check again,
# now with BOTH of this task's changes to shared files in place: the
# three x87 operand shapes in `model_translate.shapes_for` AND
# `reference.build_binary`'s one-operand branch, which now applies
# only when the mnemonic is one of the two the widening multiply
# belongs to and otherwise raises `NotModeled`. The tally must still
# be what lanes 4 and 5 read: 259 rows, 172 STATED, 87 REFUSED. No
# one-operand form of `add`, `and`, `or`, `sub` or `xor` exists in the
# corpus, so nothing the check states can move.
#
# WHAT LANE 3 FOUND, and why this lane carries eight extra lines.
# `model_translate.load_rows` reads `row["mnemonic"]` out of task o2's
# `single_opcode_units.json`. Task mn1 regenerated that file with the
# field named `mnem` (the ruling of 2026-09-08), and the reader was
# not moved with it, so `model_translate.py check` raises
#   KeyError: 'mnemonic'
# before it states a single theorem. That is a defect in a SHARED file
# this brief does not name, so this task does not edit it: it is
# FLAGGED in the log, and this lane supplies the field name in its own
# process -- `row.get("mnem")`, falling back to the old spelling --
# so the check itself runs unchanged. Nothing else about `load_rows`
# differs from the shared copy; its body is otherwise line for line
# what `model_translate.py` holds.
#
# WHAT IS CHECKED, one sentence: `check_command` states each of task
# o2's 259 single-opcode rows as a theorem against the model the sweep
# builds, or refuses it by cause; the tally of those outcomes is what
# must not move when task m1b adds three operand shapes to the sweep.
#
# WHERE IT WRITES: `model_translate.HERE` is pointed at a scratch
# directory under /work, so nothing is written into
# `Research/op_pipeline/lean`.
#
# MEMORY BOUND: 16 GB resident inside the m1b instance's 20g, named
# abort ABORT_MEMORY_M1B. Peak RSS printed at the end.
set -euo pipefail
export HOME=/work/m1bhome
mkdir -p "$HOME" /work/m1b_check_reference/archproof/Archproof
echo "[1/2] task m1b: the shapes the sweep spells now"
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
import json
import os
import resource
import sys
import time

sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "/projects/PseudoCoupHQ/Research/op_pipeline/lean")
import model_translate as MT

ABORT_MEMORY_M1B_KB = 16 * 1024 * 1024


def load_rows_reading_mnem():
    """model_translate.load_rows, with the field name task mn1 gave
    o2's artifact. Everything else is the shared copy's own body."""
    source = os.path.join(os.path.dirname(MT.OP), "oracle",
                          "arch_opcodes", "single_opcode_units.json")
    document = json.load(open(source))
    rows = []
    for language in ("c", "cpp", "go", "rust", "swift"):
        group = document["single_opcode_groups"][language]["narrow"]
        for index, row in enumerate(group):
            mnem = row.get("mnem")
            if mnem is None:
                mnem = row["mnemonic"]
            rows.append({"lang": language, "row_index": index,
                         "mnem": mnem,
                         "row_body_text": row["body_text"],
                         "unit": row["example_unit_id"],
                         "member_count": row["member_count"]})
    return rows, source


MT.load_rows = load_rows_reading_mnem
MT.HERE = "/work/m1b_check_reference"
started = time.time()
MT.check_command()
print("   check wall %.1f s" % (time.time() - started))
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("   peak RSS: %d kB" % peak)
if peak > ABORT_MEMORY_M1B_KB:
    raise SystemExit("ABORT_MEMORY_M1B: %d kB" % peak)
PY
echo "[2/2] done"
