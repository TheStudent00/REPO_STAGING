#!/usr/bin/env bash
# hub2_l12_handful_and_measure_again.sh -- task hub2, lane 12: the
# handful and the whole measure again, after TWO causes lane hub2_l10
# measured were closed, each in the one place that owned it and neither
# by a patch to a name:
#   1. a go emulation may call a HELPER function its own file declares
#      (`sel32`), and task hub1's reader carried the emulation's own
#      function alone, so every go pair composition failed to build with
#      `undefined: sel32`.  The composed go file now carries the
#      emulation file's other functions as c's file carries its `static
#      inline` helpers, deduplicated by their own text.
#   2. four go compositions failed to build with `cannot convert a
#      (variable of type bool) to type int32`: go has no conversion from
#      its truth holder into an integer holder, where c and rust both
#      have one.  That is a holder mismatch and it is now REFUSED BY
#      CAUSE, which is the brief's third answer applied on the node's
#      side.
# Memory bound 6 GB, named abort ABORT_MEMORY_HUB2.
set -uo pipefail
echo "[1/3] the handful"
cd PseudoCoupHQ/Research/oracle/hub
time python3 hub2.py handful
echo "[2/3] the whole measure"
time python3 hub2.py measure
echo "[3/3] the tables"
python3 hub2.py tables
