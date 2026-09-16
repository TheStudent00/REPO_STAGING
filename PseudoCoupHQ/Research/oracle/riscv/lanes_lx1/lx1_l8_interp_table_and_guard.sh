#!/bin/bash
# lx1_l8_interp_table_and_guard.sh -- task lx1, lane 8: the table
# (deliverable of section 2) over the full-population store lane 7
# wrote, then the spelling-key guard over every json/jsonl this task
# added. No network.
set -u

HQ=PseudoCoupHQ
RV="$HQ/Research/oracle/riscv"
PREFIX="$RV/lx1_interp_runs"
total=3

i=1
echo "[$i/$total] the table, of 255 on every row"
python3 "$RV/rv_interp.py" table "$PREFIX" "$RV/twins.json"
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the guard: check_no_spelling_keys.py wants one JSON document; the store is jsonl, so each is wrapped as an array first (the riscv folder's own convention, e.g. certificates_riscv64.jsonl.as_one.json)"
for f in "$RV/lx1_interp_runs.jsonl" "$RV/lx1_interp_sample.jsonl"; do
  echo "  -- $f --"
  python3 -c "
import json
rows = [json.loads(line) for line in open('$f') if line.strip()]
json.dump(rows, open('$f.as_one.json', 'w'))
print('  wrapped', len(rows), 'rows')
"
  python3 "$HQ/Research/op_pipeline/check_no_spelling_keys.py" "$f.as_one.json"
  echo "  exit: $?"
done

i=3
echo ""
echo "[$i/$total] grep -c exempt over the files this task added (must be 0)"
grep -c exempt "$RV/rv_interp.py"
echo "  (rv_interp.py: 0 expected)"

python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
