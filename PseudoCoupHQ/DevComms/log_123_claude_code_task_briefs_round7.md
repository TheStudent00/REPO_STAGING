# log 123 — task briefs for Claude Code, round 7

Date: 2026-09-01. Point a Claude Code session here. OPUS IS THE
DEFAULT SUB-AGENT; smaller models only for mechanical work.

STATE AT HANDOFF:
- compiled five: 74 units were stuck at round 6's start; 41 of
  them are now PROVED (36 by designated memory, log_118; 5 by
  the result-destination seat, log_117) but NOT yet added to the
  recorded converged count — that advance is the owner's call and is
  NOT a task here.
- type inventory: extracted and validated, zero holes (log_116);
  swift's missing authority is now on disk —
  Sources/swift-6.0.3-RELEASE, cloned at the
  toolchain pin, verified commit 6a862d2e... (log_122).
- task 32 (interpreter table / join / union) was LOST MID-RUN
  when its host process exited; inputs all landed.
- defect of record: lane_gen.py firstline() replaces "|" with
  "/" inside stored compiler diagnostics, altering verbatim
  testimony (log 121). Remediation shape is the owner's call; task 37
  prepares it without re-capturing.

## STANDING REQUIREMENTS

All prior rounds' rules (log_083/091/097/103/109/115 headers).
Highlights: AgentMemory + comms protocol first; SPELLING BAN
pasted verbatim into every sub-agent brief;
check_no_spelling_keys.py on everything, matching-shaped without
exemption; prove against the unit's OWN ship code; zero
regressions verified programmatically; new files only; dated
PROGRESS entry per task; evidence class per claim; name EVERY
file created; verify exclusion claims; quote pins from artifacts;
compute every "all N are X"; every "I verified X" pastes command
+ output; a file's current state is not its history — check the
vcs; the daemon commits — banking is the posterity message; a
path check proves WHICH SIDE OF THE CONTAINER WALL you are on
before it proves absence (log 121's lesson).

---

## TASK 34 — relaunch the interpreter table / join / union
## (Opus)

CONTEXT: log_119 (the lost run and what it intended), log_115
task 32 (the ruled design: three views — compiled table,
interpreter table, union — joined by proved relations, nothing
merged), log_118's designated-memory and arrival-mode machinery
(several interpreter units need it), the proved join row
(cpython fast-path + == c's + for all 64-bit inputs).

WORK: first CHECK DISK for partial artifacts from the lost run
(canon33-consuming outputs; name whatever is found and state
kept/discarded with reasons). Then run the 9 refused interpreter
units through the current canonicalizer; build
interp_table1.json (compiled-table key shape + the arrival/
representation column); build the join table (proved relations,
prover-attempted); build the union view. NO change to
dominant_table24. Guards on everything.

## TASK 35 — swift's extracted type authority (Opus; the source
## is now on disk)

CONTEXT: log_116 (type_inventory.json, every language extracted
except swift), log_122 (the clone at the pin; stdlib files
Integers.swift, Bool.swift, FloatingPointTypes.swift.gyb),
log 121 routes (a)/(b) as cross-witnesses (installed stdlib
interface files; swiftc -emit-module-interface).

WORK: read swift's scalar type authority from the pinned source;
add it to type_inventory.json with the authority line and pin,
matching the other languages' rows; validate against the corpus
exactly as log_116 did (predicted-legal vs compiler-accepted;
every difference reported). Use route (a)/(b) as a second
witness; two independent routes agreeing is the acceptance bar.

## TASK 36 — the intelligent way, measured before any compiling
## (Opus; REPORT-ONLY, no probe compilation)

CONTEXT: log 121 §3 (the owner's ruled direction and its glossary
entry: derive LEGAL probes from the authorities' own rules, then
compile only the residue), log_116's measured split (the type
pair alone explains ~71% of go/rust/swift refusals and 0% of
c/cpp — c/cpp legality lives in the operator-category rules in
clang's semantic analysis), the compiler sources on disk
(llvm-project at the pin for c/cpp; golang_src; rust; the new
swift clone), the compiler-graph builder.

WORK: read the legality rules per language from the sources —
clang's Sema operator-category checks for c/cpp; go/rust/swift's
per-operator type admissibility — and compute, per language:
naive cross-product count, filtered-legal count, and the
reduction. Validate the filter against the existing corpus (it
must predict the 1,779 accepted and the refusals; every miss is
a finding). REPORT THE REDUCTION TO DEE with the numbers; do
not compile anything. The residue-compilation decision and the
CPU-capped Airlock copy (log 121 §3 steps 3-4) come after his
read.

## TASK 37 — the verbatim-testimony defect, prepared for the owner's
## ruling (Opus for the audit; mechanical parts smaller)

CONTEXT: log 121: lane_gen.py firstline() runs
text.replace("|","/") on stored diagnostics, so wherever a
compiler quoted "|" the stored testimony is altered (rust probe
178 stores "i32 / f64" for `a | b`). Evidence doctrine: stored
testimony must be verbatim.

WORK: (a) fix the code path in a new module (wrapper precedent)
so future captures are verbatim; (b) AUDIT the damage: scan
every stored diagnostic for the substitution's fingerprint,
count affected records per language, and list which downstream
artifacts consumed the altered text; (c) write the remediation
proposal FOR DEE: re-capture cost vs annotate-in-place, with
counts. Do not re-capture without his ruling.

## TASK 38 — bank round 7 (smaller model acceptable)

WORK: full-stack verification with pasted transcripts; the
one-page state summary in the reading form; posterity message to
DevComms/next_commit_message.txt with wc -c and first lines
pasted (the daemon consumes the file — that is the mechanism).

---

Order: 34 and 35 in parallel; 36 after 35 (needs swift's
authority); 37 any time; 38 last.

DEE'S OPEN CALLS, listed so the session does not absorb them:
- advance the recorded count by the 41 round-6 proofs
  (1,635 recorded -> 1,676; the 13 withdrawn stay separate);
- the lane_gen remediation (task 37 delivers the proposal);
- whether the canonical form may carry a prologue (six go units
  need more than the 16 red-zone designated slots);
- probe regeneration go/no-go after task 36's reduction report.

---

## ADDENDUM (2026-09-01, after the briefs were written) — THE
## UNIVERSAL CANONICAL FORM RULING, binding on all tasks above

the owner ruled (recorded in AgentMemory, "THE UNIVERSAL CANONICAL
FORM"): every arch-unit uses the designated virtual-memory
system, loads from memory into registers are themselves
standardized, and HOW a value arrived (plain / pointer / tagged)
is an annotation on the one shared form — not a separate dialect.
Registers stop being the definition of the form; they are the
standardized vehicles of the standardized loads.

Effects on this round:
- TASK 34 (interpreter table): interpreter units canonicalize
  into the SAME memory-based form as compiled units, arrival
  annotated — the "meet in the middle" the owner described. The
  representation column stays as the annotation.
- The former "prologue" open call is WITHDRAWN — standardized
  loads at the top of a unit are part of the form, so the six
  go units needing more than 16 slots proceed without a ruling.
- Any refusal caused by register scarcity is now a defect, not
  a wall.

## ADDENDUM 2 (2026-09-01) — count advance ACCEPTED, and a
## standing rule so it is never asked again

the owner accepted the 41 round-6 proofs into the recorded count, and
questioned why acceptance was ever a question ("if theyre
proven, why wouldnt we say so?"). STANDING RULE, add to task 38's
bank and every future round: A PROVED UNIT IS A COUNTED UNIT.
Gate-proved convergence advances the recorded count in the same
lap, automatically; no per-round permission. The withdrawn units
remain the one separate population (withdrawal is an evidence
event, not a count preference). Task 38 reconciles the recorded
figures accordingly and states the single authoritative count
with its population line: converged N of 1,779 (compiled five),
withdrawn listed separately.
