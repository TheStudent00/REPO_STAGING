#!/usr/bin/env bash
# t101b lane 6 -- the spelling-ban guard (LAW.md, "the guard ... is
# never modified; run it in a lane over every json you write") over
# every types101_*.json this task wrote: the three top-level artifacts,
# the anchor-dwarf rows index + its sample, and every shard under
# types101_dwarf_rows/ and types101_dwarf_rows_sample/.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
files=$(ls types101_holders.json types101_spellings.json types101_entry_holders.json \
           types101_dwarf_rows.json types101_dwarf_rows_sample.json \
           types101_dwarf_rows/*.json types101_dwarf_rows_sample/*.json 2>/dev/null)
total=$(echo "$files" | wc -l)
echo "[0/${total}] guard over ${total} json files"
python3 check_no_spelling_keys.py $files
rc=$?
echo "check_no_spelling_keys.py exit ${rc}"
exit ${rc}
