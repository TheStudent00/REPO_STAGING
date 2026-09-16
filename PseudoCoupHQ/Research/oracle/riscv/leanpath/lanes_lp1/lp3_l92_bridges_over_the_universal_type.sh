#!/bin/bash
# lp3_l90_bridges_over_the_universal_type.sh -- BUILD AND CHECK `Bridges.lean`:
# one proved statement per primitive the Sail RISC-V model bottoms out in
# (log 289 §2.1, §2.2, §2.3), saying that the primitive IS its counterpart in
# the universal type of `Universal.lean`.
#
# The file was written and checked on the laptop under leanprover/lean4:v4.30.0,
# against lean-sail rev `v5` compiled there from its own sources. This lane does
# the same under the PINNED pair the emit uses -- leanprover/lean4:v4.29.0 and
# the lean-sail already built inside /work/proof -- and in three steps:
#
#   1. the module builds: `Universal.lean` then `Bridges.lean`, nothing else
#      imported, so a failure here is this file's and no one else's.
#   2. the transcriptions are FAITHFUL: `Bridges.lean` transcribes each Sail
#      primitive rather than importing it (the pattern `sailToBitsTruncate` in
#      `Universal.lean` set), so step 2 compiles, against the REAL package,
#          example : @Sail.BitVec.extractLsb = @Universal.Bridges.Sail'.extractLsb := rfl
#      for every one of them. A transcription that has drifted fails here and
#      every theorem in the file is then worth nothing -- which is the point.
#   3. no theorem rests on a sorry or on an axiom of ours: `#print axioms` for
#      each bridge, and the lane FLAGS any line naming `sorryAx`.
#
# Reads /work/proof only (its built lean-sail package); writes /work/bridges and
# lp1_harness/bridges_check.txt. Fetches nothing. Edits nothing under the cache.
# Expected wall clock: about a minute.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
S=$A/lp1_harness/leanpath_src
P=/work/proof
W=/work/bridges
OUT=$A/lp1_harness/bridges_check.txt
total=3
t0=$(date +%s)

echo "[1/$total] the working copy and the pinned toolchain  ($(( $(date +%s) - t0 ))s)"
[ -f "$S/Bridges.lean" ] || { echo "FLAG: $S/Bridges.lean is absent"; exit 3; }
[ -f "$S/Universal.lean" ] || { echo "FLAG: $S/Universal.lean is absent"; exit 3; }
SAILOLEAN=$(find $P/.lake/packages/Sail -name Common.olean -path '*/Sail/*' 2>/dev/null | head -1)
[ -n "$SAILOLEAN" ] || { echo "FLAG: no built lean-sail under $P/.lake/packages/Sail (lane l17 builds it)"; exit 3; }
SAILLIB=$(dirname "$(dirname "$SAILOLEAN")")
rm -rf $W; mkdir -p $W/build
cp $S/Universal.lean $S/Bridges.lean $W/
cp $P/lean-toolchain $W/lean-toolchain 2>/dev/null || cat $A/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/lean-toolchain > $W/lean-toolchain
cd $W
echo "  toolchain: $(cat lean-toolchain)   lean: $(lean --version 2>&1 | head -1)"
echo "  lean-sail: $SAILLIB   ($(git -C $P/.lake/packages/Sail rev-parse --short HEAD 2>&1))"
export LEAN_PATH=$W/build:$SAILLIB

echo "[2/$total] the module builds  ($(( $(date +%s) - t0 ))s)"
lean -o build/Universal.olean Universal.lean 2>&1 | tee $W/universal.log | head -20
[ -f build/Universal.olean ] || { echo "FLAG: Universal.lean did not build (this lane wrote none of it)"; exit 4; }
lean -o build/Bridges.olean Bridges.lean 2>&1 | tee $W/bridges.log | head -40
[ -f build/Bridges.olean ] || { echo "FLAG: Bridges.lean did not build; the log is $W/bridges.log"; exit 4; }
echo "  built. theorems in the file: $(grep -c '^theorem \|^@\[simp\] theorem ' Bridges.lean); bridges: $(grep -c '^theorem bridge_' Bridges.lean)"

echo "[3/$total] the transcriptions against the real package, and the axioms  ($(( $(date +%s) - t0 ))s)"
cat > Check.lean <<'LEAN'
import Sail.Common
import Sail.Sail
import Bridges

open Universal
open Universal.Bridges

section Faithful
variable {w n i : Nat}

example : @Sail.BitVec.length = @Sail'.length := rfl
example : @Sail.BitVec.toNatInt = @Sail'.toNatInt := rfl
example : @Sail.BitVec.signExtend = @Sail'.signExtend := rfl
example : @Sail.BitVec.zeroExtend = @Sail'.zeroExtend := rfl
example : @Sail.BitVec.truncate = @Sail'.truncate := rfl
example : @Sail.BitVec.extractLsb = @Sail'.extractLsb := rfl
example : @Sail.BitVec.updateSubrange' = @Sail'.updateSubrange' := rfl
example : @Sail.BitVec.updateSubrange = @Sail'.updateSubrange := rfl
example : @Sail.BitVec.access = @Sail'.access := rfl
example : @Sail.BitVec.addInt = @Sail'.addInt := rfl
example : @Sail.BitVec.subInt = @Sail'.subInt := rfl
example : @Sail.BitVec.countLeadingZeros = @Sail'.countLeadingZeros := rfl
example : @Sail.BitVec.countTrailingZeros = @Sail'.countTrailingZeros := rfl
example : @Sail.BitVec.update = @Sail'.update := rfl
example : @Sail.BitVec.join1 = @Sail'.join1 := rfl
example : @Sail.shift_bits_left = @Sail'.shift_bits_left := rfl
example : @Sail.shift_bits_right = @Sail'.shift_bits_right := rfl
example : @Sail.get_slice_int = @Sail'.get_slice_int := rfl

-- the three container declarations, the two shift instances and `^i` are
-- checked applied, at `Type`, which is where the emit uses them
example (v : Vector (BitVec 8) n) : Sail.Vector.length v = Sail'.Vector.length v := rfl
example (a : BitVec 8) : (Sail.vectorInit (n := n) a) = Sail'.vectorInit (n := n) a := rfl
example (v : Vector (BitVec 8) n) (a : BitVec 8) :
    Sail.vectorUpdate v i a = Sail'.vectorUpdate v i a := rfl
example (b : BitVec w) (k : Int) : b <<< k = Sail'.shiftLeftInt b k := rfl
example (b : BitVec w) (k : Int) : b >>> k = Sail'.shiftRightInt b k := rfl
example (x k : Int) : x ^ k = Sail'.ipow x k := rfl

-- the emit's own two rotates, from LeanIM/Prelude.lean
example (x : BitVec w) (s : Nat) :
    ((x >>> s) ||| (x <<< ((Sail.BitVec.length x) -i s))) = Emit'.rotater x s := rfl
example (x : BitVec w) (s : Nat) :
    ((x <<< s) ||| (x >>> ((Sail.BitVec.length x) -i s))) = Emit'.rotatel x s := rfl

end Faithful

#print axioms bridge_iadd
#print axioms bridge_isub
#print axioms bridge_imul
#print axioms bridge_ipow
#print axioms bridge_tdiv
#print axioms bridge_tmod
#print axioms bridge_ediv
#print axioms bridge_ediv_as_divF
#print axioms bridge_natAbs
#print axioms bridge_toInt
#print axioms bridge_toNatInt
#print axioms bridge_addInt
#print axioms bridge_subInt
#print axioms bridge_lt
#print axioms bridge_gt
#print axioms bridge_le
#print axioms bridge_ge
#print axioms bridge_get_slice_int
#print axioms bridge_and
#print axioms bridge_or
#print axioms bridge_xor
#print axioms bridge_shiftLeft
#print axioms bridge_shiftRight
#print axioms bridge_shift_bits_left
#print axioms bridge_shift_bits_right
#print axioms bridge_sshiftRight
#print axioms bridge_zeroExtend
#print axioms bridge_truncate
#print axioms bridge_signExtend
#print axioms bridge_length
#print axioms bridge_beq
#print axioms bridge_bne
#print axioms bridge_extractLsb
#print axioms bridge_append
#print axioms bridge_access
#print axioms bridge_updateSubrange
#print axioms bridge_update
#print axioms bridge_countLeadingZeros
#print axioms bridge_countTrailingZeros
#print axioms bridge_join1
#print axioms bridge_vector
#print axioms bridge_vectorUpdate
#print axioms bridge_vectorInit
#print axioms bridge_vectorLength
#print axioms bridge_rotater
#print axioms bridge_rotatel
#print axioms ediv_ne_fdiv
#print axioms ipow_neg
#print axioms truncate_eq_zeroExtend
#print axioms zeroExtend_drops
#print axioms vectorUpdate_out_of_range
LEAN
lean Check.lean > $W/check.log 2>&1
rc=$?
grep -E "error|sorryAx" $W/check.log | head -30
if [ $rc -ne 0 ]; then
  echo "FLAG: the faithfulness check did not compile -- a transcription has drifted from lean-sail, or the toolchain differs. The log is $W/check.log"
else
  echo "  every transcription is the package's own definition (all rfl)."
fi
if grep -q "sorryAx" $W/check.log; then echo "FLAG: a theorem rests on sorryAx"; fi
echo "  axioms used, over $(grep -c 'depends on axioms\|does not depend' $W/check.log) theorems:"
grep -o "\[.*\]" $W/check.log | sort | uniq -c | sed 's/^/    /'
{ echo "# bridges_check.txt -- lane lp3_l90, $(date -u +%Y-%m-%dT%H:%MZ)"
  echo "# toolchain $(cat $W/lean-toolchain), lean-sail $(git -C $P/.lake/packages/Sail rev-parse --short HEAD 2>&1)"
  cat $W/check.log ; } > $OUT
echo "  written: $OUT"
echo done
