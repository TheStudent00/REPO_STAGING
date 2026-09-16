#!/bin/bash
# lx1_l10_conventions_verifier_rerun.sh -- task lx1, lane 10: the final lane
# LAW requires -- re-run every reproducing command the log pasted, and
# report which claims MATCH, DIFFER, or are UNVERIFIABLE. No network.
set -u
total=1

i=1
echo "[$i/$total] check_conventions_log_claims.py --verify"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  PseudoCoupHQ/DevComms/log_272_lx1_riscv64_language_axis.md
echo "  exit: $?"

python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
