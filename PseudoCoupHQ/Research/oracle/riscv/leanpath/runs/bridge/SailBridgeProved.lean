-- GENERATED, and every lemma below was PUT TO LEAN and carried.
-- The tactic beside each is the one that actually proved it.
import LeanIM

-- proved by: rfl
theorem sail_bridge_zopz0zI_s {n : Nat} (x y : BitVec n) :
    zopz0zI_s x y = BitVec.slt x y := by
  rfl

-- proved by: simp [%(def)s, %(conv)s, %(target)s]
theorem sail_bridge_zopz0zI_u {n : Nat} (x y : BitVec n) :
    zopz0zI_u x y = BitVec.ult x y := by
  simp [zopz0zI_u, BitVec.toNatInt, BitVec.ult]

-- proved by: rfl
theorem sail_bridge_zopz0zIzJ_s {n : Nat} (x y : BitVec n) :
    zopz0zIzJ_s x y = BitVec.sle x y := by
  rfl

-- proved by: simp [%(def)s, %(conv)s, %(target)s]
theorem sail_bridge_zopz0zIzJ_u {n : Nat} (x y : BitVec n) :
    zopz0zIzJ_u x y = BitVec.ule x y := by
  simp [zopz0zIzJ_u, BitVec.toNatInt, BitVec.ule]

-- proved by: rfl
theorem sail_bridge_zopz0zK_s {n : Nat} (x y : BitVec n) :
    zopz0zK_s x y = BitVec.slt y x := by
  rfl

-- proved by: simp [%(def)s, %(conv)s, %(target)s]
theorem sail_bridge_zopz0zK_u {n : Nat} (x y : BitVec n) :
    zopz0zK_u x y = BitVec.ult y x := by
  simp [zopz0zK_u, BitVec.toNatInt, BitVec.ult]

-- proved by: rfl
theorem sail_bridge_zopz0zKzJ_s {n : Nat} (x y : BitVec n) :
    zopz0zKzJ_s x y = BitVec.sle y x := by
  rfl

-- proved by: simp [%(def)s, %(conv)s, %(target)s]
theorem sail_bridge_zopz0zKzJ_u {n : Nat} (x y : BitVec n) :
    zopz0zKzJ_u x y = BitVec.ule y x := by
  simp [zopz0zKzJ_u, BitVec.toNatInt, BitVec.ule]
