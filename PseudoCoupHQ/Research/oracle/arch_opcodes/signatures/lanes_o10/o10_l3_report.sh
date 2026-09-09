#!/bin/bash
# o10_l3_report.sh -- task o10: render ledger_signatures.json to .md.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/signatures
echo "[1/1] task o10: ledger_signatures.py report"
python3 ledger_signatures.py report
echo "[1/1] done"
