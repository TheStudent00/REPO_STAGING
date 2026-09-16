#!/bin/bash
# lp3_l12_strip_again_and_walk.sh -- the strip over the whole model again
# (its record now carries each alias's target and each clause's written
# register), then the walk on the handful. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
echo "[1/3] strip over every clause of the whole-model proof emit"
cd $A; start=$(date +%s)
python3 -m leanpath strip $P $PLIB $A/strip_6266b40c_8eb1fb6b_all 900 2>&1 | grep -E "strip:|FAILED" | head -6
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[2/3] the walk on the handful"
start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $A/strip_6266b40c_8eb1fb6b_all/strip.json $A/handful_units.json $A/walk_handful_all_c 900 2>&1 | tail -90
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/3] one certificate and one failure, LITERAL"
python3 - <<'PY'
import json
d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_all_c/walk.json"))
for want in ("CERTIFIED","FAILED"):
    rs=[r for r in d["rows"] if r.get("verdict")==want and r.get("lean_file")]
    if rs:
        print("---", want, rs[0]["unit"], rs[0]["lean_file"])
        t=open(rs[0]["lean_file"]).read().split("\n")
        i=[k for k,l in enumerate(t) if l.startswith("theorem meaning_")][0]
        print("\n".join(t[i:i+16])); [print("   ", e[:220]) for e in rs[0].get("errors",[])[:4]]
PY
echo done
