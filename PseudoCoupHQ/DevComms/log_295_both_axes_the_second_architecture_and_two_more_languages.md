# log 295 — both axes: the second architecture, and two more languages

2026-09-17. Follows log 294. the owner named two directions and gave the conn:
cross-architecture mappings, and language expansion. Both are measured here.
Neither needed new theory; one of them needed almost no new code.

## 1. What I had wrong going in, and what the repository already held

I told the owner that java, python, ruby and javascript "have no fixed instruction
sequence to point at". He corrected it:

> the interpreter is an intermediate step between high level compiler-operator
> and the final lowered form. the machine has to know which instructions to
> run on the machine. its not just floating in IR opcode space being computed
> by the Gods.

He was right, and the line had already proved it. `op_pipeline/term66_store`
holds **30,280 units on x86-64**, 27,866 of them `PROVED_ON_SHIP`, and among
them a population marked `interpreter`:

| unit | lang | operator | its term | how the operands arrive |
|---|---|---|---|---|
| `cpython/long_add_fastpath` | cpython | `+` | `v0 + v1` | typed-pointer(PyLongObject*) |
| `ruby/rb_fix_plus` | ruby | `+` | `v0 + v1` | tagged-value(Fixnum, 2n+1 encoding) |
| `ruby/rb_int_plus` | ruby | `+` | `v0 + v1` | tagged-value(Fixnum, 2n+1) |
| `php/add_function` and three ZEND handlers | php | `+` | `v0 + v1` | typed-pointer(zval*) |
| `java/op_1` | java | `+` | `Extract(31,0,v0) + Extract(31,0,v1)` | plain |
| `java/op_2` | java | `/` | `bvsdiv_i(…)` over `Extract(31,0,…)` | — |

Every one `PROVED_ON_SHIP`, every one `branch_lines 0` and `call_lines 0`. The
missing concept in my account was `arrival_annotation`: an interpreter's
operands arrive as a typed pointer or a tagged value, and naming that is what
makes the unit well defined. It is recorded per unit and always was.

The x86-64 side also carries **twelve languages** with real shipped bodies —
cpp 770, c 610, javascript 240, csharp 253, swift 167, rust 125, go 107,
dart 82, php 4, ruby 3, java 2, cpython 1 — while riscv64 carried two. That
asymmetry, not any property of the languages, is the actual gap.

## 2. The cross-architecture mapping

### 2.1 It was built, and it had been run on eleven units

`riscv/claim_check.py` walks a unit's x86-64 ship body with
`op_pipeline/reference.py`, walks its riscv64 body with the RISC-V reference,
turns both into z3 bitvector terms, and asks the solver whether they agree at
the unit's own answer width. Task rv1 ran it on ELEVEN units, one per cell of
the arch-opcode model table.

Nothing about it was ever limited to eleven. `attest_rv.json` carries a
riscv64 body for 507 units and marks `x86_ship_body_in_the_store` on **every
one of them**, and the term store holds an answer home for all 507. So the
pairing was complete and had simply never been run. `pick_units_all.py` (new)
builds it; lane `rv1_l15` ran it in 211 seconds.

A unit whose term store record names no answer home is written
`NO_ANSWER_HOME` and skipped rather than given an invented one — the answer
home is what the comparison reads out of, so inventing one would invent the
verdict. On this corpus that case does not arise.

### 2.2 The first answer was wrong, and its own counterexamples said so

| outcome | free arguments |
|---|---|
| DIFFER | **184** |
| IDENTICAL_AFTER_NORMALIZE | 174 |
| EQUAL_BY_Z3 | 63 |
| RISCV_WALK_REFUSED | 36 |
| UNDECIDED | 36 |
| X86_WALK_REFUSED | 14 |

184 of 507 — 36% — is not believable for the same C source, and the
counterexamples say why: `c/op_0 !a` broken at `arg0 = 1946437878141681664`,
`c/op_103 a+b` at `arg0 = 2147483648`. High bits. Both terms took their
arguments as FREE 64-bit symbols, so the solver could put anything in the top
half of a register holding a 32-bit argument — and neither compiler was
answering that question. riscv64's psABI says a 32-bit integer arrives
sign-extended; x86-64 SysV leaves the high half unspecified.

**This is the same distinction the Lean path hit independently** (log 294
§2.3): there, every `plain` counterexample was a high-bit input too, and at
the `abi` statement seven of ten proved with none false. Two different
machines — z3 over disassembly here, `bv_decide` over Sail there — finding the
same thing is worth more than either alone.

### 2.3 The same 507, with the arrival promises

`claim_check.py` gained an OPTIONAL `assume-abi` word, default off, so lane
rv1_l15 and the rv1 run of record both reproduce unchanged. A 32-bit signed
argument is the sign-extension of its low half, a 32-bit unsigned the
zero-extension, a bool is 0 or 1, a 64-bit argument carries no promise and
gets none. Lane `rv1_l17`:

| outcome | free | **with the psABI** |
|---|---|---|
| DIFFER | 184 | **86** |
| EQUAL_BY_Z3 | 63 | **157** |
| IDENTICAL_AFTER_NORMALIZE | 174 | 174 |
| UNDECIDED | 36 | 40 |
| RISCV_WALK_REFUSED | 36 | 36 |
| X86_WALK_REFUSED | 14 | 14 |

- **92** of the 184 agree once the promise is supplied — the question had been
  asked wrong.
- **86** differ even with it.
- **0** went the other way. Nothing that agreed before now disagrees.

### 2.4 What the 86 actually are

| cause | n |
|---|---|
| a float term is a FREE FUNCTION, so the solver may answer it differently on each side (NaN, rounding) | 49 |
| the x86 body reads an arrival beyond the declared arguments | 31 |
| the x86 body loads a constant from memory, rip-relative, and it is unconstrained | 4 |
| **integer, no float term, no extra arrival** | **2** |

The two:

```
c/op_210  a / b  width 32  arg0 = 0xFFFFFFFF80000000, arg1 = 0
c/op_483  a == b width 32  (NaN-boxed float patterns)
```

`c/op_210` is the real one and it is architectural: RISC-V's `divw` DEFINES
division by zero as all-ones, x86's `idiv` TRAPS. That divergence is already
in the catalogue the README carries.

**So of 507 units compared across two architectures, 331 agree outright, 92
needed only the ABI promise, 84 of the remainder are named modelling gaps, and
2 are genuine.** The modelling gaps are all fixable and all specific: pin the
float operations to the same function on both sides, constrain the extra
arrivals, and read the rip-relative constants out of the object rather than
leaving them free.

## 3. Language expansion, on the side that grows the corpus

Adding an emulation TARGET does not grow the arch-unit population. Adding a
language whose compiler lowers for riscv64 does. Two were reachable with what
the image already carries, and lane `rv1_l16` measured both before either was
used — a small run read before a wide one:

| | flags | result |
|---|---|---|
| cpp | `clang++ -std=c++17 -O1 --target=riscv64-unknown-linux-gnu` | **3 of 3** |
| cpp | c's own flags, i.e. with `-nostdlibinc` | 0 of 3 — `cstdint file not found` |
| rust | `rustc --target=riscv64gc-unknown-linux-gnu` + the corpus ship flags | **2 of 3** |
| rust | `riscv64gc-unknown-none-elf`, which `inherit.py` uses | 0 of 3 — no std |

The rust "failure" is a REAL refusal — `the trait bound u64: Neg is not
satisfied`, rust declining to negate an unsigned — which is a BUILDFAIL of
exactly the kind the corpus already records. The objects came out
`elf64-littleriscv` with the `op_` symbol intact.

`riscv_carve.py` gained `SHIP["cpp"]`, `SHIP["rust"]` and their compile rules;
`rv_attest.py`'s language plan became a command-line argument, so no earlier
invocation changes meaning. Lane `rv2_l11` swept both, writing
`attest_rv_langs.json` — a NEW prefix, leaving the c and go corpus of record
untouched.

| lang | LIFTED | BUILDFAIL | WALK_REFUSED |
|---|---|---|---|
| cpp | **722** | 254 | 26 |
| rust | **116** | 733 | 9 |

**838 new riscv64 arch-units.** And they are not c duplicated:

| | arch-units | distinct compiler-operators | NOT present in c or go |
|---|---|---|---|
| of record (c, go) | 474 | 461 | — |
| cpp | 722 | 716 | **381** |
| rust | 116 | 116 | **108** |
| **after the sweep** | **1,312** | **946** | |

cpp brings C++'s alternative spellings — `and`, `bitand`, `bitor`, `not`,
`not_eq`, `or`, `xor` — and rust brings `..` and `..=`, range operators that
do not exist in c or go at all. The arch-unit population nearly tripled and
the compiler-operator coverage doubled.

## 4. Two lists

Decided, recorded for audit:

- `pick_units_all.py` written; it refuses to invent an answer home;
- `claim_check.py` gained `assume-abi` as an OPTIONAL fifth word, default off,
  so every earlier invocation is unchanged;
- `riscv_carve.py` gained cpp and rust rules, each with the reason its flags
  differ from c's written beside it and measured in rv1_l16 first;
- `rv_attest.py`'s plan is now named on the command line and never widened
  silently; the sweep wrote a NEW prefix and did not touch `attest_rv.json`;
- lanes rv1_l15, rv1_l16, rv1_l17, rv2_l11 used, batch `lp3`;
- log 294 corrected twice where the owner caught it: the four added languages RUN on
  RISC-V, and they DO have lowered forms.

Awaiting the owner:

- **whether the 838 new arch-units should be merged into the corpus of
  record.** They are in `attest_rv_langs.json` and nothing downstream reads
  it. Merging means `attest_rv.json` stops meaning "c and go" and every count
  in logs 293 and 294 is restated against a bigger denominator. That is a
  structural change to the record and is the owner's call, not mine.
- the 84 modelling gaps of §2.4 are each specific and fixable; say whether
  closing them is worth a lane before the float side is pinned.
