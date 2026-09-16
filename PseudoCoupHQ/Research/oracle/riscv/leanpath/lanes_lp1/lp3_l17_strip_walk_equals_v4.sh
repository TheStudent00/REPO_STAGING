#!/bin/bash
# lp3_l17_strip_walk_equals_v4.sh -- the three stages in one lane over the
# current module: the strip over the whole model (its record carrying each
# alias's target and each clause's written register; the let-then-redispatch
# compressed clauses accepted as aliases), the walk on the handful, and the
# equals with enumerated candidates. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v4; W=$A/walk_handful_all_v4; E=$A/equals_handful_all_v4
echo "[1/4] strip over every clause of the whole-model proof emit"
cd $A; start=$(date +%s)
python3 -m leanpath strip $P $PLIB $S 900 2>&1 | grep -E "strip:|FAILED" | head -8
echo "  wall seconds=$(( $(date +%s) - start ))"; python3 -c "import json; d=json.load(open('$S/strip.json')); print('  aliases in the record:', sum(1 for r in d['rows'] if r.get('shape')=='alias' and r['verdict']=='CERTIFIED'))"
echo "[2/4] the walk on the handful"
start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $S/strip.json $A/handful_units.json $W 900 2>&1 | grep -vE "^\s+$" | tail -60
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/4] equals over the certified units"
start=$(date +%s)
python3 -u -m leanpath equals $P $PLIB $S/strip.json $W/walk.json $E 120 64 2>&1 | tail -120
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[4/4] one certified meaning and one proved equality, LITERAL"
python3 - <<'PY'
import json
W="PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_all_v4/walk.json"
E="PseudoCoupHQ/Research/oracle/riscv/leanpath/equals_handful_all_v4/equals.json"
try:
    d=json.load(open(W))
    for want in ("CERTIFIED","FAILED"):
        rs=[r for r in d["rows"] if r.get("verdict")==want and r.get("lean_file")]
        if rs:
            print("--- walk", want, rs[0]["unit"]); t=open(rs[0]["lean_file"]).read().split("\n"); i=[k for k,l in enumerate(t) if l.startswith("theorem meaning_")][0]; print("\n".join(t[i:i+14])); [print("   ", e[:220]) for e in rs[0].get("errors",[])[:4]]
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
