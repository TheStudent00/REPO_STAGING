#!/bin/bash
set -x
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/8] bounds"
python3 t94_read_bounds.py 2>&1 | tail -10
echo "[2/8] re-carve + render + gate"
python3 t94_recarve.py 2>&1 | tail -20
echo "[3/8] causes, recurring paths, super-op route"
python3 t94_analysis.py 2>&1 | tail -18
echo "[4/8] long_add instruction count, counted straight off objdump, in bounds and to the next symbol"
objdump -d -w --start-address=0x137370 --stop-address=0x1374e9 /persist/cpython_ship/python | grep -cE "^\s+[0-9a-f]+:"
objdump -d -w --start-address=0x137370 --stop-address=0x1374f0 /persist/cpython_ship/python | grep -cE "^\s+[0-9a-f]+:"
echo "[5/8] the java nmethod line count, real instructions only"
python3 -c "
import json
d=json.load(open('interp_jvm.json'))
for u in d['units']:
    rows=[l for r in u['arch_unit'] for l in r['objdump'] if len(l.split(chr(9)))>=3]
    cont=[l for r in u['arch_unit'] for l in r['objdump'] if len(l.split(chr(9)))<3]
    print(u['id'], 'printed lines', sum(len(r['objdump']) for r in u['arch_unit']), 'instructions', len(rows), 'byte-continuation lines', len(cont))
"
echo "[6/8] SPELLING GUARD, one process, over every artifact this task wrote"
python3 check_no_spelling_keys.py t94_bounds.json t94_recarve.json t94_analysis.json
echo "spelling guard exit=$?"
echo "[7/8] grep -c exempt over this task's own artifacts"
grep -c exempt t94_bounds.json t94_recarve.json t94_analysis.json t94_read_bounds.py t94_recarve.py t94_analysis.py
echo "[8/8] the checker is unmodified"
cd /projects/PseudoCoupHQ && git diff --stat -- Research/op_pipeline/check_no_spelling_keys.py && git log -1 --format=%H -- Research/op_pipeline/check_no_spelling_keys.py
echo done
