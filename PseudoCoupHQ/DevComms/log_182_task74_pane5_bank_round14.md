# log 182 — task 74: pane 5, and the round-14 bank

Date: 2026-09-03. Node: `hq.research.compiler_graph.dashboard` (pane 5)
and the round-14 bank over `hq.research.compiler_graph.graph` /
`.pool` / `.term`.

---

# 1. What was done, in plain words

Pane 5 (stats) was added to the dashboard: the four term states over
the full population, beside the census's top causes read from the
HIGHEST-numbered `name_census*.json` on disk — general by NUMBER, not
a hard-coded name, closing task 76's finding that a pane had read a
superseded generation. The round-14 bank was then walked: the four
compilers' graphs, go's coverage and super-op mining, the pool's
unchanged population, the plan checker, the dashboards, and the PLANNED
markers — followed by the posterity message, its daemon-consumed
commit, and the chronology append that joins it.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line — not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention — never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

---

# 2. Pane 5, the stats

## 2.1 What it draws

Two cards, over the full population:

- **the four term states**, read from `audit65.json`'s `term65` tally
  at open time: `proved`, `disproved` (labelled "disproved /
  withdrawn"), `undecided`, `no_term`.
- **the census's top causes**, the producers with no term builder,
  read from the highest-numbered `name_census*.json` present beside
  the page, sorted by `rows_blocked` descending.

The population line carries the pool's own count (`the_pool5.json`
summary: 1,831 entries / 30,432 members), the term tally's own record
count, and which census file was read.

## 2.2 The census-generation fix, made general

Task 76 (log_180) found pane 4/stats reading `name_census5.json` while
`name_census6.json` was already the highest generation on disk. Pane 5
does not hard-code a filename: `pickCensus()` in
`dashboard_pane5.js` lists `name_census*.json` via the folder handle's
own `entries()` (live page), or — on a handle without a listing API —
counts down from a ceiling trying each generation in turn; either way
it sorts by the NUMBER in the name (`name_census.json` itself counts as
generation 1) and reads the highest. `viewer_build.py`'s embed does the
analogous thing with `glob.glob` + `max(..., key=census_gen)` at build
time. I VERIFIED both pick `name_census6.json`:

```
$ /tmp/reconnect_venv/bin/python3 viewer_build.py 2>&1 | tail -1
pane 5 embedded verbatim from dashboard_pane5.js (12722 bytes) with audit65.json + the_pool5.json + name_census6.json (29272487 bytes)
```

## 2.3 Where the numbers came from — verified against source, not copied

```
$ python3 -c "
import json
d=json.load(open('audit65.json'))
print(d['term65'])
"
{'disproved': 3134, 'no_term': 419, 'proved': 26594, 'records': 30432, 'undecided': 285}

$ python3 -c "
import json
d=json.load(open('the_pool5.json'))
print(d['summary']['entries'], d['summary']['members'])
"
1831 30432
```

## 2.4 A naming collision found and fixed by running the page

The first draft of `dashboard_pane5.js` used id `#t-stats`, button
`data-t="stats"` and label "5 · stats" — following pane 6's pattern
literally. Opening the actual snapshot (not just the guard) showed
`dashboard_join.js` ALREADY owns a core pane with `id="t-stats"` (nav
label "4 · stats") and a separate core pane labelled "5 · what was
asked for" — both pre-existing. My module's `attach()` bailed out
silently (`if (root.querySelector("#t-stats")) return;`), so the new
pane never appeared; `find "5 · stats"` returned no matches.

Fixed by renaming every id/class/data-t in `dashboard_pane5.js` to
`t-pane5stats` / `pane5-terms` / `pane5-causes` / `data-t="pane5stats"`
and the button label to "term & census stats — pane 5" (the same
precedent pane 4 used — "compiler graph & coverage — pane 4" — for a
number the core nav had already taken). This is why the brief's
render-count-honesty guardrail matters: the guard alone (spelling-ban)
would have passed either way; only running the built page found the
collision.

## 2.5 Guards, RUN — literal transcript

```
$ /tmp/reconnect_venv/bin/python3 check_dashboard_js_no_spelling.py dashboard_pane5.js
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_pane5.js -- no operator token is written as a literal, so none can be a key (0 named coincidences above)
$ echo EXIT=$?
EXIT=0

$ node --check dashboard_pane5.js && echo JSOK
JSOK

$ python3 -c "import ast; ast.parse(open('viewer_build.py').read())" && echo PY SYNTAX OK
PY SYNTAX OK
```

`grep -c exempt` over the guard's own output: 0 (the guard prints
"named coincidences", never "exempt"; grepped the transcript above,
0 hits).

The snapshot build's own guard (over the DATA it embeds, unmodified,
same run as the embed):

```
$ /tmp/reconnect_venv/bin/python3 viewer_build.py 2>&1 | head -2
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_snapshot_data.json -- no operator token in any key, grouping, pairing or row structure
```

## 2.6 Verified by running the page, and by screenshot

Chrome (system `google-chrome --headless=new`, CDP on a throwaway
`--user-data-dir`) navigated to `dashboard_snapshot.html` served over
a local `python3 -m http.server` (the direct `file://` open the live
page itself uses was tried first via the Browser pane and refused by
the pane's own file-preview limit on a 52 MB file; the http server was
used ONLY to drive the verification browser, not as part of the page's
own design — the page still asks once for the folder and reads via the
File System Access API with no server, per the owner's ruling, when opened
normally). The nav button read "term & census stats — pane 5"; clicking
it rendered:

| state | members | share |
|---|---:|---:|
| proved | 26,594 | 87.4% |
| disproved / withdrawn | 3,134 | 10.3% |
| undecided | 285 | 0.9% |
| no term | 419 | 1.4% |
| records (all four states) | 30,432 | 100.0% |

— an exact match to §2.3's source read. Population line read
"population: 1,831 entries / 30,432 members (the_pool5.json summary)
· term states over 30,432 records (audit65.json) · census read from
name_census6.json". The top-causes table's first rows: `flag_pair ·
test,js` 424 rows blocked, `flag_pair · cmp,jae` 153, `flag_pair ·
cmp,jbe` 126, `flag_pair · test,jl` 122 — matching `name_census6.json`'s
own `entries` sorted by `rows_blocked` descending.

Screenshot saved: `DevComms/screens/log_182/pane5_stats.png` (1400×911
PNG, 123,589 bytes).

## 2.7 Files

New: `Research/op_pipeline/dashboard_pane5.js`.
Edited (additive only): `Research/op_pipeline/dashboard.html` (one
`<script src="dashboard_pane5.js"></script>` line), `Research/op_pipeline/viewer_build.py`
(one `PANE5` path constant, one embed block mirroring pane 6's, one
status-print line — nothing above those additions changed).
Regenerated: `Research/op_pipeline/dashboard_snapshot.html`,
`dashboard_snapshot_data.json`.

---

# 3. The bank

## 3.1 Round 14's grouping artifacts, enumerated from logs 174/175/177/181, verified against disk

From log_174 §8 (task 71, the four graphs):

```
$ ls -la graph_go.json graph_cpp.json graph_rust.json graph_swift.json \
       graph_go_lapone.json report_task71.json query_task71.json \
       coverage_go_summary.json guard_task71.txt
-rw-rw-r-- 1 <user> <user>       600 Sep  3 18:47 coverage_go_summary.json
-rw-rw-r-- 1 <user> <user> 331704231 Sep  3 18:41 graph_cpp.json
-rw-r--r-- 1 <user> <user>  49278033 Sep  3 18:40 graph_go.json
-rw-rw-r-- 1 <user> <user> 126304023 Sep  3 18:31 graph_go_lapone.json
-rw-rw-r-- 1 <user> <user>  61987708 Sep  3 18:40 graph_rust.json
-rw-rw-r-- 1 <user> <user> 165106660 Sep  3 18:41 graph_swift.json
-rw-rw-r-- 1 <user> <user>       416 Sep  3 18:43 guard_task71.txt
-rw-rw-r-- 1 <user> <user>     18744 Sep  3 18:39 query_task71.json
-rw-rw-r-- 1 <user> <user>     23956 Sep  3 18:47 report_task71.json
```
All nine present. md5 of the four graphs (recorded here as the round's
own record; not compared against a prior hash since this task did not
edit them):
```
71405afd56f3f5de41539c5c2c17c4b5  graph_go.json
5019da1619979a3412c1d527897cbc05  graph_cpp.json
0d381019cf580b77149affb30bdd784c  graph_rust.json
7e94074f6569a9497beb0224c18b76f0  graph_swift.json
```

From log_177 §8.1 (task 75, super-ops):

```
$ ls -la super_ops_go.json super_ops_go_top20.txt \
       super_ops_go_discriminating10.txt super_ops_comparison_go.json \
       coverage_go2.json report_super_ops.py guard_task75.txt
-rw-rw-r-- 1 <user> <user> 515160866 Sep  3 19:14 coverage_go2.json
-rw-rw-r-- 1 <user> <user>       346 Sep  3 19:32 guard_task75.txt
-rw-rw-r-- 1 <user> <user>     14568 Sep  3 19:31 report_super_ops.py
-rw-rw-r-- 1 <user> <user>   3480700 Sep  3 19:32 super_ops_comparison_go.json
-rw-rw-r-- 1 <user> <user> 103597545 Sep  3 19:30 super_ops_go.json
-rw-rw-r-- 1 <user> <user>     43636 Sep  3 19:31 super_ops_go_discriminating10.txt
-rw-rw-r-- 1 <user> <user>    101071 Sep  3 19:31 super_ops_go_top20.txt
```
All seven present, sizes matching the log (103.6 MB / 515 MB as
claimed). `super_ops_go.json` and `coverage_go2.json` are gitignored,
per §8.3a — confirmed:
```
$ grep -n "super_ops_go.json\|coverage_go2.json" PRIVATE/PseudoCoupHQ/.gitignore
44:Research/compiler_graph/super_ops_go.json
45:Research/compiler_graph/coverage_go2.json
```
Both were read IN PLACE for this bank (§3.2 below), per the brief.

From log_175 (task 72, the go diaries and coverage) and log_181
(task 73, pane 4): the diary and instrumentation artifacts these logs
built on (`diaries/go/*.txt`, `t72/diary_targets_all.json`,
`coverage_go.json`, `graph_go_files.json`,
`graph_{cpp,rust,swift}_files.json`, `coverage_go_files.json`) were
NOT touched by this task; their presence is implied by task 75/73
reading them successfully (recorded there), and this bank did not
re-open them — read-only carry-forward, named rather than re-verified,
since neither pane 5 nor the bank line reads them directly.

## 3.2 The authoritative count line — pool5's population, unchanged this round

```
$ python3 -c "
import json
d = json.load(open('the_pool5.json'))
print(d['summary'])
"
{'distinct_layer3_wrapped_texts': 2993, 'distinct_layer5_texts_among_eligible_units': 1267,
 'entries': 1831, 'entries_carrying_more_than_one_wrapped_text': 527,
 'entries_spanning_compiled_and_interpreted': 3, 'entries_spanning_more_than_one_language': 490,
 'entries_under_the_brief_strict_rule': 5095, 'layer3_identity_merges': 27439,
 'layer5_identity_merges': 25327, 'members': 30432, 'members_not_layer5_eligible': 3838,
 'members_whose_term_was_undecided': 285, 'members_whose_term_was_withdrawn': 3134,
 'members_with_a_proved_term': 26594, 'members_with_no_term': 419, 'proved_edges_applied': 118}
```

1,831 entries / 30,432 members; terms 26,594 proved / 3,134
disproved-withdrawn / 285 undecided / 419 no term. This task did not
regenerate the pool (no upstream input changed it); the line is
UNCHANGED this round, confirmed by direct read, not carried by
assertion.

## 3.3 The graph line

Four compilers' nodes/edges, verified directly off each `graph_*.json`
(§2.3 method, same command form):

```
$ python3 -c "
import json
for lang,f in [('go','graph_go.json'),('cpp','graph_cpp.json'),('rust','graph_rust.json'),('swift','graph_swift.json')]:
    d=json.load(open(f))
    c=d['counts']
    print(lang, c['nodes'], c['edges'], 'nodes_len=',len(d['nodes']),'edges_len=',len(d['edges']))
"
go 10393 63797 nodes_len= 10393 edges_len= 63797
cpp 112364 386065 nodes_len= 112364 edges_len= 386065
rust 13446 60382 nodes_len= 13446 edges_len= 60382
swift 71106 192655 nodes_len= 71106 edges_len= 192655
```

Go coverage, read directly off `coverage_go2.json` (in place, 515 MB,
gitignored):

```
$ python3 -c "
import json
d=json.load(open('coverage_go2.json'))
print('visited', d['instrumented_visited_by_at_least_one_probe'])
print('instrumented', d['population_instrumented'])
print('never_visited', d['never_visited_count'])
"
visited 724
instrumented 1534
never_visited 810
```
724 + 810 = 1,534 — internally consistent.

Super-op candidates, read directly off `super_ops_go.json` (in place,
104 MB, gitignored):

```
$ python3 -c "
import json
d=json.load(open('super_ops_go.json'))
print(len(d['candidates']), d['populations']['candidates_after_closure'])
print(d['parameters'])
"
9809 9809
{'min_length': 3, 'min_support': 2, 'subject': 'probe_own', 'collapse_repeats': True,
 'max_length': 12, 'max_runs_per_level': 2000000, 'memory_ceiling_mb': 6144,
 'support_is_counted_in': 'distinct probes', 'closure': 'closed contiguous runs only'}
```

The strict comparison, read directly off `super_ops_comparison_go.json`:

```
$ python3 -c "
import json
d=json.load(open('super_ops_comparison_go.json'))
for k in ['output_side_with_a_graph_counterpart_strict','output_side_with_a_graph_counterpart_loose',
          'graph_candidates_without_an_output_side_counterpart']:
    v=d[k]; print(k, v if not hasattr(v,'__len__') else len(v))
"
output_side_with_a_graph_counterpart_strict 0
output_side_with_a_graph_counterpart_loose 59
graph_candidates_without_an_output_side_counterpart 5330
```
Strict 0/59, matching the brief's stated line exactly; loose 59/59;
5,330 of 9,809 graph candidates carry no output-side counterpart.

## 3.4 Prior artifacts untouched

The four `graph_*.json` md5s (§3.1) were computed fresh this task and
are recorded here as this round's own record — this task performed no
edit on any of these files (the only files this task WROTE are named
in §2.7 and this section), and `git log` over the working tree for
this session shows no commit touching `graph_*.json`,
`super_ops_go.json`, `coverage_go2.json`, `the_pool5.json`, or
`audit65.json` — confirmed:

```
$ git log --oneline --since="2026-09-03 19:30" -- Research/compiler_graph/graph_go.json \
    Research/compiler_graph/super_ops_go.json Research/op_pipeline/the_pool5.json \
    Research/op_pipeline/audit65.json
(no output)
```

## 3.5 The plan checker

```
$ python3 PRIVATE/PlanPlan/framework/check_plans.py PRIVATE/PseudoCoupHQ/Planning
...
[WARN] edge-register: `super_node`/`sub_nodes` missing on 14 of 69 nodes (PROTOCOL §1, 2026-08-02; brought in chain by chain, not by a sweep)
    - PseudoCoupHQ/Planning: 14 of 69
[INFO] completeness: complete = settled AND all sub-nodes complete
    - PseudoCoupHQ/Planning: 0 of 69 complete (56 leaves)

summary: 5 error(s), 3 warning(s)
```
All 5 errors and 3 warnings are the pre-existing "## metadata" /
edge-register conformance gaps the tool itself explains are adopted
CHAIN BY CHAIN, not by a sweep (the owner, 2026-08-02) — unrelated to this
round's work, unchanged by it, and named rather than silently passed
over.

## 3.6 Dashboards regenerated

```
$ bash hq.sh dashboard
=== rebuilding node projections ===
every projection already matches its register.
=== regenerating dashboards ===
wrote 116 dashboard(s)
```
(Run twice this task: once before the PROGRESS edits, once after —
both produced "wrote 116 dashboard(s)".)

## 3.7 PROGRESS off **planned** for everything delivered

```
$ grep -n -i "planned" .../node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md
198:| `unit_viewer` mode "context" | nothing — constant bytes are not stored per unit | **planned** (task 69; `arch_unit.context` owes the data) |

$ grep -n -i "planned" .../node_0_3_5_9_graph/CORE_0_3_5_9_graph.md
239:| build (java, cpython, php, ruby) | nothing | **planned** |
243:| diary (every other compiler) | nothing; cost page in log_175 | **planned** |
245:| coverage (cpp, rust, swift) | 0 probes — never-visited BY ABSENCE OF MEASUREMENT | **planned** |
247:| super_ops (cpp, rust, swift) | 0 diaries | **planned** |
```
A new row was added to the dashboard CORE's realization table marking
`stats` **done** (task 74) — everything this task delivered is off
**planned**. Everything still `**planned**` above is owed work, not
this task's scope, named in §4 below.

---

# 4. The one-page state of the line (Appendix-B shape)

## 4.1 The seven-layer chain

1. **probe** — every ordered/level-2 input pair, per compiler, per
   operator/type signature.
2. **arch_unit** — the extracted instruction body a probe's binary
   carries, with its arrival contract and context.
3. **canonical_form** — `[sign, mant, expo]` decimal-string canon over
   a unit's proved output.
4. **ledger** — the row a probe writes: producer, destination rule,
   flag rule.
5. **reference** — the shared opcode table and machine-state model
   every term is built against.
6. **term** — `term65_store`: the z3 term over a unit's body, gated by
   task 64's verdicts, with the census of producers it cannot build
   for (`name_census6.json`, this round's highest generation).
7. **pool** — `the_pool5.json`: identity-merged entries over proved
   terms and banked edges. 1,831 entries / 30,432 members, unchanged
   this round (§3.2).

## 4.2 The graph line, per compiler (task 71/72/73/75, this bank)

| compiler | static (nodes/edges) | dynamic (diaries) | coverage | super_ops |
|---|---|---|---|---|
| go | 10,393 / 63,797 | 590 | 724 of 1,534 instrumented visited, 810 never | 9,809 candidates, both-ways strict 0/59 |
| cpp | 112,364 / 386,065 | 0 (priced, not run — log_175) | 0 probes | **planned** |
| rust | 13,446 / 60,382 | 0 (pin gap) | 0 probes | **planned** |
| swift | 71,106 / 192,655 | 0 (build cannot start) | 0 probes | **planned** |

## 4.3 The dashboard, six live panes + this round's pane 5

| pane | reads |
|---|---|
| 1 · arch-unit viewer | the unit index, unit bodies on demand |
| 2 · arch opcode index | the opcode → operator/signature index over all 31,078 units |
| 3 · compiler coverage | (shares pane 2/3's module — the selector) |
| 4 · compiler graph & coverage | `graph_<lang>_files.json`, `graph_<lang>_defs.json` on expand, `coverage_go_files.json`, one `Blob.slice` of `coverage_go2.json` per probe |
| 5 · stats (this task) | `audit65.json` (term states), `the_pool5.json` (population), highest `name_census*.json` (top causes) |
| 6 · chronology | `chronology.json` (39 steps as of this bank) |

## 4.4 This round's corrections

- **The 13 GB miner incident** (task 75): `Graph.super_ops` run
  unbounded took the machine's memory; redesigned to a streaming
  bounded shape (`memory_ceiling_mb`, `MemoryCeilingReached`) before
  the full run.
- **log_175's id-scheme mismatch**, found by task 75: the re-join
  command from log_175 §5.3, run verbatim, returned zeros — not a
  coverage collapse but a join-key mismatch, fixed by joining on the
  declaration coordinate.
- **174,159-vs-10,393**: named in log_174 as the difference between an
  earlier unconstrained walk's frontier count and the graph's actual
  node count — the constrained region, not a discrepancy in this
  round's own artifacts (recorded here per the brief's instruction to
  name it; this task did not re-derive the earlier figure).
- **14-vs-15 files**: log_181 §4.4 found the brief's "14 never-entered
  files" is actually 15 on direct count.
- **1,549-vs-1,534**: log_181's own named difference between
  `t72/inject_report.json`'s 1,549 instrumented targets and
  `coverage_go2.json`'s `population_instrumented` of 1,534 — 15 bodies
  counted as instrumented by the injector and not by the join, left as
  a frontier rather than smoothed over (confirmed again in §3.3's
  fresh read: `population_instrumented` is 1,534).

## 4.5 Owed work, named as next round's PLANNED items (no open calls for the owner)

- diaries for clang (priced in log_175, not run)
- rustc/swiftc fetch-and-pin (the corpus's pinned commit for each must
  be fetched before a diary can join)
- the interpreters' graphs (cpython, java, php, ruby — never
  attempted this round)
- `progress.sh` showing other instances' activity (a gap the owner hit
  directly)
- carried from round 13: destination rule 4 (float lowerings in
  `%xmm0`, 2,862 units), order-dependent layer-5 (1,479 texts),
  render_back's `if` template (13,027 units, 105/1,905 rendered),
  go/rust panic-path callees (196 units)
- pane 4's `unit_viewer` mode "context" (task 69; `arch_unit.context`
  owes the data)

---

# 5. The posterity message and its consuming commit

`DevComms/next_commit_message.txt` was written (1,713 bytes, first 5
lines):

```
round 14 banked: the graph, and pane 5

The graph is the round. Four compilers' source now has a node/edge
graph read directly off their own trees: go 10,393 nodes / 63,797
edges, cpp 112,364/386,065, rust 13,446/60,382, swift 71,106/192,655.
```

Contains the words "banked" and "round 14", per the brief (rounds 5
and 6 lacking bank commits, found by task 76's chronology build).

Polled `git log -1` until it was consumed — found on the first poll:

```
[1] 45beecdb2bbd390ace1f47ac1c8859fbe559c547 round 14 banked: the graph, and pane 5
FOUND CONSUMING COMMIT
```

`next_commit_message.txt` was 0 bytes immediately after — the daemon
consumed and cleared it, confirmed by direct read.

`chronology_build.py --append` was then run, AFTER the consuming
commit landed, per the brief's ordering:

```
$ python3 -c "import json; print(len(json.load(open('chronology.json'))['steps']))"
38
$ /tmp/reconnect_venv/bin/python3 chronology_build.py --append
append: 1 step(s) to build (38 carried forward unchanged)
  2026-09-03 45beecd9 round    {"census_producers": 49, "families": 34, "no_term": 419, ...}
...
wrote PRIVATE/PseudoCoupHQ/Research/op_pipeline/chronology.json  (39 steps: 13 with a recomputed number, 1 with a testimony number, 26 with no tracked artifact; 60621 bytes)
```

38 steps before, 39 after — the bank commit `45beecd` joined
`chronology.json` as a recomputed round step (13 recomputed, up from
12).

`viewer_build.py` was re-run after the chronology append so the
snapshot's embedded chronology and pane-5 data both carry this round's
close.

---

# 6. Complete file inventory

New:

- `Research/op_pipeline/dashboard_pane5.js`
- `DevComms/screens/log_182/pane5_stats.png`
- `DevComms/log_182_task74_pane5_bank_round14.md` — this file.

Edited, additive only:

- `Research/op_pipeline/dashboard.html` — one
  `<script src="dashboard_pane5.js"></script>` line.
- `Research/op_pipeline/viewer_build.py` — one `PANE5` path constant,
  one embed block (mirrors pane 6's `</body>`-append pattern), one
  status-print line.
- `Planning/.../node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md` —
  one realization-table row (`stats`, **done**, task 74).
- `Planning/.../node_0_3_5_10_dashboard/PROGRESS.md` — one dated entry.
- `Planning/.../node_0_3_5_compiler_graph/PROGRESS.md` — one dated
  entry under the node's single `# PROGRESS` heading.
- `DevComms/next_commit_message.txt` — written, then consumed and
  cleared by the daemon (0 bytes after).

Regenerated (not hand-edited):

- `Research/op_pipeline/dashboard_snapshot.html`,
  `dashboard_snapshot_data.json` (`viewer_build.py`, run three times
  this task — after the pane-5 fix, and again after the chronology
  append).
- `Research/op_pipeline/chronology.json` (`chronology_build.py
  --append`, 38 → 39 steps).
- 116 project DASHBOARD.md files (`hq.sh dashboard`, run twice).

Not touched (read only, in place, gitignored large ones read without
copying): `graph_go.json`, `graph_cpp.json`, `graph_rust.json`,
`graph_swift.json`, `super_ops_go.json`, `super_ops_comparison_go.json`,
`coverage_go2.json`, `the_pool5.json`, `audit65.json`,
`name_census6.json`.

---

# 7. Two lists

## 7.1 Decided, recorded for audit

- Pane 5's id/class/data-t were renamed off the pane-6 template
  (`t-stats` → `t-pane5stats`, label "5 · stats" → "term & census
  stats — pane 5") because the core join already owns nav slots 4 and
  5 ("4 · stats", "5 · what was asked for") — found by running the
  built page, not by the guard.
- The census file is picked by NUMBER (`glob` + `max(key=digits)` at
  build time; `entries()` + numeric sort, or a counting-down
  fallback, live), never by a hard-coded name, so the fix generalizes
  past this round's `name_census6.json`.
- `coverage_go2.json` (515 MB) and `super_ops_go.json` (104 MB) were
  read IN PLACE for the bank's verification reads rather than copied,
  per the brief.
- `chronology_build.py --append` was run strictly AFTER the posterity
  commit was confirmed consumed, per the brief's ordering — not
  before.

## 7.2 Awaiting the owner

Nothing structural. The owed work in §4.5 is recorded as next round's
PLANNED items on the CORE realization tables, not posed as an open
question.

## COORDINATOR NOTE (2026-09-03, after the bank) — two things visible on the page, recorded for round 15

Read off `DevComms/screens/log_182/pane5_stats.png` after the bank:

1. **The tab bar has eight entries where the CORE numbers five.** Beside the draft's `3 · compiler coverage` there is `compiler graph & coverage — pane 4` (task 73's module); beside `4 · stats` there is `term & census stats` (task 74's module); `6 · chronology` is task 76's. Each concurrent pane module appended its own tab rather than replacing the draft pane it realizes, because the concurrency rule told them to add and never rewrite. The panes are correct; the navigation is not yet the five-pane shape the owner numbered. Reconciling the tab set (one tab per CORE pane, the draft's placeholder panes retired) is round-15 work under the dashboard node, and the CORE's pane numbering is the owner's to confirm.

2. **The header line says `122 arch opcodes` while task 68's capture said `162`.** Both are counts the page computed at open; they differ by which file the header counted (to be found in `dashboard_join.js`), not by a change in the corpus (task 70's index holds 162). Named here so it is not read as a regression; the cause goes to round 15 with the tab cleanup.

   Located after writing the above (LITERAL, `dashboard_join.js:1088`):
   `Object.keys(state.opcodeIndex).length + " arch opcodes · pool "` — the header counts the live
   `state.opcodeIndex` at the moment the header is rendered. Task 70's full index lands in the
   background after first paint (log_176 §timing; log_179's rebuilt map), so a header rendered before
   that lands shows the partial map (122) and a header rendered after shows the full one (162).
   Hypothesis, not yet measured: re-rendering the header when the background index completes should
   make the two captures agree. To be verified in round 15 alongside the tab reconciliation.
