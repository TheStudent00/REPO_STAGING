#!/usr/bin/env bash
# ex1_l9_interp_the_seventy_c.sh -- task ex1, step 6, third pass.  The
# second pass (lane ex1_l8) fixed php and left three things, each fixed
# here in the layer that owns it and none of them worked around:
#
#   1. java's main was broken BY THE c# FIX: `out` is a reserved word
#      in c# and the rename was applied to the file rather than to the
#      c# dialect, so java declared `answers` and used `out`.  Both
#      mains say `answers` now.  The run that caught it is on the
#      record: `Emu.java:158: error: cannot find symbol`.
#   2. c#'s build now succeeds and its LAUNCHER does not: a
#      framework-dependent binary looks for a runtime on the machine's
#      own path and the runtime is in the persist volume, so it
#      answered `You must install .NET to run this application`, exit
#      131.  The measurement runs the dll through the host instead
#      (`dotnet exec emu.dll`).
#   3. php's signed division was spelled with `abs`, which python and
#      ruby need because their own division FLOORS -- php's `intdiv`
#      TRUNCATES and needs no such thing, and `abs(PHP_INT_MIN)` leaves
#      php's integers for a float, which declined 27 points as
#      `RAISE:TypeError`.
#
# The second pass's store is kept as `expand1_interp_pass2.jsonl`.
# Nothing is deleted.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX1.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/4] the second pass's store, kept under its own name"
if [ -f expand1_interp.jsonl ] && [ ! -f expand1_interp_pass2.jsonl ]; then
    mv expand1_interp.jsonl expand1_interp_pass2.jsonl
    echo "   expand1_interp.jsonl -> expand1_interp_pass2.jsonl"
    wc -l expand1_interp_pass2.jsonl
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
