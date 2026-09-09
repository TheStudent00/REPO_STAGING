# log 214 — task t102: the bank of rounds 16–19 (tasks 89–99) and the
# arch_unit_oracle founding (o1–o4)

Date: 2026-09-06. Node: `hq.research.operator_equivalence` /
`node_0_3_1_operator_equivalence` (rounds 16–19, tasks 89–99) and
`hq.research.arch_unit_oracle` / `node_0_3_2_arch_unit_oracle`
(founding + tasks o1–o4). Written by the implementer resuming task
t102 after a usage-limit stop; the instance's own six lane logs
(`t102_l1_verify_artifacts` through `t102_l6_verify_205_210`) had
already run and hold the evidence this log banks.

**MISSING-INPUTS NOTE, stated plainly rather than silently worked
around:** at resume time neither the law file
(`.../862ba4e5.../scratchpad/LAW.md`) nor the original brief
(`task_t102_brief.md`) was present on disk anywhere under
`/tmp/claude-1000` — both are named by the resume note but neither
survived whatever cleared that scratchpad between runs. This bank was
therefore built from: (1) `DevComms/log_195_task89_bank_round15.md`,
read in full as the shape this task's resume note points at; (2) the
six `t102` lane logs already produced (the bank's own evidence); (3)
the sibling resume/brief files sitting beside the missing one in the
same scratchpad (`task_o6_resume.md`, `task_o7_brief.md`,
`task_t100_resume.md`, `task_t101b_brief.md`), whose conventions
(concurrency rule, DevComms numbering check, verifier tally, PROGRESS
entry, instance down) are stated identically across all four and are
taken as the law's content on that basis; (4) `CORE_0_3_research.md`
§8 for the address map. Nothing below required a judgement call that
the missing brief would plausibly have settled differently — this is
recorded so the substitution is visible, not asserted as equivalent to
having read the brief itself.

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

This task ran no probe, no solver walk and no compiler build. Its own
six lanes (`l0`–`l6`) did `git log`, `os.stat`, `grep` and text-mode
`check_conventions_log_claims.py --verify` passes over DevComms `.md`
files — the largest artifact any lane or this write-up opened is
`node_0_3_1_operator_equivalence/PROGRESS.md` at 3,697 lines / under
200 KB, and the largest DevComms log re-run is `log_209` at 68,346
bytes. None of this approaches the instance's own 3,072 MB (3g) bound,
stated in `t102.conf` as generous headroom over log_195's own measured
73 MB for a 32 MB pool-json load — this bank loads nothing of that
size. Named abort for this task, never reached: `BANK_T102_MEMORY_ABORT`
(the instance-level `ABORT` is the container's own OOM kill, observed
once below, on a DIFFERENT axis — see §4).

---

# 2. Verification, per task, from `t102_l1_verify_artifacts`

`t102_l1_verify_artifacts.sh` checked existence, size, and the git
commit that last touched each artifact tasks 89–99, the founding note,
and o1–o4 name. Full manifest: `Research/op_pipeline/lanes_t102/`
(`t102_manifest.json`, `t102_artifacts_result.json`); the table below
is a reading of that lane's own printed output, not a re-statement of
each task's own prose.

## 2.1 Round 16–19 (operator_equivalence)

| task | artifacts checked | result |
|---|---|---|
| 89 (round-15 bank) | `log_195`, four CORE edits' commit `8092f18d` | all present; this is round 15's own bank, cited as the prior state |
| 90 | `check_conventions_log_claims.py`, `t90_verify_six.json`, `t90_verify_log197.json`, `log_197` | all present |
| 91 | `t91_populations.py`, `t91_regate_run.py`, `t91_regate_store_attached_callees_fix` (332 shards), `t91_audit.json`, `t91_lost_proofs.json`, `t91_timeouts.json`, four `reference`/`gate` CORE and PROGRESS files, `log_196` | all present |
| 93 | `graphs_home.py`, `graph_compact.py`, `dashboard_graph_draw.py`, `guard_task93.txt`, `coverage_cpp_files.json` (6.77 MB), `coverage_go_files.json`, four `PseudoCoupGraphs/graph_<lang>.json`, `diaries/`, `log_198` | all present — `coverage_cpp_files.json` and `PseudoCoupGraphs/diaries` are `NOT_COMMITTED` (regenerable products, per the standing rule on what belongs in a repo) |
| 94 | `t94_read_bounds.py`, `t94_bounds.json`, `t94_recarve.py/.json`, `t94_analysis.py/.json`, `lineage_carve.py`, `log_199` | all present |
| 95 | four `arch_opcode_nodes_<lang>.json` (`PseudoCoupGraphs`), four `_summary.json`, `guard_task95.txt`, `graph.py`, `log_200` | all present |
| 96 | `t96_arriving_area.py`, `t96_onto_canonical_form.py`, `t96_canonical.json`, `t96_analysis.py/.json`, `t96_wrapped_texts.txt`, `t96_step.py`, `region36.py`, `canon36_universal.py`, `log_201` | all present |
| 97 | `probe97a_unit_cost.py`, `probe97b_flag_reason.py`, `term97_walk.py`, `report97_numbers.py`, `guard97_term_pool.py`, `term66_store` (332 entries), `term66_state.json`, `name_census7.json`, `audit66.json`, four term/pool PROGRESS files, `log_202` | all present; `the_pool6.json` confirmed **absent** — task 97 finished term66 (332 of 332, closing round-15's stop) but did not itself cut a new pool generation, so `the_pool5.json` (1,831 / 30,432, log_195 §3) is still the newest pool this bank can cite |
| 98 | `dashboard_stats.py`, `t98_probe_shapes.py`, `t98_settle.py`, `t98_render_check.py`, `t98_ouro_shots.py`, `dashboard_ouro.py` (117,517 bytes), `dashboard_ouro.html`, `t98_spelling_guard_transcript.txt`, 25 screenshots, `log_203` | all present |
| 99 | `term99_reason.py`, `check_conventions_log_claims.py` (same file as task 90's, now the shared verifier tool), `log_205` | all present |

## 2.2 arch_unit_oracle founding and o1–o4

| task | artifacts checked | result |
|---|---|---|
| founding | `Research/oracle/` (5 entries), `log_206_arch_unit_oracle_founding.md` | present |
| o1 | `cross1_length_one.py/.json`, `cross2_length_two.py/.json`, `log_207` | present |
| o2 | `single_opcode_units.py/.json/.md`, `unique_opcodes.py/.json/.md`, `log_208_claims_l10.json`, `log_208` | present |
| o3 | `compiler_operators_used.py/.json/.md`, `log_209_claims_final.json`, `log_209` | present; `o3.conf` itself is `OUT_OF_SANDBOX` (not mounted — instance configs are a host artifact, checked from the host, not from inside a sandbox) |
| o4 | `operator_variants_by_search.py/.json/.md` (4.2 MB json, 344 KB md), `log_210_claims_final.json`, `log_210` | present; `o4.conf` likewise `OUT_OF_SANDBOX` |

Headline numbers, read off the founding node's own `PROGRESS.md`
(current, not re-derived — the numbers already carry their own task's
citation):
- **o1** (cross_construction, length one/two): c and cpp build each
  other ~46–52%; every language builds 45–77% of rust and go; length
  two adds under 3.1% in any cell. **Cross_construction is FROZEN by
  the owner, 2026-09-06** — no language's single-opcode units can chain to
  build another's.
- **o2** (single_opcode_units): 162 unique arch-opcode mnemonics
  across nine languages, grouped by distinct body under two chaff
  rules; naming and chaff-rule choice both await the owner.
- **o3** (compiler_operators_used): every compiler uses every scalar
  operator its own corpus lowered, except cpp's alternative spellings,
  `<=>` (clang, swiftc) and `^` (rustc, sparse checkout); llvm and rust
  checkouts are sparse (codegen dirs only), flagged rather than
  treated as complete.
- **o4** (operator_variants_by_search): fully resolved by search alone
  — clang 17%, go compiler 22%, go stdlib 20%, rustc 6%, swiftc 11%,
  swift stdlib 9%; leftover dominated by call results, member access,
  inferred bindings, and declarations in other files.

---

# 3. The sweep, from `t102_l2_sweep`, `l3_context`, `l4_context2`, `l5_graph_core`

`t102_l2_sweep.sh` grepped every `PROGRESS.md` under
`node_0_3_1_operator_equivalence` and `node_0_3_2_arch_unit_oracle`
(73 files) for `planned`/`in-progress` (69 hits) and, for absence
spot-check, for `done` (223 hits, not reproduced here — its purpose
was only to confirm `done` rows exist to sanity-check the grep itself,
not to audit them).

**Reading the 69 `planned`/`in-progress` hits, not just listing them:**
`PROGRESS.md` is an append-only diary, unlike a CORE's `## realization`
table — a diary entry correctly says "planned" for the day it was
written even after a LATER entry in the same file closes it, because
old lines are never rewritten. Spot-checked directly (not assumed):

- `node_0_3_2_arch_unit_oracle/PROGRESS.md:13` ("Status: planned",
  the founding entry) and `:56` ("in-progress", task o3 opened) are
  both this exact pattern — line 13 is followed four bullets later by
  o1's own "done"; line 56 is followed ONE bullet later, same date, by
  "task o3 done" (line 57). Read in full: **no correction needed**.
- `node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/node_0_3_1_1_8_runtime_callee/PROGRESS.md`
  carries four `planned` hits (lines 22, 25, 66, 67) from 2026-09-03,
  each superseded later in the SAME file by task 63's "done" entries
  (round 15's bank, log_195 §6.1, already corrected the CORE table
  this diary's early lines pointed at). **No correction needed.**
- The graph CORE's own `## realization` table (`t102_l5_graph_core`,
  read in full) already states rust/swift variant connections, the
  four remaining language builds, their diaries, coverage and
  super_ops all as **planned — UNMEASURED BY ABSENCE OF DIARIES**,
  with the structural cause named (rust: promisor clone, no route out,
  absent pin; swift: three of five repositories not on this disk).
  This matches what rounds 16–19 actually did (95 built the
  arch-opcode-node from SOURCE for all four regions; nothing in 89–99
  touched rust/swift instrumentation). **No correction needed.**
- The dashboard CORE's still-open items read by `t102_l3_context` /
  `l4_context2` (pane 4's wiring diagram, the tab-bar/chronology CORE
  language for panes not yet drawn) are dated 2026-09-04, the owner-in-session,
  and are not the subject of any task 89–99 report. **Genuinely open,
  left alone**, matching this same node's own round-15 disposition
  (log_195 §6.5: "editing a genuinely-open row is not this bank's
  job").

**Conclusion: zero CORE.md realization-table rows and zero PROGRESS.md
diary lines under either subtree misstate what is on disk, as of this
bank.** This differs from round 15's bank (log_195), which found four
stale rows — round 15's own corrections evidently held, and rounds
16–19 did not introduce new ones. The full 69-line grep output is kept
in the lane log (`t102_l2_sweep.sh.log`) rather than pasted a second
time here, per "show the object" — the object already exists on disk
as that lane's own transcript.

---

# 4. Verifier tallies over logs 205–210, from `t102_l6_verify_205_210`

`check_conventions_log_claims.py --verify` was re-run, from INSIDE
`t102`, over each of the six most recent logs this bank did not itself
write. `t102` mounts only `PseudoCoupHQ`, `PseudoCoupGraphs`,
`PlanPlan`, `PseudoCoup_v5/v6` and `Sources` — it does NOT mount
`<runs>/<other-instance>/agent/logs/`, so any pasted command
that reads another instance's OWN lane log, or that submits/starts/
stops a sandbox, is REFUSED by the verifier's own safety rules
(`log_unreachable`, `submits_or_moves_the_sandbox`,
`touches_the_container_host`) rather than silently skipped. This is
the EXPECTED outcome for those claims, not a defect in the log being
checked — each REFUSED claim below is named with the instance that
WOULD verify it, if brought up and asked directly.

| log | task | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE | which instance answers the REFUSED ones |
|---|---|---|---|---|---|---|---|---|
| log_205 | 99 | 15 | 1 | 0 | 5 | 9 | 0 | `t99` — all 9 REFUSED cite `t99`'s own lane logs (`/logs/202609…__t99_l*.sh.log`), unreachable from `t102` |
| log_206 | founding | 5 | 0 | 0 | 5 | 0 | 0 | n/a — a narrative note, no shell commands, nothing to refuse |
| log_207 | o1 | 8 | 5 | 0 | 3 | 0 | 0 | n/a — fully self-contained, every command re-ran inside `t102` itself |
| log_208 | o2 | 15 | 6 | 0 | 4 | 2 | 3 | `o2` — both REFUSED are `up.sh --instance o2` / `airlock submit …--instance o2`, safety-refused rather than log-unreachable (this verifier will not start or feed another instance's sandbox from inside `t102`) |
| log_209 | o3 | 37 | 5 | 0 | 6 | 23 | 3 | `o3` — 23 REFUSED split between `up.sh`/`down.sh`/`airlock submit --instance o3` (submits_or_moves_the_sandbox) and `cat <runs>/o3/agent/logs/…` (log_unreachable); 2 more `touches_the_container_host` (a bare `podman run` re-run, refused on the same "no sandbox control from inside a sandbox" ground) |
| log_210 | o4 | 18 (17 processed) | — | — | — | — | — | `o4` — see below, this pass did not finish |

**Zero DIFFERS across every log actually completed.** The REFUSED
counts are large for logs 208–210 because those three tasks ran their
OWN heavy re-verification passes as Airlock submissions from inside
their own instances, and every such command is — correctly — refused
when read back from a different instance.

**log_210 did not finish inside `t102`:** the lane log shows
`Killed` / `exit 137` (SIGKILL) after processing claim 17 of 18, with
no final tally printed by this pass. This is NOT re-run here, per the
resume note's own instruction not to redo what a lane already
answered where a result exists — and one does exist: **log_210
already carries its OWN final self-verification, printed inside the
log itself** (§"check_conventions_log_claims.py --verify, final, over
the fully corrected section"): `claims 18 | MATCHES 8 | DIFFERS 0 |
UNVERIFIABLE 3 | REFUSED 5 | NOT_RERUNNABLE 2`. `t102`'s own
independent attempt to re-derive that number externally was killed
before reaching it; the 17 claims it did classify before the kill are
consistent with that self-reported tally's shape (a mix of MATCHES,
REFUSED-by-sandbox-control, and prose UNVERIFIABLE). **Flagged, not
silently patched over:** why `t102`'s own re-run of log_210 died
(SIGKILL) where 205/208/209 completed is not diagnosed here — the
lane's own footer shows no OOM message from the verifier itself, only
the shell's `Killed`, and re-running it is a candidate for whichever
instance banks the NEXT round, not manufactured here as a forced
retry.

---

# 5. PROGRESS appends, under the concurrency rule

Per the brief's concurrency rule as attested identically across every
sibling resume file in this scratchpad (read immediately before each
append; append only; one open-for-append call per file — five other
tasks append to some of these same files), two top-level PROGRESS.md
files were appended, each read fresh immediately before its one Edit:

- `Planning/node_0_3_research/node_0_3_1_operator_equivalence/PROGRESS.md`
  — a rollup bullet for tasks 97–99 (not yet present in this file:
  confirmed by `grep -c "task 97\|task 98\|task 99"` = 0 before the
  append), plus this bank's own line.
- `Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/PROGRESS.md`
  — a rollup bullet recording this bank's verification of the founding
  note and o1–o4, and the verifier-tally table above.

No CORE.md file was edited — §3 found nothing to correct.

---

# 6. Two lists

## 6.1 Decided, recorded for audit

- Tasks 89–99 and the arch_unit_oracle founding + o1–o4: every
  artifact each task's own log names is present on disk, sized and
  git-attributed as claimed (§2).
- The stale-row sweep across both subtrees' `PROGRESS.md` files (69
  `planned`/`in-progress` hits) found **zero** rows that misstate
  current reality, after reading each hit's own file in context rather
  than trusting the grep alone (§3) — a different outcome from round
  15's bank (log_195), which found four, and stated here rather than
  assumed to be the same.
- The verifier tallies over logs 205–210 show zero DIFFERS on every
  pass that completed; the large REFUSED counts on 208–210 are the
  verifier correctly declining to reach into another instance's own
  sandbox or lane-log directory from inside `t102`, and each REFUSED
  cause is now labelled with the instance that would answer it (§4).
- log_210's own re-verification inside `t102` was killed at 17 of 18
  claims; log_210's OWN internal final tally (18 claims, 8 MATCHES, 0
  DIFFERS) is banked in its place rather than left unreported (§4).
- `the_pool5.json` remains the newest pool generation; task 97 closed
  term66 (332 of 332) but did not cut a new pool.

## 6.2 Awaiting the owner — kept minimal, none decided here

1. **Cross_construction stays FROZEN** (the owner, 2026-09-06) pending a way
   to chain arch-units down to one opcode; the founding node's next
   step (compiler_units offered-vs-used) is task o3/o4's own territory
   and is done, awaiting the owner's read of the leftover-resolution numbers
   (§2.2).
2. **o2's naming and chaff-rule choice** (log_208, restated in the
   founding PROGRESS): which chaff rule stands, the artifact folder
   name, and the guard collision where `and`/`or`/`xor`/`not` spell
   cpp's alternative operator tokens.
3. **Dashboard pane 4's wiring diagram and the tab-bar CORE language**
   for panes not yet drawn (the owner, 2026-09-04, in session) — untouched
   by rounds 16–19, carried forward rather than re-litigated (§3).
4. **Why `t102`'s own re-verification of log_210 was killed** (§4) —
   named as a flag for whichever task next has reason to re-run it,
   not diagnosed here.
5. Carried without re-opening from prior bank(s): every item in
   log_195 §9.2 that rounds 16–19's own task logs do not name as
   closed (the runtime-callee term shape, the "completed" definition
   for the compiler graph, `gate.SOLVER_MILLISECONDS` reproducibility,
   `Graph.coverage`'s memory check, log_194's four Airlock items).
