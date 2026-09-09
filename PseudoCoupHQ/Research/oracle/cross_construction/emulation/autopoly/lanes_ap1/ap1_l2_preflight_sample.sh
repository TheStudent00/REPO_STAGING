#!/usr/bin/env bash
# ap1_l2_preflight_sample.sh -- task ap1, the SAMPLE the law requires
# before a long run: the outer set printed as the loop will walk it,
# then the first twenty runs of that loop and nothing more, with the
# peak resident size printed after every one.
#
# WHAT THIS MEASURES, and why twenty: the law's memory rule ("state the
# bound, sample first, paste peak RSS"), and the pace -- twenty runs is
# five cells across the four targets, which includes one go build and
# one swiftc compile per cell, the two slow toolchains. The whole loop
# is 1,012 runs, so the seconds-per-run this lane prints is what says
# whether the brief's one-to-three hours holds.
#
# MEMORY BOUND: 6 GB resident on the one collecting process, named
# abort ABORT_MEMORY_AP1, checked after every run. The reads are
# `autopoly_cells.json` (2 MB), `model_table_rows.json` (50 MB, once),
# `single_opcode_units.json` (1.6 MB, cached) and one probe manifest
# per target.
#
# THE STORE IS INCREMENTAL: the twenty runs this lane writes stay on
# `autopoly_runs.jsonl` and the run lane resumes from run twenty-one.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/3] the toolchains this loop compiles with"
clang --version | head -1
rustc --version
go version
/persist/swift/usr/bin/swiftc --version | head -1
echo "[2/3] preflight: the outer set as the loop will walk it"
python3 autopoly.py preflight
echo "[3/3] the first twenty runs"
python3 autopoly.py run 20
