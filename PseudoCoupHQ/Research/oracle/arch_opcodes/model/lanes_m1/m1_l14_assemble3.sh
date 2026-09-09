#!/usr/bin/env bash
# m1_l14_assemble3.sh -- task m1: assemble and report, re-run after one
# more correction to how the SPLITS are counted (nothing measured
# changes; only the criterion is stated more precisely). The split is
# now the multiset of place KINDS (`reg`, `flags`, `mem`, `stack`,
# `x87`) a mnemonic's rows write, so that a mnemonic whose destination
# register merely differs between operand shapes is not read as split,
# while one-operand `imul` (two registers) against two-operand `imul`
# (one register and the flags) is -- which is the ruling's own example.
# The place-NAME count and the destination-text count are kept beside
# it as the finer readings.
set -euo pipefail
echo "[1/2] task m1: model_table.py assemble"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py assemble
echo "[2/2] task m1: model_table.py report"
python3 model_table.py report
echo "[2/2] done"
