# log 296 — the corpus quotiented, and the gate run wide

2026-09-17. Follows log 295. the owner's idea, and it is the reason this log has a
number in it that the line has wanted for a long time:

> actually, our new system could reduce the number of arch-units by proving
> equivalence via emulations.

## 1. The quotient

A compiler-operator is a (language, operator, operand types) triple, and many
triples lower to the SAME instruction sequence. c's `a & b` on two 64-bit
integers and c++'s `a bitand b` on the same types are one
`c.and a0, a1 ; c.jr ra`. Proving the emulation of one equal to the arch-unit
proves nothing new about the other — it IS the other.

`equivalence_classes.py` makes that a measurement.

### 1.1 The key, and the correction it needed

The first version keyed on the instruction sequence alone and reported
**1,312 arch-units → 304 classes, 4.3x**. That number is real but it belongs
to the `plain` goal, and log 294 §2.3 showed `plain` is FALSE BY CONSTRUCTION:
it puts the two sides together with no psABI precondition, so every
counterexample is a high-bit input the ABI forbids.

The goal actually worth proving is `abi`, and its statement WIDENS each
operand by how that operand arrives. Two units sharing a body but arriving
differently are different goals. The key therefore had to be the body **and**
the arrival shape — where the shape is what the widening depends on, not the
type's spelling, so `int32_t` and `int32` key alike.

| key | classes | reduction | sound for the goal we prove? |
|---|---|---|---|
| the body alone | 304 | 4.3x | **no** — that is the `plain` goal |
| **the body and the arrival shape** | **537** | **2.4x** | **yes, and nothing is owed** |

Caught before the classes were used for anything. The honest reduction is
**2.4x, free**: members of a class are not similar goals, they are the same
Lean goal, so one proof discharges the class with no second prover, no axiom
and no merge lemma.

### 1.2 The second level, and what it costs

Where the sequences differ but the walked terms agree — `subw a0, zero, a0`
and `sub a0, zero, a0` read at 32 bits; `c.jr ra` and `jalr zero, 0x0(ra)` —
a further merge is available: **537 → 390**, at the cost of **83 merge
lemmas**. Those are not free and are listed by name in the artifact's
`obligations`. z3 agreeing that two sequences are one function is evidence;
it is not the Lean proof the merge needs. Level 2 is not used below.

## 2. The gate, wide

The gate had been run on twelve hand-picked units, then ten. With the corpus
quotiented it can be run on **classes**, and the integer layer gives 186 of
them, covering 652 arch-units. Ten had ever been put to Lean. **176 never
had.**

Only the `abi` statement was put. `plain` is settled — false by construction
on the Lean path (log 294 §2.3) and independently on the cross-architecture
path (log 295 §2.2) — so spending 186 Lean runs to re-learn it would be
waste.

Lane `lp3_l105`. Both sides compiled for riscv64 at the census ship flags:
**186 of 186**. Then walked, then `equals`, with the simp set coming from
`leanpath.equals.simp_set` — the one place, so l101's three-layer assembly
rides.

| | classes | arch-units | share of units |
|---|---|---|---|
| **PROVED** | **100** | **462** | **71%** |
| UNDECIDED | 35 | 86 | 13% |
| NOT REACHED — a walk refused | 51 | 104 | 16% |

Proved at stage: `same_text` 33, `fixed_width` 65, `integer_level` 2.

**462 arch-units machine-certified equal to their emulations**, from a gate
that had certified seven the day before.

### 2.1 The classes that carry the most

| representative | covers | stage | languages |
|---|---|---|---|
| `au_237_c_postdec_f64` | 29 | same_text | c, cpp, rust |
| `au_198_c_sizeof_i64` | 15 | same_text | c, cpp |
| `au_348_c_bor_i64_i64` | 14 | same_text | c, cpp, rust |
| `au_364_c_bxor_i64_i64` | 14 | same_text | c, cpp, rust |
| `au_380_c_band_i64_i64` | 14 | same_text | c, cpp, rust |
| `au_244_c_add_i64_i64` | 10 | same_text | c, cpp, rust |
| `au_278_c_mul_bool_bool` | 10 | fixed_width | c, cpp, rust |

The quotient is what makes one theorem worth fourteen arch-units, and the
`languages` column is why: the same lowering is reached from c, c++ and rust
alike.

### 2.2 What did NOT prove, and it is two different things

**NOT REACHED, 51 classes.** This is the WALK refusing, not Lean failing.

| | count |
|---|---|
| the arch side certified, the emulation side refused | 29 |
| both refused | 20 |
| the arch side refused, the emulation certified | 2 |

The walk composes straight-line bodies only; an emulation that compiles to a
branch or a call is refused before Lean is reached. That is a limit of the
walk and is where the next engineering is, not a statement about provability.

**UNDECIDED, 35 classes.** These reached `bv_decide` and were not closed. The
shapes concentrate exactly where log 294 §2.4 said they would:

| lang | operands | classes |
|---|---|---|
| go | int32, int32 | 7 |
| c | int32_t, int32_t | 5 |
| c | int32_t, int64_t | 4 |
| go | int64, int64 | 4 |
| c | int64_t, int32_t | 3 |

Narrow integer comparisons and mixed widths — the `zopz0zI_u` / `Int.blt`
family. Sail defines its unsigned compare over `Int.blt`, `bv_decide` cannot
bitblast that, and Sail's Lean library ships no bridge to `BitVec.ult`. One
lemma shape stands between these 35 classes and a verdict.

## 3. Where the line now stands

| | count |
|---|---|
| arch-units, riscv64, four languages | 1,312 |
| proof obligations after the quotient | 537 |
| integer-layer classes put to Lean | 186 |
| **classes certified** | **100** |
| **arch-units those classes cover** | **462** |

## 4. Two lists

Decided, recorded for audit:

- `equivalence_classes.py` written, and re-keyed on the goal actually proved
  before any class was used; the body-only count is still reported so it
  cannot be mistaken for the real one;
- level 2 is computed and NOT used; its 83 owed lemmas are listed rather than
  folded into a count;
- lane lp3_l105 put only the `abi` statement, and says why in its own header;
- the simp set came from `leanpath.equals.simp_set`, not from a copy in the
  lane.

Awaiting the owner:

- **the `zopz0zI_u` bridge**, now sized: it is what stands between 35 classes
  (86 arch-units) and a verdict. Still hand-written Lean against Sail's
  mangled names unless it is generated from Sail's Prelude — which is what I
  would do, and still want the word on.
- the 51 NOT REACHED classes are the walk's branch-and-call refusal. Widening
  the walk is a bigger piece of engineering than the bridge and would move
  104 arch-units. Say which comes first.
