#!/usr/bin/env bash
# g1_l2_swift_where.sh -- task g1: where is swiftc in THIS image, if it
# is anywhere?
#
# WHY.  Lane g1_l1 found nothing at `/persist/swift/usr/bin/swiftc`, the
# path `lane_gen.py`'s swift branch names and the path the brief names.
# The brief's expectation was a LOAD failure (`libncurses.so.6`); what
# came back is an ABSENCE, which is a different fact, so this lane
# measures which it is rather than guessing: what `/persist` holds in
# this instance, and whether a swift toolchain sits anywhere else on the
# image's own filesystem.
#
# `|| true` everywhere: an empty answer is the measurement.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1.  Directory
# listings only.
set -uo pipefail
echo "[1/6] task g1: /persist as this instance sees it"
ls -la /persist 2>&1 | head -20 || true
echo "[2/6] task g1: swiftc on PATH"
command -v swiftc 2>&1 || echo "  (not on PATH)"
echo "[3/6] task g1: any file named swiftc on the image's own filesystem"
find / -xdev -name "swiftc" -maxdepth 8 2>/dev/null | head -10 || true
echo "[4/6] task g1: any directory named swift near the usual roots"
ls -d /usr/lib/swift /usr/share/swift /opt/swift /usr/local/swift 2>&1 | head -10 || true
echo "[5/6] task g1: is libncurses.so.6 present at all"
ls -la /usr/lib/x86_64-linux-gnu/libncurses*.so* 2>&1 | head -10 || true
echo "[6/6] task g1: the swift branch of lane_gen.py, LITERAL"
sed -n '/if LANG == "swift":/,/raise KeyError/p' \
    PseudoCoupHQ/Research/op_pipeline/lane_gen.py
grep -n "^SWIFTC" PseudoCoupHQ/Research/op_pipeline/lane_gen.py
echo "done"
