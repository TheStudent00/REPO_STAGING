#!/bin/bash
# ref2 lane 6 -- the model table swept at all FIVE states of the reference
# (before the task, and after each of its four corrections), then the written
# places whose term text moved, attributed to the correction that moved them.
#
# Nothing on disk is swapped: `ref2_model_table.py install` loads one state's
# two files under the module names `reference` and `condition_table` before
# `model_table` imports either, and every sweep writes a file of its own
# beside `model_table_rows.json`, which is not touched.
#
# THE SAMPLE BEFORE THE BULK, as the law asks: step [1/8] sweeps the smallest
# state first and prints its peak resident before the other four run.
#
# Memory bound: 12 GB, named abort ABORT_MEMORY_REF2, checked at the end of
# every sweep by `resource.getrusage`.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
OP=$HQ/Research/op_pipeline
export HOME=/work/ref2home
mkdir -p "$HOME"
cd "$L0" || exit 1

echo "[1/8] the five states, checked against the sha256 each correction lane printed"
sha256sum "$L0/ref2_originals/reference.py" \
          "$L0/ref2_originals/reference_c1.py" \
          "$L0/ref2_originals/reference_c2.py" \
          "$L0/ref2_originals/reference_c3.py" \
          "$L0/ref2_originals/reference_c4.py" \
          "$L0/ref2_originals/condition_table.py" \
          "$L0/ref2_originals/condition_table_c3.py"
diff -q "$L0/ref2_originals/reference_c4.py" "$OP/reference.py" && \
    echo "  state c4 IS the reference on disk"
diff -q "$L0/ref2_originals/condition_table_c4.py" "$OP/condition_table.py" && \
    echo "  state c4 IS the condition table on disk"
echo "--- exit $?"

echo "[2/8] the sample: the sweep at the state BEFORE the task, with its peak resident"
python3 "$L0/ref2_model_table.py" sweep before
echo "--- exit $?"

echo "[3/8] the sweep after correction 1"
python3 "$L0/ref2_model_table.py" sweep c1
echo "--- exit $?"

echo "[4/8] the sweep after correction 2"
python3 "$L0/ref2_model_table.py" sweep c2
echo "--- exit $?"

echo "[5/8] the sweep after correction 3"
python3 "$L0/ref2_model_table.py" sweep c3
echo "--- exit $?"

echo "[6/8] the sweep after correction 4 -- the reference as it now stands"
python3 "$L0/ref2_model_table.py" sweep c4
echo "--- exit $?"

echo "[7/8] the five side by side, and every place whose text moved"
python3 "$L0/ref2_model_table.py" compare "$L0/ref2_model_table_delta.json"
echo "--- exit $?"

echo "[8/8] the whole table assembled at the corrected state -- attest, edges, join, report"
python3 "$L0/ref2_model_table.py" assemble c4
echo "--- exit $?"
