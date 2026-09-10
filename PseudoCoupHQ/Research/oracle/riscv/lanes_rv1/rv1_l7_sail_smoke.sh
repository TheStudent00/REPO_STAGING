#!/usr/bin/env bash
# rv1 lane 7 -- section 3 in the small: the reference's terms against the
# ratified Sail model's simulator at 200 points per mnemonic, over a
# spread of ten instructions, so the harness is shown to work before the
# full sweep is asked for.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
export HOME=/work
mkdir -p /work/rv1sail
total=2

echo "[1/$total] the ten-instruction smoke"
python3 $RV/sail_points.py $RV/sail_smoke /work/rv1sail --points 200 \
  --only add,sub,srl,sra,slt,sltu,addw,addi,slli,lui,mul,mulh,div,rem,divu,remu,divw,remw,mulw

echo "[2/$total] the rows"
python3 -c "
import json
d = json.load(open('$RV/sail_smoke.json'))
print('| mnem | variants | points | agree | disagree | outcome |')
print('|---|---|---|---|---|---|')
for r in d['rows']:
    print('| %s | %s | %s | %s | %s | %s |' % (r['mnem'], r.get('variants'), r['points'], r.get('agree'), r.get('disagree'), r['outcome']))
    for e in r.get('examples', [])[:2]:
        print('    %s' % e)
"
python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
