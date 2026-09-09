#!/usr/bin/env bash
# t101b lane 1 -- the SAMPLE: 12 accepted probes per language, 60 in all,
# recompiled at the ANCHOR flags and their parameter / return types read
# off the binary's own DWARF with pyelftools. Then three rows LITERAL.
set -u
export HOME=/work
export PATH=/persist/swift/usr/bin:$PATH
# swift's binaries want libncurses.so.6 and the image ships only
# libncursesw.so.6.6; the probe lanes' own prologue makes this symlink
# and it does not survive a container restart (lane_gen.py).
if [ -f /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 ]; then
  ln -sf /usr/lib/x86_64-linux-gnu/libncursesw.so.6.6 \
     /usr/lib/x86_64-linux-gnu/libncurses.so.6 2>/dev/null
  ldconfig 2>/dev/null
fi
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "======== [1/2] types101_anchor_dwarf.py --sample 12 ========"
python3 types101_anchor_dwarf.py --sample 12 --workers 6 --force
rc=$?
echo "types101_anchor_dwarf.py exit ${rc}"
echo "======== [2/2] three rows LITERAL ========"
python3 -c "
import json,glob
for f in ['types101_dwarf_rows_sample/op_units2_c_c0000.json','types101_dwarf_rows_sample/op_units2_go_c0000.json','types101_dwarf_rows_sample/op_units2_swift_c0000.json']:
    try: d=json.load(open(f))
    except Exception as e: print(f,'ERR',e); continue
    rows=[r for r in d['rows'] if r['role']=='parameter']
    print(json.dumps(rows[0]) if rows else (f,'no parameter row'))
"
exit ${rc}
