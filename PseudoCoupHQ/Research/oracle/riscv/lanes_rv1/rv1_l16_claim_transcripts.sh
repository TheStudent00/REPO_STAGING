#!/usr/bin/env bash
# rv1 lane 16 -- the re-runnable claims for the log, printed as `$ command`
# followed by its own output, so the log's section 12 can be pasted from
# this lane's transcript verbatim and re-run by
# check_conventions_log_claims.py.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
total=6

run() {
  echo "\$ $1"
  eval "$1"
  echo
}

echo "[1/$total]"
run "python3 -c \"import json; d=json.load(open('$RV/level0_points.json')); e=json.load(open('$RV/level0_points_zicond.json')); r=d['rows']+e['rows']; print('mnemonics', len(r), 'variants', sum(x['variants'] for x in r), 'points', sum(x['points'] for x in r), 'agree', sum(x['agree'] for x in r), 'disagree', sum(x['disagree'] for x in r))\""

echo "[2/$total]"
run "python3 -c \"import json; d=json.load(open('$RV/level0_points.json')); print('outcomes', sorted(set(x['outcome'] for x in d['rows'])), 'refused by name', len(d['refused_by_name']))\""

echo "[3/$total]"
run "python3 -c \"import json; d=json.load(open('$RV/claim.json')); t={};\\nfor x in d['rows']: t[x['outcome']]=t.get(x['outcome'],0)+1\\nprint(sorted(t.items()))\""

echo "[4/$total]"
run "python3 -c \"import json; d=json.load(open('$RV/carved.json')); rows=d['rows']; v=set(l.split()[0] for r in rows for l in r.get('body',[])); print('carved', sum(1 for r in rows if r['outcome']=='CARVED'), 'of', len(rows), 'distinct riscv mnemonics', len(v))\""

echo "[5/$total]"
run "python3 -c \"import json; d=json.load(open('$RV/surface.json')); print([(r['layer'].split(' (')[0], r['total_lines'], r['code_lines']) for r in d['by_layer']]); print('total', sum(r['total_lines'] for r in d['by_layer']), sum(r['code_lines'] for r in d['by_layer']))\""

echo "[6/$total]"
run "python3 $OP/check_no_spelling_keys.py $RV/units.json $RV/carved.json $RV/claim.json $RV/level0_points.json $RV/level0_points_zicond.json $RV/sail_smoke.json $RV/surface.json"

python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
