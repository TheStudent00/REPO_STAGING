#!/usr/bin/env bash
# hub1_l11_measure_sample.sh -- task hub1, lane 11: the section-3 measure,
# SAMPLED FIRST as the law requires, over the first 12 of the corpus's go
# units that name one cell, so the peak resident and the per-unit cost are
# measured before the whole population is asked. Memory bound 6 GB, named
# abort ABORT_MEMORY_HUB1. It writes measure.json, which lane hub1_l12
# then overwrites with the whole population.
set -uo pipefail
echo "[1/1] the sample of 12"
cd PseudoCoupHQ/Research/oracle/hub
time python3 hub.py measure 12
