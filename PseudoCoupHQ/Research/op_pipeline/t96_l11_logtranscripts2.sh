#!/bin/bash
# TASK 96 round 19, lane 11.  The remaining commands log_201 pastes.
set -x
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "[1/5] log 3.3 -- the FORM 2 step table, at the line range the log names"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py 2>&1 | sed -n '18,32p'

echo "[2/5] log 3.3 -- the FORM 3 step table, at the line range the log names"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py 2>&1 | sed -n '57,74p'

echo "[3/5] log 4.2 -- the six checks and the solver, refusals skipped"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json'))
for r in d['records']:
    for name in ('form_two', 'form_three'):
        row = r[name]
        if row['outcome'] == 'REFUSED':
            continue
        passed = len([c for c in row['the_six_checks'] if c['passed']])
        print('%-58s %-11s %-22s checks %d/6  solver_answered=%s  120000ms=%s' % (r['unit'], name, row['verdict'], passed, row['solver_route']['the_solver_answered'], (row['gate_at_120000ms'] or {}).get('verdict')))
"

echo "[4/5] log 7.1 -- grep -c exempt at absolute paths"
grep -c exempt /projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json /projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json /projects/PseudoCoupHQ/Research/op_pipeline/t96_wrapped_texts.txt /projects/PseudoCoupHQ/Research/op_pipeline/t96_onto_canonical_form.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_arriving_area.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.py

echo "[5/5] log 3.6 -- rb_big_plus's Part B prelude"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
r = [x for x in d['records'] if x['unit'] == 'ruby/rb_big_plus'][0]
print(r['the_canonical_form_with_the_seventh_block']['prelude'])
"
echo done
