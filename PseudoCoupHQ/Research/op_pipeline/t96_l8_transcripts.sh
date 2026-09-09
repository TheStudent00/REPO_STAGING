#!/bin/bash
# TASK 96 round 19, lane 8.  The transcripts the log pastes, each one a
# command the log verifier can re-run.
set -x
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "[1/8] the compiled population and its %r15 count"
python3 -c "
import json
total = 0
hits = 0
seen = 0
for lang in ('c', 'cpp', 'go', 'rust', 'swift'):
    units = json.load(open('canon40_wrapped_%s.json' % lang))['units']
    total = total + len(units)
    for label in units:
        text = units[label].get('wrapped_text')
        if text is None:
            continue
        seen = seen + 1
        if '%r15' in text:
            hits = hits + 1
print('compiled units in the canon40 render : %d' % total)
print('of those, carrying a wrapped text    : %d' % seen)
print('wrapped texts containing %r15        : %d' % hits)
"

echo "[2/8] the verdict movement, all eleven, three forms"
python3 -c "
import json
d = json.load(open('t96_canonical.json'))
for m in d['verdict_movements']:
    print('%-58s %-18s | %-22s | %s' % (m['unit'], m['from'], m['to_form_two'], m['to_form_three']))
print()
print(json.dumps(d['summary'], indent=1, sort_keys=True))
"

echo "[3/8] the instrument question: gate.py's own C1 against FORM 1's text"
python3 -c "
import json
d = json.load(open('t96_analysis.json'))
for r in d['records']:
    one = r['form_one_under_this_instrument']
    if not one.get('asked'):
        print('%-58s not asked (no FORM 1 text)' % r['unit'])
        continue
    f = one['the_first_failure']
    print('%-58s available=%-5s  %s' % (r['unit'], one['the_structural_route_is_available_to_form_one'], f['note'][:110]))
print()
print(json.dumps(d['the_instrument_question'], indent=1, sort_keys=True))
"

echo "[4/8] the six checks, and what the SOLVER route stopped on"
python3 -c "
import json
d = json.load(open('t96_analysis.json'))
for r in d['records']:
    for name in ('form_two', 'form_three'):
        row = r[name]
        if row['outcome'] == 'REFUSED':
            print('%-58s %-11s REFUSED %s' % (r['unit'], name, row['refusal_cause']))
            continue
        passed = len([c for c in row['the_six_checks'] if c['passed']])
        print('%-58s %-11s %-22s checks %d/6  solver_answered=%s  120000ms=%s' % (r['unit'], name, row['verdict'], passed, row['solver_route']['the_solver_answered'], (row['gate_at_120000ms'] or {}).get('verdict')))
"

echo "[5/8] C1's own note for one unit under FORM 2"
python3 -c "
import json
d = json.load(open('t96_analysis.json'))
r = [x for x in d['records'] if x['unit'].startswith('php/add_function')][0]
for c in r['form_two']['the_six_checks']:
    print('%-12s %-5s %s' % (c['check'], c['passed'], c['note'][:150]))
"

echo "[6/8] the three shortfalls, per unit"
python3 -c "
import json
d = json.load(open('t96_canonical.json'))
for r in d['records']:
    s = r['the_three_shortfalls']
    a = s['the_r15_collision']
    b = s['memory_obtained_at_run_time']
    c = s['an_input_block_holds_a_pointer']
    print('%-58s r15 body=%-5s form=%-5s gone=%-5s | obtained n=%-2d gone=%-5s | areas=%d gone=%-5s n/a=%s' % (r['unit'], a['the_body_names_r15'], a['the_form_claims_r15'], a['gone'], b['sightings'], b['gone'], c['arriving_areas_found'], c['gone'], c['not_applicable']))
"

echo "[7/8] the arriving areas, and the two that overflow the extent"
python3 -c "
import json
d = json.load(open('t96_canonical.json'))
for r in d['records']:
    f = r['the_canonical_form_with_the_seventh_block']
    areas = f.get('arriving_areas') or []
    if not areas:
        print('%-58s no arriving area' % r['unit'])
        continue
    for a in areas:
        print('%-58s %%%-4s 0x%x .. 0x%x  n=%-2d indexed=%-5s advanced=%s' % (r['unit'], a['base_family'], a['smallest_displacement'], a['largest_displacement'], a['sightings'], a['reached_through_an_index_register'], len(a['advanced_by'])))
"

echo "[8/8] memory and time, and the two superseded headers"
python3 -c "
import json
a = json.load(open('t96_canonical.json'))['meta']
b = json.load(open('t96_analysis.json'))['meta']
print('t96_onto_canonical_form.py peak resident kB: %d' % a['peak_resident_size_kB'])
print('t96_analysis.py            peak resident kB: %d' % b['peak_resident_size_kB'])
print('bound kB: %d   abort names: %s / %s' % (a['memory_bound_kB'], a['memory_abort_name'], b['memory_abort_name']))
"
sed -n '4,15p' region36.py
sed -n '4,12p' canon36_universal.py
echo done
