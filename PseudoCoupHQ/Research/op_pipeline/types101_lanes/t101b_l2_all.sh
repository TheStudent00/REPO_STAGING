#!/usr/bin/env bash
# t101b lane 2 -- the WHOLE population: every accepted probe of the
# regenerated (29,288) and original (1,779) corpora recompiled at the
# ANCHOR flags, parameter and return types read off the binary's own
# DWARF with pyelftools, one shard per store file.
set -u
export HOME=/work
export PATH=/persist/swift/usr/bin:$PATH
if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then
  ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \
     /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null
  ldconfig 2>/dev/null
fi
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] types101_anchor_dwarf.py (all) ========"
python3 types101_anchor_dwarf.py --workers 6
rc=$?
echo "types101_anchor_dwarf.py exit ${rc}"
exit ${rc}
