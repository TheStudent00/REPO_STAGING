#!/usr/bin/env bash
# hub2_l10_measure_all.sh -- task hub2, lane 10: the measure over EVERY
# corpus go unit (590), each asked at the level the dictionary serves it
# at -- cell, else pair, else pool entry -- built and carved for c, rust
# and go and gated against the unit's own canon40 record, which IS go's
# own carved body.  The 134 units task hub1 asked about are flagged in
# the store so the two tasks' numbers sit beside each other.  The sample
# of 12 ran first (lane hub2_l9): 36 rows in 9.5 s at 98,516 kB peak.
# Memory bound 6 GB, named abort ABORT_MEMORY_HUB2.
set -uo pipefail
echo "[1/1] the whole population"
cd PseudoCoupHQ/Research/oracle/hub
time python3 hub2.py measure
