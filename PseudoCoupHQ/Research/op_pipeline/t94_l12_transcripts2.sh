#!/bin/bash
cd /projects/PseudoCoupHQ
run () { echo "\$ $1"; eval "$1" 2>&1; echo; echo "-----"; }
P=/projects/PseudoCoupHQ/Research/op_pipeline

run "sed -n '/^## the unit.s boundary/,/^\$/p' /projects/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_1_arch_unit/CORE_0_3_5_1_arch_unit.md | head -8"

run "python3 -c \"
import json
d=json.load(open('$P/t94_bounds.json'))
for r in d['records']:
    print('%-58s %-10s %-10s %5s %5s  dwarf_agrees=%s' % (r['unit'], r.get('new_low'), r.get('new_high'), r.get('new_byte_length'), r.get('new_instruction_count'), r.get('symbol_table_and_dwarf_agree')))
\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_bounds.json'))
for r in d['records']:
    print(r['unit'], '| symbol table:', r['symbol_table_rows'], '| dwarf:', r['dwarf_rows'])
\""

run "python3 -c \"
import json
d=json.load(open('$P/interp_jvm.json'))
for u in d['units']:
    rows=[l for r in u['arch_unit'] for l in r['objdump'] if not len(l.split(chr(9))) < 3]
    cont=[l for r in u['arch_unit'] for l in r['objdump'] if len(l.split(chr(9))) < 3]
    print(u['id'], u['nmethod_header'], '| base', u['arch_unit'][0]['base'], '| length', u['arch_unit'][0]['length'], '| instructions', len(rows), '| byte-continuation lines', len(cont))
\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_recarve.json'))
for r in d['records']:
    o=r['old']; n=r['recarved']
    print('%-58s old %-14s n=%-3s  new %-14s %-14s %4s %4s' % (r['unit'], o['old_low'], o['old_body_instruction_count'], n.get('new_low'), n.get('new_high'), n.get('new_byte_length'), n.get('new_instruction_count')))
\""

run "python3 -c \"import json;d=json.load(open('$P/interp_canon35.json'));print(d['records'][0]['prior_text'])\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_bounds.json'))
r=[x for x in d['records'] if x['unit'].startswith('cpython')][0]
for i in list(range(0,11)):
    b=r['body'][i]; print('%2d  %-9s %s' % (i,b['address'],b['mnem']))
\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_bounds.json'))
r=[x for x in d['records'] if x['unit'].startswith('cpython')][0]
for i in list(range(26,38)):
    b=r['body'][i]; print('%2d  %-9s %s' % (i,b['address'],b['mnem']))
\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_bounds.json'))
r=[x for x in d['records'] if x['unit'].startswith('cpython')][0]
for i in list(range(83,89))+[63,64]:
    b=r['body'][i]; print('%2d  %-9s %s' % (i,b['address'],b['mnem']))
\""

run "python3 -c \"import json;d=json.load(open('$P/canon_interp_units_cpython.json'));print(d['unit']['arrival_boundary_note'])\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_recarve.json'))
for m in d['verdict_movements']:
    print('%-58s %-18s  to  %-12s %s' % (m['unit'], m['from'], m['to'], m['cause'][:100]))
\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_analysis.json'))
for r in d['records']:
    c=r.get('causes')
    if c is None: print('%-58s no body' % r['unit']); continue
    print('%-58s inside %2d  runtime %2d  ptr-reads %2d  writes %2d' % (r['unit'], len(c['transfers_inside_its_own_bounds']), len(c['transfers_into_the_runtime']), len(c['reads_through_an_arriving_pointer']), len(c['memory_writes'])))
\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_recarve.json'))
for r in d['records']:
    print('%-58s %-10s changed_with_more_room=%s' % (r['unit'], r.get('gate_at_120000ms',{}).get('verdict'), r.get('answer_changed_with_more_room')))
\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_analysis.json'))
c={}
for r in d['records']:
    for p in r.get('recurring_paths',[]):
        c.setdefault(p['recurring_path'],[]).append(r['unit'])
for k in sorted(c, key=lambda x: 0-len(c[x])):
    print('%2d  %s' % (len(c[k]), k))
\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_analysis.json'))
r=[x for x in d['records'] if x['unit'].startswith('cpython')][0]
for p in r['recurring_paths']:
    if p['recurring_path'].startswith('allocation'):
        for line in p['instructions']: print(line)
\""

run "python3 -c \"
import json
d=json.load(open('$P/t94_analysis.json'))['super_op_route']
print('candidates in the miner artifact:', d['candidate_count'])
print('languages the miner mined       :', d['languages_the_miner_mined'])
print('interpreter languages among them:', d['interpreter_languages_in_that_population'])
print('candidates occurring in these bodies:', len(d['candidates_occurring_in_these_bodies']))
for h in d['candidates_occurring_in_these_bodies']:
    print('   ', h['unit'], h['candidate_instructions'], 'support', h['support'], h['languages'])
\""

run "sed -n '4,14p' $P/lineage_carve.py"

run "python3 $P/check_no_spelling_keys.py $P/t94_bounds.json $P/t94_recarve.json $P/t94_analysis.json"

run "grep -c exempt $P/t94_bounds.json $P/t94_recarve.json $P/t94_analysis.json"

run "readelf -sW /persist/cpython_ship/python | grep -w long_add"
run "readelf -sW /persist/ruby_ship/ruby | grep -wE 'rb_fix_plus|rb_int_plus|rb_big_plus|vm_opt_plus'"
run "readelf -sW /persist/php_c_ship/sapi/cli/php | grep -wE 'add_function|ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER' | grep FUNC"
run "objdump -d -w --start-address=0x137370 --stop-address=0x1374e9 /persist/cpython_ship/python | grep -cE '^ +[0-9a-f]+:'"
