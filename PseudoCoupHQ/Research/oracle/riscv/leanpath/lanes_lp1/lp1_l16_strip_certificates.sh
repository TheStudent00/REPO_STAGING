#!/bin/bash
# lp1_l16_strip_certificates.sh -- SailModel.strip over every execute clause
# of the built emit: Python proposes each clause's pure form by the one
# rule, Lean certifies it against the emitted clause (per-clause files,
# `lake env lean` inside the built project). Fetches nothing.
set -uo pipefail
total=4
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
P=/persist/lp1/Lean_IMZ
LIB=$(grep -oE 'name = "Lean[A-Za-z]*"' $P/lakefile.toml | head -1 | cut -d'"' -f2)
OUT=PseudoCoupHQ/Research/oracle/riscv/leanpath/strip_6266b40c_8eb1fb6b_IMZ
echo "[1/$total] tools; fetched nothing"; cd $P; cat lean-toolchain; lake --version | head -1; echo "lib: $LIB"; ls $P/.lake/build/lib/lean 2>/dev/null | head -3
echo "[2/$total] a first clause alone, to see one certificate and its time (LITERAL)"
cd PseudoCoupHQ/Research/oracle/riscv/leanpath
python3 -m leanpath strip $P $LIB $OUT 900 execute_DIV 2>&1 | tail -4
cat $OUT/Strip_DIV.lean
echo "[3/$total] every clause"
start=$(date +%s)
python3 -m leanpath strip $P $LIB $OUT 900 2>&1 | tail -80
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[4/$total] the failures' first errors, LITERAL"
python3 - <<'PY'
import json
d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/strip_6266b40c_8eb1fb6b_IMZ/strip.json"))
for r in d["rows"]:
    if r["verdict"]=="FAILED":
        print(" ", r["clause"]); [print("     ", e[:200]) for e in r["errors"][:4]]
print(json.dumps(d["summary"]))
PY
echo done
