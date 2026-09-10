#!/usr/bin/env bash
# hub2_l8_handful.sh -- task hub2, lane 8: the SAME handful task hub1
# composed (`hub/handful/handful.go`, eight explicitly typed functions),
# resolved against the dictionary at two levels and gated against go's
# own build of the same file, per function per target.  It writes
# composed2_c.c, composed2_rust.rs, composed2_go.go,
# composed2_go_inlinable.go and oracle_test2.json.  Memory bound 6 GB,
# named abort ABORT_MEMORY_HUB2.
set -uo pipefail
echo "[1/1] the handful"
cd PseudoCoupHQ/Research/oracle/hub
time python3 hub2.py handful
