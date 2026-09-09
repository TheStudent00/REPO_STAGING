#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: regenerate unique_opcodes.json/.md (mnem field)"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes
python3 unique_opcodes.py
echo "[1/1] done"
