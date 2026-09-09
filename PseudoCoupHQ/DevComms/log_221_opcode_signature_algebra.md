# log_221 — the arch-opcode mapping A → B, as an algebra: what it is, what we already hold, what it filters

Line-wide (research master plan; theory). Written 2026-09-06 by the
coordinator (Fable) in reply to the owner's question, verbatim:

> "i think understanding the arch opcode mapping (from `A` -> `B`)
> could also be useful for further atomizing/filtering the
> combinatorial space. `A` being the sets the input elements belong to
> and `B` being the sets the output elements belong to. i mean a fully
> closed mapping of the operator per input sets. at most partly feels
> regression-like/landscape-like. or something. idk. im sensing
> something there."

Opinion is marked; everything else is definition or measured.

## 1. What the mapping IS, one sentence, in relation

An arch opcode with its operand widths is a function from a tuple of
HOLDERS to a holder, where a holder is a set of bit patterns of one
width read under one class: the 32 holders task t101b measured
(`types101_holders.json`: signed / unsigned / float / truth / unicode
at widths 8 to 128). the owner's `A` is the tuple of input holders, his `B`
the output holder, and "the fully closed mapping per input sets" is
the table of every (opcode, input holders) → output holder the corpus
attests.

## 2. The one fact that shapes the whole table: at the machine, A is only width

- At the machine level, every holder of width w is the SAME set:
  the 2^w bit patterns. Signed, unsigned and float are not different
  sets; they are different READINGS of the same patterns. The
  language's type chooses the reading; the opcode either respects it
  or ignores it.
- So opcodes split by how they treat the reading, and this split is
  the atomization the owner is sensing:

| kind | opcodes (from task o2's 162) | what A → B looks like |
|---|---|---|
| reading-blind | `add sub and or xor not neg shl mov lea cmp`(for `==`) | same bits whatever the class: (w, w) → w; signed and unsigned are ONE mapping |
| sign-sensitive | `sar` vs `shr`, `idiv` vs `div`, `imul` vs `mul` (high half), `setl` vs `setb`, `cvtsi2ss` | two opcodes for one arithmetic idea, split by the reading of A |
| width-changing | `movzx movsx cltq cqto` and the term's `Extract Concat ZeroExt SignExt` | (w1) → w2; the reading decides zero- or sign-fill |
| reading-changing | `cvtsi2sd cvttsd2si` and the float family | integer holder ↔ float holder at a width |
| flag-producing | `cmp test` with `set*`/`j*`/`cmov*` | (w, w) → truth; the truth is read off flags, the machine's side channel |
| guarded | the bodies with `jo ud2 je … call panic` | a PARTIAL mapping: defined on part of A, another path on the rest |

- Opinion: "regression-like / landscape-like" is the last row. Every
  opcode is total on bit patterns, but the OPERATOR a language means
  is often partial: division is undefined at zero, swift's `+` traps
  on overflow, go's `/` panics. The landscape is the input space
  partitioned into the region where the arithmetic mapping holds and
  the regions where a guard sends control elsewhere. That partition
  IS the mode, and the pipeline already names it (guard-outcome rows,
  DIFFERS-BY-DESIGN, exception families, the directional bridge's
  "on projection P").

## 3. The algebra, stated

- Take the holders as SORTS and the (opcode, input holders → output
  holder) rows as OPERATION SYMBOLS. That is a many-sorted algebra:
  a finite signature, one per architecture.
- Every arch-unit's layer-4 term is a term of that algebra — the term
  walk builds exactly this: operators applied to sorted variables.
- Two units are the same dominant operator when their terms are equal
  under the algebra's equational theory, and for bit-vectors that
  theory is decidable: z3 is the decision procedure. The pool's
  entries are the equivalence classes the corpus reaches.
- A polyfill from language x to language y is a TRANSLATION between
  two such algebras: x's operation symbols expressed as terms over
  y's. It is total when every sort of x has a sort of y (or an
  encoding: 128-bit as two 64-bit words) and every operation of x has
  a term over y's operations. That coverage table, sorts × operations,
  is the derivability question made finite. Where a cell is empty the
  translation needs an idiom, proved once; where no idiom exists the
  cell is a named hole.
- Opinion: this is the thesis-shaped statement. The empirical results
  so far are instances of it: o7 (82–95% of x terms translate to c
  and prove), o8 (197 of 217 primitives land on the exact opcode),
  o2's 162-opcode vocabulary as the operation symbols, t101b's 32
  holders as the sorts.

## 4. What the table filters

- **Composition search.** A candidate composition of y-units for an
  x-unit is admissible only if its sorts line up: output holder of
  one feeds an input holder of the next, and the whole thing has x's
  input and output holders. Typed synthesis rejects the ill-sorted
  compositions before any solver call. The pool's 88 `type_key`
  buckets are already the coarse form of this filter (arrival
  register families | answer width); the holder table sharpens it to
  class and per-operand width. Measured effect of the coarse filter
  in t100: 43,410 candidate pairs instead of 1,831²/2 ≈ 1.67 million.
- **Reading-blind opcodes collapse the table.** Signed and unsigned
  `add` are one row; that is why go's `int32` and `uint32` `+` land
  in one pool entry, and why the "dominant operator" count is far
  below the language-operator count.
- **Guards separate rows that share arithmetic.** Swift's trapping
  `+` and c's wrapping `+` share the reading-blind `add` row and
  differ in the partition; the table records them as one operation
  with two modes, which is the exception family.

## 5. What exists, and the one census to build

- Sorts: `types101_holders.json` (32), `types101_entry_holders.json`
  (each pool entry's input and answer holders).
- Operations: `single_opcode_units.json` (243 rows with a proved term,
  each one opcode), and `unique_opcodes.json` (162 mnemonics).
- Missing: the JOIN — per opcode, the attested set of (input holders
  → output holder) rows, with the reading kind of §2 read off the
  data (does the same body serve a signed and an unsigned holder?
  then reading-blind), and the guard partition read off the ledger's
  guard-outcome rows. That is a census over existing json, one lane:
  task o9.

## 6. Awaiting the owner

- Whether this framing (sorts = holders, operations = opcode
  signatures, polyfill = translation between algebras) is the one the
  thesis carries; names for the reading kinds in §2 are provisional.

## 7. Addendum, same day: is constructing a provable emulation in P? (the owner's revised assessment, and the coordinator's)

the owner, verbatim: "i now agree with your original commentary that it is
not in NP. i believe it is in P because we are working within the
assumption that every language is Turing complete with fully
expressive arithmetic operators. and bounded sets. ... it collapses to
provable-equivalence. ... we could even use Lean potentially."

The coordinator's reading, split by which claim:

| claim | complexity | why |
|---|---|---|
| constructing SOME emulation of a term in y | linear in the term's size | syntax-directed rendering: one rule per operator, one idiom per missing sort or operator (constant size, proved once) |
| proving that emulation equals the term at the SOURCE level | linear, by structural induction on the term | each rule carries its lemma; the composition is the induction step; no solver, no search. This is the "induction proof" the owner names, and it is over the term's structure, not over input values |
| checking that the COMPILER's output equals the term | coNP-complete in theory (bit-vector equivalence), small in practice | the compiler is unverified, so its output is re-proved by z3; terms are short, so the gate answers in milliseconds except wide division |
| finding the SMALLEST emulation, or one the compiler lands on the exact opcode | superoptimization; hard, and compiler-version-dependent | not needed for correctness; o8 shows the compiler supplies it 91% of the time unasked |

- So: correct emulation, in P (linear); its proof, in P (structural);
  the machine-level check, coNP but cheap at our sizes; optimality,
  hard and not required. the owner's "collapses to provable-equivalence,
  not to the most optimal" is exactly the split.
- Probing intervals for the boundary where behaviour changes is the
  fuzz census's method (levels 1 and 2) and is the right tool where
  no term exists (loops). Where a term exists, z3 finds the boundary
  exactly as a counterexample; no probing is needed.
- Lean: feasible and the strongest evidence class available. Holders
  as fixed-width bit-vectors (`BitVec w`), terms as an inductive type,
  rendering as a function, and one theorem: evaluation of the term
  equals evaluation of the rendered source, by structural induction.
  Lean 4's `bv_decide` bit-blasts bit-vector goals to a SAT solver
  and CHECKS the certificate inside Lean, so the pool's term
  equivalences could be re-proved with a verified certificate, above
  z3's "tool testimony" in the evidence doctrine. A verified compiler
  (CompCert for c) would close the last gap, the compiler's own
  output, for that one target.
