#!/usr/bin/env bash
# ap2_l8_measure_the_fixes_again.sh -- task ap2: the same measurement lane as ap2_l6, re-run after two defects in the MEASUREMENT (not in a fix) were corrected: src2/ did not exist, and a pair was looked up by task ap1's own key_width, which fix 4 has since moved on eight cells.
# PAIRS IT TARGETS, before the full loop.
#
# `autopoly2.py measure <a substring of the cause>` reads task ap1's
# own store, takes exactly the (cell, target) pairs whose cause holds
# that substring, runs each again through the driver as task ap2 leaves
# it, and prints the cause before and the cause after, pair by pair and
# summed.  It writes nothing: the store this task's loop fills is
# `autopoly2_runs.jsonl` and no line of it comes from here.
#
# The six substrings below are the six rows of the brief's own table,
# in its order.  Their run counts in task ap1's loop were 134, 128, 56,
# 30, 24 and 16 -- 388 pairs in all, against the loop's 1,012.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP2, checked
# after every pair.  Task ap1's whole 1,012-run lane peaked at
# 2,414,988 kB, so 388 pairs sit well inside it; the peak is printed at
# the end of every measurement.
set -euo pipefail
mkdir -p /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/src2
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "===== FIX 1: a term that reads state that is not an arrival register ====="
python3 autopoly2.py measure "not an arrival register"

echo "===== FIX 2: no setter row to compose the flag pair from ====="
python3 autopoly2.py measure "no setter row to compose"

echo "===== FIX 3a: the whole-register vector cell with no lane to project ====="
python3 autopoly2.py measure "so there is no lane to project"

echo "===== FIX 3b: the 128-bit place go and swift have no holder for ====="
python3 autopoly2.py measure "has no holder for"

echo "===== FIX 4: the six cells whose key_width was null ====="
python3 autopoly2.py measure "a real number is required"

echo "===== FIX 5a: cmovg ====="
python3 autopoly2.py measure "'cmovg' has no entry"

echo "===== FIX 5b: movswq ====="
python3 autopoly2.py measure "'movswq' has no entry"

echo "===== FIX 5c: the lea form with no base register ====="
python3 autopoly2.py measure "lea addressing form"
echo "done"
