#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: ledger_signatures.py report -- ledger_signatures.json -> .md"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/signatures
python3 ledger_signatures.py report
echo "[1/1] done"
