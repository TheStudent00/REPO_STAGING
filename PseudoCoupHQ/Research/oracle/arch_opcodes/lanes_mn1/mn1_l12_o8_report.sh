#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: per_opcode.py report -- per_opcode_report.md"
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode
python3 per_opcode.py report
echo "[1/1] done"
