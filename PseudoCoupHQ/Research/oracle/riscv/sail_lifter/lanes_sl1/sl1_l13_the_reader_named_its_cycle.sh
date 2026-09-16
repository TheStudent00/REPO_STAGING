#!/bin/bash
# sl1 lane 13 -- lane 12 again with the call trail printed on a depth
# overflow, and the parser's unread list for InstsEnd.lean (the decoder
# is still unread there).
set -u
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
E=$SL/lean_emit
mkdir -p /work/sl1e
echo "[1/2] the unread definitions of InstsEnd.lean and Regs.lean, LITERAL"
timeout 900 python3 $SL/lean_reader.py $E 2>&1 | grep 'UNREAD' | grep 'InstsEnd\|Regs.lean\|Types.lean\|Prelude' | head -30
echo "[2/2] reset and the first words, with the trail"
sed -n '/^timeout 1200 python3 - <<.PYEOF.$/,/^PYEOF$/p' $SL/lanes_sl1/sl1_l12_the_reader_evaluates_again.sh | sed '1d;$d' > /work/sl1e/probe.py
timeout 1200 python3 /work/sl1e/probe.py 2>&1 | grep -v '^   REFUSED: no definition named encdec_backwards' | head -80
echo "done $(date -u +%FT%TZ)"
