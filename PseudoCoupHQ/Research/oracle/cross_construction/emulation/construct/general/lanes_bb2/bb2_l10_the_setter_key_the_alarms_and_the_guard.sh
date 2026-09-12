#!/bin/bash
# bb2_l10_the_setter_key_the_alarms_and_the_guard.sh -- task bb2, lane
# 10: two defects lane 9 found in this task's own machinery, each fixed
# in the file that owns it and re-measured here.
#
# DEFECT 1, the guard's own finding.  `bb2_sizes.json` wrote the setter
# cell as a bare tuple, so its mnemonic sat in a LIST element, and the
# guard refused it sixty times over --
# `$.rows[40].setter[0] -- list element is the bare operator token 'or'`
# (lane 9 step [7/8], LITERAL).  The ruling of 2026-09-08 is that the
# mnemonic is machine form when it sits in the field `mnem`; the row now
# carries `autopoly.setter_record`, which is that record.
#
# DEFECT 2, this task's own alarm count.  Lane 9 read 726 "alarms" --
# every one of them this route's verdict on one SETTER cell set against
# this route's verdict on another, because the alarm key left the setter
# out and left this task's own pass in the certified set.  A
# certificate's key is (cell, target, written place, SETTER CELL), which
# is the bank's own rule; the key now carries it.
#
#   [1/4] the sizes rewritten, with the setter as a record
#   [2/4] the alarms, keyed as the bank keys a certificate
#   [3/4] THE SPELLING GUARD over every json this task wrote
#   [4/4] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
A="$HQ/Research/oracle/cross_construction/emulation/autopoly"
OP="$HQ/Research/op_pipeline"
total=4

i=1
echo "[$i/$total] the sizes rewritten, the setter as a record"
timeout 7200 python3 "$G/bb2_run.py" sizes
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the alarms, keyed as the bank keys a certificate"
timeout 1800 python3 "$G/bb2_run.py" alarms
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] THE SPELLING GUARD over every json this task wrote"
WORK=/work/bb2_guard2
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

i=4
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
