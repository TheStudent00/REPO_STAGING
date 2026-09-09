#!/usr/bin/env bash
# t99 lane 2 -- item A dry run.  term99_reason.py --dry-run over
# term66_store: computes and prints the cause table, writes
# term99_reason.json, touches ZERO shard files.  Pasted in log_205
# BEFORE the write lane runs.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] term99_reason.py --dry-run ========"
python3 term99_reason.py --dry-run
rc=$?
echo "exit ${rc}"
exit ${rc}
