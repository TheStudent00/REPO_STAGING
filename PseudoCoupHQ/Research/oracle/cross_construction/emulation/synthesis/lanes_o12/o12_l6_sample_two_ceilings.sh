#!/usr/bin/env bash
# o12 lane 6 -- the same thirty targets twice.  The CHECK stays at the
# gate's 3,000 ms both times; only the GUESS ceiling moves, from 3,000
# ms to 30,000 ms, because at 3,000 ms twelve of the thirty ended
# UNDECIDED with the cause "the guess did not answer inside 3000 ms",
# and a time limit is a flag to re-run with more room -- never a
# reason to change what is measured.
set -u
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis
echo "======== 1. guess ceiling 3,000 ms ========"
echo "[1/3] sample at 3000 ms"
O12_GUESS_MS=3000 O12_SUB_SECONDS=300 python3 - <<'PY'
import resource, subprocess, sys
r = subprocess.run([sys.executable, "synthesize.py", "sample", "30"])
print("PEAK_RSS_KB(children)=%d"
      % resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
sys.exit(r.returncode)
PY
echo "-- exit $?"
echo
echo "======== 2. guess ceiling 30,000 ms ========"
echo "[2/3] sample at 30000 ms"
O12_GUESS_MS=30000 O12_SUB_SECONDS=900 python3 - <<'PY'
import resource, subprocess, sys
r = subprocess.run([sys.executable, "synthesize.py", "sample", "30"])
print("PEAK_RSS_KB(children)=%d"
      % resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
sys.exit(r.returncode)
PY
echo "-- exit $?"
echo
echo "======== 3. the guard ========"
echo "[3/3] guard"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  synthesis_sample_guess3000ms.json synthesis_sample_guess30000ms.json
echo "-- guard exit $?"
