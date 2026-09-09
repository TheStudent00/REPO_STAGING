#!/usr/bin/env bash
# o2 lane 2b (renamed to match; same fix) -- deliverable 2: per-language unique arch opcodes plus
# the cross-language table and the ledger cross-check. Streams every
# shard of the population, same as lane 1.
set -u
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes
echo "======== [1/1] unique_opcodes.py ========"
echo "(peak RSS reported by the script itself via resource.getrusage; container has no /usr/bin/time)"
python3 unique_opcodes.py
rc=$?
echo "exit ${rc}"
exit ${rc}
