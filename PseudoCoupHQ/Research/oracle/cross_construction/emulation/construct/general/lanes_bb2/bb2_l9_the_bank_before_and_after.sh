#!/bin/bash
# bb2_l9_the_bank_before_and_after.sh -- task bb2, lane 9: the bank and
# the readings BEFORE and AFTER this task, both derived by the same
# machinery, and the tables re-read off the corrected bank.
#
# WHY THIS LANE EXISTS, and it is a defect of this task's own found by
# its own lane.  Lane 8 rebuilt the bank with TASK t4's PASS MISSING:
# `general.register_with_the_bank` reads `general.PASS_LABEL`, which
# this task had already set to its own label, so the call registered
# THIS task's store under THIS task's name and task t4's 1,926
# certificates were never read.  Lane 8's own Table B3 shows the hole
# (`t4_general` absent) and its route table shows the consequence (the
# backstop column 0 on c, cpp and rust).  `bb2_run.register_with_the_
# bank` now spells task t4's entry out by name, and this lane rebuilds
# both banks from it.
#
#   [1/8] the bank rebuilt with every pass EXCEPT this task's two
#   [2/8] the three readings on that bank -- the `before`
#   [3/8] the bank rebuilt with this task's two in -- the `after`
#   [4/8] the three readings on that bank
#   [5/8] the three routes in one table, of 253 on every row
#   [6/8] the 100% re-derivation's alarms
#   [7/8] THE SPELLING GUARD over every json this task wrote
#   [8/8] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
A="$HQ/Research/oracle/cross_construction/emulation/autopoly"
OP="$HQ/Research/op_pipeline"
total=8

i=1
echo "[$i/$total] the bank rebuilt WITHOUT this task's two passes"
timeout 3600 python3 "$G/bb2_run.py" bank_before
echo "  exit: $?"
echo "  certificates: $(wc -l < "$A/certificates.jsonl")"

i=2
echo ""
echo "[$i/$total] the three readings on that bank -- the BEFORE"
timeout 1800 python3 "$G/bb2_run.py" readings_before
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the bank rebuilt WITH this task's two passes"
timeout 3600 python3 "$G/bb2_run.py" bank
echo "  exit: $?"
echo "  certificates: $(wc -l < "$A/certificates.jsonl")"

i=4
echo ""
echo "[$i/$total] the three readings on that bank -- the AFTER"
timeout 1800 python3 "$G/bb2_run.py" readings
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] the three routes in one table, of 253 on every row"
timeout 1800 python3 "$G/bb2_run.py" table
echo "  exit: $?"

i=6
echo ""
echo "[$i/$total] the 100% re-derivation's alarms"
timeout 1800 python3 "$G/bb2_run.py" alarms
echo "  exit: $?"

i=7
echo ""
echo "[$i/$total] THE SPELLING GUARD over every json this task wrote"
WORK=/work/bb2_guard
mkdir -p "$WORK"
for S in "$A/bb2_bit_blast_runs.jsonl" "$A/bb2_interp_runs.jsonl" \
         "$A/certificates.jsonl"; do
  if [ -f "$S" ]; then
    B=$(basename "$S" .jsonl)
    python3 -c "
import json, sys
rows = []
for line in open(sys.argv[1]):
    line = line.strip()
    if line:
        rows.append(json.loads(line))
handle = open(sys.argv[2], 'w')
json.dump(rows, handle)
handle.close()
print('  %s: %d rows -> %s' % (sys.argv[1], len(rows), sys.argv[2]))
" "$S" "$WORK/$B.json"
  fi
done
FILES=""
for F in "$G/bb2_sizes.json" "$G/bb2.json" "$G/bb2_interp.json" \
         "$G/bb2_interp_sizes.json" "$A/certificates.json" \
         "$WORK"/*.json; do
  if [ -f "$F" ]; then FILES="$FILES $F"; fi
done
echo "  files: $(echo $FILES | wc -w)"
timeout 3600 python3 "$OP/check_no_spelling_keys.py" $FILES
echo "  guard rc=$?"
echo "  grep -c exempt over the files this task added:"
for F in "$G/bb2_run.py" "$G/bitblast.py"; do
  echo "    $F: $(grep -c exempt "$F")"
done

i=8
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
