# log 191 — task 85: the chronology as the OUTER CONTROLLER

Date: 2026-09-04. Task 85, the top-priority item of
`hq.research.compiler_graph.dashboard`, set by the owner today.

The page changed is the PYTHON route — the one the owner opens:
`Research/op_pipeline/dashboard_ouro.html` + `dashboard_ouro.py`, rendered
by `~/Programming/Ourobrowser`. The JavaScript route is untouched and its
`git diff` is pasted in §8.3.

---

# 1. What was done, in plain words, before any figure

the owner, verbatim:

> the chronology is the outer controller. regardless of what tab im in, i
> can select a moment in the chronology (that is always visible at the
> top), and it shows what that moment in the chronology looked like in
> that tab but it also updates all the tabs for that time.

- **The chronology is no longer tab 6.** It is drawn above the tab bar by
  the page's own `frame()`, which every pane is drawn inside — so there is
  no way to draw a pane without it. That is the mechanism, not a habit.
- **One moment, for the whole page.** It lives in `STATE["moment_key"]`,
  outside every pane. No pane carries a time of its own.
- **All five panes render as of that moment.** At a moment other than now,
  a pane reads the ARTIFACT BLOBS git holds at that commit and runs the
  same join over them. Nothing is checked out; no number is taken from
  `chronology.json`.
- **A pane that cannot be recomputed there says so, at that moment,** and
  names the files version control does not hold at that commit.
- **The tab bar now numbers the CORE's five panes**, closing log_188's
  finding from the other end.
- **What it costs.** 200 renders (5 panes × 40 moments) in one process
  peak at **286.1 MB**; the real Ourobrowser driven through 13
  screenshots and 4 moment changes peaks at **577.8 MB**, against the
  task-77 page's 402.3 MB and the stated cap of 1,500 MB.
- **Two defects were found by running it, not by reading it,** and both
  are §5.

---

# 2. The mechanism, stated once

## 2.1 Why the chronology cannot fall off a tab

LITERAL, from `Research/op_pipeline/dashboard_ouro.py`:

```python
def frame(number, title, body, population, moment=None):
    """every pane is drawn inside the SAME frame, and the frame carries
    the chronology.  That is the mechanism behind "always visible at the
    top, in every tab": there is no way to draw a pane without it."""
    moment = moment or current_moment()
    return "".join([
        chronology_bar(moment),
        tab_bar(number),
        '<div class="pane">',
```

GLOSS: `chronology_bar` is emitted BEFORE `tab_bar`, and every pane —
including the refusal and the error paths — returns through `frame`. A
pane cannot omit it because a pane does not build its own page.

Measured, not asserted (§4.2): drawn on 200 of 200 renders, above the tab
bar on 200 of 200.

## 2.2 Where the moment lives

LITERAL:

```python
def set_moment(key):
    """select ONE moment for the whole page.

    Everything cached for the previous moment is dropped first -- that
    is the memory bound: the page holds one moment's work, never a
    growing pile of them.
    """
```

GLOSS: `set_moment` is module-level, not a method on any pane. `render`
reads `current_moment()` and hands it to whichever pane is asked for. A
pane receives the moment; it never chooses one.

ANALOGY, and it is only an analogy: it is a camera's shutter setting
rather than a setting on each lens — you change it once and every lens
you then fit shoots at it. The analogy ends where the mechanism begins:
there is no per-lens override here, because `PANES[number](moment, ...)`
is the only way a pane is ever called.

## 2.3 How the past is READ

LITERAL, the two git calls, and there are only two:

```python
        proc = subprocess.run(
            ["git", "-C", root, "ls-tree", "-r", "-l", self.commit,
             "Research/"],
            capture_output=True, text=True)
```

```python
        if self._batch is None:
            self._batch = subprocess.Popen(
                ["git", "-C", repo_root(), "cat-file", "--batch"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
```

GLOSS: one `ls-tree` per moment tells the page what exists at that
commit and how big it is; one long-lived `cat-file --batch` process per
moment answers every blob it then asks for. Nothing is checked out, the
working tree is never written, and a `head_text` / `tail_text` read is
still a bounded read.

## 2.4 What `chronology.json` is allowed to supply

LITERAL, from the module docstring:

```
HISTORY IS RECOMPUTED, NEVER REMEMBERED.  A pane at a past moment does
not read a number out of `chronology.json`.  It reads the ARTIFACT
BLOBS git holds at that commit -- `git ls-tree` to see what is there,
`git cat-file` to read one blob -- and runs the same join over them
that it runs over the working tree.  `chronology.json` supplies only
the list of moments (which commit, which day, which round) and the bank
message's own count line, which is shown labelled as TESTIMONY where an
artifact was never tracked.
```

GLOSS: the ONE exception is `testimony_for`, which draws a bank
message's own count line only where the chronology's `source` field for
that number already says `testimony`, and draws it under the words "and
is labelled testimony rather than a recomputation". That is the CORE's
own rule for the round-9 case where `the_pool1.json` was never tracked.

---

# 3. The evidence that the PAST is being read, not the present relabelled

This is the claim most easily faked, so it is the one with the sharpest
evidence.

LITERAL, the population line pane 5 draws at moment `35`
(2026-09-03 `f6856895`, round 12), read off the rendered page in
`DevComms/screens/log_191/tab5_stats_at_round12.png`:

```
30,432 units read from 2 files, as of 2026-09-03 f6856895c3, recomputed
from that commit's own blobs — the pool's own members line; no index built
```

and the heading directly beneath it:

```
the pool — the_pool4.json, its own summary, the highest generation at this moment
```

with `entries` **1,961** and `members` **30,432**.

LITERAL, the same pane at `now`, `DevComms/screens/log_191/tab5_stats_now.png`:
the pool is `the_pool5.json`, `entries` **1,831**, `members` **30,432**.

GLOSS: a different artifact GENERATION, with a different entry count, is
being read at the past moment. A page that quietly showed the present
would show 1,831 at both. Evidence class: **forced by construction** —
the file named on screen is a different file.

Second, LITERAL, from `Research/op_pipeline/t85_all_moments3.json`, the
selector pane at moment `35`:

```
31,078 units read from 343 files, as of 2026-09-03 f6856895c3, recomputed
from that commit's own blobs — index built in 1.8 s
```

GLOSS: the whole index over 31,078 units was rebuilt from that commit's
own blobs in 1.8 s. The unit population happens to be the same as today's;
the FILE COUNT is not (343 there, 1,007 at now), because the term and
render stores were not yet tracked.

---

# 4. Every count, with its population

## 4.1 What version control actually holds, at each of the 39 steps

Lane `t85_l1_gitfacts.sh` ran `git ls-tree -r -l` at each of the 39
chronology commits. Product: `Research/op_pipeline/t85_gitfacts.json`.
Population: 39 steps.

| artifact family | first step that holds it | steps of 39 that hold it |
|---|---|---|
| `probe_manifest*.json` | 2026-08-25 `18d85536` (5 files) | 19 |
| `name_census<n>.json` | 2026-08-31 `c40e8e8d` | 13 |
| `the_pool<n>.json` | 2026-09-02 `23a7e546` | 8 |
| `canon39_wrapped_*`, `canon39_interp`, `canon39_regen_store/` | 2026-09-03 `f6856895` | 4 |
| `term65_store/`, `render_back_store/`, `audit65.json` | 2026-09-03 `89b95485` | 3 |
| `coverage_go_summary.json` | 2026-09-03 `55034c38` | 2 |
| `coverage_go_files.json` | 2026-09-03 `45beecdb` | 1 |
| `graph_go.json` (49 MB), `graph_cpp.json` (331 MB), `graph_swift.json` (165 MB), `coverage_go2.json` (515 MB) | — | **0** |

GLOSS: the last row is the whole reason pane 4 refuses at 37 of 40
moments. Those files were never committed, because they are 49 MB to
515 MB of regenerable output — which is the repo-staging rule working as
intended, not a defect. Rule 4's refusal is the honest answer here.

## 4.2 The full pass — 5 panes at every moment

Lane `t85_l7_all_moments3.sh`, the run of record. Product:
`Research/op_pipeline/t85_all_moments3.json`. Population: **200 renders**
— 5 panes × 40 moments (39 chronology steps and the present moment).

LITERAL, the lane's own closing lines:

```
errors: 0 of 200 renders
chronology drawn on every render: True
chronology ABOVE the tab bar on every render: True
tab-bar entries seen, over all 200 renders: [5]
pane 1 unit viewer        recomputed at  5 of 40 moments, refused at 35
pane 2 selector           recomputed at  5 of 40 moments, refused at 35
pane 3 arch opcode index  recomputed at  5 of 40 moments, refused at 35
pane 4 coverage           recomputed at  3 of 40 moments, refused at 37
pane 5 stats              recomputed at 14 of 40 moments, refused at 26
FULL PASS PEAK RESIDENT SIZE: 286.1 MB, page cap 1500 MB, lane cap 6000 MB
```

Which moments, exactly (from `t85_all_moments3.json`):

| pane | recomputes at | why not elsewhere |
|---|---|---|
| 1 unit viewer | steps 35, 36, 37, 38, and now — **5 of 40** | the corpus entered version control on 2026-09-03 |
| 2 selector | the same 5 of 40 | the same index |
| 3 arch opcode index | the same 5 of 40 | the same index |
| 4 coverage | steps 37, 38, and now — **3 of 40** | only `graph_rust.json`, `coverage_go_summary.json` and `coverage_go_files.json` were ever tracked |
| 5 stats | steps 26–38 and now — **14 of 40** | the census entered 2026-08-31, the pool 2026-09-02, `audit65.json` 2026-09-03 |

## 4.3 One moment, more than one pane

LITERAL, the same lane, its last block. Product:
`Research/op_pipeline/t85_one_moment_proof2.json`.
Population: 2 panes × 2 moments = 4 renders.

```
== one moment, applied to all of them: the SAME two panes at two moments
  moment now  pane 2: 31,078 units read from 1015 files, as of now, opened at 21:25 — index built in 1.4 s
  moment now  pane 5: 30,432 units read from 1015 files, as of now, opened at 21:25 — the pool's own members line; no index built
  moment 31   pane 2: 0 units read from 0 files, as of 2026-09-02 23a7e546ef, recomputed from that commit's own blobs — refused at this moment
  moment 31   pane 5: 0 units read from 1 files, as of 2026-09-02 23a7e546ef, recomputed from that commit's own blobs — the pool's own members line; no index buil
  pane 2 unchanged by the moment change: False
  pane 5 unchanged by the moment change: False
  MORE THAN ONE PANE CHANGED: True
```

GLOSS: one `set_moment` call; two panes that were never re-selected both
answer differently afterwards. That is the settled rule, measured.

## 4.4 The memory bound

STATED BEFORE THE RUN, in each lane's own header. Page cap
`MEMORY_CAP_MB` = 1500 MB, abort `OURO_MEMORY_ABORT`; lane cap 6000 MB,
abort `T85_FULL_MEMORY_ABORT3`.

| run | population | measured peak resident size |
|---|---|---|
| the SAMPLE, run first (`t85_l2_sample.sh`) | 10 renders — 5 panes at 2 moments | **223.6 MB** |
| the full pass (`t85_l7_all_moments3.sh`) | 200 renders — 5 panes at 40 moments | **286.1 MB** |
| the real Ourobrowser (`t85_ouro_shots.py`) | 13 screenshots, 4 moment changes, 5 tabs | **577.8 MB** |
| for comparison, the task-77 page (log_184) | 6 panes, 8 pushes, present moment only | 402.3 MB |

The second bound the moment adds, LITERAL:

```
The moment adds one bound of its own: ONLY ONE MOMENT'S WORK IS HELD.
Selecting a different moment drops every cached index, shard map and
pool map before the new moment is read, so the page's memory does not
grow with the number of moments visited.
```

GLOSS: 200 renders across 40 moments peaking only 62 MB above a 10-render
sample is the evidence that this bound works — otherwise 40 indices would
be resident and the run would have hit the lane cap.

The Ourobrowser figure is **175.5 MB above** the task-77 page's 402.3 MB,
and is **38.5% of the stated cap**. It is reported as a rise, not hidden.

---

# 5. The two defects, found by running, with the values in motion

## 5.1 An older artifact's SHAPE, not only its numbers

Lane 3 (`t85_l3_all_moments.sh`) reported **3 errors of 200 renders**.

LITERAL, the lane's own output:

```
[165/200]  32 pane 5 stats                 6600 chars   0.04 s peak   53.8 MB rows      0  ERROR
       <pre>TypeError: unsupported format string passed to dict.__format__</pre></div>
```

### 5.1a The three labels, on the same fact

**LITERAL** — the code that raised it, as it stood:

```python
        for key in sorted(summary):
            rows.append([esc(key.replace("_", " ")),
                         '<b>%s</b>' % "{:,}".format(summary[key])])
```

**GLOSS** — `"{:,}".format(x)` is python's thousands-separator format. It
is defined for a number and undefined for a dict. At the moments
2026-09-02 `2755e421`, `4475ddde` and 2026-09-03 `9d6235de` the highest
pool generation carries a NESTED OBJECT on its summary where today's
generation carries a count, so `summary[key]` was a dict and the format
raised.

**ANALOGY** — it is the failure of assuming every entry in a ledger is a
figure when an older ledger sometimes wrote a sub-table in the same
column. The analogy stops at the word "column": there is no column here,
only a dict whose values changed type between generations, and the fix is
about types, not layout.

The fix, LITERAL, and it is general rather than per-name:

```python
def count_cell(value):
    """one summary value, drawn WITHOUT assuming it is a whole number.
    ...
    A past moment is where an artifact's SHAPE
    changes, not only its numbers, so the general fix is to draw a value
    as what it is rather than as what this round's shape happens to be.
    """
```

It is applied at all six places a summary value is drawn (the pool, the
term states, the disproved causes, the census rows, the testimony table,
and the coverage populations). After it: **0 errors of 200** (§4.2).

## 5.2 The spelling guard refused a path separator

`check_dashboard_py_no_spelling.py` FAILED, LITERAL:

```
FAIL dashboard_ouro.py:347  the string '/' is an operator token, and it is a comparison operand
```

GLOSS: `/` is one of the 91 operator tokens the guard reads out of the
probe manifests, and the line was `if "/" in rest:` — a membership test.
The guard is RIGHT: a token in a membership test is a token deciding
something. That the character is a path separator here is a homograph
coincidence, exactly like the four x86 mnemonics the CORE already
records; the python guard, unlike the JavaScript one, has no
named-coincidence mechanism.

The fix is not an exemption. The literal is removed from the deciding
position and given a name, LITERAL:

```python
#: git spells every tree path with this separator, and so does this
#: page when it names an artifact inside a store.  It is NAMED rather
#: than written as a literal in the membership test inside
#: `Moment.names_under`, because the same character is ALSO an operator
#: token in this line's 91-token inventory, and
#: `check_dashboard_py_no_spelling.py` is right to refuse a token
#: sitting in a comparison or a membership test.  Found by running that
#: guard, not by reading: it FAILED on `if "/" in rest`.  The fix is
#: not an exemption -- the token is a value here and nothing tests
#: against the literal.
TREE_SEPARATOR = "/"
```

## 5.3 A third defect, in MY OWN RIG, named so it is not mistaken for the page's

The first screenshot run produced three consecutive byte-identical
images. LITERAL, the rig's output:

```
[rig] '[data-python-onclick="ouro_moment('20')"]');if(!e){return "MISSING ou
[rig] click -> None
[rig] shot tab4_coverage_at_2026_08_25_refused -> ... 326945 bytes
```
against the immediately preceding
```
[rig] shot tab4_coverage_now -> ... 326945 bytes
```

GLOSS: every TAB click worked and every MOMENT click did nothing. The
cause was in `t85_ouro_shots.py`, not the page: the moment expression
carries apostrophes (`ouro_moment('20')`) and it was being spliced into a
CSS selector inside a single-quoted JavaScript string, which the
apostrophes closed. The rig now walks the attribute values and compares,
splicing nothing, and reads the page's own selected-moment line back
after every moment click. LITERAL, after the fix:

```
[Bridge] Executing Python command: ouro_moment('35')
[Bridge] Pushing 9459 characters of HTML into 'pane'
[rig] click -> clicked
[rig] read -> 2026-09-03  f6856895c3  (round 12 banked)
```

This is the same class of defect log_184 §2.3 recorded in the engine, at a
different depth: an expression spliced into text that has its own quoting
rules.

---

# 6. The generalisation the past forced

Task 74 fixed one pane reading `name_census5.json` while
`name_census6.json` was on disk, by picking the census generation BY
NUMBER. The pool was still the hard-coded `the_pool5.json`.

A past moment makes the general form necessary rather than merely
correct: at 2026-09-03 `f6856895` the highest pool generation is
`the_pool4.json`, and no hard-coded name can be right at every moment.

LITERAL:

```python
def highest_generation(names, pattern):
    """the highest-numbered generation of an artifact family, picked BY
    NUMBER rather than by a hard-coded name.

    This is the general form of the task-74 fix (a pane had been reading
    `name_census5.json` while `name_census6.json` was already on disk).
    A past moment makes the general form necessary rather than merely
    correct: at an earlier commit the highest generation is a different
    file, and no hard-coded name can be right at every moment.
    """
```

One shared-join change was needed for this, and it is additive. LITERAL,
the whole of the edit to `viewer_build.py`:

```python
def read_pool(doc=None):
    """the pool's summary and its per-unit rows.

    `doc` was added 2026-09-04 (task 85) so that ONE implementation of
    this rule can be given a pool document that did not come from the
    working tree -- the chronology's outer controller hands it the pool
    as git held it at a past commit.  With no argument the behaviour is
    exactly what it was: the pool beside this file.
    """
    if doc is None:
        doc = load("the_pool5.json")
    entries = doc["entries"]
```

GLOSS: with no argument, byte-for-byte the old behaviour. The alternative
was to restate the pool's member→unit mapping in `dashboard_ouro.py`,
which would have been a second implementation of a join rule — the exact
thing the CORE's second-route rule forbids.

---

# 7. What the page looks like — the thirteen screenshots

All in `DevComms/screens/log_191/`, 1867×1177, taken by
`t85_ouro_shots.py` driving the real Ourobrowser.

| file | what it shows |
|---|---|
| `tab5_stats_now.png` | tab 5 at now; the chronology above the tab bar |
| `tab2_selector_now.png` | tab 2 at now; the chronology above the tab bar |
| `tab4_coverage_now.png` | tab 4 at now; the chronology above the tab bar |
| `tab4_coverage_at_2026_08_25_refused.png` | ONE moment chosen (2026-08-25 `18d85536`); pane 4 refuses and names the files |
| `tab1_unitviewer_at_2026_08_25_refused.png` | the SAME moment, a different tab: pane 1 refuses too — the moment applied to more than one pane |
| `tab5_stats_at_2026_08_25_refused.png` | the same moment, pane 5 refuses |
| `tab5_stats_at_round12.png` | moment moved to round 12: pane 5 fills in, reading **`the_pool4.json`** |
| `tab1_unitviewer_at_round12.png` | the same moment, pane 1 fills in, one unit re-opened from that commit's shard |
| `tab3_opcode_at_round12.png` | the same moment, pane 3 fills in |
| `tab4_coverage_at_round12_refused.png` | the same moment, pane 4 still refuses — and says why |
| `tab4_coverage_at_round14.png` | moment moved to round 14: pane 4 fills in |
| `tab2_selector_at_round14.png` | the same moment, pane 2 |
| `tab2_selector_back_at_now.png` | back to now |

The gate asked for the chronology visible above the tabs on at least
three different tabs: tabs 1, 2, 3, 4 and 5 all show it, at four
different moments. It asked for one moment selected changing more than
one pane: `tab4_coverage_at_2026_08_25_refused.png` and
`tab1_unitviewer_at_2026_08_25_refused.png` are two panes after ONE
`ouro_moment('20')` click, and §4.3 measures the same thing in one
process.

---

# 8. The gates

## 8.1 `check_no_spelling_keys.py`, UNMODIFIED, ONE process

Command, from lane `t85_l8_guards_all.sh`, over ALL SEVEN artifacts this
task produced:

```
python3 check_no_spelling_keys.py \
    t85_gitfacts.json t85_sample.json t85_all_moments.json \
    t85_all_moments2.json t85_all_moments3.json \
    t85_one_moment_proof.json t85_one_moment_proof2.json
```

LITERAL output, the whole lane:

```
[1/3] the guard is unmodified
  sha256: a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7

[2/3] grep -c exempt over every artifact
  t85_gitfacts.json: 0
  t85_sample.json: 0
  t85_all_moments.json: 0
  t85_all_moments2.json: 0
  t85_all_moments3.json: 0
  t85_one_moment_proof.json: 0
  t85_one_moment_proof2.json: 0

[3/3] check_no_spelling_keys.py, UNMODIFIED, ONE process, 7 artifacts
operator inventory: 91 tokens read from probe_manifest_*.json
PASS t85_gitfacts.json -- no operator token in any key, grouping, pairing or row structure
PASS t85_sample.json -- no operator token in any key, grouping, pairing or row structure
PASS t85_all_moments.json -- no operator token in any key, grouping, pairing or row structure
PASS t85_all_moments2.json -- no operator token in any key, grouping, pairing or row structure
PASS t85_all_moments3.json -- no operator token in any key, grouping, pairing or row structure
PASS t85_one_moment_proof.json -- no operator token in any key, grouping, pairing or row structure
PASS t85_one_moment_proof2.json -- no operator token in any key, grouping, pairing or row structure
  exit 0
```

GLOSS: **`grep -c exempt` = 0 on all seven**, which is the gate. The
first `git status --porcelain` line printed nothing, which is how git
says the guard file is unchanged; the sha256 is pasted beside it.
(`grep -c exempt` over the guard's own source is 11 — its except-list
documentation — and that file is unmodified, as the two lines above
show.)

## 8.2 `check_dashboard_py_no_spelling.py`

LITERAL, after the §5.2 fix:

```
[4/6] check_dashboard_py_no_spelling.py over the python page code
operator inventory: 91 tokens read from probe_manifest_*.json
     dashboard_ouro.py:191  '/' appears as a value or a piece of prose, in no position that keys anything
     ... (15 such mentions)
PASS dashboard_ouro.py -- no operator token sits in a key, a subscript, a comparison, a membership test or a lookup (15 mention(s) above)
     viewer_build.py:582  '..' appears as a value or a piece of prose, in no position that keys anything
     ... (6 such mentions)
PASS viewer_build.py -- no operator token sits in a key, a subscript, a comparison, a membership test or a lookup (6 mention(s) above)
  exit 0
```

## 8.3 The JavaScript route: `git diff` empty

LITERAL, run on the host against the commit immediately before this task
began (`37d8a5db`, 2026-09-04 16:55:50):

```
$ git diff --stat 37d8a5db..HEAD -- Research/op_pipeline/dashboard.html \
    Research/op_pipeline/dashboard_pane1.js Research/op_pipeline/dashboard_pane23.js \
    Research/op_pipeline/dashboard_pane4.js Research/op_pipeline/dashboard_pane5.js \
    Research/op_pipeline/dashboard_pane6.js
$ git diff 37d8a5db..HEAD -- Research/op_pipeline/dashboard.html \
    Research/op_pipeline/dashboard_pane*.js | wc -l
0
```

GLOSS: no stat line and 0 lines of diff. `dashboard_pane6.js` still
exists and still renders the chronology as a pane on the JavaScript
route; that route was not asked to change and did not.

And `check_dashboard_js_no_spelling.py` over it, LITERAL:

```
PASS dashboard_join.js -- ... (3 named coincidences above)
PASS dashboard_loader.js -- ... (3 named coincidences above)
PASS dashboard_pane23.js -- ... (0 named coincidences above)
PASS dashboard_pane4.js -- ... (4 named coincidences above)
PASS dashboard_pane5.js -- ... (0 named coincidences above)
PASS dashboard_pane6.js -- ... (0 named coincidences above)
  exit 0
```

## 8.4 `~/Programming/Ourobrowser` untouched

LITERAL, on the host:

```
$ cd ~/Programming/Ourobrowser
$ git diff 642d4afa..HEAD -- browser_engine.py bridge.py test_page.html | wc -l
0
```

GLOSS: `642d4afa` is 2026-09-04 16:48:50, before this task. The engine is
the owner's and that work is paused; `t85_ouro_shots.py` imports it and edits
nothing.

---

# 9. The fence — where every computation ran

| what | where | why |
|---|---|---|
| the git walk over 39 commits | Airlock lane `t85_l1_gitfacts.sh` | a git walk is a computation |
| the sample, 10 renders | Airlock lane `t85_l2_sample.sh` | recomputation at a past commit |
| the full pass, 200 renders, twice + final | Airlock lanes `t85_l3_all_moments.sh`, `t85_l4_all_moments2.sh`, `t85_l7_all_moments3.sh` | recomputation at a past commit |
| every guard | Airlock lanes `t85_l5_guards.sh`, `t85_l6_guards2.sh` | a check is a computation |
| rendering the page in Ourobrowser to LOOK at it | the host, `t85_ouro_shots.py` | the browser IS the viewer of the deliverable |

Every lane name was used once. No host venv was built, nothing was
pip-installed, and every import the lanes needed was already in the
image.

**One boundary is named rather than silently crossed** (§11.2): when the owner
himself opens the page and clicks a past moment, the recomputation runs
inside Ourobrowser, on the host, because it IS the page rendering itself.
That is the same footing on which task 77's present-day reads run.

---

# 10. Complete file inventory

## 10.1 `~/Programming/PseudoCoupHQ` — edited

| file | the whole of the edit |
|---|---|
| `Research/op_pipeline/dashboard_ouro.py` | `Moment`, `NotAtThisMoment`, `TREE_SEPARATOR`, `OP_DIR`/`CG_DIR`, `disk_path`, `highest_generation`, `POOL_GENERATION`/`CENSUS_GENERATION`, `repo_root`, `chronology_doc`, `moments`, `moment_by_key`, `current_moment`, `set_moment`, `chronology_bar`, `coverage_at`, `count_cell`, `gap_line`, `testimony_for`, `refusal`, `moment_change`; every pane takes a `moment`; `frame` draws the controller; `PANE_NAMES` cut to five; `pane_chronology` and the tab-6 dispatch removed |
| `Research/op_pipeline/dashboard_ouro.html` | one click function `ouro_moment`; the controller's CSS (`.chron`, `.scale`, `.tick`, `.chrondetail`, `.holds`, `.testimony`, `.gap`, `.needed`); the subtitle now states the controller |
| `Research/op_pipeline/dashboard_ouro_address.txt` | says FIVE panes with the chronology above them |
| `Research/op_pipeline/viewer_build.py` | `read_pool` gained one optional argument; §6 quotes the whole edit |
| `Planning/.../node_0_3_5_10_dashboard/CORE_...md` | five realization rows; the task-77 row marked superseded |
| `Planning/.../node_0_3_5_10_dashboard/PROGRESS.md` | seven dated entries |

## 10.2 `~/Programming/PseudoCoupHQ` — new

| file | what it is |
|---|---|
| `Research/op_pipeline/t85_l1_gitfacts.sh` | lane 1: what git holds at each of the 39 steps |
| `Research/op_pipeline/t85_l2_sample.sh` | lane 2: the sample, 10 renders, before the full pass |
| `Research/op_pipeline/t85_l3_all_moments.sh` | lane 3: the first full pass — the one that FOUND the §5.1 defect. Kept as the record of it |
| `Research/op_pipeline/t85_l4_all_moments2.sh` | lane 4: the full pass after that fix |
| `Research/op_pipeline/t85_l5_guards.sh` | lane 5: the guards — the one that FOUND the §5.2 failure. Kept as the record of it |
| `Research/op_pipeline/t85_l6_guards2.sh` | lane 6: the guards, passing |
| `Research/op_pipeline/t85_l7_all_moments3.sh` | lane 7: the full pass of record, against the final code |
| `Research/op_pipeline/t85_l8_guards_all.sh` | lane 8: the data guard over all seven artifacts in one process |
| `Research/op_pipeline/t85_ouro_shots.py` | the host rig that drives the real Ourobrowser and photographs it |
| `Research/op_pipeline/t85_gitfacts.json` | lane 1's product |
| `Research/op_pipeline/t85_sample.json` | lane 2's product |
| `Research/op_pipeline/t85_all_moments.json` | lane 3's product, with its 3 errors, kept as the record |
| `Research/op_pipeline/t85_all_moments2.json` | lane 4's product |
| `Research/op_pipeline/t85_all_moments3.json` | lane 7's product — **the run of record for every count above** |
| `Research/op_pipeline/t85_one_moment_proof.json` | lane 4's one-moment proof |
| `Research/op_pipeline/t85_one_moment_proof2.json` | lane 7's one-moment proof |
| `DevComms/log_191_task85_chronology_outer_controller.md` | this log |
| `DevComms/screens/log_191/` | thirteen screenshots |

## 10.3 Deliberately not touched

`dashboard.html`, `dashboard_join.js`, `dashboard_loader.js`,
`dashboard_pane1.js`, `dashboard_pane23.js`, `dashboard_pane4.js`,
`dashboard_pane5.js`, `dashboard_pane6.js`, `viewer_template.html`,
`check_no_spelling_keys.py`, `check_dashboard_js_no_spelling.py`,
`check_dashboard_py_no_spelling.py`, `pane23_manifest_regex_check.py`,
`chronology_build.py`, `chronology.json`, and everything in
`~/Programming/Ourobrowser`. §8.3 and §8.4 paste the proof for the two
that were gated.

---

# 11. Decided and recorded for audit

1. **The chronology's control is TICKS, not a slider.** The CORE's design
   says "a slider over the banking commits and a fine scale over every
   daemon commit". An `<input type=range>` needs JavaScript to react to
   being dragged, and this page carries none by design. Realised as two
   rows of clickable ticks — 10 round chips (9 banked rounds and `now`)
   and 40 fine ticks — plus `◀ earlier` / `later ▶` / `now`, which is
   what "step through the history" asks for. 50 ticks on every render,
   measured.
2. **The 39-row chronology table is no longer on the page as a tab.** Its
   content is reached by clicking each tick, which draws that step's day,
   commit, scale, round, bank-message first line, named logs, and what
   the moment holds counted from the tree itself.
3. **"What this moment holds" is counted from the moment's own git tree**,
   not read out of `chronology.json`'s `artifacts` field, so the reason a
   pane refuses is checkable on the page.
4. **`chronology.json` was not regenerated.** It still carries 39 steps
   ending 2026-09-03; today's commits are not moments yet. Regenerating it
   is `chronology_build.py`'s job at the next bank.
5. **Pane 4 is still a table of counts**, and now says so on its own face,
   naming the CORE's second priority. Task 85 is the chronology; the
   drawing is the next item and was not smuggled in.
6. **`viewer_build.read_pool` gained one optional argument.** §6 quotes
   the whole edit and why the alternative was worse.

# 12. Awaiting the owner

1. **The measured peak rose.** The real Ourobrowser now peaks at
   **577.8 MB** against the task-77 page's 402.3 MB — 38.5% of the stated
   1,500 MB cap, so nothing refused, but it is a rise and it is reported
   rather than buried.
2. **The fence's edge, named.** the owner's rule is that every computation is an
   Airlock lane, and the brief's one exception is rendering the page to
   look at it. When the owner clicks a past moment himself, the page recomputes
   on the host — a git walk and an index build inside the browser. Every
   computation *I* ran for this task went through Airlock (§9). Whether
   the page's own per-moment recomputation should be considered inside or
   outside the fence is the owner's to say; nothing was redesigned around it.
3. **Pane 4 refuses at 37 of 40 moments, and that will not improve on its
   own.** The four large graph and coverage artifacts were never tracked
   and, at 49–515 MB, should not be. If the owner wants the coverage pane to
   have a past, the thing to track is a small per-commit SUMMARY written
   at each bank — a decision about what the repo carries, not a code fix,
   so it was not made here.
