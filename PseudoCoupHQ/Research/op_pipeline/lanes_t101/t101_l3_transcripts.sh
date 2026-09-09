#!/usr/bin/env bash
# t101 lane 3 -- run, inside the instance, exactly the commands the report
# and the DevComms log will paste, so every claim on those pages carries
# the output of a command that actually ran here. Read-only throughout.
set -u
cd /projects/PseudoCoupHQ

run() {
  echo "\$ $1"
  eval "$1"
  echo "--------8<--------"
}

echo "======== [1/8] fold.py :: dwarf_rows, the shared reader ========"
run "sed -n '80,91p' ~/Programming/PseudoCoupHQ/Research/op_pipeline/fold.py"

echo "======== [2/8] the lane that produced the DWARF text ========"
run "sed -n '255,262p' ~/Programming/PseudoCoupHQ/Research/op_pipeline/trickle_lanes/asgrecap_asgrecap_go_c0001.sh"

echo "======== [3/8] one stored DWARF parameter table, verbatim ========"
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/trickle_store/op_units2_c_c0000.json'));p=d['probes']['1'];print(p['meta']['lhs_type']);print(json.dumps(p['anchor']['dwarf']))\""

echo "======== [4/8] the measured tally over every store on disk ========"
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json'));c=d['counts'];print('files', c['store_files_read']);print('rows', c['dwarf_rows_examined']);print('rows with a byte size or encoding', c['dwarf_rows_carrying_a_byte_size_or_encoding_field'])\""

echo "======== [5/8] every distinct DWARF row shape measured ========"
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json'));[print(s['store_kind'],s['language'],s['build'],s['dwarf_row_fields'],s['rows']) for s in d['dwarf_row_shapes_measured']]\""

echo "======== [6/8] the spelling side: core size and how much is attested ========"
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/types101_dwarf_flag.json'));S=d['the_spelling_side_only']['by_language'];[print(l,len(r),sum(1 for x in r if x['attested'])) for l,r in sorted(S.items())]\""

echo "======== [7/8] the language inventory carries a class and no width ========"
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/type_inventory2_core2.json'));print(json.dumps(d['languages']['c']['scalar_core'][2]))\""

echo "======== [8/8] the canonical-form stores carry no dwarf field ========"
run "python3 -c \"import json;d=json.load(open('/projects/PseudoCoupHQ/Research/op_pipeline/canon40_regen_store/op_units2_c_c0000.json'));u=d['units']['c/regen_1'];print([k for k in sorted(u) if 'dwarf' in k.lower() or 'type' in k.lower()])\""

exit 0
