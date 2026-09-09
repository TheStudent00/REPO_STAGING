# log 134 — task briefs for Claude Code, round 9

Date: 2026-09-02. Point a Claude Code session here. OPUS IS THE
DEFAULT SUB-AGENT; smaller models only for mechanical work.

THREE CORRECTIONS FROM DEE DRIVE THIS ROUND:

1. THE UNIVERSAL FORM, GENERALIZED (the owner: "input and output isnt
   the only place where blocks can be allocated"). The form is a
   standardized virtual memory of TYPED ALLOCATION BLOCKS, one
   block per LINEAGE — every distinct origin of a value gets its
   own block: each input argument's lineage, each constant, each
   temporary, the result, a unit's own stack addresses (for
   address-of units), guard outcomes. NO DESIGNATED REGISTERS AT
   ALL: registers are scratch vehicles chosen by one fixed rule,
   never homes. Everything loads from its block and stores to its
   block. The directory base is a ruled virtual region, NOT
   %rsp-relative slots (round 8's red-zone slots are why the
   address-of units collided). Recorded in AgentMemory
   ("REFINEMENT OF THE UNIVERSAL FORM — NO DESIGNATED REGISTERS
   AT ALL"). Round 8's canon35_universal_* is NOT this form and is
   superseded.

2. THE MERGED POOL (the owner, verbatim: "there is a pool of all the
   arch-units we canonicalized and merged them when they are
   equivalent. not an accounting of every languages contribution
   to the number of units."). ONE pool of every canonicalized
   unit of every language; equivalent units COLLAPSE INTO ONE
   ENTRY; an entry is one distinct computation listing its
   members with language and arrival as columns. Today's state is
   NOT that: compiled classes are one pool, interpreter classes a
   second, and the CPython/c proof is recorded as a relation
   BETWEEN pools instead of merging the two entries — the exact
   loss of information the owner ruled against; and the 29,288
   regenerated units are in no pool. Task 44 builds the pool.

3. THE REFUSALS ARE EXPLAINED (measured this session, from the
   stored verbatim compiler messages): ~91,000 of the 100,265
   regeneration refusals are the compiler rejecting the probe's
   TYPE DECLARATION, not its operator — `_Sat _Fract`, `_Accum`
   (embedded-C fixed-point, behind a flag), `char16_t`/`wchar_t`
   (need a header in C), `__ibm128` (not on x86), `__fp16`
   (cannot be a parameter). The type inventory was extracted as
   "every type the compiler KNOWS", not "every type this target
   ACCEPTS". The operator-legality oracle is intact; the type
   inventory needs a second witness.

STATE AT HANDOFF (recomputed from artifacts this session):
- original corpus 1,779 units (compiled five); round-8 universal
  migration proved 1,744 but is superseded by correction 1.
- regenerated corpus: 129,553 probes compiled, 29,288 ACCEPTED
  and fully extracted (anchor/ship/DWARF) — NOT yet in any table.
- interpreter/JIT: 11 units (java 2, cpython 1, ruby 4, php 4);
  union_table3 indexes 9 of them plus the compiled 1,639.
- address-of units (c/op_31,32,34; cpp/op_43,44,46) disproved
  under round 8's form — expected to prove under correction 1.

## STANDING REQUIREMENTS

All prior rounds' rules (log_083/091/097/103/109/115/123/129
headers), unchanged: AgentMemory + comms protocol first; SPELLING
BAN pasted verbatim into every sub-agent brief;
check_no_spelling_keys.py on everything, matching-shaped without
exemption; prove against the unit's OWN ship code; zero
regressions in the ruled sense; new files only; dated PROGRESS
entry; evidence class per claim; name EVERY file created; verify
exclusion claims; quote pins from artifacts; compute every "all N
are X"; every "I verified X" pastes command + output; check the
vcs before ruling a write-claim false; the daemon commits —
banking is the posterity message; a path check proves which side
of the container wall you are on. ADDED: an audit sub-agent that
reports verification with fewer tool calls than claims is
rejected — the main session re-runs the checks itself.

---

## TASK 43 — THE UNIVERSAL FORM, REDONE TO DEE'S STATEMENT
## (Opus; centerpiece)

CONTEXT: AgentMemory "REFINEMENT OF THE UNIVERSAL FORM" (the
statement, verbatim), round 8's canon35_universal_* (what NOT to
repeat: designated registers as load targets, three red-zone
slots), the address-of disproofs and their recorded detail ("the
answer of this unit is the ADDRESS of one of its own private
stack locations, and that location collides with the directory").

WORK:
1. Define the block allocator: lineage -> typed block, in a
   virtual region with a RULED BASE (a symbolic base register or
   a fixed virtual address range mapped to real stack at run
   time — document the mapping and why it stays runnable);
   allocation kinds: input, constant, temp, result, own-address,
   guard-outcome. One fixed rule chooses scratch registers for
   the loads/stores; no register is a home.
2. Render EVERY unit — the 1,779, the 11 interpreter/JIT units,
   AND the 29,288 regenerated units — into the form. Assemble
   (as + objdump, real), gate-prove against each unit's own ship
   code under the arrival contract (values in their blocks).
   Chunk and checkpoint; the regenerated population is large.
3. The address-of units must PROVE: c/op_31's answer becomes an
   address WITHIN the virtual region, standardized, so two
   address-of units compare equal. Print the before/after and the
   verdict verbatim.
4. Report: proved / undecided / disproved / refused per population
   (original 1,779; interpreter 11; regenerated 29,288), with
   reasons for every non-proof.

## TASK 44 — THE MERGED POOL (Opus) — the owner's correction, verbatim:
## "there is a pool of all the arch-units we canonicalized and
## merged them when they are equivalent. not an accounting of
## every languages contribution to the number of units."

CONTEXT: every unit task 43 proved (original 1,779 + interpreter/
JIT 11 + regenerated 29,288); the proved-edge sets (cross-unit
prover, the interpreter join's 18 proved relations, the
fast-path proof); THE REPRESENTATIVE RULE; the dom_op
construction rule (unchanged).

WORK: ONE POOL. Every canonicalized unit of every language goes
in; units proved equivalent — identical universal-form text, or
joined by a proved edge — COLLAPSE INTO ONE ENTRY. An entry is
one distinct computation; it lists its member units with
language and arrival annotation as COLUMNS ON THE MEMBERS, never
as partitions of the pool. The CPython fast path sits IN the
same entry as c/op_109, not in a second table joined to it. The
compiled-only / interpreter-only tables cease to exist as
objects; anyone needing one filters the pool. Output
the_pool1.json (entries) and the_families1.json (dom_op rule
over the pool's operator-nodes, all languages). Report: entries,
member units, entries spanning >1 language, entries spanning
compiled+interpreted, families; and separately the original-1,779
subset's figures for continuity with 898/137/26/20. Print the
CPython/c entry verbatim as the acceptance instance.

## TASK 45 — THE TYPE INVENTORY'S SECOND WITNESS (Opus)

CONTEXT: correction 3; type_inventory2.json; the refusal census
(this session: `_Sat`/`_Accum`/`_Fract`, `char16_t`/`wchar_t`,
`__ibm128`, `__fp16` as the over-admitted families).

WORK: (a) add the witness "DECLARABLE ON THIS TARGET WITH THIS
TOOLCHAIN": one tiny compile per type per language (a variable
declaration of that type, nothing else), in the trickle
container; record accept/refuse with the verbatim message. This
is a few hundred compilations, not probes. (b) type_inventory3
= extracted AND declarable; list every type demoted with its
compiler message. (c) recompute the legality reduction on the
corrected inventory and RE-VALIDATE against the regeneration's
actual accept/refuse — the oracle's prediction should now match
the 29,288 closely; report the agreement and every remaining
miss as a finding. (d) do NOT re-run the regeneration; the
29,288 accepted are good data, and the ~91,000 type-refusals are
now explained rather than wasted.

## TASK 46 — bank round 9 (smaller model acceptable)

WORK: full-stack verification with pasted transcripts; the
one-page state in the reading form — the single authoritative
count line is now over THE ONE TABLE's population, with the
original-1,779 subset stated beside it; posterity message with
wc -c pasted (the daemon consumes it).

---

Order: 43 first (everything keys on its form); 45 in parallel
(independent); 44 after 43; 46 last.
