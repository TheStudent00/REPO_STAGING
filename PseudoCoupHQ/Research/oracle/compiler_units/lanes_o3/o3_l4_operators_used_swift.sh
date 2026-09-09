#!/usr/bin/env bash
# lane 4 -- task o3b: the runner image gained tree_sitter_swift, so the
# swift standard library row now runs through the same measure_row()
# path as every other row (compiler_operators_used.py was extended,
# not forked into a second script). Regenerates
# compiler_operators_used.json / .md with all six rows.
set -euo pipefail
echo "[1/1] compiler_operators_used.py (all six rows, swift stdlib now measured)"
python3 /projects/PseudoCoupHQ/Research/oracle/compiler_units/compiler_operators_used.py
echo "[1/1] done"
