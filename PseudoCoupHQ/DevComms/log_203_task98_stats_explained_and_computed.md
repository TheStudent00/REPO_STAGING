# log_203 — task 98, round 19: pane 5 explained, and pane 5 computed

**Node:** `hq.research.compiler_graph.dashboard`, sub-node `stats`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md`).

**What the owner asked for, 2026-09-05, verbatim:**

> "in the dashboard stats tab: if you could add a question mark button
> for each row to describe what it means, that would be appreciated"

> "some of the stats can be from a summary ('the pool — the_pool5.json,
> its own summary'). but i want analysis run to produce stats you havent
> curated."

**Where the evidence lives.** Thirteen Airlock lanes, on the default instance,
in the lane-log folder the sandbox itself sees as `/logs` and the host
sees as `PUBLIC/Airlock/agent/logs`. Every attribution below names
its lane log file. The transcripts in §7 are pasted from
`/logs/20260905T140949Z__t98_l9_transcript.sh.log`, which ran each
command from `PseudoCoupHQ` — the same working directory
`check_conventions_log_claims.py --verify` uses, so every one of them
re-runs.

---

## 1. What pane 5 is now

- **Two halves, labelled as two halves on the page**, because the two
  questions are different questions.
    - **`read from a stored summary`** — a figure some earlier run wrote
      into an artifact, read back. This is what the pane was.
    - **`counted at render time`** — the artifacts walked while the page
      is drawn, producing figures nobody selected in advance. This is
      new, and it is what the second request asked for.
- **136 rows, and every one of them carries a `?`.**
    - 36 rows read from a stored summary, in 4 tables.
    - 100 rows counted at render time, in 13 tables.
    - 0 rows drawn as unexplained.
    - Read off the rendered page at its own half marker, not counted by
      hand: lane 10, `/logs/20260905T141101Z__t98_l10_split.sh.log`.

```
$ python3 Research/op_pipeline/t98_render_check.py split
== pane 5's rows, split at the page's own half marker
rows read from a stored summary  36
rows counted at render time      100
rows in total                    136
tables in the stored half        4
tables in the computed half      13
`?` controls, stored half        36
`?` controls, computed half      100
unexplained rows, either half    0
```

---

## 2. Part A — the `?`, and why it cannot drift

- **The explanations are DATA, not prose in the renderer.** They live in
  `Research/op_pipeline/dashboard_stats.py` as `MEANINGS`, one record per
  row key, 46 records today.
- **Every record carries the four things the request asked of an
  explanation**, and the renderer draws them in one fixed order, so a
  part cannot be dropped from one row and kept on another:

    | part | the question it answers |
    |---|---|
    | `counts` | what is being counted, in plain words, defining any term of ours the sentence uses |
    | `population` | counted out of what |
    | `source` | which file, and whether it was `READ FROM A STORED SUMMARY` or `COUNTED AT RENDER TIME` |
    | `caution` | what the row does NOT mean, where it is easy to misread |

- **A row with no record is drawn as UNEXPLAINED, on the page**, naming
  the key that is missing — `explanation_cell` in `dashboard_stats.py`.
  That is the mechanism keeping the rows and the explanations from
  drifting apart: it is not a discipline, it is a visible marker.
    - **It fired, and it was right.** Lane 5
      (`/logs/20260905T135649Z__t98_l5_keys.sh.log`) walked pane 5 at 15
      moments of the repository's history and found **9 unexplained rows
      at two commits of 2026-09-03**, `9b9e7e674c` and `56755e32ca`. The
      pool generation standing at those commits is `the_pool3`, which
      spells the same measurements under different summary names
      (`units_in_the_pool` where `the_pool5` writes `members`, and eight
      more). Nine records were added, each naming
      `build_the_pool3.py` lines 606–634 as where that field is written.
    - After the additions, lane 7
      (`/logs/20260905T140650Z__t98_l7_final.sh.log`): *no row key went
      unexplained at any of the 15 moments walked.*

- **NO JAVASCRIPT, and the rule is not bent.** The `?` is a
  `<details>`/`<summary>` element, which Chromium opens and closes by
  itself. Measured on the rendered page: `occurrences of <script` in what
  pane 5 emits is **0**, and the whole document carries **2** script tags,
  both the engine's own (the QWebChannel handshake and the delegated
  click listener that `browser_engine.setup_script` writes).
- **The `?` was NOT wired through the python bridge**, deliberately: a
  bridge click re-renders the pane, which would re-run both walks to
  open one explanation.

---

## 3. Part B — the analysis that runs, and what it counts

Two walks, both at render time, both over the artifacts as they stand at
the page's one selected moment.

- **Walk one — the canonical-form corpus.** Every per-language file, the
  interpreter file, and every shard of the regenerated store of the
  HIGHEST canon generation present. It answers, in one pass:
    - the corpus per language and per arrival population, with totals;
    - what the gate said about them — every outcome value that occurs,
      and the unproved units per language;
    - the arch-opcode count distribution: its shape per arrival
      population, and then the distribution itself, one row per count
      value that occurs, 0 to 57;
    - how far machine code repeats, corpus-wide and per language;
    - bodies holding no instruction at all;
    - bytes of machine code per body, and ledger rows per unit.
- **Walk two — the layer-4 term store.** Every shard of the highest
  `term<n>_store` generation present. It answers:
    - records per language, and the two term states per language;
    - the store set against the population it was built over;
    - records carrying a runtime-callee row, per language;
    - records carrying a hole, a cascade, or a relink refusal.

**GENERATIONS ARE PICKED BY NUMBER, never by a hard-coded name.**
`canon39` and `canon40` are two generations of one family; `term65_store`
and `term66_store` are two of another. A hard-coded name is right at
exactly one moment, which is the general form of the defect task 74 found
in the census and task 85 found in the pool. `Moment` gained one method
for this, `dirs_under`, the twin of `names_under`, because an artifact
family can be a folder.

**One name stayed hard-coded, and the reason is on the page.**
`audit65.json` is a TASK number, not a generation: `audit61`, `audit64`,
`audit65`, `audit66` and `audit78` audit five different questions, so
"the highest number" is not "the newest generation" and picking by number
would be wrong. The stored audit rows therefore say on their own `?` that
they belong to an earlier round than the term store the computed section
walks, so the two are not read as disagreeing.

---

## 4. THE RECOUNT — where it disagreed with the brief's figures

Every figure the brief carried was recounted. **Three disagreed, and all
three are now explained; none is a defect in the brief's arithmetic.**

| the brief's figure | the recount | verdict |
|---|---|---|
| 31,078 arch-units over 9 languages | 31,078, 9 languages | agrees |
| 754 not proved by canon40; 30,324 proved | 754 / 30,324 | agrees |
| 44 with no layer-4 record; 30,280 in `term66_store` | 44 / 30,280 | agrees, but the WORDS are wrong — see below |
| store per language c 10,347 / cpp 17,545 / swift 1,117 / rust 685 / go 577 / php 4 / java 2 / ruby 2 / cpython 1 | identical, all nine | agrees |
| with-a-term 29,795, no-term 485; c 10,143/204, cpp 17,295/250, go 572/5, rust 679/6, swift 1,097/20 | identical | agrees |
| original corpus 1,779 units, 93 distinct opcodes | 1,779 / 93 | agrees |
| original peaks at 3 (543 units, 30.5%), median 4, max 23 | identical | agrees |
| regenerated 29,288 units, 162 distinct opcodes | 29,288 / 162 | agrees |
| regenerated peaks at 3 (7,796, 26.6%), median 4, max 57 | identical | agrees |
| 31,067 compiled units | 31,067 | agrees |
| **3,547 distinct `body_bytes`, 8.8 units per distinct** | **2,744 corpus-wide, 11.3 per distinct** | **DISAGREES — two different measurements** |
| cpp worst at 12.8x, one body appearing 406 times | cpp 17,840 units / 1,393 distinct = 12.8; cpp's most repeated body 406 | agrees |
| **624 regenerated and 16 original empty bodies** | **canon40: 624 and 16. canon39: 628 and 16** | **AGREES on canon40; the 4 is a generation difference** |
| — (not in the brief) | **2 interpreter units also have empty bodies** | **a row the brief omits** |

### 4.1 The distinct-body disagreement, settled

- **3,547 and 2,744 are both right and they answer different questions.**
    - 2,744 counts a body ONCE for the whole corpus.
    - 3,547 counts it once PER LANGUAGE: 1,282 + 1,393 + 192 + 169 + 511.
    - **642 bodies appear in more than one language**, which is the whole
      of the difference.
    - 8.8 = 31,067 / 3,547. 11.3 = 31,067 / 2,744.
- **The most repeated body corpus-wide appears 561 times**, not 406. Its
  bytes are `89 f8 21 f0 c3`, and it appears in c, cpp, rust and swift.
  406 is cpp's own most repeated, which is what the brief's cpp figure
  measures.
- **The page draws both**, in the same table, with the count of
  cross-language bodies beside them, and the row's `?` says why there are
  two.

### 4.2 The empty-body disagreement, settled

- The brief's 624 is **canon40**. My first recount ran on **canon39**,
  which has 628. The pane walks the highest generation, so it draws 624.
- The brief omits **2 interpreter units** with empty bodies. The pane
  draws all three arrival populations, so they appear.
- `body_bytes empty` is a DIFFERENT absence: 11 units, all interpreter
  handlers, which carry no machine code at all. The row's `?` says so.

### 4.3 "how many arch opcodes its body holds" — the definition, settled

- Three candidate definitions were counted side by side (lane 3,
  `/logs/20260905T134654Z__t98_l3_settle.sh.log`).
- The brief's distribution is **instruction lines in the body, counted
  WITH repeats** — 543 units at 3, median 4, max 23 for the original
  population, matching exactly.
- The brief's "93 / 162 distinct opcodes" is a **different measurement**:
  the vocabulary of instruction spellings over the whole population.
- **Measured: 0 of 31,078 units have a body line that does not read as an
  instruction**, so "lines" and "opcodes" are the same number here. The
  pane's `?` states that, rather than assuming it.

### 4.4 The 44, and what the brief's words get wrong

- The brief says "44 with no layer-4 record". The number is right; the
  description is not.
- Log 202 records what these units are: **their layer-4 term is built and
  PROVED**; it is the LAYER-5 normalization that does not converge —
  measured invariant at 1,536, 4,096 and 18,432 MB. What is missing is
  the comparison key, not the term. Log 202's own line, from lane 12,
  `/logs/20260905T141501Z__t98_l12_log202.sh.log`:

```
$ grep -n "does not converge for 44 of the 30,324" DevComms/log_202_task97_term_pool_canon40.md
1411:1. **§9.1** — `Term.normalize` does not converge for 44 of the 30,324
```

- The row's `?` carries exactly that as its "what it does NOT mean", and
  adds the case a past moment produces: a larger shortfall at an earlier
  commit is a store mid-flight, not a finding.

---

## 5. Memory

- **The cap is unchanged**: `MEMORY_CAP_MB` 1500, abort `OURO_MEMORY_ABORT`.
- **Both walks are bounded structurally**: one document is parsed, reduced
  to counters, and dropped before the next is opened. No unit record and
  no body text is held. What IS held is small and stated: a count per
  (language, arrival population) pair, a count per opcode-count value, and
  one count per distinct body of machine code.
- **Measured, headless** (lane 4,
  `/logs/20260905T135553Z__t98_l4_render.sh.log`; lane 7): one render of
  pane 5 costs **1.02–1.29 s and 41.7–44.2 MB peak resident**. A pass over
  15 moments peaks at **75.8 MB**.
- **Measured, in the real Ourobrowser on the host**, two passes:

    | pass | peak resident, python side | what it drove |
    |---|---|---|
    | task 85 | 577.8 MB | 12 screenshots, 4 moment changes, all panes |
    | task 86 | 566.4 MB | the same shape |
    | **task 98, comparable pass** | **599.2 MB** | 12 screenshots, 4 moment changes, all five panes |
    | task 98, pane 5 only | 412.7 MB | 13 screenshots of pane 5 alone |

- **So the page rose by 32.8 MB against the 566.4 MB it stood at**, 5.8%,
  and stands at 40% of the 1,500 MB cap. The comparable pass is reported
  because a pane-5-only pass is a smaller pass and cannot be set against
  task 86's number.
- The rise is not pane 5's: the shot-by-shot line in the rig's own output
  shows the jump at pane 2 and pane 3, which build the whole-population
  index. Pane 5 alone never took the process past 412.7 MB.
- **No figure needed a stored summary to fit.** The stop rule was not
  reached.

---

## 6. The chronology

- Both walks read through the `moment` object, so both work at a past
  commit through `git ls-tree` and `git cat-file` exactly as the rest of
  the page does.
- **Measured over 15 moments of the repository's own 1,681** (lane 7):
  **10 drew numbers, 5 drew the refusal, 0 errored.** The five refusals
  are all before 2026-09-02, when the corpus entered version control.
- **A part-built store draws its own honest number.** At 2026-09-04
  `c63e1c8e90` the pane draws 133 rows and reports `term66_store, 10
  shards` — the store as version control held it at that moment, not as
  it is now. Screenshot 11.
- The pane refuses as a whole only when NEITHER the stored artifacts nor
  the corpus is tracked; otherwise each half draws what it can and names
  what it cannot, per section.

---

## 7. The gates, each with the command that reproduces it

Everything in this section is pasted from lane 9,
`/logs/20260905T140949Z__t98_l9_transcript.sh.log`. Each command runs from
`PseudoCoupHQ`.

### 7.1 The spelling guard — unmodified, ONE process, every artifact

667 artifacts: the pool, the term audit, the census, every document of
canon40, and every shard of `term66_store`.

```
$ python3 Research/op_pipeline/check_no_spelling_keys.py Research/op_pipeline/the_pool5.json Research/op_pipeline/audit65.json Research/op_pipeline/name_census6.json Research/op_pipeline/canon40_wrapped_*.json Research/op_pipeline/canon40_interp.json Research/op_pipeline/canon40_regen_store/*.json Research/op_pipeline/term66_store/*.json | grep -c "^PASS"
667
```

```
$ python3 Research/op_pipeline/check_no_spelling_keys.py Research/op_pipeline/the_pool5.json Research/op_pipeline/audit65.json Research/op_pipeline/name_census6.json Research/op_pipeline/canon40_wrapped_*.json Research/op_pipeline/canon40_interp.json Research/op_pipeline/canon40_regen_store/*.json Research/op_pipeline/term66_store/*.json | grep -c exempt
0
```

The guard's own file is unchanged:

```
$ git diff --stat -- Research/op_pipeline/check_no_spelling_keys.py Research/op_pipeline/check_dashboard_py_no_spelling.py | wc -l
0
```

### 7.2 The spelling guard over the python page code

```
$ python3 Research/op_pipeline/check_dashboard_py_no_spelling.py Research/op_pipeline/dashboard_ouro.py Research/op_pipeline/dashboard_stats.py | grep "^PASS"
PASS dashboard_ouro.py -- no operator token sits in a key, a subscript, a comparison, a membership test or a lookup (18 mention(s) above)
PASS dashboard_stats.py -- no operator token sits in a key, a subscript, a comparison, a membership test or a lookup (3 mention(s) above)
```

Every mention it lists is a token as a value or as prose in a position
that keys nothing — `/` inside a path, and `?` as the one-character
header of the explanation column. Nothing in either file groups, pairs or
selects a unit by a token: every grouping is by language, by arrival
population, by machine code, or by the outcome the gate recorded, and the
`operator` field is not read at all.

### 7.3 Every row explained, or visibly not

```
$ python3 Research/op_pipeline/t98_render_check.py now | grep -v "wall clock" | grep -v "peak resident" | grep -v "bytes of html"
== pane 5 rendered at the present moment
tables                              17
data rows (every <tr> less headers) 136
`?` controls drawn                  136
rows drawn as UNEXPLAINED           0
occurrences of `<script`            0
explanation records on file         46

explanation records never used by any row drawn now:
```

```
$ python3 Research/op_pipeline/t98_render_check.py keys 14 | grep "no row key"
no row key went unexplained at any of the 15 moments walked
```

### 7.4 This log, put through the claims checker

`check_conventions_log_claims.py --verify` was run over this log inside
Airlock, on the version that stood before this section was added. Its own
`ONE LINE`, read back out of that lane's log:

```
$ grep "^ONE LINE" /logs/20260905T141536Z__t98_l13_claims.sh.log
ONE LINE: 13 of 13 claims reproduce; 0 (0%) carry nothing to re-run
```

Task 96 scored 28 of 35 with 20% carrying nothing to re-run.

### 7.5 The javascript route, untouched

```
$ git diff --stat -- Research/op_pipeline/dashboard.html Research/op_pipeline/dashboard_pane1.js Research/op_pipeline/dashboard_pane23.js Research/op_pipeline/dashboard_pane4.js Research/op_pipeline/dashboard_pane5.js Research/op_pipeline/dashboard_pane6.js Research/op_pipeline/dashboard_join.js Research/op_pipeline/dashboard_loader.js | wc -l
0
```

**`PUBLIC/Ourobrowser`, run on the host on 2026-09-05:**
`git -C PUBLIC/Ourobrowser diff --stat` printed nothing at all —
0 lines. **This claim cannot be re-run by the verifier**, and the cause is
named rather than hidden: `PUBLIC/Ourobrowser` is not a mount
Airlock carries, so no command inside the sandbox can reach it. The
engine was imported by the screenshot rig and never edited.

### 7.6 Every computed figure the pane draws

```
$ python3 Research/op_pipeline/t98_render_check.py figures | grep -v "figures:" | grep -v "peak resident"
== the computed figures, off the same walk the pane runs
canonical-form generation           canon40 over 332 documents
units in the corpus                 31078
languages                           9
units the gate proved               30324
units the gate did not prove        754
-- per language
   c          10620
   cpp        17840
   cpython    1
   go         590
   java       2
   php        4
   ruby       4
   rust       695
   swift      1322
-- per arrival population
   interpreter    11
   original       1779
   regenerated    29288
-- every outcome value
   GATE_DISPROVED                 112
   REFUSED                        642
   WRAPPED_TEXT_PROVED            30324
-- the arch-opcode count distribution, its shape
   interpreter    units 11, distinct opcodes 6, peak 4 (5, 45.5%), median 4, longest 6, empty 2
   original       units 1779, distinct opcodes 93, peak 3 (543, 30.5%), median 4, longest 23, empty 16
   regenerated    units 29288, distinct opcodes 162, peak 3 (7796, 26.6%), median 4, longest 57, empty 624
-- machine code repetition
   units carrying machine code        31067
   distinct bodies, corpus-wide       2744
   distinct bodies, summed per lang   3547
   bodies in more than one language   642
   units per distinct, corpus-wide    11.3
   units per distinct, summed         8.8
   most repeated body                 561 units, bytes 89 f8 21 f0 c3, languages c, cpp, rust, swift
   per language: units / distinct / ratio
     c          10620 / 1282 / 8.3
     cpp        17840 / 1393 / 12.8
     go         590 / 192 / 3.1
     rust       695 / 169 / 4.1
     swift      1322 / 511 / 2.6
-- empty bodies
   interpreter    2
   original       16
   regenerated    624
-- the term store
   store                              term66_store, 332 shards
   records                            30280
   proved units with no record        44
   NO_TERM                            485
   TERM                               29795
   per language: records / by state
     c          10347   (NO_TERM 204, TERM 10143)
     cpp        17545   (NO_TERM 250, TERM 17295)
     cpython    1   (NO_TERM 0, TERM 1)
     go         577   (NO_TERM 5, TERM 572)
     java       2   (NO_TERM 0, TERM 2)
     php        4   (NO_TERM 0, TERM 4)
     ruby       2   (NO_TERM 0, TERM 2)
     rust       685   (NO_TERM 6, TERM 679)
     swift      1117   (NO_TERM 20, TERM 1097)
```

### 7.7 The distinct-body disagreement, both measurements

```
$ python3 Research/op_pipeline/t98_settle.py bodies | grep -v "walk:" | grep -v "peak resident"
== distinct machine code, the two measurements
compiled units (carrying body_bytes)          31067
distinct bodies, COUNTED ONCE for the corpus  2744
distinct bodies, SUMMED per language          3547
bodies appearing in more than one language    642
units per distinct body, corpus-wide          11.3
units per distinct body, summed per language  8.8
the most repeated body appears                561 times
  its bytes                                   89 f8 21 f0 c3
  the languages it appears in                 c, cpp, rust, swift
-- per language: distinct bodies and the most repeated one
  c          1282 distinct
  cpp        1393 distinct
  go         192 distinct
  rust       169 distinct
  swift      511 distinct
```

### 7.8 The opcode-count definition, three candidates side by side

```
$ python3 Research/op_pipeline/t98_settle.py opcodes | grep -v "walk:" | grep -v "peak resident"
== how many arch opcodes a body holds -- the definitions, per arrival population
-- interpreter
   body lines               population 11, peak at 4 (5, 45.5%), median 4, min 0, max 6, zero 2
   lines reading as opcode  population 11, peak at 4 (5, 45.5%), median 4, min 0, max 6, zero 2
   distinct mnemonics       population 11, peak at 3 (7, 63.6%), median 3, min 0, max 4, zero 2
-- original
   body lines               population 1779, peak at 3 (543, 30.5%), median 4, min 0, max 23, zero 16
   lines reading as opcode  population 1779, peak at 3 (543, 30.5%), median 4, min 0, max 23, zero 16
   distinct mnemonics       population 1779, peak at 3 (632, 35.5%), median 3, min 0, max 16, zero 16
-- regenerated
   body lines               population 29288, peak at 3 (7796, 26.6%), median 4, min 0, max 57, zero 628
   lines reading as opcode  population 29288, peak at 3 (7796, 26.6%), median 4, min 0, max 57, zero 628
   distinct mnemonics       population 29288, peak at 3 (9738, 33.2%), median 4, min 0, max 23, zero 628

units where the two line counts differ: 0
```

That block is over **canon39**, which is why its `zero` for the
regenerated population is 628 where canon40 reads 624.

### 7.9 The term store, counted

```
$ python3 Research/op_pipeline/t98_probe_shapes.py terms | grep -v "walk:" | grep -v "peak resident"
== term66_store, 332 shards
records                        30280
-- per language
  c          10347
  cpp        17545
  cpython    1
  go         577
  java       2
  php        4
  ruby       2
  rust       685
  swift      1117
-- every term state value seen
  TERM                 29795
  NO_TERM              485
-- per language and term state
  c          NO_TERM              204
  c          TERM                 10143
  cpp        NO_TERM              250
  cpp        TERM                 17295
  cpython    TERM                 1
  go         NO_TERM              5
  go         TERM                 572
  java       TERM                 2
  php        TERM                 4
  ruby       TERM                 2
  rust       NO_TERM              6
  rust       TERM                 679
  swift      NO_TERM              20
  swift      TERM                 1097
```

---

## 8. The screenshots

`DevComms/screens/log_203/`, taken by
`Research/op_pipeline/t98_ouro_shots.py` driving the real Ourobrowser on
the host. **This claim is not re-runnable inside Airlock**: the rig needs
`PUBLIC/Ourobrowser`, which is not a mount Airlock carries.

| file | what it shows |
|---|---|
| `01_pane5_stats_the_stored_half.png` | the stats tab, first half, a `?` on every row |
| `02_pane5_one_explanation_opened_on_a_stored_row.png` | an explanation open on `members`, all four parts |
| `03_pane5_the_computed_half_corpus_by_language.png` | the corpus counted at render time |
| `04_pane5_the_arch_opcode_count_distribution.png` | the distribution, one row per count value |
| `05_pane5_distinct_machine_code_and_empty_bodies.png` | the repetition table and the empty bodies |
| `06_pane5_the_term_store_counted_here.png` | the term store's states per language |
| `07_pane5_one_explanation_opened_on_a_computed_row.png` | an explanation saying the number was counted, not read |
| `08_pane5_the_explanation_that_says_what_a_row_is_not.png` | the 44, and what it does not mean |
| `09_pane5_at_a_past_commit.png` | the tab at a past commit |
| `10_pane5_at_a_past_commit_the_computed_half.png` | the computed half, recomputed there |
| `11_pane5_at_an_earlier_day_a_part_built_store.png` | 2026-09-04 `c63e1c8e90`, `term66_store, 10 shards` |
| `12_pane5_at_a_moment_it_cannot_be_recomputed.png` | 2026-07-31 `3c8793d95c`, the refusal, naming four files |
| `13_pane5_back_at_now.png` | back at the present moment |
| `w01`–`w12_*.png` | the comparable memory pass: every pane, four moment changes |

**One oddity, reported because it was seen and does not reproduce.** The
first pass of the rig read `opened: 1` on arrival, before the rig had
pressed any `?`. A census step was added at first paint to measure it,
and on two later passes it read `opened: 0` both times. It has not
recurred and no cause was found; it is recorded rather than explained
away.

---

## 9. Every artifact this task touched or made

**Edited (2 files):**

| file | what changed |
|---|---|
| `Research/op_pipeline/dashboard_ouro.py` | `Moment.dirs_under`; `explained_table`, `share_cell`, `WHY_COLUMN`; `pane_stats` rewritten into `stats_stored`, `stats_computed`, `stats_corpus_section`, `stats_opcode_section`, `stats_machine_code_section`, `stats_term_section`; imports `dashboard_stats` |
| `Research/op_pipeline/dashboard_ouro.html` | CSS only, for `details.why`, `.whymark`, `.whybody`, `.unexplained`, `h2.half`, `.halfnote`. No script added; the page still carries no JavaScript of its own |

**New (5 files):**

| file | what it is |
|---|---|
| `Research/op_pipeline/dashboard_stats.py` | `MEANINGS` (46 records), `explanation_cell`, `explained_rows`, `unexplained_keys`, `corpus_analysis`, `term_store_analysis`, `highest_canon`, `highest_term_store`, `spread` |
| `Research/op_pipeline/t98_probe_shapes.py` | the cost of a render-time walk, and the three candidate opcode-count definitions |
| `Research/op_pipeline/t98_settle.py` | the three disagreements with the brief, counted under every candidate definition |
| `Research/op_pipeline/t98_render_check.py` | pane 5 rendered off the page and checked: `now`, `figures`, `past`, `keys`, `split` |
| `Research/op_pipeline/t98_ouro_shots.py` | the screenshot rig, on the host, importing the engine and not editing it |

**Lanes (13), in `Research/op_pipeline/lanes_t98/`, each with its log:**

| lane | log file | what it settled |
|---|---|---|
| `t98_l1_shapes.sh` | `/logs/20260905T134356Z__t98_l1_shapes.sh.log` | failed: `/usr/bin/time` is not in the image |
| `t98_l2_shapes.sh` | `/logs/20260905T134435Z__t98_l2_shapes.sh.log` | the walks cost 1.7 s and 45.0 MB in one process |
| `t98_l3_settle.sh` | `/logs/20260905T134654Z__t98_l3_settle.sh.log` | the three disagreements, counted every way |
| `t98_l4_render.sh` | `/logs/20260905T135553Z__t98_l4_render.sh.log` | 136 rows, 136 `?`, 0 unexplained, 0 `<script`; 15 moments |
| `t98_l5_keys.sh` | `/logs/20260905T135649Z__t98_l5_keys.sh.log` | the 9 unexplained keys, named, at two commits |
| `t98_l6_guards.sh` | `/logs/20260905T135806Z__t98_l6_guards.sh.log` | 667 artifacts PASS, 0 FAIL, `grep -c exempt` 0 |
| `t98_l7_final.sh` | `/logs/20260905T140650Z__t98_l7_final.sh.log` | no key unexplained at any moment walked |
| `t98_l8_transcript.sh` | `/logs/20260905T140854Z__t98_l8_transcript.sh.log` | the first transcript; it carried timing lines |
| `t98_l9_transcript.sh` | `/logs/20260905T140949Z__t98_l9_transcript.sh.log` | the transcript this log pastes |
| `t98_l10_split.sh` | `/logs/20260905T141101Z__t98_l10_split.sh.log` | 36 stored rows, 100 computed, 136 total |
| `t98_l11_claims.sh` | `/logs/20260905T141359Z__t98_l11_claims.sh.log` | `check_conventions_log_claims.py --verify` over this log |
| `t98_l12_log202.sh` | `/logs/20260905T141501Z__t98_l12_log202.sh.log` | the one prose claim given a command |
| `t98_l13_claims.sh` | `/logs/20260905T141536Z__t98_l13_claims.sh.log` | the claims checker again: 13 of 13 reproduce, 0% unverifiable |

**Artifacts READ and not written:** `the_pool5.json`, `audit65.json`,
`name_census6.json`, `name_census7.json`, `canon40_wrapped_{c,cpp,go,rust,swift}.json`,
`canon40_interp.json`, the 326 shards of `canon40_regen_store/`, the 332
shards of `term66_store/`, and — by the settle programs only —
`canon39_wrapped_{c,cpp,go,rust,swift}.json`, `canon39_interp.json` and
the 326 shards of `canon39_regen_store/`. **Nothing in this task wrote an
artifact.**

**One file written by a lane:** `Research/op_pipeline/t98_spelling_guard_transcript.txt`,
the guard's own 668-line transcript from lane 6.

---

## 10. Decided, recorded for audit

1. **The `?` is a `<details>` element, not a bridge click.** A bridge
   click re-renders the pane and would re-run both walks to open one
   explanation. The no-JavaScript rule is kept: the pane emits 0 `<script`.
2. **The explanations are data in `dashboard_stats.MEANINGS`, keyed per
   row**, and a row with no record is drawn as unexplained on the page.
3. **Every computed figure is counted at render time.** No stored summary
   was built for any of them; the stop rule was not reached.
4. **Artifact generations are picked by number** — the canonical form and
   the term store now join the pool and the census in that rule.
   `audit65.json` stays a written name because its number is a task
   number, and the page says so.
5. **Both distinct-body measurements are drawn**, with the count of
   cross-language bodies that separates them, rather than one being
   chosen as the answer.
6. **The empty bodies are surfaced with no cause offered**, because none
   has been established, and the row's `?` says exactly that.
7. **Nine explanation records were added for `the_pool3`'s summary
   names**, so past moments are explained as well as the present one.
8. **`Moment` gained one method**, `dirs_under`, the twin of
   `names_under`.
9. **The javascript route and Ourobrowser are untouched**, 0 lines each.

## 11. Awaiting the owner

1. **The stored half still reads `audit65.json`, which is round 13's
   audit over `term65_store`, while the computed half walks
   `term66_store`.** The `?` on those rows says so, so nothing on the page
   misleads. Whether the stored half should be re-pointed at `audit66.json`
   is a change to what the pane reports, not a mechanism, so it is yours.
2. **The pane is long** — 136 rows and 17 tables, about 5,500 pixels. If
   the computed half should open collapsed, or the distribution table
   should be a drawing rather than 39 rows, say which and it changes.
3. **Whether "every row carries a `?`, and a row without one is drawn as
   unexplained" becomes a settled rule of this node**, applying to panes
   1 to 4 as well as pane 5. The mechanism is general — `explained_table`
   and `MEANINGS` know nothing about stats — so it is a decision about
   scope, not about code, and a settled rule is yours to set. Nothing was
   added to the CORE's settled rules; only its realization table gained a
   row.
