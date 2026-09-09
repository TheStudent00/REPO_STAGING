#!/usr/bin/env bash
# o12 lane 13 -- the conventions checker, third pass, over log_230
# after lane 11's 5 DIFFERS / 7 REFUSED were fixed (absolute paths,
# sed's \%...% address form, git pinned to a single SHA -- lane 12's
# own output is what section 3-9 now paste).
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/1] claims verify"
python3 check_conventions_log_claims.py --verify --timeout 20 \
  /projects/PseudoCoupHQ/DevComms/log_230_task_o12_synthesis_route.md
echo "-- exit $?"
