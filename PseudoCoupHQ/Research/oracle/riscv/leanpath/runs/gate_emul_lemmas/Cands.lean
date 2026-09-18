import Std.Tactic.BVDecide
set_option linter.unusedSimpArgs false

-- the emit's own shape: Prelude.lean:263 and RegType.lean:215
def zeros {n : Nat} : BitVec n := BitVec.zero n
def zero_reg : BitVec 64 := zeros (n := 64)

-- Z0 BASELINE, the set the gate generates today
theorem z0 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros]
  all_goals bv_decide
-- Z1 candidate: BitVec.zero_eq
theorem z1 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros, BitVec.zero_eq]
  all_goals bv_decide
-- Z2 candidate: unfold BitVec.zero by name
theorem z2 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros, BitVec.zero]
  all_goals bv_decide
-- Z3 candidate: BitVec.ofNat_eq_ofNat
theorem z3 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros, BitVec.ofNat_eq_ofNat]
  all_goals bv_decide
-- Z4 the bare normalisation the whole thing turns on
theorem z4 : (BitVec.zero 64) = 0#64 := by
  simp only [BitVec.zero_eq]
-- Z5 bv_decide with no help at all
theorem z5 : (BitVec.zero 64) = 0#64 := by
  bv_decide

-- U0 ONE UNKNOWN NAME in a set that would otherwise fire
theorem u0 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros, BitVec.zero_eq, BitVec.this_name_does_not_exist]
  all_goals bv_decide

-- S0 a shift by a Nat that came from a BitVec: already in the fragment?
theorem s0 (a b : BitVec 64) : a.sshiftRight b.toNat = a.sshiftRight' b := by
  all_goals bv_decide
-- S1 the emit's own shape: the Nat came from an Int (Prelude.lean:414)
theorem s1 (a b : BitVec 64) : a.sshiftRight ((b.toNat : Int)).toNat = a.sshiftRight' b := by
  all_goals bv_decide
-- S2 the same with Int.toNat_natCast
theorem s2 (a b : BitVec 64) : a.sshiftRight ((b.toNat : Int)).toNat = a.sshiftRight' b := by
  try simp only [Int.toNat_natCast]
  all_goals bv_decide
-- S3 the au_445 shape: a 32-bit arithmetic shift by an Int-derived Nat
theorem s3 (a b : BitVec 64) :
    (BitVec.extractLsb' 0 32 a).sshiftRight (((BitVec.extractLsb' 0 5 b).toNat : Int)).toNat
      = (BitVec.extractLsb' 0 32 a).sshiftRight' (BitVec.extractLsb' 0 5 b) := by
  try simp only [Int.toNat_natCast]
  all_goals bv_decide

-- A STAND-IN, not lean-sail. Its body is stated here and is an ASSUMPTION
-- about Sail.BitVec.toNatInt, not a reading of it: the package is not present.
def toNatIntStandIn {n : Nat} (x : BitVec n) : Int := (x.toNat : Int)
def ltbStandIn (x y : Int) : Bool := decide (x < y)
-- I0 the au_319 shape, baseline
theorem i0 (x y : BitVec 64) :
    (match ltbStandIn (toNatIntStandIn x) (toNatIntStandIn y) with | true => 1#1 | false => 0#1)
      = (match x.ult y with | true => 1#1 | false => 0#1) := by
  all_goals bv_decide
-- I1 the OUTWARD bridge: unfold BitVec.ult into Nat
theorem i1 (x y : BitVec 64) :
    (match ltbStandIn (toNatIntStandIn x) (toNatIntStandIn y) with | true => 1#1 | false => 0#1)
      = (match x.ult y with | true => 1#1 | false => 0#1) := by
  try simp only [toNatIntStandIn, ltbStandIn, Int.ofNat_lt, BitVec.ult]
  all_goals bv_decide
-- I2 the INWARD bridge: rewrite the Int comparison back towards BitVec
theorem i2 (x y : BitVec 64) :
    (match ltbStandIn (toNatIntStandIn x) (toNatIntStandIn y) with | true => 1#1 | false => 0#1)
      = (match x.ult y with | true => 1#1 | false => 0#1) := by
  try simp only [toNatIntStandIn, ltbStandIn, Int.ofNat_lt, ← BitVec.lt_def, BitVec.ult_iff_lt]
  all_goals bv_decide

-- DOES THE PROPOSED ADDITION HARM WHAT ALREADY PROVES?
-- H0 a goal bv_decide proves natively, untouched
theorem h0 (x y : BitVec 64) : (x.ult y || x == y) = x.ule y := by
  all_goals bv_decide
-- H1 the same goal with the OUTWARD bridge added
theorem h1 (x y : BitVec 64) : (x.ult y || x == y) = x.ule y := by
  try simp only [BitVec.ult]
  all_goals bv_decide
-- H2 the same goal with the INWARD set this run proposes
theorem h2 (x y : BitVec 64) : (x.ult y || x == y) = x.ule y := by
  try simp only [BitVec.zero_eq, Int.toNat_natCast, Int.ofNat_lt, ← BitVec.lt_def, BitVec.ult_iff_lt]
  all_goals bv_decide
-- H3 plain arithmetic with the same set
theorem h3 (x y : BitVec 64) : (x + y) - y = x := by
  try simp only [BitVec.zero_eq, Int.toNat_natCast, Int.ofNat_lt, ← BitVec.lt_def, BitVec.ult_iff_lt]
  all_goals bv_decide
