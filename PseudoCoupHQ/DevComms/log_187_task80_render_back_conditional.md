# log 187 — task 80: render_back's conditional template

Date: 2026-09-03. Node:
`hq.research.compiler_graph.term.render_back`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_6_term/node_0_3_5_6_5_render_back/`).

Report shape: Appendix B (one numbered tree, high to low, values in
motion at the leaves). Renderings are labelled **LITERAL** or **GLOSS**
per §5.1a. Failures are grouped by cause, never by sighting (§5.3).
Every count carries its population (§3.4a).

---

# 1. What was asked, and what came back

## 1.1 The one-sentence answer

The one fixed rule that renders a proved z3 term back into runnable
arch text gained the CONDITIONAL template, read off the corpus's own
ship bodies. Over the same population round 13 measured — the 26,040
units of the 30,432 canon39-proved ones whose layer-4 term was proved —
the return path went from **5,909 rendered / 5,873 proved / 20,131
refused** to **11,911 rendered / 11,876 proved / 14,129 refused**.
Every one of the 6,002 units the conditional template itself rendered
was assembled by the real `as`, read back by the real `objdump -d`, and
PROVED_ON_SHIP by `Gate.prove_wrapped` against its own ship body. No
unit the conditional template rendered failed to prove.

## 1.2 The five headline numbers, each with its population

| figure | round 13 | this round | population |
|---|---|---|---|
| rendered | 5,909 | **11,911** | the 26,040 units with a proved layer-4 term, of the 30,432 canon39-proved units |
| assembled by `as` | 5,909 | **11,911** | the same 26,040 |
| round-tripped through `objdump -d` | 5,909 | **11,911** | the same 26,040 |
| PROVED_ON_SHIP | 5,873 | **11,876** | the same 26,040 |
| refused, by cause | 20,131 across 17 causes | **14,129 across 20 causes** | the same 26,040 |
| distinct rendered texts | 105 | **420** | the same 26,040 |
| distinct layer-3 wrapped texts | 1,905 | 1,905 | the same 26,040 |

Evidence class: **forced by construction** for the rendered, assembled
and round-tripped counts (the real assembler either took the text or
did not); **solver proof over the reference's model** for
PROVED_ON_SHIP (z3 unsat on the difference, which is a proof about the
model of the machine, and the model is the reference's testimony).

## 1.3 The template's own result, isolated

The `if` cause was 13,027 units of that 26,040 — round 13's largest
refusal by a factor of six. Measured over exactly those 13,027:

- **6,002 rendered, 6,002 assembled, 6,002 round-tripped, 6,002
  PROVED_ON_SHIP.** Zero of them rendered and then failed to prove.
- **7,025 still refused**, under six finer causes, each named in §5.2.
- 315 distinct rendered texts among the 6,002, in five languages:
  c 1,930, cpp 3,522, go 88, rust 90, swift 372.

## 1.4 What is NOT claimed

- The 35 units that rendered and did not prove this round are **not**
  the conditional template's. Not one of their rendered bodies spells a
  comparison or a flag read; 35 of round 13's own 36 non-proofs are the
  same units. §6 is the finding, with its counterexample.
- No claim is made that the rendered text equals the compiler's text.
  0 of 11,911 are character-identical to their layer-3 text, the same
  as round 13, because the rule always routes through the fixed temp
  pool where the compiler wrote in place.

---

# 2. The shape was read off the corpus, before any template was written

## 2.1 Why this step exists

The brief's own instruction: take the template from the units whose
ship bodies compute a conditional, do not invent one. So a measuring
pass ran first and wrote nothing but tallies:
`probe80_conditional_shapes.py` walked all 31,078 units of the 332
canon39 shards and grouped their flag-setting/flag-reading windows by
MACHINE FORM — every register replaced by the position it first appears
at, so the same shape in different registers counts once.

## 2.2 What the machine actually does — LITERAL

From `probe80_conditional_shapes_printed.txt` (population: 31,078
units; 15,884 of them spell a flag-reading arch opcode):

```
the flag-setting arch opcode the read binds to:
  set    after test          7114
  set    after cmp           6726
  set    after ucomiss       3560
  set    after ucomisd       1388
  cmov   after test           803
  cmov   after ucomiss        284
  cmov   after cmp            145
  cmov   after ucomisd        116

how many lines back that setter sits:
  set     1 lines back   15604
  set     2 lines back    2512
  cmov    2 lines back     614
  cmov    1 lines back     460

THE SHAPE ITSELF -- setter through read, registers replaced by first-appearance position.
     5691  test <0>,<0>; setne <1>
     1262  cmp <0>,<1>; setne <2>
      848  cmp <0>,<1>; sete <2>
      749  cmp <0>,<1>; setl <2>
      272  test $0x40,<0>; cmovne <1>,<2>
      188  test <0>,<0>; setne <1>; or <2>,<3>; setne <4>
```

**GLOSS**, beside that literal: the machine's conditional is two
instructions. One sets the flags — a subtraction whose answer is thrown
away (`cmp`), or a conjunction whose answer is thrown away (`test`).
The next reads them through a two-letter suffix, and either writes 1 or
0 into eight bits (`set<cc>`) or moves one register into another
(`cmov<cc>`). The reader binds to the MOST RECENT setter, which is why
15,604 of the 18,788 `set<cc>` reads sit exactly one line after theirs.
The reads that bind to a setter in the same body number 20,136 in all:
18,788 `set<cc>` and 1,348 `cmov<cc>`; a further 2,601 reads have no
flag setter before them in their own body, which the probe reports and
this rule never has to render, because it emits its own comparison.

## 2.3 The rule takes one of the two setters, not both

The template writes `cmp right,left` for every comparison. `test x,x`
is the same statement about a value the body has already computed
(`build_flag_only` in `reference.py` gives `test` the triple
`("test", left & right, 0)` and `cmp` the triple `("cmp", left,
right)`), so one shape covers both and no choice between them enters
the rule.

## 2.4 A measured confirmation of the suffix choice

A condition has several spellings on this machine (`ae`, `nb` and `nc`
are one condition). The rule picks the shortest, ties by alphabet —
deterministic, no judgment. The 14 suffixes it picks are
character-for-character the 14 the corpus's own bodies write:

```
the rule picks:  e ne l ge le g b ae a be s ns p np
the corpus writes (probe80, "condition suffixes on the flag READ"):
  ne 9341, p 1748, ae 1401, e 1358, a 1221, l 996, g 872, be 722,
  le 696, ge 693, b 579, s 266, ns 231, np 12
```

---

# 3. The CORE was corrected first, then PROGRESS, then code

## 3.1 The shape the tree lacked

The round-13 design says the walk computes **each sub-term into the
pool register at its own depth**. A conditional brings a sub-term whose
sort is Bool, and this machine never puts a Bool in a register: `cmp`
leaves it in the flags and a suffix reads them. So the walk needed a
second kind of step, which computes into no register and returns no
width. That shape was not in the tree, so it went into the tree first
(PROTOCOL §2; log_158's binding rule).

## 3.2 What was added to the CORE

`CORE_0_3_5_6_5_render_back.md`, `## design`, three new parts:
`condition_table` (attribute), `emit_condition` and `emit_choice`
(methods). Four new settled rules, each with a decision source:

1. **A predicate has no register; it has the flags.** Source: the
   corpus's own bodies, measured — `probe80_conditional_shapes_printed.txt`.
2. **The comparison is emitted after the arms, never before.** Source:
   `condition_table.py`'s own "most recent flag setter" rule, and
   `reference.predicate_of`, which reads the triple the last
   flag-setting opcode left.
3. **The condition suffix and its complement come from the one
   condition table.** Source: the reference CORE's "meanings come from
   one table"; `reference.predicate_of` is the builder this template
   inverts.
4. **An 8-bit choice is refused by name.** Source: the same discipline
   the 8-bit multiply refusal already carries in this file.

## 3.3 PROGRESS

Six entries appended at the moment of progress, each with its evidence
link: the CORE correction, the corpus reading, the build, population
two, the template's isolated result, population one, the guard, and the
remaining named causes. File:
`Planning/…/node_0_3_5_6_5_render_back/PROGRESS.md`.

---

# 4. The template itself, with values in motion

## 4.1 The inverse map, and where each half comes from

- The **condition name** comes from `condition_table.cond_to_z3` read
  backwards. That function's body says `if cond == "CondSLT": return
  L < R`; the table `PREDICATE_CONDITION` in `term.py` is that line and
  its nine co-lines the other way round. No second table of meanings is
  written.
- The **suffix** comes from `condition_table.SUFFIX_TO_COND` read
  backwards (§2.4).
- The **complement** — needed because z3's simplifier prints `a != b`
  as `Not(a == b)` — is not typed in either. It is PROVED at
  construction: for each pair of conditions, z3 is asked whether one
  can differ from the negation of the other, over fresh 64-bit symbols.
  The 14 answers it returns are what the rule uses.
- The **flag-reading mnemonic** is kept only where
  `Reference.opcode_table` holds it WITH a builder. `cmovg` is absent
  from that table — no body in the corpus spells one — so no template
  exists for it and a choice wanting it is refused by name. LITERAL,
  from the run's own construction:

```
set mnemonics:  14 of 14 conditions
cmov mnemonics: 11 of 14 conditions  (cmovg, cmovp, cmovnp absent)
```

## 4.2 Shape one — the arms are the literals 1 and 0

**LITERAL**, from `render_back80_one_unit_printed.txt`, unit `c/op_0`:

```
ITS OWN SHIP BODY, as the compiler wrote it:
    xor %eax,%eax
    test %edi,%edi
    sete %al
    ret

its arrival contract: families ['rdi'], answer home rax at 8 bits

LAYER 3, the same body wrapped:
    mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi; xor %eax,%eax; test %edi,%edi; sete %al; mov ledger+0x38(%rip),%r11; mov %al,0x0(%r11); ret

ITS TERM, as the reference walk left it:
    Extract(7, 0, ZeroExt(56, If(0 == Extract(31, 0, seed_rdi) & Extract(31, 0, seed_rdi), 1, 0)))

the same term simplified once, which is what the return path renders:
    If(Extract(31, 0, seed_rdi) == 0, 1, 0)

THE RENDERED BODY, by the one fixed rule:
    mov %rdi,%r11
    mov $0x0,%r10d
    cmp %r10d,%r11d
    sete %r11b
    mov %r11b,%al
    ret

THE RENDERED TEXT, wrapped by the same CanonicalForm.wrap layer 3 goes through:
    mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi; mov %rdi,%r11; mov $0x0,%r10d; cmp %r10d,%r11d; sete %r11b; mov %r11b,%al; mov ledger+0x38(%rip),%r11; mov %al,0x0(%r11); ret

ASSEMBLED by the real `as` and read back by the real `objdump -d`:
    instructions written 10, read back 10
       0:	48 8b 3d 00 00 00 00 	mov    0x0(%rip),%rdi
       7:	48 8b 3f             	mov    (%rdi),%rdi
       a:	49 89 fb             	mov    %rdi,%r11
       d:	41 ba 00 00 00 00    	mov    $0x0,%r10d
      13:	45 39 d3             	cmp    %r10d,%r11d
      16:	41 0f 94 c3          	sete   %r11b

THE GATE'S VERDICT, the rendered text against this unit's OWN ship body:
    outcome: PROVED_ON_SHIP
```

**GLOSS with values in motion**, beside that literal. Take the input
row IN-0 filled with 5.

1. `mov IN-0,%rdi` — the prelude puts 5 in `%rdi`. That is the arrival
   contract, unchanged from layer 3.
2. `mov %rdi,%r11` — the walk reaches the free symbol `seed_rdi` and
   copies it into the first pool register: `%r11` = 5. The term's
   `Extract(31, 0, …)` is a low slice at a register width, so it costs
   no instruction; the value is simply read as `%r11d` from here on.
3. `mov $0x0,%r10d` — the comparison's right side is the literal 0, and
   a literal becomes a register like anything else: `%r10d` = 0.
4. `cmp %r10d,%r11d` — AT&T order is `cmp SRC,DST`, and
   `build_flag_only` reads DST as the left of the pair, so the left
   term sits in `%r11d`. The flags now say 5 − 0.
5. `sete %r11b` — the suffix `e` is `CondEQ`, which is what the term's
   `==` maps to. 5 ≠ 0, so `%r11b` = 0.
6. `mov %r11b,%al` — the root moves to the answer home at the answer
   width, 8 bits.
7. `mov %al,OUT-0` — the epilogue stores it. The runner reads 0.

With IN-0 = 0 the same walk leaves `%r11b` = 1 and OUT-0 = 1, which is
what the compiler's own `xor`/`test`/`sete` leaves. The gate proves
this for EVERY value of the input row, not for these two.

## 4.3 Shape two — the arms are two values

**LITERAL**, same file, unit `c/op_179`:

```
ITS OWN SHIP BODY, as the compiler wrote it:
    mov %edi,%eax
    test %esi,%esi
    cmove %esi,%eax
    ret

its arrival contract: families ['rdi', 'rsi'], answer home rax at 32 bits

the same term simplified once, which is what the return path renders:
    If(Extract(31, 0, seed_rsi) == 0, Extract(31, 0, seed_rsi), Extract(31, 0, seed_rdi))

THE RENDERED BODY, by the one fixed rule:
    mov %rdi,%r11
    mov %rsi,%r10
    mov %rsi,%rax
    mov $0x0,%ecx
    cmp %ecx,%eax
    cmove %r10d,%r11d
    mov %r11d,%eax
    ret

ASSEMBLED by the real `as` and read back by the real `objdump -d`:
    instructions written 14, read back 14
          15:	49 89 fb             	mov    %rdi,%r11
          18:	49 89 f2             	mov    %rsi,%r10
          1b:	48 89 f0             	mov    %rsi,%rax
          1e:	b9 00 00 00 00       	mov    $0x0,%ecx
          23:	39 c8                	cmp    %ecx,%eax
          25:	45 0f 44 da          	cmove  %r10d,%r11d
          29:	44 89 d8             	mov    %r11d,%eax

THE GATE'S VERDICT, the rendered text against this unit's OWN ship body:
    outcome: PROVED_ON_SHIP
```

**GLOSS with values in motion.** Take IN-0 = 7 (arriving in `%rdi`) and
IN-1 = 0 (arriving in `%rsi`).

1. The ELSE arm is emitted first, into the destination register:
   `mov %rdi,%r11` — `%r11` = 7.
2. The THEN arm next: `mov %rsi,%r10` — `%r10` = 0.
3. Only now the comparison, two registers further down the pool:
   `mov %rsi,%rax` (`%rax` = 0), `mov $0x0,%ecx` (`%ecx` = 0),
   `cmp %ecx,%eax`. The flags say 0 − 0.
4. `cmove %r10d,%r11d` — the condition holds, so `%r11d` takes the then
   arm: `%r11d` = 0.
5. `mov %r11d,%eax`, then the epilogue stores `%eax`. OUT-0 = 0.

With IN-1 = 4 the comparison fails, the conditional move does nothing,
and OUT-0 = 7 — the else arm. **The order in step 3 is the load-bearing
part**: had the comparison been emitted before the arms, the arms' own
`mov`s would sit between the setter and the reader, and any arm doing
arithmetic would overwrite the flags the reader needs.

## 4.4 Nesting composes by the same rule

A choice inside a choice, or a choice under a bit operator, is ordinary
recursion: `emit_choice` calls `emit`, which reaches `emit_choice`
again at a deeper pool register. This is also what the corpus writes —
`test <0>,<0>; setne <1>; or <2>,<3>; setne <4>`, 188 sightings. Of the
26,040 proved terms, 4,081 carry more than one `If`, and those that
render do so through this recursion with no extra rule.

---

# 5. Refusals, by cause

## 5.1 The whole population, 14,129 refused of 26,040

LITERAL, from `render_back80_tally_printed.txt` (20 causes; the
sightings each cause carries as evidence are in the file):

```
    2678  a joining of 33 pieces
    2364  a shift whose count is not a literal
    1618  a choice at 8 bits has no conditional move
    1587  a joining whose upper piece is not a literal
    1452  no comparison template for the z3 predicate 'and'
    1200  no comparison template for the z3 predicate 'fp.isNaN'
     564  a value of 1 bits fits no register width
     487  an 8-bit multiply has no two-operand instruction
     464  no template for the z3 operator 'fp.to_ieee_bv'
     417  no template for the z3 operator 'bvsdiv_i'
     416  no template for the z3 operator 'bvsrem_i'
     240  no comparison template for the z3 predicate 'or'
     233  no template for the z3 operator 'bvudiv_i'
     233  no template for the z3 operator 'bvurem_i'
      65  the term reads a register the arrival contract does not name
      43  a joining of 3 pieces
      38  a value of 128 bits fits no register width
      22  a free symbol that is not an input row
       6  a joining of 25 pieces
       2  a joining of 17 pieces
```

The difference from round 13, computed from the two artifacts (not from
a log):

```
  refusal causes that are GONE:
     13027 -> 0   no template for the z3 operator 'if'

  refusal causes that are NEW:
    0 ->   1618   a choice at 8 bits has no conditional move
    0 ->   1452   no comparison template for the z3 predicate 'and'
    0 ->   1200   no comparison template for the z3 predicate 'fp.isNaN'
    0 ->    240   no comparison template for the z3 predicate 'or'

  refusal causes that CHANGED SIZE:
        41 ->     43   a joining of 3 pieces
      1140 ->   2678   a joining of 33 pieces
      2083 ->   2364   a shift whose count is not a literal
        12 ->    564   a value of 1 bits fits no register width
       345 ->    487   an 8-bit multiply has no two-operand instruction
```

**GLOSS.** The one gone cause is the `if` refusal, which is what this
task removed. The four new causes and the five that grew are the SAME
13,027 units arriving at finer refusals: the walk now descends INTO a
conditional, so it reaches sub-terms it never used to see, and refuses
on what it finds there. That is the intended behaviour of a refusal by
name — it names the next thing missing rather than the door it did not
open.

## 5.2 The 13,027 that carried a conditional, on their own

```
    6002  rendered, assembled, round-tripped and PROVED_ON_SHIP
    1618  a choice at 8 bits has no conditional move
    1538  a joining of 33 pieces
    1452  no comparison template for the z3 predicate 'and'
    1200  no comparison template for the z3 predicate 'fp.isNaN'
     552  a value of 1 bits fits no register width
     281  a shift whose count is not a literal
     240  no comparison template for the z3 predicate 'or'
     142  an 8-bit multiply has no two-operand instruction
       2  a joining of 3 pieces
   ------
   13027
```

## 5.3 The three next templates, each with the corpus shape it needs

These are named, not worked around; they are the largest remaining and
each has a measured shape in `probe80_conditional_shapes_printed.txt`.

1. **A choice at 8 bits (1,618).** `cmov` exists at 16, 32 and 64 bits
   only. Refused rather than rendered as a mask the corpus never
   writes. The corpus's own answer where it needs one is to compute at
   32 bits and narrow, which is a widening/narrowing question, not a
   conditional one.
2. **A comparison whose sides are one bit wide (564, up from 12).** The
   corpus's own shape for a single-bit condition is a masked
   conjunction: `test $0x40,<0>; cmovne <1>,<2>` — 272 sightings, and
   198 more with a second reader on the same flags. The rule refuses
   because it compares at register widths only.
3. **A predicate that is a conjunction or a disjunction (1,452 + 240).**
   The corpus's own shape is two flag reads combined by a bit operator:
   `test <0>,<0>; setne <1>; or <2>,<3>; setne <4>` — 188 sightings.
   The float family (`fp.isNaN`, 1,200) sits inside this one and is
   separately blocked by `fp.to_ieee_bv` having no template at all.

---

# 6. FINDING — 35 rendered texts did not prove, and none of them is the
# conditional template's

## 6.1 The claim, stated exactly

A template that renders but does not prove is a finding, never a
result. This round has 35 such units, of 11,911 rendered. **Zero of
them were rendered by the conditional template.** Measured: not one of
the 35 rendered bodies spells a comparison or a flag-reading arch
opcode.

## 6.2 The two causes

```
RENDERED BUT NOT PROVED, by cause (2 causes):
      31  z3 found a starting state under which the two differ
          sightings: swift/regen_1886, swift/regen_1887, swift/regen_1888, …
       4  the reference has no model for: arch opcode 'movdqu' has no entry in
          the opcode table -- no body in the corpus this table was built over
          spells it
          sightings: rust/regen_1559, rust/regen_1575, rust/op_807, rust/op_814
```

## 6.3 The counterexample, LITERAL

For `swift/regen_1886`, from `render_back80_store/`:

```
"unit": "swift/regen_1886", "lang": "swift",
"arrival_families": ["rdi", "rsi", "rdx"],
"result_family": "rax", "result_width": 64,
"layer5_normalized_text": "0",
"rendered_body": ["mov $0x0,%r11", "mov %r11,%rax", "ret"],
"verdict": {
  "outcome": "DISPROVED",
  "counterexample": "[seed_rsi = 0, seed_rdx = 63, seed_rdi = 1]",
  "reason": "z3 found a starting state under which the two sides differ",
  "route": "the wrapped text against the unit's own ship body"
}
```

**GLOSS.** The unit's layer-5 term is the constant `0`, so the rendered
body is three instructions with no conditional in it. The gate then
simulates the unit's OWN ship body and finds a starting state — first
argument 1, second 0, third 63 — where that body does not leave 0. So
the disagreement is between the term the ledger walk transcribed and
the term the gate's body simulation builds; the rendering is faithful
to the first one.

## 6.4 Where it comes from, and why it is not this task's

Round 13 recorded the same 31 units as non-proofs too, under a
different reason: "the reference has no model for: arch opcode `js` is
a census row … a transfer or trap, and this reference walks a body in
text order". So the reference now models the conditional transfer where
it used to refuse it, and the stored term (`0`) is from before that. Of
round 13's 36 non-proofs, **35 are the same units as this round's 35**;
one (`swift/regen_1893`) moved out.

This sits in the `reference` / `term` nodes' territory — a term
transcribed by the ledger walk disagreeing with the same reference's
body simulation once a body forks. It is FLAGGED here and not fixed
here, because it is not the render_back node's rule.

## 6.5 The confound that must be stated with it

`ledger.py` was being edited by another task WHILE this run was walking
(its file time moved from 13:xx to 23:07 during the run; the run began
at 23:03). The run itself is internally consistent — one process, the
modules loaded once at start — but the version of `ledger.py` this run
loaded is not the version now on disk. A re-run against the settled
`ledger.py` will move the 31, and possibly other units. The comparison
against round 13 in §5.1 carries the same caveat, softened by the fact
that 35 of the 36 non-proofs are unit-for-unit the same.

---

# 7. Population one, for the record

The 158 members of pool entry `E00029` (one layer-5 text `v0 + v1`,
seven languages):

| figure | round 13 | this round |
|---|---|---|
| rendered | 158 | 158 |
| assembled by `as` | 158 | 158 |
| round-tripped through `objdump -d` | 158 | 158 |
| PROVED_ON_SHIP | 158 | 158 |
| character-identical to layer 3 | 0 | 0 |
| distinct rendered texts | 5 | 5 |
| distinct layer-3 wrapped texts | 12 | 12 |

Unchanged, and expected to be: the entry's one layer-5 text carries no
conditional, so this task's change cannot touch it. It is reported
because the brief asks for the figures per population, and an unchanged
population is a measurement, not an omission.

---

# 8. The collapse

Over the 26,040 units with a proved term:

- **420 distinct rendered texts** against **1,905 distinct layer-3
  wrapped texts**. Round 13: 105 against the same 1,905.
- Among the 6,002 the conditional template rendered on their own: 315
  distinct rendered texts.
- 0 of 11,911 rendered texts are character-identical to their layer-3
  text.

**GLOSS.** The rendered count grew from 105 to 420 because the rendered
population doubled and the new members are conditionals, which carry
more shape than the arithmetic that was already rendering. The right
reading is the ratio against layer 3 over the same units: 1,905
compiler texts collapse to 420 rendered ones. The count is a
measurement of what the simplifier plus one fixed rule produce; it is
never a target, and the CORE says why two units with one layer-5 term
can still render differently — they render against their OWN arrival
families.

---

# 9. Guards

## 9.1 The spelling-key check, unmodified, one process

```
$ /tmp/reconnect_venv/bin/python3 guard80.py
TASK 80: 336 paths  PASS 336  FAIL 0  exempt 0  exit 0
$ grep -c exempt guard80_transcript.txt
0
```

The transcript's own head, LITERAL:

```
guard80.py -- every JSON artifact task 80 writes, unmodified guard, ONE
process.  Nothing was added to any field set, and no artifact was
declared out of the walk.

command: /tmp/reconnect_venv/bin/python3 …/check_no_spelling_keys.py
         …/probe80_conditional_shapes.json ... (336 paths)

operator inventory: 91 tokens read from probe_manifest_*.json
PASS probe80_conditional_shapes.json -- no operator token in any key, grouping, pairing or row structure
PASS render_back80_E00029.json -- no operator token in any key, grouping, pairing or row structure
PASS render_back80_tally.json -- no operator token in any key, grouping, pairing or row structure
PASS render_back80_state.json -- no operator token in any key, grouping, pairing or row structure
```

`check_no_spelling_keys.py` is unmodified: `git diff HEAD` over it is
empty. No role keys, no field whitelists, no exemptions.

## 9.2 The spelling ban itself

No operator token appears in any key, grouping, pairing, row structure,
candidate selection or comparison scope of anything this task wrote.
The `operator` field of a unit record is copied onto the member as a
display label and is never read, grouped or paired on. The probe's
groupings are keyed by arch mnemonics and by position in a window of
instructions — machine form throughout.

## 9.3 Memory bound

Stated before the run: 6 GB resident, checked after every shard, with
the named abort `ABORT_MEMORY`. One canon39 shard is opened, walked and
dropped before the next. Sample first, as the round requires:

```
canon39_wrapped_c.json:   602 with proved terms, 207 rendered, 8 skipped
canon39_wrapped_cpp.json: 764 with proved terms, 246 rendered, 6 skipped
```

Peak resident across the whole 332-shard run, from the run's own log:
**84,384 kB** (82 MB) — 1.4% of the stated cap. The measuring pass
peaked at **74,432 kB** against its own 2 GB cap.

---

# 10. The environment, stated because it changed

The venv the brief names, `/tmp/reconnect_venv`, **did not exist** at
the start of this task — `/tmp` had been cleared, and no pyvex was
installed anywhere on the machine. It was recreated:

```
$ python3 -m venv /tmp/reconnect_venv
$ /tmp/reconnect_venv/bin/pip install z3-solver capstone pyvex
$ /tmp/reconnect_venv/bin/python3 -c "import z3; print(z3.get_version_string())"
5.1.0
```

Round 13's z3 version is not recorded, so a version difference cannot
be ruled out as a contributor to any figure. The strongest available
cross-check that the two environments agree: 35 of round 13's 36
non-proofs are unit-for-unit the same units in this round, and
population one reproduces round 13's figures exactly (158/158/158/158,
5 against 12).

---

# 11. File inventory

## 11.1 Written this round

| file | what it is |
|---|---|
| `Research/op_pipeline/probe80_conditional_shapes.py` | the measuring pass: the conditional shape read off 31,078 ship bodies, before any template |
| `Research/op_pipeline/probe80_conditional_shapes.json` | its tallies |
| `Research/op_pipeline/probe80_conditional_shapes_printed.txt` | its printed report |
| `Research/op_pipeline/render_back80_run.py` | the driver; reuses `render_back_run`'s `Assembler`, `one_unit`, `proved_terms_of`, `new_tools`, `shards` and `render_back_E00029.members_of_the_entry` |
| `Research/op_pipeline/render_back80_store/` | 332 shards, one per canon39 shard |
| `Research/op_pipeline/render_back80_state.json` | the resume state |
| `Research/op_pipeline/render_back80_run_log.txt` | the run's own progress lines with per-shard peak resident |
| `Research/op_pipeline/render_back80_E00029.json` | population one |
| `Research/op_pipeline/render_back80_tally.py` | the tally; reuses `render_back_tally`'s `walk` and `report` |
| `Research/op_pipeline/render_back80_tally.json` | the tally |
| `Research/op_pipeline/render_back80_tally_printed.txt` | the printed tally plus the difference from round 13 |
| `Research/op_pipeline/render_back80_one_unit.py` | the literal end-to-end walk of one unit of each shape |
| `Research/op_pipeline/render_back80_one_unit_printed.txt` | its output, quoted in §4 |
| `Research/op_pipeline/guard80.py` | the guard runner; reuses `guard66.run_guard` |
| `Research/op_pipeline/guard80.json`, `guard80_transcript.txt` | its summary and transcript |
| `DevComms/log_187_task80_render_back_conditional.md` | this report |

## 11.2 Edited this round

| file | what changed |
|---|---|
| `Research/op_pipeline/term.py` | section 5 only: `PREDICATE_CONDITION`, `CONDITION_WIDTHS`, `MOVE_CONDITION_WIDTHS`, `RenderBack.suffix_per_condition`, `.complement_per_condition`, `.reader_mnemonics`, `.condition_of`, `.emit_condition`, `.two_literal_arms`, `.emit_choice`, `.emit_set_choice`, `.emit_move_choice`, one dispatch line in `.emit`, one line in `.check_templates_against_the_one_table`. Nothing outside `RenderBack` and its module-level tables was touched, and no import line was added — `condition_table` is reached as `R.CT`, through the module that already imports it. Task 79 is correcting `normalize` in the same file; `term.py` was re-read immediately before every edit. |
| `Planning/…/node_0_3_5_6_5_render_back/CORE_0_3_5_6_5_render_back.md` | `## design` gained `condition_table`, `emit_condition`, `emit_choice`; four settled rules with decision sources; five realization rows |
| `Planning/…/node_0_3_5_6_5_render_back/PROGRESS.md` | eight entries, each with its evidence link |

## 11.3 Read and not modified

`AgentMemory.md`, `LLM_communication_protocol.md`,
`PlanPlan/framework/PROTOCOL.md`, `log_183` (task 80's brief),
`log_170`, `log_168`, the render_back and term COREs, `reference.py`,
`condition_table.py`, `canonical_form.py`, `gate.py`, `ledger.py`,
`render_back_run.py`, `render_back_tally.py`, `render_back_E00029.py`,
`guard66.py`, `check_no_spelling_keys.py`. Round 13's
`render_back_store/`, `render_back_tally.json` and
`render_back_E00029.json` were read and left exactly as they were —
this round writes to its own store, so the earlier record stands beside
it.

---

# 12. Resume state

- **Everything this task was asked for is on disk and measured.** No
  step is half-finished and nothing is queued.
- **The one thing a next lap should do first:** re-run
  `render_back80_run.py` (delete `render_back80_state.json` to force a
  full walk, or point it at a new store) once `ledger.py` has settled
  from task 78, and re-read §6. That re-run costs about 45 minutes of
  wall clock in one process and needs no supervision; it is resumable
  from its state file if interrupted.
- **The three named gaps for a later round**, in size order, each with
  its corpus shape already measured in
  `probe80_conditional_shapes_printed.txt`: the 8-bit choice (1,618),
  the conjunction/disjunction predicate (1,692 across two causes), the
  one-bit comparison (564). §5.3.
- **Nothing here is a question for the owner.** No ontology or naming
  decision was taken; the one shape the tree lacked went into the CORE
  with its provenance before any code was written, and the finding in
  §6 is flagged to the `reference` / `term` nodes rather than decided.
- **The venv is at `/tmp/reconnect_venv` again** and will vanish on the
  next clearing of `/tmp`. §10 has the three commands that rebuild it.
