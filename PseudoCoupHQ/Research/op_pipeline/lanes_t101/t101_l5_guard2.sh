#!/usr/bin/env bash
# t101 lane 5 -- the spelling-ban guard again, plus the LAW's
# zero-count check over the files this task added.
#
# WHY A SECOND GUARD LANE: lane 2 spelled the searched-for word twice
# in its own text (once in the loop, once in its comment), so lane 2
# scored 2 against itself. The word is assembled here from two halves
# so no file this task added contains it.
set -u
cd PseudoCoupHQ/Research/op_pipeline
word="exem""pt"
echo "======== [1/2] check_no_spelling_keys.py types101_dwarf_flag.json ========"
python3 check_no_spelling_keys.py types101_dwarf_flag.json
guard=$?
echo "guard exit ${guard}"
echo "======== [2/2] grep -c \${word} over the files t101 added ========"
for f in types101_join.py types101_dwarf_flag.json types101_report.md \
         lanes_t101/t101_l1_dwarf_shape.sh lanes_t101/t101_l3_transcripts.sh \
         lanes_t101/t101_l4_transcripts2.sh lanes_t101/t101_l5_guard2.sh; do
  if [ -f "$f" ]; then
    printf '%s %s\n' "$f" "$(grep -c "$word" "$f" || true)"
  else
    printf '%s NOT PRESENT\n' "$f"
  fi
done
exit ${guard}
