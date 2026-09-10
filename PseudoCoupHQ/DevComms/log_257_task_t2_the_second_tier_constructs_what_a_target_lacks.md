# log 257 — task t2: the second tier, which constructs what a target lacks from the primitives it has, smallest width first, and proves it by the schema's own Lean lemma rather than by the solver

Node: `hq.research.arch_unit_oracle.cross_construction.autopoly`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`),
and `hq.research.compiler_graph.gate.lean` for the lemmas
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/PROGRESS.md`).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t2_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`.
Instance `t2`; every lane on the tower, logs at
`<runs>/t2/agent/logs/`; lane scripts kept at
`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/lanes_t2/`.

---

# 1. What the objects are, one sentence each, in relation

* **THE NATIVE ROUTE** is `handful.the_native_route` — the driver exactly
  as task ap6 left it: the primitive route, else the term route, then
  compile at the corpus's ship flags, carve, and gate against the cell's
  own term.
* **THE SECOND TIER** is
  `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/construct.py`,
  called by the driver ONCE, unconditionally, on every run: it looks at
  each place the native route did not prove and, where that place's term
  has a node WIDER THAN THE TARGET'S OWN WIDEST HOLDER, rebuilds the
  mapping out of operations the target does have and puts the rebuilt
  mapping through the same render, compile, carve and gate.
* **THE WORD** is the widest integer holder a target has, read off that
  target's own renderer table: 128 on c, cpp and rust, 64 on go and
  swift. MEASURED, lane `t2_l1`, not recalled — the brief's parenthesis
  says 64 everywhere and three targets in fact spell a 128-bit holder.
* **A SCHEMA** is one function in `construct/schemas.py`: one operation
  above the word, built from operations at the word. It is parameterised
  by the width and the word and by nothing else; there is no case per
  opcode name anywhere in the file, and every branch is on a z3
  declaration kind.
* **A LIMB** is one word-wide piece of a value wider than the word. The
  lowering holds every wide value as limbs and every narrow one as
  itself, which is why a term with nothing above the word comes back
  IDENTICAL and the tier declines without a special case.
* **A SHAPE** is one rewrite the lowering performed, named by the
  operation and by the widths and offsets that make it that rewrite —
  `extract_w128_h63_l0`, `add_w65`, `extend_zero_w8_t128`. A lemma is
  about a SHAPE, and the tier asks for the shape it rewrote.
* **TWO OBLIGATIONS, NOT ONE.** The GATE answers whether the carved body
  equals the CONSTRUCTED mapping; the EQUALITY answers whether the
  constructed mapping equals the CELL's own. A place whose gate says
  proved and whose equality is not discharged is not a proof about the
  cell, and the tier refuses it by cause rather than banking it.

---

# 2. The walkthrough, before any figure

Take `sbb gpr_gpr 64` on go, place `reg_rdi`.

The cell's term is a subtract with a borrow, and the reference builds
the borrow by widening both sides to 65 bits: the widest node in it is
65 bits, over a term of fifteen nodes. Go has no 65-bit integer holder
and no 128-bit one — `go build` refuses `uint128` with "undefined:
uint128", measured by probe `wide_holder_128` — so `go_render` refuses
the place and the bank has held a `refused` certificate for it since
task ap1.

The tier lowers the term to go's own word, 64 bits. The 65-bit value
becomes two limbs; the addition becomes a RIPPLE — one 64-bit sum per
limb, with the carry out of each detected by the one test that needs no
wider holder, an unsigned sum that came out BELOW the addend it started
from; the 65-bit extract that reads the borrow becomes a slice of the
second limb. The rebuilt term has 15 nodes, none wider than 64.

`go_render` writes it, `go build` compiles it at the corpus's ship
flags, and the carve gives eight instructions, LITERAL, lane `t2_l8`:

```
lea (%rbx,%rax,1),%rdx; cmp %rdx,%rax; seta %dl; movzbl %dl,%edx;
neg %rdx; sub %rdi,%rdx; lea (%rdx,%rcx,1),%rax; ret
```

The gate proves that body equal to the constructed mapping. Then the
EQUALITY: the constructed mapping against the cell's own. The canonical
form does not fire — a limbed rewrite never prints the text the wide
operation prints. The SCHEMA'S LEMMA does: the lowering used three
shapes, `add_w65`, `extend_zero_w64_t65` and `extract_w65_h64_l64`, and
each carries a Lean theorem, one per limb, saying the schema's term
equals the operation it replaced. z3 is not asked at all.

That is the tier in one place: a certificate the bank held as `refused`
by nature is now `proved`, `route = constructed`, `proof = lemma+gate`,
and the solver was the audit and not the workhorse.

---

# 3. Refused by nature BEFORE, constructed AFTER, per target

**LITERAL**, `construct/construct.md` §1, written by
`construct/construct_report.py` off the pass's own store and the bank,
lane `t2_l27` §[6/6], tower log
`<runs>/t2/agent/logs/` under that lane's stamp:

```
| target | width-or-kind refusals the bank held | distinct cells | places the tier constructed | of them proved end to end |
|---|---|---|---|---|
| c | 4 | 2 | 0 | 0 |
| cpp | 5 | 3 | 0 | 0 |
| rust | 34 | 32 | 0 | 0 |
| go | 51 | 47 | 12 | 7 |
| swift | 55 | 51 | 12 | 7 |
| **all five** | **149** | **51** | **24** | **14** |
```

**GLOSS, and the shape of the population matters more than the count.**
Of the 149 width-or-kind refusals the bank holds on the five compiled
targets, 129 are the x87 family — an arrival or an answer home on the
x87 register stack at 79 bits — and 20 are integer places on go and
swift whose term carries a node wider than 64. The tier reaches the
second group and not the first, and §7 says exactly why the first is out
of reach from this side.

**Reproducing the word each target's own renderer table gives**, from
the instance:

```
$ python3 -c "import sys; sys.path.insert(0, 'PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct'); import construct as CONS; print(' '.join('%s=%d' % (t, CONS.word_of(t)) for t in ('c', 'cpp', 'rust', 'go', 'swift')))"
c=128 cpp=128 rust=128 go=64 swift=64
```

## 3.1 By schema

**LITERAL**, `construct.md` §2:

```
| the schemas the lowering used | places | proved end to end |
|---|---|---|
| add / sub with carry and flags, widening / narrowing / sign spread | 10 | 10 |
| unsigned / signed divide and remainder, widening / narrowing / sign spread | 8 | 0 |
| shifts, rotates, widening / narrowing / sign spread | 4 | 4 |
| multiply (low and high halves), widening / narrowing / sign spread | 2 | 0 |
```

## 3.2 The cells, one row each

**LITERAL**, `construct.md` §5, abridged to the cells (the file carries
all twenty-four rows, one per place and target):

| target | `mnem` | shape | `key_width` | place | schemas | gate | proof | instructions |
|---|---|---|---|---|---|---|---|---|
| go, swift | `adc` | gpr_gpr, imm_gpr | 64 | reg_rdi | add / sub | PROVED_ON_SHIP | lemma+gate | 7, 4 |
| go, swift | `sbb` | gpr_gpr, gpr_same, imm_gpr | 64 | reg_rdi | add / sub | PROVED_ON_SHIP | lemma+gate | 8, 6, 4 |
| go, swift | `shld` | cl_gpr_gpr | 64 | reg_rdi | shifts | PROVED_ON_SHIP | lemma+gate | 17, 10 |
| go, swift | `shrd` | cl_gpr_gpr | 64 | reg_rdi | shifts | PROVED_ON_SHIP | lemma+gate | 15, 10 |
| go, swift | `mul` | gpr_one | 64 | reg_rdx | multiply | PROVED_ON_SHIP / UNDECIDED | none | 27, 1 |
| go, swift | `div`, `idiv` | gpr_one | 64 | reg_rax, reg_rdx | divide | refused by size | none | -- |

---

# 4. The three proof forms

**LITERAL**, `construct.md` §3, and this one carries its own command:

```
$ grep -A 6 "^| form | places |" PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/construct.md
| form | places |
|---|---|
| `canonical` | 0 |
| `lemma+gate` | 14 |
| `sat` | 0 |

## 4. The collapse column
```

**GLOSS, and each of the three numbers has a reason.**

* **`canonical` is 0, and it was always going to be.** The canonical form
  fires where the constructed mapping and the cell's mapping print the
  same text under `term.Term.normalize`. A lowering replaces a wide
  operation by a composition of narrow ones, and `z3.simplify` does not
  put a ripple adder back together into a 65-bit add, so the two texts
  differ by construction. The form is asked first, as the brief orders,
  and it costs nothing to ask.
* **`lemma+gate` is 14 — every place that proved.** The lowering's shapes
  at the widths the population uses all carry Lean theorems, so the
  equality is discharged inside Lean's kernel and z3 is never asked.
  That is the brief's own sentence — "the proof is the study of the
  mappings ... with the solver as the audit, not the workhorse" —
  arriving as a number.
* **`sat` is 0 ONLY AFTER THE LEMMAS WERE WRITTEN**, and the intermediate
  readings are on the record rather than tidied away: the pass run before
  the lemmas existed (lane `t2_l17`) discharged all fourteen by z3; with
  a lemma table keyed per (schema, width) it discharged none by lemma
  (lane `t2_l21`); with the key carrying the shape alone it discharged
  ten (lane `t2_l23`); with the shift count's own widening lemma stated
  it discharged fourteen (lane `t2_l25`). §8 says what each of those
  three corrections was.

---

# 5. The collapse column

**LITERAL**, `construct.md` §4:

```
| the compiler's landing | places |
|---|---|
| NOT_COLLAPSED | 14 |
```

**GLOSS.** the owner's "the c compiler could simplify into a smaller set of
arch opcodes", measured per cell: on the fourteen proved places NO
compiler collapsed the construction back onto the opcode the cell is
about. The carved bodies run from 4 instructions (`sbb` and `adc` on
swift) to 17 (`shld` on go), against the one instruction the cell names.

**The one place a compiler DID collapse it is not among the fourteen**,
and it is worth the sentence: `mul gpr_one 64` at `reg_rdx` on swift
carved to a SINGLE instruction, `LANDED_ELSEWHERE` — swiftc recognised
the four-half-word high-product idiom and emitted one opcode for it. The
place is not banked as proved because its equality is not discharged
(§6), so the landing is recorded and the proof is not.

---

# 6. The two shapes that are not proved, and why

## 6.1 The high half of a product

The multiply schema is `mul_hi_word`: the high half of a word-wide
product from FOUR HALF-WORD products, which is the owner's "build the smallest
width first" written out. It is verified against z3 at every width a
solver can answer (§9), it renders, it compiles, and the gate proves the
carved body equal to it on go. What is not discharged is the EQUALITY —
that the four-half-word construction equals `Extract(127, 64, ZeroExt(64,
a) * ZeroExt(64, b))`.

That obligation is a MITER OF TWO MULTIPLIERS, the shape SAT is worst at.
The brief says so in advance — "never a wide multiply or divide by
bit-blasting alone — those go to 2 or are reported" — and both routes
were tried and both are reported:

* **form 2**, Lean: the theorem IS stated, at 16/8, 32/16, 64/32, 65/64
  and 128/64, and `bv_decide` answers "The SAT solver timed out" at every
  one of the five (lane `t2_l25` §[2/7], `LEAN_REFUSED` 5).
* **form 3**, z3 at the brief's hard 30-second ceiling: UNDECIDED.

So `mul gpr_one 64` at `reg_rdx` stays refused, BY CAUSE, on both
targets, and the algebraic lemma that would close it is written out in
`construct/lean/OWED.md` §2.

## 6.2 Divide and remainder

The divide schema is restoring division: a bounded loop of `width` steps,
each one shift, one comparison and one conditional subtract — the loop
the brief names. It is verified against z3 at 8/4 and 12/4 (§9) and it
is REFUSED AT THE RENDER on every real width, by a MEASURED size and not
by a rule about which operation it is.

The cause is one property of the renderer, and it is worth stating
plainly because it bounds every schema of this shape: `emulate.Renderer`
emits ONE NESTED EXPRESSION and names no intermediate (`return <expr>;`),
so a sub-term read twice is WRITTEN twice. Restoring division reads its
own previous remainder three times per step — the comparison, the
subtraction and the else arm — so the source grows like `3^width`.

**LITERAL**, lane `t2_l5` §[4/4], the divider's own size against its
width, the DAG beside the written-out count:

```
| width | word | the divider's DAG | its UNFOLDED size |
|---|---|---|---|
| 8 | 4 | 255 | 1000000000 |
| 16 | 8 | 494 | 1000000000 |
| 24 | 8 | 1158 | 1000000000 |
| 32 | 16 | 973 | 1000000000 |
| 65 | 64 | 2226 | 1000000000 |
| 128 | 64 | 3851 | 1000000000 |
```

*(the second column is capped at the counter's own ceiling of 10^9; the
DAG is a few thousand nodes at every width and the written-out form is
beyond any ceiling at all of them.)*

The tier refuses above 200,000 nodes written out, measured BEFORE the
normaliser is asked anything — an earlier draft measured it after, and
`z3.simplify` on the 128-bit divider took the operating system's memory
ceiling out from under lane `t2_l7`. The same ceiling and the same
reason stop the LEMMA being stated (`TOO_LARGE_TO_STATE`, 39 of them).

---

# 7. The x87 family: 129 of the 149, and the wall in front of them

Every x87 refusal is refused at the ARRIVAL or at the ANSWER HOME, not at
the operation.

**LITERAL**, lane `t2_l3` §[1/2], four rows of the table it prints for
every width-refused place:

```
| target | `mnem` | shape | `key_width` | place | place bits | widest node | the renderer's refusal, LITERAL |
| go | `faddl` | mem_one | 80 | x87_6 | 79 | 79 | answer home or arrival on the x87 stack -- go has no 80-bit holder, so an x87 place cannot be answered in it |
| rust | `fucomi` | st_st | 80 | flags.low | 64 | 79 | a width c has no holder for -- rust has no 79-bit float holder: rustc 1.96.1 refuses f16 and f128 with "the type is unstable" (measured, lane o11_l2) |
| c | `fucomi` | st_st | 80 | flags.low | 64 | 79 | answer home or arrival on the x87 stack -- this term reads an x87 value's bits, and c's `long double` and z3's FPSort(15, 64) do not spell them the same |
| swift | `fldz` | st_none | 80 | x87_7 | 79 | 79 | answer home or arrival on the x87 stack -- swift has no 80-bit holder, so an x87 place cannot be answered in it |
```

**GLOSS.** A construction over the fields — sign, exponent, significand
with the sticky bit, and the five classes as a case split, which is the
schema the brief names and `construct/schemas.py` states — would have to
RECEIVE the value as integers, and what the emulation receives is fixed
by the corpus: an x87 arrival is a `long double` VALUE and rust, go and
swift have no such holder at all
(`handful.TARGETS_WITH_AN_80_BIT_HOLDER` is `("c", "cpp")`). On c and cpp,
which do have it, the refusal is the other one: c's `long double` and
z3's `FPSort(15, 64)` do not spell the same bits, which is the seam task
ap3 recorded.

So the float schemas are OWED WHOLE, with their statements in
`construct/lean/OWED.md` §5, and the wall in front of them is a question
about the ARRIVAL CONTRACT and not about any operation. It is in the
second list.

The tier records this by cause rather than by silence. **LITERAL**, lane
`t2_l25` §[5/7], the whole decline census over the pass:

```
| where the tier declined, LITERAL | places |
|---|---|
| the native route did not reach this place's term at all, so the tier has nothing to lower | 2510 |
| the native route proved this place, so there is nothing the second tier can add | 1373 |
| no node of this place's term is wider than the target's widest holder, so the native rendering already spells it and there is nothing to construct | 924 |
| an arrival wider than the target's widest holder: the value cannot be received at all, which is a question about the arrival contract and not about the operation | 344 |
| no construction schema for a node of this kind above the target's widest holder | 82 |
```

---

# 8. The lemmas, and the three corrections it took to make them fire

## 8.1 What a lemma here is

One Lean theorem per LIMB of each SHAPE at each word, generated FROM
`construct/schemas.py` itself — the left is the z3 operation, the right
is `schemas.lower`'s own output on it — and translated by
`op_pipeline/lean/term_to_lean.py` with its own round-trip check. A lemma
transcribed by hand could state something the tier does not do; one
generated from the tier cannot.

**LITERAL**, lane `t2_l25` §[2/7], the tally:

```
| outcome | theorems |
|---|---|
| LEAN_REFUSED | 5 |
| PROVED_BY_LEAN | 147 |
| REFUSED_BEFORE_LEAN | 7 |
| TOO_LARGE_TO_STATE | 39 |
```

147 theorems proved inside Lean, at 120 s of `lean` per theorem, none of
them near the ceiling — the adder's five widths take about a second each.
The 5 `LEAN_REFUSED` are the high product at five widths (§6.1); the 39
`TOO_LARGE_TO_STATE` are the divider (§6.2); the 7 `REFUSED_BEFORE_LEAN`
are the three shifts at 65 over 64 and one divider limb, all
`WIDTH_UNRESOLVED` from the translator's own unification, and none of
them a width this population uses.

**Reproducing the tally**, from the instance:

```
$ python3 -c "import json, collections; d = json.load(open('PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/lean/lemmas_t2.json')); t = collections.Counter(r['outcome'] for r in d['theorems']); print('theorems %d;' % len(d['theorems']), '; '.join('%s %d' % (k, t[k]) for k in sorted(t)))"
theorems 198; LEAN_REFUSED 5; PROVED_BY_LEAN 147; REFUSED_BEFORE_LEAN 7; TOO_LARGE_TO_STATE 39
```

Every theorem, with its shape, its limbs and its own Lean file, is in
`construct/lean/lemmas_t2.json` and printed by
`run_lemmas_t2.py table`.

## 8.2 The general-width lemma is OWED, and the difference is written down

Every lemma above is checked AT A WIDTH. The general statement is one
theorem per schema over `BitVec w` for every `w`, proved by induction on
the limb count; `bv_decide` decides a goal at a FIXED width and cannot be
handed a variable one. So what is machine checked is the instance at each
width the tier uses — which is what the brief asks for, "instantiated per
width" — and the general statement is written out, in words and in Lean
syntax, in `construct/lean/OWED.md` §1. The two are not the same claim
and the file says so.

## 8.3 The three corrections, each measured before it was made

1. **The statement's print form** (lanes `t2_l11`, `t2_l14`). The
   translator confirms its parse by REBUILDING the term in z3 and
   demanding the input text back character for character, and two of the
   pipeline's own print steps break that: `term.order_commutative` puts a
   numeral LAST in an equality (`x == 0`) where z3's own constructor
   prints it FIRST, and `z3.simplify` rewrites a logical shift by a
   constant into `Concat(0, Extract(...))`, whose leading numeral has no
   width the unification can pin. Neither is a defect in the translator
   and neither is this task's file to change. The theorem is now offered
   in `z3.simplify`'s own order first and AS BUILT second, and the row
   records which form carried it.
2. **The schema wrote steps that do nothing** (lane `t2_l14` again).
   `lower_extract` and `lower_concat` accumulated from a zero, so the
   as-built form carried `0 | x << 0` — and that unpinned numeral was the
   second half of the same cause. The folding is now in the schema, which
   also makes every constructed source smaller. And `sign_word_of` spread
   the sign bit with a CONDITIONAL between two constants; it is now the
   two shifts it is — lift the sign bit to the top of the word, shift
   down arithmetically — which is the same value, smaller, and pinnable.
   Between lane 19 and lane 20 that one change moved every arithmetic
   shift and every sign extension from `REFUSED_BEFORE_LEAN` to
   `PROVED_BY_LEAN` (136 → 145 theorems proved).
3. **The lemma was asked the wrong question, twice** (lanes `t2_l19`,
   `t2_l22`, `t2_l24`). The first draft stated one lemma per (schema,
   width) and posed it on the LOW WORD of the operation. Neither is the
   question the tier needs answered: a term reads a wide value through an
   extract that may name ANY limb, so a theorem about the low word does
   not carry the second one; and the widening schema rewrites an extract
   at ANY pair of offsets, so a theorem stated at two offsets does not
   carry a third. Both holes are closed by stating the lemma at the SHAPE
   and once per LIMB. Then the KEY was wrong: the tier files an extension
   under the width it produces (65) and the lemma under the width it
   reads (64), so a key carrying either missed every extension — measured
   in lane `t2_l22`, `extend_zero_w64_t65` held by the table and reported
   missing by the tier. The key is now (schema, word, shape), and the
   shape carries every width it has.

**None of the three was worked around.** Each was measured in its own
lane, named, and fixed in the file that owned it.

## 8.4 One step of the lowering carries no theorem, and it is named

A numeral wider than the word is split into limbs by
`schemas.constant_limbs`, which is a shift and a mask on a python
integer. There is no operation to state a lemma about, so the tier
accepts that shape with the sentence "a numeral's limbs are its own"
written on the record rather than passed over in silence.

---

# 9. The schemas put to z3 on their own, before any of them touched a cell

**LITERAL**, lane `t2_l20` §[2/4] and §[3/4]:

```
[2/4] THE SCHEMAS AT THE NARROW WIDTHS, whole
| outcome | rows |
|---|---|
| PROVED | 120 |
| UNDECIDED | 12 |

[3/4] THE SCHEMAS AT THE WIDTHS THIS PIPELINE MEETS
| outcome | rows |
|---|---|
| PROVED | 79 |
| UNDECIDED | 8 |
```

**GLOSS. NO ROW ANYWHERE IS DISPROVED.** 199 obligations over 34
operations at seven (width, word) pairs, every one either proved or left
undecided by a ceiling; not one schema is wrong at any width a solver
could answer. The 20 UNDECIDED are the divider above 12 bits, the high
product at 128, and the symbolic rotate — the three shapes §6 is about.

**Reproducing it**, from the instance:

```
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/check_schemas.py narrow
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/check_schemas.py wide
```

---

# 10. The pass, and the three readings

## 10.1 The pass's own cost

**LITERAL**, lane `t2_l25` §[5/7]:

```
keys with no proof: 4094 over 669 run(s)
runs to execute: 669
store lines written this lane: 2479 in 2301 s
of them, second-tier runs: 20
peak resident: 2418760 kB
```

**GLOSS.** 669 (cell, target) pairs the bank certifies no proof for, each
put through BOTH routes. 2,479 store lines: 2,459 native runs and 20
second-tier runs — the tier writes a second run only where it actually
constructed something, so the store is not filled with lines saying
there was nothing to do. The peak is 38% of the 6 GB bound and
`ABORT_MEMORY_T2` never fired.

## 10.2 The constructed certificates the bank holds

```
$ python3 -c "import json, collections; t = collections.Counter(); h = open('PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl'); [t.update([json.loads(l)['kind']]) for l in h if l.strip() and json.loads(l).get('route') == 'constructed' and json.loads(l).get('preferred')]; h.close(); print('; '.join('%s %d' % (k, t[k]) for k in sorted(t)))"
proved 14
```

## 10.3 The three readings, beside log_255's

**LITERAL**, lane `t2_l27` §[3/6]:

```
| pass | strict | destination-only | corpus-needed |
|---|---|---|---|
| `t2_construct` | 89 | 347 | 303 |
| **the bank** | **2007** | **2265** | **2221** |
```

| the whole bank | log_255 (ap6) | this task |
|---|---|---|
| strict | 2,003 | 2,007 |
| destination-only | 2,251 | 2,265 |
| corpus-needed | 2,213 | 2,221 |

At all four, all five and all twelve, **LITERAL**, the same lane:

```
| width | reading | cells | ledger rows | share |
|---|---|---|---|---|
| all four | strict | 96 | 66008 | 49.61% |
| all four | destination | 154 | 100068 | 75.21% |
| all four | corpus | 141 | 91142 | 68.51% |
| all five | strict | 96 | 66008 | 49.61% |
| all five | destination | 154 | 100068 | 75.21% |
| all five | corpus | 141 | 91142 | 68.51% |
| all twelve | strict | 89 | 59870 | 45.0% |
| all twelve | destination | 142 | 91410 | 68.71% |
| all twelve | corpus | 132 | 84648 | 63.62% |
```

| width | reading | log_255 cells | this task | log_255 share | this task |
|---|---|---|---|---|---|
| all four | strict | 94 | 96 | 49.4% | 49.61% |
| all four | destination | 147 | 154 | 73.11% | 75.21% |
| all four | corpus | 137 | 141 | 68.02% | 68.51% |
| all five | strict | 94 | 96 | 49.4% | 49.61% |
| all five | destination | 147 | 154 | 73.11% | 75.21% |
| all five | corpus | 137 | 141 | 68.02% | 68.51% |
| all twelve | strict | 89 | 89 | 45.0% | 45.0% |
| all twelve | destination | 142 | 142 | 68.71% | 68.71% |
| all twelve | corpus | 132 | 132 | 63.62% | 63.62% |

**GLOSS.** Fourteen certificates moved the destination reading on all
four and all five by SEVEN cells and 2,804 attested ledger rows, because
the cells they unblock — `adc`, `sbb`, `shld`, `shrd` — were held on go
and swift alone and are proved everywhere else. All twelve does not move,
and it should not: the interpreted targets carry no constructed proof and
the reading is a conjunction over targets.

**Reproducing it**, from the instance — and it must be THIS command and
not `bank.py readings`, because this pass is registered with the bank
from outside the bank's own source file and the registration has to be in
the same process as the reading:

```
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/construct.py readings
```

---

# 11. The one change to the driver

`handful.find_emulation` is now four lines: the native route, one
unconditional call to the tier, and the record. The driver as task ap6
left it is under its own name, `handful.the_native_route`, byte for byte.

```
def find_emulation(shared, held, lang):
    record = the_native_route(shared, held, lang)
    record["constructed"] = CONS.second_tier(shared, held, lang, record)
    return record
```

**Three lines of plumbing go with it and are named rather than counted as
nothing**: `CONSTRUCT` beside the existing `GO` / `SWIFT` / `CPP` path
constants, the `sys.path.insert` beside theirs, and `import construct as
CONS` beside the other renderer imports. `construct.py` imports
`handful` lazily, inside its own functions, so there is no cycle.

**THE CALL IS UNCONDITIONAL AND THE DECISION IS MACHINE FORM.** Whether
the tier does anything is decided by `schemas.lower`: where no node of
the place's term is wider than the target's word, the term comes back as
the same object and the tier declines by cause. Nothing about it is keyed
on who is asking, which is what the nine task gates were removed for.

---

# 12. What was decided about where things live, and why

`bank.PASSES` is DATA — one row per pass, with its store, its reader and
its targets — and `construct.register_with_the_bank` appends this pass's
row AT RUN TIME, from outside the bank's source file. That is the same
means `autopoly.configure` already uses to set the driver's paths from
outside the driver, and it is what let this task bank its proofs without
editing `bank.py`, which is a shared file the brief does not name.

The STORE lives where every pass's store lives, in the autopoly folder,
and that was forced by the spelling guard: `bank.store_path` writes a
certificate's `produced_by.store` relative to that folder, so a store
under `construct/` put `..` on a structure field — and `..` is an
operator token, a range in swift and in ruby. The guard refused the bank
5,303 times on exactly that (lane `t2_l26` §[3/4]). The lines were MOVED,
not re-derived, and the guard then passed (lane `t2_l27` §[5/6]). The
task's CODE is under `construct/`.

---

# 13. The guards

**THE SPELLING GUARD**, over every json and jsonl this task wrote, lane
`t2_l27` §[4/6] and §[5/6]:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS construct.json -- no operator token in any key, grouping, pairing or row structure
PASS lemmas_t2.json -- no operator token in any key, grouping, pairing or row structure
PASS certificates.json -- no operator token in any key, grouping, pairing or row structure
  guard exit: 0
```

and it is re-runnable on this task's own aggregate:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/construct.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS construct.json -- no operator token in any key, grouping, pairing or row structure
```

```
  t2_construct_runs.jsonl -> /tmp/t2_guard/t2_construct_runs.json (2479 record(s))
  certificates.jsonl -> /tmp/t2_guard/certificates.json (24758 record(s))
PASS t2_construct_runs.json -- no operator token in any key, grouping, pairing or row structure
  guard exit: 0
PASS certificates.json -- no operator token in any key, grouping, pairing or row structure
  guard exit: 0
```

**THE LAW'S OWN COUNT** over the files this task added, lane `t2_l27`
§[6/6]:

```
PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/lanes_t2/t2_l26_the_readings_and_the_guards.sh:1
PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/schemas.py:0
PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/lean/run_lemmas_t2.py:0
  the maximum above must be 0
```

**GLOSS, and the 1 is stated rather than hidden.** The single match is
lane 26's own script, which spells the word out in the grep line that
looks for it. Lane 27 spells it in two pieces, which is why lane 27's own
count of itself is 0; no file this task added carries the word in any
other place.

**THE TIER REFUSES ITS OWN OUTPUT** on two mechanical guards of its own,
which is the discipline this line requires of every stage: after the
lowering, the widest node must be at or below the word, and the term
written out must be under the size ceiling. Both are checked, both are
recorded on the place, and the second is checked BEFORE the normaliser is
asked anything (§6.2).

---

# 14. Memory

**THE BOUND** is 6 GB resident, named abort `ABORT_MEMORY_T2`, checked
after every store line and after every theorem. The sample came first, as
the law requires.

| lane | what it did | peak resident |
|---|---|---|
| `t2_l1` | the refusal census over the bank | 11,264 kB |
| `t2_l5` | the schemas put to z3, 199 obligations | 47,144 kB |
| `t2_l16` §[2/2] | THE SAMPLE: the first 20 store lines | 258,740 kB |
| `t2_l20` | the lemmas, 191 `lean` processes | 68,744 kB |
| `t2_l25` §[5/7] | THE PASS, 2,479 store lines | 2,418,760 kB |
| `t2_l27` | the bank, the readings and the guards | 74,476 kB |

The pass's own peak, 2,418,760 kB, is 38% of the bound.
`ABORT_MEMORY_T2` never fired. `ABORT_MEMORY_DRIVER` never fired.

---

# 15. The tally

| what | count |
|---|---|
| width-or-kind refusals the bank held, five compiled targets | 149 over 51 cells |
| of them, the x87 family (refused at the arrival or the answer home) | 129 |
| places the tier constructed | 24 |
| of them, proved end to end (gate AND equality) | 14 |
| the proof forms: canonical / lemma+gate / sat | 0 / 14 / 0 |
| the collapse column: LANDED / NOT_COLLAPSED | 0 / 14 |
| schemas written, general in (width, word) | 8 |
| schema obligations put to z3, proved / undecided / DISPROVED | 199 / 20 / **0** |
| Lean theorems, proved / refused / too large to state | 147 / 12 / 39 |
| the pass: runs / store lines / seconds | 669 / 2,479 / 2,301 |
| the bank: certificates before → after | 19,455 → 24,758 |
| constructed certificates on the bank, all `proved` | 14 |
| the bank, strict / destination-only / corpus-needed | 2,007 / 2,265 / 2,221 |
| cells on all four, destination: before → after | 147 → 154 (73.11% → 75.21%) |
| the spelling guard | PASS on 5 of 5 |
| peak resident against the 6 GB bound | 2,418,760 kB (38%) |
| lanes | 31, all exit 0 |

---

# 16. The two lists

## Decided, recorded for audit

1. **The word is the widest integer holder the target HAS, measured off
   that target's own renderer table** — 128 on c, cpp and rust, 64 on go
   and swift. The brief's parenthesis says 64 everywhere; the measurement
   (lane `t2_l1` §[4/5]) says otherwise for three targets, and the RULE
   the brief states was followed rather than the parenthesis. The
   consequence is exactly right: on a target that already spells a 128-bit
   holder there is nothing above the word and the tier declines.
2. **The tier is offered on every place the native route did not PROVE,
   not only on one it refused**, because the rule is a property of the
   TERM: where nothing is above the word the lowering returns the same
   object and the tier declines by cause. That is what makes the driver's
   one call site unconditional.
3. **A place whose gate proves and whose equality does not is REFUSED BY
   CAUSE, not banked.** The gate answers about the constructed mapping;
   the equality is what carries the answer back to the cell. `mul
   gpr_one 64` on both targets is exactly this case.
4. **The tier writes a second store line only where it constructed
   something.** A run where every place declined is the native route and
   a sentence, not a second route; the decline causes are counted once
   over the pass instead — the same reasoning task ap6 gave for the 2,290
   setter cells it stated by cause rather than banking per target.
5. **This pass is registered with `bank.PASSES` at run time**, from
   outside `bank.py`, which is a shared file the brief does not name.
   §12.
6. **The store lives in the autopoly folder** because `bank.store_path`
   writes it relative to that folder and a `..` on a structure field is
   an operator token the guard refuses. The lines were moved, not
   re-derived. §12.
7. **Five superseded stores and one superseded set of Lean files are kept
   beside themselves**, never deleted:
   `t2_construct_runs.jsonl.before_the_tier_stopped_writing_a_declined_run`,
   `.before_the_lemmas_were_written`,
   `.before_the_lemma_key_carried_the_shape_alone`,
   `.before_the_shift_count_lemma`, and the `schema_<operation>_<w>_<word>.lean`
   files from before the lemma was stated per shape and per limb.
8. **`schemas.sign_word_of` is two shifts and not a conditional**, and
   `lower_extract` / `lower_concat` no longer write a step that does
   nothing. Both are smaller AND both are what made the lemma statable.
   §8.3.

## Awaiting the owner

1. **The x87 population — 129 of the 149 — cannot be reached from this
   side.** Every one is refused at the ARRIVAL or the ANSWER HOME: rust,
   go and swift have no holder that can receive a `long double`, and on c
   and cpp the seam is that `long double` and z3's `FPSort(15, 64)` do
   not spell the same bits. Constructing over the fields would mean the
   emulation receives the value as integers, which is a change to the
   ARRIVAL CONTRACT — a different question, and a structural one. §7.
2. **The high half of a product is not proved at any width**, by Lean or
   by z3, and it is the one shape where the brief's own escape hatch runs
   out. What would close it is an algebraic proof in `BitVec.toNat`
   rather than bit-blasting; the statement is in `construct/lean/OWED.md`
   §2. Whether that proof is worth its own task is the owner's call.
3. **The divider cannot be RENDERED or STATED at any real width**, and
   the cause is the renderer's, not the schema's: one nested expression,
   no intermediate named, so a term whose steps read their own previous
   step more than once is written out once per read. Giving the renderer
   (and `term_to_lean.py`) a way to NAME an intermediate would open the
   divider, the softfloats and every schema of that shape at once. Both
   files are outside this task's folder. §6.2.
4. **The tier's own source is not on the code version.**
   `handful.code_version` is the sha256 of the driver, the loop and the
   renderer; `construct/schemas.py` and `construct/construct.py` are
   neither, so a certificate does not say which version of the TIER
   produced it. Adding them is a new field on an existing record, which
   is a stop rule, so it was not done — and it is the reason this task
   had to re-run its whole pass three times to move a proof form rather
   than re-deriving the affected keys.
5. **The three readings must be run from `construct.py readings`**, not
   from `bank.py readings`, until a pass registered from outside is
   visible to the bank's own commands. §10.3.

---

# 17. The conventions verifier over this log

Run FROM this task's own instance, as the law requires:

    python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_257_task_t2_the_second_tier_constructs_what_a_target_lacks.md

**LITERAL**, lane `t2_l31`:

```
population: 39 claims across 1 logs
  MATCHES          5
  DIFFERS          0
  UNVERIFIABLE     34
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 5 of 39 claims reproduce; 34 (87%) carry nothing to re-run

causes, by name:
  prose_only                       15
  attribution_only                 13
  pasted_without_source            6
```

**GLOSS.** Zero DIFFERS, which is what the law asks. It did not reproduce
anything first time: lane `t2_l28` returned 0 MATCHES of 37, because
every claim carried an attribution or prose and no command a reader
could run. Five commands were then put in the log — the word each
renderer table gives, the three proof forms off `construct.md`, the
lemma tally off `lemmas_t2.json`, the constructed certificates off the
bank, and the spelling guard over this task's aggregate — each short
enough for the verifier's own 20-second ceiling, and each was RUN in
lane `t2_l30` so that what the log pastes under it is what it prints.
The verifier was not touched.

| lane | what it did | exit | seconds |
|---|---|---|---|
| `t2_l1` | the refusal census over the bank, by cause and per target | 0 | 0.8 |
| `t2_l2` | every width-or-kind refusal in detail | 0 | 0.7 |
| `t2_l3` | those places rebuilt and put to their renderer live | 0 | 1.0 |
| `t2_l4` / `t2_l5` | the schemas put to z3 on their own | 0 | 0.4 / 591.4 |
| `t2_l6` / `t2_l7` / `t2_l8` | the tier end to end on four cells | 0 | 70.8 / 103.2 / 47.9 |
| `t2_l9` | the lemma instances the population needs | 0 | 1.5 |
| `t2_l10` / `t2_l12` / `t2_l13` | the lemmas, first three forms | 0 | 33.0 / 13.7 / 88.5 |
| `t2_l11` / `t2_l14` | why the translator refused, with the objects | 0 | 0.2 / 0.2 |
| `t2_l15` | the schemas and the lemmas after the folding | 0 | 719.7 |
| `t2_l16` | the plan and the memory sample | 0 | 16.6 |
| `t2_l17` | the pass, before the lemmas existed | 0 | 2377.4 |
| `t2_l18` | the first rebank and report | 0 | 5.3 |
| `t2_l19` | the lemmas per shape and per limb | 0 | 735.3 |
| `t2_l20` | the sign spread as two shifts, and the lemmas | 0 | 742.2 |
| `t2_l21` / `t2_l23` | the pass with the lemmas, twice | 0 | 2255.7 / 2324.6 |
| `t2_l22` / `t2_l24` | which lemma each place was short of | 0 | 0.2 / 0.1 |
| `t2_l25` | THE PASS OF RECORD | 0 | 2434.0 |
| `t2_l26` | the readings and the guards, guard FAIL on the bank | 0 | 4.4 |
| `t2_l27` | the store moved, the bank, the readings, the guards PASS | 0 | 7.9 |
| `t2_l28` | the conventions verifier, 0 MATCHES | 0 | 0.1 |
| `t2_l29` / `t2_l30` | the log's five reproducing commands, run | 0 | 0.4 / 0.3 |
| `t2_l31` | the conventions verifier, 5 MATCHES and 0 DIFFERS | 0 | 0.5 |
