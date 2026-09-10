---
id: pcv6.tools.t6_slicer.extraction
level: 3
status: draft
settled_by: the owner
supersedes: null
---

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

`PRIVATE/PseudoCoup_v6/Tools/tree_sitter_base/`,
`.../Tools/ledger/`, `.../Tools/transpiler/` (three ingestors, each
byte-identical to its PCv5 oracle), `.../Tools/polyfill/`.

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
