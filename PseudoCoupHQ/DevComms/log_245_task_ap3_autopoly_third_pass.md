# log 245 — task ap3: AutoPoly's loop, third pass — the vector ARRIVAL as two halves, the x87 cells through c's 80-bit holder, the blocked check un-blocked, and one fix measured alone

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/`).
Line: arch_unit_oracle, the "goal" section of 2026-09-07 and the ruling of
2026-09-08 in
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`.
Law: `PseudoCoupHQ/Research/LAW.md`, read in full including
its tower section; task ap2's first awaiting-the owner item — that the law was
not staged — is answered, it is staged and it was read.
Date: 2026-09-09. Instance `ap3`, on the tower guest.

Artifact folder:
`PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`,
writing `autopoly3_*`; tasks ap1's and ap2's products are not
overwritten. Lane scripts: `.../autopoly/lanes_ap3/`, sixteen of them,
each kept in the repo as the standing rule of 2026-09-07 requires. Every
lane log named below is on the TOWER (`<user>@<tower>`) under
`<runs>/ap3/agent/logs/`.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PseudoCoupHQ`, mounted into
the instance. Every rendering is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself, quoted;
**GLOSS** is a plain-words reading beside a literal.

---

# 1. What this is, one sentence per object in relation

* A **CELL** is one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table, holding the z3 term the reference simulator's
  own builder puts in each place the opcode writes.
* The **OUTER SET** is the 253 cells the canon40 corpus attests, over
  133,044 attested ledger rows — task ap2's, unchanged, including the
  eight `key_width`s its fix 4 moved off null.
* A **RUN** is `find_emulation(cell, lang)` on one of the four compiled
  targets: the target's own operator where its whole lowered body IS the
  cell, the cell's term written in the target's operators where it is
  not, compiled at the corpus's ship flags, carved, and put back to z3
  against the cell's own term.
* **THIS TASK** is that loop run a third time, after two more of the
  causes task ap2 counted were fixed in the layer that owns each, plus
  two measurements the brief asks for on their own: the `check` that has
  been blocked since log_237, and task h2's normalise-before-render.

**THE ANSWER: 151 cells proved on all four targets, 85,530 attested
ledger rows, 64.29%** — up from task ap2's 144 / 85,368 / 64.17% and task
ap1's 120 / 76,634 / 57.6%. Cells proved on NO target fell from 66 to 56,
and their ledger rows from 16,534 to 15,134. Runs carrying a cause: 293
of 1,012, down from 324. **Runs task ap2 proved and this loop does not:
0.**

Two of the four fixes did what they were written to do; the other two are
findings rather than failures, and both are said before the numbers so
the numbers are not read as a disappointment:

* **Fix 2 renders, compiles and LANDS the x87 opcode on c, and proves
  nothing**, because the CANONICAL FORM refuses the body it produces:
  `no answer home` — "this unit's own code names no register the answer
  is left in". A `long double` answer is left in st(0) and its arguments
  arrive on the stack; neither is a register family. §6.
* **Fix 4 is NOT a no-op at scale**: 15 of 1,012 runs render a different
  source with task h2's fix off and 9 differ in verdict — though on none
  of the 9 does a proved run become unproved or an unproved one proved.
  §8.

---

# 2. The lanes

| lane | what it did | log, on the tower |
|---|---|---|
| `ap3_l1_check_unblocked.sh` | FIX 3: the one line in `model_translate.load_rows`, `check` re-run, the artifacts it writes snapshotted and restored | `...182507Z` |
| `ap3_l2_probe_x87_and_the_two_populations.sh` | THE PROBE fix 2 turns on, and what the two populations hold | `...182800Z` |
| `ap3_l3_probe_the_x87_terms.sh` | what the 32 x87 cells' terms actually read, and at what sort | `...182924Z` |
| `ap3_l4_cells_and_guards.sh` | the guards, first pass; it stopped on an import order in the lane's own python block | `...184107Z` |
| `ap3_l5_cells_and_guards_b.sh` | the guards, second pass — **it caught fix 1 reaching the handful's two vector cells** | `...184137Z` |
| `ap3_l6_cells_and_guards_c.sh` | the guards, third pass; its twenty-run sample **caught the bare `st` prefix refusing `push`** | `...184253Z` |
| `ap3_l7_guards_again_and_the_sample.sh` | **THE GUARDS OF RECORD**, fix 1 measured on its 40 pairs, and the twenty-run memory sample | `...184435Z` |
| `ap3_l8_measure_fix2.sh` | fix 2 on its 128 pairs, first pass; it **caught `KeyError: 79`** and showed the c rendering in full | `...184634Z` |
| `ap3_l9_probe_the_x87_body.sh` | why the gate says the c body of an x87 cell carries no body | `...184747Z` |
| `ap3_l10_measure_fix2_again.sh` | **FIX 2'S MEASUREMENT OF RECORD** | `...184842Z` |
| `ap3_l11_run_the_loop.sh` | **THE LOOP**: 1,012 runs in 1,431 s | `...184846Z` |
| `ap3_l12_run_the_loop_with_the_fix_off.sh` | **FIX 4'S OTHER LOOP**: the same 1,012 runs with task h2's fix OFF, 1,418 s | `...191240Z` |
| `ap3_l13_aggregate_and_report.sh` | the aggregate, the report, the store check, the spelling guard, the tally | `...193711Z` |
| `ap3_l14_claims.sh` | the claims of this log, first pass | `...193740Z` |
| `ap3_l15_claims2.sh` | **THE CLAIMS OF RECORD** (the fix-4 table now prints the first line that differs, not two whole sources) | `...193930Z` |
| `ap3_l16_the_appendix.sh` | the probe, the `check` tally and fix 4's table appended to `autopoly3.md`, each generated | `...194048Z` |

---

# 3. FIX 3 — `model_translate.py check` runs again

**THE DEFECT**, open since log_237 §14 item 1 and blocking a guard since
task ap2 (log_244 §7): `load_rows` read task o2's artifact by the field
name `mnemonic`, which task mn1 renamed to `mnem`, so `check` stopped on
`KeyError: 'mnemonic'` and `check_L2` could not be re-derived by anyone.

**THE CHANGE**, the one line in a shared file the brief authorises.
**LITERAL**, from
`PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py`:

```
    for language in ("c", "cpp", "go", "rust", "swift"):
        group = document["single_opcode_groups"][language]["narrow"]
        for index, row in enumerate(group):
            rows.append({"lang": language, "row_index": index,
                         # task mn1 renamed this field to `mnem`;
                         # `mnemonic` is task o2's older artifact,
                         # accepted as a fallback (task ap3).
                         "mnem": row.get("mnem",
                                         row.get("mnemonic")),
```

**THE TALLY**, which is the brief's own guard. **LITERAL**, lane
`ap3_l1_check_unblocked.sh`, on the tower at
`<runs>/ap3/agent/logs/20260909T182507Z__ap3_l1_check_unblocked.sh.log`:

```
[3/6] the stored tally, off the artifact as it stands
   check_L2.json rows: 259
      DISCREPANCY  19
      REFUSED      87
      STATED       153

[4/6] python3 model_translate.py check
rows: 259
  REFUSED                  87
  STATED                   172
definitions after the check: 4006
```

**GLOSS.** Exactly the brief's expectation: 259 rows, 87 REFUSED, 172
STATED — and 153 + 19 = 172, the 19 being what the LEAN RUN of record
turned from STATED into DISCREPANCY. No number is a finding.

**WHAT THE LANE PROTECTED, and why it had to.** `check_command`
OVERWRITES `lean/check_L2.json` and rewrites every
`lean/archproof/Archproof/*.lean`. The stored `check_L2.json` carries the
Lean run's 19 DISCREPANCY verdicts, which a fresh `check` cannot know;
and nothing but the one line is authorised to change under
`Research/op_pipeline`. So the lane sha256'd every file `check` can
write, ran it, copied the regenerated `check_L2.json` into THIS task's
artifact folder as `autopoly3_check_L2_rerun.json`, and restored the
originals. **LITERAL**, same lane:

```
[6/6] restore, then sha256 against BEFORE
   RESTORED IDENTICAL: every file check_command wrote is back to its stored bytes
```

Every one of the `.lean` files did move while `check` ran, and all are
back; the two sha256 listings are in the lane log in full.

---

# 4. THE PROBE, which fix 2 was not written until it landed

The brief's rule is the order: probe first, and render the x87 cells as
`long double` only if clang emits the x87 opcode for one at the corpus's
own ship flags.

**LITERAL**, lane `ap3_l2_probe_x87_and_the_two_populations.sh`, on the
tower at
`<runs>/ap3/agent/logs/20260909T182800Z__ap3_l2_probe_x87_and_the_two_populations.sh.log`:

```
   the compiler: /usr/bin/clang
   the ship flags, LITERAL: -std=c17 -O1 -c
   the flags' source, LITERAL: lane_gen.py compile_probe: `[CLANG, "-std=c17"] + ["-O1"] + ["-c", src, "-o", obj]` -- the ship build of every c unit in the corpus

   -- probe 'add', the source LITERAL:
      long double emu_probe_ld_add(long double a, long double b)
      {
          return a + b;
      }
      the carved body, LITERAL: fldt 0x18(%rsp); fldt 0x8(%rsp); faddp %st,%st(1); ret
      instructions: 4; the mnemonics whose spelling begins with f: ['faddp', 'fldt']

   -- probe 'mul', the source LITERAL:
      long double emu_probe_ld_mul(long double a, long double b)
      {
          return a * b;
      }
      the carved body, LITERAL: fldt 0x18(%rsp); fldt 0x8(%rsp); fmulp %st,%st(1); ret
      instructions: 4; the mnemonics whose spelling begins with f: ['fldt', 'fmulp']
```

**GLOSS. THE PROBE LANDS.** c's `long double` is the x86-64 80-bit
extended format and clang lowers arithmetic on it to the x87 opcode
itself. rust, go and swift have no 80-bit floating holder at all — `f64`,
`float64` and `Double` are the widest each spells — so their rows are
refused BY NATURE and not by a defect, which is the brief's own rule.

**cpp is the other target the brief names for this fix and it is NOT one
of this loop's four.** Adding a fifth target changes what "proved on all
four" counts, which is structural; it is on the awaiting-the owner list and was
not done.

---

# 5. FIX 1 — a 128-bit arriving vector register is two 64-bit arriving values

**THE DEFECT.** Task ap2's fix 3 answered the ANSWER side — a 128-bit
written place is two 64-bit written places — and left the ARRIVAL side
behind as the cause `vector arrival used beyond its low lane`, 40 runs
over 5,600 attested ledger rows on all four targets (log_244 §11).

**THE POPULATION, measured before anything was written. LITERAL**, lane
`ap3_l2`, same log:

```
| cell | targets | the place | bits | the arrival read beyond bit 63 | how it is read |
|---|---|---|---|---|---|
| `andpd` xmm_xmm 128 | c,go,rust,swift | `reg_xmm0.high` | 64 | seed_xmm0 Extract(127, 64); seed_xmm1 Extract(127, 64) | collect_uses |
| `movapd` xmm_xmm 128 | c,go,rust,swift | `reg_xmm0.high` | 64 | seed_xmm1 Extract(127, 64) | collect_uses |
| `unpckhpd` xmm_xmm 128 | c,go,rust,swift | `reg_xmm0.low` | 64 | seed_xmm0 Extract(127, 64) | collect_uses |
| `unpckhpd` xmm_xmm 128 | c,go,rust,swift | `reg_xmm0.high` | 64 | seed_xmm1 Extract(127, 64) | collect_uses |
```

(ten cells in all; the four rows above are the shapes, the log holds every
row.)

**THE FIX, one sentence**, in the driver
(`handful.vector_arrivals_in_halves`): where a place's term reads a
128-bit vector arrival above bit 63, that arrival is rewritten as
`Concat(seed_<family>_high, seed_<family>_low)` — two 64-bit arriving
values — so the place is rendered from two parameters the target CAN
receive, and the gate aligns them against the arrival's own two 64-bit
slices, because `pool100_entry_equivalence.family_bits` gives a family
that is not a vector register 64 bits and `align_by_row` puts each half
on its own IN row.

**WHY IT IS PER PLACE AND NOT PER CELL, and the guard is what taught it
that.** The first pass rewrote the arrival wherever the CELL read one
wide, and lane `ap3_l5` caught it on the handful's own two vector cells:
`addss` xmm_xmm 32's place is the whole 128-bit register — the lane the
operation writes, joined under the arrival bits it leaves alone — so the
place DOES read `seed_xmm0` above bit 63, and task h2's fix 2 projects
the lane out of it before anything is rendered. The test is now
`emulate.Renderer.collect_uses` asked of the place, and a place task h2's
fix will project is passed through untouched.

**THE MEASUREMENT OF RECORD. LITERAL**, lane
`ap3_l7_guards_again_and_the_sample.sh`, on the tower at
`<runs>/ap3/agent/logs/20260909T184435Z__ap3_l7_guards_again_and_the_sample.sh.log`:

```
task ap2's own runs carrying a cause holding 'beyond its low lane': 40

the 40 pairs, by what they say now:
     31  PROVED: proved
      9  the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either
```

**GLOSS.** 31 of the 40 prove. The 9 that do not are `movaps`, `movapd`
and `movdqa` on c, rust and swift, and their cause is not this fix's: the
compiler emits an EMPTY body for a register-to-register vector copy whose
answer is its own argument, so there is no ship code to walk. That cause
was already in task ap2's table with 23 runs and is now 68 (§7).

---

# 6. FIX 2 — the 32 x87 cells, and the two things the objects said

## 6.1 They were never flag consumers

Task ap2 recorded these 128 runs as `no setter row to compose the flag
pair from: None at width 8` and read the cause as a missing setter; its
own §5 showed the corpus records no x87 mnemonic as a flag consumer at
all. Task ap3 asked the other side of it.

**LITERAL**, lane `ap3_l2`, same log, its last count:

```
   cells with at least one DESTINATION place reading the arriving flag state: 0 of 32
```

**GLOSS.** Not one of the 32 rows reads `seed_FLAG_L` or `seed_FLAG_R`.
`cell_input` composed a setter for every row the sweep marked
`preseeded`, and `preseeded` says only that the sweep HANDED the builder
a flag state, not that the opcode read it. **The fix is one condition**
(`handful.a_place_reads_the_arriving_flags`): a preseeded row is composed
with a setter only where one of its own terms actually reads the arriving
flag state. `cmovne` gpr_gpr 32 and `setne` gpr_one 8 are the guard and
both still compose with `test` (§9, guard 4).

## 6.2 What their terms hold, and what c can write

**LITERAL**, lane `ap3_l3_probe_the_x87_terms.sh`, on the tower at
`<runs>/ap3/agent/logs/20260909T182924Z__ap3_l3_probe_the_x87_terms.sh.log`:

```
| `faddl` mem_one 80 | `x87_6` | 79 | seed_X87_0:FPSort(15, 64) x87__rsi_:FPSort(15, 64) | REFUSED term reads state that is not an arrival register: seed_X87_0 |
| `fucomi` st_st 80 | `flags` | 158 | seed_X87_0:FPSort(15, 64) seed_X87_1:FPSort(15, 64) | REFUSED term reads state that is not an arrival register: seed_X87_1 |

the sorts the 32 cells' terms read, and how often:
   FPSort(15, 64)           64

ONE CELL IN FULL, `faddl` mem_one 80 -- the row's own line and the place's term, LITERAL:
   the row's line: faddl (%rsi)
   place `x87_6`, 79 bits:
      (fp.to_ieee_bv (fp.add roundNearestTiesToEven seed_X87_0 x87__rsi_))
```

**GLOSS, and the 79-against-80 seam, which is the whole of why this fix
is written the way it is.** Every arrival of these cells is
`reference.X87_SORT`, `FPSort(15, 64)`, and an x87 place is 79 bits as z3
spells it — a sign bit, 15 exponent bits and a 63-bit fraction. The same
value IN MEMORY is 80 bits, the extra one being the explicit integer bit
the hardware stores and z3 does not. So a `memcpy` between a `long
double` and a 79-bit holder would be a DIFFERENT FUNCTION from
`fp.to_ieee_bv`, and the fix never writes one: the driver hands the
renderer the FLOAT under the place's own `fp.to_ieee_bv`
(`handful.the_x87_value`, the x87 counterpart of task h2's
`projected_lane`), and the rendered function answers a `long double` in
st(0), which is where the c calling rule leaves it. Where a term reads an
x87 value's BITS inside itself — which is exactly what an x87 compare's
flag pair is — there is nothing to hand over and the place is REFUSED by
cause. Lane `ap3_l8` is what found that: before it, those two places
raised `KeyError: 79` out of `Renderer.helper_text`, looking for an
unsigned holder 79 bits wide. That was a defect in this task's own new
code and it is now a refusal.

## 6.3 It renders, it compiles, it lands — and the canonical form refuses the body

**LITERAL**, lane `ap3_l8_measure_fix2.sh`, on the tower at
`<runs>/ap3/agent/logs/20260909T184634Z__ap3_l8_measure_fix2.sh.log`:

```
== faddl mem_one 80 -> c
   place `x87_6`, 79 bits, home X87_0, families ['X87_0', 'x87__rsi_']
   rendered: True
   THE RENDERED SOURCE, LITERAL:
      long double
      emu_faddl_mem_one_80__x87_6__c(long double a, long double b)
      {
          return ((long double)((a) + (b)));
      }
   compiled: True
   the carved body, LITERAL: fldt 0x18(%rsp); fldt 0x8(%rsp); faddp %st,%st(1); ret
   landing: NOT_COLLAPSED
   the gate: UNDECIDED -- the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either

== faddl mem_one 80 -> rust
   rendered: False
   refusal: answer home or arrival on the x87 stack: rust has no 80-bit holder, so an x87 place cannot be answered in it
```

**WHY THE GATE SAYS "no body" WHEN THE BODY IS RIGHT THERE**, asked of
the object rather than reasoned about. **LITERAL**, lane
`ap3_l9_probe_the_x87_body.sh`, on the tower at
`<runs>/ap3/agent/logs/20260909T184747Z__ap3_l9_probe_the_x87_body.sh.log`:

```
   arrival_families                 []
   body_text                        'fldt 0x18(%rsp); fldt 0x8(%rsp); faddp %st,%st(1); ret'
   entry_contract                   {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'result': 'xmm0'}
   outcome                          'REFUSED'
   refusal                          "this unit's own code names no register the answer is left in, so there is nothing to store into OUT-0"
   refusal_cause                    'no answer home'

body_verbatim: None
canon40 outcome: 'REFUSED'
```

**GLOSS, and it is a STOP under the law's stop rules rather than a
result to work around.** The canonical form — a shared layer, not the
driver — models an arrival and an answer as REGISTER FAMILIES. A `long
double` argument is classed X87 by System V and arrives IN MEMORY on the
stack; a `long double` answer is left in st(0). Neither is a register
family, so `canonical_form.render_one` refuses the unit `no answer home`,
`body_verbatim` is never set, and `reference.body_lines` says the record
carries no body. Teaching the canonical form an x87 answer home would be
a change to a shared file the brief did not name AND an ontology question
— what is an arrival that is not a register — which is the same question
the arrival-contract group has been awaiting a ruling on since task g1b.
It is flagged in §12 and nothing was shimmed over it.

**THE MEASUREMENT OF RECORD. LITERAL**, lane
`ap3_l10_measure_fix2_again.sh`, on the tower at
`<runs>/ap3/agent/logs/20260909T184842Z__ap3_l10_measure_fix2_again.sh.log`:

```
the 128 pairs, by what they say now:
     92  answer home or arrival on the x87 stack
     30  the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either
      6  a width c has no holder for
```

**GLOSS.** 92 are refused by nature — 90 of them are the 30 arithmetic
cells on rust, go and swift, and 2 are the x87 compares on c, whose flags
place reads an x87 value's bits. 30 are the c rows that render, compile
and carve to the x87 opcode and meet the canonical form. 6 are the x87
compares' 94-bit high half on the three targets with no 128-bit integer
holder. **Zero of the 128 now carry a cause that is false about the
objects**, which is what this fix was for.

---

# 7. THE table: per target, what the loop reached

**LITERAL**, lane `ap3_l15_claims2.sh`, on the tower at
`<runs>/ap3/agent/logs/20260909T193930Z__ap3_l15_claims2.sh.log`:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly3.py tables
## 1. THE table: per target, what the loop reached

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.

| step or verdict | c | rust | go | swift |
|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `compiled` | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `LANDED` | 76 cells, 41829 rows, 31.44% | 72 cells, 39199 rows, 29.46% | 30 cells, 22970 rows, 17.26% | 70 cells, 38915 rows, 29.25% |
| `LANDED_ELSEWHERE` | 27 cells, 11867 rows, 8.92% | 23 cells, 11885 rows, 8.93% | 16 cells, 5448 rows, 4.09% | 35 cells, 18714 rows, 14.07% |
| `NOT_COLLAPSED` | 142 cells, 73383 rows, 55.16% | 114 cells, 73310 rows, 55.1% | 154 cells, 91600 rows, 68.85% | 95 cells, 62389 rows, 46.89% |
| `proved` | 163 cells, 89630 rows, 67.37% | 166 cells, 94779 rows, 71.24% | 170 cells, 99240 rows, 74.59% | 159 cells, 87998 rows, 66.14% |
| `proved under caller extension` | 20 cells, 20530 rows, 15.43% | 21 cells, 21502 rows, 16.16% | 0 cells, 0 rows, 0.0% | 17 cells, 19778 rows, 14.87% |
| `sat` | 14 cells, 4212 rows, 3.17% | 15 cells, 5085 rows, 3.82% | 16 cells, 5157 rows, 3.88% | 5 cells, 3723 rows, 2.8% |
| `undecided` | 48 cells, 12707 rows, 9.55% | 7 cells, 3028 rows, 2.28% | 14 cells, 15621 rows, 11.74% | 19 cells, 8519 rows, 6.4% |
| `refused` | 8 cells, 5965 rows, 4.48% | 44 cells, 8650 rows, 6.5% | 53 cells, 13026 rows, 9.79% | 53 cells, 13026 rows, 9.79% |

## 2. Per target, how far the primitive route reached

Table 2 -- `primitive` is a target operator whose whole lowered body IS the cell; `primitive+setup` is that plus zero-operand accumulator setup (task g1c's widened lookup); `term` is the cell's own term written in the target's operators, which is the fallback.

| route | c | rust | go | swift |
|---|---|---|---|---|
| `primitive` | 29 cells, 19706 rows, 14.81% | 22 cells, 12245 rows, 9.2% | 17 cells, 10351 rows, 7.78% | 9 cells, 7774 rows, 5.84% |
| `primitive+setup` | 2 cells, 1726 rows, 1.3% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |
| `term` | 222 cells, 111612 rows, 83.89% | 231 cells, 120799 rows, 90.8% | 236 cells, 122693 rows, 92.22% | 244 cells, 125270 rows, 94.16% |
| `no route reached` | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |

Table 3 -- a cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 4 of 4 | 151 | 85530 | 64.29% |
| 3 of 4 | 29 | 27938 | 21.0% |
| 2 of 4 | 8 | 3081 | 2.32% |
| 1 of 4 | 9 | 1361 | 1.02% |
| 0 of 4 | 56 | 15134 | 11.38% |

`sat` at the plain comparison, every written place: 152
`sat` surviving the caller-extension re-pose: 67
the handful's forty pairs: 32 agree character for character, 36 agree on the verdict, 4 not in this outer set
```

**GLOSS**, three readings the table does not make on its own.

* **THE POLYFILL-COMPLETE SET IS 151 CELLS, 85,530 attested ledger rows,
  64.29%**, against task ap2's 144 / 85,368 / 64.17% and task ap1's 120 /
  76,634 / 57.6%. Proved on none fell from 66 cells / 16,534 rows /
  12.43% to 56 / 15,134 / 11.38%.
* **`no route reached` IS ZERO ON EVERY TARGET**, where task ap2 had 32
  cells on each. That is fix 2's whole visible effect on this table: the
  32 x87 cells now have a route, and on c they reach the compiler.
* **c's `undecided` rose from 8 cells to 48 and its `refused` fell from
  54 to 8.** Those are the same 30 x87 c rows moving from a refusal
  before the render to a gate call the canonical form declines (§6.3),
  plus the 40 vector runs. A cell that reaches the gate and is declined
  is not better proved than one refused earlier; it is measured further
  along, and the cause it now carries is true.

---

# 8. FIX 4 — task h2's normalise-before-render, measured alone on 1,012 runs

The whole loop was run twice, all else as task ap2 left it and both of
this task's own fixes on, with one module-level switch moved:
`handful.NORMALISE_BEFORE_RENDER`. The OFF loop wrote its own store
(`autopoly3_off_runs.jsonl`) and its own source folder (`src3_off/`), so
neither loop can read or write the other's.

**LITERAL**, lane `ap3_l15_claims2.sh`, same log:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly3.py fix4 | sed -n '1,6p'
runs with the fix ON  (autopoly3_runs.jsonl): 1012
runs with the fix OFF (autopoly3_off_runs.jsonl): 1012
pairs on both: 1012

runs whose RENDERED SOURCE differs between the two loops: 15
runs whose VERDICT differs between the two loops: 9
```

and the verdict table in full:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly3.py fix4 | grep -A 10 'the verdict with the fix OFF'
| run | the verdict with the fix OFF | the verdict with the fix ON |
|---|---|---|
| div|gpr_one|8|rust | NOT_COLLAPSED (8) / DISPROVED, DISPROVED under caller extension | NOT_COLLAPSED (8) / DISPROVED, UNDECIDED under caller extension |
| idiv|gpr_one|16|c | NOT_COLLAPSED (21) / DISPROVED, DISPROVED under caller extension | NOT_COLLAPSED (21) / UNDECIDED, DISPROVED at 30000 ms |
| idiv|gpr_one|16|rust | NOT_COLLAPSED (21) / DISPROVED, UNDECIDED under caller extension | NOT_COLLAPSED (21) / DISPROVED, DISPROVED under caller extension |
| setnp|gpr_one|8|c | NOT_COLLAPSED (26) / PROVED_ON_SHIP | NOT_COLLAPSED (19) / PROVED_ON_SHIP |
| setnp|gpr_one|8|go | NOT_COLLAPSED (42) / PROVED_ON_SHIP | NOT_COLLAPSED (49) / PROVED_ON_SHIP |
| setnp|gpr_one|8|rust | NOT_COLLAPSED (26) / PROVED_ON_SHIP | NOT_COLLAPSED (19) / PROVED_ON_SHIP |
| setp|gpr_one|8|c | NOT_COLLAPSED (27) / PROVED_ON_SHIP | NOT_COLLAPSED (20) / PROVED_ON_SHIP |
| setp|gpr_one|8|go | NOT_COLLAPSED (42) / PROVED_ON_SHIP | NOT_COLLAPSED (49) / PROVED_ON_SHIP |
| setp|gpr_one|8|rust | NOT_COLLAPSED (27) / PROVED_ON_SHIP | NOT_COLLAPSED (20) / PROVED_ON_SHIP |
```

**GLOSS. THE FIX IS NOT A NO-OP AT SCALE, and it does not move a single
proof.** It reaches 15 of 1,012 runs and 9 of them answer differently.
What the 15 are is two shapes, and the first line the two sources differ
on is the measurement:

* **Nine float cells** (`addsd`, `addss`, `subsd`, `subss` on rust, swift
  and c) where the fix changes only the ORDER of a commutative operand
  pair: `(b) + (a)` off, `(a) + (b)` on. **LITERAL**, same command:
  `` `f64::from_bits((((((b) + (a))).to_bits() as u64)) as u64)` `` against
  `` `f64::from_bits((((((a) + (b))).to_bits() as u64)) as u64)` ``. None of
  the nine changes a verdict.
* **Six `setp` / `setnp` cells** on c, rust, go and swift, where the fix
  changes the SHAPE of the parity computation and the compiler emits a
  materially different body: 26 instructions off against 19 on for c and
  rust, 27 against 20 for `setp`, and the other way on go, 42 against 49.
  All are PROVED_ON_SHIP on both sides.
* **Three divide runs** where the two loops differ only in which of
  `DISPROVED` and `UNDECIDED` the solver reached inside its ceiling —
  the ceiling being a FLAG, and neither answer a proof.

**So the fix stays ON**, which is where task ap2 left it: it never turns
a proof into a non-proof, it shrinks the rendered body on the two cells
where it changes the shape at all on c and rust, and its 24-place no-op
result from task h2 is confirmed on 997 of 1,012 runs rather than
assumed.

---

# 9. The guards

**LITERAL**, lane `ap3_l7_guards_again_and_the_sample.sh`, same log:

```
   handful.TASK ap3  fixes_are_on True  primitive_first True  setup_is_allowed True  NORMALISE_BEFORE_RENDER True
   emulate.X87_ARRIVAL, LITERAL: ('X87_', 'x87_')
   emulate.FLOAT, LITERAL: {16: '_Float16', 32: 'float', 64: 'double', 79: 'long double'}
   handful.TARGETS_WITH_AN_80_BIT_HOLDER, LITERAL: ('c',)

   GUARD 2: places of the handful's ten cells that come out IDENTICAL (name, width, layer-5 text, arrival families): 14
   places that DIFFER: 0
   places task ap3 produces that task g1b's product has no row for: 0  []

   GUARD 3: the vector places of the handful, and whether task ap3's fix 1 touched their arrivals
      addss     xmm_xmm   32   reg_xmm0     bits 128  halved: False arrivals_in_halves: None families ['xmm0', 'xmm1']
      cvtsi2sd  gpr_xmm   64   reg_xmm0     bits 128  halved: False arrivals_in_halves: None families ['rdi', 'xmm0']

   GUARD 4: the setter each flag-reading cell of the handful composes with, and the reason the driver gives
      cmovne    gpr_gpr   32   setter test     why: the setter this cell's own attestation records the most ledger rows for
      setne     gpr_one   8    setter test     why: the setter this cell's own attestation records the most ledger rows for

   GUARD 6: THE PLACES OF `push` gpr_one 64, the cell the bare `st` prefix refused
      `stack_-8` bits 64 home None families ['rdi'] x87? False
```

and guard 1, `handful.py sources_counts`, **LITERAL**, the same lane, on
the tower at
`<runs>/ap3/agent/logs/20260909T184435Z__ap3_l7_guards_again_and_the_sample.sh.log`:

```
NOT_RENDERED 4
ONE_SIDE_REFUSED 4
SOURCE_UNCHANGED 24
identical to the file task h1 wrote under src: 24 of 24 rendered
```

**GLOSS.** Both fixes are UNGATED in `handful.py` — neither is switched
on by a task name, for the reason `handful.use_task_ap2`'s docstring gave
and `use_task_ap3` repeats: a task-name gate is what let task h2's fix 1
fall out from under three tasks. So every guard asks the same question,
and all five answer it. Task h2's 24 sources are unchanged (guard 1). The
handful's 14 places come out of the driver identical in name, width,
layer-5 text and arrival families to task g1b's own product (guard 2).
The handful's two vector cells are untouched by fix 1 (guard 3, the
brief's own guard on it). `cmovne` and `setne` still compose with `test`
(guard 4). `push` gpr_one 64 writes `stack_-8`, which is not an x87 place
(guard 6, added after the bare `st` prefix claimed it).

**THE STRONGEST GUARD IS THE CHANGE TABLE'S: runs task ap2 proved and
this loop does not: 0** (§10).

---

# 10. The change table

**LITERAL**, lane `ap3_l15_claims2.sh`, same log:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly3.py change | sed -n '1,20p'
runs on task ap2's store: 1012
runs on task ap3's store: 1012
pairs on both: 1012

Table C1 -- every cause of task ap2's loop, what it counted then, and what those same runs say now.

| task ap2's cause | ap2 runs | ap3 runs, same cause | where the rest went |
|---|---|---|---|
| PROVED | 688 | 688 | -- |
| no setter row to compose the flag pair from: None at width 8 | 128 | 0 | 92 answer home or arrival on the x87 stack; 30 the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either; 6 a width c has no holder for |
| the gate answered sat: the body holds on a region, not on every input | 50 | 49 | 1 the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| term reads state that is not an arrival register | 48 | 20 | 22 answer home or arrival on the x87 stack; 6 the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| vector arrival used beyond its low lane | 40 | 0 | 31 PROVED; 9 the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 23 | 23 | -- |
| a width c has no holder for | 18 | 18 | -- |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 11 | 10 | 1 the gate answered sat: the body holds on a region, not on every input |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | 2 | 2 | -- |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | 2 | 2 | -- |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows | 1 | 1 | -- |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 1 | -- |
```

and the two summary counts, same command:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly3.py change | grep -E '^runs task ap2 proved|^pairs that moved to'
runs task ap2 proved and task ap3 does not: 0
pairs that moved to `sat`: 1
```

**GLOSS.** All 1,012 pairs join and every one of task ap2's 688 proved
runs is proved again; the regression list is empty. Two of task ap2's
causes are gone entirely — `vector arrival used beyond its low lane` (40
runs, 31 of them now proved) and `no setter row to compose the flag pair
from` (128 runs, none of which was ever a flag pair). The 28 runs that
left `term reads state that is not an arrival register` are the x87
memory operands and stack positions fix 2 admits as arriving values.

**THE ONE PAIR THAT MOVED TO `sat`** is `idiv` gpr_one 16 on rust, which
task ap2 left UNDECIDED at the 3,000 ms ceiling and which now answers
with a counterexample: `[IN_0 = 32768, IN_1 = 0, IN_2 = 673554405]`. 32768
is `0x8000`, the most negative 16-bit value — the signed-division
overflow edge, where the quotient of `-32768 / -1` has no 16-bit
representation. Nothing about the gate was touched; the solver reached an
answer this time inside the same ceiling.

---

# 11. Every `sat`, the re-pose, and the arrival-contract group

**LITERAL**, lane `ap3_l15_claims2.sh`, same log:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly3.py sat | grep -v counterexample
sat at the plain comparison, every written place: 152
sat surviving the caller-extension re-pose: 67
   c      19
   go     19
   rust   22
   swift  7
the five surviving sat places with the most ledger rows:
   ucomiss    xmm_xmm      32    c      [flags] 2270 rows
   ucomiss    xmm_xmm      32    go     [flags] 2270 rows
   ucomiss    xmm_xmm      32    rust   [flags] 2270 rows
   ucomiss    xmm_xmm      32    swift  [flags] 2270 rows
   ucomisd    xmm_xmm      64    c      [flags.low] 1026 rows
```

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly3.py repose
places UNDECIDED at the 3,000 ms ceiling of record and re-posed once at 30,000 ms: 147
   DISPROVED        3
   PROVED_ON_SHIP   3
   UNDECIDED        141

| cell | lang | place | route | ledger rows | the re-pose's answer |
|---|---|---|---|---|---|
| `div` gpr_one 32 | c | reg_rdx | term | 384 | DISPROVED |
| `div` gpr_one 16 | swift | reg_rdx | term | 36 | DISPROVED |
| `div` gpr_one 8 | go | reg_rax | term | 28 | PROVED_ON_SHIP |
| `div` gpr_one 8 | swift | reg_rax | term | 28 | PROVED_ON_SHIP |
| `idiv` gpr_one 16 | c | reg_rax | term | 16 | DISPROVED |
| `idiv` gpr_one 8 | go | reg_rax | term | 8 | PROVED_ON_SHIP |
```

**GLOSS.** `sat` is 152 places at the plain comparison against task ap2's
154, and 67 survivors against 69 — the same population, the same regions,
and **no `sat` was touched**, which the brief requires. The re-pose is a
FLAG followed literally: 147 places were re-posed at 30,000 ms, six moved,
and the verdict OF RECORD stays the 3,000 ms one in every case.

**THE ARRIVAL-CONTRACT GROUP IS UNCHANGED. LITERAL**, same lane, from
`causes`:

```
places the gate declined on the IN-row alignment: 38
   17 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows
   12 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 2 IN rows
   5 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows
   4 place(s): the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows
```

38 places over the same 12 cells task ap2 recorded, and the by-cause table
carries the same 5 runs on c at the destination place. The brief's
instruction was that these cells are not touched, and they are not.

---

# 12. The by-cause table

**LITERAL**, lane `ap3_l15_claims2.sh`, same log:

```
$ python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly3.py causes | sed -n '1,16p'
Table 5 -- what did not work, by cause, the four targets summed. `rows` counts a cell's attested ledger rows once per run, so a cause seen on all four targets counts them four times.

| cause | runs | ledger rows | targets |
|---|---|---|---|
| answer home or arrival on the x87 stack | 114 | 10478 | c, go, rust, swift |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 68 | 27611 | c, go, rust, swift |
| the gate answered sat: the body holds on a region, not on every input | 50 | 18177 | c, go, rust, swift |
| a width c has no holder for | 24 | 12169 | go, rust, swift |
| term reads state that is not an arrival register | 20 | 18020 | c, go, rust, swift |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 11 | 3820 | c, go, rust, swift |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | 2 | 840 | c |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | 2 | 1726 | c |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows | 1 | 5190 | c |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 | c |

runs carrying a cause: 293 of 1012
```

**GLOSS.** Ten causes rather than eleven, and 293 runs rather than 324.
The largest is now `answer home or arrival on the x87 stack` at 114 runs
— the refusal BY NATURE the brief asked for, on the three targets with no
80-bit holder plus the two x87 compares on c. The second, at 68 runs, is
`this unit record carries no body`, and it is two different things summed:
23 runs of an empty compiled body (a vector register copy the compiler
elides), 30 of the x87 c bodies the canonical form refuses (§6.3), and 15
more of the same two kinds on the cells fix 1 and fix 2 moved. That is the
one place in this table where one cause name covers two situations, and it
is named here rather than split, because splitting it would be inventing a
new outcome name.

---

# 13. Memory

The bound stated in `Airlock/instances/ap3.conf`, in every
lane header and in `autopoly3.py`'s own constants is 6 GB resident on the
one collecting process, named abort `ABORT_MEMORY_AP3`, checked after
every run. The sample the law asks for is the first twenty runs, printed
with the peak after each; twenty runs took 18 s and the peak was 261,712
kB.

| lane | what it read | peak resident |
|---|---|---|
| `ap3_l2_probe_x87_and_the_two_populations.sh` | the cells file and task ap2's store | 85,044 kB |
| `ap3_l3_probe_the_x87_terms.sh` | the same, and the 32 cells' terms rebuilt | 80,824 kB |
| `ap3_l7_guards_again_and_the_sample.sh` | the two reads, 40 measured pairs, then 20 runs | 261,712 kB |
| `ap3_l10_measure_fix2_again.sh` | the two reads, then 128 pairs re-run | 261,492 kB |
| `ap3_l11_run_the_loop.sh` | the two reads, then 1,012 runs | 2,419,276 kB |
| `ap3_l12_run_the_loop_with_the_fix_off.sh` | the same, 1,012 runs | 2,383,220 kB |
| `ap3_l13_aggregate_and_report.sh` | the whole 1,012-run store | 87,560 kB |
| `ap3_l15_claims2.sh` | both 1,012-run stores | 104,112 kB |

The high-water mark, 2,419,276 kB, is 39% of the bound. No abort fired.
Task ap2's own run lane ended at 1,450,280 kB and task ap1's at 2,414,988
kB over the same run count; the three are not comparable as a claim about
the code, because the three lanes ran different amounts of z3 work, and
that is left as the measurement it is.

**One measurement in this task is defective and is named rather than
dropped:** lane `ap3_l1_check_unblocked.sh` ends with `peak resident: 0
kB`, because its last line asks `resource.getrusage(RUSAGE_CHILDREN)` in
a python process that has forked no child. It is a defect in that lane's
own footer and not a measurement of anything; the lane's real work is
`model_translate.py check` in a separate process, whose peak that call
cannot see.

---

# 14. The deliverables

Under
`PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/`:

| file | what it is |
|---|---|
| `autopoly3.py` | the loop, the bookkeeping, the aggregate, the report, the per-fix measurement, the change table, the OFF loop and fix 4's comparison |
| `autopoly3_cells.json` | the 253 attested cells, task ap2's file copied and its counts re-measured |
| `autopoly3_runs.jsonl` | the incremental store of the loop of record, 1,012 lines |
| `autopoly3_off_runs.jsonl` | fix 4's other loop, 1,012 lines |
| `autopoly3.json` | the aggregate |
| `autopoly3.md` | the report, 600 lines, its §7 the appendix lane `ap3_l16` generates |
| `autopoly3_check_L2_rerun.json` | the `check` re-derived, kept here rather than over the stored artifact |
| `src3/`, `src3_off/` | the rendered sources of the two loops |
| `lanes_ap3/` | the sixteen lane scripts |
| `autopoly3_runs.jsonl.before_the_guards_passed`, `...before_the_x87_bits_refusal` | the two partial stores written before the guards passed, moved aside and NOT removed |

Changed outside that folder:

| file | the change |
|---|---|
| `Research/op_pipeline/lean/model_translate.py` | FIX 3, the one line the brief authorises in a shared file |
| `Research/oracle/cross_construction/emulation/handful/handful.py` | the driver: `vector_arrivals_in_halves`, `a_place_reads_the_arriving_flags`, `x87_as_arrivals`, `the_x87_value`, `home_of`'s x87 convention, `expected_families`'s refusal, `NORMALISE_BEFORE_RENDER`, `use_task_ap3` |
| `Research/oracle/cross_construction/emulation/emulate.py` | the c renderer: `FLOAT[79] = "long double"`, `is_an_x87_arrival`, the x87 arrival plan, the x87 answer home, and the refusal of `fp.to_ieee_bv` at the x87 width |

`lean/check_L2.json` and every `lean/archproof/Archproof/*.lean` were
written by `check` and RESTORED byte for byte; the lane's sha256
comparison is §3.

---

# 15. The guard and the tally

**LITERAL**, lane `ap3_l13_aggregate_and_report.sh`, on the tower at
`<runs>/ap3/agent/logs/20260909T193711Z__ap3_l13_aggregate_and_report.sh.log`:

```
[3/6] the store and the aggregate compared run for run
lines on the store: 1012
runs on the aggregate: 1012
run for run identical: 1012
distinct (cell, target) pairs: 1012
[4/6] the spelling guard, over every json this task wrote
operator inventory: 91 tokens read from probe_manifest_*.json
PASS autopoly3_cells.json -- no operator token in any key, grouping, pairing or row structure
PASS autopoly3.json -- no operator token in any key, grouping, pairing or row structure
PASS autopoly3_check_L2_rerun.json -- no operator token in any key, grouping, pairing or row structure
```

and the tally, **LITERAL**, the same lane, on the tower at
`<runs>/ap3/agent/logs/20260909T193711Z__ap3_l13_aggregate_and_report.sh.log`:

```
[6/6] the tally
runs recorded: 1012 of 1012

| target | attempted | rendered | compiled | LANDED | proved | sat | undecided | refused |
|---|---|---|---|---|---|---|---|---|
| c | 253 | 245 | 245 | 76 | 163 | 14 | 48 | 8 |
| rust | 253 | 209 | 209 | 72 | 166 | 15 | 7 | 44 |
| go | 253 | 200 | 200 | 30 | 170 | 16 | 14 | 53 |
| swift | 253 | 200 | 200 | 70 | 159 | 5 | 19 | 53 |
```

**`grep -c exempt` over what this task added is 0 everywhere except one
file, and that file is the lane that runs the grep.** Its two matches are
its own two lines — `echo "[5/6] no exemption anywhere in what this task
wrote"` and `grep -c exempt "$A/autopoly3.py" "$A/lanes_ap3/"*.sh` — and
there is no exemption in any product.

---

# 16. The two lists

## Decided, recorded for audit

1. **The law was staged and read in full**, including the tower section,
   which answers the first awaiting-the owner item of log_244.
2. **Both driver fixes are UNGATED on a task name**, for the reason
   `use_task_ap2` gave and `use_task_ap3` repeats; the five guards of §9
   are what a task name would have been standing in for and all five
   pass.
3. **Fix 1 is applied PER PLACE, not per cell**, and a place task h2's
   fix 2 will project a lane out of is left to task h2's fix (§5). The
   guard is what taught it that, and the first form of the fix is
   recorded as having been wrong rather than quietly replaced.
4. **`emulate.is_an_x87_arrival` spells `X87_` and `x87_` and NOT a bare
   `st`** (§9, guard 6). The bare prefix also spells `push`'s `stack_-8`
   place and refused the corpus's third-most-attested cell on all four
   targets; the twenty-run sample of lane `ap3_l6` is what caught it.
5. **An x87 value's BITS are refused rather than memcpy'd** (§6.2). c's
   `long double` and z3's `FPSort(15, 64)` differ by the explicit integer
   bit, so a helper at that width would be a different function from the
   node it stands for.
6. **An x87 place's answer home is `X87_0` BY CONVENTION**, written into
   `handful.home_of` beside the convention the flags place already
   carries, because the c calling rule leaves a `long double` answer in
   st(0).
7. **An x87 place is not halved** (`in_halves_where_it_must_be`): halving
   exists because no target can answer more than 64 bits, and c can
   answer this place whole. The consequence is stated rather than hidden:
   these rows are NOT comparable target for target, which is the brief's
   own "rust, go and swift are refused by nature".
8. **The `check` was re-derived without changing the stored artifact**
   (§3): every file `check_command` writes was snapshotted, compared by
   sha256 and restored, and the re-derived `check_L2.json` sits in this
   task's own folder.
9. **The arrival-contract cells and every `sat` were not touched** (§11).
   The group is the same 38 places over the same 12 cells.
10. **Two partial stores were moved aside and nothing was removed.** The
    40 lines written before the guards passed and the 20 written before
    the `KeyError: 79` was refused are beside the store with
    `.before_the_guards_passed` and `.before_the_x87_bits_refusal`
    suffixes. Nothing under `<runs>/` or `Airlock/`
    was deleted on either machine; three lane names collided and each
    took a new name.
11. **Task h2's normalise-before-render stays ON** (§8), on the
    measurement rather than on the assumption: it reaches 15 of 1,012
    runs, changes 9 verdicts, and moves no proof either way.

## Awaiting the owner

1. **The canonical form has no answer home and no arrival for a value
   that is not in a register** (§6.3), and that is now what stops the 30
   x87 c rows: they render, compile and carve to the x87 opcode, and
   `canonical_form.render_one` refuses the unit `no answer home`. It is
   the same question as the arrival-contract group and it is now measured
   on the ANSWER side as well as the arrival side. Ontology, not
   implementation, and a shared file this brief did not name.
2. **The arrival-contract question still needs the ruling task g1b asked
   for**: 38 places over 12 cells, unchanged (§11).
3. **cpp is named by the brief for fix 2 and is not one of this loop's
   four targets** (§4). Adding a fifth changes what "proved on all four"
   counts, which is structural. `model_translate.load_rows` already walks
   five compiled languages including cpp, so the corpus has the rows.
4. **A whole 128-bit vector arrival now HAS a holder** — two 64-bit
   parameters — which retires item 3 of log_244's list on the arrival
   side; what remains of it is item 2 above.

---

# 17. The conventions verifier over this log

Two passes, each a lane of this task's own instance, each over this log
as it then stood.

| pass | lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|---|
| first | `ap3_l17_verify_245.sh` | 32 | 7 | **0** | 24 | 1 | 0 |
| second | `ap3_l18_verify_245b.sh` | 32 | 8 | **0** | 24 | 0 | 0 |

**GLOSS**, and the obligation the law states is the DIFFERS column: **0**
on both passes.

* **The one REFUSED of the first pass was fixed in the CLAIM and never in
  the verifier.** One pasted command cut its output with `sed -n '/the
  verdict with the fix OFF/,$p'`, and the verifier read the `$p` as a
  file path it could not reach. The same eleven lines are now cut with
  `grep -A 10`, which is why the second pass has 8 MATCHES rather than 7.
  Two bare pastes — task h2's `sources_counts` and the tally — were given
  the lane log they came from, which moves them from
  `pasted_without_source` to `attribution_only` and leaves the
  UNVERIFIABLE count where it was.
* **MATCHES (8)** — `tables`, `causes`, `repose`, `sat`, `fix4` in its
  two pieces, and `change` in its two pieces.
* **UNVERIFIABLE (24)** — eight prose paragraphs (the answer, the two
  findings said before the numbers, the polyfill-complete reading, the
  cpp note, fix 4's conclusion, the change table's gloss, and the first
  item of the awaiting-the owner list) and sixteen attributions, each naming
  the lane log it came from.

This section was appended after the second pass, and a third pass over
the log WITH it in place — lane `ap3_l19_verify_245c.sh`, the closing one
— returns the identical tally: 32 claims, 8 MATCHES, 0 DIFFERS, 24
UNVERIFIABLE, 0 REFUSED, 0 NOT_RERUNNABLE. The count has reached its
fixed point, so the table above is the log as it stands.
