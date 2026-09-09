# LAW — read in this order before touching anything (binds every brief that includes this file)

Kept in the repository since 2026-09-09: the session scratchpad it lived in
was wiped twice, and a brief without its law is not a brief. Briefs live
beside it under `Research/briefs/`.

1. `~/Programming/DevComms/LLM_communication_protocol.md` — all of it.
   §1.8 what-is-it in one sentence first; §3.5 walkthrough before
   numbers; §4.3 pipe tables only; §5.1 quote the object; §5.1a every
   rendering says LITERAL or GLOSS; §5.3 report by cause; §8 full paths.
2. `~/Programming/PseudoCoupHQ/Planning/node_0_3_research/CORE_0_3_research.md`
   — the master plan; your task is one of its §4.2 steps.
3. `~/Programming/PseudoCoupHQ/AgentMemory.md` — "the operator-
   equivalence pipeline (RATIFIED)", "the rulings of 2026-09-04 /
   2026-09-05", "communication, added 2026-09-05".
4. `~/Programming/PseudoCoupHQ/CLAUDE.md` (never parent/child/sibling/
   orphan; never kill/die — ABORT; two-list rule in every report).
5. Pasted verbatim, as required:

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

The guard `~/Programming/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py`
is never modified; run it in a lane over every json you write and
paste its output; `grep -c exempt` over files you add = 0.

Ruling of 2026-09-08 that the guard already encodes: a mnemonic alone is a
spelling; the machine-form key is (mnemonic, operand form, width); the
mnemonic sits in the field `mnem`, which the guard exempts as machine form.
Whether two rows compute the same mapping is z3's verdict on their terms,
never a reading of names.

## Process rules (standing)
- DO THE WORK YOURSELF. Do not use the Agent tool; do not spawn
  sub-agents.
- ALL compute through Airlock. One instance per task:
  `~/Programming/Airlock/instances/<task>.conf`, copied from
  `t97.conf` (or `o3.conf` for light tasks), every number in the
  header stating its reason. An instance that needs the swift toolchain
  mounts `sandbox-persist` read-only (`persist_volume = sandbox-persist`,
  `persist_mode = ro`); an instance with no persist line gets an EMPTY
  volume of its own. `python3 ~/Programming/Airlock/airlock --help`
  for up / submit (`--instance <task> --batch <task> --weight <n>`) /
  status. Lane names used ONCE: `<task>_l<N>_<what>.sh`; every lane
  prints `[$i/$total]`. Bring the instance down when done. Poll lane
  completion in a timeout-bounded loop inside one Bash call (foreground
  sleep is blocked).
- Memory: state the bound, sample first, paste peak RSS
  (`resource.getrusage`; `/usr/bin/time` is absent in the image), named
  abort `ABORT_MEMORY_<TASK>` at the stated ceiling. Stream shards;
  never load a whole store at once.
- Time or memory limits are FLAGS: re-run with more room, report
  whether the answer changed; never change what is measured to fit.
- Report: `~/Programming/PseudoCoupHQ/DevComms/log_<nnn>_<task>_<topic>.md`
  (take the next free number when you finish; several tasks run at
  once, so check `ls ~/Programming/PseudoCoupHQ/DevComms | tail` right
  before writing and never overwrite). First line names the project
  node. Every claim carries its reproducing command or says it can't;
  every attribution names its lane log file (host path stated). Final
  lane: `python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 <log>`
  FROM YOUR INSTANCE; paste the tally; zero DIFFERS (fix the log or
  the claim, never the verifier). No hand-tidied transcripts.
- Writes go ONLY under the artifact folder the brief names, plus the
  log and the node's PROGRESS.md (one dated entry, status). Nothing
  else under `Research/` changes unless the brief says so.
- Report shape: one numbered tree (protocol Appendix B); §1 what the
  objects are, one sentence each in relation; instances before
  mechanisms; the two lists at the end: "decided, recorded for audit"
  and "awaiting the owner" (kept minimal; never forward an implementation
  problem as an ontology question).
- Stop rules: a new record field, a new outcome name, a new node, a
  change to a shared file the brief did not name, or a fetch/install
  → stop, write what you found under "flag for the coordinator", do
  not work around it.

## Lane scripts are kept in the repo (the owner, 2026-09-07)
Every lane script you submit is FIRST written under the task's artifact
folder as `lanes_<task>/<lane name>.sh` (the repo-daemon commits it),
and submitted from there. Airlock's own `.done/` archive is not the
record and may be cleared. Never delete anything under
`~/Programming/Airlock/` or `~/AirlockRuns/`, on either machine — not a
status file, not a lane, not a log. A lane name that collides gets a new
name; nothing is removed to make room.

## Never end your turn while a lane you need is still running (2026-09-07)
Agents receive NO notification when a lane finishes and NO wake-up from
a background watcher. Poll in a timeout-bounded loop inside one Bash call
(e.g. `timeout 3500 bash -c 'until ...; do sleep 60; done'`), repeated as
needed, and continue. Two closers stopped "waiting for the notification"
and their work had to be redone.

## Compute runs on the TOWER now (the owner, 2026-09-08). Every lane goes there
The sandbox is a virtual machine on the owner's tower server, reached over ssh by
key from this laptop. Nothing about the lane protocol changes; only where it
runs. The one tool for it, kept in the Airlock repo:

    export AIRLOCK_REMOTE=<tower-user>@<host> AIRLOCK_REMOTE_ROOT=Programming/Airlock
    R="bash ~/Programming/Airlock/remote_lane.sh"

| step | command |
|---|---|
| your instance conf (write it under `~/Programming/Airlock/instances/<task>.conf` here, copied from `t97.conf`, every number with its reason) | `$R conf ~/Programming/Airlock/instances/<task>.conf` then `$R up --instance <task>` |
| BEFORE every submit: mirror your artifact folder and any code you changed to the tower (paths are the same relative to the home directory on both machines) | `$R sync-to Programming/PseudoCoupHQ/Research/<your artifact folder>` and the same for `Research/op_pipeline` if you touched it |
| submit a lane (the script lives here in the repo under `lanes_<task>/`; the copy on the tower is a working copy) | `$R submit --instance <task> --batch <task> --weight <n> <path to lane.sh>` |
| wait for it, in one call, bounded; it prints the status lines then the whole log | `$R wait --instance <task> <lane.sh> --timeout 3500` (repeat if it times out) |
| AFTER every lane: bring its artifacts back here; the laptop repo is the record | `$R sync-back Programming/PseudoCoupHQ/Research/<your artifact folder>` and `$R sync-back Programming/PseudoCoupHQ/DevComms` if a lane wrote a log |
| done | `$R down --instance <task>` |

Rules that follow from this:
- The tower copy of the repo is written ONLY by lanes. Never edit code on the
  tower by hand over ssh; edit here, sync-to, submit.
- sync-to and sync-back never delete and newer wins, so never leave a stale
  copy of a file you have re-generated on the other side: regenerate, then
  sync in the right direction.
- The verifier lane runs on the tower like any other lane. A lane-log
  attribution in your report names the TOWER path
  (`~/AirlockRuns/<task>/agent/logs/...`) and says so.
- The tower guest has 31 GB and runs one heavy lane at a time. Your instance
  is capped at 8 cpus / 20g; the memory bound you state in your script still
  governs, and `work_size` is memory-backed and counts inside the 20g.
