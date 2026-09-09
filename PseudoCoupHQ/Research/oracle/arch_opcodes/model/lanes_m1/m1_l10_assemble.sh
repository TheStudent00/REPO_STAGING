#!/usr/bin/env bash
# m1_l10_assemble.sh -- task m1: join the attestation onto the rows,
# count, and write model_table.json (the deliverable). MEMORY BOUND:
# 16g, named abort ABORT_MEMORY_M1; this lane holds the three documents
# (41.4 MB + 17.2 MB + small) at once, which is what the bound is for.
set -euo pipefail
echo "[1/2] task m1: model_table.py assemble"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py assemble
echo "[2/2] task m1: model_table.py report"
python3 model_table.py report
echo "[2/2] done"
