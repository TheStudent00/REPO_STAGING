#!/usr/bin/env bash
# t99 lane 4 -- item A idempotence.  Run term99_reason.py --write a
# SECOND time (the store already carries reasons from lane 3).  Must
# report "records given a reason this run: 0" for every record to be
# untouched on the second pass.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] term99_reason.py --write, second run ========"
python3 term99_reason.py --write
rc=$?
echo "exit ${rc}"
exit ${rc}
