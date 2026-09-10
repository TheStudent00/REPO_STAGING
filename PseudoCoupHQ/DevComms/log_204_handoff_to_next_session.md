# log 204 — hand-off: project state and what comes next

Written 2026-09-05 at the close of the session that ran rounds 15–19.
Written by the Claude Code coordinator (Fable), for the next session.
the owner's own words are quoted where a ruling rests on them.

READ FIRST, in this order, before doing anything:
1. `PRIVATE/DevComms/LLM_communication_protocol.md` — all of it.
   §1.8 (answer "what is it" in one sentence, in relation, first),
   §4.6 (machine mechanisms shown as machine state) and §4.7 were
   written this session after failures that cost the owner an hour. Read
   them as the reason this session was abandoned.
2. `PRIVATE/PseudoCoupHQ/AgentMemory.md` — section "the rulings
   of 2026-09-04 / 2026-09-05" and the "communication, added
   2026-09-05" section at the end.
3. `PRIVATE/PseudoCoupHQ/CLAUDE.md`.
4. This file.

---

## 1. Where the research stands — the numbers, each with its population

The line: **operator equivalence across nine languages.** An
arch-unit is one operator's machine code, extracted from a function
body. A term is that arch-unit expressed as a z3 expression. The pool
is one entry per distinct computation, filled by merging units whose
normalized term text is identical.

### 1.1 The corpus
| | count |
|---|---:|
| arch-units, 9 languages | **31,078** |
| — cpp 17,840 · c 10,620 · swift 1,322 · rust 695 · go 590 · php 4 · java 2 · ruby 2 · cpython 1 | |
| not proved by canon40 (gate 1) — never transcribed | 754 |
| proved, eligible | 30,324 |
| layer-5 normalization never converges — term built and proved, no comparison key | 44 |
| **in `term66_store`** | **30,280** |

Distinct machine bodies, corpus-wide: **2,744** of 31,067 compiled
units (11.3 units per body). **642 bodies appear in more than one
language.** Most repeated: `89 f8 21 f0 c3`, 561 times, in c/cpp/
rust/swift. (Per-language count is 3,547 — a different measurement.)

### 1.2 The four term states (task 97, log_202, over the 30,280)
| | round 14 | now | move |
|---|---:|---:|---:|
| proved | 26,594 | **27,866** | +1,272 |
| disproved | 3,134 | **1,676** | −1,458 |
| undecided | 285 | **253** | −32 |
| no term | 419 | **485** | +66 |
Consistency 0. Dominant cause: 1,272 disproved→proved, all carrying
a runtime-callee row — task 78's corrected destination rule landing.
Wall-clock control: 302 of 302 identical.

- **no term** (485): the unit could not be put into z3 form. The
  walk hit something with no rule — e.g. `__divti3` has a loop. The
  record stores its holes but the `reason` field is NULL on all 485
  (a recording gap).
- **undecided** (253): in z3 form, but nothing to compare against —
  115 every path leaves the unit, 76 branch sides leave the stack at
  different depths, 13 overflow flag never set, **47 solver timeout**.

### 1.3 The pool — NOT rebuilt
`the_pool6.json`, `the_families6.json`, `exception_families6.json`
do not exist. `pool66_run.py` refused its own output: 44 proved units
have no layer-5 key. **Authoritative pool is still `the_pool5.json`:
1,831 entries / 30,432 members.** `name_census7.json` WAS produced
(50 producers over 30,280).

### 1.4 The compiler graph (task 87, 93, 95)
- Three connection kinds — structural, dynamic, per-operator-traced-
  variant — exist for **go** and **c/cpp (clang)**. Not complete:
  rust and swift have structure only; java/cpython/php/ruby have no
  graph. the owner ruled "completed" = actual implementation of what was
  asked, all nine. NOT a question.
- Graphs live in `PseudoCoupGraphs` (NO remote, by
  design; repo-daemon commits locally). Compact form: 608 MB → 72 MB,
  byte-identical round trip.
- **arch-opcode-nodes** (task 95, log_200): static detection from
  source of which compiler definitions emit machine instructions.
  go: 57 emitters of 1,859 defs; cpp 251 of 10,789. Restricted to
  emitters + callers the graphs are 3.6% / 3.3% of definitions.
  **rust emits nothing** — rustc emits LLVM IR; LLVM is the cpp
  region. swift: one inline-asm `nop`.

### 1.5 The reference simulator (task 91, log_196)
`reference.py` is the one simulator (canon9/10/12 superseded).
`SRem`/`URem` fixed, machine stack and x87 built. Re-gate: 415/415
withdrawn disproofs prove; 5,602 undecided → 2,356 proved / 2,969
disproved / 277 undecided. **2,916 of the 2,969 are the LEDGER's gap
(canon38 has no row for transfers into the runtime), not the
reference's** — belongs to the canon rebuild.

### 1.6 The interpreters (tasks 94, 96; logs 199, 201)
11 units, re-carved to **function bodies** (the owner's ruling). On
`canonical_form.py` (the correct form): 9 of 11
PROVED_BY_CONSTRUCTION — the wrapping is faithful; z3 answered for
none (the reference has no model for e.g. `movl`). Java ×2 refused at
the seventh block kind (reach 0x538 past `own-address`'s 0x100).

### 1.7 The dashboard (tasks 85, 86, 93, 98)
Python route: `Research/op_pipeline/dashboard_ouro.py` +
`dashboard_ouro.html`, opened in Ourobrowser at
`ourobrowser://local/PRIVATE/PseudoCoupHQ/Research/op_pipeline/dashboard_ouro.html`
(saved in `dashboard_ouro_address.txt`).
- Chronology is the OUTER CONTROLLER above the tab bar; a moment is
  a commit; scale is raw `git log`, nothing curates it.
- Five panes. Pane 4 draws the compiler graph by its own directory
  structure (go, clang; rust/swift structure only; others `no graph`).
- Pane 5: 136 rows, 100 computed at render time, 36 from stored
  summaries, every row has a `?` (`dashboard_stats.py`, 46 meaning
  records), 0 unexplained.
- Peak 599 MB / 1,500 cap.

---

## 2. What landed this session, by task
| task | log | one line |
|---|---|---|
| 77 | 184 | dashboard rendered by python in Ourobrowser |
| 78 | 185 | runtime-callee answer registers, 608 → 49,362 rows |
| 79 | 186 | layer-5 text stabilised |
| 80 | 187 | render_back conditional template |
| 81 | 190 | clang instrumented; 1,380 c/cpp diaries + 2,600 regen |
| 82 | 188 | Airlock cross-instance view; dashboard tab dedup |
| 83 | 189 | term walk STOPPED (misdiagnosed — see 97) |
| 85 | 191 | chronology as outer controller (round scale — wrong) |
| 86 | 192 | chronology corrected to raw VCS |
| 87 | 193 | third connection kind: per-operator-variant connections |
| 88 | 194 | Airlock products audit: 6.35 GB only in `agent/out`, 99.6% regenerable |
| 89 | 195 | bank round 15 (3 hand-tidied transcripts found later) |
| 90 | 197 | **`check_conventions_log_claims.py`** — re-runs a log's commands |
| 91 | 196 | reference: one simulator, SRem, stack+x87, re-gate |
| 93 | 198 | graphs moved/shrunk/drawn |
| 94 | 199 | interpreters re-carved to function bodies |
| 95 | 200 | arch-opcode-nodes, static |
| 96 | 201 | interpreters onto `canonical_form.py`; seventh block kind |
| 97 | 202 | term walk COMPLETED (fork per unit: 1,112 s → 13.4 s) |
| 98 | 203 | stats pane: `?` per row + render-time stats |

---

## 3. Rulings the owner made this session (all in AgentMemory; do not re-litigate)
- Unit boundary = function body, read from symtab/DWARF.
- Canonical form = body UNCHANGED, virtual memory only at load/store.
  `region36.py`'s %r15 rewrite was a MISREADING. `%r15` collision is
  an artifact of it — never "fix" by moving the base.
- Seventh block kind: an arriving addressable area (precedent:
  `own-address`).
- "Completed" graph = all nine compilers/interpreters. Not a question.
- Chronology = raw `git log`. No project vocabulary in the mechanism.
- Pane 4 cannot exist before the object it draws.
- Time/memory limits: FLAG, re-run with more room, report if the
  answer changed. Never change what is measured to make it fit.
- The 6.32 GB kind-fuzz results: gitignored folder, move on.
- Dashboard is becoming a general PlanPlan dashboard.

---

## 4. Genuinely open — the owner's to decide (kept minimal)
1. **Reporting protocol**: should an attribution block be REQUIRED to
   name its lane log file? Would move ~74% unverifiable → ~19%.
   (Already enforced in briefs; not yet a protocol rule.)
2. **`Term.normalize` does not converge for 44 of 30,324.** Term is
   proved; comparison key missing. Whether the pool can be built
   without them, and what a record for such a unit IS.
3. **`gate.SOLVER_MILLISECONDS = 3000` is a wall clock.** Task 91
   measured 120,000 ms turns UNDECIDED→DISPROVED and never into a
   proof. Whether the ceiling moves.
4. **`AREA_SPAN` 0x100** — two java units need 0x538.
5. Task 95: should go's `one_static_hop` sites carry all 564 amd64
   opcodes in the inverse index, or only the constants + name the table.
6. Task 98: re-point stored half `audit65`→`audit66`; collapse the
   computed half by default; extend `?` to panes 1–4.
7. log_194's four: placement of 6.32 GB corpus; 10 diverged files'
   canonical side; loose lane scripts in Airlock root; pin
   `sem_anchored` deps (angr not in image).

## 5. Work that is NOT a decision (just do it)
- Rebuild the pool once #2 is ruled (or with the 44 excluded and
  named).
- Record a `reason` on NO_TERM records (null on all 485).
- Verifier: refuse a claim whose log file isn't reachable from the
  running instance instead of calling it DIFFERS (it did this to me
  twice).
- `Graph.coverage` has no in-process memory check (signature takes no
  ceiling). Shape question for the graph CORE.
- `install_quadlet.sh` re-render: `mounts.conf` names
  `PseudoCoupGraphs` but the running container predates that line.
- Stale `planned` rows get swept at each bank; task 89 found one row
  that said DONE and was false.
- Bank round 16–19 (no bank since round 15).

## 6. Next round candidates (round 20)
1. The pool over canon40 (blocked on §4 item 2 or a named exclusion).
2. Remaining graphs: java/cpython/php/ruby builds; rust/swift diaries
   (rust blocked on fetch, swift unstartable here — FLAG, don't redefine).
3. The interpreter proofs: the reference has no model for `movl` etc.;
   9 units are PROVED_BY_CONSTRUCTION not solver-proved.
4. The 2,916 ledger-gap disproofs → canon rebuild.
5. Bank.

## 7. Standing process rules
- **ALL compute through Airlock.** One instance per heavy task
  (`instances/t<N>.conf`, copy `t87.conf`). Lane names used ONCE.
  Print `[$i/$total]`. Down when done.
- **Memory**: state bound, sample first, paste peak RSS, abort by name
  ~6 GB. Stream, never whole-corpus.
- **Every report**: claims carry a reproducing command or say they
  can't; attribution names the lane log file; run
  `check_conventions_log_claims.py --verify <log>` FROM THE SAME
  INSTANCE whose logs it cites. Best scores: 98 → 14/14; 97 → 38/45;
  96 → 28/35.
- **Spelling ban**: paste verbatim into every brief; guard unmodified,
  one process, `grep -c exempt` = 0.
- **Coordinator verifies independently** — every result this session
  was spot-checked before relay; two false claims (task 48 history,
  log_195 transcripts) show why.

## 8. What went wrong this session — for the next coordinator
- Explaining "term" took ~10 replies and an hour. The one-sentence
  answer ("the arch-unit expressed as a z3 expression") existed from
  the start. Protocol §1.8 now.
- Three visualisations were built when one table was wanted; text
  overflowed SVG boxes. Protocol §4.6.
- Twice a non-decision was handed to the owner as his to make ("completed"
  graph; runtime-callee term shape — turned out to be a process-
  lifetime bug, fixed by forking). Never offer a reduced deliverable
  as a reading of the requirement; never forward an implementation
  problem as an ontology question.
- Vocabulary drift: "unit" used bare when arch-unit / runtime-callee
  unit / interpreter unit were all in play (§1.7, written and broken
  the same day).
