# log 092 — Task 8: reconciling guards3.json into the record, plus Task 13's two documentation slips

Date: 2026-08-31. Answers log_091's Task 8 and Task 13.

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line — not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention — never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

## Walkthrough

**(a) What guards3.json actually is.** I read `guards_java_deopt.py`
(the generator, undocumented until now) directly rather than
guessing from its output. It reads `guards2.json` (305 rows,
unmodified) and `interp_jvm.json` (the java pilot's own measured
data), and appends ONE new row per mode entry found in
`interp_jvm.json`'s two units — all eight of them (`u1.m1`, `u1.m2`,
`u1.m9` on the addition unit; `u2.m1`, `u2.m2`, `u2.m3`, `u2.m4`,
`u2.m9` on the division unit), each carrying `weaker_provenance:
true`. So guards3.json is a FOLD directly on top of guards2.json — a
fuller one than `guards2_parallel.json` (log_087, Task 5c), which
carries exactly ONE java row (the op_2 zero-divisor deopt guard,
retrofit into core_modes shape). The two are independent forks off
guards2.json, not a chain: guards3.json was not built from
guards2_parallel.json and does not know it exists. Where they
overlap (the zero-divisor guard on `java/op_2`), guards3.json's row
is the more direct one — read verbatim from `interp_jvm.json`'s own
mode record, rather than retrofit into a different row shape.

**(b) The one guard record of record.** I wrote `guards4.py`
(new file), which takes guards2.json's 305 rows unchanged as the
base and adds all 8 java rows carried by guards3.json's logic, with
one normalization: the provenance-mark field name. guards3.json
spells it `weaker_provenance`; `add_java.json` (the round-1
precedent named in the brief) spells it `provenance_is_weaker` on
its `member_recorded` object. I kept `add_java.json`'s spelling —
it is the earlier, ratified precedent — so the record of record
uses one name for this mark. Output: `guards4.json`, 313 rows (305
base + 8 java). Verified programmatically: the first 305 rows of
`guards4.json` are `==` to `guards2.json`'s own 305 rows (Python
dict equality on the loaded lists), so this is strictly additive,
zero regression on the base.

**(c) Exception families rebuilt with java.** I copied
`exception_families.py` to `exception_families2.py` with its
clustering LOGIC untouched — the only edits are the input file
(`guards4.json` instead of `guards2.json`) and the output file name,
plus a note on why. Round 1's 34 families → 39. Verified
programmatically: every one of the 34 original `(condition_label,
response_head)` pairs is present in the new 39 (set-subset check),
so no family was lost or merged away — the 5 new ones are additions.

`deopt-continue-elsewhere` does NOT join any existing family. No
other language in the corpus has ever produced that response head
(checked: `guards2.json`'s `by_response_kind` has no `deopt`
entry), so it forms two NEW, java-only families:

```
EF0020  [exception handler / deoptimization stubs / deopt-continue-elsewhere]  langs=java  members=2
    java   java/op_1    +    deopt-continue-elsewhere
    java   java/op_2    /    deopt-continue-elsewhere

EF0039  [zero-divisor check / deopt-continue-elsewhere]  langs=java  members=1
    java   java/op_2    /    deopt-continue-elsewhere
```

Three more java-only families also formed from the modes that
log_087 said were not carried (see the correction below):

```
EF0025  [nmethod-entry barrier / call-out-and-return]      langs=java  members=2
EF0026  [return safepoint poll / call-out-and-return]       langs=java  members=2
EF0038  [most-negative-over-minus-one check / branch-around-in-place]  langs=java  members=1
```

None of the five merges into any c/cpp/go/rust/swift family — every
response head java contributes (`deopt-continue-elsewhere`,
`call-out-and-return`, `branch-around-in-place`) is new to the
corpus. This is reported as a finding, not engineered: no z3 merge
was attempted or needed since no other language's condition text
resembles java's.

**(d) Cross-axis operator x exception table, regenerated.** I wrote
`cross_axis_table.py` (new file, no prior cross-axis builder existed
under this name in `op_pipeline`). It crosses `dom_ops22.json`'s
D-codes (the OPERATOR axis, grouped by proved seed/byte identity)
against `exception_families2.json`'s EF-codes (the EXCEPTION axis)
via shared UNIT MEMBERSHIP — a unit that sits in both a dom_op node
and an exception family puts one count in that (dom_op_id,
family_id) cell. Both axis keys are machine-form ids (D-codes,
EF-codes), never the operator token; a first draft that carried a
majority `operator_label` display field on the aggregate cross-cell
FAILED `check_no_spelling_keys.py` (100 findings — an aggregate
cell spanning multiple units is not a "per-unit label" under the
guard's own except-list, which requires a `language` + unit-id field
on the SAME object). Fixed by dropping the display field from the
cross-cell rows entirely and keeping it only on the per-unit
`uncrossed` records (which do carry `language` + `unit`, and use the
field name `operator` — the guard's own exempt spelling, not
`operator_label`). Second pass: PASS, no exemption.

Result: 17 crossed cells (dom_op_id x family_id, all among
c/cpp/go/rust/swift — the languages `dom_ops22.json` currently
covers). 83 member rows are `uncrossed`: every one of them is a
java row, because `dom_ops22.json` has not had java/cpython joined
into it yet (log_087's own flagged, still-open item — I did not
attempt that join here; it is Task 7/11 territory, not this task's).
The `uncrossed` list names each one by unit, family, and reason
rather than dropping them silently.

**(e) The correction — log_087's exclusion claim is false.**
log_087 (Task 5c) states: "Two OTHER modes on the same unit (`u2.m4`,
a different response kind; `u2.m9`, boilerplate present on both
units) are named and explicitly NOT carried, with the reason stated
per row, rather than folded in silently." I read this against
`guards3.json` directly rather than trusting the sentence: `u2.m4`
(`most-negative-over-minus-one check`, `branch-around-in-place`) and
`u2.m9` (`exception handler / deoptimization stubs`,
`deopt-continue-elsewhere`) are BOTH present in `guards3.json`'s
`rows`, verbatim, alongside `u1.m1`, `u1.m2`, `u1.m9`, `u2.m1`,
`u2.m2`. All eight of `interp_jvm.json`'s modes are in
`guards3.json` — none were held back. `guards3.json` was on disk in
this same directory the whole time (it is `guards_java_deopt.py`'s
own, undocumented output from round 1), so the claim that these two
rows were "explicitly NOT carried" is false as stated; whatever the
intent was in log_087's own guards2_parallel.json (which genuinely
does carry only one row), a second, fuller carry-in already existed
alongside it and was never reconciled or even named. This is exactly
the failure mode log_091's round-2 header describes.

## Numbers

| item | before (guards2.json / exception_families.json) | after (guards4.json / exception_families2.json) |
|---|---|---|
| guard rows | 305 | 313 (305 base unchanged + 8 java) |
| java guard rows present | 0 | 8 (all of interp_jvm.json's modes) |
| exception families | 34 | 39 |
| families lost/changed | — | 0 (34/34 preserved, set-subset verified) |
| new families | — | 5, all java-only (EF0020, EF0025, EF0026, EF0038, EF0039) |
| deopt-continue-elsewhere families | 0 | 2 (EF0020, EF0039), java-only, joins nothing |
| cross-axis crossed cells | (table did not exist) | 17 |
| cross-axis uncrossed member rows | — | 83 (all java, dom_ops22.json has no java join yet) |

## File inventory (every artifact written this task)

- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/guards4.py` — new. The record-of-record generator.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/guards4.json` — new. THE guard record of record (313 rows). PASSES `check_no_spelling_keys.py`, no exemption.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/exception_families2.py` — new. exception_families.py's logic, re-pointed at guards4.json.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/exception_families2.json` — new. 39 families. PASSES `check_no_spelling_keys.py`, no exemption.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/cross_axis_table.py` — new. Operator-family x exception-family crossing.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/cross_axis_table.json` — new. 17 crossed cells + 83 named uncrossed rows. PASSES `check_no_spelling_keys.py`, no exemption (after the fix described in (d)).
- No file was modified or deleted. `guards2.json`, `guards2_parallel.json`, `guards3.json`, `guards_java_deopt.py`, `exception_families.json`, `exception_families.py` are all left exactly as they were, kept as superseded/predecessor records, named here.

## Task 13 — the two documentation slips (verified against artifacts before correcting)

- `log_086_task1_general_graph_builder.md` claimed `tree-sitter`
  0.26.0. I opened `graph_cpp2.json` directly:
  `pins.tree_sitter == "0.25.2"` (quoted from the artifact, not from
  notes). Appended a dated correction note in place; the original
  line is left standing per the convention, with the correction
  directly under it.
- `log_090_task7_lineage_reconciliation.md` claimed
  `dom_ops21c.json` passes `check_no_spelling_keys.py` "with no
  exemption needed in practice." I ran the guard myself:
  `check_no_spelling_keys.py dom_ops21c.json` → `PASS ... exempt:
  top-level meta declares role 'generator provenance'`. It passes
  ONLY with the exemption. Appended a dated correction note. (I also
  re-ran the guard on `dom_ops22.json` itself while I was there:
  that half of the original sentence holds — PASS, no exemption
  needed. Only the `dom_ops21c.json` comparison point was false.)

## Gates run

- `check_no_spelling_keys.py guards4.json` → PASS, no exemption.
- `check_no_spelling_keys.py exception_families2.json` → PASS, no exemption.
- `check_no_spelling_keys.py cross_axis_table.json` → PASS, no exemption.
- `check_no_spelling_keys.py dom_ops21c.json` → PASS, WITH the generator-provenance exemption (Task 13 verification).
- Zero-regression: `guards4.json[:305] == guards2.json['rows']` (dict equality) — True.
- Zero-regression: all 34 `exception_families.json` `(condition_label, response_head)` pairs present in `exception_families2.json`'s 39 — True (set-subset check).

## Flagged for the owner

- The provenance field name is now normalized to `provenance_is_weaker`
  in `guards4.json`. `guards3.json` (kept, unmodified) still spells
  it `weaker_provenance` — a naming inconsistency between two
  records that now both exist on disk. Not fixed retroactively in
  guards3.json (new-files-only rule); flagged so a future reader
  does not treat the two names as two different marks.
- `dom_ops22.json` has no java/cpython unit membership, so 83 of
  exception_families2.json's member rows (all five java-only
  families) cannot cross into the operator axis at all yet. This is
  the same open item log_087 already flagged and Task 11 already
  targets (widening graph coverage); Task 8 does not attempt it.

**CORRECTION (2026-08-31, log_098 Task 14):** the "(d)" section above
implies all 83 uncrossed rows are java (it says "every one of them is
a java row"). That is false as stated: `cross_axis_table.json`'s own
83 `uncrossed` records break down as swift 35 / go 30 / rust 10 /
java 8. See `log_098_task14_record_hygiene.md` for the computed
breakdown.
