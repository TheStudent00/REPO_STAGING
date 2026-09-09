#!/bin/bash
set -x
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/7] re-run bounds"
python3 t94_read_bounds.py 2>&1 | tail -12
echo "[2/7] re-carve + render + gate"
python3 t94_recarve.py 2>&1 | tail -30
echo "[3/7] causes, recurring paths, super-op route"
python3 t94_analysis.py 2>&1 | tail -20
echo "[4/7] the 92-vs-94 question: what lies between long_add's end and the next label"
objdump -d -w --start-address=0x1374e0 --stop-address=0x137500 /persist/cpython_ship/python | sed -n '1,40p'
echo "[5/7] SPELLING GUARD, one process, over every artifact this task wrote"
python3 check_no_spelling_keys.py t94_bounds.json t94_recarve.json t94_analysis.json
echo "spelling guard exit=$?"
echo "[6/7] grep -c exempt over this task's own artifacts"
grep -c exempt t94_bounds.json t94_recarve.json t94_analysis.json t94_read_bounds.py t94_recarve.py t94_analysis.py
echo "[7/7] checker unmodified?"
cd /projects/PseudoCoupHQ && git status --porcelain Research/op_pipeline/check_no_spelling_keys.py
echo "done"
