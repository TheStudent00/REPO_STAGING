#!/usr/bin/env bash
# g1_l4_go_facts2.sh -- task g1: the go probes again, with the second
# set added.
#
# WHY A SECOND SET: the first set (lane g1_l3) answered the arithmetic,
# the shifts, the division and the arrival registers, and its answers
# RAISED three more questions -- the standard library's bit-cast
# carried a `nop` and the pointer-cast form did not, so the other three
# directions are measured; the two absent-holder probes were refused
# with go's package banner rather than a diagnostic, so they are re-read
# through the pipeline's own three-pass rule (`lane_gen.firstline`); and
# the conditional helper, which go needs because the language has no
# conditional EXPRESSION at all, is measured at every width and sort the
# renderer will ask it for.  The first set is re-run unchanged in the
# same lane so one file holds one version's answers end to end.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1; the program
# prints its own peak.  Lane g1_l3 measured it at 27,696 kB.
set -euo pipefail
echo "[1/2] task g1: go_facts.py probe, both sets"
python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_facts.py probe
echo "[2/2] done"
