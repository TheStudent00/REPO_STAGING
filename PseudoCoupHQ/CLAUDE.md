# PseudoCoupHQ — settled facts, load before working

Written 2026-08-21. This file exists so the things the owner has already
ruled are never re-litigated in a later session. If something here
looks wrong, ASK — do not quietly change it.

## vocabulary, absolute

- Never parent / child / children / sibling / ancestor / descendant /
  orphan. Use super-node / sub-node / co-node / sub-tree, higher /
  lower for levels, derive / extend for inheritance in our own
  designs, unlinked / detached for a node with nothing above it.
- Never death / kill / died / dead for a process, probe or run. The
  outcome where the operating system stops a process with no
  language-level error is **ABORT**. Third-party spellings
  (`SIGKILL`, `kill -9`, a `death:` token already written into a data
  file) stay in backticks as theirs.
- Botanical terms are fine: root, leaf, branch, tree, pruning.

## the fuzz-clustering line — what the objects ARE

Read `Planning/node_0_3_research/node_0_3_0_2_kind_fuzz_clustering/SUPPORT_conversion_spec.md`
for the full settled spec. The short form:

- **holder** — the typed slot a value sits in before an operation is
  applied. `rust i64`, `ruby BigDecimal`, `python ctypes.c_int64`.
  One census camp can own several holders.
- **form** — the census-level kind above the holder: nothing, truth,
  whole, fractional, text, sequence, keyed, nesting.
- **X set (the interval sample)** — the list of values probed for one
  form. Whole carries 17 spellings (−2^63 … 2^64−1), fractional 16,
  truth 6 (`true, false, 0, 1, "", nil`). **A ROW CARRIES ITS
  INTERVAL**: the row's `x_set` IS the sampled interval, and the row
  holds one output per input pair drawn from it.
- **row** — one (operator, lhs holder, rhs holder) at one level. Its
  outputs cover every ordered pair from its x_set.
- **key** — one input pair, `(lhs_canon, rhs_canon)` at level 1,
  `(x0,x1,x2,x3)` at level 2. Comparison between two rows happens key
  by key over the INTERSECTION of their keys.

## canonical form — settled after several corrections

`[sign, mant, expo]`, sign in {−1, 1}, **mant a DECIMAL string in
[1,2)** with 31 fractional digits, expo an integer. Zero is
`[1, 0.0, 0]` / `[-1, 0.0, 0]` — the word negzero is retired, the sign
carries it. Infinities `[1, inf]` / `[-1, inf]`. `nan` is the only
special word kept.

- **Never show fractions or rationals in a visible column.** Exact
  rationals live in a sidecar file. Integer mantissas were rejected
  (the decomposition is not unique). No `~` markers, no arrows, no
  annotations inside cells.
- Bytes columns hold the bytes as the language holds them; fixed-width
  holders keep their leading zeros, unbounded holders are minimal.
- Text canon `t|<NFC utf-8 hex>|byte_len|codepoint_len|grapheme_len`.
  Container canon `c|<sorted member canons>|key_format|order_flag`.
- Outcome tokens `REFUSE`, `RAISE:<kind>`, `ABORT` ride in the same
  column as values, from a universal vocabulary, never language
  message text.

## probe design — settled 2026-08-21, RUN in log 052

- **Level 1**: `y = op(x0, x1)` for ALL ordered pairs from X.
- **Level 2**: `z = op(op(x0,x1), op(x2,x3))`, all four operands from
  X (a subset X' when |X|^4 is too costly). The intermediates are
  never enumerated, deduped, capped or unioned — they live inside the
  expression, so both languages evaluate identical expressions on
  identical inputs and rows compare with no alignment step.
- X must carry **one point on each side of every critical point**
  where both exist (p−1, p, p+1; p−1ulp, p, p+1ulp), plus ordinary
  values so normal-condition behaviour is measured, not only edges.
- REJECTED, do not resurrect: the geometric ladder (`2^(k*63/14)`
  magnitudes) — it was never an interval sweep; constant-offset
  shifted pairing — `y − x` constant makes every difference-only
  operator answer a constant vector; composition with equal operands
  `op(op(x,x), op(x,x))` — degenerate for operators idempotent on
  equal operands.

## scoring and clustering

- Only `lhs_canon`, `rhs_canon`, `output_canon` are scored. Holder
  names, byte spellings, value-class names and probe ids are carried
  for reading, never scored.
- **Declines are never scored.** A key where either side answers
  REFUSE / RAISE:* / ABORT is dropped from numerator AND denominator.
  Zero comparable keys means NO connector, not a zero-weight one.
- Two weights ride on every connector: **exact-match rate** (are these
  the same operator) and **graded per-element similarity** (how
  related are they — sign distance, mant distance, expo decay). The
  explorer switches; neither is chosen for the owner.
- **Alignment is by shared key**, never by identical whole vectors.
  Holders represent different subsets of X, and the earlier
  identical-vector rule threw away 172,187 real comparisons.
- **CONTRACT (case 1)**: rows with the SAME key set and byte-identical
  outputs are one node. Plain identity, transitive, no clique test.
- **GROUP (case 2)**: nodes agreeing 1.0 over a PARTIAL overlap are
  drawn inside a hull, not contracted — every pair must be mutually
  1.0 (a maximal clique, never a connected component; chaining through
  never-compared pairs is the hazard, measured at 7,212 triples).
- **the owner's edge criterion**: input-overlap percentage must be >= the
  output-agreement percentage. A 1.0 resting on 4 shared keys out of
  321 fails it — that is how `*` and `&` got grouped (they are
  identical on {0,1}, the only ground a whole row and a truth row
  share).

## explorer requirements, already fixed — preserve them

- Autofit runs ONCE and never again; any wheel or mousedown disables
  it permanently; a "fit view" button exists.
- Internal connector springs near zero — they tether a row to its
  operator node visually and must never dominate the layout.
- Threshold slider cuts EXTERNAL connectors only; components are
  counted on external connectors only.
- Self-contained single file, data embedded, no CDN.

## how the owner wants to be worked with

- Show the object, do not describe it. Quote the file, paste the rows,
  render a markdown table (raw text blocks wrap and become unreadable;
  markdown tables scroll).
- Two-list rule in every agent report: "decided, recorded for audit"
  strictly separate from "awaiting the owner", the second kept minimal.
- Substantial output goes in a DevComms log; the chat carries the
  conclusion and points at the log.
- Ask before deciding anything structural — architecture, ontology,
  naming. Decide mechanical details without asking.

## the sandbox — Airlock, since 2026-08-22

The sandbox is `Airlock`. It was derived from
`SandboxDesign` on 2026-08-22 and this line now uses it.
`SandboxDesign` is not retired and still works, but the
two share container names and **must not run at the same time** — see
`Airlock/MIGRATING.md`. The migration is recorded in
`PseudoCoupHQ/DevComms/log_060_sandbox_to_airlock_migration.md`.

- **The CLI is the way in.** Submit a lane with
  `python3 Airlock/airlock submit <lane.sh> --batch <label> --weight <n>`.
  It validates the lane before it becomes a run and refuses by name
  rather than queueing something that fails twenty minutes later. A
  batch decision is **mandatory** — `--batch <label>` or `--no-batch`,
  no default — so no lane is ever queued without a denominator.
- The file protocol underneath is unchanged and is still the truth:
  lanes land in `Airlock/agent/drop`, run serially by the
  watcher, logs in `agent/logs`, statuses in `agent/status`, products in
  `agent/out`. A direct file write into `agent/drop` still works and
  nothing is required to go through the CLI.
- Progress across ALL runs: `python3 Airlock/airlock status`
  (or `airlock watch` to refresh). It shows the batch summary, the
  queue, the running lane with its latest progress line, and the most
  recent finished. `bash Airlock/progress.sh` still exists
  and still works — it is carried across unchanged, `-w` still
  refreshes, and it is the only view that lists live processes inside
  `sandbox-runner`. Every CLI view ends by pointing at it.
- `python3 Airlock/airlock doctor` reports podman and
  container state, granted cores versus the configured cap, clutter in
  `agent/drop`, toolchains, the allowlist and free space — each finding
  with a severity and a one-line remedy.
- **Lane scripts are kept in the repo** (the owner, 2026-09-07): every lane
  script is written under the task's artifact folder as
  `lanes_<task>/<lane>.sh` and submitted from there; Airlock's `.done/`
  archive is not the record. Never delete under `Airlock/`
  or `<runs>/`.
- "work free" in a lane footer is DISK SPACE in the work directory, not
  a worker state.
- A lane the operating system stops on the wall-clock ceiling is
  rendered **ABORT** by `airlock status`. The daemon's own raw token in
  the status file is untouched and is named alongside it.
- Probes are batched per file — rust ~1,500 per chunk, ruby one
  process. Compute is seconds to minutes; the long waits in a session
  are agent engineering, not probe throughput.
- **Not yet migrated, deliberately:** the probe generators and readers
  under `PseudoCoupHQ/Research/kind_fuzz_clustering/` and
  `Research/data_representation/` still resolve
  `SandboxDesign/agent/...`, because the 480 products of
  the runs of record live in that tree and Airlock's `agent/out` starts
  empty. Repointing them is the owner's call; the inventory is in log 060.

- **Running on the tower guest instead of the laptop?** Read
  `DevComms/note_server_session_start_here.md` first: it carries the
  bring-up steps, the standing rules, and the queue. The same file sits at
  the root of the Airlock bundle as `START_HERE_CLAUDE.md`.
