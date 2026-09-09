# log 091 — task briefs for Claude Code, round 2

Date: 2026-08-31. Written after the verification audit of round 1
(log_083's seven tasks, logs 084-090). Same handoff shape: point
a Claude Code session here.

STATE AT HANDOFF, audited and recomputed rather than taken from
the round-1 logs:

- converged 1,457 of 1,779 units
- THE table is `dominant_table24.json` / `dom_ops22.json`:
  901 classes, 137 nodes, 26 families, 20 edgeless
- 28 branching units unreconciled into that table, named
- parallel branch: java and cpython re-run under the adopted
  pipeline; cpython's type key corrected to ptr64 BY MACHINE
  FACT; ruby and php folded into HQ artifacts
- super-op provenance: 96 of 494 idiom candidates resolved to an
  emitting function; 398 frontier (189 of them ambiguous ties)

## STANDING REQUIREMENTS — every task, every sub-agent

Unchanged from log_083's header; re-read it. In brief: read
AgentMemory.md and the comms protocol in full first; paste THE
SPELLING BAN verbatim into every sub-agent brief; run
`check_no_spelling_keys.py` on everything, matching-shaped files
without exemption; prove every rendering against the unit's OWN
ship code; verify zero regressions programmatically; new files
only, defective artifacts stay as records; dated PROGRESS entry
per task; evidence class on every claim; refuse honestly.

ADDED THIS ROUND, from the audit's findings:

- EVERY ARTIFACT YOU WRITE IS NAMED IN YOUR LOG. The audit found
  `guards3.json` and `guards_java_deopt.py` on disk, feeding the
  exception axis, mentioned in NO log and NO PROGRESS entry —
  while the log claimed the rows they contain were excluded. An
  unlisted artifact is how java silently fell out of the tables
  once already. List every file you create, including drafts and
  superseded attempts.
- CLAIMS ABOUT WHAT YOU DID *NOT* DO ARE CHECKED TOO. "X was
  explicitly not carried" is a claim; if X is on disk, the claim
  is false. Verify your own exclusions before writing them.
- QUOTE PINS FROM THE ARTIFACT, NOT FROM YOUR NOTES. One log said
  tree-sitter 0.26.0 where the artifact recorded 0.25.2.

---

## TASK 8 — reconcile guards3.json into the record (do first,
## small)

CONTEXT: `op_pipeline/guards3.json`, `guards_java_deopt.py`
(undocumented, from the round-1 session), `guards2_parallel.json`,
`exception_families.json`, `log_087_task5_parallel_branch_reconnect.md`
(whose exclusion claim is false).

WORK: (a) determine what guards3.json actually is and how it
relates to guards2/guards2_parallel — is it a superset, a
parallel attempt, or a fold? (b) produce ONE guard record of
record, with java's rows carried and marked
`provenance_is_weaker: true` per add_java.json's own precedent;
(c) rebuild the exception families over it — the round-1 families
(34) were built WITHOUT java's deopt evidence, so the
`deopt-continue-elsewhere` response kind may now form or join a
family; report whether it does, with the family row verbatim;
(d) rebuild the cross-axis operator x exception table; (e) write
a short correction note in the new log naming log_087's false
exclusion claim, so the record is straight.

ACCEPTANCE: one guard artifact of record; exception families
rebuilt with java included; the cross-axis table regenerated; the
correction stated plainly.

## TASK 9 — the 322 unconverged units, re-briefed against what
## round 1 learned

CONTEXT: round-1 Task 2 (log_084) converged ZERO and the audit
confirmed the zero is real with diagnosed causes — read that log
for the four refusal reasons and the branching-classification
mismatch that made canon25's targets unreachable. Also
`name_census.json` (the ranking), `vex_names.py` (the generic
translator that DID work, +42 units), `condition_table10.py`
(round 1's new table), `canon26*.py` (newest driver/gate).

WORK, in this order:
1. RE-SURVEY the 322 from the CURRENT newest generation — the
   round-1 survey counted from an older baseline and its target
   sets did not match the drivers' population filters. Produce a
   fresh census: refusal reason x language x branching/straight,
   with counts, before writing any code.
2. Fix the population-filter mismatch itself (the round-1 cause
   of "0 attempted"): the driver's unit selection must be derived
   from the same records the survey counts, not from an
   independent classification.
3. Then work the largest buckets. The 57 raw-text
   amd64g_calculate_condition units and the 19
   amd64g_calculate_rflags_c units are the named ones; whatever
   the fresh census puts on top takes priority over that guess.
4. Report converged delta from 1,457 honestly; zero is an
   acceptable result if it is diagnosed, but a SECOND zero with
   the same cause is not.

## TASK 10 — the 28 unreconciled branching units

CONTEXT: `dominant_table24.json`'s
`unreconciled_branching_units` (the 28 ids), `seeds2.json` (66
resolved seeds, of which only 4 matched a class in the
reconciliation), `log_090_task7_lineage_reconciliation.md`,
`log_089_task3_branching_seeds.md`.

WORK: 58 of the 66 resolved seeds found no matching class and 4
were ambiguous. Diagnose per unit: is the seed text simply not
converged (so no class exists to match), is it a representative
mismatch (the seed matches a class member's raw text but not the
group representative), or is it genuinely a new computation? Fix
what is fixable — in particular, seed matching should use the
representative rule and the proved-edge set, not exact text
alone, since a seed proved equal to a class member belongs in
that class. Rebuild the table; report family changes verbatim.

## TASK 11 — widen graph coverage so super-op provenance
## resolves

DEPENDS ON: round-1 Task 1's builder (`compiler_graph/build_graph2.py`,
`graph_cpp2.json`: 1,232 nodes, 3,070 edges, 37,733 unresolved
calls).
CONTEXT: `super_ops.json` — 96 resolved, 398 frontier, of which
189 are AMBIGUOUS TIES (several candidate emitters, none
selected) and 64 are no-graph-coverage.

WORK: (a) the 37,733 unresolved calls are the reason ties do not
break — extend the builder's call resolution (the Go lap's
`resolve_dots.py`/`fix_bindings.py` are precedent for the same
problem in another language) and widen the file set beyond the
probe's six files to the functions those calls reach; (b) re-run
the provenance join; report how many of the 189 ties break and
how many of the 64 gain coverage; (c) the single emitting
function found so far (`SelectionDAGLegalize::ExpandNode`) is a
dispatcher — resolving through it to the specific expander (e.g.
ExpandLegalINT_TO_FP for the halving idiom, which Task 1 found by
hand) is the concrete test of whether the widening worked.

## TASK 12 — ruby and php: from dispatch measurements to handler
## slices

CONTEXT: `interp_ruby.json`, `interp_php.json` (folded round 1,
with pins: ruby 3.3.0, php 7.4.33 after eight build attempts),
`interp_cpython.md` (the pilot that DID extract handler slices —
7 symbols, anchor and ship), `SUPPORT_scaling_design.md`'s
interpreter track.

WORK: ruby and php have dispatch measurements (which interpreter
lines ran) but no handler slices — the arch-unit equivalent. Do
for them what the CPython pilot did: identify the handler
function each probe reaches, build anchor and ship, slice the
handler's machine code, record instruction counts. Then the
honest question the CPython pilot also faces: do these slices
belong in the operator table at all, or do they join through
bridges/dominance? Report, do not assert — and mark provenance
weaker, as java's does.

## TASK 13 — the documentation slips (trivial, bundle with any
## other task)

- `log_086` quotes tree-sitter 0.26.0; `graph_cpp2.json` records
  0.25.2. Correct the log.
- `log_090` states dom_ops21c passes the spelling guard without
  the exemption; it passes only WITH it. Correct the log.

---

Order recommendation: 8 first (small, and it straightens a false
record). 9 next (largest population, and its round-1 failure is
diagnosed). 10 and 11 are independent and can run in parallel.
12 is self-contained. 13 rides along with anything.
