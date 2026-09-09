#!/usr/bin/env bash
# t85_l8_guards_all.sh -- TASK 85, lane 8: the data guard over ALL SEVEN
# artifacts this task produced, in ONE process, unmodified.
set -uo pipefail
cd PseudoCoupHQ/Research/op_pipeline || exit 2
echo "[1/3] the guard is unmodified"
git -C PseudoCoupHQ status --porcelain -- \
    Research/op_pipeline/check_no_spelling_keys.py
echo "  sha256: $(sha256sum check_no_spelling_keys.py | cut -d' ' -f1)"
echo
echo "[2/3] grep -c exempt over every artifact"
for f in t85_gitfacts.json t85_sample.json t85_all_moments.json \
         t85_all_moments2.json t85_all_moments3.json \
         t85_one_moment_proof.json t85_one_moment_proof2.json; do
    echo "  $f: $(grep -c exempt "$f")"
done
echo
echo "[3/3] check_no_spelling_keys.py, UNMODIFIED, ONE process, 7 artifacts"
python3 check_no_spelling_keys.py \
    t85_gitfacts.json t85_sample.json t85_all_moments.json \
    t85_all_moments2.json t85_all_moments3.json \
    t85_one_moment_proof.json t85_one_moment_proof2.json
echo "  exit $?"
