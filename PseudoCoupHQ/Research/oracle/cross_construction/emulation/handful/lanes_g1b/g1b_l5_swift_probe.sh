#!/usr/bin/env bash
# g1b_l5_swift_probe.sh -- task g1b, section 2: is there a swift compiler
# in this container at the path the whole swift corpus was built at, and
# what does it answer?
#
# WHAT CHANGED SINCE TASK g1 MEASURED THE SAME THINGS, and it is two
# things, not one:
#   1. THE IMAGE.  The coordinator rebuilt `sandbox-runner:latest` with
#      `libncurses6` and streamed it to the tower.  An instance picks a
#      new image only when its CONTAINER is re-created, so this task ran
#      `remote_lane.sh down --instance g1` then `up --instance g1`
#      before this lane.
#   2. THE PERSIST VOLUME.  `g1.conf` named none, so Airlock gave the
#      container the default `g1-persist`, which is EMPTY -- and swift
#      lives at /persist/swift on the DEFAULT instance's volume,
#      `sandbox-persist`.  That, and not a loader failure, is why every
#      swift place task g1 ran was refused with "No such file or
#      directory".  `g1.conf` now names `sandbox-persist` READ-ONLY,
#      exactly as `t101b.conf` and `t103.conf` already do for the same
#      toolchain.
# Each step below separates the two, so the answer says which of them
# was the obstacle rather than asserting one.
#
# NO WORKAROUND IS ATTEMPTED HERE and none is anywhere in this task: no
# LD_LIBRARY_PATH, no copied library, no second path.  If swiftc still
# refuses, its own words are the result.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1B.  Every step
# is a listing or one compiler invocation.
set -uo pipefail
run () { echo; printf '$'; printf ' %q' "$@"; echo; "$@"; }

echo "[1/6] task g1b: /persist as this instance now sees it"
run ls -la /persist

echo "[2/6] task g1b: the swiftc the corpus was built with, at the path lane_gen.py names"
run ls -la /persist/swift/usr/bin/swiftc

echo "[3/6] task g1b: is libncurses.so.6 in the image now"
run ls -la /usr/lib/x86_64-linux-gnu/libncurses.so.6

echo "[4/6] task g1b: swiftc --version, LITERAL"
run /persist/swift/usr/bin/swiftc --version

echo "[5/6] task g1b: the shared libraries swiftc asks the loader for, and whether each resolves"
run ldd /persist/swift/usr/bin/swift-driver

echo "[6/6] task g1b: one swift source through it at the corpus's own ship flags"
D=$(mktemp -d)
printf '%s\n' '@_cdecl("emu_probe")' 'public func emu_probe(_ a: Int32, _ b: Int32) -> Int32 {' '    return a &+ b' '}' > $D/probe.swift
run cat $D/probe.swift
run /persist/swift/usr/bin/swiftc -O -c $D/probe.swift -o $D/probe.o
run ls -la $D/probe.o
echo "done"
