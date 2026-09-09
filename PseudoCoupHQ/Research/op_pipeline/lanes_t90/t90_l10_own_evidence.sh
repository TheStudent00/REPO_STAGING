#!/usr/bin/env bash
# t90_l10_own_evidence.sh -- TASK 90, lane 10.
# The evidence block for log_197, re-captured after the tool fix lane 8 found.
# Every command here is one this task's own verifier will re-run, so it is
# deliberately of the kind that reproduces: no ls -l, no HEAD, no elided
# path, no wall clock.  Reads only.
# Node: hq.conventions
set -uo pipefail
cd PseudoCoupHQ
run () { echo "\$ $1"; eval "$1"; }
echo "[1/7]"; run 'wc -l Research/op_pipeline/check_conventions_log_claims.py'
echo "[2/7]"; run 'grep -c "^def " Research/op_pipeline/check_conventions_log_claims.py'
echo "[3/7]"; run "python3 -c \"import json;d=json.load(open('Research/op_pipeline/t90_verify_six.json'));print(d['population'])\""
echo "[4/7]"; run "python3 -c \"import json;d=json.load(open('Research/op_pipeline/t90_verify_six.json'));t=d['tally'];print(' '.join('%s=%d'%(k,t[k]) for k in ['MATCHES','DIFFERS','UNVERIFIABLE','REFUSED','NOT_RERUNNABLE']))\""
echo "[5/7]"; run "python3 -c \"import json,collections;d=json.load(open('Research/op_pipeline/t90_verify_six.json'));c=collections.Counter(x['log'] for x in d['claims'] if x['outcome']=='UNVERIFIABLE');print('\n'.join('%s %d'%(k,v) for k,v in sorted(c.items())))\""
echo "[6/7]"; run "python3 -c \"import json,collections;d=json.load(open('Research/op_pipeline/t90_verify_six.json'));c=collections.Counter(x['shape'] for x in d['claims']);print('\n'.join('%s %d'%(k,v) for k,v in sorted(c.items())))\""
echo "[7/7]"; run "python3 -c \"import json;d=json.load(open('Research/op_pipeline/t90_verify_six.json'));print('\n'.join(sorted(set(x['reason'].split(' -- ')[0] for x in d['claims'] if x['outcome'] in ('REFUSED','NOT_RERUNNABLE')))))\""
