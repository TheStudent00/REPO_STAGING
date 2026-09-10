# log 145 — three open calls on Airlock, for its owner

2026-09-02. Airlock is `PUBLIC/Airlock`, an application several
projects use through `AIRLOCK_ROOT` and lanes. Three questions about its
shape are open. Nothing here decides anything; each section carries the
real lines so its question is answerable from this page alone.

An **instance**, in Airlock's own words
(`PUBLIC/Airlock/README.md`, Instances section) — LITERAL:

> An **instance** is one running sandbox: its own runner container, its own
> proxy, its own networks, its own agent lane, its own caps. One Airlock
> install runs as many as you ask for, side by side.

Every quoted line below was grepped this session; the commands are in §4.

---

# 1. Call one — the ten names the instances feature introduced

## 1.1 The instance: the ten names, and the line each one lives on

LITERAL — the table as it stands in
`PRIVATE/PseudoCoupHQ/DevComms/log_138_airlock_instances_feature.md`
§7, reproduced row for row, with a fourth column added holding the exact
artifact line grepped this session.

| # | the name I used | what it names | where it would be changed | the artifact line (LITERAL) |
|---|---|---|---|---|
| 1 | `AIRLOCK_INSTANCE` | the environment variable naming which sandbox | `instance.sh` (`airlock_parse_instance`, `airlock_instance_load`) and one `elif` in `airlock`'s `main()` | `instance.sh:128: AL_INSTANCE="${AIRLOCK_INSTANCE:-sandbox}"` and `airlock:246: or os.environ.get("AIRLOCK_INSTANCE")` |
| 2 | `--instance` | the flag spelling of the same | the same two places | `instance.sh:54: AIRLOCK_INSTANCE="$2"` (inside the `--instance` case) and `airlock:1135: command = ["bash", target, "--instance", paths.instance] + list(args)` |
| 3 | **"instance"** as the concept word | one running sandbox | prose only — README's Instances section, and the `AL_INSTANCE` variable name | `instance.sh:128: AL_INSTANCE="${AIRLOCK_INSTANCE:-sandbox}"` |
| 4 | `instances/<name>.conf` | where an instance's settings live | one line in `instance.sh`: `AL_CONF="$AL_ROOT/instances/$AL_INSTANCE.conf"`, plus one `.gitignore` stanza | `instance.sh:137: AL_CONF="$AL_ROOT/instances/$AL_INSTANCE.conf"` |
| 5 | the conf keys — `cpus`, `memory`, `pids_limit`, `tmp_size`, `work_size`, `proxy`, `proxy_memory`, `proxy_cpus`, `proxy_pids_limit`, `allowlist_file`, `mounts_file`, `agent_dir`, `runner_image`, `proxy_image`, `persist_volume`, `persist_mode`, `lane_nice`, `script_timeout`, `watch`, `daemon_file` | each setting | one `_airlock_conf_get "$AL_CONF" <key>` call each, all in one block of `instance.sh` | `instance.sh:176: AL_CPUS="$(_airlock_pick "$AL_CPUS" "$(_airlock_conf_get "$AL_CONF" cpus)")"` — one such line per key |
| 6 | `<instance>-runner`, `<instance>-proxy`, `<instance>-internal`, `<instance>-egress` | the derived container and network names | five lines in `airlock_instance_load` | `instance.sh:140-143:` `AL_RUNNER="$AL_INSTANCE-runner"` / `AL_PROXY="$AL_INSTANCE-proxy"` / `AL_NET_INTERNAL="$AL_INSTANCE-internal"` / `AL_NET_EGRESS="$AL_INSTANCE-egress"` |
| 7 | `AL_*` | the variable prefix the scripts read | `instance.sh` and the scripts that use them | the same four lines, `instance.sh:140-143` — every exported name begins `AL_` |
| 8 | `instances/<name>/agent` | a non-default instance's lane | one `default_agent` branch in `instance.sh` | `instance.sh:154: default_agent="$AL_ROOT/instances/$AL_INSTANCE/agent"` |
| 9 | `watch = poll` / `auto` | the polling doorbell | `daemon/watcher.py`'s `open_watcher`, plus the `watch` key | `daemon/watcher.py:91: WATCH_MODE = os.environ.get("AIRLOCK_WATCH", "inotify").strip().lower()` and `instance.sh:224: AL_WATCH="$(_airlock_pick "$(_airlock_conf_get "$AL_CONF" watch)" "inotify")"` |
| 10 | `daemon_file` | binding a host daemon over the image's | `instance.sh` and one block in `up.sh` | `instance.sh:219: AL_DAEMON_FILE="$(_airlock_conf_get "$AL_CONF" daemon_file)"` and `up.sh:175: DAEMON_ARGS=(-v "$AL_DAEMON_FILE:/opt/daemon/watcher.py:ro")` |

## 1.2 The mechanism

- Every one of the ten was picked by the implementer so the feature could
  be built and proved. Naming is the owner's ruling, not the
  implementer's.
- Each name is written in exactly one place, so a rename is a one-line
  edit — that is what the fourth column above shows.
- Two rows carry more than spelling. Row 8 is call three of this page (a
  location, not a word). Row 10 is a bridge the README already documents
  as temporary — `PUBLIC/Airlock/README.md`, Configuration table,
  LITERAL: "It exists because the daemon is part of the image: a change
  to `daemon/watcher.py` otherwise needs a full rebuild before any
  instance can use it. Drop the key after the next `build.sh`."

## 1.3 The question

Keep, rename, or drop each of the ten names above — a keep on all ten is
a complete answer.

---

# 2. Call two — may one instance run several lanes at once?

## 2.1 The instance: the daemon says serial, in its own words

LITERAL — `PUBLIC/Airlock/daemon/watcher.py`, lines 30-32:

```
EXECUTION IS SERIAL. run_script() is called synchronously from the single
event loop, so two scripts dropped at once run one after the other. This is
deliberate: concurrent heavy runs are what exhaust scratch space.
```

GLOSS of those three lines: one loop reads the drop folder and calls the
runner function directly, so the next lane cannot begin until the current
one returns; the stated reason is the scratch filesystems, which are
fixed-size tmpfs (`work_size = 4g`, `tmp_size = 2g` in
`PUBLIC/Airlock/instances/sandbox.conf.example`).

## 2.2 What a caller gives up, in values in motion

LITERAL — `PRIVATE/PseudoCoupHQ/Research/op_pipeline/trickle2.py`,
lines 51-52 and 333:

```
scratch space" (daemon/watcher.py). So this program submits one chunk at a
time and waits.
...
print("%d chunk(s) to run, one at a time (Airlock runs lanes serially)"
```

The walk, with the real numbers from that program's state file
(`trickle2_state.json`, 326 chunks remaining, 1 done):

- Chunk 1 is rendered to a lane and handed over with
  `airlock --instance trickle submit regen_go_c0000.sh --no-batch`
  (trickle2.py:182 builds exactly that argument list).
- The program then polls the status file until it reads `state=done`.
- Only then is chunk 2 submitted. 326 chunks therefore cost 326 waits in
  a row.
- The earlier fork ran six chunks at once by calling `podman exec`
  directly — going around the daemon, which is the move that created the
  fork in the first place. `trickle2.py` gives that up rather than
  repeat it.
- What is NOT given up: the cap. One lane may use all six cores
  (`cpus = 6`). The loss is overlap between lanes, not throughput inside
  one lane.

## 2.3 The two shapes, side by side

| shape A — serial, as built | shape B — a `workers` key |
|---|---|
| `run_script()` called synchronously from the one event loop (`daemon/watcher.py:30`) | an instance's conf gains `workers = N`, default `1`; the loop starts up to N lanes before waiting |
| scratch space can only be consumed by one lane at a time — the stated reason for the design | N lanes share the one 4g `/work` and 2g `/tmp` tmpfs; the failure mode the comment names becomes reachable |
| a 326-chunk batch is 326 sequential waits | the same batch overlaps N-wide |
| every caller of Airlock, today, behaves this way | the change lands on every caller of Airlock, not only the one asking |

The key does not exist: `grep -rn "workers"` over every `.sh`, `.py` and
the `airlock` CLI in `PUBLIC/Airlock` returns nothing (§4).

## 2.4 The question

Should an instance be allowed to run N lanes at once through a `workers`
key defaulting to 1, accepting the scratch-space exhaustion its own
daemon comment names — or does serial stay the rule for every caller?

---

# 3. Call three — where an instance's run records live by default

## 3.1 The instance: the derivation, and the ignore stanza

LITERAL — `PUBLIC/Airlock/instance.sh`, lines 146-156:

```
    # --- the agent lane -------------------------------------------------
    # The default instance keeps `<root>/agent`, unchanged. Any other
    # instance gets its own tree so two instances never share a drop
    # folder — one derivation rule, not a per-name special case.
    local default_agent
    if [ "$AL_INSTANCE" = "sandbox" ]; then
        default_agent="$AL_ROOT/agent"
    else
        default_agent="$AL_ROOT/instances/$AL_INSTANCE/agent"
    fi
    AL_AGENT_DIR="$(_airlock_pick "$(_airlock_conf_get "$AL_CONF" agent_dir)" "$default_agent")"
```

GLOSS: the last line is the whole of the choice. `_airlock_conf_get`
reads the `agent_dir` key out of the instance's conf; `_airlock_pick`
takes that value if it is non-empty and the derived default otherwise.
So the conf key already accepts any path; the default is what is being
asked about.

LITERAL — `PUBLIC/Airlock/.gitignore`, lines 28-34:

```
# Which INSTANCES this install runs, and each one's caps. Same pattern as
# mounts.conf: instances/sandbox.conf.example is committed and is the
# documentation, the real .conf files never are. An instance's own agent
# tree lives under instances/<name>/ and is a run record, not a tool file.
instances/*.conf
!instances/*.conf.example
instances/*/
```

LITERAL — `PUBLIC/Airlock/instances/sandbox.conf.example`, the
`agent_dir` block as shipped (commented out, so the derivation applies):

```
# ---- what this instance can see -----------------------------------------
mounts_file     = mounts.conf
# agent_dir     = <root>/agent for the `sandbox` instance,
#                 <root>/instances/<name>/agent for any other
```

## 3.2 The two shapes, side by side

| shape A — inside the checkout (as built) | shape B — outside the checkout |
|---|---|
| an instance named `trickle` gets `PUBLIC/Airlock/instances/trickle/agent/{drop,status,logs,out}` | the earlier fork put its tree at `AirlockTrickle/agent`, deliberately |
| kept out of git by the stanza `instances/*/` quoted above | outside the repo entirely, so no ignore rule is load-bearing |
| `airlock doctor` finds every instance by listing `instances/`, so one directory answers "what else runs here" | a second place to look; `doctor`'s listing no longer sees the tree |
| the reason the fork avoided it: the 30-second commit daemon (`~/Programming` repos, all 16) walks the checkout; run records sit next to source, protected only by the ignore rule | run records never sit beside source at all |
| no per-machine path in the conf | a real absolute path goes into `instances/<name>.conf` — that file is already gitignored and per-machine, like `mounts.conf` |

## 3.3 The question

Should the default home for a non-default instance's drop/status/logs/out
tree stay inside the checkout at `instances/<name>/agent` (gitignored), or
become a path outside it — given the `agent_dir` key already allows either
and only the default is in question?

---

# 4. Verification — every quoted line, grepped this session

```
$ cd PUBLIC/Airlock

$ grep -n -i "serial\|concurrent\|scratch" daemon/watcher.py
27:    a run that exhausts scratch space is otherwise diagnosed only by its
30:EXECUTION IS SERIAL. run_script() is called synchronously from the single
32:deliberate: concurrent heavy runs are what exhaust scratch space.

$ grep -n "instances" .gitignore
32:instances/*.conf
33:!instances/*.conf.example
34:instances/*/

$ grep -n "agent_dir\|default_agent" instance.sh
150:    local default_agent
152:        default_agent="$AL_ROOT/agent"
154:        default_agent="$AL_ROOT/instances/$AL_INSTANCE/agent"
156:    AL_AGENT_DIR="$(_airlock_pick "$(_airlock_conf_get "$AL_CONF" agent_dir)" "$default_agent")"

$ grep -n 'AL_INSTANCE=\|AL_CONF=\|AL_RUNNER=\|AL_PROXY=\|AL_NET_' instance.sh
128:    AL_INSTANCE="${AIRLOCK_INSTANCE:-sandbox}"
137:    AL_CONF="$AL_ROOT/instances/$AL_INSTANCE.conf"
140:    AL_RUNNER="$AL_INSTANCE-runner"
141:    AL_PROXY="$AL_INSTANCE-proxy"
142:    AL_NET_INTERNAL="$AL_INSTANCE-internal"
143:    AL_NET_EGRESS="$AL_INSTANCE-egress"

$ grep -n 'AL_DAEMON_FILE=\|AL_WATCH=' instance.sh
219:    AL_DAEMON_FILE="$(_airlock_conf_get "$AL_CONF" daemon_file)"
224:    AL_WATCH="$(_airlock_pick "$(_airlock_conf_get "$AL_CONF" watch)" "inotify")"

$ grep -n 'WATCH_MODE' daemon/watcher.py
91:WATCH_MODE = os.environ.get("AIRLOCK_WATCH", "inotify").strip().lower()

$ grep -n 'AL_DAEMON_FILE' up.sh
175:    DAEMON_ARGS=(-v "$AL_DAEMON_FILE:/opt/daemon/watcher.py:ro")

$ grep -rn "workers" --include=*.sh --include=*.py --include=airlock .
(no output)

$ grep -n "one at a time\|serially" PRIVATE/PseudoCoupHQ/Research/op_pipeline/trickle2.py
52:time and waits.
333:    print("%d chunk(s) to run, one at a time (Airlock runs lanes serially)"
```

Sources: `PRIVATE/PseudoCoupHQ/DevComms/log_138_airlock_instances_feature.md`
§6.4.1, §7, §8;
`PRIVATE/PseudoCoupHQ/DevComms/log_140_open_calls_explained.md` §5-§7;
`PUBLIC/Airlock/README.md` Instances and Configuration sections;
`PUBLIC/Airlock/instances/sandbox.conf.example`.

No recommendation is made on any of the three; no fact on this page forces
one.
