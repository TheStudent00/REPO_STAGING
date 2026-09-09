#!/usr/bin/env bash
# task o6 lane 6 (resume): go_types_join.py -- o4's walk re-run per site
# (gated equal to o4's json row), joined by position to the oracle's
# sites (go_types_sites.json.gz, streamed), writing go_types_join.json and
# go_types_report.md. Bound 3 GB (ABORT_MEMORY_O6), peak RSS printed.
set -uo pipefail
echo "[1/1] go_types_join.py"
python3 /projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_join.py
echo "join exit: $?"
ls -l /projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_join.json /projects/PseudoCoupHQ/Research/oracle/compiler_units/go_types_report.md
echo "[1/1] done"
