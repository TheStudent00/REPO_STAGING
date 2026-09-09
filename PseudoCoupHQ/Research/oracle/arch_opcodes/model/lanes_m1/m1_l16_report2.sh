#!/usr/bin/env bash
# m1_l16_report2.sh -- task m1: model_table.md re-rendered after three
# additions to the REPORT only (model_table.json is not rewritten and
# nothing measured changes): the count of units the relink refused; the
# separation of arch-opcode rows SEEN from rows PLACED into a cell; and
# two paragraphs naming what the three condition marks do not catch
# (a branch on the number of operands, which is how a one-operand
# BINARY line becomes a widening multiply) and what the division rows'
# condition column means (a width refusal only; z3's SDiv/UDiv are
# total, so no fault region is named).
set -euo pipefail
echo "[1/1] task m1: model_table.py report"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py report
echo "[1/1] done"
