#!/usr/bin/env bash
# mn1_l7_o10_census.sh -- task mn1: regenerate ledger_signatures.json
# (mnem field). MEMORY BOUND: ledger_signatures.py's own named abort
# ABORT_MEMORY_O10 fires at 2 GB resident (resource.getrusage), checked
# after every one of the 332 canon40 shards it streams (259 MB total on
# disk, one shard held at a time); the original o10 run stayed inside
# 12g on the instance level. Peak RSS is printed by the script itself
# ("collector peak NNNN kB").
set -euo pipefail
echo "[1/1] task mn1: ledger_signatures.py census (reads unique_opcodes.json's mnem field)"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/signatures
python3 ledger_signatures.py census
echo "[1/1] done"
