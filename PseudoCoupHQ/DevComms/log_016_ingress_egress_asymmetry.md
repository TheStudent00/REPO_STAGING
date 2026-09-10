# log 016 — the ingress/egress asymmetry, now measured: shapes are universal, intentions are shape-invisible

2026-08-12, at the owner's request ("yeah its brilliant -- please make a
log"), preserving the conversation that followed the basis report
(`log_015_basis_report.md`). the owner judged it big enough to justify
insertion into the development plan; that insertion is DISCUSSED here
and ruled separately.

## 1. the owner's three questions, and his own answer

Verbatim framing (2026-08-12):

> 1. how much of this language dendrogram structure is
>    keep-able/use-able for ingress into the `ur` and `ledger`
> 2. how much of it is use-able for egress from the hub?
> 3. and in the context of (1) and (2), how do their answers change
>    when viewed from the discipline established early on in PC
>    versions?
>
> (1) could be potentially very flexible. where the ur and ledger
> are very generous to induct into the hub -- which is meant to be
> very accepting. however, regarding (2) egress from the hub, it
> feels right that core egress capabilities be constrained to the
> discipline. just because otherwise, its essentially disclaimed
> that the target polyfill optimization is on the user. which feels
> pretty reasonable -- along with practical.

## 2. The finding: the instinct is a theorem of the data

The basis report's central split (log_015 §1, V1 vs V2):

- **shapes are universal** — every minimum-set object except
  `service call` has stable many-language clusters; 77.4% of all
  31,212 kinds sit in ≥10-language clusters at t=0.40; the isolated
  end is empty (log_014 §1).
- **intentions are shape-invisible** — A/B/C/E/G/H/I have no
  clusters of their own anywhere in 411 grammars: an
  `await_expression` is shaped like a unary expression, an
  interface like a class, `with` like `try` (log_015 §3).

Reading the owner's two questions against that split:

- **ingress consumes shapes** — the thing the ecosystem shares
  generously. A generous ingress is therefore cheap AND safe:
  almost everything arriving has a recognizable shape to record,
  and what does not is honestly marked (refuse-by-name, or
  unresolved `ur_kind` — the already-ruled posture).
- **egress produces intentions realized in a target** — the thing
  shape does not carry. Emitting suspension into a language without
  it is a semantics-preservation problem, not a mapping problem.

So the asymmetry is not a design preference. **The hub accepts by
shape and promises by intention**; generosity on one side and
discipline on the other are the two faces of the measured split.

## 3. Question 1 — what ingress keeps, concretely

In descending settledness:

- **map seeding.** `top_counterparts_all.json` + cluster membership
  mechanically propose ts_kind → ur_kind rows for any language,
  each row carrying its evidence ("kotlin `when_entry` sits with 63
  languages' match-arms"); the human rules the residue. This is the
  overhead reduction that opened the research branch (PCv5 q1's
  163 hand rows → a proposed table plus a short residue).
- **the form tier is the generosity mechanism.** The two
  shape-poverty giants (369/398 languages, log_014 §4 rows 2 and 9)
  land in the form tier honestly labeled — most kinds in most
  grammars are structurally humble, and the vocabulary is rightly
  silent about them (log_015 M10).
- **where the artifacts live: NOT in the ledger.** The ledger
  stores facts about FILES; the basis is knowledge about LANGUAGES
  — pack-side and shared-basis data, versioned like the grammar
  pins, re-derivable by the scripts in
  `PRIVATE/PseudoCoupHQ/Research/kind_signature_clustering/` (which is
  what keeps it maintainable under grammar churn).

## 4. Question 2 — egress: a router, never an authority

- the similarity data answers WHICH target construct realizes an
  intention, and — equally valuable — WHEN THE TARGET HAS NONE: an
  intention whose cluster family has no member in the target
  language is a polyfill site detected by lookup instead of by
  failure.
- what it cannot do is make the emission CORRECT. Correctness lives
  in the target's own grammar tables (stencils, variants) and the
  judges (faithful convergence, compile-as-oracle). The dendrogram
  picks the door; the pack and the oracles walk through it.

## 5. Question 3 — the discipline is WHY the answers differ

The early-PC discipline (constrain the accepted subset so the
exceptionally difficult issues never arise) does not change the
answers to (1) and (2); it explains their asymmetry:

- the hub GUARANTEES egress only for the disciplined core — the 11
  objects plus settled forms, the subset the oracles can vouch for.
- everything outside it is the polyfill frontier, explicitly
  disclaimed to the user — the owner's framing, kept as ruled sentiment.
- one sharpening accepted in discussion: with M1–M10 enumerated
  (log_015 §4), the disclaimer can be SPECIFIC rather than blanket
  — the egress boundary can say "this target lacks an error-clause
  construct; here are its nearest shapes" — the practical
  difference between disclaiming and abandoning.

## 6. Plan-insertion candidates (the owner: justified; placement his)

Held as proposals pending the talk-through:

- P-a. the pack generator: per-language ts_kind → ur_kind proposal
  machinery (map seeding, §3) as a `ts_to_ur`/pack build step —
  directly unblocks PCv5 q1 (rust ratification arrives as evidence
  + residue instead of 163 raw judgments).
- P-b. the shared basis as a versioned data artifact consumed by
  language packs (spectrum + counterparts + archetypes, with the
  re-derivation scripts pinned alongside).
- P-c. the egress router + specific-polyfill disclaimer at the hub
  boundary (far side of the funnel; lands with `builder`/egress
  planning, not ledgerer's current scope).
- P-d. log_015 §7's nine vocabulary proposals (P1–P9) walked with
  the owner — the ur.kinds rulings the basis report makes decidable.

## 7. Sources

- `PRIVATE/PseudoCoupHQ/DevComms/log_014_ecosystem_spectrum.md`
  (the structure), `log_015_basis_report.md` (the cross-reference),
  logs 008–013 (the build-up).
- PCv5 discipline history:
  `PRIVATE/PseudoCoup_v5/DevComms/log_013_discipline_history.md`
  (unverified this session — cited from memory of the campaign
  record; the discipline principle itself is quoted from the owner's
  recollection recorded in
  `PRIVATE/PseudoCoupHQ/DevComms/log_006_ur_research_record.md`).
