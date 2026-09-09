# T5 — Intentions

Turns the project's hand-made intentions data into slicer-steering
data. Two settled sub-nodes of the T5 super node govern this tool:

- `~/Programming/PseudoIR/Planning/node_0_1_research/node_0_1_0_intentions/SUPPORT_intentions_data_shape.md`
  — the four structured fields R1 found missing (row_satisfiers,
  canon, minimum_set, policy_refs; working names, the owner's to settle).
- `~/Programming/PseudoIR/Planning/node_0_1_research/node_0_1_0_intentions/SUPPORT_retired_seam_declarations.md`
  — slicing request forms, whose core is the seam declaration. The
  automation boundary: a human declares seams once per language;
  everything downstream is mechanical. (This once cited an "r5 slice
  mechanism survey" report; no such report exists — `Research/` holds
  r1 through r4 only. Citation removed 2026-07-31 rather than left
  pointing at nothing.)

Per the schema-extension node's recommendation, the verdict data is
COPIED FORWARD from the archived PCv5 tree and maintained here from
now on; nothing writes back into `~/Programming/PseudoCoup_v5`.

## Files

| file | role |
|---|---|
| `intentions_data.py` | vendored data: PCv5's `intention_tables_gen.py` tables and `build_verdicts.py` basis/lattice (provenance header inside), plus the four extension data blocks lifted from the PCv5 Designing documents |
| `build_intentions.py` | builds `pc_intentions.json`; REFUSES to emit on a missing satisfier row, missing/drifted canon, a minimum set that is not 11, or a dangling/unlinked policy reference. Deterministic: sorted keys, no timestamps, byte-identical rebuilds |
| `pc_intentions.json` | the built artifact: every pre-existing `pc_verdicts.json` field byte-stable, plus `row_satisfiers`, `canon`, `minimum_set`, `policy_refs` |
| `validate_form.py` | validates a form: path resolves under the declared root, entry symbol found by the T1 tree-sitter tool, scope filter parses, cited constructs present verbatim; a broken form is REFUSED with the failure named |
| `test_intentions.py` | the acceptance suite implementing the schema-extension sub-node's acceptance section |

A prior `forms/` directory held four proven-chain slicing-request forms
(routing, lowering, encoding, a divide-guard) built against a retired
reference backend instead of the settled LLVM/rustc-LLVM direction; they
were removed as mis-aimed (2026-07-30) along with the tests that
exercised them. `validate_form.py` is generic (rust/python/cpp) and
stays for the next, LLVM-facing, form.

## Provenance

- Verdict data: `~/Programming/PseudoCoup_v5/Designing/intention_tables_gen.py`
  and `~/Programming/PseudoCoup_v5/Designing/build_verdicts.py`,
  copied forward 2026-07-28; the R1-verified reference artifact is
  `~/Programming/PseudoCoup_v5/Designing/pc_verdicts.json`.
- row_satisfiers: `~/Programming/PseudoCoup_v5/Designing/intention_row_satisfiers.md`
  and `~/Programming/PseudoCoup_v5/Designing/BEJ_expansion.md`.
- canon: the `pc_verdict` strings themselves; every entry cites the
  exact string it came from and the builder refuses on drift.
- minimum_set: `~/Programming/PseudoCoup_v5/Designing/minimum_intention_set.md`
  (the 11 objects, post-audit).
- policy_refs: the "policy N" mentions in verdict strings, linked to
  `~/Programming/PseudoCoup_v5/Designing/PCv7_policy_decisions.md`.
## Run

Rebuild the artifact (refuses on incomplete data):

```
python3 ~/Programming/PseudoIR/Tools/intentions/build_intentions.py
```

Validate a form:

```
python3 ~/Programming/PseudoIR/Tools/intentions/validate_form.py \
    FORM.json --root ~/Programming/PseudoCoup_v5
```

Acceptance:

```
python3 -m pytest ~/Programming/PseudoIR/Tools/intentions/ -q
```

No environment variable and no other repo needed. The R1-verified
artifact the suite compares against is vendored at
`fixtures/upstream/pc_verdicts.json`.

*(Until 2026-07-31 it was found via `PCV5_ROOT`, else guessed at as a
co-tree beside PseudoCoup_v6. That broke the day PCv5 was gutted; see
that folder's MANIFEST.)*

## Deviations flagged for the owner

- `meta` is a pre-existing field but cannot stay byte-identical in a
  copy-forward: `generated_by` now truthfully names
  `build_intentions.py`. The nine data fields ARE byte-stable
  (compared field by field against the R1 artifact); the original
  `sources` list is asserted preserved inside the new meta.
- The forms live as JSON files in `forms/` rather than inside
  `pc_intentions.json`; the seam-declaration sub-node places them
  "alongside" the four fields, and the folder keeps them one file
  per seam so a form can be filled and validated on its own.
