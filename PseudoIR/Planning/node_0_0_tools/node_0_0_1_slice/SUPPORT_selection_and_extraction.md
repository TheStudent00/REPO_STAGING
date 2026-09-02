---
id: pir.slice.support.selection_and_extraction
status: projected
---

# SUPPORT — selection and extraction

projected 2026-07-30 from the previous plan, now archived at
`<WORKSPACE_DIR>/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_5_slicer/node_0_0_5_0_selection/CORE_0_0_5_0_selection.md  (343 words)
source: node_0_0_tools/node_0_0_5_slicer/node_0_0_5_1_extraction/CORE_0_0_5_1_extraction.md  (519 words)
verdict: substitute for selection, clean for extraction
changed: selection already disowns its old ground truth in its own
"Harvest and reference" section — the four proven slices cut against
a retired reference backend were removed as mis-aimed, with the
forward direction stated as LLVM/rustc-LLVM re-deriving its own
proven slices. Carried intact, backend unnamed as in the source.
Extraction was already rewritten to be backend-independent (its
acceptance section is explicitly "PCv5-free", stage expectations
written from the compiler sources themselves and the CPU manual, not
from any past artifact); carried with no further changes.

---

## from selection

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
- Mechanism detail: the R5 slice-mechanism survey report USED to
  carry it. R5 was removed with its subject in the 2026-07-30 purge —
  it surveyed the retired backend's chain — so there is no current
  document holding this. Recorded in
  `<WORKSPACE_DIR>/PseudoCoup_v6/Planning/PROGRESS.md` ("R5 removed
  with its subject"). Rebuilding the mechanism detail against LLVM is
  open work, not a lost file to go and find.

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

## from extraction

# CORE 0_0_5_1 — Extraction

Execute a slice plan: drive T3's ingestors over the planned
regions and emit hub-side Python that computes what the compiler
region computed.

## Mechanism

- Input: a plan from the selection node.
- **Follow-the-calls rule (the owner, 2026-07-28)**: if a planned
  region's code calls something resolvable in the vendored
  compiler source — any module, operator, or function, in ANY
  file — that callee is transpiled+sliced too, under a generous
  configurable depth limit. Hitting the limit emits a loud
  TRUNCATION WARNING naming the callee; a human then decides
  whether it becomes a wrapper (stand-in). Stand-ins declared in
  the form are pre-made instances of that same human decision
  (known infrastructure like TyCtxt, where following would drag
  in half the compiler). Worked precedent: PCv5 transpiled
  `type_sign` from outside num.rs — this rule, done by hand.
- For each region: parse with T1, ingest with the T3 ingestor for
  that grammar, follow resolvable callees per the rule above,
  apply the plan's stand-in substitutions at the declared
  boundaries, render.
- Wrap arithmetic through T4's polyfill layer under the uniform
  law; `check_uniformity` runs on the emitted module as a gate,
  not as advice.
- Populate T2's ledger for every emitted region so each slice line
  traces to its source node id (provenance is structural, not a
  comment).
- Emitted artifacts follow the stability-layer rules: deterministic,
  no timestamps, provenance header naming source file, entry
  symbol, and pinned commit.

## Reuse (already built and green)

`<WORKSPACE_DIR>/PseudoCoup_v6/Tools/ledgerer/tree_sitter/`,
`<WORKSPACE_DIR>/PseudoCoup_v6/Tools/ledgerer/`,
`<WORKSPACE_DIR>/PseudoCoup_v6/Tools/transpiler/`,
`<WORKSPACE_DIR>/PseudoCoup_v6/Tools/polyfill/`.

(Renamed 2026-07-31: `Tools/tree_sitter_base/` became a component of
the ledgerer, and `Tools/ledger/` became `Tools/ledgerer/`. The
transpiler's "three ingestors, each byte-identical to its PCv5
oracle" is no longer true as written — two of the three were removed
in the 2026-07-30 purge as mis-aimed, leaving the LLVM C++ encoder
ingestor.)

## Acceptance (SETTLED by the owner, 2026-07-28 — PCv5-free)

Governing rule: past-project oracles INFORM, never ANCHOR. The
pass/fail path contains no PCv5 artifact.

- **Stage expectations written from the sources themselves**: the
  emitted modules, executed, must produce — routing: the IR
  operation the compiler source's match arms dictate (div →
  `sdiv`); lowering: the instruction sequence its lowering rules
  dictate (`sdiv` → `cqto`, `idiv`); encoding: the numeric
  machine code per the CPU's own encoding rules for the in-scope
  instructions (expected number lists written down from the
  x86-64 manual, not from any past artifact).
- **Execution-based semantic grid** (lands fully with the
  insertion increment): the hub runs the produced machine code
  and arithmetic RESULTS match independently computed Rust
  semantics — `-7 / 2 == -3` (truncating), `MIN / -1` traps —
  over the full signed+unsigned grid including extremes.
- **Optional strongest anchor** (host, one command): diff our
  machine-code numbers against live `rustc` output for the same
  operations — the source compiler itself, an inherent dependency.
- `check_uniformity` passes on every emitted module; ledger
  `--check` green over the emitted set (every region traces to a
  source node id); two runs byte-identical.
- PCv5 slices: informative reference during development only.

## Future resource (the owner, 2026-07-28 — noted, not scheduled)

Compiler sources ship their own test suites. Extracting the test
relevant to a slice and TRANSPILING IT TOO would let us compare
the Rust original and the hub-transpiled version against the
compiler authors' own intent statements — a native-born test per
slice. Revisit when a slice's manual-derived expectations feel
thin.
