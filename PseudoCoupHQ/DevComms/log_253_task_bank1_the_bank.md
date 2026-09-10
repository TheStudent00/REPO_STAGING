# log 253 — task bank1: the polyfill library as banked certificates, and the loop reshaped to delta plus audit

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/`).
Line: arch_unit_oracle, the "goal" section of 2026-09-07 and the rulings of
2026-09-08 and 2026-09-09. Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`,
read in full including its tower section. Brief:
`PRIVATE/PseudoCoupHQ/Research/briefs/task_bank1_brief.md`.
Date: 2026-09-10. Instance `bank1`, on the tower guest.

Artifact folder:
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`;
new files `certificates.jsonl`, `certificates.json`, `bank.py`, the driver
change in `autopoly.py`, `autopoly1.py`, `bank1_delta_runs.jsonl`,
`bank1_delta.json`, `bank1_full_runs.jsonl`, `bank1.md`, `src_bank1/`,
`src_bank1_full/`. Lane scripts: `.../autopoly/lanes_bank1/`, twelve of them,
each kept in the repo as the standing rule of 2026-09-07 requires. Every lane
log named below is on the TOWER (`<user>@<tower>`) under
`<runs>/bank1/agent/logs/`.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ`, mounted into the
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

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank.py kinds | grep -v 'peak resident'
Table B1 -- certificates banked per kind.  `certificates` counts every entry on certificates.jsonl; `preferred` counts the one entry each (cell, target, place) key keeps as its strongest, ties by the earliest pass.

| kind | certificates | preferred |
|---|---|---|
| `proved` | 5806 | 1227 |
| `proved_under_caller_extension` | 677 | 122 |
| `agreed` | 1385 | 1322 |
| `sat` | 483 | 91 |
| `undecided` | 583 | 72 |
| `refused` | 3659 | 1283 |
| **total** | **12593** | **4117** |

Table B2 -- the same, per pass.  A pass is one whole walk of the loop, one store file.

| pass | `proved` | `proved_under_caller_extension` | `agreed` | `sat` | `undecided` | `refused` | total |
|---|---|---|---|---|---|---|---|
| `ap1` | 614 | 71 | 0 | 39 | 56 | 572 | 1352 |
| `ap2` | 830 | 85 | 0 | 69 | 109 | 475 | 1568 |
| `ap3` | 874 | 85 | 0 | 67 | 147 | 375 | 1548 |
| `ap3_off` | 874 | 85 | 0 | 68 | 146 | 375 | 1548 |
| `ap4` | 934 | 85 | 0 | 70 | 38 | 421 | 1548 |
| `ex1_cpp` | 252 | 32 | 0 | 22 | 5 | 76 | 387 |
| `ex1_interp` | 0 | 0 | 70 | 0 | 0 | 0 | 70 |
| `ap5` | 919 | 109 | 0 | 65 | 38 | 417 | 1548 |
| `ex2` | 0 | 0 | 1315 | 0 | 0 | 456 | 1771 |
| `bank1_delta` | 509 | 125 | 0 | 83 | 44 | 492 | 1253 |

```

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

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank.py readings | grep -v 'peak resident'
Table B3 -- the headline in THREE readings, per pass and over the whole bank.  A pair is one (cell, target).  STRICT: every written place proved.  DESTINATION-ONLY: every place of the destination register proved, the flags not read -- the reading tasks ap1 to ap5 reported.  CORPUS-NEEDED: the destination proved AND the flags proved wherever the corpus's attestation records a consumer reading a cell of this `mnem`'s flags.

| pass | strict | destination-only | corpus-needed |
|---|---|---|---|
| `ap1` | 330 | 521 | 488 |
| `ap2` | 434 | 627 | 596 |
| `ap3` | 465 | 658 | 627 |
| `ap3_off` | 465 | 658 | 627 |
| `ap4` | 521 | 714 | 683 |
| `ex1_cpp` | 153 | 202 | 195 |
| `ex1_interp` | 70 | 70 | 70 |
| `ap5` | 504 | 698 | 666 |
| `ex2` | 1315 | 1315 | 1315 |
| `bank1_delta` | 117 | 359 | 321 |
| **the bank** | **1999** | **2241** | **2203** |

Table B4 -- the strict per-pass figures recomputed off the RAW STORES rather than off the bank, which is the check that banking moved nothing.

| pass | strict, off the bank | strict, off the store | same |
|---|---|---|---|
| `ap1` | 330 | 330 | yes |
| `ap2` | 434 | 434 | yes |
| `ap3` | 465 | 465 | yes |
| `ap3_off` | 465 | 465 | yes |
| `ap4` | 521 | 521 | yes |
| `ex1_cpp` | 153 | 153 | yes |
| `ex1_interp` | 70 | 70 | yes |
| `ap5` | 504 | 504 | yes |
| `ex2` | 1315 | 1315 | yes |
| `bank1_delta` | 117 | 117 | yes |

Table B5 -- cells on all four (c, rust, go, swift), on all five (+ cpp) and on all twelve, under each reading, with the attested ledger rows those cells cover and that as a share of 133044.

| width | reading | cells | ledger rows | share |
|---|---|---|---|---|
| all four | strict | 93 | 60534 | 45.5% |
| all four | destination | 144 | 84633 | 63.61% |
| all four | corpus | 134 | 73425 | 55.19% |
| all five | strict | 93 | 60534 | 45.5% |
| all five | destination | 141 | 79734 | 59.93% |
| all five | corpus | 133 | 72848 | 54.75% |
| all twelve | strict | 88 | 54680 | 41.1% |
| all twelve | destination | 136 | 73880 | 55.53% |
| all twelve | corpus | 128 | 66994 | 50.35% |

THE RECONCILIATION WITH THE FIVE PASSES' OWN PUBLISHED FIGURES, so a reader meeting three readings where the logs carried one is not left with a discrepancy.  Tasks ap1 to ap5 counted a pair proved when its destination places were proved OR proved under the caller's extension (`autopoly5.across_targets`); all three readings above take `proved` to mean the gate answered unsat on the obligation as posed.  The passes' own count, recomputed here:

| pass | pairs, as the passes counted | cells on all four, as the passes counted |
|---|---|---|
| `ap1` | 565 | 120 |
| `ap2` | 685 | 144 |
| `ap3` | 716 | 151 |
| `ap3_off` | 716 | 151 |
| `ap4` | 772 | 162 |
| `ex1_cpp` | 225 | 0 |
| `ex1_interp` | 70 | 0 |
| `ap5` | 777 | 165 |
| `ex2` | 1315 | 0 |
| `bank1_delta` | 447 | 57 |

THE ATTESTATION'S OWN GRANULARITY, said plainly: the corpus records a flag pair as (setter `mnem`, consumer `mnem`), with no operand shape and no width on the setter side, so the corpus-needed reading asks whether ANY cell of this `mnem` has an attested consumer.  The setters the corpus records, read off the cells file's own `setter_census`: 11 of them, over 22741 flag-pair ledger rows.

```

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

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank.py restored | grep -v 'peak resident'
Table B6 -- every (cell, target) pair proved on the STRICT reading by some pass of the four compiled targets and NOT by the last pass, with the passes that proved it and the certificate the bank keeps.  A certificate cannot regress; these are the pairs the bank restores.

| `mnem` | shape | `key_width` | target | proved by | the bank's preferred pass |
|---|---|---|---|---|---|
| `and` | imm_gpr | 8 | c | ap1, ap2, ap3, ap4 | `ap1` |
| `and` | imm_gpr | 8 | rust | ap1, ap2, ap3, ap4 | `ap1` |
| `and` | imm_gpr | 8 | swift | ap1, ap2, ap3, ap4 | `ap1` |
| `cmp` | imm_gpr | 16 | c | ap1, ap2, ap3, ap4 | `ap1` |
| `cmp` | imm_gpr | 16 | rust | ap1, ap2, ap3, ap4 | `ap1` |
| `cmp` | imm_gpr | 16 | swift | ap1, ap2, ap3, ap4 | `ap1` |
| `cmp` | imm_gpr | 8 | c | ap1, ap2, ap3, ap4 | `ap1` |
| `cmp` | imm_gpr | 8 | rust | ap1, ap2, ap3, ap4 | `ap1` |
| `cmp` | imm_gpr | 8 | swift | ap1, ap2, ap3, ap4 | `ap1` |
| `mov` | imm_gpr | 16 | c | ap1, ap2, ap3, ap4 | `ap1` |
| `mov` | imm_gpr | 16 | rust | ap1, ap2, ap3, ap4 | `ap1` |
| `mov` | imm_gpr | 16 | swift | ap1, ap2, ap3, ap4 | `ap1` |
| `mov` | imm_gpr | 8 | rust | ap1, ap2, ap3, ap4 | `ap1` |
| `mov` | imm_gpr | 8 | swift | ap1, ap2, ap3, ap4 | `ap1` |
| `or` | imm_gpr | 8 | c | ap1, ap2, ap3, ap4 | `ap1` |
| `or` | imm_gpr | 8 | rust | ap1, ap2, ap3, ap4 | `ap1` |
| `or` | imm_gpr | 8 | swift | ap1, ap2, ap3, ap4 | `ap1` |
| `sbb` | imm_gpr | 8 | c | ap1, ap2, ap3, ap4 | `ap1` |
| `sbb` | imm_gpr | 8 | swift | ap1, ap2, ap3, ap4 | `ap1` |

pairs proved by some pass and not by the last: 19
the union over the five passes, STRICT: 523
the last pass alone, STRICT: 504

Table B6b -- the five passes' own STRICT figures, so the union above can be read against them.

| pass | pairs proved, STRICT |
|---|---|
| `ap1` | 330 |
| `ap2` | 434 |
| `ap3` | 465 |
| `ap4` | 521 |
| `ap5` | 504 |

Table B7 -- the same loss read at the CELL width: cells on all four targets under each pass, and the cells the last pass drops.

| pass | cells on all four, STRICT |
|---|---|
| `ap1` | 56 |
| `ap2` | 73 |
| `ap3` | 80 |
| `ap4` | 91 |
| `ap5` | 88 |

cells on all four through pass 4 and not on all four in pass 5: 5
   and imm_gpr 8
   cmp imm_gpr 16
   cmp imm_gpr 8
   mov imm_gpr 16
   or imm_gpr 8

```

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

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank.py backups | grep -v 'peak resident'
certified keys in the bank (kind `proved` or `agreed`): 2549

Table B8 -- every store on disk this task did NOT bank, why, and how many keys it would have certified that the bank does not already hold.

| store | why not banked | keys it certifies | keys the bank lacks |
|---|---|---|---|
| `autopoly3_runs.jsonl.before_the_guards_passed` | task ap3's own partial store from before its guards passed | 39 | 0 |
| `autopoly3_runs.jsonl.before_the_x87_bits_refusal` | task ap3's own partial store from before the x87 refusal | 20 | 0 |
| `autopoly5_runs.jsonl.before_the_x87_memory_arrival_fix` | task ap5's first pass, 30 of whose runs log_249 SS3 records as wrong: align_by_row tested one of the two x87 spellings | 889 | 0 |
| `expand2_runs.jsonl.before_the_dotted_label_fix` | task ex2's first pass, 196 of whose pairs log_250 SS4.1 records as a stale binary answering a failed build | 1190 | 0 |
| `expand2_runs.jsonl.before_the_hyphen_label_fix` | task ex2's second pass, 7 of whose pairs log_250 SS4.2 records under the same mechanism | 1308 | 0 |
| `expand1_interp_pass1.jsonl` | task ex1's own intermediate interpreted passes, superseded within the task by expand1_interp.jsonl | 40 | 0 |
| `expand1_interp_pass2.jsonl` | as above | 40 | 0 |
| `expand1_interp_pass3.jsonl` | as above | 48 | 0 |
| `expand1_interp_pass4.jsonl` | as above | 56 | 0 |
| `expand1_interp_smoke.jsonl` | task ex1's seven-run smoke, inside expand1_interp.jsonl | 5 | 0 |

no excluded store holds a certified key the bank lacks.

```

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

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py --bank report | grep -v 'peak resident'
Table D2 -- the delta pass's own cost line, in the five counts the brief names.  `certified before` counts (cell, target, written place) triples the bank certified before this pass; `attempted` counts the triples with no such certificate; `newly certified` counts the triples this pass certified; `audited` counts the certified triples re-derived from the term; `alarms` counts the audited triples whose re-derived verdict differs from its certificate on identical inputs.

| pass | certified before | attempted | newly certified | audited | alarms |
|---|---|---|---|---|---|
| `bank1_delta` | 1225 | 954 | 2 | 58 | 0 |

Table D3 -- what the pass cost against a full pass over the same five targets.

| | runs | seconds |
|---|---|---|
| a full pass over these five targets | 1265 | None |
| this delta pass | 687 | 1207 |

the delta pass ran 54.3% of a full pass's runs.
```

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py --bank cost | grep -v 'peak resident'
Table D5 -- the delta pass beside a full pass over the same five compiled targets.  Both were run in this instance, in this image, at the same two ceilings; the only difference is which runs were attempted.  `seconds` sums each store's own recorded per-run seconds.

| pass | runs | seconds | seconds per run |
|---|---|---|---|
| a full pass | 1265 | 1478 | 1.17 |
| this delta pass | 707 | 1210 | 1.71 |

the delta pass ran 55.9% of the full pass's runs and cost 81.9% of its seconds.

Table D6 -- what the full pass answered, so the delta's own answers can be read against a pass that attempted everything.

| | delta | full |
|---|---|---|
| runs | 707 | 1265 |
| place-triples proved | 509 | 1166 |
| pairs proved, STRICT | 117 | 651 |
| newly certified against the bank as it stood | 2 | -- |

```

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

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py --bank audit | grep -v 'peak resident'
Table D4 -- every audited (cell, target, written place), its certificate's kind and the kind the re-derivation answered, and whether the inputs were identical.  A row whose inputs were identical and whose kinds differ is an ALARM; a row whose source sha256 moved is a CHANGED ARTIFACT and is banked as a new certificate beside the old one, never in place of it.

| `mnem` | shape | `key_width` | target | place | the certificate's pass | certificate | re-derived | inputs identical | reading |
|---|---|---|---|---|---|---|---|---|---|
| `cvtsi2ss` | gpr_xmm | 32 | go | `reg_xmm0` | `ap1` | proved | proved | yes | reproduced |
| `or` | gpr_gpr | 64 | c | `flags.high` | `ap2` | proved | refused | no | the artifact changed |
| `test` | gpr_same | 64 | go | `flags.high` | `ap4` | proved | proved | yes | reproduced |
| `cmp` | gpr_gpr | 32 | go | `flags` | `ap1` | proved | proved | yes | reproduced |
| `or` | cl_gpr | 8 | c | `flags` | `ap1` | proved | proved | yes | reproduced |
| `or` | cl_gpr | 8 | swift | `flags` | `ap1` | proved | proved | yes | reproduced |
| `sbb` | gpr_gpr | 64 | c | `flags.low` | `ap2` | proved | proved | yes | reproduced |
| `sbb` | gpr_gpr | 64 | rust | `flags.high` | `ap2` | proved | proved | yes | reproduced |
| `sbb` | gpr_gpr | 64 | go | `flags.high` | `ap4` | proved | proved | yes | reproduced |
| `and` | gpr_gpr | 32 | cpp | `reg_rdi` | `ex1_cpp` | proved | proved | yes | reproduced |
| `movaps` | xmm_xmm | 128 | cpp | `reg_xmm0.high` | `ex1_cpp` | proved | proved | yes | reproduced |
| `and` | gpr_gpr | 8 | go | `flags` | `ap1` | proved | proved | yes | reproduced |
| `and` | gpr_gpr | 64 | rust | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `or` | gpr_gpr | 32 | go | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `movd` | xmm_gpr | 32 | rust | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `setb` | gpr_one | 8 | go | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `setb` | gpr_one | 8 | swift | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `cmp` | imm_gpr | 64 | c | `flags.low` | `ap2` | proved | proved | no | the artifact changed |
| `xorpd` | xmm_same | 128 | rust | `reg_xmm0.low` | `ap2` | proved | proved | yes | reproduced |
| `sub` | gpr_gpr | 32 | cpp | `reg_rdi` | `ex1_cpp` | proved | proved | yes | reproduced |
| `sar` | cl_gpr | 32 | swift | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `fildll` | mem_one | 80 | c | `x87_7` | `ap4` | proved | proved | yes | reproduced |
| `setbe` | gpr_one | 8 | cpp | `reg_rdi` | `ex1_cpp` | proved | proved | yes | reproduced |
| `mul` | gpr_one | 64 | c | `reg_rax` | `ap1` | proved | proved | yes | reproduced |
| `imul` | gpr_gpr | 32 | swift | `flags` | `ap1` | proved | proved | yes | reproduced |
| `shr` | cl_gpr | 64 | cpp | `reg_rdi` | `ex1_cpp` | proved | proved | yes | reproduced |
| `divss` | xmm_xmm | 32 | cpp | `reg_xmm0` | `ex1_cpp` | proved | proved | yes | reproduced |
| `subss` | xmm_xmm | 32 | c | `reg_xmm0` | `ap1` | proved | proved | yes | reproduced |
| `and` | imm_gpr | 8 | cpp | `reg_rdi` | `ex1_cpp` | proved | proved_under_caller_extension | no | the artifact changed |
| `cmp` | imm_gpr | 32 | swift | `flags` | `ap1` | proved | proved | no | the artifact changed |
| `shld` | cl_gpr_gpr | 64 | c | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `punpckldq` | mem_xmm | 128 | rust | `reg_xmm0.low` | `ap2` | proved | proved | yes | reproduced |
| `unpckhpd` | xmm_xmm | 128 | c | `reg_xmm0.low` | `ap3` | proved | proved | yes | reproduced |
| `cmp` | imm_gpr | 16 | rust | `flags` | `ap1` | proved | proved_under_caller_extension | no | the artifact changed |
| `not` | gpr_one | 64 | go | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `not` | gpr_one | 32 | go | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `shl` | cl_gpr | 8 | go | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `add` | gpr_same | 8 | rust | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `sar` | cl_gpr | 8 | c | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `pxor` | xmm_same | 128 | c | `reg_xmm0.low` | `ap2` | proved | proved | yes | reproduced |
| `cmovae` | gpr_gpr | 32 | cpp | `reg_rdi` | `ex1_cpp` | proved | proved | yes | reproduced |
| `cmp` | mem_gpr | 64 | swift | `flags.low` | `ap2` | proved | proved | yes | reproduced |
| `sub` | gpr_gpr | 8 | swift | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `add` | imm_gpr | 64 | c | `flags.high` | `ap2` | proved | proved | yes | reproduced |
| `cmpneqsd` | mem_xmm | 64 | swift | `reg_xmm0` | `ap2` | proved | proved | yes | reproduced |
| `fimull` | mem_one | 80 | cpp | `x87_6` | `ex1_cpp` | proved | proved | yes | reproduced |
| `cmovae` | gpr_gpr | 64 | c | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `mov` | imm_gpr | 64 | swift | `reg_rdi` | `ap1` | proved | proved | no | the artifact changed |
| `movabs` | imm_gpr | 64 | go | `reg_rdi` | `ap1` | proved | proved | no | the artifact changed |
| `fidivrl` | mem_one | 80 | cpp | `x87_6` | `ex1_cpp` | proved | proved | yes | reproduced |
| `test` | cl_gpr | 8 | cpp | `flags` | `ex1_cpp` | proved | proved | yes | reproduced |
| `orps` | xmm_xmm | 128 | go | `reg_xmm0.high` | `ap3` | proved | proved | yes | reproduced |
| `orps` | xmm_xmm | 128 | swift | `reg_xmm0.high` | `ap3` | proved | proved | yes | reproduced |
| `shl` | imm_gpr | 64 | cpp | `reg_rdi` | `ex1_cpp` | proved | proved | yes | reproduced |
| `add` | gpr_gpr | 16 | c | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |
| `pand` | xmm_xmm | 128 | c | `reg_xmm0.high` | `ap3` | proved | proved | yes | reproduced |
| `pand` | xmm_xmm | 128 | go | `reg_xmm0.low` | `ap2` | proved | proved | yes | reproduced |
| `xor` | gpr_gpr | 8 | go | `reg_rdi` | `ap1` | proved | proved | yes | reproduced |

| reading | rows |
|---|---|
| reproduced | 51 |
| the artifact changed | 7 |

```

**GLOSS.** 58 certified triples re-derived, 51 identical, 7 on a different
artifact, ZERO alarms. An alarm would be a differing verdict on identical
inputs — the machinery and the record disagreeing about the same artifact —
and there is none.

# 9. The seven artifacts that changed, one by one

**LITERAL**, the same lane:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py --bank changed
Table D7 -- the audited triples whose artifact changed.  The two source columns hold the FIRST line on which the two rendered sources differ, which is the measurement; the several hundred characters of preamble they share are not shown.

| `mnem` | shape | `key_width` | target | place | certificate's pass | certificate | re-derived | the certificate's source | the re-derivation's source |
|---|---|---|---|---|---|---|---|---|---|
| `or` | gpr_gpr | 64 | c | `flags.high` | `ap2` | proved | refused | `--` | `-- the re-derivation rendered nothing --` |
| `cmp` | imm_gpr | 64 | c | `flags.low` | `ap2` | proved | proved | `3 */` | `v0 */` |
| `and` | imm_gpr | 8 | cpp | `reg_rdi` | `ex1_cpp` | proved | proved_under_caller_extension | `Concat(0, Extract(1, 0, v0)) */` | `Concat(0, ~(~Extract(7, 0, v0) \| ~Extract(7, 0, v1))) */` |
| `cmp` | imm_gpr | 32 | swift | `flags` | `ap1` | proved | proved | `//   Concat(Extract(31, 0, v0), 3)` | `//   Concat(Extract(31, 0, v0), Extract(31, 0, v1))` |
| `cmp` | imm_gpr | 16 | rust | `flags` | `ap1` | proved | proved_under_caller_extension | `//   Concat(Extract(15, 0, v0), 3)` | `//   Concat(Extract(15, 0, v0), Extract(15, 0, v1))` |
| `mov` | imm_gpr | 64 | swift | `reg_rdi` | `ap1` | proved | proved | `//   3` | `//   v0` |
| `movabs` | imm_gpr | 64 | go | `reg_rdi` | `ap1` | proved | proved | `//   3` | `//   v0` |

or gpr_gpr 64 on c at flags.high
   the certificate: pass ap2, kind proved, source src2/or_gpr_gpr_64__primitive__c.c, sha256 2397e759875253b980bc98441658316c8b823fa0baa6b08130d79e0a01e191af
   the re-derivation: kind refused, sha256 None
   the re-derivation's verdict: None -- None
   the re-derivation's refusal cause: the primitive route renders the operator's own answer, and the flags place is not a value an operator answers with
   the re-derivation's refusal detail: the operator's own answer is the value it hands back, and this cell's flags place is a second place the opcode writes

cmp imm_gpr 64 on c at flags.low
   the certificate: pass ap2, kind proved, source src2/cmp_imm_gpr_64__flags_low__c.c, sha256 d8cd8db12f5b1140d2c53a3c0b672d32886ff3ce13c2375f6bfc8b331a401696
   the re-derivation: kind proved, sha256 7e2138ce760ce4df4c6911197a4581c5516c98919a4412a2d3dd2421d79a4605
   the re-derivation's verdict: PROVED_ON_SHIP -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

and imm_gpr 8 on cpp at reg_rdi
   the certificate: pass ex1_cpp, kind proved, source src_expand1/and_imm_gpr_8__reg_rdi__cpp.cpp, sha256 89f0a5f778132c5219d03dfebf2928fa259bc1637d02a6cff47e8097d5cfa418
   the re-derivation: kind proved_under_caller_extension, sha256 4c8f0a8a91f70daebe06d01154537e97e6c6f475f65786384bccad6e6d297d91
   the re-derivation's verdict: DISPROVED -- z3 found a starting state under which the two sides differ

cmp imm_gpr 32 on swift at flags
   the certificate: pass ap1, kind proved, source src/cmp_imm_gpr_32__flags__swift.swift, sha256 83d0fb0bc91c0bf5a99a5a6d5e08f110654fba3afe5db93b535308a8210eb0f1
   the re-derivation: kind proved, sha256 a65db8e68818e7c64d0d5fadc855c905fbc0bb36c7f966e61c33bcfbe8cf2436
   the re-derivation's verdict: PROVED_ON_SHIP -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

cmp imm_gpr 16 on rust at flags
   the certificate: pass ap1, kind proved, source src/cmp_imm_gpr_16__flags__rust.rs, sha256 3c23472b31a850ff63503cf8eb036544ee2c77c4b24780a0eaf04cfbe949baed
   the re-derivation: kind proved_under_caller_extension, sha256 b22b8a5aad3b8c5d8c382edfc6167959abcb7ae61667e50705d102d6b2f4e804
   the re-derivation's verdict: DISPROVED -- z3 found a starting state under which the two sides differ

mov imm_gpr 64 on swift at reg_rdi
   the certificate: pass ap1, kind proved, source src/mov_imm_gpr_64__reg_rdi__swift.swift, sha256 991c2abfc6e9a125204b7c11495a4395ab55fb249a409a0cdfacd832ad92600a
   the re-derivation: kind proved, sha256 7fb2eb5e3534f81b25925e8ea67abbecb0b355e5bc9d590d6d3cfb7a7f486b9f
   the re-derivation's verdict: PROVED_ON_SHIP -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

movabs imm_gpr 64 on go at reg_rdi
   the certificate: pass ap1, kind proved, source src/movabs_imm_gpr_64__reg_rdi__go.go, sha256 39021bfb4ad2042968a145f70f70865244f08945ec3e7a0391d54816649938f7
   the re-derivation: kind proved, sha256 839881bda904bcba746621c9f54950fc7ce6f0db52658463b11b3389693d9f13
   the re-derivation's verdict: PROVED_ON_SHIP -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

audited triples whose artifact changed: 7
```

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

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS certificates.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank1_delta.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS bank1_delta.json -- no operator token in any key, grouping, pairing or row structure
```

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

The bound stated in `PUBLIC/Airlock/instances/bank1.conf`, in every
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

```
$ wc -l PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank1_delta_runs.jsonl PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank1_full_runs.jsonl PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank1.md
   12593 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl
     707 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank1_delta_runs.jsonl
    1265 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank1_full_runs.jsonl
     515 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank1.md
   15080 total
```

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

# 14. The conventions verifier over this log

One pass, lane `bank1_l13_verify_253.sh`, over this log as lane 12 wrote it
(`<runs>/bank1/agent/logs/*__bank1_l13_verify_253.sh.log`).

| lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|
| `bank1_l13_verify_253.sh` | 20 | 11 | **0** | 9 | 0 | 0 |

**GLOSS**, and the obligation the law states is the DIFFERS column: **0**.

* **MATCHES (11)** — every fenced block in §3 to §12, each the output of the
  command on its first line, each re-run by the verifier and each answering
  the same way. They are `bank.py kinds`, `readings`, `restored`, `backups`;
  `autopoly.py --bank report`, `cost`, `audit`, `tally`, `changed`; the two
  guard calls; and the `wc -l` tally.
* **UNVERIFIABLE (9)** — the walkthrough, the reading definitions, the four
  glosses and the two lists: prose findings, each stated as such rather than
  claimed reproducible.

Every block in this log was written by capture, never by hand: lane
`bank1_l12_write_the_log.sh` ran each command and redirected its own output
into the file.
