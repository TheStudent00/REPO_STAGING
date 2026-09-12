#!/bin/bash
# bb2_l8_the_bank_the_readings_and_the_tables.sh -- task bb2, lane 8:
# the bank rebuilt with this task's two passes in it, the three
# readings before and after, the three routes in one table, this
# route's own outcomes and causes, the 100% re-derivation's alarms, and
# the spelling guard over every json this task wrote.
#
#   [1/7] the bank and the readings AS THEY STAND, before this task's
#         passes are registered -- the `before` of `before -> after`
#   [2/7] the bank rebuilt with this task's two passes registered
#   [3/7] the three readings with them in
#   [4/7] the three routes in one table, destination-only and strict,
#         of 253 on every row
#   [5/7] the 100% re-derivation: every certified place this route
#         disproves
#   [6/7] THE SPELLING GUARD over every json this task wrote, and
#         `grep -c exempt` over the files it added
#   [7/7] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
A="$HQ/Research/oracle/cross_construction/emulation/autopoly"
OP="$HQ/Research/op_pipeline"
total=7

i=1
echo "[$i/$total] the bank and the readings BEFORE this task's passes"
echo "  certificates on the bank now: $(wc -l < "$A/certificates.jsonl")"
timeout 1800 python3 "$A/bank.py" readings
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the bank rebuilt with this task's two passes in it"
timeout 3600 python3 "$G/bb2_run.py" bank
echo "  exit: $?"
echo "  certificates on the bank now: $(wc -l < "$A/certificates.jsonl")"

i=3
echo ""
echo "[$i/$total] the three readings with this task's passes in"
timeout 1800 python3 "$G/bb2_run.py" readings
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] the three routes in one table, of 253 on every row"
timeout 1800 python3 "$G/bb2_run.py" table
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] the 100% re-derivation's alarms"
timeout 1800 python3 "$G/bb2_run.py" alarms
echo "  exit: $?"

i=6
echo ""
echo "[$i/$total] THE SPELLING GUARD over every json this task wrote"
# The guard reads ONE json document per file.  A `.jsonl` store is one
# json object per LINE, so each store is presented to the guard as the
# list of its own rows -- the same content, in the one shape the guard
# reads.  The conversion is written to the lane's own work directory
# and never into the repository.
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

i=7
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
