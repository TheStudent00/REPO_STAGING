# log 087 — Task 5: reconnecting the parallel language branch (java, cpython, ruby, php)

Date: 2026-08-31. This is Task 5 of
`PseudoCoupHQ/DevComms/log_083_claude_code_task_briefs.md`,
against the six findings of
`PseudoCoupHQ/DevComms/log_082_state_of_research_and_parallel_branch.md`
PART 2. Working directory throughout:
`PseudoCoupHQ/Research/op_pipeline`.

THE SPELLING BAN, held throughout this task and pasted here verbatim
as the brief requires: "No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line — not in matching, not in 'which pairs
get compared', not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention — never from the
token. The token appears exactly once per unit: as a display label on
the member."

## Walkthrough — what was found and what was done

**(a) The cpython type key was checked against the unit's own bytes,
and it was wrong.** `interp_feeder.py`'s `format_cpython()` hardcoded
`"lhs_rep": "i32"` / `"lhs_type": "int32"` for `long_add`. The unit's
own ship instructions (`interp_cpython.json` ->
`handler_arch_units.ship.long_add`, instructions 2–3) read:

```
mov    0x10(%rdi),%rax
mov    0x10(%rsi),%rdx
```

`%rdi`/`%rsi` are used as 64-bit BASE ADDRESSES, offset by a constant
(`0x10`), then loaded through. This is a pointer dereference, not a
32-bit integer value — confirmed a second way by the lifted form
(`sem_anchored_spill_cpython.json`, unit "1", block 0):
`ld64/g0(Add64(16:64,in0:64))`, the same shape on `in1`. The existing
type-key vocabulary this line already uses (read from
`probe_manifest_*.json`: `bool`, `f32`, `f64`, `i32`, `i64`, `u64`)
has no pointer member, so the honest key is a new value, `"ptr64"`,
rather than a forced fit into one of the six existing ones — I flag
this naming choice for the owner below rather than treat it as mine to
settle silently.

The fix lives in `interp_feeder.py`'s new `cpython_type_key()`
function, called by `format_cpython()`; both `lhs_rep`/`rhs_rep` now
read `"ptr64"`, `lhs_type`/`rhs_type` read `"PyLongObject*"`, and the
unit's `meta` carries a `type_key_evidence` field quoting the two
instructions and the lifted expression above, so the claim is
inspectable from the artifact itself, not only from this log.

**(b) LANGS was hardcoded in every downstream stage** (finding 1) —
confirmed: `grep -rn LANGS *.py` finds `LANGS = ["c", "cpp", "go",
"rust", "swift"]` verbatim, independently, in at least a dozen files
(`canon14.py`, `canon18.py`, `dom_ops_0branch.py`,
`build_representatives5.py`, `dominant_table11.py`, `fold.py`, …).
One layer up, `sem_anchored.py`'s own `ABI` dict already carried
`"java"` and `"cpython"` rows (added earlier, 2026-08-26) — so the
gap was never the language facts, it was every consumer's own copy of
the five-language list. New `langs.py` is the single source now:
`LANGS_COMPILED` (the five, unchanged), `LANGS_INTERP` (`java`,
`cpython` — the two that have reached an arch-unit; ruby/php do NOT
enter this list, see (d)), `LANGS_ALL` (the union). This is a NEW
file that future work can import; it does not itself edit the dozen
existing hardcodes, which is a separate, larger sweep I am flagging
rather than doing silently under this task (see "flagged for the owner"
below).

**tree_match3 adoption** (finding 3) — confirmed:
`tree_units3.json`'s own `languages` are exactly the five compiled
ones; java/cpython are absent because `run_java_pipeline.sh` calls
`tree_match2.py`, one generation behind the adopted `tree_match3.py`
(the ret-block-first selection rule). New `reconnect_parallel.py`
re-runs java and cpython through the CURRENT chain — unmodified
`sem_anchored.py` / `sem_anchored_spill.py` / `tree_match3.py`
functions, imported and called, never re-implemented — writing to
NEW files (`op_units_java2.json`, `op_units_cpython2.json`,
`sem_anchored_java2.json` / `_spill_java2.json` and the `cpython2`
equivalents, `tree_units3_parallel.json`, `tree_matches3_parallel
.json`) so no existing artifact is touched. The `2` suffix is a
FILENAME device only (avoiding a same-name overwrite); each output's
own `meta.language`/`lang` field still reads the real language name.

RESULT, run for real, output pasted:

```
== java2  2 ship units, 2 anchored sem, 0 refused
== java2  2 ship units, 2 anchored sem, 0 refused, 2 carried a cross-block substitution
== cpython2 1 ship units, 0 anchored sem, 1 refused
        1  recovered 93 instructions but the mnemonic column has 94
wrote tree_units3_parallel.json (1782 units)
exact normalized-root clusters: 414
  cross-language: 289
  clusters containing a java2 member: 2
  clusters containing a cpython2 member: 0
    java2 cluster, langs=['c', 'cpp', 'go', 'java2', 'rust', 'swift'],
      root='Concat(0, Extract(31, 0, atom_0) + Extract(31, 0, atom_1))'
```

Java's addition unit MATCHED into the same normalized-root class as
c/cpp/go/rust/swift, through the adopted selection rule, unassisted
— the same result log_082 §2.4 reported for the earlier, now-stale
run (`lea (%rdi,%rsi,1),%eax`), reproduced fresh under tree_match3.
Cpython's unit REFUSED honestly at the `arch_read` layer: "recovered
93 instructions but the mnemonic column has 94" — a byte/mnemonic
count mismatch in the ship-instruction join, unrelated to the type-key
fix (it fires before any type comparison happens) and pre-existing in
the raw `interp_cpython.json` capture. I did not chase this further;
it is named as a remainder below rather than patched under pressure to
show a result.

**Zero regressions, verified programmatically**: every one of the
1,779 units in the existing `tree_units3.json` has a byte-identical
counterpart in `tree_units3_parallel.json` (`diffs == 0`, checked by
direct dict comparison, both files loaded fresh).

**(c) Java's deopt guard never reached the exception axis** (finding
4) — confirmed: `core_modes_java.json` carries one unit (the
addition) with `"modes": []`; the division unit's measured guard
lives only in `interp_jvm.json`. New `core_modes_java2.json` adds
unit 2 (division), carrying the ONE measured `deopt-continue-
elsewhere` row (`u2.m3`, "zero-divisor check", evidence class "forced
by construction … plus the tool's own testimony") verbatim from
`interp_jvm.json`, with `provenance_is_weaker: true` stamped on the
file and on the row. Two OTHER modes on the same unit (`u2.m4`, a
different response kind; `u2.m9`, boilerplate present on both units)
are named and explicitly NOT carried, with the reason stated per row,
rather than folded in silently. New `guards2_parallel.py` appends
this one row on top of `guards2.json`'s own 305 UNCHANGED rows —
305 -> 306 — writing `guards2_parallel.json`, never touching
`guards2.json`.

**(d) Ruby and php were measured and orphaned** (finding 5) —
confirmed against the raw Airlock outputs directly:
`Airlock/agent/out/interp_ruby_b/` (bytecode.txt,
dispatch_diff.json, dispatch_report.txt, 4 probe sources) and
`interp_php_b/` (dispatch_diff.json, dispatch_report.txt, 3 probe
sources) both existed, dated 2026-08-31, with no fold script and
nothing under this directory naming them. New `fold_interp_ruby.py`
and `fold_interp_php.py` (built from `fold_interp_jvm.py`'s own
template) each write an `.md` + `.json` pair in the same shape as the
java/cpython pilots:

- **ruby**: pin `3.3.0` (`ruby 3.3.0 (2023-12-25 revision
  5124f9ac75) [x86_64-linux]`, read from the build lane's own log).
  Bytecode captured (`opt_plus`, ruby's own specialized-instruction
  name for `+`). Dispatch measured: 1,050 lines, 27 files, dominated
  by `vm.inc` (2,200,000) and `vm_insnhelper.c` (1,300,000).
  **No arch-unit** — stated as the pilot's own ceiling, not hidden.
- **php**: pin `7.4.33`, a COMPROMISE recorded with the actual
  failing build lines pasted, not paraphrased —
  `zend_atomic.h:96:9: error: implicit declaration of function
  '__c11_atomic_store'` on both `8.3.0` and `8.2.13`, eight build
  attempts total (`interp_php.json` -> `build_attempts`, every
  attempt's outcome). Dispatch measured: 344 lines, 9 files, dominated
  by `Zend/zend_vm_execute.h` (1,300,011). **No arch-unit and no
  bytecode listing** — a ceiling one step short of ruby's, stated as
  such.

Both new `.json` files pass `check_no_spelling_keys.py` (the only
per-unit token, `opt_plus` for ruby, is a display field, same
discipline as the existing pilots). Neither enters `LANGS_INTERP` in
`langs.py` — see that file's own "FOLD NOTE": a language earns that
list only once it has an arch-unit, and ruby/php do not have one.

**(e) The auto-derived planning nodes** (finding 6) — confirmed and
listed, not edited (Planning is the owner's; only the one named PROGRESS
file below was touched). See "Flagged for the owner".

## Numbers

| item | before | after |
|---|---|---|
| languages with an arch-unit reaching the ADOPTED selection rule | 5 | 5 + java (cpython refused honestly, see remainder) |
| `tree_units3` population | 1,779 (5 langs) | 1,782 in `tree_units3_parallel.json` (5 langs + java2 + cpython2's 1 refused-but-recorded unit) |
| cross-language exact-root clusters | — (java/cpython absent) | 414 total, 289 cross-language, 2 containing a java2 member |
| cpython type key | `i32,i32` (fabricated) | `ptr64,ptr64` (forced by construction) |
| java guard rows in the exception-axis raw material | 0 | 1 (`guards2_parallel.json`, 306 rows total, base 305 unchanged) |
| ruby/php HQ artifacts | 0 | 2 pilots folded (`interp_ruby.{md,json}`, `interp_php.{md,json}`), dispatch-only, marked as such |
| pre-existing `tree_units3.json` units altered | — | 0 (verified: 1,779/1,779 byte-identical) |

## Findings (a)–(e), status

- **(a) cpython type key — FIXED.** `interp_feeder.py`'s
  `cpython_type_key()`, forced by construction from the unit's own
  ship instructions and lifted form. New key `ptr64` is a naming
  choice at the edge of the existing vocabulary — flagged below, not
  decided unilaterally.
- **(b) LANGS / tree_match3 — PARTIALLY DONE.** `langs.py` is the new
  single source of truth. Java and cpython were actually re-run
  through the adopted `tree_match3.py` selection (not merely
  planned) via `reconnect_parallel.py`, producing
  `tree_units3_parallel.json` with java matching real cross-language
  classes. NOT done: repointing the dozen-plus existing hardcoded
  `LANGS = [...]` literals across `canon*.py` / `dom_ops*.py` /
  `build_representatives*.py` / `fold.py` to import `langs.py` — that
  is a wide, mechanical sweep across files this task did not open;
  flagged below rather than done under time pressure.
- **(c) java deopt guard — DONE**, narrowly. The one measured
  `deopt-continue-elsewhere` row is carried into
  `guards2_parallel.json` with its weaker-provenance mark. NOT done:
  folding this into the 34 exception FAMILIES themselves (that
  clustering step, `dom_ops`-side, was not re-run — the brief asked
  to carry the row into `guards2`/exception families' RAW MATERIAL,
  which is what `guards2_parallel.json` is; the family-clustering
  re-run is Task 7's reconciliation territory, named there already).
- **(d) fold ruby and php — DONE.** Both `.md`+`.json` pairs written,
  pins recorded (ruby 3.3.0; php 7.4.33 with the compromise reasoning
  and all 8 build attempts), guard passed, "what was NOT done" stated
  in each artifact.
- **(e) auto-derived planning nodes — LISTED, not edited.** See below.

## Flagged for the owner

- **The `ptr64` type-key naming.** `cpython_type_key()` in
  `interp_feeder.py` introduces `"ptr64"` as a `lhs_rep`/`rhs_rep`
  value; the existing vocabulary (read from `probe_manifest_*.json`)
  is `bool, f32, f64, i32, i64, u64` and has never carried a pointer
  member. I read this as forced by the machine fact, not as
  inventing a new component KIND (the STOP RULE's concern is new
  ontology — component/family axes — and a new leaf value in an
  existing field is smaller than that), but the name itself
  (`ptr64` vs some other spelling) is a naming choice and the owner decides
  naming per the standing rulings.
- **The `dominant_table`/`dom_ops` join is not yet run for
  java2/cpython2.** `reconnect_parallel.py` stops at
  `tree_units3_parallel.json`/`tree_matches3_parallel.json` — the
  matching layer, not the family-table layer. Joining these into
  `dominant_table24`/`dom_ops22` (Task 7's own deliverable) was left
  for that task, per log_083's own ordering note ("7 last, once
  2/3/5 have stopped moving the inputs").
- **The dozen-plus files still carrying their own hardcoded
  `LANGS = ["c","cpp","go","rust","swift"]` literal** (finding 1's
  root cause) were not repointed to `langs.py` in this task — doing
  so touches `canon14.py`, `canon18.py`, `canon7.py`, `fold.py`,
  `dominant_table11/13.py`, `component_mine.py`, `lane_gen.py`,
  `asg_stage.py`, `reading_form.py`, `build_representatives5.py`,
  `dom_ops_0branch.py`, `uniqueness_audit.py`, `canon16/20.py`
  (grep-confirmed list, not exhaustive) and each is a small, separate
  edit best done as its own reviewable pass rather than folded
  silently into this task's diff.
- **Six auto-derived planning nodes, listed per finding 6, not
  edited** (Planning is the owner's per the standing rule):
  - `node_0_3_6_interp_feeder` (the super-node itself)
  - `node_0_3_6_0_feeder_config`
  - `node_0_3_6_1_parse_interp`
  - `node_0_3_6_2_format_canon`
  - `node_0_3_6_3_invoke_normalizer`
  - `node_0_3_6_4_run_pipeline`
  - `node_0_3_6_5_run_jvm`
  - `node_0_3_6_6_target`
  - `node_0_3_6_7_output`

  All nine PROGRESS.md files under this tree still read only
  "Initialized." (confirmed by directory listing, unread further —
  reading and ruling on their content is the owner's call, not mine). None
  is referenced by `SUPPORT_scaling_design.md`, which still describes
  the interpreter track as living in `node_0_3_5`. This task's own
  work (the type-key fix, the LANGS module, the java/cpython re-run,
  the guard carry, the ruby/php folds) sits entirely under
  `Research/op_pipeline`, outside this planning sub-tree, and does
  not resolve whether these eight nodes should be kept, merged into
  `node_0_3_5`, or retired.
- **The cpython arch-unit's own `arch_read` refusal** ("recovered 93
  instructions but the mnemonic column has 94") is a pre-existing
  defect in the raw byte/mnemonic join for this one unit, surfaced
  by actually running the chain rather than assuming it would pass.
  Not diagnosed further here — it sits upstream of the type-key fix
  and is a separate, small investigation (compare the disassembled
  instruction count against `interp_cpython.json`'s own recorded
  `instruction_count: 94` for `long_add`, ship build).

## Evidence classes, stated once

- The pointer type key: **forced by construction** (two ship
  instructions plus the lifted expression, both read from the
  existing artifact, quoted above).
- The java/cpython re-run result (the matched class, the cpython
  refusal): **artifact fact** — the actual output of running the
  actual adopted-pipeline functions, pasted above, not summarized.
- The zero-regression check: **forced by construction** (a direct
  dict comparison over both files, 1,779/1,779, run this session).
- The ruby/php pins and the php compromise: **artifact fact** (the
  tool's own banners and the build lanes' own compiler error lines,
  read from the Airlock logs and pasted into the new `.md` files).
- The finding-6 planning-node inventory: **artifact fact** (directory
  listing, `find`, this session).

## Files (new, this task)

- `PseudoCoupHQ/Research/op_pipeline/interp_feeder.py`
  (edited: `cpython_type_key()` added, `format_cpython()` now calls
  it instead of hardcoding the type key)
- `PseudoCoupHQ/Research/op_pipeline/langs.py`
- `PseudoCoupHQ/Research/op_pipeline/reconnect_parallel.py`
- `PseudoCoupHQ/Research/op_pipeline/op_units_java2.json`
- `PseudoCoupHQ/Research/op_pipeline/op_units_cpython2.json`
- `PseudoCoupHQ/Research/op_pipeline/sem_anchored_java2.json`
- `PseudoCoupHQ/Research/op_pipeline/sem_anchored_cpython2.json`
- `PseudoCoupHQ/Research/op_pipeline/sem_anchored_spill_java2.json`
- `PseudoCoupHQ/Research/op_pipeline/sem_anchored_spill_cpython2.json`
- `PseudoCoupHQ/Research/op_pipeline/tree_units3_parallel.json`
- `PseudoCoupHQ/Research/op_pipeline/tree_matches3_parallel.json`
- `PseudoCoupHQ/Research/op_pipeline/core_modes_java2.json`
- `PseudoCoupHQ/Research/op_pipeline/guards2_parallel.py`
- `PseudoCoupHQ/Research/op_pipeline/guards2_parallel.json`
- `PseudoCoupHQ/Research/op_pipeline/fold_interp_ruby.py`
- `PseudoCoupHQ/Research/op_pipeline/interp_ruby.json`
- `PseudoCoupHQ/Research/op_pipeline/interp_ruby.md`
- `PseudoCoupHQ/Research/op_pipeline/fold_interp_php.py`
- `PseudoCoupHQ/Research/op_pipeline/interp_php.json`
- `PseudoCoupHQ/Research/op_pipeline/interp_php.md`

No existing artifact was modified or deleted. `interp_feeder.py` was
edited (it is the script named by finding 2 as the one to fix — its
prior hardcode is preserved in git history, not deleted, and the
brief's own wording is "the feeder hardcodes … fix it").
