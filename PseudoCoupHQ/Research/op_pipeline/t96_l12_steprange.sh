#!/bin/bash
# TASK 96 round 19, lane 12.  The exact line ranges of the two step
# tables, so log_201's sed commands name real ranges.
set -x
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/3] FORM 2's table"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py 2>&1 | sed -n '21,35p'
echo "[2/3] FORM 3's table"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py 2>&1 | sed -n '67,84p'
echo "[3/3] the memory at the end, both forms identical"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/t96_step.py 2>&1 | sed -n '52,59p'
echo done
