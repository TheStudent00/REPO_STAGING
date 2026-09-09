#!/usr/bin/env bash
# o12 lane 3 -- three targets only, to see the search work end to end
# before the sample of thirty is spent on it.
set -u
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis
echo "[1/1] smoke, three targets"
python3 - <<'PY'
import resource, subprocess, sys
r = subprocess.run([sys.executable, "synthesize.py", "sample", "3"])
print("PEAK_RSS_KB(children)=%d"
      % resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
sys.exit(r.returncode)
PY
echo "-- exit $?"
