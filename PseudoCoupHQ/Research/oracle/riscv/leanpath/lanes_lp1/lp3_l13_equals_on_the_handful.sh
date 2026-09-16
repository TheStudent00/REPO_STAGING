#!/bin/bash
# lp3_l13_equals_on_the_handful.sh -- LeanExpr.equals: each certified unit
# meaning against every definition of its arity, every value of each
# enumerated operation, in the plan's order (same text; integer level by
# grind; fixed width by bv_decide), budget 120 s a stage. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
echo "[1/2] equals over the walk's certified units"
cd $A; start=$(date +%s)
python3 -u -m leanpath equals $P $PLIB $A/strip_6266b40c_8eb1fb6b_all/strip.json $A/walk_handful_all_c/walk.json $A/equals_handful_all 120 64 2>&1 | tail -120
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[2/2] one proved theorem, LITERAL"
python3 - <<'PY'
import json
d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/equals_handful_all/equals.json"))
for r in d["rows"]:
    for res in r["results"]:
        if res["verdict"]=="PROVED":
            ok=[t for t in res["tried"] if t["rc"]==0][0]
            print("---", r["unit"], res["definition"], res["operation"], res["stage"]); t=open(ok["lean_file"]).read().split("\n"); i=[k for k,l in enumerate(t) if l.startswith("theorem ")][-1]; print("\n".join(t[i:i+6])); raise SystemExit
PY
echo done
