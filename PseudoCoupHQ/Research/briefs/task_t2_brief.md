# Task t2 — the second tier: construct what a target lacks from the primitives it has, smallest width first, proved canonical-form first

Law: `PseudoCoupHQ/Research/LAW.md`, ALL of it (waits in short
calls). Then `task_ap6_brief.md` beside this file and its log (ap6 runs
BEFORE this task: the driver is one, versioned, gate-free), `log_234`
(the mappings as fits: the two bases and the mixed case), `log_221` §7
(construction linear; proof by structure), `log_251` (the trust classes),
the bank (`certificates.jsonl`, the `refused` certificates and their
causes: "float of 80 bits", "answer 128 bits", "no spelling for kind",
"no 80-bit holder"), the renderers, `Research/op_pipeline/term.py`
(`Term.normalize`, `identical_text`'s basis), `Research/op_pipeline/lean/`
(L1's preservation theorem; `run_edges_L1.py`). Instance `t2.conf` (copy
from `Airlock/instances/t2.conf`). Artifact folder:
`.../emulation/`, new sub-folder `construct/`; lanes under `construct/lanes_t2/`.

## 1. The ruling this task carries out (the owner, 2026-09-10)
A language that offers `& | ^ ~`, a conditional and a variable has every
logic gate a microprocessor is built from, so every opcode's mapping is
constructible from them: a guaranteed solution, not necessarily the
fastest. "I'm fine with the algorithm being whoever gets there first."
Today's renderer REFUSES where the target lacks a primitive at a width or
kind; this task adds the tier that constructs it instead. Two more of
the owner's points are in the design: build the smallest width first and use it
to build the larger; and the proof is the study of the mappings — same
canonical form ⇒ same function — with the solver as the audit, not the
workhorse.

## 2. The construction schemas
One schema per operation, parameterised by width, instantiated over the
target's WIDEST available integer holder as the word (64 on every target;
32 where a target has no 64):
| schema | built from | the smaller-width step |
|---|---|---|
| add / sub with carry and flags | word add/sub, `^ & |`, a conditional for the carry | w from two w/2 (ripple) |
| shifts, rotates | word shifts, masks, a conditional on the count | w from two w/2 |
| multiply (low and high halves) | word multiply where the target has it; else shift-and-add over `& ^` | w from four w/2 products |
| unsigned / signed divide and remainder | restoring division: shifts, compare, conditional subtract; a bounded loop of w steps | w from w/2 by the same loop |
| comparisons and the flag word | `^ & |`, a conditional | — |
| widening / narrowing / sign spread | masks and a conditional | — |
| float add / sub / mul / div / compare / convert, 32 and 64 (and 80 where a target has no `long double`) | integer schemas above over the fields sign, exponent, significand with the sticky bit; the five classes as a case split (log_228 §3) | the proof-system's float model, reached from this side |
Each schema is one function in `construct/schemas.py` producing a z3 term
(the CONSTRUCTED mapping) AND target source (its rendering, through the
existing renderers, which now never see an operator they lack).

## 3. Whoever gets there first
Per (cell, target) with no `proved` certificate: try the native route
(ap6's driver) and the constructed route; bank whichever proves; if both,
the smaller carved body. Record on every constructed certificate:
`route = constructed`, the schema, the word width, and the compiler's
collapse (LANDED / NOT_COLLAPSED with the instruction count) — the owner's
"the c compiler could simplify into a smaller set of arch opcodes",
measured per cell.

## 4. The proof, in this order, recorded on the certificate
1. **canonical form**: the constructed mapping and the cell's mapping
   normalised by `Term.normalize`; identical text ⇒ proved, no solver
   (`proof = canonical`). Report how many fall here.
2. **the schema's lemma**: for the schemas where a term of width w is the
   composition of two of width w/2, the induction lemma in Lean (one per
   schema, `construct/lean/`), instantiated per width; the carved body is
   checked against the schema's OUTPUT term at the pipeline's ceiling
   (`proof = lemma+gate`). Write the adder's and the shifter's lemmas at
   least; list the others as owed with their statement.
3. **z3** at the pipeline's ceiling as the last resort (`proof = sat`),
   never above 30 s, never a wide multiply or divide by bit-blasting
   alone — those go to 2 or are reported.

## 5. Deliverable
`construct/schemas.py`, `construct/construct.py` (the tier, called by the
driver where the native route refuses by width or kind — the ONE change
to the driver, unconditional), the Lean lemmas, `construct.md`: per
target, refused-by-nature certificates before → constructed and proved
after, by schema; the three proof forms' counts; the collapse column; the
three readings of the polyfill-complete set beside ap6's; every `sat`
with its point. Guard over every json; log (next free number); verifier
lane; PROGRESS on the autopoly node and the lean node; sync-back;
instance down. Memory bound 6g, sample 20, peak RSS, abort
`ABORT_MEMORY_T2`; z3 ceiling 30 s hard. Shared-file changes: the
driver's one call site and `construct/` only. Never delete anything under
`<runs>/` or `Airlock/`. Reply with the before →
after by schema and target, the proof-form counts, the collapse counts,
the three readings, the tally, the two lists.
