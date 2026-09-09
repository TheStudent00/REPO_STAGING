#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: per_opcode.py run -- every valid row's polyfill (243 rows)"
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode
python3 per_opcode.py run
echo "[1/1] done"
