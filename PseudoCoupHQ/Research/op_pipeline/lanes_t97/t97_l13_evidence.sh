#!/usr/bin/env bash
# t97 lane 13 -- the extra reproducing commands log_202 attaches to the
# conclusions it draws, run so their output can be pasted verbatim.
# Every one is read-only.
set -u
P=PseudoCoupHQ/Research/op_pipeline
echo "=====C1"
sed -n '7,17p' /logs/20260905T095231Z__t97_l8_numbers.sh.log
echo "=====C2"
sed -n '92,105p' /logs/20260905T070502Z__t97_l1_sample.sh.log
echo "=====C3"
sed -n '25,29p' /logs/20260905T070634Z__t97_l2_flag_reason.sh.log
echo "=====C4"
grep elapsed_s /status/t97_l3_pass1.sh.status
echo "=====C5"
python3 -c "import json;d=json.load(open('PseudoCoupHQ/Research/op_pipeline/term97_finalize.json'));print('inputs complete',d['inputs_complete'],'of',d['inputs_total'],'| inputs short',len(d['inputs_short']),'| records in store',d['records_in_store'])"
echo "=====C6"
sed -n '38,47p' /logs/20260905T095120Z__t97_l10_downstream_partial.sh.log
echo "=====C7"
python3 -c "import json;a=json.load(open('PseudoCoupHQ/Research/op_pipeline/the_pool5.json'))['summary'];b=json.load(open('PseudoCoupHQ/Research/op_pipeline/the_families5.json'))['summary'];print('entries',a['entries'],'| members',a['members'],'| more than one language',a['entries_spanning_more_than_one_language'],'| compiled and interpreted',a['entries_spanning_compiled_and_interpreted'],'| families',b['families'])"
echo "=====C8"
python3 -c "import json,glob;n=0;r=0;
for p in sorted(glob.glob('PseudoCoupHQ/Research/op_pipeline/term66_store/*.json')):
    d=json.load(open(p))
    for k in d['units']:
        r+=1
        if 'MemoryError' in json.dumps(d['units'][k]): n+=1
print('records in term66_store',r,'| records naming MemoryError',n)"
echo "=====C9"
sed -n '56,60p' /logs/20260905T094242Z__t97_l6_pass2_residue.sh.log
echo "=====C10"
python3 -c "import json;d=json.load(open('PseudoCoupHQ/Research/op_pipeline/term97_control.json'));print('compared',d['compared'],'| identical',d['identical'],'| differ',d['differ'],'| ceiling MB',d['ceiling_mb'],'| wall clock s',d['seconds'])"
echo "=====END"
