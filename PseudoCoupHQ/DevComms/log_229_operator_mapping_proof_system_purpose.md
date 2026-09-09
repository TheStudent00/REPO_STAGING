# log_229 — the operator-mapping proof system: the purpose log_228 left out, what in log_228 stands, and what was over-corrected

Line-wide (research master plan; theory). Written 2026-09-07 by the
coordinator (Fable) at the owner's request after reading
`PseudoCoupHQ/DevComms/log_228_lean_float_model_and_the_proof_system.md`,
a branch conversation's record. the owner's own words about that log: it
"didnt capture the grander purpose beyond the float model proofs.
particularly how the automated study of arch opcode behavior
(complete mapping model) being used to construct the same behavior
using via emulation with other language arch-units." Opinion is
marked; the rest is definition or measured.

## 1. The purpose, stated once, top down

The operator-mapping proof system is the chain from the machine's
own semantics to proved polyfills, with every link a definition or a
theorem and only one link a per-instance check.

| level | object | what it is, in relation | state 2026-09-07 |
|---|---|---|---|
| 0 | the complete mapping model of every arch opcode | for each opcode and operand widths, the total function on bit patterns, INCLUDING the flags it writes and the partial region where a guard sends control elsewhere; the hardware's own reading, not a language's | held today as the reference simulator (`reference.py`, VEX semantics) and the opcode table; not yet a Lean definition |
| 1 | an arch-unit as a term | a composition of level-0 mappings, read off the unit's machine code by the ledger and the term walk | 27,866 of 30,280 units have a proved term |
| 2 | dominant operators | the equivalence classes of terms under the algebra's equational theory (decidable for bit-vectors) | the pool: 1,831 entries; 226 more proved edges (t100); normalization gap being closed (t104) |
| 3 | emulation, the translation between two languages' algebras | x's mapping rebuilt from y's operations: EITHER rendered to y's source operators and lowered by y's compiler (o7, o8, o11), OR composed directly from y's arch-units (synthesis, not yet run) | source route: 76–95% proved per target; 91–93% land on the exact primitive; preservation theorem proved for the integer subset (L1) |
| 4 | AutoPoly, and the Hub as source composition | the proved emulations, kept per (dominant operator, target language), as the polyfill library; the Hub's egress composes them | brainstorm stage; `SUPPORT_BRAINSTORM_autopoly.md` |

The sentence that ties them, which log_228 did not write: **the automated
study of arch-opcode behaviour is level 0, and it is what makes
levels 3 and 4 complete rather than heuristic.** An emulation is
derived FROM the model of the opcode's mapping, so it covers the
opcode's whole landscape, guards included, by construction; the
compiler then shows (levels 3's measurement) whether it collapses the
emulation back to the primitive; the proof system shows it computes
the same mapping either way.

## 2. What in log_228 stands

- **The float model as the owner stated it** (§3): sign, an implicit-leading-1
  significand, an exponent, as bit-vector fields; five classes
  (normal, subnormal, zero, infinity, NaN) as an exhaustive case
  split; rounding as shift, compare, conditional increment, with the
  sticky bit making the exact width finite. This is IEEE-754's own
  structure and how every software float library and every hardware
  unit is built. Correct as stated.
- **Width as a parameter** (§3.3): proofs over `BitVec w` for variable
  w do not grow with w. Correct. Bit-blasting is the one method whose
  cost grows with width, and it is a fallback.
- **The three obligations** (§4.1): definitional (a single-opcode unit
  IS the model's operation), by rewriting with lemmas, by bit-blasting
  as fallback whose cost measures the lemma library's gap. Correct,
  and the best framing in the log.
- **The one per-instance check that cannot be removed** (§4.2): the
  unverified compiler's output, checked by the gate against the
  reference, or by a verified compiler. Correct.
- **No NP barrier** (§5): construction is a definition, source-level
  proof is an induction. Correct; it is log_221 §7 restated.

## 3. What in log_228 was over-corrected (opinion, held to the evidence)

- **The estimate for floating point.** log_228 §0.1 retracts "15–30
  person-days" and replaces it with "days". The right split is
  neither number alone:
    - the MODEL (fields, classes, rounding, the five operations,
      comparisons, conversions): days, as §3 says;
    - the single-opcode float units checked against the model
      definitionally: days;
    - the LEMMA LIBRARY that makes the rewrite route work for
      multi-opcode float bodies and rendered float emulations: weeks.
      This is the measured experience of every published float
      formalization (Flocq in Coq, the HOL IEEE libraries): the
      rounding lemmas that compose — "round after exact is the same
      as round after round at a wider width", the sticky-bit
      correctness, the error bounds — are the ones that take experts
      long, and they are exactly the lemmas the rewrite route needs
      when a body does two float operations in a row;
    - until that library exists, bit-blasting is what runs for those
      bodies, and the 16-bit division at 283 s / 12 GB is its price.
  So: the model is cheap, the compositional proofs are not, and the
  retraction should have said both.
- **Tone.** Four retractions in a row read as capitulation rather
  than calibration. Two of them were right (the ordering opinion;
  the width remark for the abstract proof), one was partial (the
  estimate, above), one was a definitional clarification (run-time
  `Float` versus the abstract float) that needed no retraction at
  all. The evidence doctrine applies to the coordinator's own claims:
  a corrected claim is replaced by the corrected claim, not by
  agreement.

## 4. Expert insights, beyond what log_228 covers

### 4.1 Level 0 should be DERIVED from the reference, not written twice
- The reference simulator already holds every opcode's mapping as
  code (VEX semantics through pyvex, plus the pipeline's own opcode
  table). A Lean model written by hand beside it would be a second
  reading of the hardware, and two readings can disagree silently.
- Opinion: the first Lean artifact for level 0 is a TRANSLATOR from
  the opcode table's semantics to Lean definitions, so the model and
  the gate's simulator are one source. Then the single-opcode checks
  (log_228's step 3) test the translator, and a discrepancy is a
  finding about one of the two readings, located.

### 4.2 The other opcodes are mappings too, and the term language must grow to hold them
- the owner: "other arch opcodes are also mappings. defining a mapping is
  remarkably easy with control flow." Agreed, with the shapes named:
    - flag producers and readers: the mapping's output includes the
      flags word; `cmov`, `set`, `j` read it. The ledger already has
      flag rows; the term language needs flags as an explicit
      output sort, not a side channel.
    - control transfer: a guard is `ite` over which block runs; a
      body with branches is one term with `ite` at each join, which
      the walk already does for straight-line joins and refuses for
      cycles.
    - memory: loads and stores over an addressable area (the seventh
      block kind). The mapping's domain gains a memory state. This is
      where aliasing lives and where proofs get genuinely hard; it is
      also where the 5 `movb` store rows o8 could not emulate sit.
    - loops: `rep` string operations and the digit loops of t103.
      Bounded by a count they fold to a term; unbounded they need an
      invariant. This is the walk's one refusal today and it blocks
      two populations (the 128-bit library routines, the interpreter
      handlers).
- So the frontier of the mapping model is not arithmetic, and not
  floats: it is memory and loops. Arithmetic and floats are
  definitions; memory and loops are where invariants enter.

### 4.3 The two producers of an emulation, and why both matter
- The source route (render, compile, carve) uses the compiler as an
  unverified but highly capable simplifier; the compiler's collapse
  rate (91–93% to the exact primitive) is a measurement of the
  optimizer, and its output must be re-checked.
- The synthesis route (compose y's arch-units directly, guided by
  counterexamples) needs no compiler and yields machine-level
  compositions the gate proves directly; it is bounded search at our
  term sizes (log_221 §7's discussion, and the reply of 2026-09-06 on
  counterexample-guided synthesis).
- Opinion: run both, because agreement between two independent
  producers of the same emulation is the oracle this research line
  was founded on, and disagreement locates a defect in one of them.
  The synthesis route is not yet run; it is one task.

### 4.4 What "complete" means for the mapping model, and how it is measured
- Complete = for every opcode the corpus uses (162 today; the
  architecture has more), the model's mapping agrees with the
  hardware on every bit pattern, flags included, and the partial
  region is named.
- Measurable in three ways, weakest to strongest: fuzz agreement on
  sampled inputs (the census method); z3 equivalence of the model
  against the reference for each opcode (bit-blasting, feasible per
  opcode at ≤64 bits except division-like ones); Lean definitional
  agreement once the model is derived from the reference (§4.1),
  which turns the question into "is the translator right".
- The hardware itself is the last oracle: executing the opcode on
  the machine for sampled inputs and comparing with the model, which
  the fuzz line's runners can do.

### 4.5 On sycophancy, as a standing instruction to any agent on this line
- A claim of the owner's that is right is confirmed with the reason it is
  right, once. A claim that is partly right is split, and the part
  that is not right is said. A corrected claim of the agent's is
  replaced, not apologised for. Agreement is not evidence and is
  never the deliverable.

## 5. Where this is recorded, and what it changes

- `Planning/node_0_3_research/SUPPORT_BRAINSTORM_autopoly.md` gains a
  section on the proof system as levels 0–4 (this log's §1).
- The lean node's CORE keeps its definition ("a second discharger of
  the gate") and gains a "proposed widening" section naming the owner's
  words — "the operator-mapping proof system" — as the pending
  ruling; the definition changes only when he rules.
- The proposed order for the lean node stands as log_228 §6 wrote
  it, with one insertion at the front: the translator of §4.1, so the
  float model's operations are the reference's operations.

## 6. Awaiting the owner

- Whether the lean node's definition becomes "the operator-mapping
  proof system" with z3 as the check on the unverified compiler.
- Whether the synthesis route (§4.3) is opened as a task beside the
  source route.
- The order for the lean node with the translator inserted first.
