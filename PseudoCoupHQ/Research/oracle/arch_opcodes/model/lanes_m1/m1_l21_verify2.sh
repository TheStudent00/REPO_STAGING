#!/usr/bin/env bash
# m1_l21_verify2.sh -- task m1: check_conventions_log_claims.py --verify
# over log_236, re-run after the one DIFFERS the first verify lane found
# was fixed in the LOG (its guard transcript was pasted from a lane that
# had cd'd into the model folder, so its relative paths did not resolve
# where the verifier runs; the transcript is now the absolute-path run
# of the same unmodified guard, from lane m1_l20_claims2.sh). The
# verifier itself was not touched.
set -euo pipefail
echo "[1/1] task m1: check_conventions_log_claims.py --verify over log_236"
cd /projects/PseudoCoupHQ
python3 Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 \
  DevComms/log_236_task_m1_arch_opcode_model_table.md
echo "[1/1] done"
