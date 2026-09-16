#!/bin/bash
# lp3_l11_walk_only.sh -- the walk on the handful alone, over the strip
# lane 10 produced, with the walk's parser fixed for the decoder's printed
# form (hex indices, multi-line constructors, stub trace lines) and the
# proof library's prefix on every term. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
echo "[1/2] the walk on the handful"
cd $A; start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $A/strip_6266b40c_8eb1fb6b_all/strip.json $A/handful_units.json $A/walk_handful_all_b 900 2>&1 | tail -90
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[2/2] one certificate and one failure, LITERAL"
python3 - <<'PY'
import json
d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_all_b/walk.json"))
for want in ("CERTIFIED","FAILED"):
    rs=[r for r in d["rows"] if r.get("verdict")==want and r.get("lean_file")]
    if rs:
        print("---", want, rs[0]["unit"], rs[0]["lean_file"])
        t=open(rs[0]["lean_file"]).read().split("\n")
        i=[k for k,l in enumerate(t) if l.startswith("theorem meaning_")][0]
        print("\n".join(t[i:i+16])); [print("   ", e[:220]) for e in rs[0].get("errors",[])[:4]]
PY
echo done
