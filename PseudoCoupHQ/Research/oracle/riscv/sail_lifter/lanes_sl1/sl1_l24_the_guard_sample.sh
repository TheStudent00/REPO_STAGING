#!/bin/bash
# sl1 lane 24 -- the guard, SAMPLE: the first 40 rows of the generated
# population at 300 points each, against the Sail model's C simulator.
set -u
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
mkdir -p /work/sl1g
echo "[1/1] the guard sample"
timeout 3000 python3 $SL/sail_guard.py $SL/guard_sample /work/sl1g --points 300 --first 40 2>&1 | cut -c1-260
echo "done $(date -u +%FT%TZ)"
