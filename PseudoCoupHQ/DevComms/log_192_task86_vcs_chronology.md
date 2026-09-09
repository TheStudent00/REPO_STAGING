# log 192 — task 86: the chronology IS version control

Date: 2026-09-04. Task 86, the CORRECTION of task 85, which built the
right frame on the wrong scale.

The page changed is the PYTHON route — the one the owner opens:
`Research/op_pipeline/dashboard_ouro.html` + `dashboard_ouro.py`,
rendered by `~/Programming/Ourobrowser`. The JavaScript route is
untouched and its `git diff` is pasted in §8.4.

---

# 1. What was done, in plain words, before any figure

the owner, verbatim:

> rounds? i said vcs chronology. i dont want you to have any say in how
> it updates. do you understand why im doing this? because i cant trust
> you.

and

> plans are now in place to convert this to a general purpose PlanPlan
> dashboard design. so think abstractly.

- **A moment is a commit, and every commit is a moment.** The scale is
  `git log`, unfiltered and ungrouped. `chronology_build.py:163`'s
  `git log --grep=banked -i` and `:155`'s `round\s+(\d+)\s+bank` are
  gone from the page's data path: it no longer reads `chronology.json`
  at all.
- **Nothing curates it.** The moment list is proved equal to
  `git rev-list --reverse HEAD`, commit for commit and in the same
  order, by the lane itself (§3.1). No message is read to decide
  anything. A commit's subject line is drawn as a LABEL and read by no
  ordering, grouping, windowing or selection.
- **What the scale degrades to, said plainly.** Measured, not assumed:
  this repository holds **0 tags, 0 merge commits, 1 root commit, 2
  refs**. Tags and merges therefore offer nothing, and the scale
  degrades to exactly two rows — the commits, and the days their own
  timestamps fall on. The day row **selects nothing**; it moves the
  window of the commit row. No coarser rule was invented to fill the
  gap.
- **No project vocabulary in the mechanism.** `round`, `bank`, `lap`
  appear nowhere in the new code except in the one sentence that names
  the retired defect. The grep is §8.6.
- **Everything task 85 got right was kept**: `frame()` draws the
  chronology before the tab bar, so no pane can be drawn without it;
  one moment in `STATE["moment_key"]` outside every pane; all five panes
  as of it; a pane that cannot recompute there says so and names what it
  would need; the tab bar numbers five. Measured on **205 of 205**
  renders (§4.2).
- **What it costs.** 205 renders over 41 moments peak at **276.4 MB**
  (task 85: 286.1 MB over 200). The real Ourobrowser, driven through 14
  screenshots, 4 window moves and 4 moment changes, peaks at
  **566.4 MB** (task 85: 577.8 MB). Cap 1,500 MB, untouched.
- **Three defects were found by RUNNING it, not by reading**, and all
  three are §5. One of them was mine and structural: with the commit
  cache sitting on each `Moment`, a pass over the whole population held
  **1,970.2 MB**, over this page's own cap.

---

# 2. The mechanism, stated once

## 2.1 The walk

LITERAL, from `Research/op_pipeline/dashboard_ouro.py`:

```python
def history():
    """EVERY COMMIT OF THIS REPOSITORY, earliest first.

    One `git log` process, unfiltered and ungrouped.  There is no
    `--grep`, no `--since`, no message pattern and no selection of any
    kind: which commits exist as moments is a fact of the repository.
```

and the call itself, with nothing else in it:

```python
        proc = subprocess.run(
            ["git", "-C", root, "log",
             "--format=%H" + FIELD_MARK + "%cI" + FIELD_MARK + "%s"
             + RECORD_MARK],
            capture_output=True, text=True)
```

GLOSS: three fields, all of them version control's own — identity,
committer timestamp, subject. No flag filters the walk. `FIELD_MARK` and
`RECORD_MARK` are `\x01` and `\x02`, control characters a subject cannot
contain, so the walk needs no quoting rule and no parser.

## 2.2 What the subject line is allowed to be

LITERAL, from the `Moment` class:

```python
        #: display only.  Never consulted by this module for anything.
        self.subject = None if record is None else record.get("subject")
```

GLOSS: the subject is drawn twice — as a tick's hover title, and in the
detail line under the words *its subject line, drawn as a label and read
by nothing*. It is the same discipline the spelling ban imposes on an
operator token: the token appears once per unit, as a display label on
the member, and nothing keys, groups or compares by it. The test is the
same one: replace every subject with a glyph and the mechanism is
unchanged.

ANALOGY, and it is only an analogy: the subject is a caption under a
photograph in an archive. The archive's order is the negatives' own
numbering; the captions are for the reader. The analogy ends where the
mechanism begins — a caption in a real archive can be re-filed under, and
here `history()` literally never touches `record["subject"]` again.

## 2.3 The two rows, and which of them can select

LITERAL:

```python
def set_window(where):
    """move the window of the commit row -- to the first commit of one
    day, or one windowful back or on.

    THIS SELECTS NOTHING.  The day row and the two shift controls are
    navigation, not curation: they change which stretch of commits the
    bar draws, and the moment the page holds is untouched.  That is what
    keeps every commit equal -- no commit is ever picked out as the one
    that stands for its day, and every commit is reachable, because the
    window can be walked over the whole history.
    """
```

GLOSS: the page has two click entry points into the chronology, and they
are different functions. `ouro_moment(key)` selects; `ouro_window(where)`
does not — it returns `render(STATE["pane"], *STATE["args"])` with
`STATE["moment_key"]` untouched. Proved on the running page: after
clicking the day `2026-08-19` the rig read the selected moment back off
the page and got `now — the working tree on disk` (§7).

## 2.4 The stated ceiling

LITERAL:

```python
#: HOW MANY COMMITS THE BAR DRAWS AT ONCE.  A stated ceiling, printed on
#: the page beside the number it was cut down from -- the CORE's rule
#: for any view over a population too large to draw whole ("A pane over
#: the whole population needs a stated ceiling"; a ceiling that is not
#: printed would be a hidden sample).  Nothing outside the window is
#: removed from the population: every commit is reachable by moving the
#: window, and the window follows whatever moment is selected.
WINDOW_TICKS = 60
```

LITERAL, what that renders as, read back off the running page by the rig:

```
every commit — showing 741 to 800 of 1,347 moments (1,346 commits and
the working tree); the window follows the selection
```

## 2.5 The one place this project's own paths still enter

LITERAL:

```python
#: THE ONE PLACE THIS PROJECT'S OWN PATHS ENTER THE MOMENT MACHINERY,
#: and it is caller configuration rather than mechanism.  The
#: chronology knows no paths at all -- it is `git log`.  `Moment.tree()`
#: lists only these prefixes so that listing a commit's tree costs what
#: the panes actually read; point them elsewhere and the same moment
#: machinery serves a repository that has never heard of this research.
ARTIFACT_ROOTS = [OP_DIR, CG_DIR]
```

GLOSS: task 85 had `"Research/"` written into the `git ls-tree` call
itself. For a dashboard that is becoming general-purpose that is a
defect, so the prefix list is now named, documented as the caller's, and
passed after `--`. What remains project-specific is which FILES the five
panes read — which is the panes' business, not the chronology's.

---

# 3. The evidence that nothing curates the moments

## 3.1 The moment list IS `git rev-list`

This is the claim most easily faked, so it is checked mechanically
rather than asserted. LITERAL, from lane `t86_l3_sample2.sh`'s own
output:

```
    every commit of git rev-list is a moment       PASS  1324 moments, 1324 commits from git rev-list, identical order: True
    the moments are the commits plus the working tree PASS  1325 moments = 1324 commits + 1 (now)
    no moment is selected by its message           PASS  nothing in dashboard_ouro reads a message: the walk is `git log --format=%H..%cI..%s` with no --grep and no filter
```

GLOSS: the lane runs `git rev-list --reverse HEAD` itself and compares
the list to `dashboard_ouro.history()` element by element. Evidence
class: **forced by construction** — a curated list cannot equal the
uncurated one.

## 3.2 The chronology is drawn at EVERY moment, not only at sampled ones

LITERAL, same lane:

```
[2/3] the chronology bar at EVERY moment -- 1325 of them
    the bar is drawn at every moment of the population PASS  1325 moments, 0 faults; 22.1 s for all of them
    one moment's work only -- the open slot holds at most one PASS  after walking every moment the open slot holds 'now'
```

Population: **1,325 moments — 1,324 commits and the working tree** — the
whole population, not a sample.

## 3.3 The count moves while you look at it, and that is correct

The repository's own daemon commits every 30 s (`repo-daemon`), so the
population grows during a session. Every count in this log therefore
carries the moment it was taken:

| when | commits | source |
|---|---|---|
| the brief | 1,309 | the owner, 2026-09-04 |
| lane 1, 21:56 UTC | 1,311 | `t86_vcs_scale.json` |
| lane 2, 22:03 UTC | 1,320 | `t86_sample.json` |
| lane 3, 22:05 UTC | 1,324 | `t86_sample2.json` |
| lane 4, 22:06 UTC | 1,325 | `t86_all_panes.json` |
| lane 7, 22:19 UTC | 1,349 | `t86_all_panes2.json` |
| the screenshots, 22:26 UTC | 1,346 | read off the rendered page |

GLOSS: the differences are not drift in the measurement; they are the
repository committing this task's own edits. That is the mechanism
working — the chronology has no build step to fall out of step with, and
it is a general dashboard's correct behaviour. It is also the one thing
in this design that is now visibly LIVE: reopen the page and the
chronology is longer.

---

# 4. Every count, with its population

## 4.1 What marks version control actually carries here

Lane `t86_l1_vcs_scale.sh`, product
`Research/op_pipeline/t86_vcs_scale.json`. Population: every commit
reachable from HEAD, at 21:56 UTC.

LITERAL, the lane's own output with the command above each figure:

```
-- git rev-list --count HEAD
1311
-- git rev-list --count --all
1311
-- git tag | wc -l
0
-- git rev-list --count --merges HEAD
0
-- git for-each-ref --format='%(refname)' | wc -l
2
```

| mark | count | what a coarser scale could do with it |
|---|---|---|
| commits (HEAD) | **1,311** | the fine row: every one of them is a moment |
| commits (all refs) | 1,311 | nothing outside HEAD exists |
| tags | **0** | nothing |
| merge commits | **0** | nothing |
| root commits | 1 | the history is one line |
| refs | 2 (`refs/heads/master`, `refs/remotes/origin/master`) | nothing |
| distinct committer days | **31** | the coarse row |
| commits per day | min 1, median 3, **max 521** | why one day is not one windowful |

GLOSS, and this is the answer to the brief's second question: **the
scale degrades to the commits and their days, and nothing else, because
there is nothing else.** No tag, no merge, no second branch. The day is
admissible because it is the commit's own timestamp truncated — a fact
version control carries — and it is drawn as navigation only, so it
curates nothing. The page says this itself, at every moment:

```
the marks version control carries here: 1,346 commits, 0 tags, 0 merge
commits, 2 refs, 31 days. a coarser scale can only be built from these;
with no tags and no merges it degrades to the commits and their days.
```

## 4.2 The full pass — five panes at a mechanically spaced sample

Lane `t86_l7_all_panes2.sh`, the run of record against the final code.
Product: `Research/op_pipeline/t86_all_panes2.json`. Population: **205
renders — 5 panes × 41 moments** (40 positions spaced every
`(commits-1)/39`-th of the history, plus the working tree), drawn from a
population of 1,350 moments.

The sample rule is over POSITIONS, not content: nothing about a commit's
message makes it more or less likely to be sampled.

LITERAL, the lane's closing lines:

```
renders            205
errors             0
chronology drawn   205 of 205
above the tab bar  205 of 205
tab bar of five    205 of 205
pane 1             recomputed at 18 of 41 moments, refused at 23
pane 2             recomputed at 18 of 41 moments, refused at 23
pane 3             recomputed at 18 of 41 moments, refused at 23
pane 4             recomputed at 12 of 41 moments, refused at 29
pane 5             recomputed at 37 of 41 moments, refused at 4
PEAK RESIDENT      276.4 MB (cap 1500 MB)
```

| pane | recomputed | refused | why |
|---|---|---|---|
| 1 unit viewer | 18 of 41 | 23 | the corpus entered version control on 2026-09-03 |
| 2 selector | 18 of 41 | 23 | the same corpus |
| 3 arch opcode index | 18 of 41 | 23 | the same corpus |
| 4 coverage | 12 of 41 | 29 | only `graph_rust.json`, `coverage_go_summary.json` and `coverage_go_files.json` were ever tracked |
| 5 stats | 37 of 41 | 4 | the census entered 2026-08-31, the pool 2026-09-02 |

GLOSS, and it matters: these are **better** than task 85's 5/40, 3/40
and 14/40, and that is NOT an improvement in the page. It is a different
population. Task 85 sampled 39 curated steps spread evenly over five
weeks; task 86 samples the commits, and 946 of the repository's 1,311
commits were made on 2026-09-02, -03 and -04. An even sample of
positions therefore lands mostly in the recent, well-tracked days. The
refusal rule is unchanged and refuses for exactly the same reasons.

## 4.3 One moment, more than one pane

LITERAL, the same lane's own block:

```
-- one moment change, more than one pane different
   one click from now to d9ec4db3bf45 (2026-09-04 18:08): panes changed = [1, 2, 3, 4, 5]
```

GLOSS: five panes are rendered at `now`, ONE moment is selected, the same
five are rendered again, and all five differ. The moment is held outside
the panes, so a pane cannot fail to follow it.

Photographed as well as measured: `tab1_unitviewer_now.png` against
`tab1_unitviewer_at_2026_09_03_0318.png`, and `tab5_stats_now.png`
against `tab5_stats_at_2026_09_03_0318.png` — one moment change, two
different tabs, both different.

## 4.4 The memory bound

Stated before the full pass, sampled first, then measured — and the
sample is what caught the defect.

| what | renders | peak resident | against |
|---|---|---|---|
| the `git log` walk alone (lane 1) | — | **16.5 MB** | 1,311 commits, 265,611 bytes of output, 0.012 s |
| the bar at every moment, cache on each `Moment` (lane 2) | 1,321 bars | **1,970.2 MB** | **OVER the 1,500 MB cap** — §5.1 |
| the bar at every moment, one open slot (lane 3) | 1,325 bars | **30.7 MB** | the same work, 64× less |
| the sample, 10 renders (lane 3) | 10 | **174.3 MB** | cap 1,500 MB |
| the full pass (lane 7) | 205 | **276.4 MB** | task 85's 286.1 MB over 200 renders |
| the real Ourobrowser (`t86_ouro_shots.py`) | 14 shots, 4 moment changes, 4 window moves | **566.4 MB** | task 85's 577.8 MB; cap 1,500 MB |

Both figures BEAT task 85's, and the abort `OURO_MEMORY_ABORT` and the
cap `MEMORY_CAP_MB` 1500 are unchanged. No abort fired.

---

# 5. The three defects, found by running, with the values in motion

## 5.1 The memory bound was a habit, not a mechanism — 1,970.2 MB

LITERAL, lane 2's output, which is kept on disk as the record:

```
[2/3] the chronology bar at EVERY moment -- 1321 of them
    peak after every bar: 1970.2 MB
...
SAMPLE PEAK RESIDENT: 2045.8 MB (cap 1500 MB)
```

What happened: each `Moment` cached its own `git ls-tree` listing and its
own `git cat-file --batch` process, and the CORE's rule "only one
moment's work is held" was enforced by `set_moment` remembering to call
`close()`. A pass that walked the population without going through
`set_moment` held 1,321 tree listings.

The fix is not discipline. LITERAL:

```python
def open_at(moment):
    """THE ONE OPEN MOMENT, and the memory bound made structural.

    Everything reading a past commit costs memory -- the commit's tree
    listing, and the `git cat-file --batch` process answering for its
    blobs.  None of it is cached on the moment object: it lives in ONE
    slot here, and asking for a different moment evicts the slot first.
```

Same pass afterwards: **30.7 MB**, and the lane checks the slot itself —
`after walking every moment the open slot holds 'now'`.

### 5.1a The three labels, on the same fact

- **LITERAL.** After the change, one pass drawing the chronology bar at
  each of 1,325 moments peaks at 30.7 MB of resident size, measured by
  `resource.getrusage(RUSAGE_SELF).ru_maxrss` in the same process; before
  it, the same pass over 1,321 moments peaked at 1,970.2 MB.
- **GLOSS.** The page could only ever have shown one moment at a time, so
  the old code was not WRONG on the page — it was unbounded in a way the
  page happened not to exercise. A bound that holds because of how the
  caller behaves is not a bound. Now the cache belongs to a single slot
  that evicts, so the same guarantee holds however the module is driven.
- **ANALOGY, and only an analogy.** It is a reading room with one desk
  rather than an honour rule about returning books. The analogy ends
  immediately: a reading room can add desks, and here `open_at` has
  exactly one slot by construction, keyed by the moment.

## 5.2 A tick that is not drawn cannot be pressed

LITERAL, the first screenshot run's output:

```
[rig] click -> MISSING
[rig] read -> 2026-08-19 09:05  4f175cbc00
```

What happened: the rig clicked `ouro_moment('4457428eef88')` directly
after selecting a commit 750 positions earlier. The commit row draws 60
ticks, so that tick was not in the DOM, and — because the rig verifies
by reading the selected moment back off the page — the two screenshots
that followed would have been LABELLED as a moment they were not at.

Two things came of it, and neither is an exemption:

1. The page gained the two window shifts (`◀◀` / `▶▶`) so that every
   commit is reachable in a bounded number of clicks rather than only the
   drawn windowful. Without them, a day carrying 521 commits could not be
   crossed except one `later ▶` at a time.
2. The rig now moves the window by DAY, then shifts it, then selects —
   which is how a person navigates too, and which the second run
   verifies by reading the window line back off the page at each step
   (§7).

## 5.3 A day is not a windowful

LITERAL, the second run's readbacks, in order:

```
[rig] read -> every commit — showing 681 to 740 of 1,347 moments ...
[rig] read -> every commit — showing 741 to 800 of 1,347 moments ...
[rig] read -> 2026-09-03 03:18  4457428eef
```

GLOSS: 2026-09-03 carries 521 commits. Clicking its day mark puts the
window at the day's first commit; reaching 03:18 took one shift. This is
the measured shape of the repository (max 521 commits in a day, median
3) meeting a stated ceiling of 60, and it is why the shifts exist. It is
NOT a reason to sample the day, which would be a curation rule.

---

# 6. What was retired, and why

## 6.1 `chronology.json` is no longer read by this page

`chronology_build.py` and `chronology.json` both **stay on disk as
records**, and `chronology_build.py` now says so in its own first
paragraph. LITERAL, the banner added to it:

```
chronology_build.py -- SUPERSEDED 2026-09-04 BY TASK 86.  Kept on disk
as the record of what it was, and no longer read by the python page.

WHY.  Line 163 below runs `git log --grep=banked -i` and line 155 matches
`round\s+(\d+)\s+bank`, so a step of the chronology existed because a
person had written a word into a commit message.
```

Nothing else in the program was changed. The JavaScript route's
`dashboard_pane6.js` still reads `chronology.json`, and that route was
not touched.

## 6.2 The testimony fallback is retired with the mechanism that fed it

`testimony_for()` drew a count line parsed out of a commit message
wherever an artifact was untracked at that commit. LITERAL, what stands
in its place in `dashboard_ouro.py`:

```python
#: WHAT USED TO BE HERE, AND WHY IT IS GONE.  `testimony_for` drew a
#: count line parsed out of a commit message wherever an artifact was
#: untracked at that commit.  That is a number taken from text a person
#: wrote, which is precisely what the CORE's rule "The chronology is
#: version control, and nothing curates it" retires.  A moment that
#: cannot be recomputed now draws its refusal and names the files it
#: would need -- `refusal` and `gap_line`, which every pane already
#: reaches -- and shows no number at all.  Removed by task 86.
```

This is the one place where the CORE's amended settled rules and an
older sentence in the CORE's `chronology` design block disagree: that
block still says *"the bank message's count line stands in and is
labelled as testimony"*. The settled rule dated 2026-09-04 retires the
mechanism that sentence depends on — a bank message is text a writer
chose — so the rule was implemented and the stale sentence is flagged in
§12 for the owner, not edited by me.

---

# 7. What the page looks like — the fourteen screenshots

`~/Programming/PseudoCoupHQ/DevComms/screens/log_192/`. All 1867×1177,
grabbed out of the real Ourobrowser by `t86_ouro_shots.py`.

| file | what it shows |
|---|---|
| `tab5_stats_now.png` | the chronology above tab 5: the day row (31 days), the commit row (a window of 60 shas), the marks line, the holdings line |
| `tab2_selector_now.png` | the same chronology above tab 2 |
| `tab1_unitviewer_now.png` | the same chronology above tab 1 |
| `day_click_moves_the_window_selects_nothing.png` | after clicking the day `2026-08-19`: the window has moved to `showing 34 to 93`, and the selected moment is still `now — the working tree on disk` |
| `tab1_unitviewer_at_2026_08_19_refused.png` | one moment change: tab 1 refuses, naming the corpus files |
| `tab5_stats_at_2026_08_19_refused.png` | the same moment, tab 5 refuses |
| `tab4_coverage_at_2026_08_19_refused.png` | the same moment, tab 4 refuses, naming `graph_<lang>.json`, `coverage_go_summary.json`, `coverage_go_files.json` |
| `tab4_coverage_at_2026_09_03_0318_refused.png` | a later commit: tab 4 still refuses, and says which files |
| `tab1_unitviewer_at_2026_09_03_0318.png` | the same commit: tab 1 fills in — one moment, two panes different from their `now` versions |
| `tab5_stats_at_2026_09_03_0318.png` | the same commit: tab 5 fills in |
| `tab5_stats_at_2026_09_04_1445.png` | a commit where every pane recomputes |
| `tab4_coverage_at_2026_09_04_1445.png` | the coverage pane at that commit |
| `tab3_opcode_at_2026_09_04_1445.png` | the arch opcode index at that commit — the chronology on a fourth tab |
| `tab3_opcode_back_at_now.png` | back at `now`, read back off the page |

The chronology is photographed on tabs 1, 2, 3, 4 and 5 — the gate asked
for three.

LITERAL, read off the rendered page by the rig rather than off my notes:

```
[rig] read -> now — the working tree on disk
[rig] read -> every commit — showing 34 to 93 of 1,345 moments (1,344 commits and the working tree); the window follows the selection
```

GLOSS: that pair is the day row's whole claim, verified — the window
moved, the moment did not.

---

# 8. The gates

## 8.1 `check_no_spelling_keys.py`, UNMODIFIED, ONE process, five artifacts

Lane `t86_l9_data_guard.sh`. LITERAL, its whole output:

```
the guard, unmodified: sha256 a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7
  grep -c exempt t86_vcs_scale.json: 0
  grep -c exempt t86_sample.json: 0
  grep -c exempt t86_sample2.json: 0
  grep -c exempt t86_all_panes.json: 0
  grep -c exempt t86_all_panes2.json: 0
operator inventory: 91 tokens read from probe_manifest_*.json
PASS t86_vcs_scale.json -- no operator token in any key, grouping, pairing or row structure
PASS t86_sample.json -- no operator token in any key, grouping, pairing or row structure
PASS t86_sample2.json -- no operator token in any key, grouping, pairing or row structure
PASS t86_all_panes.json -- no operator token in any key, grouping, pairing or row structure
PASS t86_all_panes2.json -- no operator token in any key, grouping, pairing or row structure
  exit 0
```

The sha256 `a377462b…` is the same one log_191 §8.1 recorded, and
`git diff b86366cd..HEAD` over the guard is empty (§8.4). `grep -c
exempt` = **0** on every artifact.

## 8.2 `check_dashboard_py_no_spelling.py`

LITERAL, lane `t86_l8_guards_final.sh`:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_ouro.py -- no operator token sits in a key, a subscript, a comparison, a membership test or a lookup (16 mention(s) above)
PASS viewer_build.py -- no operator token sits in a key, a subscript, a comparison, a membership test or a lookup (6 mention(s) above)
  exit 0
```

## 8.3 `check_dashboard_js_no_spelling.py`

LITERAL, the same lane:

```
PASS dashboard_join.js -- no operator token is written as a literal, so none can be a key (3 named coincidences above)
PASS dashboard_loader.js -- no operator token is written as a literal, so none can be a key (3 named coincidences above)
PASS dashboard_pane1.js -- no operator token is written as a literal, so none can be a key (2 named coincidences above)
PASS dashboard_pane23.js -- no operator token is written as a literal, so none can be a key (0 named coincidences above)
PASS dashboard_pane4.js -- no operator token is written as a literal, so none can be a key (4 named coincidences above)
PASS dashboard_pane5.js -- no operator token is written as a literal, so none can be a key (0 named coincidences above)
PASS dashboard_pane6.js -- no operator token is written as a literal, so none can be a key (0 named coincidences above)
  exit 0
```

A first run of this guard (lane `t86_l5_guards.sh`) called it with no
arguments and it answered its own usage text, exit 2. Kept as the record;
lane 6 and lane 8 call it with the file list.

## 8.4 The JavaScript route: `git diff` empty, twice over

The repository's daemon commits every 30 s, so a working-tree diff alone
proves nothing here. Both are pasted. LITERAL, lane 8:

```
-- git diff (working tree), lines:
0
-- git diff b86366cd38c72e557064e44d8d062d83f7610e5d..HEAD, lines (the daemon commits every 30 s, so
   this is the diff that proves it):
0
```

`b86366cd` is the commit that landed task 85 (`task 85: the chronology
becomes the dashboard's OUTER CONTROLLER`, 2026-09-04T17:33:35-04:00), so
that span is exactly task 86. The paths are `dashboard.html` and
`dashboard_pane1.js`, `dashboard_pane23.js`, `dashboard_pane4.js`,
`dashboard_pane5.js`, `dashboard_pane6.js` — and lane 5 listed what the
glob actually matches, so the file list is not a claim:

```
dashboard.html
dashboard_join.js
dashboard_loader.js
dashboard_pane1.js
dashboard_pane23.js
dashboard_pane4.js
dashboard_pane5.js
dashboard_pane6.js
```

## 8.5 `~/Programming/Ourobrowser` untouched

LITERAL, on the host (that repository is not mounted into the sandbox, so
this could not be a lane; §9 names the boundary):

```
$ cd ~/Programming/Ourobrowser
$ git diff | wc -l
0
$ git log --format='%h %cI %s' --since='2026-09-04T17:33:00-04:00' | head
$ git log --format='%H %cI %s' -1
5661ec915153eed9855ae38e3e228fbf6b014a17 2026-09-04T17:20:20-04:00 auto: 41 files (...)
```

GLOSS: no commit in that repository since before task 85 landed, and no
working-tree change. `git status --porcelain` shows one untracked folder,
`Research/Qutebrowser_Fork/`, which is the owner's own rebuild and not this
task's.

## 8.6 The vocabulary grep

LITERAL, lane 8, everything the grep finds:

```
-- grep -nEi 'round|bank|lap' over the changed page, everything:
dashboard_ouro.py:65:`git log --grep=banked -i` and line 155 matched `round\\s+(\\d+)\\s+bank`,
dashboard_ouro.html:12:body{margin:0;background:var(--bg);color:var(--ink);
dashboard_ouro.html:17:.head{padding:10px 16px;border-bottom:1px solid var(--line);background:var(--panel)}
dashboard_ouro.html:20:border-bottom:1px solid var(--line);background:var(--panel)}
dashboard_ouro.html:23:.tab.on{background:var(--accent);color:#fff;border-color:var(--accent)}
dashboard_ouro.html:27:table{border-collapse:collapse;margin:4px 0 10px 0;font-size:13px}
dashboard_ouro.html:30:th{background:var(--code);font-weight:600}
dashboard_ouro.html:31:pre{background:var(--code);border:1px solid var(--line);padding:8px;
dashboard_ouro.html:36:.chip.on{background:var(--accent);color:#fff;border-color:var(--accent)}
dashboard_ouro.html:49:background:var(--panel)}
dashboard_ouro.html:63:background:transparent}
dashboard_ouro.html:68:.tick.on{background:var(--accent);color:#fff;border-color:var(--accent)}
-- the same, minus the CSS property and the sentence that names the
   retired defect:
  (no match)
```

What remains, and why neither is a curation rule:

| what | why it is not a rule |
|---|---|
| `dashboard_ouro.py:65` | one sentence of the module docstring, naming the retired defect verbatim so the history is legible. It is prose. No expression, key, pattern or comparison in the file contains any of the three words |
| `background`, `border-collapse` | CSS property names in the page's stylesheet. `round` is a substring of `background`; the grep is case-insensitive and unanchored, which is why they appear |

The words `round`, `bank` and `lap` appear in **no** identifier, dict
key, regular expression, comparison or git argument anywhere in the new
mechanism.

---

# 9. The fence — where every computation ran

| what | where | why |
|---|---|---|
| the `git log` walk and the mark counts | Airlock lane `t86_l1_vcs_scale.sh` | a git walk is a computation |
| the moment list against `git rev-list`, the bar at every moment, 10 renders | Airlock lanes `t86_l2_sample.sh`, `t86_l3_sample2.sh` | recomputation at a past commit |
| the full pass, 205 renders, twice | Airlock lanes `t86_l4_all_panes.sh`, `t86_l7_all_panes2.sh` | recomputation at a past commit |
| every guard, and the `git diff` over the JavaScript route | Airlock lanes `t86_l5_guards.sh`, `t86_l6_js_guard.sh`, `t86_l8_guards_final.sh`, `t86_l9_data_guard.sh`, `t86_l10_final_check.sh` | a check is a computation |
| rendering the page in Ourobrowser to LOOK at it | the host, `t86_ouro_shots.py` | the browser IS the viewer of the deliverable |
| `git diff` over `~/Programming/Ourobrowser` | the host | that repository is **not mounted** into the sandbox (`Airlock/mounts.conf` carries PseudoCoupHQ, PseudoCoup_v5/v6, Sources and PlanPlan). Named here rather than crossed silently; nothing was installed or built to do it |

Every lane name was used once (`t86_l1` … `t86_l10`). No host venv was
built, nothing was pip-installed, and every import the lanes needed was
already in the image.

---

# 10. Complete file inventory

## 10.1 `~/Programming/PseudoCoupHQ` — edited

| file | the whole of the edit |
|---|---|
| `Research/op_pipeline/dashboard_ouro.py` | the module docstring's chronology section rewritten; `ARTIFACT_ROOTS`; `open_at`/`close_open`; `Moment` (record instead of step, `stamp`, `subject`, no per-moment cache); `Moment.tree` takes the artifact roots after `--`; `history`; `vcs_marks`; `moments`; `moment_at`; `set_moment`; `WINDOW_TICKS`, `window_start`, `set_window`, `WINDOW_BACK`/`WINDOW_ON`; `chronology_bar` rebuilt as two rows; `window_change`; `chronology_doc` and `testimony_for` removed with a note in place of the latter; `count_cell`'s docstring reworded |
| `Research/op_pipeline/dashboard_ouro.html` | one click function `ouro_window`; `.tick.day` and `.tick.page` styling, `.tick` monospaced, `.testimony` → `.subject`; the subtitle states that a moment is a commit |
| `Research/op_pipeline/chronology_build.py` | a SUPERSEDED banner at the top of its docstring. Nothing else; the program still runs and still writes what it wrote |
| `Research/op_pipeline/dashboard_ouro_address.txt` | a paragraph on the new scale |
| `Planning/.../node_0_3_5_10_dashboard/CORE_...md` | realization rows: the task-85 chronology rows marked superseded, three new rows |
| `Planning/.../node_0_3_5_10_dashboard/PROGRESS.md` | the dated entries for this task |

## 10.2 `~/Programming/PseudoCoupHQ` — new

| file | what it is |
|---|---|
| `Research/op_pipeline/t86_l1_vcs_scale.sh` | lane 1: what marks version control carries |
| `Research/op_pipeline/t86_l2_sample.sh` | lane 2: the sample — the run that FOUND the §5.1 defect. Kept as its record |
| `Research/op_pipeline/t86_l3_sample2.sh` | lane 3: the sample after the fix |
| `Research/op_pipeline/t86_l4_all_panes.sh` | lane 4: the first full pass, before the window shifts |
| `Research/op_pipeline/t86_l5_guards.sh` | lane 5: the guards — the run that called the JS guard with no arguments. Kept as its record |
| `Research/op_pipeline/t86_l6_js_guard.sh` | lane 6: the JS guard with its file list |
| `Research/op_pipeline/t86_l7_all_panes2.sh` | lane 7: the full pass of record, against the final code |
| `Research/op_pipeline/t86_l8_guards_final.sh` | lane 8: every gate against the final code |
| `Research/op_pipeline/t86_l9_data_guard.sh` | lane 9: the data guard over all five artifacts in one process |
| `Research/op_pipeline/t86_l10_final_check.sh` | lane 10: every edited python file parses, and the python guard over all three |
| `Research/op_pipeline/t86_ouro_shots.py` | the host rig that drives the real Ourobrowser and photographs it |
| `Research/op_pipeline/t86_vcs_scale.json` | lane 1's product |
| `Research/op_pipeline/t86_sample.json` | lane 2's product, with the 1,970.2 MB peak, kept as the record |
| `Research/op_pipeline/t86_sample2.json` | lane 3's product |
| `Research/op_pipeline/t86_all_panes.json` | lane 4's product |
| `Research/op_pipeline/t86_all_panes2.json` | lane 7's product — **the run of record for every count above** |
| `DevComms/log_192_task86_vcs_chronology.md` | this log |
| `DevComms/screens/log_192/` | fourteen screenshots |

## 10.3 Deliberately not touched

| file | why |
|---|---|
| `Research/op_pipeline/dashboard.html`, `dashboard_join.js`, `dashboard_loader.js`, `dashboard_pane1.js`, `dashboard_pane23.js`, `dashboard_pane4.js`, `dashboard_pane5.js`, `dashboard_pane6.js` | the JavaScript route. `git diff` empty both ways, §8.4 |
| `Research/op_pipeline/chronology.json` | the superseded product, kept as a record; `dashboard_pane6.js` still reads it |
| `Research/op_pipeline/check_no_spelling_keys.py` | the guard, unmodified, sha256 `a377462b…` |
| `~/Programming/Ourobrowser` | the owner's engine; §8.5 |

---

# 11. Decided and recorded for audit

1. **`chronology.json` is not read by the python page; `git log` is read
   directly, at render time.** Decided on the evidence: the whole walk
   costs 0.012 s and 16.5 MB for 1,311 commits, the page already shells
   out to git for `ls-tree` and `cat-file`, and a build step is a place
   for the chronology to fall out of step with the repository. The old
   program and its product stay on disk as records; `chronology_build.py`
   says so in its own first paragraph.
2. **The scale is the commits and their days, and nothing more.** There
   are no tags and no merges to build a coarser scale from, so none was
   invented. The page prints the marks it has at every moment, so the
   degradation is visible rather than asserted.
3. **The day row selects nothing.** It is a separate click function and
   leaves `STATE["moment_key"]` alone, so no commit is ever elevated to
   stand for its day. Verified on the running page by reading the
   selected moment back after a day click.
4. **The window carries a printed ceiling of 60**, beside the population
   it was cut from, and two shift controls so every commit is reachable.
   The ceiling follows the CORE's existing rule for any view over a
   population too large to draw whole.
5. **A commit's subject is drawn as a label and read by nothing.** The
   same discipline the spelling ban imposes on an operator token.
6. **The testimony fallback is removed**, because it took a number from
   text a person wrote. A moment that cannot be recomputed draws its
   refusal and names the files.
7. **The memory bound is structural**, not a caller's discipline:
   `open_at` holds one moment's reads and evicts on any other. Found by
   measuring, at 1,970.2 MB.
8. **`ARTIFACT_ROOTS` names the one place this project's paths enter the
   moment machinery**, so the same mechanism serves a repository that has
   never heard of this research.
9. **Moment keys are commit identities, not positions**, so a stored or
   pasted key keeps meaning the same moment while the repository grows.
10. **Nothing in the JavaScript route was touched**, and the proof is the
    span diff, not the working-tree diff, because the daemon commits
    every 30 s.

---

# 12. Awaiting the owner

1. **One sentence of the CORE's `chronology` design block is now stale.**
   It still says the bank message's count line "stands in and is labelled
   as testimony" where an artifact was untracked. The settled rule dated
   2026-09-04 retires the mechanism that sentence rests on, and the code
   follows the rule. The sentence is the CORE's to cut, not mine.
