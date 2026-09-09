# agent/ — the unattended lane

Four host-bound directories that let a Cowork/Claude session run commands in
the sandbox **without a shell of its own**. A session can write files under
`<WORKSPACE_DIR>` but cannot run podman; these binds turn a file write into a
sandbox run.

| directory | mounts at | direction | who writes |
|---|---|---|---|
| `drop/` | `/drop` | in | the session writes `x.sh` here |
| `status/` | `/status` | out | daemon writes `x.sh.status` |
| `logs/` | `/logs` | out | daemon writes `<stamp>__x.sh.log` |
| `out/` | `/out` | out | the script writes its products here |

## The loop

1. The session writes `agent/drop/run_thing.sh`. A direct write is safe —
   the daemon watches `close_write` as well as `moved_to`, so it fires when
   the writer closes the file, never mid-write. (`submit.sh` still uses the
   hidden-then-rename path because `podman cp` needs it.)
2. The daemon runs it, `cwd=/work`, serially — `run_script()` is called
   synchronously from the single event loop, so two scripts dropped together
   run one after the other. Concurrent heavy runs are what exhaust scratch.
3. The session polls `agent/status/run_thing.sh.status`, a path derivable
   from the script name alone (the log's name embeds a run timestamp and so
   cannot be predicted). Key=value lines, written atomically:

   `state=running` on start, then `state=done`, `exit=<rc>`, `elapsed_s`,
   `log=<path>`, `work_consumed_mb`.
4. Products in `agent/out/` are read by the session and placed into the real
   tree by the session — which is why the project mounts can stay read-only.

## What a dropped script can see

- `PseudoCoup_v6` and `PseudoCoup_v5` — **read-only**.
  Test against the real tree with no copy step; you cannot alter the
  originals. Write products to `/out`.
- `/work` — scratch, tmpfs, **capped at 4 GB**. Exceeding it fails loudly
  with ENOSPC in the container rather than filling the host disk. Wiped on
  restart. Note this is also where `submit_project.sh` copies a project, so
  a multi-gigabyte copy-in now fails at the cap — for PseudoCoup_v6 and _v5
  use the read-only `/projects` mounts instead, which need no copy.
- `/persist` — a named volume that survives restarts. Opt-in, for iterating
  on something expensive across runs. Deliberately not the default:
  persistence carries corruption forward, which copy-per-run cannot.
- The network only through the allowlist proxy (`../allow.sh denied` names
  anything refused).

## Templates

`templates/pcv6_suite.sh` runs the full PseudoCoup_v6 tool suite against the
read-only mounts. To use it, the session copies its text into
`agent/drop/<name>.sh`. Copy rather than symlink — the daemon archives what
it runs into `drop/.done/`.
