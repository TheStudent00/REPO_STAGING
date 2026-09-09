# 00 — The Project

## Thesis

PseudoCoup: write applications once in disciplined Python (the
**hub**), render to any of 12 target languages losslessly. The hub
**dominates intentions** — its canon of intention objects is chosen
so that any of the 12 languages maps in with no semantic distance to
cross; that dominance is what makes ingress trivial. Where a target
language cannot express an intention natively, the shortfall is
recorded as the destination's shortfall, never as a constraint on
the hub.

The mechanism that makes the hub able to compute any target's exact
semantics: **extract the routing logic from the target's own
compiler and execute it inside Python** (proven in PCv5 — a real
compiler's division routing, lowering, and encoding transpiled to
Python, producing machine bytes byte-identical to native rustc,
executed in-process in stock CPython).

## Goals

- **Ultimate:** greatest amount of automation of transpiling and
  slicing of languages — in particular the 12. Purpose stated by
  the owner (2026-07-28, level-0 note in
  `~/Programming/PseudoCoup_v6/Planning/CORE_0.md`): CHURN
  RESILIENCE — the Hub satisfies the source scripts' intentions;
  when the intention-landscape changes, a mostly-automated
  transpile+slice+insert system updates the repo quickly, keeping
  it maintainable by a handful of developers, potentially one.
- **Intermediate:** Rust (LLVM) transpiling and slicing.

## Core components (the owner's Level 1, 2026-07-27)

- **transpiler** — PCvX: the most advanced version-state of the one
  PseudoCoup transpiler lineage. "Most advanced" = most
  sophisticated at ACCURATELY transpiling, not advanced w.r.t. any
  particular source/target pair. Survey found it DISTRIBUTED across
  versions (see 03).
- **intentions** — JSON of language assessments; intention dominance
  as data. Exists (`pc_verdicts.json`), requires validating.
- **lessons** — useful info from the PCv5 (erroneous-in-places)
  project state; requires validating.
- **polyfill** — wrappers from transpilation that fill behavior to
  match the source. Governing law: uniform wrapping, no exemptions;
  every operator on a polyfilled type routes through the simulator
  or none do.
- **slicer** — the system that uses the intentions JSON to extract
  the slice of a source compiler and insert it into the hub
  interpreter. DOES NOT EXIST as a system yet; both halves
  (extraction, insertion) are individually proven. This is the
  novel component; automation lives here.

Resolved 2026-07-28: the **ledger is an independent tool**
(PseudoCoup is a module of tools; centralized control later,
"hopefully ontology will reveal itself"). "Oracles" is not a
component but a standing rule (every tool ships with its
acceptance test; oracle assets live beside the tool — the owner
confirmed). Design principle: **generalize then specialize** —
tree-sitter handling, ledger, and most transpiler machinery
overlap massively across languages. Lowering-to-IR and
lowering-to-arch logic enters the hub by TRANSPILING THE COMPILER
AND SLICING — never by mining/reconstructing tables (see 02, IR
question closed).

## Foundation: tree-sitter

Arguably the most significant module in the project (the owner). It
produces the ASTs that make the 12 languages connectable at all;
the ledgers are populated by tree-sitter ingestors; node identity
(idgen) is defined over the tree-sitter tree; coverage gates
partition tree-sitter node kinds; 12 grammars exist vendored and
commit-pinned (PseudoIR v2 pattern). Settled 2026-07-28: PCv6
compiler-source ingress rides tree-sitter too; PCv5's bespoke
parsers were expedience and are archived as lessons. Any future
argument against tree-sitter bears an extraordinary burden of
proof.

## The 12 target languages

python, typescript, java, csharp, go, rust, ruby, php, kotlin,
cpp, dart, swift (the vendored-grammar set; also the pc_verdicts
column set).

## Repos

- `~/Programming/PseudoCoup_v6/` — THIS repo: the build.
- `~/Programming/PseudoCoup_v5/` — research stage: proofs, oracle
  assets, surveys, plans. Being archived except what carries
  forward (oracle assets stay live).
- Earlier versions + precursors: see 03.
