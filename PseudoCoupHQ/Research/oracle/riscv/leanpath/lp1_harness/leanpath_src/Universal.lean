/-
  Universal.lean -- ONE universal numeric type, and the exact operations
  on it. Written once, general in its parameters; nothing in this file
  is keyed by an instruction name or an operator token.

  the owner's definition, 2026-09-15, verbatim:

    "universal type: (sign, mant, expo) where: sign is length-1 bit_vec;
     mant is unbounded bit_vec; expo is (bit_vec, bit_vec), where the
     first bit_vec is length-1 and the second bit_vec is unbounded"

  The value is

      (-1)^sign * mant * 2^expo,   expo = (-1)^expo.sign * expo.mag

  with `mant` read as an integer, its bits weighted from the least
  significant end; an integer is `expo = 0`.

  Every primitive kind (unsigned n-bit, signed n-bit, bool, IEEE binary,
  fixed-point) is a CONSTRAINT on this one object plus a PROJECTION of an
  exact result back into the kind. The kinds live in `Kinds.lean`; this
  file holds only the object and the exact operations, so that the
  projection is the only place a kind's behaviour is written.

  This module imports nothing. It is deliberately independent of the
  Sail emit, so that it builds whether or not the model is built, and so
  that churn in the model cannot break it.
-/

namespace Universal

/-- An **unbounded bit_vec**: its bits weighted from the least significant
end, which is to say a `Nat`. `bit` recovers the bit reading. -/
abbrev Ubv := Nat

namespace Ubv

/-- bit `i` of an unbounded bit_vec, as a length-1 bit_vec. -/
def bit (v : Ubv) (i : Nat) : BitVec 1 := BitVec.ofBool (v.testBit i)

/-- how many bits the unbounded bit_vec occupies: `0` for zero, else
`1 + ⌊log2 v⌋`. The leading bit of a nonzero `v` is bit `len v - 1`. -/
def len (v : Ubv) : Nat :=
  if h : v = 0 then 0 else len (v / 2) + 1
decreasing_by exact Nat.div_lt_self (Nat.pos_of_ne_zero h) (by omega)

end Ubv

/-- minimum of two integers (core pins no `Min Int` we want to depend on). -/
def imin (a b : Int) : Int := if a ≤ b then a else b
/-- maximum of two integers. -/
def imax (a b : Int) : Int := if a ≤ b then b else a

/-- the exponent: a length-1 bit_vec for the sign, an unbounded bit_vec
for the magnitude. -/
structure Expo where
  sign : BitVec 1
  mag  : Ubv
deriving DecidableEq, Repr, Inhabited, BEq

namespace Expo

/-- `(-1)^sign * mag`. -/
def val (x : Expo) : Int := if x.sign == 1#1 then -(x.mag : Int) else (x.mag : Int)

def ofInt (k : Int) : Expo := { sign := if k < 0 then 1#1 else 0#1, mag := k.natAbs }

/-- the exponent of an integer. -/
def zero : Expo := { sign := 0#1, mag := 0 }

end Expo

/-- **the universal type**: `(sign, mant, expo)`. -/
structure Uni where
  sign : BitVec 1
  mant : Ubv
  expo : Expo
deriving DecidableEq, Repr, Inhabited, BEq

namespace Uni

/-- the exponent as an integer. -/
def e (u : Uni) : Int := u.expo.val

def isNeg (u : Uni) : Bool := u.sign == 1#1

/-- the mantissa with its sign: `(-1)^sign * mant`. -/
def smant (u : Uni) : Int := if u.isNeg then -(u.mant : Int) else (u.mant : Int)

/-- build from a sign, a magnitude and an exponent. -/
def mk' (neg : Bool) (m : Ubv) (k : Int) : Uni :=
  { sign := if neg then 1#1 else 0#1, mant := m, expo := Expo.ofInt k }

/-- `m * 2^k`, the sign read off `m`. -/
def ofSignedAt (m : Int) (k : Int) : Uni := mk' (decide (m < 0)) m.natAbs k

/-- an integer: `expo = 0`. -/
def ofInt (n : Int) : Uni := ofSignedAt n 0

def zero : Uni := ofInt 0

def isZero (u : Uni) : Bool := u.mant == 0

/-- the exponent of the leading bit of `|u|` (meaningless when `u` is zero). -/
def topExp (u : Uni) : Int := u.e + (Ubv.len u.mant : Int) - 1

/-- the two values at one common exponent: `(m₁, m₂, k)` with
`x = m₁ * 2^k` and `y = m₂ * 2^k`, exactly. -/
def alignPair (x y : Uni) : Int × Int × Int :=
  let ex := x.e
  let ey := y.e
  let k := imin ex ey
  (x.smant * 2 ^ (ex - k).toNat, y.smant * 2 ^ (ey - k).toNat, k)

/-! ## the exact operations on the universal object

Each is exact: no width, no rounding, no saturation. A kind's projection
is the only place anything is lost. -/

def add (x y : Uni) : Uni := let (a, b, k) := alignPair x y; ofSignedAt (a + b) k

def sub (x y : Uni) : Uni := let (a, b, k) := alignPair x y; ofSignedAt (a - b) k

def mul (x y : Uni) : Uni := ofSignedAt (x.smant * y.smant) (x.e + y.e)

/-- truncated toward zero, which is what Sail's own integer definitions
use (`Int.tdiv`); a zero divisor gives zero, as `Int.tdiv` does, and the
model's own guard (quotient `-1` on a zero divisor) is the MODEL's, never
the kind's. Aligning both to one exponent makes the quotient exactly the
integer quotient of the aligned mantissas. -/
def divT (x y : Uni) : Uni := let (a, b, _) := alignPair x y; ofInt (Int.tdiv a b)

/-- the matching remainder (`Int.tmod`); it carries the common exponent. -/
def remT (x y : Uni) : Uni := let (a, b, k) := alignPair x y; ofSignedAt (Int.tmod a b) k

def cmp (x y : Uni) : Ordering := let (a, b, _) := alignPair x y; compare a b

/-- `u * 2^k`, exactly: a shift is a move of the exponent. -/
def scale (u : Uni) (k : Int) : Uni := ofSignedAt u.smant (u.e + k)

/-- left shift: exact, no width. -/
def shl (u : Uni) (k : Nat) : Uni := u.scale (k : Int)

/-- the integer the object denotes; when the object is not an integer
(`expo < 0`) this truncates toward zero. -/
def toInt (u : Uni) : Int :=
  let k := u.e
  if 0 ≤ k then u.smant * 2 ^ k.toNat
  else
    let d := (-k).toNat
    let q : Int := ((u.mant / 2 ^ d : Nat) : Int)
    if u.isNeg then -q else q

/-! ## the bit operations

A bit operation has no meaning without a width -- `not` least of all --
so each takes the width it reads the object at, as the w-bit two's
complement string, and gives the result back as a universal object. -/

def bitsAt (w : Nat) (u : Uni) : BitVec w := BitVec.ofInt w u.toInt
def ofBitsU {w : Nat} (b : BitVec w) : Uni := ofInt (b.toNat : Int)
def ofBitsS {w : Nat} (b : BitVec w) : Uni := ofInt b.toInt

def band (w : Nat) (x y : Uni) : Uni := ofBitsU (bitsAt w x &&& bitsAt w y)
def bor  (w : Nat) (x y : Uni) : Uni := ofBitsU (bitsAt w x ||| bitsAt w y)
def bxor (w : Nat) (x y : Uni) : Uni := ofBitsU (bitsAt w x ^^^ bitsAt w y)
def bnot (w : Nat) (x : Uni) : Uni := ofBitsU (~~~ bitsAt w x)

/-- logical right shift at a width: the unsigned reading, floored. -/
def shrL (w : Nat) (x : Uni) (k : Nat) : Uni := ofInt (((bitsAt w x).toNat / 2 ^ k : Nat) : Int)
/-- arithmetic right shift at a width: the signed reading, floored. -/
def shrA (w : Nat) (x : Uni) (k : Nat) : Uni := ofInt (Int.fdiv (bitsAt w x).toInt (2 ^ k))

/-! ## the one primitive rounding needs -/

/-- `|u|` split at the quantum exponent `q`:

    |u| = sig * 2^q  +  guard * 2^(q-1)  +  (the bits below)

reported as `(sig, guard, sticky)`. `sticky` is whether ANY bit below the
guard is set -- the idiom that makes the exact width finite. When `q` is
at or below the object's own exponent nothing is lost and both bits are
false. -/
def splitAt (u : Uni) (q : Int) : Nat × Bool × Bool :=
  let k := u.e
  if q ≤ k then (u.mant * 2 ^ (k - q).toNat, false, false)
  else
    let d := (q - k).toNat
    let sig := u.mant / 2 ^ d
    let rest := u.mant % 2 ^ d
    (sig, rest.testBit (d - 1), !(rest % 2 ^ (d - 1) == 0))

end Uni

/-! ## Sail's own truncation, transcribed

`to_bits_truncate` in the emitted `LeanIM/Prelude.lean` is
`get_slice_int l n 0`, and `get_slice_int` in the support library
(`Sail/Common.lean`) is `BitVec.extractLsb' lo len (BitVec.ofInt (lo + len + 1) n)`.
Transcribed here so the integer kinds can be checked against it without
this module importing the emit. -/
def sailToBitsTruncate (l : Nat) (n : Int) : BitVec l :=
  BitVec.extractLsb' 0 l (BitVec.ofInt (0 + l + 1) n)

/-- Sail's truncation IS the wrap modulo `2^l` that the fixed-width
integer kinds project by. -/
theorem sailToBitsTruncate_eq_ofInt (l : Nat) (n : Int) :
    sailToBitsTruncate l n = BitVec.ofInt l n := by
  apply BitVec.eq_of_toNat_eq
  simp [sailToBitsTruncate, BitVec.toNat_ofInt]
  have hp : (0:Int) < 2 ^ l := by exact_mod_cast Nat.two_pow_pos l
  have hp1 : (0:Int) < 2 ^ (l + 1) := by exact_mod_cast Nat.two_pow_pos (l + 1)
  have hd : ((2:Int) ^ l) ∣ ((2:Int) ^ (l + 1)) := ⟨2, by rw [Int.pow_succ]⟩
  have h1 : n % (2:Int) ^ (l + 1) % (2:Int) ^ l = n % (2:Int) ^ l :=
    Int.emod_emod_of_dvd n hd
  have h0 : (0:Int) ≤ n % (2:Int) ^ (l + 1) := Int.emod_nonneg n (by omega)
  have h2 := Int.toNat_emod h0 (by omega : (0:Int) ≤ (2:Int) ^ l)
  rw [h1] at h2
  simpa using h2.symm

end Universal
