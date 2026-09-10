#!/usr/bin/env bash
# rv1 lane 10 -- the one instruction outside RV64I+M that a carved body
# spells, `czero.eqz` of the Zicond extension (with its co-instruction
# `czero.nez`), put against the Sail model at the same 20,000 points.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
export HOME=/work
mkdir -p /work/rv1czero
total=2
echo "[1/$total] the two Zicond instructions"
python3 $RV/sail_points.py $RV/level0_points_zicond /work/rv1czero --points 20000 --only czero.eqz,czero.nez
echo "[2/$total] the rows"
python3 -c "
import json
d = json.load(open('$RV/level0_points_zicond.json'))
for r in d['rows']:
    print('| %s | %s | %s | %s | %s |' % (r['mnem'], r['points'], r.get('agree'), r.get('disagree'), r['outcome']))
    for e in r.get('examples', [])[:3]: print('   ', e)
    if r.get('cause'): print('    cause:', r['cause'])
"
python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
