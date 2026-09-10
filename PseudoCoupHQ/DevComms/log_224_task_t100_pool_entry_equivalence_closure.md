# log_224 — task t100: solver equivalence between pool5 entries, closed on the pair lane's own budget (master plan step 2)

Node: `hq.research.operator_equivalence.pool`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_7_pool/CORE_0_3_1_7_pool.md`).
Master plan: `CORE_0_3_research` §4.2 step 2. Prior record: this task's
pair lane ran across three windows in an earlier session
(`t100_l4_pairs.sh`, `t100_l5_pairs_resume.sh`,
`t100_l7_pairs_resume3.sh`; `t100_l6_pairs_resume2.sh` was a no-op —
its slice files were already `finished: true`) and the third window
ended on its own stated budget with the six slice files at 21,502 of
43,410 pairs answered. This session runs the closing step only —
`pool100_entry_equivalence.py close`, already written and unchanged —
over that state: no new pair is solved here (the closing note names
this explicitly; the pair lane's own budget, not this session, is why
83 of 88 groups are partial).

**What happened, one sentence:** `pool100_entry_equivalence.py close`
ran clean in one lane (5.1 s, exit 0), built the per-group coverage
table, closed the 12 PROVED-and-applied edges under transitivity over
pool5's 1,831 entries into a 1,819-entry CANDIDATE
(`pool100_pool6_candidate.json`, not `the_pool6.json`), wrote
`pool100_edges.json` and `pool100_report.md`, and the spelling guard
passed all 11 files it wrote.

---

## 1. What the objects are

- **entry**: one distinct computation in `the_pool5.json` (1,831
  entries over 30,432 members); it carries `type_key` (arrival
  register families | answer width; 88 distinct), `members`, and
  `representative` (the member with the fewest assembled bytes).
- **term**: a unit's computation as a z3 expression, built from its
  canon40 record by `term.Term.transcribe` — the same function
  `term66_run.one_unit` calls; nothing new was written to build it.
- **pair**: two entries of one `type_key` — the machine-form candidate
  set (arrival register families | answer width), never the operator
  token. `pool100_plan.json` fixed all 43,410 pairs, across 88
  groups, before any solver ran.
- **edge**: a pair the gate's own solver call (`gate.Gate.decide`,
  `SOLVER_MILLISECONDS = 3000`, never raised) PROVED equal (unsat on
  the negation), APPLIED to the closure only when both terms were
  separately proved against their own unit's ship body.
- **the pool6 CANDIDATE**: pool5's 1,831 entries closed under the
  applied edges by transitivity — a candidate for the owner to ratify,
  never written as `the_pool6.json`.

## 2. The instance and its lane history

```
$ python3 PUBLIC/Airlock/airlock status --instance t100
```

| lane | state | exit | elapsed | progress |
|---|---|---|---|---|
| t100_l8_close.sh | done | 0 | 5.1s | [3/3] |
| t100_l7_pairs_resume3.sh | done | 0 | 14512.9s | [406/475] |
| t100_l6_pairs_resume2.sh | done | 0 | 1.2s | - |
| t100_l5_pairs_resume.sh | done | 0 | 14494.1s | [75/475] |
| t100_l4_pairs.sh | done | -15 | 4557.7s | - |
| t100_l3_sample_by_row.sh | done | 0 | 5.2s | [200/200] |
| t100_l2_sample.sh | done | 0 | 1.2s | [60/60] |
| t100_l1_plan.sh | done | 0 | 3.2s | [332/332] |

`t100_l1_plan.sh` through `t100_l7_pairs_resume3.sh` are the earlier
session's (its own logs, not reproduced here — the state they left is
read directly, below). `t100_l8_close.sh` is this session's one lane:
it prints the six slice files' state, runs `close`, and lists the
three files `close` wrote. Its full log, LITERAL, in full:

```
# script: /drop/t100_l8_close.sh
# started: 2026-09-06T20:08:03+00:00
# timeout: 21600s
# work free before: 4096 MB
------------------------------------------------------------
[1/3] pre-close state: six slice files
  slice0: answered 3983 of 7235, finished True, stopped_by_budget True
  slice1: answered 3724 of 7235, finished True, stopped_by_budget True
  slice2: answered 3297 of 7235, finished True, stopped_by_budget True
  slice3: answered 3868 of 7235, finished True, stopped_by_budget True
  slice4: answered 3345 of 7235, finished True, stopped_by_budget True
  slice5: answered 3285 of 7235, finished True, stopped_by_budget True
  total answered 21502 of 43410
[2/3] running close
-- CLOSE
   pair records 21502 (retry superseded 0)
   groups complete 5 of 88
   edges applied 12, proved but not applied (a term unproved against its own body) 214
   entries before 1831, after 1819
-- wrote pool100_pool6_candidate.json
-- wrote pool100_edges.json
{
 "disproved_whose_counterexample_assigns_a_constant_pool_symbol": 2279,
 "edges_applied": 12,
 "entries_after": 1819,
 "entries_before": 1831,
 "groups_complete": 5,
 "groups_total": 88,
 "pairs_answered": 21502,
 "pairs_total": 43410,
 "proved_but_not_applied": 214,
 "states": {
  "DISPROVED": 19640,
  "PROVED": 226,
  "UNBUILDABLE": 537,
  "UNDECIDED": 1099
 },
 "the_44": {
  "entries": 18,
  "entries_alone_in_their_group": 0,
  "entries_in_a_complete_group": 0,
  "entries_with_a_pair_answered": 2,
  "units": 44
 },
 "unbuildable_by_cause": {
  "NO_TERM -- the attached body of the runtime callee '__floatuntidf' spells '', which the shared opcode": 258,
  "NO_TERM -- the attached body of the runtime callee '__floatuntisf' spells '', which the shared opcode": 264,
  "NO_TERM -- the attached body of the runtime callee '__floatuntidf' spells '', which the shared opcode / the attached body of the runtime callee '__floatuntisf' spells '', which the shared opcode": 15
 },
 "undecided_by_cause": {
  "runner limit: TIMED_OUT": 1099
 },
 "undecided_that_would_be_retried_at_120000_ms": 0
}
-- wrote pool100_report.md
-- the spelling guard, unmodified, over 11 files
   operator inventory: 91 tokens read from probe_manifest_*.json
   PASS pool100_plan.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_representatives.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_edges.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_pool6_candidate.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_sample.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_pairs_slice0.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_pairs_slice1.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_pairs_slice2.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_pairs_slice3.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_pairs_slice4.json -- no operator token in any key, grouping, pairing or row structure
   PASS pool100_pairs_slice5.json -- no operator token in any key, grouping, pairing or row structure
-- guard exit 0
[3/3] close finished, files on disk:
-rw-r--r-- 1 root root 67440169 Sep  6 20:08 pool100_edges.json
-rw-r--r-- 1 root root 30655778 Sep  6 20:08 pool100_pool6_candidate.json
-rw-r--r-- 1 root root    13115 Sep  6 20:08 pool100_report.md
------------------------------------------------------------
# exit 0 in 5.1s
# work free after: 4096 MB (consumed 0 MB)
```

**GLOSS.** `close` reads the six slice files and (if present — none
here) `pool100_pairs_retry.json`, needs no z3 context of its own (all
solving happened in the pair lane), and is one process: hence one
worker, 5.1 s, and no memory note beyond what the lane header prints.

## 3. Coverage: 5 of 88 groups complete, the 20 largest groups + total

**LITERAL**, `pool100_report.md` §1 (this session's own generated
file, read back unmodified):

| rank | type_key | entries before | pairs | answered | complete | PROVED | DISPROVED | UNDECIDED | UNBUILDABLE | edges applied | entries after |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `rdi,rsi\|32` | 102 | 5151 | 5151 | yes | 39 | 5112 | 0 | 0 | 0 | 102 |
| 2 | `rdi,rsi\|8` | 94 | 4371 | 4371 | yes | 18 | 4353 | 0 | 0 | 2 | 92 |
| 3 | `rdi,rsi,rcx\|8` | 92 | 4186 | 4186 | yes | 8 | 4178 | 0 | 0 | 8 | 84 |
| 4 | `rcx,xmm0,xmm1\|32` | 85 | 3570 | 3570 | yes | 93 | 3111 | 366 | 0 | 0 | 85 |
| 5 | `rcx,xmm0\|32` | 76 | 2850 | 2714 | NO | 11 | 1477 | 689 | 537 | 1 | 75 |
| 6 | `xmm0,xmm1\|8` | 67 | 2211 | 1105 | NO | 45 | 1060 | 0 | 0 | 1 | 66 |
| 7 | `rcx,xmm0,xmm1\|8` | 62 | 1891 | 405 | NO | 12 | 349 | 44 | 0 | 0 | 62 |
| 8 | `rdi,rsi,rdx\|32` | 61 | 1830 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 61 |
| 9 | `rdi,rsi\|64` | 60 | 1770 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 60 |
| 10 | `rdi,rsi,rdx\|64` | 59 | 1711 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 59 |
| 11 | `xmm0\|8` | 58 | 1653 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 58 |
| 12 | `rcx,xmm0\|8` | 50 | 1225 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 50 |
| 13 | `rdi,rcx,xmm0,xmm1\|32` | 50 | 1225 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 50 |
| 14 | `rdi,rsi,rdx\|8` | 43 | 903 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 43 |
| 15 | `rdi,xmm0,xmm1\|32` | 42 | 861 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 42 |
| 16 | `rdi,rcx,xmm0,xmm1\|8` | 36 | 630 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 36 |
| 17 | `rdi,xmm0\|8` | 36 | 630 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 36 |
| 18 | `xmm0,xmm1\|32` | 36 | 630 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 36 |
| 19 | `rdi,xmm0\|32` | 34 | 561 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 34 |
| 20 | `xmm0\|32` | 34 | 561 | 0 | NO | 0 | 0 | 0 | 0 | 0 | 34 |
| total | 88 type keys | 1831 | 43410 | 21502 | 5 of 88 | 226 | 19640 | 1099 | 537 | 12 | 1819 |

**GLOSS.** All 5 complete groups, by rank, read from
`pool100_edges.json`'s `groups` rows:

```
$ python3 -c "
import json
d = json.load(open('Research/op_pipeline/pool100_edges.json'))
for r in sorted((r for r in d['groups'] if r['complete']), key=lambda r: r['rank']):
    print(r['rank'], r['type_key'], r['pairs'], r['pairs_answered'])
"
1 rdi,rsi|32 5151 5151
2 rdi,rsi|8 4371 4371
3 rdi,rsi,rcx|8 4186 4186
4 rcx,xmm0,xmm1|32 3570 3570
88 rbx|32 0 0
```

Ranks 1–4 are the pair lane's four largest groups, run in full before
the budget ran out (§1 above). Rank 88, `rbx|32`, is complete
trivially: 0 pairs (a `type_key` with exactly one pool5 entry, so no
unordered pair exists to run). Partial: the other 83 of 88, listed
exhaustively in `pool100_report.md` §1's "Groups NOT complete" list;
61 of those 83 have 0 pairs answered at all — the pair lane's budget
ran out before reaching them, in the fixed largest-first order
`pool100_plan.json` set before any solver ran.

## 4. The three largest merges

**LITERAL**, `pool100_report.md` §2 (all three; the file has no
fourth):

### C00170 — 2 pool5 entries, 264 members, type_key `rdi,rsi|8`, representative `cpp/op_509` (40 bytes)

| pool5 entry | members | languages | representative | layer-5 texts in pool5 (LITERAL) |
|---|---|---|---|---|
| E00170 | 240 | c,cpp | `cpp/op_509` | `If(v0 == Concat(0, Extract(31, 0, v1)), 0, 1)` |
| E01654 | 24 | swift | `swift/regen_1023` | `If(Concat(0, Extract(31, 0, v0)) == v1, 0, 1)` |

Why text identity missed them (GLOSS, computed by `close`): ground two
joins on STRING IDENTITY of the layer-5 text, and these two entries
print different texts for terms the solver proves equal for every
input — the normalizer is a fixed rewrite rule (simplify, order
commutative arguments, rename positionally), not a decision
procedure, so two equal terms may print differently.

Edge: `E00170` (cpp/op_509) == `E01654` (swift/regen_1023):
PROVED_ON_SHIP; inputs IN-0=IN_0, IN-1=IN_1; answer width 8; own
verdicts PROVED_ON_SHIP / PROVED_ON_SHIP; timeout 3000 ms.

### C00156 — 2 pool5 entries, 176 members, type_key `rdi,rsi|8`, representative `cpp/op_473` (40 bytes)

| pool5 entry | members | languages | representative | layer-5 texts in pool5 (LITERAL) |
|---|---|---|---|---|
| E00156 | 152 | c,cpp | `cpp/op_473` | `If(v0 == Concat(0, Extract(31, 0, v1)), 1, 0)` |
| E01664 | 24 | swift | `swift/regen_1413` | `If(Concat(0, Extract(31, 0, v0)) == v1, 1, 0)` |

Same reason as C00170 (GLOSS): different printed layer-5 text, terms
proved equal for every input.

Edge: `E00156` (cpp/op_473) == `E01664` (swift/regen_1413):
PROVED_ON_SHIP; inputs IN-0=IN_0, IN-1=IN_1; answer width 8; own
verdicts PROVED_ON_SHIP / PROVED_ON_SHIP; timeout 3000 ms.

### C00338 — 2 pool5 entries, 10 members, type_key `rdi,rsi,rcx|8`, representative `swift/op_446` (259 bytes)

| pool5 entry | members | languages | representative | layer-5 texts in pool5 (LITERAL) |
|---|---|---|---|---|
| E00338 | 5 | swift | `swift/op_446` | `If(v0 == v1, 0, 1) \| If(0 <= v0, 0, 1)` |
| E00339 | 5 | swift | `swift/op_451` | `If(v0 == v1, 0, 1) \| If(0 <= v1, 0, 1)` |

Same reason (GLOSS): different printed layer-5 text (the two texts
differ only in which operand feeds the second `If`, `v0` vs `v1`),
terms proved equal for every input.

Edge: `E00338` (swift/op_446) == `E00339` (swift/op_451):
PROVED_ON_SHIP; inputs IN-0=IN_0, IN-1=IN_1, IN-2=IN_2; answer width
8; own verdicts PROVED_ON_SHIP / PROVED_ON_SHIP; timeout 3000 ms.

All 12 applied edges join exactly one pair of pool5 entries each (no
edge chains through a third entry), so the candidate's 12 merges are
all size 2 — `pool100_pool6_candidate.json`'s own `summary.merged_entries`
is 12, matching `edges_applied` 12, confirmed directly:

```
$ python3 -c "
import json
d = json.load(open('Research/op_pipeline/pool100_pool6_candidate.json'))
print('summary', d['summary'])
merges = [e for e in d['entries'] if e['merged_entry_count'] != 1]
print('num merges', len(merges))
print(sorted((e['merged_entry_count'], e['member_count'], e['entry_id']) for e in merges))
"
summary {'edges_applied': 12, 'entries_after': 1819, 'entries_before': 1831, 'groups_complete': 5, 'groups_total': 88, 'merged_entries': 12}
num merges 12
[(2, 2, 'C01442'), (2, 2, 'C01649'), (2, 2, 'C01653'), (2, 2, 'C01654'), (2, 2, 'C01657'), (2, 2, 'C01659'), (2, 2, 'C01663'), (2, 4, 'C00918'), (2, 10, 'C00338'), (2, 10, 'C00340'), (2, 176, 'C00156'), (2, 264, 'C00170')]
```

## 5. Three DISPROVED pairs, counterexample seeds

**LITERAL**, `pool100_report.md` §3, all three (the report picks
those whose smaller entry has the most members; it does not pick
pairs with a constant-pool-symbol counterexample, reported separately
in §6 below):

### `E00073` (`go/op_240`) against `E00125` (`go/op_384`), type_key `rdi,rsi|32`
- layer-5 texts: a = `~(~Extract(31, 0, v0) | ~Extract(31, 0, v1))`;
  b = `Extract(31, 0, v0) | Extract(31, 0, v1)`
- gate's reason: `z3 found a starting state under which the two sides differ`
- solver's model: `[IN_0 = 2147483648, IN_1 = 0]`

### `E00073` (`go/op_240`) against `E00143` (`go/op_420`), type_key `rdi,rsi|32`
- layer-5 texts: a = `~(~Extract(31, 0, v0) | ~Extract(31, 0, v1))`;
  b = `Extract(31, 0, v0) ^ Extract(31, 0, v1)`
- gate's reason: `z3 found a starting state under which the two sides differ`
- solver's model: `[IN_0 = 4294967295, IN_1 = 0]`

### `E00125` (`go/op_384`) against `E00143` (`go/op_420`), type_key `rdi,rsi|32`
- layer-5 texts: a = `Extract(31, 0, v0) | Extract(31, 0, v1)`;
  b = `Extract(31, 0, v0) ^ Extract(31, 0, v1)`
- gate's reason: `z3 found a starting state under which the two sides differ`
- solver's model: `[IN_0 = 2147483648, IN_1 = 2147483648]`

## 6. UNDECIDED and UNBUILDABLE by cause

**LITERAL**, `pool100_report.md` §4:

| state | cause | pairs |
|---|---|---|
| UNDECIDED | `runner limit: TIMED_OUT` | 1099 |
| UNBUILDABLE | `NO_TERM -- the attached body of the runtime callee '__floatuntisf' spells '', which the shared opcode` | 264 |
| UNBUILDABLE | `NO_TERM -- the attached body of the runtime callee '__floatuntidf' spells '', which the shared opcode` | 258 |
| UNBUILDABLE | `NO_TERM -- the attached body of the runtime callee '__floatuntidf' spells '', which the shared opcode / the attached body of the runtime callee '__floatuntisf' spells '', which the shared opcode` | 15 |

- UNDECIDED that would be retried at 120,000 ms (NOT retried; the
  ceiling is the owner's, log_204 §4.3): **0** — every one of the 1,099
  UNDECIDED pairs was stopped by the pair lane's own 120 s
  sub-process runner limit (`runner limit: TIMED_OUT`), not by the
  gate's 3,000 ms solver returning `unknown`; none carries the "did
  not answer inside its 3000 ms limit" cause the 120,000 ms question
  is about.
- DISPROVED whose counterexample assigns a constant-pool symbol
  (recorded separately from the three plain DISPROVED pairs in §5):
  **2279**.
- PROVED but NOT applied (one term not proved against its own ship
  body): **214**.

## 7. The 44 non-converging units

Their entries take part like any other entry — this merge proves term
against term and needs no layer-5 key (brief §3, stop rule 2).
**LITERAL**, `pool100_report.md` §5: units 44; pool5 entries holding
them 18; of those, in a group whose every pair was answered: **0**;
with at least one pair answered: **2** (`E01438`, `E01460`, both
`rcx,xmm0|32`, that group's 2,714-of-2,850 partial coverage); alone in
their group: **0**. The other 16 entries sit in `xmm0|32` (8 entries,
0 of 561 pairs answered) and `xmm0|8` (8 entries, 0 of 1,653 pairs
answered) — both groups the pair lane's budget never reached.

## 8. The tally

**LITERAL**, `pool100_report.md` §6: pairs total 43410; answered
21502; states `{"DISPROVED": 19640, "PROVED": 226, "UNBUILDABLE": 537,
"UNDECIDED": 1099}`; edges applied 12; entries 1831 -> 1819; groups
complete 5 of 88.

## 9. The spelling-ban guard, pasted verbatim as required

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

`close` ran `check_no_spelling_keys.py`, unmodified, over the 11 files
it wrote or depends on (§2's lane log above): 11 PASS, 0 FAIL, exit 0.
`grep -c exempt` over every file this task added, run on the host:

```
$ grep -c exempt Research/op_pipeline/pool100_edges.json Research/op_pipeline/pool100_pool6_candidate.json Research/op_pipeline/pool100_plan.json Research/op_pipeline/pool100_representatives.json Research/op_pipeline/pool100_sample.json Research/op_pipeline/pool100_pairs_slice0.json Research/op_pipeline/pool100_pairs_slice1.json Research/op_pipeline/pool100_pairs_slice2.json Research/op_pipeline/pool100_pairs_slice3.json Research/op_pipeline/pool100_pairs_slice4.json Research/op_pipeline/pool100_pairs_slice5.json Research/op_pipeline/pool100_entry_equivalence.py
Research/op_pipeline/pool100_edges.json:0
Research/op_pipeline/pool100_pool6_candidate.json:0
Research/op_pipeline/pool100_plan.json:0
Research/op_pipeline/pool100_representatives.json:0
Research/op_pipeline/pool100_sample.json:0
Research/op_pipeline/pool100_pairs_slice0.json:0
Research/op_pipeline/pool100_pairs_slice1.json:0
Research/op_pipeline/pool100_pairs_slice2.json:0
Research/op_pipeline/pool100_pairs_slice3.json:0
Research/op_pipeline/pool100_pairs_slice4.json:0
Research/op_pipeline/pool100_pairs_slice5.json:0
Research/op_pipeline/pool100_entry_equivalence.py:0
```

## 10. What was NOT done, by the brief's own stop rules

- `the_pool5.json` and `the_families5.json` were not touched;
  `the_pool6.json` was not written — `pool100_pool6_candidate.json`
  is a candidate for the owner to ratify.
- The solver ceiling stayed 3,000 ms throughout; no pair was retried
  at a higher ceiling (§6 above: 0 UNDECIDED pairs would even qualify
  — all 1,099 were stopped by the runner's 120 s sub-process limit,
  a different ceiling from the solver's).
- No new pair was solved in this session: the pair lane's own three
  windows (an earlier session) are the entire source of the 21,502
  answered pairs; this session only closed over them.

## 11. Two lists

**Decided, recorded for audit:**
- The closing note's instruction to work from the pair lane's state
  as it stood (three windows, budget-stopped, 21,502 of 43,410
  answered) rather than run a fourth window, per `close_t100.md`'s
  own item list (no pairs step listed).
- `close()`'s own edge-application rule (a PROVED pair applies to the
  closure only when both terms are separately proved against their
  own ship body) — pre-existing code, read and reused, not changed.

**Awaiting the owner:**
- Ratification of `pool100_pool6_candidate.json` (12 merges, 1,819
  entries) into `the_pool6.json`.
- Whether the remaining 83 partial/untouched groups (61 of them at 0
  pairs answered, §3) get a further pair-lane window before or after
  ratification — this session did not run one, per the closing note.

## 12. Verifier tally

Three passes, same shape prior closing logs used (log_215 §"second
pass", log_217 §7): pass 1 (`t100_l9_verify.sh`) found 0 DIFFERS but 1
REFUSED (a `> 1` inside a `python3 -c` snippet in §4, misread by the
checker's redirect scanner as a shell write into a file named `1]` —
the same `redirects_into_a_path` shape log_217 §7 hit); changed to the
equivalent `!= 1` (merge count is never 0, so `!= 1` means the same
thing as `> 1`), no logic changed. Pass 2 (`t100_l10_verify2.sh`) then
found 1 DIFFERS on that same §4 snippet — not from the `!= 1` change,
but from a transcription bug this session's own drafting introduced: a
stray trailing `"` on its own line after the real output, a second
copy of the command's closing quote pasted where no output line
belongs. Removed. Pass 3, LITERAL, in full:

```
$ python3 PUBLIC/Airlock/airlock submit <scratch>/t100_l11_verify3.sh --instance t100 --batch t100 --weight 1
```

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_224_task_t100_pool_entry_equivalence_closure.md
log_224_task_t100_pool_entry_equivalence_closure.md: 15 claims extracted
   claims 15 | MATCHES 3 | DIFFERS 0 | UNVERIFIABLE 10 | REFUSED 1 | NOT_RERUNNABLE 1
   VERDICT: 3 of 15 claims reproduce; 10 (67%) carry nothing to re-run
population: 15 claims across 1 logs
  MATCHES          3
  DIFFERS          0
  UNVERIFIABLE     10
  REFUSED          1
  NOT_RERUNNABLE   1
causes, by name:
  prose_only                       9
  out_of_sandbox                   1
  attribution_only                 1
  submits_or_moves_the_sandbox     1
check_conventions_log_claims.py exit 0
```

**TALLY LINE: claims 15 | MATCHES 3 | DIFFERS 0 | UNVERIFIABLE 10 |
REFUSED 1 | NOT_RERUNNABLE 1. Zero DIFFERS.** The 3 MATCHES are §3's
and §4's `python3 -c` snippets plus §9's `grep -c exempt`; the
NOT_RERUNNABLE is this log's own `airlock status --instance t100`
call in §2 (`PUBLIC/Airlock` is not an Airlock-mounted path,
the same `out_of_sandbox` shape log_217 §7 recorded); the REFUSED is
this section's own `airlock submit` call for this verifier lane itself
(`submits_or_moves_the_sandbox`, by design — the checker never
re-issues a submit); the 10 UNVERIFIABLE are prose/GLOSS sentences and
one attribution citing a lane log by name with no fresh command beside
it (those lane logs are quoted LITERAL in §2 directly, not re-run as a
claim of their own).

## 13. See also

- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/pool100_entry_equivalence.py`
  — the program (`close` mode used this session; unchanged).
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/pool100_report.md`
  — the narrative deliverable, full 88-row coverage table.
- `PRIVATE/PseudoCoupHQ/Research/op_pipeline/pool100_edges.json`,
  `pool100_pool6_candidate.json` — the two artifacts this session
  wrote.
- `<scratch>/close_t100.md`
  — the closing note this session worked from.
- `PRIVATE/PseudoCoupHQ/DevComms/log_217_task_t101b_dominant_types_join.md`
  — the closing-task log this one's shape follows.
