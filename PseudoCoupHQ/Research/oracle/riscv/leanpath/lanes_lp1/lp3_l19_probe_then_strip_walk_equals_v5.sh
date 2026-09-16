#!/bin/bash
# lp3_l19_probe_then_strip_walk_equals_v5.sh -- first one certificate
# (c_op_210, divw) with the simp list extended by RETIRE_SUCCESS, the
# register-name mapping, to_bits, extractLsb and zero_reg; if it closes,
# the strip (the c.mul alias on one line), the walk on the eighteen units,
# and the equals. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5; W=$A/walk_handful_all_v5; E=$A/equals_handful_all_v5
echo "[1/5] the probe: the divw certificate with the extended list"
F=$A/walk_handful_all_v4/Walk_c_op_210.lean
sed 's/^    rX_bits, rX, wX_bits, wX, regval_from_reg, regval_into_reg, PreSail.readReg, PreSail.writeReg,$/    rX_bits, rX, wX_bits, wX, regval_from_reg, regval_into_reg, PreSail.readReg, PreSail.writeReg,\n    RETIRE_SUCCESS, reg_name_forwards, to_bits, Sail.BitVec.extractLsb, zero_reg,/' $F > /work/W_probe.lean
cd $P; start=$(date +%s); timeout 600 lake env lean /work/W_probe.lean > /work/W_probe.out 2>&1; rc=$?
echo "  rc=$rc seconds=$(( $(date +%s) - start )); error lines: $(grep -c error /work/W_probe.out)"; grep -vE "warning|Hint|^\s*$|simp \(config|̵|̲" /work/W_probe.out | head -30 | cut -c1-220
[ $rc -eq 0 ] || { echo "FLAG: the certificate does not close; the walk is not run"; exit 3; }
echo "[2/5] strip over every clause of the whole-model proof emit"
cd $A; start=$(date +%s)
python3 -m leanpath strip $P $PLIB $S 900 2>&1 | grep -E "strip:|FAILED" | head -8
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/5] the walk on the handful"
start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $S/strip.json $A/handful_units.json $W 900 2>&1 | grep -vE "^\s*$" | tail -60
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[4/5] equals over the certified units"
start=$(date +%s)
python3 -u -m leanpath equals $P $PLIB $S/strip.json $W/walk.json $E 120 64 2>&1 | tail -140
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[5/5] one certified meaning and one proved equality, LITERAL"
python3 - <<'PY'
import json
W="PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_all_v5/walk.json"; E="PseudoCoupHQ/Research/oracle/riscv/leanpath/equals_handful_all_v5/equals.json"
try:
    d=json.load(open(W))
    for want in ("CERTIFIED","FAILED"):
        rs=[r for r in d["rows"] if r.get("verdict")==want and r.get("lean_file")]
        if rs:
            print("--- walk", want, rs[0]["unit"]); t=open(rs[0]["lean_file"]).read().split("\n"); i=[k for k,l in enumerate(t) if l.startswith("theorem meaning_")][0]; print("\n".join(t[i:i+4])); [print("   ", e[:230]) for e in rs[0].get("errors",[])[:5]]
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
