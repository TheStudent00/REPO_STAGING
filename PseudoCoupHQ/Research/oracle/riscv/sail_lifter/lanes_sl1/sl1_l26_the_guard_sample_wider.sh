#!/bin/bash
# sl1 lane 26 -- the guard sample again, wider (the first 260 rows at 200
# points) after the reader learned Lean's early `return`; every refusal
# cause printed whole enough to read.
set -u
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
mkdir -p /work/sl1g
echo "[1/1] the guard sample"
timeout 3000 python3 $SL/sail_guard.py $SL/guard_sample /work/sl1g --points 200 --first 260 2>&1 | cut -c1-330
echo "done $(date -u +%FT%TZ)"
