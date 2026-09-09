# log 180 — task 76: pane 6, the chronology, and the first statement of this line's progress read off the version control history

Node: `hq.research.compiler_graph.dashboard`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md`),
the `chronology` method. Brief: log_172 task 76. Date: 2026-09-03.

the owner, 2026-09-03: "i would like the dashboard to also have a chronology based
on vcs so i can step through the history to see progress."

---

# 1. What now exists, at the top resolution

## 1.1 The three things delivered

- **`Research/op_pipeline/chronology_build.py`** (27,300 bytes) walks the
  repository's own history at two scales and, at each step, asks git for the
  stat artifacts THAT COMMIT holds and recomputes the stats pane's numbers
  from them. It never copies a number out of a log.
- **`Research/op_pipeline/chronology.json`** (56,904 bytes, tracked) is what
  it writes: **38 steps**, one record each, carrying the commit, the date,
  the round, the numbers, a `source` field PER NUMBER, the artifacts read,
  that round's logs and the bank message as committed.
- **`Research/op_pipeline/dashboard_pane6.js`** (15,907 bytes) is pane 6: a
  slider over the rounds with a day strip under it, the stats table as it
  stood at the chosen step, the change from the step before, that round's
  logs, and a population line naming the commit hash and the date.

## 1.2 The population, stated once

- **38 steps.** 8 of them are ROUND steps (a commit whose message says a
  round was banked); 30 are DAY steps (the last commit of each day since
  2026-07-31).
- **12 steps carry at least one recomputed number.** 1 step carries a
  testimony number (round 9). 25 steps have no stat artifact tracked at that
  commit at all, and say so on the step rather than showing a gap.
- **1,043 commits** in the history at build time; HEAD when the table below
  was printed is named in each step's own row.

## 1.3 The one rule the pane exists to obey

- the owner's standing ruling for this dashboard is "update mechanically" — every
  number is a count over a file. This pane applies that ruling TO THE PAST:
  a number for 2026-09-02 is a count over the file git holds at the
  2026-09-02 commit, computed at build time, not a number remembered from a
  log written that day.
- The one exception is labelled on the page in the row itself:
  **`testimony`** — the artifact was never tracked, so the commit message's
  own count line stands in. It happens once in 38 steps.

---

# 2. The chronology itself, printed whole

This is the deliverable the brief asked for by name: the first time this
line's progress is stated from the version control history rather than from
memory.

- **LITERAL** — standard output of
  `/tmp/reconnect_venv/bin/python3 chronology_build.py --append --print`,
  pasted unedited:

```
round  date       commit      extracted   distinct  dominant proved terms  source
---------------------------------------------------------------------------------
day    2026-07-31 ecca8149d           -          -         -            -  no artifact tracked
day    2026-08-01 0b12c8b53           -          -         -            -  no artifact tracked
day    2026-08-02 1c029184c           -          -         -            -  no artifact tracked
day    2026-08-03 e803c6f2d           -          -         -            -  no artifact tracked
day    2026-08-05 e6ea0d8d0           -          -         -            -  no artifact tracked
day    2026-08-07 da9b9202a           -          -         -            -  no artifact tracked
day    2026-08-08 cd5d808db           -          -         -            -  no artifact tracked
day    2026-08-12 560d6f914           -          -         -            -  no artifact tracked
day    2026-08-13 f39f1c128           -          -         -            -  no artifact tracked
day    2026-08-14 016ea24a6           -          -         -            -  no artifact tracked
day    2026-08-15 e5ffdc290           -          -         -            -  no artifact tracked
day    2026-08-16 13808fc0d           -          -         -            -  no artifact tracked
day    2026-08-17 7adda6d49           -          -         -            -  no artifact tracked
day    2026-08-18 d1265cdf6           -          -         -            -  no artifact tracked
day    2026-08-19 3f469c782           -          -         -            -  no artifact tracked
day    2026-08-20 188ae14e2           -          -         -            -  no artifact tracked
day    2026-08-21 2594321f2           -          -         -            -  no artifact tracked
day    2026-08-22 473f0ff46           -          -         -            -  no artifact tracked
day    2026-08-23 68a915563           -          -         -            -  no artifact tracked
day    2026-08-24 7325275b5           -          -         -            -  no artifact tracked
day    2026-08-25 18d855363           -          -         -            -  no artifact tracked
day    2026-08-26 604da0996           -          -         -            -  no artifact tracked
day    2026-08-27 ed29de10d           -          -         -            -  no artifact tracked
day    2026-08-28 841a0d63e           -          -         -            -  no artifact tracked
day    2026-08-29 3fbdf04b6           -          -         -            -  no artifact tracked
day    2026-08-30 c362c882f           -          -         -            -  no artifact tracked
day    2026-08-31 c40e8e8df           -          -         -            -  recomputed (1 numbers)
4      2026-09-01 a90b33906           -          -         -            -  recomputed (1 numbers)
7      2026-09-01 a68e4a55c           -          -         -            -  recomputed (1 numbers)
day    2026-09-01 4733eb60c           -          -         -            -  recomputed (1 numbers)
8      2026-09-02 33b21b716           -          -         -            -  recomputed (1 numbers)
9      2026-09-02 23a7e546e           -      5,548        31            -  mixed: distinct=testimony, dominant=recomputed
10     2026-09-02 2755e4217      31,078      5,274        35       23,414  recomputed (11 numbers)
day    2026-09-02 4475dddef      31,078      5,274        35       23,135  recomputed (11 numbers)
11     2026-09-03 9d6235de6      31,078      2,247        36       23,132  recomputed (11 numbers)
12     2026-09-03 f6856895c      31,078      1,961        34       26,040  recomputed (11 numbers)
13     2026-09-03 89b95485f      31,078      1,831        34       26,594  recomputed (11 numbers)
day    2026-09-03 55034c38d      31,078      1,831        34       26,594  recomputed (11 numbers)
```

- **GLOSS** — reading the rows that carry numbers, in order:
  - **rounds 4, 7, 8** (2026-09-01 to 2026-09-02): only `name_census.json`
    existed, and it counts 17 unmodelled producers. Nothing else of the
    stats pane was tracked yet.
  - **round 9** (2026-09-02, `23a7e546e`): the pool's own file was never
    tracked (`the_pool1.json`, 18 MB), so its 5,548 entries over 28,984
    members are read off the bank message and marked `testimony`. The
    families file WAS tracked, so 31 families is recomputed. The two sources
    sit side by side in one step — that is why `source` is per number.
  - **round 10** (2026-09-02, `2755e4217`): the first step where the whole
    stats pane can be rebuilt. 31,078 arch-units extracted, 30,436 wrapped
    and proved, 5,274 pool entries, 35 families, 23,414 proved terms.
  - **round 11 → 12 → 13**: the pool contracts, 5,274 → 2,247 → 1,961 →
    1,831 entries, while proved terms climb 23,414 → 23,132 → 26,040 →
    26,594. The pool shrinking IS the progress: fewer distinct computations
    over the same 30,432 members means more of them proved equivalent.
  - the 27 day steps before 2026-08-31 have nothing to recompute, because
    the research artifacts were only committed from 2026-08-25 on.

---

# 3. The recomputation, with values in motion

This section walks one number from a commit hash to a rendered cell, because
the whole claim of the pane is that the number was DERIVED and not
remembered.

## 3.1 The step

`89b95485f7729b6751b3a7afb418e1c15cdcb7a0`, 2026-09-03T14:16:19-04:00 — the
commit whose message says round 13 was banked.

## 3.2 Finding the artifacts, without a hand-written table

The program lists that commit's tree and takes the HIGHEST GENERATION of
each artifact family present. No table of file names is written anywhere in
the program.

- **LITERAL** — `git ls-tree -r 89b9548 -- Research/op_pipeline`, the pool
  and term families filtered:

```
the_pool2.json  the_pool3.json  the_pool4.json  the_pool5.json
term61_store/…  term65_store/…
```

- **GLOSS** — generation 5 is the highest pool present, so `the_pool5.json`
  is round 13's pool; generation 65 is the highest term store, so
  `term65_store/` is round 13's terms. That agrees with what round 13's own
  bank message says it built ("term/pool/census rebuilt as term65/pool5/
  census6") without the program ever reading the message to find out.

## 3.3 One number, all the way through: `proved terms = 26,594`

- The program walks the 332 files of `term65_store/` as git holds them at
  that commit — `git cat-file` on the blob sha the tree names, never the
  working copy.
- Each file's `units` object is one row per unit. Take
  `term65_store/canon39_wrapped_c.json`'s row for `c/op_0`. The fields that
  decide its state are `term_state`, `verdict_ship` and `verdict_source`.
- The partition rule, one row at a time:
  - `term_state` is not `TERM` → **no term**. 419 rows land here.
  - either verdict's `outcome` is `PROVED_EQUAL` → **proved**. 26,594 rows.
  - either verdict's `outcome` is `DISPROVED` → **withdrawn**. 3,134 rows.
  - otherwise → **undecided**. 285 rows.
- 419 + 26,594 + 3,134 + 285 = 30,432, the whole gated population.
- 26,594 is then written into `chronology.json` as
  `numbers.proved_terms` with `source.proved_terms = "recomputed"`, and pane
  6 renders it in the `proved terms` row with a `recomputed` tag beside it.

## 3.4 The check that makes the rule trustworthy: it reproduces testimony it never read

The same partition rule, applied to a DIFFERENT generation of the artifact
(round 11's `layer4c`, where the two routes are spelled `gate_ship_verdict`
and `gate_textorder_verdict` instead), reproduces round 11's bank message
exactly — four numbers, none of them copied.

- **LITERAL** — the round-11 bank message, as committed
  (`9d6235de64d3f60f95abbf3cca58cbe3194825d9`):

```
Layer 4 on that same 30,436: 23,132 proved / 415 withdrawn /
5,602 undecided / 1,287 no-term.
```

- **LITERAL** — the recomputation over `layer4c_terms_*.json` +
  `layer4c_interp.json` + `layer4c_regen_store/*.json`:

```
Counter({'proved': 23132, 'undecided': 5602, 'no term': 1287, 'withdrawn': 415})
```

- **GLOSS** — same four numbers. The rule is not tuned to the round it was
  written against; it is the artifact's own two-route partition, and it
  agrees with a message it does not read. Round 13's 26,594 likewise equals
  `audit65.json`'s `layer5.proved_terms`, which the program also does not
  read.

## 3.5 What the history says that no single bank message said

- Round 12 (`term61_store`) has **0 withdrawn terms and 3,865 undecided**.
  Round 13 (`term65_store`) has **3,134 withdrawn and 285 undecided**.
- The re-gate of task 64 is what moved that population from undecided to
  disproved — `audit65.json`'s `disproved_by_cause` names 2,860 of them as
  the runtime-callee cause.
- This is only visible because two generations were recomputed side by side.
  It is the kind of thing a chronology is for.

---

# 4. The pane, and how it is driven

## 4.1 What is on the screen

- A range slider over all 38 steps, and under it a strip of one button per
  step — the banking steps carry their round number and a filled background,
  the day steps are blank, and a step with nothing to recompute is drawn
  unfilled. Both controls write the same index, so they are one control at
  two resolutions.
- The population line, at the top of the pane, states the commit hash, the
  date, whether a round was banked there, how many numbers the step carries
  and how many of them were recomputed.
- Four cards under it: the stats table with a change column against the
  previous step that had numbers; the per-language split; what was read at
  this commit (family, generation, file count, first file — so the
  recomputation is auditable from the page); this round's logs as links; and
  the bank message as committed.

## 4.2 Screenshots

All under `DevComms/screens/log_180/`, taken headless at 1500×1500 against
the real `chronology.json` and the real artifacts:

| file | what it shows |
|---|---|
| `pane6_round13_recomputed.png` | round 13, every number recomputed, deltas against round 12 (pool entries −130, proved terms +554, withdrawn +3,134) |
| `pane6_round10_first_full_recompute.png` | round 10, the first step where the whole pane rebuilds; the per-language split (cpp 17,840 · c 10,620 · swift 1,322 · rust 695 · go 590 · interpreter 11) and the "what was read" card naming canon37 / the_pool2 / layer4b / name_census3 |
| `pane6_round9_testimony.png` | round 9, the one step with testimony: pool entries and members tagged `testimony`, families and census tagged `recomputed`, with the bank message printed below |
| `pane6_day_with_nothing_to_recompute.png` | a day step before the artifacts were ever committed: the pane says so instead of showing a gap |

## 4.3 How it was driven, and why a rig was needed

- The live page reads the folder through the File System Access API, whose
  folder dialog belongs to the operating system; no automation here can
  click it. Task 68 built `dashboard_test_shim.js` and
  `dashboard_test_server.py` for exactly this.
- A NEW rig file, `dashboard_pane6_harness.html`, loads
  `dashboard_join.js`, `dashboard_loader.js` and `dashboard_pane6.js`
  unchanged against that shim. It is a separate file rather than an edit to
  `dashboard_test_harness.html` because two tasks were editing the dashboard
  at the same time and the rigs must not collide.
- **LITERAL** — the rig's own console line, read out of the browser:

```
[pane6] ready; nav buttons: 6; strip steps: 38
```

- **GLOSS** — six nav buttons means pane 6 attached beside the five that were
  already there; 38 strip steps means every record of `chronology.json`
  reached the control.
- The live page itself (`dashboard.html`, http, so the script tags resolve)
  was loaded and renders its folder gate with no console error, so the added
  script tag breaks nothing before a folder is chosen.

---

# 5. The concurrency rule, and exactly what was touched

Tasks 69, 70 and 76 were editing the dashboard at the same time. The rule
given was: all pane-6 code in a new module; one line in `dashboard.html`;
additive only in `viewer_build.py`.

## 5.1 `dashboard.html` — one line, appended

- **LITERAL** — the diff:

```
 <script src="dashboard_join.js"></script>
 <script src="dashboard_loader.js"></script>
+<script src="dashboard_pane6.js"></script>
```

- The file was re-read immediately before the edit and immediately after;
  task 70 added `dashboard_pane23.js` on the next line during this session
  and both are present. No line was rewritten.

## 5.2 `dashboard_join.js` — NOT TOUCHED

- The module installs itself by wrapping `DashboardJoin.mount`: the original
  mount runs first and draws panes 1–5 exactly as before, then pane 6
  appends one nav button and one `<section>` to the existing `<main>`. Zero
  lines of `dashboard_join.js` were changed, so the byte-for-byte join proof
  of log_176 §2.2 is untouched.

## 5.3 `viewer_build.py` — additive, one block

- Two constants (`PANE6`, `CHRONOLOGY`) and one block that appends
  `window.__CHRONOLOGY__`, the module, and one `attach` call before
  `</body>`. Nothing above it changes; `viewer_template.html` is untouched.
- Task 70's own block (panes 2 and 3, inserted before the snapshot script
  because it wraps `mount` at parse time) and this one coexist in the file
  as written; pane 6 is appended AFTER the snapshot script and calls
  `attach` explicitly, precisely so the two do not contend for the same seam.
- The snapshot build itself is task 74's step to run; the block is written
  and prints its own line when it fires
  (`pane 6 embedded verbatim from dashboard_pane6.js (N bytes) with
  chronology.json (M bytes)`).

---

# 6. `--append`: a step of every bank task from now on

## 6.1 The command, documented in the module header

```
/tmp/reconnect_venv/bin/python3 \
    ~/Programming/PseudoCoupHQ/Research/op_pipeline/chronology_build.py --append
```

Task 74 calls it after the round's artifacts are committed and before the
posterity message is written.

## 6.2 Why idempotence needed thought, with the values

- A DAY step is the LAST commit of its day. While today is still running,
  that commit moves — the repo-daemon commits every 30 s. The first cut
  added a new step for today on every run: 37 steps, then 39, then 41.
- The rule now: a day already carried is REPLACED by its newest last-commit,
  never added beside it. A round step is keyed by its commit and never moves.

## 6.3 The proof, three runs

- **LITERAL** — a full rebuild, then `--append` twice, with the `steps`
  array dumped sorted after each and diffed:

```
wrote …/chronology.json  (38 steps: 12 with a recomputed number, 1 with a testimony number, 25 with no tracked artifact; 56904 bytes)
append: 0 step(s) to build (38 carried forward unchanged)
wrote …/chronology.json  (38 steps: …; 56904 bytes)
append: 0 step(s) to build (38 carried forward unchanged)
wrote …/chronology.json  (38 steps: …; 56904 bytes)
--- diff of the steps array across the three runs ---
run1 vs run2: identical
run2 vs run3: identical
c4fff90079ca15950327e12c9837972b  /tmp/a.json
c4fff90079ca15950327e12c9837972b  /tmp/b.json
c4fff90079ca15950327e12c9837972b  /tmp/c.json
```

- **GLOSS** — three identical md5 sums over the steps array. Only
  `meta.built_at` differs between runs, which is the point of a build stamp.

## 6.4 Cost

The whole 38-step walk takes **2.8 s** wall clock, because steps that name
the same set of blob shas share one cached result — the 30 day steps mostly
reuse what the round steps already computed. `git cat-file --batch` runs as
one long-lived process for the whole build.

---

# 7. The material is thinner than the brief assumed, and that is a finding

The brief said "there are 13 [banking commits], one per round; count them,
pasted". Counted:

- **LITERAL** — `git log --grep=banked -i --oneline | wc -l`:

```
12
```

- **GLOSS**, from `chronology.json`'s own `meta`:
  - **12 commits match**, not 13.
  - **8 distinct rounds are named**: 4, 7, 8, 9, 10, 11, 12, 13.
  - **Rounds 5 and 6 have no banking commit at all.**
  - Two commits carry the same round-4 message and two the same round-10
    message — the repo-daemon committing one file twice. The earliest of
    each pair is the step; the other is recorded, not counted.
  - Two matches name no round and are excluded from the round scale, both
    recorded in `meta.bank_matches_naming_no_round`:
    `a90f8ca` "RETRACTION OF RECORD (main session, 2026-09-01)" and
    `7e8d2a6` (2026-08-24) "compiler_graph: the O0 anchor ruled in; map+
    diary+movement laps banked" — a lap bank, not a round bank.

A second finding, noted rather than fixed because task 74 owns the stats
pane: the live page's stats read `name_census5.json`, but the highest
generation on disk is `name_census6.json` (round 13's, 49 producers against
census5's 52). The chronology takes the highest generation, so pane 6 and
pane 4 will disagree by that one number until pane 4 is moved forward.

---

# 8. THE SPELLING BAN, and the guards run unmodified

> THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
> second violation). No operator token may appear in ANY key, grouping,
> pairing, row structure, candidate selection, or comparison scope, anywhere
> in this line — not in matching, not in "which pairs get compared", not in
> report rows, not in dropdowns. The candidate set for comparison comes from
> machine-form evidence (clusters, connections, type pairs) or from ratified
> intention — never from the token. The token appears exactly once per unit:
> as a display label on the member. HISTORY OF VIOLATIONS, so the pattern is
> visible: (1) the arch campaign's cross-language matrix (caught by the owner
> 2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25 — the
> fix brief itself reintroduced it as "same-operator pairs"). MECHANICAL
> GUARD REQUIRED: every pipeline stage that groups or pairs units must run
> the spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
> its own output on failure. A brief handed to any subagent for this line
> MUST paste this paragraph verbatim.

## 8.1 How this task obeys it

- Nothing here groups, pairs or selects by an operator token. A chronology
  step is keyed by a **commit hash**; a number is keyed by an **artifact
  family** (`corpus`, `terms`, `pool`, `families`, `census`). No operator
  token is read, written or compared anywhere in either file.
- `chronology_build.py` runs the guard over its own output and DELETES the
  file and exits 2 if it fails.
- One violation was caught by the guard and fixed rather than exempted: the
  delta column's rise sign was written as a one-character string literal
  that happens to be an operator token. It is now built from its character
  code, with the reason in a comment. No entry was added to the guard's
  named-coincidence list.

## 8.2 The transcripts, one process each, unmodified guards

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py chronology.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS chronology.json -- no operator token in any key, grouping, pairing or row structure

$ /tmp/reconnect_venv/bin/python3 check_dashboard_js_no_spelling.py dashboard_pane6.js
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_pane6.js -- no operator token is written as a literal, so none can be a key (0 named coincidences above)
```

```
$ grep -c exempt <(check_no_spelling_keys.py chronology.json; check_dashboard_js_no_spelling.py dashboard_pane6.js)
0
```

- **LITERAL** — the three blocks above are the programs' own standard
  output. Neither guard file was modified; `git status` shows neither as
  changed.

---

# 9. Complete file inventory

## 9.1 New files

| path | bytes | what it is |
|---|---|---|
| `Research/op_pipeline/chronology_build.py` | 27,300 | the walker: git log + git cat-file, recompute, `--append` |
| `Research/op_pipeline/chronology.json` | 56,904 | 38 steps, tracked, the pane's whole input |
| `Research/op_pipeline/dashboard_pane6.js` | 15,907 | pane 6, self-installing over `DashboardJoin.mount` |
| `Research/op_pipeline/dashboard_pane6_harness.html` | 2,160 | TEST RIG ONLY, not part of the dashboard |
| `DevComms/screens/log_180/pane6_round13_recomputed.png` | 239,688 | screenshot |
| `DevComms/screens/log_180/pane6_round10_first_full_recompute.png` | 226,896 | screenshot |
| `DevComms/screens/log_180/pane6_round9_testimony.png` | 225,779 | screenshot |
| `DevComms/screens/log_180/pane6_day_with_nothing_to_recompute.png` | 85,740 | screenshot |
| `DevComms/log_180_task76_pane6_chronology.md` | this file | the report |

## 9.2 Edited files, and the whole of each edit

| path | edit |
|---|---|
| `Research/op_pipeline/dashboard.html` | one line appended: `<script src="dashboard_pane6.js"></script>` |
| `Research/op_pipeline/viewer_build.py` | two constants (`PANE6`, `CHRONOLOGY`), one additive embed block before `</body>`, two print lines |
| `…/node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md` | the `chronology` realization row moved from **planned** to **done**, plus one new row recording the chronology's own measured population |
| `…/node_0_3_5_10_dashboard/PROGRESS.md` | six entries at the moment of progress: what landed, the agreement check, the round-12/13 finding, the thinner material, the idempotence proof, the guards |

## 9.3 Not touched, deliberately

`dashboard_join.js`, `dashboard_loader.js`, `viewer_template.html`,
`dashboard_test_harness.html`, `dashboard_test_shim.js`,
`check_no_spelling_keys.py`, `check_dashboard_js_no_spelling.py`.

---

# 10. Decided and recorded for audit / awaiting the owner

## 10.1 Decided, mechanical, recorded here

- Artifacts are discovered per commit by highest generation rather than from
  a hand-written per-round table. It agrees with what the bank messages name
  and keeps working for generations not yet written.
- A day step is the last commit of that day (end-of-day state), and is
  replaced rather than duplicated while the day is still running.
- The testimony parser is a short list of patterns anchored on the words the
  bank messages themselves use, and the whole bank message is stored beside
  the numbers so nothing it read is hidden.
- Round steps that name no round (the retraction, the 2026-08-24 lap bank)
  are excluded from the round scale and recorded in `meta`.

## 10.2 Awaiting the owner

- Nothing. No ontology or naming question arose.
