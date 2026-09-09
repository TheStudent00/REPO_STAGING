#!/usr/bin/env bash
# g1_l1_toolchains.sh -- task g1, step 0: does each of the four target
# toolchains START in this image, and which version is it?
#
# WHY THIS LANE EXISTS AND RUNS FIRST.  The brief states that
# `/persist/swift/usr/bin/swiftc` fails to load `libncurses.so.6` in the
# image task h2 ran under, and that a rebuilt image is being pushed to
# the tower.  So swiftc's ability to START is a MEASUREMENT this task
# takes before it writes a single swift spelling -- if it still fails,
# every swift row of the deliverable is REFUSED with the literal error
# and no workaround is attempted (no LD_LIBRARY_PATH, no copied
# libraries).  The other three are printed beside it so the four
# columns of the deliverable are all attested by one lane.
#
# `|| true` on each step: a toolchain that cannot start is the RESULT
# this lane is measuring, not a lane failure.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1.  Four
# version prints; nothing here allocates.
set -uo pipefail
echo "[1/5] task g1: clang, the c corpus's compiler"
/usr/bin/clang --version 2>&1 | head -2 || true
echo "[2/5] task g1: rustc, the rust corpus's compiler"
rustc --version 2>&1 | head -2 || true
echo "[3/5] task g1: go, the go corpus's compiler"
go version 2>&1 | head -2 || true
echo "[4/5] task g1: swiftc at the path lane_gen.py names"
/persist/swift/usr/bin/swiftc --version 2>&1 | head -5 || true
echo "[5/5] task g1: the loader's own reading of that swiftc"
ldd /persist/swift/usr/bin/swiftc 2>&1 | grep -E "not found|ncurses" || true
echo "done"
