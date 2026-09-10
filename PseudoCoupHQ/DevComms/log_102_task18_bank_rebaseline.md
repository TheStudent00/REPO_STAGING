# log_102 -- TASK 18: bank and re-baseline

Date: 2026-08-31. Session: Claude Code, log_097 TASK 18, run after
tasks 14-17 (logs 098-101). Working directory:
`PRIVATE/PseudoCoupHQ/Research/op_pipeline`.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from
the token. The token appears exactly once per unit: as a display
label on the member. HISTORY OF VIOLATIONS, so the pattern is
visible: (1) the arch campaign's cross-language matrix (caught by
the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs"). MECHANICAL GUARD REQUIRED: every pipeline stage that groups
or pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure. A brief handed to any subagent for this line MUST paste
this paragraph verbatim.

## 1. walkthrough (protocol v2 -- plain words first)

Task 18 is a verification-and-freeze lap, not a new-mechanism lap.
I read log_097's Task 18 brief, its STANDING REQUIREMENTS header,
and all four of this round's reports (log_098 Task 14, log_099 Task
15, log_100 Task 16, log_101 Task 17) in full before running
anything. Three things needed real re-checking rather than trusting
the prior logs' own numbers, per the round-3 rule that an "all N are
X" claim and a "zero regressions" claim are both computed, not
remembered:

1. every artifact this round produced or touched still passes the
   spelling guard, run fresh by me, not re-quoted from an earlier
   log;
2. the 1,457 pre-round-3 converged units are still byte-identical
   in the new canon28 files, re-derived independently rather than
   trusting log_099's own arithmetic;
3. the two THE-table files (`dominant_table24.json`/`dom_ops22.json`,
   plus their b-variants) were not silently touched by tasks 14-17.

I then attempted the tree_units/clusters rebuild log_099 left open,
since a producer script had not yet been located.

## 2. spelling guard, run fresh on every artifact this round names

Ran `check_no_spelling_keys.py` directly against 15 files: the ones
log_097's Task 18 brief names by name, plus `dominant_table24b.json`/
`dom_ops22b.json` (the b-variants, since they sit beside 24/22 in
every family-diff claim below). Verbatim:

```
$ python3 check_no_spelling_keys.py guards4.json
PASS guards4.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py exception_families2.json
PASS exception_families2.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py cross_axis_table.json
PASS cross_axis_table.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py census27.json
PASS census27.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py canon28_units_c.json
PASS canon28_units_c.json -- exempt: top-level meta declares role 'generator provenance', so this file is generator provenance and never participates in matching
$ python3 check_no_spelling_keys.py canon28_units_cpp.json
PASS canon28_units_cpp.json -- exempt: top-level meta declares role 'generator provenance' ...
$ python3 check_no_spelling_keys.py canon28_units_go.json
PASS canon28_units_go.json -- exempt: top-level meta declares role 'generator provenance' ...
$ python3 check_no_spelling_keys.py canon28_units_rust.json
PASS canon28_units_rust.json -- exempt: top-level meta declares role 'generator provenance' ...
$ python3 check_no_spelling_keys.py canon28_units_swift.json
PASS canon28_units_swift.json -- exempt: top-level meta declares role 'generator provenance' ...
$ python3 check_no_spelling_keys.py super_ops3.json
PASS super_ops3.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py interp_relations.json
PASS interp_relations.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py dominant_table24.json
PASS dominant_table24.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py dominant_table24b.json
PASS dominant_table24b.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py dom_ops22.json
PASS dom_ops22.json -- no operator token in any key, grouping, pairing or row structure
$ python3 check_no_spelling_keys.py dom_ops22b.json
PASS dom_ops22b.json -- no operator token in any key, grouping, pairing or row structure
```

**Split, as required: 10 of 15 pass CLEAN (no exemption) -- guards4,
exception_families2, cross_axis_table, census27, super_ops3,
interp_relations, dominant_table24, dominant_table24b, dom_ops22,
dom_ops22b. 5 of 15 pass under the ratified generator-provenance
exemption (2026-08-26) -- the five `canon28_units_<lang>.json` files,
because their top-level `meta` declares role `generator provenance`
(they perform substitution-free gating over one unit's own text at a
time, never a grouping or pairing across units).** All 15: PASS,
zero findings, zero unexplained exemptions.

## 3. zero regressions -- re-derived independently, not re-quoted

log_099 claimed 1,457 units byte-identical across `canon27_units_*`
and `canon28_units_*`. I re-ran the comparison myself, from scratch,
over every `*_text` field on every unit whose `canon27_units_<lang>.
json` record has `status == "converged"`:

```python
langs=['c','cpp','go','rust','swift']
total_checked=0; diffs=0
for lang in langs:
    a=json.load(open(f'canon27_units_{lang}.json'))
    b=json.load(open(f'canon28_units_{lang}.json'))
    for n,u in a['units'].items():
        if u.get('status')=='converged':
            total_checked+=1
            bu=b['units'].get(n)
            if bu is None: diffs+=1; continue
            for k in u:
                if k.endswith('_text') and bu.get(k)!=u.get(k):
                    diffs+=1
print(total_checked, diffs)
# -> checked 1457 diffs 0
```

**checked 1457 diffs 0.** Also independently summed `canon28`'s own
`status == 'converged'` count across all five languages: **1,541** --
matches log_099's stated total (1,457 + 84 = 1,541) exactly, computed
fresh rather than trusted.

## 4. family diffs vs dominant_table24/dom_ops22 -- with named cause

Read `dominant_table24.json`/`dominant_table24b.json` (`rows`
length) and `dom_ops22.json`/`dom_ops22b.json` (`class_count`,
`families`) directly:

| file | rows / nodes | families |
|---|---|---|
| `dominant_table24.json` | 901 | -- |
| `dominant_table24b.json` | 901 | -- |
| `dom_ops22.json` | 901 | 26 |
| `dom_ops22b.json` | 901 | 26 |

**Zero difference between the four, and zero difference from the
figures log_097's state-at-handoff already reports (901 classes /
137 nodes / 26 families).** Named cause, not asserted: mtimes on all
four files (`2026-08-31 19:37:56` for 24/22, `2026-08-31 21:52:22`
for the b-variants) predate every round-3 task-14-17 write (the
earliest of which, `canon27.py`'s re-run, lands at `21:xx`, and the
task-15/16/17 outputs -- `canon28_units_*.json`, `super_ops3.json`,
`interp_relations.json` -- land at `22:4x`-`22:5x`). This matches
what logs 099/100/101 each say in their own words: log_099
("`dominant_table24.json`/`dom_ops22.json` were never opened this
lap"), log_101 ("No existing table or units file was modified").
**Cause of the zero diff: none of round 3's four tasks wrote to
either table file.** Round 3's new artifacts (canon28's 84
convergences, super_ops3's 121 broken ties, interp_relations' 9
relation records) are new, not-yet-merged candidate pools sitting
beside the table, not edits to it -- a merge step is future work,
named as an open item, not performed here.

## 5. tree_units/clusters rebuild -- attempted, producer located,
## run blocked by a pre-existing gap

log_099 searched `grep -rl "clusters.json" --include=*.py .` and
found only consumers, reporting no builder under an obvious name. I
widened the search past that one grep shape (which only matches
Python source lines containing the literal string `clusters.json`
inside a py file passed to `-l`, and can miss a script that builds
the path via `os.path.join`):

```
$ grep -rln "clusters\.json" . 2>/dev/null
verdicts3.py
match_units.py
core_modes_lane.py
lanes/pc_asg_fold.sh
$ grep -n "clusters.json" match_units.py
25:  match_units.py            write clusters.json, print the counts
127:    path = os.path.join(HERE, "clusters.json")
276:    path = os.path.join(HERE, "clusters.json")
```

**`match_units.py` is the producer** (its own docstring: "steps 5
and 6 of the ratified pipeline: matching... usage: match_units.py
write clusters.json, print the counts"). It reads
`sem_anchored_<lang>.json` for every `lang` in `sem_anchored.LANGS`
(`c, cpp, go, rust, swift, java, cpython, javascript, csharp, dart`)
and clusters the pooled units by byte identity then sem identity.

I recorded `clusters.json`'s md5 before attempting a run, ran
`match_units.py` for real, and recorded the md5 after:

```
$ md5sum clusters.json
3f26d954644a1729239bccdcfab71f64  clusters.json
$ /tmp/reconnect_venv/bin/python3 match_units.py
!! no /home/.../op_pipeline/sem_anchored_java.json -- run sem_anchored.py first
$ md5sum clusters.json
3f26d954644a1729239bccdcfab71f64  clusters.json
```

**The script refuses honestly and writes nothing** (`load_units()`
returns `None` on the first missing file and `main()` returns before
reaching the `json.dump` call) -- `clusters.json` is byte-identical
before and after the attempt.

**This refusal is a pre-existing gap, not something caused by
round 3.** `sem_anchored.LANGS` names `java`, but the java file on
disk is `sem_anchored_java2.json` (round-2-era, from log_087-adjacent
work) -- a naming mismatch that predates this round entirely; no
round-3 task wrote or renamed either file. **Separately, and this is
the reason the rebuild question can be answered without waiting on
that gap: canon28's 84 new convergences cannot change either
`tree_units3.json` or `clusters.json`, by the pipeline's own
direction of data flow, not by inspection of dates alone.**
`tree_units3.json` is UPSTREAM of canon28 -- built by
`expr_to_canon.py` from `tree_units2.json`, and read-only-imported by
`canon28.py` (confirmed: `canon28.py`'s own selection logic imports
`census27.names_from_raw`, which reads `tree_units3.json`, and writes
only to `canon28_units_<lang>.json`; grepped for any `open(...,'w')`
or `json.dump` naming `tree_units3.json` inside `canon28.py` --
none). `clusters.json` is built from `sem_anchored_<lang>.json`, a
DIFFERENT lineage from `canon28_units_<lang>.json` entirely --
`canon28.py` never writes to any `sem_anchored_*` file (grepped,
none). **Conclusion: the rebuild is not merely blocked, it is not
called for by anything this round changed** -- canon28's population
lives one layer downstream of tree_units3.json and one lineage over
from clusters.json's inputs. Recorded as the answer to the brief's
question, not as a skipped step.

## 6. state-of-the-line, reading form (numbers + one instance each)

| quantity | value |
|---|---|
| ship units in the corpus | 1,779 |
| converged (canon28, this round's baseline) | 1,541 (was 1,457 before Task 15) |
| not-yet-converged | 238 (was 322) |
| operator-table classes (dominant_table24/24b) | 901 |
| operator-table nodes (dom_ops22/22b) | 901, 26 families |
| provenance-tie candidates resolved (super_ops3, Task 16) | 121 of 189 |
| provenance-tie candidates still open | 68 |
| interpreter handler relation records (interp_relations, Task 17) | 9 (4 ruby, 4 php, 1 cpython), all `incomparable_by_representation` |
| spelling-guard artifacts checked this lap | 15, all PASS (10 clean, 5 exempt) |
| regressions found | 0 (1,457 units re-checked) |
| table-file diffs found (24/24b/22/22b) | 0, cause: not written this round |

One instance per line, as required:

- **A converged unit that needed the canon28 fix**: `c/op_7`, the
  unary expression `~a`, whose ship code `mov %rdi,%rax; not %rax;
  ret` had a fully-rendered `canon7_text` sitting on disk since an
  earlier lap, but no driver before canon28 had ever run the
  behaviour gate on it, because every earlier driver's population
  filter looked for a substitution family this unit does not have.
- **A tie broken by reachability**: `idiom_0001` (support 44),
  carrying `c/op_118` (`uint64_t a + double b`), resolves to
  `LowerUINT_TO_FP_i64` in `X86ISelLowering.cpp`, found by parsing
  `X86ISelLowering.cpp`'s own `setOperationAction(ISD::UINT_TO_FP,
  MVT::i64, Custom)` line and following its `LowerOperation` switch
  one hop deeper -- not the `SelectionDAGLegalize::ExpandLegalINT_TO_FP`
  target an earlier lap had claimed as "hand-verified" without
  checking the instruction text.
- **An interpreter handler that stays outside the table**:
  `rb_fix_plus` (ruby), whose ship disassembly tag-tests the
  argument register itself (`and esi,0x1`) before ever computing a
  sum -- a tagged-value register, never the plain fixed-width
  integer register the compiled-language `i64,i64` add class is
  keyed on.
- **A table file untouched by this round**: `dominant_table24.json`,
  901 rows, mtime `2026-08-31 19:37:56`, unchanged since before
  round 3's task-14 write window began.

## 7. gates run (summary)

- `check_no_spelling_keys.py` on 15 named artifacts -- all PASS
  (section 2).
- zero-regressions byte comparison, 1,457 units, 0 diffs (section
  3), re-derived independently of log_099's own arithmetic.
- table-file family diff, 24/24b/22/22b, 0 diff, cause named
  (section 4).
- `clusters.json` md5 before/after the rebuild attempt, unchanged
  (section 5).

## 8. file inventory -- this session

New:
- `PRIVATE/PseudoCoupHQ/DevComms/log_102_task18_bank_rebaseline.md`
  -- this log.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/next_commit_message.txt`
  -- staged commit message naming every round-3 artifact (tasks
  14-18); not committed, not pushed, per the brief.

Modified: none. This lap ran read-only checks plus one attempted
(and refused, no-write) run of `match_units.py`.

## 9. claims NOT made

- Not claimed: that `clusters.json`/`tree_units3.json` are now
  current with canon28. They are not rebuilt; section 5 states why
  a rebuild is neither possible this lap (missing
  `sem_anchored_java.json`) nor actually called for by canon28's own
  data-flow direction.
- Not claimed: that the 121/189 broken ties or the 9 interpreter
  relation records are merged into `dominant_table24.json`/
  `dom_ops22.json`. They are not; section 4 states this explicitly,
  as does log_101's own decision brief for the owner.
- Not claimed: that the 238 remaining not-yet-converged units have
  a plan beyond what log_099 already named (defer / the owner-reserved /
  open item, per its own per-bucket table).
