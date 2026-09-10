#!/usr/bin/env bash
# rv1 lane 9 -- the brief's section 3(b) at full size: every base-integer
# instruction of the RISC-V reference put against the ratified Sail model's
# own simulator at up to 20,000 concrete points each, the edges first.
# Memory bound 6g, abort ABORT_MEMORY_RV1 (the driver raises it itself).
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
export HOME=/work
mkdir -p /work/rv1sailfull
total=2

echo "[1/$total] the full sweep"
python3 $RV/sail_points.py $RV/level0_points /work/rv1sailfull --points 20000

echo "[2/$total] the table"
python3 -c "
import json
d = json.load(open('$RV/level0_points.json'))
print('| mnem | variants | points | agree | disagree | unevaluated | outcome |')
print('|---|---|---|---|---|---|---|')
for r in d['rows']:
    print('| %s | %s | %s | %s | %s | %s | %s |' % (r['mnem'], r.get('variants'), r['points'], r.get('agree'), r.get('disagree'), r.get('unevaluated'), r['outcome']))
    for e in r.get('examples', [])[:3]:
        print('%s' % e)
print()
print('refused by name:', len(d['refused_by_name']))
for r in d['refused_by_name']:
    print('  %-12s %s' % (r['mnem'], r['cause']))
print('total points:', sum(r['points'] for r in d['rows']))
print('peak RSS reported by the driver:', d['meta'].get('peak_rss_mb'), 'MB')
"
python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
