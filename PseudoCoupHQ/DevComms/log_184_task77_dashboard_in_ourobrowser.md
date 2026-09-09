# log 184 — task 77: the dashboard rendered by python, inside Ourobrowser

Date: 2026-09-03. Task 77 of round 15 (`log_183`), the round's headline,
and the one item in that round that is **the owner's own request, verbatim**:

> have a look at `~/Programming/Ourobrowser` because the browser allows
> python to be run locally natively within the browser. id like to see
> the dashboard written to run in it.

Two repos were touched: `~/Programming/Ourobrowser` (the browser gained
the ability for python to put HTML on the page) and
`~/Programming/PseudoCoupHQ` (a second dashboard page that uses it).
Nothing that existed was retired.

---

# 1. What was done, in plain words, before any figure

Ourobrowser is a browser whose scripting language is python. A page's
`<script type="text/python">` block is executed by the browser's own
python at the moment the page is requested, and every ordinary
`<script>` is deleted, so no JavaScript runs at all.

It could not render a page from python. A block's text was replaced by
the empty string, so a block could compute anything and show nothing;
and the bridge that carries a click into python threw the answer away.
That gap is what this task closed.

- **Three additions to the browser, and one repair.** A block may now
  put HTML in its own place (`emit`); a block knows which file it is in
  (`page_path`); python may fill a named element at any later moment
  (`set_html`). The repair: the rewrite that turns `onclick="python:…"`
  into a bridge call emitted a page Chromium refused to run, so **no
  page had ever reached the bridge**. Both defects were found by
  running, not by reading, and both are quoted below with the browser's
  own error text.
- **A second dashboard page, rendered by python.** It has no JavaScript
  in it at all. Python opens the artifacts with `open()`, so the folder
  picker, the remembered-folder handle, the opaque-origin finding of
  log_176 §4 and the Firefox gap of log_176 §5 all simply do not arise.
- **The join is not written a third time.** The python page imports the
  python join `viewer_build.py` already holds and calls its functions.
  Two rules of the join exist ONLY in `dashboard_join.js` and have no
  python twin on disk; those two are ported, and they are labelled as
  ports rather than described as reuse.
- **All six panes render.** Panes 1–6 as the dashboard CORE numbers
  them. Every pane carries its population line.
- **What it costs.** First paint 0.064 s. Peak resident size of the
  whole Ourobrowser process, over all six panes and eight pushes:
  402.3 MB, against a stated cap of 1,500 MB.
- **`test_page.html` still works, and works better.** The two renders
  are byte-identical; its button reaches python for the first time.

---

# 2. The two engine defects, with the values in motion

## 2.1 The wire form: what the browser sends when you click

`test_page.html` carries one button. LITERAL, from
`~/Programming/Ourobrowser/test_page.html`:

```html
<button onclick="python:fetch_system_data()">Fetch System Data (Python)</button>
```

GLOSS: `onclick="python:EXPR"` is Ourobrowser's own spelling. The
browser is meant to strip it out and arrange for `EXPR` to be executed
by python when the button is clicked.

## 2.2 Defect one — the rewrite wrote a page Chromium refused

LITERAL, the replacement template as it stood at commit `a5d8bee`, in
`~/Programming/Ourobrowser/browser_engine.py`:

```python
replacement = r'onclick="if(window.pyBridge) { window.pyBridge.execute_python(\'\1\'); }"'
```

GLOSS: it is a RAW string, so `\'` is a backslash followed by an
apostrophe, and both characters reach the page.

LITERAL, what Chromium was therefore served — produced by running that
same expression over that same file:

```html
<button onclick="if(window.pyBridge) { window.pyBridge.execute_python(\'fetch_system_data()\'); }">Fetch System Data (Python)</button>
```

LITERAL, Chromium's own answer when that button is clicked:

```
js: Uncaught SyntaxError: Failed to execute 'click' on 'HTMLElement': Invalid or unexpected token
```

So the feature the README advertises had never worked from a page.
Evidence class: **forced by construction** — the served text and the
browser's refusal of it.

## 2.3 Defect two — the pattern closed on the wrong quote

Found later, by driving the new dashboard rather than by reading.

LITERAL, the pattern as it stood:

```python
PYTHON_ONCLICK_PATTERN = re.compile(r'\bonclick=["\']python:(.*?)["\']', re.IGNORECASE)
```

GLOSS: the closing delimiter is a character CLASS — either quote
character will do. So it does not have to match the quote that opened
the attribute.

Values in motion, on one real chip of the new pane 3:

```
the page writes      onclick="python:ouro_opcode('arch0000')"
the pattern opens on "  and then closes on the FIRST ' it meets
what it captures     ouro_opcode(
the attribute becomes data-python-onclick="ouro_opcode("
```

LITERAL, the bridge's own message when that chip was clicked:

```
[Bridge] Executing Python command: ouro_opcode(
[Bridge] Error executing python command 'ouro_opcode(': '(' was never closed
```

The fix is a backreference, so the closing quote is the opening one:

```python
PYTHON_ONCLICK_PATTERN = re.compile(r'\bonclick=(["\'])python:(.*?)\1', re.IGNORECASE)
```

LITERAL, the same click after the fix:

```
[Bridge] Executing Python command: ouro_opcode('arch0000')
[Bridge] Pushing 32800 characters of HTML into 'pane'
```

## 2.4 One cause, one fix, in the layer where it lives

Both defects are the same cause at two depths: the click's wire form
was **inline executable text**, and inline executable text has to be
quoted correctly inside an HTML attribute. The fix removes the
requirement rather than satisfying it: the wire form is now an
ATTRIBUTE holding the expression, html-escaped, and the one delegated
click listener that reads it lives in the browser's own setup script.

---

# 3. The three additions, and why they are three and not one

## 3.1 The shape, stated at the top

A python block runs at REQUEST time — before Chromium has been given
any HTML, so there is no element to fill. A click runs AFTER first
paint — by which time the block's text is gone, so there is no block to
fill. The two moments need two different acts, and neither substitutes
for the other.

| working name | what it does | when it can work | where it is defined |
|---|---|---|---|
| `emit` | a block puts HTML in its own place | request time only | `browser_engine.PAGE_EMIT_NAME` |
| `page_path` | a block knows the file it is in | request time | `browser_engine.PAGE_PATH_NAME` |
| `set_html` | python fills a named element | after first paint | `browser_engine.PAGE_PUSH_NAME`, method on `PythonBridge` |

## 3.2 `emit` — a block may put HTML in its own place

LITERAL, from `~/Programming/Ourobrowser/browser_engine.py`:

```python
def execute_and_replace(match):
    code = match.group(1)
    print("[Engine] Executing embedded Python script...")
    emitted = []

    def collect(markup):
        emitted.append(str(markup))

    had_emit = PAGE_EMIT_NAME in self.context
    previous_emit = self.context.get(PAGE_EMIT_NAME)
    self.context[PAGE_EMIT_NAME] = collect
    self.context[PAGE_PATH_NAME] = absolute
    try:
        exec(code, self.context, self.context)
    ...
    return "".join(emitted)
```

GLOSS: whatever the block collected replaces the block. A block that
collects nothing returns the empty string — which is exactly the old
behaviour, and is why `test_page.html` is unaffected.

## 3.3 `page_path` — and why it is not a convenience

The dashboard page lives in `Research/op_pipeline` and the browser is
launched from `~/Programming/Ourobrowser`. Without `page_path` the
page's own text would have to name the folder it lives in — a
machine-specific path inside a tracked file, which this line forbids.

LITERAL, the whole of how the page reaches its renderer, from
`~/Programming/PseudoCoupHQ/Research/op_pipeline/dashboard_ouro.html`:

```python
sys.path.insert(0, os.path.dirname(page_path))
import dashboard_ouro
```

## 3.4 `set_html` — the return path

The bridge could not answer: `execute_python` is a slot whose return
value is discarded. Rather than make it return, the bridge gained a Qt
SIGNAL, because QWebChannel already publishes a registered object's
signals to the page — so the return path needs no new transport and no
page-authored JavaScript.

LITERAL, from `~/Programming/Ourobrowser/bridge.py`:

```python
html_pushed = pyqtSignal(str, str)

def set_html(self, target, html):
    text = self.rewriter(html)
    print(f"[Bridge] Pushing {len(text)} characters of HTML into '{target}'")
    self.html_pushed.emit(str(target), text)
```

- **`rewriter` is INJECTED, not imported.** HTML pushed after first
  paint never passes through the scheme handler, so it would otherwise
  carry `python:` handlers nothing had rewritten. The engine hands the
  bridge its own `rewrite_python_onclick` when it builds it, so there is
  ONE rewrite with two callers and the bridge never imports the engine.
- **The click listener is delegated from `document`**, so an element
  that arrives through `set_html` is already live and nothing re-wires
  it.

## 3.5 One click, walked end to end, with the real values

```
a person clicks the chip labelled "ret" in pane 3

the setup script         reads data-python-onclick
                         = ouro_opcode('arch0000')
  pyBridge.execute_python("ouro_opcode('arch0000')")

bridge.execute_python    exec's it in the shared context
  the page's own block   defined ouro_opcode at request time

ouro_opcode              dashboard_ouro.render(3, 'arch0000')
                         builds 32,800 characters of html in python

set_html("pane", html)   runs rewrite_python_onclick over it
                         emits html_pushed("pane", html)

the setup script         document.getElementById("pane")
                             .innerHTML = html

the screen now shows     "ret appears in 29,653 (language, operator
                          group, signature) groups — drawing 200"
```

---

# 4. `test_page.html`, before and after

Run as the brief requires: the engine as it stood at commit `a5d8bee`,
then the engine as it stands. Same page, same flags, same rig.

LITERAL, both transcripts:

```
################ BEFORE — test_page.html on the engine at commit a5d8bee ################
[Engine] Executing embedded Python script...
Ourobrowser native context initialized. `fetch_system_data` is ready.
[rig] loadFinished ok=True  first paint 0.155 s after QApplication was built
[rig] shot test_page_before -> .../screens/log_184/test_page_before.png (1400x1000, saved=True, 51235 bytes)
[rig] click button
js: Uncaught SyntaxError: Failed to execute 'click' on 'HTMLElement': Invalid or unexpected token
[rig] wait 2 s
[rig] peak resident size of the python side: 233.4 MB

################ AFTER — test_page.html on the engine as it stands now ################
[Engine] Executing embedded Python script...
Ourobrowser native context initialized. `fetch_system_data` is ready.
[rig] loadFinished ok=True  first paint 0.037 s after QApplication was built
[rig] shot test_page_after -> .../screens/log_184/test_page_after.png (1400x1000, saved=True, 51235 bytes)
[rig] click button
[Bridge] Executing Python command: fetch_system_data()
\n--- System Data Fetched ---
OS: Linux 7.0.0-30-generic, Python: 3.13.9
---------------------------\n
[rig] wait 2 s
[rig] peak resident size of the python side: 237.7 MB
```

Two things are shown against each other, and both matter:

- **The page looks exactly the same.** The two screenshots are
  byte-identical:

  ```
  a18bfe33fef5d9131c06fb2f2bcb9015  .../screens/log_184/test_page_before.png
  a18bfe33fef5d9131c06fb2f2bcb9015  .../screens/log_184/test_page_after.png
  ```

- **The button behaves differently, and that is the point.** Before, a
  syntax error. After, python ran.

`test_page.html` itself was not edited: `git diff a5d8bee..HEAD --
test_page.html` prints nothing.

---

# 5. The dashboard page, and how it differs from `dashboard.html`

## 5.1 The two pages, side by side

| | `dashboard.html` (task 68, untouched) | `dashboard_ouro.html` (this task) |
|---|---|---|
| where it runs | any browser with the File System Access API | Ourobrowser |
| how it gets the artifacts | the person picks the folder; the page reads it in the browser | python calls `open()` |
| the join | `dashboard_join.js`, in JavaScript | `viewer_build.py`'s python join, imported |
| JavaScript in the page | the join and five pane modules | **none at all** |
| the folder must be re-picked each time | yes, on a double-clicked file (log_176 §4) | the question does not arise |
| Firefox | says so, points at the snapshot (log_176 §5) | the question does not arise |
| clicks | JavaScript event handlers | `onclick="python:…"`, executed by python |

Neither replaces the other. `dashboard.html`, `dashboard_join.js`,
`dashboard_loader.js` and the five `dashboard_pane*.js` modules were not
edited: `git diff a5d8bee..HEAD` over all of them prints nothing.

## 5.2 The reuse, proved by import rather than asserted

The brief asks which functions are CALLED rather than copied. LITERAL,
the transcript of asking python:

```
viewer_build file : ~/Programming/PseudoCoupHQ/Research/op_pipeline/viewer_build.py
   dashboard_ouro -> viewer_build.units_of       <function units_of at 0x72125f656340>
   dashboard_ouro -> viewer_build.load           <function load at 0x72125f656160>
   dashboard_ouro -> viewer_build.carve          <function carve at 0x72125f6ef240>
   dashboard_ouro -> viewer_build.OperatorGroups <class 'viewer_build.OperatorGroups'>
   dashboard_ouro -> viewer_build.read_pool      <function read_pool at 0x72125f6eee80>
   dashboard_ouro -> viewer_build.read_coverage  <function read_coverage at 0x72125f6ef2e0>
   dashboard_ouro -> viewer_build.census_name    <function census_name at 0x72125f6ef100>
   dashboard_ouro -> viewer_build.trim_unit      <function trim_unit at 0x72125f6eef20>
   dashboard_ouro -> viewer_build.trim_rendered  <function trim_rendered at 0x72125f6eefc0>
   dashboard_ouro -> viewer_build.read_store     <function read_store at 0x72125f6eede0>
manifest shortcut : ~/Programming/PseudoCoupHQ/Research/op_pipeline/pane23_manifest_regex_check.py
   PAT is the same object: True
   unq is the same object: True
   viewer_build is the same module object: True
```

GLOSS: `is the same object: True` is the proof that the shortcut is
called and not retyped — a copy would be a different object.

What each is used for:

- `units_of` — the units of any artifact document, whichever of the two
  shapes it uses.
- `load`, `carve` — an artifact beside the page; `carve` lifts ONE
  member out of a large file's text without parsing it.
- `OperatorGroups` — **the machine operator-group key**. This is the
  spelling ban's own mechanism, and reusing it rather than re-minting
  ids is what keeps the two pages' groups the same groups.
- `read_pool` — the pool, and its per-unit rows, for pane 1.
- `read_coverage` — the 256 KB head read of each compiler graph.
- `census_name` — a census producer's display name.
- `PAT`, `unq` — the manifest shortcut of log_179 §3, whose own script
  is the proof that it agrees with `json.load` probe for probe.

**Two rules are ports, not reuse, and are labelled so in the source.**
`mnemsOf` (`dashboard_join.js` line 141) and `signatureOf` (line 169)
exist only in JavaScript; `viewer_build.py` has no twin of either, even
though the JavaScript comments name one. They are written in python in
`dashboard_ouro.py` as `mnems_of` and `signature_of`, each citing the
JavaScript line it mirrors. **This is the one place the same rule now
exists twice**, and it is named here rather than buried.

## 5.3 The ports are checked against the JavaScript pane's own measured
## numbers

A port claimed to mirror another implementation is worth nothing until
the two agree on real data. The python index over the whole population
answers, and log_179's realization row for `dashboard_pane23.js` says
what the JavaScript answered over the same population:

| what is counted | `dashboard_pane23.js` (log_179) | `dashboard_ouro.py`, measured now |
|---|---|---|
| units | 31,078 | 31,078 |
| units carrying a type signature | 31,067 | 31,067 |
| units carrying none, being interpreter handlers with no probe | 11 | 11 |
| distinct type signatures | 3,390 | 3,390 |
| operator groups | 131 | 131 |
| languages | 9 | 9 |
| arch opcodes | 162 | 162 |

LITERAL, the run that produced the right-hand column:

```
signatures: 133993 in 0.7 s, peak 161.9 MB
index: 31078 rows in 1.1 s, peak 161.9 MB
arch opcodes: 162
operator groups: 131
per language: [('c', 10620), ('cpp', 17840), ('cpython', 1), ('go', 590), ('java', 2), ('php', 4), ('ruby', 4), ('rust', 695), ('swift', 1322)]
distinct signatures: 3390
rows with no signature: 11
files read: 342
```

Evidence class: **forced by construction** for the agreement — two
independent implementations of one rule, over one population, printing
the same seven numbers.

---

# 6. The memory bound, stated and measured

## 6.1 What it is

```
cap    MEMORY_CAP_MB = 1500          peak resident size, MB
abort  OURO_MEMORY_ABORT             raised by name; the pane that asked
                                     for the work renders the refusal
                                     instead of a number
```

`guard_memory(stage)` is called after every stage that could grow —
after each manifest, after each artifact family, after the pool — and
`render()` catches the abort per pane, so one expensive pane can never
take the page down.

## 6.2 What is never opened whole, and what is read instead

| artifact | size | what the page does |
|---|---|---|
| `graph_cpp.json` | 331 MB | a 256 KB head, through `viewer_build.read_coverage` |
| `coverage_go2.json` | 515 MB | never opened; the file-level summary is read instead |
| `canon39_regen_store` | 219 MB over 326 shards | one shard at a time; index rows kept, the parsed document dropped |
| `the_pool5.json` | 32 MB | its `summary` by a TAIL carve for pane 5; the whole file only when pane 1 needs a per-unit row |
| the ten probe manifests | 94 MB | read as TEXT, scanned with the checked expression, dropped before the next |

A unit BODY is never held in the index. The index row remembers which
file the unit came from, and pane 1 re-opens that one file.

## 6.3 The measurements, pasted

- bare python, index over 31,078 units: **161.9 MB**
- bare python, index dumped for the guard: **162.1 MB**
- the whole Ourobrowser process, all six panes and eight pushes:
  **402.3 MB** (`[rig] peak resident size of the python side: 402.3 MB`)
- Ourobrowser on `test_page.html`, for comparison: **237.7 MB** — so
  the dashboard's own share is about 165 MB, which agrees with the bare
  python figure.

Against the cap of 1,500 MB, the abort was never reached. Stated
because today's incident (log_183's added rule) came from a miner that
reached 13.2 GB and exhausted the machine's swap.

---

# 7. The six panes, what each reads, and its population line

Every pane prints "N units read from M files, opened at HH:MM" — the owner's
mechanical-update rule made visible. LITERAL, three of them as
photographed:

```
pane 5   30,432 units read from 3 files, opened at 23:08
         — the pool's own members line; no index built
pane 2   31,078 units read from 345 files, opened at 23:13
         — index built in 2.2 s
pane 1   31,078 units read from 1016 files, opened at 23:08
         — one unit re-opened from canon39_regen_store/op_units2_cpp_c0158.json
```

| pane | what it draws | what it reads | cost |
|---|---|---|---|
| 5 stats | the pool's own summary, the four term states, why terms were disproved, the census's top 12 | `the_pool5.json` (tail carve), `audit65.json`, the HIGHEST-numbered `name_census*.json` | **the first paint**: 3 files, 0.024 s |
| 6 chronology | 39 steps over 1,107 commits, 13 carrying a recomputed number, each saying how the number was got | `chronology.json` | 0.00 s |
| 4 coverage | four compiler graphs' counts, go's coverage populations, the 25 most visited files, the 15 never entered | `graph_<lang>.json` heads, `coverage_go_summary.json`, `coverage_go_files.json` | 0.06 s |
| 2 selector | language → operator group → type signature → units, plus a seeded random unit | the index | 2.2 s to build the index, then instant |
| 3 arch opcode index | all 162 opcodes; one opcode → its (language, operator group, signature) groups, ceiling 200, saying what it cut down from | the index | instant on the built index |
| 1 unit viewer | one unit in nine modes: header, raw extracted, context, canonical, ledger, term, rendered back, pool entry, verdicts | the one store file the index row names, plus the two per-unit stores and the pool | ~2 s the first time |

Two numbers on the page reproduce numbers this line already had, which
is the check that the panes are reading and not remembering:

- pane 3 says `ret` is in **30,432** units — log_179 §3 recorded that
  the arch opcode in the most units is in 30,432 of them.
- pane 4 says **15** go files were never entered — log_181 §4.4
  recorded that the brief's "14 never-entered files" is 15.


## 7.1 Where the python panes render LESS than the JavaScript ones, named

All six panes are ported in the sense that each reads its artifacts and
answers its question. Three of them draw a plainer thing than
`dashboard.html` does, and the difference is stated here rather than
left to be discovered:

| pane | `dashboard.html` draws | `dashboard_ouro.html` draws | why |
|---|---|---|---|
| 4 coverage | the compiler region as a WIRING DIAGRAM — file boxes, directory-grouped or force-laid, one file expanded on click into its definitions; a probe's diary path lit in order with a step slider; coverage shading | tables: the four graphs' counts, go's coverage populations, the 25 most visited files, the 15 never entered | the diagram is an SVG layout driven by drag and hover. Nothing about Ourobrowser prevents it — the page can hold SVG and a click can redraw it — but a slider and a drag are per-frame interactions, and every frame here is a round trip through python |
| 6 chronology | a SLIDER over the banking commits with a fine scale over every daemon commit | the 39 steps as a table, each row saying how its number was got | the same reason: a slider is a per-frame interaction |
| 1 unit viewer | the nine modes as selectable tabs | all nine sections stacked down the page | a choice, not a limit; one click per mode would work |

**The honest general statement**: this browser gives python the DOM one
push at a time, so it is well suited to a page whose interactions are
discrete — a click that changes what is shown — and poorly suited to
one whose interactions are continuous. Everything the panes MEASURE is
here in full; what is thinner is the drawing, in exactly the two places
the JavaScript page uses a continuous control.

Whether the wiring diagram and the slider should be built for this page
too — and if so, whether Ourobrowser should gain a way for python to
push into an element WITHOUT replacing all of it — is the owner's, and it is
listed in §13.2.

---

# 8. Proof that it runs

## 8.1 The command, exactly as typed

```
cd ~/Programming/Ourobrowser && python3 browser_engine.py \
    /~/Programming/PseudoCoupHQ/Research/op_pipeline/dashboard_ouro.html
```

- The argument is new: `main()` now takes the page to open, defaulting
  to `test_page.html` as before.
- The leading `//` is the scheme's own. The browser builds
  `ourobrowser://local/` + the argument, and with an absolute path that
  gives `ourobrowser://local//home/...`. `resolve_page_path` serves an
  absolute path as given and anything else relative to the working
  directory, so both forms work.

**ONE THING ON THIS MACHINE, and it is not a repo change.** The host
`python3` is anaconda's, and importing `PyQt6.QtWebEngineWidgets` fails
on it:

```
ImportError: /usr/lib/x86_64-linux-gnu/libbrotlidec.so.1: undefined symbol: BrotliSharedDictionaryDestroyInstance
```

The cause is two brotli builds in one process — anaconda ships 1.0.9 and
the system 1.2.0. Preloading the system's common library fixes it, and
this belongs in the owner's shell, not in a tracked file:

```
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1 python3 browser_engine.py …
```

## 8.2 The terminal transcript of the run that produced the screenshots

LITERAL:

```
[Engine] Executing embedded Python script...
[Engine] Block emitted 3940 characters of HTML
[rig] loadFinished ok=True  first paint 0.064 s after QApplication was built
[rig] shot pane5_stats -> .../screens/log_184/pane5_stats.png (1400x1000, saved=True, 140334 bytes)
[rig] click [data-python-onclick="ouro_pane(6)"]
[Bridge] Executing Python command: ouro_pane(6)
[Bridge] Pushing 7545 characters of HTML into 'pane'
[rig] shot pane6_chronology -> .../screens/log_184/pane6_chronology.png (1400x1000, saved=True, 159249 bytes)
[rig] click [data-python-onclick="ouro_pane(4)"]
[Bridge] Executing Python command: ouro_pane(4)
[Bridge] Pushing 6544 characters of HTML into 'pane'
[rig] shot pane4_coverage -> .../screens/log_184/pane4_coverage.png (1400x1000, saved=True, 167292 bytes)
[rig] click [data-python-onclick="ouro_pane(2)"]
[Bridge] Executing Python command: ouro_pane(2)
[Bridge] Pushing 1616 characters of HTML into 'pane'
[rig] shot pane2_selector -> .../screens/log_184/pane2_selector.png (1400x1000, saved=True, 70655 bytes)
[rig] click [data-python-onclick*=rust]
[Bridge] Executing Python command: ouro_select('rust')
[Bridge] Pushing 4081 characters of HTML into 'pane'
[rig] click [data-python-onclick*=g00]
[Bridge] Executing Python command: ouro_select('rust','rust#g00')
[Bridge] Pushing 9676 characters of HTML into 'pane'
[rig] shot pane2_selector_drilled -> .../screens/log_184/pane2_selector_drilled.png (1400x1000, saved=True, 162753 bytes)
[rig] click [data-python-onclick="ouro_pane(3)"]
[Bridge] Executing Python command: ouro_pane(3)
[Bridge] Pushing 16564 characters of HTML into 'pane'
[rig] shot pane3_opcode_index -> .../screens/log_184/pane3_opcode_index.png (1400x1000, saved=True, 180302 bytes)
[rig] click .chip
[Bridge] Executing Python command: ouro_opcode('arch0000')
[Bridge] Pushing 32800 characters of HTML into 'pane'
[rig] shot pane3_opcode_drilled -> .../screens/log_184/pane3_opcode_drilled.png (1400x1000, saved=True, 230111 bytes)
[rig] click [data-python-onclick="ouro_pane(1)"]
[Bridge] Executing Python command: ouro_pane(1)
[Bridge] Pushing 3809 characters of HTML into 'pane'
[rig] shot pane1_unit_viewer -> .../screens/log_184/pane1_unit_viewer.png (1400x1000, saved=True, 159145 bytes)
[rig] peak resident size of the python side: 402.3 MB
```

- **First paint: 0.064 s** on this run. Across five runs the range was
  0.032 s to 1.681 s; the slow one was a cold file cache. First paint
  is pane 5, which reads three small files and never builds the index —
  that is why it is the first paint.
- Every `[Bridge] Pushing …` line is `set_html` working. Eight pushes,
  the largest 32,800 characters.

## 8.3 Screenshots, by path

All in `~/Programming/PseudoCoupHQ/DevComms/screens/log_184/`:

| file | what it shows |
|---|---|
| [pane1_unit_viewer.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/pane1_unit_viewer.png) | `cpp/regen_63240`, label `bitor`, signature `(a: unsigned long long, b: unsigned int) -> 64-bit`, its three instructions, its wrapped text, its ledger |
| [pane2_selector.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/pane2_selector.png) | the nine languages with their counts |
| [pane2_selector_drilled.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/pane2_selector_drilled.png) | rust → 21 operator groups → 22 type signatures under one group |
| [pane3_opcode_index.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/pane3_opcode_index.png) | all 162 arch opcodes with their unit counts, `ret` at 30,432 |
| [pane3_opcode_drilled.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/pane3_opcode_drilled.png) | one opcode's (language, operator group, signature) groups |
| [pane4_coverage.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/pane4_coverage.png) | four compiler graphs, go's coverage populations, the never-entered files |
| [pane5_stats.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/pane5_stats.png) | the pool summary, the term states, the disproof causes |
| [pane6_chronology.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/pane6_chronology.png) | 39 steps, each saying how its number was got |
| [test_page_before.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/test_page_before.png) | `test_page.html` at commit `a5d8bee` |
| [test_page_after.png](file://~/Programming/PseudoCoupHQ/DevComms/screens/log_184/test_page_after.png) | the same page now — byte-identical |

**How the screenshots were taken, stated plainly.** A window on a
Wayland desktop cannot be photographed from this terminal session, so a
RIG drives the browser: it builds the same `OurobrowserWindow` the
program builds, waits for `loadFinished`, clicks by CSS selector through
`page().runJavaScript`, and saves `window.grab()`. Two settings make it
work headless: `QT_QPA_PLATFORM=offscreen`, and
`QTWEBENGINE_CHROMIUM_FLAGS="--disable-gpu --disable-gpu-compositing"`
— without the second, the Qt chrome is captured and the web content
area comes out blank, because the composited GPU surface is not part of
the widget. The rig lives outside both repos, in this session's
scratchpad, so it adds no un-ruled file to the owner's projects.

**The command the owner runs to see it himself**, with a real window:

```
cd ~/Programming/Ourobrowser && LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1 python3 browser_engine.py /~/Programming/PseudoCoupHQ/Research/op_pipeline/dashboard_ouro.html
```

---

# 9. THE SPELLING BAN, applied and RUN

## 9.1 How this work obeys it

- **Units are grouped by a machine id, minted by the join's own
  `OperatorGroups`**, not re-minted here. A group is `rust#g00`; the
  token rides beside it as a display label.
- **Arch opcodes are keyed by an opaque id** — `arch0000` — with the
  mnemonic as a VALUE on the row. This is the CORE's own resolution of
  the homograph finding: `and`, `or`, `xor` and `not` are x86 mnemonics
  AND alternative operator spellings in C++, and a dict key cannot carry
  that distinction.
- **The token appears exactly once per unit**, as `label` on the unit's
  own row, which is the one place the ban allows it.
- **The glyph test**: replace every label with a glyph and every pane
  still works, because no pane reads a label for anything but printing.

## 9.2 The three guards, ONE process, transcript pasted

LITERAL, the whole run:

```
### 0. the two inherited guards are UNMODIFIED -- git says so, not me
fdff0b2 Wed Aug 26 13:14:26 2026 -0400  update
38cea92 Thu Sep 3 19:15:20 2026 -0400  auto: 3 files (dashboard_join.js, viewer_build.py, check_dashboard_js_no_spelling.py)
(no diff lines above = neither guard was touched by this task)

### 1. the grouping structure the python renderer builds, dumped for the guard
wrote .../scratchpad/ouro_index.json (10.2 MB): 31078 units, 131 operator groups, 162 arch opcodes
peak resident size while building the index: 162.1 MB

### 2. check_no_spelling_keys.py, UNMODIFIED, over that structure
operator inventory: 91 tokens read from probe_manifest_*.json
PASS ouro_index.json -- no operator token in any key, grouping, pairing or row structure
   exit=0

### 3. check_dashboard_js_no_spelling.py over the JavaScript that remains
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_ouro.html -- no operator token is written as a literal, so none can be a key (0 named coincidences above)
     browser_engine.py:99  '/' -- the artifacts' own unit-id separator, as in c/op_100
PASS browser_engine.py -- no operator token is written as a literal, so none can be a key (1 named coincidences above)
PASS bridge.py -- no operator token is written as a literal, so none can be a key (0 named coincidences above)
   exit=0

### 4. check_dashboard_py_no_spelling.py -- NEW, over the python renderer
operator inventory: 91 tokens read from probe_manifest_*.json
     dashboard_ouro.py:846  '..' appears as a value or a piece of prose, in no position that keys anything
     dashboard_ouro.py:274  '/' appears as a value or a piece of prose, in no position that keys anything
PASS dashboard_ouro.py -- no operator token sits in a key, a subscript, a comparison, a membership test or a lookup (2 mention(s) above)
   exit=0
```

```
=================== grep -c exempt over the whole transcript ===================
0
```

- **The 91-token inventory is the same inventory**, read by all three
  from the unmodified `check_no_spelling_keys.inventory()`.
- **The page emits no JSON**, so there was nothing for the data guard
  to walk. Rather than skip it, the grouping structure the renderer
  actually builds in memory — 31,078 unit rows, 131 operator groups, 162
  arch opcodes — was dumped to the scratchpad and walked by the
  unmodified guard. That is a real check on the real structure, and the
  dump is outside both repos because the CORE's rule is that the page
  reads the artifacts live and stores no copy.
- **The two mentions in the python renderer, named.** Line 274 is
  `uid.split("/")` — the artifacts' own unit-id separator, as in
  `c/op_100`. Line 846 is `os.path.join(HERE, "..", "compiler_graph")` —
  a path segment. Neither keys anything, and the guard says so itself
  rather than my saying it for it.

## 9.3 Why a THIRD guard was needed

The data guard walks JSON; the JavaScript guard walks string literals in
JavaScript. The python renderer is neither, and it is where the
grouping now happens. `check_dashboard_py_no_spelling.py` reads the
python SYNTAX TREE rather than grepping, so it can tell a dict key from
a piece of prose — a distinction a grep cannot make, and this line has
been burned twice by a token that reached a key by accident.

It fails a token in exactly the positions that decide identity: a key in
a dict display, a subscript index, a comparison operand, a membership
element, and the first argument of `.get`/`.setdefault`/`.pop`.

---

# 10. The planning trees, written before the code

Both trees carry the shape before the code, per PROTOCOL §2 and
log_183's standing rules.

## 10.1 Ourobrowser's own tree

The design went into the two LEVEL-2 nodes, which are agent-editable
with provenance:

- `Planning/node_0_3_engine/node_0_1_scheme_handler/CORE_0_1_scheme_handler.md`
  — `## definition`, `## design`, `## settled rules`: `PAGE_EMIT_NAME`,
  `PAGE_PATH_NAME`, `PYTHON_CLICK_ATTRIBUTE`, `rewrite_python_onclick`,
  and the measured record of the broken rewrite.
- `Planning/node_0_3_engine/node_0_2_executor/CORE_0_2_executor.md` —
  the one shared context, the two moments code enters it, and the
  request-time/click-time walk.
- `Planning/node_0_4_bridge/node_0_0_web_channel/CORE_0_0_web_channel.md`
  — `html_pushed`, `set_html`, and the injected rewriter.

**The two LEVEL-1 COREs each gained a `## design` ROLLUP, and that is
flagged.** PROTOCOL §2 says a level-1 CORE changes only through the owner.
The brief instructed writing the design into "its engine and bridge
nodes' CORE". The compromise made, and the owner's to accept or undo: the
substance is in the level-2 nodes; each level-1 CORE carries only a
table pointing at them, marked as appended by the implementer on the
brief's instruction. The reason for adding anything at level 1 is the
framework's completeness rule — a reader who stops at `engine` would
otherwise not know the node had gained a capability.

Six PROGRESS files carry two entries each, one at the moment the design
was written and one at the moment the code landed.

## 10.2 The dashboard node in PseudoCoupHQ

`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md`
gained one settled rule and four realization rows. The rule, LITERAL:

> - **A SECOND ROUTE MAY RENDER THE SAME PANES, AND NEITHER ROUTE OWNS
>   THE JOIN.** … The condition that makes a second route legal is that
>   it ADDS NO THIRD JOIN — the python page imports the python join
>   `viewer_build.py` already holds rather than restating it.

---

# 11. Complete file inventory

## 11.1 `~/Programming/Ourobrowser` — new content in existing files

| file | what changed |
|---|---|
| `browser_engine.py` | `PAGE_EMIT_NAME`, `PAGE_PATH_NAME`, `PAGE_PUSH_NAME`, `PYTHON_CLICK_ATTRIBUTE`, `PYTHON_ONCLICK_PATTERN` (repaired), `rewrite_python_onclick`, `resolve_page_path`, `setup_script`; `requestStarted` collects what a block emits; `OurobrowserWindow(start_page=…)`; `main()` takes the page as its one argument |
| `bridge.py` | `html_pushed` signal, `set_html` method, injected `rewriter`, `_identity` default. `execute_python` unchanged |
| `test_page.html` | **not edited** — `git diff a5d8bee..HEAD` is empty |

## 11.2 `~/Programming/Ourobrowser/Planning` — five COREs, six PROGRESS

| file | what changed |
|---|---|
| `node_0_3_engine/CORE_0_3_engine.md` | `## design` rollup appended (level 1 — flagged for the owner) |
| `node_0_3_engine/node_0_1_scheme_handler/CORE_0_1_scheme_handler.md` | rewritten: definition, design, settled rules |
| `node_0_3_engine/node_0_2_executor/CORE_0_2_executor.md` | rewritten: definition, design, settled rules |
| `node_0_4_bridge/CORE_0_4_bridge.md` | `## design` rollup appended (level 1 — flagged for the owner) |
| `node_0_4_bridge/node_0_0_web_channel/CORE_0_0_web_channel.md` | rewritten: definition, design, settled rules |
| `node_0_3_engine/PROGRESS.md` | design entry + code-landed entry |
| `node_0_3_engine/node_0_1_scheme_handler/PROGRESS.md` | design entry + code-landed entry |
| `node_0_3_engine/node_0_2_executor/PROGRESS.md` | design entry + code-landed entry |
| `node_0_4_bridge/PROGRESS.md` | design entry + code-landed entry |
| `node_0_4_bridge/node_0_0_web_channel/PROGRESS.md` | design entry + code-landed entry |
| `node_0_5_test_page/PROGRESS.md` | the before/after proof |

## 11.3 `~/Programming/PseudoCoupHQ` — new files

| file | what it is |
|---|---|
| `Research/op_pipeline/dashboard_ouro.html` | the page: no JavaScript, one python block |
| `Research/op_pipeline/dashboard_ouro.py` | the renderer: six panes, the memory bound, the two ports |
| `Research/op_pipeline/check_dashboard_py_no_spelling.py` | the spelling guard over python page code |
| `DevComms/log_184_task77_dashboard_in_ourobrowser.md` | this log |
| `DevComms/screens/log_184/` | ten screenshots |

## 11.4 `~/Programming/PseudoCoupHQ` — edited

| file | the whole of the edit |
|---|---|
| `Planning/.../node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md` | one settled rule; four realization rows |
| `Planning/.../node_0_3_5_10_dashboard/PROGRESS.md` | one entry |

## 11.5 Deliberately not touched

`dashboard.html`, `dashboard_join.js`, `dashboard_loader.js`,
`dashboard_pane1.js`, `dashboard_pane23.js`, `dashboard_pane4.js`,
`dashboard_pane5.js`, `dashboard_pane6.js`, `viewer_build.py`,
`viewer_template.html`, `check_no_spelling_keys.py`,
`check_dashboard_js_no_spelling.py`, `pane23_manifest_regex_check.py`,
`chronology_build.py`. `git diff a5d8bee..HEAD` over all of them prints
nothing.

---

# 12. FOR DEE'S RULING — every name and every shape I chose

Nothing below is decided. Each is implemented under a working name that
lives in exactly ONE place, so changing it is one edit.

## 12.1 Names in the browser

| working name | where it is defined, one place | what it names | the alternative I did not take |
|---|---|---|---|
| `emit` | `browser_engine.PAGE_EMIT_NAME` | a block puts HTML in its own place | a magic `__html__` variable the engine reads after the block; rejected because it cannot be called twice |
| `page_path` | `browser_engine.PAGE_PATH_NAME` | the absolute path of the file being served | `__file__`, which would shadow python's own meaning |
| `set_html` | `browser_engine.PAGE_PUSH_NAME`, and the method name on `PythonBridge` | fill a named element | `push_html`, `render_into`, `fill` |
| `data-python-onclick` | `browser_engine.PYTHON_CLICK_ATTRIBUTE` | the click wire form | keeping inline JavaScript, which is what broke |
| `html_pushed` | `bridge.PythonBridge.html_pushed` | the Qt signal carrying (element id, html) | `htmlPushed` (Qt's own casing); python casing was chosen because the page never types it |
| `rewriter` | `PythonBridge.__init__` argument | the injected click rewrite | importing the engine from the bridge, which is a cycle |

## 12.2 Shapes in the browser

- **Two additions rather than one.** `emit` at request time, `set_html`
  after first paint. A single mechanism was considered and does not
  exist: at request time there is no element; at click time there is no
  block.
- **The bridge answers with a SIGNAL, not a return value.** A returned
  value only reaches the page through an asynchronous JavaScript
  callback, which would put page-authored JavaScript back into a project
  built to remove it.
- **The click wire form is an ATTRIBUTE, and the listener is delegated
  from `document`.** This is what makes HTML pushed later work with no
  re-wiring. It also means the engine writes exactly one script into a
  page: its own.
- **`main()` takes the page as its one argument, and an absolute path is
  served as given.** Needed to point the browser at a page outside its
  own folder. `resolve_page_path` tries absolute first, then relative.
- **A block that emits nothing behaves exactly as before.** This is what
  keeps every existing page working, and it is why `test_page.html` is
  byte-identical.

## 12.3 Names and shapes in the dashboard

| working name | what it is | note |
|---|---|---|
| `dashboard_ouro.html` / `dashboard_ouro.py` | the page and its renderer | "ouro" is a shortening of the browser's name; the CORE calls the panes what the owner numbered them |
| `ouro_pane`, `ouro_unit`, `ouro_select`, `ouro_opcode` | the four functions a click calls | defined in the page's own block, so they are the page's vocabulary, not the module's |
| `arch0000` | the opaque arch opcode id | prefix in `dashboard_ouro.ARCH_ID_PREFIX` |
| `MEMORY_CAP_MB` = 1500, `OURO_MEMORY_ABORT` | the memory bound and its abort | the cap is a judgement; measured peak is 402.3 MB |
| `check_dashboard_py_no_spelling.py` | the third guard | named to sit beside the two that exist |

- **Pane 5 is the first paint.** It is the cheapest — three small files,
  0.024 s, no index. A reader who opens the page and reads nothing else
  gets the authoritative counts immediately. Whether pane 1 should be
  the first paint instead is the owner's.
- **The index is built lazily, once per browser session**, when a pane
  first needs it. It is not written to disk, because the CORE's rule is
  that the page reads the artifacts live.
- **The tab bar shows six panes, numbered as the CORE numbers them.**
  Log_182's coordinator note recorded that the JavaScript page's tab bar
  had drifted to eight; this page was built from the CORE's numbering
  and has six. If the CORE's names no longer cover what exists, that is
  the same open question task 82 carries.
- **The two ports.** `mnems_of` and `signature_of` now exist in both
  JavaScript and python. They agree on seven measured numbers today, and
  nothing enforces that they keep agreeing. Whether to make one of them
  the only copy — and if so which — is an architecture question, and it
  is the only structural debt this task adds.

## 12.4 One governance point

The `## design` rollups appended to `CORE_0_3_engine.md` and
`CORE_0_4_bridge.md` are edits to LEVEL-1 COREs, which PROTOCOL §2
reserves to the owner. They were made on the brief's instruction and are
marked as such inside the files. Removing them costs one deletion each;
the level-2 nodes hold the substance either way.

---

# 12b. The plan checker: zero regressions, and eight defects that are not mine

Ourobrowser's tree does not pass `check_plans.py`, and it did not before
this task. The comparison is apples to apples — a real git checkout at
commit `4fb9d3f` (the last commit before task 77 touched anything), with
the same remote url, and the same checker:

| error | at `4fb9d3f` | now |
|---|---|---|
| `grammar` — the tree root has no PROGRESS.md | 1 | 1 |
| `missing-check` — a node with no CHECK file | 1 | 1 |
| `projection` — `## sub_nodes` disagrees with the register | 2 | 2 |
| `edge-unresolved` — an edge naming a file that does not exist | 4 | 4 |
| `edge-one-ended` — an edge stated at one end only | 4 | 4 |
| `node-self-path` — a `node.path` that does not name its own file | 4 | 4 |
| `node-self-name` — a `node.name` disagreeing with its folder | 1 | 1 |
| `node-self-repo` — the root's repo/remote | 2 (the checkout was detached) | 1 |
| **summary** | **8 errors, 1 warning** | **8 errors, 1 warning** |

- **I preserved the frontmatter of every CORE I rewrote.** LITERAL, the
  same field before and after in one of the three:

  ```
  4fb9d3f:     path: node_0_3_engine/node_0_1_scheme_handler/CORE_0_1_scheme_handler.md
  HEAD   :     path: node_0_3_engine/node_0_1_scheme_handler/CORE_0_1_scheme_handler.md
  ```

- **The five COREs that changed are all mine, and git names them**:
  `719ed5a`, `8450925`, `ca148eb`.

**The defects are Ourobrowser's own, and two of them are the owner's to fix
because they sit on a level-0 or level-1 CORE.** They are named here
rather than swept (PROTOCOL §6c), and none of them is a consequence of
this task:

- the three level-1 registers name `node_1_0_*` paths while the folders
  on disk are `node_0_0_*`, which is what produces both the
  `edge-unresolved` and the `edge-one-ended` counts of 4;
- the four level-2 COREs carry a `node.path` without its `Planning/`
  prefix, and `level: 1` where the folder is at level 2;
- `Planning/CORE_0.md` says the remote is `Ourobrowser.git`; git says
  `https://github.com/TheStudent00/PyBrowser.git`. The project was
  renamed in commit `74f2a1c` and the CORE was updated ahead of the
  remote, or the remote was never renamed.

---

# 13. Two lists

## 13.1 Decided, mechanical, recorded for audit

- Pane 5 as the first paint, on cost.
- The index built lazily and never stored.
- `the_pool5.json`'s summary read by a TAIL carve rather than a whole
  load, applying the CORE's existing ranged-read rule.
- The screenshot rig kept outside both repos.
- The `LD_PRELOAD` line kept out of every tracked file — it is a fact
  about this machine's two brotli builds, not about the project.
- The guard's subject being a scratchpad dump of the in-memory structure,
  because the page emits no JSON.

## 13.2 Awaiting the owner

- Every name in §12.1 and §12.3.
- The two-additions shape, and the signal-not-return-value decision
  (§12.2).
- The `## design` rollups on the two level-1 COREs (§12.4).
- Which of the two copies of `mnemsOf`/`signatureOf` should survive
  (§12.3, last bullet) — the one structural debt this task adds.
- Whether panes 4 and 6 should get the wiring diagram and the slider the
  JavaScript page has (§7.1) — and, if so, whether Ourobrowser should
  gain a way for python to push into part of an element rather than
  replacing all of it.
- Whether `DevComms/` should stay in Ourobrowser's `.gitignore`. This
  task wrote that project's first numbered log,
  `~/Programming/Ourobrowser/DevComms/log_001_python_renders_the_page.md`,
  and the repo's own rule keeps it untracked.
