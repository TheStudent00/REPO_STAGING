#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: opcode_signatures.py census (reads unique_opcodes.json's mnem field)"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/signatures
python3 opcode_signatures.py census
echo "[1/1] done"
