# log 188 — task 82: Airlock's cross-instance view, and the dashboard's tabs

Date: 2026-09-03/04. Task 82 from log_183 (round 15 briefs, written by the
Claude Code coordinator, not by the owner — nothing in that log is a ruling).

---

## 1. Walkthrough

Two unrelated fixes, one in Airlock and one in the dashboard, both
already measured problems rather than new investigations.

- **Airlock.** `progress.sh` and `airlock status` only ever look at the
  ONE instance the command names (or `sandbox` by default). By the
  round-11 ruling every task runs in its OWN instance, so a lane could
  be running in `t82` for the whole hour and the command someone
  actually types with no flags would still read "nothing running." The
  fix adds a one-line header, on both the shell and the python side,
  naming any OTHER instance that has a lane queued or running. It
  reuses the exact instance-discovery Airlock's own `doctor` command
  already had (`instances/*.conf` plus `<runs>/*`) rather than
  re-deriving that list a second time. Proved with a second instance
  (`t82`) brought up, a 60-second lane run in it, and both views read
  while it ran, then again after it finished.
- **The dashboard.** Two things were wrong on the same page, both read
  off a screenshot in log_182's own coordinator note: the tab bar had
  eight buttons where the CORE names six panes, because three pane
  modules (task 73's coverage view, task 74's stats, task 76's
  chronology) each appended a NEW tab beside the placeholder draft tab
  it was built to replace, instead of retiring that draft; and the
  header's own arch-opcode count read differently in two different
  screenshots (122 in one, 162 in another) because it counts a number
  that is still growing in the background when the page first paints,
  and nothing forced one more paint once that growth finished. Both are
  fixed and both are shown working, live, with real screenshots below —
  not asserted.

---

## 2. Part (a) — Airlock's cross-instance view

### 2.1 The cause, quoted

Operator, 2026-09-03: "what is running and why cant i see it in Airlock
status?"

LITERAL, `Airlock/progress.sh` (before this change) —
the "running" section only ever reads the CURRENT instance's own
`agent/status`:

```
echo "== running =="
local any=0
if compgen -G "$STATUS/*.status" > /dev/null; then
  for s in "$STATUS"/*.status; do
```

`$STATUS` is `$AL_AGENT_DIR/status`, and `$AL_AGENT_DIR` is resolved
for exactly one instance — the one named by `--instance` /
`AIRLOCK_INSTANCE`, `sandbox` if neither is given. A lane running in
`t82` never appears here no matter how long it runs, because this loop
never looks at `t82`'s own `agent/status`.

### 2.2 The fix, mechanically

**Discovery is reused, not duplicated.** `airlock doctor` already had
the two-source scan for what instances exist:
`instances/*.conf` (an instance's settings, inside the checkout) and
`<runs>/*` (an instance's run tree, outside the checkout — an
instance can exist with no conf file at all, since every key has a
default, and then it leaves a trace only under `~/AirlockRuns`).

- **Python side.** `Airlock/airlock` gained a module-level
  function `known_instances(paths)`, holding exactly that two-source
  scan, pulled out of `Doctor.check_instances` (which now calls it
  instead of re-listing both sources itself — one scan, two callers).
  A new function `other_busy_instances_line(paths)` walks every OTHER
  known instance, opens its `Paths` (the same object every other
  command uses to resolve an instance's `agent/drop` and
  `agent/status`), and checks two things per instance: any `.sh` file
  sitting in its `drop` that is not also reported `running`, and any
  `LaneStatus` in its `status` directory whose `state` is `running`.
  Called once, from `_render_status` — the function `status` and
  `watch` both already share — so both commands print the header
  identically.
- **Shell side.** `Airlock/instance.sh`'s existing
  `airlock_instance_list()` (previously only `instances/*.conf` plus
  `sandbox`) now also scans `<runs>/*`, so it matches the
  python side's two-source discovery exactly. A new function,
  `airlock_other_busy_instances(root, current)`, walks that list; for
  each OTHER instance it runs `airlock_instance_load` in a SUBSHELL
  (so it never overwrites the caller's own `AL_*` variables), reads
  that instance's `drop` and `status`, and prints one line per busy
  instance. `Airlock/progress.sh` calls it once, from a
  new `print_other_instances()`, right after the instance banner and
  before the batch summary.
- **The one correction made while proving it.** The daemon
  (`daemon/watcher.py`, `run_script()`) leaves a running lane's script
  sitting in `/drop` for its WHOLE run, and only archives it into
  `/drop/.done` when it finishes. The first draft of both
  implementations counted that script as ALSO queued, double-counting
  a running lane. Both now exclude a script already reported `running`
  from the queued count.
- **Degrades quietly.** An instance whose conf cannot be read, whose
  agent tree does not exist, or whose status directory is unreadable
  is skipped, never an error — this is a header, not a check, and the
  brief is explicit that it must never turn a status view into one.

### 2.3 Proof — a second instance, a 60-second lane, both views

`instances/t82.conf` (gitignored, per-machine, proxy off, its own
persist volume, `watch = poll`, `script_timeout = 300`) brought
`t82` up beside the default `sandbox` instance. A lane printing
`[n/6]` every 10 seconds for 60 seconds was submitted to it with
`python3 ./airlock --instance t82 submit ... --no-batch`, and both
views were read while it was running.

LITERAL — default instance, `bash
Airlock/progress.sh` (head):

```
== instance sandbox  (runner sandbox-runner, agent <airlock>/agent) ==

== other instances busy ==
  t82 (running: t82_sleep60b.sh)
  (this view is instance 'sandbox' — bash progress.sh --instance <name> [-w])

== batch summary ==
  batch:    task27  (id batch-20260901T154117Z)
```

LITERAL — default instance, `python3 Airlock/airlock
status` (head):

```
  other instances busy: t82 (running: t82_sleep60b.sh)   (this view is instance 'sandbox' — airlock --instance <name> status, or bash <airlock>/progress.sh --instance <name>)

batch summary
```

LITERAL — the `t82` instance's OWN view,
`AIRLOCK_INSTANCE=t82 bash progress.sh`:

```
== instance t82  (runner t82-runner, agent <runs>/t82/agent) ==

== batch summary ==
  no batch manifest present (<runs>/t82/agent/batch.json) — showing all lanes below

== queued (waiting in <runs>/t82/agent/drop) ==
  t82_sleep60b.sh

== running ==
  t82_sleep60b.sh   started 2026-09-04T02:56:05+00:00
    log: <runs>/t82/agent/logs/20260904T025605Z__t82_sleep60b.sh.log
    [3/6] sleeping 10s
    last: [3/6] sleeping 10s
```

The lane finished (`state=done exit=0 elapsed_s=60.1`),
`bash Airlock/down.sh --instance t82` removed the
container (`down` did not refuse — nothing was `running` at that
point), and the default view was read again. The header is gone
because nothing is queued or running in `t82` any more — the
instance's own run tree still exists on disk; the check is over its
STATE FILES, not over whether the tree exists:

```
== instance sandbox  (runner sandbox-runner, agent <airlock>/agent) ==

== batch summary ==
  batch:    task27  (id batch-20260901T154117Z)
```

Confirmed after this session's crash and restart, `podman ps -a
--filter name=t82` returns no rows — the `t82` container stayed down.

### 2.4 Guard

```
$ bash Airlock/scrub_check.sh
=== scrub_check: 7 pattern(s), 54 tracked file(s), 4 untracked-and-unignored file(s) ==="
scrub_check: PASS - no personal or machine-identifying pattern found.
```

One round-trip was needed getting here: the first draft of the code
comments quoted the operator's question with a name attached;
`scrub_check.sh` caught it (its "personal handle of the maintainer"
pattern) in `airlock`, `instance.sh` and `progress.sh`, and again in
the first draft of this task's own Airlock-side log. Fixed by dropping
the attribution and keeping the quote itself, dated but unattributed —
matching how the rest of the repo's comments record a ruling by date
alone.

### 2.5 Recorded in Airlock's own log

`Airlock/DevComms/log_004_cross_instance_status_header.md`
— Airlock's own record of this change set, independent of this file
(§9.1 of the communication protocol: a tool's own DevComms carries the
tool's record; a project's own log carries the caller-side report).

---

## 3. Part (b) — the dashboard's tabs and header

### 3.1 Both causes, read off the code

**Cause 1 — the tab bar.** `dashboard_join.js`'s own `mount()` draws
FIVE draft tabs synchronously (`units`, `opcodes`, `coverage`,
`stats`, `spec`). Three pane modules each wrap `DashboardJoin.mount`
and APPEND their own new nav button rather than retiring the draft one
they were built to replace:

LITERAL, `dashboard_pane4.js` (before this change), inside `attach()`:

```
var btn = document.createElement("button");
btn.dataset.t = "graph4";
btn.textContent = "compiler graph & coverage — pane 4";
nav.appendChild(btn);
```

— with no corresponding removal of `nav button[data-t="coverage"]` or
`#t-coverage`, the draft section it stands in for. `dashboard_pane5.js`
does the identical thing for `stats`/`#t-stats`. `dashboard_pane6.js`
adds `chrono`, which is genuinely new (the join's own draft never had
a sixth tab) — not a duplicate.

5 draft tabs + 3 appended (coverage_view's own, stats' own,
chronology) = **8**, matching log_182's own measurement exactly:
"the tab bar has eight entries where the CORE numbers five" — the CORE
had, by the time task 82 started, already been updated to six panes
(chronology added), so the arithmetic is 5 (draft) + 3 (appended) = 8,
retiring 2 (the coverage and stats drafts) gives 6.

**Cause 2 — the header.** LITERAL, `dashboard_join.js:1088` (unchanged
by this task, quoted as the object the finding is about):

```
Object.keys(state.opcodeIndex).length + " arch opcodes · pool "
```

`state.opcodeIndex` is the SAME object reference `source.opcodeRows`
in `dashboard_loader.js` mutates in place as the background scan
(`indexAll()`) adds more arch mnemonics to it — the count this line
reads is genuinely LIVE, so `paintHeader()` already shows a bigger
number the later it is called. The existing on-tick callback
(`repaintIndexPanes()`, called from `indexAll`'s own progress
callback) already repaints on every chunk including the last one — but
nothing repainted the header a GUARANTEED final time once
`indexAll()`'s own promise had fully resolved, so a screenshot taken
right at that instant could in principle still show a value from the
tick before it, and the coordinator's own two captures (122, 162) are
exactly this: the same live count, read at two different moments.

### 3.2 The fix, mechanically — additive, no rewrite

Three files, all additive edits (new lines beside the existing ones,
no restructuring), re-read immediately before each edit:

- **`dashboard_pane4.js`** — after creating its own `graph4` button
  and `#t-graph4` section (unchanged), a few new lines remove
  `nav button[data-t="coverage"]` and `#t-coverage` if present. Safe
  here because `attach()` runs AFTER the join's own `drawCoverage()`
  has already populated (and no longer needs) that draft section — the
  existing wrap already defers `attach()` to `inner(...).then(...)`.
- **`dashboard_pane5.js`** — the SAME retirement for `stats`/`#t-stats`,
  but NOT inside `attach()`: pane 5's existing wrap calls `attach()`
  SYNCHRONOUSLY, before the join's own async `drawStats()` has
  populated `#t-stats`, so removing the section there first would make
  `drawStats()` write into a since-removed node and throw, breaking
  the whole `mount()` promise chain. The new `retireDraftStats(root)`
  function is instead called from `out.then(...)`, deferred exactly
  the way pane 4 already was.
- **`dashboard_loader.js`** — inside `boot()`'s `indexAll(...).then(...)`
  completion handler (previously only a `console.log`), one explicit
  `api.paintPopulation(source.pop); api.repaintIndexPanes();` call,
  made ONCE MORE after `rows` proves `indexAll`'s own promise has
  fully resolved — independent of whether the last on-tick callback
  happened to land at exactly the right moment.

`dashboard_join.js` and `dashboard.html` are UNCHANGED by this task —
confirmed by `git log`, no commit in this session's range touches
either file.

### 3.3 Proof — a real page, real artifacts, screenshots

The live page needs a folder picked through the browser's OS-level
dialog, which no automation here can drive (the same limitation the
existing `dashboard_test_harness.html` and
`dashboard_pane6_harness.html` document and work around). A new file,
`PseudoCoupHQ/Research/op_pipeline/dashboard_full_harness.html`,
follows the SAME established pattern — `dashboard_test_shim.js`
dresses ranged HTTP fetches as directory handles — but loads every
script `dashboard.html` loads, in the same order, so the FULL tab bar
and header could be measured, not just one pane. Nothing in
`dashboard.html`, `dashboard_join.js`, `dashboard_loader.js` or any
`dashboard_pane*.js` file knows this file exists — it is a test rig
only, the same posture the precedent files declare of themselves.

Served with the repo's own `dashboard_test_server.py` (unchanged) over
the real artifacts in `PseudoCoupHQ/Research`, and
captured with `google-chrome --headless` at two points controlled by
`--virtual-time-budget` (a short one to catch the page mid-load, a
long one to let the full background scan finish) — a genuinely
different real-browser run each time, not the interactive session
re-screenshotted.

Screenshots, `PseudoCoupHQ/DevComms/screens/log_188/`:

| file | shows |
|---|---|
| `header_before_background_index.png` | header reads **133 arch opcodes**, population line says "unit index 40 of 332 files read" — mid-load, live count |
| `header_after_background_index.png` | header reads **162 arch opcodes** (the CORE's own measured total, log_179), population line says "every unit body indexed" — the explicit final repaint landed |
| `tabbar_pane4_coverage_view.png` | the tab bar in BOTH screenshots above, and this one: exactly **six** buttons — `1 · arch-unit viewer`, `2 · arch opcode index`, `5 · what was asked for`, `6 · chronology`, `term & census stats — pane 5`, `compiler graph & coverage — pane 4`. No `3 · compiler coverage` or `4 · stats` draft left. Pane 4 itself renders fully: the go compiler graph, 81 file boxes, 331 wires |
| `tabbar_pane5_stats.png` | pane 5's own tab, rendering correctly after the draft's retirement: the four term states (proved 26,594 / disproved 3,134 / undecided 285 / no term 419 of 30,432) and the top census causes |
| `tabbar_pane6_chronology.png` | pane 6, unaffected by this task's changes (it had no draft to retire), rendering the round-14 step correctly, shown for completeness of the six-tab set |

Both `header_*` captures were reproduced twice each (once before this
session's crash and restart, again after, since the first pair lived
only under `/tmp` and did not survive) — the SAME numbers came back
both times: 133 (or 148, or 144, depending on exactly which
`virtual-time-budget` value landed the capture) partial, 162 final,
always the CORE's own measured total.

### 3.4 Guards

```
$ /tmp/reconnect_venv/bin/python3 check_dashboard_js_no_spelling.py \
    dashboard_join.js dashboard_loader.js dashboard_pane1.js \
    dashboard_pane23.js dashboard_pane4.js dashboard_pane5.js dashboard_pane6.js
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_join.js -- ... (3 named coincidences above)
PASS dashboard_loader.js -- ... (3 named coincidences above)
PASS dashboard_pane1.js -- ... (2 named coincidences above)
PASS dashboard_pane23.js -- ... (0 named coincidences above)
PASS dashboard_pane4.js -- ... (4 named coincidences above)
PASS dashboard_pane5.js -- ... (0 named coincidences above)
PASS dashboard_pane6.js -- ... (0 named coincidences above)

$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py dashboard_snapshot_data.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_snapshot_data.json -- no operator token in any key, grouping, pairing or row structure
```

`grep -c exempt` over both transcripts together: **0**.

Both guard scripts are UNMODIFIED — confirmed by md5sum, unchanged
across this whole task:
`check_no_spelling_keys.py` `1d6aba67cbcdb021c3bdfd7f40fd2020`,
`check_dashboard_js_no_spelling.py` `2e4cd1f088d8375342fcfa82ce88b462`.

THE SPELLING BAN, pasted verbatim as required by the brief: "No
operator token may appear in ANY key, grouping, pairing, row
structure, candidate selection, or comparison scope, anywhere in this
line — not in matching, not in 'which pairs get compared', not in
report rows, not in dropdowns. The candidate set for comparison comes
from machine-form evidence (clusters, connections, type pairs) or from
ratified intention — never from the token. The token appears exactly
once per unit: as a display label on the member." Nothing this task
touched groups, pairs, selects or compares by an operator token — the
two retirement functions match nav buttons by their `data-t` id
(`"coverage"`, `"stats"`), an internal DOM attribute the tab code
itself assigns, never a spelling drawn from the corpus.

### 3.5 Flagged for the owner — naming and coverage, not decided here

Per the brief: naming is the owner's, and this task does not rename or
restructure panes on its own authority. Two things worth his eyes,
neither blocking the two fixes above:

- The CORE (`CORE_0_3_5_10_dashboard.md`) was ALREADY updated, before
  this task started, to name six sub-nodes — `unit_viewer`,
  `selector`, `opcode_index`, `coverage_view`, `stats`, `chronology` —
  and its own "definition" section already says "Five panes ... and
  (6) a chronology." So the five-vs-six gap log_183 flagged as a live
  problem had, by the time this task ran, already been closed IN THE
  PLAN; what this task fixed was the CODE catching up to that plan
  (retiring the two duplicate tabs).
- What the reconciled tab bar actually shows is **six tabs that do
  not map one-to-one onto those six sub-node names**: the `units` tab
  bundles BOTH `unit_viewer` (pane 1) and `selector` (pane 2) into one
  screen (existing since task 68, not something this task changed),
  and a SEVENTH concept — a "what was asked for" checklist/status
  view (`spec`/`5 · what was asked for`, `drawSpec()` in
  `dashboard_join.js`) — sits in the tab bar as its own tab without
  being one of the CORE's six named sub-nodes at all. Nothing here
  needed to move for this task's two fixes (the tab COUNT is right,
  eight became six, matching the coordinator's own arithmetic), but
  whether `spec` should be a sub-node of its own, folded into another
  pane, or left as an unnamed extra, is a naming question this task is
  not authorized to answer.

---

## 4. File inventory

### 4.1 Airlock (part a)

| file | change |
|---|---|
| `Airlock/airlock` | `known_instances(paths)` (new, the one discovery scan); `other_busy_instances_line(paths)` (new); `Doctor.check_instances` refactored to call `known_instances` instead of re-listing; `_render_status` prints the header |
| `Airlock/instance.sh` | `airlock_instance_list()` extended to scan `<runs>/*`; `airlock_other_busy_instances(root, current)` (new) |
| `Airlock/progress.sh` | `print_other_instances()` (new), called from `snapshot()` |
| `Airlock/DevComms/log_004_cross_instance_status_header.md` | new — Airlock's own record |
| `Airlock/instances/t82.conf` | new, gitignored, per-machine — the proof instance's config |

### 4.2 The dashboard (part b)

| file | change |
|---|---|
| `PseudoCoupHQ/Research/op_pipeline/dashboard_pane4.js` | retires the join's draft `coverage` tab once its own attaches |
| `PseudoCoupHQ/Research/op_pipeline/dashboard_pane5.js` | retires the join's draft `stats` tab once its own attaches, deferred until the join's own mount promise resolves |
| `PseudoCoupHQ/Research/op_pipeline/dashboard_loader.js` | one explicit final header/index repaint when `indexAll()`'s own promise resolves |
| `PseudoCoupHQ/Research/op_pipeline/dashboard_full_harness.html` | new — test rig only, loads every script `dashboard.html` loads, for measuring the tab bar and header without the OS folder dialog |
| `PseudoCoupHQ/DevComms/screens/log_188/*.png` | 5 screenshots, listed in §3.3 |
| `PseudoCoup/.claude/launch.json` | the Browser pane's own preview config for `dashboard_test_server.py` (unrelated repo, but this is where the tool reads it from) |

### 4.3 Unchanged, confirmed by git log

`dashboard_join.js`, `dashboard.html`, `check_no_spelling_keys.py`,
`check_dashboard_js_no_spelling.py`. Task 77's `dashboard_ouro.py` and
task 79's `term.py` are running concurrently in the same repo (both
visible in the daemon's own commit history alongside this task's
files) and neither touches any file this task owns.

---

## 5. What was measured but not changed

- The `spec` tab's own checklist text (`drawSpec()` in
  `dashboard_join.js`) still says chronology is "not built — task 76",
  which is stale now that pane 6 exists. Out of scope for this task's
  two named fixes and not part of what log_182's coordinator note
  flagged — left as found rather than rewritten on the side.
