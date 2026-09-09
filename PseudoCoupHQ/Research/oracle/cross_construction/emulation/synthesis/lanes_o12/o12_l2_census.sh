#!/usr/bin/env bash
# o12 lane 2 -- the plan: every target of task o7's population P3 with
# its term's text, its DWARF holders, its bucket's arrival and answer
# widths, and the component library its own machine type key bucket
# offers; then the spelling guard over the plan json.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== 1. census ========"
echo "[1/2] census"
python3 - <<'PY'
import resource, subprocess, sys
r = subprocess.run([sys.executable,
    "PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis/synthesize.py",
    "census"])
print("PEAK_RSS_KB(children)=%d"
      % resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
sys.exit(r.returncode)
PY
echo "-- exit $?"
echo
echo "======== 2. the guard over the plan json ========"
echo "[2/2] guard"
python3 check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis/synthesis_plan.json
echo "-- guard exit $?"
