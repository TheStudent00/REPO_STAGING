/-
  Bridges.lean -- one PROVED statement per primitive the Sail RISC-V model
  bottoms out in, saying that the primitive IS its counterpart in the
  universal type of `Universal.lean`.

  The inventory of primitives is log 289 §2.1 (22 fixed-width value
  operations), §2.2 (17 unbounded number operations) and §2.3 (5 container
  operations) -- 44 in all, counted from the 354 `execute` clauses of the
  emit at
  `cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM/`.

  ## how a primitive gets into this file

  Exactly as `Universal.sailToBitsTruncate` does it: Sail's own definition
  is TRANSCRIBED here, verbatim, from the pinned library, so that this
  module imports the universal type and nothing else and builds whether or
  not the model is built. The transcriptions live in `Sail'` below and each
  one carries its source line. The library is

      lean-sail, rev `v5` (the rev `lakefile.toml` of the emit pins),
      file `Sail/Common.lean`, toolchain `leanprover/lean4:v4.29.0`.

  A transcription is only as good as its faithfulness, so every one of them
  is checked mechanically against the library's own text: for each,

      example : @Sail.BitVec.extractLsb = @Universal.Bridges.Sail'.extractLsb := rfl

  compiled against the REAL package. A transcription that has drifted fails
  that check, loudly, and no theorem in this file is then worth anything.

  Where that stands, 2026-09-15: all 26 of those checks pass, and this file
  builds with no error and no warning, on the laptop under
  `leanprover/lean4:v4.30.0` with lean-sail `v5` compiled there from its own
  sources (the whole package builds clean under 4.30 as well). The lane
  `lanes_lp1/lp3_l90_bridges_over_the_universal_type.sh` repeats both under
  the PINNED `leanprover/lean4:v4.29.0` and the lean-sail already built inside
  `/work/proof`, and prints `#print axioms` for every bridge.

  ## the form of a bridge

  For a fixed-width primitive the universal side is the SPECIFICATION and
  the width is explicit -- a bit operation has no meaning without one:

      (x &&& y) = Uni.bitsAt w (Uni.band w (Uni.ofBitsU x) (Uni.ofBitsU y))

  For an unbounded primitive it is stated over `Int` through `Uni.ofInt`.
  Where a primitive only agrees with its counterpart under a side condition
  the condition is a hypothesis of the theorem, never a weakening of it.

  ## what is NOT here

  `untilFuelM` (log 289 §2.3, 3 uses) is a bounded monadic loop over an
  arbitrary monad. The universal type is one number; it has no loop, so
  there is no counterpart to state a bridge against. It is reported as
  unbridged rather than given a vacuous theorem.

  Nothing in this file is keyed by an instruction name or an operator token.
  Nothing here is left unfinished, nothing is admitted, no proof is by
  evaluation outside the kernel, and no axiom of ours is declared: the lane
  prints `#print axioms` for every bridge and the answer is Lean's own three
  (propext, Quot.sound, Classical.choice) and nothing else.
-/

import Universal

namespace Universal
namespace Bridges

open Uni

/-! # 0. Sail's primitives, transcribed

Verbatim from lean-sail `v5`, `Sail/Common.lean`, with only the namespace
changed (`Sail.BitVec.f` becomes `Sail'.f`) and the `simp_sail` attribute
dropped, that attribute being declared in `Sail/Attr.lean` which this module
does not import. Line numbers are that file's. -/

namespace Sail'

/-- `Sail/Common.lean:19` -/
abbrev length {w : Nat} (_ : BitVec w) : Nat := w

/-- `Sail/Common.lean:22` -/
def toNatInt {w : Nat} (x : BitVec w) : Int :=
  Int.ofNat x.toNat

/-- `Sail/Common.lean:26` -/
def signExtend {w : Nat} (x : BitVec w) (w' : Nat) : BitVec w' :=
  x.signExtend w'

/-- `Sail/Common.lean:30` -/
def zeroExtend {w : Nat} (x : BitVec w) (w' : Nat) : BitVec w' :=
  x.zeroExtend w'

/-- `Sail/Common.lean:34` -/
def truncate {w : Nat} (x : BitVec w) (w' : Nat) : BitVec w' :=
  x.truncate w'

/-- `Sail/Common.lean:42` -/
def extractLsb {w : Nat} (x : BitVec w) (hi lo : Nat) : BitVec (hi - lo + 1) :=
  x.extractLsb hi lo

/-- `Sail/Common.lean:46` -/
def updateSubrange' {w : Nat} (x : BitVec w) (start len : Nat) (y : BitVec len) : BitVec w :=
  let mask := ~~~(((BitVec.allOnes len).zeroExtend w) <<< start)
  let y' := ((y.zeroExtend w) <<< start)
  (mask &&& x) ||| y'

/-- `Sail/Common.lean:64` -/
def updateSubrange {w : Nat} (x : BitVec w) (hi lo : Nat) (y : BitVec (hi - lo + 1)) : BitVec w :=
  updateSubrange' x lo _ y

/-- `Sail/Common.lean:75` -/
def access {w : Nat} (x : BitVec w) (i : Nat) : BitVec 1 :=
  BitVec.ofBool x[i]!

/-- `Sail/Common.lean:83` -/
def addInt {w : Nat} (x : BitVec w) (i : Int) : BitVec w :=
  x + BitVec.ofInt w i

/-- `Sail/Common.lean:87` -/
def subInt {w : Nat} (x : BitVec w) (i : Int) : BitVec w :=
  x - BitVec.ofInt w i

/-- `Sail/Common.lean:91` -/
def countLeadingZeros {w : Nat} (x : BitVec w) : Nat := x.clz.toNat

/-- `Sail/Common.lean:94` -/
def countTrailingZeros {w : Nat} (x : BitVec w) : Nat :=
  countLeadingZeros (x.reverse)

/-- `Sail/Common.lean:103` -/
def update {m : Nat} (x : BitVec m) (n : Nat) (b : BitVec 1) := updateSubrange' x n _ b

/-- `Sail/Common.lean:118` -/
def join1 (xs : List (BitVec 1)) : BitVec xs.length :=
  (BitVec.ofBoolListBE (xs.map fun x => x[0])).cast (by simp)

/-- `Sail/Common.lean:185` -/
def shift_bits_left {n m : Nat} (bv : BitVec n) (sh : BitVec m) : BitVec n :=
  bv <<< sh

/-- `Sail/Common.lean:189` -/
def shift_bits_right {n m : Nat} (bv : BitVec n) (sh : BitVec m) : BitVec n :=
  bv >>> sh

/-- `Sail/Common.lean:251` -/
def get_slice_int (len : Nat) (n : Int) (lo : Nat) : BitVec len :=
  BitVec.extractLsb' lo len (BitVec.ofInt (lo + len + 1) n)

/-- `Sail/Common.lean:265` -/
abbrev Vector.length {α : Type} {n : Nat} (_v : Vector α n) : Nat := n

/-- `Sail/Common.lean:268` -/
def vectorInit {α : Type} {n : Nat} (a : α) : Vector α n := Vector.replicate n a

/-- `Sail/Common.lean:271` -/
def vectorUpdate {α : Type} {m : Nat} (v : Vector α m) (n : Nat) (a : α) := v.set! n a

/-- `Sail/Common.lean:274`, the `HShiftLeft (BitVec w) Int` instance's field,
written as a function so that transcribing it declares no instance. -/
def shiftLeftInt {w : Nat} (b : BitVec w) (i : Int) : BitVec w :=
  match i with
  | .ofNat n => BitVec.shiftLeft b n
  | .negSucc n => BitVec.ushiftRight b (n + 1)

/-- `Sail/Common.lean:281`, the `HShiftRight (BitVec w) Int` instance's field. -/
def shiftRightInt {w : Nat} (b : BitVec w) (i : Int) : BitVec w :=
  shiftLeftInt b (-i)

/-- `Sail/Sail.lean:117`, the `^i` of log 289 §2.2: Sail's own `HPow Int Int Int`.
A NEGATIVE exponent is `Int.toNat`-ed to `0`, so `a ^i (-1) = 1`. -/
def ipow (x n : Int) : Int := x ^ n.toNat

end Sail'

/-! # 1. the universal counterparts that `Universal.lean` does not carry

Each is written from the universal object alone -- its unsigned or signed
reading at a width, its mantissa, its exponent -- or from the exact
operations `Universal.lean` already has (`band`, `bor`, `bnot`, `shl`,
`add`, `scale`). None of them mentions a Sail function, so no bridge below
is true by construction. -/

namespace Uni

/-- the low `hi .. lo` bits of the object read at width `w`. -/
def extract (w hi lo : Nat) (u : Uni) : Uni :=
  ofInt ((((bitsAt w u).toNat / 2 ^ lo) % 2 ^ (hi - lo + 1) : Nat) : Int)

/-- the `len` bits from `lo` up, as a mask: `(2^len - 1) * 2^lo`. -/
def maskAt (len lo : Nat) : Uni := ofInt (((2 ^ len - 1) * 2 ^ lo : Nat) : Int)

/-- write the `len` bits from `lo` up of `u` with the low `len` bits of `v`:
clear them with the mask, then place the value. -/
def depositAt (w len lo : Nat) (u v : Uni) : Uni :=
  bor w (band w u (bnot w (maskAt len lo))) (shl (ofBitsU (bitsAt len v)) lo)

/-- write bits `hi .. lo` of `u` with the low `hi - lo + 1` bits of `v`. -/
def deposit (w hi lo : Nat) (u v : Uni) : Uni := depositAt w (hi - lo + 1) lo u v

/-- bit `i` of the object read at width `w`, as a 1-bit object. -/
def bitAt (w i : Nat) (u : Uni) : Uni :=
  ofInt ((((bitsAt w u).toNat / 2 ^ i) % 2 : Nat) : Int)

/-- two objects end to end: `x` above, `y` below, at their two widths. -/
def cat (wx wy : Nat) (x y : Uni) : Uni :=
  ofInt (((bitsAt wx x).toNat * 2 ^ wy + (bitsAt wy y).toNat : Nat) : Int)

/-- widen by the unsigned reading: the object IS the number, so a zero
extension is a re-read at the new width. -/
def zext (w : Nat) (u : Uni) : Uni := ofBitsU (bitsAt w u)

/-- widen by the signed reading. -/
def sext (w : Nat) (u : Uni) : Uni := ofBitsS (bitsAt w u)

/-- shift left by a VALUE, the value read unsigned at its own width. -/
def shlV (wk : Nat) (u k : Uni) : Uni := shl u (bitsAt wk k).toNat

/-- shift right by a value, logically. -/
def shrV (w wk : Nat) (u k : Uni) : Uni := shrL w u (bitsAt wk k).toNat

/-- rotate right at width `w` by `k`: the low `k` bits come back on top. -/
def rotR (w k : Nat) (u : Uni) : Uni := bor w (shrL w u k) (shl u (w - k))

/-- rotate left at width `w` by `k`. -/
def rotL (w k : Nat) (u : Uni) : Uni := bor w (shl u k) (shrL w u (w - k))

/-- the zeros above the leading one at width `w`. `Ubv.len` is the universal
type's own "how many bits this magnitude occupies". -/
def clzU (w : Nat) (u : Uni) : Nat := w - Ubv.len (bitsAt w u).toNat

/-- how many times 2 divides `v`: the exponent the universal object would
carry if its mantissa were made odd. `0` for an odd `v`, and for `v = 0`. -/
def twoAdic (v : Nat) : Nat :=
  if h : v = 0 ∨ v % 2 = 1 then 0 else twoAdic (v / 2) + 1
decreasing_by
  have hv : v ≠ 0 := fun hz => h (Or.inl hz)
  exact Nat.div_lt_self (Nat.pos_of_ne_zero hv) (by omega)

/-- the zeros below the lowest one at width `w`: `w` when there is no one,
else the exponent of the lowest set bit. -/
def ctzU (w : Nat) (u : Uni) : Nat :=
  let v := (bitsAt w u).toNat
  if v = 0 then w else twoAdic v

/-- the value of a list of single-bit objects, most significant first. -/
def joinBE : List Uni → Int
  | [] => 0
  | b :: bs => (b.toInt % 2) * 2 ^ bs.length + joinBE bs

/-- single bits joined most significant first. -/
def joinBits (xs : List Uni) : Uni := ofInt (joinBE xs)

/-- the power: an exponent is repeated multiplication, exact. -/
def pow (u : Uni) (n : Nat) : Uni := ofSignedAt (u.smant ^ n) (u.e * n)

/-- flooring division, the counterpart of `Int.fdiv`. -/
def divF (x y : Uni) : Uni := let (a, b, _) := alignPair x y; ofInt (Int.fdiv a b)

/-- Euclidean division, the counterpart of `Int.ediv` (Lean's `/` on `Int`). -/
def divE (x y : Uni) : Uni := let (a, b, _) := alignPair x y; ofInt (a / b)

/-- `len` bits of an unbounded number from bit `lo` up. -/
def sliceInt (len : Nat) (u : Uni) (lo : Nat) : Uni :=
  ofInt (u.toInt / 2 ^ lo % 2 ^ len)

/-! ## the container form

A container is outside the universal object (log 289 §3.4), so its
counterpart is a container OF universal objects together with the two
readings that carry a container across. -/

/-- every element read into the universal type. -/
def ofVecBits {w n : Nat} (v : Vector (BitVec w) n) : Vector Uni n := v.map ofBitsU

/-- every element read back out at width `w`. -/
def toVecBits (w : Nat) {n : Nat} (v : Vector Uni n) : Vector (BitVec w) n := v.map (bitsAt w)

/-- write one element, pointwise. -/
def vecSet {n : Nat} (v : Vector Uni n) (i : Nat) (a : Uni) : Vector Uni n :=
  Vector.ofFn (fun j => if (j : Nat) = i then a else v[j])

/-- a container with every element the same, pointwise. -/
def vecConst (n : Nat) (a : Uni) : Vector Uni n := Vector.ofFn (fun _ => a)

end Uni

/-! # 2. the workhorse lemmas

Everything below rests on these: an object built by `ofInt` reports that
integer back, and reading a fixed-width value into the universal type and
out again at the same width is the identity. -/

@[simp] theorem e_ofInt (n : Int) : (Uni.ofInt n).e = 0 := by
  simp [Uni.ofInt, Uni.ofSignedAt, Uni.mk', Uni.e, Expo.ofInt, Expo.val]

@[simp] theorem smant_ofInt (n : Int) : (Uni.ofInt n).smant = n := by
  simp [Uni.ofInt, Uni.ofSignedAt, Uni.mk', Uni.smant, Uni.isNeg]
  split <;> omega

@[simp] theorem mant_ofInt (n : Int) : (Uni.ofInt n).mant = n.natAbs := rfl

@[simp] theorem toInt_ofInt (n : Int) : (Uni.ofInt n).toInt = n := by
  simp [Uni.toInt]

@[simp] theorem smant_ofSignedAt (m k : Int) : (Uni.ofSignedAt m k).smant = m := by
  simp [Uni.ofSignedAt, Uni.mk', Uni.smant, Uni.isNeg]
  split <;> omega

@[simp] theorem e_ofSignedAt (m k : Int) : (Uni.ofSignedAt m k).e = k := by
  simp [Uni.ofSignedAt, Uni.mk', Uni.e, Expo.ofInt, Expo.val]
  split <;> omega

theorem toInt_ofSignedAt (m : Int) (k : Nat) :
    (Uni.ofSignedAt m (k : Int)).toInt = m * 2 ^ k := by
  simp [Uni.toInt]

theorem toInt_ofSignedAt_zero (m : Int) : (Uni.ofSignedAt m 0).toInt = m := by
  simp [Uni.toInt]

theorem ofInt_natCast (w n : Nat) : BitVec.ofInt w (n : Int) = BitVec.ofNat w n := by
  apply BitVec.eq_of_toNat_eq
  rw [BitVec.toNat_ofInt, BitVec.toNat_ofNat, ← Int.natCast_emod, Int.toNat_natCast]

@[simp] theorem bitsAt_ofInt (w : Nat) (n : Int) :
    Uni.bitsAt w (Uni.ofInt n) = BitVec.ofInt w n := by
  simp [Uni.bitsAt]

theorem bitsAt_ofNat (w n : Nat) :
    Uni.bitsAt w (Uni.ofInt (n : Int)) = BitVec.ofNat w n := by
  simp

/-- the round trip: a value read into the universal type and back out at the
same width is that value. -/
@[simp] theorem bitsAt_ofBitsU {w : Nat} (b : BitVec w) :
    Uni.bitsAt w (Uni.ofBitsU b) = b := by
  simp [Uni.ofBitsU]

@[simp] theorem bitsAt_ofBitsS {w : Nat} (b : BitVec w) :
    Uni.bitsAt w (Uni.ofBitsS b) = b := by
  simp [Uni.ofBitsS]

@[simp] theorem toInt_ofBitsU {w : Nat} (b : BitVec w) :
    (Uni.ofBitsU b).toInt = (b.toNat : Int) := by
  simp [Uni.ofBitsU]

@[simp] theorem e_ofBitsU {w : Nat} (b : BitVec w) : (Uni.ofBitsU b).e = 0 := by
  simp [Uni.ofBitsU]

@[simp] theorem smant_ofBitsU {w : Nat} (b : BitVec w) :
    (Uni.ofBitsU b).smant = (b.toNat : Int) := by
  simp [Uni.ofBitsU]

@[simp] theorem toInt_ofBitsS {w : Nat} (b : BitVec w) :
    (Uni.ofBitsS b).toInt = b.toInt := by
  simp [Uni.ofBitsS]

@[simp] theorem alignPair_ofInt (a b : Int) :
    Uni.alignPair (Uni.ofInt a) (Uni.ofInt b) = (a, b, 0) := by
  simp [Uni.alignPair, imin]

theorem bitsAt_shl_ofBitsU {w wx : Nat} (x : BitVec wx) (k : Nat) :
    Uni.bitsAt w (Uni.shl (Uni.ofBitsU x) k) = BitVec.ofNat w (x.toNat * 2 ^ k) := by
  rw [Uni.shl, Uni.scale, Uni.bitsAt]
  simp only [e_ofBitsU, smant_ofBitsU, Int.zero_add, toInt_ofSignedAt]
  rw [show ((x.toNat : Int) * 2 ^ k) = ((x.toNat * 2 ^ k : Nat) : Int) by push_cast; rfl,
      ofInt_natCast]

/-! # 3. the bridges -/

/-! ## 3.1 the unbounded number operations -- log 289 §2.2

Seventeen primitives, stated over `Int` through `Uni.ofInt`. The universal
object of an integer is the integer at exponent zero, so each of these says
that Sail's operation on numbers is the universal exact operation read back
out with `Uni.toInt`. -/

/-- `+i` (119 uses). -/
theorem bridge_iadd (a b : Int) : a + b = (Uni.add (Uni.ofInt a) (Uni.ofInt b)).toInt := by
  simp [Uni.add, toInt_ofSignedAt_zero]

/-- `-i` (233 uses). -/
theorem bridge_isub (a b : Int) : a - b = (Uni.sub (Uni.ofInt a) (Uni.ofInt b)).toInt := by
  simp [Uni.sub, toInt_ofSignedAt_zero]

/-- `*i` (116 uses). -/
theorem bridge_imul (a b : Int) : a * b = (Uni.mul (Uni.ofInt a) (Uni.ofInt b)).toInt := by
  simp [Uni.mul, toInt_ofSignedAt_zero]

/-- `^i` (54 uses). The exponent reaches the universal side as `Int.toNat`
because that is what Sail's own `HPow Int Int Int` does with it; see
`ipow_neg_is_one` below for what that costs. -/
theorem bridge_ipow (a n : Int) : Sail'.ipow a n = (Uni.pow (Uni.ofInt a) n.toNat).toInt := by
  simp [Sail'.ipow, Uni.pow, toInt_ofSignedAt_zero]

/-- `Int.tdiv` (42 uses), a zero divisor included: both sides answer `0`. -/
theorem bridge_tdiv (a b : Int) : Int.tdiv a b = (Uni.divT (Uni.ofInt a) (Uni.ofInt b)).toInt := by
  simp [Uni.divT]

/-- `Int.tmod` (24 uses). -/
theorem bridge_tmod (a b : Int) : Int.tmod a b = (Uni.remT (Uni.ofInt a) (Uni.ofInt b)).toInt := by
  simp [Uni.remT, toInt_ofSignedAt_zero]

/-- `Int.ediv` (2 uses). Lean's `/` on `Int` IS `Int.ediv`, so the universal
counterpart is `divE` and the bridge holds for every divisor. -/
theorem bridge_ediv (a b : Int) : a / b = (Uni.divE (Uni.ofInt a) (Uni.ofInt b)).toInt := by
  simp [Uni.divE]

/-- the SAME primitive against a FLOORING counterpart, which needs the
divisor nonnegative. Log 289 §2.2 calls `Int.ediv` "divide, flooring"; that
reading is only true on a nonnegative divisor, and `ediv_ne_fdiv` below is
the counterexample. -/
theorem bridge_ediv_as_divF (a b : Int) (hb : 0 ≤ b) :
    a / b = (Uni.divF (Uni.ofInt a) (Uni.ofInt b)).toInt := by
  simp [Uni.divF, Int.fdiv_eq_ediv_of_nonneg a hb]

/-- `Int.natAbs` (3 uses) IS the universal mantissa: the magnitude the sign
was taken off. -/
theorem bridge_natAbs (a : Int) : a.natAbs = (Uni.ofInt a).mant := rfl

/-- `BitVec.toInt` (36 uses) IS the universal signed reading. -/
theorem bridge_toInt {w : Nat} (x : BitVec w) : x.toInt = (Uni.ofBitsS x).toInt := by
  simp

/-- `BitVec.toNatInt` (112 uses) IS the universal unsigned reading. -/
theorem bridge_toNatInt {w : Nat} (x : BitVec w) : Sail'.toNatInt x = (Uni.ofBitsU x).toInt := by
  simp [Sail'.toNatInt]

/-- `BitVec.addInt` (19 uses): the exact sum, projected back at the width. -/
theorem bridge_addInt {w : Nat} (x : BitVec w) (i : Int) :
    Sail'.addInt x i = Uni.bitsAt w (Uni.add (Uni.ofBitsU x) (Uni.ofInt i)) := by
  simp [Sail'.addInt, Uni.add, Uni.alignPair, imin, toInt_ofSignedAt_zero, Uni.bitsAt,
        BitVec.ofInt_add]

/-- `BitVec.subInt` (7 uses). -/
theorem bridge_subInt {w : Nat} (x : BitVec w) (i : Int) :
    Sail'.subInt x i = Uni.bitsAt w (Uni.sub (Uni.ofBitsU x) (Uni.ofInt i)) := by
  simp [Sail'.subInt, Uni.sub, Uni.alignPair, imin, toInt_ofSignedAt_zero, Uni.bitsAt,
        Int.sub_eq_add_neg, BitVec.ofInt_add, BitVec.ofInt_neg, BitVec.sub_eq_add_neg]

/-- `<b` (65 uses). -/
theorem bridge_lt (a b : Int) :
    decide (a < b) = (Uni.cmp (Uni.ofInt a) (Uni.ofInt b)).isLT := by
  simp only [Uni.cmp, alignPair_ofInt]
  rw [Bool.eq_iff_iff]
  simp [Ordering.isLT_iff_eq_lt, Int.compare_eq_lt]

/-- `>b` (61 uses). -/
theorem bridge_gt (a b : Int) :
    decide (a > b) = (Uni.cmp (Uni.ofInt a) (Uni.ofInt b)).isGT := by
  simp only [Uni.cmp, alignPair_ofInt]
  rw [Bool.eq_iff_iff]
  simp [Ordering.isGT_iff_eq_gt, Int.compare_eq_gt]

/-- `≤b` (86 uses): not greater. -/
theorem bridge_le (a b : Int) :
    decide (a ≤ b) = (Uni.cmp (Uni.ofInt a) (Uni.ofInt b)).isLE := by
  simp only [Uni.cmp, alignPair_ofInt]
  rw [Bool.eq_iff_iff]
  simp [Ordering.isLE_iff_ne_gt, Int.compare_eq_gt]
  all_goals omega

/-- `≥b` (73 uses): not less. -/
theorem bridge_ge (a b : Int) :
    decide (a ≥ b) = (Uni.cmp (Uni.ofInt a) (Uni.ofInt b)).isGE := by
  simp only [Uni.cmp, alignPair_ofInt]
  rw [Bool.eq_iff_iff]
  simp [Ordering.isGE_iff_ne_lt, Int.compare_eq_lt]
  all_goals omega

/-! ## 3.2 the fixed-width value operations -- log 289 §2.1

Twenty-two primitives. The universal side names the width it reads the
object at, and gives the result back through `Uni.bitsAt`. -/

theorem two_pow_nonneg {k : Nat} : (0 : Int) ≤ 2 ^ k := by
  exact_mod_cast Nat.zero_le (2 ^ k)

theorem shl_eq {w : Nat} (x : BitVec w) (k : Nat) :
    x <<< k = BitVec.ofNat w (x.toNat * 2 ^ k) := by
  apply BitVec.eq_of_toNat_eq
  simp [Nat.shiftLeft_eq]

/-- `&&&` (55 uses). -/
theorem bridge_and {w : Nat} (x y : BitVec w) :
    (x &&& y) = Uni.bitsAt w (Uni.band w (Uni.ofBitsU x) (Uni.ofBitsU y)) := by
  simp [Uni.band]

/-- `|||` (27 uses). -/
theorem bridge_or {w : Nat} (x y : BitVec w) :
    (x ||| y) = Uni.bitsAt w (Uni.bor w (Uni.ofBitsU x) (Uni.ofBitsU y)) := by
  simp [Uni.bor]

/-- `^^^` (74 uses). -/
theorem bridge_xor {w : Nat} (x y : BitVec w) :
    (x ^^^ y) = Uni.bitsAt w (Uni.bxor w (Uni.ofBitsU x) (Uni.ofBitsU y)) := by
  simp [Uni.bxor]

/-- `<<<` by a count (22 uses): a left shift IS a move of the exponent. -/
theorem bridge_shiftLeft {w : Nat} (x : BitVec w) (k : Nat) :
    x <<< k = Uni.bitsAt w (Uni.shl (Uni.ofBitsU x) k) := by
  rw [bitsAt_shl_ofBitsU, shl_eq]

/-- `>>>` by a count (33 uses): the unsigned reading, floored. -/
theorem bridge_shiftRight {w : Nat} (x : BitVec w) (k : Nat) :
    x >>> k = Uni.bitsAt w (Uni.shrL w (Uni.ofBitsU x) k) := by
  rw [Uni.shrL, bitsAt_ofBitsU, bitsAt_ofNat]
  apply BitVec.eq_of_toNat_eq
  simp [Nat.shiftRight_eq_div_pow, Nat.mod_eq_of_lt,
        Nat.lt_of_le_of_lt (Nat.div_le_self _ _) x.isLt]

/-- `shift_bits_left` (12 uses): the shift amount is a VALUE, read unsigned
at its own width. -/
theorem bridge_shift_bits_left {n m : Nat} (x : BitVec n) (s : BitVec m) :
    Sail'.shift_bits_left x s = Uni.bitsAt n (Uni.shlV m (Uni.ofBitsU x) (Uni.ofBitsU s)) := by
  rw [Sail'.shift_bits_left, Uni.shlV, bitsAt_ofBitsU, bitsAt_shl_ofBitsU]
  exact shl_eq x s.toNat

/-- `shift_bits_right` (10 uses). -/
theorem bridge_shift_bits_right {n m : Nat} (x : BitVec n) (s : BitVec m) :
    Sail'.shift_bits_right x s = Uni.bitsAt n (Uni.shrV n m (Uni.ofBitsU x) (Uni.ofBitsU s)) := by
  rw [Sail'.shift_bits_right, Uni.shrV, bitsAt_ofBitsU]
  exact bridge_shiftRight x s.toNat

/-- `BitVec.sshiftRight` (1 use): the SIGNED reading, floored -- which is
why the universal counterpart is `shrA` and not `shrL`. -/
theorem bridge_sshiftRight {w : Nat} (x : BitVec w) (k : Nat) :
    x.sshiftRight k = Uni.bitsAt w (Uni.shrA w (Uni.ofBitsU x) k) := by
  rw [Uni.shrA, bitsAt_ofBitsU, bitsAt_ofInt, BitVec.sshiftRight,
      Int.shiftRight_eq_div_pow, Int.fdiv_eq_ediv_of_nonneg _ two_pow_nonneg]
  push_cast
  rfl

/-- `Sail.BitVec.zeroExtend` (2 uses): the unsigned reading, re-read at the
new width. No side condition -- when `w' < w` both sides truncate. -/
theorem bridge_zeroExtend {w : Nat} (x : BitVec w) (w' : Nat) :
    Sail'.zeroExtend x w' = Uni.bitsAt w' (Uni.zext w (Uni.ofBitsU x)) := by
  rw [Sail'.zeroExtend, Uni.zext, bitsAt_ofBitsU, Uni.ofBitsU, bitsAt_ofNat,
      BitVec.ofNat_toNat]

/-- `Sail.BitVec.truncate` (2 uses). Sail's `truncate` and its `zeroExtend`
are the SAME function of the same two arguments -- both are `setWidth` --
and so have the same bridge; only the width constraint Sail's type carries
tells them apart. -/
theorem bridge_truncate {w : Nat} (x : BitVec w) (w' : Nat) :
    Sail'.truncate x w' = Uni.bitsAt w' (Uni.zext w (Uni.ofBitsU x)) := by
  rw [Sail'.truncate, Uni.zext, bitsAt_ofBitsU, Uni.ofBitsU, bitsAt_ofNat,
      BitVec.ofNat_toNat]

/-- `Sail.BitVec.signExtend` (1 use). -/
theorem bridge_signExtend {w : Nat} (x : BitVec w) (w' : Nat) :
    Sail'.signExtend x w' = Uni.bitsAt w' (Uni.sext w (Uni.ofBitsU x)) := by
  rw [Sail'.signExtend, Uni.sext, bitsAt_ofBitsU, Uni.ofBitsS, bitsAt_ofInt]
  rfl

/-- `Sail.BitVec.length` (54 uses): the width the universal object was read
at IS the length Sail reports. -/
theorem bridge_length (w : Nat) (u : Uni) : Sail'.length (Uni.bitsAt w u) = w := rfl

/-- `==` (290 uses). -/
theorem bridge_beq {w : Nat} (x y : BitVec w) :
    (x == y) = (Uni.cmp (Uni.ofBitsU x) (Uni.ofBitsU y)).isEq := by
  simp only [Uni.cmp, Uni.ofBitsU, alignPair_ofInt]
  rw [Bool.eq_iff_iff]
  simp [Ordering.isEq_iff_eq_eq, BitVec.toNat_eq, Int.natCast_inj]

/-- `!=` (59 uses). -/
theorem bridge_bne {w : Nat} (x y : BitVec w) :
    (x != y) = !(Uni.cmp (Uni.ofBitsU x) (Uni.ofBitsU y)).isEq := by
  rw [← bridge_beq]
  rfl

/-- `Sail.BitVec.extractLsb` (325 uses, the most used primitive in the
model). -/
theorem bridge_extractLsb {w : Nat} (x : BitVec w) (hi lo : Nat) :
    Sail'.extractLsb x hi lo
      = Uni.bitsAt (hi - lo + 1) (Uni.extract w hi lo (Uni.ofBitsU x)) := by
  rw [Sail'.extractLsb, Uni.extract, bitsAt_ofBitsU, bitsAt_ofNat, BitVec.extractLsb,
      BitVec.extractLsb']
  apply BitVec.eq_of_toNat_eq
  simp [Nat.shiftRight_eq_div_pow]

/-- `+++` (94 uses): two values end to end. -/
theorem bridge_append {wx wy : Nat} (x : BitVec wx) (y : BitVec wy) :
    x ++ y = Uni.bitsAt (wx + wy) (Uni.cat wx wy (Uni.ofBitsU x) (Uni.ofBitsU y)) := by
  rw [Uni.cat, bitsAt_ofBitsU, bitsAt_ofBitsU, bitsAt_ofNat]
  apply BitVec.eq_of_toNat_eq
  have hb : x.toNat * 2 ^ wy + y.toNat < 2 ^ (wx + wy) := by
    have hx : x.toNat + 1 ≤ 2 ^ wx := x.isLt
    have hy := y.isLt
    have hm : (x.toNat + 1) * 2 ^ wy ≤ 2 ^ wx * 2 ^ wy := Nat.mul_le_mul_right _ hx
    rw [Nat.succ_mul] at hm
    rw [Nat.pow_add]
    omega
  rw [BitVec.toNat_append, BitVec.toNat_ofNat, ← Nat.shiftLeft_add_eq_or_of_lt y.isLt,
      Nat.shiftLeft_eq, Nat.mod_eq_of_lt hb]

/-- `BitVec.access` (142 uses). No side condition: out of range Sail's
`x[i]!` is the `Inhabited` default `false`, and the universal side reads a
zero bit there too, because `x.toNat < 2 ^ w ≤ 2 ^ i`. -/
theorem bridge_access {w : Nat} (x : BitVec w) (i : Nat) :
    Sail'.access x i = Uni.bitsAt 1 (Uni.bitAt w i (Uni.ofBitsU x)) := by
  rw [Sail'.access, Uni.bitAt, bitsAt_ofBitsU, bitsAt_ofNat]
  by_cases hi : i < w
  · rw [getElem!_pos x i hi, BitVec.getElem_eq_testBit_toNat,
        Nat.testBit_eq_decide_div_mod_eq]
    rcases Nat.mod_two_eq_zero_or_one (x.toNat / 2 ^ i) with h | h <;> rw [h] <;> decide
  · have hz : x.toNat / 2 ^ i = 0 := by
      apply Nat.div_eq_of_lt
      exact Nat.lt_of_lt_of_le x.isLt (Nat.pow_le_pow_right (by omega) (by omega))
    rw [getElem!_neg x i hi, hz]
    rfl

/-! ## 3.3 the container operations -- log 289 §2.3

A container is outside the universal object, so the bridge is stated on the
container OF universal objects: every element crosses in, the operation is
the pointwise one, and every element crosses back at its width. -/

/-- `Vector` (135 uses): reading a container into the universal type and back
out at the width is the identity, which is what makes the two containers the
same container. -/
theorem bridge_vector {w n : Nat} (v : Vector (BitVec w) n) :
    Uni.toVecBits w (Uni.ofVecBits v) = v := by
  rw [Uni.toVecBits, Uni.ofVecBits, Vector.map_map]
  exact Vector.map_id'' (fun x => bitsAt_ofBitsU x) v

/-- `vectorUpdate` (99 uses): Sail's `set!` IS the pointwise write, out of
range included -- there `set!` keeps the container and no index is equal to
`i`, so both sides keep it. -/
theorem bridge_vectorUpdate {w n : Nat} (v : Vector (BitVec w) n) (i : Nat) (a : BitVec w) :
    Uni.ofVecBits (Sail'.vectorUpdate v i a)
      = Uni.vecSet (Uni.ofVecBits v) i (Uni.ofBitsU a) := by
  apply Vector.ext
  intro j hj
  have hset : Sail'.vectorUpdate v i a = v.setIfInBounds i a := rfl
  simp only [Uni.ofVecBits, Uni.vecSet, hset, Vector.getElem_map, Vector.getElem_ofFn,
             Vector.getElem_setIfInBounds hj]
  by_cases h : i = j
  · simp [h]
  · simp [h]
    all_goals exact fun hh => absurd (Eq.symm hh) h

/-- `vectorInit` (15 uses). -/
theorem bridge_vectorInit {w n : Nat} (a : BitVec w) :
    Uni.ofVecBits (Sail'.vectorInit (n := n) a) = Uni.vecConst n (Uni.ofBitsU a) := by
  apply Vector.ext
  intro j hj
  simp [Sail'.vectorInit, Uni.ofVecBits, Uni.vecConst]

/-- `Vector.length` (4 uses). -/
theorem bridge_vectorLength {n : Nat} (v : Vector Uni n) : Sail'.Vector.length v = n := rfl

/-! ## 3.4 the subrange write

`updateSubrange'` is the one Sail primitive whose body is a mask, a shift
and an or; the universal counterpart is written from `Universal.lean`'s own
`band`, `bor`, `bnot` and `shl` and the same three steps. -/

theorem ofNat_shiftLeft (w a k : Nat) :
    BitVec.ofNat w a <<< k = BitVec.ofNat w (a * 2 ^ k) := by
  rw [shl_eq]
  apply BitVec.eq_of_toNat_eq
  simp [BitVec.toNat_ofNat, Nat.mul_mod]

theorem allOnes_shiftLeft (w len lo : Nat) :
    ((BitVec.allOnes len).zeroExtend w) <<< lo
      = Uni.bitsAt w (Uni.maskAt len lo) := by
  rw [Uni.maskAt, bitsAt_ofNat, ← ofNat_shiftLeft]
  congr 1
  rw [BitVec.zeroExtend, ← BitVec.ofNat_toNat, BitVec.toNat_allOnes]

theorem zeroExtend_shiftLeft {len : Nat} (w : Nat) (y : BitVec len) (lo : Nat) :
    (y.zeroExtend w) <<< lo = Uni.bitsAt w (Uni.shl (Uni.ofBitsU y) lo) := by
  rw [bitsAt_shl_ofBitsU, BitVec.zeroExtend, ← BitVec.ofNat_toNat, ofNat_shiftLeft]

/-- the shape every subrange write has: `updateSubrange'` IS `depositAt`. -/
theorem bridge_updateSubrange' {w len : Nat} (x : BitVec w) (lo : Nat) (y : BitVec len) :
    Sail'.updateSubrange' x lo len y
      = Uni.bitsAt w (Uni.depositAt w len lo (Uni.ofBitsU x) (Uni.ofBitsU y)) := by
  rw [Sail'.updateSubrange', Uni.depositAt, Uni.bor, bitsAt_ofBitsU, Uni.band, bitsAt_ofBitsU,
      Uni.bnot, bitsAt_ofBitsU, bitsAt_ofBitsU, bitsAt_ofBitsU, allOnes_shiftLeft,
      zeroExtend_shiftLeft, BitVec.and_comm]

/-- `Sail.BitVec.updateSubrange` (150 uses). -/
theorem bridge_updateSubrange {w : Nat} (x : BitVec w) (hi lo : Nat)
    (y : BitVec (hi - lo + 1)) :
    Sail'.updateSubrange x hi lo y
      = Uni.bitsAt w (Uni.deposit w hi lo (Uni.ofBitsU x) (Uni.ofBitsU y)) :=
  bridge_updateSubrange' x lo y

/-- `BitVec.update` (26 uses): one bit written is a subrange of one bit. -/
theorem bridge_update {w : Nat} (x : BitVec w) (i : Nat) (b : BitVec 1) :
    Sail'.update x i b
      = Uni.bitsAt w (Uni.depositAt w 1 i (Uni.ofBitsU x) (Uni.ofBitsU b)) :=
  bridge_updateSubrange' x i b

/-! ## 3.5 the leading zeros

`Ubv.len` -- the universal type's own "how many bits this magnitude
occupies" -- is what counts them, so the statement is `w - Ubv.len`. -/

theorem Ubv.len_eq (v : Nat) : Ubv.len v = if v = 0 then 0 else Ubv.len (v / 2) + 1 := by
  rw [Ubv.len]
  split <;> rfl

theorem Ubv.len_le_iff : ∀ (k v : Nat), Ubv.len v ≤ k ↔ v < 2 ^ k
  | 0, v => by
      rw [Ubv.len_eq]
      split
      · simp_all
      · simp_all
  | k + 1, v => by
      rw [Ubv.len_eq]
      split
      · next h => simp [h, Nat.two_pow_pos]
      · next h =>
          rw [Nat.add_le_add_iff_right, Ubv.len_le_iff k (v / 2), Nat.pow_succ,
              Nat.div_lt_iff_lt_mul (by omega)]
          all_goals omega

theorem Ubv.len_eq_of_bounds {v k : Nat} (h1 : v < 2 ^ k) (h2 : ¬ v < 2 ^ (k - 1)) :
    Ubv.len v = k := by
  have hle := (Ubv.len_le_iff k v).mpr h1
  have hgt : ¬ Ubv.len v ≤ k - 1 := fun h => h2 ((Ubv.len_le_iff (k - 1) v).mp h)
  omega

/-- `BitVec.countLeadingZeros` (5 uses). -/
theorem bridge_countLeadingZeros {w : Nat} (x : BitVec w) :
    Sail'.countLeadingZeros x = Uni.clzU w (Uni.ofBitsU x) := by
  rw [Sail'.countLeadingZeros, Uni.clzU, bitsAt_ofBitsU]
  by_cases hx : x = 0#w
  · subst hx
    have hz : (0#w : BitVec w).clz = BitVec.ofNat w w := BitVec.clz_eq_iff_eq_zero.mpr rfl
    rw [hz]
    simp [Ubv.len_eq, BitVec.toNat_ofNat, Nat.mod_eq_of_lt Nat.lt_two_pow_self]
  · have hne : x ≠ 0#w := hx
    have hw : 0 < w := by
      rcases Nat.eq_zero_or_pos w with h | h
      · subst h; exact absurd (Subsingleton.elim x _) hne
      · exact h
    have hlt : x.clz.toNat < w := by
      have hlt' := BitVec.clz_lt_iff_ne_zero.mpr hne
      simp only [BitVec.lt_def, BitVec.natCast_eq_ofNat, BitVec.toNat_ofNat,
                 Nat.mod_eq_of_lt Nat.lt_two_pow_self] at hlt'
      exact hlt'
    have hub : x.toNat < 2 ^ (w - x.clz.toNat) := BitVec.toNat_lt_two_pow_sub_clz
    have hlb : 2 ^ (w - 1 - x.clz.toNat) ≤ x.toNat :=
      BitVec.two_pow_sub_clz_le_toNat_of_ne_zero hw hne
    have : Ubv.len x.toNat = w - x.clz.toNat := by
      apply Ubv.len_eq_of_bounds hub
      have : w - x.clz.toNat - 1 = w - 1 - x.clz.toNat := by omega
      rw [this]
      omega
    omega

/-! ## 3.6 bits taken out of an unbounded number

`get_slice_int` is the primitive `to_bits_truncate` is built from, and
`Universal.sailToBitsTruncate_eq_ofInt` is its `lo = 0` case. This is the
general one. -/

theorem two_pow_pos_int (k : Nat) : (0 : Int) < 2 ^ k := by
  exact_mod_cast Nat.two_pow_pos k

theorem two_pow_succ_split (lo len : Nat) :
    (2:Int) ^ (lo + len + 1) = 2 ^ len * 2 * 2 ^ lo := by
  rw [Int.pow_add, Int.pow_add, Int.pow_one]
  simp [Int.mul_comm, Int.mul_left_comm]

/-- the arithmetic of the slice: cutting the number down to `lo + len + 1`
bits first changes nothing about bits `lo .. lo+len-1`. -/
theorem slice_emod (n : Int) (lo len : Nat) :
    (n % 2 ^ (lo + len + 1)) / 2 ^ lo % 2 ^ len = n / 2 ^ lo % 2 ^ len := by
  have hP : (2:Int) ^ lo ≠ 0 := Int.ne_of_gt (two_pow_pos_int lo)
  have hinner : n % 2 ^ (lo + len + 1)
      = n + 2 ^ len * (-(2 * (n / 2 ^ (lo + len + 1)))) * 2 ^ lo := by
    rw [Int.emod_def, two_pow_succ_split lo len]
    simp [Int.mul_comm, Int.mul_left_comm, Int.mul_assoc, Int.sub_eq_add_neg, Int.mul_neg]
  rw [hinner, Int.add_mul_ediv_right _ _ hP, Int.add_mul_emod_self_left]

/-- `get_slice_int` (4 uses). -/
theorem bridge_get_slice_int (len : Nat) (n : Int) (lo : Nat) :
    Sail'.get_slice_int len n lo = Uni.bitsAt len (Uni.sliceInt len (Uni.ofInt n) lo) := by
  have h0 : 0 ≤ n % 2 ^ (lo + len + 1) := Int.emod_nonneg n (Int.ne_of_gt (two_pow_pos_int _))
  have hcast : ((n % 2 ^ (lo + len + 1)).toNat : Int) = n % 2 ^ (lo + len + 1) :=
    Int.toNat_of_nonneg h0
  have key : (((n % 2 ^ (lo + len + 1)).toNat / 2 ^ lo % 2 ^ len : Nat) : Int)
      = n / 2 ^ lo % 2 ^ len := by
    push_cast [hcast]
    exact slice_emod n lo len
  rw [Sail'.get_slice_int, Uni.sliceInt, toInt_ofInt, bitsAt_ofInt]
  apply BitVec.eq_of_toNat_eq
  rw [BitVec.extractLsb', BitVec.toNat_ofNat, BitVec.toNat_ofInt, BitVec.toNat_ofInt,
      Nat.shiftRight_eq_div_pow]
  push_cast
  rw [Int.emod_emod_of_dvd _ (Int.dvd_refl _), ← key, Int.toNat_natCast]

/-! ## 3.7 the trailing zeros

The universal counterpart is `twoAdic`: how many times 2 divides the
magnitude, which is the exponent the object would carry with an odd
mantissa. Three lemmas make it the index of the lowest set bit, and Sail's
count is that index. -/

theorem Uni.twoAdic_eq (v : Nat) :
    Uni.twoAdic v = if v = 0 ∨ v % 2 = 1 then 0 else Uni.twoAdic (v / 2) + 1 := by
  rw [Uni.twoAdic]
  split <;> rfl

theorem testBit_twoAdic : ∀ (v : Nat), v ≠ 0 → Nat.testBit v (Uni.twoAdic v) = true := by
  intro v
  induction v using Nat.strongRecOn with
  | _ v ih =>
    intro hv
    rw [Uni.twoAdic_eq]
    split
    · next h =>
        rcases h with h | h
        · exact absurd h hv
        · simp [Nat.testBit_eq_decide_div_mod_eq, h]
    · next h =>
        have h2 : v % 2 = 0 := by omega
        have hlt : v / 2 < v := Nat.div_lt_self (Nat.pos_of_ne_zero hv) (by omega)
        have hne : v / 2 ≠ 0 := by omega
        rw [Nat.testBit_succ]
        exact ih (v / 2) hlt hne

theorem testBit_lt_twoAdic :
    ∀ (v i : Nat), i < Uni.twoAdic v → Nat.testBit v i = false := by
  intro v
  induction v using Nat.strongRecOn with
  | _ v ih =>
    intro i hi
    rw [Uni.twoAdic_eq] at hi
    split at hi
    · omega
    · next h =>
        have h2 : v % 2 = 0 := by omega
        have hv : v ≠ 0 := by omega
        have hlt : v / 2 < v := Nat.div_lt_self (Nat.pos_of_ne_zero hv) (by omega)
        cases i with
        | zero => simp [Nat.testBit_eq_decide_div_mod_eq, h2]
        | succ j =>
            rw [Nat.testBit_succ]
            exact ih (v / 2) hlt j (by omega)

/-- the lowest set bit IS `twoAdic`. -/
theorem twoAdic_unique (v c : Nat) (hc : Nat.testBit v c = true)
    (hlow : ∀ i, i < c → Nat.testBit v i = false) : c = Uni.twoAdic v := by
  have hv : v ≠ 0 := by
    intro h; subst h; simp at hc
  rcases Nat.lt_trichotomy c (Uni.twoAdic v) with h | h | h
  · exact absurd hc (by simp [testBit_lt_twoAdic v c h])
  · exact h
  · exact absurd (testBit_twoAdic v hv) (by simp [hlow _ h])

theorem reverse_zero {w : Nat} : (0#w : BitVec w).reverse = 0#w := by
  apply BitVec.eq_of_getLsbD_eq
  intro i
  simp [BitVec.getLsbD_reverse]

/-- `BitVec.countTrailingZeros` (5 uses). -/
theorem bridge_countTrailingZeros {w : Nat} (x : BitVec w) :
    Sail'.countTrailingZeros x = Uni.ctzU w (Uni.ofBitsU x) := by
  rw [Sail'.countTrailingZeros, Sail'.countLeadingZeros, Uni.ctzU, bitsAt_ofBitsU]
  by_cases hx : x = 0#w
  · subst hx
    rw [reverse_zero]
    have hz : (0#w : BitVec w).clz = BitVec.ofNat w w := BitVec.clz_eq_iff_eq_zero.mpr rfl
    simp [hz, BitVec.toNat_ofNat, Nat.mod_eq_of_lt Nat.lt_two_pow_self]
  · have hne : x ≠ 0#w := hx
    have hxn : x.toNat ≠ 0 := by
      intro h
      exact hne (BitVec.eq_of_toNat_eq (by simp [h]))
    rw [← BitVec.ctz_eq_reverse_clz]
    have h1 : Nat.testBit x.toNat x.ctz.toNat = true := by
      have hb := BitVec.getLsbD_true_ctz_of_ne_zero (x := x) hne
      simpa [BitVec.getLsbD] using hb
    have h2 : ∀ i, i < x.ctz.toNat → Nat.testBit x.toNat i = false := by
      intro i hi
      have hb := BitVec.getLsbD_false_of_lt_ctz (x := x) (i := i) hi
      simpa [BitVec.getLsbD] using hb
    simp only [hxn, if_false]
    exact twoAdic_unique x.toNat x.ctz.toNat h1 h2

/-! ## 3.8 single bits joined -/

theorem toNat_bitvec_one (y : BitVec 1) : y.toNat = 0 ∨ y.toNat = 1 := by
  have := y.isLt
  omega

theorem getElem_zero_toNat (y : BitVec 1) : (y[0] : Bool).toNat = y.toNat := by
  rw [BitVec.getElem_eq_testBit_toNat, Nat.testBit_eq_decide_div_mod_eq]
  rcases toNat_bitvec_one y with h | h <;> rw [h] <;> rfl

theorem join1_toNat (xs : List (BitVec 1)) :
    ((Sail'.join1 xs).toNat : Int) = Uni.joinBE (xs.map Uni.ofBitsU) := by
  induction xs with
  | nil => rfl
  | cons y ys ih =>
      have hR : (BitVec.ofBoolListBE (ys.map fun x => (x[0] : Bool))).toNat
          < 2 ^ (ys.map fun x => (x[0] : Bool)).length :=
        (BitVec.ofBoolListBE (ys.map fun x => (x[0] : Bool))).isLt
      have hih : ((BitVec.ofBoolListBE (ys.map fun x => (x[0] : Bool))).toNat : Int)
          = Uni.joinBE (ys.map Uni.ofBitsU) := by
        rw [← ih, Sail'.join1, BitVec.toNat_cast]
      rw [Sail'.join1, BitVec.toNat_cast, List.map_cons, BitVec.ofBoolListBE,
          BitVec.toNat_cons, ← Nat.shiftLeft_add_eq_or_of_lt hR, Nat.shiftLeft_eq,
          getElem_zero_toNat, List.map_cons, Uni.joinBE, ← hih]
      push_cast
      rcases toNat_bitvec_one y with h | h <;> simp [h]

/-- `BitVec.join1` (5 uses). -/
theorem bridge_join1 (xs : List (BitVec 1)) :
    Sail'.join1 xs = Uni.bitsAt xs.length (Uni.joinBits (xs.map Uni.ofBitsU)) := by
  rw [Uni.joinBits, bitsAt_ofInt, ← join1_toNat, ofInt_natCast, BitVec.ofNat_toNat,
      BitVec.setWidth_eq]

/-! # 4. the rotates

Not primitives -- the emit defines them itself -- but the universal
counterparts were missing, so they are here with their bridges. These two
transcriptions come from the EMIT's own prelude, not from the library:
`cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM/Prelude.lean:423`
and `:427`. Note the `-i`: the second shift amount is an INT, so it is
Sail's `HShiftLeft (BitVec w) Int` that runs there, not core's. -/

namespace Emit'

/-- `LeanIM/Prelude.lean:423` -/
def rotater {w : Nat} (value : BitVec w) (shift : Nat) : BitVec w :=
  (value >>> shift) ||| Sail'.shiftLeftInt value ((Sail'.length value : Int) - (shift : Int))

/-- `LeanIM/Prelude.lean:427` -/
def rotatel {w : Nat} (value : BitVec w) (shift : Nat) : BitVec w :=
  (value <<< shift) ||| Sail'.shiftRightInt value ((Sail'.length value : Int) - (shift : Int))

end Emit'

theorem shiftLeftInt_ofNat {w : Nat} (b : BitVec w) (n : Nat) :
    Sail'.shiftLeftInt b (n : Int) = b <<< n := rfl

theorem shiftRightInt_ofNat {w : Nat} (b : BitVec w) (n : Nat) :
    Sail'.shiftRightInt b (n : Int) = b >>> n := by
  rcases n with _ | m
  · have h0 : Sail'.shiftRightInt b ((0 : Nat) : Int) = BitVec.shiftLeft b 0 := rfl
    rw [h0]
    apply BitVec.eq_of_toNat_eq
    simp
  · rw [Sail'.shiftRightInt, show (-((m + 1 : Nat) : Int)) = Int.negSucc m by omega]
    rfl

/-- rotate right, for a rotation no wider than the value -- which is the
constraint the emit's own type carries (`k_m ≥ shift`). -/
theorem bridge_rotater {w : Nat} (x : BitVec w) (k : Nat) (hk : k ≤ w) :
    Emit'.rotater x k = Uni.bitsAt w (Uni.rotR w k (Uni.ofBitsU x)) := by
  rw [Emit'.rotater, Sail'.length,
      show ((w : Int) - (k : Int)) = ((w - k : Nat) : Int) by omega,
      shiftLeftInt_ofNat, Uni.rotR, Uni.bor, bitsAt_ofBitsU, ← bridge_shiftRight,
      ← bridge_shiftLeft]

/-- rotate left. -/
theorem bridge_rotatel {w : Nat} (x : BitVec w) (k : Nat) (hk : k ≤ w) :
    Emit'.rotatel x k = Uni.bitsAt w (Uni.rotL w k (Uni.ofBitsU x)) := by
  rw [Emit'.rotatel, Sail'.length,
      show ((w : Int) - (k : Int)) = ((w - k : Nat) : Int) by omega,
      shiftRightInt_ofNat, Uni.rotL, Uni.bor, bitsAt_ofBitsU, ← bridge_shiftRight,
      ← bridge_shiftLeft]

/-! # 5. what the bridges turned up

Four places where a primitive does NOT mean what its name, or log 289's
one-line reading of it, says. Each is a theorem, so each is checked. -/

/-- FINDING 1. Log 289 §2.2 reads `Int.ediv` as "divide, flooring". It is
EUCLIDEAN, not flooring, and the two part company on a negative divisor.
So `bridge_ediv` (against the Euclidean counterpart `divE`) holds with no
side condition, while `bridge_ediv_as_divF` (against a flooring counterpart)
needs `0 ≤ b`. Anything that rewrites `Int.ediv` to a flooring operation
without that hypothesis is unsound. -/
theorem ediv_ne_fdiv : (7 : Int) / (-2) ≠ Int.fdiv 7 (-2) := by decide

/-- FINDING 2. `^i` is Sail's own `HPow Int Int Int`, whose exponent goes
through `Int.toNat`. A negative exponent is therefore not a reciprocal and
not an error: it is the exponent zero, and the answer is `1` for every base,
zero included. -/
theorem ipow_neg (a : Int) (n : Int) (hn : n < 0) : Sail'.ipow a n = 1 := by
  rw [Sail'.ipow, show n.toNat = 0 by omega, Int.pow_zero]

/-- FINDING 3. `Sail.BitVec.truncate` and `Sail.BitVec.zeroExtend` are the
SAME function of the same two arguments -- both are Lean's `setWidth`. Only
the width constraint Sail's type carries tells them apart, and a `zeroExtend`
to a NARROWER width silently drops the high bits. -/
theorem truncate_eq_zeroExtend {w : Nat} (x : BitVec w) (w' : Nat) :
    Sail'.truncate x w' = Sail'.zeroExtend x w' := rfl

theorem zeroExtend_drops {w : Nat} (x : BitVec w) (w' : Nat) :
    (Sail'.zeroExtend x w').toNat = x.toNat % 2 ^ w' := by
  rw [Sail'.zeroExtend, BitVec.zeroExtend, BitVec.toNat_setWidth]

/-- FINDING 4. `vectorUpdate` past the end of the container is a SILENT
no-op: the write is dropped and no error is raised. Anything that reasons
"the element at `i` is now `a`" after a `vectorUpdate` needs `i < n`. -/
theorem vectorUpdate_out_of_range {α : Type} {n : Nat} (v : Vector α n) (i : Nat) (a : α)
    (h : n ≤ i) : Sail'.vectorUpdate v i a = v :=
  Vector.setIfInBounds_eq_of_size_le h

/-! # 6. the tally

  §2.1 fixed-width values, 22 of 22:
    extractLsb, updateSubrange, length, zeroExtend, signExtend, truncate,
    shift_bits_left, shift_bits_right, access, update, countTrailingZeros,
    countLeadingZeros, sshiftRight, join1, +++, ^^^, &&&, |||, <<<, >>>,
    ==, !=
  §2.2 unbounded numbers, 17 of 17:
    +i, -i, *i, ^i, tdiv, tmod, ediv, natAbs, toInt, toNatInt, addInt,
    subInt, get_slice_int, <b, ≤b, >b, ≥b
  §2.3 containers, 4 of 5:
    Vector, vectorUpdate, vectorInit, Vector.length; `untilFuelM` has no
    counterpart in a type that holds one number, and is not bridged.

Every bridge is proved for a GENERIC width: no statement here is
instantiated at 8, 16, 32 or 64, and `bv_decide` is never used, so nothing
below is restricted to the widths the model happens to use. Two bridges
carry a side condition, both of them stated above: `bridge_ediv_as_divF`
(`0 ≤ b`) and the two rotates (`k ≤ w`), which are not primitives. -/

end Bridges
end Universal
