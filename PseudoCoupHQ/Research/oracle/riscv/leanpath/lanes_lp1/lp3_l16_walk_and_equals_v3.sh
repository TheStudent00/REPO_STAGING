#!/bin/bash
# lp3_l16_walk_and_equals_v3.sh -- the walk on the handful (now eighteen
# units: the ten of rv1, rv9's four rendered multiply-high sources, and four
# small multiply probes) over lane 14's strip record, with the certificate
# unfolding the emitted callbacks, assuming the support axioms are no-ops,
# and using the default simp set; then the equals. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v2; W=$A/walk_handful_all_v3; E=$A/equals_handful_all_v3
echo "[1/3] the walk"
cd $A; start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $S/strip.json $A/handful_units.json $W 900 2>&1 | grep -vE "^\s*$" | tail -70
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[2/3] equals over the certified units"
start=$(date +%s)
python3 -u -m leanpath equals $P $PLIB $S/strip.json $W/walk.json $E 120 64 2>&1 | tail -140
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/3] one certified meaning and one proved equality, LITERAL"
python3 - <<'PY'
import json
W="PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_all_v3/walk.json"; E="PseudoCoupHQ/Research/oracle/riscv/leanpath/equals_handful_all_v3/equals.json"
try:
    d=json.load(open(W))
    for want in ("CERTIFIED","FAILED"):
        rs=[r for r in d["rows"] if r.get("verdict")==want and r.get("lean_file")]
        if rs:
            print("--- walk", want, rs[0]["unit"]); t=open(rs[0]["lean_file"]).read().split("\n"); i=[k for k,l in enumerate(t) if l.startswith("theorem meaning_")][0]; print("\n".join(t[i:i+5])); [print("   ", e[:230]) for e in rs[0].get("errors",[])[:5]]
except Exception as ex: print("walk record:", ex)
try:
    d=json.load(open(E))
    for r in d["rows"]:
        for res in r["results"]:
            if res["verdict"]=="PROVED":
                ok=[t for t in res["tried"] if t["rc"]==0][0]; print("--- equals PROVED", r["unit"], res["definition"], res["operation"], res["stage"]); t=open(ok["lean_file"]).read().split("\n"); i=[k for k,l in enumerate(t) if l.startswith("theorem ")][-1]; print("\n".join(t[i:i+6])); raise SystemExit
except SystemExit: pass
except Exception as ex: print("equals record:", ex)
PY
echo done
