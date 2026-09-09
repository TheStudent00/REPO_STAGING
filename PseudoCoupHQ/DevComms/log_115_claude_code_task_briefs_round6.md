# log 115 — task briefs for Claude Code, round 6

Date: 2026-09-01. Point a Claude Code session here. OPUS IS THE
DEFAULT SUB-AGENT (the owner's standing policy, round 5): smaller models
only for genuinely mechanical work.

STATE AT HANDOFF (recounted from artifacts this session):
- compiled five: 1,705 of 1,779 converged-or-unchanged; 74 remain
  (by cause: 19 erasure-ok-but-empty, 16 unresolved branch
  target, 8 two-operands-in-memory, 6 join paths, 1
  read-before-defined, 9 one unmodelled op, 6 two, 6 SP leaf,
  3 no return block).
- interpreter/JIT: 11 units (cpython 1, ruby 4, php 4, java 2);
  2 with proved canonical text, 9 refused for ordinary reasons.
- THE table: dominant_table24/dom_ops22 (901/137/26/20) plus
  guards/exception families; untouched since round 3 by design.
- expansion to kotlin/csharp/v8/dart FROZEN (the owner).

DEE'S RULINGS THIS SESSION, binding on these tasks:
- TYPE INVENTORY IS EXTRACTED, NEVER HAND-WRITTEN. The operator
  inventory already is (operator_arity.json's own authority line);
  the six-type HOLDERS list in probe_gen.py is the hand-written
  half and must be replaced by extraction. Both routes validate
  each other: the extracted list's cross product vs what the
  compiler accepted; any difference is a finding.
- MEMORY IS DESIGNATED, LIKE REGISTERS. The canonical form gains
  designated LOCATIONS (standardized virtual slots with a
  directory: which location holds which designation), alongside
  the designated registers. Runnable because slots are real stack
  offsets mapped at run time.
- POINTER ARRIVAL IS LOGGED, THEN SIMPLIFIED — OR CANONICALIZED
  AS POINTER-BASED THROUGHOUT. the owner's statement, both halves: (1)
  log the pointer-types as part of tracked modes, then (2)
  simplify the expression so the unit is no longer a pointer
  unit; OR standardize the canonical form as pointer-based
  everywhere so everything is uniform. Two canon units agreeing
  on the simplified instructions but differing in modes is
  INFORMATION for dominant-operator decisions, not a nuisance —
  record the difference, never discard it.
- THE ENTRY CONTRACT GAINS A RESULT-DESTINATION SEAT. The
  struct-return units anchor with %rdi designated "result
  destination"; a/b shift to their designated seats. This also
  begins relaxing the fixed-arity ceiling the owner has objected to.
- INTERPRETER TABLE: THREE VIEWS. Compiled table, interpreter
  table, union — joined by proved relations, nothing merged,
  nothing destroyed. Membership is not a pending ontology
  question; it is construction.

## STANDING REQUIREMENTS

All prior rounds' rules (read log_083/091/097/103/109 headers):
AgentMemory + comms protocol first; SPELLING BAN pasted verbatim
into every sub-agent brief; check_no_spelling_keys.py on
everything, matching-shaped without exemption; prove against the
unit's OWN ship code; zero regressions verified programmatically;
new files only; dated PROGRESS entry; evidence class per claim;
name EVERY file created; verify exclusion claims; quote pins from
artifacts; compute every "all N are X"; every "I verified X"
pastes command + output; a file's current state is not its
history — check the vcs before ruling a write-claim false; the
daemon commits — banking is the posterity message.

---

## TASK 29 — the extracted type inventory (Opus)

CONTEXT: probe_gen.py (HOLDERS: the hand-written six-type list),
operator_arity.json (the precedent: grammar-authored, pinned,
per-language), the compiler-graph builder (build_graph2.py) and
the compiled languages' type-checking sources.

WORK: (a) extract each language's scalar type inventory from
authoritative sources (the grammar's primitive-type rules; the
compiler's own type tables where reachable; DWARF base types
observed in the corpus as a third witness). Output
type_inventory.json in operator_arity.json's style: per language,
per type, the authority that admits it, pinned. (b) VALIDATE both
directions against the existing corpus: does the extracted
inventory's cross product predict exactly the probes the compiler
accepted? Report every difference as a finding — a missed type,
or a refused combination we do not model. (c) Do NOT regenerate
probes this round — measure the gap first, report its size, and
the regeneration decision goes to the owner with numbers.

## TASK 30 — designated memory + pointer modes + the 8 units
## (Opus)

CONTEXT: the canonical form's ratified stack-slot overflow homes
(canon7 lineage), the erasure-by-substitution rule and its
all-or-nothing refusal on two-parked-operands (8 units: 2 cpp, 4
rust, 2 swift; NOTE the refusal fires against the ANCHOR build
and the message does not say which build — fix that labelling),
the owner's designated-memory ruling above.

WORK: (a) extend the canonical form with designated locations: a
directory (designation -> slot) beside the register map, slots as
standardized stack offsets; document in the file header. (b)
extend the erasure rule so two erasures meeting at one
instruction resolve by loading one operand into a designated
temp — justified as the park-reload idiom, gate-proved as always.
(c) pointer arrival: per the owner's ruling, record arrival
representation (plain / typed-pointer(T) / tagged) as a tracked
mode-like dimension on every unit (compiled units: plain), then
simplify pointer units to their value computation where the
carve supports it; where two units agree on simplified
instructions but differ in these recorded modes, the difference
is a REPORTED finding. (d) re-run the 8 units + any unit the new
rules reach; report converged delta from 1,705 per bucket.

## TASK 31 — the result-destination seat (Opus)

CONTEXT: the 5 rust struct-return units (range operator; caller
passes result address in %rdi, displacing a/b), the entry
contract (canon7's context record), the owner's ruling above.

WORK: add the third seat to the entry contract (designation:
result-destination), teach the anchoring layer the displaced ABI
(sret), re-run the 5 units through canonicalization + gate.
Survey the corpus for OTHER units the sret pattern explains
(other struct-returning operators, any language) and run them
too. Report per unit. This is also the first arity relaxation:
note in the report what the fourth seat would be (three-argument
operators) and what would break, for the owner's future call — do not
build it.

## TASK 32 — the interpreter table and the union (Opus)

CONTEXT: 11 interpreter/JIT units, 2 proved canonical; the
representation column ruling; dominant_table24/dom_ops22; the
proved join row (cpython fast path == c's + for all 64-bit
inputs); proposal_representation_dimension3.json (typed keys).

WORK: (a) run the 9 refused interpreter units through the
current canonicalizer (with task 30's designated memory and
pointer-mode machinery, which several need); honest refusals
where they stand. (b) build interp_table1.json: same class-key
shape as the compiled table plus the representation column;
guards/mode rows included (the growing family already exists).
(c) build the join table: proved relations between interp classes
and compiled classes (the cpython row first; attempt the others
via the prover). (d) the union view: all units, all three views
navigable; NO change to dominant_table24 itself. Guards on
everything; matching-shaped without exemption.

## TASK 33 — bank round 6 (smaller model acceptable)

WORK: full-stack verification with pasted transcripts; the
one-page state summary in the reading form; posterity message to
DevComms/next_commit_message.txt with wc -c and first lines
pasted (the daemon consumes the file — that is the mechanism,
say so).

---

Order: 29 and 31 in parallel (independent); 30 next (its
machinery feeds 32); 32 after 30; 33 last.
