# log_227 — task L1: Lean 4 as a second discharger — install verified, eight of ten edges certified, the renderer's preservation theorem proved for the integer subset, and a scope estimate

Node: `hq.research.compiler_graph.gate.lean`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_6_lean/CORE_0_3_1_5_6_lean.md`).
Its super-node is the gate
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/CORE_0_3_1_5_gate.md`).
Artifacts: `PseudoCoupHQ/Research/op_pipeline/lean/`.
Instance: `Airlock/instances/L1.conf`. Lanes: 24, all kept at
`PseudoCoupHQ/Research/op_pipeline/lean/lanes_L1/`.

---

## 0. What was done and found, in plain words, before any figures

Lean 4 was already in the Airlock image when this task started, put there the
same day the node was opened. The first thing this task did was ask the image
whether that was true, and it was: version 4.24.0, and a fresh `lake` project
built a one-line theorem with the network switched off, which is what the
brief cared about — nothing was allowed to fetch, and nothing did.

The next question was whether the pipeline's own proved pairs can be restated
as Lean theorems. A pair here is two pool entries that task t100's solver
proved compute the same thing; each entry's computation is printed as a single
line of text, and that line is what had to become Lean. A program was written
to do the translation, and it carries one guard that turned out to matter: it
rebuilds the term it parsed using z3 itself and demands that z3's printer hand
back the original line, character for character. If a parser reads a printed
term differently from the printer that wrote it, the theorem handed to Lean is
a different theorem, and nobody would notice. Every pair that went to Lean
passed that check.

Ten pairs were chosen and eight of them were proved by Lean's kernel, each in
about a fifth of a second. The other two are floating point, and the
translator refused them by name rather than attempting them: Lean's bit-vector
tactic bit-blasts to a SAT solver and has no floating-point theory, so there
is no honest way to state those two.

The brief also asked for three pairs that t100 had left undecided, expecting
them to be wide divisions. They are not. All 1,099 of t100's undecided pairs
sit in three machine type keys, every one of them an xmm register family,
which is to say floating point; and their pair records carry no term at all,
because the sub-process t100 ran was stopped at its 120-second ceiling before
one was written. Going to the pool entries themselves for the terms did not
help either: five of the six entries print no text, and the sixth prints
floating point. So the question the brief was really asking — does Lean's
bit-blasting fare differently from z3's on the hard shapes — was answered a
second way, by measuring the cost of a divider directly. That measurement is
the most interesting number in this log, and it moved twice as ceilings were
raised.

Last, the renderer. The claim that a rendered emulation computes what its term
computes had been argued on paper and demonstrated per instance. It is now a
theorem in Lean over the whole integer subset of the term language — eighteen
constructors, proved by structural induction, with no holes. Writing it forced
one correction to the C model that is a fact about C rather than about Lean,
and that correction is in section 5.

---

## 1. What the objects are, one sentence each, in relation

- **term** — an arch-unit's computation as a z3 expression, read off its
  ledger from OUT-0 downward. This is layer 4.
- **printed layer-5 text** — that expression simplified once and printed on
  one line with its free symbols renamed positionally `v0`, `v1`, …. This is
  what is stored, and what this task translates.
- **pair** — two pool entries of one machine type key (arrival register
  families | answer width), which is the candidate set t100 fixed from the
  machine form before any solver ran.
- **`bv_decide`** — Lean's tactic for bit-vector goals: it bit-blasts the goal
  to a SAT problem, runs CaDiCaL in the same process, and then CHECKS the
  solver's certificate inside Lean's kernel. That last step is why a Lean
  answer sits above a solver's answer in the evidence doctrine.
- **`term_to_lean.py`** — the program that turns one printed layer-5 text into
  one Lean `BitVec` expression:
  `PseudoCoupHQ/Research/op_pipeline/lean/term_to_lean.py`.
- **`Render.lean`** — the file holding the term language, a C integer
  expression language, the rendering between them, and the preservation
  theorem:
  `PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof/Render.lean`.

---

## 2. The install, verified inside a lane

### 2.1 The version line

**LITERAL**, from `L1_l1_install_check.sh`
(host log `<runs>/L1/agent/logs/20260907T000732Z__L1_l1_install_check.sh.log`):

```
--- which lean; which lake
/opt/elan/bin/lean
/opt/elan/bin/lake
--- lean --version
Lean (version 4.24.0, x86_64-unknown-linux-gnu, commit 797c613eb9b6d4ec95db23e3e00af9ac6657f24b, Release)
--- lake --version
Lake version 5.0.0-src+797c613 (Lean version 4.24.0)
--- elan toolchain list
leanprover/lean4:v4.24.0
```

### 2.2 A project, created and built with no route out

The instance is configured `proxy = no`, so there is no network in any lane of
this task. **LITERAL**, same lane log, the files `lake new archproof` wrote and
the toolchain file it pinned:

```
--- files lake created
archproof/.github/workflows/lean_action_ci.yml
archproof/.gitignore
archproof/Archproof.lean
archproof/Archproof/Basic.lean
archproof/Main.lean
archproof/README.md
archproof/lakefile.toml
archproof/lean-toolchain
--- archproof/lean-toolchain, LITERAL
leanprover/lean4:v4.24.0
```

The first build FAILED, and the failure is the useful part. **LITERAL**:

```
error: Archproof/Smoke.lean:6:2: to use `bv_decide`, please include `import Std.Tactic.BVDecide`
```

**GLOSS.** `bv_decide` ships with the toolchain but is not in scope by
default; one import brings it in, and no package resolution and no fetch are
involved, which is what mattered here.

With that import added, **LITERAL**, from `L1_l2_survey_and_smoke.sh`
(host log `<runs>/L1/agent/logs/20260907T000940Z__L1_l2_survey_and_smoke.sh.log`):

```
--- Archproof/Smoke.lean, LITERAL
-- The smallest possible check that this toolchain proves anything:
-- one arithmetic identity over 32-bit words, discharged by bv_decide,
-- which bit-blasts the goal to a SAT solver and checks the solver's
-- certificate inside Lean's kernel.
import Std.Tactic.BVDecide

theorem smoke_add_comm (v0 v1 : BitVec 32) : v0 + v1 = v1 + v0 := by
  bv_decide
--- lake build
✔ [4/10] Built Archproof.Smoke (179ms)
✔ [5/10] Built Archproof.Smoke:c.o (32ms)
✔ [6/10] Built Archproof (157ms)
✔ [7/10] Built Archproof:c.o (34ms)
✔ [8/10] Built Main (153ms)
✔ [9/10] Built Main:c.o (40ms)
✔ [10/10] Built archproof:exe (83ms)
Build completed successfully (10 jobs).
```

---

## 3. The ten certified edges

### 3.1 Where the ten came from, and the one thing that constrained the choice

`pool100_edges.json` (task t100's product, log_224) carries two lists that
both matter. `edges` holds the 12 pairs t100 APPLIED to its closure. `pairs`
holds all 21,502 pairs it ANSWERED, with their states. Reading the union and
counting, **LITERAL**, from `L1_l3_survey_pairs.sh`
(host log `<runs>/L1/agent/logs/20260907T001053Z__L1_l3_survey_pairs.sh.log`):

```
states: {"DISPROVED": 19640, "PROVED": 226, "UNBUILDABLE": 537, "UNDECIDED": 1099}
PROVED with both layer-5 texts present: 12 of 226
PROVED type_key spread: 4 distinct; [["rdi,rsi,rcx|8", 8], ["rdi,rsi|8", 2], ["xmm0,xmm1|8", 1], ["rcx,xmm0|32", 1]]
```

**GLOSS.** Only 12 of the 226 PROVED pairs carry a printed text on BOTH sides;
the other 214 have a hole on one side, and a term with a hole has no
normalized text. So the population to choose ten from is twelve, spanning four
machine type keys. The ten SHORTEST of those twelve span only two keys, so a
per-key cap of six is what makes the brief's "across at least three type keys"
true — six plus two plus one plus one is exactly ten, over four keys. The cap
is a size rule over the machine form; no operator token takes part in it.

### 3.2 The operator table this task translates by

**LITERAL**, printed by
`python3 PseudoCoupHQ/Research/op_pipeline/lean/term_to_lean.py table`
inside `L1_l7_ten_edges.sh`
(host log `<runs>/L1/agent/logs/20260907T001937Z__L1_l7_ten_edges.sh.log`):

| printed layer-5 form | arity | result | Lean 4.24 form |
|---|---|---|---|
| `Extract(hi, lo, x)` | 3 | bv | `x.extractLsb hi lo` |
| `Concat(a, b, ...)` | n | bv | `a ++ b` |
| `If(c, a, b)` | 3 | bv | `if c = true then a else b` |
| `ZeroExt(n, x)` | 2 | bv | `x.zeroExtend (n + width x)` |
| `SignExt(n, x)` | 2 | bv | `x.signExtend (n + width x)` |
| `a + b` | 2 | bv | `a + b` |
| `a - b` | 2 | bv | `a - b` |
| `a*b` | 2 | bv | `a * b` |
| `a & b` | 2 | bv | `a &&& b` |
| `a \| b` | 2 | bv | `a ||| b` |
| `a ^ b` | 2 | bv | `a ^^^ b` |
| `~a` | 1 | bv | `~~~a` |
| `-a` | 1 | bv | `-a` |
| `a << b` | 2 | bv | `a <<< b` |
| `LShR(a, b)` | 2 | bv | `a >>> b` |
| `a >> b` | 2 | bv | `a.sshiftRight' b` |
| `bvudiv_i(a, b)` | 2 | bv | `REFUSED, cause UNGUARDED_DIVISION` |
| `bvsdiv_i(a, b)` | 2 | bv | `REFUSED, cause UNGUARDED_DIVISION` |
| `bvurem_i(a, b)` | 2 | bv | `REFUSED, cause UNGUARDED_DIVISION` |
| `bvsrem_i(a, b)` | 2 | bv | `REFUSED, cause UNGUARDED_DIVISION` |
| `bvsmod_i(a, b)` | 2 | bv | `REFUSED, cause UNGUARDED_DIVISION` |
| `UDiv(a, b)` | 2 | bv | `a / b` |
| `URem(a, b)` | 2 | bv | `a % b` |
| `SRem(a, b)` | 2 | bv | `a.srem b` |
| `a == b` | 2 | bool | `a == b` |
| `a != b` | 2 | bool | `!(a == b)` |
| `a <= b` | 2 | bool | `a.sle b` |
| `a < b` | 2 | bool | `a.slt b` |
| `a >= b` | 2 | bool | `b.sle a` |
| `a > b` | 2 | bool | `b.slt a` |
| `ULE(a, b)` | 2 | bool | `a.ule b` |
| `ULT(a, b)` | 2 | bool | `a.ult b` |
| `UGE(a, b)` | 2 | bool | `b.ule a` |
| `UGT(a, b)` | 2 | bool | `b.ult a` |
| `And(a, b, ...)` | n | bool | `a && b` |
| `Or(a, b, ...)` | n | bool | `a \|\| b` |
| `Not(a)` | 1 | bool | `!a` |
| `<numeral>` | 0 | bv | `n#w` |
| `v0, v1, ...` | 0 | bv | `the theorem's bound variable` |

**GLOSS on the five refusals in that table.** z3's simplifier does not leave a
division alone. It splits it into a test for a zero divisor and an UNGUARDED
division symbol, printed `bvudiv_i` and friends, whose value at a zero divisor
is not specified at all. Lean's `/` answers zero there — measured, section 4.3
— so mapping one to the other would state a theorem about a function neither
system holds. The refusal is by cause, not a gap.

### 3.3 The outcomes

**LITERAL**, from `L1_l9_ten_and_undecided2.sh`
(host log `<runs>/L1/agent/logs/20260907T002109Z__L1_l9_ten_and_undecided2.sh.log`):

| # | type_key | entries | outcome | wall s | child peak MB | cause |
|---|---|---|---|---|---|---|
| 0 | `rdi,rsi,rcx\|8` | E00338 == E00339 | PROVED_BY_LEAN | 0.227 | 452.5 | - |
| 1 | `rdi,rsi\|8` | E00156 == E01664 | PROVED_BY_LEAN | 0.148 | 452.5 | - |
| 2 | `rdi,rsi\|8` | E00170 == E01654 | PROVED_BY_LEAN | 0.166 | 452.5 | - |
| 3 | `rdi,rsi,rcx\|8` | E00341 == E00342 | PROVED_BY_LEAN | 0.23 | 453.5 | - |
| 4 | `rdi,rsi,rcx\|8` | E01658 == E01661 | PROVED_BY_LEAN | 0.211 | 453.5 | - |
| 5 | `rdi,rsi,rcx\|8` | E01653 == E01660 | PROVED_BY_LEAN | 0.215 | 453.5 | - |
| 6 | `rdi,rsi,rcx\|8` | E01659 == E01663 | PROVED_BY_LEAN | 0.215 | 453.5 | - |
| 7 | `rdi,rsi,rcx\|8` | E01672 == E01675 | PROVED_BY_LEAN | 0.214 | 453.6 | - |
| 8 | `rcx,xmm0\|32` | E01445 == E01507 | REFUSED_BEFORE_LEAN | - | - | FLOATING_POINT |
| 9 | `xmm0,xmm1\|8` | E00920 == E01004 | REFUSED_BEFORE_LEAN | - | - | FLOATING_POINT |

**GLOSS on "child peak MB".** That column is the peak resident memory of the
`lean` process itself, read from `resource.getrusage(RUSAGE_CHILDREN)` after
that one process ended. About 450 MB is the cost of elaborating a module that
imports `Std.Tactic.BVDecide` at all; the goals themselves add nothing
measurable at these sizes.

### 3.4 One theorem in full, so the translation can be inspected

**LITERAL**, the printed layer-5 texts of the two entries and the Lean theorem
built from them, same lane log, row 4:

```
### 4  E01658 == E01661  (rdi,rsi,rcx|8)
    layer-5 a: If(Extract(7, 0, v0) == Extract(7, 0, v1), 0, 1) | If(0 <= Extract(7, 0, v0), 0, 1)
    layer-5 b: If(Extract(7, 0, v0) == Extract(7, 0, v1), 0, 1) | If(0 <= Extract(7, 0, v1), 0, 1)
    theorem:   theorem edge_04_E01658_E01661 (v0 : BitVec 64) (v1 : BitVec 64) : ((if ((v0.extractLsb 7 0) == (v1.extractLsb 7 0)) = true then (0#8) else (1#8)) ||| (if ((0#8).sle (v0.extractLsb 7 0)) = true then (0#8) else (1#8))) = ((if ((v0.extractLsb 7 0) == (v1.extractLsb 7 0)) = true then (0#8) else (1#8)) ||| (if ((0#8).sle (v1.extractLsb 7 0)) = true then (0#8) else (1#8))) := by bv_decide
```

**GLOSS.** The two sides differ in one place — `v0` on the left, `v1` on the
right, inside the second comparison — and they are nevertheless equal for
every pair of 64-bit inputs, which is the fact t100's solver found and Lean's
kernel has now certified. Note what the translation had to recover that the
printed text never says: the `0` inside `0 <= Extract(7, 0, v0)` is eight bits
wide, and the `0` and `1` that the `If` chooses between are eight bits wide,
because the answer width is eight. Widths are inferred by unification, seeded
with the arrival rows' widths and the term's result width.

### 3.5 The check that makes the parse evidence rather than assumption

`term_to_lean.py` rebuilds every parsed term in z3 and demands z3's own
printer reproduce the input line. **LITERAL**, from `L1_l5_api_probe.sh`
(host log `<runs>/L1/agent/logs/20260907T001427Z__L1_l5_api_probe.sh.log`),
z3 printing terms built through its own API:

```
z3 version: 5.1.0
  If(v0 == v1, 0, 1) | If(0 <= v0, 0, 1)
  If(Concat(0, Extract(31, 0, v0)) == v1, 1, 0)
  ~(If(v0 == v1, 254, 255) | If(0 <= v0, 254, 255))
  Extract(31, 0, v0)*Extract(31, 0, v1)
  UDiv(v0, v1)
  v0/v1
  URem(v0, v1)
  SRem(v0, v1)
  LShR(v0, v1)
  v0 >> v1
  v0 << v1
  ULE(v0, v1)
```

**GLOSS.** These are the exact shapes the corpus stores, so a parser that
agrees with z3 can be confirmed by round trip rather than trusted. Every one
of the eight proved edges round-tripped; a mismatch is a refusal with the
cause `ROUNDTRIP_MISMATCH`, never a warning.

---

## 4. The three UNDECIDED pairs, and what replaced the question

### 4.1 What t100's UNDECIDED pairs actually are

The brief asked for three pairs t100 marked UNDECIDED "with wide division".
There are none. **LITERAL**, from `L1_l4_survey_undecided.sh`
(host log `<runs>/L1/agent/logs/20260907T001145Z__L1_l4_survey_undecided.sh.log`):

```
UNDECIDED pairs: 1099
term_a/term_b field frequencies over the 1,099: {}
--- one whole UNDECIDED record, LITERAL
{
 "a": "E00288",
 "b": "E00684",
 "cause": "runner limit: TIMED_OUT (sub-process ceiling 1536 MB, wall clock 120 s)",
 "rep_a": "cpp/op_771",
 "rep_b": "c/regen_28723",
 "runner_word": "TIMED_OUT",
 "state": "UNDECIDED",
 "sub_ceiling_mb": 1536,
 "sub_peak_kb": 240828,
 "sub_seconds": 120.0,
 "type_key": "rcx,xmm0,xmm1|32",
 "wall_seconds": 121.035
}
sub_seconds: min 120.0 median 120.0 max 120.0
UNDECIDED type_key spread: [["rcx,xmm0|32", 689], ["rcx,xmm0,xmm1|32", 366], ["rcx,xmm0,xmm1|8", 44]]
```

**GLOSS, three readings of that record.** First, an UNDECIDED record carries
NO term: the `term_a`/`term_b` field tally over all 1,099 is the empty object,
because t100's sub-process was stopped before it wrote one. Second, every one
of the 1,099 sat at exactly 120.0 seconds — the runner's own ceiling, not the
solver's 3,000 ms one, which log_224 §6 already recorded. Third, all three
machine type keys that hold UNDECIDED pairs are xmm register families, which
is to say floating point; there is no division among them.

And separately, over the pairs that DO carry printed texts, **LITERAL** from
`L1_l6_select_and_divsamples.sh`
(host log `<runs>/L1/agent/logs/20260907T001528Z__L1_l6_select_and_divsamples.sh.log`):

```
UNDECIDED pairs in t100: 1099; of those, carrying a division node at a free-symbol width of 64 or more: 0
pair sides whose printed text carries a division node: 505
by t100 state: {"DISPROVED": 505}
```

**GLOSS.** Every division-carrying text in the answered population belongs to
a DISPROVED pair, and the divisions there are not wide: the shortest is an
8-bit division widened to 32, **LITERAL** from the same log:

```
        Concat(0, Extract(7, 0, bvudiv_i(Concat(0, Extract(7, 0, v0)), Concat(0, Extract(7, 0, v1)))))
```

### 4.2 The three pairs, taken anyway, and what stopped them

One pair per UNDECIDED machine type key, so all three machine forms that hold
UNDECIDED pairs are represented. Their terms were sought in
`the_pool5.json`'s entries, since the pair record has none. **LITERAL**, from
`L1_l10_divide_ladder.sh`
(host log `<runs>/L1/agent/logs/20260907T002141Z__L1_l10_divide_ladder.sh.log`):

```
  entry_a E00288: representative cpp/op_771, distinct layer-5 texts 2, member count 2
     translation probe: REFUSED FLOATING_POINT -- node 'fpToFP'
     translation probe: REFUSED FLOATING_POINT -- node 'fpEQ'
  entry_b E00684: representative c/regen_28723, distinct layer-5 texts 0, member count 2
     layer5_normalized_texts, LITERAL: []
  entry_a E00801: representative c/regen_34995, distinct layer-5 texts 0, member count 1
     layer5_normalized_texts, LITERAL: []
  entry_b E00806: representative c/regen_35007, distinct layer-5 texts 0, member count 1
     layer5_normalized_texts, LITERAL: []
  entry_a E00679: representative c/regen_28668, distinct layer-5 texts 0, member count 20
     layer5_normalized_texts, LITERAL: []
  entry_b E00707: representative c/regen_29567, distinct layer-5 texts 0, member count 2
     layer5_normalized_texts, LITERAL: []
```

| # | type_key | entries | outcome | cause |
|---|---|---|---|---|
| 0 | `rcx,xmm0,xmm1\|32` | E00288 == E00684 | REFUSED_BEFORE_LEAN | NO_LAYER5_TEXT_ON_THE_ENTRY |
| 1 | `rcx,xmm0,xmm1\|8` | E00801 == E00806 | REFUSED_BEFORE_LEAN | NO_LAYER5_TEXT_ON_THE_ENTRY |
| 2 | `rcx,xmm0\|32` | E00679 == E00707 | REFUSED_BEFORE_LEAN | NO_LAYER5_TEXT_ON_THE_ENTRY |

**GLOSS.** Five of the six entries print nothing at all. The sixth, E00288,
prints two texts, and both are refused as floating point on their first node.
So the answer to "does `bv_decide` decide t100's undecided pairs" is that it
cannot state them: not because bit-blasting is too slow on them, but because
they are floating point and there is no bit-vector statement to bit-blast.

### 4.3 Two places where Lean's arithmetic and SMT-LIB's differ, measured

**LITERAL**, `#eval` output from `L1_l5_api_probe.sh`, same host log as §3.5:

```
info: Archproof/Api.lean:42:0: 0x00#8      -- (7#8) / (0#8)
info: Archproof/Api.lean:43:0: 0x07#8      -- (7#8) % (0#8)
info: Archproof/Api.lean:44:0: 0x00#8      -- BitVec.sdiv (7#8) (0#8)
info: Archproof/Api.lean:45:0: 0x07#8      -- BitVec.srem (7#8) (0#8)
info: Archproof/Api.lean:46:0: 0x00#8      -- (1#8) <<< (200#8)
info: Archproof/Api.lean:47:0: 0xff#8      -- BitVec.sshiftRight' (128#8) (200#8)
info: Archproof/Api.lean:48:0: 0x00#8      -- (128#8) >>> (200#8)
```

**GLOSS, by cause, with a status on each.**

- **Division at a zero divisor DIFFERS — open, and named on every record.**
  Lean's `/` and `.sdiv` answer zero; SMT-LIB's `bvudiv` answers all ones and
  its `bvsdiv` answers all ones or one depending on the sign of the dividend.
  Any future division work must state the guard rather than assume the two
  systems agree.
- **Remainder at a zero divisor AGREES — closed.** Both answer the dividend.
- **All three shifts past the width AGREE — closed.** Left and logical-right
  clear the holder; arithmetic-right fills with the sign bit.

---

## 5. The renderer's preservation theorem, integer subset

### 5.1 What is stated, and why it is not a restatement of itself

The file is
`PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof/Render.lean`,
374 lines. It holds five things: an inductive `Term` indexed by width, an
`eval` from a term and an environment to a `BitVec w`, an inductive `CExpr`
for the C integer expressions the renderer emits, an `evalC`, a `render`
between them, and the theorem.

The one design decision that makes the theorem carry content is the type of
`evalC`. **LITERAL**, from the file's own header:

> A bit-vector expression is total: every operator has a value at every
> input.  A C expression is not.  C leaves a shift by a count of w or more
> UNDEFINED, and an undefined C expression has no value to compare against.
> So `evalC` answers `Option (BitVec w)`: `none` is "this C expression has
> undefined behaviour on this environment".  The theorem then says two
> things at once, and the second is the one that would otherwise be assumed:
>   * the rendered expression is DEFINED on every environment (never `none`,
>     so the renderer emitted the guards C needs), and
>   * its value is the term's value.
> Modelling the undefined region as some convenient number instead -- zero,
> say -- would make the shift cases hold for free and prove nothing.

The theorem itself, **LITERAL**:

```
theorem render_preserves : {w : Nat} → (t : Term w) → (e : Env) →
    evalC (render t) e = some (eval t e) := by
```

### 5.2 The eighteen constructors, and that all of them close

`Term` carries `var lit add sub mul and or xor not shl lshr ashr extract
concat zext sext eq ite` — the list the brief named. Two choices inside it are
worth stating because the brief flagged one of them as an open question:

- **`eq` answers `Term 1` and `ite` takes a `Term 1` condition.** A comparison
  at the machine is read off a flag as one bit, so the condition stays a
  one-bit word and the Bool-versus-`BitVec 1` question does not arise inside
  the term language at all. It arises only at the boundary, where `evalC`'s
  `csel` compares its condition against `1#1`.
- **`Env` is `(w : Nat) → Nat → BitVec w`** — indexed by width and slot, so a
  variable is well-typed by construction and there is no way to read a 32-bit
  slot as 64 bits.

**LITERAL**, the final build, from `L1_l22_render10.sh`
(host log `<runs>/L1/agent/logs/20260907T011111Z__L1_l22_render10.sh.log`):

```
--- lean exit 0
--- declarations using sorry: 0
--- error lines: 0
```

A build with no errors is not by itself the claim that there are no holes, so
the axioms were printed. **LITERAL**, from `L1_l24_final_measurements.sh`
(host log `<runs>/L1/agent/logs/20260907T011305Z__L1_l24_final_measurements.sh.log`):

```
'Archproof.render_preserves' depends on axioms: [propext, Classical.choice, Quot.sound]
'Archproof.append_as_shift_or' depends on axioms: [propext, Quot.sound]
'Archproof.sshiftRight_out_of_range' depends on axioms: [propext, Classical.choice, Quot.sound]
'Archproof.shiftInRange_says' depends on axioms: [propext, Quot.sound]
```

**GLOSS.** Those are Lean's three standard axioms and nothing else. `sorryAx`
— the axiom a hole would introduce — appears nowhere, which is the check that
distinguishes a proof from a build.

### 5.3 The correction the proof forced, which is a fact about C

The first C model gave every shift a count of the same holder width, matching
the term language. Two cases then could not be rendered at all, and the reason
is not a Lean limitation:

- **What was wrong.** `Extract(31, 0, v0)` renders as a shift right by 31 then
  a truncation, and `Concat(a, b)` renders as a widen, a shift left by the
  width of `b`, and an or. With the count held in the shifted type, a count of
  31 in an 8-bit holder is not representable, and a count of `w` in a `w`-bit
  holder wraps — at `w = 1`, the count 1 becomes 0.
- **What is true of C.** C's shift operand undergoes the usual arithmetic
  promotions and is an `int`. It is NOT a value of the shifted type. A count
  that does not fit the left operand's type is still a legal C expression;
  only a count at or above the left operand's width is undefined.
- **What changed.** `CExpr` now carries both forms: `shlC`/`shrC`/`sarC` take
  a computed holder as the count and are guarded at run time by
  `shiftInRange`, while `shlN`/`shrN`/`sarN` take a plain natural and are
  guarded when the renderer writes them. The slice and the append use the
  second form, which is what a real emitter writes.

### 5.4 The shift guard, and the one place its width matters

**LITERAL**, from `Render.lean`:

```
/-- The guard C needs on a shift: `(uintW1_t)k < (uintW1_t)w`, computed one
bit wider than the holder so the width itself is always representable.  At
`w = 1` the count `1` does not fit in a one-bit holder, which is why the
comparison is not made at width `w`. -/
def shiftInRange (w : Nat) (k : CExpr w) : CExpr 1 :=
  .cult (.castU (w + 1) k) (.lit (BitVec.ofNat (w + 1) w))
```

**GLOSS.** The guard is computed one bit wider than the holder for exactly one
reason: at a one-bit holder, the number 1 is not representable, so a guard
written at the holder's own width would compare against 0 and reject every
count. The supporting fact, `w % 2 ^ (w + 1) = w`, is its own named theorem in
the file.

### 5.5 Five bit-vector facts, stated separately so an open one could be named

The hard cases rest on named theorems rather than on tactics buried in the
induction, so that any case that had not closed could be reported by the fact
it was waiting for. All five closed:

| theorem | what it says | how it closed |
|---|---|---|
| `w_mod_pow` | a width fits in a holder one bit wider | `Nat.lt_two_pow_self` and `Nat.pow_le_pow_right` |
| `shiftInRange_says` | the guard is true exactly when the count is below the width | simp over `BitVec.ult` and `w_mod_pow` |
| `shiftLeft_out_of_range` | a left shift past the width clears the holder | shipped as `BitVec.shiftLeft_eq_zero` |
| `ushiftRight_out_of_range` | a logical right shift past the width clears the holder | shipped as `BitVec.ushiftRight_eq_zero` |
| `sshiftRight_out_of_range` | an arithmetic right shift past the width equals one by `w - 1` | `BitVec.getLsbD_sshiftRight`, split at bit 0, then `BitVec.msb_eq_getLsbD_last` |
| `append_as_shift_or` | an append is a widen, a shift and an or | `BitVec.getLsbD_append` and friends, split at the low half |

**GLOSS.** The three shipped names were read out of the toolchain's own source
inside a lane (`L1_l14_core_lemma_names.sh`, host log
`<runs>/L1/agent/logs/20260907T005407Z__L1_l14_core_lemma_names.sh.log`)
rather than recalled, which removed two rounds of guessing. No Mathlib was
used, and none is installed.

---

## 6. The cost of bit-blasting a divider — the measurement that moved twice

### 6.1 Why this was measured at all, and what it is NOT

t100 left 1,099 pairs UNDECIDED and none of them carries a division (§4.1), so
the shape the brief expected to test does not exist in the corpus. The
underlying question — what does bit-blasting cost where a solver struggles —
was answered instead on the division identity: `b = 0` or
`(a / b) * b + a % b = a`. It is true, and it needs the whole divider circuit,
so it measures what a divider costs. **These are constructed theorems, not
corpus pairs, and are labelled as such in `L1_divide_ladder.json` itself.**

### 6.2 The ladder, at three ceilings

| width | SAT ceiling | elaborator heartbeats | /tmp | outcome | wall s | `lean` peak MB |
|---|---|---|---|---|---|---|
| 8 | 10 s (default) | default | 1g | PROVED | 0.47 | 477 |
| 16 | 10 s (default) | default | 1g | SAT solver timed out | 10.2 | 477 |
| 32 | 10 s (default) | default | 1g | SAT solver timed out | 10.2 | 477 |
| 64 | 10 s (default) | default | 1g | SAT solver timed out | 10.3 | 508 |
| 16 | 600 s | default | 1g | elaborator heartbeat limit | 218.8 | 6,800 |
| 32 | 600 s | default | 1g | SAT solver timed out | 601.4 | 6,800 |
| 64 | 600 s | default | 1g | SAT solver timed out | 601.5 | 6,800 |
| 16 | 600 s | OFF | 1g | certificate truncated at the /tmp cap | 223.3 | 6,803 |
| 16 | 600 s | OFF | **4g** | **PROVED** | **283.1** | **12,209** |
| 32 | 600 s | default | 4g | SAT solver timed out | 601.4 | 12,462 |
| 64 | 600 s | default | 4g | SAT solver timed out | 601.5 | 12,462 |

**GLOSS, and this is the point of the table.** Three DIFFERENT ceilings stopped
the 16-bit case in turn, and each looked like a final answer until it was
raised. The first was the SAT solver's own 10-second default. The second was
Lean's elaborator heartbeat limit. The third was not a time limit at all —
**LITERAL**, from `L1_l13_render_errors_and_heartbeats.sh`
(host log `<runs>/L1/agent/logs/20260907T004924Z__L1_l13_render_errors_and_heartbeats.sh.log`):

```
exit 1  wall 223.3 s  child peak 6803.1 MB
Edges/divide_identity_16_nolimit.lean:7:2: error: SAT solver produced invalid LRAT: offset 1073500160: unexpected end of input
```

That offset is 1,073,500,160 bytes, which is the instance's 1 GiB `/tmp` cap
to within a rounding of the tmpfs's own overhead. The SAT solver had SOLVED the
problem; the proof certificate Lean then wanted to check did not fit. With
`/tmp` raised to 4g the same theorem is accepted — **LITERAL**, from
`L1_l24_final_measurements.sh`:

```
exit 0  wall 283.1 s  child peak 12208.8 MB
(no output: the theorem was accepted)
```

**So the answer changed at the raised ceiling, and the earlier "16 bits does
not prove" is retracted: 16-bit division PROVES, in 283 seconds, needing about
12 GB of memory and more than a gigabyte of certificate.** 32 and 64 bits
remain undecided at a 600-second SAT ceiling; whether they would prove with
more room is not known and was not measured.

### 6.3 The memory appetite is opportunistic, which the instance conf now records

The `lean` child's peak went 6,800 MB at an 8g container and 12,462 MB at a
12g container, on the same theorems. That is the same pattern task 83 measured
for the term transcription (log_189 §2.6): the peak follows whatever ceiling
it is given. `Airlock/instances/L1.conf` states this, states
that `/tmp` is RAM so raising it raises the instance's memory need by the same
amount, and states that the per-lane named abort `ABORT_MEMORY_L1` watches
only the lane's own parent process — the `lean` child is governed by the
container ceiling and by nothing else.

---

## 7. The operators the term walk emits, and what the subset covers

Counted over every printed layer-5 text in `the_pool5.json` — 1,267 distinct
texts over 1,831 entries, of which 862 print any text at all. **LITERAL**,
from `L1_l13_render_errors_and_heartbeats.sh` (host log
`<runs>/L1/agent/logs/20260907T004924Z__L1_l13_render_errors_and_heartbeats.sh.log`):

| printed token | uses | entries carrying it | covered by Render.lean | if not, why |
|---|---|---|---|---|
| `<numeral>` | 25143 | 855 | yes, `lit` | - |
| `<free symbol vN>` | 11489 | 856 | yes, `var` | - |
| `Extract` | 9337 | 727 | yes, `extract` | - |
| `fpToFP` | 5855 | 287 | no | floating point |
| `fpIsNaN` | 2251 | 275 | no | floating point |
| `If` | 2092 | 656 | yes, `ite` | - |
| `Concat` | 1811 | 548 | yes, `concat` | - |
| `fp` | 1801 | 145 | no | floating point |
| `to_ieee_bv` | 1801 | 145 | no | floating point |
| `+` | 1221 | 250 | yes, `add` | - |
| `Or` | 1219 | 360 | no | a truth connective; the subset's condition is a one-bit word |
| `\|` | 1011 | 420 | yes, `or` | - |
| `RNE` | 983 | 115 | no | floating point (a rounding mode) |
| `Not` | 944 | 371 | no | a truth negation; the subset's condition is a one-bit word |
| `fpEQ` | 880 | 248 | no | floating point |
| `~` | 614 | 222 | yes, `not` | - |
| `-` | 503 | 34 | yes, `sub` | - |
| `==` | 488 | 335 | yes, `eq` | - |
| `<` | 384 | 90 | no | a signed compare; the subset carries only eq |
| `*` | 239 | 133 | yes, `mul` | - |
| `And` | 216 | 108 | no | a truth connective; the subset's condition is a one-bit word |
| `ULE` | 167 | 160 | no | an unsigned compare; the subset carries only eq |
| `<=` | 140 | 126 | no | a signed compare; the subset carries only eq |
| `^` | 128 | 22 | yes, `xor` | - |
| `>>` | 91 | 87 | yes, `ashr` | - |
| `LShR` | 52 | 47 | yes, `lshr` | - |
| `<<` | 35 | 34 | yes, `shl` | - |
| `bvsrem_i` | 33 | 9 | no | remainder, and z3's UNGUARDED remainder at that |
| `/` | 29 | 22 | no | no rule written |
| `bvudiv_i` | 14 | 14 | no | division, and z3's UNGUARDED division at that |
| `bvurem_i` | 11 | 11 | no | remainder, and z3's UNGUARDED remainder at that |
| `bvsdiv_i` | 8 | 8 | no | division, and z3's UNGUARDED division at that |

```
pool5 entries whose every printed token is covered by Render.lean's subset: 213 of 862 entries that print any text (of 1831 entries in all)
```

**GLOSS.** 213 of 862 is 25%. What keeps it there is not exotic: the two
comparison groups and the three truth connectives together appear in far more
entries than division and remainder do, and they are the cheapest thing to
add. Floating point is the large remainder and is a different kind of problem.

**A census artifact, recorded because it changed a number.** An earlier run of
this census matched RUNS of symbol characters, so `2*~x` counted as one token
`*~`; the tokenizer now takes two-character operators and then single
characters. The difference was one use of `*` and one of `~`, and one entry.

---

## 8. Scope estimate

Estimates, stated as estimates. The unit is person-days of the same kind of
work this task did, and the base is that the integer subset took this session:
374 lines of Lean over ten build iterations.

| part | what it needs | covered today | estimate |
|---|---|---|---|
| the integer subset, 18 constructors | done | yes | 0 (this task) |
| signed and unsigned comparisons (`<`, `<=`, `ULE`, `ULT`) as one-bit results | 4 constructors; render as `(a < b) ? 1 : 0`, with a cast to the signed holder for the signed pair; the lemmas are the cast round trip | no | 1–2 |
| truth connectives (`And`, `Or`, `Not`) over conditions | either a Bool sort in `Term` or the one-bit word kept and rendered `&&`, `\|\|`, `!`; the second is smaller and matches the machine | no | 1–2 |
| division and remainder, guarded | the zero-divisor split AND C's second undefined case, `INT_MIN / -1`; the Lean-versus-SMT-LIB disagreement of §4.3 has to be stated in the term language, not papered over | no | 3–5 |
| z3's unguarded division symbols | NOT a Lean problem: the term store prints `bvudiv_i`, which has no specified value at a zero divisor. Either the transcriber stops simplifying into it, or the store keeps the guarded form beside it | blocked upstream | 1, in the pipeline |
| floating point | `bv_decide` has no floating-point theory, and core Lean ships no bit-blasted IEEE-754 model; an explicit model would have to be written and its `fpToFP` / `fpEQ` / `fpIsNaN` / rounding-mode cases proved | no | 15–30, and a line of its own |
| a rust `RExpr` | the term side, the induction, and every bit-vector lemma are reused unchanged; only the target language changes. Rust has no undefined behaviour here, so `evalR` is TOTAL and the `Option` disappears — but a shift past the width PANICS in a debug build and masks the count in a release build, so the renderer must pick one and the theorem must say which. Arithmetic is `wrapping_add` and friends; width changes are `as` casts | no | 2–4 |

**Total to close the integer side (comparisons, connectives, division):** 5–9
person-days, estimate. **With rust beside C:** 7–13. **Floating point is the
large item and is not on that path.**

---

## 9. The spelling-ban guard, pasted verbatim as required

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

**The guard caught this task, and the program was fixed rather than the
guard.** In `L1_l23_axioms_and_guard.sh` (host log
`<runs>/L1/agent/logs/20260907T011140Z__L1_l23_axioms_and_guard.sh.log`)
the two division-ladder files FAILED
with 8 findings each: the ladder rows are not pairs of pool entries, and the
program had written the string `"-"` into their `entry_a` and `entry_b`
fields as a placeholder — and `-` is one of the 91 operator tokens the guard
reads from the probe manifests. **LITERAL**, one finding:

```
FAIL L1_divide_ladder.json -- 8 spelling-keyed place(s)
     $.rows[0].entry_a
         operator token '-' on a structure field -- this is a grouping/row key, not a per-unit label
```

`run_edges_L1.py` now writes `null` in those fields and the report prints
`(not a pool pair)`, and the ladder was re-run. **LITERAL**, from
`L1_l24_final_measurements.sh`:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS L1_edges_selected.json -- no operator token in any key, grouping, pairing or row structure
PASS L1_ten_edges.json -- no operator token in any key, grouping, pairing or row structure
PASS L1_three_undecided.json -- no operator token in any key, grouping, pairing or row structure
PASS L1_divide_ladder.json -- no operator token in any key, grouping, pairing or row structure
PASS L1_divide_ladder_t600.json -- no operator token in any key, grouping, pairing or row structure
--- guard exit 0
PseudoCoupHQ/Research/op_pipeline/lean/L1_edges_selected.json:0
PseudoCoupHQ/Research/op_pipeline/lean/L1_ten_edges.json:0
PseudoCoupHQ/Research/op_pipeline/lean/L1_three_undecided.json:0
PseudoCoupHQ/Research/op_pipeline/lean/L1_divide_ladder.json:0
PseudoCoupHQ/Research/op_pipeline/lean/L1_divide_ladder_t600.json:0
PseudoCoupHQ/Research/op_pipeline/lean/edges_L1.py:0
PseudoCoupHQ/Research/op_pipeline/lean/term_to_lean.py:0
PseudoCoupHQ/Research/op_pipeline/lean/run_edges_L1.py:0
PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof/Render.lean:0
```

The last block is `grep -c exempt` over every file this task added: zero in
every one. That grep's own exit status is 1 because a count of zero is what
`grep -c` reports as "no match", which is why the lane's exit line reads 1
while the guard's own exit line reads 0.

**On the selection keys, stated because the ban governs them.** The ten were
chosen by the printed character length of the longer of the two texts, capped
per machine type key — both machine-form properties. The three UNDECIDED pairs
were chosen one per UNDECIDED machine type key. No member's spelling label was
read at any point, and no candidate set was formed here at all: t100 fixed all
43,410 pairs from the machine form before any solver ran, and this task
re-read answered ones.

---

## 10. What was NOT done, by the brief's own stop rules

- **No Mathlib and no fetch.** The instance runs `proxy = no`, so no lane had a
  route out; `lake new` and `lake build` ran offline and the project has no
  dependencies.
- **Nothing under `Research/op_pipeline/` outside `lean/` was changed.** The
  spelling guard and `check_conventions_log_claims.py` were run unmodified.
- **The 32-bit and 64-bit division identities were not pursued past a
  600-second SAT ceiling.** They are reported as undecided at that ceiling,
  not as unprovable.
- **`the_pool5.json`, `pool100_edges.json` and every other t100 artifact were
  read only.**

---

## 11. Two lists

**Decided, recorded for audit:**

- The ten were taken from the union of `pool100_edges.json`'s `edges` and
  `pairs` lists, restricted to PROVED pairs that carry a printed text on both
  sides — a population of twelve — with a per-machine-type-key cap of six, the
  smallest cap that yields ten records across more than two keys.
- `bvudiv_i` and its four co-symbols are REFUSED by cause rather than
  translated, because z3's unguarded division has no specified value at a zero
  divisor and Lean's `/` answers zero there.
- `Term.eq` answers a one-bit word and `Term.ite` takes a one-bit condition,
  which keeps the Bool-versus-`BitVec 1` question out of the term language and
  confines it to the C model's `csel`.
- `CExpr` carries a shift by a plain integer beside a shift by a computed
  holder, because C's shift operand is an `int` after the usual promotions
  (§5.3). This changed the C model, not the term language.
- `L1.conf`'s `memory` was raised from the brief's 8g to 12g and `tmp_size`
  from 1g to 4g, with the measured reason written into the file: the 16-bit
  division's proof certificate was truncated at exactly the 1 GiB `/tmp` cap.
  The answer changed at the raised ceiling and both answers are in §6.2.
- `run_edges_L1.py` was changed after the spelling guard failed it; the guard
  was not touched.

**Awaiting the owner:**

- Whether the next step on this node is the cheap one — the four comparisons
  and the three truth connectives, 2–4 person-days, taking the covered share
  of pool entries from 25% toward roughly 60% — or the rust `RExpr`, which
  reuses the whole induction and would give the line two target languages
  proved rather than one.
- Whether the term store should stop printing z3's unguarded `bvudiv_i` form
  (§8, the row marked "blocked upstream"). It is one day of work in the
  pipeline and it is the only thing standing between the corpus's divisions
  and a Lean statement of them.

---

## 12. The same facts as commands that re-run

The verifier's first pass found 0 DIFFERS and 0 MATCHES: every claim was prose
or an attribution with nothing beside it. These five commands state the same
facts in a form the checker re-runs. Each was run in
`L1_l26_rerunnable_claims.sh` (host log
`<runs>/L1/agent/logs/20260907T014729Z__L1_l26_rerunnable_claims.sh.log`);
the working directory is `PseudoCoupHQ`.

**The ten, by outcome** — eight proved, two refused as floating point (§3.3):

```
$ python3 -c "
import json
d = json.load(open('Research/op_pipeline/lean/L1_ten_edges.json'))
for r in d['rows']:
    print(r['type_key'], r['entry_a'], r['entry_b'], r['outcome'], r.get('cause','-'))
"
rdi,rsi,rcx|8 E00338 E00339 PROVED_BY_LEAN -
rdi,rsi|8 E00156 E01664 PROVED_BY_LEAN -
rdi,rsi|8 E00170 E01654 PROVED_BY_LEAN -
rdi,rsi,rcx|8 E00341 E00342 PROVED_BY_LEAN -
rdi,rsi,rcx|8 E01658 E01661 PROVED_BY_LEAN -
rdi,rsi,rcx|8 E01653 E01660 PROVED_BY_LEAN -
rdi,rsi,rcx|8 E01659 E01663 PROVED_BY_LEAN -
rdi,rsi,rcx|8 E01672 E01675 PROVED_BY_LEAN -
rcx,xmm0|32 E01445 E01507 REFUSED_BEFORE_LEAN FLOATING_POINT
xmm0,xmm1|8 E00920 E01004 REFUSED_BEFORE_LEAN FLOATING_POINT
```

**The proof file's size, and that it contains no hole** (§5.2). The second
count is of the word a hole would leave behind, and it is zero:

```
$ wc -l Research/op_pipeline/lean/archproof/Archproof/Render.lean
374 Research/op_pipeline/lean/archproof/Archproof/Render.lean
```

```
$ grep -c sorry Research/op_pipeline/lean/archproof/Archproof/Render.lean
0
```

**The eighteen constructors, read off the file rather than retyped** (§5.2):

```
$ python3 -c "
import re
s = open('Research/op_pipeline/lean/archproof/Archproof/Render.lean').read()
body = s.split('inductive Term')[1].split('/-- The term')[0]
names = re.findall(r'^  \| (\w+)', body, re.M)
print(len(names), names)
"
18 ['var', 'lit', 'add', 'sub', 'mul', 'and', 'or', 'xor', 'not', 'shl', 'lshr', 'ashr', 'extract', 'concat', 'zext', 'sext', 'eq', 'ite']
```

**The division ladder at both SAT ceilings** (§6.2). `sat_timeout None` is
`bv_decide`'s own 10-second default:

```
$ python3 -c "
import json
for f in ('L1_divide_ladder.json', 'L1_divide_ladder_t600.json'):
    d = json.load(open('Research/op_pipeline/lean/' + f))
    print(f, 'sat_timeout', d['meta']['sat_timeout_seconds'])
    for r in d['rows']:
        print('   ', r['type_key'], r['outcome'], r['wall_seconds'], 's')
"
L1_divide_ladder.json sat_timeout None
    constructed, 8 bits PROVED_BY_LEAN 0.474 s
    constructed, 16 bits LEAN_ERROR 10.173 s
    constructed, 32 bits LEAN_ERROR 10.192 s
    constructed, 64 bits LEAN_ERROR 10.278 s
L1_divide_ladder_t600.json sat_timeout 600
    constructed, 8 bits PROVED_BY_LEAN 0.49 s
    constructed, 16 bits LEAN_ERROR 239.455 s
    constructed, 32 bits LEAN_ERROR 601.402 s
    constructed, 64 bits LEAN_ERROR 601.483 s
```

**What t100's UNDECIDED pairs are** (§4.1) — 1,099 of them, in three machine
type keys that are all xmm register families, and not one carries a term:

```
$ python3 -c "
import json
d = json.load(open('Research/op_pipeline/pool100_edges.json'))
u = [e for e in d['pairs'] if e.get('state') == 'UNDECIDED']
k = {}
for e in u:
    k[e['type_key']] = k.get(e['type_key'], 0) + 1
print('UNDECIDED', len(u))
print('type keys', sorted(k.items(), key=lambda kv: -kv[1]))
print('carrying a term_a field', sum(1 for e in u if e.get('term_a')))
"
UNDECIDED 1099
type keys [('rcx,xmm0|32', 689), ('rcx,xmm0,xmm1|32', 366), ('rcx,xmm0,xmm1|8', 44)]
carrying a term_a field 0
```

---

## 13. Verifier tally

Two passes. Pass 1 (`L1_l25_verify.sh`, host log
`<runs>/L1/agent/logs/20260907T014651Z__L1_l25_verify.sh.log`)
found 0 DIFFERS but also 0 MATCHES over 29 claims: everything was prose or an
attribution with nothing beside it. Section 12 was added in answer, stating the
same facts as commands. Pass 2, **LITERAL**, from `L1_l27_verify2.sh` (host log
`<runs>/L1/agent/logs/20260907T014810Z__L1_l27_verify2.sh.log`),
run FROM the L1 instance:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_227_task_L1_lean_second_discharger.md
   claims 35 | MATCHES 6 | DIFFERS 0 | UNVERIFIABLE 29 | REFUSED 0 | NOT_RERUNNABLE 0
population: 35 claims across 1 logs
  MATCHES          6
  DIFFERS          0
  UNVERIFIABLE     29
  REFUSED          0
  NOT_RERUNNABLE   0
ONE LINE: 6 of 35 claims reproduce; 29 (83%) carry nothing to re-run
causes, by name:
  attribution_only                 20
  prose_only                       8
  pasted_without_source            1
check_conventions_log_claims.py exit 0
```

**TALLY LINE: claims 35 | MATCHES 6 | DIFFERS 0 | UNVERIFIABLE 29 | REFUSED 0 |
NOT_RERUNNABLE 0. Zero DIFFERS.** All six MATCHES are section 12's commands.
The 29 UNVERIFIABLE are the prose and the LITERAL blocks quoted from lane logs;
each of those names its lane script and the host path of its log, which is the
attribution the standing rule asks for, but a quoted lane transcript is not
itself a command the checker can re-issue.

---

## 14. See also

- `PseudoCoupHQ/Research/op_pipeline/lean/README.md` — what is
  in the artifact folder and what the first runs found.
- `PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof/Render.lean`
  — the preservation theorem and everything it rests on.
- `PseudoCoupHQ/Research/op_pipeline/lean/term_to_lean.py` — the
  translator, with its refusal causes documented in its header.
- `PseudoCoupHQ/Research/op_pipeline/lean/lanes_L1/` — all 24
  lane scripts, in submission order.
- `PseudoCoupHQ/DevComms/log_224_task_t100_pool_entry_equivalence_closure.md`
  §6 — t100's own account of the 1,099 UNDECIDED pairs and the 120-second
  runner limit that produced them.
- `PseudoCoupHQ/DevComms/log_221_opcode_signature_algebra.md`
  §7 — the claim this task's §5 is the source-level half of.
