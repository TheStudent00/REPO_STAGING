# R1 Report — Intentions-Data Verification

Date: 2026-07-28. Checks 1–2 run by the owner on host via
`run_checks.sh` (output pasted into session, logs in `runs/` on
host). Checks 3–4 performed by direct file inspection (both sides
are text; every claim below was read, not characterized).

## Verdict summary

| Check | Result |
|---|---|
| 1. Byte-identical regeneration | **PASS** — both artifacts |
| 2. Internal consistency | **PASS** — all counts reconcile |
| 3. External agreement | **PASS** — 108/108 classifications agree; one label-wording variance (not a verdict change); class-7 suite absence explained by recorded demotion |
| 4. Dominance as data | **PARTIAL** — realizations/verdicts are data; the slicer-steering facts are prose-only (list below) |

Overall: **no context-corruption artifacts found.** The data is
internally sound and agrees with its ground-truth sources. What it
lacks for the slicer was never claimed to be there — it is missing
structure, not corrupted content.

## Check 1 — reproducibility: PASS

`build_verdicts.py` and `intention_tables_gen.py` regenerate
`pc_verdicts.json` and `intention_tables.html` byte-identical to
git HEAD (the no-timestamps rule makes this a real equality).

## Check 2 — internal consistency: PASS

Field sizes, all as expected: languages 12; intent_categories 10;
t1_realizations 10 (×12 languages each — verified by reading all
rows); t2_compatibility 45 = C(10,2) pairwise, plus t2_diagonal 10;
primitives 12 (×12 cells); operators 7 (×12 cells); basis_audit 9
members × 12 languages = the 108 cells; border_lattice 11.

## Check 3 — external agreement: PASS

- **basis_audit vs `Research/basis_audit/results.md`** (the 12/12
  probe-run matrix): compared cell by cell, all 9×12
  classifications agree, including every flagged hazard (Go
  slice-alias-detach, PHP value-copy + float-drift, Swift COW
  value-copy, executor withheld on exactly TypeScript/JS, Dart,
  PHP).
  - One wording variance, verdict unaffected: Rust hashing is
    "cheap: order" in results.md, "cheap:unordered" in the JSON.
    Both classify it cheap; the JSON label is the semantically
    correct one (Rust HashMap is unordered; C++ map is
    differently-ordered, and the JSON keeps "cheap:order" there).
    Not corruption — terse-vs-precise labeling.
- **border_lattice vs the divergence classes**: 11 entries cover
  classes 1–8 plus J3, with classes 2 and 7 carrying two crossings
  each — consistent with the recorded class membership.
- **Divergence suite files**: `class_{1,2,3,4,5,6,8}_*.py` exist;
  there is NO `class_7_*.py`. Explained by the recorded demotion
  of class 7 (concurrency) to a performance matter ("simultaneity
  is a resource, not a semantic" — project_state 2026-07-24);
  the lattice still carries class-7 BORDER rules (spawn-boundary
  crossings), which is coherent: demoted as a divergence class,
  retained as a border condition. Flagged for awareness, not a
  defect.

## Check 4 — dominance as data: PARTIAL

What IS data: per-category × per-language realizations (t1), the
45 pairwise merge verdicts + 10 internal-merge notes (t2), 12
primitives and 7 operator families each with a `pc_verdict`, the
basis matrix, the border lattice.

What exists ONLY in prose and must be lifted into data before the
slicer (T6) can be steered by this file:

1. **Row satisfiers** — which language satisfies which intent row
   (e.g. Rust satisfies A/C/D/G; B/E/J solved in-hub). Lives in
   `intention_row_satisfiers.md` + `BEJ_expansion.md`; absent from
   the JSON. This is THE dominance fact the slicer needs first —
   it selects which compiler to slice for which intention.
2. **Canonical-source language per verdict** — every `pc_verdict`
   embeds its canon in prose ("Rust canon", "Kotlin split",
   "Swift view model", "C# ^"). No structured `canon` field
   exists; a slicer would have to parse English.
3. **Minimum intention set membership** — the 11 objects
   (`minimum_intention_set.md`); not represented in the JSON.
4. **Policy references** — verdicts cite policies ("policy 6",
   "policy 7") by prose only; no machine link to
   `PCv7_policy_decisions.md` entries.

## Feeds

- **T5 (intentions tooling)**: keep the data and generators as-is
  (verified sound); the work is ADDITIVE — new structured fields
  (satisfiers, canon, set membership, policy links), builder
  validation extended to refuse if they're incomplete.
- **T6 (slicer)**: its steering schema should be designed against
  the four gaps above; item 1 is the entry point.
- Provenance note: all subject artifacts remain in
  `<WORKSPACE_DIR>/PseudoCoup_v5/Designing/`; nothing was modified.
