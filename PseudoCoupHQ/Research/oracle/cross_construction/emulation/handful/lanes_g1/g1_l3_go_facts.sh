#!/usr/bin/env bash
# g1_l3_go_facts.sh -- task g1: what the go toolchain ITSELF does, one
# probe per question the go renderer's spelling table asks.
#
# WHY THIS RUNS BEFORE A SINGLE GO SPELLING IS WRITTEN: task o11's
# section 3.1 is the shape this task was told to copy -- the target is
# MEASURED, and three of task o11's twenty rust spellings changed on
# what the probes came back with.  Each probe is built at the go
# corpus's own ship flags (a plain `go build`, read off `lane_gen.py`'s
# go branch, which the program prints) and carved with the pipeline's
# own objdump reader.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1; the program
# prints its own peak.  Each build writes one executable into a
# temporary directory and deletes it.
set -euo pipefail
echo "[1/2] task g1: go_facts.py probe"
python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/go/go_facts.py probe
echo "[2/2] done"
