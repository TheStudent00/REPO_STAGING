# log 194 — task 88: what's in Airlock's agent/out, and what it would cost to lose it

## The number that answers the owner's question

**6.35 GB of the 9.73 GB in `agent/out` exists nowhere else, by content, in
`PseudoCoupHQ`.** Of that 6.35 GB, essentially none of it is irreplaceable:
every byte traces to a lane script that is still preserved (in
`agent/drop/.done` or committed under the project's own
`Research/*/lanes*/`), and the single largest chunk — the layer-3 CARTESIAN
probe corpus (`ct_*` files plus most of `kind_fuzz_clustering`, 6.32 GB, 99.6%
of the total) — is **deterministic**: its probe tables are fixed and embedded
in the lane script itself, not sampled at runtime, so rerunning the lane
reproduces the same bytes, not merely equivalent ones. Losing it costs
**compute time to rerun the lanes, not lost results.**

The one caveat, at 12.46 MB (0.2% of the total): the `sem_anchored_*` family
depends on `pip install pyvex archinfo angr` with no version pin, run from a
lane wrapper that itself is not checked in anywhere (see "A protocol
deviation, flagged separately" below). A rerun today is not guaranteed
byte-identical, though the analysis script it calls (`sem_anchored.py`) is
tracked. This is the only product family where "regenerable" is a
qualified claim rather than a demonstrated one.

**Container volumes** (`sandbox-persist`, `t72-persist`, `t81-persist`,
17.6 GB together): toolchains, source clones, and build caches, plus a
handful of small diary/log files that are themselves lane output. Nothing
in any of the three is primary research data. **If the volumes vanished,
Airlock would need to rebuild toolchains — nothing would be lost that
isn't also reconstructable.** That is the direct answer to "are we leaving
everything in the Airlock — is that unstable?": the *toolchains* are
disposable by design (that's what `/persist` is for); the *research
results* are disposable **only because their generating lane scripts still
exist**, which this audit had to go and check rather than assume.

---

## Method, and where the fence was drawn

Per the brief, hashing 9.7 GB and searching a multi-GB tree run as Airlock
lanes, numbered once each, on the default (`sandbox`) instance:

```
cd ~/Programming/Airlock
./airlock submit ~/Programming/PseudoCoupHQ/Research/airlock_audit/t88_l1_inventory.sh     --no-batch
./airlock submit ~/Programming/PseudoCoupHQ/Research/airlock_audit/t88_l2_hash_out.sh      --no-batch
./airlock submit ~/Programming/PseudoCoupHQ/Research/airlock_audit/t88_l3_rss_sample.sh    --no-batch
./airlock submit ~/Programming/PseudoCoupHQ/Research/airlock_audit/t88_l4_hash_hq_matches.sh --no-batch
```

Lane scripts live at
`~/Programming/PseudoCoupHQ/Research/airlock_audit/t88_l{1,2,3,4}_*.sh` (in
the project's own repo, per Airlock's own README: "no lane scripts" belong
in Airlock itself). All four write only to stdout (captured into
`agent/logs/`) or read-only reads of `/out` and `/projects/PseudoCoupHQ`;
none writes into `/out` or `/projects`.

| lane | did | log | result |
|---|---|---|---|
| `t88_l1_inventory.sh` | recounted `agent/out`: top-level entries, `du -sb`, recursive file count, per-product size/mtime | `20260904T220000Z__t88_l1_inventory.sh.log` | 268 top-level products, 9,734,518,662 bytes (9.73 GB / 9.07 GiB — matches `doctor`'s "9.1 GB"), 6,004 files, 0.2s |
| `t88_l2_hash_out.sh` | sha256 (streaming) every file under `/out` | `20260904T220217Z__t88_l2_hash_out.sh.log` | 6,004 `HASHOUT` rows, 49.9s, `work_consumed_mb=0` |
| `t88_l3_rss_sample.sh` | re-measured peak RSS in-process (see Memory below) | `20260904T220347Z__t88_l3_rss_sample.sh.log` | 20,612 KB peak, cross-checked digest matches lane 2's shell-tool digest for the same (largest, 1.85 GB) file |
| `t88_l4_hash_hq_matches.sh` | for every product name, `find`-matched it under `/projects/PseudoCoupHQ` and sha256-compared file-by-file | `20260904T220401Z__t88_l4_hash_hq_matches.sh.log` | 269 products searched (see drift note), 5,691 file-level `CMP` rows, 14.4s |

Recount commands, run **inside** lane 1, pasted verbatim from its log:

```
$ find /out -mindepth 1 -maxdepth 1 | wc -l
268
$ du -sb /out
9734518662	/out
$ find /out -type f | wc -l
6004
```

Container volumes were inspected directly (`podman volume inspect` +
streaming `du -sh`) rather than as a lane, because they are infrastructure
disk usage on volumes belonging to instances that are not the running
`sandbox` (`t72`, `t81`) — the same class of check `./airlock doctor`
itself does with raw `podman`, not a computation over project data:

```
$ podman volume inspect sandbox-persist t72-persist t81-persist   # -> Mountpoint under
  ~/.local/share/containers/storage/volumes/<name>/_data (host-readable, rootless)
$ du -sh .../sandbox-persist/_data   ->  11G
$ du -sh .../t72-persist/_data       ->  3.6G
$ du -sh .../t81-persist/_data       ->  3.0G
```

**Data-freshness caveat, stated plainly rather than hidden:** lanes 1-2 and
lane 4 are ~4 minutes apart, and other tasks (t86, t87) were actively
dropping lanes into the *same* Airlock instance throughout — `agent/out`
gained `t86_sample.json` and one more file inside `kind_fuzz_clustering`
between lane 1 (22:00:00Z) and lane 4 (22:04:01Z): lane 1 counted 4,972
files there, lane 4 walked 4,973. This is concurrent, unrelated in-flight
work, not an audit error, and it accounts for the ~36 MB gap between the
per-product byte reconciliation and the lane-1 total. It does not change
the headline number's order of magnitude or its regenerable/not
classification.

## Memory bound

sha256sum and Python's `hashlib` both stream in fixed-size chunks — RSS is
flat in file size, not linear in it. Sampled on the actual largest file
under `/out` (**`ct_typescript_l2.txt`, 1.85 GB** — not `kind_fuzz_clustering`,
which is a directory of many small files, not one large one):

```
ru_maxrss before: 18432 KB
ru_maxrss after (streaming sha256 of a 1.85 GB file): 20612 KB
```

20.1 MB peak, 305x under the 6 GB bound. (The brief's suggested
`/usr/bin/time -v` is not installed in the sandbox image — lane 2's first
attempt at this measurement silently returned an empty value, caught and
re-measured properly in lane 3 with `resource.getrusage`, whose digest for
the same file matches lane 2's shell-tool digest exactly — cross-validated,
not just re-run.) No abort was needed; lane 2 then hashed all 6,004 files
in 49.9s with `work_consumed_mb=0`.

## Classification: PLACED / DIVERGED / ABSENT, by content

268 top-level products (excludes `agent/out`'s own `.gitignore`, 141 bytes,
tallied separately as infrastructure, not a research product):

| status | products | notes |
|---|---|---|
| PLACED (whole product byte-identical somewhere in HQ) | 58 | 39.9 MB |
| MIXED (a directory product, partially placed) | 16 | see below |
| DIVERGED (single file, same name, different content) | 10 | 4.14 MB total |
| ABSENT (no trace of the name anywhere in HQ) | 183 | 3.267 GB |

File-level rollup across the 16 MIXED directory products (`op_pipeline`,
`kind_fuzz_clustering`, `jvm_a/b/c`, `canon_units_*`, `sem_anchored_*`,
`verdicts2.json`): 3.38 GB placed, 3.078 GB not (2,486 absent-in-HQ + 4
diverged files, **all but 26 KB of it inside `kind_fuzz_clustering`
alone**; `op_pipeline` itself is 599/614 files placed).

**ABSENT, grouped by family (the standing rule is provenance, not size —
so products are grouped by what produced them, not judged one at a time):**

| family | count | bytes | what it is |
|---|---:|---:|---|
| `ct_*` (cartesian probe results, per-language, some sharded) | 86 | 3.239 GB | layer-3 CARTESIAN probes — deterministic, fixed embedded table |
| `sem_*` (`sem_anchored_*.json`, per language) | 6 | 12.46 MB | semantic-anchoring pass via `sem_anchored.py` (tracked) + `pyvex`/`archinfo`/`angr` (unpinned) |
| `interp_*` (b, b3, c, d, php_b, ruby_b) | 7 | 11.25 MB | interpreter dispatch probe diaries |
| `op_*` (op_asg, op_c, etc.) | 20 | 1.87 MB | operator probe diaries |
| `arch_*`, `ce_*`, `cg_*` (compiler-graph coverage/arch/codegen) | 36 | 0.67 MB | compiler-graph coverage/diary probes |
| `d76_*`, `d78_*` (register-allocation spike investigation) | 9 | 0.26 MB | spike/investigation diaries |
| `cpython_*`, `ruby_*`, `php_nm*` (toolchain build transcripts) | 11 | 0.19 MB | build/configure logs and `nm` symbol dumps of toolchains already built into `sandbox-persist` |
| everything else (`t27`, `asm`, `handlers`, `ordering`, `verdicts3b_pairs.json`, `t86_vcs_scale.json`, `normalizer.log`, `lap5_smoke`) | 8 | 1.85 MB | assorted small diary/probe outputs |

**Every one of these 183 was traced to a producing lane script**, either
archived in `agent/drop/.done` (227 scripts, one per historical run) or
committed under the project's own `Research/*/lanes*/` (734 such scripts
already live in the tree — e.g. the exact `ct_php_l1.sh` that produced
`ct_php_l1.txt` is at
`Research/kind_fuzz_clustering/lanes/ct_php_l1.sh`). Where a name didn't
match a lane 1:1 (a lane can emit several differently-named files —
`pc_dom_ops.sh`, `pc_step8_table.sh`, `pc_core_modes.sh`, `d76_c1b_198.sh`
each produce a handful), the trace was confirmed by grepping the run's own
log for the output name. **Applying the standing rule** ("gate by
provenance — regenerable output vs. something that cannot be regenerated
— not by size"): a product whose generating lane script and inputs are
still present is regenerable output. Every family above qualifies. This
is a factual check (does the script exist, do its inputs exist), not a
judgment call about what the repo *should* carry — so it did not trip the
brief's stop rule.

**`kind_fuzz_clustering` specifically** (the ABSENT dir/file portion above
+ 3.08 GB inside the MIXED accounting, 6.32 GB total, 99.6% of everything
at risk): its lane scripts (`Research/kind_fuzz_clustering/lanes/*.sh`)
embed a **fixed, base64-gzip'd probe table** generated once by
`l3_cart_gen.py` — "every ordered holder pair times the operator menu
runs," per the lane's own header comment. It is an exhaustive Cartesian
sweep over a static table, not stochastic fuzzing despite the directory's
name. Rerunning the lane reproduces the same probes and (for a
deterministic target language) the same recorded answers. **Losing it
costs the wall-clock time of rerunning already-preserved, deterministic
lanes — not information.**

**DIVERGED (10 single-file products, both copies exist, content differs —
this is a placement decision, listed in full below since it's short):**

| product | HQ path | newer | out bytes | hq bytes |
|---|---|---|---:|---:|
| `bf_rust-release.txt` | `Research/dominant_intentions/harness/results/` | out | 726 | 600 |
| `bf_rust.txt` | same dir | out | 726 | 600 |
| `bf_typescript.txt` | same dir | out | 20 | 621 |
| `core_modes_c.json` | `Research/op_pipeline/` | out | 1,184,609 | 1,258,979 |
| `core_modes_cache.json` | `Research/op_pipeline/` | out | 1,074,776 | 317,512 |
| `core_modes_cpp.json` | `Research/op_pipeline/` | out | 1,338,713 | 1,415,050 |
| `core_modes_go.json` | `Research/op_pipeline/` | out | 163,916 | 148,670 |
| `core_modes_rust.json` | `Research/op_pipeline/` | out | 183,482 | 171,018 |
| `core_modes_swift.json` | `Research/op_pipeline/` | out | 190,966 | 187,786 |
| `probe_manifest_java.json` | `Research/op_pipeline/` | **hq** | 1,040 | 1,074 |

Plus, inside the MIXED directories: `op_pipeline` has 13 further
file-level diverged pairs and 2 file-level absent-in-HQ files; each
`canon_units_*.json` and `sem_anchored_{c,cpp,go,rust,swift}.json` is
itself a *directory* (2 files each) where both files diverge from their
HQ counterpart. All are small (none over ~1.3 MB) and none changes the
headline number meaningfully.

## A protocol deviation, flagged separately

Six loose scripts sit in the Airlock repo's own root —
`run_sem_anchored.sh`, `run_sem_anchored2.sh`, `run_sem_anchored3.sh`,
`run_interp_normalizer3.sh`, `run_pip_list.sh`, `run_test_interp.sh`,
`run_test_interp4.sh` — plus a **0-byte** `d76_c1b_198.sh` (the real one,
non-empty, is correctly archived in `agent/drop/.done`). Airlock's own
`agent/README.md` says explicitly: "No lane scripts. A lane belongs to
the project that wrote it and lives in that project's own repo... There
is no `templates/` directory in Airlock, deliberately." These seven files
violate that. They are why `sem_anchored_*`'s exact wrapper (the
unpinned `pip install`) isn't traceable the way everything else was —
worth the owner's attention as a separate, small cleanup, not part of this
audit's product-by-product accounting.

## Volumes, in full

| volume | size (recounted) | largest contents | verdict |
|---|---:|---|---|
| `sandbox-persist` | 11 GB | `swift` 2.5G, `gocache` 860M, `dart-sdk` 642M, `dotnet` 624M, `rustup076` 578M, `ruby_ship` 547M, `cpython_ship` 492M, `cpython` 459M, ... plus small (`interp_b3` 129M = gcov/probe diary output, `ruby_test` 130M = upstream Ruby's own test suite) | toolchains + caches; the two "small" outliers are themselves regenerable diary output / upstream source, not original data |
| `t72-persist` | 3.6 GB | `llvmsrc` 2.2G (upstream clone), `llvmbuild` 784M, `gosrc` 316M, `gocache` 286M, `compile_diary_all` 36M (a diary, by definition regenerable) | toolchain source + build cache |
| `t81-persist` | 3.0 GB | `llvmsrc` 2.2G, `llvmbuild` 801M, `streams_cpp_probe_own.i32` 4.6M (probe output) | toolchain source + build cache |

**Nothing in any of the three volumes is anything other than toolchains,
build caches, or small regenerable probe/diary byproducts of building
them.** This is the direct, unqualified answer to the owner's "is that
unstable?": no — everything durable enough to need protecting either
already has a preserved recipe (checked above) or is disposable toolchain
material by design.

---

## Decided, recorded for audit

- Recount of `agent/out`: **268 top-level products, 9,734,518,662 bytes
  (9.73 GB), 6,004 files** at 2026-09-04T22:00:00Z (commands and output
  above).
- 58 products PLACED whole, 16 MIXED (partially placed), 10 DIVERGED
  (single file), 183 ABSENT — all by sha256 content comparison, not name.
- **6,345,478,961 bytes (6.35 GB, 65.2% of the total) exist only in
  `agent/out`.** Of that, 6.32 GB (99.6%) is the deterministic
  layer-3 CARTESIAN / `kind_fuzz_clustering` probe corpus, traced to
  preserved, deterministic lane scripts — regenerable, at the cost of
  compute time only. The remaining 12.46 MB (`sem_anchored_*`) is
  regenerable in substance but not guaranteed bit-identical on a rerun,
  because its lane wrapper is one of the seven not-checked-in scripts
  flagged above.
- Container volumes (17.6 GB total, recounted): toolchains and build
  caches throughout, with a handful of small regenerable diary files;
  nothing irreplaceable.
- No file was moved, copied into the tree, or deleted. Proof:

  ```
  $ cd ~/Programming/PseudoCoupHQ && git status --porcelain
  ?? Research/compiler_graph/variant_connections_c.json
  ?? Research/compiler_graph/variant_connections_c_and_cpp.json
  ?? Research/compiler_graph/variant_connections_cpp.json
  ```
  (all three are from concurrent, unrelated task-87 work — not written by
  this audit; this audit's own 4 lane scripts under
  `Research/airlock_audit/` were auto-committed by the repo-daemon during
  the run, visible at commits `95301377`/`8d65f19b`, and are the *only*
  files this audit added to the tree — no `agent/out` product among them)

  ```
  $ cd ~/Programming/Airlock && git status --porcelain
  ?? php-7.4.33.tar.gz
  ?? php-8.2.13.tar.gz
  ?? php-8.3.0.tar.gz
  ?? ruby-3.3.0.tar.gz
  ```
  (pre-existing, unrelated to this task, unchanged by it)

## Awaiting the owner

- **Whether to place the 6.32 GB regenerable probe corpus** (`ct_*` +
  `kind_fuzz_clustering`'s absent portion) into `Research/kind_fuzz_clustering/`
  now, or leave it in `agent/out` and treat "rerun the lane" as the
  recovery path. Either is defensible; this audit only established that
  it's safe either way (deterministic, recipe preserved).
- **The 10 single-file DIVERGED products + the diverged files inside
  `op_pipeline`, `canon_units_*`, `sem_anchored_*`**: which side is
  canonical. 9 of 10 single-file cases are newer in `agent/out`; 1
  (`probe_manifest_java.json`) is newer in the tree.
- **The seven loose lane scripts in Airlock's own root** (protocol
  deviation, above): move into a project repo, archive, or delete the
  stale 0-byte `d76_c1b_198.sh`.
- **Pin `pyvex`/`archinfo`/`angr`** in whatever becomes `sem_anchored`'s
  proper lane script, if the `sem_anchored_*` family is meant to be
  reproducible going forward.

Lane scripts and this log are the only artifacts this task added to
`PseudoCoupHQ`; nothing in `agent/out` was touched.
