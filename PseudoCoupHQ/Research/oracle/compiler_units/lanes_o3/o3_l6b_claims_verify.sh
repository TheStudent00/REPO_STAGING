#!/usr/bin/env bash
# lane 6b -- task o3b: claims-verify over log_209 with §8 appended
# (continuing the lane numbering from o3_l3d, the last number task o3
# used). o3_l6 (--timeout 120) was killed (exit 137/OOM at the 6g
# container cap): §8's ADDENDUM-adjacent self-referential claim (this
# same verify command, embedded in the file from task o3's own
# ADDENDUM) recurses -- each nested subprocess re-verifies the same
# file and meets the same self-referential claim again. At 12 claims
# (task o3's run) that chain fit inside the memory bound before any
# level's own --timeout tripped; at 25 claims (task o3b's larger file)
# each level does more work, so the chain grew deep enough to exceed
# 6g before any level timed out. Lowering --timeout to 20s bounds each
# level's wall time tightly, shortening the reachable chain -- the
# claim itself still resolves the same way (NOT_RERUNNABLE, an
# ellipsis-elided self-paste), just via a faster-terminating recursion
# rather than a redesign of the log or the checker.
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log_209 (with §8)"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  --json PseudoCoupHQ/Research/oracle/compiler_units/log_209_claims_o3b.json \
  PseudoCoupHQ/DevComms/log_209_task_o3_compiler_operators_used.md
echo "verifier exit: $?"
