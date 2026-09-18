# log 294 — eight languages, and the gate read at the right statement

2026-09-16. Follows `log_293_below_sail_gmp_softfloat_and_the_float_gap_sized.md`.
Two results, on the two axes the owner named: emulation across languages, and proof
of the emulations. Both are measured; nothing here is a plan.

## 1. The correction that opened the turn

the owner challenged §6.8.2 of log 293 and the matching passage in the public
README:

> we have emulations for every arch-opcode and every primitive so how is
> anything escaping the machinery? im questioning your understanding of the
> project.

He was right. `BUILDFAIL` means *that compiler refused that spelling*, and
the log had written it up as *the operation has no meaning*. Sorted by what
was actually refused, **691 of the 737 are buildable from pieces already in
the corpus** and only 46 are not runtime operations at all. Both documents
were corrected in place, with the original sentence named rather than quietly
removed; §6.8.2 and §8 of log 293 carry the full table.

## 2. The gate: 5 of 20 to 8 of 20, and why the rest are not failures

### 2.1 The run that had been measured against superseded code

`leanpath/equals.py` carries this in `simp_set`'s docstring:

> This was three copies — two here and a third in a lane's heredoc — and on
> 2026-09-16 a fix landed in one of them while the gate ran another, so the
> run reported UNDECIDED against code that had not changed.

That is exactly what had happened. Lane l100 ran its own inlined
`bodies_and_defs`, which assembles the simp set in TWO layers — the emitted
definitions the text reaches, then the lean-sail helpers those call. Lane
l101 measured what `bv_decide` actually accepts (eighteen probes, eleven
proved, seven refused) and added the THIRD layer to the module as
`CORE_NORMALISE`. The gate had never been run with it.

Lane **l102** changed exactly one thing: the simp set comes from
`leanpath.equals.simp_set`, the one place, instead of from a copy inside the
lane. The tower did not have l101's `equals.py` or `strip.py` at all — those
edits existed only on the laptop — so both files were copied across first and
the module import checked before the lane was submitted.

| | l100 | l102 |
|---|---|---|
| theorems proved | 5 of 20 | **8 of 20** |
| moved | — | `au_182_c_pos_i32` abi, `au_409_go_pos_i32` abi, `au_452_go_band_i32_i32` abi |

(Log 293's chat summary said "4 of 20" for l100. That was a count of table
ROWS, not of theorems; l100 proved 5. Corrected here.)

### 2.2 My own defect in l102, and its retraction

l102's step [4/4] re-elaborated the still-unproved files to classify them, and
ran `lake env lean` from the artifact folder instead of from the proof
project. All twelve answered `unknown module prefix 'LeanIM'`, and the lane
then counted zero counterexamples and zero spurious abstractions in twelve
files that had never been elaborated. **That count said nothing and is
retracted.** The VERDICTS are unaffected: `equals` runs Lean through
`walk.lean_run(proof_project, …)`, which sets the project itself. Lane
**l103** redid the reading from `$P`.

### 2.3 What the twelve actually are

`bv_decide` says two different things and they are not the same result:

| cause | n | what it means |
|---|---|---|
| **FALSE — real counterexample** | 6 | the statement is wrong, and Lean gives the input that breaks it |
| **NORMALISATION — an atom stayed abstract** | 6 | the goal was never fully bit-blasted; not a disproof |

Every one of the six FALSE is a `plain` statement, and every counterexample
is a high-bit input — `a = 0xffffffffffffffff`, or `0x7fffffffffffffff`. That
is not a proving failure. It is the psABI: an `int32_t` argument arrives in a
64-bit register already sign-extended, and the `plain` form puts the two
sides against each other with **no such precondition**, where they genuinely
differ in the high bits. The `plain` statement is the wrong statement to put.

Read at the statement that is actually true, the gate stands at:

| statement | proved | blocked | false |
|---|---|---|---|
| **abi** (the psABI precondition supplied) | **7 of 10** | 3 | 0 |
| plain (no precondition) | 1 of 10 | 3 | 6 |

### 2.4 The remaining three, named

All three abstract the same shape, Sail's "is this bitvector non-zero" test:

```
match 0 <b Int.ofNat (…).toNat with | true => 1#1 | false => 0#1
```

The scrutinee leaves the BitVec fragment through `Int`, and the `match` around
it is abstracted whole. `au_445_go_shr_i32_u64` additionally carries
`.sshiftRight (Int.ofNat …)` — an arithmetic shift whose count arrives the
same way.

**Lane l104 put that to the test and my hypothesis was wrong.** The lane
re-ran l102's own three files — not an imitation of them — with the
`simp only` list edited four ways:

| variant | the list | result |
|---|---|---|
| V0 | exactly as l102 put it | still abstract |
| V1 | minus `zopz0zI_u`, `zopz0zI_s`, `Sail.BitVec.toNatInt` | still abstract, and WORSE |
| V2 | V0 plus six library lemmas | still abstract |
| V3 | V1 plus the same six | still abstract |

All fourteen candidate names elaborate — `BitVec.ofBool`, `BitVec.ult`,
`BitVec.ult_iff_lt`, `BitVec.toNat_ne_zero`, `Int.ofNat_pos`,
`decide_eq_true_eq`, `Bool.cond_eq_ite` and the rest — so none of this is a
vanished name. They simply do not reach it. And leaving Sail's comparison
folded made the atom BIGGER, not smaller: under V1 and V3 `bv_decide`
abstracts the whole `pure_RTYPE zero_reg (…) SLTU` instead of just the
comparison inside it.

**The cause, read out of the Sail library rather than guessed.**

```lean
-- .lake/packages/Sail/Sail/Common.lean
@[simp_sail] def toNatInt {w : Nat} (x : BitVec w) : Int := Int.ofNat x.toNat

-- LeanIM/Prelude.lean
def zopz0zI_u (x y : BitVec k_n) : Bool :=
  ((BitVec.toNatInt x) <b (BitVec.toNatInt y))
```

Sail defines its unsigned comparison over **Int**, through `Int.blt` — the
Bool-valued `<b`. `BitVec.ult` is the same predicate and is inside
`bv_decide`'s fragment; `Int.blt` is not. The library lemmas that would
bridge a Prop-valued `<` (`Int.ofNat_lt` and kin) cannot fire on a Bool-valued
`<b`, which is exactly why every candidate missed.

And Sail ships no bridge: `@[simp_sail]` marks the DEFINITIONS so they unfold,
and a grep for `ult` or `blt` across the whole Sail Lean library returns
nothing. **This is the same shape of finding as the float gap of log 293 — a
hole in Sail's Lean backend, not in Lean and not in the walk.**

What would close it is one small lemma per comparison,
`zopz0zI_u x y = x.ult y` and `zopz0zI_s x y = x.slt y`, proved rather than
assumed. That is NOT yet measured, and it is hand-written Lean against Sail's
own mangled names, so it carries the churn hazard recorded for `Bridges.lean`:
it breaks the day Sail renames `zopz0zI_u`. It should be generated from Sail's
Prelude, not typed.

## 3. Language expansion: four to eight

The emitter turns each flattened single-block slice into ordinary source by a
one-instruction-to-one-statement walk, so a language is one `Backend` class.
Four were added, chosen because the sandbox image already carries their
toolchains.

**Corrected twice, 2026-09-16, both by the owner.** The first draft said "none of
them compiles to RISC-V natively" — wrong; OpenJDK, CPython, CRuby and V8 all
have riscv64 ports and all four run on RISC-V. The second draft said they
"cannot contribute an arch-unit" because their operators have "no fixed
instruction sequence to point at" — also wrong, and the same error twice:

> the interpreter is an intermediate step between high level
> compiler-operator and the final lowered form. the machine has to know which
> instructions to run on the machine. its not just floating in IR opcode space
> being computed by the Gods.

He is right. An interpreter is a step on the way to the lowering, not a
substitute for it. python's `a + b` on two ints runs a definite sequence of
riscv64 instructions — the `BINARY_OP` dispatch in `ceval.c`, the specialised
integer path, `long_add` in `longobject.c` — and that sequence is compiled
into the CPython binary. It is an arch-unit. So is ruby's. java's and
javascript's lowered forms are produced by their JITs at run time and are
dumpable (`-XX:+PrintAssembly`, `--print-opt-code`), varying with tier and
profile but not absent.

So the honest statement about these four is only this: **the line has not yet
carved their arch-units**, and what was added here is emulation targets. What
it would take to carve them is named in §4 — it is the SAME pipeline the 67
SoftFloat slices came out of, pointed at the interpreter binary instead of at
`libsoftfloat`.

python, ruby and javascript share one representation and differ only in
spelling, so they share a `_MaskedBackend`. Width 1 is the integer 0 or 1
rather than a boolean, so `and`, `or` and `xor` are the same three symbols at
every width; 128 costs nothing. java is the one that had to do real work.

The three don't-care pins of the emitter — a shift amount taken modulo the
width, `ctlz(0)` the bit width, `udiv` by zero yielding zero — are made in
each language's helper file and nowhere else, and are the Go helpers'
semantics, which the SoftFloat test had already passed.

### 3.1 Verification

`verify_emulations.py` links c, c++, rust and go to SoftFloat IN-PROCESS.
None of the four new languages can do that without an FFI layer whose own
correctness would then be part of what is under test, so `verify_langs.py`
makes the comparison OUT OF PROCESS and states the split rather than hiding
it: one vector plan in python so every language is handed identical bytes; a
C program built against the SAME `sfref_<op>` oracle writes the expected
answers; each language reads both files and reports the first mismatch. What
is compared is still SoftFloat's bits.

```
  java     67 of 67 operations bit-exact
  python   67 of 67 operations bit-exact
  ruby     67 of 67 operations bit-exact
  js       67 of 67 operations bit-exact
```

Roughly 20,000 vectors per operation — every edge crossing the plan keeps
(±0, ±inf, quiet and signalling NaN, largest and smallest normal and
subnormal, ±1, ±2, ±0.5 and one ulp either side of each), then uniform random
patterns from the same xorshift64 seed. The record is
`softfloat_slices/measurements/verify_langs.json`.

**Every RISC-V float arch-opcode now has an integer-only definition in eight
languages, four of which have no float instruction to lower to at all.**

### 3.2 The arch-units, the same four languages

The 492 arch-units went the same way. Both builders carry their own, smaller,
all-`uint64` backend — every arch-opcode routes through an `au_*` helper, so a
language is its backend plus its helper library and nothing else.

Three things had to be fixed, and each was a real defect rather than a
transcription slip:

- **the file header comment** was chosen by a hard-coded language list
  (`"//" if be.lang in ("rust", "go", "cpp") else " *"`), so python and ruby
  were handed a C block-comment body and every file failed to parse. It is now
  a backend property, `line_comment`, and the in-body note is a backend method,
  `note()`. A language added later cannot silently inherit C's comment.
- **java's argument widths.** An emulation whose IR parameter width is 32
  takes an `int`, and java will not pass a `long` for one.
- **java's return widening.** `(long) anInt` SIGN-extends, which would put
  ones in the top half of a register that must be zero. Every call is now cut
  to the parameter widths and widened back by an explicit mask, both read from
  the corpus record rather than guessed. python, ruby and javascript need
  neither: their emulations already answer non-negative and held to the width.

The integer helper library was cross-checked against the C one before any
arch-unit was built — 34 helpers over 18 values, 9,162 rows including
`MIN64 / -1`, divide and remainder by zero, shifts at 63 and 64, the `sra`
sign fill and every `w` variant:

```
  python   agrees with C on all 9162 rows
  ruby     agrees with C on all 9162 rows
  js       agrees with C on all 9162 rows
  java     agrees with C on all 9162 rows
```

Then `scripts/verify_arch_langs.py` put every arch-unit against the c
arch-unit — c is the oracle here because `verify_arch_units.py` and
`verify_arch_units_int.py` already put c against the real compiled RISC-V
behaviour — over 2,021 to 2,441 vectors each (every crossing of 21 register
boundary values, then uniform random):

```
  java     492 of 492 arch-units bit-identical to c
  python   492 of 492 arch-units bit-identical to c
  ruby     492 of 492 arch-units bit-identical to c
  js       492 of 492 arch-units bit-identical to c
```

**What this is and is not, in the standard language.** There are still
exactly **492 arch-units**, every one of them **riscv64**
(`clang --target=riscv64-unknown-linux-gnu`, `GOARCH=riscv64 go build`), and
every one of them lowered from a **c (385) or go (107)** compiler-operator.
Those two languages are the only ones that contribute arch-units. What grew is
the number of languages each arch-unit is EMULATED in, four to eight. Per
the owner's ruling of 2026-09-14, a compiled emulation is not an arch-unit, and a
table reading "492 arch-units | 8 languages" blurs exactly that — it is 492
arch-units, each with 8 emulations.

**No cross-architecture mapping is used anywhere in this.** One architecture
throughout. The only x86 in `attest_rv.json` is a compile-or-refuse agreement
cross-tab — whether the x86 build refused the same probes — not a mapping of
bodies between architectures.

| | arch-units | architecture | lowered from | emulated in | verified against | vectors each |
|---|---|---|---|---|---|---|
| 67 SoftFloat operations | — | — | — | 8 | Berkeley SoftFloat | ~20,000 |
| the arch-unit corpus | 492 | riscv64 only | c, go | 8 | the c emulations | ~2,000–2,400 |

The record is `measurements/verify_langs.json` and
`measurements/verify_arch_langs.json`.

## 4. What is NOT done

- The normalisation probe of §2.4 — lane l104 puts it to the REAL goals rather
  than to an imitation of them: l102's own three files, re-run with the
  `simp only` list edited four ways, including the one that leaves Sail's
  comparison folded instead of unfolding it into Int.
- The `plain` statement should stop being put: §2.3 shows it is false by
  construction, so it costs a Lean run per unit and can only ever answer
  UNDECIDED or FALSE.
- The arch-units are emulated in eight languages and PROVEN in none of them
  except through the ten-unit gate, which is c and go only. Widening the gate
  is the next measurement, not a new capability.
- **Carving arch-units out of an interpreter.** python and ruby each have a
  lowered form for every operator; it sits inside the interpreter binary. The
  route is the one already built and already run once:

  | stage | on SoftFloat | on CPython |
  |---|---|---|
  | compile for riscv64 | `libsoftfloat` | CPython |
  | link transitive helpers | done | done |
  | `internalize` to one entry | `f64_add` | the specialised `BINARY_OP` integer path |
  | inline, dead-code eliminate | done | done |

  What is genuinely harder, and must be named rather than waved at: the
  interpreter path ALLOCATES (`_PyLong_New`), LOOPS over bignum digits, and
  refcounts. Memory and loops are what the FLATTENER refuses — not the
  slicer, and not the attestation. Localising the allocation is the same
  problem as the exception-flag globals of log 293 §6, which was solved at IR
  level; bounding the bignum loop means pinning the small-integer fast path,
  which is a context specialisation exactly like pinning the rounding mode.
  So the obstacle is real and it is engineering, not absence.
- **The architecture axis, which is not the language axis.** Every arch-unit
  in the corpus is riscv64. The original corpus also records each unit's
  x86-64 ship body (`riscv/claim_check.py` walks it; `attest_rv.json` counts
  610 c and 107 go probes the x86 store holds one for). The same
  compiler-operator therefore already has two lowerings on record, and joining
  them keyed on the compiler-operator is available and unbuilt. Nothing in
  this log does that.

## 5. Two lists

Decided, recorded for audit:

- §6.8.2 and §8 of log 293 and the README passage corrected; the original
  wording is named in place;
- l102 submitted after copying `equals.py` and `strip.py` to the tower, which
  did not have l101's changes; module import verified before submission;
- l102's residual step was wrong, is retracted in §2.2, and l103 replaced it;
- four backends added to `scripts/emit_emulations.py`, four more to each of
  `scripts/build_arch_units.py` and `scripts/build_arch_units_int.py`, their
  helper libraries hand-written and cross-checked against C before use, and
  `scripts/verify_langs.py` and `scripts/verify_arch_langs.py` added;
  everything tracked and committed by the daemon;
- the file-header comment and the in-body note became backend properties in
  both arch-unit builders, replacing a hard-coded language list;
- lane names l102, l103 and l104 used, batch `lp3`.
- l104 is a NEGATIVE result and is reported as one: the hypothesis it
  tested was mine, it was wrong, and the four variants are in §2.4 with
  what they actually did.

Awaiting the owner:

- **the `zopz0zI_u` bridge.** §2.4 shows the last three arch-units are blocked
  by Sail defining its comparison over `Int.blt`, with no lemma back to
  `BitVec.ult` anywhere in its Lean library. The fix is a generated bridging
  lemma per comparison. It is small, but it is Lean we would be WRITING rather
  than deriving, against Sail's mangled names — the exact hazard recorded when
  `Bridges.lean` broke on a Lean minor version. Generating it from Sail's own
  Prelude is the way that keeps it a derivation; confirm before it is built.
- everything else in §4 is unambiguous and needs no ruling.
