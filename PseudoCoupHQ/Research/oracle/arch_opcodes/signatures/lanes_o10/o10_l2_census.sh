#!/bin/bash
# o10_l2_census.sh -- task o10: run the ledger signature census.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/arch_opcodes/signatures
echo "[1/1] task o10: ledger_signatures.py census"
python3 ledger_signatures.py census
echo "[1/1] done"
