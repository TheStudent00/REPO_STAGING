#!/usr/bin/env bash
# ex1_l10_interp_the_seventy_d.sh -- task ex1, step 6, fourth pass, and
# the one thing left is c#: its build's PRODUCT was being handed to the
# operating system as a program, and a .NET dll is not one -- the run
# that caught it answered `emu.dll: Permission denied`.  The build's
# `prepare` now returns the dialect's own command, which runs the dll
# through the host (`dotnet exec`).
#
# The third pass's store is kept as `expand1_interp_pass3.jsonl`.
# Nothing is deleted.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX1.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/4] the third pass's store, kept under its own name"
if [ -f expand1_interp.jsonl ] && [ ! -f expand1_interp_pass3.jsonl ]; then
    mv expand1_interp.jsonl expand1_interp_pass3.jsonl
    echo "   expand1_interp.jsonl -> expand1_interp_pass3.jsonl"
    wc -l expand1_interp_pass3.jsonl
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
