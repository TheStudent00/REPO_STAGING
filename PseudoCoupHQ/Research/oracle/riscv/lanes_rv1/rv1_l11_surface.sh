#!/usr/bin/env bash
# rv1 lane 11 -- the brief's section 5: the per-architecture surface,
# counted by layer, with the x86 counterpart beside each layer and the
# objects this task read unchanged listed with their sizes.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
total=2
echo "[1/$total] the count"
python3 $RV/surface.py $RV $OP $RV/surface
echo "[2/$total] every file this task wrote, and nothing outside its own folder"
find PseudoCoupHQ/Research/oracle/riscv -type f | sort
python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
echo "--- lane finished"
