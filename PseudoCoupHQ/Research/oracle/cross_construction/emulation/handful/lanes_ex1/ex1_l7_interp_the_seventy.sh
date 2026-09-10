#!/usr/bin/env bash
# ex1_l7_interp_the_seventy.sh -- task ex1, step 6: THE INTERPRETED
# HANDFUL.  The ten cells on each of the seven interpreted targets
# whose runner this machine has.
#
# THE SMOKE STORE IS KEPT, NOT OVERWRITTEN.  Lane ex1_l6's seven runs
# found two defects of this task's own -- php's prelude redeclared the
# built-in `fdiv`, and c#'s `dotnet run` wrote its build's lines onto
# standard output where the answers are read -- so that store is
# renamed `expand1_interp_smoke.jsonl` and stays on the record, and the
# run of record starts on a fresh file.  Nothing is deleted.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX1; every runner is a separate short-lived process
# handed the whole sample at once.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/4] the smoke store, kept under its own name"
if [ -f expand1_interp.jsonl ] && [ ! -f expand1_interp_smoke.jsonl ]; then
    mv expand1_interp.jsonl expand1_interp_smoke.jsonl
    echo "   expand1_interp.jsonl -> expand1_interp_smoke.jsonl"
    wc -l expand1_interp_smoke.jsonl
else
    echo "   nothing to move"
fi

echo ""
echo "[2/4] the seventy"
python3 expand1.py interp_run

echo ""
echo "[3/4] the aggregate"
python3 expand1.py interp_aggregate

echo ""
echo "[4/4] the table"
python3 expand1.py interp_table
echo "done"
