# log 155 — Task 55: Airlock, ruling 6 implemented and verified end to end

Date: 2026-09-02. Repository worked on: `PUBLIC/Airlock`, as a
DEVELOPER of Airlock (the standing rule that a project never modifies
Airlock is about callers; the owner ruled these changes into the tool itself).

Ruling 6 verbatim, from log 151's ruling list — the owner: "keep. idc as long as
it works for you … go with your lean": keep all ten names from log 138;
serial execution stays, no `workers` key; `down` refuses while any lane's
status is `running` unless `--force`; the default agent tree for a
non-default instance is `<runs>/<name>/agent` (outside the checkout);
`daemon_file` dropped after the next `build.sh`.

Every rendering below is labelled LITERAL (the object as it is on disk or as
a command printed it) or GLOSS (a plain-words reading sitting next to its
literal), per protocol §5.1a.

---

# 1. The result, at the top level

| # | ruled item | state | where it is proved |
|---|---|---|---|
| 1 | the ten names of log 138 §7 are kept | done — not one was renamed | §2.1 |
| 2 | serial execution stays; no `workers` key | done — nothing was added; the daemon is untouched | §2.2 |
| 3 | `down` refuses while a lane is `running`; `--force` overrides | done | §3, §6.3, §6.4 |
| 4 | a non-default instance's agent tree defaults to `<runs>/<name>/agent` | done | §4, §6.1 |
| 5 | `airlock doctor` lists `<runs>/*` as well as `instances/` | done | §4.3, §6.5 |
| 6 | `daemon_file` dropped after the next `build.sh` | done — the build ran first, then the key and both of its blocks were removed | §5 |
| 7 | README paragraph on serial execution / one instance per task / a trickle jamming only its own instance | done | §4.4 |
| 8 | the running `sandbox` instance and the `trickle` instance's stores are not touched | done — proved by a before/after pair | §7 |
| 9 | no personal or machine-specific path in any tracked file | done — `scrub_check.sh` PASS | §8 |

Six tracked files changed. Nothing was created inside Airlock except one
DevComms log; nothing was deleted anywhere.

# 2. What was deliberately NOT changed

## 2.1 The ten names

Log 138 §7's table lists ten renameable names —`AIRLOCK_INSTANCE`,
`--instance`, the concept word "instance", `instances/<name>.conf`, the conf
keys, `<instance>-runner`/`-proxy`/`-internal`/`-egress`, the `AL_*` prefix,
the non-default agent lane, `watch = poll`/`auto`, and `daemon_file`. the owner
ruled: keep them. Nine are untouched. The tenth, `daemon_file`, is not a
rename but a deletion the same ruling ordered (§5).

## 2.2 Serial execution

GLOSS: no `workers` key was added, and `daemon/watcher.py` was not edited at
all in this task. The daemon's own words on the matter are unchanged.

LITERAL — `PUBLIC/Airlock/daemon/watcher.py`, module docstring:

```
EXECUTION IS SERIAL. run_script() is called synchronously from the single
event loop, so two scripts dropped at once run one after the other. This is
deliberate: concurrent heavy runs are what exhaust scratch space.
```

# 3. (a) `down` refuses while a lane is running

## 3.1 The mechanism

GLOSS: the daemon writes `state=running` into
`<agent>/status/<lane>.status` when a lane starts, and rewrites the same
file with `state=done` when it ends. So one scan of that one folder answers
"is this instance busy" without asking podman anything, and it answers it
per instance — which is the same reason one instance per task is the rule
(§4.4).

LITERAL — the new block in `PUBLIC/Airlock/down.sh`:

```bash
RUNNING_LANES=()
STATUS_DIR="$AL_AGENT_DIR/status"
if [ -d "$STATUS_DIR" ]; then
    for f in "$STATUS_DIR"/*.status; do
        [ -e "$f" ] || continue
        if grep -qx 'state=running' "$f"; then
            base="$(basename "$f")"
            RUNNING_LANES+=("${base%.status}")
        fi
    done
fi

if [ ${#RUNNING_LANES[@]} -gt 0 ] && [ "$FORCE" -eq 0 ]; then
    echo "  REFUSING to take '$AL_INSTANCE' down: a lane is running." >&2
    ...
    exit 1
fi
```

## 3.2 Values in motion — one status file becoming a refusal

The verification run of §6, step by step with the real values:

1. The lane `r11_sixty.sh` is dropped into
   `<runs>/r11check/agent/drop/`. The daemon starts it and writes one
   file.
2. LITERAL — `<runs>/r11check/agent/status/r11_sixty.sh.status`,
   6 seconds into the run:

   ```
   script=r11_sixty.sh
   state=running
   started=2026-09-03T03:20:04+00:00
   log=/logs/20260903T032004Z__r11_sixty.sh.log
   work_free_mb_before=4096
   ```
3. `down.sh` globs that folder, finds one `*.status`, and `grep -qx
   'state=running'` matches line 2 of it. `RUNNING_LANES` becomes
   `("r11_sixty.sh")` — the file's basename with `.status` stripped, which
   is exactly the lane name the submitter used.
4. `FORCE` is 0, so the refusal prints that name and `exit 1` runs before
   any `podman rm`. The container is still up afterwards (§6.3).
5. With `--force`, `FORCE` is 1, the same list is printed as a warning
   instead, and the removal proceeds (§6.4).

## 3.3 The refusal text, verbatim

LITERAL — the whole of what `airlock --instance r11check down` printed:

```
running: bash PUBLIC/Airlock/down.sh --instance r11check
(this CLI delegates so container flags have one source of truth: PUBLIC/Airlock/down.sh)

=== airlock down ===
  instance: r11check   runner: r11check-runner   agent: <runs>/r11check/agent
  REFUSING to take 'r11check' down: a lane is running.
    running lane:  r11_sixty.sh
      status file: <runs>/r11check/agent/status/r11_sixty.sh.status
    Removing the runner now stops that lane mid-flight, and the
    submitter sees no error — only a run that stopped.
    Wait for it, or override deliberately:
      bash PUBLIC/Airlock/down.sh --instance r11check --force
```

GLOSS: the second and third lines of the refusal are the lane's name and the
file the verdict was read from, so the operator can check the claim rather
than take it. The fourth and fifth lines are the incident of log 143 §7.4
stated as a consequence.

## 3.4 `airlock down` routes through the same check, by construction

GLOSS: the CLI does not reimplement `down`; it runs the shell script. So the
refusal is written once and both front doors have it. The transcript above
is the CLI's, and its first line is the command it ran.

LITERAL — `PUBLIC/Airlock/airlock`, `delegate()`:

```python
    command = ["bash", target, "--instance", paths.instance] + list(args)
```

## 3.5 The other paths through the new flag parsing

- `--networks` still works and is no longer positional: it was read as
  `"${1:-}"` before, so `./down.sh --networks --force` would have missed it.
  Both flags are now parsed in a loop.
- An unrecognised flag is refused with exit 2 (§6.6), where before it was
  silently ignored.
- An instance with no status folder at all takes the empty-list path and
  proceeds (§6.6).

# 4. (b) The run tree moves outside the checkout

## 4.1 The derivation

LITERAL — the changed lines of `PUBLIC/Airlock/instance.sh`
(`git diff`, the hunk at line 147):

```
     local default_agent
     if [ "$AL_INSTANCE" = "sandbox" ]; then
         default_agent="$AL_ROOT/agent"
     else
-        default_agent="$AL_ROOT/instances/$AL_INSTANCE/agent"
+        default_agent="$HOME/AirlockRuns/$AL_INSTANCE/agent"
     fi
```

GLOSS: `$HOME` is expanded at run time by the shell, so no machine's path is
written into the file. The `sandbox` branch is untouched, which is what
keeps every existing caller of the default instance working unchanged.

LITERAL — the three derivations, asked of `instance.sh` itself
(`$HOME` rewritten as `~` in the output):

```
$ bash -c 'source ./instance.sh; airlock_instance_load; echo "$AL_AGENT_DIR"'
PUBLIC/Airlock/agent
$ bash -c 'source ./instance.sh; AIRLOCK_INSTANCE=r11check airlock_instance_load; echo "$AL_AGENT_DIR"'
<runs>/r11check/agent
$ bash -c 'source ./instance.sh; AIRLOCK_INSTANCE=trickle airlock_instance_load; echo "$AL_AGENT_DIR"'
PUBLIC/Airlock/instances/trickle/agent
```

GLOSS: the third line is the legacy case of §4.2, pinned on purpose.

## 4.2 The existing `instances/trickle/agent` tree: documented as legacy, nothing moved

The brief allowed migration or documentation. **Documented, not migrated** —
the tree holds eight finished runs' products, and moving files is a way to
lose them for no gain.

The instance names its own tree in its own conf file, which is per-machine
and gitignored (so no real path enters a tracked file, and the value used is
repo-relative in any case).

LITERAL — the block added to `PUBLIC/Airlock/instances/trickle.conf`:

```
# LEGACY TREE, kept in place (2026-09-02). The default home for a
# non-default instance's agent tree moved OUTSIDE the checkout, to
# <runs>/<name>/agent. This instance's existing drop/status/logs/out
# tree — with its finished runs' products in it — stays exactly where it is
# and is named explicitly here. Nothing was moved and nothing was deleted.
# Delete this key to adopt the new default; the old tree is then simply
# unread, still on disk at instances/trickle/agent.
agent_dir         = instances/trickle/agent
```

The `instances/*/` ignore stanza is kept for these trees, and its comment
now says so.

LITERAL — `PUBLIC/Airlock/.gitignore`, the changed comment:

```
# tree is a run record, not a tool file, and since 2026-09-02 it lives
# OUTSIDE the checkout at <runs>/<name>/agent. The instances/*/ rule
# below stays for trees created under the older default, which were left in
# place rather than moved.
```

## 4.3 `airlock doctor` lists both places

GLOSS: an instance leaves two traces and either can exist without the other.
`instances/<name>.conf` is its SETTINGS; `<runs>/<name>` is its RUN
TREE. An instance started with no conf file at all is legal — every key has
a default — and such an instance appears only under `AirlockRuns`, so
listing `instances/` alone would miss it. Each row now says which of the two
it was found in.

LITERAL — the new listing code in `PUBLIC/Airlock/airlock`:

```python
        runs = runs_home()
        if os.path.isdir(runs):
            for entry in sorted(os.listdir(runs)):
                if os.path.isdir(os.path.join(runs, entry)):
                    note(entry, "runs")
```

Two helpers were added beside it: `runs_home()`, which is the CLI's one
spelling of `~/AirlockRuns`, and `tilde()`, which rewrites a home path as
`~` for anything the CLI prints. The `Paths` fallback for a non-default
instance's agent tree was moved to `runs_home()` too, so the CLI and
`instance.sh` cannot disagree even when the CLI cannot read the shell
library.

## 4.4 (d) The README paragraph

Two sections were added to the README's Instances section. The second is the
ruled paragraph.

LITERAL — `PUBLIC/Airlock/README.md`, the new section
"One instance per task, and why a jam stays local":

```
**Execution inside one instance is serial, deliberately.** The daemon runs
one lane to completion before starting the next; concurrent heavy runs are
what exhaust the scratch tmpfs, and there is no `workers` key to change
that. The consequence is that a long lane holds up every lane behind it —
in **that instance**, and only there.

So the unit of separation is the instance: **one task, one instance.** Two
tasks that share an instance queue behind each other and, worse, can stop
each other — on 2026-09-02 one agent took a shared instance down at the end
of its own work while a second agent's lane was mid-run, and the second
agent saw no error, only a run that had stopped. `down.sh` now refuses in
exactly that situation, naming the running lane, and `--force` is the
deliberate override. A slow lane — a trickle — jams its own instance's
queue and nothing else on the machine: another instance has its own runner,
its own drop folder and its own caps, and never waits behind it.
```

The first added section, "An instance's run tree lives outside the
checkout", states the new default, that `up.sh` creates it, that `agent_dir`
overrides it, and that `doctor` lists both places. Three tables were updated
in place: the derived-names table's agent-lane row, the `airlock down`
command row, and the `down.sh` shell-script row.

# 5. (c) The rebuild, then `daemon_file`'s removal

Order matters and was kept: the image was rebuilt FIRST, so the daemon the
key existed to bridge to is in the image before the bridge is removed.

LITERAL — the tail of `bash ./build.sh`:

```
STEP 8/8: CMD ["squid", "-N", "-d", "1", "-f", "/etc/squid/squid.conf"]
COMMIT sandbox-proxy:latest
--> f46c9d74c631
Successfully tagged localhost/sandbox-proxy:latest
f46c9d74c631318d6237f339c3183e5aa8da5755b1b95891999370edd6115123

done. images:
  localhost/sandbox-runner:latest  3.48 GB
  localhost/sandbox-proxy:latest  209 MB

next:  ./up.sh
```

LITERAL — the resulting image ids:

```
$ podman images --format '{{.Repository}}:{{.Tag}}  {{.ID}}  {{.Created}}  {{.Size}}' | grep -E 'sandbox-(runner|proxy)'
localhost/sandbox-proxy:latest  f46c9d74c631  About a minute ago  209 MB
localhost/sandbox-runner:latest  eb3774c9ac56  About a minute ago  3.48 GB
```

LITERAL — the daemon inside the new image carries the polling doorbell the
bridge existed for:

```
$ podman run --rm --network none localhost/sandbox-runner:latest grep -c "AIRLOCK_WATCH" /opt/daemon/watcher.py
5
```

GLOSS: five occurrences of `AIRLOCK_WATCH` inside the image's own
`/opt/daemon/watcher.py` — the image no longer predates the feature, so
nothing needs binding over it.

The key was then removed in three places: the `AL_DAEMON_FILE` read in
`instance.sh` (replaced by a comment recording why it is gone), its name in
that function's `export` line, and the whole `DAEMON_ARGS` block in `up.sh`
together with its `"${DAEMON_ARGS[@]}"` line in the `podman run`.

LITERAL — the `up.sh` block that was deleted:

```bash
# ---- the daemon this instance runs ---------------------------------------
# Unset by default: the daemon baked into the image is what runs, and the
# container spec is exactly what it always was. An instance that names
# `daemon_file` binds that host file read-only over the image's copy, which
# is how a daemon change reaches a running instance without a rebuild.
DAEMON_ARGS=()
if [ -n "${AL_DAEMON_FILE:-}" ]; then
    if [ ! -f "$AL_DAEMON_FILE" ]; then
        echo "  DAEMON ERROR: no such file: $AL_DAEMON_FILE (daemon_file in $AL_CONF)" >&2
        exit 1
    fi
    DAEMON_ARGS=(-v "$AL_DAEMON_FILE:/opt/daemon/watcher.py:ro")
    echo "  daemon:   $AL_DAEMON_FILE (bound over the image's copy)"
fi
```

LITERAL — no reference survives:

```
$ grep -n "DAEMON\|daemon_file" up.sh instance.sh
instance.sh:218:    # There was a `daemon_file` key here until 2026-09-02: it bound a host
```

GLOSS: the single remaining hit is the comment that records the removal.
The README's configuration row and its conf-key list dropped the key too,
and `instances/sandbox.conf.example` records that it is gone. The `trickle`
instance's own conf had the key set; it was removed there and replaced with
a note, since `watch = poll` now works from the image's own daemon.

# 6. (e) The end-to-end verification

Every command and its output, in the order run. `$HOME` is rendered as `~`
throughout.

## 6.0 Which side of the container wall

```
$ echo "host: /projects exists? $( [ -d /projects ] && echo yes || echo no ) ; cwd $(pwd)"
host: /projects exists? no ; cwd PUBLIC/Airlock
$ podman run --rm --network none localhost/sandbox-runner:latest bash -c \
    'echo "container: /drop exists? $( [ -d /drop ] && echo yes || echo no ) ; /out exists? $( [ -d /out ] && echo yes || echo no )"'
container: /drop exists? yes ; /out exists? yes
```

GLOSS: every command in this section ran on the HOST. The host has no
`/projects` and no `/drop`; the container has both. The host side is where
podman, the checkout and `~/AirlockRuns` are.

## 6.1 Bring up `r11check`

The instance is one six-line conf file plus a flag. Nothing was copied.

```
$ cat > instances/r11check.conf <<'EOF'
# `r11check` — a throwaway instance used to verify round 11's Airlock
# ruling end to end. Removed again at the end of that verification.
cpus              = 2
memory            = 2g
proxy             = no
runner_image      = sandbox-runner:latest
watch             = poll
EOF
$ bash ./up.sh --instance r11check
=== airlock up ===
  instance: r11check   runner: r11check-runner   agent: <runs>/r11check/agent
  config:   PUBLIC/Airlock/instances/r11check.conf
r11check-internal
  proxy: none (instance is configured 'proxy = no' — no route out at all)
3625ec3eeb29634185b7968621bd780bd314540b33f1ce3116bf8b6378d71060
  r11check-runner started
    cpus:     2 (--cpus 3 or AIRLOCK_CPUS=3 to throttle a long run)
    memory:   2g   /tmp 2g   /work 4g
    persist:  r11check-persist (rw)
    watch:    poll
    drop:     <runs>/r11check/agent/drop      (write x.sh here to run it)
    status:   <runs>/r11check/agent/status    (x.sh.status — poll this)
    out/logs: <runs>/r11check/agent/{out,logs}
    mounts:   from PUBLIC/Airlock/mounts.conf —
      [five read-only/read-write host mounts, per-machine; elided]

  r11check-runner  Up Less than a second  localhost/sandbox-runner:latest

next:  ./selftest.sh --instance r11check
```

GLOSS: line 2 is the proof of (b) in its intended use — the agent tree is
`<runs>/r11check/agent`, outside the checkout, and `up.sh` created it
(it did not exist beforehand; see §7). `~/AirlockRuns` itself did not exist
before this command. The mount lines are this machine's own `mounts.conf`
and name directories, so they are elided rather than pasted.

## 6.2 Submit a 60-second lane

LITERAL — the lane:

```bash
#!/usr/bin/env bash
# A 60-second lane: it exists only so `down` has something running to refuse.
for i in $(seq 1 60); do
  echo "[$i/60] tick"
  sleep 1
done
echo "done" > /out/r11_sixty.txt
```

```
$ ./airlock --instance r11check submit <scratch>/r11_sixty.sh --batch r11check --weight 60
wrote <runs>/r11check/agent/batch.json
  batch 'r11check' (id batch-20260903T032003Z, created 2026-09-03T03:20:03+00:00): 1 lane(s), total weight 60

dropped <runs>/r11check/agent/drop/r11_sixty.sh
  from:     <scratch>/r11_sixty.sh
  written hidden as <runs>/r11check/agent/drop/.r11_sixty.sh first, then renamed - the daemon never sees a partial file
  poll:     <runs>/r11check/agent/status/r11_sixty.sh.status
  log:      <runs>/r11check/agent/logs/<stamp>__r11_sixty.sh.log
  products: <runs>/r11check/agent/out
```

## 6.3 `down` while it runs — the refusal

```
$ sleep 6; cat <runs>/r11check/agent/status/r11_sixty.sh.status
script=r11_sixty.sh
state=running
started=2026-09-03T03:20:04+00:00
log=/logs/20260903T032004Z__r11_sixty.sh.log
work_free_mb_before=4096

$ ./airlock --instance r11check down
```

The refusal it printed is §3.3, verbatim. Its exit code and its effect:

```
$ ./airlock --instance r11check down > refusal.txt 2>&1; echo "EXIT CODE = $?"
EXIT CODE = 1
$ podman ps --filter name=r11check --format '{{.Names}}  {{.Status}}'
r11check-runner  Up 27 seconds
$ bash ./down.sh --instance r11check >/dev/null 2>&1; echo "down.sh EXIT CODE = $?"
down.sh EXIT CODE = 1
```

GLOSS: the refusal exits 1 through both front doors, and the runner is still
up afterwards — the check runs before any `podman rm`, so a refused `down`
changes nothing.

## 6.4 `--force`

```
$ ./airlock --instance r11check down --force
running: bash PUBLIC/Airlock/down.sh --instance r11check --force
(this CLI delegates so container flags have one source of truth: PUBLIC/Airlock/down.sh)

=== airlock down ===
  instance: r11check   runner: r11check-runner   agent: <runs>/r11check/agent
  --force: taking it down with 1 lane(s) recorded running:
    r11_sixty.sh
time="2026-09-02T23:20:38-04:00" level=warning msg="StopSignal SIGTERM failed to stop container r11check-runner in 10 seconds, resorting to SIGKILL"
  removed r11check-runner
done.

$ podman ps --format '{{.Names}}  {{.Status}}'
va-proxy  Up 8 hours
sandbox-proxy  Up 8 hours
sandbox-runner  Up 8 hours
```

GLOSS: `--force` does not go quiet — it names the lane it is overriding, so
the record says a running lane was stopped on purpose. The podman warning
line is podman's own: the lane was mid-`sleep`, so the container needed the
harder signal. Only `r11check-runner` was removed; the three containers that
were already up are the same three.

## 6.5 `doctor`

```
$ ./airlock doctor
| NOTE | instances | 3 known, from instances/*.conf and <runs>/*: r11check (r11check-runner: absent; conf+runs); sandbox (sandbox-runner: running; built-in+conf) <- this command; trickle (trickle-runner: absent; conf) | airlock --instance <name> <command>, or bash PUBLIC/Airlock/up.sh --instance <name>; a new instance is a new instances/<name>.conf (see instances/sandbox.conf.example), and its run tree is made under ~/AirlockRuns on the first up |
```

(the full run printed 1 WARN, 4 NOTE, 9 OK and exited 0; the row above is
the one this task changed.)

GLOSS, reading the three rows: `r11check` is `conf+runs` — it has both a
conf file and a tree under `~/AirlockRuns`, which is the row that proves the
new listing. `sandbox` is `built-in+conf` and has no `AirlockRuns` tree,
because the default instance's tree is `<root>/agent`. `trickle` is `conf`
only, because its tree is the legacy one inside the checkout (§4.2).

## 6.6 Two edge paths

```
$ bash ./down.sh --instance nosuchinst
=== airlock down ===
  instance: nosuchinst   runner: nosuchinst-runner   agent: <runs>/nosuchinst/agent
done.
EXIT=0

$ bash ./down.sh --instance nosuchinst --bogus
unknown argument: --bogus
usage: ./down.sh [--instance NAME] [--networks] [--force]
EXIT=2
```

GLOSS: an instance with no status folder takes the empty-list path and
proceeds; an unrecognised flag is a usage error rather than silence.

## 6.7 Removing `r11check` — what was removed

```
$ podman network ls --format '{{.Name}}' | grep r11check ; podman volume ls --format '{{.Name}}' | grep r11check
r11check-internal
r11check-persist
$ find ~/AirlockRuns -type f
<runs>/r11check/agent/batch.json
<runs>/r11check/agent/drop/r11_sixty.sh
<runs>/r11check/agent/logs/20260903T032004Z__r11_sixty.sh.log
<runs>/r11check/agent/status/r11_sixty.sh.status

$ podman network rm r11check-internal ; podman volume rm r11check-persist
$ rm -f instances/r11check.conf
$ rm -rf <runs>/r11check
$ rmdir ~/AirlockRuns
```

Five things were removed, all created by this verification and nothing else:
the conf file `instances/r11check.conf`, the run tree
`<runs>/r11check` (four files), the now-empty `~/AirlockRuns`, the
network `r11check-internal`, and the volume `r11check-persist`. The runner
container was already gone (§6.4).

```
$ podman network ls --format '{{.Name}}' | grep -c r11check ; podman volume ls --format '{{.Name}}' | grep -c r11check
0
0
$ ls ~/AirlockRuns
ls: cannot access '~/AirlockRuns': No such file or directory
$ ls instances/
sandbox.conf
sandbox.conf.example
trickle
trickle.conf
```

# 7. The default instance and the `trickle` stores were not touched

LITERAL — before any change was made:

```
$ podman ps --format '{{.Names}}  {{.Status}}  {{.Image}}'
va-proxy  Up 8 hours  localhost/va-proxy:latest
sandbox-proxy  Up 8 hours  localhost/sandbox-proxy:latest
sandbox-runner  Up 8 hours  localhost/sandbox-runner:latest
$ find instances/trickle/agent -type f | wc -l ; du -sb instances/trickle/agent
38
1188427	instances/trickle/agent
$ ls -la ~/AirlockRuns
ls: cannot access '~/AirlockRuns': No such file or directory
```

LITERAL — after everything, including the cleanup:

```
$ podman ps --format '{{.Names}}  {{.Status}}  {{.Image}}'
va-proxy  Up 8 hours  localhost/va-proxy:latest
sandbox-proxy  Up 8 hours  localhost/sandbox-proxy:latest
sandbox-runner  Up 8 hours  localhost/sandbox-runner:latest
$ find instances/trickle/agent -type f | wc -l ; du -sb instances/trickle/agent
38
1188427	instances/trickle/agent
```

GLOSS: same three containers, same uptime bucket, same images. The
`trickle` tree is byte-identical — 38 files, 1,188,427 bytes both times.
`trickle` was never brought up during this task; the only thing written on
its side is its per-machine conf file (§4.2), which pins the tree it already
had so that the changed default cannot orphan it.

One caveat stated rather than hidden: `sandbox-runner` is still running on
the image that existed before §5's rebuild. A rebuild does not restart a
running container, and restarting the default instance was out of scope.
The next `up.sh` on a fresh container picks up `eb3774c9ac56`.

# 8. `scrub_check.sh`

```
$ bash ./scrub_check.sh
=== scrub_check: 7 pattern(s), 52 tracked file(s), 5 untracked-and-unignored file(s) ===
scrub_check: PASS - no personal or machine-identifying pattern found.
EXIT = 0
```

GLOSS: it scans both tracked files and untracked-but-not-ignored ones, which
is the set `git add -A` would publish. The new DevComms log is in the second
set and passed with the rest. No tracked file names a home path: the
derivation uses `$HOME`, expanded at run time.

# 9. Evidence class per claim

| claim | evidence class |
|---|---|
| `down` refuses, names the lane, exits 1, and removes nothing | executed; §3.3 and §6.3 paste the output, the exit code and the still-running container |
| `--force` overrides | executed; §6.4 |
| `airlock down` routes through the same check | executed (§6.3 ran through the CLI) plus the delegating line of source, §3.4 |
| the non-default default agent tree is `<runs>/<name>/agent` | executed; the derivation asked of `instance.sh` (§4.1) and the tree created by a real `up.sh` (§6.1) |
| `sandbox` keeps `<root>/agent` | executed; §4.1 third command |
| `doctor` lists `<runs>/*` | executed; §6.5 |
| the images were rebuilt before the key was removed | executed; §5, with the build tail, the image ids, and the daemon inside the new image |
| no `daemon_file` reference survives | executed; the `grep` in §5 |
| the `trickle` stores are untouched | measured; identical file count and byte count before and after, §7 |
| the running default instance is untouched | observed; identical `podman ps` before and after, §7 |
| nothing personal in a publishable file | executed; `scrub_check.sh` PASS, §8 |
| serial execution is unchanged | observed; the daemon was not edited, and its own docstring is quoted, §2.2 |

# 10. Complete file inventory

## 10.1 Files changed in `PUBLIC/Airlock` (all tracked)

`git diff --stat` from the last commit before this task
(`5baaf98`) to the current head:

```
 .gitignore  |  5 +++-
 README.md   | 44 ++++++++++++++++++++++++++++----
 airlock     | 83 ++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 down.sh     | 74 ++++++++++++++++++++++++++++++++++++++++++++++++++++--
 instance.sh | 30 +++++++++++-----------
 up.sh       | 16 ------------
 6 files changed, 201 insertions(+), 51 deletions(-)
```

| file | what changed |
|---|---|
| `PUBLIC/Airlock/down.sh` | the running-lane refusal, `--force`, loop-based flag parsing, and the header comment recording why |
| `PUBLIC/Airlock/instance.sh` | `default_agent` for a non-default instance; `AL_DAEMON_FILE` removed from the load and the export |
| `PUBLIC/Airlock/up.sh` | the `DAEMON_ARGS` block and its `podman run` line removed |
| `PUBLIC/Airlock/airlock` | `tilde()` and `runs_home()` added; `check_instances` lists `<runs>/*` and says where each instance was found; the `Paths` agent fallback; the `down` help row and docstring |
| `PUBLIC/Airlock/README.md` | two new sections; three table rows updated; the `daemon_file` configuration row and key-list entry removed |
| `PUBLIC/Airlock/.gitignore` | the `instances/*/` stanza's comment now says the rule is for legacy trees |

## 10.2 File created in `PUBLIC/Airlock`

| file | what it is |
|---|---|
| `PUBLIC/Airlock/DevComms/log_003_down_refuses_and_run_trees_move.md` | Airlock's own record of this change set, next in its sequence after `log_002` |

## 10.3 Per-machine files changed (gitignored, never committed)

| file | what changed |
|---|---|
| `PUBLIC/Airlock/instances/sandbox.conf.example` | the `agent_dir` block documents the new derivation; a note records that `daemon_file` is gone (this one IS tracked — it is the committed template) |
| `PUBLIC/Airlock/instances/trickle.conf` | `agent_dir` pins the legacy tree; the `daemon_file` key removed and replaced with a note |

## 10.4 Files created and then removed

| file | why |
|---|---|
| `PUBLIC/Airlock/instances/r11check.conf` | the verification instance; removed in §6.7 |
| `<runs>/r11check/agent/**` (4 files) | that instance's run tree; removed in §6.7 |
| the verification lane, in this session's scratch directory | not in any repository |

## 10.5 Files read, not written

`PUBLIC/Airlock/README.md`, `instance.sh`, `up.sh`, `down.sh`,
`airlock`, `daemon/watcher.py`, `build.sh`, `Containerfile`, `.gitignore`,
`instances/sandbox.conf.example`, `instances/sandbox.conf`,
`instances/trickle.conf`;
`PRIVATE/PseudoCoupHQ/DevComms/log_151_claude_code_task_briefs_round11.md`,
`log_138_airlock_instances_feature.md`,
`log_145_task50c_airlock_calls_for_dee.md`,
`log_143_task50a_swift_emitter_fix.md`;
`PRIVATE/DevComms/LLM_communication_protocol.md`.

## 10.6 This report

`PRIVATE/PseudoCoupHQ/DevComms/log_155_task55_airlock_ruling6.md`.

# 11. Open points

1. **The default instance still runs the pre-rebuild image.** Stated in §7.
   Restarting it is a decision about other work in flight, not this task's.
2. **The `instances/*/` ignore stanza is now legacy-only.** It stays because
   one tree still lives there. It can go when that tree does.
