# Launch note, 2026-09-13 — three RISC-V tasks in parallel, then the housekeeping a shell needs

Written by the research coordinator (Fable) for the session that
launches; that session has a shell and can spawn implementers, this
one cannot. Everything below is on disk and committed. the owner's words
are quoted where a task exists because of them.

## 0. Before anything: read these, in this order
1. `PRIVATE/PseudoCoupHQ/Research/LAW.md` — ALL of it.
   The spelling ban and its guard; the tower section (`remote_lane.sh`
   at `$HOME/Programming/PUBLIC/Airlock/remote_lane.sh`, never `~`
   inside a quoted variable; waits in short calls under 110 s; sync
   args in the flat form `Programming/PseudoCoupHQ/...`); lane scripts
   kept in the repo; never delete under `PUBLIC/Airlock/`
   or `<runs>/`.
2. `PRIVATE/PseudoCoupHQ/Research/GLOSSARY.md` — the
   words of the line, in the owner's form.
3. `PRIVATE/PseudoCoupHQ/AgentMemory.md`, the section
   "the arch-opcode emulation line" — the rulings and the state.
4. `PRIVATE/DevComms/LLM_communication_protocol.md` —
   how to write to the owner. Two rules a shell-less session could not put
   back into it and that bind anyway: every raw text block stays
   inside 72 columns (wrapped blocks are unreadable to him); every
   table row that counts something reads "N of M" with M the
   population the loop actually ran over.

## 1. The three tasks (launch all three at once, separate instances)

| task | brief | instance | model | what it is |
|---|---|---|---|---|
| sl1 | `Research/briefs/task_sl1_brief.md` | `instances/sl1.conf` | Opus (or the highest available) | the RISC-V lifter's table generated from the Sail model by a tool on every run; nobody types a row; the point check as guard; rv6 re-run on it; the regeneration test |
| rv9 | `Research/briefs/task_rv9_brief.md` | `instances/rv9.conf` | Opus | the arch-opcode axis under the owner's rule: the multiply-high cause named from the literal objects on the native route; the bit-blast route at three optimization settings; rv4's regression cause named |
| lx1 | `Research/briefs/task_lx1_brief.md` | `instances/lx1.conf` (proxy = yes, for the swift install lane only) | Sonnet | the language axis: swift for riscv64 as an install measured with the network on; the seven interpreted languages against the 255 RISC-V definitions by agreement |

the owner's criterion, which every brief carries at its top and which the
launcher repeats to each implementer:

> if i stop making updates to the repo and things that it processes
> churn, the system will still be able to re-generate essentially all
> the proofs, Hub, and whatever else downstream by running the system.

> no human intelligence (LLM or biological) is pointing to a spelling
> and saying "that's div!"

So: nothing written for any particular arch-opcode; a change that
would differ for `mulh` and for `add` is refused; tables are produced
by tools from the Sail model; identity is by behavior, never by name.

### the implementer prompt (one per task; swap the task id, brief, instance, node)
```
You are the implementer of task <id>. Read, in this order and in
full: PRIVATE/PseudoCoupHQ/Research/LAW.md (ALL of it),
then PRIVATE/PseudoCoupHQ/Research/briefs/task_<id>_brief.md
including its section 0, then Research/GLOSSARY.md, then every file
the brief names. Then do the task exactly as the brief states it.

Rules that bind you beyond the brief:
- Do it yourself: no Agent tool, no sub-agents. Run in the foreground.
- ALL compute on the tower through remote_lane.sh
  ($HOME/Programming/PUBLIC/Airlock/remote_lane.sh: conf
  instances/<id>.conf, up --instance <id>, sync-to, submit --batch
  <id>, wait in calls of at most 100 s repeated, sync-back, down).
  Never a host venv, never a host compile. One process per lane; no
  worker pools; no clocks in drivers.
- Sample first (a handful of cells in their own lane, numbers pasted),
  then the whole population.
- Never end your turn while a lane is running on the tower. A tool
  call is cut at 120 s, so wait in repeated short calls.
- Never delete anything under PUBLIC/Airlock/ or
  <runs>/ on either machine. Never modify
  check_no_spelling_keys.py. Under Research/op_pipeline/ touch nothing.
- Never use the words parent/child/sibling/orphan; never kill/die
  (say ABORT).
- A tool that is absent, a build that fails, a disproof, a check that
  runs out: a FLAG in your log with the literal output and the count;
  never a hand edit to make a cell pass; never a case keyed by an
  opcode's name.
- Your report goes in
  PRIVATE/PseudoCoupHQ/DevComms/log_<next free number>_<id>_<slug>.md
  (check the folder: the other two tasks may take numbers), with every
  table row reading "N of 255", every flag LITERAL, and two lists kept
  strictly apart: "decided, recorded for audit" and "awaiting the owner".
  Append PROGRESS on the task's planning node:
  Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/<node>/PROGRESS.md
  where <node> is node_0_3_2_3_1_0_lifter_from_sail (sl1),
  node_0_3_2_3_1_1_arch_opcode_axis (rv9),
  node_0_3_2_3_1_2_language_axis (lx1).
  Commit (git add -A && git commit); no push.
- Your final reply: the brief's reply items, the log's path, every
  flag LITERAL. No prose beyond that.
```

Facts to hand each implementer: the Sail model is mounted at
`/sources/sail-riscv` inside the container; the image has `sail`
0.20.2 (opam, `/opt/opam`), `sail_riscv_sim`, z3, Lean 4.24, clang 21,
go 1.26, rust with `riscv64gc-unknown-none-elf` and
`riscv64gc-unknown-linux-gnu`, `g++-riscv64-linux-gnu` headers at
`/usr/riscv64-linux-gnu`; riscv64 c/cpp compile with
`--target=riscv64-linux-gnu --gcc-toolchain=/usr`; rust with
`--target riscv64gc-unknown-linux-gnu --emit=obj`; carve with
`llvm-objdump --mattr=+m,+a,+f,+d,+c,+zba,+zbb,+zbs -M no-aliases`.
sl1 is the only task allowed to change `riscv_reference.py`; rv9 and
lx1 READ it and record its sha256 per lane. lx1's instance has the
network on; it uses it only in the swift install lane and says so.

## 2. After the three land (or while they run, in the launcher's own turns)
1. Planning projections and dashboards, which the shell-less session
   could not run after registering the three nodes by hand:
   ```
   cd PRIVATE/PseudoCoupHQ/Planning
   python3 PRIVATE/PlanPlan/framework/generate_nodes.py . --projections --apply
   python3 PRIVATE/PlanPlan/framework/generate_dashboards.py .
   python3 PRIVATE/PlanPlan/framework/check_plans.py . | tail -3
   ```
   (the nine pre-existing dangling-path errors are old; anything new
   is a defect to name).
2. The repo daemon: the owner restarts it (`systemctl --user restart
   repo-daemon`). On restart it (a) splits the research repo's two
   files over GitHub's line (the bank, 127 MB; the x86 bit-blast run
   record, 274 MB) into parts and re-cuts the 17 unpushed commits into
   pushable ones — the one allowed history rewrite, the owner's ruling of
   2026-09-12 — and (b) stops re-announcing standing holds. The
   launcher checks `journalctl --user -u repo-daemon` for "split",
   "batch push" and errors, and reports.
3. The mirror: after the split, `PRIVATE/RepoDaemon/stage.sh --no-push`
   from `PUBLIC/REPO_STAGING`; the scrub must report
   clean on patterns and on plain tokens; the daemon now pushes the
   mirror itself.
4. Owed, in the owner's order, each already written as a brief or a note:
   rm1 (`Research/briefs/task_rm1_brief.md`, the rewrite rules mined
   from emulator arch-units, independent); the branch-following walk
   in the RISC-V lifter (a body with an `if` is read in text order);
   the `remu` build refusal with an empty message; the 32 audit alarms
   of bb2 (log_269); after sl1: the model table swept over every
   instruction Sail defines (the arch-opcode axis proper).
5. Planning writes the owner has agreed to, for a session with a shell and
   his go on the level-1 items: the PseudoIR `autopoly` tree as a
   draft (ledgerer_operators / polyfiller / hub_composer /
   architectures / simplification; hub.dictionary), the three
   ledgerer additions in PseudoCoup_v5 (the semantic slot as a
   reference to cell key + certificate id; the table's frame stating
   its key form; divergence confidence as the certificate's proof
   form), one clause in the exchange node for the owner's settling (the
   operator ledger reaches PseudoCoup as part of the hub's surface),
   and the width rule back into the protocol as a card.

## 3. What to report back to the owner, and how
Three tables "of 255" (sl1's instruction count beside 49 and its
point check; rv9's union-of-routes table beside log_268's; lx1's
interpreted table and the swift row or flag), every flag literal, the
log paths, and the daemon's split result. Plain words, terms declared
before use, raw blocks inside 72 columns, tables for numbers.
