#!/usr/bin/env bash
# rv1 lane 8 -- the brief's section 4: each unit's riscv64 term against its
# own x86-64 term, per written place, at the unit's own answer width.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
total=2

echo "[1/$total] the claim, unit by unit"
python3 $RV/claim_check.py $OP $RV/units.json $RV/carved.json $RV/claim

echo "[2/$total] the table"
python3 -c "
import json
d = json.load(open('$RV/claim.json'))
print('| unit | x86 body | riscv body | outcome |')
print('|---|---|---|---|')
for r in d['rows']:
    print('| %s | %s | %s | %s |' % (r.get('unit') or '(none)', r.get('x86_body',''), r.get('riscv_body',''), r['outcome']))
print()
for r in d['rows']:
    if not r.get('unit'): continue
    print('=== %s' % r['unit'])
    print('  store      : %s' % r.get('x86_term_from_the_store'))
    print('  re-derived : %s' % r.get('x86_term_rederived'))
    print('  matches    : %s' % r.get('rederivation_matches_the_store'))
    print('  riscv      : %s' % r.get('riscv_term'))
    print('  extra x86 arrivals: %s' % r.get('x86_arrivals_beyond_the_arguments'))
    print('  counterexample: %s' % r.get('counterexample'))
"
python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
