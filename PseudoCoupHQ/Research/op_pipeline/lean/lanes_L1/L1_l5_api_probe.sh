#!/bin/bash
# L1 lane 5 — pin down the two toolchains this task writes against, before it
# generates anything:
#   [1/2] z3 in the image, and whether z3's own printer round-trips the
#         printed layer-5 form (the check that will confirm term_to_lean.py's
#         parse is z3's reading and not a lookalike)
#   [2/2] the exact Lean 4.24 BitVec names: extractLsb, append, zeroExtend,
#         signExtend, sle/ule/slt/ult, sshiftRight', sdiv/srem, udiv-by-zero,
#         and whether `if` on a Bool condition survives bv_decide
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"

echo '[1/2] z3 in the image'
python3 - <<'PY'
try:
    import z3
    print("z3 version:", z3.get_version_string())
except Exception as e:
    print("z3 IMPORT FAILED:", e)
    raise SystemExit(0)

# Does z3's own printer reproduce these exact strings? If it does, a parser
# that agrees with z3 can be confirmed by round-trip rather than trusted.
v0 = z3.BitVec("v0", 64)
v1 = z3.BitVec("v1", 64)
samples = [
    z3.If(v0 == v1, z3.BitVecVal(0, 8), z3.BitVecVal(1, 8))
      | z3.If(z3.BitVecVal(0, 64) <= v0, z3.BitVecVal(0, 8), z3.BitVecVal(1, 8)),
    z3.If(z3.Concat(z3.BitVecVal(0, 32), z3.Extract(31, 0, v0)) == v1,
          z3.BitVecVal(1, 8), z3.BitVecVal(0, 8)),
    ~(z3.If(v0 == v1, z3.BitVecVal(254, 8), z3.BitVecVal(255, 8))
      | z3.If(z3.BitVecVal(0, 64) <= v0, z3.BitVecVal(254, 8), z3.BitVecVal(255, 8))),
    z3.Extract(31, 0, v0) * z3.Extract(31, 0, v1),
    z3.UDiv(v0, v1),
    v0 / v1,
    z3.URem(v0, v1),
    z3.SRem(v0, v1),
    z3.LShR(v0, v1),
    v0 >> v1,
    v0 << v1,
    z3.ULE(v0, v1),
]
for s in samples:
    print("  %s" % s)
PY
echo "--- z3 probe exit $?"

echo '[2/2] the Lean 4.24 BitVec names this task will emit'
mkdir -p "$LEANDIR/archproof/Archproof"
cat > "$LEANDIR/archproof/Archproof/Api.lean" <<'LEAN'
import Std.Tactic.BVDecide

-- Every name term_to_lean.py intends to emit, checked for existence and type
-- rather than assumed from memory.
section Names
variable (x y : BitVec 64) (a b : BitVec 32) (c : BitVec 1)
#check (x + y : BitVec 64)
#check (x * y : BitVec 64)
#check (x - y : BitVec 64)
#check (x &&& y : BitVec 64)
#check (x ||| y : BitVec 64)
#check (x ^^^ y : BitVec 64)
#check (~~~x : BitVec 64)
#check (x <<< y : BitVec 64)
#check (x >>> y : BitVec 64)
#check (BitVec.sshiftRight' x y : BitVec 64)
#check (x / y : BitVec 64)
#check (x % y : BitVec 64)
#check (BitVec.sdiv x y : BitVec 64)
#check (BitVec.srem x y : BitVec 64)
#check (BitVec.smod x y : BitVec 64)
#check (x.extractLsb 31 0 : BitVec 32)
#check (BitVec.extractLsb 31 0 x : BitVec 32)
#check (a ++ b : BitVec 64)
#check (a.zeroExtend 64 : BitVec 64)
#check (a.signExtend 64 : BitVec 64)
#check (a.setWidth 64 : BitVec 64)
#check (BitVec.sle x y : Bool)
#check (BitVec.slt x y : Bool)
#check (BitVec.ule x y : Bool)
#check (BitVec.ult x y : Bool)
#check (x == y : Bool)
#check ((5#32) : BitVec 32)
#check (if x = y then a else b)
#check (if (x == y) = true then a else b)
#check (bif (x == y) then a else b)
end Names

-- Lean's own udiv at a zero divisor, against SMT-LIB's bvudiv (all ones).
-- This is the semantic seam between z3's answer and Lean's, and it must be
-- measured rather than assumed.
#eval ((7#8) / (0#8))
#eval ((7#8) % (0#8))
#eval (BitVec.sdiv (7#8) (0#8))
#eval (BitVec.srem (7#8) (0#8))
#eval ((1#8) <<< (200#8))
#eval (BitVec.sshiftRight' (128#8) (200#8))
#eval ((128#8) >>> (200#8))

-- Does bv_decide close a goal whose condition is a Bool `if`?
theorem api_if_bool (x y : BitVec 8) :
    (if (x == y) = true then (1#8) else (0#8))
      = (if (y == x) = true then (1#8) else (0#8)) := by
  bv_decide

-- Does bv_decide close a goal carrying extract, concat and a signed compare?
theorem api_mixed (v0 v1 : BitVec 64) :
    (if ((v0.extractLsb 31 0 ++ (0#32)) == v1) = true then (1#8) else (0#8))
      = (if (v1 == (v0.extractLsb 31 0 ++ (0#32))) = true then (1#8) else (0#8)) := by
  bv_decide

-- Does bv_decide reach unsigned division at all?
theorem api_udiv (v0 : BitVec 8) : v0 / (1#8) = v0 := by
  bv_decide
LEAN
cat > "$LEANDIR/archproof/Archproof.lean" <<'LEAN'
import Archproof.Basic
import Archproof.Smoke
import Archproof.Api
LEAN
cd "$LEANDIR/archproof" || exit 1
time lake build
echo "--- lake build exit $?"
