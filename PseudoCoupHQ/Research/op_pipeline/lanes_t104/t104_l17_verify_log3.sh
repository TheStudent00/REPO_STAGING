#!/usr/bin/env bash
# t104 lane 17 -- third verifier pass, after lane 16 found 1 DIFFERS
# (the guard command in Section 5 was missing its `Research/op_pipeline/`
# prefix -- the verifier's working directory is /projects/PseudoCoupHQ,
# not the op_pipeline directory). Fixed; this pass re-checks.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py --verify --timeout 20 /projects/PseudoCoupHQ/DevComms/log_233_task_t104_normalize_commutative_order_close.md
echo "verifier exit $?"
