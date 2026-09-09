# log_144 — TASK 50(b): the assignment-run re-capture

Dated 2026-09-02. TASK 50 part (b) from
`~/Programming/PseudoCoupHQ/DevComms/log_142_claude_code_task_briefs_round10.md`:
re-capture the 118 assignment-run testimony findings through the
verbatim path.

## 1. The starting facts, all three cited

1. `log_126_task37_testimony_defect.md` §3.2 measured the ALTERED
   count per store, including the three assignment stores:
   `op_units_asg_go.json` 33, `op_units_asg_rust.json` 26,
   `op_units_asg_swift.json` 0 (c and cpp asg stores: 0 each).
2. `log_131_task40_regeneration_trickle.md` §7.7 and §12.2 stated the
   118 as go 33 + rust 26 distinct captures, each appearing twice (in
   `op_pipeline/op_units_asg_<lang>.json` and its `stage_asg` union
   copy) = 118, and named the reason the round-8 re-capture never
   touched them: `probe_gen.py`'s `EXCLUDED_BUCKETS` excludes the
   assignment bucket, and its probes come from a different generator,
   `asg_stage.py`.
3. `log_140_open_calls_explained.md` §8 restated the same population
   and asked the open question this task answers: re-capture, or
   leave marked altered.

## 2. What ran — the mechanism, one step at a time

### 2.1 The manifests are already there

`asg_stage.py` already reads `probe_manifest_asg_<lang>.json` for
go/rust/swift/c/cpp (its own `combine()` call). Those three files
carry the SAME schema as the plain `probe_manifest_<lang>.json`
(`n`, `symbol`, `symbol_exact`, `source`, plus display-only fields
`operator`, `expression`, …), and the same probe counts log 126
measured:

```
$ python3 -c "..."
go 432 0 431 [...]
rust 396 0 395 [...]
swift 216 0 215 [...]
```

So `trickle2.py`'s existing `probes_for(lang, first, last, prefix)`
and `run_chunk` needed no new probe-reading code — only a different
`manifest_prefix`.

### 2.2 A new driver, `recapture_asg.py`, through Airlock's front door

`recapture_original.py` (round 8's plain-lane re-capture) drives
`trickle.run_chunk`, which reaches the container with `podman exec`
against a hand-copied Airlock (`~/Programming/AirlockTrickle`). That
route is superseded, stated in
`Research/op_pipeline/TRICKLE_SUPERSEDED.md` (2026-09-02): "Nothing
on the project side runs `podman`." So the new driver
(`Research/op_pipeline/recapture_asg.py`) uses `trickle2.py`'s
`Instance` / `run_chunk`, which submits through
`python3 <airlock>/airlock --instance trickle submit <lane> --no-batch`
and polls the instance's own status file — never `podman exec`.

### 2.3 The run

```
$ bash ~/Programming/Airlock/up.sh --instance trickle --cpus 6
  trickle-runner already existed; started (bound to .../instances/trickle/agent/drop)
  trickle-runner  Up 55 seconds  localhost/sandbox-runner:latest

$ /tmp/reconnect_venv/bin/python3 recapture_asg.py --plan
planned 4 chunks over 1044 probes

$ /tmp/reconnect_venv/bin/python3 recapture_asg.py --run
instance trickle  runner trickle-runner  cpus 6  agent .../instances/trickle/agent
  asgrecap_go_c0000      400 submitted     54 accepted    346 refused    31.4s
  asgrecap_go_c0001       32 submitted      5 accepted     27 refused     7.5s
  asgrecap_rust_c0000    396 submitted     61 accepted    335 refused    17.5s
  asgrecap_swift_c0000   216 submitted     29 accepted    187 refused    49.5s
operator inventory: 91 tokens read from probe_manifest_*.json
PASS recapture_asg_state.json -- no operator token in any key, grouping, pairing or row structure
```

The two go chunks sum to 59 accepted / 373 refused, matching log
131's original `op_asg_go.sh` table exactly (432 submitted, 59
accepted, 373 refused, 23.0s original vs 38.9s here — this run
included the compiler-version self-check every lane carries, on a
6-core capped instance rather than the 2026-08-25 uncapped one). Rust
(61/335) and swift (29/187) match their original tables identically
too.

```
$ /tmp/reconnect_venv/bin/python3 recapture_asg.py --merge
  go       432 probes  tally {'submitted': 432, 'accepted': 59, 'refused': 373, ...}
           -> op_units_asg_go_verbatim.json
  rust     396 probes  tally {'submitted': 396, 'accepted': 61, 'refused': 335, ...}
           -> op_units_asg_rust_verbatim.json
  swift    216 probes  tally {'submitted': 216, 'accepted': 29, 'refused': 187, ...}
           -> op_units_asg_swift_verbatim.json
PASS op_units_asg_go_verbatim.json -- no operator token in any key, grouping, pairing or row structure
PASS op_units_asg_rust_verbatim.json -- (same)
PASS op_units_asg_swift_verbatim.json -- (same)
```

**No existing store was touched.** `op_units_asg_<lang>.json`,
`probe_manifest_asg_<lang>.json`, and every `stage_asg/*` copy were
opened read-only, by `build_supersession_asg.py` only, in step 3.
The three `op_units_asg_<lang>_verbatim.json` files are new.

## 3. The supersession sidecar, extended

### 3.1 The join

`build_supersession_asg.py` reads `supersession_altered_testimony.json`'s
`out_of_scope` list (118 records) and joins each to the new verbatim
stores by PROBE NUMBER, never by spelling:

- `origin_store` starting `op_pipeline/` → the verbatim store's key
  is the record number unchanged.
- `origin_store` starting `stage_asg/` → `asg_stage.py`'s own
  `ASG_N_OFFSET = 100000` is subtracted to get the verbatim store's
  key (verified against `asg_stage.py`'s `offset_probes()`).

A record is marked SUPERSEDED only when the verbatim store's decoded
`refused` text for that key equals `suspected_original_in_log_126`
CHARACTER FOR CHARACTER; anything else is reported as a mismatch or
unresolved, never guessed.

### 3.2 The result

```
$ /tmp/reconnect_venv/bin/python3 build_supersession_asg.py
out_of_scope in source     118
superseded now             118
mismatched                 0
unresolved                 0
operator inventory: 91 tokens read from probe_manifest_*.json
PASS supersession_altered_testimony2.json -- no operator token in any key, grouping, pairing or row structure
```

**118/118 matched, 0 mismatches, every mismatch line pasted above
would be empty because there were none.** One worked example, the
same record log 126 §3.2 walked:

| field | value |
|---|---|
| origin | `op_pipeline/op_units_asg_go.json` record 325 |
| stored (2026-08-25 lane) | `./main.go:6:2: invalid operation: a /= b (mismatched types int32 and int64)` |
| log 126 suspected original | `./main.go:6:2: invalid operation: a \|= b (mismatched types int32 and int64)` |
| recaptured (task 50(b)) | `./main.go:6:2: invalid operation: a \|= b (mismatched types int32 and int64)` |
| match | character for character |

## 4. Instance down

```
$ bash ~/Programming/Airlock/down.sh --instance trickle
  removed trickle-runner
done.
```

## 5. THE SPELLING BAN — where the guard ran

`check_no_spelling_keys.py` ran on every output this task wrote:
`recapture_asg_state.json`, the three `op_units_asg_<lang>_verbatim.json`
stores, and `supersession_altered_testimony2.json` — all four PASS
lines pasted above/in §2.3/§3.2. Both new programs (`recapture_asg.py`,
`build_supersession_asg.py`) delete their own output and raise on
guard failure, per the mechanical-guard requirement.

Pasted verbatim, as required: "THE SPELLING BAN, ABSOLUTE (the owner,
restated in anger 2026-08-25 after a second violation). No operator
token may appear in ANY key, grouping, pairing, row structure,
candidate selection, or comparison scope, anywhere in this line — not
in matching, not in "which pairs get compared", not in report rows,
not in dropdowns. The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from
ratified intention — never from the token. The token appears exactly
once per unit: as a display label on the member. HISTORY OF
VIOLATIONS, so the pattern is visible: (1) the arch campaign's
cross-language matrix (caught by the owner 2026-08-24); (2) verdicts.py's
row pairing (caught by the owner 2026-08-25 — the fix brief itself
reintroduced it as "same-operator pairs"). MECHANICAL GUARD REQUIRED:
every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

## 6. Full file inventory

All paths under `~/Programming/PseudoCoupHQ/Research/op_pipeline/`
unless noted. All NEW files; nothing pre-existing was opened for
writing.

| file | what it is |
|---|---|
| `recapture_asg.py` | driver: plans/runs/merges the assignment-lane re-capture through `trickle2.py`'s Airlock-submit route |
| `recapture_asg_state.json` | chunk-level resume state (4 chunks, all done) |
| `trickle_lanes/asgrecap_asgrecap_{go_c0000,go_c0001,rust_c0000,swift_c0000}.sh` | the exact lane scripts submitted |
| `trickle_raw/asgrecap_asgrecap_*.{txt,console.log}` | raw lane products and console logs, one pair per chunk |
| `trickle_store/op_units_asgrecap_asgrecap_{go_c0000,go_c0001,rust_c0000,swift_c0000}.json` | per-chunk folded stores (verbatim-decoded) |
| `op_units_asg_go_verbatim.json` (301,518 bytes) | merged go assignment-run verbatim store, 432 probes |
| `op_units_asg_rust_verbatim.json` (269,284 bytes) | merged rust assignment-run verbatim store, 396 probes |
| `op_units_asg_swift_verbatim.json` (137,723 bytes) | merged swift assignment-run verbatim store, 216 probes |
| `build_supersession_asg.py` | sidecar builder: joins the 118 out-of-scope findings to the verbatim stores by probe number |
| `supersession_altered_testimony2.json` (83,976 bytes) | the extended sidecar — 118/118 superseded, 0 mismatched, 0 unresolved |

`supersession_altered_testimony.json` (round 8's sidecar, 218/336
superseded) is UNCHANGED — read-only in this task, never opened for
writing.

## 7. What is now true

- All 336 altered-testimony findings from log 126 are accounted for:
  218 superseded in round 8 (`supersession_altered_testimony.json`),
  118 superseded now (`supersession_altered_testimony2.json`). 0
  remain marked merely altered.
- The 336 total splits as go 101 (68 plain + 33 assignment), rust 58
  (32 + 26), swift 9 (9 plain + 0 assignment) — the swift assignment
  bucket contributed 0 altered records to begin with (log 126 §3.2),
  so its re-capture ran (216 probes, 29 accepted, 187 refused) but
  superseded nothing because there was nothing in that bucket to
  supersede.
- The daemon commits; this session made no manual commit.

Report path: `~/Programming/PseudoCoupHQ/DevComms/log_144_task50b_assignment_recapture.md`.
