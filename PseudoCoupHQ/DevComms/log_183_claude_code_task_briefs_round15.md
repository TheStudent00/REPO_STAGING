# log 183 — task briefs for Claude Code, round 15

Date: 2026-09-03. OPUS default. ONE AIRLOCK INSTANCE PER TASK.

## WHO WROTE THIS, AND WHAT THAT CHANGES

**These briefs were written by the Claude Code coordinator, not by
the owner.** the owner asked for them in his own words: "we dont have enough
session usage for me to request new tasks from the Claude Cowork
conversation. if you want to try for Round 15 tasks and launch them,
thatd be appreciated." Every other round's briefs came from the owner.

What that changes, and it binds every task below:

- **Nothing here is a ruling.** Every task is drawn from a row the
  planning tree already marks **planned**, or from a defect a round-14
  log already measured and named. Where a task would need a decision
  that is the owner's — architecture, ontology, naming — it is FLAGGED in
  the task's own report, never decided, exactly as if the owner had written
  the brief.
- **The one exception the owner stated himself**, and the round's second
  headline: `Ourobrowser` — "the browser allows python
  to be run locally natively within the browser. id like to see the
  dashboard written to run in it." That is task 77.

## WHAT EACH TASK IS DRAWN FROM (so nothing here is invented)

| task | drawn from |
|---|---|
| 77 | the owner's request, quoted above |
| 78 | log_168 §5.3 finding 2 — 2,862 units disproved by a wrong destination rule; the CORE says "planned, round 14" and round 14 did not reach it |
| 79 | log_169 §5.3 — the layer-5 text is not a function of the unit for 1,479 of 26,594; CORE_…_normalize says "REPAIR IS PLANNED FOR ROUND 14" |
| 80 | log_170 — render_back refuses 13,027 units for want of a conditional template |
| 81 | graph CORE realization rows "diary (every other compiler)", "coverage (cpp, rust, swift)", "super_ops (cpp, rust, swift)" — all **planned**; priced in log_175 §6 |
| 82 | the owner hit it today ("what is running and why cant i see it in Airlock status?"); plus log_182's coordinator note (the tab bar and the header count) |
| 83 | the term and pool nodes, re-run over what 78/79/80 change |
| 84 | the bank, as every round |

## STANDING REQUIREMENTS

All of log_158's binding rules stand and are unchanged: code carries
the node's name; a shape the tree lacks goes into the CORE first with
provenance, then PROGRESS, then code; nothing reaches the owner that a CORE
or AgentMemory already answers; PROGRESS at the moment of progress
with its evidence link; the SPELLING BAN pasted verbatim into every
sub-agent brief; the unmodified guard in one process with
`grep -c exempt` = 0, no role keys and no field whitelists — a flagged
machine-form value gets a typed-object SHAPE; prove against the unit's
OWN ship code; zero regressions in the ruled sense; new files only;
evidence class per claim; every number with its population; every "I
verified X" pastes command and output, and an audit whose claims
outnumber its tool calls is rejected; reports in Appendix-B shape with
§5.1a LITERAL / GLOSS / ANALOGY labels.

**ADDED THIS ROUND, from the 2026-09-03 incident:** a task computing
over the diaries, the regen stores or the compiler graphs STATES ITS
MEMORY BOUND, runs a small sample first and pastes its peak resident
size, and caps live memory with a named abort. A miner that enumerated
every sub-path of 10,015,022 events reached 13.2 GB, exhausted the
machine's swap and was stopped by the coordinator; the bounded rebuild
ran in 487 MB. The rule is already settled in the graph CORE.

STATE AT HANDOFF (log_182 bank, commit `45beecd`): canon39 30,432
proved / 646 refused of 31,078; terms 26,594 proved / 3,134 disproved
/ 285 undecided / 419 no term; pool5 1,831 entries over 30,432
members, 490 multi-language; census6 49 producers; graphs go
10,393/63,797, cpp 112,364/386,065, rust 13,446/60,382, swift
71,106/192,655; go coverage 724 of 1,534 instrumented bodies;
super_ops_go 9,809 candidates; chronology 39 steps.

---

## TASK 77 — the dashboard in Ourobrowser (Opus; the owner's own request)

CONTEXT: `Ourobrowser` — `browser_engine.py` (the
scheme handler: `<script type="text/python">` is exec'd natively at
request time into a shared context and then REMOVED from the HTML
Chromium sees; every other `<script>` is stripped, so there is no
JavaScript at all; `onclick="python:expr"` is rewritten to a bridge
call), `bridge.py` (`PythonBridge.execute_python`, one way, return
value discarded), `Planning/` (the project has its OWN tree:
`node_0_3_engine`, `node_0_4_bridge`, `node_0_5_test_page`),
`DevComms/LLM_communication_protocol.md`.

WHAT THIS BUYS, measured against the current page: Ourobrowser's
Python has the filesystem natively, so the folder picker, the
IndexedDB handle, the opaque-origin finding and the Firefox gap all
disappear, and the join need not exist twice — `viewer_build.py`'s
Python join can be THE join, with no JS port.

THE ONE THING MISSING, and it is an Ourobrowser feature, not a
dashboard trick: **there is no path from Python back into the DOM.**
A `<script type="text/python">` cannot emit HTML (its text is replaced
by the empty string) and the bridge cannot answer.

WORK:
1. Read Ourobrowser's `Planning/CORE_0.md` and the engine and bridge
   nodes IN FULL. Design the SMALLEST engine additions that let a page
   be rendered by Python — the obvious two are (a) a python block may
   emit HTML in place of itself, (b) the bridge may push HTML into a
   named element. Write the design into Ourobrowser's own tree FIRST,
   with provenance, as its nodes' CORE and PROGRESS require. NAMING
   AND ARCHITECTURE ARE DEE'S: implement under working names, put
   every name and every shape choice in a "for the owner's ruling" section
   of your report, each changeable in one place.
2. Implement in `Ourobrowser` (the owner's project, and this
   capability is what he asked for). Keep `test_page.html` working —
   run it before and after and paste both.
3. Build the dashboard for Ourobrowser in
   `PseudoCoupHQ/Research/op_pipeline`: a page plus a
   Python module that reads the artifacts with `open()` and renders
   the panes. REUSE the existing join — state which functions of
   `viewer_build.py` / the pane builders are called rather than
   copied, and prove the reuse by naming them. All six panes if they
   fit the budget; if not, panes 1, 2 and 5 first, and say plainly
   which are not yet ported. Every pane keeps its population line
   ("N units read from M files, opened at HH:MM").
4. Prove it RUNS: launch Ourobrowser on the page, screenshot every
   pane, paste the terminal output, state the first-paint time and the
   peak resident size of the Python side. The existing
   `dashboard.html` is NOT edited or retired — the two coexist and the
   log says how they differ.
5. Guards: `check_no_spelling_keys.py` unmodified over any JSON;
   `check_dashboard_js_no_spelling.py` over any JS that remains; a
   grep proving no operator token is a key in the Python renderer.

## TASK 78 — the runtime answer register, and the panic-path callees (Opus)

CONTEXT: log_168 §5.3 (`destination_rules` rule 4 says a transfer into
the runtime writes the accumulator; the float lowerings answer in
`%xmm0`, so **2,862 units** carry a stored term asserting the transfer
changed nothing, and the reference disproves all of them — the fix
named there is the archive index's own 36-name runtime set plus a
canon rebuild, because `term.relink` checks its re-run against the
stored ledger row for row); log_167 (the 36 callee names and their
attachment; the **196** callers not attached — go 170 and rust 26
panic paths, which no builtins archive defines); the CORE
`node_0_3_5_3_ledger/node_0_3_5_3_3_destination_rules/`.

WORK: correct the destination rule so a runtime transfer writes what
the ATTACHED CALLEE's own answer register is (read from the callee
arch unit, not asserted); handle the panic-path callers by their own
named rule or a named refusal — they are go's and rust's own runtime,
not a builtins routine, and what they are is a shape question: put it
in the CORE first. Rebuild the ledgers and the wrapped texts into
`canon40_*` through `canonical_form.py`, gate with `gate.py`, and
report proved / refused per population against canon39's 30,432 / 646,
every movement with its cause. The 2,862 are the expectation to test,
not to assume.

## TASK 79 — the layer-5 text as a function of the unit (Opus)

CONTEXT: log_169 §5.3 — a second walk of the same rule over the same
26,594 terms prints a different text for **1,479** of them, because
`z3.simplify` orders a commutative operator's arguments by internal
node identity, which depends on what the process built earlier; the
positional renaming follows and the symbols swap. Round 14 implemented
the obvious repair as a probe and MEASURED it insufficient (299 of
1,292 collapsed, 39 of 582 c units still order-dependent), so the
ruled three steps were left unedited. `CORE_0_3_5_6_3_normalize.md`
carries the correction and "REPAIR IS PLANNED FOR ROUND 14".

WORK: make the normalizer a function of the unit. The likely shape is
a structural canonical ordering applied after simplification (order a
commutative operator's arguments by a key computed from the sub-term
itself — its printed form, its depth, its leaf set — never by z3's
node id), but MEASURE before ruling it in: the acceptance test is that
two walks in two fresh processes, and a walk in an order-shuffled
process, print the same text for **26,594 of 26,594**. Any residue is
named with its cause. The rule's steps are in the CORE: change them
there first, with provenance.

## TASK 80 — render_back's conditional template (Opus)

CONTEXT: log_170 — `Term.render_back` renders 5,909 of 26,040 proved
terms and refuses 20,131 across 17 named causes, the largest being
`if` at **13,027 units**: a conditional needs a comparison-plus-
conditional-move template the one fixed rule does not yet produce.
The CORE `node_0_3_5_6_5_render_back/` carries the six-part design
and five settled rules written in round 13.

WORK: extend the one fixed rule with the conditional template
(the shape the corpus itself uses — read it off the units, do not
invent one), assemble with `as`, round-trip through `objdump -d`, and
gate with `Gate.prove_wrapped` against each unit's OWN ship code
exactly as a wrapped text is. Report rendered / assembled / proved /
refused by cause against 5,909 / 5,873 / 20,131, and the collapse
(distinct rendered texts vs distinct layer-3 texts) over the same
population. A template that renders but does not prove is a finding,
not a result.

## TASK 81 — clang instrumented, the c and cpp diaries, cpp coverage and super_ops (Opus; its own Airlock instance)

CONTEXT: the graph CORE's three **planned** rows; log_175 §6's cost
page, measured: clang's sparse tree expands in 10 s, configure 11 s,
one region object cold 73 s / warm 9 s, **full clang build 1,316 s /
784 MB**, and the emission hook PROVED by an instrumented one-file
build; `graph_cpp.json` (112,364 nodes over 269 files, clang serving
both c and cpp); task 72's injector as the precedent.

WORK: instrument clang at the pin, diary the ORIGINAL corpus's c and
cpp units first (610 + 770 = 1,380 probes — recount from
`canon39_wrapped_c.json` / `_cpp.json` and paste), then extend to the
regenerated population only if the measured per-probe cost allows,
saying exactly how far you got. `Graph.coverage` joins them to
`graph_cpp.json`; report visited / total and the never-visited set BY
FILE. Then `Graph.super_ops` over the cpp diaries with the same stated
parameters go used, and the both-ways comparison against the
output-side miner's cpp candidates. MEMORY BOUND STATED, sample first,
peak resident pasted. Everything in your own instance, brought down
when done.

## TASK 82 — Airlock's cross-instance view, and the dashboard's tabs (smaller model acceptable)

CONTEXT (a): the owner today, verbatim: "what is running and why cant i see
it in Airlock status?" — `progress.sh` reports the DEFAULT instance,
and by the round-11 ruling every task runs in its own instance, so a
busy instance is invisible from the command he types. The fix belongs
in Airlock, generically for every caller.

CONTEXT (b): log_182's coordinator note — the tab bar carries eight
entries where the dashboard CORE numbers five, because each concurrent
pane module appended its own tab instead of replacing the draft pane
it realizes; and the header's arch-opcode count differs between
captures (122 vs 162) because `dashboard_join.js:1088` counts the live
index at render time, before or after the background load lands.

WORK: (a) in `Airlock` — a one-line header on
`progress.sh` naming any OTHER instance with a queued or running lane
(and `airlock status` likewise), so the default view can never say
"nothing running" while another instance is busy; prove it by bringing
up a second instance with a lane and pasting both views. Airlock's own
DevComms log records the change. (b) reconcile the dashboard's tabs to
the CORE's pane numbering, retiring the draft placeholders the new
modules replace, and re-render the header when the background index
completes; verify both by screenshot. Naming of the panes is the owner's —
if the CORE's five names do not cover what now exists, FLAG it.

## TASK 83 — term and pool over what this round changed (Opus; after 78, 79, 80)

WORK: `term66` / `name_census7.json` / `the_pool6.json` /
`the_families6.json` / `exception_families6.json` over the newest
canon and with the round's normalizer and render_back; the four term
states per population against 26,594 / 3,134 / 285 / 419 with every
movement's cause; the pool delta against 1,831 / 30,432 / 490 / 3 / 34
with computed causes; E00029's successor printed; the consistency line
pasted. If 78 lands a new canon, this runs on it and says so; if it
does not, this runs on canon39 and says that instead.

## TASK 84 — bank round 15 (smaller model acceptable)

WORK: as log_172 task 74 — verification transcripts, the authoritative
count line over the newest pool's population, `check_plans.py` pasted,
dashboards regenerated, PROGRESS off **planned** for everything
delivered with anything still planned named, the posterity message
containing the words "banked" and "round 15", and
`chronology_build.py --append` as the final step after the daemon
consumes it. The state page must say, in one line, that this round's
briefs were written by the coordinator and not by the owner.

---

Order: 77, 78, 79, 80, 82 in parallel; 81 when the machine is quiet
(it builds a compiler); 83 after 78, 79 and 80; 84 last.

DEE DECIDES, NOT THIS ROUND: Ourobrowser's engine and bridge names and
shapes (task 77 flags them); what a go or rust panic path IS in the
ledger's vocabulary (task 78 flags it); the dashboard's pane names if
five no longer covers what exists (task 82 flags it).
