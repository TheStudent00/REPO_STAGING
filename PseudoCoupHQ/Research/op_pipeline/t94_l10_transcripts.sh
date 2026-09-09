#!/bin/bash
cd /projects/PseudoCoupHQ/Research/op_pipeline
run () { echo "\$ $1"; eval "$1" 2>&1; echo; }
echo "======== [1/8] the symbol table row for each handler function ========"
run "readelf -sW /persist/cpython_ship/python | grep -w long_add"
echo "======== [2/8] ruby ========"
run "readelf -sW /persist/ruby_ship/ruby | grep -wE 'rb_fix_plus|rb_int_plus|rb_big_plus|vm_opt_plus'"
echo "======== [3/8] php ========"
run "readelf -sW /persist/php_c_ship/sapi/cli/php | grep -wE 'add_function|ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER|ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER' | grep FUNC"
echo "======== [4/8] the four instructions the old cpython unit was, and the function they came out of ========"
run "python3 -c \"import json;d=json.load(open('interp_canon35.json'));print(d['records'][0]['prior_text'])\""
run "objdump -d -w --start-address=0x137370 --stop-address=0x1374e9 /persist/cpython_ship/python | grep -cE '^ +[0-9a-f]+:'"
echo "======== [5/8] old bounds against new, all eleven ========"
run "python3 -c \"
import json
d=json.load(open('t94_recarve.json'))
for r in d['records']:
    o=r['old']; n=r['recarved']
    print('%-58s %-12s %3s  ->  %-12s %-12s %4s %4s' % (r['unit'], o['old_low'], o['old_body_instruction_count'], n.get('new_low'), n.get('new_high'), n.get('new_byte_length'), n.get('new_instruction_count')))
\""
echo "======== [6/8] verdict movement, all eleven ========"
run "python3 -c \"
import json
d=json.load(open('t94_recarve.json'))
for m in d['verdict_movements']:
    print('%-58s %-18s -> %-12s %s' % (m['unit'], m['from'], m['to'], m['cause'][:110]))
\""
echo "======== [7/8] the recurring paths, by cause ========"
run "python3 -c \"
import json
d=json.load(open('t94_analysis.json'))
c={}
for r in d['records']:
    for p in r.get('recurring_paths',[]):
        c.setdefault(p['recurring_path'],[]).append(r['unit'])
for k in sorted(c, key=lambda x:-len(c[x])):
    print('%2d  %s' % (len(c[k]), k))
\""
echo "======== [8/8] the super-op route, asked of the miner's own artifact ========"
run "python3 -c \"
import json
d=json.load(open('t94_analysis.json'))['super_op_route']
print('candidates in the miner artifact:', d['candidate_count'])
print('languages the miner mined      :', d['languages_the_miner_mined'])
print('interpreter languages among them:', d['interpreter_languages_in_that_population'])
print('candidates occurring in these bodies:', len(d['candidates_occurring_in_these_bodies']))
for h in d['candidates_occurring_in_these_bodies']:
    print('   ', h['unit'], h['candidate_instructions'], 'support', h['support'], h['languages'])
\""
run "python3 check_no_spelling_keys.py t94_bounds.json t94_recarve.json t94_analysis.json"
run "grep -c exempt t94_bounds.json t94_recarve.json t94_analysis.json"
