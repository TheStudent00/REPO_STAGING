# log 156 — TASK 56: bank round 11

Date: 2026-09-03. Author: Claude Code (implementer), no sub-agents.
Working directory: `PseudoCoupHQ/Research/op_pipeline`.
Python: `/tmp/reconnect_venv/bin/python3`.

Every rendering below is labelled **LITERAL**, **GLOSS** or **ANALOGY**,
per the protocol's §5.1a. A gloss never appears without the literal it
glosses. Every figure states its population, per §3.4a.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line — not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention — never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

Correction-sections check, done before anything else: `log_152`,
`log_153`, `log_154`, `log_155` each searched for a heading containing
"correction" — none found. Reading each in full turned up no place
where a round-11 claim was walked back. Stated here because the brief
requires re-running before ruling, not trusting the absence.

---

## 1. Full-stack verification

### 1.1 The spelling-ban guard, run unmodified, 16 files

I VERIFIED. Command run once per file, same process, same script,
no edits:

```
$ cd PseudoCoupHQ/Research/op_pipeline
$ for f in the_pool3.json canon38_guard.json layer4c_state.json \
    name_census4.json canon38_wrapped_c.json canon38_wrapped_cpp.json \
    canon38_wrapped_go.json canon38_wrapped_rust.json \
    canon38_wrapped_swift.json layer4c_terms_c.json \
    layer4c_terms_cpp.json layer4c_terms_go.json \
    layer4c_terms_rust.json layer4c_terms_swift.json \
    the_pool2.json name_census3.json; do
  out=$(/tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py "$f" 2>&1)
  rc=$?
  cnt=$(echo "$out" | grep -c exempt)
  echo "$f rc=$rc exempt_count=$cnt last=$(echo "$out"|tail -1)"
done
```

Output (all 16 lines):

```
the_pool3.json rc=0 exempt_count=0 last=PASS the_pool3.json -- no operator token in any key, grouping, pairing or row structure
canon38_guard.json rc=0 exempt_count=0 last=PASS canon38_guard.json -- no operator token in any key, grouping, pairing or row structure
layer4c_state.json rc=0 exempt_count=0 last=PASS layer4c_state.json -- no operator token in any key, grouping, pairing or row structure
name_census4.json rc=0 exempt_count=0 last=PASS name_census4.json -- no operator token in any key, grouping, pairing or row structure
canon38_wrapped_c.json rc=0 exempt_count=0 last=PASS canon38_wrapped_c.json -- no operator token in any key, grouping, pairing or row structure
canon38_wrapped_cpp.json rc=0 exempt_count=0 last=PASS canon38_wrapped_cpp.json -- no operator token in any key, grouping, pairing or row structure
canon38_wrapped_go.json rc=0 exempt_count=0 last=PASS canon38_wrapped_go.json -- no operator token in any key, grouping, pairing or row structure
canon38_wrapped_rust.json rc=0 exempt_count=0 last=PASS canon38_wrapped_rust.json -- no operator token in any key, grouping, pairing or row structure
canon38_wrapped_swift.json rc=0 exempt_count=0 last=PASS canon38_wrapped_swift.json -- no operator token in any key, grouping, pairing or row structure
layer4c_terms_c.json rc=0 exempt_count=0 last=PASS layer4c_terms_c.json -- no operator token in any key, grouping, pairing or row structure
layer4c_terms_cpp.json rc=0 exempt_count=0 last=PASS layer4c_terms_cpp.json -- no operator token in any key, grouping, pairing or row structure
layer4c_terms_go.json rc=0 exempt_count=0 last=PASS layer4c_terms_go.json -- no operator token in any key, grouping, pairing or row structure
layer4c_terms_rust.json rc=0 exempt_count=0 last=PASS layer4c_terms_rust.json -- no operator token in any key, grouping, pairing or row structure
layer4c_terms_swift.json rc=0 exempt_count=0 last=PASS layer4c_terms_swift.json -- no operator token in any key, grouping, pairing or row structure
the_pool2.json rc=0 exempt_count=0 last=PASS the_pool2.json -- no operator token in any key, grouping, pairing or row structure
name_census3.json rc=0 exempt_count=0 last=PASS name_census3.json -- no operator token in any key, grouping, pairing or row structure
```

16/16 PASS, `grep -c exempt` = 0 on every transcript, one process each
(the count column above IS that grep, computed inline and pasted, not
narrated). File selection: every grouping artifact log_152/153/154's
own inventories name for round 11 (`the_pool3.json` — the pool;
`canon38_guard.json` — the layer-3 guard; `layer4c_state.json` — the
layer-4 census store; `name_census4.json` — the name census), plus
their five per-language shards each (canon38's wrapped store,
layer4c's terms store), plus the two superseded artifacts the_pool2.json
and name_census3.json as the brief's spot-check of prior stores. This
is the full set of round-11 JSON stores that group or pair units; no
file matching that description was left out.

### 1.2 The authoritative count line over the_pool3's population

LITERAL — `the_pool3.json`, `summary` block, read directly:

```
$ /tmp/reconnect_venv/bin/python3 -c "
import json
d=json.load(open('the_pool3.json'))
print(json.dumps(d['summary'], indent=1))
"
{
 "brief_strict_layer5_identity_merges": 22028,
 "distinct_layer3_wrapped_texts": 2997,
 "distinct_layer5_texts_among_eligible_units": 1104,
 "entries": 2247,
 "entries_spanning_compiled_and_interpreted": 3,
 "entries_spanning_more_than_one_language": 632,
 "entries_under_the_brief_strict_rule": 8394,
 "entries_with_more_than_one_layer5_text": 187,
 "entries_with_more_than_one_wrapped_text": 394,
 "layer3_identity_merges": 27439,
 "layer5_identity_merges": 22028,
 "proved_edges_applied": 118,
 "units_by_arrival_population": {
  "interpreter": 9,
  "original": 1763,
  "regenerated": 28664
 },
 "units_in_the_pool": 30436,
 "units_not_layer5_eligible": 7304,
 "units_undecided_at_layer4": 5602,
 "units_with_no_layer4_term": 1287,
 "units_withdrawn_at_layer4": 415
}
```

**THE COUNT LINE: 2,247 entries over the_pool3's population of 30,436
member units** (original 1,763 of 1,779 attempted; interpreter 9 of
11 attempted; regenerated 28,664 of 29,288 attempted — denominators
from log_154 §1.2, which cites `the_pool3.json` `meta.population`;
1,779 + 11 + 29,288 = 31,078, matching log_154's "30,436 of 31,078
attempted"). Layer 4 beside it, same 30,436 population:
**23,132 proved / 415 withdrawn / 5,602 undecided / 1,287 no term**
(415 + 5,602 + 1,287 = 7,304 = `units_not_layer5_eligible`; 30,436 −
7,304 = 23,132 proved, matching log_153).

**THE 13 ROUND-5/6 WITHDRAWN UNITS, LISTED SEPARATELY** (source:
log_139 §2.2, itself citing log_112 lines 459-475, 661): 11 swift
units and 2 go units, re-gated against real ship blocks and found
DISPROVED with a counterexample. These are NOT part of the 30,436 —
they are a round-5/6 population the continuity chain still excludes
by name from both the 1,779 and the current pool, worked instance
`swift/op_13` (real code keeps a shift's value 64-bit, `mov
%rdi,%rax`; the withdrawn candidate truncated it to 32-bit, `mov
%edi,%eax`; its 32-bit counterpart `swift/op_12` is correct and still
proves — a real candidate defect, not a modelling artifact).

**THE BRIEF-STRICT COUNT'S ACTUAL KEY PATH**: `entries_under_the_
brief_strict_rule` = 8,394, at `the_pool3.json` → `summary` →
`entries_under_the_brief_strict_rule`. Confirmed by direct read above
(the key literally appears in the `summary` dict printed). No
top-level key named for it exists in the file (the top level is only
`entries`, `meta`, `summary` — checked: `list(d.keys())` = `['entries',
'meta', 'summary']`); the count lives inside `summary`, one level
down. Distinguish from `brief_strict_layer5_identity_merges` (22,028),
a different figure on the same object — the 8,394 is the entry count
under the brief-strict rule, the 22,028 is a merge count.

### 1.3 Prior artifacts verified untouched, as superseded records

I VERIFIED (md5 + `git status --porcelain` + `git log -1`, from
`PseudoCoupHQ/Research/op_pipeline`):

```
$ md5sum the_pool2.json canon37_guard.txt layer4b_state.json name_census3.json
1ed4f2fab6640f0fef302fc43cbd47f1  the_pool2.json
34794e29b522dacf3c4a629fd5f51dbd  canon37_guard.txt
2f9df10fd24661f363831be8cd5fd342  layer4b_state.json
3e8f64df8a364bddb9ac2582a8e70375  name_census3.json

$ git status --porcelain the_pool2.json canon37_guard.txt layer4b_state.json name_census3.json
(empty -- working tree matches HEAD on all four)

$ git log -1 --format="%H %ci" -- the_pool2.json
7cf2c2db320240100284347262f3af556ada70cf 2026-09-02 21:09:42 -0400
$ git log -1 --format="%H %ci" -- canon37_guard.txt
b760c3d87774947ac911826c307e2d4345c86e94 2026-09-02 20:00:12 -0400
$ git log -1 --format="%H %ci" -- layer4b_state.json
5752b7d6fa57babc53f5eebd580cf847b29168c8 2026-09-02 21:01:42 -0400
$ git log -1 --format="%H %ci" -- name_census3.json
5752b7d6fa57babc53f5eebd580cf847b29168c8 2026-09-02 21:01:42 -0400
```

No round-11 task wrote to any of these four files: `git status
--porcelain` is empty on all of them and the last commit touching each
predates round 11's canon38/layer4c/pool3 work. They stand as the
superseded records log_152/153/154 describe them as.

### 1.4 Airlock

I VERIFIED:

```
$ podman ps
CONTAINER ID  IMAGE                            COMMAND               CREATED      STATUS      PORTS       NAMES
4ed0765eb489  localhost/va-proxy:latest        squid -N -d 1 -f ...  9 hours ago  Up 9 hours  3128/tcp    va-proxy
ffa29c11714e  localhost/sandbox-proxy:latest   squid -N -d 1 -f ...  9 hours ago  Up 9 hours  3128/tcp    sandbox-proxy
66eaf0524a25  localhost/sandbox-runner:latest  python3 -u /opt/d...  9 hours ago  Up 9 hours              sandbox-runner

$ python3 Airlock/airlock doctor
doctor: Airlock
| severity | check | what was seen | what to do |
|---|---|---|---|
| WARN | agent/drop clutter | .../agent/drop/test_parse.py is not a runnable lane | rm it, on the host |
| NOTE | instances | 2 known: sandbox (running), trickle (absent) | -- |
| NOTE | AIRLOCK_CPUS | instance sandbox resolves to 6 cpu(s) | -- |
| NOTE | agent/out contents | 259 entries, nothing prunes automatically | -- |
| NOTE | /work headroom | most recent lane recorded 4096 MB free | -- |
| OK | podman | on PATH | -- |
| OK | sandbox-runner | running | -- |
| OK | sandbox-proxy | running | -- |
| OK | agent binds | bound to this repo's agent folders | -- |
| OK | quadlet vs up.sh | agree on 6 cpu(s) | -- |
| OK | granted cores | 6 cpu(s), matching setting | -- |
| OK | toolchains | python3, rustc, cargo, go, node, javac, gcc, clang, git all answer inside sandbox-runner | -- |
| OK | egress allowlist | 25 hostnames allowed | -- |
| OK | agent/out free space | 68.7 GB free (87% used) | -- |
  1 WARN, 4 NOTE, 9 OK
  exit 0 -- no real faults.
```

sandbox-runner container is up, but this is a process check, not an
image check — it does not by itself confirm the rebuilt image from
log_155's ruling 6 is what is running. Carried forward as an open
item in §3 below (log_155 already flagged it: "sandbox-runner still
on the pre-rebuild image until restarted").

---

## 2. State of the line (Appendix-B shape)

### 2.1 The seven-layer chain, current artifact per layer, as it stands on disk

| layer | current artifact | population | note |
|---|---|---|---|
| 1 assembled bytes | canon38 assemble store (`canon38_assemble.json` + `canon38_regen_store`) | 31,078 attempted, 30,436 succeeded | superseded canon37 store retained, untouched |
| 2 interp table | `canon38_interp.json` | per log_152 | |
| 3 canonical/wrapped text | `canon38_wrapped_*.json` (5 languages) | 2,997 distinct texts | down from canon37's 6,277 (ruling 4's positional branch labels) |
| 4 z3 term / proof | `layer4c_terms_*.json` (5 languages) + `layer4c_state.json` | 23,132 proved / 415 withdrawn / 5,602 undecided / 1,287 no term, over 30,436 | STACK (3,360) and X87 (1,405) rows written, lineage closed, not proved |
| 5 dominant-operator merge | `the_pool3.json` (layer5 identity merges 22,028) | 1,104 distinct layer-5 texts among eligible units | |
| 6 pool / entry | `the_pool3.json` | 2,247 entries over 30,436 members | pool2 (5,274 entries) superseded, kept on disk |
| 7 name census | `name_census4.json` | 54/1,719/1,668 (per log_153) | three predicted causes at zero |

### 2.2 The pool

2,247 entries / 30,436 members / 632 multi-language / 3
compiled-and-interpreted / 36 families over the same 197 nodes.
E00029 unchanged at 158 members. 60 splits / 719 merges against pool2
(causes: layer-3 identity 711, layer-5 identity 13, transitive-only
0). Brief-strict rule: 8,394 entries (§1.2, key path stated there).

### 2.3 The census

`name_census4.json`: 54 / 1,719 / 1,668, the three predicted causes at
zero (per log_153's own statement; this session did not re-derive the
census, only confirmed the artifact is guard-clean, §1.1).

### 2.4 This round's corrections

None. Re-running the correction-section check (§0 above, repeated
here as the ruling): logs 152, 153, 154, 155 carry no heading or
passage walking back a round-11 claim. Stated only after the check,
per the brief's instruction to re-run rather than assume.

### 2.5 the owner's open calls, read from each cited log's correction-adjacent sections first

1. **The SRem-vs-percent remainder reference** (log_153 §"THE CARRY
   BIT..." / item 1, lines ~425-437). z3's `%` is signed-modulo; x86's
   `idiv` remainder is signed-remainder. Reproduced: `7 % −3` gives
   `−2` under modulo, `1` under SRem. 415 units remain withdrawn on
   this split; 410 others already moved from withdrawn to proved once
   the reference was corrected to SRem for the quotient half. Which
   reference the layer-4 term should use for the remainder half is
   still open.
2. **`call` as a producer** (log_153, a 300-unit census cause).
3. **A gate route for the machine stack (STACK, 3,360 units
   undecided) and the x87 stack (X87, 1,405 units undecided)**
   (log_153 §4.3). Both rows are written and their lineage is closed,
   but neither has a proof route yet: `STACK: units carrying such a
   row 3360`, `STACK: units undecided on both routes 3360`, `X87:
   units carrying such a row 1405` (figures pasted directly from
   log_153's own transcript, not re-derived here).
4. **The canon38 prelude/dataflow disagreement on mixed vector+general
   arrivals** (log_153 §"THE ARRIVAL BINDING...", worked instance
   `c/op_105`: `cvtsi2ss %edi,%xmm1; addss %xmm1,%xmm0; ret`).
   `ledger48.build_prelude` emits vector arrivals first, so `IN-0` is
   the first vector family's row; `ledger48.walk_dataflow`'s own
   wiring disagrees with the prelude's binding on which input `IN-0`
   names. log_153's ruling: the arrival binding follows the ledger's
   wiring, not the prelude's — but this is recorded as a call still
   open for the owner to ratify, not closed by this session.
5. **The `!!reloc` note in 8 assembled texts** (log_154 §"the stored
   text keeps..."): a constant-pool relocation comment
   (`addsd 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4`) that
   falls back to character length rather than being parsed structurally.
6. **Restarting `sandbox-runner` onto the rebuilt image** (log_155
   ruling 6): confirmed still open in §1.4 above — the container is
   up but this session did not verify which image build it is running.

---

## 3. Posterity message

I VERIFIED:

```
$ wc -c PseudoCoupHQ/DevComms/next_commit_message.txt
2280 PseudoCoupHQ/DevComms/next_commit_message.txt

$ head -5 PseudoCoupHQ/DevComms/next_commit_message.txt
Round 11 banked (TASK 56, log_156). The pool now stands at 2,247
entries over the full 30,436-member population (original 1,763 of
1,779; interpreter 9 of 11; regenerated 28,664 of 29,288), built over
canon38 and layer4c. Layer 4 on that same 30,436: 23,132 proved / 415
withdrawn / 5,602 undecided / 1,287 no-term. The 13 round-5/6
```

The daemon consumes this file by design: `Misc/repo_
daemon/repo_daemon.py` line 159-161 names exactly this path
(`"DevComms/next_commit_message.txt"`, plus two legacy variants) as
one of the message sources it reads and (per `README.md` line 107)
clears after consuming. As of this write it has NOT yet run against
this file: `git log -1 -- DevComms/next_commit_message.txt` on
PseudoCoupHQ shows no commit touching this path at the current HEAD
(the most recent PseudoCoupHQ commits are generic `auto: N files
(...)` messages from before this write). Whether it has run by the
time this report is read: check `git log -1 --format=%s` on
PseudoCoupHQ — if it names this round's content rather than a bare
file list, the daemon consumed it.

---

## 4. Files created this session

- `PseudoCoupHQ/DevComms/next_commit_message.txt` (2,280
  bytes) — posterity message, §3.
- `PseudoCoupHQ/DevComms/log_156_task56_bank_round11.md`
  — this report.
- Appended to `PseudoCoupHQ/Planning/node_0_3_research/
  node_0_3_5_compiler_graph/PROGRESS.md` under the existing `# PROGRESS`
  heading (not a new file).

No pipeline artifact (JSON, py, txt) was created or modified this
session — TASK 56 is a verification and banking pass over round 11's
existing output, not a new pipeline stage.
\n\n## CORRECTION (2026-09-03, coordinator) — the "call as a producer" open call is WITHDRAWN\n\nThe 300 units whose answer comes from `call __udivti3` / `__umodti3` / `__divti3` / `__modti3` are LIBRARY ROUTINES, not compiler operations. By the standing ruling (AgentMemory line 135: layer 3 is "what the COMPILER can do to a representation — the measured dynamics, never builtins") they are OUT OF SCOPE. They should never have been posed as a question for the owner, and the phrase "library-call units" should not have been coined. Recorded as excluded in `Research/op_pipeline/out_of_scope_library_calls.json`; the next pool/proof rebuild drops them from its population. Nothing in this log's earlier text is edited.\n