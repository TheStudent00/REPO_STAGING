# log 129 — task briefs for Claude Code, round 8

Date: 2026-09-01. Point a Claude Code session here. OPUS IS THE
DEFAULT SUB-AGENT; smaller models only for mechanical work.

THE HEADLINE CORRECTION DRIVING THIS ROUND (the owner, verbatim): "not
just interpreter languages. ive been saying 'canonical form using
universal memory' in reference to everything. for every
language." Round 7 canonicalized only the 9 interpreter units
under the universal memory-based form; the 1,779 compiled units
still carry register-first canonical texts. That is an
implementation shortfall against the ruling in AgentMemory
("THE UNIVERSAL CANONICAL FORM ... every arch-unit"). Task 39
migrates everything.

STATE AT HANDOFF (audited, recomputed):
- converged 1,676 of 1,779 (compiled five; 13 withdrawn and 90
  unchanged accounted separately; proved-is-counted is standing).
- interpreter side: 9 units proved under the universal form;
  interp_table2 (8 classes), interp_join2 (18 proved relations),
  union_table2 built; dominant_table24 untouched, hash-verified.
- intelligent-way numbers for the owner's regen call: naive 152,298 /
  legal 121,081 / reduction only 1.18x — the filter is a
  validated oracle (99.9% agreement, 0 illegal-but-accepted),
  not a cost saver.
- testimony audit: correct figure is 158 distinct altered
  captures (go 101, rust 48, swift 9) — the logged "168 / rust
  58" is an arithmetic error that reached the bank and posterity
  commit (task 41 corrects the record).

## STANDING REQUIREMENTS

All prior rounds' rules (log_083/091/097/103/109/115/123
headers), unchanged. Highlights: AgentMemory + comms protocol
first; SPELLING BAN pasted verbatim into every sub-agent brief;
check_no_spelling_keys.py on everything, matching-shaped without
exemption; prove against the unit's OWN ship code; zero
regressions verified programmatically (NOTE for task 39: the
universal-form texts REPLACE the register-first texts as the
canonical column, so "zero regressions" there means no unit
loses its PROVED status and no class loses members without a
named, proved cause — text change is the point, not a
regression); new files only; dated PROGRESS entry; evidence
class per claim; name EVERY file created including caches;
verify exclusion claims; quote pins from artifacts; compute
every "all N are X"; every "I verified X" pastes command +
output; check the vcs before ruling a write-claim false; the
daemon commits — banking is the posterity message.

---

## TASK 39 — THE UNIVERSAL-FORM MIGRATION: every compiled unit
## (Opus; the round's centerpiece)

CONTEXT: AgentMemory "THE UNIVERSAL CANONICAL FORM" (the ruling:
designated virtual-memory locations for every value, standardized
loads into registers as the vehicles, arrival annotated
plain/pointer/tagged — one shared form for ALL units);
log_118's designated-memory machinery and slot directory;
log_124's interp_canon35 (the 9 interpreter units already in the
form — the template for what a universal-form record looks
like); canon lineage newest generation (canon31+ / the round-6/7
drivers); the gate (prove against the unit's own ship code).

WORK:
1. Define the universal-form rendering for a compiled unit
   mechanically and document it in the module header: every
   argument value originates at its designated memory location;
   the standardized load sequence brings it to its standardized
   register; the computation proceeds as before; the answer is
   stored to its designated location (and remains in its
   register — record both); arrival annotation plain for
   compiled scalar units, pointer/tagged where task 31/30
   machinery says otherwise (the 5 sret + measured exceptions).
2. Render ALL 1,779 compiled units into the universal form.
   Every rendered text assembles (as + objdump, real runs) and
   is gate-proved equivalent to the unit's own ship code UNDER
   THE ARRIVAL CONTRACT (the loads from designated memory are
   part of the form — the proof obligation is: for all values in
   the designated locations, the universal text computes what
   the original computes on those values).
3. Zero-regression in the ruled sense: every unit that was
   PROVED stays PROVED under the universal form; refusals are
   honest with reasons; report converged count under the
   universal form vs 1,676.
4. REBUILD the class table keyed on the universal-form text
   (operand types + machine-fact result type + universal text +
   arrival annotation as recorded data): dominant_table25.json,
   dom_ops23.json. EXPECTATION TO TEST, not assume: the
   universal form removes register-idiosyncrasy (go's ABI
   differences become invisible below the standardized loads),
   so cross-language classes may MERGE further. Report classes/
   nodes/families/edgeless vs 901/137/26/20 and print every
   family change verbatim with its cause.
5. The interpreter table then re-joins against the new compiled
   table (the join re-run); union rebuilt. Three views preserved.

## TASK 40 — regeneration decision package (Opus; report-only)

CONTEXT: the owner has the intelligent-way numbers (1.18x). His
go/no-go is pending. What he lacks is the operational cost side.

WORK: measure and report, compiling NOTHING: wall-clock and CPU
estimate for the 129,043-probe residue based on the measured
per-probe cost of the existing 4,440-candidate run (find its
timing records in the lane logs; if absent, time a 20-probe
sample ONLY — that is 20 compilations, state them); the
CPU-capped Airlock copy design (renamed containers, the
no-shared-names constraint, cap at 50% of cores per the owner's
overheating concern); checkpointed chunking plan. One page, for
the owner's go/no-go.

## TASK 41 — record hygiene (smaller model acceptable)

WORK: (a) correction notes for the 168->158 / rust 58->48 error
where it appears (log_126 §3.2 second statement, §5, log_128
§4.4, and a posterity correction in the next banking message);
evidence pasted per the transcript rule. (b) name the five
__pycache__ files the round-7 audit flagged as unlisted;
(c) sweep the round-8 window's files as always.

## TASK 42 — bank round 8 (smaller model acceptable)

WORK: full-stack verification with pasted transcripts; the
one-page state summary in the reading form; the single
authoritative count line (converged N of 1,779 under the
UNIVERSAL form, compiled five; withdrawn separate); posterity
message with wc -c and first lines pasted; include the 158
correction in the banked text.

---

Order: 39 first and alone (everything else reads its outputs);
40 in parallel (independent, report-only); 41 any time; 42 last.

DEE'S OPEN CALLS (not tasks): probe-regeneration go/no-go (after
task 40's cost page); testimony remediation route (158 captures:
re-capture lane exists unsubmitted vs annotate-in-place); F35-1
swift truth-value class; F36-1 c++ bool-increment marking.

---

## ADDENDUM (2026-09-01) — the owner's rulings on the open calls;
## task 40 upgraded from report-only to EXECUTION

- PROBE REGENERATION: GO ("yeah lets try it"). Task 40 is now:
  (1) the cost page as written, briefly; then (2) stand up the
  CPU-capped Airlock copy (renamed containers, no shared names
  with Airlock/SandboxDesign, cap 50% of cores — the machine
  must never overheat); (3) trickle the 129,043-probe residue
  through it in checkpointed chunks, using the verbatim-capture
  path (task 37's fix) so the new stores are testimony-clean
  from birth. Every chunk banks its partial results; an
  interrupted run resumes, never restarts. Report per-chunk
  tallies. Extraction (anchor/ship/DWARF) on accepted probes is
  part of the trickle, same recipes as the original lanes.
- TESTIMONY REMEDIATION: fold INTO the regeneration. the owner asked
  for the routes described plainly (done in-conversation): Route
  A re-captures the six affected lanes in ~5 minutes with the
  verbatim path (only risk: toolchain pins must match — verify
  pins in-lane before capture); Route B annotates in place but
  leaves reconstructions, not testimony. Since regeneration
  re-runs everything anyway with the verbatim path, Route A is
  subsumed: the regenerated stores ARE the remediation. The
  annotate route is dead. Mark the 158 old records as superseded
  by the regeneration capture when their lanes land.
- F35-1 / L125-1 RESOLVED — NOT an ontology question. The shared
  extraction rule's own stated text counts "an integer, a float
  or a truth value" as scalar core, but its NUMERIC_MARKS tuple
  lacks a truth-value entry, so booleans land "undecided" by
  code gap, not by decision. Booleans have been in the ratified
  six-type core since the first probe run. FIX: add the
  truth-value mark to the shared rule; swift's Bool and rust's
  bool enter their cores; recompute the affected counts.
  (the owner: "theres no fucking way we havent resolved every naming
  decision already" — correct; this was a missing tuple entry
  presented as a decision.)
- F36-1 RESOLVED (the owner: "if c++ allows it and someone can use it
  with intention, its valid"). c++'s bool increment/decrement is
  LEGAL in the legality rules, annotated as a language quirk
  (deprecated-but-allowed), not a standing miss. The 4
  validated-miss cases become 4 validated agreements.
