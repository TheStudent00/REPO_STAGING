# log 255 — task ap6: one driver with no task-name gates, consumers over every posed setter cell, holders on the primitive lookup, and re-attempts by code version

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_ap6_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`.
Instance `ap6`; every lane on the tower, logs at
`<runs>/ap6/agent/logs/`; lane scripts kept at
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap6/`.

This task was started by one agent and finished by another after a usage
limit; §11 says exactly which part each did, because the record should
not pretend it was one sitting.

---

# 1. What this is, one sentence per object in relation

* **The DRIVER** is
  `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py`:
  given one arch table CELL and one target language it renders the cell's
  term as source, compiles it, carves the body out and puts the two to z3.
* **A CELL** is one (`mnem`, operand shape, `key_width`) row of the arch
  opcode model table — the machine-form key of the ruling of 2026-09-08.
* **A TASK-NAME GATE** was a branch in the driver switched on by which
  task was running (`use_task_ap4()` and eight more), so that an older
  pass reproduced verbatim. This task removes all nine.
* **THE CODE VERSION** is the sha256 of the driver's source, of the loop's
  and of the target's renderer, recorded on every run this task's loop
  writes; it is what replaced the task label.
* **THE LOOP** is
  `.../emulation/autopoly/autopoly.py`, which walks the outer set of 253
  cells over five compiled targets; in BANK MODE it attempts only what
  the bank does not certify and audits a sample of what it does.
* **THE BANK** is `.../emulation/autopoly/certificates.jsonl`, one
  certificate per (cell, target, written place, SETTER CELL) key, built
  by `.../emulation/autopoly/bank.py` from every run store on disk.
* **A SETTER CELL** is the arch cell that wrote the flag state a flag
  CONSUMER reads. The pair is the node, so the pair is the key.
* **THE PRIMITIVE ROUTE** asks whether the target already has an operator
  whose whole lowered body IS this cell, and renders that instead of the
  term; its LOOKUP now carries the matched body's parameter HOLDERS.
* **THE HOLDER** is the typed slot a parameter sits in; the TRUTH holder
  (`bool` in c, cpp, rust and go, `Bool` in swift) holds 0 or 1 and is
  not a faithful holder of a register.
* **THE NARROW-ANSWER RE-POSE** is the gate asked a second time with both
  sides cut to the bits the node itself answers in, beside task o7's
  caller-extension re-pose for narrow arguments.

---

# 2. The walkthrough, before any figure

Take `setne gpr_one 8` on c. It reads a flag state, so before 2026-09-10
the driver built ONE held cell for it: the flags of `add gpr_gpr 8`,
because `add` is the setter mnemonic the corpus records the most ledger
rows for before `setne`. One held cell, one render, one compile, one gate
call, one certificate — and every other pair the corpus attests before
`setne` was not answered at all, not even by a refusal.

It now builds thirty-one: `test` in five operand shapes at width 8, `cmp`
in seven, `or` in six, `add` in seven, and the rest. Each is rendered,
compiled, carved and gated on its own, and each leaves its own
certificate, because the same consumer over another setter is another
artifact. The thirty-one are not a cross product: the corpus attests a
setter by MNEMONIC only, so the driver joins that attestation to the
sweep's own rows to get cells, and then keeps only the cells the SWEEP
POSED — the ones where the consumer has a TRANSLATED row seeded by that
setter and the setter's flag values are the width of the consumer's flag
arrival. 2,674 cells come out of the join for the 39 flag consumers of
the outer set; 384 are posed; the other 2,290 are counted and stated by
cause, once, in §5, rather than banked as a run per target.

Then take `add gpr_gpr 64` on c. The primitive lookup matched a corpus
body whose one instruction classifies to that cell, and rendered it — but
the body's own parameter sits in c's `bool`. A `bool` parameter holds 0
or 1, so the compiler is free to lower an operation over it to something
correct for those two values and wrong for every other byte of the
register, and the gate DISPROVED it (task ap5, log 249). The same family
left three c entries and two rust entries PROVED in the bank and unusable
by any composition (task hub1, log_252 §7). The lookup now matches on the
holders too: it tries the members of every row that classifies to the
cell until one fits the cell's own width with no truth holder, and where
none does it refuses BY CAUSE and the run takes the term route, which
renders the cell at a holder of its own width.

---

# 3. The gates: nine before, none after

**LITERAL**, lane `ap6_l1b` §[2/7] and §[3/7], tower log
`<runs>/ap6/agent/logs/20260910T062244Z__ap6_l1b_preflight_and_the_gate_count.sh.log`:

```
[2/7] THE GATES BEFORE: the driver as it stood this morning

a task entry: 39
a task label: 36
an opcode name: 2
task-name gates: 75
opcode-name branches: 2

  the task ENTRIES it carried, one per gate:
9
382:def use_task_h2():
394:def use_task_g1():
410:def use_task_g1b():
430:def use_task_g1c():
444:def use_task_ap2():
463:def use_task_ap3():
481:def use_task_ap4():
499:def use_task_ap5():
517:def use_task_ex1():

[3/7] THE GATES AFTER: the one driver, and the loop over it
the arch mnemonic vocabulary: 142 tokens, read off autopoly5_cells.json and off task o2's own chaff tables

| file | line | what is compared | kind | the line |
|---|---|---|---|---|
| handful.py | 3537 | `ret` | an opcode name | `if mnem == "ret":` |

an opcode name: 1
task-name gates: 0
opcode-name branches: 1

  task entries left in the driver:
0
```

**GLOSS.** Nine task entries, seventy-five branches switched on a task
label, gone. The checker is
`.../emulation/check_no_task_gates.py`, which parses the file and reports
every branch whose condition compares against a task label or an arch
mnemonic; `handful_frozen.py` is `handful.py` as it stood before the
strip, so the two runs of one checker over two files are the before and
the after. The one branch left compares against `ret`, which is the
return instruction and not an operand mapping — it is how the carver
finds the end of a body.

**THE GREP THE BRIEF ASKS FOR**, lane `ap6_l17` §[5/5]:

```
$ cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful && grep -n 'TASK in (\|def use_task_\|mnem *== *"' handful.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.py
handful.py:3824:        if mnem == "ret":
```

---

# 4. THE 100% AUDIT — the guard on the gate removal

Every certificate the bank held for the five compiled targets was
re-derived once through the gate-free driver: 1,227 certified
place-triples, 962 runs, 645 seconds.

**LITERAL**, lane `ap6_l4` §[1/1], tower log
`<runs>/ap6/agent/logs/20260910T062531Z__ap6_l4_the_hundred_percent_audit.sh.log`:

```
[1/1] THE 100% AUDIT, whole
certified before: 1227 place-triple(s)
attempted: 0 place-triple(s) over 0 run(s)
audited: 1227 place-triple(s), seed '2026-09-10'
runs to execute: 962
...
runs performed this lane: 942 in 644 s
lines on PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/ap6_audit_runs.jsonl: 962
audited place-triples this lane: 1198
alarms: 0
peak resident: 304716 kB
```

**GLOSS, and the scope stated exactly.** `--attempts off` leaves only the
audit, so what this measures is re-derivation and nothing else. It ran
against the driver with the gates stripped and BEFORE the three changes
of §5, §6 and §7, which is what makes it the guard on the gate removal
and on nothing else: those three changes are meant to move artifacts, and
each carries its own guard below. **0 alarms** — no certificate's verdict
moved on identical inputs when the nine gates were taken out.

---

# 5. Consumers over every posed setter cell

## 5.1 Where the setter cells come from, and why it is not the token

Two machine-form readings joined, in
`handful.attested_setter_cells` / `handful.derived_setter_cells`:

| the reading | what it gives | where it is on disk |
|---|---|---|
| the consumer cell's own `attestation.setter` | which setter MNEMONICS the corpus records before this consumer, with the flag-pair ledger rows for each — task m1b's reading | `.../autopoly/autopoly5_cells.json`, on every row of every asked cell |
| the outer set's own `setter_rows` | which CELLS each of those mnemonics has, each already carrying its operand shape and its `key_width`, classified off the row's own LINE by `model_table.classify_line` when the outer set was built | the same file, key `setter_rows`, 1,122 rows |

Neither is a reading of a name; `mnem` is the guard-exempt field of the
machine-form key. The corpus records a flag pair as (setter `mnem`,
consumer `mnem`) and carries no operand shape and no width on the setter
side — the same sentence `bank.py` and log_253 §4 already carry — so the
cell granularity has to come from the sweep, and the join is what makes
the pair.

## 5.2 The census: 2,674 offered, 384 posed

**LITERAL**, lane `ap6_l9` §[2/4], tower log
`<runs>/ap6/agent/logs/20260910T071924Z__ap6_l9_delta_preflight_and_sample.sh.log`:

```
[2/4] THE SETTER CELL CENSUS over the outer set
| what | count |
|---|---|
| asked cells that read an arriving flag state | 39 |
| setter cells the corpus attests before them | 2674 |
| of them, held cells the sweep POSED and the driver builds | 384 |
| of those, at the consumer's own `key_width` | 368 |
| offered by the join and not posed by the sweep | 2290 |

| the cause it was not posed | count |
|---|---|
| the setter's flag values and the consumer's flag arrival are of different widths | 1452 |
| no TRANSLATED row at this cell whose arriving flag state was written by this setter | 838 |

| consumer `mnem` | shape | `key_width` | held cells |
|---|---|---|---|
| `setne` | gpr_one | 8 | 31 |
| `sete` | gpr_one | 8 | 31 |
| `setg` | gpr_one | 8 | 21 |
| `setle` | gpr_one | 8 | 21 |
| `setb` | gpr_one | 8 | 21 |
| `cmove` | gpr_gpr | 32 | 21 |
| `cmovne` | gpr_gpr | 64 | 14 |
| `cmove` | gpr_gpr | 64 | 14 |
| `cmovb` | gpr_gpr | 64 | 14 |
| `cmovae` | gpr_gpr | 64 | 14 |
| `cmovl` | gpr_gpr | 64 | 14 |
| `cmovge` | gpr_gpr | 64 | 14 |
```

**GLOSS.** The two causes are properties of the OUTER SET and of neither
target nor compiler, so recording them as a run per target would write the
same sentence five times about a pair no proof was ever posed for — 11,450
records saying nothing. `handful.setter_cell_census` states them once,
by cause; `handful.cell_inputs` keeps the 384 plus the one held cell per
consumer the loop always built, which is why the per-consumer column
reads 31 where the census counted 30.

**Reproducing it**, from the instance:

```
$ python3 -c "import sys, json; sys.path.insert(0, 'PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful'); sys.path.insert(0, 'PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly'); import autopoly as AP, handful as H; c = H.setter_cell_census(json.load(open(AP.CELLS))); print(c['consumers'], c['setter_cells_attested'], c['held_cells_built'], sum(c['refused_by_cause'].values()))"
39 2674 384 2290
```

## 5.3 The guard: hub2's pair entries, and hub2's pair holes

**LITERAL**, lane `ap6_l15` §[1/1], tower log
`<runs>/ap6/agent/logs/20260910T081736Z__ap6_l15_the_pair_guard_by_kind.sh.log`:

```
[1/1] every pair entry hub2 serves, at its own kind
| what | count |
|---|---|
| pair-level entries task hub2's dictionary serves | 111 |
| of them, the bank still holds AT THE ENTRY'S OWN KIND | 111 |
| REGRESSED: the bank no longer holds that kind | 0 |

| the kind the entry was served at | entries |
|---|---|
| `proved` | 105 |
| `proved_under_caller_extension` | 6 |
```

**LITERAL**, lane `ap6_l17` §[2/5], tower log
`<runs>/ap6/agent/logs/`, under that lane's own stamp:

```
[2/5] THE PAIR GUARD, the other half: the pairs hub2 could
          NOT serve because the loop rendered one setter
| what | count |
|---|---|
| pair-level holes task hub2 recorded | 111 |
| of them, the bank now holds a certificate of ANY kind | 9 |
| of them, the bank now certifies `proved` | 9 |
```

**GLOSS.** Nothing hub2 served regressed: all 111 pair-level entries of
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/dictionary2.json` are still
carried by the bank at the kind they were served at. Nine of the 111 pair
HOLES hub2 recorded — pairs the corpus attests that the loop could not
answer because it rendered one setter — are now certified `proved`. The
other 102 are pairs at a width the sweep never posed, which is the second
row of §5.2's cause table and is now a stated cause rather than a silence.

## 5.4 The pair-level certificates, before and after

| what | before this task's pass | after |
|---|---|---|
| certificates on the bank | 12,593 | 19,455 |
| of them, PAIR-LEVEL (a setter cell on the key) | 2,623 | 7,519 |
| distinct (consumer cell, setter cell) pairs | 39 | 397 |

*(before: lane `ap6_l2` §[5/7], tower log
`.../20260910T062339Z__ap6_l2_rebank_and_the_guard.sh.log`; after: lane
`ap6_l13` §[4/9], tower log
`.../20260910T081439Z__ap6_l13_rebank_readings_and_the_guards.sh.log`.)*

**LITERAL**, the after, lane `ap6_l13` §[4/9]:

```
[4/9] THE PAIR-LEVEL CERTIFICATES, after this task's pass
| what | count |
|---|---|
| certificates on the bank | 19455 |
| of them, PAIR-LEVEL (a setter cell on the key) | 7519 |
| distinct (consumer cell, setter cell) pairs | 397 |

| kind | pair-level certificates |
|---|---|
| `proved` | 2570 |
| `proved_under_caller_extension` | 151 |
| `refused` | 3927 |
| `sat` | 812 |
| `undecided` | 59 |
```

---

# 6. The primitive lookup carries the matched body's holders

Two conditions, both machine form, in `handful.holders_fit`: NO TRUTH
HOLDER (the manifest records a parameter's REPRESENTATION and `bool` is
the truth one), and THE WIDTH IS THE CELL'S (a parameter must be as wide
as the cell's own `key_width`). Members of every row that classifies to
the cell are tried in order until one fits; where none does, the lookup
refuses by cause and the run takes the term route.

**LITERAL**, lane `ap6_l17` §[3/5]:

```
[3/5] THE HOLDERS GUARD, on the outer set the loop walks
| cell | target | the lookup's answer | the holders it matched |
|---|---|---|---|
| `and` gpr_gpr 32 | c | matched `mov %edi,%eax; and %esi,%eax; ret` | i32 in `int32_t`, i32 in `int32_t` |
| `or` gpr_gpr 32 | c | matched `mov %edi,%eax; or %esi,%eax; ret` | i32 in `int32_t`, i32 in `int32_t` |
| `not` gpr_one 32 | c | matched `mov %edi,%eax; not %eax; ret` | i32 in `int32_t` |
| `and` gpr_gpr 32 | rust | matched `mov %edi,%eax; and %esi,%eax; ret` | i32 in `i32`, i32 in `i32` |
| `or` gpr_gpr 32 | rust | matched `mov %edi,%eax; or %esi,%eax; ret` | i32 in `i32`, i32 in `i32` |
| `add` gpr_gpr 64 | c | refused by cause: every member of every row that classifies to this cell is written over holders the cell's own operands do not fit | 4 member(s) refused; the first: the member's parameter 0 sits in the target's TRUTH holder (`bool`), which holds 0 or 1 and is not a faithful holder of a register |
```

**GLOSS, and it is the answer the brief's guard asked for.** Task hub1's
five unusable entries (log_252 §7: three on c, two on rust) all became
USABLE — the lookup walked past the truth-holder members and matched a
member at `int32_t` / `i32`, the cell's own width. The sixth row is task
ap5's `add gpr_gpr 64` on c, the same family: every one of its four
members sits in c's truth holder, so the lookup REFUSES BY CAUSE at the
loop, which is the other of the two answers the brief allowed. Neither is
a placeholder and neither is a per-name patch: one rule over one table.

---

# 7. The gate's narrow-answer re-pose

`handful.decided` takes the node's own answer width and, where it is
narrower than BOTH sides, cuts both to it in the re-pose, beside task
o7's caller extension. A caller that states nothing gets exactly the
re-pose o7 wrote; a loop whose node IS the place it compares never
reaches the cut.

**LITERAL**, lane `ap6_l17` §[4/5]:

```
[4/5] THE NARROW-ANSWER GUARD: hub2's own sighting, posed
          with the node's answer width stated and without it
| the node's answer width | the gate, as posed | the re-pose |
|---|---|---|
| not stated | DISPROVED | not reached |
| 8 bits | DISPROVED | PROVED_ON_SHIP, cut to 8 bits |
```

**GLOSS.** The object is task hub2's own sighting, `go/regen_146`
(log_254 §8, cause 2): go's body divides at 16 bits and leaves the
quotient in the low eight with the REMAINDER above it, the composed c
body divides at 8 and leaves the remainder in bits 8 to 15, both
quotients agree, and the node answers in `uint8`. The strict verdict is
unchanged — DISPROVED, as it must be, because the two DO differ above the
node's eight bits — and the re-pose now says what hub2's second list asked
to be said. It is a re-pose and it is recorded beside the first verdict,
never in place of it, exactly as the caller extension is.

**THE HUB WAS NOT TOUCHED.** `hub.py` and `hub2.py` are outside this
task's artifact folder and the brief forbids changing them; the re-pose
is in the driver, and the hub reaches it through `H.decided` the moment
its caller states a node width. That is one line in a file that is not
this task's, and it is in the second list.

---

# 8. The delta pass, its cost, and the three readings

## 8.1 The cost line, beside log_253's

**LITERAL**, lane `ap6_l13` §[7/9]:

```
Table D3 -- what the pass cost against a full pass over the same five targets.

| | runs | seconds |
|---|---|---|
| a full pass over these five targets | 1265 | None |
| this delta pass | 2499 | 2224 |

the delta pass ran 197.5% of a full pass's runs.
```

```
Table D5 -- the delta pass beside a full pass over the same five compiled targets.  Both were run in this instance, in this image, at the same two ceilings; the only difference is which runs were attempted.  `seconds` sums each store's own recorded per-run seconds.

| pass | runs | seconds | seconds per run |
|---|---|---|---|
| a full pass | 1265 | 1478 | 1.17 |
| this delta pass | 2499 | 2172 | 0.87 |

the delta pass ran 197.5% of the full pass's runs and cost 146.9% of its seconds.
```

**GLOSS, and the number needs its sentence.** log_253's delta ran 707
runs, 55.9% of a full pass, and cost 81.9% of its seconds. This one ran
2,499 — 197.5% of a full pass — and cost 146.9%. It is not a regression
in the delta rule; it is the loop getting BIGGER. A pair is no longer one
run: a flag consumer is one run per setter cell the sweep posed, so 709
(cell, target) pairs became 2,499 runs. The seconds per run FELL from
1.17 to 0.87, because the added runs are 8-bit flag pairs the solver
answers quickly. The delta rule itself is intact and measured: `held by
the code version` is 0 this pass, because the driver's own sha256 moved
when the gates were stripped, so nothing was held back — which is exactly
what the rule is for.

The cost line in the five counts the brief named:

```
Table D2 -- the delta pass's own cost line, in the five counts the brief names.  `certified before` counts (cell, target, written place) triples the bank certified before this pass; `attempted` counts the triples with no such certificate; `newly certified` counts the triples this pass certified; `audited` counts the certified triples re-derived from the term; `alarms` counts the audited triples whose re-derived verdict differs from its certificate on identical inputs.

| pass | certified before | attempted | newly certified | audited | alarms |
|---|---|---|---|---|---|
| `ap6_delta` | 1227 | 875 | 1053 | 61 | 0 |
```

*(the label reads `ap6_delta` because this task fixed a literal
`bank1_delta` in `autopoly.bank_report_command` that printed one pass's
name over another pass's counts; log_253's own table is unaffected, it
was that pass.)*

log_253's delta certified 2 place-triples of 954 attempted. This one
certified 1,053 of 875 attempted — more than it attempted, because the
attempt list counts keys the bank already knew and the pass also ran
every setter cell the bank had never seen.

## 8.2 The three readings, beside log_253's

**LITERAL**, lane `ap6_l13` §[3/9]:

```
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
| `ap6_audit` | 651 | 895 | 855 |
| `ap6_delta` | 123 | 371 | 333 |
| **the bank** | **2003** | **2251** | **2213** |
```

| the whole bank | log_253 | this task |
|---|---|---|
| strict | 1,999 | 2,003 |
| destination-only | 2,241 | 2,251 |
| corpus-needed | 2,203 | 2,213 |

At all four, all five and all twelve, **LITERAL**, the same lane:

```
| width | reading | cells | ledger rows | share |
|---|---|---|---|---|
| all four | strict | 94 | 65724 | 49.4% |
| all four | destination | 147 | 97264 | 73.11% |
| all four | corpus | 137 | 90502 | 68.02% |
| all five | strict | 94 | 65724 | 49.4% |
| all five | destination | 147 | 97264 | 73.11% |
| all five | corpus | 137 | 90502 | 68.02% |
| all twelve | strict | 89 | 59870 | 45.0% |
| all twelve | destination | 142 | 91410 | 68.71% |
| all twelve | corpus | 132 | 84648 | 63.62% |
```

| width | reading | log_253 cells | this task | log_253 share | this task |
|---|---|---|---|---|---|
| all four | strict | 93 | 94 | 45.5% | 49.4% |
| all four | destination | 144 | 147 | 63.61% | 73.11% |
| all four | corpus | 134 | 137 | 55.19% | 68.02% |
| all five | strict | 93 | 94 | 45.5% | 49.4% |
| all five | destination | 141 | 147 | 59.93% | 73.11% |
| all five | corpus | 133 | 137 | 54.75% | 68.02% |
| all twelve | strict | 88 | 89 | 45.5% → 41.1% | 45.0% |
| all twelve | destination | 136 | 142 | 55.53% | 68.71% |
| all twelve | corpus | 128 | 132 | 50.35% | 63.62% |

**GLOSS.** The cell counts move by one to six; the LEDGER-ROW share moves
much further — all five, destination, from 59.93% to 73.11% — because the
cells that came in carry many attested rows. All five now equals all four
on every reading, which it did not before: cpp is no longer the target
that drops a cell.

**Reproducing both**, from the instance:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank.py readings | grep -v 'peak resident' | tail -32

| width | reading | cells | ledger rows | share |
|---|---|---|---|---|
| all four | strict | 94 | 65724 | 49.4% |
| all four | destination | 147 | 97264 | 73.11% |
| all four | corpus | 137 | 90502 | 68.02% |
| all five | strict | 94 | 65724 | 49.4% |
| all five | destination | 147 | 97264 | 73.11% |
| all five | corpus | 137 | 90502 | 68.02% |
| all twelve | strict | 89 | 59870 | 45.0% |
| all twelve | destination | 142 | 91410 | 68.71% |
| all twelve | corpus | 132 | 84648 | 63.62% |

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
| `ap6_audit` | 947 | 151 |
| `ap6_delta` | 449 | 57 |

THE ATTESTATION'S OWN GRANULARITY, said plainly: the corpus records a flag pair as (setter `mnem`, consumer `mnem`), with no operand shape and no width on the setter side, so the corpus-needed reading asks whether ANY cell of this `mnem` has an attested consumer.  The setters the corpus records, read off the cells file's own `setter_census`: 11 of them, over 22741 flag-pair ledger rows.
```

## 8.3 The delta's own audit

61 certified place-triples re-derived, **0 alarms**: 49 reproduced, 11
carried a changed artifact, 1 was not reproduced.

**LITERAL**, lane `ap6_l13` §[8/9], the tally at the foot of Table D4:

```
| reading | rows |
|---|---|
| not reproduced | 1 |
| reproduced | 49 |
| the artifact changed | 11 |
```

**GLOSS.** A changed artifact is not an alarm and is banked BESIDE the old
certificate, never in place of it — the eleven are the holders rule and
the answer-width re-pose doing what they were put in to do (two of them
read `proved` on the certificate and `proved_under_caller_extension` on
the re-derivation, which is the answer-width re-pose arriving). The one
NOT REPRODUCED is `sbb gpr_gpr 64` on rust at `flags`: the certificate
stands, the machinery produced no place for that key this pass. It is in
the second list.

---

# 9. The alarm this task stopped on, and what it turned out to be

The delta pass STOPPED the first time it was run, at pair 192 of 709, on
three ALARM rows. The brief's rule was followed literally: the pass
stopped and named the pairs, and nothing was worked around until the
object had been looked at.

**LITERAL**, lane `ap6_l10`, tower log
`<runs>/ap6/agent/logs/20260910T072031Z__ap6_l10_the_delta_pass.sh.log`:

```
ALARM: the re-derived verdict differs from the certificate on IDENTICAL inputs.  The pass stops here, as the brief requires.
   setb gpr_one 8 on cpp at reg_rdi: the certificate says proved, the re-derivation says sat
   setb gpr_one 8 on cpp at reg_rdi: the certificate says proved, the re-derivation says sat
   setb gpr_one 8 on cpp at reg_rdi: the certificate says proved, the re-derivation says sat
```

**LITERAL**, lane `ap6_l11` §[1/1], the objects behind them, tower log
`<runs>/ap6/agent/logs/20260910T073455Z__ap6_l11_the_three_alarms.sh.log`:

```
| setter cell | place | verdict | source sha256 | term text |
|---|---|---|---|---|
| `cmp` gpr_gpr 8 | reg_rdi | PROVED_ON_SHIP | 729430908e294315 | `Concat(0, If(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), 0, 1))` |
| `cmp` cl_gpr 8 | reg_rdi | PROVED_ON_SHIP | 729430908e294315 | `Concat(0, If(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), 0, 1))` |
| `cmp` cl_gpr_gpr 8 | reg_rdi | PROVED_ON_SHIP | 729430908e294315 | `Concat(0, If(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), 0, 1))` |
| `cmp` gpr_mem 8 | reg_rdi | DISPROVED | 729430908e294315 | `Concat(0, If(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), 0, 1))` |
| `cmp` gpr_same 8 | reg_rdi | PROVED_ON_SHIP | 2e84af2e08cd9ca5 | `0` |
| `cmp` imm_gpr 8 | reg_rdi | PROVED_ON_SHIP | 1e5445e6abe5ade8 | `Concat(0, If(Or(Extract(1, 0, v0) == 3, Not(Extract(7, 2, v0) == 0)), ` |
| `cmp` mem_gpr 8 | reg_rdi | DISPROVED | 729430908e294315 | `Concat(0, If(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), 0, 1))` |
| `cmp` xmm_gpr 8 | reg_rdi | DISPROVED | 729430908e294315 | `Concat(0, If(ULE(Extract(7, 0, v0), Extract(7, 0, v1)), 0, 1))` |
```
*(abridged to the eight rows the cause is visible in; the lane printed
all twenty and the file above carries them.)*

**GLOSS, and this is the finding.** The certificate's setter cell is
`cmp gpr_gpr 8`, which is PROVED. The three alarm rows are the runs over
`cmp gpr_mem 8`, `cmp mem_gpr 8` and `cmp xmm_gpr 8`, which are DISPROVED.
They print the same term text and render to the same source, so the
audit's identity test said IDENTICAL INPUTS — and they are not the same
obligation. The printer canonicalises a free symbol to `v0` and `v1`, so
two terms whose arrival contracts differ print identically; a memory
operand arrives as `seed_MEM_*` and a register as a register family, and
that is exactly the difference the two verdicts are about.

**The defect was in the audit's MATCHER, and it is this task's own.** A
certificate's key is six-part — (cell, target, written place, SETTER
CELL) — and `autopoly.audited_rows_of` compared four of the parts. That
was harmless while the loop wrote ONE run per (cell, target); it stopped
being harmless the moment this task made the loop write one run per
setter cell. The matcher now compares the setter as well, which is not a
weakening of the guard: an audit compares a key with itself.

**What was NOT done, and it matters:** the audit's own identity test was
not touched. It reads the place's term TEXT and the source sha256, and
this task showed the term text does not carry the arrival contract. With
the matcher keyed on the setter that is no longer reachable — two runs at
one key have one setter and so one contract — but the test is weaker than
the thing it is testing, and putting the arrival families on a certificate
is a NEW RECORD FIELD, which is a stop rule. It is in the second list.

After the fix the pass ran to the end with 0 alarms (§8.3), and lane 10's
store was moved beside itself as
`.../autopoly/ap6_delta_runs.jsonl.before_the_audit_key_carried_the_setter`
rather than deleted.

---

# 10. The guards

**THE SPELLING GUARD**, over every json and jsonl this task wrote,
lane `ap6_l13` §[9/9]:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS certificates.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/ap6_delta.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS ap6_delta.json -- no operator token in any key, grouping, pairing or row structure
```

The two jsonl stores and the bank were materialised as json under `/tmp`
inside the instance and never in the repository, and passed the same
guard: `certificates.jsonl` (19,455 records), `ap6_delta_runs.jsonl`
(2,499) and `ap6_audit_runs.jsonl` (962). **LITERAL**, the same lane:

```
  certificates.jsonl -> /tmp/ap6_guard13/certificates.json (19455 record(s))
  ap6_delta_runs.jsonl -> /tmp/ap6_guard13/ap6_delta_runs.json (2499 record(s))
  ap6_audit_runs.jsonl -> /tmp/ap6_guard13/ap6_audit_runs.json (962 record(s))
operator inventory: 91 tokens read from probe_manifest_*.json
PASS ap6_audit_runs.json -- no operator token in any key, grouping, pairing or row structure
  guard exit: 0
operator inventory: 91 tokens read from probe_manifest_*.json
PASS ap6_delta_runs.json -- no operator token in any key, grouping, pairing or row structure
  guard exit: 0
operator inventory: 91 tokens read from probe_manifest_*.json
PASS certificates.json -- no operator token in any key, grouping, pairing or row structure
  guard exit: 0
```

**THE LAW'S OWN COUNT over the files this task added**, and it did not
pass first time: lane `ap6_l14` carried the token once, in a prose
comment naming which field of the machine-form key the guard reads.  The
comment was reworded and the lane resubmitted under its own name,
`ap6_l17`, so the file on disk is the file that ran; nothing it prints
changed.  The count over the lane scripts this task wrote:

```
$ grep -rc exempt PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap6/ | sort | tail -3
PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap6/ap6_l7_which_setter_cells_compose.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap6/ap6_l8_delta_preflight_and_sample.sh:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/lanes_ap6/ap6_l9_delta_preflight_and_sample.sh:0
```

---

# 11. Memory, and who did what

**THE BOUND** is 6 GB resident, named abort `ABORT_MEMORY_AP6`, checked
after every run. The sample came first, as the law requires.

| lane | what it did | peak resident |
|---|---|---|
| `ap6_l1b` §[7/7] | the first 20 runs of every store, banked | 60,704 kB |
| `ap6_l3b` | the first 20 runs of the 100% audit | 258,352 kB |
| `ap6_l4` | the 100% audit, 942 runs | 304,716 kB |
| `ap6_l7` | every attested setter cell of every consumer, built | 67,588 kB |
| `ap6_l9` §[4/4] | the first 60 runs of the delta | 258,808 kB |
| `ap6_l12` | the delta pass, 2,499 runs | 1,461,924 kB → 2,413,732 kB |
| `ap6_l13` | the rebank and the four readings | 73,408 kB |

The pass's own peak, 2,413,732 kB, is 38% of the bound. `ABORT_MEMORY_AP6`
never fired.

**WHO DID WHAT.** The first agent stripped the nine gates, wrote
`handful_frozen.py`, put `code_version` on every run, added the setter
cell to the bank's key, ran lanes 1 to 4 (including the 100% audit), and
had written the holders rule and the `answer_bits` parameter into
`handful.py` when it was cut off by a usage limit — the parameter was
threaded into no caller and the setter-cell derivation returned an empty
list, so neither change could fire. The second agent read the state on
disk, finished the model-table path in `bank.py`, wired `answer_bits`
through `one_place` / `check_one_place` / `the_identity` / `x87_aligned`,
wrote `derived_setter_cells`, `setter_cell_census` and the census filter,
made the plan attempt a pair carrying a setter cell no pass ever ran,
fixed the audit matcher of §9 and the report label of §8.1, and ran lanes
5 to 15.

---

# 12. The tally

| what | count |
|---|---|
| task entries in the driver, before → after | 9 → 0 |
| task-name gated branches, before → after | 75 → 0 |
| opcode-name branches left | 1 (`ret`, the return instruction) |
| the 100% audit: certified place-triples re-derived | 1,227 |
| the 100% audit: alarms | 0 |
| the delta pass: runs / seconds | 2,499 / 2,224 |
| the delta pass: newly certified place-triples | 1,053 |
| the delta pass: audited / alarms | 61 / 0 |
| pair-level certificates, before → after | 2,623 → 7,519 |
| distinct (consumer, setter) pairs, before → after | 39 → 397 |
| hub2 pair entries still carried at their own kind | 111 of 111 |
| hub2 pair holes now certified `proved` | 9 of 111 |
| hub1's five unusable entries now matched at a real holder | 5 of 5 |
| the bank, strict / destination-only / corpus-needed | 2,003 / 2,251 / 2,213 |
| the spelling guard | PASS on 5 of 5 |
| peak resident against the 6 GB bound | 2,413,732 kB (38%) |
| lanes | 18, all exit 0 |

---

# 13. The two lists

## Decided, recorded for audit

1. **The setter cells the driver poses are the join of two readings, cut
   to what the sweep posed.** The corpus attests a setter by mnemonic
   only; the sweep gives the cells; a cell the sweep never seeded this
   consumer with, or whose flag values are not the width of this
   consumer's arrival, is not a pair the loop can pose. The 2,290 such
   cells are counted and stated by cause once, over the outer set, rather
   than banked as a run per target — 11,450 records that would all say the
   same thing about pairs no proof was ever posed for. §5.2.
2. **A refused held cell carries the setter cell it is about**, so a
   refusal at the composition lands on its own key rather than collapsing
   every refusal of one consumer onto one line.
3. **The plan attempts a pair carrying a setter cell no pass ever ran**,
   on the same rule as a pair no pass ever ran; without it every new pair
   would be invisible to a delta whose other rules ask only about keys the
   bank already holds. 140 pairs entered the pass that way.
4. **The audit's matcher compares the setter**, which is the sixth part of
   its own key. §9.
5. **`autopoly.bank_report_command` names the pass it is reporting** and
   no longer prints a literal `bank1_delta` over another pass's counts.
6. **Lane 8's and lane 10's stores were moved beside themselves**, as
   `.before_the_setter_cell_filter` and
   `.before_the_audit_key_carried_the_setter`. Nothing was deleted.
7. **`autopoly1.py` is untouched** and remains the reproduction of
   log_243; `handful_frozen.py` is `handful.py` as it stood before the
   strip and is what the closed passes' own commands answer through.

## Awaiting the owner

1. **The audit's identity test reads the term TEXT, and the text does not
   carry the arrival contract.** §9 showed two obligations that print
   identically and are not the same question. With the matcher keyed on
   the setter this is not reachable today, but the test is weaker than the
   thing it tests. Putting the place's arrival families on a certificate
   is a NEW RECORD FIELD, which is a stop rule, so it was not done.
2. **The narrow-answer re-pose is in the driver and the hub does not
   reach it.** `hub.gate_two_bodies` calls `handful.decided` without an
   answer width, because it has none to hand: the node's width is known to
   the hub's caller and not to that function. One argument on one call in
   `hub.py` would close it, and `hub.py` is outside this task's artifact
   folder. §7.
3. **102 of hub2's 111 pair holes are still holes**, and the cause is now
   stated: the corpus attests the pair at a width the SWEEP never posed a
   consumer row for. Whether the sweep should be re-run to seed a consumer
   at the setter's width, rather than only at its own, is a question about
   `model_translate` and not about this loop.
4. **One certified key was not reproduced**: `sbb gpr_gpr 64` on rust at
   `flags`. The certificate stands and the machinery produced no place for
   it this pass. §8.3.

---

# 14. The conventions verifier over this log

Run FROM this task's own instance, as the law requires:

    python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_255_task_ap6_one_versioned_driver.md

**LITERAL**, lane `ap6_l18` §[1/1]:

```
population: 30 claims across 1 logs
  MATCHES          5
  DIFFERS          0
  UNVERIFIABLE     24
  REFUSED          1
  NOT_RERUNNABLE   0

ONE LINE: 5 of 30 claims reproduce; 24 (80%) carry nothing to re-run

causes, by name:
  attribution_only                 15
  prose_only                       7
  pasted_without_source            2
  head_not_on_the_read_only_allowlist 1
```

**GLOSS.** Zero DIFFERS, which is what the law asks. It did not pass
first time: lane `ap6_l16` returned two, both transcription errors of
this log's own — a paste whose first line is blank and one cell that read
`70` where the tool prints `0`. The log was corrected and the lane re-run
under its own name; the verifier was not touched. The one REFUSED is the
§3 grep, whose command begins `cd ... && grep`, and the verifier's
read-only allowlist does not carry `cd` as a head; the same grep is
pasted from lane `ap6_l17`'s own log, which ran it.

| lane | what it did | exit | seconds |
|---|---|---|---|
| `ap6_l1` / `ap6_l1b` | the gate count before and after, the code version, the memory sample | 0 | 1.4 / 1.4 |
| `ap6_l2` | the bank rebuilt with the setter on the key, and the guard | 0 | 3.9 |
| `ap6_l3` / `ap6_l3b` | the 100% audit's plan and its memory sample | 0 | 0.6 / 19.2 |
| `ap6_l4` | THE 100% AUDIT, 942 runs | 0 | 644.6 |
| `ap6_l5` | the setter cells, the holders and the re-pose, on the handful's own cells file | 0 | 1.1 |
| `ap6_l6` | the setter cell population on the outer set, two readings | 0 | 1.9 |
| `ap6_l7` | every attested setter cell of every consumer, built | 0 | 6.8 |
| `ap6_l8` | the delta's plan and sample, before the census filter | 0 | 17.7 |
| `ap6_l9` | the census, the plan and the sample, after it | 0 | 25.1 |
| `ap6_l10` | the delta pass, stopped at 192/709 on three alarms | 0 | 726.0 |
| `ap6_l11` | the three alarms, and the objects behind them | 0 | 0.1 |
| `ap6_l12` | THE DELTA PASS, 2,499 runs, 0 alarms | 0 | 2231.8 |
| `ap6_l13` | the rebank, the four readings, the cost line and the guards | 0 | 8.3 |
| `ap6_l14` | the three guards, first form | 0 | 1.0 |
| `ap6_l15` | the pair guard against each entry's own kind | 0 | 0.3 |
| `ap6_l16` | the conventions verifier, 2 DIFFERS | 0 | 7.4 |
| `ap6_l17` | the three guards, the lane of record | 0 | 1.0 |
| `ap6_l18` | the conventions verifier, 0 DIFFERS | 0 | 7.5 |
