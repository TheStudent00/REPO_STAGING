#!/bin/sh
# runtime_callee_swift_lane2.sh -- TASK 63 (b): extract swift's runtime
# callees from SWIFT'S OWN builtins archive, inside the `trickle`
# Airlock instance, which is the only place /persist/swift is mounted.
#
# Submitted with:
#   python3 Airlock/airlock --instance trickle submit \
#       PseudoCoupHQ/Research/op_pipeline/runtime_callee_swift_lane2.sh \
#       --batch t63 --weight 1
#
# The path check below is what proves which side of the container wall
# this is running on: /persist/swift exists only inside the instance.
set -u
echo "=== task 63 (b) rerun, swiftc itself answering -- swift's runtime callees ==="
date -u +%Y-%m-%dT%H:%M:%SZ
echo
echo "--- which side of the wall ---"
echo "uname:   $(uname -a)"
echo "hostname: $(hostname)"
ls -l /persist/swift/usr/bin/swiftc
echo
# swift's binaries want libncurses.so.6 and the image ships only
# libncursesw.so.6.6; the symlink lives in the image's own /usr/lib and
# does NOT survive a container restart (lane_gen.py carries the same
# block, for the same reason).
if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then
  ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \
     /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null
  ldconfig 2>/dev/null
fi
if [ ! -x /persist/swift/usr/bin/swiftc ]; then
  echo "!! REFUSING TO START: /persist/swift/usr/bin/swiftc is not runnable."
  exit 4
fi
for tool in nm ar objdump python3; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "!! REFUSING TO START: $tool is not runnable."
    exit 4
  fi
done
nm --version | head -1
objdump --version | head -1
python3 --version
echo
python3 PseudoCoupHQ/Research/op_pipeline/runtime_callee_swift_lane.py
code=$?
echo
echo "lane exit: $code"
exit $code
