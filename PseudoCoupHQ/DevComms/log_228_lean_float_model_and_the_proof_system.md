# log_228 — the operator-mapping proof system: what Lean holds, the float model, and where proof cost actually is

Line-wide (research master plan; theory; the gate/lean node). Written
2026-09-07 by the coordinator (Fable) on the owner's instruction to make
"robust notes ... regarding the realizations of this conversation."
the owner's words are verbatim. Where the coordinator's earlier statements
were wrong, the wrong statement is quoted and the correction follows
it, per protocol §2.2 (retraction and replacement as two statements).
Nothing here is ruled unless it says so; the node is
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/CORE_0_3_1_5_6_lean.md`.

## 0. The two lists

### 0.1 Decided, recorded for audit
- Retracted: "floats stay with z3; Lean closes the integer side." That
  was an ordering opinion stated as a conclusion; the ordering is
  the owner's. the owner: "Lean is a potentially fundamental part of the
  operator-mapping proof system."
- Retracted: the 15–30 person-day estimate for a float model (log_227
  §5, repeated by the coordinator). Replaced by §4 below: the model
  and its lemmas are days; bit-blasting cost is a property of the
  fallback method, not of the model.
- Retracted: "aligning two exponents before adding means the exact
  sum lives in a wide bit-vector [and] the width ... is the difference
  between a fast proof and a slow one." True of bit-blasting only.
  In the abstract proof the width is a parameter and the proof does
  not grow with it (§3.3).
- Corrected: the coordinator's first answer about Lean's `Float`
  described the RUN-TIME instance type, which is opaque; the owner's
  question was about the ABSTRACT float. They are different objects
  (§2).

### 0.2 Awaiting the owner
- The plan for the lean node with the float model in from the start
  (a proposed order is in §6); whether the node's definition changes
  from "a second discharger of the gate" to "the operator-mapping
  proof system" — the owner's words — with the gate's z3 as the check on
  the unverified compiler.

## 1. the owner's commentary on this branch, verbatim

> "Lean is a potentially fundamental part of the operator-mapping
> proof system."

> "idu why your statement isnt: MATHLIB does not have the float
> model, however, SMT-LIB does. or if SMT-LIB doesnt, propose a float
> model. i have ideas already if the integer is defined using a bit
> vector of maximum size. the float is a signed integer with an
> implicit leading-1 with another signed integer for the exponent. i
> dont see how a float isnt a simpler definition than an abstract
> complex number."

> "im not sure if youre confusing the Lean evaluation of float
> numbers -- like actual instances of floats -- with the abstract
> object float. ... the abstract float wouldnt be converted to
> anything. it is what it is."

> "are you saying Lean doesnt have the ability to define cases? like
> exhaustively? and for each case, using induction to prove behavior?
> also, the rounding is a modulo function no? i can think of any
> number of ways to prove the full model of a mathematical operator
> involving floats."

> "either: (1) the model is literal, in which case, we are feeding in
> literal bit vectors and trivially proving the result of a
> calculation. spoon-fed; or (2) the abstract case precision doesnt
> increase the complexity of the proof beyond a scalar multiplier --
> per term precision ..."

> "SAT solver? the behavior of the arch opcode being models is so the
> arch-units can be used to emulate a single opcode. creating the
> building blocks of how to approximate mappings is also trivially
> true. arithmetic arch opcodes are probably the easiest. but other
> arch opcodes are also mappings. defining a mapping is remarkably
> easy with control flow. ... currently i dont see any barriers --
> especially not an NP barrier."

## 2. The two floats, named apart

- **Lean core's `Float`**: the run-time instance type. Verified in the
  image (`#print Float`): a structure over `floatSpec.float`, and
  `floatSpec` is declared `opaque`. Compiled to a native double; in
  the logic it has no equations. Useless for proof. This is the one
  the coordinator described first, wrongly, as "Lean's float".
- **The abstract float**: a value of a type WE define over bit-vectors.
  It is converted to nothing; it is what it is; the bit-blasting
  tactic and every bit-vector lemma apply to it because it is made of
  bit-vectors. Neither Lean core nor Mathlib defines it. Mathlib's
  `Real` is the mathematical reals, a different object with no
  rounding, no NaN, no signed zero.
- **The clean statement**: Mathlib does not have the float model.
  SMT-LIB does (the theory z3 implements: sign, exponent and
  significand as bit-vectors, every operation as exact-then-round
  under a named rounding mode). In Lean it is ours to write, and
  SMT-LIB's definition is the specification to transcribe.

## 3. The float model, as the owner stated it, and what it needs added

### 3.1 the owner's model is IEEE-754's representation for the normal numbers
- "a signed integer with an implicit leading-1 with another signed
  integer for the exponent": a sign, a significand of m bits with the
  leading 1 implicit, an exponent of e bits. Value = ±1.m × 2^exp.
- Two encoding differences from the standard, neither affecting
  correctness: the standard keeps the sign as its own bit
  (sign-magnitude, not two's complement), and stores the exponent
  biased (unsigned e-bit field minus a constant) rather than signed.
- To add, so the model equals the hardware on every bit pattern:
  subnormals (exponent field all zero, leading bit 0, no implicit 1);
  the two zeros; the two infinities (exponent field all ones,
  significand zero); NaN (exponent all ones, significand non-zero).
  Five classes, each a constructor or a predicate over the three
  fields; pattern matching makes the case split exhaustive.

### 3.2 Rounding is shift, compare, conditional increment
- the owner: "the rounding is a modulo function no?" Modulo keeps the LOW
  bits and discards the high; rounding keeps the HIGH bits and
  discards the low. So rounding is truncation (a right shift) plus a
  decision on the discarded bits:
    - round toward zero: shift, done;
    - round to nearest, ties to even: shift; if the discarded bits are
      above half, add 1; if exactly half and the kept low bit is 1,
      add 1; if the add carried out of the top, shift once more and
      bump the exponent;
    - the other modes: the same shape with a different condition.
- Each is a few lines over bit-vectors. An operation is: compute the
  exact result at a width that holds it, then round. Addition's exact
  result after exponent alignment, multiplication's 2m-bit product,
  division's quotient with enough extra bits to round correctly —
  all definable; the "sticky bit" (whether ANY discarded bit is set)
  is the one idiom that makes the exact width finite instead of
  unbounded, and it is standard.

### 3.3 Cases, induction, and why precision is a parameter
- Lean defines the cases exhaustively (a missing case is a compile
  error) and proves per case. Ordinary.
- Proofs about `BitVec w` operations are written for a variable `w`
  and hold for every width; the width is a parameter of the lemma,
  not a cost of the proof. So the owner's "(2) the abstract case precision
  doesnt increase the complexity of the proof beyond a scalar
  multiplier" is right, and stronger: for width-polymorphic proofs
  the multiplier is 1.
- The only method whose cost grows with width is bit-blasting, which
  builds a circuit of size proportional to the width (quadratic for
  multipliers) and hands it to SAT. That is where the coordinator's
  "wide exact sum" remark came from, and it applies to that method
  only.

## 4. Where proof cost actually is, and where it is not

### 4.1 The three kinds of proof obligation in the system
| obligation | how it is proved | cost |
|---|---|---|
| a unit whose term IS one operation of the model (a single-opcode unit) equals the model's operation | definitional: unfold, `rfl` | none |
| a unit or emulation whose term is a DIFFERENT expression equals the model's operation (multi-opcode bodies; rendered emulations; two entries' terms) | by rewriting with operator lemmas: commutativity, associativity, extract/concat laws, the rounding lemmas; each step a lemma application | linear in the length of the rewrite chain; finding the chain is the proof search |
| the same, when no chain is known | bit-blasting to SAT with a checked certificate (the fallback) | grows with width; the 283 s / 12 GB for 16-bit division is THIS row |

- the owner's "(1) literal, spoon-fed": the first row, and also every
  evaluation at concrete inputs (`decide`, `native_decide`).
- The rewrite route is the one the lemma library serves, and the
  lemma library is exactly the owner's earlier "cache patterns → lemmas":
  a rewrite chain found once for one pair is a lemma for every pair
  of that shape.
- So SAT is not fundamental. It is the brute-force fallback when the
  lemma library has a gap, and its cost measures the gap, not the
  problem.

### 4.2 Where hard work genuinely remains, and it is outside the algebra
- The COMPILER's output. A rendered emulation is proved equal to its
  term by structural induction (done: log_227 §4, the preservation
  theorem). But the machine code the compiler emits for that source
  is not the source; the compiler is unverified. Checking that its
  output equals the term is the gate's job (z3 against the reference
  simulator), or a verified compiler's job (CompCert for c). This is
  the one place a per-instance solver check is unavoidable, and it
  is not a Lean limitation; it is the price of trusting clang.
- Nothing else in the chain needs search: representation, operations,
  rounding, cases, translation between algebras (§5) are all
  definitions plus induction.

## 5. The operator-mapping proof system, as this branch leaves it

- Every arch opcode is a mapping between holders (log_221): a
  definition over bit-vectors, with control flow where the machine
  has it (guards, flags, the partial region). Arithmetic opcodes are
  the easiest; the others are the same kind of object with more
  cases. the owner: "defining a mapping is remarkably easy with control
  flow."
- Lean holds the algebra: sorts (holders) as `BitVec w` under a
  reading; operation symbols as definitions; the term language as an
  inductive type; equivalence of two terms as a theorem by rewriting
  (or bit-blasting as fallback); translation to a target language as
  a rendering function with its preservation theorem by structural
  induction (proved for the integer subset).
- There is no NP barrier in constructing an emulation or in proving
  it at the source level. The construction is a definition; the
  proof is an induction. the owner's assessment (log_221 §7) stands and is
  now sharper: "in P" undersells it — the source-level proof is
  linear and the construction is a table.
- z3 keeps one role: the unverified compiler's output, checked per
  instance against the reference simulator. And it keeps a second,
  practical role until the lemma library fills in: the fallback for
  term equivalences without a known rewrite chain.

## 6. A proposed order for the lean node (the owner's to rule)

1. The float model: sign, exponent, significand as bit-vectors; the
   five classes; decode; round-to-nearest-even and the other three
   modes as the shift-compare-increment functions; the five
   operations, comparisons, conversions. Days.
2. The model's own lemmas: encode/decode identity; each class's
   behaviour under each operation; overflow to infinity; NaN
   propagation; the rounding lemmas that the rewrite route needs.
   Days, mechanical.
3. The single-opcode float units against the model, definitionally
   (row one of §4.1): the reference simulator's semantics for
   `addss`, `mulsd`, `divss`, `ucomiss`, `cvtsi2ss` ... are the
   model's operations or they are not; each is a `rfl` or a named
   discrepancy. This is where the model is checked against the
   hardware's own reading, and it is the most valuable single step.
4. The multi-opcode float bodies and the rendered float emulations
   by rewriting; bit-blasting only where the chain is missing, with
   the cost recorded as the measure of the gap.
5. The integer side's remaining constructors (comparisons, truth
   connectives, guarded division) into the same library; the rust
   expression type with the same induction.

## 7. Process note
Task t104 (the commutative-order normalization with its audit) was
running when the previous coordinator process exited and did not
complete; its state on disk is unknown and it is not restarted on
this branch (the owner: "dont launch tasks").
