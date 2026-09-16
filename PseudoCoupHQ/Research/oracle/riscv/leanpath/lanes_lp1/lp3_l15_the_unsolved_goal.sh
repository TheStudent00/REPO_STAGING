#!/bin/bash
# lp3_l15_the_unsolved_goal.sh -- the walk certificate for c_op_210 (divw):
# the goal simp leaves, in full; then two variants of the proof on the same
# file: (a) the same simp then `rfl`; (b) `simp` with the full default set
# plus the list. LITERAL. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
P=/work/proof; cd $P
F=PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_handful_all_v2/Walk_c_op_210.lean
echo "[1/3] the goal simp leaves, in full (the file as generated)"
timeout 600 lake env lean $F 2>&1 | head -80 | cut -c1-260
echo "[2/3] variant a: the same simp, then rfl; variant b: simp with the default set too"
sed 's/^    h10, h11\]$/    h10, h11]\n  rfl/' $F > /work/W_a.lean
sed 's/simp (config := {decide := true}) only \[/simp (config := {decide := true}) [/' $F > /work/W_b.lean
for v in a b; do echo "--- variant $v"; timeout 600 lake env lean /work/W_$v.lean 2>&1 | head -30 | cut -c1-240; done
echo "[3/3] what rX unfolds to on a literal index: a tiny probe"
cat > /work/RX.lean <<'L'
import LeanIM
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIM LeanIM.Functions
set_option maxHeartbeats 1000000000
example : (BitVec.toNatInt (0x0a#5 : BitVec 5)) = 10 := by decide
example : (BitVec.toNatInt (0x0a#5 : BitVec 5)) = 10 := by simp [BitVec.toNatInt]
example : (BitVec.toNatInt (0x0a#5 : BitVec 5)) = 10 := by rfl
example (s : SequentialState RegisterType trivialChoiceSource) : (rX (Regno 10)) s = (do let v ← readReg Register.x10; pure (regval_from_reg v)) s := by
  simp only [rX]
example (s : SequentialState RegisterType trivialChoiceSource) : (rX (Regno 10)) s = (do let v ← readReg Register.x10; pure (regval_from_reg v)) s := by
  rfl
L
timeout 600 lake env lean /work/RX.lean 2>&1 | head -40 | cut -c1-240
echo done
