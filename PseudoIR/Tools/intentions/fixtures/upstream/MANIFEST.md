# Vendored artifact — the R1-verified verdicts

One file, 32 KB.

| file | came from |
|---|---|
| `pc_verdicts.json` | `PseudoCoup_v5/Designing/pc_verdicts.json` (historical) |

sha256 at vendoring, 2026-07-31: `1c5f434bc57663f0...`

## What it is

The intentions verdict data as R1 verified it. R1's report
(`PseudoCoup_v6/Research/r1_intentions_validation/REPORT.md`)
found no context-corruption artifacts, byte-identical regeneration,
and 108/108 basis cells agreeing with probe ground truth.

This suite checks that the copy-forward into `pc_intentions.json`
preserved every field. That check needs the pre-copy artifact to
compare against, which is this file.

## Why it is here, and the mistake that put it here

It used to be read out of PCv5 through a `PCV5_ROOT` environment
variable with a fallback guessing at a co-tree path. On 2026-07-31
PCv5 was gutted, `Designing/` was deleted, and **10 tests in this
suite broke immediately** — the deletion had been checked against
PseudoCoup_v6's references and not against PseudoIR's.

That is the dependency-on-a-past-project failure recorded in
`PseudoCoup_v6/AgentMemory/02_decisions.md`, caught by
its own test rather than by review. The fix is the same one applied to
the vendored compiler sources: copy the artifact in, so this repo
passes on its own.

By the recorded test — *after the harvest, could the source repo be
deleted without anything breaking?* — this is now a transplant. PCv5's
`Designing/` is gone and this suite passes.

## Note on the rest of PCv5's Designing folder

Everything else this tool cites from `Designing/` —
`build_verdicts.py`, `intention_tables_gen.py`,
`intention_row_satisfiers.md`, `BEJ_expansion.md`,
`minimum_intention_set.md`, `PCv7_policy_decisions.md` — is cited as
PROVENANCE in comments and READMEs, not read at runtime. Those
citations are historical and their target is recoverable from PCv5's
git history. Nothing else needs vendoring.

## Rules

- Do not edit. It is a frozen comparison baseline; editing it would
  make the copy-forward check pass by construction.
