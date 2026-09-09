#!/usr/bin/env bash
# t104 lane 16 -- second verifier pass, after lane 15's first pass
# found 0 DIFFERS but 0 MATCHES (every claim lacked an inline `$ `
# reproducing command); this pass runs after adding one beside each
# quantitative claim, following the shape prior closing logs used
# (log_224 §12, log_231's grep-c-exempt sweep).
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py --verify --timeout 20 /projects/PseudoCoupHQ/DevComms/log_233_task_t104_normalize_commutative_order_close.md
echo "verifier exit $?"
