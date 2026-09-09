#!/bin/bash
# TASK 96 round 19, lane 10.  Every command log_201 pastes, run exactly
# as the log writes it, so the log carries real output and not a
# paraphrase.
set -x
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "[1/8] log 1.1 -- the correction in its own file"
sed -n '/^## the form, as the owner meant it/,/^WHAT WAS MISREAD/p' /projects/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_2_canonical_form/CORE_0_3_5_2_canonical_form.md

echo "[2/8] log 2.1 -- the two forms side by side"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
r = [x for x in d['records'] if x['unit'].startswith('cpython')][0]
for title, text in (('FORM 1, region36 + canon36_universal', r['the_superseded_form']['wrapped_text']), ('FORM 2, canonical_form.py', r['the_canonical_form']['wrapped_text'])):
    lines = text.split('; ')
    print('%s -- %d lines' % (title, len(lines)))
    for line in lines[:8]:
        print('   ', line)
    print('    ...')
    for line in lines[-6:]:
        print('   ', line)
    print()
"

echo "[3/8] log 2.3 -- the refusals that no longer fire"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
for r in d['records']:
    old = r['the_superseded_form']
    if old['wrapped_text'] is not None:
        continue
    print(r['unit'])
    print('   ', (old['refusal'] or '')[:150])
"

echo "[4/8] log 2.4 -- the preludes under FORM 2"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
for r in d['records']:
    f = r['the_canonical_form']
    if f['outcome'] == 'REFUSED':
        continue
    print('%-58s prelude %s' % (r['unit'], f['prelude']))
"

echo "[5/8] log 3.5 -- the reach that is a floor"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_canonical.json'))
for r in d['records']:
    f = r['the_canonical_form_with_the_seventh_block']
    for a in (f.get('arriving_areas') or []):
        if not a['reached_through_an_index_register']:
            continue
        print('%s  %%%s' % (r['unit'], a['base_family']))
        print('   ', a['the_reach_is_a_floor_not_the_extent'])
        break
"

echo "[6/8] log 4.4 -- what the solver route stopped on, both forms"
python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.json'))
for r in d['records']:
    for name in ('form_two', 'form_three'):
        row = r[name]
        if row['outcome'] == 'REFUSED':
            continue
        s = row['solver_route']['what_it_had_no_model_for']
        if s is None:
            continue
        print('%-46s %-11s %s' % (r['unit'][:46], name, s[:96]))
"

echo "[7/8] log 6 -- the two superseded headers, and that nothing imports them"
sed -n '4,13p' /projects/PseudoCoupHQ/Research/op_pipeline/region36.py
sed -n '5,12p' /projects/PseudoCoupHQ/Research/op_pipeline/canon36_universal.py
grep -c "region36\|canon36_universal" /projects/PseudoCoupHQ/Research/op_pipeline/t96_onto_canonical_form.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_arriving_area.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_analysis.py /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py
grep -n "^import\|^ *import " /projects/PseudoCoupHQ/Research/op_pipeline/t96_arriving_area.py

echo "[8/8] log 7.1 -- the checker's last commit"
cd /projects/PseudoCoupHQ && git log -1 --format=%H -- Research/op_pipeline/check_no_spelling_keys.py
echo done
