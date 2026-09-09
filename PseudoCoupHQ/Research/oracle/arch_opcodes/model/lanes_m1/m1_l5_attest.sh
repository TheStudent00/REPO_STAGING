#!/usr/bin/env bash
# m1_l5_attest.sh -- task m1: the corpus's attestation. One stream over
# the 332 canon40 shards; every arch-opcode ledger row is classified
# into the sweep's own (operand shape, width) by the operand texts of
# the body line term.relink says made it. Writes
# model_table_attest.json. MEMORY BOUND: 16g resident, named abort
# ABORT_MEMORY_M1 (resource.getrusage, checked after every shard); one
# shard is held at a time and dropped, as task o10's census did under
# 12g. Peak RSS is printed by the script itself.
set -euo pipefail
echo "[1/1] task m1: model_table.py attest"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py attest
echo "[1/1] done"
