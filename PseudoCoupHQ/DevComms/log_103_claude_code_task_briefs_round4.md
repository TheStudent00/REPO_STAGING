# log 103 — task briefs for Claude Code, round 4

Date: 2026-08-31. Written after the fast-path proof and the owner's
rulings. Point a Claude Code session here.

STATE AT HANDOFF (audited):
- converged 1,541 of 1,779; THE table is dominant_table24/
  dom_ops22 (901 classes / 137 nodes / 26 families / 20
  edgeless).
- CPython fast-path PROVED equal to c's i64 `+` (unconditionally,
  all 64-bit inputs): interp_fastpath.json. The general path is
  the first measured instance of the `growing` response.
- NEW RULINGS in AgentMemory, read them before anything:
  `branch-to-alternate-computation` (third detection route,
  approved), THE ARRIVAL/COMPUTATION BOUNDARY IS LINEAGE
  CONFLUENCE (the "where the arguments meet" rule is retired
  again — the owner caught the backslide; the boundary is the first
  node whose ancestors include BOTH lineages), BANKING IS A
  MESSAGE NOT A COMMIT (the vcs daemon commits every 30s;
  banking = a posterity message, fine to land after the commits).
- the owner's membership lean for interpreter handlers: option B (a
  representation dimension) with a bit of A — the pointer changes
  ARRIVAL, the core operator is the same; typed pointers group
  with same-seed units. The fast-path proof supports this lean.
  Task 19 turns the lean into a measured proposal; ratification
  stays with the owner.

## STANDING REQUIREMENTS — as log_083/091/097, plus their added
## rules

Read AgentMemory.md and the comms protocol in full first; paste
THE SPELLING BAN verbatim into every sub-agent brief; run
check_no_spelling_keys.py on everything (matching-shaped without
exemption); prove renderings against the unit's OWN ship code;
zero regressions verified programmatically; new files only,
defective artifacts stay as records; dated PROGRESS entry per
task; evidence class per claim; name EVERY file created
(including drafts, stray logs, and PROGRESS edits); verify your
own exclusion claims; quote pins from artifacts; any "all N are
X" sentence is computed, not remembered; never claim
staged-not-committed — the daemon commits; banking messages go to
DevComms/next_commit_message.txt for posterity.

---

## TASK 19 — the representation dimension, built as a measured
## proposal

CONTEXT: interp_fastpath.json (the proof), interp_relations.json
(three shapes measured: struct-pointer, tagged-value, opaque
dispatcher), the fast-path arrival/computation carve, log_101 §4
(the A/B/C options), the owner's lean (B with a bit of A), THE
ARRIVAL/COMPUTATION BOUNDARY ruling (lineage confluence), the
entry-contract precedent (canon7's context record: it declares
WHERE values arrive; it would now also declare HOW they unpack).

WORK: build the proposal as artifacts, not prose:
1. Extend the entry-contract record with an ARRIVAL section per
   unit: representation (plain / typed-pointer(T) /
   tagged-value(scheme)), and the unpacking prefix (the
   instructions of each lineage before confluence), carved by the
   lineage-confluence rule. Compiled units get
   representation=plain and an empty prefix — state that
   explicitly in the record rather than omitting the field.
2. For the nine interpreter handlers: carve arrival vs
   computation by lineage confluence (the fast-path carve is the
   worked precedent), and attempt the computation-part proof
   against candidate compiled classes (the cross-unit prover;
   type key from the DWARF-recovered typed pointer, e.g.
   PyLongObject*, not bare ptr64 — extend the machine-fact type
   read where needed).
3. Output proposal_representation_dimension.json: per handler —
   representation, arrival prefix, computation part, proof
   verdict vs which class, and the WOULD-BE table row under
   option B (a new representation-keyed family) and under
   B-with-A (joins the same-seed family with representation
   carried as a dimension). NO changes to dominant_table24 —
   membership is the owner's ratification, and this artifact is what he
   ratifies from.
4. The `growing` mode row for CPython's `+`
   (branch-to-alternate-computation) goes into the guard record
   of record with provenance marks; rebuild exception families;
   report whether a `growing` family forms (it would be the
   first).

## TASK 20 — the block cutter for real binaries (two named
## defects)

CONTEXT: interp_fastpath.json's carve.defects_found_* record:
(a) alignment padding after ret/jmp is not treated as a block
leader, so walks fall through padding into unrelated code;
(b) a bare `<symbol>` jump target resolves as offset-0-into-this-
unit — right for self-contained probes, wrong for real binaries
where it names another function. Also the extraction artifact:
instruction 88 of the stored long_add slice is an empty mnemonic
with a stray byte (the tail of the previous 8-byte lea) — fix the
EXTRACTOR that produced it, and re-extract the affected slices.

WORK: fix both cutter defects in the shared machinery (new module
wrapping canon2's cutter, per the wrapper precedent), with a
regression test built from the long_add slice (the walk must
produce exactly the 48-instruction set the local fix found,
three address ranges, verbatim in interp_fastpath.json). Fix the
slice extractor's split-instruction bug; re-extract and diff.
These fixes gate future branching work on ruby/php/jvm slices.

## TASK 21 — canonicalize the interpreter units (never run on
## them; registers are NOT the issue)

CONTEXT: measured this session — no canon*_units_cpython.json or
canon*_units_java.json exists; canonicalization has never run on
the interpreter/JIT units. CPython's arguments already arrive in
the designated registers; what differs is what they hold, which
Task 19's arrival section declares. So canonicalization should
mostly succeed on the COMPUTATION parts.

WORK: run the newest canonicalization generation over the
interpreter/JIT units' computation parts (post-carve, from Task
19's step 2): java's 2 units, cpython's fast path, ruby/php's
handler slices where the carve succeeds. Gate against their own
real ship code as always. Report per unit: canonical text or
honest refusal. provenance_is_weaker carried in the JSON (the
round-3 gap, already fixed for ruby/php — match it).

## TASK 22 — the remaining 238 unconverged, fourth round

CONTEXT: log_099 (round 3: +84, with per-bucket accounting and
recommendations for the deferred). Work the deferred buckets per
its own recommendations; a bucket recommended "model" gets
modelled, one recommended "defer" stays deferred unless its
blocker fell, one recommended "out of scope" is NOT reopened
without new evidence. Report converged delta from 1,541 with
per-bucket accounting.

## TASK 23 — bank and re-baseline (as task 18, corrected for the
## daemon)

WORK, after 19-22 land: full-stack verification (guards, zero
regressions, family diffs vs dominant_table24/dom_ops22 with
named causes); the one-page state summary in the reading form;
write the posterity message to DevComms/next_commit_message.txt
naming the round's artifacts and any decisions taken — the
daemon has already committed everything, the message is for
searchability, and saying so is the correct report.

---

Order: 20 first (it gates 19's carves on ruby/php), then 19,
then 21 (needs 19's carves), 22 in parallel with any, 23 last.
