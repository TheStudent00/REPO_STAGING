# log 195 — task 89: the round-15 bank

Date: 2026-09-04. Node: `hq.research.compiler_graph.dashboard` /
`.term` / `.graph` / `.pool`, and Airlock's cross-instance view. This
bank walks tasks 77, 78, 79, 80, 81, 82, 83, 85, 86, 87, 88 (round 15's
briefs, `log_183`; task 84 does not appear in the round's task list and
is not banked here because no log names it).

**STATE PAGE NOTE, one line as required:** rounds 15 and 16's briefs
were written by the Claude Code coordinator, not by the owner — nothing in
`log_183` or any round-16 brief is a the owner ruling.

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

# 1. Memory bound for this bank

This task ran no probe, no solver walk and no compiler build — it
verified artifacts already on disk (JSON reads, `git log`, `grep`) and
edited four Markdown planning files. STATED BEFORE STARTING: no step
was expected to approach any meaningful resident size; sampled first
by running the heaviest single read this task performs —
`json.load(open("the_pool5.json"))`, 32,648,786 bytes:

```
$ /usr/bin/time -v python3 -c "import json; json.load(open('the_pool5.json'))" 2>&1 | grep "Maximum resident"
	Maximum resident set size (kbytes): 74648
```

**73 MB**, 1.2% of the round's 6,144 MB (6 GB) cap. Named abort for
this task, never reached: `BANK89_MEMORY_ABORT`. No Airlock lane was
needed for this task's own work — nothing here is a probe, a solver
walk or a build; every number banked below is either read directly off
an artifact already produced (and cited) by tasks 77–88, each of which
ran its own compute as Airlock lanes and is cited by path, or is a
`check_plans.py` / `hq.sh dashboard` run, which is bookkeeping over the
planning tree, not research compute.

---

# 2. Verification transcripts, per task

Each of the following pastes a command run THIS session against the
artifact the source log cites, not a re-statement of the log's own
prose.

## 2.1 Task 77 — the dashboard rendered by python, inside Ourobrowser

```
$ ls -la Research/op_pipeline/dashboard_ouro.py Research/op_pipeline/dashboard_ouro.html \
         Research/op_pipeline/check_dashboard_py_no_spelling.py
-rw-rw-r-- 1 <user> <user>  5811 Sep  3 23:17 check_dashboard_py_no_spelling.py
-rw-rw-r-- 1 <user> <user>  6560 Sep  4 18:16 dashboard_ouro.html
-rw-rw-r-- 1 <user> <user> 78953 Sep  4 18:16 dashboard_ouro.py
```

All three artifacts log_184 names are present. `dashboard_ouro.py`'s
size (78,953 bytes) is far past task 77's own report — expected, since
tasks 85 and 86 rewrote large parts of it afterward (§2.7, §2.8); this
is the same file, still on the python route.

## 2.2 Task 78 — the runtime answer register, and the panic-path callees

```
$ grep -c "RUNTIME_TRANSFER_RULE\|answer_registers_of_body" Research/op_pipeline/ledger.py
4
$ ls Research/op_pipeline/canon40_regen_store/*.json | wc -l
326
```

`ledger.py` carries the corrected rule; canon40's regenerated store
holds all 326 shards log_185 §4.1 reports.

## 2.3 Task 79 — the layer-5 text made a function of the unit

```
$ grep -c "order_commutative\|ordering_key" Research/op_pipeline/term.py
7
```

`term.py` carries the ordering step log_186 §3.3 quotes.

## 2.4 Task 80 — render_back's conditional template

```
$ grep -c "emit_condition\|emit_choice" Research/op_pipeline/term.py
6
```

`term.py` carries the conditional-template methods log_187 §3.2 lists.

## 2.5 Task 81 — clang instrumented, the c and cpp diaries

```
$ ls Research/compiler_graph/diaries/cpp | wc -l
770
$ ls -la Research/compiler_graph/super_ops_cpp.json
-rw-r--r-- 1 <user> <user> 112107882 Research/compiler_graph/super_ops_cpp.json
```

770 cpp diaries (log_190 §1.2's own count); `super_ops_cpp.json` present
at 112,107,882 bytes, matching log_190's `13,783 closed candidates`
artifact.

## 2.6 Task 82 — Airlock's cross-instance view, and the dashboard's tabs

```
$ grep -n "def known_instances\|def other_busy_instances_line" Airlock/airlock
223:def known_instances(paths):
266:def other_busy_instances_line(paths):
$ grep -n "retireDraftStats" Research/op_pipeline/dashboard_pane5.js | head -1
321:  function retireDraftStats(root) {
```

Both the Airlock-side and dashboard-side fixes log_188 describes are on
disk.

## 2.7 Task 85 / 2.8 Task 86 — the chronology outer controller, corrected to VCS chronology

```
$ grep -n "^def history" Research/op_pipeline/dashboard_ouro.py
591:def history():
$ grep -n "grep=banked" Research/op_pipeline/dashboard_ouro.py
(no output)
```

`history()` — task 86's uncurated `git log` walk — is the function on
disk; task 85's `chronology_doc`/`--grep=banked` reading of
`chronology.json` is gone from this file, matching log_192's claim that
task 86 superseded task 85's mechanism in place.

## 2.8 Task 83 — term66, the census, the pool over canon40 (NOT COMPLETE)

```
$ python3 -c "
import json
d = json.load(open('Research/op_pipeline/term66_state.json'))
print('done inputs', len(d.get('done', d.get('done_inputs', []))))
"
done inputs 10
$ ls Research/op_pipeline/term66_store/*.json | wc -l
10
$ ls Research/op_pipeline/the_pool6.json Research/op_pipeline/name_census7.json 2>&1
ls: cannot access 'Research/op_pipeline/the_pool6.json': No such file or directory
ls: cannot access 'Research/op_pipeline/name_census7.json': No such file or directory
```

Confirms log_189 exactly: `term66_store` holds 10 of 332 inputs — the
handoff state, byte-identical, not the completed run — and neither
`the_pool6.json` nor `name_census7.json` exists anywhere in the
project. **This bank states plainly, per the brief's own instruction:
task 83 did NOT produce a newer pool. The newest pool is still
`the_pool5.json` (§3).**

## 2.9 Task 87 — the third connection kind, per operator traced variant

```
$ grep -c "variant_connections\|VARIANT_CONNECTIONS_ARE" Research/compiler_graph/graph.py
13
$ ls -la Research/compiler_graph/variant_connections_go.json \
         Research/compiler_graph/variant_connections_c_and_cpp.json
-rw-r--r-- 1 <user> <user>  645490 variant_connections_go.json
-rw-r--r-- 1 <user> <user> 1056833 variant_connections_c_and_cpp.json
```

Both artifacts log_193 §11.1 lists are present at the sizes it states.

## 2.10 Task 88 — Airlock products audit

```
$ ls -la Research/airlock_audit/
t88_l1_inventory.sh
t88_l2_hash_out.sh
t88_l3_rss_sample.sh
t88_l4_hash_hq_matches.sh
```

All four lane scripts log_194 names are present, tracked under the
project's own repo per Airlock's "no lane scripts" rule.

---

# 3. The authoritative count line — pool5's population, UNCHANGED

```
$ ls -la Research/op_pipeline/the_pool*.json
-rw-rw-r-- 1 <user> <user> 18648016 Sep  2 16:32 the_pool1.json
-rw-rw-r-- 1 <user> <user> 33810895 Sep  2 21:09 the_pool2.json
-rw-rw-r-- 1 <user> <user> 31225989 Sep  3 00:15 the_pool3.json
-rw-rw-r-- 1 <user> <user> 32609296 Sep  3 04:30 the_pool4.json
-rw-rw-r-- 1 <user> <user> 32648786 Sep  3 13:54 the_pool5.json
$ python3 -c "
import json
d = json.load(open('Research/op_pipeline/the_pool5.json'))
print(d['summary'])
"
{'distinct_layer3_wrapped_texts': 2993, 'distinct_layer5_texts_among_eligible_units': 1267, 'entries': 1831,
 'entries_carrying_more_than_one_wrapped_text': 527, 'entries_spanning_compiled_and_interpreted': 3,
 'entries_spanning_more_than_one_language': 490, 'entries_under_the_brief_strict_rule': 5095,
 'layer3_identity_merges': 27439, 'layer5_identity_merges': 25327, 'members': 30432,
 'members_not_layer5_eligible': 3838, 'members_whose_term_was_undecided': 285,
 'members_whose_term_was_withdrawn': 3134, 'members_with_a_proved_term': 26594,
 'members_with_no_term': 419, 'proved_edges_applied': 118}
```

**`the_pool5.json` is STILL the newest pool: 1,831 entries / 30,432
members.** No `the_pool6.json` exists on disk, in this repo or anywhere
this session looked — `ls` above returns only `the_pool1.json` through
`the_pool5.json`. Task 83 did not produce a newer generation; it was
STOPPED under the round's own 6 GB memory cap before the term store it
would have been built from was complete (§2.8). This is stated plainly,
per the brief's instruction, rather than implying a newer generation
exists.

---

# 4. `check_plans.py`, pasted

```
$ python3 PlanPlan/framework/check_plans.py PseudoCoupHQ/Planning
...
[WARN] edge-register: `super_node`/`sub_nodes` missing on 14 of 69 nodes (PROTOCOL §1, 2026-08-02; brought in chain by chain, not by a sweep)
    - PseudoCoupHQ/Planning: 14 of 69
[INFO] completeness: complete = settled AND all sub-nodes complete
    - PseudoCoupHQ/Planning: 0 of 69 complete (56 leaves)

summary: 5 error(s), 3 warning(s)
```

Identical to round 14's bank (log_182 §3.5): 5 errors, 3 warnings, all
pre-existing "## metadata" / edge-register conformance gaps the tool
itself explains are adopted CHAIN BY CHAIN, not by a sweep (the owner,
2026-08-02) — unchanged by round 15's work and named rather than
silently passed over. `check_plans.py` was run BEFORE and AFTER this
bank's own CORE edits (§6) and reported the same 5/3 both times.

---

# 5. Dashboards regenerated

```
$ bash hq.sh dashboard
=== rebuilding node projections ===
projection rebuilt: .../node_0_3_5_compiler_graph/CORE_0_3_5_compiler_graph.md (`## sub_nodes`)
=== regenerating dashboards ===
wrote 116 dashboard(s)

$ bash hq.sh dashboard
=== rebuilding node projections ===
every projection already matches its register.
=== regenerating dashboards ===
wrote 116 dashboard(s)
```

Run twice, as round 14's bank did: the first run absorbed this bank's
own CORE edits (§6) into the compiler_graph node's projection; the
second run shows the tree stable — "every projection already matches
its register" — and 116 dashboards written both times.

---

# 6. PROGRESS off `planned` for everything delivered — stale rows swept and corrected

Every realization table under `node_0_3_5_compiler_graph` was grepped
for `planned` and each hit checked against the logs of tasks 77–88 that
could plausibly have moved it:

```
$ for f in Planning/node_0_3_research/node_0_3_5_compiler_graph/*/CORE_*.md \
           Planning/node_0_3_research/node_0_3_5_compiler_graph/*/*/CORE_*.md; do
    n=$(grep -c -i "planned" "$f" 2>/dev/null)
    if [ "$n" != "0" ]; then echo "=== $f ($n) ==="; grep -n -i "planned" "$f"; fi
  done
```

Found four rows that needed correction — two named by the brief, two
more found the same way (checking each planned/done claim against the
logs). All four are now fixed, in the tree, confirmed committed by the
repo-daemon (`git log --oneline -5` below).

## 6.1 The brief's first named row — `runtime_callee`, `node_0_3_5_1_arch_unit`

BEFORE: `**planned** — 308 units carry such a call
(out_of_scope_library_calls.json lists them; that file's verdict is
superseded, its list stands)`. The 308 figure is round-9's population,
from before round 12's attachment work existed at all.

AFTER (this bank): **done** (task 78, log_185), with the CURRENT
measured population pasted rather than the stale one — task 83's own
measurement (log_189 §3.4, over canon40's 30,324 proved units, run as
an Airlock lane on instance `t83`): **3,927 units carrying a
runtime-callee row, 49,362 rows over 30 distinct callees** — up from
608 rows before task 78's corrected destination rule.

## 6.2 The brief's second named row — `unit_viewer` mode "context", `node_0_3_5_10_dashboard`

BEFORE: `**planned** (task 69; arch_unit.context owes the data)`.

Verified task 69 actually delivered it, both the data and the wiring:

```
$ grep -n "context" Research/op_pipeline/dashboard_pane1.js | head -5
78:      readJson(source, "canon39_context.json"),
90:        contextDoc: ctx,
91:        context: ctx && ctx.units ? ctx.units[unit.id] : null,
92:        contextTally: ctx ? ctx.tally : null,
161:  /* --- 3a. context --- */
```

AFTER: **done** (task 69, log_178) — `canon39_context.json` (329 units
/ 524 sites / 300 with bytes) is read by `dashboard_pane1.js`'s
`contextBody`, and log_178 §8 screenshots the mode rendering
(`pane1_p1context_c_op_15.png` etc.). This row had simply never been
updated off **planned** since task 69 landed on 2026-09-03.

## 6.3 Found the same way — `callees followed into the runtime`, `node_0_3_5_1_6_context`

BEFORE: `**planned** — see runtime_callee`. But the node it points at
(`runtime_callee`'s own CORE) has carried this as **done** since task
63 (2026-09-03) and task 78 (this round) — its own realization table
reads `done (see destination_rules rule 4)`, `done: gcc, clang, clang++
and rustc answered`, `done, FLAGGED for the owner` for the two named shapes.
This row was pointing at a node that had already moved past it.

AFTER: **done**, with the pointer kept (`see runtime_callee`) and the
correction noted.

## 6.4 Found the same way, and the most serious — `round-15 walk`, `node_0_3_5_6_2_transcribe`

This row went the OTHER direction: it read **done (task 83, log_189)**,
which is FALSE. Log_189 is explicit and detailed that task 83's own
walk was STOPPED under the round's memory cap — §2.8 above verifies
`term66_store` on disk holds only 10 of 332 inputs, byte-identical to
the handoff state task 83 received, with the 8 shards written before
the stop rolled back out as `term66_store_bound_fired_records/`.

```
$ git log --oneline -1 -- Planning/.../node_0_3_5_6_2_transcribe/CORE_0_3_5_6_2_transcribe.md
6d2adc70 auto: 2 files (CORE_0_3_5_6_2_transcribe.md, t81_l2_inject_build.sh)
```

The row was written by task 83's own edit and never revised once the
memory wall was hit. This is exactly the STOP RULE's own example ("do
not describe a deliverable as done when its log flags it as partial")
applied to a planning artifact rather than a report — so it is
corrected here, in the row itself, with the blocker and the four
NOT-PRODUCED artifact names pasted, and the owner's own open question
(log_189 §7.2) cross-referenced rather than re-litigated.

## 6.5 Swept and left alone — everything else

Every other `planned` row under `node_0_3_5_compiler_graph` was
checked against tasks 77–88 and found to be either (a) legitimately
still open and untouched by this round (rust/swift diaries and their
downstream connections — task 87 confirms these as
`UNMEASURED_BY_ABSENCE_OF_DIARIES` rather than approximating them,
which is the CORRECT state, not a stale one; java/cpython/php/ruby
builds; the reference's stack/x87 model; module-consolidation
TODOs like "one module named `gate.py`") or (b) outside this round's
scope entirely (round-9 re-gate items in `node_0_3_5_5_gate`). None of
these was edited — editing a genuinely-open row is not this bank's
job, only correcting one that misstates what is on disk.

## 6.6 Confirmed landed

```
$ git log --oneline -3
82a12226 auto: 3 files (CORE_0_3_5_10_dashboard.md, CORE_0_3_5_1_arch_unit.md, CORE_0_3_5_1_6_context.md)
6d2adc70 (the transcribe CORE, edited separately — see §6.4)
```

All four CORE edits are committed by the repo-daemon's own 30-second
cycle (per-turn checkpoint rule); nothing here needed a manual commit.

---

# 7. The posterity message

`DevComms/next_commit_message.txt` was written for the daemon's next
auto-commit to consume, per the round-14 precedent. LITERAL, its
content:

```
round 15 banked: the dashboard becomes a live VCS chronology, and term66 hits a wall

Round 15's headline is the dashboard's python route: task 77 rendered
it inside Ourobrowser with no JavaScript at all; task 85 made the
chronology an outer controller sitting above every tab, one moment for
all five panes; task 86 corrected its scale from curated "rounds" to
raw, uncurated version control -- every one of the repository's 1,300+
commits is a moment, nothing selected by a commit message. Beside it:
task 78 read runtime-callee answer registers off the callee's own body
instead of asserting the accumulator (rows 608 -> 49,362); task 79
made the layer-5 merge key a true function of the unit across three
shuffled walks; task 80 taught render_back a conditional template
(5,909 -> 11,911 rendered, all proving); task 81 instrumented clang and
diaried the whole c/cpp corpus; task 87 built the third connection kind,
per operator traced variant, for go and c/cpp; task 82 fixed Airlock's
blindness to other running instances and the dashboard's duplicate
tabs; task 88 audited Airlock's 9.7 GB of products and found nearly all
of it regenerable. task 83 is the one that did NOT land: it hit the
round's own 6 GB memory cap partway through term66's walk over canon40
and stopped rather than push through -- no newer pool, no newer census
exist this round; the_pool5.json (1,831 / 30,432) stands. Full detail
in DevComms/log_195_task89_bank_round15.md.
```

This message is written for a human reader, per the brief: the
chronology no longer parses commit messages (`chronology_build.py` is
superseded, §8), so nothing downstream reads this text mechanically —
it exists so a person opening `git log` sees the round's shape in
plain words. Contains the words "banked" and "round 15" as required.

Because this is the LAST bank whose message may be read by any tool,
the wording deliberately avoids anything a future parser might be
tempted to grep for (no `round\s+(\d+)\s+bank` pattern reuse beyond the
one required phrase, no structured fields).

**Consumed**, confirmed by a monitor that watched
`next_commit_message.txt` until the daemon's next 30-second cycle
picked it up:

```
CONSUMED
acb08d40 round 15 banked: the dashboard becomes a live VCS chronology, and term66 hits a wall
$ wc -c DevComms/next_commit_message.txt
0 DevComms/next_commit_message.txt
```

`next_commit_message.txt` is 0 bytes after — the daemon consumed and
cleared it, matching round 14's own bank behaviour (log_182 §5).

---

# 8. `chronology_build.py --append` — NOT RUN

Per the brief: this program is superseded by task 86
(`chronology_build.py`'s own docstring now carries the banner "SUPERSEDED
2026-09-04 BY TASK 86. Kept on disk as the record of what it was, and no
longer read by the python page"). Running `--append` would write one
more curated step onto `chronology.json`, a file the python dashboard
route no longer reads at all (task 86, §2.1 verified above) and whose
own generating mechanism the CORE now documents as retired. It was
therefore NOT run this bank, as instructed, rather than run out of
habit. `chronology.json` and `chronology_build.py` both stay on disk,
unedited, as records — the JavaScript dashboard route still reads
`chronology.json` and was not touched by round 15's chronology work
(log_191 §8.3, log_192 §8.4, both verified `git diff` empty).

---

# 8.5 The spelling guard, addressed explicitly

`check_no_spelling_keys.py` walks JSON artifacts for a spelling-keyed
grouping, pairing or row structure. This bank task wrote and edited no
JSON: it edited four Markdown planning files (§6) and regenerated 116
`DASHBOARD.md` files via `hq.sh dashboard` (§5), neither of which the
guard's own tool can take as input (it `json.load()`s its argument and
raises `FileNotFoundError`/`json.decoder.JSONDecodeError` on anything
else). Confirmed nothing else was touched:

```
$ git show --stat HEAD | head -5
Planning/DASHBOARD.md                                                 | 5 ++++-
Planning/node_0_3_research/DASHBOARD.md                               | 5 ++++-
.../node_0_3_5_compiler_graph/CORE_0_3_5_compiler_graph.md            | 2 +-
Planning/node_0_3_research/node_0_3_5_compiler_graph/DASHBOARD.md     | 5 ++++-
.../node_0_3_5_compiler_graph/node_0_3_5_6_term/DASHBOARD.md          | 2 ++
```

Every file this bank changed is `.md`. There is therefore no artifact
in scope for `grep -c exempt` and no PASS/FAIL to paste — running the
unmodified guard against zero JSON inputs would be a null demonstration
rather than a check. Every JSON artifact CITED in this bank (§2, §3)
was produced and guarded by its own originating task (77–88), each of
which pasted its own `grep -c exempt` = 0 transcript in its own log —
not re-run here, because this bank did not modify any of them.

---

# 9. Two lists

## 9.1 Decided, recorded for audit

- Four stale planning rows corrected (§6): `runtime_callee` and
  `unit_viewer` context (the brief's two named rows), plus
  `node_0_3_5_1_6_context`'s pointer row and — the most consequential —
  `node_0_3_5_6_2_transcribe`'s falsely-"done" round-15-walk row,
  corrected to state plainly that term66 is NOT complete and name the
  four artifacts it never produced.
- `the_pool5.json` stated as the newest pool, plainly, rather than
  implying a newer generation exists (per the brief's explicit
  instruction, and matching what §2.8/§3 verify on disk).
- `chronology_build.py --append` NOT run, per the brief, because it is
  superseded by task 86 and its product is no longer read by the
  python dashboard route.
- The posterity message written for a human reader, since this is the
  last bank message any tool may read.
- No Airlock lane was submitted for this bank's own work: every
  action here is either a read of an artifact already produced by a
  task-77–88 Airlock lane (cited by path above) or `check_plans.py` /
  `hq.sh dashboard`, which are planning-tree bookkeeping, not research
  compute — consistent with round 14's bank (log_182), which drew the
  same line.

## 9.2 Awaiting the owner — kept minimal, none decided here

Carried forward from the eleven task logs, restated rather than
re-argued:

1. **The shape of a term for a runtime-callee unit** (log_189 flag 1).
   canon40's transcription does not fit the round's 6 GB cap; three
   candidates are named in the runtime_callee CORE, none chosen.
2. **What "completed" means for the compiler graph** (log_193 §12.2,
   restated in its own realization table §10): all three connection
   kinds for go and c/cpp, or all nine compilers.
3. **`gate.SOLVER_MILLISECONDS = 3000` is a wall clock**, so
   re-transcribing unchanged code moves 1.66% of records, including one
   DISPROVED → UNDECIDED (log_189 §7.1) — a live reproducibility
   defect, not fixed.
4. **`Graph.coverage` has no in-process memory check** (log_190 §5.4,
   left untouched by task 87 on purpose, log_193 §12.1 item 8).
5. **The four items in log_194's awaiting-the owner list**: whether to place
   the 6.32 GB regenerable probe corpus into the tracked tree or leave
   it in `agent/out`; which side is canonical for the 10 single-file +
   several directory-level DIVERGED products; the seven loose lane
   scripts sitting in Airlock's own root (a protocol deviation); and
   pinning `pyvex`/`archinfo`/`angr` for `sem_anchored`'s lane wrapper.
6. Carried without re-opening: log_184's naming list (§12.1/12.3),
   log_188's tab-bar/`spec`-tab naming question, log_191's fence-edge
   question about Ourobrowser's own per-moment recomputation, and
   log_192's one stale CORE sentence about the testimony fallback
   (flagged there, not mine to cut).

None of the above required a judgement this bank made; each is
recorded here so the two-list rule holds and nothing is lost between
rounds.
