# log 142 — task briefs for Claude Code, round 10

Date: 2026-09-02. Point a Claude Code session here. OPUS IS THE
DEFAULT SUB-AGENT; smaller models only for mechanical work.

## THE RULINGS THIS ROUND IMPLEMENTS (the owner, 2026-09-02; recorded in
## AgentMemory and log_141)

1. THE MEMORY-WRAPPED FORM (the owner's proposal, verbatim): "keeping
   the arch-unit usage of registers as is but with our insertion
   of loading from memory. because if the compiler already
   presents a form that is free of register conflicts and we can
   insert our memory-paradigm to update within the compiler-proven
   register use, we get the consistent symbolics for z3 and a
   functioning arch-unit."
   - The compiler's body is kept VERBATIM. No renaming of its
     registers. Its register assignment is compiler-proven
     conflict-free; that proof is reused, not redone.
   - A standardized PRELUDE loads each input from its ledger block
     into the register the compiler expects it in (the arrival
     contract names which). A standardized EPILOGUE stores the
     compiler's result register to OUT-0. Nothing else is touched.
   - THE LEDGER LIVES AT AN ABSOLUTE ADDRESS (rip-relative or a
     loader-relocated fixed address). NO register is reserved for
     the region base. Round 9's %r15 anchor is superseded; the
     four units it refused (cpp/op_765, cpp/op_770, swift/op_703,
     swift/op_739) must render without a special case.
   - Blocks are TYPED and addressed through the ledger (log_141
     §8): fixed block order IN / CONST / TEMP / OWN / GUARD / OUT,
     rows sized by type (a 16-byte value gets a 16-byte row — the
     1,479 vector-lane refusals become attempts), no contiguity
     assumed.
2. LEDGER ROWS CARRY PROVENANCE (the owner: "the ledger should also
   track the operator that a result might create. all the data
   moving through the arch-units, even temporary data"). Every
   row: block kind, type, value-at-run (when executed), PRODUCED
   BY (the operation), OPERANDS (the rows it read). The ledger is
   the dataflow graph written as a table. Temporaries and guard
   outcomes are rows whether or not they are also stored to
   memory (storing them is a cheap separate choice; the rows are
   the information).
3. LAYER 4 (the z3 form) IS A TRANSCRIPTION OF THE LEDGER. Read
   producer/operands bottom-up from OUT-0 and you have the term.
   THE CENSUS IS A FILTER: rows whose producer has no z3 term.
   No mining over instruction sequences.
4. LAYER 5 (the fixed-rule re-render) is the TEXTUAL NORMALIZER,
   applied after proof so equivalent units become textually
   identical. It is never the only route to a canonical text —
   layer 3 (the wrapped body) exists for every unit regardless.
5. The seven-layer chain of record: (1) original extraction,
   (2) context, (2b) arrival contract, (3) wrapped canonical unit,
   (4) ledger-transcribed z3 form, (5) normalized re-render,
   (6) the proof of 3 against 1, (7) the pool.

STATE AT HANDOFF (verified from artifacts this session):
- the_pool1: 5,548 entries over 28,984 units; 663 entries span
  >1 language; 3 span compiled+interpreted; E00033 is integer
  addition with 18 members across c/cpp/go/rust/cpython/php/ruby
  (representative php/add_function under the fewest-bytes rule —
  flagged for the owner's eye, not a defect).
- round-9 form (region36, %r15 anchor): original 1,752/1,779
  proved; interpreter 9/11; regenerated 27,223/29,288; 4 units
  refused for %r15 conflict; 1,479 refused for 16-byte lanes.
- name_census.json is STALE (keyed to canon24); it must be
  regenerated from the ledger filter (task 48).
- type_inventory3: 85 of 208 types demoted as known-but-not-
  declarable; the corrected oracle's budget is within 4,894 of
  the 29,288 accepted.

## STANDING REQUIREMENTS

All prior rounds' rules (log_083 … log_134 headers), unchanged:
AgentMemory + comms protocol first; SPELLING BAN pasted verbatim
into every sub-agent brief; check_no_spelling_keys.py on
everything, matching-shaped without exemption; prove against the
unit's OWN ship code; zero regressions in the ruled sense; new
files only; dated PROGRESS entry; evidence class per claim; name
EVERY file created; verify exclusion claims; quote pins from
artifacts; compute every "all N are X"; every "I verified X"
pastes command + output; check the vcs before ruling a
write-claim false; the daemon commits — banking is the posterity
message; a path check proves which side of the container wall you
are on; an audit whose claims outnumber its tool calls is
rejected. Reports in Appendix B shape: one numbered tree, high
to low, values in motion under every claim.

---

## TASK 47 — THE MEMORY-WRAPPED FORM (Opus; centerpiece)

CONTEXT: rulings 1–2 above; log_141 (the saved explanation, §8
the ledger); log_135_task43 (region36 — what to keep: the block
vocabulary and the gate; what to drop: the %r15 anchor and the
scratch-register rewrite); the arrival contracts already recorded
per unit (which register the compiler expects each input in — c
%rdi/%rsi, go %rax/%rbx, sret units with the destination seat).

WORK:
1. Implement the wrapper: for each unit, prelude (ledger -> the
   compiler's expected registers), body verbatim, epilogue
   (compiler's result register -> OUT-0). Ledger at an absolute
   address; document the addressing mode and the relocation.
2. Build the ledger for each unit WITH provenance: walk the body's
   dataflow (the lifted form already gives it) and emit rows —
   kind, type, producer, operands — for every value including
   temporaries and guard outcomes.
3. Render EVERY unit: 1,779 + 11 + 29,288. Assemble (as+objdump,
   real). Gate-prove against the unit's own ship code under the
   arrival contract. Chunk and checkpoint.
4. ACCEPTANCE INSTANCES, printed verbatim with values: (a) the
   four %r15 units now render and prove; (b) c/op_31 (address-of)
   proves with OUT-0 = the address of OWN-0; (c) a 16-byte-lane
   unit from the 1,479 renders with a 16-byte row; (d) c/op_109
   and go/op_319 (integer add): different bodies, different
   preludes (c loads into %rdi/%rsi; go into %rax/%rbx), and the
   SAME ledger table — print both ledgers side by side.
5. Report proved / undecided / disproved / refused per population
   with reasons; every refusal named.

## TASK 48 — LAYER 4 FROM THE LEDGER; THE CENSUS AS A FILTER
## (Opus)

CONTEXT: rulings 3–4; vex_names.py (the generic translator);
condition_table4/8/9 (the condition routes); the stale
name_census.json.

WORK:
1. Build each unit's z3 term by transcribing its ledger from
   OUT-0 downward (producer -> term, operands -> sub-terms). No
   separate expression pipeline.
2. THE CENSUS: filter every ledger for rows whose producer has no
   term. Output name_census2.json from the CURRENT generation:
   name, units blocked, languages, regular/irregular. Print it.
3. Write the missing rows — the generic parser for regular names,
   one written row per irregular name — and re-filter until the
   census is empty or every remaining name carries an honest
   "cannot model because …" with the reason.
4. Layer 5: the fixed-rule re-render of each proved term, as the
   textual normalizer. Record per unit: wrapped text (layer 3),
   normalized text (layer 5), and whether the two are
   character-identical.

## TASK 49 — THE POOL, REBUILT ON THE WRAPPED FORM (Opus)

CONTEXT: the_pool1 (baseline: 5,548 entries / 663 multi-language
/ 3 compiled+interpreted); THE REPRESENTATIVE RULE; the dom_op
rule.

WORK: the_pool2.json / the_families2.json over every unit task
47 proved, merging on layer-5 text identity and proved edges.
Report entries / multi-language / compiled+interpreted /
families against the_pool1; print E00033's successor (integer
addition) verbatim; print every entry that SPLIT or MERGED
between pool1 and pool2 with its cause. State the population.

## TASK 50 — THE FOUR CALLS THE LEDGER DID NOT TOUCH (mixed)

WORK: (a) fix the swift probe emitter's @_cdecl test now (Opus
for the fix; the owner's lean: now, since the corrected type inventory
already makes the next regeneration non-comparable). (b) the 118
testimony findings from the assignment run: re-capture through
the verbatim path (smaller model; it is a lane re-run). (c) the
three Airlock design calls — instance naming, several lanes per
instance, where an instance's agent tree lives — write ONE page
for the owner with the instance and the question for each (log_140 §5–7
already have the material); decide nothing.

## TASK 51 — bank round 10 (smaller model acceptable)

WORK: full-stack verification with pasted transcripts; the
one-page state in Appendix B shape; the authoritative count line
over the pool's population; posterity message with wc -c pasted.

---

Order: 47 first and alone; 48 after 47 (reads its ledgers); 49
after 48; 50 in parallel with any; 51 last.

---

## ADDENDUM (2026-09-02, before launch) — task 48 refined by the owner's
## question "why doesnt it have arch-opcodes associated with it"

- IRREGULAR NAMES ARE MODELLED FROM THE ARCH OPCODES, NOT FROM THE
  LIFTER'S INTERNALS. `amd64g_calculate_condition` is the lifter's
  own helper routine standing in for "read the flags the previous
  compare left"; the ARCH OPCODES that produce it are already in the
  unit's text (`cmp`/`test` then `sete`/`setl`/…), and
  condition_table.py's route already reads the condition off those
  opcodes (SUFFIX_TO_COND: `e`->CondEQ, `l`->CondSLT, …; cond_to_z3
  builds `L == R`, `L < R`, …). Under the provenance ledger, the
  producer of a flag-derived row is the PAIR (flag-setting opcode,
  flag-reading opcode) — a real arch-opcode producer with a real z3
  term — never the helper name. Task 48 step 3 is amended: every
  "irregular" lifter name is first asked "which arch opcodes in the
  unit produced this row?" and modelled from those; a lifter-internal
  name may appear in the ledger only when no arch opcode accounts
  for it, and then it is an honest hole, reported.
- LITERAL-OR-GLOSS IS NOW PROTOCOL (§5.1a, added 2026-09-02): every
  report in this round labels each rendering literal / gloss /
  analogy, and a gloss never appears without its literal.
