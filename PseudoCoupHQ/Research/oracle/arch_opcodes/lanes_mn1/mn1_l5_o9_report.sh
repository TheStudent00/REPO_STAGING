#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: opcode_signatures.py report -- opcode_signatures.json -> .md"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/signatures
python3 opcode_signatures.py report
echo "[1/1] done"
