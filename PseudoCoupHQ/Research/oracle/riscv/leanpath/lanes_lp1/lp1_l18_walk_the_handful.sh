#!/bin/bash
# lp1_l18_walk_the_handful.sh -- ArchUnit.meaning on the handful: the ten
# units of rv1 (their words from carved.json) and the four rendered
# multiply-high c sources of rv9 (compiled and carved here at ship flags):
# decode by Sail's own decoder evaluated in the executable emit, compose the
# certified pure forms, certify each unit's meaning in the proof emit.
# Fetches nothing.
set -uo pipefail
total=3
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
P=/persist/lp1/Lean_IMZ; X=/persist/lp1/Lean_IMZ_exec
LIB=$(grep -oE 'name = "Lean[A-Za-z]*"' $P/lakefile.toml | head -1 | cut -d'"' -f2)
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
OUT=$A/walk_handful_6266b40c_8eb1fb6b_IMZ
echo "[1/$total] tools; fetched nothing"; cd $P; cat lean-toolchain; ls $X/.lake/build/lib/lean 2>/dev/null | head -2; clang --version | head -1; llvm-objdump --version | head -2 | tail -1
echo "[2/$total] the walk"
cd $A; start=$(date +%s)
python3 -m leanpath walk $P $X $LIB $A/strip_6266b40c_8eb1fb6b_IMZ_b/strip.json $A/handful_units.json $OUT 900 2>&1 | tail -60
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/$total] one certificate, LITERAL (the first unit that certified, else the first file)"
f=$(python3 - <<'PY'
import json
d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_6266b40c_8eb1fb6b_IMZ/walk.json"))
c=[r for r in d["rows"] if r.get("verdict")=="CERTIFIED"]; a=[r for r in d["rows"] if r.get("lean_file")]
print((c or a)[0]["lean_file"] if (c or a) else "")
PY
); [ -n "$f" ] && { echo "$f"; grep -n "theorem meaning_" -A4 "$f" | cut -c1-200; }
echo done
