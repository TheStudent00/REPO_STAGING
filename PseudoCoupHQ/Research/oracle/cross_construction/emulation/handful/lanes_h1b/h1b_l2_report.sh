#!/usr/bin/env bash
# h1b_l2_report.sh -- task h1b: `handful.md` regenerated after
# `composition_gloss` was fixed so an unmapped instruction (starred)
# is never dropped by the table cell's length cut -- lane h1b_l1's own
# md had `cqto` truncated out of the `idiv` rows.  `handful.json` is
# unchanged (the fix is in the report writer, not the data); `compose`
# is not re-run.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
echo "[1/2] task h1b: handful.py report"
python3 handful.py report
echo "[2/2] the spelling guard, unmodified, over every json this task touched"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful_cells.json \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.json
echo "done"
