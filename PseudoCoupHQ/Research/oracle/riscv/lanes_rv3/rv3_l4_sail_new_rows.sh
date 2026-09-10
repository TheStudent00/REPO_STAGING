#!/usr/bin/env bash
# rv3 lane 4 -- LEVEL 0 FOR THE FIVE NEW ROWS.  The ratified Sail model's
# own simulator run over a bare-metal program that executes each new
# instruction at many concrete inputs, against `riscv_reference.py`'s own
# term for it evaluated at the same inputs.  THIS IS A CHECK AT POINTS,
# NOT AN EQUALITY, exactly as task rv1's was; the count of points is on
# every row.  The sample the law asks for runs first at 200 points.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
export HOME=/work
mkdir -p /work/rv3sail_sample /work/rv3sail
total=3

echo "[1/$total] the reference imports and the five entries are in place"
python3 - <<'EOF'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import riscv_reference as RV
table = RV.OpcodeTable()
print("mnemonics with an entry:", len(table.entries))
for m in ["add.uw", "bseti", "fsgnjn.d"]:
    e = table.entry_for(m)
    print("  ", m, "->", e)
for m in ["c.mul", "c.zext.w"]:
    print("  ", m, "expands to", RV.COMPRESSED[m][0])
EOF
echo "import rc=$?"

echo "[2/$total] the sample: the five rows at 200 points each"
python3 "$RV/sail_points.py" "$RV/level0_points_rv3_sample" \
  /work/rv3sail_sample --points 200 \
  --only add.uw,bseti,c.mul,c.zext.w,fsgnjn.d
echo "sample rc=$?"

echo "[3/$total] the five rows at the brief's cap of 20,000 points each"
python3 "$RV/sail_points.py" "$RV/level0_points_rv3" /work/rv3sail \
  --points 20000 --only add.uw,bseti,c.mul,c.zext.w,fsgnjn.d
echo "full rc=$?"
echo "lane rv3_l4 done"
