#!/usr/bin/env bash
# o12 lane 11 -- the conventions checker, second pass, over log_230
# after section 3-9's LITERAL blocks were rewritten as real re-run
# commands (lane 8's first pass found 0 MATCHES because every block
# was a bare citation, not a command).
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/1] claims verify"
python3 check_conventions_log_claims.py --verify --timeout 20 \
  PseudoCoupHQ/DevComms/log_230_task_o12_synthesis_route.md
echo "-- exit $?"
