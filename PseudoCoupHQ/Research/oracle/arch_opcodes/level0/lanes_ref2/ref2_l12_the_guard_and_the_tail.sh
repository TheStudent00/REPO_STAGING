#!/bin/bash
# ref2 lane 12 -- the guard's own correction, the bank re-marked with its
# breakdown, and the 184 the term walk could not answer.
#
# THE GUARD REFUSED THREE OF THIS TASK'S OWN FILES on its first run (lane 9,
# step [7/7]): `ref2_delta_c1.json`, `ref2_delta_whole.json` and
# `ref2_model_table_delta.json` carried mnemonics as BARE LIST ELEMENTS, which
# is a row structure, and `and`, `or`, `xor` and `not` are arch mnemonics AND
# operator spellings.  The guard was right.  Each name now rides in the field
# `mnem`, which the guard reads as machine form under the ruling of
# 2026-09-08, and the two programs are re-run so the files on disk are the
# programs' own output and not a patched copy.
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

echo "[1/7] the five level-0 comparisons, re-run with the mnemonic in a field"
for pair in "before c1" "c1 c2" "c2 c3" "c3 c4"; do
    set -- $pair
    python3 "$L0/ref2_compare.py" \
        "$L0/level0_check_ref2_$1.json" \
        "$L0/level0_check_ref2_$2.json" \
        "$L0/ref2_delta_$2.json" \
        "the state $1 against the state $2" | head -8
    echo "   ---"
done
python3 "$L0/ref2_compare.py" \
    "$L0/level0_check_ref2_before.json" \
    "$L0/level0_check_ref2_c4.json" \
    "$L0/ref2_delta_whole.json" \
    "the four corrections together"
echo "--- exit $?"

echo "[2/7] the model table's five sweeps, compared again"
python3 "$L0/ref2_model_table.py" compare "$L0/ref2_model_table_delta.json" \
    | head -22
echo "--- exit $?"

echo "[3/7] the bank re-marked, with the breakdown by target and by place"
python3 "$L0/ref2_bank.py" mark
echo "--- exit $?"

echo "[4/7] the standing view and THE THREE READINGS, before and after"
python3 "$L0/ref2_bank.py" standing
echo "  before -- the bank as it stands:"
python3 "$L0/ref2_bank.py" readings "$A/certificates.jsonl" | \
    grep -v 'peak resident' | sed -n '/| width |/,/^$/p'
echo "  after -- what it still certifies about the corrected cells:"
python3 "$L0/ref2_bank.py" readings "$A/certificates_ref2_standing.jsonl" | \
    grep -v 'peak resident' | sed -n '/| width |/,/^$/p'
echo "--- exit $?"

echo "[5/7] the 184 the walk could not answer: their word, their peak, and whether they are task t104's own 184"
python3 -c "
import json
here = '$L0'
handle = open(here + '/ref2_term_walk_evidence.json')
evidence = json.load(handle)
handle.close()
short = sorted(evidence['still_short_after_pass_2'])
print('still short after the retry at 10,240 MB: %d' % len(short))
words = {}
peaks = []
for row in evidence['pass2_rows']:
    if row['unit'] not in set(short):
        continue
    words[row['word']] = words.get(row['word'], 0) + 1
    peaks.append(row['sub_peak_kb'])
for name in sorted(words):
    print('  %-16s %d' % (name, words[name]))
if peaks:
    print('  sub-process peak resident: %d to %d kB' % (min(peaks), max(peaks)))
handle = open('$OP/t104_audit.json')
t104 = json.load(handle)
handle.close()
theirs = set(t104.get('converged_on_retry') or [])
print('task t104 retried and converged: %d units' % len(theirs))
print('the same units: %d; ours and not theirs: %d; theirs and not ours: %d'
      % (len(set(short) & theirs), len(set(short) - theirs),
         len(theirs - set(short))))
for name in short[:5]:
    print('  example still short: %s' % name)
"
echo "--- exit $?"

echo "[6/7] the guard over every json this task wrote"
python3 "$OP/check_no_spelling_keys.py" \
    "$L0/level0_check_ref2_before.json" "$L0/level0_check_ref2_c1.json" \
    "$L0/level0_check_ref2_c2.json" "$L0/level0_check_ref2_c3.json" \
    "$L0/level0_check_ref2_c4.json" \
    "$L0/ref2_delta_c1.json" "$L0/ref2_delta_c2.json" \
    "$L0/ref2_delta_c3.json" "$L0/ref2_delta_c4.json" \
    "$L0/ref2_delta_whole.json" "$L0/ref2_condition_proof.json" \
    "$L0/ref2_suffix_audit.json" "$L0/ref2_model_table_delta.json" \
    "$L0/ref2_canon40_sample.json" "$L0/ref2_bank_summary.json" \
    "$L0/ref2_term_audit.json" "$L0/ref2_term_moved.json" \
    "$L0/ref2_term_walk_evidence.json" "$L0/ref2_term_walk_state.json" \
    "$L0/ref2_term_state_c1.json" "$L0/ref2_term_state_c2.json" \
    "$L0/ref2_term_state_c3.json" \
    "$L0/model_table_rows_ref2_before.json" \
    "$L0/model_table_rows_ref2_c4.json" \
    "$L0/model_table_attest_ref2_c4.json" \
    "$L0/ref2_check_L2_c1.json" "$L0/ref2_check_L2_c2.json" \
    "$L0/ref2_check_L2_c3.json" "$L0/ref2_check_L2_c4.json"
echo "--- guard exit $?"
python3 "$OP/check_no_spelling_keys.py" "$A/certificates_ref2.jsonl" \
    "$A/certificates_ref2_standing.jsonl"
echo "--- bank guard exit $?"

echo "[7/7] grep -c exempt over every file this task added"
grep -c exempt "$L0"/ref2_*.py "$L0"/ref2_*.json \
    "$OP/reference.py" "$OP/condition_table.py" || true
echo "--- exit $?"
