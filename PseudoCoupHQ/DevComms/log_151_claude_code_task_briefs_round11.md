# log 151 — task briefs for Claude Code, round 11

Date: 2026-09-02. Point a Claude Code session here. OPUS IS THE
DEFAULT SUB-AGENT; smaller models only for mechanical work.
ONE AIRLOCK INSTANCE PER TASK (ruling 6 below): a task that needs
the sandbox brings up its own named instance and takes down only
that one.

## THE RULINGS THIS ROUND IMPLEMENTS (the owner, 2026-09-02; AgentMemory
## "ROUND 10 RULINGS"; audit in log_150)

1. THE POOL MERGES ON THREE GROUNDS — layer-5 text identity (proved
   terms only), proved edges, and layer-3 wrapped-text identity.
   Log 148 §1.4's departure is ratified. The brief-strict count is
   recorded on the artifact, not used.
2. THE LEDGER GETS TWO MORE BLOCK KINDS: STACK (the machine stack —
   push/pop, 4,298 census rows) and X87 (the x87 register stack —
   fucomip/fucomi pairs, 1,072 rows). Fixed block order becomes
   IN / CONST / TEMP / OWN / STACK / X87 / GUARD / OUT.
3. IMPLICIT DESTINATIONS ARE PER-OPCODE RULES in `ledger47.py`:
   idiv/div write quotient to the accumulator and remainder to the
   data register; mul/one-operand imul write the accumulator (and
   data register for the high half); cltd/cqto make a row for the
   data register; an unconditional `jmp` is NEVER a flag reader; a
   comparison opcode's row is typed as "flags only", not as a write
   of its destination. Log 147 §5.3 names all four.
4. BRANCH LABELS ARE POSITIONAL in the wrapped text: `L0`, `L1`, …
   in address order; the objdump symbol comment (`<main.op_174+0x18>`)
   is dropped from the stored text. Log 148 §4.2.2 measured the
   effect: distinct layer-3 texts 6,277 -> ~2,999.
5. EVERY ARTIFACT THE PIPELINE READS IS WALKED BY THE UNMODIFIED
   GUARD. No file that feeds grouping declares `role: generator
   provenance`. Producers are typed objects `{"kind": ..., "mnem":
   ...}` (log 147 §13.3's shape). Log 150 §3: task 47's canon37
   files pass today only by exemption and fail with 579 places in
   `canon37_wrapped_c.json` once the role line is removed. A guard
   transcript is one process, all files, `grep -c exempt` = 0.
6. AIRLOCK (the owner: "keep. idc as long as it works for you … go with
   your lean"): keep all ten names from log_138; serial execution
   stays, no `workers` key; `down` refuses while any lane's status
   is `running` unless `--force`; the default agent tree for a
   non-default instance is `<runs>/<name>/agent` (outside the
   checkout); `daemon_file` dropped after the next `build.sh`.

STATE AT HANDOFF (verified in log_150 from artifacts):
- canon37 (memory-wrapped form): 30,436 of 31,078 proved, 642
  refused by name (16 + 2 + 624).
- layer4b: 23,414 terms proved, 826 withdrawn (all three spellings
  of the divide idiom), 4,142 no term, 2,054 undecided both routes.
  `name_census3.json`: 47 producers / 8,044 rows / 5,507 units.
- the_pool2: 5,274 entries over 30,436 members; 423 multi-language;
  3 compiled+interpreted; E00029 = integer addition, 158 members,
  layer-5 text `v0 + v1`, representative go/op_319 (35 bytes).
- the_families2: 35 families over 197 nodes.
- swift emitter fixed (`probe_gen3.py`); banked 29,288 predate it.

## STANDING REQUIREMENTS

All prior rounds' rules (log_083 … log_142 headers), unchanged:
AgentMemory + comms protocol first (§5.1a: every rendering labelled
LITERAL / GLOSS / ANALOGY; a gloss never without its literal);
SPELLING BAN pasted verbatim into every sub-agent brief;
check_no_spelling_keys.py UNMODIFIED on everything, in one process,
no exemption of any kind — a stage that quiets the checker about its
own field has failed (log 147 §13.7); prove against the unit's OWN
ship code; zero regressions in the ruled sense; new files only;
dated PROGRESS entry under the single `# PROGRESS` heading; evidence
class per claim; name EVERY file created; compute every "all N are
X"; every "I verified X" pastes command + output; check the vcs
before ruling a write-claim false; banking is the posterity message;
a path check proves which side of the container wall you are on;
an audit whose claims outnumber its tool calls is rejected. Reports
in Appendix B shape: one numbered tree, high to low, values in
motion under every claim, every number with its population. READ
§13 OF ANY LOG YOU CITE BEFORE CITING ITS EARLIER SECTIONS (log 149
reported as open a point log 147 §13.5 had closed).

---

## TASK 52 — THE LEDGER, REPAIRED: canon38 (Opus; centerpiece)

CONTEXT: rulings 2–5; `ledger47.py` (the form — do not edit it;
write `ledger48.py` importing what is unchanged); log 147 §5 (the
idiv instance, `c/op_210`: OUT-0 wired to the dividend); log 147
§4.1 (the five cannot-model causes); log 148 §4.2.2 (branch
labels); log 150 §3 (the guard finding); `layer4.producer_object`
(the typed-producer shape to reuse).

WORK:
1. `ledger48.py`: (a) per-opcode destination rules for idiv, div,
   mul, one-operand imul, cltd, cqto, cwtl/cltq (a table, one row
   per opcode: which registers it writes, which it reads implicitly);
   (b) STACK and X87 block kinds with rows for push/pop and for the
   x87 stack positions %st..%st(7); (c) `jmp` removed from the
   flag-reader pattern; (d) comparison rows typed "flags only";
   (e) positional branch labels `L0..` in address order, symbol
   comments dropped; (f) every `produced_by` a typed object
   `{"kind": "arrival"|"arch_opcode"|"flag_pair"|"stack_slot"|...,
   "mnem": ...}`; (g) no `role` key in any artifact's meta.
2. Re-render ALL three populations into canon38_* (1,779 + 11 +
   29,288). Assemble (as + objdump, real). Gate-prove against each
   unit's own ship code as task 47 did. Chunk and checkpoint.
3. ACCEPTANCE INSTANCES, verbatim with values: (a) `c/op_210`'s
   ledger now has OUT-0 produced by idiv reading (TEMP-of-cltd,
   IN-1) — print ledger before/after; (b) one push/pop unit with
   STACK rows; (c) one fucomip unit with X87 rows; (d) `go/op_174`
   and `go/op_180` (log 148 §4.2.2) now have IDENTICAL layer-3
   texts — print both; (e) `c/op_109` and `go/op_319` unchanged in
   verdict.
4. Zero regressions vs canon37: no unit loses WRAPPED_TEXT_PROVED
   without a named, proved cause. Report per population.
5. THE GUARD: unmodified `check_no_spelling_keys.py`, one process,
   every canon38 file, transcript pasted, `grep -c exempt` = 0.
   Then the same over the canon37 files WITH their role line
   removed, to show the before (expected FAIL) beside the after.

## TASK 53 — LAYER 4 ON canon38; THE CENSUS RE-FILTERED (Opus)

CONTEXT: `layer4.py`, `textwalk48.py`, `gate48.py`, `census48b.py`
(reuse; write `layer4c` drivers reading canon38); `name_census3.json`
(the baseline: 47 producers, five causes).

WORK:
1. Transcribe every canon38 ledger from OUT-0 downward; both gate
   routes; layer-5 normalization. Population: every unit task 52
   proved.
2. `name_census4.json`, typed producers, no role key. Print it.
   EXPECTATION TO TEST: the idiv family (1,558 rows), push/pop
   (4,298) and the x87 pairs (1,072) leave the census; the 826
   withdrawn units prove. Report the delta against census3 by cause.
3. Write the rows for STACK and X87 producers (a push is a store to
   a STACK row; fucomip compares two X87 rows — the flag pair then
   reads them through `condition_table.py` as today).
4. Report proved / withdrawn / undecided / no-term per population
   against log 147 §13.5's 23,414 / 826 / 2,054 / 4,142.
5. Guard as in task 52 step 5.

## TASK 54 — the_pool3 (Opus)

CONTEXT: `build_the_pool2.py`, `build_the_families2.py`,
`compare_pool1_pool2.py` (reuse; new output names); ruling 1; THE
REPRESENTATIVE RULE.

WORK: the_pool3.json / the_families3.json over every unit task 52
proved, three grounds. Report entries / multi-language /
compiled+interpreted / families against pool2 (5,274 / 423 / 3 /
35); print E00029's successor verbatim; print every split and every
merge between pool2 and pool3 with its computed cause; state how
many of pool2's 4,499 symbolic-target members now merge on layer-3
identity. Guard as above.

## TASK 55 — AIRLOCK: ruling 6 (Opus for the code; the repo is
## `PUBLIC/Airlock`)

WORK: (a) `down.sh` reads the instance's status folder and refuses
with the running lane's name when any status is `running`;
`--force` overrides; print the refusal text. (b) `instance.sh`'s
`default_agent` for a non-default instance becomes
`$HOME/AirlockRuns/$AL_INSTANCE/agent` (created on `up`); the
`sandbox` instance keeps `<root>/agent`; README and
`sandbox.conf.example` updated; `airlock doctor` lists
`<runs>/*` as well as `instances/`. (c) run `build.sh`, then
remove the `daemon_file` key and its `up.sh` block. (d) README
gains one paragraph: serial execution is deliberate; one instance
per task; a trickle jams only its own instance. (e) Verify: bring
up an instance named `r11check`, submit a 60-second lane, run
`airlock --instance r11check down` — paste the refusal; then
`--force`; then `doctor`. Nothing here touches the `trickle`
instance's stores.

## TASK 56 — bank round 11 (smaller model acceptable)

WORK: full-stack verification with pasted transcripts; the
one-page state in Appendix B shape; the authoritative count line
over the_pool3's population; the round's open points ONLY after
reading every cited log's correction sections; posterity message
with `wc -c` pasted.

---

Order: 52 first and alone; 53 after 52; 54 after 53; 55 in parallel
with any (its own instance); 56 last.

DEE'S OPEN CALLS (none blocking): the representative php/add_function
question is moot — go/op_319 is E00029's representative by bytes.
