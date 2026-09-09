#!/usr/bin/env bash
# t86_l9_data_guard.sh -- TASK 86, lane 9: the DATA guard over all FIVE
# artifacts in ONE process.  Lane 8 ran the same check before
# t86_all_panes2.json had been copied out of the sandbox's /out into the
# tree, and refused by name on the missing file -- kept as the record.
set -uo pipefail
cd PseudoCoupHQ/Research/op_pipeline || exit 2
echo "the guard, unmodified: sha256 $(sha256sum check_no_spelling_keys.py | cut -d' ' -f1)"
for f in t86_vcs_scale.json t86_sample.json t86_sample2.json \
         t86_all_panes.json t86_all_panes2.json; do
    echo "  grep -c exempt $f: $(grep -c exempt "$f")"
done
python3 check_no_spelling_keys.py \
    t86_vcs_scale.json t86_sample.json t86_sample2.json \
    t86_all_panes.json t86_all_panes2.json
echo "  exit $?"
