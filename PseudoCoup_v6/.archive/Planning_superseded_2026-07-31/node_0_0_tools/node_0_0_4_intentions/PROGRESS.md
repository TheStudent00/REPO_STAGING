---
id: pcv6.tools.t5_intentions.progress
status: living
---

# PROGRESS — T5 intentions

- plan — **settled** 2026-07-28; reframed same day by the owner:
  intentions data is largely BY HAND; the artifact filled by
  human+LLM analysis is the SLICING REQUEST FORM.
- **build — done** 2026-07-28 (delegated to a Sonnet subagent;
  all suites re-run and confirmed here):
  `PRIVATE/PseudoCoup_v6/Tools/intentions/` —
  `pc_intentions.json` (PCv5 verdicts copied forward + the four
  R1 gap fields: 10 satisfier rows, 19 canon entries each citing
  its verdict string, 11-member minimum set, policy links
  cross-checked both directions), `build_intentions.py`
  (refuses incomplete data, byte-identical rebuilds),
  `forms/` (FORM_SCHEMA.md + the four slicing request forms
  expressing the proven PCv5 chain, entry symbols verified by
  tree-sitter at their cited lines), `validate_form.py`
  (broken forms refused with the failure named).
- acceptance: intentions 27/27; neighbors unbroken (87 + 17).
  Verified independently after the delegate's run.
- **notable correction found by the build**: PCv5 comments cite
  the guard as `CheckedDivOrRemSeq (emit.rs:215)`; the vendored
  0.134.2 source actually contains `Inst::CheckedSRemSeq` in
  `fn emit` at line 162. The form declares what the source
  contains; discrepancy recorded in the form and schema.
- deviations flagged for the owner in the delegate's report (recorded
  in `PRIVATE/PseudoCoup_v6/Tools/intentions/README.md`):
  meta.generated_by renamed truthfully; four canon entries carry
  marked inferences (P9/O3 → Rust, P11 JS→TypeScript column, O7
  C# scope note); forms live as separate JSON files rather than
  embedded — one file per seam, fillable/validatable alone.
- open: T6 consumes the forms (selection); future interface
  (searchable menu / UR-AST) unscheduled.
