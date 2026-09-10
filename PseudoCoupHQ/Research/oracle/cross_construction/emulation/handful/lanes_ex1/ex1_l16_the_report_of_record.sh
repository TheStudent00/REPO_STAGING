#!/usr/bin/env bash
# ex1_l16_the_report_of_record.sh -- task ex1: the report of record,
# with the two sources compared on what they COMPUTE (the label carries
# the target's own name, which is not a difference in the source) and
# the JIT section measured rather than asserted.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/4] the handful's ten cells on cpp beside c, with the sources compared"
python3 expand1.py handful
echo ""
echo "[2/4] what the corpus's JIT output actually is"
python3 expand1.py jit
echo ""
echo "[3/4] the report"
python3 expand1.py report
echo ""
echo "[4/4] the report's own first lines"
sed -n '1,20p' expand1.md
wc -l expand1.md
echo "done"
