#!/usr/bin/env bash
# rv1 lane 17 -- the one claim transcript lane 16 could not print, its
# command rewritten as a single expression, plus the two rows of section 4
# that differ, quoted with their counterexamples.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
export HOME=/work
total=2
run() { echo "\$ $1"; eval "$1"; echo; }

echo "[1/$total]"
run "python3 -c \"import json, collections; d=json.load(open('$RV/claim.json')); print(sorted(collections.Counter(x['outcome'] for x in d['rows']).items()))\""

echo "[2/$total]"
run "python3 -c \"import json; d=json.load(open('$RV/claim.json')); print([(x['unit'], x['answer_width'], sorted(x['counterexample'].items())) for x in d['rows'] if x['outcome']=='DIFFER'])\""

python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
