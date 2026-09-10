---
id: pcv6.tools.t6_slicer.selection
level: 3
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_0_5_0 — Selection

The steering half: read the intentions artifact and decide WHAT to
slice. Bounded by the automation boundary established in
`../../node_0_0_4_intentions/node_0_0_4_1_seam_declarations/` —
seams are declared by hand; everything from a seam downward is
mechanical.

## What selection does, mechanically

Given (intention, language) it resolves:

1. the seam declaration for that pair (which file, which entry
   symbol, which stage);
2. the scope filter — the operator/type set in play;
3. the reachable region from the entry symbol under that filter:
   the call graph walked over T1's parse trees, stopping at
   declared stand-ins and at declared cut points;
4. an ordered slice plan — the regions to extract, in dependency
   order, each with its stand-in substitutions named.

Item 3 is where the survey's "(b) derivable given a table of
intentions" is cashed in: branch pruning by operator/type set is
mechanical once the set is stated.

## Harvest and reference

- The original "four proven slices" cited here as ground truth
  (a MIR-routing slice cut from rustc `num.rs::codegen_int_binop`,
  plus a lowering slice, an encoder slice, and a divide/remainder
  guard, all cut against a retired reference backend) were removed
  as mis-aimed (2026-07-30); they are no longer this node's ground
  truth. The forward direction is LLVM/rustc-LLVM — a future
  increment re-derives its own proven slices against that target.
- Mechanism detail:
  `PRIVATE/PseudoCoup_v6/Research/r5_slice_mechanism_survey/REPORT.md`.

## Acceptance (delegation-ready)

- Pointed at an integer-arithmetic intention, selection produces a
  plan whose regions correspond to a set of proven slices for the
  declared seam — same entry symbols, same scope exclusions (no
  i128, no checked-overflow, no compares), same stand-ins.
- A scope filter that excludes an operator removes exactly the
  regions serving it and nothing else.
- An undeclared (intention, language) pair is REFUSED with the
  missing declaration named — never silently guessed.
- Determinism: same artifact and filter produce a byte-identical
  plan.

## Settled (the owner, 2026-07-28)

- Plans are PERSISTED artifacts: committed, diffable, reviewable
  before extraction; drift in a compiler source is visible as a
  plan diff.
