#!/bin/bash
# bank1_l12_write_the_log.sh -- task bank1, lane 12.
#
# WHAT THIS LANE DOES: writes DevComms/log_253_task_bank1_the_bank.md.
# Every fenced block in it is the output of the command on its first
# line, run by this lane and captured; the prose between the blocks is
# written here.  No transcript in that log is typed by hand, which is
# the rule log_195 broke and the conventions verifier now checks.
#
# `grep -v 'peak resident'` on the command lines is deliberate and is
# task ap1's own device: peak resident moves between runs, so a claim
# that carried it could never MATCH on a re-run.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BANK1.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
OP=PseudoCoupHQ/Research/op_pipeline
L=PseudoCoupHQ/DevComms/log_253_task_bank1_the_bank.md
total=2

block () {
    echo '```' >> "$L"
    echo "\$ $1" >> "$L"
    eval "$1" >> "$L" 2>&1
    echo '```' >> "$L"
    echo >> "$L"
}

i=1
echo "[$i/$total] writing $L"
: > "$L"

cat >> "$L" <<'S0'
# log 253 — task bank1: the polyfill library as banked certificates, and the loop reshaped to delta plus audit

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/`).
Line: arch_unit_oracle, the "goal" section of 2026-09-07 and the rulings of
2026-09-08 and 2026-09-09. Law: `PseudoCoupHQ/Research/LAW.md`,
read in full including its tower section. Brief:
`PseudoCoupHQ/Research/briefs/task_bank1_brief.md`.
Date: 2026-09-10. Instance `bank1`, on the tower guest.

Artifact folder:
`PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`;
new files `certificates.jsonl`, `certificates.json`, `bank.py`, the driver
change in `autopoly.py`, `autopoly1.py`, `bank1_delta_runs.jsonl`,
`bank1_delta.json`, `bank1_full_runs.jsonl`, `bank1.md`, `src_bank1/`,
`src_bank1_full/`. Lane scripts: `.../autopoly/lanes_bank1/`, twelve of them,
each kept in the repo as the standing rule of 2026-09-07 requires. Every lane
log named below is on the TOWER (`<user>@<tower>`) under
`<runs>/bank1/agent/logs/`.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PseudoCoupHQ`, mounted into the
instance. Every rendering is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself, quoted;
**GLOSS** is a plain-words reading beside a literal. `grep -v 'peak
resident'` appears on the command lines because peak resident moves between
runs and a claim carrying it could never re-run to a match; the peaks
themselves are §8.

---

# 1. What this is, one sentence per object in relation

* A **CELL** is one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table, holding, per place the opcode writes, the z3 term
  the reference simulator's own builder puts there.
* A **WRITTEN PLACE** is one destination that opcode writes — `reg_rdi`,
  `flags`, `reg_xmm0.low`, `x87_7`, `stack_-8` — and it is part of a
  certificate's key because the gate answers PER PLACE, not per run.
* A **CERTIFICATE** is one record about ONE ARTIFACT: one (cell, target,
  written place) with the term text it was posed on, the rendered source and
  its sha256, the compiler and its flags LITERAL, the carved body's bytes and
  text, and the gate's verdict in z3's own words with the region sentence
  where one applied.
* **THE BANK** is `certificates.jsonl`: every certificate of every pass on
  disk, the strongest for each key marked `preferred`, every weaker or later
  one kept beside it and marked `superseded_by`.
* A **PASS** is one whole walk of the loop, one store file: `ap1` … `ap5` on
  the four compiled targets, task ap3's normalise-off ablation, task ex1's
  cpp pass, task ex1's interpreted handful, task ex2's interpreted loop, and
  now this task's own delta pass.
* **THE DELTA PASS** is the loop run over the (cell, target, written place)
  triples the bank holds no proof for, plus a 5% AUDIT SAMPLE of the ones it
  does, re-derived from the term.
* An **ALARM** is an audited triple whose re-derived verdict differs from its
  certificate ON IDENTICAL INPUTS — same term text, same source sha256, same
  compiler and flags. An alarm stops the pass and names the pair.

# 2. The walkthrough, before any figure

Nine stores were on disk when this task began. Each was read line by line and
every run turned into one certificate per written place; a run that never
reached a place at all was banked as one certificate with a null place and
the kind `refused`, so an attempt and its cause are banked rather than lost.
The strongest certificate of each key was marked preferred, ties going to the
earliest pass, and every other entry kept beside it. That is the bank: 12,593
certificates over 4,117 distinct (cell, target, written place) keys.

The brief asked for three readings before the driver was touched, and the
three reproduce the coordinator's own figures object for object: the STRICT
count of proved pairs per pass is 330 / 434 / 465 / 521 / 504, their union
523, and 19 pairs proved by some pass are not proved by the last — the same
19, the same five cells on all four through pass 4 and not in pass 5, every
one an `imm_gpr` cell, which is what task ap5 changed. Two readings sit above
STRICT: DESTINATION-ONLY, which is the reading tasks ap1 to ap5 actually
published, and CORPUS-NEEDED, which reads the flags only where the corpus
attests a consumer of them.

Two things the first build got wrong were found by reading its own output and
each was fixed in the one place that owned it, and both are recorded rather
than tidied away. The interpreted route was read `rendered` first and
`refusal_cause` second, so task ex2's thirty-eight nullary runs came out
`undecided` where task ex2's own account calls them refused — 418 against
ex2's 456. And every certificate named its store as `...`; the
spelling guard splits a string on `/ | : ,` and refuses any piece that is an
operator token, and `~` is one, so the guard refused the file 11,340 times,
once per certificate. The record is now written the guard's way.

Then the loop was reshaped and one delta pass run on the five compiled
targets: 707 runs where a full pass over the same five is 1,265, zero alarms,
two newly certified triples, 58 audited of which 51 came back identical and
7 came back on a DIFFERENT artifact. A full pass was then run in the same
instance and the same hour so the cost is measured rather than inferred. The
delta ran 55.9% of the full pass's runs and cost 81.9% of its seconds, and
that second figure is the one worth reading twice: the runs the delta skips
are the ones the machinery already answers quickly, and the ones it keeps are
the unproved ones that spend the gate's ceiling and then its re-pose.

# 3. The bank, per kind and per pass

**LITERAL**, lane `bank1_l7_delta_report_and_rebank.sh`
(`<runs>/bank1/agent/logs/20260910T041102Z__bank1_l7_delta_report_and_rebank.sh.log`):

S0

block "python3 $A/bank.py kinds | grep -v 'peak resident'"

cat >> "$L" <<'S1'
**GLOSS.** `certificates` counts every entry; `preferred` counts the one
entry each key keeps. The gap between them is the measure of how much of the
five passes' work was re-derivation: 12,593 records over 4,117 keys.
`ex1_interp`'s 70 and `ex2`'s 1,315 sum to 1,322 preferred `agreed`
certificates, which is exactly task ex2's own arithmetic — 63 of task ex1's
70 pairs are inside task ex2's outer set and reproduce there, and the other
7 are `sub` imm_gpr 64 on the seven interpreted targets, a cell no compiler
emits and which is therefore not in the outer set at all.

# 4. THE THREE READINGS

Stated as three every time from now on.

* **STRICT** — every written place of the pair is proved, flags included.
* **DESTINATION-ONLY** — every place of the pair's destination register is
  proved; the flags are not read. This is the reading tasks ap1 to ap5
  reported, restated here from the certificates alone.
* **CORPUS-NEEDED** — the destination is proved AND the flags are proved
  wherever the corpus's own attestation records a consumer reading a cell of
  this `mnem`'s flags; where no consumer ever does, the flags place is not
  read.

**LITERAL**, the same lane:

S1

block "python3 $A/bank.py readings | grep -v 'peak resident'"

cat >> "$L" <<'S2'
**GLOSS, four things.** Table B4 is the check that banking moved nothing:
the STRICT figure computed off the bank equals the one computed off the raw
store, pass for pass, and the five compiled passes read 330 / 434 / 465 /
521 / 504 — the coordinator's own numbers. The reconciliation table below
B5 is why the logs said 165 and this task says 88 for `ap5` cells on all
four: the passes counted `proved` OR `proved under caller extension`, and
all three readings here take `proved` to mean the gate answered unsat on the
obligation as posed. The corpus-needed reading is at `mnem` granularity
because the corpus's flag-pair rows record a setter by `mnem` alone, with no
operand shape and no width on the setter side — 11 setters over 22,741
flag-pair ledger rows. And the delta pass's own row is low (117 STRICT)
because a delta pass does not run the pairs it already holds proofs for; the
line to read is the bank's, which is the union.

# 5. The nineteen pairs a certificate restores

**LITERAL**, the same lane:

S2

block "python3 $A/bank.py restored | grep -v 'peak resident'"

cat >> "$L" <<'S3'
**GLOSS.** Every one of the nineteen is an `imm_gpr` cell, and the mechanism
is task ap5's own symbolic-immediate change: the cell key carries no
immediate, so the sweep's `imm_*` spelling baked `$0x3` in, and task ap5
spelled those shapes a second time with a symbolic immediate. The re-rendered
artifact is a different artifact, and the old proof described the old one.
§9 shows that difference as a line of source.

# 6. The stores this task did not bank, and the audit of that exclusion

Ten stores on disk are WITHIN-PASS backups their own logs record as
defective and keep beside the run of record; none is a pass of the loop, and
none is banked. Leaving one out silently would be a claim, so each was read
anyway and the answer measured.

**LITERAL**, the same lane:

S3

block "python3 $A/bank.py backups | grep -v 'peak resident'"

cat >> "$L" <<'S4'
**GLOSS.** Zero. No excluded store holds a certified key the bank lacks, so
the exclusion costs the library nothing.

# 7. The loop reshaped: delta plus audit, and what it cost

`autopoly.py` gains a `--bank` mode. What it attempts is (a) every (cell,
target, written place) with no certificate of kind `proved` or `agreed` and
(b) an audit sample of 5% of the certified triples, chosen by
`random.Random("2026-09-10")` and re-derived from the term. The unit the loop
executes is the RUN, one (cell, target), because the four steps render,
compile and carve every place of a pair together — so a pair with one
unproved place is run whole, and its already-proved places are re-derived
along with it.

**THE UNFLAGGED COMMANDS ARE STILL TASK ap1'S.** `DevComms/log_243` cites
seven commands of `autopoly.py` as reproducing commands and
`lanes_ap1/ap1_l5_run.sh` calls its `run`; a driver that answered differently
under those names would make a closed task's log unreproducible. So task
ap1's file was copied unchanged to `autopoly1.py` and every unflagged command
is delegated to it verbatim. The bank mode is reached as `autopoly.py --bank
<command>` and is the way the loop runs from now on.

**LITERAL**, lane `bank1_l11_the_report_whole.sh`
(`<runs>/bank1/agent/logs/20260910T044029Z__bank1_l11_the_report_whole.sh.log`):

S4

block "python3 $A/autopoly.py --bank report | grep -v 'peak resident'"
block "python3 $A/autopoly.py --bank cost | grep -v 'peak resident'"

cat >> "$L" <<'S5'
**GLOSS, and it is the finding about cost.** The delta pass ran 707 of 1,265
runs — 55.9% — and cost 81.9% of the full pass's seconds. The two
percentages differ because of WHICH runs the delta drops: a pair every one of
whose places is already proved is a pair the machinery answers quickly, and
those are exactly the ones dropped, while the pairs kept are the unproved
ones that spend the gate's 3,000 ms ceiling and then its 30,000 ms re-pose.
The saving is real and it is in runs. It is not, over this population, a
proportional saving in seconds, and saying otherwise would be reading the
run count as if it were the clock.

**The second figure that needs its own sentence: `newly certified` is 2.**
The delta attempted 954 place-triples and certified two of them. That is not
a failure of the delta — it is the measurement that tasks ap1 to ap5 had
already reached what this machinery can reach, and that the 954 remaining
triples are refusals by nature, `sat` verdicts and undecided obligations
rather than work waiting to be done. The full pass run beside it proves
the same thing from the other side: attempting all 1,265 produced 1,166
proved place-triples, every one of which the bank already held.

# 8. The audit

**LITERAL**, the same lane:

S5

block "python3 $A/autopoly.py --bank audit | grep -v 'peak resident'"

cat >> "$L" <<'S6'
**GLOSS.** 58 certified triples re-derived, 51 identical, 7 on a different
artifact, ZERO alarms. An alarm would be a differing verdict on identical
inputs — the machinery and the record disagreeing about the same artifact —
and there is none.

# 9. The seven artifacts that changed, one by one

**LITERAL**, the same lane:

S6

block "python3 $A/autopoly.py --bank changed"

cat >> "$L" <<'S7'
**GLOSS.** Six of the seven are `imm_*` cells and the differing source line
is the whole of the mechanism: the certificate's source says `3` and the
re-derivation's says `v0`, which is task ap5's baked immediate becoming a
symbolic one. The seventh, `or` gpr_gpr 64 on c at `flags.high`, is a
different and more interesting mechanism — task ap2 proved it through the
PRIMITIVE route, and the current driver refuses that place outright with
`the primitive route renders the operator's own answer, and the flags place
is not a value an operator answers with`. A proof that exists is one the
machinery can no longer reach. The certificate keeps it, which is the whole
of what a bank is for.

# 10. The guard

**LITERAL**, lane `bank1_l7_delta_report_and_rebank.sh`:

S7

block "python3 $OP/check_no_spelling_keys.py $A/certificates.json"
block "python3 $OP/check_no_spelling_keys.py $A/bank1_delta.json"

cat >> "$L" <<'S8'
The two jsonl stores were guarded by the same program over a json array of
their lines, materialised under `/tmp` inside the instance and never in the
repository; lane `bank1_l7_delta_report_and_rebank.sh` carries that pass and
both read PASS. `grep -c exempt` over every file this task adds, LITERAL,
lane `bank1_l4_guard_passes_and_delta_preflight.sh`: `bank.py` 0,
`autopoly.py` 0, `autopoly1.py` 0, and 0 on every lane script except
`bank1_l3_build_again_and_guard.sh`, which reads 2 because the word appears
twice inside its own `grep` command line; lane 4 builds the pattern from two
pieces for exactly that reason and reads 0 everywhere.

# 11. Memory

The bound stated in `Airlock/instances/bank1.conf`, in every
lane header and in both programs' own constants is 6 GB resident on the one
collecting process, named abort `ABORT_MEMORY_BANK1`, checked after every
store in `bank.py` and after every run in `autopoly.py`. The sample the law
asks for is lane 1's `bank.py sample 20` — the first 20 runs of every store
turned into certificates, nothing written — and lane 5's `autopoly.py --bank
run 20`.

| lane | what it did | peak resident, kB | share of the 6 GB bound |
|---|---|---|---|
| `bank1_l1_preflight_and_sample.sh` | the 20-run sample of every store | 31,000 | 0.5% |
| `bank1_l5_delta_sample.sh` | the delta pass's first 20 runs | 255,548 | 4.1% |
| `bank1_l6_the_delta_pass.sh` | the delta pass, 687 runs | 996,780 | 15.8% |
| `bank1_l8_the_full_pass_for_the_cost.sh` | the full pass, 1,265 runs | 2,412,736 | 38.4% |
| `bank1_l11_the_report_whole.sh` | the report | 61,428 | 1.0% |

No abort fired at any point across the twelve lanes. Every store is streamed
line by line and none is held whole; the one document held whole is the cells
file, 2 MB.

# 12. The tally

S8

block "wc -l $A/certificates.jsonl $A/bank1_delta_runs.jsonl $A/bank1_full_runs.jsonl $A/bank1.md"

cat >> "$L" <<'S9'
`certificates.jsonl` is 21,467,474 bytes over 12,593 lines; `src_bank1` holds
758 rendered sources and `src_bank1_full` 1,440.

# 13. The two lists

## Decided, recorded for audit

1. **The bank is keyed (cell triple, target, written place), and the cell is
   three fields with the mnemonic in `mnem`** — never a joined string, which
   the spelling guard refuses and which `autopoly5.cell_of`'s own docstring
   records an earlier draft being refused for.
2. **`proved` means the gate answered unsat on the obligation as posed, at
   the pipeline's own 3,000 ms ceiling of record.** A place whose one re-pose
   at 30,000 ms answered unsat is banked `undecided` with the re-pose inside
   its verdict, because task ap1's rule is that the verdict OF RECORD is the
   pipeline's own ceiling and the re-pose sits beside it. Three certificates
   are in that position. Reading it the other way would have made the bank's
   figures unequal to the five passes' own, which is the one thing the three
   readings exist to prevent.
3. **`proved_under_caller_extension` is a kind of its own and is NOT
   certified**, so the delta pass attempts those triples again — the brief's
   own words are "no certificate of kind `proved`/`agreed`".
4. **Task ap3's normalise-off ablation (`autopoly3_off_runs.jsonl`) IS
   banked**, as its own pass `ap3_off`, because its runs are real artifacts
   with real verdicts and banking them can only add. The ten WITHIN-PASS
   backup stores are NOT banked, and each was read anyway: none holds a
   certified key the bank lacks (§6).
5. **Task ap1's driver was copied unchanged to `autopoly1.py` and every
   unflagged command of `autopoly.py` delegates to it**, so log 243's seven
   reproducing commands and `lanes_ap1/ap1_l5_run.sh` answer exactly as they
   did. The bank mode is `autopoly.py --bank <command>`.
6. **The delta pass entered through `handful.use_task_ex1`, not a new task
   name.** `handful.py` gates three route switches on a list of task names
   and is a shared file this brief does not authorise changing; `ex1` carries
   all three switches on and its `targets()` answers the five compiled
   targets the brief names. Task ap5's own two changes are not gated on a
   task name at all, so the route a run was put through is task ap5's route.
7. **Two defects of this task's own were found by its own output and fixed in
   the one place each owned** (§2): the interpreted kind read `rendered`
   before `refusal_cause`, and the certificate's store path began `~/`. Both
   earlier lanes' logs stand as the record and nothing was deleted.
8. **No shared file changed.** `handful.py`, `Research/op_pipeline/` and the
   five renderers are untouched; the only file outside this task's own new
   ones that changed is `autopoly.py`, which the brief names.

## Awaiting the owner

1. **The delta pass's saving is in RUNS (44%) and not proportionally in
   SECONDS (18%)**, because the runs it drops are the fast already-proved
   ones. A pass that also skipped the pairs whose only unproved places are
   refusals BY NATURE — an 80-bit x87 place on rust, go and swift; a vector
   arrival with no holder — would drop most of the remaining cost, but
   deciding which causes are "by nature" is a judgement about the causes and
   not a fact about the bank, so it is flagged rather than taken.
2. **`or` gpr_gpr 64 on c at `flags.high` is proved in the bank and
   unreachable by the current machinery** (§9): task ap2 proved it through
   the primitive route and the driver now refuses that place by cause. The
   certificate stands and the loop will not re-derive it. Whether the
   primitive route should render a flags place at all is the question that
   refusal encodes, and it is not this task's to answer.
3. **The cpp column is no longer stale.** Task ex2's awaiting-the owner item 2 said
   the all-five figure was read off task ex1's cpp store, which predates task
   ap5's symbolic-immediate change; this task's delta pass attempted cpp
   against the current outer set, so the bank's all-five figures are now read
   off current cpp runs. The figures are in Table B5 and no longer carry that
   caveat.
S9

echo "  $L written: $(wc -l < "$L") line(s), $(stat -c %s "$L") byte(s)"
echo

i=2
echo "[$i/$total] the log's own head, so this lane's own output shows it"
head -20 "$L"
echo
echo "lane done"
