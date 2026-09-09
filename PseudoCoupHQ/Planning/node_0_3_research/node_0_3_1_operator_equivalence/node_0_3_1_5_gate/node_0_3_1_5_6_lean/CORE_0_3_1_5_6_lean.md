---
id: hq.research.compiler_graph.gate.lean
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: lean
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/CORE_0_3_1_5_6_lean.md
super_node:
    name: gate
    path: ../CORE_0_3_1_5_gate.md
sub_nodes:
    - name: model_translator
      path: node_0_3_1_5_6_0_model_translator/CORE_0_3_1_5_6_0_model_translator.md
    - name: certificates
      path: node_0_3_1_5_6_1_certificates/CORE_0_3_1_5_6_1_certificates.md
    - name: renderer_theorem
      path: node_0_3_1_5_6_2_renderer_theorem/CORE_0_3_1_5_6_2_renderer_theorem.md
    - name: float_model
      designation: code (module)
      realize: false
    - name: term_algebra
      designation: code (module)
      realize: false
---

# CORE 0_3_1_5_6 — lean

## metadata

- **id:** hq.research.compiler_graph.gate.lean
- **level:** 4
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [gate](../CORE_0_3_1_5_gate.md)

## sub_nodes

- [model_translator](node_0_3_1_5_6_0_model_translator/CORE_0_3_1_5_6_0_model_translator.md) — The translator from the reference simulator's opcode semantics (the opcode table `reference.py` and the term walk use, VEX semantics via pyvex) to Lean definitions, so that level 0 of the proof system — the mapping model of every arch opcode, flags and partial region included — is DERIVED from the one source the gate already uses and never written a second time.
- [certificates](node_0_3_1_5_6_1_certificates/CORE_0_3_1_5_6_1_certificates.md) — Term equivalences re-proved in Lean with a checked certificate: the pool's proved edges as theorems `∀ v0 v1, tA = tB` discharged by `bv_decide` (bit-blasting with the SAT certificate verified in Lean), translated from the layer-5 print form by `term_to_lean.py` with a z3 round-trip check.
- [renderer_theorem](node_0_3_1_5_6_2_renderer_theorem/CORE_0_3_1_5_6_2_renderer_theorem.md) — The preservation theorem: the term language as an inductive type with an evaluator, the target language's expressions as a second type with theirs, rendering as a function, and one theorem by structural induction that evaluating the rendered expression equals evaluating the term.
- float_model — code (module) *(realize: false)*
- term_algebra — code (module) *(realize: false)*

## definition

The operator-mapping proof system: the complete mapping model of every
arch opcode (level 0, DERIVED from the reference simulator by a
translator, never written twice), the term algebra over it, the
equivalence proofs between terms, and the translation to each target
language with its preservation theorem — held in Lean 4, whose kernel
checks every proof — with z3 kept in the gate as the per-instance check
on the unverified compiler's output. Ruled by the owner 2026-09-07 ("Lean is
a potentially fundamental part of the operator-mapping proof system";
"make the updates according to our alignment"), widening this node
from its founding definition of the same week, "a second discharger of
the gate's proof obligations beside z3", which it still is.

In the evidence doctrine this sits ABOVE z3's "the tool's own
testimony": the proof object is checked by a small trusted kernel, and
the bit-vector tactic `bv_decide` bit-blasts to a SAT solver and
verifies the solver's certificate inside Lean.

Lean 4 (elan, toolchain v4.24.0, core only, no Mathlib) was installed
INTO the Airlock image on 2026-09-07 (`Airlock/Containerfile`,
the Lean block).

## the levels this node holds (log_229 §1)

| level | object | state |
|---|---|---|
| 0 | the mapping model per opcode, flags and partial region included, derived from the reference | sub-node model_translator; not started |
| 1 | terms over the model | the term walk's terms, translated (`term_to_lean.py`, L1) |
| 2 | equivalence of terms with a checked certificate | sub-node certificates: 8 of 10 t100 edges proved in ~0.2 s (L1); floating point refused |
| 3 | translation to a target language, proved once by induction | sub-node renderer_theorem: the integer subset, 18 constructors, PROVED (L1) |
| — | floating point: the model (days), its compositional lemmas (weeks), bit-blasting as fallback | float_model, registered, not started |

## the three proof obligations and their cost (log_228 §4.1)

- definitional: a single-opcode unit IS the model's operation — `rfl`;
- by rewriting with the lemma library — cheap once the lemma exists;
  a rewrite chain found once is a lemma for every pair of that shape
  (the owner's "cache patterns → lemmas");
- by bit-blasting to SAT with a checked certificate — the fallback;
  its cost measures the lemma library's gap (16-bit division: 283 s,
  12 GB; 32 and 64 bits undecided at 600 s).

## the order, ruled 2026-09-07

1. model_translator: the opcode table's semantics → Lean definitions,
   checked by the single-opcode units definitionally (a discrepancy is
   a finding about one of the two readings).
2. comparisons and truth connectives into the term algebra and the
   renderer theorem (coverage from 25% toward ~60% of printed entries).
3. the rust expression type with the same induction.
4. guarded division (zero divisor and INT_MIN / −1); the term store's
   unguarded `bvudiv_i` print form retired after t104.
5. the float model, then its lemma library; bit-blasting recorded as
   the gap's measure.

## what stays outside Lean

The compiler's output: a rendered emulation is proved equal to its
term here; the machine code the compiler emits for it is re-proved by
the gate against the reference simulator, or by a verified compiler
(CompCert, for c). That is the price of trusting clang and rustc, and
it is not a Lean limitation.

## artifacts

`PseudoCoupHQ/Research/op_pipeline/lean/` (the `archproof`
lake project; `term_to_lean.py`; `lanes_L1/`). Logs 227, 228, 229.
