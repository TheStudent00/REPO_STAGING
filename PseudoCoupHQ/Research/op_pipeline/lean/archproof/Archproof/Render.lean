/-
Render.lean -- the renderer's preservation theorem, integer subset.

WHAT THIS FILE IS, in relation to the rest of the line:
  The pipeline's TERM is an arch-unit's computation as a bit-vector
  expression.  The RENDERER turns a term into an expression of a target
  language -- here C's integer expressions.  This file states both languages
  inside Lean, states the rendering as a function between them, and proves
  ONE theorem by structural induction: evaluating the rendered C expression
  gives exactly the term's value, for every term and every environment.
  That is the source-level half of log_221 section 7's claim, proved for
  every term of the subset at once instead of per instance.

WHY `evalC` ANSWERS AN OPTION AND `eval` DOES NOT
  A bit-vector expression is total: every operator has a value at every
  input.  A C expression is not.  C leaves a shift by a count of w or more
  UNDEFINED, and an undefined C expression has no value to compare against.
  So `evalC` answers `Option (BitVec w)`: `none` is "this C expression has
  undefined behaviour on this environment".  The theorem then says two
  things at once, and the second is the one that would otherwise be assumed:
    * the rendered expression is DEFINED on every environment (never `none`,
      so the renderer emitted the guards C needs), and
    * its value is the term's value.
  Modelling the undefined region as some convenient number instead -- zero,
  say -- would make the shift cases hold for free and prove nothing.

WHAT THE C MODEL COMMITS TO
  Every holder is an unsigned integer of width w, so + - * & | ^ ~ wrap and
  are fully defined (C's unsigned arithmetic).  Signedness enters only
  through explicit casts: `castS` is `(intV_t)e` and is how the arithmetic
  shift and the sign extension are written.  Signed OVERFLOW never arises,
  because no arithmetic is done on a signed holder.
-/
import Std.Tactic.BVDecide

namespace Archproof

/-- A value for every (width, slot).  Indexing by the width as well as the
slot is what makes a variable well-typed by construction: there is no way to
read a 32-bit slot as 64 bits. -/
def Env := (w : Nat) → Nat → BitVec w

/-- The term language: the integer subset of what the term walk emits. -/
inductive Term : Nat → Type where
  | var     : (w : Nat) → Nat → Term w
  | lit     : {w : Nat} → BitVec w → Term w
  | add     : {w : Nat} → Term w → Term w → Term w
  | sub     : {w : Nat} → Term w → Term w → Term w
  | mul     : {w : Nat} → Term w → Term w → Term w
  | and     : {w : Nat} → Term w → Term w → Term w
  | or      : {w : Nat} → Term w → Term w → Term w
  | xor     : {w : Nat} → Term w → Term w → Term w
  | not     : {w : Nat} → Term w → Term w
  | shl     : {w : Nat} → Term w → Term w → Term w
  | lshr    : {w : Nat} → Term w → Term w → Term w
  | ashr    : {w : Nat} → Term w → Term w → Term w
  | extract : {w : Nat} → (hi lo : Nat) → Term w → Term (hi - lo + 1)
  | concat  : {w₁ w₂ : Nat} → Term w₁ → Term w₂ → Term (w₁ + w₂)
  | zext    : {w : Nat} → (v : Nat) → Term w → Term v
  | sext    : {w : Nat} → (v : Nat) → Term w → Term v
  | eq      : {w : Nat} → Term w → Term w → Term 1
  | ite     : {w : Nat} → Term 1 → Term w → Term w → Term w

/-- The term's meaning.  Every case is a total bit-vector operation. -/
def eval : {w : Nat} → Term w → Env → BitVec w
  | _, .var w i,         e => e w i
  | _, .lit c,           _ => c
  | _, .add a b,         e => eval a e + eval b e
  | _, .sub a b,         e => eval a e - eval b e
  | _, .mul a b,         e => eval a e * eval b e
  | _, .and a b,         e => eval a e &&& eval b e
  | _, .or a b,          e => eval a e ||| eval b e
  | _, .xor a b,         e => eval a e ^^^ eval b e
  | _, .not a,           e => ~~~ eval a e
  | _, .shl a b,         e => eval a e <<< eval b e
  | _, .lshr a b,        e => eval a e >>> eval b e
  | _, .ashr a b,        e => (eval a e).sshiftRight' (eval b e)
  | _, .extract hi lo a, e => (eval a e).extractLsb hi lo
  | _, .concat a b,      e => eval a e ++ eval b e
  | _, .zext v a,        e => (eval a e).setWidth v
  | _, .sext v a,        e => (eval a e).signExtend v
  | _, .eq a b,          e => if eval a e == eval b e then 1#1 else 0#1
  | _, .ite c a b,       e => if eval c e == 1#1 then eval a e else eval b e

/-- The C integer expressions the renderer emits.  Holders are unsigned;
signedness is written with an explicit cast. -/
inductive CExpr : Nat → Type where
  | var   : (w : Nat) → Nat → CExpr w
  | lit   : {w : Nat} → BitVec w → CExpr w
  | add   : {w : Nat} → CExpr w → CExpr w → CExpr w
  | sub   : {w : Nat} → CExpr w → CExpr w → CExpr w
  | mul   : {w : Nat} → CExpr w → CExpr w → CExpr w
  | band  : {w : Nat} → CExpr w → CExpr w → CExpr w
  | bor   : {w : Nat} → CExpr w → CExpr w → CExpr w
  | bxor  : {w : Nat} → CExpr w → CExpr w → CExpr w
  | bnot  : {w : Nat} → CExpr w → CExpr w
  /-- `a << k` on the unsigned holder.  UNDEFINED when `k` is `w` or more. -/
  | shlC  : {w : Nat} → CExpr w → CExpr w → CExpr w
  /-- `a >> k` on the unsigned holder: the logical shift.  Same undefined
  region. -/
  | shrC  : {w : Nat} → CExpr w → CExpr w → CExpr w
  /-- `(uintW_t)((intW_t)a >> k)`: the arithmetic shift, written through the
  signed holder.  Same undefined region. -/
  | sarC  : {w : Nat} → CExpr w → CExpr w → CExpr w
  /-- `(uintV_t)e` -- truncation or zero extension, always defined. -/
  | castU : {w : Nat} → (v : Nat) → CExpr w → CExpr v
  /-- `(uintV_t)(intV_t)(intW_t)e` -- the value read as signed, then widened
  or truncated. -/
  | castS : {w : Nat} → (v : Nat) → CExpr w → CExpr v
  /-- `a == b`, whose C value is 0 or 1, held in the one-bit holder. -/
  | ceq   : {w : Nat} → CExpr w → CExpr w → CExpr 1
  /-- `a < b` on the unsigned holders. -/
  | cult  : {w : Nat} → CExpr w → CExpr w → CExpr 1
  /-- `a << n` where `n` is a plain integer literal.  C's shift count is an
  `int` after the usual promotions, NOT a value of the shifted type, so a
  count that does not fit the holder is still a legal C expression.  The
  value-counted `shlC` above is for a count that is itself a computed holder;
  this one is for the counts the renderer writes itself. -/
  | shlN  : {w : Nat} → CExpr w → Nat → CExpr w
  /-- `a >> n` on the unsigned holder, `n` a plain integer literal. -/
  | shrN  : {w : Nat} → CExpr w → Nat → CExpr w
  /-- `(uintW_t)((intW_t)a >> n)`, `n` a plain integer literal. -/
  | sarN  : {w : Nat} → CExpr w → Nat → CExpr w
  /-- `c ? a : b`.  C evaluates only the branch it takes, and so does this. -/
  | csel  : {w : Nat} → CExpr 1 → CExpr w → CExpr w → CExpr w

/-- The C expression's meaning.  `none` is "undefined behaviour here". -/
def evalC : {w : Nat} → CExpr w → Env → Option (BitVec w)
  | _, .var w i,    e => some (e w i)
  | _, .lit c,      _ => some c
  | _, .add a b,    e => match evalC a e, evalC b e with
                         | some x, some y => some (x + y) | _, _ => none
  | _, .sub a b,    e => match evalC a e, evalC b e with
                         | some x, some y => some (x - y) | _, _ => none
  | _, .mul a b,    e => match evalC a e, evalC b e with
                         | some x, some y => some (x * y) | _, _ => none
  | _, .band a b,   e => match evalC a e, evalC b e with
                         | some x, some y => some (x &&& y) | _, _ => none
  | _, .bor a b,    e => match evalC a e, evalC b e with
                         | some x, some y => some (x ||| y) | _, _ => none
  | _, .bxor a b,   e => match evalC a e, evalC b e with
                         | some x, some y => some (x ^^^ y) | _, _ => none
  | _, .bnot a,     e => match evalC a e with
                         | some x => some (~~~ x) | _ => none
  | w, .shlC a b,   e => match evalC a e, evalC b e with
                         | some x, some k =>
                             if k.toNat < w then some (x <<< k) else none
                         | _, _ => none
  | w, .shrC a b,   e => match evalC a e, evalC b e with
                         | some x, some k =>
                             if k.toNat < w then some (x >>> k) else none
                         | _, _ => none
  | w, .sarC a b,   e => match evalC a e, evalC b e with
                         | some x, some k =>
                             if k.toNat < w then some (x.sshiftRight' k) else none
                         | _, _ => none
  | w, .shlN a n,   e => match evalC a e with
                         | some x => if n < w then some (x <<< n) else none
                         | _ => none
  | w, .shrN a n,   e => match evalC a e with
                         | some x => if n < w then some (x >>> n) else none
                         | _ => none
  | w, .sarN a n,   e => match evalC a e with
                         | some x => if n < w then some (x.sshiftRight n) else none
                         | _ => none
  | _, .castU v a,  e => match evalC a e with
                         | some x => some (x.setWidth v) | _ => none
  | _, .castS v a,  e => match evalC a e with
                         | some x => some (x.signExtend v) | _ => none
  | _, .ceq a b,    e => match evalC a e, evalC b e with
                         | some x, some y => some (if x == y then 1#1 else 0#1)
                         | _, _ => none
  | _, .cult a b,   e => match evalC a e, evalC b e with
                         | some x, some y => some (if x.ult y then 1#1 else 0#1)
                         | _, _ => none
  | _, .csel c a b, e => match evalC c e with
                         | some cv => if cv == 1#1 then evalC a e else evalC b e
                         | _ => none

/-- The guard C needs on a shift: `(uintW1_t)k < (uintW1_t)w`, computed one
bit wider than the holder so the width itself is always representable.  At
`w = 1` the count `1` does not fit in a one-bit holder, which is why the
comparison is not made at width `w`. -/
def shiftInRange (w : Nat) (k : CExpr w) : CExpr 1 :=
  .cult (.castU (w + 1) k) (.lit (BitVec.ofNat (w + 1) w))

/-- The rendering: one rule per term constructor. -/
def render : {w : Nat} → Term w → CExpr w
  | _, .var w i        => .var w i
  | _, .lit c          => .lit c
  | _, .add a b        => .add (render a) (render b)
  | _, .sub a b        => .sub (render a) (render b)
  | _, .mul a b        => .mul (render a) (render b)
  | _, .and a b        => .band (render a) (render b)
  | _, .or a b         => .bor (render a) (render b)
  | _, .xor a b        => .bxor (render a) (render b)
  | _, .not a          => .bnot (render a)
  | w, .shl a b        =>
      .csel (shiftInRange w (render b)) (.shlC (render a) (render b)) (.lit 0#w)
  | w, .lshr a b       =>
      .csel (shiftInRange w (render b)) (.shrC (render a) (render b)) (.lit 0#w)
  | w, .ashr a b       =>
      -- Out of range, C is undefined and the bit-vector answer is the sign
      -- bit repeated, which the in-range shift by w-1 already produces.
      -- Out of range, C is undefined and the bit-vector answer is the sign
      -- bit repeated, which the in-range shift by w-1 already produces.  At
      -- a zero-width holder there is no such shift, and no bits either, so
      -- the zero holder is the answer.
      .csel (shiftInRange w (render b))
            (.sarC (render a) (render b))
            (if w - 1 < w then .sarN (render a) (w - 1) else .lit 0#w)
  | _, @Term.extract w hi lo a =>
      if lo < w then .castU (hi - lo + 1) (.shrN (render a) lo)
      else .lit 0#(hi - lo + 1)
  | _, @Term.concat w₁ w₂ a b =>
      if w₂ < w₁ + w₂ then
        .bor (.shlN (.castU (w₁ + w₂) (render a)) w₂)
             (.castU (w₁ + w₂) (render b))
      else .castU (w₁ + w₂) (render b)
  | _, .zext v a       => .castU v (render a)
  | _, .sext v a       => .castS v (render a)
  | _, .eq a b         => .ceq (render a) (render b)
  | _, .ite c a b      => .csel (render c) (render a) (render b)


/- ------------------------------------------------------------------
   The bit-vector facts the shift, slice and append cases rest on.  Each
   is stated on its own so that, if one does not close, the report can
   name exactly which fact the renderer's proof is waiting for.
   ------------------------------------------------------------------ -/

/-- A width always fits in a holder one bit wider, so the shift guard can be
computed there.  At `w = 1` the count `1` does not fit a one-bit holder, which
is the whole reason the guard is computed at `w + 1`. -/
theorem w_mod_pow (w : Nat) : w % 2 ^ (w + 1) = w := by
  have h1 : w < 2 ^ w := Nat.lt_two_pow_self
  have h2 : (2 : Nat) ^ w ≤ 2 ^ (w + 1) := Nat.pow_le_pow_right (by omega) (by omega)
  exact Nat.mod_eq_of_lt (by omega)

/-- The guard says exactly what the C standard asks: is the count below the
width. -/
theorem shiftInRange_says {w : Nat} (k : CExpr w) (e : Env) (kv : BitVec w)
    (h : evalC k e = some kv) :
    evalC (shiftInRange w k) e = some (if kv.toNat < w then 1#1 else 0#1) := by
  simp [shiftInRange, evalC, h, BitVec.ult, w_mod_pow]

/-- An arithmetic right shift by the width or more gives the same holder as a
shift by `w - 1`: both fill with the sign bit.  OPEN.  Core ships
`BitVec.getLsbD_sshiftRight`, whose out-of-range answer is `x.msb`; the step
this is waiting for is the bridge from that `msb` to the bit at `w - 1` that
the in-range shift reads, which core states as
`BitVec.msb_eq_getLsbD_last`. -/
theorem sshiftRight_out_of_range {w : Nat} (x : BitVec w) (n : Nat) (h : w ≤ n) :
    x.sshiftRight n = x.sshiftRight (w - 1) := by
  apply BitVec.eq_of_getLsbD_eq
  intro i hlt
  simp only [BitVec.getLsbD_sshiftRight]
  have h1 : ¬ (n + i < w) := by omega
  by_cases h0 : i = 0
  · subst h0
    have h2 : w - 1 + 0 < w := by omega
    simp only [h1, h2, if_false, if_true, decide_eq_true_eq]
    first
    | simp [BitVec.msb_eq_getLsbD_last]
    | simp [BitVec.getLsbD_last]
    | rfl
  · have h3 : ¬ (w - 1 + i < w) := by omega
    simp [h1, h3]

/-- Appending two holders is a widen, a shift and an or -- which is how C
writes it, having no append of its own.  The shift count is a plain integer,
which is what C's shift operand is. -/
theorem append_as_shift_or {w₁ w₂ : Nat} (a : BitVec w₁) (b : BitVec w₂) :
    a ++ b = ((a.setWidth (w₁ + w₂)) <<< w₂) ||| (b.setWidth (w₁ + w₂)) := by
  apply BitVec.eq_of_getLsbD_eq
  intro i hlt
  simp only [BitVec.getLsbD_append, BitVec.getLsbD_or, BitVec.getLsbD_shiftLeft,
             BitVec.getLsbD_setWidth]
  by_cases hi : i < w₂
  · simp [hi]
    try (intro _; omega)
  · have h2 : i - w₂ < w₁ := by omega
    have hb0 : b.getLsbD i = false := by
      first
      | exact BitVec.getLsbD_ge b i (by omega)
      | exact BitVec.getLsbD_of_ge b i (by omega)
      | (apply BitVec.getLsbD_ge; omega)
      | simp [BitVec.getLsbD_ge, Nat.le_of_not_lt hi]
    simp [hi, h2, hlt, hb0, show i - w₂ < w₁ + w₂ by omega]
    try (intro _; omega)

/-- THE PRESERVATION THEOREM.  For every term of the integer subset and every
environment, the rendered C expression is defined and its value is the term's
value. -/
theorem render_preserves : {w : Nat} → (t : Term w) → (e : Env) →
    evalC (render t) e = some (eval t e) := by
  intro w t
  induction t with
  | var w i => intro e; simp [render, evalC, eval]
  | lit c => intro e; simp [render, evalC, eval]
  | add a b iha ihb => intro e; simp [render, evalC, eval, iha, ihb]
  | sub a b iha ihb => intro e; simp [render, evalC, eval, iha, ihb]
  | mul a b iha ihb => intro e; simp [render, evalC, eval, iha, ihb]
  | and a b iha ihb => intro e; simp [render, evalC, eval, iha, ihb]
  | or a b iha ihb => intro e; simp [render, evalC, eval, iha, ihb]
  | xor a b iha ihb => intro e; simp [render, evalC, eval, iha, ihb]
  | not a iha => intro e; simp [render, evalC, eval, iha]
  | @shl w' a b iha ihb =>
      intro e
      have hg := shiftInRange_says (render b) e (eval b e) (ihb e)
      simp only [render, eval, evalC, hg, iha e, ihb e]
      by_cases hb : (eval b e).toNat < w'
      · simp [hb]
      · simp [hb, BitVec.shiftLeft_eq_zero (Nat.le_of_not_lt hb)]
  | @lshr w' a b iha ihb =>
      intro e
      have hg := shiftInRange_says (render b) e (eval b e) (ihb e)
      simp only [render, eval, evalC, hg, iha e, ihb e]
      by_cases hb : (eval b e).toNat < w'
      · simp [hb]
      · simp [hb, BitVec.ushiftRight_eq_zero (Nat.le_of_not_lt hb)]
  | @ashr w' a b iha ihb =>
      intro e
      have hg := shiftInRange_says (render b) e (eval b e) (ihb e)
      simp only [render, eval, evalC, hg, iha e, ihb e]
      by_cases hb : (eval b e).toNat < w'
      · simp [hb]
      · by_cases hw : w' - 1 < w'
        · simp only [hb, hw, if_false, if_true, BitVec.sshiftRight', evalC]
          simp [hw, iha e, sshiftRight_out_of_range _ _ (Nat.le_of_not_lt hb)]
        · have hz : w' = 0 := by omega
          subst hz
          simp only [hb, hw, if_false, evalC]
          simp only [show ((0#1 : BitVec 1) == 1#1) = false from by decide,
                     Bool.false_eq_true, if_false, Option.some.injEq]
          apply BitVec.eq_of_getLsbD_eq
          intro i hlt
          omega
  | @extract w' hi lo a iha =>
      intro e
      by_cases hlo : lo < w'
      · simp only [render, eval, evalC, iha e, hlo, if_true, Option.some.injEq]
        apply BitVec.eq_of_toNat_eq
        simp [BitVec.extractLsb, BitVec.extractLsb', BitVec.toNat_setWidth,
              BitVec.toNat_ushiftRight, BitVec.toNat_ofNat]
      · simp only [render, eval, evalC, iha e, hlo, if_false, Option.some.injEq]
        have h1 : (eval a e).toNat < 2 ^ w' := (eval a e).isLt
        have h2 : (2 : Nat) ^ w' ≤ 2 ^ lo :=
          Nat.pow_le_pow_right (by omega) (Nat.le_of_not_lt hlo)
        have hz : (eval a e).toNat >>> lo = 0 := by
          rw [Nat.shiftRight_eq_div_pow]
          exact Nat.div_eq_of_lt (by omega)
        simp [BitVec.extractLsb, BitVec.extractLsb', BitVec.toNat_ushiftRight, hz]
  | @concat w₁ w₂ a b iha ihb =>
      intro e
      by_cases hw : w₂ < w₁ + w₂
      · simp [render, eval, evalC, iha e, ihb e, hw, append_as_shift_or]
      · have hz : w₁ = 0 := by omega
        subst hz
        simp only [render, eval, evalC, iha e, ihb e, hw, if_false, Option.some.injEq]
        apply BitVec.eq_of_getLsbD_eq
        intro i hlt
        simp [BitVec.getLsbD_append, BitVec.getLsbD_setWidth]
        intro _
        omega
  | zext v a iha => intro e; simp [render, evalC, eval, iha]
  | sext v a iha => intro e; simp [render, evalC, eval, iha]
  | eq a b iha ihb => intro e; simp [render, evalC, eval, iha, ihb]
  | ite c a b ihc iha ihb =>
      intro e
      simp only [render, eval, evalC, ihc e, iha e, ihb e]
      split <;> simp_all

end Archproof
