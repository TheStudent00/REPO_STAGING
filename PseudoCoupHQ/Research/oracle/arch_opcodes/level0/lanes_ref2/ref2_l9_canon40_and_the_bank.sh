#!/bin/bash
# ref2 lane 9 -- the two things that rest on the reference and are quick to
# answer: 200 canon40 proofs re-run under the corrected reading, and the bank
# stamped and marked.
#
#   * a canon40 proof puts the wrapped text's answer and the unit's own ship
#     body's answer to z3, and BOTH are built by the reference -- so a
#     correction moves both together.  The sample measures that rather than
#     asserting it.
#   * every certificate gains `reference_version`, the sha256 of `reference.py`
#     and `condition_table.py`; a certificate whose cell's term text moved
#     gains `reference_superseded` and is KEPT.  `certificates.jsonl` is read
#     and never written; the marked bank is `certificates_ref2.jsonl` beside
#     it.
#
# Memory bound: 12 GB, named abort ABORT_MEMORY_REF2.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
OP=$HQ/Research/op_pipeline
A=$HQ/Research/oracle/cross_construction/emulation/autopoly
export HOME=/work/ref2home
mkdir -p "$HOME"
cd "$L0" || exit 1

echo "[1/7] 200 canon40 proofs re-run under the corrected reference"
python3 "$L0/ref2_canon40_sample.py" "$L0/ref2_canon40_sample.json" 200
echo "--- exit $?"

echo "[2/7] the bank stamped and marked"
python3 "$L0/ref2_bank.py" mark
echo "--- exit $?"

echo "[3/7] the standing view: the marked bank minus the superseded"
python3 "$L0/ref2_bank.py" standing
echo "--- exit $?"

echo "[4/7] THE THREE READINGS, before -- the bank as it stands"
python3 "$L0/ref2_bank.py" readings "$A/certificates.jsonl" | grep -v 'peak resident' | tail -32
echo "--- exit $?"

echo "[5/7] THE THREE READINGS, after -- what the bank still certifies about the corrected cells"
python3 "$L0/ref2_bank.py" readings "$A/certificates_ref2_standing.jsonl" | grep -v 'peak resident' | tail -32
echo "--- exit $?"

echo "[6/7] the delta the widened code-version rule would run, and nothing run"
python3 "$L0/ref2_bank.py" plan
echo "--- exit $?"

echo "[7/7] the guard over every json this task has written, and the exempt count"
python3 "$OP/check_no_spelling_keys.py" \
    "$L0/level0_check_ref2_before.json" \
    "$L0/level0_check_ref2_c1.json" \
    "$L0/level0_check_ref2_c2.json" \
    "$L0/level0_check_ref2_c3.json" \
    "$L0/level0_check_ref2_c4.json" \
    "$L0/ref2_delta_c1.json" "$L0/ref2_delta_c2.json" \
    "$L0/ref2_delta_c3.json" "$L0/ref2_delta_c4.json" \
    "$L0/ref2_delta_whole.json" \
    "$L0/ref2_condition_proof.json" \
    "$L0/ref2_suffix_audit.json" \
    "$L0/ref2_model_table_delta.json" \
    "$L0/ref2_canon40_sample.json" \
    "$L0/ref2_bank_summary.json"
echo "--- guard exit $?"
grep -c exempt "$L0/ref2_compare.py" "$L0/ref2_condition_proof.py" \
    "$L0/ref2_suffix_audit.py" "$L0/ref2_model_table.py" \
    "$L0/ref2_term_walk.py" "$L0/ref2_bank.py" \
    "$L0/ref2_canon40_sample.py" || true
echo "--- exit $?"
