# The lemmas this task owes, each with its statement

Written by task t2 (`PRIVATE/PseudoCoupHQ/Research/briefs/task_t2_brief.md`).
Node: `hq.research.compiler_graph.gate.lean`.

The brief asks for the adder's and the shifter's lemmas at least, and
for the others to be **listed as owed with their statement**. This file
is that list. Nothing here carries `sorry`: a statement that is owed is
written as prose and as Lean SYNTAX inside a comment, and there is no
`.lean` file claiming it.

The lemmas that ARE machine checked are generated and run by
`construct/lean/run_lemmas_t2.py prove`, one `lean` process per theorem,
and recorded in `construct/lean/lemmas_t2.json`. Their two sides are
printed from `construct/schemas.py` itself, so a lemma cannot state
something the tier does not do.

---

## 1. The general-width lemma, owed for every schema

Every lemma below is machine checked AT A WIDTH. The general statement
is one theorem per schema over `BitVec w` for every `w`, proved by
induction on the limb count. `bv_decide` — the bit-blasting tactic this
project's proof system already uses — decides a goal at a FIXED width
and cannot be handed a variable one, so the general statement needs a
proof in `BitVec.toNat` arithmetic instead, which is a different piece
of work.

The adder's, written out, so the shape of what is owed is on the record:

```lean
theorem ripple_add_general {w : Nat} (a1 a0 b1 b0 : BitVec w) :
    (a1 ++ a0) + (b1 ++ b0)
      = (a1 + b1 + (if (a0 + b0) < a0 then 1 else 0)) ++ (a0 + b0)
```

and its induction step over limb counts, which is what makes it a lemma
about the SCHEMA rather than about two limbs:

```lean
theorem ripple_add_limbs {w n : Nat} (a b : Fin n → BitVec w) :
    value (add_limbs a b) = value a + value b
```

where `value` is the limb list read as one `BitVec (n * w)`.

---

## 2. Owed: the high half of a product

`schema_product_high_<width>_<word>.lean` IS generated and stated at
every width of the ladder, and `bv_decide` does not close any of them:
the SAT solver times out. The statement, at 128 over 64:

```lean
theorem schema_product_high_128_64 (v0 v1 v2 v3 : BitVec 64) :
    ((v0 ++ v1) * (v2 ++ v3)).extractLsb 127 64 = <schemas.mul_hi_word's own term>
```

This is a MITER OF TWO MULTIPLIERS, which is the shape SAT is known to
be worst at, and the brief says so in advance: "never a wide multiply or
divide by bit-blasting alone — those go to 2 or are reported." It is
reported. What would close it is an algebraic proof in `BitVec.toNat`:

```lean
theorem mul_hi_word {w : Nat} (x y : BitVec (2 * w)) :
    ((x * y).toNat) = x.toNat * y.toNat % 2 ^ (2 * w)
    -- and the schoolbook identity
    --   (x1·2^w + x0)(y1·2^w + y0)
    --     = x1·y1·2^(2w) + (x1·y0 + x0·y1)·2^w + x0·y0
    -- carried through `BitVec.toNat_mul`, `BitVec.toNat_append` and
    -- `Nat.add_mul_div_left`, which `omega` cannot do because the
    -- statement is not linear.
```

## 3. Owed: divide and remainder, at every width

The divider's lemma is not even STATED, and the cause is measured rather
than assumed: a theorem's statement is the term WRITTEN OUT, a printed
term names no intermediate, and restoring division reads its own
previous remainder three times per step — so the statement grows like
`3^width`. `run_lemmas_t2.py` refuses it at or above 200,000 nodes and
records the measured size (`TOO_LARGE_TO_STATE`); it is the same ceiling
and the same reason that stops the RENDERER writing the divider's source
(`construct.UNFOLDED_CEILING`).

What is owed is therefore two things, in this order:

1. a way to STATE it — a translation to Lean that names intermediates
   (`let`), which `op_pipeline/lean/term_to_lean.py` does not do today
   and which is not this task's file to change;
2. then the proof, which is an induction over the loop's steps with the
   restoring-division invariant:

```lean
theorem restoring_step {w : Nat} (a b rem : BitVec w) (i : Nat) :
    -- after step i the remainder is the dividend's top (w - i) bits
    -- modulo the divisor, and the quotient's bits above i are the
    -- corresponding quotient bits
    True   -- the statement is owed with the translation above
```

## 4. Owed: the widening schema at an arbitrary extract offset

`schemas.lower_extract` handles an extract at ANY pair of offsets and the
lemmas state two of them — the low word and the high word. So
`schemas.EXHAUSTIVE[WIDEN]` is False and the tier's lemma route is not
offered where the widening schema is among the instances; z3 answers
those. What is owed is one theorem per offset the population actually
uses, which is mechanical (the instance rows would carry the offsets) and
is not done here.

The same flag is False for `shifts, rotates`, for the same kind of
reason: the schema handles the two rotates and the lemmas state the three
shifts.

## 5. Owed: the float schemas, and the wall in front of them

`float add / sub / mul / div / compare / convert` at 32, 64 and 80 bits
is owed WHOLE. `construct/schemas.py` states the shape — the integer
schemas over the fields sign, exponent and significand with the sticky
bit, and the five classes as a case split — and constructs nothing,
because a softfloat that is nearly right is a wrong mapping that looks
like a right one.

And the population that needs it cannot be reached from this side today
even if it were written. Every one of the x87 places the bank refuses is
refused at the ARRIVAL or the ANSWER HOME, not at the operation: the
value arrives as a value on the x87 register stack, rust, go and swift
have no holder that can receive it (`handful.TARGETS_WITH_AN_80_BIT_
HOLDER` is `("c", "cpp")`), and c's own `long double` and z3's
`FPSort(15, 64)` do not spell the same bits. Constructing over the fields
would mean the emulation receives the value as integers instead, which is
a change to the ARRIVAL CONTRACT — a different question, and one for the
coordinator.
