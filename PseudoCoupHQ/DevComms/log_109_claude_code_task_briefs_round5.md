# log 109 — task briefs for Claude Code, round 5

Date: 2026-09-01. Point a Claude Code session here.

MODEL POLICY (the owner, this round): OPUS IS THE DEFAULT SUB-AGENT.
Delegate to a smaller model only for genuinely simple mechanical
work (a file rename, a re-run of an existing script, a count).
Anything involving judgment — modelling, proving, carving,
diagnosis, report-writing — goes to Opus.

STATE AT HANDOFF (audited):
- converged 1,561 of 1,779; THE table is dominant_table24/
  dom_ops22 (901/137/26/20), untouched by rounds 3-4 as required.
- block cutter fixed for real binaries, regression-tested;
  cpython slices re-extracted (94 -> 93 instructions).
- guards5.json / exception_families3.json carry the growing mode
  row and EF0039, the first `grows` family.
- proposal_representation_dimension.json exists but its ONE
  PROVED record carries the forbidden bare ptr64 key — must be
  regenerated before the owner ratifies (task 24).
- ROUND-4 AUDIT FINDINGS OF RECORD: log_108 contained a FALSE
  VERIFICATION CLAIM (asserted a readback of a file that was 0
  bytes); log_105 mis-bucketed 19 units; DevComms/scratch.py was
  created and named nowhere. The posterity message
  (DevComms/next_commit_message.txt) records all three.

## STANDING REQUIREMENTS — all prior rounds' rules, plus one

All of log_083/091/097/103's rules apply (read them; in brief:
AgentMemory + comms protocol first; SPELLING BAN pasted verbatim
into every sub-agent brief; check_no_spelling_keys.py on
everything, matching-shaped without exemption; prove against the
unit's OWN ship code; zero regressions verified programmatically;
new files only; dated PROGRESS entry; evidence class per claim;
name EVERY file created; verify exclusion claims; quote pins from
artifacts; compute every "all N are X"; the daemon commits —
banking is the posterity message).

RULE ADDED THIS ROUND (round 4 produced a false verification
claim — a report asserted a readback that never happened):
- ANY SENTENCE OF THE FORM "I VERIFIED X" PASTES THE COMMAND AND
  ITS OUTPUT. A verification without its transcript is an
  assertion and will be treated as one. This applies to file
  writes (paste the wc/cat), gate runs (paste the tally line),
  and guard runs (paste the PASS line).

---

## TASK 24 — regenerate the representation-dimension proof with
## the typed key (Opus; gates the owner's ratification)

CONTEXT: proposal_representation_dimension.json (round 4; its
proof record reads type_pair "ptr64,ptr64" while its prose claims
PyLongObject* — the machine field is the one that counts and it
is wrong), the brief that forbade bare ptr64 (log_103 task 19),
fix_cpython_type_key.py (the machine-fact type read precedent),
interp_fastpath.json (the proof itself is sound; the KEY on the
record is what must be regenerated).

WORK: extend the machine-fact type read to produce the DWARF-
typed key (PyLongObject*, and the equivalent for the other eight
handlers where reachable); regenerate the proposal artifact with
typed keys in the MACHINE FIELDS, prose and fields agreeing;
re-run the proof tally; paste the diff between old and new
records. Then PROGRESS entry stating the artifact is ready for
the owner's ratification of option B / B-with-A.

## TASK 25 — record repairs from the round-4 audit (simple parts
## may go to a smaller model; the retraction wording is Opus)

WORK: (a) PROGRESS.md's task-23 entry repeats the false
"posterity banking message written" claim — append a dated
retraction note to PROGRESS (do not edit the false entry; the
record of the failure stays); (b) log_105's mis-bucketing: append
a correction note — 14 units belong to the already-counted cause
(8 -> 22), 3 to another (1 -> 4), 2 carry the genuinely new
reason "answer never entered a tracked register" (now a named
bucket); (c) name scratch.py in the record: read it, state what
it is, and either give it a home or state that the owner may delete it;
(d) every correction pastes its evidence per the new rule.

## TASK 26 — the two-unit new bucket, and the 238-20 remainder
## (Opus)

CONTEXT: log_105's corrected accounting (after task 25): the
genuinely new refusal "answer never entered a tracked register"
(2 units), plus the deferred buckets per round-3/4
recommendations. The false-bucket "model next round" plan is
void; re-derive the plan from the corrected counts.

WORK: diagnose the 2-unit new bucket properly (what does "answer
never entered a tracked register" mean mechanically — likely the
answer lives in memory or a flag at return); then work whatever
the corrected accounting ranks largest among buckets recommended
"model". Report converged delta from 1,561 with per-bucket
accounting, transcripts pasted.

## TASK 27 — ruby and php slices in the required shape (Opus)

CONTEXT: task 21's honest exclusion — ruby/php have only short
hand excerpts, no op_units-shaped slice, so carving and
canonicalization could not run. The block cutter now handles real
binaries (task 20). interp_ruby.json / interp_php.json hold
dispatch measurements and pins (ruby 3.3.0, php 7.4.33).
The CPython pilot's extraction method is the precedent
(interp_cpython.json's handler_arch_units: anchor and ship
slices per symbol).

WORK: extract proper handler slices for ruby (opt_plus ->
rb_fix_plus / rb_int_plus route) and php (ZEND_ADD handler) from
their pinned builds (rebuild from the recorded Airlock recipes if
binaries are gone — the lane scripts are in Airlock's .done);
op_units-shaped records; then carve arrival/computation by
lineage confluence with the fixed cutter; then the computation-
part proofs against compiled classes (typed keys); extend
proposal_representation_dimension.json with their rows. This
completes the nine-handler evidence for the owner's ratification.

## TASK 28 — bank round 5 (simple; smaller model acceptable)

WORK: full-stack verification with transcripts pasted (guard
runs, zero-regression diff vs 1,561 and the table baseline);
one-page state summary in the reading form; write the posterity
message to DevComms/next_commit_message.txt and PASTE ITS wc -c
AND ITS FIRST 5 LINES in the log per the new rule.

---

Order: 25 first (small, straightens the record). 24 next (gates
ratification). 26 and 27 in parallel after 24. 28 last.
