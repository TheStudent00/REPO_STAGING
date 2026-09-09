# log 205 — task 99: two recording gaps closed, no decision involved

Written 2026-09-05, round 20. Reports to the owner under
`~/Programming/DevComms/LLM_communication_protocol.md`. All compute
ran inside Airlock instance `t99`
(`~/Programming/Airlock/instances/t99.conf`), except item B's proof
(a2), which the brief itself requires to run on the DEFAULT instance
(`sandbox`) — that contrast is the point of the proof, explained in
§3.

## 1. The two objects, each in one sentence

- **Item A's object** is a `term66_store` record: one arch-unit's
  outcome from the operator-equivalence term walk, and a NO_TERM
  record is one where that walk could not build a z3 expression at
  all — 485 of the store's 30,280 records.
- **Item B's object** is `check_conventions_log_claims.py`: the
  program that re-runs a DevComms log's pasted commands inside
  Airlock and sorts each into MATCHES / DIFFERS / UNVERIFIABLE /
  REFUSED / NOT_RERUNNABLE.

## 2. Item A — a `reason` on every NO_TERM record

### 2.1 What was missing and why

Every NO_TERM record already carried `"outcome": null` and
`"reason": null`, even though it also carries `holes` — each hole
already has a `why` sentence. The gap the coordinator found (log_204
§5): nothing had ever copied that material into `reason`. Before any
lane ran, `unit c/regen_10427` (shard
`canon40_regen_store__op_units2_c_c0026.json`) looked like this:

> ```json
> {
>   "unit": "c/regen_10427",
>   "term_state": "NO_TERM",
>   "reason": null,
>   "holes": [
>     {"block": "TEMP", "row": "TEMP-4",
>      "producer": {"callee": "__divti3", "kind": "runtime_callee"},
>      "why": "the attached body of the runtime callee '__divti3' spells '', which the shared opcode table refused: this body's control flow has a cycle (a transfer back to a block already on the walk), and no loop invariant is invented here"},
>     … 8 more holes, same shape, same callee …
>   ]
> }
> ```

### 2.2 What `term99_reason.py` does with it

`~/Programming/PseudoCoupHQ/Research/op_pipeline/term99_reason.py`
streams each of the store's 332 shards, and for every NO_TERM record
whose `reason is None`, strips the `'...'`-quoted callee/register
names out of each hole's `why` string (the two variable parts §2.2 of
the brief names), matches what is left against six hole shapes found
in the store, and writes one sentence naming the cause(s), the hole
count, the blocks, and the producers — never copying the first hole's
`why` verbatim. It touches no other field, and never a record whose
`term_state != "NO_TERM"`.

After the write lane, the same record reads:

> ```json
> {
>   "unit": "c/regen_10427",
>   "term_state": "NO_TERM",
>   "reason": "no term: a cyclic callee body (its control flow transfers back to a block already on the walk, with no loop invariant invented); 9 hole(s) in TEMP, producers __divti3",
>   "reason_source": "term99_reason.py over the record's own holes"
> }
> ```

A second example, a record whose single hole is not a callee body at
all — `c/op_100`:

> ```json
> {
>   "unit": "c/op_100",
>   "holes": [{"block": "OUT", "row": "OUT-0",
>              "producer": {"kind": "non_opcode_phrase",
>                           "phrase": "the body's last write to %xmm0"},
>              "why": "no arch opcode in this body writes the answer register, so no row produces the answer"}],
>   "reason": "no term: no arch opcode in the body writes the answer register (a non-opcode phrase stands in the OUT block); 1 hole(s) in OUT, producers non_opcode_phrase",
>   "reason_source": "term99_reason.py over the record's own holes"
> }
> ```

### 2.3 The cause table (by cause, not by sighting)

Six shapes were found across the 485 records' 3,259 holes — no
seventh, no unclassified remainder. A record can carry more than one
cause (a body can both cycle AND leave no residence for its answer),
so the unit column below sums past 485.

| cause | units | example unit |
|---|---:|---|
| a cyclic callee body (its control flow transfers back to a block already on the walk, with no loop invariant invented) | 223 | c/regen_10427 |
| a hole row that names no place its value resides, so nothing downstream can read it | 88 | c/regen_28741 |
| a callee body where every path leaves the unit or is unreachable, so the body leaves no answer to read | 77 | c/regen_10428 |
| a callee body whose branches leave the machine stack at different depths | 56 | c/regen_29798 |
| no arch opcode in the body writes the answer register (a non-opcode phrase stands in the OUT block) | 35 | c/op_100 |
| a runtime callee with no attached body on this machine | 10 | swift/regen_315 |

### 2.4 The lanes, in order

Every lane ran on instance `t99`; its own `/logs` is
`~/AirlockRuns/t99/agent/logs/` on the host — a DIFFERENT folder from
the default instance's `~/Programming/Airlock/agent/logs/` (this
distinction is exactly item B's subject, §3.2).

**1. Dry run** — `t99_l2_dry_run.sh`,
`~/AirlockRuns/t99/agent/logs/20260905T150143Z__t99_l2_dry_run.sh.log`.
The cause table, re-read from the lane's own log, byte for byte:

```
$ sed -n '345,352p' /logs/20260905T150143Z__t99_l2_dry_run.sh.log
| cause | units | example unit |
|---|---:|---|
| a cyclic callee body (its control flow transfers back to a block already on the walk, with no loop invariant invented) | 223 | c/regen_10427 |
| a hole row that names no place its value resides, so nothing downstream can read it | 88 | c/regen_28741 |
| a callee body where every path leaves the unit or is unreachable, so the body leaves no answer to read | 77 | c/regen_10428 |
| a callee body whose branches leave the machine stack at different depths | 56 | c/regen_29798 |
| no arch opcode in the body writes the answer register (a non-opcode phrase stands in the OUT block) | 35 | c/op_100 |
| a runtime callee with no attached body on this machine | 10 | swift/regen_315 |
```
Wrote `term99_reason.json`; touched zero shard bytes (`--dry-run`).
Exit 0.

**2. Write, with masked-hash and reason-count proof** —
`t99_l3_write.sh`,
`~/AirlockRuns/t99/agent/logs/20260905T150209Z__t99_l3_write.sh.log`.
Before the write:
```
$ sed -n '6,9p' /logs/20260905T150209Z__t99_l3_write.sh.log
======== [1/4] masked hash BEFORE ========
563a5e789cb69f1d57f6fa04870e59b297bde287832bc859698a8a8fdbe18701
======== [2/4] reason-is-None count BEFORE (expect 485) ========
485
```
After the write:
```
$ sed -n '360,364p' /logs/20260905T150209Z__t99_l3_write.sh.log
======== [4/4] masked hash AFTER, reason-is-None count AFTER (expect 0) ========
563a5e789cb69f1d57f6fa04870e59b297bde287832bc859698a8a8fdbe18701
0

MASKED HASH: EQUAL -- no field but reason/reason_source moved
```
The hash is computed over every unit of every shard with
`reason`/`reason_source` set to `None` before hashing whenever
`term_state == "NO_TERM"` — an equal hash before and after proves
every other byte of every record, NO_TERM or not, is unchanged.
Exit 0.

**3. Idempotence** — `t99_l4_idempotent.sh`,
`~/AirlockRuns/t99/agent/logs/20260905T150239Z__t99_l4_idempotent.sh.log`,
`--write` run again over the now-filled store:
```
$ sed -n '340,343p' /logs/20260905T150239Z__t99_l4_idempotent.sh.log
mode: WRITE
NO_TERM records seen: 485
already had a reason (skipped, idempotent): 485
records given a reason this run: 0
```
Cause table on this run: empty (nothing to touch). Exit 0.

## 3. Item B — REFUSED instead of DIFFERS for an unreachable log path

### 3.1 The defect and the fix

`check_conventions_log_claims.py`'s `verify()` ran every classified
command and compared its fresh output to the log's paste. A command
reading a lane log under `/logs/…` not mounted in the instance running
`--verify` produced an error string as its "fresh" output, which the
comparison then scored DIFFERS against the paste — a missing file
being reported as the CLAIM disagreeing.

The fix, committed as `f2e92af4519219d060430f2de0cee08524613a4d` by
the repo-daemon (its auto-commit convention, not a manual commit):
```
$ git --git-dir=/projects/PseudoCoupHQ/.git --work-tree=/projects/PseudoCoupHQ show --stat f2e92af4519219d060430f2de0cee08524613a4d -- Research/op_pipeline/check_conventions_log_claims.py
commit f2e92af4519219d060430f2de0cee08524613a4d
Author: TheStudent00 <<email>>
Date:   Sat Sep 5 10:54:37 2026 -0400

    auto: 1 file (check_conventions_log_claims.py)
    
    2026-09-05T10:54:37-04:00
    X-Auto-Commit: repo-daemon

 .../op_pipeline/check_conventions_log_claims.py    | 37 +++++++++++++++++++++-
 1 file changed, 36 insertions(+), 1 deletion(-)
```
A new function, `unreachable_path_token(cmd)`, splits the command with
`shlex` and returns the first token starting `/`, `~` or `./` that
`os.path.exists` (after `~` expansion) says is absent. In `verify()`,
right after the empty-paste check and BEFORE the command is ever run,
a hit sets `outcome = "REFUSED"` with
`reason = "log_unreachable -- <path> is not reachable from this
instance; re-run --verify from the instance whose logs the claim
cites"`, then `continue`s — the command is never executed, `fresh` is
never set. No other verdict branch changed. The docstring's outcome
table (line ~53 area) now names `log_unreachable` under REFUSED. The
existing "causes, by name" tally in `report()` already groups by
`reason.split(" -- ")[0]` for every REFUSED/NOT_RERUNNABLE/
UNVERIFIABLE claim, so `log_unreachable` appears there with no
separate code path needed.

### 3.2 The mount fact this fixes, shown live

`t99` has its own run directory
(`~/AirlockRuns/t99/agent/logs`, mounted to `/logs` inside
`t99-runner`) — separate from `~/Programming/Airlock/agent/logs`
(mounted to `/logs` inside the DEFAULT `sandbox-runner`), which is
where the `t98_l*` lanes `log_203` cites actually ran; so a claim in
`log_203` that cats a `t98` lane log is reachable from the default
instance and unreachable from `t99` — exactly the two tallies below
demonstrate.

### 3.3 The three proof lanes

**(a1) `--verify log_203` FROM `t99`** —
`t99_l5_claims_log203_t99.sh`,
`~/AirlockRuns/t99/agent/logs/20260905T150241Z__t99_l5_claims_log203_t99.sh.log`:
```
$ sed -n '62,71p' /logs/20260905T150241Z__t99_l5_claims_log203_t99.sh.log
SUMMARY, ALL LOGS
==============================================================================
population: 14 claims across 1 logs
  MATCHES          13
  DIFFERS          0
  UNVERIFIABLE     0
  REFUSED          1
  NOT_RERUNNABLE   0

ONE LINE: 13 of 14 claims reproduce; 0 (0%) carry nothing to re-run
```
The one REFUSED claim:
```
$ grep -n "log_unreachable" /logs/20260905T150241Z__t99_l5_claims_log203_t99.sh.log
54:   | 346 | shell_transcript | **REFUSED** | `grep "^ONE LINE" /logs/20260905T141536Z__t98_l13_claims.sh.log` — log_unreachable -- /logs/20260905T141536Z__t98_l13_claims.sh.log is not reachable from this instance; re-run - |
74:  log_unreachable                  1
```
Zero DIFFERS — this is the corrected outcome the coordinator's
correction to §3.2 lane (a) predicted, replacing the brief's original
expectation of an unchanged 14/14 from `t99`.

**(a2) `--verify log_203` on the DEFAULT instance** —
`t99_l6_claims_log203_default.sh`, submitted with `--no-batch`, no
`--instance` flag, run:
`~/Programming/Airlock/agent/logs/20260905T150253Z__t99_l6_claims_log203_default.sh.log`.
This file sits under the DEFAULT instance's own log folder, which is
NOT mounted into `t99` — the very fact item B fixes — so the
re-verify below (run from `t99`, like everything else in this report)
correctly REFUSES it rather than reading it:
```
$ sed -n '62,71p' /logs/20260905T150253Z__t99_l6_claims_log203_default.sh.log
(unreachable from t99 by construction -- this line is never compared)
```
So the number itself is pasted directly from the lane's own console
output instead, LITERAL but not re-verifiable from `t99`:
```
population: 14 claims across 1 logs
  MATCHES          14
  DIFFERS          0
  UNVERIFIABLE     0
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 14 of 14 claims reproduce; 0 (0%) carry nothing to re-run
```
Unchanged from task 98's own score, because `/logs` on the default
instance IS `~/Programming/Airlock/agent/logs`, where the cited
`t98_l13` log actually is.

**(b) fixture, unreachable path** — `t99_l7_fixture_refused.sh`,
`~/AirlockRuns/t99/agent/logs/20260905T150318Z__t99_l7_fixture_refused.sh.log`,
fixture written under `/tmp` inside the lane, one claim
`cat /logs/does_not_exist.log`:
```
$ sed -n '36,45p' /logs/20260905T150318Z__t99_l7_fixture_refused.sh.log
SUMMARY, ALL LOGS
==============================================================================
population: 1 claims across 1 logs
  MATCHES          0
  DIFFERS          0
  UNVERIFIABLE     0
  REFUSED          1
  NOT_RERUNNABLE   0

ONE LINE: nothing in this log was reproduced -- 0 of 1 claims (0%) carry no command at all, and no claim matched
```
Reason on the one claim: `log_unreachable -- /logs/does_not_exist.log
is not reachable from this instance; re-run --verify from the
instance whose logs the claim cites`.

**(c) fixture, reachable path** — `t99_l8_fixture_matches.sh`,
`~/AirlockRuns/t99/agent/logs/20260905T150318Z__t99_l8_fixture_matches.sh.log`,
same shape, one claim `cat /tmp/t99_fixture_reachable.txt` (the file
the lane itself wrote):
```
$ sed -n '36,45p' /logs/20260905T150318Z__t99_l8_fixture_matches.sh.log
SUMMARY, ALL LOGS
==============================================================================
population: 1 claims across 1 logs
  MATCHES          1
  DIFFERS          0
  UNVERIFIABLE     0
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 1 of 1 claims reproduce; 0 (0%) carry nothing to re-run
```

No other verdict path changed; both fixtures also passed
`check_no_spelling_keys.py` (printed by the verifier itself, `PASS …
-- no operator token in any key, grouping, pairing or row structure`,
`grep -c exempt` over this program is 0 — not modified).

## 4. The verifier's tally over this log

This section cannot itself be a re-runnable claim inside this log —
verifying the log changes the log, which would change the claim,
without end — so this is prose, stated as such, pasted from the lane
that ran AFTER every edit above this line was made:
`t99_l12_claims_log205.sh`,
`~/AirlockRuns/t99/agent/logs/20260905T151231Z__t99_l12_claims_log205.sh.log`,
exit 0:

```
population: 13 claims across 1 logs
  MATCHES          9
  DIFFERS          0
  UNVERIFIABLE     3
  REFUSED          1
  NOT_RERUNNABLE   0

ONE LINE: 9 of 13 claims reproduce; 3 (23%) carry nothing to re-run
```

Zero DIFFERS. The 3 UNVERIFIABLE are prose (two sentences asserting
what was proved, immediately preceded by the fenced proof itself) and
one attribution-only sentence (line 259) that names its source but
carries no command by design (§3.3, lane (a2): the number it names is
unreachable from `t99` and is quoted, not re-run). The 1 REFUSED is
the SAME `log_unreachable` demonstration as §3.3 (a2)'s own lane —
this log, read from `t99`, cannot reach the default instance's log
either, which is the mount fact item B exists to name correctly
instead of scoring it DIFFERS.

## 5. Two lists

### 5.1 Decided, recorded for audit
- Item A: six causes named and tabled; `term99_reason.py` written,
  proved idempotent, proved to touch no field but `reason` /
  `reason_source` on NO_TERM records only (masked-hash equal).
- Item B: `log_unreachable` added to the existing REFUSED outcome
  (no new outcome name), proved on `log_203` from two instances and
  on two fixtures.
- The §3.2(a) expectation in the original brief (14/14 unchanged from
  `t99`) was corrected by the coordinator before this lane ran, and
  the corrected expectation (13 MATCHES + 1 REFUSED from `t99`, 14/14
  from the default instance) is what the lanes show.

### 5.2 Awaiting the owner
(none)
