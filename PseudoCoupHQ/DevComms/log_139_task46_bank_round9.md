# log_139 — Task 46: bank round 9

Population of this log: round 9's four reports (log_135 Task 43,
log_136 Task 44, log_137 Task 45, log_138 Airlock instances) plus this
task's own verification runs. Every number below states which of
those populations it counts.

---

## 1. Guard: check_no_spelling_keys.py over round 9's grouping artifacts

Artifacts enumerated from log_135/136/137's own inventories and
verified present on disk before running: `the_pool1.json` (log_136,
built by `build_the_pool1.py`), `the_families1.json` (log_136, built
by `build_the_families1.py`). These are round 9's only two grouping
artifacts of population size (the pool over 28,984 member units and
its families over 190 nodes) — dominant_table24/24b/25 and
dom_ops22/22b/23 are round-8-and-earlier records, checked separately
in §3 as superseded, not as round-9 grouping output.

I VERIFIED (command + output pasted, run from
`PRIVATE/PseudoCoupHQ/Research/op_pipeline`):

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py the_pool1.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS the_pool1.json -- no operator token in any key, grouping, pairing or row structure
EXIT:0

$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py the_families1.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS the_families1.json -- no operator token in any key, grouping, pairing or row structure
EXIT:0
```

Both PASS with EXIT 0, no exemption argument passed, no exemption
present in the script's own except-list applying to a grouping key
here (the except-list is per-unit display fields only, per the
script's own docstring, read in full before running it).

---

## 2. The one authoritative count line

**Pool entries 5,548 over 28,984 member units.**

Populations that make up the 28,984, each stated against its own
corpus size:

- original: 1,752 proved of 1,779
- interpreter: 9 proved of 11
- regenerated: 27,223 proved of 29,288

I VERIFIED (same directory):

```
$ /tmp/reconnect_venv/bin/python3 -c "
import json
d=json.load(open('the_pool1.json'))
print(json.dumps(d['summary'], indent=2))"
{
  "distinct_universal_texts": 5572,
  "entries": 5548,
  "entries_spanning_compiled_and_interpreted": 3,
  "entries_spanning_more_than_one_language": 663,
  "entries_with_more_than_one_universal_text": 20,
  "proved_edges_applied": 118,
  "text_identity_merges": 23412,
  "units_by_arrival_population": {
    "interpreter": 9,
    "original": 1752,
    "regenerated": 27223
  },
  "units_in_the_pool": 28984
}
```

### 2.1 The original-1,779 subset, beside it

Filter is a real filter over the live pool (keep members whose
`population` field reads `original`), not a second kept table — run
via `the_pool1_original_subset.py`, which is itself the same script
log_136 built for this purpose.

I VERIFIED:

```
$ /tmp/reconnect_venv/bin/python3 the_pool1_original_subset.py
== filtered to members whose population reads 'original'
{
 "edges_mutual": 205,
 "edges_raw": 391,
 "entries": 604,
 "families": 26,
 "member_units": 1752,
 "nodes": 140,
 "nodes_in_a_family": 119,
 "nodes_with_no_surviving_edge": 21
}
```

So: **1,752 units / 604 entries / 140 nodes / 26 families / 21
unattached** — matching log_136's own reported figures exactly (no
drift since that report).

### 2.2 The 13 withdrawn units, listed separately

These are NOT round 9 output — they are a round-5/6 population
(log_112 Task 26's branching audit) that the continuity chain still
carries as a named exclusion from the 1,561/1,622 baseline, kept
separate rather than folded into either the 1,779 or the 1,752:
11 swift units and 2 go units, each re-gated against real ship blocks
and found DISPROVED with a counterexample, not silently dropped.
Worked instance recorded in log_112: `swift/op_13` — real code keeps
the shifted value 64-bit (`mov %rdi,%rax`), the candidate truncated it
to 32-bit (`mov %edi,%eax`); its 32-bit counterpart `swift/op_12` is
correct and still proves, so the defect is a real candidate defect,
not a modelling artifact. Source: log_112 lines 459-475, 661.

---

## 3. Prior tables verified untouched, as superseded records

I VERIFIED (md5 + git diff against last commit, from
`PRIVATE/PseudoCoupHQ/Research/op_pipeline`):

```
$ md5sum dominant_table24.json dominant_table24b.json dominant_table25.json dom_ops22.json dom_ops22b.json dom_ops23.json
c33b62c32cc084b1abc826eab536c9be  dominant_table24.json
0887dd403a950c10fd5a25e51d552cb2  dominant_table24b.json
b36a90976aaf567b1ef2610e753f0160  dominant_table25.json
6e8bb141a2b7bbe9589668a538333f42  dom_ops22.json
1f67e9bc8f42e35795beb217e41b13f2  dom_ops22b.json
72aa97859f01c52f88b1ac6e334f3a29  dom_ops23.json

$ git log -1 --format=%H -- Research/op_pipeline/dominant_table24.json Research/op_pipeline/dominant_table25.json Research/op_pipeline/dom_ops22.json Research/op_pipeline/dom_ops23.json
d2e929d7e7b317c590fb5fd5814126b3f7232a90

$ git diff --stat -- Research/op_pipeline/dominant_table24.json Research/op_pipeline/dominant_table25.json Research/op_pipeline/dom_ops22.json Research/op_pipeline/dom_ops23.json
(no output -- empty diff, working tree matches last commit)
```

Empty diff means the working-tree copy is byte-identical to what git
already holds; nothing in round 9 wrote to these files. They stand as
superseded records only, cited for continuity in §2.1/log_136, never
recomputed.

---

## 4. Airlock: two instances, default running

I VERIFIED:

```
$ podman ps
CONTAINER ID  IMAGE                            COMMAND               CREATED         STATUS         PORTS       NAMES
4ed0765eb489  localhost/va-proxy:latest        squid ...             57 minutes ago  Up 57 minutes  3128/tcp    va-proxy
ffa29c11714e  localhost/sandbox-proxy:latest   squid ...             57 minutes ago  Up 57 minutes  3128/tcp    sandbox-proxy
66eaf0524a25  localhost/sandbox-runner:latest  python3 -u /opt/d...  57 minutes ago  Up 57 minutes              sandbox-runner

$ python3 PUBLIC/Airlock/airlock doctor
| severity | check | what was seen |
| WARN | agent/drop clutter | test_parse.py not a runnable lane |
| NOTE | instances | 2 known: sandbox (sandbox-runner: running) <- this command; trickle (trickle-runner: absent) |
...
| OK | sandbox-runner | running |
| OK | sandbox-proxy | running |
  1 WARN, 4 NOTE, 9 OK
  exit 0 - no real faults.
```

Both instances (`sandbox`, `trickle`) are listed by the doctor's own
`instances` row; `sandbox` is the one running and is the default this
command resolved to with no `--instance` flag given, confirming
default-running as required.

---

## 5. One-page state-of-the-line summary (reading form)

**region36 (the form redone).** log_135, Task 43. The universal form
was rebuilt end to end under `region36.py`: 1,752/1,779 original
proved, 9/11 interpreter proved, 27,223/29,288 regenerated proved.
Zero-regression run against round 8: 1,744 → 1,752 proved (net +8: 2
lost — `swift/op_703`, `swift/op_739`, both spend `%r15` as a value
across what the gate treats as an absolute relocation — 10 gained).
17 round-8 texts merged into one round-9 text; 36 split into more than
one. Six address-of units proved this round that were not proved
before. Three items were left open for the owner (§6).

**The pool (the owner's correction 2 satisfied).** log_136, Task 44. The
compiled-only table stops existing as a kept object; anyone wanting
one now filters `the_pool1.json`, the single pool of 5,548 entries
over 28,984 member units, spanning 3 compiled+interpreted languages
and 31 families with none a singleton. the owner's correction — that the
CPython/c entry (`E00033`) must be named, not folded silently — is
satisfied by the pool's own `entries_spanning_compiled_and_interpreted:
3` field and the entry's presence in `the_pool1.json` under that id.

**The type witness (declarable witness).** log_137, Task 45. A second,
independent witness for a unit's declared type — not derived from the
same evidence the first witness used — demoted 85 of 208 candidate
types the first witness alone would have accepted. Over the full
candidate space of 34,182, the two witnesses together explain 95.1%
of refusals, and zero accepted unit carries a demoted type. 276 misses
trace to one swift emitter cause (open call, §6).

**Airlock (the application fix).** log_138. The AirlockTrickle fork —
a renamed, modified copy of the Airlock tree, built to let two sandbox
configurations run at once — is retired as the wrong shape: Airlock is
an application projects USE, never clone/rename/modify (standing
rule). The real fix is the "instances" feature added to Airlock
itself: `instances/<name>.conf` plus `airlock --instance <name>`,
verified in §4 running two named instances (`sandbox` running,
`trickle` absent) from the one codebase. The inotify-instance-cap
attribution for the watcher failure was corrected in the same log to
`fs.inotify.max_user_watches` (a different kernel limit than the one
first named). 339 fork lanes were deleted externally; surviving
material lives in `trickle_lanes/raw/store`.

---

## 6. the owner's open calls (carried forward, not decided this round)

From Task 43 (log_135, §13.2):
1. The 4 units that spend `%r15` across an absolute relocation
   (`swift/op_703`, `swift/op_739`, and two more of the same shape) —
   whether the gate's relocation model should widen or the units
   should stay refused.
2. Materializing temp/guard lineages as first-class records rather
   than reconstructing them per-run.
3. The 1,479 vector-upper-lane refusals — whether they are a modelling
   gap or a genuine population the gate should keep refusing.

From Task 45 (log_137): the swift emitter fix behind the 276 misses
that trace to one cause.

From Task 44/Airlock (log_138): Airlock's ten naming choices for the
instances feature; whether trickle-style multi-instance use should run
serial or concurrent; where the agent-tree/session-tree state for a
non-default instance should live.

From the assignment-run testimony work: 118 findings, not yet ruled on.

---

## 7. Posterity message

Written to `PRIVATE/PseudoCoupHQ/DevComms/next_commit_message.txt`,
including this session's two process corrections (the AirlockTrickle
copy-where-a-feature-was-needed correction, and the inotify
max_user_watches attribution correction). The repo-daemon consumes
this file by design (systemd auto commit-push every 30s across the
~/Programming repos, per the repo-daemon memory note) — it is a
message left for the next commit, not a commit itself, and is expected
to be overwritten by that pass.

I VERIFIED:

```
$ wc -c PRIVATE/PseudoCoupHQ/DevComms/next_commit_message.txt
2422 PRIVATE/PseudoCoupHQ/DevComms/next_commit_message.txt

$ head -5 PRIVATE/PseudoCoupHQ/DevComms/next_commit_message.txt
Round 9 banked (Task 46, log_139): region36 form redone (1,752/1,779
original proved, 9/11 interpreter, 27,223/29,288 regenerated), THE
POOL (5,548 entries over 28,984 member units; original-1,779 subset:
1,752 units / 604 entries / 140 nodes / 26 families / 21 unattached),
the declarable-witness type second witness (85/208 demoted), and the
```

---

## 8. Complete file inventory, this task

New files created by Task 46:

- `PRIVATE/PseudoCoupHQ/DevComms/next_commit_message.txt` (2,422
  bytes; overwritten, previously empty/absent content)
- `PRIVATE/PseudoCoupHQ/DevComms/log_139_task46_bank_round9.md`
  (this file)

Files read, not modified: `the_pool1.json`, `the_families1.json`,
`the_pool1_original_subset.py`, `check_no_spelling_keys.py`,
`dominant_table24.json`, `dominant_table24b.json`,
`dominant_table25.json`, `dom_ops22.json`, `dom_ops22b.json`,
`dom_ops23.json` (all under `Research/op_pipeline`), plus
`AgentMemory.md`, `LLM_communication_protocol.md`, and logs 134-138.

Also appended: a dated PROGRESS entry under the single `# PROGRESS`
heading in
`Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`
(see that file for the entry itself; not duplicated here).
