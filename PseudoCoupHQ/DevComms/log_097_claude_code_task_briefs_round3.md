# log 097 — task briefs for Claude Code, round 3

Date: 2026-08-31. Written after the round-2 audit. Point a Claude
Code session here.

STATE AT HANDOFF (audited, recomputed):
- converged 1,457 of 1,779; THE table is dominant_table24/dom_ops22
  (901 classes / 137 nodes / 26 families / 20 edgeless), with
  byte-identical variants 24b/22b from task 10's honest zero.
- guard record of record: guards4.json (313 rows); exception
  families 39 (java's deopt evidence included); cross-axis table
  rebuilt. Uncrossed rows: swift 35, go 30, rust 10, java 8
  (log_092 misstates this as "all java" — task 14 corrects it).
- graph: widened but 0 of 189 provenance ties broken; the
  dispatcher edge ExpandNode -> ExpandLegalINT_TO_FP exists;
  task 11's own acceptance test honestly FAILED (reopened here
  as task 16 with the diagnosis in the brief).
- ruby/php: handler slices extracted with exact pins; the
  provenance_is_weaker mark is prose-only, not in the JSON
  (task 14 fixes).
- the 322 unconverged: two rounds of honest zeros with DIFFERENT
  diagnoses; task 15 re-attacks with round 2's diagnosis in hand.

## STANDING REQUIREMENTS — unchanged from log_083/log_091

Read AgentMemory.md and the comms protocol in full first; paste
THE SPELLING BAN verbatim into every sub-agent brief; run
check_no_spelling_keys.py on everything (matching-shaped without
exemption); prove renderings against the unit's OWN ship code;
zero regressions verified programmatically; new files only,
defective artifacts stay as records; dated PROGRESS entry per
task; evidence class per claim; name EVERY file your session
creates, including drafts and stray logs; verify your own
exclusion claims; quote pins from artifacts.

RULE ADDED THIS ROUND (both rounds' false claims had one shape):
- ANY SENTENCE OF THE FORM "all N are X" IS COMPUTED, NOT
  REMEMBERED. Run the count, paste the breakdown. Round 1's
  "u2.m4/u2.m9 not carried" and round 2's "all 83 uncrossed are
  java" were both this failure.

---

## TASK 14 — record hygiene (small, do first, one lap)

WORK: (a) correction note for log_092's "all 83 uncrossed rows
are java" — real split swift 35 / go 30 / rust 10 / java 8;
append the note to a new log, do not edit log_092 beyond adding a
pointer line. (b) move `provenance_is_weaker: true` into the
ruby/php JSON artifacts themselves (interp_ruby.json,
interp_php.json, and any op_units/sem_anchored records derived
from them), matching add_java.json's precedent — downstream joins
read JSON, not prose. (c) formally name
`op_pipeline/task10_seed_prove.log` in the record (a stray stdout
capture from task 10, benign). (d) sweep op_pipeline and
compiler_graph mtimes for the round-2 window (Aug 31 21:00-22:00)
and name anything else unlisted.

## TASK 15 — the 322, third attempt, with round 2's diagnosis
## in hand

CONTEXT: log_093 (round 2: census-first done, filter mismatch
fixed, delta still zero — READ ITS DIAGNOSIS SECTION and carry it
into your plan; a third zero with round 2's cause is
unacceptable; a third zero with a NEW, diagnosed cause is a valid
result but must be accompanied by a recommendation: model, defer,
or declare the bucket structurally out of scope with reasons).
Also name_census.json, vex_names.py, condition_table10.py,
canon26*.py.

WORK: attack the top buckets from log_093's fresh census in its
order. Where round 2 diagnosed a specific blocker per bucket,
address THAT blocker, not the bucket in general. Report converged
delta from 1,457 with per-bucket accounting.

## TASK 16 — provenance tie-breaking (reopens round-2 task 11,
## with its failure diagnosis)

CONTEXT: log_094 (the honest failure: widening files did not
break ties because tie-breaking needs CALL-GRAPH DEPTH — which
emitter is actually REACHED for the idiom's node kinds — not more
parsed files), graph_cpp2.json + its widened successor,
super_ops.json (96 resolved / 398 frontier, 189 ambiguous ties),
the probe's hand-verified answer (idiom_0001's emitter is
ExpandLegalINT_TO_FP, reached through ExpandNode).

WORK: break ties by reachability, not file count: from the IR
operation kind that the idiom's carrier units contain (their
lifted forms name it — e.g. the unsigned-conversion units carry
the UINT_TO_FP shape), query WHICH candidate emitter handles that
kind — the dispatch switch in ExpandNode names its cases; parse
the case labels as data. A tie breaks when exactly one candidate
handles the kind. ACCEPTANCE: idiom_0001 resolves uniquely to
ExpandLegalINT_TO_FP by this route (the hand-verified answer);
report how many of the 189 ties break; honest frontier for the
rest.

## TASK 17 — interpreter units into the table question
## (ruby/php/cpython), posed not forced

CONTEXT: interp_ruby.json, interp_php.json (slices + pins, after
task 14 adds the JSON provenance marks), interp_cpython.md's own
honest expectation ("python's + byte-matches nobody... joins
through BRIDGES and DOMINANCE, or through ratified intention"),
the bridge/dominance machinery (bridges*.json, dominance2.py),
cpython's corrected ptr64 type key.

WORK: do NOT put interpreter handler slices into the operator
table by assertion. Instead: (a) canonicalize the slices as far
as the enforced form allows (they are big — report sizes and
what refuses); (b) compute their relations to the compiled
units' classes via the bridge/dominance machinery (projection
agreements, e.g. the handler's fixed-width behaviour vs the
compiled add) and the cross-unit prover where types genuinely
align; (c) output a RELATION artifact (interp_relations.json):
handler -> {class, relation kind, proof/witness}, no table
membership changes; (d) write the decision brief FOR DEE: the
options (table members with weak provenance / a third axis /
bridges only), with the measured evidence for each. Membership is
his ruling, not yours.

## TASK 18 — bank and re-baseline

WORK, after 14-17 land: (a) verify the full stack end to end one
more time (spelling guards, zero regressions, family diffs vs
dominant_table24/dom_ops22 with named causes); (b) write a
one-page state-of-the-line summary in the reading form (numbers
+ one instance each, per the log_082 §1.2 rewrite's shape);
(c) stage a git commit message in next_commit_message.txt
naming the round's artifacts; do NOT commit or push — the owner banks.

---

Order: 14 first. 15 and 16 in parallel. 17 after 14 (needs the
provenance marks). 18 last.
