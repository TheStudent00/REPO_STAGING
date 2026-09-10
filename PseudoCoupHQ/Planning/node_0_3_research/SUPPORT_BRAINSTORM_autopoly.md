---
id: hq.research.support.BRAINSTORM_autopoly
status: draft
---

# SUPPORT_BRAINSTORM — autopoly

Stage: brainstorm (the `SUPPORT_BRAINSTORM_` convention: a proposed
shape, not a ruled one). Opened 2026-09-06 from the owner's commentary on
task o7's result; the record of the day, with the owner's words verbatim
and the coordinator's commentary, is
`PRIVATE/PseudoCoupHQ/DevComms/log_219_autopoly_brainstorm.md`.
Nothing here is ruled; what is ruled is in the CORE.

## 1. The idea, in one sentence

**AutoPoly** is the automated polyfiller: for one dominant operator
(a pool entry) and one target language y, the proved source-level
function in y that computes it — produced by rendering the entry's
term to y source, compiling it with y's own compiler at ship flags,
carving it, and gating it against the entry's unit. Task o7 (log_218)
is AutoPoly with y = c: 168 of 204 proved, 193 of 204 under the
caller-extension reading.

## 2. The route it proposes

```
AutoPoly -> Hub, et al.
    (instead of PCv5 -> PseudoIR -> PCv6)

AutoPoly
    per (pool entry, target language y):
        term -> y source -> y's compiler -> carve
             -> gate against the entry's unit
        output: proved y function, kept with its proof

Hub, et al.
    ingress:  x source -> tree-sitter tree
              -> types at each operator node
                 (o6: the language's own front end,
                  cheap on go)
              -> dominant operator per node
                 (the pool, via the probe corpus's
                  routing)
    egress:   y source composed from AutoPoly's
              proved functions, one per node;
              y's compiler lowers and optimizes
              ACROSS them
    check:    the gate over the composed function
              against x's compiler's own output
```

## 3. What it would change in the master plan

- hub_compiler's lowering: from one canonical BODY per node joined
  through memory rows (machine-code stitching) to one proved SOURCE
  function per node composed as y source. the owner's to rule.
- Master-plan step 5 (one go file lowered and gated) would be run in
  the source-composition form.
- The pool's deliverable gains a second table beside the
  dominant-operator table: per (entry, y), the proved emulation.

## 4. What it does not change

- The typing of ingress: the key needs types at every node; a
  tree-sitter tree has none (o4: search resolves 6–22%; o6: go's own
  front end resolves 77%).
- The aggregate forms: text, sequence, keyed, nesting have no
  arch-units yet.
- The languages without a corpus.
- The judge: the gate, against the one reference simulator. Nothing
  learned is evidence.

## 5. The two observations the owner named, and the coordinator's reading

- **Collapse to the direct c equivalent.** The optimizer's algebra,
  not ours: rendered literally, a 128-bit division nest became the
  32-bit `div`. Lever: render several equivalent forms per term, keep
  the smallest proved body — superoptimization with the gate as the
  proof.
- **Equivalence not detected when it is by design.** The disproofs are
  guards the term lacks (zero divisor, signed extreme). The pipeline
  already names these (guard-outcome rows, DIFFERS-BY-DESIGN,
  exception families, the directional bridge). AutoPoly must render
  the MODE — emit the guard — or pose the proof on the named
  projection. Not a z3 limit.

## 6. Where z3 does limit us, and what ML could be, held to the doctrine

- Limits: UNDECIDED on wide division and multiplication at the 3,000
  ms ceiling; the cost of 43,410 candidate pairs (t100).
- ML as PROPOSER, never judge: rank which pairs to prove first (18,307
  labelled verdicts exist); order the search over source forms; propose
  lemmas. Every acceptance is a proof. First experiment: the ranker
  over t100's verdicts, scored by proved edges in the first N.

## 7. Proposed tasks (none opened without the owner) — see log_219 §4

1. Render the mode; re-run the 36 disproved.
2. Rust renderer, then go, then swift.
3. Size and cycles of proved emulations against native units.
4. The Hub as source composition on one typed go file.
5. The ranker experiment.
6. The five unattributed disproofs, one lane.

## 8. Awaiting the owner

- Unfreeze cross_construction on the emulation route, or found
  AutoPoly as its own sub-node of arch_unit_oracle.
- Whether hub_compiler's definition moves to source composition.
- The order among §7.

## 9. The proof system beneath AutoPoly, as levels (added 2026-09-07)

Record: `PRIVATE/PseudoCoupHQ/DevComms/log_228_lean_float_model_and_the_proof_system.md`
(a branch conversation) and `log_229_operator_mapping_proof_system_purpose.md`
(the purpose that log_228 left out, and its corrections).

| level | object | state |
|---|---|---|
| 0 | the complete mapping model of every arch opcode: the hardware's own reading, flags and the partial region included | the reference simulator and opcode table; not yet a Lean definition — to be DERIVED from the reference by a translator, not written twice |
| 1 | an arch-unit as a term over level 0 | the ledger and the term walk |
| 2 | dominant operators: equivalence classes of terms | the pool |
| 3 | emulation: x's mapping rebuilt from y's operations, by rendering to y source and lowering (measured 76–95% proved, 91–93% landing on the primitive) or by composing y's arch-units directly (synthesis, not yet run) | o7, o8, o11; preservation theorem proved for the integer subset (L1) |
| 4 | AutoPoly and the Hub as source composition | this file |

- Level 0 is what makes 3 and 4 complete rather than heuristic: the
  emulation is derived from the opcode's whole mapping, guards
  included.
- Floating point: the model is days; the compositional lemma library
  is weeks; bit-blasting is the fallback whose cost measures the gap.
- The frontier of the mapping model is memory and loops, not
  arithmetic or floats.
- Two producers of an emulation (compiler route, synthesis route);
  agreement is the oracle.
