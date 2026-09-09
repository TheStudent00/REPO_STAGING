# SandboxDesign

A general-purpose isolated execution sandbox: a podman container with a
hot-folder daemon inside it, and no route to the internet except a proxy
that only permits hostnames declared in advance.

SandboxDesign is **not** built for any one project. It is a template —
one container image, one drop/status/logs protocol, one egress gate — that
any project under `<WORKSPACE_DIR>` can use the same way. This document
describes the tool on its own terms. Where an example helps, it is written
generically ("a project might drop a lane that..."); a live user of the
tool is named only where unavoidable, and marked as one user among others.

## What it is, mechanically

- `up.sh` starts two containers: `sandbox-runner` (does the work) and
  `sandbox-proxy` (the only thing `sandbox-runner` can reach on the
  network).
- You write a bash script into `agent/drop/`.
- A daemon (`daemon/watcher.py`) inside `sandbox-runner` watches that
  folder and runs each script it sees, **serially**, one after another.
- You poll `agent/status/<name>.status` for the run's state
  (`state=running`, then `state=done exit=<rc>`).
- Whatever the script printed lands in `agent/logs/`; whatever it wrote to
  `/out` lands in `agent/out/`.

That loop — write a script, a run happens, read a status file, read the
output — is the entire interface. There is no API, no queue client, no
language binding. It is four folders and a naming convention.

## What it is for

Running work that is untrusted, long-running, or resource-hungry, off the
host's main environment, with:

| property | how it is enforced |
|---|---|
| capped CPU share | `sandbox-runner` starts with `--cpus "$SANDBOX_CPUS"` |
| capped memory | `sandbox-runner` starts with `--memory 12g`; `sandbox-proxy` with `--memory 512m` |
| size-capped scratch filesystem | `/work` and `/tmp` are tmpfs with fixed `size=` caps — a run that exceeds one fails loudly with ENOSPC instead of filling the host disk |
| dropped capabilities | both containers start `--cap-drop=ALL --security-opt no-new-privileges` |
| egress proxy with an allowlist | `sandbox-runner` sits on a podman network created `--internal` (no route out exists at all); its only reachable peer is `sandbox-proxy`, a default-deny squid that refuses any hostname not in `proxy/allowlist.txt` |

None of this reads temperature or backs off dynamically — every cap above
is a fixed number, changed by hand. See CONFIGURATION below for where each
one lives.

## The contract — what SandboxDesign owns, what a project owns

This is the seam the owner has asked to keep clean, repeatedly: **SandboxDesign
is not a project-specific solution.** A project keeps its own copy of
whatever is project-specific — its own lane scripts, its own generators,
its own data — inside its own repo, and only ever hands SandboxDesign a
bash script to run. Nothing project-specific belongs in this repo.

| SandboxDesign owns | a project owns |
|---|---|
| the container image and the toolchains baked into it | its own lane scripts — the bash files that actually do the work |
| the `drop` / `status` / `logs` / `out` protocol | the generators, compilers, and probes those lane scripts call |
| the batch manifest format (`agent/batch.json`) and `progress.sh`'s reporting of it | its own data, fixtures, and results |
| the egress allowlist *mechanism* (`allow.sh`, `proxy/allowlist.txt`) | which hostnames it needs added to that allowlist |
| the `mounts.conf` *mechanism* (how a mount line is read and applied) | its own entries in that machine's `mounts.conf` (per-machine, gitignored, never committed here) |

A project's lane script is *dropped* here — copied in by `submit.sh`, or
written directly into `agent/drop/` — and archived once it has run. It is
never checked into this repo. If you find a project-specific script,
template, or wording living in SandboxDesign outside `mounts.conf` (which
is deliberately per-machine and gitignored), that is drift, not design —
see `DevComms/log_002_documentation_scope_correction.md` for a known
instance found while writing this document.

## How to use it from any project

Every script `cd`s to its own directory first, so these all work from
anywhere once you use the full path.

| command | what it does |
|---|---|
| `bash <WORKSPACE_DIR>/SandboxDesign/build.sh` | builds both container images — the only phase with open network access |
| `bash <WORKSPACE_DIR>/SandboxDesign/up.sh` | creates the two networks and starts the proxy and runner |
| `bash <WORKSPACE_DIR>/SandboxDesign/selftest.sh` | six checks that prove the sandbox behaves as designed (daemon alive, isolation holds, allowlist works both ways) |
| `bash <WORKSPACE_DIR>/SandboxDesign/submit.sh path/to/script.sh [--follow]` | hands one script to the running sandbox |
| `bash <WORKSPACE_DIR>/SandboxDesign/submit_project.sh <host-dir> <command...>` | copies a whole project directory in and runs a command against the copy (see "using this from a project" below) |
| `bash <WORKSPACE_DIR>/SandboxDesign/batch.sh <label> <lane.sh>:<weight> ...` | declares a batch manifest, so `progress.sh` can report weighted completion and an ETA across a set of lanes launched together |
| `bash <WORKSPACE_DIR>/SandboxDesign/progress.sh [-w]` | one snapshot (or `-w` to refresh every 2s) of queued/running/finished lanes, with a batch summary on top if one was declared |
| `bash <WORKSPACE_DIR>/SandboxDesign/allow.sh list\|add\|remove\|sync\|denied` | manage the egress allowlist — what the runner may reach, and what it tried to reach and was refused |
| `bash <WORKSPACE_DIR>/SandboxDesign/logs.sh [substring\|--daemon\|--pull DIR]` | read run logs out of the sandbox |
| `bash <WORKSPACE_DIR>/SandboxDesign/pull.sh <dest-dir> [--logs]` | copy `/out` (and optionally `/logs`) back to the host |
| `bash <WORKSPACE_DIR>/SandboxDesign/down.sh [--networks]` | stops and removes the containers |
| `bash <WORKSPACE_DIR>/SandboxDesign/probe_host.sh` | inventories the host machine's toolchains, read-only, into `DevComms/host_inventory.txt` |
| `bash <WORKSPACE_DIR>/SandboxDesign/install_quadlet.sh [--remove]` | hands the sandbox to systemd, so it survives reboots and restarts itself if the daemon crashes (replaces `up.sh`/`down.sh`; every other script above still works the same) |

## The `sandbox` command — a validating front end

`<WORKSPACE_DIR>/SandboxDesign/sandbox` is a single python3 file (stdlib
only) that checks a lane before it becomes a run. **It is a client, not a
replacement.** The file protocol above stays the truth: a hand-drop into
`agent/drop/` and every shell script in the table above keep working
exactly as they do now, with or without it.

```
python3 <WORKSPACE_DIR>/SandboxDesign/sandbox --help
<WORKSPACE_DIR>/SandboxDesign/sandbox doctor
```

| command | what it does |
|---|---|
| `sandbox up` / `sandbox down` / `sandbox allow ...` | delegate straight to `up.sh` / `down.sh` / `allow.sh`, so every podman flag keeps exactly one spelling — the CLI never repeats them |
| `sandbox submit <lane.sh> (--batch <label> [--weight N] \| --no-batch)` | validates the lane, then drops it hidden-then-renamed into `agent/drop/`. **A batch decision is mandatory**, so a lane is never queued without a denominator again |
| `sandbox status [<lane.sh>]` | compact view of one lane, or of the queue and the recent runs |
| `sandbox watch` | the same, refreshed |
| `sandbox doctor` | podman and container state, cores actually granted versus `SANDBOX_CPUS`, the `quadlet` / `up.sh` cpu disagreement, non-`.sh` clutter in `agent/drop`, toolchains inside the runner, the allowlist, and free space — each finding with a severity and a one-line "what to do" |

`submit` **refuses**, by name and with a non-zero exit, when the lane file
does not exist or is unreadable, when its name does not end in `.sh` or
starts with `.`, when a lane of that name is already queued in
`agent/drop` or already archived in `agent/drop/.done`, when the file has
no shebang, or when no batch decision was given. It **warns** but still
drops when the lane prints no `[n/total]`-style progress line, when the
shebang names something other than a shell, on CRLF line endings, and
when `--batch` was given with no `--weight`.

It does not reimplement `progress.sh` — every view ends by pointing at
it. `--root <dir>` (or `SANDBOX_DESIGN_ROOT`) points the CLI at a
different SandboxDesign tree.

Design, rationale and rendered output:
`DevComms/log_003_cli_plan_and_build.md`.

## Using this from a project

What a project-side "client" looks like **today**:

1. The project writes its own lane scripts — plain bash, one job each —
   and keeps them in its own repo. For example, a project might drop a
   lane that compiles and runs its probe programs, or a lane that runs its
   test suite against a read-only mount.
2. If several lanes are being launched together, the project calls
   `batch.sh <label> <lane1.sh>:<weight1> <lane2.sh>:<weight2> ...`
   **before** dropping any of them, so `progress.sh` can attribute weight
   from the first snapshot.
3. The project drops the lane scripts (`submit.sh`, or a direct write into
   `agent/drop/` for a session that has no shell — see `agent/README.md`).
4. The project polls `agent/status/<lane>.status` per lane, or watches
   `progress.sh` for the whole batch, and reads `agent/logs/` and
   `agent/out/` for results.

**This is a file-based protocol. There is no library wrapper yet** — no
importable module, no function calls, just files landing in folders
according to the naming convention above. A thin project-side client (a
small module that writes lane scripts, writes the batch manifest, drops
them, and polls status on the project's behalf) is a **possible future
addition that has not been designed or ruled on**. Building one is a
structural decision the owner wants to discuss first — nothing here should be
read as a proposal for its shape.

## Configuration

| setting | default | where it lives | how to change it |
|---|---|---|---|
| `SANDBOX_CPUS` | **6** (the full share; ruled 2026-08-22 — default is full, the user throttles as they see fit) | read by `up.sh` at container start | `SANDBOX_CPUS=3 ./up.sh` throttles a long run so it does not hold every core hot for hours; roughly halving the cores roughly doubles the wall clock. A fixed share, not a feedback loop. The systemd unit carries the same default. |
| runner memory | `12g` | `--memory` in `up.sh`; `Memory=12g` in `quadlet/sandbox-runner.container` | edit both places — they are not derived from one source |
| proxy memory/CPU | `512m` / `1` cpu | `up.sh` | fixed; the proxy does no compute work, so it is not expected to need more |
| `/tmp` tmpfs cap | `2g` | `--tmpfs` in `up.sh`; `Tmpfs=` in the quadlet unit | raise deliberately if a run needs more; a run that exceeds the cap fails loudly with ENOSPC rather than filling the host disk |
| `/work` tmpfs cap | `4g` | same as above | same as above — this is also where `submit_project.sh` copies a project in, so a multi-gigabyte copy-in needs the cap raised first, or should use a read-only mount from `mounts.conf` instead of a copy |
| `LANE_NICE` | `15` | env var read by `daemon/watcher.py`, applied via `os.nice()` before each lane execs | set the env var on the container; a lane still competes for CPU under the `SANDBOX_CPUS` cap, just gently |
| `mounts.conf` | none (no mounts exposed) | `<WORKSPACE_DIR>/SandboxDesign/mounts.conf`, gitignored, per-machine | `cp mounts.conf.example mounts.conf` and edit; one `<host>:<container>[:mode]` per line, default read-only. This file legitimately names real project paths — it is *configuration*, not documentation, so it is exempt from the project-neutral rule that applies to the rest of this repo. |
| egress allowlist | Ubuntu/Python/Rust/Go/Node/Java/GitHub/Swift hosts (see `proxy/allowlist.txt.example`) | `proxy/allowlist.txt`, gitignored, per-machine live copy, managed through `allow.sh` | `bash <WORKSPACE_DIR>/SandboxDesign/allow.sh add <hostname>...`, which rewrites the file and reloads squid without restarting the container |

Note: the checked-in `quadlet/sandbox-runner.container` unit currently
hardcodes `PodmanArgs=--cpus=6`, independent of the `SANDBOX_CPUS`
environment variable `up.sh` reads. Whether that is deliberate (the
systemd-managed path is meant to run at full speed by default) or a
gap left when the `SANDBOX_CPUS` knob was added to `up.sh` is not
recorded anywhere — **unverified**, flagged for the owner below.

## The image inventory

Verified directly against `Containerfile` on 2026-08-22, not carried over
from older prose.

| category | what is installed |
|---|---|
| compilers / build tools | gcc-15, g++-15, clang-21, lld-21, llvm-21 (symlinked to unsuffixed names), make, cmake, ninja-build, pkg-config, build-essential |
| Python | Ubuntu's own `python3` (3.14, ships with the base image) **and** a separately installed Python 3.13 (via `uv`, to match the host's development version), placed in a writable venv at `/opt/venv` that is first on `PATH` — so `python`, `python3`, and `pip` all mean 3.13 inside the container; Ubuntu's own tooling still uses `/usr/bin/python3` (3.14) by hardcoded path |
| Go | golang-1.26, on `PATH` via `/usr/lib/go-1.26/bin` |
| Rust | 1.96.1, installed via rustup (not apt-packaged), under `/opt/cargo` / `/opt/rustup` |
| Node | apt's `nodejs`/`npm`, with a best-effort upgrade to `npm@11` that is allowed to fail without failing the build if the distro's node is too old for it |
| Java | openjdk-25-jdk-headless |
| other languages | ruby, perl, php-cli |
| misc tooling | git, jq, ripgrep, fd-find (symlinked to `fd`), plocate, inotify-tools, unzip, xz-utils, curl, wget, ca-certificates |

**Deliberately absent, by decision (2026-08-22):** Haxe and Flutter — the
`Containerfile`'s own comment records this as deferred by the owner on
2026-07-30.

**Also absent, verified against the `Containerfile`, but not recorded
anywhere as a deliberate decision** (so treat the omission as current
fact, not a ruled-on choice): .NET/dotnet, Anaconda/conda, Kotlin, Scala,
Swift, Dart, Zig, Nim, OCaml, Haskell, Julia, R, Lua. If a project needs
one of these, adding it to the `Containerfile` is a build-image change,
not a per-run configuration change.

## How the parts fit

```
  ┌────────────────────────────────────────────────────────┐
  │ host                                                    │
  │                                                        │
  │   ./submit.sh ──podman cp──┐                           │
  │                            │                           │
  │  ┌─────────────────────────▼───────────────────────┐   │
  │  │ sandbox-runner                                  │   │
  │  │   /drop   scripts land here, daemon watches it  │   │
  │  │   /logs   one log per run                       │   │
  │  │   /work   scratch, cwd for every script         │   │
  │  │                                                 │   │
  │  │   network: sandbox-internal ONLY                │   │
  │  │   (created --internal: no route out exists)     │   │
  │  └──────────────────┬──────────────────────────────┘   │
  │                     │ http_proxy=sandbox-proxy:3128    │
  │  ┌──────────────────▼──────────────────────────────┐   │
  │  │ sandbox-proxy                                   │   │
  │  │   squid, default-deny                           │   │
  │  │   allows only hostnames in allowlist.txt        │   │
  │  │   never decrypts TLS — matches the plaintext     │   │
  │  │   "CONNECT host:443" line and tunnels or denies │   │
  │  │                                                 │   │
  │  │   networks: sandbox-internal + sandbox-egress   │   │
  │  └──────────────────┬──────────────────────────────┘   │
  └─────────────────────┼──────────────────────────────────┘
                        ▼
                    internet
```

## The agent lane — running things without a shell

A Cowork/Claude session can write files under `<WORKSPACE_DIR>` but cannot
run podman. `agent/` bridges that: four host directories bound into the
runner, so a **file write becomes a run**.

```
agent/drop/     -> /drop     write x.sh here; daemon runs it
agent/status/   -> /status   daemon writes x.sh.status (poll this)
agent/logs/     -> /logs     one log per run
agent/out/      -> /out      whatever the script produced
```

A direct write is safe: the daemon watches `close_write` as well as
`moved_to`, so it fires when the writer closes the file, never mid-write.
The status file's path follows from the script's name — the log's does
not, because it embeds the run timestamp — so a poller reads one
predictable path to learn `state=running` / `state=done exit=<rc>`.

`/work` is a size-capped tmpfs (see CONFIGURATION). `/persist` is a named
volume for iterating across runs — opt-in, because persistence carries
corruption forward where copy-per-run cannot.

**Consequence for `submit_project.sh`, know this before you hit it.** It
copies the project into `/work`, which is capped, so copying a
multi-gigabyte tree there fails with ENOSPC rather than silently
consuming the host disk. If a project is already exposed read-only under
`...` via `mounts.conf`, a lane script can use it in place
instead of copying — faster, and immune to the cap. If a genuinely large
copy-in is required, raise the cap deliberately in `up.sh` and the
quadlet unit, or stage it through `/persist`.

See `agent/README.md` for the loop in full and `agent/templates/` for
example lane scripts.

Lane scripts run niced (`LANE_NICE`, see CONFIGURATION) so a long lane
leaves the host responsive for anything else run on it at the same time.
Paired with the CPU cap.

### Progress, and the batch manifest

```
bash <WORKSPACE_DIR>/SandboxDesign/progress.sh          one snapshot
bash <WORKSPACE_DIR>/SandboxDesign/progress.sh -w       refresh every 2s
```

Always shows: queued lanes, the running lane with its latest progress
line, live processes inside `sandbox-runner`, and the ten most recently
finished lanes.

If a set of lanes was launched together as a **batch**, `progress.sh` also
prints a short summary block at the top: lanes done / total, percentage
**by weight** (not by lane count — a large lane and a small lane are not
equal), elapsed time, and an ETA. The current lane gets its own
percentage (read from a `[n/total]`-style line in its log) and its own
ETA. Every ETA is labeled an estimate, and prints "not enough data yet"
rather than a number computed from too little throughput (nothing
finished yet, or under 5 seconds elapsed).

The batch is declared by writing `agent/batch.json` **before** dropping
any lane script:

```
bash <WORKSPACE_DIR>/SandboxDesign/batch.sh <label> <lane.sh>:<weight> [<lane2.sh>:<weight2> ...]

# example
bash <WORKSPACE_DIR>/SandboxDesign/batch.sh acceptance-sweep \
    verify.sh:40 all.sh:120 rust.sh:60
```

`weight` is any comparable unit shared across the lanes in that batch —
for example, work-item count. The manifest itself:

```json
{
  "batch_id": "batch-20260822T140512Z",
  "label": "acceptance-sweep",
  "created": "2026-08-22T14:05:12+00:00",
  "lanes": [
    { "script": "verify.sh", "weight": 40 },
    { "script": "all.sh", "weight": 120 },
    { "script": "rust.sh", "weight": 60 }
  ]
}
```

`progress.sh` matches each lane's `script` name against
`agent/status/<script>.status` the same way the rest of the agent lane
does. `agent/batch.json` is per-run state, not part of the template, so it
is gitignored (`agent/.gitignore`) the same way `agent/status/*.status`
and `agent/logs/*.log` are. With no manifest present, `progress.sh`
behaves exactly as it always has, plus one line noting the absence. A
missing or malformed manifest never makes it fail.

Teardown: `./down.sh`, or `./down.sh --networks` to remove the networks
too.

## Running it under systemd instead

`./up.sh` starts containers that die on reboot. `./install_quadlet.sh`
hands them to systemd instead — they come back on boot and restart if the
daemon crashes:

```
./install_quadlet.sh            # install units and start
systemctl --user status sandbox-runner
journalctl --user -u sandbox-runner -f
./install_quadlet.sh --remove   # go back to ./up.sh
```

Every other script (`submit.sh`, `submit_project.sh`, `logs.sh`,
`allow.sh`, `pull.sh`, `selftest.sh`) works the same either way.

## Why scripts are submitted hidden-then-renamed

The kernel signals a new file when it is *created*, not when the writer
has finished. A daemon reacting to creation will sometimes execute a
script that is only half on disk.

`submit.sh` copies the file in as `/drop/.name.sh` and then renames it to
`/drop/name.sh`. The daemon ignores every name starting with `.`, and
reacts to the rename. A rename inside one directory is atomic, so
`/drop/name.sh` never exists in a partial state. `selftest.sh` check 3
verifies this.

## Files

- `Containerfile` — runner image; toolchains listed above
- `daemon/watcher.py` — the hot-folder daemon; inotify via ctypes, no pip
  dependencies; writes `/status/<name>.status` per run and records `/work`
  headroom
- `agent/` — the unattended lane: `drop/ status/ logs/ out/` bound from
  the host, plus `templates/`. See `agent/README.md`
- `proxy/Containerfile.proxy`, `proxy/squid.conf`, `proxy/allowlist.txt`
  (per-machine, gitignored), `proxy/allowlist.txt.example` (committed
  baseline) — the egress gate
- `build.sh` `up.sh` `down.sh` `submit.sh` `logs.sh` `allow.sh`
  `selftest.sh` — operator commands
- `progress.sh` — snapshot of every lane (queued/running/finished); prints
  a batch summary at the top when `agent/batch.json` is present
- `batch.sh` — writes `agent/batch.json`, the manifest `progress.sh` reads
  for overall percentage and ETA
- `submit_project.sh` — copy a host directory into `/work` and run a
  command against the copy
- `pull.sh` — bring `/out` (and optionally `/logs`) back to the host
- `report.sh` — writes container state + selftest results to
  `DevComms/sandbox_report.txt`, so pushing makes them readable from a
  Cowork session
- `quadlet/*.container`, `quadlet/*.network`, `install_quadlet.sh` —
  systemd units, for running the sandbox as a managed service
- `probe_host.sh` — host inventory, read-only
- `mounts.conf.example` — the template for `mounts.conf` (per-machine,
  gitignored); see CONFIGURATION
- `sandbox` — a validating python3 front end over the same file protocol;
  see "The `sandbox` command" above and
  `DevComms/log_003_cli_plan_and_build.md`
- `create_github_repo.sh`, `git_commit_push.sh` — one-time repo setup and
  add-commit-push, run by the owner on the host (the sandbox itself cannot push)
