#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: regenerate single_opcode_units.json/.md (mnem field)"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes
python3 single_opcode_units.py
echo "[1/1] done"
