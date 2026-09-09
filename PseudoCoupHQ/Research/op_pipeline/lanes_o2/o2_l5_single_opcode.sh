#!/usr/bin/env bash
# o2 lane 5 (rerun after fixing a bug: branch-target labels like "L0:" were being counted as arch opcodes; excluded now) --
# both chaff rules. Streams every shard of the population (canon40
# wrapped x5, canon40_regen_store x326, canon40_interp.json); never
# holds the whole ~110 MB store at once. Memory bound 2 GB
# (ABORT_MEMORY_O2 if exceeded -- watched via /usr/bin/time -v peak
# RSS below, pasted into log_208).
set -u
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes
echo "======== [1/1] single_opcode_units.py ========"
echo "(peak RSS reported by the script itself via resource.getrusage; container has no /usr/bin/time)"
python3 single_opcode_units.py
rc=$?
echo "exit ${rc}"
exit ${rc}
