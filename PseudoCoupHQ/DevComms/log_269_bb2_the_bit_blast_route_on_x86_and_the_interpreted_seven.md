# log 269 — task bb2: the bit-blast route on every attested x86 arch-opcode, five compiled languages, beside the native route and the backstop; then the interpreted seven by agreement

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`).
It also serves the x86_64 architecture node
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_0_x86_64/PROGRESS.md`).

Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_bb2_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it.
It follows task bb1 (`PRIVATE/PseudoCoupHQ/DevComms/log_267_bb1_the_bit_blast_route_on_riscv.md`),
which ran this route on RISC-V, and task t4
(`PRIVATE/PseudoCoupHQ/DevComms/log_262_t4_the_general_construction_tier.md`),
whose x86 pass this one drives.

Date: 2026-09-12. Instance `bb2`
(`PUBLIC/Airlock/instances/bb2.conf`). Every lane ran on the
tower guest through `bash $HOME/Programming/PUBLIC/Airlock/remote_lane.sh`;
nothing but file editing, git and those commands ran on the laptop. A lane
log's host path on the tower is
`<runs>/bb2/agent/logs/<stamp>__<lane>.sh.log`, and
every attribution below names its file. Paths inside a pasted command are
the ones the lane sees: `PseudoCoupHQ` IS
`PRIVATE/PseudoCoupHQ`. Every rendering is labelled
**LITERAL** (the object, quoted) or **GLOSS** (a plain-words reading beside
a literal).

THE SPELLING BAN, pasted verbatim as required:

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

---

# 1. What this is, one sentence per object, in relation

* A **CELL** is one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table, holding, per place the opcode writes, the z3
  term the reference simulator's own builder puts there. The **OUTER
  SET** is the 253 attested x86 cells of
  `Research/oracle/cross_construction/emulation/autopoly/autopoly5_cells.json`,
  and 253 is the denominator on every x86 row and every interpreted row
  below.
* The **BIT-BLAST ROUTE** is task bb1's: z3's own `bit-blast` tactic
  turns a cell's term into an and-or-not-xor circuit over the input
  bits, and the renderer writes one named local per gate in the target
  language. No adder, multiplier or divider is authored by anyone.
* **THIS TASK** is task t4's x86 pass with ONE thing swapped, the
  render: the population, the arrival contract, the compile at the
  corpus's ship flags, the carve, the gate, the store and the bank
  registration are `general.py`'s and `autopoly.py`'s own and are
  CALLED. The swap is `bb2_run.one_attempt`, which asks
  `bitblast.blast` for the circuit and `bitblast.render_gates` for the
  source — exactly as `bb1_run.py` swapped `rv_general.one_attempt` on
  RISC-V.
* **THE THIRD ROUTE.** The tier is offered EVERY place, including the
  places the native route proved: task t4's tier declines those, which
  is right for a tier that catches what a route misses and wrong for a
  third route whose own count over the whole population is the
  measurement. The population is the whole outer set, not the bank's
  delta, for the same reason.
* **THE INTERPRETED ROUTE** has no carve and no gate — an interpreted
  target hands us no machine body of its own — so the same circuit is
  written as source over the target's own value model and run beside
  the definition at points, and the outcome is `agreed`, NEVER
  `proved`. The loop is `interp_check.one_run`, CALLED, with
  `interp_render.InterpRenderer` replaced by `bb2_run.GateRenderer`.
* **THE FILES THIS TASK ADDED**, and there are two:
  `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/bb2_run.py`
  (the driver) and
  `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/lanes_bb2/`
  (sixteen lane scripts). `bitblast.py` gained three swift branches and
  two comments and nothing else; `render_general.py` is task rd1's file
  and was not touched.

---

# 2. The walkthrough, before any figure

One cell, all the way through, on c. **LITERAL**, lane
`bb2_l6_the_pass.sh` step [2/4], tower log
`<runs>/bb2/agent/logs/20260912T082800Z__bb2_l6_the_pass.sh.log`:

```
| mnem | shape | width | place | language | gates | source lines | render s | compile s | body instructions | outcome | check s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `xor` | `gpr_gpr` | 8 | reg_rdi | c | 24 | 171 | 0.001 | 0.041 | 6 | PROVED_ON_SHIP | 0.023 |
| `xor` | `gpr_gpr` | 8 | reg_rdi | cpp | 24 | 172 | 0.001 | 0.052 | 6 | PROVED_ON_SHIP | 0.022 |
| `xor` | `gpr_gpr` | 8 | reg_rdi | rust | 24 | 172 | 0.001 | 0.054 | 6 | PROVED_ON_SHIP | 0.022 |
| `xor` | `gpr_gpr` | 8 | reg_rdi | go | 24 | 179 | 0.001 | 2.215 | 250 | PROVED_ON_SHIP | 0.122 |
| `xor` | `gpr_gpr` | 8 | reg_rdi | swift | 24 | 169 | 0.001 | 0.891 | 1 | UNDECIDED | 0.022 |
| `xor` | `gpr_gpr` | 8 | flags | c | 25 | 68 | 0.0 | 0.036 | 4 | PROVED_ON_SHIP | 0.022 |
| `xor` | `gpr_gpr` | 8 | flags | cpp | 25 | 69 | 0.0 | 0.036 | 4 | PROVED_ON_SHIP | 0.022 |
| `xor` | `gpr_gpr` | 8 | flags | rust | 25 | 69 | 0.001 | 0.042 | 4 | PROVED_ON_SHIP | 0.022 |
| `xor` | `gpr_gpr` | 8 | flags | go | 25 | 76 | 0.001 | 2.26 | 83 | PROVED_ON_SHIP | 0.062 |
| `xor` | `gpr_gpr` | 8 | flags | swift | 25 | 66 | 0.0 | 0.522 | 4 | UNDECIDED | 0.022 |
```

**GLOSS.** One cell has two written places — the destination register
and the flags. z3's blast gives the destination 24 gates and the flags
25. The render writes 171 lines of c, one named local per gate and one
per input bit read; clang at the corpus's ship flags compiles it in
0.041 s and the carve gets SIX instructions, because the compiler
recognised the circuit and wrote the one instruction the cell names.
The gate then proves that body equal to the cell's own term in 0.023 s.
The same circuit, unchanged, is what go compiles to 250 instructions
and still proves, and what swift carves to ONE instruction and does
not — section 7.2 is that one instruction, quoted.

**THERE IS ONE OBLIGATION HERE AND NOT TWO.** Task t4's tier renders a
term of its own and must then prove that term is the CELL's; this route
poses the gate on the CELL's own term — the circuit is z3's blast of it
and the carved body is compared to that term itself — so the equality
is discharged by the question asked. The row says so in those words and
claims no second proof.

---

# 3. The lanes

| lane | what it did | elapsed | exit |
|---|---|---|---|
| `bb2_l1_the_stores_the_sizes_and_the_swift_probe.sh` | the sha256 of every store read; the preflight; the circuit size of all 1,199 written places; THE SWIFT riscv64 PROBE | 125.6 s | 0 |
| `bb2_l2_the_six_cell_sample_and_the_interpreted_cost.sh` | the six-cell sample, which recorded `the gate render refused` on all 60 attempts; the first interpreted gate runs, which AGREED | 34.0 s | 0 |
| `bb2_l3_the_gate_render_refusal_named.sh` | the refusal's own words and the frame it was raised in (§7.1) | 10.1 s | 0 |
| `bb2_l4_the_sample_after_the_statement_shape.sh` | the gate render on two small cells, all five targets; the six-cell sample again, cut by swiftc's own 600 s bound; the interpreted work over the whole population | 772.4 s | 0 |
| `bb2_l5_the_swift_cost_curve_and_the_interpreted_rate.sh` | the swift compile at three sizes; one interpreted gate run on each of the seven, timed | 4,217.4 s | 0 |
| `bb2_l6_the_pass.sh` | where the gate's time goes, stage by stage; THE PASS: 1,265 runs, 5,705 store lines | 14,854.8 s | 0 |
| `bb2_l7_the_interpreted_seven.sh` | the interpreted loop, 1,771 runs, and the counts | 1,514.3 s | 0 |
| `bb2_l8_the_bank_the_readings_and_the_tables.sh` | the first bank rebuild, which left task t4's pass OUT (§7.3) | 44.6 s | 0 |
| `bb2_l9_the_bank_before_and_after.sh` | the bank and the readings before and after, both from the same machinery; the routes; the guard, which FAILED (§7.4) | 50.5 s | 0 |
| `bb2_l10_the_setter_key_the_alarms_and_the_guard.sh` | the sizes rewritten with the setter as a record; the guard, PASS; the alarms off the raw outcome (294) | 143.3 s | 0 |
| `bb2_l11_the_alarms_by_the_banks_own_kind.sh` | the alarms by the bank's own kind (32) (§7.5) | 10.1 s | 0 |
| `bb2_l12_the_six_largest_off_the_store.sh` | the six-cell sample finished, off the pass's own store | 3.0 s | 0 |
| `bb2_l13_the_conventions_verifier.sh` | the conventions verifier over this log, first pass: 2 DIFFERS | 0.2 s | 0 |
| `bb2_l14_the_swift_runtime_directories_raw.sh` | the two commands the verifier disagreed with, re-run raw (§9) | 0.0 s | 0 |
| `bb2_l15_the_conventions_verifier_again.sh` | the conventions verifier over this log, the tally of record (§10.4): 0 DIFFERS | 0.2 s | 0 |
| `bb2_l16_the_conventions_verifier_of_record.sh` | the verifier once more, over the log with its own tally in it: 0 DIFFERS | 0.2 s | 0 |

Every lane script is in the repository under
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/lanes_bb2/`
and was submitted from there, as the standing rule of 2026-09-07
requires.

---

# 4. The population, and what the circuits cost before anything is compiled

Reproducing command, from the instance:
`python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/bb2_run.py sizes`.
The product is
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/bb2_sizes.json`.

Table 4.1 — the circuit of every written place, nothing compiled and
nothing gated. **LITERAL**, lane `bb2_l10` step [1/4] (the same numbers
lane 1 first produced; lane 10 re-ran it after the setter-record fix of
§7.4):

```
| what | places | smallest | median | mean | largest |
|---|---|---|---|---|---|
| gates per definition | 618 | 0 | 64 | 1015.311 | 74786 |
| blast seconds | 618 | 0.006 | 0.032 | 0.092 | 6.508 |

| gates | places |
|---|---|
| 0 to 100 | 346 |
| 100 to 1000 | 211 |
| 1000 to 4000 | 44 |
| 4000 to 10000 | 5 |
| 10000 to 50000 | 7 |
| 50000 to 1000000000 | 5 |
```

Table 4.2 — the twenty largest circuits. **LITERAL**, the same step:

```
| mnem | shape | width | place | gates | input bits | blast s |
|---|---|---|---|---|---|---|
| `idiv` | `gpr_one` | 32 | reg_rdx | 74786 | 96 | 4.312 |
| `idiv` | `gpr_one` | 32 | reg_rax | 74503 | 96 | 4.33 |
| `mul` | `gpr_one` | 64 | reg_rdx | 64059 | 128 | 6.508 |
| `div` | `gpr_one` | 32 | reg_rdx | 55836 | 96 | 3.124 |
| `div` | `gpr_one` | 32 | reg_rax | 55550 | 96 | 3.151 |
| `imul` | `gpr_gpr` | 64 | reg_rdi | 28098 | 128 | 2.219 |
| `mul` | `gpr_one` | 64 | reg_rax | 28098 | 128 | 2.205 |
| `idiv` | `gpr_one` | 16 | reg_rdx | 18449 | 96 | 1.087 |
| `idiv` | `gpr_one` | 16 | reg_rax | 18310 | 96 | 1.096 |
| `mul` | `gpr_one` | 32 | reg_rdx | 15404 | 64 | 1.357 |
| `div` | `gpr_one` | 16 | reg_rdx | 13595 | 96 | 0.783 |
| `div` | `gpr_one` | 16 | reg_rax | 13453 | 96 | 0.781 |
| `imul` | `gpr_gpr` | 32 | reg_rdi | 6643 | 64 | 0.513 |
| `mul` | `gpr_one` | 32 | reg_rax | 6643 | 64 | 0.51 |
| `idiv` | `gpr_one` | 8 | reg_rax | 4546 | 72 | 0.275 |
| `cmovne` | `gpr_gpr` | 64 | reg_rdi | 4352 | 192 | 0.129 |
| `cmove` | `gpr_gpr` | 64 | reg_rdi | 4352 | 192 | 0.13 |
| `mul` | `gpr_one` | 16 | reg_rdx | 3555 | 80 | 0.337 |
| `div` | `gpr_one` | 8 | reg_rax | 3227 | 72 | 0.199 |
| `sbb` | `gpr_gpr` | 64 | reg_rdi | 2638 | 256 | 0.272 |
```

Table 4.3 — the 581 written places of the 1,199 that do NOT blast, by
cause. **LITERAL**, the same step:

```
THE PLACES THE BLAST REFUSED OR THE DRIVER DID NOT REACH: 581
| cause, LITERAL | places |
|---|---|
| the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes | 494 |
| the bit-blast route is a circuit over BITS and this term is not a bit-vector term over bit-vector arrivals: z3's bit-blast tactic has nothing to blast | 75 |
| term reads state that is not an arrival register | 8 |
| the circuit is larger than the number of gates this task states, measured before anything is written: at or above 200000 gates | 4 |
```

**GLOSS.** Of 1,199 written places, 618 have a circuit at all. The
largest cause is not about the route: 494 places are the flag state a
preseeded row ARRIVED with, which no opcode writes, and the driver
declines them for every route. 75 are float terms, which a circuit over
bits has no node for. 4 are above the 200,000-gate ceiling
`bitblast.GATE_CEILING` states, measured before anything is written.

---

# 5. The six largest circuits, all the way through — the sample the brief asks for first

Reproducing command, from the instance:
`python3 .../bb2_run.py largest 6`. The six are chosen by CIRCUIT SIZE
off this task's own sizes file — machine-form evidence, measured, never
a reading of any name.

**LITERAL**, lane `bb2_l12_the_six_largest_off_the_store.sh` step [1/2],
tower log
`<runs>/bb2/agent/logs/20260912T131110Z__bb2_l12_the_six_largest_off_the_store.sh.log`
(the header rows of each cell; the whole table is in the lane log):

```
the sample: the 6 cells with the largest circuits, off bb2_sizes.json
   `idiv` `gpr_one` 32 -- largest place 74786 gates
   `mul` `gpr_one` 64 -- largest place 64059 gates
   `div` `gpr_one` 32 -- largest place 55836 gates
   `imul` `gpr_gpr` 64 -- largest place 28098 gates
   `idiv` `gpr_one` 16 -- largest place 18449 gates
   `mul` `gpr_one` 32 -- largest place 15404 gates

| mnem | shape | width | place | language | gates | source lines | render s | compile s | body instructions | outcome | check s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `div` | `gpr_one` | 32 | reg_rax | c | 55550 | 55721 | 0.043 | 14.365 | 61169 | the carved body is larger than the number of instructions this task's gate is of | None |
| `div` | `gpr_one` | 32 | reg_rdx | go | 55836 | 56016 | 0.039 | 5.566 | 81035 | the carved body is larger than the number of instructions this task's gate is of | None |
| `div` | `gpr_one` | 32 | reg_rax | swift | 55550 | 55719 | 0.039 | 600.121 | None | the compiler refused | None |
      the compile refused, LITERAL: TimeoutExpired: Command '['/persist/swift/usr/bin/swiftc', '-O', '-c', '/tmp/g1_ibjv9l71/unit.swift', '-o', '/tmp/g1_ibjv9l71/unit_ship.o']' timed out after 600 seconds
| `mul` | `gpr_one` | 64 | reg_rdx | c | 64059 | 64262 | 0.076 | 19.598 | 92742 | the carved body is larger than the number of instructions this task's gate is of | None |
| `mul` | `gpr_one` | 64 | reg_rdx | rust | 64059 | 64263 | 0.072 | 21.288 | 92582 | the carved body is larger than the number of instructions this task's gate is of | None |
| `mul` | `gpr_one` | 64 | reg_rdx | go | 64059 | 64270 | 0.074 | 4.411 | 105829 | the carved body is larger than the number of instructions this task's gate is of | None |
| `imul` | `gpr_gpr` | 64 | reg_rdi | c | 28098 | 28301 | 0.041 | 4.547 | 40757 | the carved body is larger than the number of instructions this task's gate is of | None |
| `imul` | `gpr_gpr` | 64 | flags.low | c | 0 | 139 | 0.0 | 0.037 | 2 | PROVED_ON_SHIP | 0.061 |
| `imul` | `gpr_gpr` | 64 | flags.high | go | 0 | 146 | 0.0 | 2.282 | 192 | PROVED_ON_SHIP | 0.204 |
| `idiv` | `gpr_one` | 16 | reg_rax | c | 18310 | 18481 | 0.016 | 2.766 | 22288 | the carved body is larger than the number of instructions this task's gate is of | None |
| `idiv` | `gpr_one` | 16 | reg_rax | swift | 18310 | 18479 | 0.014 | 133.266 | 1 | UNDECIDED | 0.028 |
| `mul` | `gpr_one` | 32 | reg_rax | c | 6643 | 6782 | 0.005 | 0.586 | 9562 | the carved body is larger than the number of instructions this task's gate is of | None |
| `mul` | `gpr_one` | 32 | reg_rdx | swift | 15404 | 15541 | 0.012 | 84.711 | 1 | UNDECIDED | 0.025 |
```

**GLOSS, and it is the cost line the brief asks for.** At the expensive
end the source is 15,000 to 64,000 lines; the render takes hundredths
of a second; clang and rustc take 0.6 to 21 s, go 3 to 6 s, and swiftc
16 to 600 s — swiftc is the one compiler this size reaches, and at
55,000 lines its own 600-second bound fires and the row says so with the
command quoted. Every carved body at this end is above the 4,000
instructions the gate is offered, so every one of them is NOT_GATED with
its instruction count on the row. The flags places of the same cells are
zero-gate circuits and are proved in hundredths of a second.

**THE SAMPLE WAS RUN FIRST AND WAS CUT.** Lane `bb2_l4` ran it as its
own command and did not finish: swiftc did not come back from a
74,674-line source and its own bound raised `subprocess.TimeoutExpired`
out of the run. The bound firing is now a row with a cause
(`bb2_run.one_attempt` catches it and records the compiler's own words),
and the pass then ran every one of these cells on every target, so the
table above is the same measurement finished rather than a second one.

---

# 6. THE MEASUREMENT

## 6.1 The pass

Reproducing command, from the instance:
`python3 .../bb2_run.py run`. The store is
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bb2_bit_blast_runs.jsonl`
(5,705 lines, 262 MB) and the sources are beside it under
`.../autopoly/src_bb2_bit_blast/` (2,614 files, 20 MB).

Lane of record: `bb2_l6_the_pass.sh`, tower log
`<runs>/bb2/agent/logs/20260912T082800Z__bb2_l6_the_pass.sh.log`,
`state=done exit=0` in 14,854.8 s. Six attempts, the store written line
by line and each attempt skipping what is already on it: 0 → 1,838 →
2,461 → 4,156 → 5,608 → 5,705 → 5,705, and the sixth attempt added no
line, which is how the pass says it is finished. Peak resident over the
whole lane: 2,427,268 kB, under the 6 GB this task states, named abort
`ABORT_MEMORY_BB2` never reached.

FOUR RUNS WERE LEFT BEHIND, each one an attempt entered and not come out
of inside that attempt's own wall clock. **LITERAL**,
`.../autopoly/bb2_bit_blast_left_behind.json`:

```
[["imul","gpr_gpr",64,"swift"],
 ["mul","gpr_one",64,"swift"],
 ["cmp","mem_gpr",64,"go"],
 ["mul","gpr_one",16,"go"]]
```

## 6.2 Deliverable 1 — the three routes, population 253 on every row

Reproducing command, from the instance: `python3 .../bb2_run.py table`.
The route of every certificate is the certificate's own `route` field,
which is what the pass that wrote it recorded, never a reading of a
name: the NATIVE route is `term`, `primitive`, `primitive+setup` and the
rows an early pass wrote before the field existed; the BACKSTOP is
`general` (task t4's general tier) and `constructed` (task t2's eight
schemas before it); the BIT-BLAST route is `bit_blast`.

**LITERAL**, lane `bb2_l11_the_alarms_by_the_banks_own_kind.sh` step
[2/3], tower log
`<runs>/bb2/agent/logs/20260912T131110Z__bb2_l11_the_alarms_by_the_banks_own_kind.sh.log`:

```
THE THREE ROUTES, PROVED, destination_only reading, of 253 on every row
| language | native route | backstop (t4, t2) | bit-blast (bb2) | any route | of |
|---|---|---|---|---|---|
| c | 205 | 9 | 122 | 207 | 253 |
| c++ | 227 | 9 | 122 | 229 | 253 |
| rust | 176 | 8 | 122 | 176 | 253 |
| go | 157 | 7 | 126 | 164 | 253 |
| swift | 160 | 12 | 13 | 167 | 253 |
| **proved on at least one language** | **233** | **17** | **127** | **233** | **253** |
| **proved on all five languages** | | | | **154** | **253** |


THE THREE ROUTES, PROVED, strict reading, of 253 on every row
| language | native route | backstop (t4, t2) | bit-blast (bb2) | any route | of |
|---|---|---|---|---|---|
| c | 160 | 2 | 91 | 168 | 253 |
| c++ | 183 | 2 | 91 | 197 | 253 |
| rust | 132 | 2 | 91 | 138 | 253 |
| go | 110 | 2 | 95 | 119 | 253 |
| swift | 120 | 4 | 13 | 124 | 253 |
| **proved on at least one language** | **192** | **4** | **96** | **201** | **253** |
| **proved on all five languages** | | | | **111** | **253** |
```

**GLOSS.** The bit-blast route proves 122 of 253 cells on c, cpp and
rust and 126 on go under the destination-only reading, and 91 to 95
under the strict one. It is a THIRD route and not a replacement: the
native route is ahead of it everywhere, and what the bit-blast route
buys is the cells the other two leave — the `any route` column is 207 on
c where the native route alone is 205, 229 on cpp where it is 227, and
164 on go where it is 157. Swift's 13 is not a fact about the route; it
is section 7.2.

## 6.3 Deliverable 1 continued — this route's own outcomes, by cause

**LITERAL**, the same step:

```
THE BIT-BLAST ROUTE'S OWN OUTCOMES OVER WRITTEN PLACES, of 253 cells on every row
| language | cells run | places | proved | disproved | undecided | refused |
|---|---|---|---|---|---|---|
| c | 172 | 1108 | 353 | 110 | 20 | 625 |
| c++ | 174 | 1110 | 353 | 111 | 20 | 626 |
| rust | 174 | 1110 | 353 | 110 | 21 | 626 |
| go | 172 | 1106 | 359 | 142 | 1 | 604 |
| swift | 172 | 1105 | 43 | 0 | 548 | 514 |
```

Table 6.3 — every outcome that is not a proof, with its cause, the four
largest. **LITERAL**, the same step:

```
| language | outcome | cause | attempts |
|---|---|---|---|
| swift | UNDECIDED | the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 527 |
| c++ | DISPROVED | z3 found a starting state under which the two sides differ | 199 |
| rust | DISPROVED | z3 found a starting state under which the two sides differ | 198 |
| c | DISPROVED | z3 found a starting state under which the two sides differ | 196 |
```

## 6.4 Deliverable 4 — the sizes and the seconds over the whole pass

**LITERAL**, the same step:

```
THE SIZES AND THE SECONDS
| what | attempts | smallest | median | mean | largest |
|---|---|---|---|---|---|
| gates per definition | 3069 | 0 | 64 | 981.149 | 74786 |
| blast seconds | 3069 | 0.007 | 0.033 | 0.091 | 6.598 |
| source lines | 3069 | 33 | 220 | 1148.399 | 74966 |
| render seconds | 3069 | 0.0 | 0.001 | 0.002 | 0.091 |
| compile seconds | 3069 | 0.032 | 0.102 | 1.829 | 600.124 |
| carved body instructions | 3049 | 1 | 70 | 1251.819 | 105829 |
| check seconds | 2975 | 0.023 | 0.084 | 1.734 | 10.034 |

PER LANGUAGE
| language | attempts | gates, median | body, median | body, largest | compile s, median | compile s, summed |
|---|---|---|---|---|---|---|
| c | 614 | 64 | 80 | 92742 | 0.044 | 188 |
| c++ | 616 | 64 | 85 | 92619 | 0.048 | 190 |
| rust | 616 | 64 | 85 | 92582 | 0.057 | 200 |
| go | 612 | 64 | 345 | 105829 | 2.256 | 1405 |
| swift | 611 | 64 | 1 | 4 | 0.935 | 3629 |
```

**NOT GATED, counted by size and by clock. LITERAL**, the same step:

```
NOT GATED -- the gate was never asked, by cause: 505 attempts (the ceilings are 4000 carved instructions and 10 seconds on a wall clock that stops it)
| the cause, LITERAL | attempts |
|---|---|
| the gate did not come back inside the seconds this task allows one gate call on a wall clock that stops it: the carved body is on the canonical form a | 431 |
| the carved body is larger than the number of instructions this task's gate is offered: the lift builds one term per instruction and a body of this siz | 74 |
```

**GLOSS, and it is this task's own bound justifying itself.** The check
that ANSWERS answers fast: the median is 0.084 s over 2,975 gate calls.
The one that does not answer does not answer a little late — section 7.6
quotes `add gpr_gpr 32` on c at 1,800 s with nothing back. So 431 of
3,069 attempts are NOT_GATED with the clock named on the row and 74 with
the instruction count named on the row, and neither is a verdict.

## 6.5 Deliverable 2 — the three readings, the bank before → after

Both banks were built by the same machinery, one registration apart.
Reproducing commands, from the instance:
`python3 .../bb2_run.py bank_before` then `readings_before`, and
`python3 .../bb2_run.py bank` then `readings`. Lane
`bb2_l9_the_bank_before_and_after.sh`, tower log
`<runs>/bb2/agent/logs/20260912T130438Z__bb2_l9_the_bank_before_and_after.sh.log`.

Table 6.5a — the bank's own pair counts. The `before` row is the bank
with every pass up to and including task t4 registered, and it
reproduces task t4's own published figures exactly.

| reading | before | after | moved |
|---|---|---|---|
| strict | 2,015 | **2,105** | +90 |
| destination-only | 2,273 | **2,331** | +58 |
| corpus-needed | 2,229 | **2,303** | +74 |

Table 6.5b — cells on all four compiled targets (c, rust, go, swift),
beside task t4's 96 / 154 / 141 of 205.

| reading | before | after | moved |
|---|---|---|---|
| strict | 96 | **107** | +11 |
| destination-only | 154 | **163** | +9 |
| corpus-needed | 141 | **150** | +9 |

Table 6.5c — all twelve (the five compiled proved and the seven
agreeing).

| reading | before | after | moved |
|---|---|---|---|
| strict | 89 | **102** | +13 |
| destination-only | 142 | **158** | +16 |
| corpus-needed | 132 | **145** | +13 |

**LITERAL**, lane `bb2_l9` step [4/8], this task's own two passes on the
bank's per-pass table:

```
| pass | strict | destination-only | corpus-needed |
|---|---|---|---|
| `t2_construct` | 89 | 347 | 303 |
| `t4_general` | 21 | 79 | 64 |
| `bb2_bit_blast` | 727 | 943 | 919 |
| `bb2_interp` | 1158 | 1158 | 1158 |
| **the bank** | **2105** | **2331** | **2303** |
```

**GLOSS, and it is the answer to the question task t4 left open.** Task
t4's tier moved the three CELL readings by zero: what it reached were
places on targets that were already the ones holding out. This route
moves them by +11 / +9 / +9, and the bank's pair counts by +90 / +58 /
+74. The reason is the population: this route was offered every place of
every cell on every target, including the places another route had
already proved, so where it reaches a cell it reaches it on all of c,
cpp, rust and go at once.

The bank file went from 26,684 certificates to **39,980**; this task's
two passes contribute 11,525 and 1,771 of them.

## 6.6 The 100% re-derivation, and its 32 alarms

Because this pass ran the whole population rather than the bank's delta,
every certified key on the five compiled targets was re-derived by an
INDEPENDENT route. That is a 100% audit, and the alarm is a place
another pass certifies and this route records `sat`.

Reproducing command: `python3 .../bb2_run.py alarms`. **LITERAL**, lane
`bb2_l11` step [1/3], the count and the first rows of each shape:

```
certified places another pass holds, on the five compiled targets: 2383
alarms: 32
```

```
| language | mnem | shape | width | place | setter | the bank's pass | counterexample, LITERAL |
|---|---|---|---|---|---|---|---|
| c | `cmovns` | `gpr_gpr` | 64 | reg_rdi | `test` `gpr_same` 64 | t2_construct | [IN_2 = 18446744073709551615, seed_MEM_0xd0_rsp_ = 0, ... |
| c | `shr` | `cl_gpr` | 64 | reg_rdi | -- | ap6_delta | [seed_MEM_m0x28_rsp_ = 0, seed_MEM_0x140_rsp_ = 0, ... |
| cpp | `movsbq` | `widen_gpr_gpr` | 64 | reg_rdi | -- | t2_construct | [seed_rsi = 138525786257407, IN_0 = 1941159936] |
| go | `andpd` | `xmm_xmm` | 128 | reg_xmm0.high | -- | t2_construct | [IN_1 = 9223372036854775808, IN_0 = 9223372036854775808] |
| go | `punpckldq` | `mem_xmm` | 128 | reg_xmm0.low | -- | t2_construct | [seed_MEM_0xc_rsp_ = 4294967295, IN_0 = 0, IN_1 = 0] |
```

**GLOSS, said carefully.** 32 of 2,383, and 21 of the 32 are go at a
128-bit xmm place — the vector-lane question — with the counterexample
in the half the lane does not write. The rest are four shapes: a
conditional move over a setter, a shift by `cl` at 64 bits, a sign-widen
at 64 bits, and a 32-bit move out of xmm. NOTHING WAS WORKED AROUND and
no cell was edited to agree: these are two routes' verdicts on the same
obligation, and which of the two is right is an evidence question, not
an implementation one. It is item 1 of the awaiting-the owner list.

---

# 7. The defects, each found by a lane, each fixed in the layer that owns it

## 7.1 The statement shape: `render_general.assemble` changed under this task

**THE SYMPTOM.** Lane `bb2_l2` recorded `the gate render refused` on all
sixty of its attempts, at every circuit size and on every target,
INCLUDING a place whose circuit is zero gates.

**THE CAUSE, LITERAL**, lane `bb2_l3_the_gate_render_refusal_named.sh`
step [2/3], tower log
`<runs>/bb2/agent/logs/20260912T070006Z__bb2_l3_the_gate_render_refusal_named.sh.log`:

```
  File "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/bitblast.py", line 779, in render_gates
    source, symbol = RG.assemble(lang, renderer, label, return_type,
                                 statements, answer_lines, body, text)
  File "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/render_general.py", line 1229, in assemble
    lines.append(indented(lang, depth, line))
  File "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/render_general.py", line 1134, in indented
    return "    " * (depth + 1) + line
TypeError: can only concatenate str (not "int") to str
```

`render_general.assemble`'s own docstring on the tower now reads
`statements` is (depth, line) per written line, the depth being how many
conditionals written as control flow the line sits inside`, and
`bitblast.render_gates` hands it `(name, line)` — the shape that
function took when task bb1 wrote the route.

**THE FIX, and where it was made.** `render_general.py` is task rd1's
file and THIS TASK DID NOT TOUCH IT. The adapter is in `bb2_run.py`, on
this task's own side of the call
(`bb2_run.install_the_statement_shape`), and it rewrites every statement
to `(0, line)` — a circuit is flat and sits inside no conditional, so
its depth is zero. It is correct under BOTH contracts: the old
`assemble` binds the first element to a name it ignores and the new one
binds it to the depth, which is what 0 is.

**FLAG FOR THE COORDINATOR.** `bitblast.render_gates` as it stands in
the repository is BROKEN against the current `render_general.assemble`,
and so therefore is task bb1's route if it is re-run. This task did not
fix it there, because `bitblast.py` is shared with bb1 and
`render_general.py` is rd1's.

## 7.2 Swift: the `@_cdecl` entry is a thunk and the carve gets it

**THE SYMPTOM.** 527 of 611 swift attempts are UNDECIDED on one cause,
and the swift carved body is 1 instruction at the median and 4 at the
largest, at every circuit size.

**THE OBJECT, LITERAL**, read off the store
(`.../autopoly/bb2_bit_blast_runs.jsonl`, the `xor gpr_gpr 8` swift run):

```
reg_rdi | 1 | 'jmp 5 <emu_xor_gpr_gpr_8__reg_rdi__swift__bit_blast+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship012emu_xor_gpr_E29_8__reg_rdi__swift__bit_blastys6UInt64VAD_s5UInt8VtF-0x4'
   landing: LANDED_ELSEWHERE
   check: UNDECIDED | the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either
flags | 4 | 'push %rax; call 6 <emu_xor_gpr_gpr_8__flags__swift__bit_blast+0x6> !!reloc=R_X86_64_PLT32:$s9unit_ship012emu_xor_gpr_E27_8__flags__swift__bit_blastys6UInt16Vs5UInt8V_AFtF-0x4; pop %rcx; ret'
   landing: LANDED_ELSEWHERE
   check: UNDECIDED | the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read
```

**GLOSS.** swiftc emits the `@_cdecl` name as a THUNK that jumps or
calls into the mangled Swift function, and the carve — which asks
objdump for the C symbol — gets the thunk. The body is under
`$s9unit_ship...`. This is a property of the swift ROUTE and not of the
circuit: it happens at 24 gates and at 74,786. It is why swift's
bit-blast column is 13 of 253 where c's is 122. NOTHING WAS EDITED to
make swift pass; the rows stand with the thunk quoted. It is item 2 of
the awaiting-the owner list.

## 7.3 The bank rebuild left task t4's pass out

**THE SYMPTOM.** Lane `bb2_l8`'s rebuild wrote a bank of 38,054
certificates whose per-pass table has no `t4_general` row at all, and
whose route table reads `backstop 0` on c, cpp and rust.

**THE CAUSE.** `general.register_with_the_bank` reads
`general.PASS_LABEL`, which this task had already set to its own label,
so the call registered THIS task's store under THIS task's name and task
t4's 1,926 certificates were never read. Task t4's own docstring warns
of exactly this shape: "a rebuild run from HERE with only this pass
registered would write a bank with task t2's fourteen proved places
missing, which is not a delta but a loss".

**THE FIX.** `bb2_run.register_with_the_bank` spells task t4's entry out
by name rather than calling the function that reads a label. Lane
`bb2_l9` then rebuilt both banks: 26,684 certificates before, 39,980
after, with `t4_general` at 21 / 79 / 64 exactly as log 262 records it.

## 7.4 The setter cell as a bare tuple — the guard's own finding

**THE SYMPTOM, LITERAL**, lane `bb2_l9` step [7/8]:

```
FAIL bb2_sizes.json -- 60 spelling-keyed place(s)
     $.rows[40].setter[0]
         list element is the bare operator token 'or'
```

**THE CAUSE AND THE FIX.** `bb2_sizes.json` wrote the setter cell as a
bare `(mnem, shape, width)` tuple, which puts the mnemonic in a LIST
element. The ruling of 2026-09-08 is that a mnemonic is machine form
when it sits in the field `mnem`; the row now carries
`autopoly.setter_record`, which is that record. Lane `bb2_l10` re-ran
the sizes and the guard PASSED — section 9.

## 7.5 The alarm key: the setter, and the bank's own kind

**TWO WRONG COUNTS BEFORE THE RIGHT ONE**, and both are this task's own.
Lane `bb2_l9` read **726** alarms with the setter left out of the key and
this task's own pass left in the certified set — every one of them this
route's verdict on one setter cell set against its verdict on another.
Lane `bb2_l10` put the setter in the key and excluded this task's passes
and read **294** — off the gate's RAW outcome, which counts a place whose
caller-extension re-pose then proved. A certificate's key is
(cell, target, written place, SETTER CELL) and a place's kind is
`bank.kind_of_place`; read that way, lane `bb2_l11` reads **32**.

## 7.6 Where the gate's time goes, and the bound that follows from it

**THE MEASUREMENT, LITERAL**, lane `bb2_l6` step [1/4], each stage in a
process of its own under a 60-second clock:

```
  xor gpr_gpr 8 / reg_rdi on c: 24 gates, 6 carved instructions
    form.wrap alone              0.02 s
    wrapped_body (wrap+canon40)  0.02 s
    body_answer (the lift)       0.02 s
    check_one_place, whole       0.02 s
  add gpr_gpr 32 / reg_rdi on c: 461 gates, 766 carved instructions
    form.wrap alone              0.02 s
    wrapped_body (wrap+canon40)  0.14 s
    body_answer (the lift)       0.18 s
    check_one_place, whole       ABORTED at 60 s (the clock fired)
```

**GLOSS.** The canonical form is cheap (0.14 s) and the lift is cheap
(0.18 s) even at 766 instructions; what runs out is the rest of
`handful.check_one_place` — the alignment and the solver calls after it.
Lane `bb2_l5` had already measured the same cell at 1,800 s with nothing
back (exit 124), at 100% processor and 82 MB resident.

**AND THAT IS WHY THE GATE IS ASKED IN A PROCESS OF ITS OWN.** Task t4's
bound is `signal.setitimer` calling `z3.main_ctx().interrupt()`, which
stops a SOLVER; on this route the time is not inside a solver call and
an interrupt reaches nothing. `bb2_run.gate_in_its_own_process` forks, lets
the forked process run `handful.check_one_place` — the gate of record,
CALLED, with its own arrival contract and its own 3,000 ms solver
ceiling — and ABORTS that process (`SIGKILL`, the operating system's
own spelling) where the ten-second clock fires. The place is then NOT GATED
with its seconds and its instruction count on the row.

---

# 8. Deliverable 3 — the interpreted seven, by agreement, of 253

Reproducing commands, from the instance:
`python3 .../bb2_run.py interp`, then `interp_retry`, then
`interp_table`. The store is
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bb2_interp_runs.jsonl`
(1,771 lines) and the sources are
`.../emulation/interp/src_bb2/` (1,200 files, 39 MB). Lane
`bb2_l7_the_interpreted_seven.sh`, tower log
`<runs>/bb2/agent/logs/20260912T123557Z__bb2_l7_the_interpreted_seven.sh.log`,
1,771 runs in 1,513 s.

**LITERAL**, lane `bb2_l7` step [4/4]:

```
THE INTERPRETED SEVEN, THE BIT-BLAST CIRCUIT RUN BESIDE THE DEFINITION, of 253 on every row
| language | agreed | disagreed | refused | timed out | of |
|---|---|---|---|---|---|
| cpython | 166 | 0 | 87 | 0 | 253 |
| php | 166 | 0 | 87 | 0 | 253 |
| ruby | 166 | 0 | 87 | 0 | 253 |
| java | 162 | 0 | 91 | 0 | 253 |
| javascript | 166 | 0 | 87 | 0 | 253 |
| dart | 166 | 0 | 87 | 0 | 253 |
| csharp | 166 | 0 | 87 | 0 | 253 |
| **agreeing on all seven** | **162** | | | | **253** |
```

Beside task ex2's own, which ran the TERM in each language's own
operators rather than the circuit (log 250, deliverable 1):

| language | ex2, the term's own operators | bb2, the bit-blast circuit | of |
|---|---|---|---|
| cpython | 193 | 166 | 253 |
| php | 184 | 166 | 253 |
| ruby | 193 | 166 | 253 |
| java | 184 | 162 | 253 |
| javascript | 193 | 166 | 253 |
| dart | 184 | 166 | 253 |
| csharp | 184 | 166 | 253 |

**AN AGREEMENT IS `agreed` AND IS NEVER A PROOF**, which is task ex1's
own doctrine and this task's: a cell whose whole sample agrees is
evidence that the rendering computes the cell's mapping, at the strength
the fuzz line gives an executed measurement, and nothing more. ZERO
DISAGREEMENTS over all 1,771 runs; zero timeouts; the retry pass has no
lines.

Table 8.1 — every refusal by cause, the four largest. **LITERAL**, the
same step:

```
| language | cause | cells |
|---|---|---|
| cpython | the bit-blast route is a circuit over BITS and this term is not a bit-vector term over bit-vector arrivals: z3's bit-blast tactic has nothing to blast | 71 |
| csharp | a width c has no holder for | 39 |
| csharp | the bit-blast route is a circuit over BITS and this term is not a bit-vector term over bit-vector arrivals: z3's bit-blast tactic has nothing to blast | 33 |
| java | the runner did not answer | 9 |
| cpython | the runner did not answer | 6 |
| cpython | term reads state that is not an arrival register | 4 |
| cpython | the circuit is larger than the work this task's interpreted runner is offered | 4 |
| cpython | the circuit is larger than the number of gates this task states, measured before anything is written | 2 |
```

**THE WORK CEILING IS MEASURED AND IS NOT A PREFERENCE.** Lane `bb2_l5`
ran `sbb gpr_same 64` — 695 gates over 19,683 sample points, 13,679,685
gate evaluations — in 2.4 s on cpython, 2.3 s on php and 2.3 s on ruby,
the interpreter's start-up included. That is about six million gate
evaluations a second, so this task's ceiling of two hundred million is
about thirty-three seconds, inside the sixty `interp_check` is handed.
Of the 176 cells whose destination place blasts, 174 are under it and
FOUR carry the ceiling on the row, with their own numbers: `idiv
gpr_one 32` at 1,466,442,549 gate evaluations and `div gpr_one 32` at
1,093,390,650 are the two largest.

**THE SAMPLE IS TASK ex1's OWN, UNCHANGED**, printed LITERAL by lane
`bb2_l7` step [1/4] before anything ran: edge values first, at most
20,000 points, declines never scored.

---

# 9. Deliverable 5 — the probe for a Swift SDK for riscv64 linux, LITERAL

The brief asks whether a Swift SDK for riscv64 Linux exists to install —
a probe, not a guess. Reproducing command, from the instance:
`python3 .../bb2_run.py swift_riscv`. **LITERAL**, lane
`bb2_l1_the_stores_the_sizes_and_the_swift_probe.sh` step [5/6], tower
log
`<runs>/bb2/agent/logs/20260912T065453Z__bb2_l1_the_stores_the_sizes_and_the_swift_probe.sh.log`:

```
$ /persist/swift/usr/bin/swiftc --version
  exit 0
  out: Swift version 6.0.3 (swift-6.0.3-RELEASE)
  out: Target: x86_64-unknown-linux-gnu

$ /persist/swift/usr/bin/swiftc -target riscv64-unknown-linux-gnu -print-target-info
  exit 0
  out: {
  out:   "compilerVersion": "Swift version 6.0.3 (swift-6.0.3-RELEASE)",
  out:   "target": {
  out:     "triple": "riscv64-unknown-linux-gnu",
  out:     "unversionedTriple": "riscv64-unknown-linux-gnu",
  out:     "moduleTriple": "riscv64-unknown-linux-gnu",
  out:     "compatibilityLibraries": [ ],
  out:     "librariesRequireRPath": false
  out:   },
  out:   "paths": {
  out:     "runtimeLibraryPaths": [
  out:       "/persist/swift/usr/lib/swift/linux"
  out:     ],
  out:     "runtimeLibraryImportPaths": [
  out:       "/persist/swift/usr/lib/swift/linux",
  out:       "/persist/swift/usr/lib/swift/linux/riscv64"
  out:     ],
  out:     "runtimeResourcePath": "/persist/swift/usr/lib/swift"
  out:   }
  out: }

$ /persist/swift/usr/bin/swift sdk list
  exit 127
  err: /persist/swift/usr/bin/swift-sdk: error while loading shared libraries: libxml2.so.2: cannot open shared object file: No such file or directory

$ /persist/swift/usr/bin/swiftc -O -c -target riscv64-unknown-linux-gnu /tmp/bb2_swift_riscv/probe.swift -o /tmp/bb2_swift_riscv/probe.o
  exit 1
  err: <unknown>:0: error: could not find module '_Concurrency' for target 'riscv64-unknown-linux-gnu'; found: x86_64-unknown-linux-gnu, at: /persist/swift/usr/lib/swift/linux/_Concurrency.swiftmodule
```

**WHAT IS ON DISK UNDER THAT DIRECTORY, and the resolver beside it.**
The probe's own rendering prefixes every line with `out:`, which is its
shape and not the command's, so these three are re-run raw in their own
lane so a reader re-running them gets what is pasted. **LITERAL**, lane
`bb2_l14_the_swift_runtime_directories_raw.sh` step [1/2], tower log
`<runs>/bb2/agent/logs/20260912T132059Z__bb2_l14_the_swift_runtime_directories_raw.sh.log`:

```
$ ls -1d /persist/swift/usr/lib/swift/linux/*/
/persist/swift/usr/lib/swift/linux/Cxx.swiftmodule/
/persist/swift/usr/lib/swift/linux/CxxStdlib.swiftmodule/
/persist/swift/usr/lib/swift/linux/Distributed.swiftmodule/
/persist/swift/usr/lib/swift/linux/Foundation.swiftmodule/
/persist/swift/usr/lib/swift/linux/FoundationEssentials.swiftmodule/
/persist/swift/usr/lib/swift/linux/FoundationInternationalization.swiftmodule/
/persist/swift/usr/lib/swift/linux/FoundationNetworking.swiftmodule/
/persist/swift/usr/lib/swift/linux/FoundationXML.swiftmodule/
/persist/swift/usr/lib/swift/linux/Glibc.swiftmodule/
/persist/swift/usr/lib/swift/linux/Observation.swiftmodule/
/persist/swift/usr/lib/swift/linux/RegexBuilder.swiftmodule/
/persist/swift/usr/lib/swift/linux/Swift.swiftmodule/
/persist/swift/usr/lib/swift/linux/SwiftOnoneSupport.swiftmodule/
/persist/swift/usr/lib/swift/linux/Synchronization.swiftmodule/
/persist/swift/usr/lib/swift/linux/Testing.swiftmodule/
/persist/swift/usr/lib/swift/linux/_Backtracing.swiftmodule/
/persist/swift/usr/lib/swift/linux/_Builtin_float.swiftmodule/
/persist/swift/usr/lib/swift/linux/_Concurrency.swiftmodule/
/persist/swift/usr/lib/swift/linux/_Differentiation.swiftmodule/
/persist/swift/usr/lib/swift/linux/_FoundationCollections.swiftmodule/
/persist/swift/usr/lib/swift/linux/_RegexParser.swiftmodule/
/persist/swift/usr/lib/swift/linux/_StringProcessing.swiftmodule/
/persist/swift/usr/lib/swift/linux/x86_64/
$ ls -1 /persist/swift/usr/lib/swift/linux | wc -l
57
$ cat /etc/resolv.conf
search home
nameserver <tower>
nameserver 1.1.1.1
```

**GLOSS, in three sentences and no guess beyond them.** The COMPILER
accepts the riscv64 triple: `swiftc -target riscv64-unknown-linux-gnu
-print-target-info` exits 0 and names
`/persist/swift/usr/lib/swift/linux/riscv64` as where it would look for
that target's runtime. THAT DIRECTORY DOES NOT EXIST — the directory
listing above has 23 directories in it, 22 of them `.swiftmodule`
bundles and exactly ONE an architecture, `x86_64` — so a compile for
riscv64 fails at the first import with the module it could not find,
quoted above. WHETHER ONE COULD BE INSTALLED IS NOT ANSWERED BY THIS
LANE and is not invented here: `swift sdk list`, which is the command
that would say what this toolchain can install, exits 127 for a missing
`libxml2.so.2`, and the instance is configured `proxy = no` and has no
route out, so nothing about what could be DOWNLOADED was measured. What
IS measured: the toolchain in this image has the riscv64 target and
lacks the riscv64 runtime, and the missing piece is a directory of
`.swiftmodule` and `.so` files under a name the compiler already prints.
It is item 3 of the awaiting-the owner list.

---

# 10. The guards

## 10.1 The spelling guard

Reproducing command, from the instance:
`python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py <files>`.
The three `.jsonl` stores are presented as the list of their own rows,
which is the one shape the guard reads; the conversion is written to the
lane's work directory and never into the repository.

**LITERAL**, lane `bb2_l10_the_setter_key_the_alarms_and_the_guard.sh`
step [3/4], tower log
`<runs>/bb2/agent/logs/20260912T130738Z__bb2_l10_the_setter_key_the_alarms_and_the_guard.sh.log`:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS bb2_sizes.json -- no operator token in any key, grouping, pairing or row structure
PASS bb2.json -- no operator token in any key, grouping, pairing or row structure
PASS bb2_interp.json -- no operator token in any key, grouping, pairing or row structure
PASS bb2_interp_sizes.json -- no operator token in any key, grouping, pairing or row structure
PASS certificates.json -- no operator token in any key, grouping, pairing or row structure
PASS bb2_bit_blast_runs.json -- no operator token in any key, grouping, pairing or row structure
PASS bb2_interp_runs.json -- no operator token in any key, grouping, pairing or row structure
PASS certificates.json -- no operator token in any key, grouping, pairing or row structure
  guard rc=0
  grep -c exempt over the files this task added:
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/bb2_run.py: 0
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/bitblast.py: 0
```

`check_no_spelling_keys.py` was not modified; nothing under
`Research/op_pipeline/` was touched.

## 10.2 Memory

Bound 6 GB resident, named abort `ABORT_MEMORY_BB2`, checked after every
store line. The peak over the whole pass was **2,427,268 kB**, read off
`resource.getrusage` in the pass's own progress lines; the abort was
never reached. The interpreted loop's peak was 81,904 kB. One process
throughout, no pool.

## 10.3 The conventions verifier

Reproducing command, FROM THIS INSTANCE:
`python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_269_bb2_the_bit_blast_route_on_x86_and_the_interpreted_seven.md`.

The FIRST pass, lane `bb2_l13_the_conventions_verifier.sh`, read **2
DIFFERS**, both in the swift probe of §9: the probe's own rendering puts
`out:` in front of every line, and the `ls` of the swift runtime
directory had been cut down in the log's first draft to the one entry
the sentence was about — a hand-tidied transcript, which this line
forbids. The log was fixed, not the verifier: lane `bb2_l14` re-runs the
three commands raw and §9 pastes what a re-run produces. The tally of
record is §10.4.

## 10.4 The verifier's tally of record

**LITERAL**, lane `bb2_l15_the_conventions_verifier_again.sh` step
[1/2], tower log
`<runs>/bb2/agent/logs/20260912T132227Z__bb2_l15_the_conventions_verifier_again.sh.log`
(the tally was produced over this log as it stood before the tally
itself was pasted into it):

```
population: 40 claims across 1 logs
  MATCHES          2
  DIFFERS          0
  UNVERIFIABLE     33
  REFUSED          5
  NOT_RERUNNABLE   0

ONE LINE: 2 of 40 claims reproduce; 33 (82%) carry nothing to re-run

causes, by name:
  attribution_only                 21
  prose_only                       11
  head_not_on_the_read_only_allowlist 4
  pasted_without_source            1
  log_unreachable                  1
```

**ZERO DIFFERS.** The five REFUSED are four commands whose head is
`/persist/swift/usr/bin/swiftc` or `swift`, which is not on the
verifier's own read-only allowlist, and one `ls -1d` whose glob the
verifier does not expand; none is a claim the verifier disagreed with.
The 33 UNVERIFIABLE are attributions (21) and prose (11) and the one
figure pasted without a command beside it.

Run once more over the log WITH this tally pasted into it, lane
`bb2_l16_the_conventions_verifier_of_record.sh`, tower log
`<runs>/bb2/agent/logs/20260912T132327Z__bb2_l16_the_conventions_verifier_of_record.sh.log`,
so the log a reader holds is the log the verifier answered for:
`claims 41 | MATCHES 2 | DIFFERS 0 | UNVERIFIABLE 34 | REFUSED 5 |
NOT_RERUNNABLE 0`.

## 10.5 The stores this task read, unchanged

**LITERAL**, lane `bb2_l1` step [1/6], the four that matter:

```
40df3b55455f8d7a6e35ef04b7219701b957af65ad08f4d81fd550d911525e72  PseudoCoupHQ/Research/op_pipeline/reference.py
8b27c79cccc7d77e24cdb821a6e4c7de55bbd64be47494b67dd95c3d200ceda1  PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5_cells.json
97f10c28b74eb8f90b18a825ff04a3d03381d1c31c55bcd305deb7f842910d49  PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py
04366247b577a4fd066638086e101e1ec8a62b6e82a5c5b6630e59383536c871  PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/bitblast.py
```

`40df3b55…` is the CORRECTED `reference.py` task ref2 left, the same one
task t4 read.

---

# 11. The two lists

## Decided, recorded for audit

1. **The population is the whole outer set, not the bank's delta.** A
   route's column is not comparable with another's unless it is measured
   over the same 253 cells. The bank's own delta is computed and printed
   beside it (`bb2_run.py preflight`: 2,255 keys certified, 3,984 with
   no certificate, 0 held by the code version, 645 runs the delta would
   execute against the 1,265 this pass executed).
2. **The tier is offered every place, including the places the native
   route proved.** Task t4's tier declines those; this is a third route
   and its own count is the measurement.
3. **The gate is asked in a process of its own under a ten-second wall
   clock.** §7.6 is the measurement it follows from. The verdict of
   record is still `handful.check_one_place`'s, CALLED and not copied.
4. **The carved body's text is kept on the store under a 20,000-
   instruction ceiling** (task bb1's number and its reason: five times
   the 4,000 the gate is offered). The instruction COUNT is exact and
   unbounded on every row. The store is 262 MB.
5. **The rendered source is written beside the store under a 2,000-line
   ceiling** (task bb1's number and reason). Above it the row carries
   the line count and the path is null.
6. **The interpreted work ceiling is 200,000,000 gate evaluations**,
   read off lane `bb2_l5`'s own measured rate (§8), with four cells over
   it carrying their numbers on the row.
7. **An interpreted outcome is `agreed`, never `proved`.**
8. **`render_general.py` was not touched.** The statement-shape adapter
   is in `bb2_run.py` (§7.1).
9. **`bitblast.py` gained three swift branches** (`word_of`, `local`,
   `widened`) and two comments. Each is a branch on a target name task
   bb1 never ran; nothing that file already did changed.
10. **Task t4's pass and task t2's are registered with the bank by name**
    from `bb2_run.py` (§7.3), so a rebuild from here is a delta and not
    a loss.
11. Four runs were left behind by the pass's own left-behind mechanism
    and are named in §6.1.
12. **Two lane scripts were edited AFTER they ran, for the vocabulary
    ban and for nothing else**, and it is disclosed here rather than
    hidden: `bb2_l6_the_pass.sh` named the forked process with a word
    this line forbids (three identifier occurrences, renamed `forked`),
    and `bb2_l1_the_stores_the_sizes_and_the_swift_probe.sh` used
    another in one comment line (now ABORTED). Neither edit changes what
    either lane did; the lane logs on the tower are the run of record
    and are untouched.

## Awaiting the owner

1. **The 32 alarms (§6.6).** Two routes give opposite verdicts on the
   same obligation at 32 certified places, 21 of them go at a 128-bit
   xmm place. Which side is right is an evidence question. Nothing was
   worked around and no cell was edited.
2. **Swift's `@_cdecl` thunk (§7.2).** The carve at the C symbol gets a
   `jmp` into the mangled Swift function at every circuit size, so
   swift's bit-blast column is 13 of 253 where c's is 122. Whether the
   carve should follow the relocation to the mangled symbol is a change
   to the swift route, which this task's brief did not name.
3. **A Swift SDK for riscv64 linux (§9).** The compiler has the target
   and the image has no riscv64 runtime under it; `swift sdk list` is
   itself broken in the image for a missing `libxml2.so.2`, and the
   instance has no route out, so what could be INSTALLED was not
   measured here and is not guessed.
4. **`bitblast.render_gates` is broken in the repository** against the
   current `render_general.assemble` (§7.1), and task bb1's route with
   it. This task adapted on its own side rather than touch task rd1's
   file.
5. **The store is 262 MB and is committed.** It carries what the brief's
   section 4 asks for — the carved body's TEXT per attempt — under task
   bb1's own 20,000-instruction ceiling, which is five times the 4,000
   the gate is offered. That margin is most of the size: a body above
   4,000 instructions was NOT_GATED by definition and its text is text
   nobody can pose. A ceiling of exactly 4,000 would keep every body
   that WAS gated whole and cut the store by most of its bulk, and the
   repository's own `.gitignore` records that this line has met
   GitHub's file-size limits before. Whether to re-write the store's
   transcript bound (the instruction COUNT is exact on every row at
   every size, and no verdict would move) is the owner's call, not this
   task's, and it is not done here.
