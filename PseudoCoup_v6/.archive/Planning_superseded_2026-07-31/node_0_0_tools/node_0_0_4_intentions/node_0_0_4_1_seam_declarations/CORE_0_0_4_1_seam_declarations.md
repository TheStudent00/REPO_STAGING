---
id: pcv6.tools.t5_intentions.seam_declarations
level: 3
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_0_4_1 — Slicing Request Forms (seam declarations)

**Renamed by the owner's framing (2026-07-28)**: the artifact is a
SLICING REQUEST FORM — a formalized, validatable document filled
by human+LLM analysis against the hand-made intentions data.
Evaluating intentions is human-level work and stays by hand; the
form is what makes the process easy and the downstream mechanical.
A form's core content is the seam declaration below. Future
outlook (unscheduled): a searchable/selectable menu interface, or
interfacing with the UR-AST, could fill forms interactively.

**Why this node exists.** The survey of PCv5's working chain
(`PseudoCoup_v6/Research/r5_slice_mechanism_survey/REPORT.md`)
assessed, stage by stage, whether the SELECTION of what to slice
was mechanically derivable. The finding: choosing the entry seam
— e.g. that `codegen_int_binop` in rustc's `num.rs` is where MIR
meets the backend's intermediate form — was a **judgment call
requiring knowledge of the compiler's internals**, not derivable
from source. But once a seam is named, deciding which branches to
keep for a given operator/type set IS mechanically derivable.

So the automation boundary is exactly here: **a human declares
seams once per language; the machine does everything downstream.**
A seam declaration is data, so it belongs in the intentions
artifact — which makes this a T5 node, not a T6 one.

## What a seam declaration carries (working shape)

| element | meaning | example from the proven chain |
|---|---|---|
| language | which of the 12 | rust |
| intention | which intent this seam serves | integer arithmetic (div/rem/mul/add/sub) |
| stage | where in the compiler's own pipeline | MIR → IR |
| source file | vendored path, commit-pinned | rustc `.../src/num.rs` |
| entry symbol | the function the slice starts at | `codegen_int_binop` |
| scope filter | which branches are in scope | i64/u64; excludes i128, checked-overflow, compares |
| stand-ins | what the hub substitutes for compiler context | Ledger for TyCtxt; accumulator for InstBuilder |
| rule | policy governing the cut | cut from generated code, never the DSL |

The proven chain needs four such declarations (MIR routing, a
lowering stage, encoding, and the guard); they were the worked
examples the format was validated against. Those four declarations
were built against a retired reference backend and were removed as
mis-aimed (2026-07-30, see the tools PROGRESS); the format itself —
the schema below — is independent of which compiler backs it, and a
future set of declarations against LLVM/rustc-LLVM is the forward
path.

## Work items

1. Define the declaration schema; add it to the intentions
   artifact alongside the schema-extension node's four fields.
2. Write declarations that describe an ALREADY-PROVEN chain — the
   format is validated by expressing work that exists, never by
   inventing new cuts.
3. Validation: every declaration's source file exists at its
   pinned path, and its entry symbol is findable by T1's parser in
   that file (a mechanical check, not a claim).

## Acceptance (delegation-ready)

- The four declarations validate: paths resolve, entry symbols
  found by tree-sitter, scope filters parse.
- A deliberately broken declaration (missing symbol, wrong path)
  is REFUSED with the specific failure named.
- Round-trip determinism with the rest of the artifact.

## Open (the owner)

- **The automation boundary itself**: seams declared by hand, all
  downstream mechanical. This is the honest reading of the survey
  and it caps what "automation of slicing" can mean. the owner's ruling
  needed — it shapes the ultimate goal's wording.
- Whether stand-ins are declared per seam (as above) or belong to
  the hub's own vocabulary and are referenced by name.
