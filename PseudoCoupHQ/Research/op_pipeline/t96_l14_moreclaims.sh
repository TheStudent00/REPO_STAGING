#!/bin/bash
# TASK 96 round 19, lane 14.  Commands for the claims log_201 carried as
# prose, so they carry something to re-run instead.
set -x
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "[1/5] log 2.1 -- the side by side, with no ellipsis in the command"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
r = [x for x in d['records'] if x['unit'].startswith('cpython')][0]
for title, text in (('FORM 1, region36 + canon36_universal', r['the_superseded_form']['wrapped_text']), ('FORM 2, canonical_form.py', r['the_canonical_form']['wrapped_text'])):
    lines = text.split('; ')
    print('%s -- %d lines' % (title, len(lines)))
    for line in lines[:8]:
        print('   ', line)
    print('    [%d lines not printed]' % (len(lines) - 14))
    for line in lines[-6:]:
        print('   ', line)
    print()
"

echo "[2/5] log 0.2 and 3.4 -- the extent, and the reach that passes it"
python3 -c "
import json
import t96_arriving_area as AREA
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
print('AREA_SPAN  = 0x%x   (own-address OWN_SPAN, unchanged)' % AREA.AREA_SPAN)
print('AREA_ORIGIN= 0x%x   (measured, the identity map)' % AREA.AREA_ORIGIN)
for r in d['records']:
    f = r['the_canonical_form_with_the_seventh_block']
    if f['outcome'] != 'REFUSED':
        continue
    print('%-58s %s' % (r['unit'], f['refusal_cause']))
    print('   ', f['refusal'])
"

echo "[3/5] log 4.1 -- log_199's own baseline sentence"
grep -n "9 PROVED to UNDECIDED" /projects/PseudoCoupHQ/DevComms/log_199_task94_interpreter_function_bodies.md | head -3

echo "[4/5] log 4.4 -- gate.py's own binder message"
grep -n "two-step load per input row" /projects/PseudoCoupHQ/Research/op_pipeline/gate.py

echo "[5/5] log 7.1 -- the checker's own bytes"
sha256sum /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
echo done
