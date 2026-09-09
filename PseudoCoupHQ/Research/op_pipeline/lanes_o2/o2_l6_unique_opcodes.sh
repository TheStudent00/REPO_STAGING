#!/usr/bin/env bash
# o2 lane 6 (rerun for the same label-line fix) --
# the cross-language table and the ledger cross-check. Streams every
# shard of the population, same as lane 1.
set -u
cd PseudoCoupHQ/Research/oracle/arch_opcodes
echo "======== [1/1] unique_opcodes.py ========"
echo "(peak RSS reported by the script itself via resource.getrusage; container has no /usr/bin/time)"
python3 unique_opcodes.py
rc=$?
echo "exit ${rc}"
exit ${rc}
