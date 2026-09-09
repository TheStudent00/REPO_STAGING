#!/bin/bash
# task o13, lane 9: the closing sweep -- the unmodified spelling guard
# over every json this task's artifact folder holds, in one place.
set -u
M=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode
G=/projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
export PATH=/opt/cargo/bin:$PATH
FILES=(mode_diagnose_c.json mode_facts.json mode_population.json \
       mode_results.json mode_run_c.json mode_run_c_30000_ms.json \
       mode_run_rust.json mode_run_rust_30000_ms.json)
i=0
total=${#FILES[@]}
for f in "${FILES[@]}"; do
  i=$((i+1))
  echo "[$i/$total] $f"
  python3 "$G" "$M/$f"
done
echo "lane o13_l9 done"
