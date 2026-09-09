# R2 Report — Tree-sitter Census of the Compiler Sources

Date: 2026-07-28. Run in-session with T1
(`PseudoCoup_v6/Tools/ledgerer/tree_sitter/`, pinned
grammars). Script: `census_sources.py` in this folder; per-file
censuses in `outputs/`.

## Headline

**Tree-sitter parses every subject file clean — zero ERROR nodes —
and the census is deterministic (byte-identical rerun, all 5
files).** The tree-sitter foundation decision is validated against
the real ingress targets; the Rust ingestor's worklist is now
measured, not estimated.

## Census

| subject | grammar | size | named kinds | total nodes | ERROR nodes |
|---|---|---|---|---|---|
| assembler_generated (a retired reference backend's generated crate) | rust | 99,935 lines | 71 | 1,277,321 | no |
| support_rex (`rex.rs`) | rust | 236 lines | 63 | 1,830 | no |
| support_custom (`custom.rs`) | rust | 731 lines | 65 | 8,551 | no |
| rvalue (`rvalue.rs`, rustc front half) | rust | 1,180 lines | 86 | 11,466 | no |
| x86_mc_code_emitter (LLVM, hand-written C++) | cpp | 2,033 lines | 94 | 16,918 | no |

Subject paths are recorded in
`PseudoCoup_v6/Planning/node_0_1_research/PROGRESS.md`.
The full support crate has 15 `.rs` files (incl. `vex.rs`,
`evex.rs` — the stubbed SIMD surface); only the two
transpiled-in-PCv5 files were censused here, the rest join when
their stubs are revisited.

## Kind-set analysis (the T3 worklist)

- **Milestone-1 surface (an early generated-vocabulary reproduction
  target, since removed as mis-aimed — see the tools PROGRESS):
  91 named kinds** — the generated file's 71 plus exactly 20
  support-only additions
  (measured list in the run log; includes `assignment_expression`,
  `unary_expression`, `type_cast_expression`, `struct_pattern`,
  module/use scaffolding).
- **Front-half increment (`rvalue.rs`): +19 kinds** beyond
  generated+support (closures, for/range expressions, tuple and
  or-patterns, `let_chain`, `compound_assignment_expr`, lifetimes).
- **C++ (LLVM encoder): 94 kinds**, its own grammar — sized for
  the later C++ ingestor node table.
- Perspective on counts: PCv5's "12 node kinds" for the generated
  file counted the transpiler's SEMANTIC categories (let, method
  call, if-let, …); tree-sitter counts every CST kind (identifier,
  literal, block, …). 71 CST kinds collapse onto few semantic
  build rules — most are trivial leaves. Not a contradiction; a
  granularity difference.
- **Measured correction to the PCv5 record**: one PCv5 table row
  described the generated assembler.rs as "14,876 lines"; the file
  on disk is 99,935 lines (~9.3 MB — consistent with the "9.3 MB
  in" figure elsewhere in the same record). The line figure was
  wrong or referred to a different artifact; recorded here so it
  doesn't propagate.

## Feeds

- **T3 rust ingestor — UNBLOCKED at the time**: node table sized at
  91 kinds for milestone 1; censuses in `outputs/` are the frozen
  worklist; the coverage gate's baseline (trivial-leaf
  justifications) gets written against these exact lists. The
  ingestor increment this unblocked was later removed as mis-aimed
  (2026-07-30, see the tools PROGRESS); the rustc/LLVM-facing
  subjects measured here (rvalue.rs, the LLVM encoder) remain valid.
- **T4 polyfill**: the arithmetic surface is present and named
  (`binary_expression`, `unary_expression`,
  `compound_assignment_expr`, shifts/masks inside the generated
  formulas) — the wrapper requirements list starts from these.
- **T2 ledger**: the pinned corpus for the first `--check` can be
  these five files — real targets, already censused.

Housekeeping note: `.archive_outputs_run1/` (hidden) is a
byte-identical duplicate of `outputs/` produced by the determinism
check; the sandbox is denied deleting files — removable on host if
wanted.
