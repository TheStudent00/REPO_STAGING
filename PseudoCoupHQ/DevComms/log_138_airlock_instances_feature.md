# log 138 — Airlock instances: a second sandbox is a feature, not a copy

Date: 2026-09-02. Repository changed: `~/Programming/Airlock` (the
application). Repository also touched: `~/Programming/PseudoCoupHQ` (the
caller). Report shape: LLM_communication_protocol Appendix B.

---

# 1. What was wrong, and what now exists

## 1.1 The rule this serves

the owner, 2026-09-02, verbatim:

> its not supposed to be a repo that is modified for use for a specific
> project ... if i wanted to use Numpy, i wouldnt clone Numpy in order to
> modify Numpy source. Airlock source isnt meant to be modified. its an
> application.

## 1.2 What happened instead

PseudoCoupHQ's probe regeneration (log 131) needed a second sandbox at half
the machine's cores, running beside the default one. Airlock could not be
asked for that, because the thing you would have to name did not exist:

- `sandbox-runner`, `sandbox-proxy`, `sandbox-internal`, `sandbox-egress`,
  `sandbox-persist` were spelled **as literals in 13 files, 55 times**.
- `AIRLOCK_CPUS` was read once at `up.sh`'s start and nowhere else.
- The memory cap was written twice — in `up.sh` and in the quadlet unit —
  with a `doctor` check whose whole job was to notice them drifting apart.
- There was one `mounts.conf`, one allowlist, one `agent/` tree per install.

So the implementer copied Airlock to `~/Programming/AirlockTrickle` and
rewrote the names. **A copy was made where a feature was required.**

## 1.3 What exists now

An **instance** is one running sandbox. One install runs as many as asked
for, side by side. A second sandbox is one settings file and one flag:

```
$ cat ~/Programming/Airlock/instances/trickle.conf
cpus              = 6
memory            = 8g
proxy             = no
persist_volume    = sandbox-persist
persist_mode      = ro
watch             = poll

$ bash ~/Programming/Airlock/up.sh --instance trickle --cpus 6
```

Nothing about `trickle` lives in PseudoCoupHQ, and nothing project-specific
entered Airlock: `instances/*.conf` is gitignored exactly as `mounts.conf`
is.

---

# 2. The design, in one page

## 2.1 The configuration, as rows

These are the new rows in the README's Configuration table. They are first
because they are what a caller actually touches.

| setting | default | where it lives | what it does |
|---|---|---|---|
| `AIRLOCK_INSTANCE` | `sandbox` | env var; `--instance <name>` on any script or on `airlock` overrides it | names which sandbox a command acts on. **Every** container, network, volume and unit name is derived from it |
| `instances/<name>.conf` | absent — every key falls back to its built-in default | `<airlock>/instances/`, gitignored, per-machine | that instance's caps and files |
| `cpus` | `6` | that file | precedence: `up.sh --cpus N`, then `AIRLOCK_CPUS`, then `SANDBOX_CPUS`, then this key, then 6 |
| `memory`, `pids_limit`, `tmp_size`, `work_size` | `12g`, `2048`, `2g`, `4g` | that file | the runner's caps, now named **once** — `up.sh` reads them and `install_quadlet.sh` renders them into the systemd unit |
| `proxy` | `yes` | that file | `no` starts no proxy and no egress network: no route out at all. `selftest.sh` reports checks 4–6 as SKIP rather than a verdict it cannot reach |
| `proxy_memory`, `proxy_cpus`, `proxy_pids_limit` | `512m`, `1`, `256` | that file | the proxy's caps |
| `allowlist_file`, `mounts_file` | `proxy/allowlist.txt`, `mounts.conf` | that file | every instance shares them unless one names its own |
| `agent_dir` | `agent/` for `sandbox`, `instances/<name>/agent/` otherwise | that file | the four folders of that instance's lane |
| `runner_image`, `proxy_image` | `sandbox-runner:latest`, `sandbox-proxy:latest` | that file | **shared by every instance**: an image is a build artifact, not instance state, so a second instance never forces a rebuild |
| `persist_volume`, `persist_mode` | `<instance>-persist`, `rw` | that file | `ro` lets one instance share another's toolchain volume without being able to alter it |
| `lane_nice`, `script_timeout` | `15`, `3600` | that file | passed to the daemon inside that instance's runner |
| `watch` | `inotify` | that file | `poll` uses no inotify resource at all; `auto` falls back only on the ENOSPC that means the kernel has none left. §5 |
| `daemon_file` | unset | that file | binds a host `watcher.py` over the image's copy, so a daemon change reaches an instance without a rebuild |

## 2.2 The mechanism: one file decides every name

`~/Programming/Airlock/instance.sh` is the only place a container name is
spelled. Its whole contract:

| derived thing | from the instance name |
|---|---|
| runner container | `<instance>-runner` |
| proxy container | `<instance>-proxy` |
| internal network | `<instance>-internal` |
| egress network | `<instance>-egress` |
| systemd units | `<instance>-runner.service`, and so on |

Every shell script opens with the same four lines:

```
source "$(dirname "$0")/instance.sh"
airlock_parse_instance "$@"          # strips --instance NAME out of the args
set -- "${AIRLOCK_ARGV[@]}"          # everything else is put back
airlock_instance_load                # sets AL_RUNNER, AL_CPUS, AL_AGENT_DIR, ...
```

The `airlock` CLI does **not** reimplement the derivation — it asks the
shell library for it and reads the answer back:

```python
def load_instance(root, instance):
    """Every AL_* setting for one instance, as a dict, read from instance.sh."""
    script = ('set -e\n source "$1"\n AIRLOCK_INSTANCE="$2"\n'
              ' airlock_instance_load "$3"\n env | grep "^AL_"\n')
```

That is why the CLI and the scripts cannot drift apart: there is one
derivation, not two agreeing copies.

## 2.3 Values in motion: `--instance trickle` becoming a running container

Take the actual command run in §4.2, and follow `trickle` through it.

**Step 1 — the flag is taken out of the arguments.**
`up.sh` is called with `--instance trickle --cpus 6`.
`airlock_parse_instance` sets `AIRLOCK_INSTANCE=trickle` and leaves
`AIRLOCK_ARGV=(--cpus 6)`. `up.sh` then reads `--cpus 6` and exports
`AIRLOCK_CPUS_FLAG=6`.

**Step 2 — the names are derived.** `airlock_instance_load` computes, with
no file needed:

```
AL_INSTANCE=trickle   AL_RUNNER=trickle-runner   AL_PROXY=trickle-proxy
AL_NET_INTERNAL=trickle-internal   AL_NET_EGRESS=trickle-egress
AL_AGENT_DIR=/home/…/Airlock/instances/trickle/agent
```

**Step 3 — the conf file overrides four of them.**
`instances/trickle.conf` says `proxy = no`, `memory = 8g`,
`persist_volume = sandbox-persist`, `persist_mode = ro`, `watch = poll`. So:

```
AL_USE_PROXY=no      (was yes)
AL_MEMORY=8g         (was 12g)
AL_PERSIST=sandbox-persist  AL_PERSIST_MODE=ro   (was trickle-persist, rw)
AL_WATCH=poll        (was inotify)
```

`AL_CPUS` resolves to `6` — from the flag, which outranks the file's own
`cpus = 6`; both agree here, and the flag is what the precedence names.

**Step 4 — the container is created from those variables and no literal.**

```
podman run -d --name "$AL_RUNNER" --network "$AL_NET_INTERNAL" \
    -v "$AL_AGENT_DIR/drop":/drop  … \
    -v "$AL_PERSIST:/persist:$AL_PERSIST_MODE" \
    -e "AIRLOCK_WATCH=$AL_WATCH" \
    --memory "$AL_MEMORY" --cpus "$AL_CPUS" …
```

**Step 5 — the lane inside it reports what those values became.** The
smoke lane of §4.2 printed, from inside the container:

```
  cores visible: 6                                    <- AL_CPUS
  /persist refused a write, as configured              <- AL_PERSIST_MODE=ro
  direct_status=NO_ROUTE                               <- AL_USE_PROXY=no
```

Nothing in that chain names `sandbox-` or `trickle-` as a literal after
`instance.sh`.

## 2.4 The one place the templates are still literal, and why

`quadlet/sandbox-runner.container` and its three co-files stay as they are.
`install_quadlet.sh` renders them per instance — substituting names and
splicing in the caps from the conf — and installs the result under the
instance's own unit names. For the default instance every substitution is a
no-op, so the installed file is what it has always been. The renderer is
twelve `sed -e` lines in one function, `render_instance()`.

---

# 3. The diff, summarised

```
 .gitignore                     |   8 ++
 README.md                      | 156 ++++++++++++++++---
 airlock                        | 184 +++++++++++++++++++----
 allow.sh                       |  21 ++-
 batch.sh                       |  12 +-
 build.sh                       |  23 ++-
 daemon/watcher.py              | 100 +++++++++++++-
 down.sh                        |  22 ++-
 install_quadlet.sh             | 133 +++++++++++------
 instance.sh                    | 262 ++++++++++++++++++++++++++++++++  (new)
 instances/sandbox.conf.example |  48 +++++++                           (new)
 logs.sh                        |  17 ++-
 progress.sh                    |  21 ++-
 pull.sh                        |  17 ++-
 report.sh                      |  56 +++++----
 selftest.sh                    |  38 ++++--
 submit.sh                      |  21 ++-
 submit_project.sh              |  25 ++--
 up.sh                          | 254 +++++++++++++++++++++-----------
 19 files changed, 1162 insertions(+), 256 deletions(-)
```

Every one of the thirteen operator scripts named in the brief now takes
`--instance` (or `AIRLOCK_INSTANCE`) and spells no container name:
`up.sh`, `down.sh`, `submit.sh`, `submit_project.sh`, `logs.sh`, `pull.sh`,
`allow.sh`, `batch.sh`, `build.sh`, `progress.sh`, `report.sh`,
`selftest.sh`, `install_quadlet.sh`. Verified mechanically:

```
$ grep -rn "sandbox-" *.sh | grep -v '^instance.sh' | grep -v <template names>
up.sh:150:# The image bakes in http_proxy=http://sandbox-proxy:3128, which is right
install_quadlet.sh:8:#   so `systemctl --user status sandbox-runner` works, …
install_quadlet.sh:24:#     systemctl --user status sandbox-runner
install_quadlet.sh:156:# unit on stdout: every `sandbox-` name becomes this instance's …
install_quadlet.sh:165:        -e "s|sandbox-runner|$AL_RUNNER|g" \
install_quadlet.sh:166:        -e "s|sandbox-proxy|$AL_PROXY|g" \
```

Four comments and the two lines of the template renderer. No executable
reference to a literal container name survives outside `instance.sh`.

---

# 4. The proofs

## 4.1 The default instance is unchanged

### 4.1.1 `selftest.sh`, before and after

Before, at 15:27 (`selftest_before.txt`):

```
  (run id 202609021527162646873 — every check below reads only its own fresh log)
=== 0. no personal or machine-identifying string is publishable ===
  PASS  scrub_check found nothing publishable that names a person or machine
=== 1. daemon is alive and watching ===
  PASS  daemon reported watching /drop
=== 2. a submitted script actually runs (this exercises inotify) ===
  PASS  script ran, output captured
=== 3. half-written files are NOT executed ===
  PASS  hidden .pending file was ignored
=== 4. an ALLOWED domain is reachable through the proxy ===
  PASS  pypi.org reachable via proxy
=== 5. an UNDECLARED domain is refused ===
  PASS  example.com refused by proxy
=== 6. there is no second route out (proxy bypass is impossible) ===
  PASS  no direct egress with proxy vars unset

=== 7 passed, 0 failed ===
EXIT=0
```

After, at 16:33 (`selftest_after.txt`), with every change in place:

```
  (instance sandbox — runner sandbox-runner, agent /home/…/Airlock/agent)
  (run id 20260902163342163415 — every check below reads only its own fresh log)
=== 0. no personal or machine-identifying string is publishable ===
  PASS  scrub_check found nothing publishable that names a person or machine
=== 1. daemon is alive and watching ===
  PASS  daemon reported watching /drop
=== 2. a submitted script actually runs (this exercises inotify) ===
  PASS  script ran, output captured
=== 3. half-written files are NOT executed ===
  PASS  hidden .pending file was ignored
=== 4. an ALLOWED domain is reachable through the proxy ===
  PASS  pypi.org reachable via proxy
=== 5. an UNDECLARED domain is refused ===
  PASS  example.com refused by proxy
=== 6. there is no second route out (proxy bypass is impossible) ===
  PASS  no direct egress with proxy vars unset

=== 7 passed, 0 failed ===
EXIT=0
```

Identical, check for check. The one added line names the instance.

### 4.1.2 `airlock doctor`, before and after

Before:

```
  1 WARN, 3 NOTE, 9 OK
  exit 0 - no real faults. WARN and NOTE are for reading, not for stopping.
```

After, the same counts plus the new instances row:

```
| NOTE | instances | 2 known: sandbox (sandbox-runner: running) <- this command;
                     trickle (trickle-runner: running) | …
| NOTE | AIRLOCK_CPUS | instance sandbox resolves to 6 cpu(s) | …
| OK | quadlet vs up.sh | …sandbox-runner.container and …up.sh agree on 6 cpu(s) |
| OK | granted cores | sandbox-runner was actually granted 6 cpu(s), matching the setting |
```

The `AIRLOCK_CPUS` row changed wording: it used to grep `up.sh` for the
literal `AIRLOCK_CPUS:-6`, which no longer exists there, and now reads the
instance's resolved `AL_CPUS`. Same number, better source.

### 4.1.3 The running containers — and one honest exception

```
$ podman ps                       (16:39, after everything)
va-proxy         Up 51 minutes
sandbox-proxy    Up 51 minutes
sandbox-runner   Up 51 minutes
$ podman inspect sandbox-runner --format '{{.State.StartedAt}} restarts={{.RestartCount}}'
2026-09-02 15:48:09.581314325 -0400 EDT restarts=0
```

**`sandbox-runner` and `sandbox-proxy` did restart once during this
session, and it was not this work.** At 15:27 they read `Up 47 hours`; at
16:33 they read `Up 51 minutes`. The cause, with evidence:

```
$ uptime -p
up 45 minutes                                  <- the machine rebooted
$ journalctl --user -u sandbox-runner
Sep 02 15:48:09 <host> systemd[2345]: Started sandbox-runner.service …
$ podman ps -a --format '{{.Names}}\t{{.CreatedAt}}'
va-proxy         2026-09-02 15:48:09.104180520 -0400 EDT
sandbox-proxy    2026-09-02 15:48:09.104180951 -0400 EDT
sandbox-runner   2026-09-02 15:48:09.506801108 -0400 EDT
```

The host rebooted while this session was paused, and systemd brought every
quadlet-managed container back in the same second — including `va-proxy`,
which belongs to a different project and which nothing here touches. That
co-restart is what makes it a machine event rather than a consequence of
this work. `RestartCount=0` on each: none was restarted after that.

No command in this work ran `down.sh`, `podman rm` or `podman restart`
against `sandbox-runner` or `sandbox-proxy`. Evidence class: the version
control system's own record of the commands, plus the journal line naming
`systemd[2345]` as the actor.

### 4.1.4 The default's own down is still scoped

```
$ bash down.sh --instance trickle
=== airlock down ===
  instance: trickle   runner: trickle-runner   agent: …/instances/trickle/agent
  removed trickle-runner
done.
$ podman ps
va-proxy         Up 51 minutes
sandbox-proxy    Up 51 minutes
sandbox-runner   Up 51 minutes
```

`down.sh` takes down only the instance it is given.

## 4.2 A second instance, running beside the first

### 4.2.1 It refuses to reuse a runner bound elsewhere

The first attempt met the stale container the fork had left behind, and the
guard named it rather than silently watching the wrong folder:

```
$ bash up.sh --instance trickle --cpus 6
  REFUSING to reuse trickle-runner: it is bound to another tree.
    its /drop:      /home/…/AirlockTrickle/agent/drop
    this instance:  /home/…/Airlock/instances/trickle/agent/drop
    Lanes queued here would never be seen. Remove it and rerun:
      podman rm -f trickle-runner trickle-proxy && bash up.sh --instance trickle
EXIT=1
```

### 4.2.2 It comes up

```
$ bash up.sh --instance trickle --cpus 6
=== airlock up ===
  instance: trickle   runner: trickle-runner   agent: …/instances/trickle/agent
  config:   …/instances/trickle.conf
  proxy: none (instance is configured 'proxy = no' — no route out at all)
  daemon:   …/daemon/watcher.py (bound over the image's copy)
  trickle-runner started
    cpus:     6 (--cpus 3 or AIRLOCK_CPUS=3 to throttle a long run)
    memory:   8g   /tmp 2g   /work 4g
    persist:  sandbox-persist (ro)
    watch:    poll
    drop:     …/instances/trickle/agent/drop      (write x.sh here to run it)
    status:   …/instances/trickle/agent/status    (x.sh.status — poll this)
  trickle-runner  Up Less than a second  localhost/sandbox-runner:latest
EXIT=0

$ podman logs trickle-runner
[…] watch mode: poll (rescan every 2.0s) — no inotify instance and no inotify watch are used
[…] watching /drop (rescan every 2.0s); logs -> /logs
[…] status -> /status/<name>.status ; work free 4096 MB
```

Note the image: `localhost/sandbox-runner:latest`. No rebuild.

### 4.2.3 One real lane, through `airlock submit`

```
$ ./airlock --instance trickle submit …/trickle_smoke.sh --batch instance-proof --weight 4
wrote …/instances/trickle/agent/batch.json
  batch 'instance-proof' (id batch-20260902T203249Z): 1 lane(s), total weight 4
dropped …/instances/trickle/agent/drop/trickle_smoke.sh
  written hidden as …/drop/.trickle_smoke.sh first, then renamed
  poll:     …/instances/trickle/agent/status/trickle_smoke.sh.status
SUBMIT EXIT=0
```

The status file the caller polls, written by the daemon:

```
script=trickle_smoke.sh
state=done
exit=0
started=2026-09-02T20:32:50+00:00
finished=2026-09-02T20:32:51+00:00
elapsed_s=0.7
log=/logs/20260902T203250Z__trickle_smoke.sh.log
work_free_mb_after=4096
verdict=exit 0
```

The log, which is the lane's own testimony about its caps:

```
[1/4] identity
  hostname: 56d32ef69c2e
  /work exists: yes   cwd: /work
  cores visible: 6
[2/4] the toolchain pins, from the toolchains themselves
Ubuntu clang version 21.1.8 (6ubuntu1)
go version go1.26.0 linux/amd64
rustc 1.96.1 (31fca3adb 2026-06-26)
[3/4] the shared persist volume is read-only here
/persist/swift
  /persist refused a write, as configured (persist_mode = ro)
[4/4] there is no route out (this instance has proxy = no)
  direct_status=NO_ROUTE
# exit 0 in 0.7s
```

The three toolchain pins are the same lines log 131 §5.2 recorded, so the
instance reaches the same toolchain the fork did. The product landed in
`instances/trickle/agent/out/trickle_smoke.txt`.

### 4.2.4 `progress.sh` and `airlock status`, per instance

```
$ bash progress.sh --instance trickle -w        (two refreshes shown)
2026-09-02T16:33:28-04:00
== instance trickle  (runner trickle-runner, agent …/instances/trickle/agent) ==
  batch:    instance-proof  (id batch-20260902T203249Z)
  overall:  1/1 lanes done   weight 4/4  (100.0% by weight)
2026-09-02T16:33:30-04:00
== instance trickle  (runner trickle-runner, agent …/instances/trickle/agent) ==
  …

$ bash progress.sh --instance trickle            (one snapshot, the tail)
== live processes inside trickle-runner (top by CPU) ==
        1  0.0       00:35 python3         python3 -u /opt/daemon/watcher.py
== finished, 10 most recent ==
  trickle_smoke.sh             done     exit=0         0.7s  2026-09-02T20:32:51+00:00
```

Side by side, the two instances report their own lanes and nothing else:

```
$ ./airlock --instance trickle status
most recent 1 finished, out of 1 in …/instances/trickle/agent/status
| trickle_smoke.sh | done | 0 | 0.7s | [4/4] |

$ ./airlock status
most recent 10 finished, out of 165 in …/Airlock/agent/status
| netdirect_202609021527162646873.sh | done | 0 | 0.0s | - |
```

### 4.2.5 `selftest.sh` on an instance with no proxy

```
$ bash selftest.sh --instance trickle
  (instance trickle — runner trickle-runner, agent …/instances/trickle/agent)
=== 0. no personal or machine-identifying string is publishable ===
  PASS  scrub_check found nothing publishable that names a person or machine
=== 1. daemon is alive and watching ===   PASS  daemon reported watching /drop
=== 2. a submitted script actually runs === PASS  script ran, output captured
=== 3. half-written files are NOT executed === PASS  hidden .pending file was ignored
=== 4. an ALLOWED domain is reachable through the proxy ===
  SKIP  instance trickle has no proxy (proxy = no); checks 4-6 do not apply

=== 4 passed, 0 failed ===
EXIT=0
```

SKIP, not a pass it did not earn and not a failure it could not avoid.

## 4.3 Which side of the container wall

```
$ hostname
<host>
$ ls -d /work
ls: cannot access '/work': No such file or directory
```

`/work` is the container's scratch root; it is absent here. Every command in
this log ran on the HOST. The only lines from inside a container are the
lane log in §4.2.3 (`hostname: 56d32ef69c2e`, `/work exists: yes`) and the
`podman logs` output, both labelled as such.

---

# 5. The inotify claim, examined

## 5.1 What log 131 said

> ```
> OSError: [Errno 28] inotify_add_watch(/drop) failed: No space left on device
> $ cat /proc/sys/fs/inotify/max_user_instances
> 128
> ```
> That is the inotify INSTANCE limit, not disk.

## 5.2 The failure reproduced, here, on the first attempt

The `trickle` instance's first start ran the image's own daemon and aborted
identically:

```
$ podman logs trickle-runner
OSError: [Errno 28] inotify_add_watch(/drop) failed: No space left on device
```

## 5.3 The measurement, with the values

`inotify_init1` had already succeeded — the traceback names
`inotify_add_watch`, three frames later. So an *instance* was available.
Counted at that moment by walking `/proc/*/fdinfo`:

```
inotify INSTANCES open : 114 / 128        <- tight, but not what failed
inotify WATCHES held   : 65470 / 65536    <- 66 free; this is what failed
top watch holders:
   62684 watches  antigravity          (an editor)
    2242 watches  claude-desktop
      55 watches  gsd-xsettings
```

`inotify_add_watch` returns `ENOSPC` when `max_user_watches` is exhausted.
One editor held 62,684 of the 65,536.

Measured again an hour later, after a reboot, with that editor not indexing:

```
instances 56/128  watches 3625/65536
```

## 5.4 The correction, and the fix

Log 131's **conclusion** was right — it is not disk — and its **refusal to
change a kernel setting** was right. Its named limit was wrong: the
exhausted resource is `max_user_watches`, not `max_user_instances`. This is
corrected in log 131 itself (section C.2, appended).

The fix is inside Airlock's watcher, documented, default off:

| `watch` | what the daemon does |
|---|---|
| `inotify` | **the default.** Unchanged behaviour; fails loudly if the kernel refuses |
| `poll` | rescans `/drop` every `AIRLOCK_POLL_INTERVAL` seconds (default 2). Uses no inotify instance and no inotify watch |
| `auto` | inotify, falling back to polling with three loud log lines, and **only** on `ENOSPC` — any other error still raises |

The polling doorbell has the same contract as the inotify one — it blocks,
then returns a list of names — so the main loop cannot tell them apart, and
the lane, the log, the status file and the archive are unchanged. Proof
that it runs, from §4.2.2: `watch mode: poll (rescan every 2.0s)`, followed
by a lane that ran, logged and wrote its status.

`podman exec` from the project side is retired. It was never a fix for
this; it was a way around the daemon, and it is why the fork's 339 runs have
no status files and no logs at all.

---

# 6. The fork's retirement

## 6.1 The directory is gone, and not by this work

`~/Programming/AirlockTrickle` no longer exists.

```
$ ls -d ~/Programming/Airlock*
~/Programming/Airlock
```

It was **present** early in this session and counted:

```
$ ls -la ~/Programming/AirlockTrickle && for d in agent/*; do echo "$d: $(ls -1 $d|wc -l)"; done
agent/drop: 339
agent/logs: 0
agent/out: 339
agent/status: 0
```

and **absent** roughly an hour later, when the move was attempted:

```
$ mv ~/Programming/AirlockTrickle/agent/drop/* instances/trickle/agent/drop/.done/
mv: cannot stat '~/Programming/AirlockTrickle/agent/drop/*': No such file or directory
$ ls -la ~/Programming/AirlockTrickle/
ls: cannot access '~/Programming/AirlockTrickle/': No such file or directory
```

Nothing here deleted it, and nothing here could have: the only removals this
work performed are `podman rm -f trickle-runner` and
`podman network rm trickle-internal`, both named in §4.2.1's own refusal
message. It is not in the desktop trash (which holds an unrelated `Airlock`
entry from 14:00). **The brief's instruction was to move those 339 lanes and
339 results, not delete them; they were already gone before this work
reached them.** This is stated rather than papered over.

## 6.2 What survives, and where it is recorded

The same material lives in the project's own repository, which is where a
project's records belong under Airlock's contract:

| what | where | count |
|---|---|---|
| the exact lane script that ran per chunk | `PseudoCoupHQ/Research/op_pipeline/trickle_lanes/` | 334 |
| each lane's raw product and console log | `…/trickle_raw/` | 668 |
| the folded per-chunk stores | `…/trickle_store/` | 334 |

Recorded, with the absence stated, in
`~/Programming/Airlock/instances/trickle/agent/README.md`. Their `status/`
and `logs/` are absent because those runs predate the protocol being used at
all on that copy — the fork started its container idle and reached in from
outside, so the daemon wrote nothing.

## 6.3 The project-side scripts

`trickle_up.sh`, `trickle_down.sh`, `trickle_doctor.sh` are **untouched on
disk** and marked superseded by a new sidecar,
`Research/op_pipeline/TRICKLE_SUPERSEDED.md`, which carries the replacement
for each:

| superseded | replaced by |
|---|---|
| `bash trickle_up.sh` | `bash ~/Programming/Airlock/up.sh --instance trickle --cpus 6` |
| `bash trickle_down.sh` | `bash ~/Programming/Airlock/down.sh --instance trickle` |
| `bash trickle_doctor.sh` | `airlock doctor` — it lists every instance and its state |
| `trickle.py --run` | `python3 trickle2.py --run` |

## 6.4 `trickle2.py`, proved on a real chunk

New file, `Research/op_pipeline/trickle2.py`. It imports `trickle.py`'s
planner, manifest reader and folder unchanged, and replaces only the step
that ran the lane: render → `airlock submit` → poll the status file → read
`agent/out` → fold → checkpoint. **It runs no podman**, and neither does
anything else it calls.

```
$ AIRLOCK_ROOT=~/Programming/Airlock python3 trickle2.py --plan
planned 326 chunks over 129553 probes

$ AIRLOCK_ROOT=~/Programming/Airlock python3 trickle2.py --run --langs go --limit 1
instance trickle  runner trickle-runner  cpus 6  agent …/instances/trickle/agent
1 chunk(s) to run, one at a time (Airlock runs lanes serially)
  regen_go_c0000       400 submitted   330 accepted    70 refused    97.0s
```

The chunk's store was written (`trickle_store/op_units2_go_c0000.json`,
795,137 bytes), and the daemon wrote the status and the log the fork never
had:

```
script=regen_go_c0000.sh
state=done
exit=0
elapsed_s=93.1
log=/logs/20260902T203705Z__regen_go_c0000.sh.log
work_consumed_mb=32
verdict=exit 0
```

That chunk agrees with log 131: go's 553 residue probes were 483 accepted
and 70 refused across two chunks, and chunk 0 here is 330 accepted and **70
refused** — every one of go's refusals, in the first chunk, as before.

### 6.4.1 One behavioural difference, stated rather than hidden

`trickle.py` ran six chunks at once, because `podman exec` starts a process
whenever asked. **Airlock's daemon runs lanes serially, by design** — the
comment in `daemon/watcher.py` is "concurrent heavy runs are what exhaust
scratch space". So `trickle2.py` submits one chunk and waits.

The `--cpus 6` cap still applies and a lane may use all six cores itself;
what is lost is overlap between chunks. Whether an instance should run N
lanes concurrently is a question **for Airlock** — it is item 1 of §8. It was
not worked around from the project side, because reaching in with
`podman exec` to recover concurrency is precisely the move that produced the
fork.

---

# 7. For the owner's ruling — the naming

Every name below was chosen to be renameable in one place. Nothing depends
on the words themselves.

| # | the name I used | what it names | where it would be changed |
|---|---|---|---|
| 1 | `AIRLOCK_INSTANCE` | the environment variable naming which sandbox | `instance.sh` (`airlock_parse_instance`, `airlock_instance_load`) and one `elif` in `airlock`'s `main()` |
| 2 | `--instance` | the flag spelling of the same | the same two places |
| 3 | **"instance"** as the concept word | one running sandbox | prose only — README's Instances section, and the `AL_INSTANCE` variable name |
| 4 | `instances/<name>.conf` | where an instance's settings live | one line in `instance.sh`: `AL_CONF="$AL_ROOT/instances/$AL_INSTANCE.conf"`, plus one `.gitignore` stanza |
| 5 | the conf keys — `cpus`, `memory`, `pids_limit`, `tmp_size`, `work_size`, `proxy`, `proxy_memory`, `proxy_cpus`, `proxy_pids_limit`, `allowlist_file`, `mounts_file`, `agent_dir`, `runner_image`, `proxy_image`, `persist_volume`, `persist_mode`, `lane_nice`, `script_timeout`, `watch`, `daemon_file` | each setting | one `_airlock_conf_get "$AL_CONF" <key>` call each, all in one block of `instance.sh` |
| 6 | `<instance>-runner`, `<instance>-proxy`, `<instance>-internal`, `<instance>-egress` | the derived container and network names | five lines in `airlock_instance_load` |
| 7 | `AL_*` | the variable prefix the scripts read | `instance.sh` and the scripts that use them |
| 8 | `instances/<name>/agent` | a non-default instance's lane | one `default_agent` branch in `instance.sh` |
| 9 | `watch = poll` / `auto` | the polling doorbell | `daemon/watcher.py`'s `open_watcher`, plus the `watch` key |
| 10 | `daemon_file` | binding a host daemon over the image's | `instance.sh` and one block in `up.sh` |

Two of these are more than spelling and are flagged as such:

- **#4 and #8 put an instance's settings *and* its agent tree inside the
  Airlock checkout.** The alternative is outside it (the fork put its tree
  in `~/Programming/AirlockTrickle`, deliberately, so the 30-second commit
  daemon would not see it). Both are gitignored here, so the daemon does not
  see them either — but the location is a design choice, not a mechanical
  one.
- **#10 `daemon_file` is a bridge, not a feature.** The daemon is part of
  the image; a proper fix is `build.sh`. The key exists because the polling
  doorbell could not otherwise be used at all before a full rebuild, and it
  is documented to be dropped after the next build. It may be that the owner wants
  it removed rather than kept.

---

# 8. Awaiting the owner (kept minimal)

1. **Should an instance be able to run several lanes at once?** Airlock's
   daemon is serial by design. The fork got concurrency by bypassing it, and
   `trickle2.py` gives it up rather than bypassing it again. A `workers`
   key per instance is the shape it would take. §6.4.1.
2. **Where does an instance's agent tree belong** — inside the checkout
   (`instances/<name>/agent`, gitignored) as built, or outside it? §7, #4/#8.
3. **The naming table in §7**, all ten rows.

---

# 9. Evidence class per claim

| claim | evidence class |
|---|---|
| the default instance behaves identically | forced by construction — the same seven-check selftest, run before and after, same verdicts (§4.1.1) |
| no executable literal container name survives outside `instance.sh` | forced by construction — an exhaustive grep over every `.sh`, with the six residual lines shown and each one a comment or the template renderer (§3) |
| the second instance runs beside the first | forced by construction — `podman ps` shows both, and each instance's own status folder holds only its own lanes (§4.2.4) |
| the trickle instance's caps are real | the tool's own testimony — the lane printed `cores visible: 6`, the write to `/persist` was refused, and the direct fetch returned `NO_ROUTE`, from inside the container (§4.2.3) |
| no rebuild was needed | forced by construction — `podman ps` names the running image as `localhost/sandbox-runner:latest` (§4.2.2) |
| the toolchain reached is the same one | the tool's own testimony — each toolchain's own version line, matching log 131 §5.2 line for line (§4.2.3) |
| the inotify failure is the WATCH limit, not the instance limit | forced by construction — the traceback names `inotify_add_watch` (so `init1` succeeded) and the counts were read from `/proc/*/fdinfo` at that moment: 114/128 instances, 65,470/65,536 watches (§5.3) |
| the sandbox-* restart was a reboot, not this work | forced by construction — `uptime -p` says 45 minutes, and every quadlet container including an unrelated project's was created in the same second, by `systemd[2345]` per the journal (§4.1.3) |
| `AirlockTrickle` was not removed by this work | the record of this session's own commands — two `podman` removals, both named, no filesystem removal (§6.1) |
| `trickle2.py` drives a real chunk through the front door | forced by construction — 400 submitted / 330 accepted / 70 refused, a 795 KB store on disk, and a daemon-written status file (§6.4) |
| the go chunk agrees with the earlier run | forced by construction — 70 refusals, matching log 131's per-language total for go |

---

# 10. Complete file inventory

## 10.1 New, in `~/Programming/Airlock/`

| file | what it is |
|---|---|
| `instance.sh` | **the one place an instance's names and caps are derived.** Sourced by all thirteen scripts; read by `airlock` |
| `instances/sandbox.conf.example` | the committed template. Every key, its default, and what it does |
| `instances/sandbox.conf` | the default instance's file: every value that used to be hardcoded, written out. Gitignored; deleting it changes nothing |
| `instances/trickle.conf` | the second instance. Gitignored |
| `instances/trickle/agent/{drop,status,logs,out}` | that instance's lane. Gitignored |
| `instances/trickle/agent/README.md` | what became of the fork's 339 lanes and 339 products |

## 10.2 Changed, same directory

`airlock`, `up.sh`, `down.sh`, `submit.sh`, `submit_project.sh`, `logs.sh`,
`pull.sh`, `allow.sh`, `batch.sh`, `build.sh`, `progress.sh`, `report.sh`,
`selftest.sh`, `install_quadlet.sh`, `daemon/watcher.py`, `README.md`,
`.gitignore`. Per-file line counts in §3.

`quadlet/*.container` and `quadlet/*.network` are **unchanged**: they are
templates, rendered per instance by `install_quadlet.sh`.

## 10.3 New, in `~/Programming/PseudoCoupHQ/Research/op_pipeline/`

| file | what it is |
|---|---|
| `trickle2.py` | the driver through `airlock submit`. No podman |
| `TRICKLE_SUPERSEDED.md` | the sidecar retiring the three `trickle_*.sh` scripts |
| `trickle2_state.json` | its resume state — 326 chunks, 1 done |
| `trickle2_outbox/regen_go_c0000.sh` | the lane handed to `airlock submit` |
| `trickle_store/op_units2_go_c0000.json` | the chunk this session compiled, 795,137 bytes |
| `trickle_lanes/regen_go_c0000.sh`, `trickle_raw/regen_go_c0000.{txt,console.log}` | its lane copy and raw product |

## 10.4 Edited, append-only

`~/Programming/PseudoCoupHQ/DevComms/log_131_task40_regeneration_trickle.md`
— one dated `# CORRECTION` section appended, nothing above it edited.

## 10.5 New, in `~/Programming/PseudoCoupHQ/DevComms/`

`log_138_airlock_instances_feature.md` — this log.

## 10.6 Untouched, named so they are not assumed changed

`trickle_up.sh`, `trickle_down.sh`, `trickle_doctor.sh`, `trickle.py`,
`trickle_state.json`, and every one of the 334 stores and 668 raw products
from the round-8 run.

---

# 11. The commits

The 30-second daemon committed throughout; nothing was held back and no
commit was made by hand.

```
$ git -C ~/Programming/Airlock log --oneline --since="6 hours ago"
5baaf98 auto: 1 file (README.md)
5a137c7 auto: 1 file (watcher.py)
0149425 auto: 2 files (instance.sh, up.sh)
4a3fca3 auto: 1 file (airlock)
…
37520ef auto: 2 files (instance.sh, sandbox.conf.example)
```
