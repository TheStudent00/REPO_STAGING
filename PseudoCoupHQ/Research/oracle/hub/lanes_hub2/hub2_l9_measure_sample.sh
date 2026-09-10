#!/usr/bin/env bash
# hub2_l9_measure_sample.sh -- task hub2, lane 9: the measure SAMPLED
# FIRST as the law requires, over the first 12 of the corpus's go units,
# so the peak resident and the per-unit cost are measured before the
# whole population is asked.  Memory bound 6 GB, named abort
# ABORT_MEMORY_HUB2.  It writes measure2.json, which lane hub2_l10 then
# overwrites with the whole population.
set -uo pipefail
echo "[1/1] the sample of 12"
cd PseudoCoupHQ/Research/oracle/hub
time python3 hub2.py measure 12
