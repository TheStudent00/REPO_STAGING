#!/usr/bin/env bash
# o12 lane 7 -- all 206 targets of task o7's population P3, at the
# guess ceiling the sample settled on (30,000 ms; the check stays at
# the gate's 3,000 ms), then the report, then the guard over every json
# this task writes.
set -u
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis
echo "======== 1. the run ========"
echo "[1/3] run, 206 targets"
O12_GUESS_MS=30000 O12_SUB_SECONDS=900 python3 - <<'PY'
import resource, subprocess, sys
r = subprocess.run([sys.executable, "synthesize.py", "run"])
print("PEAK_RSS_KB(children)=%d"
      % resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
sys.exit(r.returncode)
PY
echo "-- exit $?"
echo
echo "======== 2. the report ========"
echo "[2/3] report"
O12_GUESS_MS=30000 python3 synthesize.py report synthesis_run_guess30000ms.json
echo "-- exit $?"
echo
echo "======== 3. the guard over every json ========"
echo "[3/3] guard"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  synthesis_plan.json \
  synthesis_sample_guess3000ms.json \
  synthesis_sample_guess30000ms.json \
  synthesis_run_guess30000ms.json \
  synthesis_results.json
echo "-- guard exit $?"
echo
echo "-- grep -c exempt over the files this task adds"
grep -c exempt synthesize.py || true
for f in synthesis_plan.json synthesis_sample_guess3000ms.json \
         synthesis_sample_guess30000ms.json synthesis_run_guess30000ms.json \
         synthesis_results.json synthesis_report.md; do
  printf "%-42s %s\n" "$f" "$(grep -c exempt "$f" || true)"
done
