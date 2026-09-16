#!/bin/bash
# lp3_l7_filled_state_probe_strip_and_walk_third.sh -- the decoder's state built
# as the model's own emulator builds it (every register written first, then
# sail_model_init, then init_model), probed on six words; then the strip
# over the whole-model proof emit (its library name read correctly: that
# lakefile declares two libraries), then the walk on the handful.
set -uo pipefail
total=4
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
XLIB=$(grep -A1 '\[\[lean_lib\]\]' $X/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
echo "[1/$total] the filled state and the decoder, LITERAL (exec lib $XLIB; proof lib $PLIB)"
cd $A && python3 - $X $XLIB <<'PY' > /work/Probe10.lean
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath import walk as W
import os
X, lib = sys.argv[1], sys.argv[2]
print("import %s\nopen Sail Sail.ConcurrencyInterfaceV1 PreSail %s %s.Functions\nset_option maxHeartbeats 1000000000\nset_option maxRecDepth 100000" % (lib, lib, lib))
print("\n".join(W.state_defs(os.path.join(X, lib))))
print('#eval IO.println ("registers written: " ++ toString filled.regs.size)')
print('#eval IO.println ("init on filled: " ++ (match (do sail_model_init (); init_model "") filled with | .ok _ s => s!"ok, regs {s.regs.size}" | .error e s => s!"ERROR {e.print} (regs {s.regs.size})"))')
print('#eval IO.println ("misa: " ++ (match s0.regs.get? .misa with | some v => toString (repr v) | none => "absent"))')
for tag, w in [("c.add", "952e"), ("divw", "02b5453b"), ("mulh", "02b54533"), ("c.jr ra", "8082"), ("fcvt.s.w", "d00577d3"), ("czero.eqz", "0eb55533")]:
    print('#eval IO.println ("%-9s " ++ (%s))' % (tag, W.decode_expr(w)))
PY
cd $X; timeout 900 lake env lean /work/Probe10.lean 2>&1 | cut -c1-240 | head -12
timeout 900 lake env lean /work/Probe10.lean 2>&1 | grep -q "divw .*instruction\.[A-Z]" || { echo "FLAG: the decoder still does not answer"; exit 3; }
echo "[2/$total] strip over every clause of the whole-model proof emit"
cd $A; start=$(date +%s)
python3 -m leanpath strip $P $PLIB $A/strip_6266b40c_8eb1fb6b_all 900 2>&1 | tail -4
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/$total] the walk on the handful"
start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $A/strip_6266b40c_8eb1fb6b_all/strip.json $A/handful_units.json $A/walk_handful_all 900 2>&1 | tail -80
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[4/$total] one certificate, LITERAL"
f=$(python3 - <<'PY'
import json
d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_all/walk.json"))
c=[r for r in d["rows"] if r.get("verdict")=="CERTIFIED"]; a=[r for r in d["rows"] if r.get("lean_file")]
print((c or a)[0]["lean_file"] if (c or a) else "")
PY
); [ -n "$f" ] && { echo "--- $f"; grep -n "theorem meaning_" -A4 "$f" | cut -c1-220; }
echo done
