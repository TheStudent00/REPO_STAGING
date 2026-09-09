# Task pub2 — the PUBLIC / PRIVATE split of ~/Programming (planned; runs only when the tower is idle and the coordinator says go)

the owner, 2026-09-09: "we should probably organize `~/Programming` into public
and private folders. like if its public it goes into `PUBLIC`
and if its private it goes into `PRIVATE`." This brief is the
plan; it is executed by a Sonnet implementer ONLY after the coordinator
confirms no lane is running on the tower and no agent is editing the
repositories, because the tower mirrors `…` by the same
relative layout and every running instance binds those paths.

## 1. The split, from `gh repo view --json visibility` on 2026-09-09
| PUBLIC (→ `PUBLIC/`) | PRIVATE (→ `PRIVATE/`) | left where it is |
|---|---|---|
| Airlock, GraphModel, Ourobrowser, PseudoCoup, REPO_STAGING, ZSpectralCompression | DevComms, GitSpaceTime, Misc, ModelModel, PlanPlan, PseudoCoupHQ, PseudoCoup_v5, PseudoCoup_v6, PseudoIR, StressBot, and every repo with no remote (PseudoCoupGraphs) | upstream clones and non-repo data: flutter, depot_tools, chromium_src, Sources, 0_Archive, ModellingResearch, WFL_Projects, and the small non-repo folders — the owner to rule; default PRIVATE |
Before moving anything, re-run the visibility query and paste it; a repo
whose visibility changed goes where the query says.

## 2. Everything that names a `<repo>` path, and how each is fixed
| what | fix |
|---|---|
| `~/.config/repo-daemon/config.json` roots and excludes; the daemon's discovery depth (check `repo_daemon.py`: if it lists one level below each root, add `PUBLIC` and `PRIVATE` as roots; the REPO_STAGING exclude glob moves with it) | edit, `systemctl --user restart repo-daemon`, then `repo-daemon repos` pasted: every repo found exactly once |
| `Airlock/mounts.conf` (host side of every bind) | rewrite paths; the CONTAINER side (`PseudoCoupHQ`, `/sources`) stays exactly as it is, so every command inside a lane and every verifier claim keeps working |
| `remote_lane.sh`: `AIRLOCK_REMOTE_ROOT=Programming/Airlock` and every `sync-to` / `sync-back` relative path | the tower mirrors the SAME layout: move the tower's `<repo>` into `PUBLIC/` and `PRIVATE/` over ssh with `mv` (never `rm`), rewrite the tower's `mounts.conf`, re-create its instances (`down` then `up` for each that will run again; the default `sandbox` included) |
| `REPO_STAGING/stage.sh` SOURCES paths | rewrite |
| `PseudoCoupHQ/Research/LAW.md`, `CLAUDE.md`, `DevComms/note_server_session_start_here.md`, the briefs under `Research/briefs/` | rewrite the host paths; container paths unchanged |
| the systemd unit `repo-daemon.service` | check its `WorkingDirectory`/paths; rewrite if any |
| `~/.claude-home-<user>-Programming-<repo>/` memory and session directories, keyed by the working directory | for every repo that moves, COPY (not move) its directory to the new key (`-home-<user>-Programming-PUBLIC-<repo>` / `-home-<user>-Programming-PRIVATE-<repo>`), so the next session opened in the new path finds its memory; leave the old directory in place |
| symlinks at the old paths | NONE: the daemon would discover a repo twice through a symlink |
| DevComms logs citing host paths | NOT edited: they are the record; their commands run inside the container by container paths |

## 3. Order of execution
1. Coordinator confirms the tower idle and no agent active. 2. Visibility
query re-run and pasted. 3. Laptop moves (`mv`, one per repo, listed
LITERAL before and after with `ls`). 4. Config rewrites (each file's diff
LITERAL). 5. Daemon restart and `repos` listing. 6. Tower moves and
mounts, instance re-creation, `airlock doctor` and `selftest.sh` pasted.
7. Memory directories copied, listed. 8. A smoke lane through
`remote_lane.sh` on the default instance reading `PseudoCoupHQ`.
9. Report as a DevComms log (next free number), every step with its
command and output; the two lists. Nothing is deleted anywhere; a leftover
is reported.
