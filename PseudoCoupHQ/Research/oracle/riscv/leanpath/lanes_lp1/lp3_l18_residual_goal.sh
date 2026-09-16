#!/bin/bash
# lp3_l18_residual_goal.sh -- the residual goal of the c_op_210 certificate
# (divw), in full; then variants on the same file: (a) the simp, then
# simp_all; (b) the simp with reg_name_forwards, xreg_full_write_callback
# and to_bits unfolded too; (c) the simp with `decide := true` replaced by
# a following `decide`. LITERAL. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
P=/work/proof; cd $P
F=PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_all_v4/Walk_c_op_210.lean
echo "[1/2] the residual goal, in full"
timeout 600 lake env lean $F 2>&1 | head -150 | cut -c1-240
echo "[2/2] variants"
sed 's/^    h10, h11, hk0, hk1, hk2\]$/    h10, h11, hk0, hk1, hk2]\n  simp_all/' $F > /work/W_a.lean
sed 's/^    rX_bits, rX, wX_bits, wX, regval_from_reg, regval_into_reg, PreSail.readReg, PreSail.writeReg,$/    rX_bits, rX, wX_bits, wX, regval_from_reg, regval_into_reg, PreSail.readReg, PreSail.writeReg, reg_name_forwards, to_bits, Sail.BitVec.extractLsb, zero_reg,/' $F > /work/W_b.lean
sed 's/^    h10, h11, hk0, hk1, hk2\]$/    h10, h11, hk0, hk1, hk2]\n  decide/' $F > /work/W_c.lean
for v in a b c; do echo "--- variant $v"; timeout 600 lake env lean /work/W_$v.lean 2>&1 | head -40 | cut -c1-240; done
echo done
