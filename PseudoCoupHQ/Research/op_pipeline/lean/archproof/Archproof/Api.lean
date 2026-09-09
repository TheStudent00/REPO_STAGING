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
