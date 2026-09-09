#!/usr/bin/env bash
# o12 lane 14 -- the conventions checker, fourth pass, over log_230
# after lane 13's two DIFFERS were fixed (the sed range for
# leaf/inner/root_admissible was one line short; the guard block
# included the lane's own trailing echo, not the guard's own output).
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/1] claims verify"
python3 check_conventions_log_claims.py --verify --timeout 20 \
  /projects/PseudoCoupHQ/DevComms/log_230_task_o12_synthesis_route.md
echo "-- exit $?"
