/-
  Kinds.lean -- the five primitive kinds, each a CONSTRAINT on the one
  universal type of `Universal.lean` plus a PROJECTION of an exact result
  back into the kind. Written once, general in its parameters; nothing
  here is keyed by an instruction name or an operator token.

    kind            constraint                            projection
    ------------    ----------------------------------    ---------------------------
    unsigned n      sign 0, expo 0, mant ≤ n bits         wrap modulo 2^n
    signed n        expo 0, mant < 2^(n-1) with the sign  wrap modulo 2^n
    bool            sign 0, expo 0, mant ≤ 1 bit          nonzero to 1
    IEEE (e, m)     on the format's grid and in range     round (five modes), five flags
    fixed (w, q)    expo held at the type's value         round, then saturate or wrap

  One signature serves all five: the rounding mode goes in, the five
  flags come out. The integer kinds ignore the mode and raise no flag;
  fixed-point uses the mode and raises inexact / overflow; IEEE uses
  both fully. Sail's own integer definitions have exactly this shape --
  an exact unbounded operation, then `to_bits_truncate` -- so the
  integer kinds ARE Sail's functions (`sailToBitsTruncate_eq_ofInt`).

  The IEEE operations have exactly the shape of the axioms Sail's Lean
  emit declares in `LeanIM/RiscvExtras.lean`:

      axiom riscv_f64Add : BitVec 3 → BitVec 64 → BitVec 64 → (BitVec 5 × BitVec 64)

  so `Kinds.Axioms.riscv_f64Add` can become that axiom's body. THE CACHE
  IS NEVER EDITED: see the note at `Axioms` below.

  Imports `Universal` and nothing else.
-/

import Universal

namespace Kinds

open Universal

/-! ## the five flags, in the model's own order

`LeanIM/FextInsts.lean` fixes them: NX = bit 0, UF = bit 1, OF = bit 2,
DZ = bit 3, NV = bit 4. -/

def noFlag : BitVec 5 := 0b00000#5
def nxFlag : BitVec 5 := 0b00001#5
def ufFlag : BitVec 5 := 0b00010#5
def ofFlag : BitVec 5 := 0b00100#5
def dzFlag : BitVec 5 := 0b01000#5
def nvFlag : BitVec 5 := 0b10000#5

/-! ## the rounding modes, in the model's own encoding

`encdec_rounding_mode_forwards` in the emit: RNE 000, RTZ 001, RDN 010,
RUP 011, RMM 100, DYN 111. The model resolves DYN and refuses the
reserved 101/110 before it ever calls one of these, so those three
never reach here; they are read as RNE. -/

inductive RM where
  | rne | rtz | rdn | rup | rmm
deriving DecidableEq, Repr, Inhabited, BEq

def RM.ofBits (b : BitVec 3) : RM :=
  match b.toNat with
  | 0 => .rne
  | 1 => .rtz
  | 2 => .rdn
  | 3 => .rup
  | 4 => .rmm
  | _ => .rne

/-- the increment decision: truncation keeps the high bits, and the mode
plus the guard and sticky bits decide whether one is added back. This is
the whole of rounding. -/
def wantsInc (rm : RM) (neg odd g st : Bool) : Bool :=
  match rm with
  | .rne => g && (st || odd)
  | .rmm => g
  | .rtz => false
  | .rdn => neg && (g || st)
  | .rup => (!neg) && (g || st)

/-! ## a value of a kind

The universal object carries the numbers. `±∞` and NaN are not numbers:
they exist only in the IEEE kind's ENCODING, so the projection's
codomain names them apart. -/

inductive Val where
  | num (u : Uni)
  | inf (neg : Bool)
  | nan
deriving DecidableEq, Repr, Inhabited, BEq

/-- **a primitive kind**: a constraint on the universal object, and the
projection of an exact result back into it. -/
structure Kind where
  name  : String
  /-- is this exact universal object a value OF the kind -/
  holds : Uni → Bool
  /-- project an exact result into the kind: mode in, five flags out -/
  proj  : BitVec 3 → Uni → BitVec 5 × Val

/-! ## kind 1 -- unsigned n-bit -/

def unsignedK (n : Nat) : Kind where
  name := "unsigned " ++ toString n
  holds u := u.sign == 0#1 && u.expo.mag == 0 && decide (Ubv.len u.mant ≤ n)
  proj _ u := (noFlag, .num (Uni.ofInt (u.toInt % ((2 : Int) ^ n))))

/-! ## kind 2 -- signed n-bit -/

def signedK (n : Nat) : Kind where
  name := "signed " ++ toString n
  holds u := u.expo.mag == 0 &&
    (if u.isNeg then decide (u.mant ≤ 2 ^ (n - 1)) else decide (u.mant < 2 ^ (n - 1)))
  proj _ u := (noFlag, .num (Uni.ofInt (BitVec.ofInt n u.toInt).toInt))

/-! ## kind 3 -- bool -/

def boolK : Kind where
  name := "bool"
  holds u := u.sign == 0#1 && u.expo.mag == 0 && decide (Ubv.len u.mant ≤ 1)
  proj _ u := (noFlag, .num (Uni.ofInt (if u.mant == 0 then 0 else 1)))

/-! ## kind 4 -- IEEE binary (e exponent bits, m significand bits) -/

structure Fmt where
  e : Nat
  m : Nat
deriving DecidableEq, Repr, Inhabited, BEq

namespace Fmt
/-- the encoding's total width. -/
def w (f : Fmt) : Nat := 1 + f.e + f.m
def bias (f : Fmt) : Int := (2 : Int) ^ (f.e - 1) - 1
/-- the largest exponent of a finite number. -/
def emax (f : Fmt) : Int := f.bias
/-- the exponent of the smallest normal number. -/
def emin (f : Fmt) : Int := 1 - f.bias
/-- the quantum exponent of the subnormals. -/
def qmin (f : Fmt) : Int := f.emin - (f.m : Int)
end Fmt

def binary16 : Fmt := { e := 5,  m := 10 }
def binary32 : Fmt := { e := 8,  m := 23 }
def binary64 : Fmt := { e := 11, m := 52 }
/-- brain float: binary32's exponent range on seven significand bits. It is
another VALUE of `Fmt`, never another code path. -/
def bfloat16 : Fmt := { e := 8,  m := 7 }

/-- the five special classes. -/
inductive FClass where
  | zero | subnormal | normal | inf | nan
deriving DecidableEq, Repr, Inhabited, BEq

structure Dec where
  cls : FClass
  neg : Bool
  /-- the exact value, for zero / subnormal / normal -/
  val : Uni
  /-- a signalling NaN -/
  sig : Bool
deriving Repr, Inhabited

/-- read one encoding as its class and its exact universal value. -/
def decode (f : Fmt) (x : Nat) : Dec :=
  let neg := x.testBit (f.e + f.m)
  let E := (x / 2 ^ f.m) % 2 ^ f.e
  let M := x % 2 ^ f.m
  if E == 0 then
    if M == 0 then { cls := .zero, neg := neg, val := Uni.mk' neg 0 0, sig := false }
    else { cls := .subnormal, neg := neg, val := Uni.mk' neg M f.qmin, sig := false }
  else if E == 2 ^ f.e - 1 then
    if M == 0 then { cls := .inf, neg := neg, val := Uni.zero, sig := false }
    else { cls := .nan, neg := neg, val := Uni.zero, sig := !M.testBit (f.m - 1) }
  else
    { cls := .normal, neg := neg,
      val := Uni.mk' neg (2 ^ f.m + M) ((E : Int) - f.bias - (f.m : Int)), sig := false }

def encZero (f : Fmt) (neg : Bool) : Nat := if neg then 2 ^ (f.e + f.m) else 0
def encInf (f : Fmt) (neg : Bool) : Nat := encZero f neg + (2 ^ f.e - 1) * 2 ^ f.m
/-- the canonical quiet NaN: what RISC-V produces for every NaN result. -/
def encNaN (f : Fmt) : Nat := (2 ^ f.e - 1) * 2 ^ f.m + 2 ^ (f.m - 1)
def encMax (f : Fmt) (neg : Bool) : Nat :=
  encZero f neg + (2 ^ f.e - 2) * 2 ^ f.m + (2 ^ f.m - 1)

/-- `sig * 2^q` with `sig` of at most `m+1` bits and `q ≥ qmin`:
`sig < 2^m` is the subnormal grid (exponent field 0), otherwise normal. -/
def encFinite (f : Fmt) (neg : Bool) (sig : Nat) (q : Int) : Nat :=
  if sig < 2 ^ f.m then encZero f neg + sig
  else encZero f neg + (q + (f.m : Int) + f.bias).toNat * 2 ^ f.m + (sig - 2 ^ f.m)

/-- tininess AFTER rounding (IEEE 754-2008 7.5, the detection RISC-V
requires and the one SoftFloat's RISCV specialization makes): the exact
nonzero value, rounded to the format's precision (m+1 bits) with the
exponent UNBOUNDED, lies strictly below the smallest normal `2^emin`.
`topExp` is the exponent of the exact value's leading bit and
`(s, g, st)` its magnitude split at `topExp - m`, the quantum of that
rounding. Deciding it from the result rounded at the subnormal quantum
instead differs exactly when the first m+1 bits just below `2^emin` are
all ones: found by the level-0 check against Sail's softfloat,
2026-09-15. -/
def tinyAfter (f : Fmt) (rm : RM) (neg : Bool) (topExp : Int) (s : Nat) (g st : Bool) : Bool :=
  if f.emin ≤ topExp then false
  else
    let s1 := if wantsInc rm neg (s % 2 == 1) g st then s + 1 else s
    -- the rounded magnitude is s1 * 2^(topExp - m): it reaches 2^emin only by
    -- the carry out of m+1 bits, and only from the exponent just below emin
    !(topExp + 1 == f.emin && s1 == 2 ^ (f.m + 1))

/-- the one place the increment, the carry out of the significand,
overflow, underflow and the five flags are decided. `sig0 * 2^q0` is the
truncated magnitude, `g` and `st` the guard and sticky bits, `tinyU` the
exact value's tininess after rounding (`tinyAfter`). -/
def assemble (f : Fmt) (rm : RM) (neg : Bool) (sig0 : Nat) (q0 : Int) (g st : Bool) (tinyU : Bool) :
    BitVec 5 × Nat :=
  let inexact := g || st
  let inc := wantsInc rm neg (sig0 % 2 == 1) g st
  let sig1 := if inc then sig0 + 1 else sig0
  let sig := if sig1 == 2 ^ (f.m + 1) then sig1 / 2 else sig1
  let q := if sig1 == 2 ^ (f.m + 1) then q0 + 1 else q0
  if f.emax < q + (f.m : Int) then
    let toInf := match rm with
      | .rne => true | .rmm => true | .rtz => false | .rdn => neg | .rup => !neg
    (ofFlag ||| nxFlag, if toInf then encInf f neg else encMax f neg)
  else
    -- underflow: tiny after rounding (`tinyU`) AND the delivered result inexact
    ((if inexact then nxFlag else noFlag) ||| (if tinyU && inexact then ufFlag else noFlag),
     encFinite f neg sig q)

/-- round an exact nonzero universal object into the format. -/
def roundUni (f : Fmt) (rm : RM) (u : Uni) : BitVec 5 × Nat :=
  if u.mant == 0 then (noFlag, encZero f (rm == .rdn))
  else
    let q := imax (u.topExp - (f.m : Int)) f.qmin
    let s := u.splitAt q
    let sU := u.splitAt (u.topExp - (f.m : Int))
    assemble f rm u.isNeg s.1 q s.2.1 s.2.2 (tinyAfter f rm u.isNeg u.topExp sU.1 sU.2.1 sU.2.2)

/-! ### the operations, exact then rounded -/

def nanOut (f : Fmt) (a b : Dec) : BitVec 5 × Nat :=
  ((if a.sig || b.sig then nvFlag else noFlag), encNaN f)

/-- the same for an operation of ANY arity, and for a conversion, whose
format `f` is the TARGET's while the operands were read at the source's:
the target's canonical quiet NaN, invalid when any operand signals. -/
def nanOutN (f : Fmt) (ds : List Dec) : BitVec 5 × Nat :=
  ((if ds.any (fun d => d.sig) then nvFlag else noFlag), encNaN f)

def addRaw (f : Fmt) (rm : RM) (a b : Nat) : BitVec 5 × Nat :=
  let da := decode f a
  let db := decode f b
  if da.cls == .nan || db.cls == .nan then nanOut f da db
  else if da.cls == .inf && db.cls == .inf then
    (if da.neg == db.neg then (noFlag, encInf f da.neg) else (nvFlag, encNaN f))
  else if da.cls == .inf then (noFlag, encInf f da.neg)
  else if db.cls == .inf then (noFlag, encInf f db.neg)
  else
    let s := da.val.add db.val
    if s.mant == 0 then
      -- the sign of an exact zero sum: the common sign when both addends
      -- are that zero, otherwise + except under roundTowardNegative
      let zneg := if da.cls == .zero && db.cls == .zero && da.neg == db.neg
                  then da.neg else rm == .rdn
      (noFlag, encZero f zneg)
    else roundUni f rm s

/-- flip the sign bit of an encoding; NaN stays the NaN it was. -/
def negBit (f : Fmt) (x : Nat) : Nat :=
  if x.testBit (f.e + f.m) then x - 2 ^ (f.e + f.m) else x + 2 ^ (f.e + f.m)

def subRaw (f : Fmt) (rm : RM) (a b : Nat) : BitVec 5 × Nat := addRaw f rm a (negBit f b)

def mulRaw (f : Fmt) (rm : RM) (a b : Nat) : BitVec 5 × Nat :=
  let da := decode f a
  let db := decode f b
  let sgn := da.neg != db.neg
  if da.cls == .nan || db.cls == .nan then nanOut f da db
  else if (da.cls == .inf && db.cls == .zero) || (da.cls == .zero && db.cls == .inf) then
    (nvFlag, encNaN f)
  else if da.cls == .inf || db.cls == .inf then (noFlag, encInf f sgn)
  else if da.cls == .zero || db.cls == .zero then (noFlag, encZero f sgn)
  else roundUni f rm (da.val.mul db.val)

def divRaw (f : Fmt) (rm : RM) (a b : Nat) : BitVec 5 × Nat :=
  let da := decode f a
  let db := decode f b
  let sgn := da.neg != db.neg
  if da.cls == .nan || db.cls == .nan then nanOut f da db
  else if da.cls == .inf && db.cls == .inf then (nvFlag, encNaN f)
  else if da.cls == .zero && db.cls == .zero then (nvFlag, encNaN f)
  -- an infinite dividend is exactly infinite and signals nothing, a zero
  -- divisor included: divide-by-zero is the exception of a FINITE nonzero
  -- dividend (IEEE 754-2008 7.3). This line stood below the zero divisor's
  -- until the level-0 check against Sail's softfloat, 2026-09-15.
  else if da.cls == .inf then (noFlag, encInf f sgn)
  else if db.cls == .zero then (dzFlag, encInf f sgn)
  else if db.cls == .inf then (noFlag, encZero f sgn)
  else if da.cls == .zero then (noFlag, encZero f sgn)
  else
    -- both finite and nonzero. The quotient of two dyadic numbers is not
    -- dyadic, so it is produced already scaled to one bit below a
    -- quantum exponent: that bit is the guard, and a nonzero remainder
    -- is the sticky bit.
    let na := da.val.mant
    let nb := db.val.mant
    let ea := da.val.e
    let eb := db.val.e
    let la := Ubv.len na
    let lb := Ubv.len nb
    -- |a/b| ≥ 2^(la-lb) decides which of the two candidate leading
    -- exponents is the true one (Nat subtraction truncates, which is the
    -- max with 0 wanted on each side)
    let big := nb * 2 ^ (la - lb) ≤ na * 2 ^ (lb - la)
    let eTop := (la : Int) - (lb : Int) + ea - eb - (if big then 0 else 1)
    -- |a/b| split at the quantum `qq`: (the quotient's bits above `qq`, the
    -- guard, the sticky)
    let splitQ : Int → Nat × Bool × Bool := fun qq =>
      let t : Int := ea - eb - qq + 1
      let num := if 0 ≤ t then na * 2 ^ t.toNat else na
      let den := if 0 ≤ t then nb else nb * 2 ^ (-t).toNat
      let Q := num / den
      (Q / 2, Q % 2 == 1, !(num % den == 0))
    let q := imax (eTop - (f.m : Int)) f.qmin
    let s := splitQ q
    let sU := splitQ (eTop - (f.m : Int))
    assemble f rm sgn s.1 q s.2.1 s.2.2 (tinyAfter f rm sgn eTop sU.1 sU.2.1 sU.2.2)

/-- the fused multiply-add: `a * b + c` rounded ONCE. `Uni.mul` and `Uni.add`
are both exact, so the exact sum is formed and `roundUni` applied a single
time -- which is the whole of the operation.

The refusals are Sail's softfloat's, in ITS order: a NaN factor first, then
`inf * 0`, which refuses whatever the addend is, a QUIET NaN included (IEEE
754-2008 7.2 leaves that one implementation-defined and RISC-V's softfloat
signals it), then a NaN addend, then the infinities. -/
def mulAddRaw (f : Fmt) (rm : RM) (a b c : Nat) : BitVec 5 × Nat :=
  let da := decode f a
  let db := decode f b
  let dc := decode f c
  -- the product's sign
  let sgn := da.neg != db.neg
  if da.cls == .nan || db.cls == .nan then nanOutN f [da, db, dc]
  else if (da.cls == .inf && db.cls == .zero) || (da.cls == .zero && db.cls == .inf) then
    (nvFlag, encNaN f)
  else if dc.cls == .nan then nanOutN f [dc]
  else if da.cls == .inf || db.cls == .inf then
    (if dc.cls == .inf && dc.neg != sgn then (nvFlag, encNaN f) else (noFlag, encInf f sgn))
  else if dc.cls == .inf then (noFlag, encInf f dc.neg)
  else
    let s := (da.val.mul db.val).add dc.val
    if s.mant == 0 then
      -- the sign of an exact zero, as in `addRaw`: the common sign when the
      -- product and the addend carry it -- which they can only do when both
      -- are zero -- otherwise + except under roundTowardNegative
      (noFlag, encZero f (if sgn == dc.neg then sgn else rm == .rdn))
    else roundUni f rm s

/-! ### the one arithmetic the universal object has not got

`Uni` has add, multiply and divide but no root, and the square root of a
dyadic number is not dyadic. `isqrtFrom n i r` decides bits `i, i-1, ..., 0`
of the root, greedily from the top, with `r` carrying the bits already
decided: the recursion is on the bit INDEX, so it is structural and total,
and the greedy choice is the largest `r` with `r * r ≤ n`. Starting ABOVE
the answer's leading bit is harmless -- a bit the root cannot carry fails
`c * c ≤ n` and stays zero. -/
def isqrtFrom (n : Nat) : Nat → Nat → Nat
  | 0,     r => if (r + 1) * (r + 1) ≤ n then r + 1 else r
  | i + 1, r => let c := r + 2 ^ (i + 1); isqrtFrom n i (if c * c ≤ n then c else r)

/-- `⌊√n⌋`. `n < 2 ^ Ubv.len n` puts the root below `2 ^ ((Ubv.len n + 1) / 2)`,
so that index is at or above its leading bit. -/
def isqrt (n : Nat) : Nat := isqrtFrom n ((Ubv.len n + 1) / 2) 0

/-- the square root, exact then rounded, in the shape `divRaw` uses: the
digits down to one bit BELOW a quantum -- that bit is the guard -- and a
sticky bit saying whether anything nonzero remains. `2^topExp ≤ |a| <
2^(topExp+1)` puts the root's leading bit at `⌊topExp / 2⌋`, and no root of a
finite nonzero number can overflow or fall subnormal (`emin ≤ -m` in every
format here, so `qmin / 2 ≥ emin`). -/
def sqrtRaw (f : Fmt) (rm : RM) (a : Nat) : BitVec 5 × Nat :=
  let da := decode f a
  if da.cls == .nan then nanOutN f [da]
  -- each zero is its own root, the negative one included
  else if da.cls == .zero then (noFlag, encZero f da.neg)
  -- every other negative refuses, `-inf` with them
  else if da.neg then (nvFlag, encNaN f)
  else if da.cls == .inf then (noFlag, encInf f false)
  else
    let na := da.val.mant
    let ea := da.val.e
    let eTop := Int.fdiv da.val.topExp 2
    -- `√a` split at the quantum `qq`: `N = ⌊√a / 2^(qq-1)⌋`, whose low bit
    -- is the guard. `⌊√x⌋ = ⌊√⌊x⌋⌋` makes the shifted-down case an integer
    -- root too, and what the shift dropped joins the sticky.
    let splitR : Int → Nat × Bool × Bool := fun qq =>
      let d : Int := ea - 2 * (qq - 1)
      let X := if 0 ≤ d then na * 2 ^ d.toNat else na / 2 ^ (-d).toNat
      let cut := if 0 ≤ d then 0 else na % 2 ^ (-d).toNat
      let N := isqrt X
      (N / 2, N % 2 == 1, !(N * N == X) || !(cut == 0))
    let q := imax (eTop - (f.m : Int)) f.qmin
    let s := splitR q
    let sU := splitR (eTop - (f.m : Int))
    assemble f rm false s.1 q s.2.1 s.2.2 (tinyAfter f rm false eTop sU.1 sU.2.1 sU.2.2)

/-- round to a whole number, in the SAME format. The exact value is split at
the unit quantum and `wantsInc` decides the increment -- the same rounding
`assemble` does, at a quantum the format fixes instead of the value. The
whole number is then re-encoded by `roundUni`, which is exact for it: a
magnitude at or above `2^m` was already whole, and one below rounds to at
most `2^m`, which every format here holds exactly. Infinities pass through
and `exact` is Sail's own third argument -- the inexact flag is raised only
when it is set. -/
def roundToIntRaw (f : Fmt) (rm : RM) (a : Nat) (exact : Bool) : BitVec 5 × Nat :=
  let da := decode f a
  if da.cls == .nan then nanOutN f [da]
  else if da.cls == .inf then (noFlag, encInf f da.neg)
  else if da.cls == .zero then (noFlag, encZero f da.neg)
  else
    let s := da.val.splitAt 0
    let inexact := s.2.1 || s.2.2
    let n := if wantsInc rm da.neg (s.1 % 2 == 1) s.2.1 s.2.2 then s.1 + 1 else s.1
    ((if inexact && exact then nxFlag else noFlag),
     -- a magnitude rounded away keeps the OPERAND's sign, which is not the
     -- sign `roundUni` gives a zero
     if n == 0 then encZero f da.neg else (roundUni f rm (Uni.mk' da.neg n 0)).2)

/-! ### the integer targets of the conversions -/

/-- an `n`-bit integer target, signed or not. -/
structure IntFmt where
  n      : Nat
  signed : Bool
deriving DecidableEq, Repr, Inhabited, BEq

namespace IntFmt
def lo (t : IntFmt) : Int := if t.signed then -((2 : Int) ^ (t.n - 1)) else 0
def hi (t : IntFmt) : Int := if t.signed then (2 : Int) ^ (t.n - 1) - 1 else (2 : Int) ^ t.n - 1
end IntFmt

def int32  : IntFmt := { n := 32, signed := true }
def uint32 : IntFmt := { n := 32, signed := false }
def int64  : IntFmt := { n := 64, signed := true }
def uint64 : IntFmt := { n := 64, signed := false }

/-- float to integer: round on the whole-number grid at the mode, then
saturate. The saturation is RISC-V's, read off Berkeley SoftFloat's RISCV
`specialize.h`, which sets `i32_fromNaN = i32_fromPosOverflow` and
`ui32_fromNaN = ui32_fromPosOverflow`: a NaN gives the target's LARGEST
value, signed and unsigned alike, and anything out of range gives the nearer
endpoint. Both raise invalid and NOTHING beside it -- `softfloat_roundToI32`
leaves for its `invalid` label before it can reach the inexact flag. Note
`Uni.toInt` is not this rounding: it only truncates toward zero. -/
def toIntRaw (f : Fmt) (t : IntFmt) (rm : RM) (a : Nat) : BitVec 5 × Int :=
  let da := decode f a
  if da.cls == .nan then (nvFlag, t.hi)
  else if da.cls == .inf then (nvFlag, if da.neg then t.lo else t.hi)
  else
    let s := da.val.splitAt 0
    let mag := if wantsInc rm da.neg (s.1 % 2 == 1) s.2.1 s.2.2 then s.1 + 1 else s.1
    let v : Int := if da.neg then -(mag : Int) else (mag : Int)
    if v < t.lo || t.hi < v then (nvFlag, if da.neg then t.lo else t.hi)
    else ((if s.2.1 || s.2.2 then nxFlag else noFlag), v)

/-- integer to float: the exact integer, rounded. A zero operand gives `+0`
in EVERY mode -- SoftFloat's `i32_to_f64` and its fellows answer a zero
before they ever read the rounding mode, where `roundUni` would give `-0`
under roundTowardNegative. -/
def ofIntRaw (f : Fmt) (rm : RM) (v : Int) : BitVec 5 × Nat :=
  if v == 0 then (noFlag, encZero f false) else roundUni f rm (Uni.ofInt v)

/-- float to float: the source's exact value, rounded into the target. ONE
code path for both directions -- widening loses nothing and `roundUni` says
so, narrowing rounds and may overflow or fall subnormal. -/
def cvtRaw (fs ft : Fmt) (rm : RM) (a : Nat) : BitVec 5 × Nat :=
  let da := decode fs a
  if da.cls == .nan then nanOutN ft [da]
  else if da.cls == .inf then (noFlag, encInf ft da.neg)
  else if da.cls == .zero then (noFlag, encZero ft da.neg)
  else roundUni ft rm da.val

/-- the comparisons: exact, no rounding. `quiet` is the variant that does
not signal on a quiet NaN. -/
def cmpRaw (f : Fmt) (quiet : Bool) (want : Ordering → Bool) (a b : Nat) : BitVec 5 × Bool :=
  let da := decode f a
  let db := decode f b
  if da.cls == .nan || db.cls == .nan then
    ((if da.sig || db.sig || !quiet then nvFlag else noFlag), false)
  else
    let ord : Ordering :=
      if da.cls == .inf && db.cls == .inf then
        (if da.neg == db.neg then .eq else if da.neg then .lt else .gt)
      else if da.cls == .inf then (if da.neg then .lt else .gt)
      else if db.cls == .inf then (if db.neg then .gt else .lt)
      else da.val.cmp db.val
    (noFlag, want ord)

/-- the IEEE kind. `holds` is the constraint on the FINITE numbers -- the
special classes are not values of the universal object at all. -/
def ieeeK (f : Fmt) : Kind where
  name := "binary" ++ toString f.w
  holds u :=
    u.mant == 0 ||
      (let q := imax (u.topExp - (f.m : Int)) f.qmin
       let s := u.splitAt q
       !s.2.1 && !s.2.2 && decide (u.topExp ≤ f.emax))
  proj rm u :=
    if u.mant == 0 then (noFlag, .num Uni.zero)
    else
      let r := roundUni f (RM.ofBits rm) u
      let d := decode f r.2
      (r.1, match d.cls with
            | .inf => .inf d.neg
            | .nan => .nan
            | _ => .num d.val)

/-! ## kind 5 -- fixed-point -/

structure FixFmt where
  /-- the stored signed mantissa's width -/
  w : Nat
  /-- the type's exponent: the value is `mant * 2^q` -/
  q : Int
  /-- saturate (true) or wrap (false) when the mantissa leaves the width -/
  sat : Bool
deriving DecidableEq, Repr, Inhabited, BEq

def fixedK (t : FixFmt) : Kind where
  name := "fixed " ++ toString t.w ++ " at 2^(" ++ toString t.q ++ ")"
  holds u := decide (u.e = t.q) &&
    (if u.isNeg then decide (u.mant ≤ 2 ^ (t.w - 1)) else decide (u.mant < 2 ^ (t.w - 1)))
  proj rm u :=
    let s := u.splitAt t.q
    let g := s.2.1
    let st := s.2.2
    let inexact := g || st
    let neg := u.isNeg
    let inc := wantsInc (RM.ofBits rm) neg (s.1 % 2 == 1) g st
    let mag : Int := ((if inc then s.1 + 1 else s.1 : Nat) : Int)
    let v : Int := if neg then -mag else mag
    let lo : Int := -((2 : Int) ^ (t.w - 1))
    let hi : Int := (2 : Int) ^ (t.w - 1) - 1
    let over := v < lo || hi < v
    let v' : Int :=
      if !over then v
      else if t.sat then (if v < lo then lo else hi)
      else (BitVec.ofInt t.w v).toInt
    ((if inexact then nxFlag else noFlag) ||| (if over then ofFlag else noFlag),
     .num (Uni.ofSignedAt v' t.q))

/-! ## the bodies Sail's axioms could take

Each has EXACTLY the type its axiom in `LeanIM/RiscvExtras.lean` declares.
The cached emit is left as Sail produced it: the substitution is a
documented, reversible one-line rewrite applied to the WORKING COPY only,

    axiom riscv_f64Add : BitVec 3 → BitVec 64 → BitVec 64 → (BitVec 5 × BitVec 64)
    ->  def   riscv_f64Add := Kinds.Axioms.riscv_f64Add

undone by restoring the file from `cache/`. Nothing here needs it: the
alternative is a theorem `riscv_f64Add rm a b = Kinds.Axioms.riscv_f64Add rm a b`
per axiom, which is the same statement without touching any file -- but
it cannot be PROVED, only assumed, because the axiom has no body. Hence
the rewrite. -/

def ieeeAdd {w : Nat} (f : Fmt) (rm : BitVec 3) (a b : BitVec w) : BitVec 5 × BitVec w :=
  let r := addRaw f (RM.ofBits rm) a.toNat b.toNat
  (r.1, BitVec.ofNat w r.2)

def ieeeSub {w : Nat} (f : Fmt) (rm : BitVec 3) (a b : BitVec w) : BitVec 5 × BitVec w :=
  let r := subRaw f (RM.ofBits rm) a.toNat b.toNat
  (r.1, BitVec.ofNat w r.2)

def ieeeMul {w : Nat} (f : Fmt) (rm : BitVec 3) (a b : BitVec w) : BitVec 5 × BitVec w :=
  let r := mulRaw f (RM.ofBits rm) a.toNat b.toNat
  (r.1, BitVec.ofNat w r.2)

def ieeeDiv {w : Nat} (f : Fmt) (rm : BitVec 3) (a b : BitVec w) : BitVec 5 × BitVec w :=
  let r := divRaw f (RM.ofBits rm) a.toNat b.toNat
  (r.1, BitVec.ofNat w r.2)

def ieeeCmp {w : Nat} (f : Fmt) (quiet : Bool) (want : Ordering → Bool)
    (a b : BitVec w) : BitVec 5 × Bool :=
  cmpRaw f quiet want a.toNat b.toNat

def ieeeMulAdd {w : Nat} (f : Fmt) (rm : BitVec 3) (a b c : BitVec w) : BitVec 5 × BitVec w :=
  let r := mulAddRaw f (RM.ofBits rm) a.toNat b.toNat c.toNat
  (r.1, BitVec.ofNat w r.2)

def ieeeSqrt {w : Nat} (f : Fmt) (rm : BitVec 3) (a : BitVec w) : BitVec 5 × BitVec w :=
  let r := sqrtRaw f (RM.ofBits rm) a.toNat
  (r.1, BitVec.ofNat w r.2)

def ieeeRoundToInt {w : Nat} (f : Fmt) (rm : BitVec 3) (a : BitVec w) (exact : Bool) :
    BitVec 5 × BitVec w :=
  let r := roundToIntRaw f (RM.ofBits rm) a.toNat exact
  (r.1, BitVec.ofNat w r.2)

/-- the two widths are free: the float's and the integer's. -/
def ieeeToInt {wf wi : Nat} (f : Fmt) (t : IntFmt) (rm : BitVec 3) (a : BitVec wf) :
    BitVec 5 × BitVec wi :=
  let r := toIntRaw f t (RM.ofBits rm) a.toNat
  (r.1, BitVec.ofInt wi r.2)

def ieeeOfInt {wi wf : Nat} (f : Fmt) (signed : Bool) (rm : BitVec 3) (a : BitVec wi) :
    BitVec 5 × BitVec wf :=
  let r := ofIntRaw f (RM.ofBits rm) (if signed then a.toInt else (a.toNat : Int))
  (r.1, BitVec.ofNat wf r.2)

def ieeeCvt {ws wt : Nat} (fs ft : Fmt) (rm : BitVec 3) (a : BitVec ws) : BitVec 5 × BitVec wt :=
  let r := cvtRaw fs ft (RM.ofBits rm) a.toNat
  (r.1, BitVec.ofNat wt r.2)

def isLt (o : Ordering) : Bool := o == Ordering.lt
def isLe (o : Ordering) : Bool := o == Ordering.lt || o == Ordering.eq
def isEq (o : Ordering) : Bool := o == Ordering.eq

namespace Axioms

def riscv_f16Add : BitVec 3 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) := ieeeAdd binary16
def riscv_f16Sub : BitVec 3 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) := ieeeSub binary16
def riscv_f16Mul : BitVec 3 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) := ieeeMul binary16
def riscv_f16Div : BitVec 3 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) := ieeeDiv binary16
def riscv_f32Add : BitVec 3 → BitVec 32 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeAdd binary32
def riscv_f32Sub : BitVec 3 → BitVec 32 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeSub binary32
def riscv_f32Mul : BitVec 3 → BitVec 32 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeMul binary32
def riscv_f32Div : BitVec 3 → BitVec 32 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeDiv binary32
def riscv_f64Add : BitVec 3 → BitVec 64 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeAdd binary64
def riscv_f64Sub : BitVec 3 → BitVec 64 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeSub binary64
def riscv_f64Mul : BitVec 3 → BitVec 64 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeMul binary64
def riscv_f64Div : BitVec 3 → BitVec 64 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeDiv binary64

def riscv_f16Lt       : BitVec 16 → BitVec 16 → (BitVec 5 × Bool) := ieeeCmp binary16 false isLt
def riscv_f16Lt_quiet : BitVec 16 → BitVec 16 → (BitVec 5 × Bool) := ieeeCmp binary16 true  isLt
def riscv_f16Le       : BitVec 16 → BitVec 16 → (BitVec 5 × Bool) := ieeeCmp binary16 false isLe
def riscv_f16Le_quiet : BitVec 16 → BitVec 16 → (BitVec 5 × Bool) := ieeeCmp binary16 true  isLe
def riscv_f16Eq       : BitVec 16 → BitVec 16 → (BitVec 5 × Bool) := ieeeCmp binary16 true  isEq
def riscv_f32Lt       : BitVec 32 → BitVec 32 → (BitVec 5 × Bool) := ieeeCmp binary32 false isLt
def riscv_f32Lt_quiet : BitVec 32 → BitVec 32 → (BitVec 5 × Bool) := ieeeCmp binary32 true  isLt
def riscv_f32Le       : BitVec 32 → BitVec 32 → (BitVec 5 × Bool) := ieeeCmp binary32 false isLe
def riscv_f32Le_quiet : BitVec 32 → BitVec 32 → (BitVec 5 × Bool) := ieeeCmp binary32 true  isLe
def riscv_f32Eq       : BitVec 32 → BitVec 32 → (BitVec 5 × Bool) := ieeeCmp binary32 true  isEq
def riscv_f64Lt       : BitVec 64 → BitVec 64 → (BitVec 5 × Bool) := ieeeCmp binary64 false isLt
def riscv_f64Lt_quiet : BitVec 64 → BitVec 64 → (BitVec 5 × Bool) := ieeeCmp binary64 true  isLt
def riscv_f64Le       : BitVec 64 → BitVec 64 → (BitVec 5 × Bool) := ieeeCmp binary64 false isLe
def riscv_f64Le_quiet : BitVec 64 → BitVec 64 → (BitVec 5 × Bool) := ieeeCmp binary64 true  isLe
def riscv_f64Eq       : BitVec 64 → BitVec 64 → (BitVec 5 × Bool) := ieeeCmp binary64 true  isEq

def riscv_f16MulAdd : BitVec 3 → BitVec 16 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) := ieeeMulAdd binary16
def riscv_f32MulAdd : BitVec 3 → BitVec 32 → BitVec 32 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeMulAdd binary32
def riscv_f64MulAdd : BitVec 3 → BitVec 64 → BitVec 64 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeMulAdd binary64

def riscv_f16Sqrt : BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 16) := ieeeSqrt binary16
def riscv_f32Sqrt : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeSqrt binary32
def riscv_f64Sqrt : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeSqrt binary64

def riscv_f16roundToInt : BitVec 3 → BitVec 16 → Bool → (BitVec 5 × BitVec 16) := ieeeRoundToInt binary16
def riscv_f32roundToInt : BitVec 3 → BitVec 32 → Bool → (BitVec 5 × BitVec 32) := ieeeRoundToInt binary32
def riscv_f64roundToInt : BitVec 3 → BitVec 64 → Bool → (BitVec 5 × BitVec 64) := ieeeRoundToInt binary64

def riscv_f16ToI32  : BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 32) := ieeeToInt binary16 int32
def riscv_f16ToUi32 : BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 32) := ieeeToInt binary16 uint32
def riscv_f16ToI64  : BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 64) := ieeeToInt binary16 int64
def riscv_f16ToUi64 : BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 64) := ieeeToInt binary16 uint64
def riscv_f32ToI32  : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeToInt binary32 int32
def riscv_f32ToUi32 : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeToInt binary32 uint32
def riscv_f32ToI64  : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 64) := ieeeToInt binary32 int64
def riscv_f32ToUi64 : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 64) := ieeeToInt binary32 uint64
def riscv_f64ToI32  : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 32) := ieeeToInt binary64 int32
def riscv_f64ToUi32 : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 32) := ieeeToInt binary64 uint32
def riscv_f64ToI64  : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeToInt binary64 int64
def riscv_f64ToUi64 : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeToInt binary64 uint64

def riscv_i32ToF16  : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 16) := ieeeOfInt binary16 true
def riscv_ui32ToF16 : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 16) := ieeeOfInt binary16 false
def riscv_i64ToF16  : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 16) := ieeeOfInt binary16 true
def riscv_ui64ToF16 : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 16) := ieeeOfInt binary16 false
def riscv_i32ToF32  : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeOfInt binary32 true
def riscv_ui32ToF32 : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 32) := ieeeOfInt binary32 false
def riscv_i64ToF32  : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 32) := ieeeOfInt binary32 true
def riscv_ui64ToF32 : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 32) := ieeeOfInt binary32 false
def riscv_i32ToF64  : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 64) := ieeeOfInt binary64 true
def riscv_ui32ToF64 : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 64) := ieeeOfInt binary64 false
def riscv_i64ToF64  : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeOfInt binary64 true
def riscv_ui64ToF64 : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 64) := ieeeOfInt binary64 false

def riscv_f16ToF32  : BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 32) := ieeeCvt binary16 binary32
def riscv_f16ToF64  : BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 64) := ieeeCvt binary16 binary64
def riscv_f32ToF64  : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 64) := ieeeCvt binary32 binary64
def riscv_f32ToF16  : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 16) := ieeeCvt binary32 binary16
def riscv_f64ToF16  : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 16) := ieeeCvt binary64 binary16
def riscv_f64ToF32  : BitVec 3 → BitVec 64 → (BitVec 5 × BitVec 32) := ieeeCvt binary64 binary32
def riscv_f32ToBF16 : BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 16) := ieeeCvt binary32 bfloat16

end Axioms

/-! ## the checks

Known values, read off the object itself. Nothing below is part of the
definition. -/

structure Chk where
  name : String
  ok   : Bool
  got  : String
  want : String

def chk {α : Type} [BEq α] [Repr α] (name : String) (got want : α) : Chk :=
  { name := name, ok := got == want,
    got := toString (repr got), want := toString (repr want) }

def report (title : String) (cs : List Chk) : IO Unit := do
  IO.println ("== " ++ title)
  for c in cs do
    if c.ok then IO.println ("  ok   " ++ c.name ++ " = " ++ c.got)
    else IO.println ("  FAIL " ++ c.name ++ ": got " ++ c.got ++ " want " ++ c.want)
  IO.println ("  -- " ++ toString (cs.filter (fun c => c.ok)).length ++ "/" ++
              toString cs.length ++ " ok")

open Axioms in
#eval report "binary64 add / sub, round to nearest even (rm 000)" [
  chk "1.0 + 2.0"
    (riscv_f64Add 0#3 0x3FF0000000000000#64 0x4000000000000000#64)
    ((0#5 : BitVec 5), (0x4008000000000000#64 : BitVec 64)),
  chk "0.1 + 0.2 (inexact)"
    (riscv_f64Add 0#3 0x3FB999999999999A#64 0x3FC999999999999A#64)
    ((1#5 : BitVec 5), (0x3FD3333333333334#64 : BitVec 64)),
  chk "2^53 + 1 (tie, to even, down)"
    (riscv_f64Add 0#3 0x4340000000000000#64 0x3FF0000000000000#64)
    ((1#5 : BitVec 5), (0x4340000000000000#64 : BitVec 64)),
  chk "2^53 + 3 (tie, to even, up)"
    (riscv_f64Add 0#3 0x4340000000000000#64 0x4008000000000000#64)
    ((1#5 : BitVec 5), (0x4340000000000002#64 : BitVec 64)),
  chk "1.0 - 1.0 = +0"
    (riscv_f64Sub 0#3 0x3FF0000000000000#64 0x3FF0000000000000#64)
    ((0#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "1.0 - 1.0 = -0 under RDN (rm 010)"
    (riscv_f64Sub 2#3 0x3FF0000000000000#64 0x3FF0000000000000#64)
    ((0#5 : BitVec 5), (0x8000000000000000#64 : BitVec 64))
]

open Axioms in
#eval report "binary64 subnormals and underflow" [
  chk "2^-1074 + 2^-1074 (exact, no underflow)"
    (riscv_f64Add 0#3 0x0000000000000001#64 0x0000000000000001#64)
    ((0#5 : BitVec 5), (0x0000000000000002#64 : BitVec 64)),
  chk "largest subnormal + 2^-1074 = smallest normal (exact)"
    (riscv_f64Add 0#3 0x000FFFFFFFFFFFFF#64 0x0000000000000001#64)
    ((0#5 : BitVec 5), (0x0010000000000000#64 : BitVec 64)),
  chk "smallest normal - 2^-1074 = largest subnormal (exact)"
    (riscv_f64Sub 0#3 0x0010000000000000#64 0x0000000000000001#64)
    ((0#5 : BitVec 5), (0x000FFFFFFFFFFFFF#64 : BitVec 64)),
  chk "smallest normal / 2 (exact subnormal, no underflow)"
    (riscv_f64Div 0#3 0x0010000000000000#64 0x4000000000000000#64)
    ((0#5 : BitVec 5), (0x0008000000000000#64 : BitVec 64)),
  chk "2^-1074 * 0.5 -> 0, underflow and inexact"
    (riscv_f64Mul 0#3 0x0000000000000001#64 0x3FE0000000000000#64)
    ((3#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "3*2^-1074 * 0.5 -> 2*2^-1074, underflow and inexact"
    (riscv_f64Mul 0#3 0x0000000000000003#64 0x3FE0000000000000#64)
    ((3#5 : BitVec 5), (0x0000000000000002#64 : BitVec 64)),
  chk "5*2^-1074 * 0.5 -> 2*2^-1074 (tie to even)"
    (riscv_f64Mul 0#3 0x0000000000000005#64 0x3FE0000000000000#64)
    ((3#5 : BitVec 5), (0x0000000000000002#64 : BitVec 64)),
  chk "a product just below the smallest normal, first 53 bits all ones: rounds to it, yet tiny at 53 bits, underflow (level 0, Sail's softfloat)"
    (riscv_f64Mul 0#3 0x3FE4000000000000#64 0x0019999999999999#64)
    ((3#5 : BitVec 5), (0x0010000000000000#64 : BitVec 64)),
  chk "the same pair under RMM (rm 100): underflow (level 0, Sail's softfloat)"
    (riscv_f64Mul 4#3 0x3FE4000000000000#64 0x0019999999999999#64)
    ((3#5 : BitVec 5), (0x0010000000000000#64 : BitVec 64))
]

open Axioms in
#eval report "binary64 the special classes" [
  chk "+inf + -inf = canonical NaN, invalid"
    (riscv_f64Add 0#3 0x7FF0000000000000#64 0xFFF0000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "quiet NaN + 1.0 = canonical NaN, no flag"
    (riscv_f64Add 0#3 0x7FF8000000000000#64 0x3FF0000000000000#64)
    ((0#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "signalling NaN + 1.0 = canonical NaN, invalid"
    (riscv_f64Add 0#3 0x7FF0000000000001#64 0x3FF0000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "maxfinite + maxfinite = +inf, overflow and inexact"
    (riscv_f64Add 0#3 0x7FEFFFFFFFFFFFFF#64 0x7FEFFFFFFFFFFFFF#64)
    ((5#5 : BitVec 5), (0x7FF0000000000000#64 : BitVec 64)),
  chk "the same under RTZ (rm 001): maxfinite"
    (riscv_f64Add 1#3 0x7FEFFFFFFFFFFFFF#64 0x7FEFFFFFFFFFFFFF#64)
    ((5#5 : BitVec 5), (0x7FEFFFFFFFFFFFFF#64 : BitVec 64)),
  chk "1.0 / 0.0 = +inf, divide by zero"
    (riscv_f64Div 0#3 0x3FF0000000000000#64 0x0000000000000000#64)
    ((8#5 : BitVec 5), (0x7FF0000000000000#64 : BitVec 64)),
  chk "-1.0 / 0.0 = -inf, divide by zero"
    (riscv_f64Div 0#3 0xBFF0000000000000#64 0x0000000000000000#64)
    ((8#5 : BitVec 5), (0xFFF0000000000000#64 : BitVec 64)),
  chk "inf / 0.0 = +inf, no flag (level 0, Sail's softfloat)"
    (riscv_f64Div 0#3 0x7FF0000000000000#64 0x0000000000000000#64)
    ((0#5 : BitVec 5), (0x7FF0000000000000#64 : BitVec 64)),
  chk "inf / -0.0 = -inf, no flag (level 0, Sail's softfloat)"
    (riscv_f64Div 0#3 0x7FF0000000000000#64 0x8000000000000000#64)
    ((0#5 : BitVec 5), (0xFFF0000000000000#64 : BitVec 64)),
  chk "0.0 / 0.0 = canonical NaN, invalid"
    (riscv_f64Div 0#3 0x0000000000000000#64 0x0000000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "inf * 0 = canonical NaN, invalid"
    (riscv_f64Mul 0#3 0x7FF0000000000000#64 0x0000000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64))
]

open Axioms in
#eval report "binary64 multiply, divide, compare" [
  chk "3.0 * 0.5 = 1.5"
    (riscv_f64Mul 0#3 0x4008000000000000#64 0x3FE0000000000000#64)
    ((0#5 : BitVec 5), (0x3FF8000000000000#64 : BitVec 64)),
  chk "pi * e"
    (riscv_f64Mul 0#3 0x400921FB54442D18#64 0x4005BF0A8B145769#64)
    ((1#5 : BitVec 5), (0x402114580B45D474#64 : BitVec 64)),
  chk "1.0 / 3.0"
    (riscv_f64Div 0#3 0x3FF0000000000000#64 0x4008000000000000#64)
    ((1#5 : BitVec 5), (0x3FD5555555555555#64 : BitVec 64)),
  chk "2.0 / 3.0"
    (riscv_f64Div 0#3 0x4000000000000000#64 0x4008000000000000#64)
    ((1#5 : BitVec 5), (0x3FE5555555555555#64 : BitVec 64)),
  chk "3.0 / 1.5 = 2.0 (exact)"
    (riscv_f64Div 0#3 0x4008000000000000#64 0x3FF8000000000000#64)
    ((0#5 : BitVec 5), (0x4000000000000000#64 : BitVec 64)),
  chk "1.0 < 2.0"
    (riscv_f64Lt 0x3FF0000000000000#64 0x4000000000000000#64) ((0#5 : BitVec 5), true),
  chk "NaN < 1.0 signals invalid"
    (riscv_f64Lt 0x7FF8000000000000#64 0x3FF0000000000000#64) ((16#5 : BitVec 5), false),
  chk "NaN < 1.0 quiet does not"
    (riscv_f64Lt_quiet 0x7FF8000000000000#64 0x3FF0000000000000#64) ((0#5 : BitVec 5), false),
  chk "+0 = -0"
    (riscv_f64Eq 0x0000000000000000#64 0x8000000000000000#64) ((0#5 : BitVec 5), true),
  chk "-inf <= -inf"
    (riscv_f64Le 0xFFF0000000000000#64 0xFFF0000000000000#64) ((0#5 : BitVec 5), true)
]

open Axioms in
#eval report "binary32 and binary16 (the same code, other parameters)" [
  chk "widths are 16 / 32 / 64"
    (binary16.w, binary32.w, binary64.w) ((16, 32, 64) : Nat × Nat × Nat),
  chk "f32 1.0 + 2.0"
    (riscv_f32Add 0#3 0x3F800000#32 0x40000000#32)
    ((0#5 : BitVec 5), (0x40400000#32 : BitVec 32)),
  chk "f32 0.1 + 0.2"
    (riscv_f32Add 0#3 0x3DCCCCCD#32 0x3E4CCCCD#32)
    ((1#5 : BitVec 5), (0x3E99999A#32 : BitVec 32)),
  chk "f16 1.0 + 2.0"
    (riscv_f16Add 0#3 0x3C00#16 0x4000#16)
    ((0#5 : BitVec 5), (0x4200#16 : BitVec 16)),
  chk "f16 0.1 + 0.2"
    (riscv_f16Add 0#3 0x2E66#16 0x3266#16)
    ((1#5 : BitVec 5), (0x34CC#16 : BitVec 16)),
  chk "f16 maxfinite + maxfinite = +inf"
    (riscv_f16Add 0#3 0x7BFF#16 0x7BFF#16)
    ((5#5 : BitVec 5), (0x7C00#16 : BitVec 16))
]

/-! ### the integer kinds against Sail's own functions -/

def tvals : List Int :=
  [0, 1, -1, 7, -7, 255, 256, -256, 2 ^ 31, -(2 ^ 31), 2 ^ 31 - 1,
   2 ^ 63, -(2 ^ 63), 2 ^ 63 - 1, 2 ^ 64, -(2 ^ 64), 2 ^ 64 - 1, -(2 ^ 100)]

def dpairs : List (Int × Int) :=
  [(7, 2), (-7, 2), (7, -2), (-7, -2), (7, 0), (-7, 0), (0, 0),
   (2 ^ 63 - 1, 2), (-(2 ^ 63), -1), (2 ^ 63, -1), (1, 3)]

#eval report "the fixed-width integer kinds are Sail's to_bits_truncate" (
  (tvals.map (fun n => chk ("to_bits_truncate 64 " ++ toString n)
      (sailToBitsTruncate 64 n) (BitVec.ofInt 64 n))) ++
  (tvals.map (fun n => chk ("unsigned 64 projects " ++ toString n)
      ((unsignedK 64).proj 0#3 (Uni.ofInt n)).2
      (Val.num (Uni.ofInt ((sailToBitsTruncate 64 n).toNat : Int))))) ++
  (tvals.map (fun n => chk ("signed 64 projects " ++ toString n)
      ((signedK 64).proj 0#3 (Uni.ofInt n)).2
      (Val.num (Uni.ofInt (sailToBitsTruncate 64 n).toInt)))) ++
  (tvals.map (fun n => chk ("unsigned 32 projects " ++ toString n)
      ((unsignedK 32).proj 0#3 (Uni.ofInt n)).2
      (Val.num (Uni.ofInt ((sailToBitsTruncate 32 n).toNat : Int)))))
)

#eval report "divide and remainder are Int.tdiv / Int.tmod, zero divisor included" (
  (dpairs.map (fun p => chk ("divT " ++ toString p)
      (Uni.divT (Uni.ofInt p.1) (Uni.ofInt p.2)).toInt (Int.tdiv p.1 p.2))) ++
  (dpairs.map (fun p => chk ("remT " ++ toString p)
      (Uni.remT (Uni.ofInt p.1) (Uni.ofInt p.2)).toInt (Int.tmod p.1 p.2)))
)

#eval report "the constraint sets" [
  chk "unsigned 8 holds 255 / 256"
    (((unsignedK 8).holds (Uni.ofInt 255)), ((unsignedK 8).holds (Uni.ofInt 256)))
    ((true, false) : Bool × Bool),
  chk "unsigned 8 refuses -1 (the sign)"
    ((unsignedK 8).holds (Uni.ofInt (-1))) false,
  chk "unsigned 8 refuses a non-integer exponent"
    ((unsignedK 8).holds (Uni.ofSignedAt 1 (-1))) false,
  chk "signed 8 holds -128 and 127, refuses 128"
    (((signedK 8).holds (Uni.ofInt (-128))), ((signedK 8).holds (Uni.ofInt 127)),
     ((signedK 8).holds (Uni.ofInt 128))) ((true, true, false) : Bool × Bool × Bool),
  chk "bool holds 0 and 1, refuses 2"
    ((boolK.holds (Uni.ofInt 0)), (boolK.holds (Uni.ofInt 1)), (boolK.holds (Uni.ofInt 2)))
    ((true, true, false) : Bool × Bool × Bool),
  chk "bool projects 7 to 1"
    (boolK.proj 0#3 (Uni.ofInt 7)).2 (Val.num (Uni.ofInt 1)),
  chk "binary64 holds 1.0 and 2^-1074, refuses 2^-1075"
    ((ieeeK binary64).holds (Uni.ofInt 1),
     (ieeeK binary64).holds (Uni.ofSignedAt 1 (-1074)),
     (ieeeK binary64).holds (Uni.ofSignedAt 1 (-1075)))
    ((true, true, false) : Bool × Bool × Bool),
  chk "binary64 refuses 2^53+1 (too many significant bits)"
    ((ieeeK binary64).holds (Uni.ofInt (2 ^ 53 + 1))) false,
  chk "binary64 refuses 2^1024 (out of range)"
    ((ieeeK binary64).holds (Uni.ofSignedAt 1 1024)) false,
  chk "binary64 projects floor(2^60/3) * 2^-60 (60 significant bits) inexactly"
    ((ieeeK binary64).proj 0#3 (Uni.ofSignedAt (2 ^ 60 / 3) (-60))).1
    (1#5 : BitVec 5)
]

/-- 8.8 fixed-point, saturating, and the same wrapping. -/
def fix88s : FixFmt := { w := 16, q := -8, sat := true }
def fix88w : FixFmt := { w := 16, q := -8, sat := false }

#eval report "fixed-point: the exponent held, then round or saturate" [
  chk "1.5 at 2^-8 is exact"
    ((fixedK fix88s).proj 0#3 (Uni.ofSignedAt 3 (-1))).1 (0#5 : BitVec 5),
  chk "1.5 at 2^-8 is 384 * 2^-8"
    ((fixedK fix88s).proj 0#3 (Uni.ofSignedAt 3 (-1))).2
    (Val.num (Uni.ofSignedAt 384 (-8))),
  chk "floor(2^20/3) * 2^-20 rounds to 85 * 2^-8, inexact"
    ((fixedK fix88s).proj 0#3 (Uni.ofSignedAt (2 ^ 20 / 3) (-20)))
    ((1#5 : BitVec 5), Val.num (Uni.ofSignedAt 85 (-8))),
  chk "200.0 saturates to 32767 * 2^-8, overflow"
    ((fixedK fix88s).proj 0#3 (Uni.ofInt 200))
    ((4#5 : BitVec 5), Val.num (Uni.ofSignedAt 32767 (-8))),
  chk "200.0 wraps instead when the type says wrap"
    ((fixedK fix88w).proj 0#3 (Uni.ofInt 200))
    ((4#5 : BitVec 5), Val.num (Uni.ofSignedAt (BitVec.ofInt 16 51200).toInt (-8))),
  chk "the kind holds what it projects"
    ((fixedK fix88s).holds (Uni.ofSignedAt 384 (-8))) true
]

#eval report "the exact operations on the universal object" [
  chk "add carries the smaller exponent"
    ((Uni.add (Uni.ofSignedAt 1 10) (Uni.ofSignedAt 1 0)).toInt) (1025 : Int),
  chk "mul adds the exponents"
    ((Uni.mul (Uni.ofSignedAt 3 10) (Uni.ofSignedAt 5 (-4))).toInt) (15 * 2 ^ 6 : Int),
  chk "sub of equals is zero"
    ((Uni.sub (Uni.ofSignedAt 7 (-3)) (Uni.ofSignedAt 7 (-3))).isZero) true,
  chk "compare aligns first"
    ((Uni.cmp (Uni.ofSignedAt 1 10) (Uni.ofSignedAt 1024 0))) Ordering.eq,
  chk "a shift is a move of the exponent"
    ((Uni.shl (Uni.ofInt 3) 40).toInt) (3 * 2 ^ 40 : Int),
  chk "arithmetic right shift at 64 bits floors"
    ((Uni.shrA 64 (Uni.ofInt (-7)) 1).toInt) (-4 : Int),
  chk "logical right shift at 64 bits does not"
    ((Uni.shrL 64 (Uni.ofInt (-7)) 1).toInt) ((2 ^ 64 - 7) / 2 : Int),
  chk "and / or / xor / not at 8 bits"
    (((Uni.band 8 (Uni.ofInt 12) (Uni.ofInt 10)).toInt),
     ((Uni.bor 8 (Uni.ofInt 12) (Uni.ofInt 10)).toInt),
     ((Uni.bxor 8 (Uni.ofInt 12) (Uni.ofInt 10)).toInt),
     ((Uni.bnot 8 (Uni.ofInt 12)).toInt))
    ((8, 14, 6, 243) : Int × Int × Int × Int),
  chk "the bit reading of an unbounded bit_vec"
    ((Ubv.bit 12 2), (Ubv.bit 12 0), (Ubv.len 12), (Ubv.len 0))
    ((1#1, 0#1, 4, 0) : BitVec 1 × BitVec 1 × Nat × Nat)
]

/-! ### the forty bodies that had none

Every expected value below is Sail's OWN softfloat's: the RISCV-specialized
Berkeley SoftFloat 3 that the model's simulator links, run on the same point
and read off. Nothing here is hand-computed. -/

#eval report "the new format, the new arithmetic, the new targets" [
  chk "bfloat16 is 16 bits wide on binary32's exponent range, with seven significand bits"
    (bfloat16.w, bfloat16.bias, bfloat16.emax, bfloat16.emin, bfloat16.qmin)
    ((16, 127, 127, -126, -133) : Nat × Int × Int × Int × Int),
  chk "bfloat16's canonical quiet NaN is 0x7FC0, its infinity 0x7F80"
    ((encNaN bfloat16), (encInf bfloat16 false), (encMax bfloat16 false))
    ((0x7FC0, 0x7F80, 0x7F7F) : Nat × Nat × Nat),
  chk "the integer square root on the perfect squares and their neighbours"
    ((isqrt 0), (isqrt 1), (isqrt 2), (isqrt 3), (isqrt 4), (isqrt 15), (isqrt 16))
    ((0, 1, 1, 1, 2, 3, 4) : Nat × Nat × Nat × Nat × Nat × Nat × Nat),
  chk "the integer square root far above any machine word"
    ((isqrt (2 ^ 106)), (isqrt (2 ^ 128 - 1)), (isqrt (10 ^ 40)))
    ((2 ^ 53, 2 ^ 64 - 1, 10 ^ 20) : Nat × Nat × Nat),
  chk "the signed integer targets' ranges"
    (int32.lo, int32.hi, int64.lo, int64.hi)
    ((-(2:Int) ^ 31, (2:Int) ^ 31 - 1, -(2:Int) ^ 63, (2:Int) ^ 63 - 1) : Int × Int × Int × Int),
  chk "the unsigned integer targets' ranges"
    (uint32.lo, uint32.hi, uint64.lo, uint64.hi)
    ((0, (2:Int) ^ 32 - 1, 0, (2:Int) ^ 64 - 1) : Int × Int × Int × Int)
]

open Axioms in
#eval report "the fused multiply-add is not multiply then add" [
  chk "f64 (1+2^-52) * (1+3*2^-52) - 1: one rounding keeps 2^-102, two lose it"
    ((riscv_f64MulAdd 0#3 0x3FF0000000000001#64 0x3FF0000000000003#64 0xBFF0000000000000#64).2,
     (riscv_f64Add 0#3
        (riscv_f64Mul 0#3 0x3FF0000000000001#64 0x3FF0000000000003#64).2
        0xBFF0000000000000#64).2)
    ((0x3CD0000000000001#64, 0x3CD0000000000000#64) : BitVec 64 × BitVec 64),
  chk "f32 (1+2^-23) * (1+3*2^-23) - 1: the same at 32 bits"
    ((riscv_f32MulAdd 0#3 0x3F800001#32 0x3F800003#32 0xBF800000#32).2,
     (riscv_f32Add 0#3 (riscv_f32Mul 0#3 0x3F800001#32 0x3F800003#32).2 0xBF800000#32).2)
    ((0x35000001#32, 0x35000000#32) : BitVec 32 × BitVec 32)
]

open Axioms in
#eval report "the fused multiply-add: one rounding, not two" [
  chk "f64 1.0 * 1.0 + 1.0 = 2.0 exact"
    (riscv_f64MulAdd 0#3 0x3FF0000000000000#64 0x3FF0000000000000#64 0x3FF0000000000000#64)
    ((0#5 : BitVec 5), (0x4000000000000000#64 : BitVec 64)),
  chk "f64 (1+2^-52) * (1+3*2^-52) - 1: the ONE rounding keeps 2^-102"
    (riscv_f64MulAdd 0#3 0x3FF0000000000001#64 0x3FF0000000000003#64 0xBFF0000000000000#64)
    ((1#5 : BitVec 5), (0x3CD0000000000001#64 : BitVec 64)),
  chk "f64 pi * e + 1"
    (riscv_f64MulAdd 0#3 0x400921FB54442D18#64 0x4005BF0A8B145769#64 0x3FF0000000000000#64)
    ((1#5 : BitVec 5), (0x402314580B45D474#64 : BitVec 64)),
  chk "f64 2.0 * 3.0 + (-6.0) = +0"
    (riscv_f64MulAdd 0#3 0x4000000000000000#64 0x4008000000000000#64 0xC018000000000000#64)
    ((0#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f64 the same under RDN (rm 010): -0"
    (riscv_f64MulAdd 2#3 0x4000000000000000#64 0x4008000000000000#64 0xC018000000000000#64)
    ((0#5 : BitVec 5), (0x8000000000000000#64 : BitVec 64)),
  chk "f64 (-0) * 1.0 + (-0) = -0, the addend's own sign"
    (riscv_f64MulAdd 0#3 0x8000000000000000#64 0x3FF0000000000000#64 0x8000000000000000#64)
    ((0#5 : BitVec 5), (0x8000000000000000#64 : BitVec 64)),
  chk "f64 (+0) * 1.0 + (-0) = +0"
    (riscv_f64MulAdd 0#3 0x0000000000000000#64 0x3FF0000000000000#64 0x8000000000000000#64)
    ((0#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f64 (+0) * 1.0 + (-0) = -0 under RDN"
    (riscv_f64MulAdd 2#3 0x0000000000000000#64 0x3FF0000000000000#64 0x8000000000000000#64)
    ((0#5 : BitVec 5), (0x8000000000000000#64 : BitVec 64)),
  chk "f64 0.0 * 1.0 + 3.5 = 3.5, no flag"
    (riscv_f64MulAdd 0#3 0x0000000000000000#64 0x3FF0000000000000#64 0x400C000000000000#64)
    ((0#5 : BitVec 5), (0x400C000000000000#64 : BitVec 64)),
  chk "f64 inf * 0 + 1.0 = canonical NaN, invalid"
    (riscv_f64MulAdd 0#3 0x7FF0000000000000#64 0x0000000000000000#64 0x3FF0000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 inf * 0 + QUIET NaN still refuses (softfloat's choice of the one IEEE leaves open)"
    (riscv_f64MulAdd 0#3 0x7FF0000000000000#64 0x0000000000000000#64 0x7FF8000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 inf * 1.0 + (-inf) = canonical NaN, invalid"
    (riscv_f64MulAdd 0#3 0x7FF0000000000000#64 0x3FF0000000000000#64 0xFFF0000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 inf * 1.0 + inf = +inf, no flag"
    (riscv_f64MulAdd 0#3 0x7FF0000000000000#64 0x3FF0000000000000#64 0x7FF0000000000000#64)
    ((0#5 : BitVec 5), (0x7FF0000000000000#64 : BitVec 64)),
  chk "f64 1.0 * 1.0 + inf = +inf, no flag"
    (riscv_f64MulAdd 0#3 0x3FF0000000000000#64 0x3FF0000000000000#64 0x7FF0000000000000#64)
    ((0#5 : BitVec 5), (0x7FF0000000000000#64 : BitVec 64)),
  chk "f64 quiet NaN * 1.0 + 1.0 = canonical NaN, no flag"
    (riscv_f64MulAdd 0#3 0x7FF8000000000000#64 0x3FF0000000000000#64 0x3FF0000000000000#64)
    ((0#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 signalling NaN * 1.0 + 1.0 = canonical NaN, invalid"
    (riscv_f64MulAdd 0#3 0x7FF0000000000001#64 0x3FF0000000000000#64 0x3FF0000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 1.0 * 1.0 + signalling NaN = canonical NaN, invalid"
    (riscv_f64MulAdd 0#3 0x3FF0000000000000#64 0x3FF0000000000000#64 0x7FF0000000000001#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 maxfinite * 2.0 + 0 = +inf, overflow and inexact"
    (riscv_f64MulAdd 0#3 0x7FEFFFFFFFFFFFFF#64 0x4000000000000000#64 0x0000000000000000#64)
    ((5#5 : BitVec 5), (0x7FF0000000000000#64 : BitVec 64)),
  chk "f64 2^-1074 * 0.5 + 0 = +0, underflow and inexact"
    (riscv_f64MulAdd 0#3 0x0000000000000001#64 0x3FE0000000000000#64 0x0000000000000000#64)
    ((3#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f64 3*2^-1074 * 0.5 + 2^-1074 = 3*2^-1074 (the product alone is inexact)"
    (riscv_f64MulAdd 0#3 0x0000000000000003#64 0x3FE0000000000000#64 0x0000000000000001#64)
    ((3#5 : BitVec 5), (0x0000000000000002#64 : BitVec 64)),
  chk "f32 (1+2^-23) * (1+3*2^-23) - 1: the single rounding again"
    (riscv_f32MulAdd 0#3 0x3F800001#32 0x3F800003#32 0xBF800000#32)
    ((1#5 : BitVec 5), (0x35000001#32 : BitVec 32)),
  chk "f32 1.0 * 1.0 + 1.0 = 2.0"
    (riscv_f32MulAdd 0#3 0x3F800000#32 0x3F800000#32 0x3F800000#32)
    ((0#5 : BitVec 5), (0x40000000#32 : BitVec 32)),
  chk "f32 maxfinite * maxfinite + 0 = +inf, overflow"
    (riscv_f32MulAdd 0#3 0x7F7FFFFF#32 0x7F7FFFFF#32 0x00000000#32)
    ((5#5 : BitVec 5), (0x7F800000#32 : BitVec 32)),
  chk "f16 (1+2^-10) * (1+3*2^-10) - 1: the single rounding at 16 bits"
    (riscv_f16MulAdd 0#3 0x3C01#16 0x3C03#16 0xBC00#16)
    ((1#5 : BitVec 5), (0x1C01#16 : BitVec 16)),
  chk "f16 1.0 * 1.0 + 1.0 = 2.0"
    (riscv_f16MulAdd 0#3 0x3C00#16 0x3C00#16 0x3C00#16)
    ((0#5 : BitVec 5), (0x4000#16 : BitVec 16)),
  chk "f16 maxfinite * 2.0 + 0 = +inf, overflow"
    (riscv_f16MulAdd 0#3 0x7BFF#16 0x4000#16 0x0000#16)
    ((5#5 : BitVec 5), (0x7C00#16 : BitVec 16)),
  chk "f16 inf * 0 + 1.0 = canonical NaN, invalid"
    (riscv_f16MulAdd 0#3 0x7C00#16 0x0000#16 0x3C00#16)
    ((16#5 : BitVec 5), (0x7E00#16 : BitVec 16))
]

open Axioms in
#eval report "the square root: the one arithmetic the universal object had not got" [
  chk "f64 sqrt(4.0) = 2.0, exact"
    (riscv_f64Sqrt 0#3 0x4010000000000000#64)
    ((0#5 : BitVec 5), (0x4000000000000000#64 : BitVec 64)),
  chk "f64 sqrt(1.0) = 1.0"
    (riscv_f64Sqrt 0#3 0x3FF0000000000000#64)
    ((0#5 : BitVec 5), (0x3FF0000000000000#64 : BitVec 64)),
  chk "f64 sqrt(0.25) = 0.5"
    (riscv_f64Sqrt 0#3 0x3FD0000000000000#64)
    ((0#5 : BitVec 5), (0x3FE0000000000000#64 : BitVec 64)),
  chk "f64 sqrt(2.0), inexact"
    (riscv_f64Sqrt 0#3 0x4000000000000000#64)
    ((1#5 : BitVec 5), (0x3FF6A09E667F3BCD#64 : BitVec 64)),
  chk "f64 sqrt(2.0) under RTZ (rm 001)"
    (riscv_f64Sqrt 1#3 0x4000000000000000#64)
    ((1#5 : BitVec 5), (0x3FF6A09E667F3BCC#64 : BitVec 64)),
  chk "f64 sqrt(2.0) under RDN (rm 010)"
    (riscv_f64Sqrt 2#3 0x4000000000000000#64)
    ((1#5 : BitVec 5), (0x3FF6A09E667F3BCC#64 : BitVec 64)),
  chk "f64 sqrt(2.0) under RUP (rm 011)"
    (riscv_f64Sqrt 3#3 0x4000000000000000#64)
    ((1#5 : BitVec 5), (0x3FF6A09E667F3BCD#64 : BitVec 64)),
  chk "f64 sqrt(2.0) under RMM (rm 100)"
    (riscv_f64Sqrt 4#3 0x4000000000000000#64)
    ((1#5 : BitVec 5), (0x3FF6A09E667F3BCD#64 : BitVec 64)),
  chk "f64 sqrt(1e300) (a 512-bit exponent halved)"
    (riscv_f64Sqrt 0#3 0x7E37E43C8800759C#64)
    ((1#5 : BitVec 5), (0x5F138D352E5096AF#64 : BitVec 64)),
  chk "f64 sqrt(maxfinite)"
    (riscv_f64Sqrt 0#3 0x7FEFFFFFFFFFFFFF#64)
    ((1#5 : BitVec 5), (0x5FEFFFFFFFFFFFFF#64 : BitVec 64)),
  chk "f64 sqrt(2^-1074), the smallest subnormal: a NORMAL root, exact"
    (riscv_f64Sqrt 0#3 0x0000000000000001#64)
    ((0#5 : BitVec 5), (0x1E60000000000000#64 : BitVec 64)),
  chk "f64 sqrt(3*2^-1074), a subnormal operand, inexact"
    (riscv_f64Sqrt 0#3 0x0000000000000003#64)
    ((1#5 : BitVec 5), (0x1E6BB67AE8584CAA#64 : BitVec 64)),
  chk "f64 sqrt(largest subnormal)"
    (riscv_f64Sqrt 0#3 0x000FFFFFFFFFFFFF#64)
    ((1#5 : BitVec 5), (0x1FFFFFFFFFFFFFFF#64 : BitVec 64)),
  chk "f64 sqrt(smallest normal), exact"
    (riscv_f64Sqrt 0#3 0x0010000000000000#64)
    ((0#5 : BitVec 5), (0x2000000000000000#64 : BitVec 64)),
  chk "f64 sqrt(+0) = +0"
    (riscv_f64Sqrt 0#3 0x0000000000000000#64)
    ((0#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f64 sqrt(-0) = -0, the one negative the root keeps"
    (riscv_f64Sqrt 0#3 0x8000000000000000#64)
    ((0#5 : BitVec 5), (0x8000000000000000#64 : BitVec 64)),
  chk "f64 sqrt(-1.0) = canonical NaN, invalid"
    (riscv_f64Sqrt 0#3 0xBFF0000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 sqrt(-2^-1074) = canonical NaN, invalid"
    (riscv_f64Sqrt 0#3 0x8000000000000001#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 sqrt(+inf) = +inf, no flag"
    (riscv_f64Sqrt 0#3 0x7FF0000000000000#64)
    ((0#5 : BitVec 5), (0x7FF0000000000000#64 : BitVec 64)),
  chk "f64 sqrt(-inf) = canonical NaN, invalid"
    (riscv_f64Sqrt 0#3 0xFFF0000000000000#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 sqrt(quiet NaN) = canonical NaN, no flag"
    (riscv_f64Sqrt 0#3 0x7FF8000000000000#64)
    ((0#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 sqrt(signalling NaN) = canonical NaN, invalid"
    (riscv_f64Sqrt 0#3 0x7FF0000000000001#64)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f32 sqrt(4.0) = 2.0, exact"
    (riscv_f32Sqrt 0#3 0x40800000#32)
    ((0#5 : BitVec 5), (0x40000000#32 : BitVec 32)),
  chk "f32 sqrt(2.0), inexact"
    (riscv_f32Sqrt 0#3 0x40000000#32)
    ((1#5 : BitVec 5), (0x3FB504F3#32 : BitVec 32)),
  chk "f32 sqrt(2^-149), the smallest subnormal"
    (riscv_f32Sqrt 0#3 0x00000001#32)
    ((1#5 : BitVec 5), (0x1A3504F3#32 : BitVec 32)),
  chk "f32 sqrt(maxfinite)"
    (riscv_f32Sqrt 0#3 0x7F7FFFFF#32)
    ((1#5 : BitVec 5), (0x5F7FFFFF#32 : BitVec 32)),
  chk "f16 sqrt(4.0) = 2.0, exact"
    (riscv_f16Sqrt 0#3 0x4400#16)
    ((0#5 : BitVec 5), (0x4000#16 : BitVec 16)),
  chk "f16 sqrt(2.0), inexact"
    (riscv_f16Sqrt 0#3 0x4000#16)
    ((1#5 : BitVec 5), (0x3DA8#16 : BitVec 16)),
  chk "f16 sqrt(2^-24), the smallest subnormal"
    (riscv_f16Sqrt 0#3 0x0001#16)
    ((0#5 : BitVec 5), (0x0C00#16 : BitVec 16)),
  chk "f16 sqrt(maxfinite)"
    (riscv_f16Sqrt 0#3 0x7BFF#16)
    ((1#5 : BitVec 5), (0x5BFF#16 : BitVec 16)),
  chk "f16 sqrt(-1.0) = canonical NaN, invalid"
    (riscv_f16Sqrt 0#3 0xBC00#16)
    ((16#5 : BitVec 5), (0x7E00#16 : BitVec 16))
]

open Axioms in
#eval report "round to a whole number, in the same format" [
  chk "f64 0.5 under RNE (rm 000)"
    (riscv_f64roundToInt 0#3 0x3FE0000000000000#64 true)
    ((1#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f64 0.5 under RTZ (rm 001)"
    (riscv_f64roundToInt 1#3 0x3FE0000000000000#64 true)
    ((1#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f64 0.5 under RDN (rm 010)"
    (riscv_f64roundToInt 2#3 0x3FE0000000000000#64 true)
    ((1#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f64 0.5 under RUP (rm 011)"
    (riscv_f64roundToInt 3#3 0x3FE0000000000000#64 true)
    ((1#5 : BitVec 5), (0x3FF0000000000000#64 : BitVec 64)),
  chk "f64 0.5 under RMM (rm 100)"
    (riscv_f64roundToInt 4#3 0x3FE0000000000000#64 true)
    ((1#5 : BitVec 5), (0x3FF0000000000000#64 : BitVec 64)),
  chk "f64 -0.5 under RNE"
    (riscv_f64roundToInt 0#3 0xBFE0000000000000#64 true)
    ((1#5 : BitVec 5), (0x8000000000000000#64 : BitVec 64)),
  chk "f64 -0.5 under RDN"
    (riscv_f64roundToInt 2#3 0xBFE0000000000000#64 true)
    ((1#5 : BitVec 5), (0xBFF0000000000000#64 : BitVec 64)),
  chk "f64 -0.5 under RUP"
    (riscv_f64roundToInt 3#3 0xBFE0000000000000#64 true)
    ((1#5 : BitVec 5), (0x8000000000000000#64 : BitVec 64)),
  chk "f64 -0.5 under RMM"
    (riscv_f64roundToInt 4#3 0xBFE0000000000000#64 true)
    ((1#5 : BitVec 5), (0xBFF0000000000000#64 : BitVec 64)),
  chk "f64 1.5 to nearest even = 2.0"
    (riscv_f64roundToInt 0#3 0x3FF8000000000000#64 true)
    ((1#5 : BitVec 5), (0x4000000000000000#64 : BitVec 64)),
  chk "f64 2.5 to nearest even = 2.0"
    (riscv_f64roundToInt 0#3 0x4004000000000000#64 true)
    ((1#5 : BitVec 5), (0x4000000000000000#64 : BitVec 64)),
  chk "f64 2.5 under RMM = 3.0"
    (riscv_f64roundToInt 4#3 0x4004000000000000#64 true)
    ((1#5 : BitVec 5), (0x4008000000000000#64 : BitVec 64)),
  chk "f64 0.25 under RUP = 1.0"
    (riscv_f64roundToInt 3#3 0x3FD0000000000000#64 true)
    ((1#5 : BitVec 5), (0x3FF0000000000000#64 : BitVec 64)),
  chk "f64 -0.25 under RDN = -1.0"
    (riscv_f64roundToInt 2#3 0xBFD0000000000000#64 true)
    ((1#5 : BitVec 5), (0xBFF0000000000000#64 : BitVec 64)),
  chk "f64 4.0 is already whole, no flag"
    (riscv_f64roundToInt 0#3 0x4010000000000000#64 true)
    ((0#5 : BitVec 5), (0x4010000000000000#64 : BitVec 64)),
  chk "f64 2^52 is already whole, no flag"
    (riscv_f64roundToInt 0#3 0x4330000000000000#64 true)
    ((0#5 : BitVec 5), (0x4330000000000000#64 : BitVec 64)),
  chk "f64 maxfinite is already whole, no flag"
    (riscv_f64roundToInt 0#3 0x7FEFFFFFFFFFFFFF#64 true)
    ((0#5 : BitVec 5), (0x7FEFFFFFFFFFFFFF#64 : BitVec 64)),
  chk "f64 +0 keeps its sign, no flag"
    (riscv_f64roundToInt 0#3 0x0000000000000000#64 true)
    ((0#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f64 -0 keeps its sign, no flag"
    (riscv_f64roundToInt 0#3 0x8000000000000000#64 true)
    ((0#5 : BitVec 5), (0x8000000000000000#64 : BitVec 64)),
  chk "f64 2^-1074 to nearest = +0, inexact"
    (riscv_f64roundToInt 0#3 0x0000000000000001#64 true)
    ((1#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f64 2.5 with `exact` false raises nothing"
    (riscv_f64roundToInt 0#3 0x4004000000000000#64 false)
    ((0#5 : BitVec 5), (0x4000000000000000#64 : BitVec 64)),
  chk "f64 +inf passes through"
    (riscv_f64roundToInt 0#3 0x7FF0000000000000#64 true)
    ((0#5 : BitVec 5), (0x7FF0000000000000#64 : BitVec 64)),
  chk "f64 -inf passes through"
    (riscv_f64roundToInt 0#3 0xFFF0000000000000#64 true)
    ((0#5 : BitVec 5), (0xFFF0000000000000#64 : BitVec 64)),
  chk "f64 quiet NaN = canonical NaN, no flag"
    (riscv_f64roundToInt 0#3 0x7FF8000000000000#64 true)
    ((0#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f64 signalling NaN = canonical NaN, invalid"
    (riscv_f64roundToInt 0#3 0x7FF0000000000001#64 true)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f32 0.5 to nearest even = +0"
    (riscv_f32roundToInt 0#3 0x3F000000#32 true)
    ((1#5 : BitVec 5), (0x00000000#32 : BitVec 32)),
  chk "f32 -1.5 to nearest even = -2.0"
    (riscv_f32roundToInt 0#3 0xBFC00000#32 true)
    ((1#5 : BitVec 5), (0xC0000000#32 : BitVec 32)),
  chk "f32 2^-149 under RUP = 1.0"
    (riscv_f32roundToInt 3#3 0x00000001#32 true)
    ((1#5 : BitVec 5), (0x3F800000#32 : BitVec 32)),
  chk "f16 0.5 to nearest even = +0"
    (riscv_f16roundToInt 0#3 0x3800#16 true)
    ((1#5 : BitVec 5), (0x0000#16 : BitVec 16)),
  chk "f16 -0.6 under RDN = -1.0"
    (riscv_f16roundToInt 2#3 0xB8CD#16 true)
    ((1#5 : BitVec 5), (0xBC00#16 : BitVec 16)),
  chk "f16 maxfinite is already whole"
    (riscv_f16roundToInt 0#3 0x7BFF#16 true)
    ((0#5 : BitVec 5), (0x7BFF#16 : BitVec 16))
]

open Axioms in
#eval report "float to integer: round on the whole-number grid, then saturate" [
  chk "f64 3.5 to i32 under RTZ = 3"
    (riscv_f64ToI32 1#3 0x400C000000000000#64)
    ((1#5 : BitVec 5), (0x00000003#32 : BitVec 32)),
  chk "f64 3.5 to i32 to nearest even = 4"
    (riscv_f64ToI32 0#3 0x400C000000000000#64)
    ((1#5 : BitVec 5), (0x00000004#32 : BitVec 32)),
  chk "f64 2.5 to i32 to nearest even = 2"
    (riscv_f64ToI32 0#3 0x4004000000000000#64)
    ((1#5 : BitVec 5), (0x00000002#32 : BitVec 32)),
  chk "f64 -3.5 to i32 under RTZ = -3"
    (riscv_f64ToI32 1#3 0xC00C000000000000#64)
    ((1#5 : BitVec 5), (0xFFFFFFFD#32 : BitVec 32)),
  chk "f64 -3.5 to i32 under RDN = -4"
    (riscv_f64ToI32 2#3 0xC00C000000000000#64)
    ((1#5 : BitVec 5), (0xFFFFFFFC#32 : BitVec 32)),
  chk "f64 2^31-1 to i32, exact at the endpoint"
    (riscv_f64ToI32 0#3 0x41DFFFFFFFC00000#64)
    ((0#5 : BitVec 5), (0x7FFFFFFF#32 : BitVec 32)),
  chk "f64 2^31 to i32 is out of range: invalid, the top endpoint, and NOTHING else"
    (riscv_f64ToI32 0#3 0x41E0000000000000#64)
    ((16#5 : BitVec 5), (0x7FFFFFFF#32 : BitVec 32)),
  chk "f64 -2^31 to i32, exact at the low endpoint"
    (riscv_f64ToI32 0#3 0xC1E0000000000000#64)
    ((0#5 : BitVec 5), (0x80000000#32 : BitVec 32)),
  chk "f64 -2^31-1 to i32 is out of range: invalid, the low endpoint"
    (riscv_f64ToI32 0#3 0xC1E0000000200000#64)
    ((16#5 : BitVec 5), (0x80000000#32 : BitVec 32)),
  chk "f64 2^31-0.5 to i32 rounds UP out of range under RNE"
    (riscv_f64ToI32 0#3 0x41DFFFFFFFE00000#64)
    ((16#5 : BitVec 5), (0x7FFFFFFF#32 : BitVec 32)),
  chk "f64 2^31-0.5 to i32 under RTZ stays in range, inexact"
    (riscv_f64ToI32 1#3 0x41DFFFFFFFE00000#64)
    ((1#5 : BitVec 5), (0x7FFFFFFF#32 : BitVec 32)),
  chk "f64 NaN to i32 gives the LARGEST POSITIVE, invalid"
    (riscv_f64ToI32 0#3 0x7FF8000000000000#64)
    ((16#5 : BitVec 5), (0x7FFFFFFF#32 : BitVec 32)),
  chk "f64 +inf to i32: invalid, the top endpoint"
    (riscv_f64ToI32 0#3 0x7FF0000000000000#64)
    ((16#5 : BitVec 5), (0x7FFFFFFF#32 : BitVec 32)),
  chk "f64 -inf to i32: invalid, the low endpoint"
    (riscv_f64ToI32 0#3 0xFFF0000000000000#64)
    ((16#5 : BitVec 5), (0x80000000#32 : BitVec 32)),
  chk "f64 NaN to ui32 gives the LARGEST POSITIVE too, not zero"
    (riscv_f64ToUi32 0#3 0x7FF8000000000000#64)
    ((16#5 : BitVec 5), (0xFFFFFFFF#32 : BitVec 32)),
  chk "f64 -0.5 to ui32 under RTZ rounds to 0, in range, inexact"
    (riscv_f64ToUi32 1#3 0xBFE0000000000000#64)
    ((1#5 : BitVec 5), (0x00000000#32 : BitVec 32)),
  chk "f64 -0.5 to ui32 under RDN floors to -1, out of range: invalid, zero"
    (riscv_f64ToUi32 2#3 0xBFE0000000000000#64)
    ((16#5 : BitVec 5), (0x00000000#32 : BitVec 32)),
  chk "f64 -0.5 to ui32 to nearest even gives -0, which IS in range"
    (riscv_f64ToUi32 0#3 0xBFE0000000000000#64)
    ((1#5 : BitVec 5), (0x00000000#32 : BitVec 32)),
  chk "f64 -0.0 to ui32 = 0, no flag"
    (riscv_f64ToUi32 0#3 0x8000000000000000#64)
    ((0#5 : BitVec 5), (0x00000000#32 : BitVec 32)),
  chk "f64 2^32-1 to ui32, exact at the endpoint"
    (riscv_f64ToUi32 0#3 0x41EFFFFFFFE00000#64)
    ((0#5 : BitVec 5), (0xFFFFFFFF#32 : BitVec 32)),
  chk "f64 2^32 to ui32 is out of range: invalid, the top endpoint"
    (riscv_f64ToUi32 0#3 0x41F0000000000000#64)
    ((16#5 : BitVec 5), (0xFFFFFFFF#32 : BitVec 32)),
  chk "f64 -2^63 to i64, exact at the low endpoint"
    (riscv_f64ToI64 0#3 0xC3E0000000000000#64)
    ((0#5 : BitVec 5), (0x8000000000000000#64 : BitVec 64)),
  chk "f64 2^63 to i64 is out of range: invalid, the top endpoint"
    (riscv_f64ToI64 0#3 0x43E0000000000000#64)
    ((16#5 : BitVec 5), (0x7FFFFFFFFFFFFFFF#64 : BitVec 64)),
  chk "f64 2^64-2048 to ui64, exact"
    (riscv_f64ToUi64 0#3 0x43EFFFFFFFFFFFFF#64)
    ((0#5 : BitVec 5), (0xFFFFFFFFFFFFF800#64 : BitVec 64)),
  chk "f64 2^64 to ui64 is out of range: invalid, the top endpoint"
    (riscv_f64ToUi64 0#3 0x43F0000000000000#64)
    ((16#5 : BitVec 5), (0xFFFFFFFFFFFFFFFF#64 : BitVec 64)),
  chk "f64 -1.0 to ui64: invalid, zero"
    (riscv_f64ToUi64 0#3 0xBFF0000000000000#64)
    ((16#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "f32 3.5 to i32 under RTZ = 3"
    (riscv_f32ToI32 1#3 0x40600000#32)
    ((1#5 : BitVec 5), (0x00000003#32 : BitVec 32)),
  chk "f32 2^31 to i32 is out of range"
    (riscv_f32ToI32 0#3 0x4F000000#32)
    ((16#5 : BitVec 5), (0x7FFFFFFF#32 : BitVec 32)),
  chk "f32 maxfinite to i64 is out of range"
    (riscv_f32ToI64 0#3 0x7F7FFFFF#32)
    ((16#5 : BitVec 5), (0x7FFFFFFFFFFFFFFF#64 : BitVec 64)),
  chk "f32 2^-149 to ui32 = 0, inexact"
    (riscv_f32ToUi32 0#3 0x00000001#32)
    ((1#5 : BitVec 5), (0x00000000#32 : BitVec 32)),
  chk "f16 maxfinite 65504 to i32, exact"
    (riscv_f16ToI32 0#3 0x7BFF#16)
    ((0#5 : BitVec 5), (0x0000FFE0#32 : BitVec 32)),
  chk "f16 maxfinite 65504 to ui64, exact"
    (riscv_f16ToUi64 0#3 0x7BFF#16)
    ((0#5 : BitVec 5), (0x000000000000FFE0#64 : BitVec 64)),
  chk "f16 -1.5 to i64 under RTZ = -1"
    (riscv_f16ToI64 1#3 0xBE00#16)
    ((1#5 : BitVec 5), (0xFFFFFFFFFFFFFFFF#64 : BitVec 64)),
  chk "f16 NaN to ui64 gives the largest positive"
    (riscv_f16ToUi64 0#3 0x7E00#16)
    ((16#5 : BitVec 5), (0xFFFFFFFFFFFFFFFF#64 : BitVec 64))
]

open Axioms in
#eval report "integer to float: the exact integer, rounded" [
  chk "i32 0 to f64 is +0 under RDN too, never -0"
    (riscv_i32ToF64 2#3 0x00000000#32)
    ((0#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "ui32 0 to f64 is +0 under RDN too"
    (riscv_ui32ToF64 2#3 0x00000000#32)
    ((0#5 : BitVec 5), (0x0000000000000000#64 : BitVec 64)),
  chk "i32 1 to f64 = 1.0"
    (riscv_i32ToF64 0#3 0x00000001#32)
    ((0#5 : BitVec 5), (0x3FF0000000000000#64 : BitVec 64)),
  chk "i32 -1 to f64 = -1.0"
    (riscv_i32ToF64 0#3 0xFFFFFFFF#32)
    ((0#5 : BitVec 5), (0xBFF0000000000000#64 : BitVec 64)),
  chk "i32 -2^31 to f64, exact"
    (riscv_i32ToF64 0#3 0x80000000#32)
    ((0#5 : BitVec 5), (0xC1E0000000000000#64 : BitVec 64)),
  chk "ui32 2^32-1 to f64, exact"
    (riscv_ui32ToF64 0#3 0xFFFFFFFF#32)
    ((0#5 : BitVec 5), (0x41EFFFFFFFE00000#64 : BitVec 64)),
  chk "ui32 0x80000000 to f64 reads UNSIGNED: 2147483648.0"
    (riscv_ui32ToF64 0#3 0x80000000#32)
    ((0#5 : BitVec 5), (0x41E0000000000000#64 : BitVec 64)),
  chk "i64 2^53 to f64, exact"
    (riscv_i64ToF64 0#3 0x0020000000000000#64)
    ((0#5 : BitVec 5), (0x4340000000000000#64 : BitVec 64)),
  chk "i64 2^53+1 to f64, tie to even: down"
    (riscv_i64ToF64 0#3 0x0020000000000001#64)
    ((1#5 : BitVec 5), (0x4340000000000000#64 : BitVec 64)),
  chk "i64 2^53+3 to f64, tie to even: up"
    (riscv_i64ToF64 0#3 0x0020000000000003#64)
    ((1#5 : BitVec 5), (0x4340000000000002#64 : BitVec 64)),
  chk "i64 2^63-1 to f64, inexact"
    (riscv_i64ToF64 0#3 0x7FFFFFFFFFFFFFFF#64)
    ((1#5 : BitVec 5), (0x43E0000000000000#64 : BitVec 64)),
  chk "i64 -2^63 to f64, exact"
    (riscv_i64ToF64 0#3 0x8000000000000000#64)
    ((0#5 : BitVec 5), (0xC3E0000000000000#64 : BitVec 64)),
  chk "ui64 2^64-1 to f64, inexact, rounds to 2^64"
    (riscv_ui64ToF64 0#3 0xFFFFFFFFFFFFFFFF#64)
    ((1#5 : BitVec 5), (0x43F0000000000000#64 : BitVec 64)),
  chk "ui64 2^64-1 to f64 under RTZ stays below"
    (riscv_ui64ToF64 1#3 0xFFFFFFFFFFFFFFFF#64)
    ((1#5 : BitVec 5), (0x43EFFFFFFFFFFFFF#64 : BitVec 64)),
  chk "i32 2^24+1 to f32, inexact"
    (riscv_i32ToF32 0#3 0x01000001#32)
    ((1#5 : BitVec 5), (0x4B800000#32 : BitVec 32)),
  chk "i32 2^24 to f32, exact"
    (riscv_i32ToF32 0#3 0x01000000#32)
    ((0#5 : BitVec 5), (0x4B800000#32 : BitVec 32)),
  chk "i64 2^63-1 to f32, inexact"
    (riscv_i64ToF32 0#3 0x7FFFFFFFFFFFFFFF#64)
    ((1#5 : BitVec 5), (0x5F000000#32 : BitVec 32)),
  chk "i32 65504 to f16, exact at maxfinite"
    (riscv_i32ToF16 0#3 0x0000FFE0#32)
    ((0#5 : BitVec 5), (0x7BFF#16 : BitVec 16)),
  chk "i32 65536 to f16 OVERFLOWS: +inf, overflow and inexact"
    (riscv_i32ToF16 0#3 0x00010000#32)
    ((5#5 : BitVec 5), (0x7C00#16 : BitVec 16)),
  chk "i32 65536 to f16 under RTZ gives maxfinite instead"
    (riscv_i32ToF16 1#3 0x00010000#32)
    ((5#5 : BitVec 5), (0x7BFF#16 : BitVec 16)),
  chk "i64 2^62 to f16 overflows to +inf"
    (riscv_i64ToF16 0#3 0x4000000000000000#64)
    ((5#5 : BitVec 5), (0x7C00#16 : BitVec 16)),
  chk "ui64 2^64-1 to f16 overflows to +inf"
    (riscv_ui64ToF16 0#3 0xFFFFFFFFFFFFFFFF#64)
    ((5#5 : BitVec 5), (0x7C00#16 : BitVec 16)),
  chk "i32 -65536 to f16 overflows to -inf"
    (riscv_i32ToF16 0#3 0xFFFF0000#32)
    ((5#5 : BitVec 5), (0xFC00#16 : BitVec 16)),
  chk "i32 2049 to f16, inexact (11 bits into 11)"
    (riscv_i32ToF16 0#3 0x00000801#32)
    ((1#5 : BitVec 5), (0x6800#16 : BitVec 16))
]

open Axioms in
#eval report "float to float: one path, widening exact and narrowing rounded" [
  chk "f16 1.0 to f32, exact"
    (riscv_f16ToF32 0#3 0x3C00#16)
    ((0#5 : BitVec 5), (0x3F800000#32 : BitVec 32)),
  chk "f16 2^-24 (the smallest subnormal) becomes a NORMAL f32, exact"
    (riscv_f16ToF32 0#3 0x0001#16)
    ((0#5 : BitVec 5), (0x33800000#32 : BitVec 32)),
  chk "f16 maxfinite to f64, exact"
    (riscv_f16ToF64 0#3 0x7BFF#16)
    ((0#5 : BitVec 5), (0x40EFFC0000000000#64 : BitVec 64)),
  chk "f16 -inf to f64"
    (riscv_f16ToF64 0#3 0xFC00#16)
    ((0#5 : BitVec 5), (0xFFF0000000000000#64 : BitVec 64)),
  chk "f16 quiet NaN to f64 = f64's canonical NaN, no flag"
    (riscv_f16ToF64 0#3 0x7E00#16)
    ((0#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f16 signalling NaN to f64 = canonical NaN, invalid"
    (riscv_f16ToF64 0#3 0x7C01#16)
    ((16#5 : BitVec 5), (0x7FF8000000000000#64 : BitVec 64)),
  chk "f32 1.0 to f64, exact"
    (riscv_f32ToF64 0#3 0x3F800000#32)
    ((0#5 : BitVec 5), (0x3FF0000000000000#64 : BitVec 64)),
  chk "f32 2^-149 to f64 becomes normal, exact"
    (riscv_f32ToF64 0#3 0x00000001#32)
    ((0#5 : BitVec 5), (0x36A0000000000000#64 : BitVec 64)),
  chk "f64 1.0 to f32, exact"
    (riscv_f64ToF32 0#3 0x3FF0000000000000#64)
    ((0#5 : BitVec 5), (0x3F800000#32 : BitVec 32)),
  chk "f64 pi to f32, inexact"
    (riscv_f64ToF32 0#3 0x400921FB54442D18#64)
    ((1#5 : BitVec 5), (0x40490FDB#32 : BitVec 32)),
  chk "f64 maxfinite to f32 OVERFLOWS: +inf, overflow and inexact"
    (riscv_f64ToF32 0#3 0x7FEFFFFFFFFFFFFF#64)
    ((5#5 : BitVec 5), (0x7F800000#32 : BitVec 32)),
  chk "f64 maxfinite to f32 under RTZ gives f32's maxfinite"
    (riscv_f64ToF32 1#3 0x7FEFFFFFFFFFFFFF#64)
    ((5#5 : BitVec 5), (0x7F7FFFFF#32 : BitVec 32)),
  chk "f64 2^-140 to f32 falls SUBNORMAL, exact, no underflow"
    (riscv_f64ToF32 0#3 0x3730000000000000#64)
    ((0#5 : BitVec 5), (0x00000200#32 : BitVec 32)),
  chk "f64 2^-150 to f32 underflows to +0"
    (riscv_f64ToF32 0#3 0x3690000000000000#64)
    ((3#5 : BitVec 5), (0x00000000#32 : BitVec 32)),
  chk "f64 2^-149*1.5 to f32: underflow and inexact"
    (riscv_f64ToF32 0#3 0x36A8000000000000#64)
    ((3#5 : BitVec 5), (0x00000002#32 : BitVec 32)),
  chk "f64 signalling NaN to f32 = canonical NaN, invalid"
    (riscv_f64ToF32 0#3 0x7FF0000000000001#64)
    ((16#5 : BitVec 5), (0x7FC00000#32 : BitVec 32)),
  chk "f64 65504 to f16, exact at maxfinite"
    (riscv_f64ToF16 0#3 0x40EFFC0000000000#64)
    ((0#5 : BitVec 5), (0x7BFF#16 : BitVec 16)),
  chk "f64 65520 to f16: the midpoint rounds to +inf, overflow"
    (riscv_f64ToF16 0#3 0x40EFFE0000000000#64)
    ((5#5 : BitVec 5), (0x7C00#16 : BitVec 16)),
  chk "f64 65520 to f16 under RTZ gives maxfinite, overflow all the same"
    (riscv_f64ToF16 1#3 0x40EFFE0000000000#64)
    ((1#5 : BitVec 5), (0x7BFF#16 : BitVec 16)),
  chk "f64 2^-24 to f16 is the smallest subnormal, exact"
    (riscv_f64ToF16 0#3 0x3E70000000000000#64)
    ((0#5 : BitVec 5), (0x0001#16 : BitVec 16)),
  chk "f64 2^-25 to f16 underflows to +0"
    (riscv_f64ToF16 0#3 0x3E60000000000000#64)
    ((3#5 : BitVec 5), (0x0000#16 : BitVec 16)),
  chk "f32 2^-140 to f16 underflows to +0"
    (riscv_f32ToF16 0#3 0x00000200#32)
    ((3#5 : BitVec 5), (0x0000#16 : BitVec 16)),
  chk "f32 1.0 to bfloat16 = 0x3F80, exact"
    (riscv_f32ToBF16 0#3 0x3F800000#32)
    ((0#5 : BitVec 5), (0x3F80#16 : BitVec 16)),
  chk "f32 pi to bfloat16, inexact"
    (riscv_f32ToBF16 0#3 0x40490FDB#32)
    ((1#5 : BitVec 5), (0x4049#16 : BitVec 16)),
  chk "f32 pi to bfloat16 under RTZ"
    (riscv_f32ToBF16 1#3 0x40490FDB#32)
    ((1#5 : BitVec 5), (0x4049#16 : BitVec 16)),
  chk "f32 maxfinite to bfloat16 OVERFLOWS: bfloat16 has the same exponents but eight fewer bits"
    (riscv_f32ToBF16 0#3 0x7F7FFFFF#32)
    ((5#5 : BitVec 5), (0x7F80#16 : BitVec 16)),
  chk "f32 maxfinite to bfloat16 under RTZ gives bfloat16's maxfinite"
    (riscv_f32ToBF16 1#3 0x7F7FFFFF#32)
    ((1#5 : BitVec 5), (0x7F7F#16 : BitVec 16)),
  chk "f32 quiet NaN to bfloat16 = 0x7FC0, bfloat16's own canonical NaN"
    (riscv_f32ToBF16 0#3 0x7FC00000#32)
    ((0#5 : BitVec 5), (0x7FC0#16 : BitVec 16)),
  chk "f32 signalling NaN to bfloat16 = 0x7FC0, invalid"
    (riscv_f32ToBF16 0#3 0x7F800001#32)
    ((16#5 : BitVec 5), (0x7FC0#16 : BitVec 16)),
  chk "f32 -inf to bfloat16"
    (riscv_f32ToBF16 0#3 0xFF800000#32)
    ((0#5 : BitVec 5), (0xFF80#16 : BitVec 16)),
  chk "f32 2^-133 to bfloat16 is its smallest subnormal, exact"
    (riscv_f32ToBF16 0#3 0x00010000#32)
    ((0#5 : BitVec 5), (0x0001#16 : BitVec 16)),
  chk "f32 2^-134 to bfloat16 underflows to +0"
    (riscv_f32ToBF16 0#3 0x00008000#32)
    ((3#5 : BitVec 5), (0x0000#16 : BitVec 16)),
  chk "f32 2^-149 to bfloat16 underflows to +0"
    (riscv_f32ToBF16 0#3 0x00000001#32)
    ((3#5 : BitVec 5), (0x0000#16 : BitVec 16))
]

end Kinds
