#!/usr/bin/env bash
# hub1_l13_handful_and_measure_again.sh -- task hub1, lane 13.
# WHY IT RE-RUNS BOTH: lane hub1_l12 measured 21 DISPROVED on c and 14
# rust units that would not build, and both are ONE cause, read off the
# record: the primitive route can match a corpus body whose own probe was
# written over TRUTH holders, so the dictionary entry's parameters are
# declared `bool`, and a composition that passes a 32-bit operand through
# them is outside what the loop proved (`(a) as bool` is not even legal
# rust). The composition now refuses such an entry BY CAUSE, and refuses
# any parameter narrower than the operand it would carry, instead of
# calling it. Nothing about the dictionary or the loop changes; the
# refusal is in the composition, where the question belongs.
# Memory bound 6 GB, named abort ABORT_MEMORY_HUB1.
set -uo pipefail
cd PseudoCoupHQ/Research/oracle/hub
echo "[1/4] the handful"
python3 hub.py handful
echo "[2/4] the measure, whole population"
python3 hub.py measure
echo "[3/4] the tables"
python3 hub.py tables
echo "[4/4] the spelling guard over every json this task writes"
for f in dictionary.json oracle_test.json measure.json; do
    python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
        PseudoCoupHQ/Research/oracle/hub/$f
done
