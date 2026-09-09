#!/bin/bash
set -x
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/5] bounds"
python3 t94_read_bounds.py 2>&1 | tail -10
echo "[2/5] re-carve + render + gate"
python3 t94_recarve.py 2>&1 | tail -20
echo "[3/5] causes, recurring paths, super-op route"
python3 t94_analysis.py 2>&1 | tail -18
echo "[4/5] SPELLING GUARD, one process, over every artifact this task wrote"
python3 check_no_spelling_keys.py t94_bounds.json t94_recarve.json t94_analysis.json
echo "spelling guard exit=$?"
echo "[5/5] grep -c exempt over this task's own artifacts"
grep -c exempt t94_bounds.json t94_recarve.json t94_analysis.json t94_read_bounds.py t94_recarve.py t94_analysis.py
echo done
