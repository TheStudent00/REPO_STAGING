# log 060 — PseudoCoupHQ migrated from SandboxDesign to Airlock

2026-08-22. the owner: *"if you can migrate from SandboxDesign to Airlock for
PCHQ -- and the Claude skill if needed -- yes please"*.

The sandbox this line drives is now `PUBLIC/Airlock`.
`SandboxDesign` is **not** retired, **not** modified and
**not** moved by this work; it still runs. Airlock is a derivation of it,
recorded in `PUBLIC/Airlock/DevComms/log_001_airlock_derivation.md`,
and the move-across instructions are in
`PUBLIC/Airlock/MIGRATING.md`.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree,
higher / lower; the outcome where the operating system stops a lane is
**ABORT**. No lane ran in this session.

## 1 — the mapping

### paths

| old | new |
|---|---|
| `SandboxDesign` | `PUBLIC/Airlock` |
| `SandboxDesign/agent/drop/<lane>.sh` | `PUBLIC/Airlock/agent/drop/<lane>.sh` |
| `SandboxDesign/agent/status/<lane>.sh.status` | `PUBLIC/Airlock/agent/status/<lane>.sh.status` |
| `SandboxDesign/agent/logs/<stamp>__<lane>.sh.log` | `PUBLIC/Airlock/agent/logs/<stamp>__<lane>.sh.log` |
| `SandboxDesign/agent/out/` | `PUBLIC/Airlock/agent/out/` |
| `SandboxDesign/agent/batch.json` | `PUBLIC/Airlock/agent/batch.json` |
| `SandboxDesign/proxy/allowlist.txt` | `PUBLIC/Airlock/proxy/allowlist.txt` |
| `SandboxDesign/mounts.conf` | `PUBLIC/Airlock/mounts.conf` |

The tail of every path under `agent/` is identical. Only the repo
directory changed.

### commands

| old | new |
|---|---|
| a hand-write into `SandboxDesign/agent/drop/x.sh` | `python3 PUBLIC/Airlock/airlock submit x.sh --batch <label> --weight <n>` (the hand-write still works, and is still the truth underneath) |
| `SandboxDesign/sandbox submit x.sh --batch b --weight 40` | `python3 PUBLIC/Airlock/airlock submit x.sh --batch b --weight 40` |
| `SandboxDesign/sandbox status x.sh` | `python3 PUBLIC/Airlock/airlock status x.sh` |
| `SandboxDesign/sandbox watch` | `python3 PUBLIC/Airlock/airlock watch` |
| `SandboxDesign/sandbox doctor` | `python3 PUBLIC/Airlock/airlock doctor` |
| `bash SandboxDesign/progress.sh` | `python3 PUBLIC/Airlock/airlock status` — **or** `bash PUBLIC/Airlock/progress.sh`, which still exists, is carried across unchanged, and still works |
| `bash SandboxDesign/progress.sh -w` | `python3 PUBLIC/Airlock/airlock watch` — **or** `bash PUBLIC/Airlock/progress.sh -w`, unchanged |
| `bash SandboxDesign/allow.sh sync` | `bash PUBLIC/Airlock/allow.sh sync` (or `airlock allow sync`, which delegates to it) |
| `bash SandboxDesign/up.sh` / `down.sh` / `build.sh` / `selftest.sh` / `submit.sh` / `logs.sh` / `pull.sh` / `report.sh` / `batch.sh` / `probe_host.sh` / `submit_project.sh` / `install_quadlet.sh` | the same script name under `PUBLIC/Airlock/`, same arguments, same behaviour |

`PUBLIC/Airlock/progress.sh` is not deprecated and is not
replaced. It is the only view that lists live processes inside
`sandbox-runner`, and every `airlock` view ends by pointing at it.

### environment variables

| old | new |
|---|---|
| `SANDBOX_DESIGN_ROOT` | `AIRLOCK_ROOT` — the old spelling is still read, **after** the new one |
| `SANDBOX_CPUS` | `AIRLOCK_CPUS` — same, still read after. Default is now **6**, the full share |

### what did NOT change

The container, network, image and volume names keep their `sandbox-`
prefix: `sandbox-runner`, `sandbox-proxy`, `sandbox-internal`,
`sandbox-egress`, `sandbox-persist`. Do **not** search-and-replace them.

The consequence: **Airlock and SandboxDesign must never run at the same
time.** Both `up.sh` scripts test `podman container exists
sandbox-runner` first, so whichever starts second starts the *other*
one, bound to the other repo's `agent/` directories — lanes would appear
to vanish and status files would never be written where anyone is
looking. Bring one down before bringing the other up.

## 2 — what was changed in this repo

| file | what changed |
|---|---|
| `PRIVATE/PseudoCoupHQ/CLAUDE.md` | the `## the sandbox` section rewritten as `## the sandbox — Airlock, since 2026-08-22`: Airlock paths, the CLI as the way in, the mandatory batch decision, `airlock status` / `watch` / `doctor`, the plain statement that `PUBLIC/Airlock/progress.sh` still exists and still works, the ABORT rendering, and the named exception for the Research generators (§4) |
| `PRIVATE/PseudoCoupHQ/AgentMemory.md` | the `sandbox/toolchain:` entry under `## where things are` repointed to `PUBLIC/Airlock`, with the CLI commands and the note that `progress.sh` still works |
| `Planning/node_0_3_research/node_0_3_1_dominant_intentions/CORE_0_3_1_dominant_intentions.md` | `**runner**: the SandboxDesign agent lane` → the Airlock agent lane, with the submit and status commands |
| `Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md` | step 2 of `## the method`: `run — through the SandboxDesign agent lane` → the Airlock agent lane, with the submit and status commands |
| `DevComms/log_060_sandbox_to_airlock_migration.md` | this file, new |

Four existing files edited, one written.

## 3 — the DevComms logs were deliberately NOT touched

**A log said what was true on its date.** Eighteen logs in
`PRIVATE/PseudoCoupHQ/DevComms/` name `SandboxDesign`, and every
one of those references **is correct as of that log's date**. Every run
they record really did go through
`SandboxDesign/agent/`, and rewriting them would make the
record disagree with what happened. **None of their bodies was
rewritten, and none will be.**

| log | left untouched |
|---|---|
| `log_017_dominant_intentions_inventory.md` | yes |
| `log_018_handoff_plan_2026_08_13.md` | yes |
| `log_019_calibration_run.md` | yes |
| `log_020_full_census_run.md` | yes |
| `log_022_type_vocabulary_union.md` | yes |
| `log_023_layer2_representations.md` | yes |
| `log_024_layer3_python_fuzz.md` | yes |
| `log_025_probe_timing_measurements.md` | yes |
| `log_026_compiler_acceptance_shape.md` | yes |
| `log_027_phase3_build_and_runs.md` | yes |
| `log_028_phase3_closeout.md` | yes |
| `log_038_constructs_value_grain.md` | yes |
| `log_049_interval_sampling_pilot.md` | yes |
| `log_052_cartesian_probe_run.md` | yes |
| `log_054_handoff_fuzz_clustering_state.md` | yes |
| `log_057_ruby_float_canon_fix_and_rust_release.md` | yes |
| `log_058_ten_language_launch_held_pending_gate.md` | yes |
| `log_059_ten_language_launch_still_held_postscript_unverifiable.md` | yes |

To read one of those logs against today's tree, apply the mapping in §1.
This log is the single place that mapping lives; no log above needed a
note appended to it, and none got one.

The same rule was applied inside the Planning tree. Every
`SandboxDesign` mention in a `PROGRESS.md` sits inside a **dated bullet
recording a past event**, not in a present-tense instruction, so those
were left alone too:

| file | line | what it records, and why it stays |
|---|---|---|
| `Planning/node_0_3_research/node_0_3_1_dominant_intentions/PROGRESS.md` | 72–73 | a dated 2026-08-13 entry: `.googleapis.com` staged in `SandboxDesign/proxy/allowlist.txt`, awaiting a sync that a later dated entry records as done. A closed past state |
| `Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/PROGRESS.md` | 1100 | "Phase 2 ran them through the SandboxDesign agent lane in **64.5 s**". It did. Rewriting this to say Airlock would be false |
| `Planning/node_0_3_research/node_0_3_4_data_representation/PROGRESS.md` | 75 | a dated 2026-08-17 entry naming an `allow.sh sync` the owner then ran, recorded as done in the very next entry |
| `Planning/node_0_3_research/node_0_3_4_data_representation/PROGRESS.md` | 83 | a dated 2026-08-17 observation, "worth folding into `SandboxDesign` generally" |

The CORE files carry the **method**, in the present tense, and those
were updated (§2). The rule applied is one line: **a reference is
updated when it tells someone what to do next; it is left when it
records what happened on a date.**

## 4 — the Research tooling was NOT repointed, and why

Seventeen files under `PRIVATE/PseudoCoupHQ/Research/` resolve a
`SandboxDesign` path. They are live tooling, and the obvious move is to
repoint them. **They were deliberately left alone**, because repointing
them would break them against the data they read.

`SandboxDesign/agent/out/` holds **480 products** — every
run of record for this line. `PUBLIC/Airlock/agent/out/` holds
**0**, and `PUBLIC/Airlock/MIGRATING.md` states the rule
explicitly: *"Nothing is copied out of `SandboxDesign/agent/`.
Old logs, statuses and products stay where they are; Airlock starts with
an empty lane."* A reader repointed at Airlock would find nothing.

| file | what the reference is | direction |
|---|---|---|
| `Research/kind_fuzz_clustering/l3_interval_read.py` | `LANE_OUT` | reads products |
| `Research/kind_fuzz_clustering/l3_interval_c_read.py` | `LANE_OUT` | reads products |
| `Research/kind_fuzz_clustering/l3_cart_read.py` | `LANE_OUT` | reads products |
| `Research/kind_fuzz_clustering/l3_boundary_fold.py` | out directory | reads products |
| `Research/kind_fuzz_clustering/l3_value_fold.py` | `OUT` (with a session-mount fallback) | reads products |
| `Research/kind_fuzz_clustering/l3_cart_gen.py` | `DROP` and `LANE_OUT`, plus a docstring | writes lanes, reads products |
| `Research/kind_fuzz_clustering/l3_interval_gen.py` | `DROP`, plus a docstring | writes lanes |
| `Research/kind_fuzz_clustering/l3_interval_c.py` | `DROP` and an out path | writes lanes, reads products |
| `Research/kind_fuzz_clustering/l3_boundary_lane.py` | `DROP` | writes lanes |
| `Research/kind_fuzz_clustering/lane_build.py` | docstring | writes lanes |
| `Research/kind_fuzz_clustering/probe_generate.py` | docstring | writes lanes |
| `Research/kind_fuzz_clustering/timing_build.py` | docstring, and a hardcoded drop path carrying a **stale session mount** (`/sessions/brave-optimistic-cannon/...`) | writes lanes |
| `Research/kind_fuzz_clustering/HARVEST.md` | the harvest procedure, four references | operating notes |
| `Research/kind_fuzz_clustering/HARVEST_constructs.md` | one status path | operating notes |
| `Research/data_representation/audit_generate.py` | docstring | writes lanes |
| `Research/dominant_intentions/harness/generate_run.py` | docstring | writes lanes |
| `Research/type_vocabulary/raw/python.types.json` | a `how_run` provenance field | a record of a past run — stays regardless |

This is a structural choice about where the line's data lives, so it is
the owner's, not an agent's. It appears on the awaiting-the owner list. The two
coherent options:

1. **Leave them.** PCHQ keeps driving `SandboxDesign`,
   which is not retired and still works. Nothing breaks. Airlock is then
   the sandbox for new work and for anyone else.
2. **Repoint them, and move the products.** Copy
   `SandboxDesign/agent/out/` into
   `PUBLIC/Airlock/agent/out/` first, then repoint. The readers
   keep working because the data moved with them.

`timing_build.py`'s hardcoded `/sessions/brave-optimistic-cannon/...`
drop path is stale under either option — that session mount no longer
exists — and is worth fixing whichever way the owner rules.

## 5 — PCHQ's own scripts

Checked line by line for a `SandboxDesign` path:

| script | result |
|---|---|
| `PRIVATE/PseudoCoupHQ/hq.sh` | **no `SandboxDesign` reference.** Its four occurrences of the word "sandbox" all mean the Cowork agent sandbox — the thing that cannot set an executable bit and leaves stale `.git/index.lock` files — not this repo. Nothing to change |
| `PRIVATE/PseudoCoupHQ/create_github_repo.sh` | none |
| `PRIVATE/PseudoCoupHQ/git_commit_push.sh` | none (same Cowork-sandbox sense) |
| `PRIVATE/PseudoCoupHQ/git_commit_push_all.sh` | none (same) |

`bash PRIVATE/PseudoCoupHQ/hq.sh check` was run after every edit
above and reports the same clean result it did before: **0 errors.**

## 6 — the toolchain skill

`~/.claude/skills/toolchain/SKILL.md` carries roughly fifteen
`SandboxDesign` references, and its §0 is a standing policy written
entirely about that repo. The copy visible from an agent session is a
**read-only cache**; editing it does not change the saved skill, so it
was **not** edited.

The exact replacement text for every affected section — quoted
old-versus-new, ready to paste — is at
`PUBLIC/Airlock/DevComms/toolchain_skill_airlock_patch.md`. It has
to be applied through the skill-save mechanism by a session that has it.

## decided, recorded for audit

- **The sandbox of record for this line is `PUBLIC/Airlock`**, as
  of 2026-08-22. `SandboxDesign` is untouched, still
  works, and is not retired by this log.
- **Four files updated, one written**, listed in §2. The rule applied:
  a reference is updated when it tells someone what to do next, and left
  when it records what happened on a date.
- **The eighteen DevComms logs naming SandboxDesign were not rewritten**
  and their bodies were not touched. Their references are correct as of
  their dates. This log is the one place the mapping lives.
- **Four `PROGRESS.md` references were left for the same reason** — each
  sits inside a dated bullet recording a past event. Named individually
  in §3.
- **`PUBLIC/Airlock/progress.sh` still exists and still works.**
  It is carried across unchanged, `-w` still refreshes, and it is the
  only view listing live processes inside `sandbox-runner`.
- **The `sandbox-` container, network, image and volume names are
  unchanged**, so the two installs must never run at the same time.
- **`hq.sh` needed no change** — its "sandbox" occurrences mean the
  Cowork agent sandbox. Verified line by line.
- **`hq.sh check` reports 0 errors** after the edits.
- **The toolchain skill's cached copy was not edited**, because editing
  it changes nothing. The replacement text is a separate deliverable.

## awaiting the owner

Two, kept minimal.

- **Whether to repoint the seventeen `Research/` files** (§4) — and if
  so, whether to move the 480 products out of
  `SandboxDesign/agent/out/` first. This decides where the
  line's data lives, so it is not an agent's call.
- **Saving the toolchain skill patch.** The text is written and ready;
  applying it needs the skill-save mechanism.
