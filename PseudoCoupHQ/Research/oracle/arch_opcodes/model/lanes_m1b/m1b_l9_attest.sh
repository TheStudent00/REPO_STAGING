#!/usr/bin/env bash
# m1b_l9_attest.sh -- task m1b: model_table.py attest. One stream over
# the 332 canon40 shards, now reading THREE populations rather than
# one: every arch-opcode ledger row as before; every flag-pair row
# whose reading half writes a value, as that mnemonic's own cell with
# the flag-setting mnemonic recorded on it; and every flag-pair row
# whose reading half writes the branch condition, as a GUARD row of
# that branch mnemonic. Every cell is keyed by (mnem, shape,
# key_width).
# MEMORY BOUND: 16 GB resident, named abort ABORT_MEMORY_M1B, checked
# after every shard; one shard is held and dropped. m1's own run of
# this command peaked at 83 MB. Peak RSS printed by the script.
set -euo pipefail
echo "[1/1] task m1b: model_table.py attest"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py attest
echo "[1/1] done"
