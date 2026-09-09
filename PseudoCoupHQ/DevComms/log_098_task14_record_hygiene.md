# log 098 — Task 14: record hygiene (correction, provenance marks into JSON, stray-log naming, mtime sweep)

Date: 2026-08-31. Answers log_097's Task 14 (round 3, item one). Working
directory: `~/Programming/PseudoCoupHQ/Research/op_pipeline` (+
`../compiler_graph` for part (d)).

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

## 1. walkthrough (protocol v2 — plain words first)

Task 14 is four small hygiene fixes, none of them touching the pipeline's
logic:

**(a)** log_092 claims, in its section (d), that all 83 rows the
cross-axis table could not cross onto the operator axis are java rows.
I did not trust that sentence — round 3's own rule says a sentence
of the shape "all N are X" is computed, never remembered. I opened
`cross_axis_table.json` directly and counted the `language` field on
every one of its 83 `uncrossed` records.

**(b)** `add_java.json` (round 1's precedent for a weak-provenance mark)
carries `"provenance_is_weaker": true` as a top-level field on the
member record. log_092 already normalized this field name (over
`guards3.json`'s `weaker_provenance`) into `guards4.json`. The
ruby/php interpreter artifacts (`interp_ruby.json`, `interp_php.json`
from round 2's log_087-adjacent work, `interp_ruby_handlers.json`,
`interp_php_handlers.json` from log_095's Task 12) carry the mark only
in prose (log_095 section 6: "every row... carries `provenance_is_weaker:
true` or its equivalent framing" — but the JSON itself did not have the
field). I added `"provenance_is_weaker": true` as a top-level key to
all four files, matching `add_java.json`'s field name and shape (a
top-level boolean on the record, not a per-row field, since none of
these four files' top-level shape is a member-record array — see the
per-file shapes below). I searched for derived `op_units_*`/`sem_anchored_*`
records built from ruby or php and found none on disk (listed below);
no derived record exists to carry the field into.

**(c)** `task10_seed_prove.log` is named formally here: it is a 2-line
stray stdout capture from round 2's Task 10 seed-prove run
(`resolved(1 proof)=0 proof-ambiguous=0 of 62`) — the same honest zero
log_097's state-at-handoff already cites ("task 10's honest zero").
Benign, kept as a record, no action needed beyond this naming.

**(d)** I swept `op_pipeline` and `compiler_graph` file mtimes for the
round-2 window (2026-08-31 21:00–22:00) and checked every file's name
against what round-2's own logs (log_092 through log_096) name as
created. Nothing was found on disk that no round-2 log lists — full
breakdown below.

## 2. computed breakdown — (a) the 83 uncrossed rows

Read directly from `cross_axis_table.json`'s `uncrossed` list (83
records), tallying the `language` field on each:

```python
import json, collections
d = json.load(open('cross_axis_table.json'))
u = d['uncrossed']
len(u)                                            # 83
collections.Counter(r['language'] for r in u)
# Counter({'swift': 35, 'go': 30, 'rust': 10, 'java': 8})
```

| language | uncrossed rows |
|---|---|
| swift | 35 |
| go | 30 |
| rust | 10 |
| java | 8 |
| **total** | **83** |

35 + 30 + 10 + 8 = 83. Matches log_097's own audit figure exactly
(swift 35 / go 30 / rust 10 / java 8), which is what triggered this
task. log_092's sentence ("83 member rows are `uncrossed`: every one
of them is a java row... because `dom_ops22.json` has not had java/
cpython joined into it yet") is FALSE as stated — only 8 of the 83
are java. The other 75 are uncrossed for the SAME underlying reason
(no `dom_op_id` yet for that unit in `dom_ops22.json`) but on
swift/go/rust units log_092 never counted. A sample of the reason
strings, read verbatim off three non-java rows, confirms the
mechanism is the same one log_092 describes, just broader than it
claimed:

```
{'family_id': 'EF0001', 'unit': 'go/op_176', 'language': 'go', 'operator': '<<',
 'reason': 'unit has no dom_op_id (not yet joined into dom_ops22.json -- see COVERAGE NOTE)'}
```

Correction appended to log_092 as a single pointer line (its body left
standing, per the standing convention of correcting in place rather
than rewriting history):

> **CORRECTION (2026-08-31, log_098 Task 14):** the "(d)" section above
> implies all 83 uncrossed rows are java... See
> `log_098_task14_record_hygiene.md` for the computed breakdown.

## 3. (b) provenance marks moved into the JSON artifacts

Per-file shape (read before editing, since the four files do not
share a schema — none is a member-record-array like `add_java.json`
happens to be, so the field is added top-level rather than
per-member):

| file | top-level keys before | field added |
|---|---|---|
| `interp_ruby.json` | meta, method, header_counts, bytecode_disasm, dispatch_top_lines, reading, what_was_not_done | `provenance_is_weaker: true` (top-level) |
| `interp_php.json` | meta, method, header_counts, dispatch_top_lines, reading, what_was_not_done | `provenance_is_weaker: true` (top-level) |
| `interp_ruby_handlers.json` | pin, arch, handlers | `provenance_is_weaker: true` (top-level) |
| `interp_php_handlers.json` | pin, arch, defect, defect_detail, what_this_means, handlers | `provenance_is_weaker: true` (top-level) |

**Derived-record search (verified against disk, not assumed):**

```
$ grep -rl "interp_ruby\|interp_php" --include="*.py" .
fold_interp_php.py   fold_interp_ruby.py   langs.py
$ grep -rl "interp_ruby\|interp_php" --include="*.json" .
interp_php.json   interp_ruby.json
$ ls | grep -i "op_units_\|sem_anchored_"
op_units_asg_{c,cpp,go,rust,swift}.json  op_units_{c,cpp,cpython,cpython2,csharp,dart,go,java,java2,javascript,rust,swift}.json
sem_anchored_{c,cpp,cpython2,go,java2,rust,spill*,swift}.json
```

`fold_interp_ruby.py`/`fold_interp_php.py` are the GENERATORS that
produced `interp_ruby.json`/`interp_php.json` themselves (they write to
those exact paths, confirmed by reading their `json.dump(doc, json_path...)`
lines) — not downstream consumers. There is no `op_units_ruby.json`,
`op_units_php.json`, `sem_anchored_ruby*.json`, or `sem_anchored_php*.json`
on disk. **Claim verified: no op_units or sem_anchored record has been
derived from ruby or php evidence.** Nothing further to mark.

Spelling guard re-run on all four touched files after the edit:

```
$ python3 check_no_spelling_keys.py interp_ruby.json
PASS interp_ruby.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py interp_php.json
PASS interp_php.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py interp_ruby_handlers.json
PASS interp_ruby_handlers.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py interp_php_handlers.json
PASS interp_php_handlers.json -- no operator token in any key, grouping, pairing or row structure
```

All four PASS, no exemption.

## 4. (c) task10_seed_prove.log, named

`~/Programming/PseudoCoupHQ/Research/op_pipeline/task10_seed_prove.log`
— 2 lines, stray stdout capture from round 2's Task 10 run
(`task10_seed_prove.py`):

```
wrote ~/Programming/PseudoCoupHQ/Research/op_pipeline/task10_seed_prove_results.json (62 targets)
resolved(1 proof)=0 proof-ambiguous=0 of 62
```

Benign, matches `task10_seed_prove_results.json`'s own honest-zero
result already cited in log_097's state-at-handoff and detailed in
log_096. No file created or modified by this task other than naming
it here.

## 5. (d) mtime sweep, round-2 window (2026-08-31 21:00–22:00)

**op_pipeline** — 34 files with mtime in the window (`find . -maxdepth 1
-type f -newermt "2026-08-31 21:00:00" ! -newermt "2026-08-31 22:00:00"`):

```
guards4.py  guards4.json  exception_families2.py  exception_families2.json
interp_probe_persist.sh  census27.py  census27.json  cross_axis_table.py
interp_e_handlers.sh  cross_axis_table.json  interp_probe2.sh
interp_probe3.sh  interp_e2_handlers.sh  build_super_ops2.py  super_ops2.json
canon27.py  canon27_units_c.json  canon27_units_cpp.json  canon27_units_go.json
canon27_units_rust.json  canon27_units_swift.json  interp_probe4.sh
interp_e3_php_fix.sh  interp_e4_php_libxml.sh  task10_seed_prove.log
task10_seed_prove.py  task10_seed_prove_results.json  task10_nonzero_pool_dump.txt
build_table24b.py  dominant_table24b.json  dom_ops22b.json  representatives24b.json
interp_ruby_handlers.md  interp_php_handlers.md
```

Every name checked against grep over log_092/093/094/095/096 (the
round-2 task logs):

- `guards4.*`, `exception_families2.*`, `cross_axis_table.*` — named in
  log_092 (Task 8).
- `census27.*`, `canon27*` — named in log_093 (Task 9).
- `build_super_ops2.py`, `super_ops2.json` — named in log_094 (Task 11).
- `task10_seed_prove.*`, `task10_nonzero_pool_dump.txt`,
  `build_table24b.py`, `dominant_table24b.json`, `dom_ops22b.json`,
  `representatives24b.json` — named in log_096 (Task 10).
- `interp_probe_persist.sh`, `interp_e_handlers.sh`, `interp_probe2.sh`,
  `interp_probe3.sh`, `interp_e2_handlers.sh`, `interp_probe4.sh`,
  `interp_e3_php_fix.sh`, `interp_e4_php_libxml.sh`,
  `interp_ruby_handlers.md`, `interp_php_handlers.md` — named in log_095
  (Task 12). (`interp_ruby_handlers.json`/`interp_php_handlers.json`
  themselves fall outside the window on disk now because this task's
  own edit in section 3 above updated their mtimes to today; log_095
  already names both explicitly, so nothing is lost by that.)

**Result: every file in the window is named by some round-2 log.
Nothing unlisted found.**

**compiler_graph** — 2 files in the same window:

```
build_graph3.py   graph_cpp3.json
```

Both named in log_094 (Task 11's widened-graph work). **Nothing
unlisted found here either.**

## 6. gates run

- `check_no_spelling_keys.py interp_ruby.json` → PASS, no exemption.
- `check_no_spelling_keys.py interp_php.json` → PASS, no exemption.
- `check_no_spelling_keys.py interp_ruby_handlers.json` → PASS, no exemption.
- `check_no_spelling_keys.py interp_php_handlers.json` → PASS, no exemption.
- Computed count, not remembered: `cross_axis_table.json`'s 83
  `uncrossed` rows, tallied by `language` field — swift 35 / go 30 /
  rust 10 / java 8, sums to 83.

## 7. file inventory (every file this session touched or created)

New:
- `~/Programming/PseudoCoupHQ/DevComms/log_098_task14_record_hygiene.md` — this log.

Modified (permitted by this task's explicit grants — (a) one pointer
line into log_092; (b) the `provenance_is_weaker` field into the four
named ruby/php JSON artifacts):
- `~/Programming/PseudoCoupHQ/DevComms/log_092_task8_guards_record.md` —
  one correction pointer line appended at the end; original body left
  standing.
- `~/Programming/PseudoCoupHQ/Research/op_pipeline/interp_ruby.json` —
  added top-level `provenance_is_weaker: true`.
- `~/Programming/PseudoCoupHQ/Research/op_pipeline/interp_php.json` —
  added top-level `provenance_is_weaker: true`.
- `~/Programming/PseudoCoupHQ/Research/op_pipeline/interp_ruby_handlers.json` —
  added top-level `provenance_is_weaker: true`.
- `~/Programming/PseudoCoupHQ/Research/op_pipeline/interp_php_handlers.json` —
  added top-level `provenance_is_weaker: true`.

No other file was created, modified, or deleted. No op_units or
sem_anchored file exists for ruby or php (verified, section 3), so
none was touched.

## 8. claims NOT made

- No claim that the mtime sweep is exhaustive proof no OTHER file was
  ever touched in the window and then reverted/renamed before this
  sweep ran — only that, of what is on disk NOW with an mtime in the
  window, every name is accounted for in a round-2 log.
- No claim about php's dead-end build (log_095's territory) — untouched
  here.
- No table-membership or bridge/dominance claim about the ruby/php
  handler slices — that is Task 17's reserved question, not this
  task's.
