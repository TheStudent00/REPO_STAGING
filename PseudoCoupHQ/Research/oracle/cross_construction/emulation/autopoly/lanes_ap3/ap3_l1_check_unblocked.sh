#!/usr/bin/env bash
# ap3_l1_check_unblocked.sh -- task ap3, FIX 3: `model_translate.py
# check` runs again.
#
# THE DEFECT, open since log_237 section 14 item 1 and blocking a guard
# since task ap2 (log_244 section 7): `load_rows` reads task o2's
# artifact by the field name `mnemonic`, which task mn1 renamed to
# `mnem`, so `check` stopped on `KeyError: 'mnemonic'` and `check_L2`
# could not be re-derived by anyone.
#
# THE CHANGE, the one line the brief authorises in a shared file:
# `load_rows` reads `row["mnem"]`, with `mnemonic` accepted as a
# fallback for the older artifact.
#
# WHAT THIS LANE PROTECTS.  `check_command` OVERWRITES
# `lean/check_L2.json` and rewrites the Lean model files under
# `lean/archproof/Archproof/`.  The stored `check_L2.json` carries the
# 19 DISCREPANCY verdicts the LEAN RUN wrote, which a fresh `check`
# does not have; and nothing but the one line is authorised to change
# under `Research/op_pipeline`.  So this lane records a sha256 of every
# file `check` can write, copies them aside, runs `check`, copies the
# regenerated `check_L2.json` into THIS TASK's artifact folder, and
# restores every file that moved -- then prints the sha256 comparison
# so the restore is measured and not asserted.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP3.  This lane
# reads `single_opcode_units.json` (1.6 MB) and the canon40 term store
# through `stream_store`; peak resident is printed at the end.
set -euo pipefail
LEAN=/projects/PseudoCoupHQ/Research/op_pipeline/lean
ART=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
BACK=/work/ap3_l1_before
mkdir -p "$BACK/archproof/Archproof"

echo "[1/6] the one line, LITERAL, as it now stands"
sed -n '1244,1258p' "$LEAN/model_translate.py"

echo ""
echo "[2/6] sha256 BEFORE, of every file check_command can write"
cp "$LEAN/check_L2.json" "$BACK/check_L2.json"
cp "$LEAN/archproof/Archproof/"*.lean "$BACK/archproof/Archproof/" 2>/dev/null || true
( cd "$LEAN" && sha256sum check_L2.json archproof/Archproof/*.lean ) | tee /work/ap3_l1_before.sha

echo ""
echo "[3/6] the stored tally, off the artifact as it stands"
python3 - <<'PY'
import json
d = json.load(open("/projects/PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json"))
tally = {}
for row in d["rows"]:
    tally[row["outcome"]] = tally.get(row["outcome"], 0) + 1
print("   check_L2.json rows: %d" % len(d["rows"]))
for name in sorted(tally):
    print("      %-12s %d" % (name, tally[name]))
PY

echo ""
echo "[4/6] python3 model_translate.py check"
cd "$LEAN"
python3 model_translate.py check

echo ""
echo "[5/6] sha256 AFTER, and the regenerated artifact kept under this task's folder"
( cd "$LEAN" && sha256sum check_L2.json archproof/Archproof/*.lean ) > /work/ap3_l1_after.sha
cp "$LEAN/check_L2.json" "$ART/autopoly3_check_L2_rerun.json"
echo "   files whose sha256 moved:"
diff /work/ap3_l1_before.sha /work/ap3_l1_after.sha | sed -n 's/^< /      was  /p;s/^> /      now  /p' || true

echo ""
echo "[6/6] restore, then sha256 against BEFORE"
cp "$BACK/check_L2.json" "$LEAN/check_L2.json"
cp "$BACK/archproof/Archproof/"*.lean "$LEAN/archproof/Archproof/" 2>/dev/null || true
( cd "$LEAN" && sha256sum check_L2.json archproof/Archproof/*.lean ) > /work/ap3_l1_restored.sha
if diff -q /work/ap3_l1_before.sha /work/ap3_l1_restored.sha >/dev/null; then
  echo "   RESTORED IDENTICAL: every file check_command wrote is back to its stored bytes"
else
  echo "   RESTORE DIFFERS -- this is a FINDING:"
  diff /work/ap3_l1_before.sha /work/ap3_l1_restored.sha
fi
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)"
echo "done"
