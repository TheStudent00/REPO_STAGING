# arch_units — every RISC-V arch-unit with a readable body, in c, c++, rust and go

Float layer made 2026-09-16 from `../../attest_rv.json` (task rv2) and
`../emulations/`; integer layer added 2026-09-16 from the same file.

## What an arch-unit is here

- a **compiler-operator** is one operator of one language on one pair of
  operand types — c's `!` on `float`, go's `>>` on `int32` and `uint64`
- an **arch-unit** is that compiler-operator wrapped in a function and lowered:
  the machine instructions the compiler emitted
- an **arch-opcode** is one machine instruction with what it reads and its width
- so an arch-unit is a list of arch-opcodes

## The population

`attest_rv.json` holds 1,244 RISC-V arch-units. 507 of them carry a body.

| | | |
|---|---:|---|
| `LIFTED` | 474 | a body, and the RISC-V reference walked all of it |
| `WALK_REFUSED` | 33 | a body, but one arch-opcode is missing from the walker's opcode table |
| `BUILDFAIL` | 737 | no body: the probe source did not compile for riscv64 at all |

**492 arch-units are emitted here, in two layers**, each as a single function in
**c, c++, rust and go**:

| layer | arch-units | languages | what it is |
|---|---:|---|---|
| **float** | 174 (150 c, 24 go) | 4 | every body containing a float instruction — 156 `LIFTED` plus the 18 `WALK_REFUSED` ones. Emulated with **integer operators only**. |
| **integer** | 318 (235 c, 83 go) | 4 | every `LIFTED` body containing **no** float instruction. |
| | **492** | | **all 474 `LIFTED` arch-units, plus 18 of the 33 `WALK_REFUSED`** |

Failures: **0**. Nine are emulated under a stated reduction (`&a`, see each
layer). The 15 `WALK_REFUSED` rows with no float instruction are not emitted:
they are outside the attested `LIFTED` population — see the last section.

---

# Layer 1 — the 174 arch-units that contain a float instruction

| | |
|---|---|
| arch-units | 174 (150 c, 24 go) |
| emulated as a bit function of the operands | 170 |
| emulated under a stated reduction | 4 (`&a`, see below) |
| failed | 0 |
| lines of source | 4,347 c · 4,698 c++ · 4,167 rust · 3,987 go |

## How an arch-opcode is mapped

Each arch-opcode goes one of three ways.

- **a float arch-opcode whose Sail clause calls a SoftFloat external** → the
  already-built emulation of that external, from `../emulations/`, re-emitted
  here at rounding mode 0.
- **a float arch-opcode whose Sail clause calls nothing** → written out here as
  bit manipulation. Sail declares these with a body, not as an external: they
  are register moves, sign splicing, the Zfa constant table, and loads and
  stores.
- **an integer arch-opcode** → the language's own integer operator.

The composition threads the machine's registers as ordinary unsigned 64-bit
locals in SSA order. **No float type appears in the arithmetic.** The caller
hands over the operand's bit pattern already, so there is no reinterpret to do
at the boundary at all.

### The float arch-opcodes across the 174

| arch-opcode | Sail clause | occurrences | arch-units | mapped to |
|---|---|---:|---:|---|
| `fadd.s` | `F_BIN_RM_TYPE_S` | 12 | 12 | emulation `f32_add_rm0` |
| `fsub.s` | `F_BIN_RM_TYPE_S` | 10 | 10 | emulation `f32_sub_rm0` |
| `fmul.s` | `F_BIN_RM_TYPE_S` | 10 | 10 | emulation `f32_mul_rm0` |
| `fdiv.s` | `F_BIN_RM_TYPE_S` | 10 | 10 | emulation `f32_div_rm0` |
| `fadd.d` | `F_BIN_RM_TYPE_D` | 14 | 14 | emulation `f64_add_rm0` |
| `fsub.d` | `F_BIN_RM_TYPE_D` | 12 | 12 | emulation `f64_sub_rm0` |
| `fmul.d` | `F_BIN_RM_TYPE_D` | 12 | 12 | emulation `f64_mul_rm0` |
| `fdiv.d` | `F_BIN_RM_TYPE_D` | 12 | 12 | emulation `f64_div_rm0` |
| `feq.s` | `F_BIN_TYPE_X_S` | 36 | 34 | emulation `f32_eq_rm0` |
| `flt.s` | `F_BIN_TYPE_X_S` | 2 | 2 | emulation `f32_lt_rm0` |
| `fle.s` | `F_BIN_TYPE_X_S` | 2 | 2 | emulation `f32_le_rm0` |
| `feq.d` | `F_BIN_X_TYPE_D` | 38 | 36 | emulation `f64_eq_rm0` |
| `flt.d` | `F_BIN_X_TYPE_D` | 2 | 2 | emulation `f64_lt_rm0` |
| `fle.d` | `F_BIN_X_TYPE_D` | 2 | 2 | emulation `f64_le_rm0` |
| `fcvt.s.w` | `F_UN_RM_XF_TYPE_S` | 10 | 10 | emulation `i32_to_f32_rm0` |
| `fcvt.s.wu` | `F_UN_RM_XF_TYPE_S` | 10 | 10 | emulation `ui32_to_f32_rm0` |
| `fcvt.s.l` | `F_UN_RM_XF_TYPE_S` | 10 | 10 | emulation `i64_to_f32_rm0` |
| `fcvt.s.lu` | `F_UN_RM_XF_TYPE_S` | 10 | 10 | emulation `ui64_to_f32_rm0` |
| `fcvt.d.w` | `F_UN_RM_XF_TYPE_D` | 10 | 10 | emulation `i32_to_f64_rm0` |
| `fcvt.d.wu` | `F_UN_RM_XF_TYPE_D` | 10 | 10 | emulation `ui32_to_f64_rm0` |
| `fcvt.d.l` | `F_UN_RM_XF_TYPE_D` | 10 | 10 | emulation `i64_to_f64_rm0` |
| `fcvt.d.lu` | `F_UN_RM_XF_TYPE_D` | 10 | 10 | emulation `ui64_to_f64_rm0` |
| `fcvt.d.s` | `F_UN_RM_FF_TYPE_D` | 10 | 10 | emulation `f32_to_f64_rm0` |
| `fmv.w.x` | `F_UN_TYPE_F_S` | 23 | 23 | bit manipulation — the low 32 bits |
| `fmv.d.x` | `F_UN_X_TYPE_D` | 23 | 23 | bit manipulation — a plain copy |
| `fsgnjn.s` | `F_BIN_TYPE_F_S` | 2 | 2 | bit manipulation — sign splice |
| `fsgnjn.d` | `F_BIN_F_TYPE_D` | 2 | 2 | bit manipulation — sign splice |
| `fli.s` | `FLI_S` | 2 | 2 | bit manipulation — Zfa constant table |
| `fli.d` | `FLI_D` | 2 | 2 | bit manipulation — Zfa constant table |
| `fsw` | `STORE_FP` | 3 | 2 | bit manipulation — in a REDUCED unit only |
| `flw` | `LOAD_FP` | 1 | 1 | bit manipulation — in a REDUCED unit only |
| `c.fsdsp` | `C_FSDSP` | 3 | 2 | bit manipulation — in a REDUCED unit only |
| `c.fldsp` | `C_FLDSP` | 1 | 1 | bit manipulation — in a REDUCED unit only |

Thirty-three distinct float arch-opcodes: **23 to an emulation, 10 to bit
manipulation, none failed.**

## Rounding mode 0, not 1

`../emulations/` is emitted at rounding mode 1 (RTZ). The c arch-units carry
`dyn`, which reads `frm`; `frm` is 0 (round to nearest, ties to even) on a
fresh hart, and the go arch-units name `rne` outright. The host rounds the
same way. So `emul_rm0/` here is the **rounding-mode-0** emission of the same
67 operations, from the same flattened IR by the same emitter — the only thing
that changes is which slice of `../flattened/` is read.

## The one reduction: `&a`

Four arch-units are `&a` — c on `float` and `double`, go on `float32` and
`float64`. Their answer is an **address**, which is not a function of the
operand bits:

```
c   c.addi sp, -0x10 | c.addi4spn a0, sp, 0xc | fsw fa0, 0xc(sp) | ...
go  ... | jal ra, <runtime.newobject> | c.lwsp t0, 0x28(sp) | sw t0, 0x0(a0) | ...
```

The blocking arch-opcode is named in `arch_units.json` per unit:
`c.addi4spn a0, sp, 0xc` for c, `jal ra, <runtime.newobject>` for go. What IS
emulated and verified for these four is the **stated reduction `*(&a)`** — the
bit pattern the float store/load arch-opcode moves — and the reference is the
same reduction in the same language. The reduction is written into the head of
each of the sixteen source files and into `arch_units.json`
(`"reduced": true`).

## Verified against the ORIGINAL compiler-operator, not against SoftFloat

For each arch-unit the reference is its own `expression` and operand types from
`attest_rv.json`, written as a native function **in the arch-unit's own
language** and compiled for the **host** at `-O2`: c for the 150 c units, go
for the 24 go units. No `-ffast-math`, no contraction, no oracle library.

| | |
|---|---|
| inputs per arch-unit | 300,050 – 302,500 |
| inputs per language | **52,478,900** |
| comparisons against the native operator | **209,915,600** |
| **mismatches** | **0** |
| cross-language comparisons (c++/rust/go against c, byte for byte) | **157,436,700** |
| **cross-language mismatches** | **0** |
| NaN-divergent, reported apart (see below) | 94,744 per language |

Inputs per operand: every edge value — ±0, ±inf, quiet and signalling NaN,
largest and smallest normal, largest and smallest subnormal, ±1, ±2, ±0.5, and
one ulp either side of each — crossed over every operand; for an integer
operand 0, 1, the extremes, and the powers of two either side of every
significant bit. Then 200,000 uniform random bit patterns per operand, then
100,000 with the exponent banded around the bias so subnormals, the rounding
path and overflow are actually reached. All six programs draw the identical
sequence from the same xorshift64 seed in the same order.

## The NaN divergence, which is real and is not a bug

94,744 inputs per language answer differently from the native host operator.
**On every one of them both answers are a NaN of the result type, and they
differ only in sign and payload.** Two examples straight out of the run:

```
arch-unit  6  c  ++a        a = 0x7f800001                 native 0x7fc00001  emul 0x7fc00000
arch-unit 26  c  a + b      a = 0x0, b = 0x7ff0000000000001  native 0x7ff8000000000001  emul 0x7ff8000000000000
arch-unit 154 go a * b      a = 0x0, b = 0x7f800000        native 0xffc00000  emul 0x7fc00000
```

- **C leaves it open.** C23 Annex F / IEEE 754-2019 §6.2 do not specify the sign
  or the payload of a NaN result. Go says the same.
- **RISC-V pins one answer.** Every float instruction that produces a NaN
  returns the *canonical* quiet NaN, `0x7fc00000` / `0x7ff8000000000000`.
- **x86-64 SSE pins a different one.** `addss`/`mulsd`/… propagate the first
  NaN operand with its payload, quieted; an invalid operation with no NaN input
  returns the *negative* "real indefinite", `0xffc00000`.

Setting the NaN payload aside, the count of differences is **0**. The
divergence reaches **92 of the 174** — the 88 `+ - * /` units and the 4
`++a` / `--a` units.

## No float, checked at the machine level

`scripts/nofloat_probe.py` disassembles everything that was actually compiled
and reports every distinct host instruction in it.

| language | objects | distinct host instructions | float instructions | float register references |
|---|---:|---:|---:|---:|
| c | 241 | 68 | **0** | **0** |
| c++ | 241 | 67 | **0** | **0** |
| rust | 2 rlibs | 61 | **0** | **0** |
| go | 179 symbols | 72 | **0** | **0** |

---

# Layer 2 — the 318 integer-only arch-units

Every `LIFTED` arch-unit whose body contains no float instruction: **235 c,
83 go, 27 distinct operators**. The bodies are short — 33 are one arch-opcode,
189 two, 52 three, and a tail out to 24 (go's guarded `/`, `%`, `<<`, `>>`).

| | |
|---|---|
| arch-units | 318 (235 c, 83 go) |
| emulated as a bit function of the operands | 313 |
| emulated under a stated reduction | 5 (`&a`) |
| carrying a second `_trap` predicate | 18 (go's guarded arch-units) |
| failed | 0 |
| lines of source | 7,686 c · 8,322 c++ · 7,032 rust · 6,714 go |

## How an arch-opcode is mapped

Each of the 1,119 arch-opcode occurrences goes one of five ways.

- **arithmetic, logic, compare, shift** → the target language's own integer
  operator, over `uint64` locals threaded in SSA order. The **word-width
  forms** (`addw`, `subw`, `addiw`, `mulw`, `sraw`, `c.addw`, `c.subw`,
  `c.addiw`, `divw`, `remw`) are written out as *operate on the low 32 bits,
  then sign-extend into 64*, which is what RV64 does and is the usual source
  of error. Every shift count is masked to the 6 bits (5 for the word forms)
  RISC-V actually uses **before** it reaches a `<<` or `>>`, so no shift in
  the emitted source is ever undefined in C or C++.
- **divide and remainder** → a written-out **restoring long division**
  (`au_divrem_u`, 64 steps). No `/` and no `%` of the host language appears
  anywhere in the emitted code. RISC-V's `div`/`divu`/`rem`/`remu` do not
  trap: `b == 0` gives an all-ones quotient and the dividend back as the
  remainder, and the signed most-negative over minus one gives the
  most-negative back with a zero remainder. All four languages' own `/`
  differ, and three of them have no defined answer at all for those inputs.
- **go's stack-growth prologue** (`ld t1, <bound>(s11)` · `bltu t1, sp, <entry>`
  · spill · `jal t0, runtime.morestack_noctxt` · reload ·
  `jal zero, <this function>`) → **elided**: it re-enters the function at its
  real entry with the same arguments, so it cannot change the answer.
- **frame bookkeeping** (`sd`/`c.sdsp`/`c.ldsp` of `ra`, `sp` adjustment,
  `c.nop`) → **elided**.
- **a guard branch to a runtime panic** (`beq b, zero → runtime.panicdivide`,
  `blt b, zero → runtime.panicshift`) → a **second function** per arch-unit,
  `<name>_trap`, that is 1 exactly when the arch-unit takes the branch. It is
  checked against go's own panic, observed with `recover()`.

### The integer arch-opcodes across the 318

Fifty-five distinct arch-opcodes, 1,119 occurrences, **none failed**.

| arch-opcode | occurrences | arch-units | role | mapped to |
|---|---:|---:|---|---|
| `c.jr` | 235 | 235 | integer | return |
| `jalr` | 83 | 83 | integer | return |
| `jal` | 66 | 22 | prologue / trap-tail / address | stack-growth call and restart, the panic tail, and (in a REDUCED unit) `runtime.newobject` |
| `sltu` | 49 | 40 | integer | `operator:<` unsigned |
| `c.addi` | 48 | 25 | integer / frame / address | `operator:+`; frame or stack-address when the destination is `sp` |
| `c.ldsp` | 48 | 22 | frame / prologue / memory | elided; the load the reduction `*(&a)` reads |
| `c.sdsp` | 48 | 22 | frame / prologue / memory | elided; the store the reduction `*(&a)` reads |
| `sltiu` | 47 | 47 | integer | `operator:<` unsigned |
| `c.and` | 37 | 37 | integer | `operator:&` |
| `c.xor` | 37 | 37 | integer | `operator:^` |
| `c.or` | 36 | 36 | integer | `operator:\|` |
| `c.li` | 29 | 29 | integer | constant |
| `sub` | 26 | 26 | integer | `operator:-` |
| `sd` | 24 | 22 | frame / memory | elided; the store the reduction reads |
| `bltu` | 22 | 22 | prologue | the stack-growth check — elided |
| `ld` | 22 | 22 | prologue / memory | the stack bound — elided |
| `addiw` | 20 | 14 | integer | `operator:+` then sign-extend the low 32 bits |
| `c.nop` | 18 | 18 | trap-tail | part of the panic tail |
| `c.add` | 16 | 16 | integer | `operator:+` |
| `c.sub` | 16 | 16 | integer | `operator:-` |
| `c.lwsp` | 16 | 11 | prologue / memory | elided; the load the reduction reads |
| `c.swsp` | 16 | 11 | prologue / memory | elided; the store the reduction reads |
| `and` | 15 | 15 | integer | `operator:&` |
| `blt` | 12 | 12 | guard | → the `_trap` predicate (`runtime.panicshift`) |
| `sll` | 9 | 9 | integer | `operator:<<`, count masked to 6 bits |
| `xori` | 9 | 9 | integer | `operator:^` |
| `c.addi16sp` | 8 | 4 | address | frame adjustment in a REDUCED unit |
| `slt` | 8 | 8 | integer | `operator:<` signed |
| `divu` | 7 | 7 | integer | written-out restoring division |
| `remu` | 7 | 7 | integer | written-out restoring division |
| `beq` | 6 | 6 | guard | → the `_trap` predicate (`runtime.panicdivide`) |
| `czero.eqz` | 6 | 6 | integer | conditional select |
| `or` | 6 | 6 | integer | `operator:\|` |
| `slli` | 6 | 6 | integer | `operator:<<` |
| `srli` | 6 | 6 | integer | `operator:>>` unsigned |
| `addi` | 5 | 5 | integer / address | `operator:+`; a stack address in a REDUCED unit |
| `div` | 5 | 5 | integer | written-out restoring division |
| `rem` | 5 | 5 | integer | written-out restoring division |
| `auipc` | 4 | 4 | address | the go type descriptor, in a REDUCED unit only |
| `sb` | 4 | 2 | memory | the store the reduction reads |
| `c.addw` | 3 | 3 | integer | `operator:+` then sign-extend the low 32 bits |
| `c.subw` | 3 | 3 | integer | `operator:-` then sign-extend the low 32 bits |
| `divw` | 3 | 3 | integer | written-out restoring division, 32-bit form |
| `remw` | 3 | 3 | integer | written-out restoring division, 32-bit form |
| `sra` | 3 | 3 | integer | arithmetic right shift, written out in unsigned bit operations |
| `sraw` | 3 | 3 | integer | the same on the low 32 bits, then sign-extended |
| `srl` | 3 | 3 | integer | `operator:>>` unsigned, count masked to 6 bits |
| `c.addiw` | 2 | 2 | integer | `operator:+` then sign-extend the low 32 bits |
| `mul` | 2 | 2 | integer | `operator:*` |
| `mulw` | 2 | 2 | integer | `operator:*` then sign-extend the low 32 bits |
| `c.mv` | 1 | 1 | integer | register move |
| `lb` | 1 | 1 | memory | the load the reduction reads |
| `lbu` | 1 | 1 | memory | the load the reduction reads |
| `subw` | 1 | 1 | integer | `operator:-` then sign-extend the low 32 bits |
| `sw` | 1 | 1 | memory | the store the reduction reads |

The whole integer arch-opcode vocabulary lives in
`{c,cpp,rust,go}/au_int.{h,hpp,rs}` / `go/helpers_int.go` — one small function
per arch-opcode, identical in all four languages.

## What the answer is

The emulation answers **the result type's own bit pattern, zero-extended into
a `uint64`** — 1 bit for a boolean result, 32 for a 32-bit one, 64 otherwise.
The C reference takes the result type **from the C compiler itself** with
`__typeof__`, exactly as the corpus's own probe did
(`__typeof__(~(float){0})`), so nothing about C's usual arithmetic conversions
is assumed anywhere. Go's result type is read off the operator.

## Verified against the ORIGINAL compiler-operator

For each arch-unit the reference is its own `expression` and operand types,
written as a native function **in the arch-unit's own language** and compiled
for the **host** at `-O2`: c for the 235 c units, go for the 83 go units.

| | |
|---|---|
| inputs per arch-unit | 300,002 – 307,056 |
| inputs per language | **96,363,378** |
| comparisons against the native operator | **379,402,096** |
| of which value comparisons | 372,099,944 |
| of which trap comparisons (the `_trap` predicate against go's own panic) | 7,302,152 |
| **mismatches** | **0** |
| inputs excluded because the C reference is undefined | 6,051,416 (1,512,854 per language) |
| cross-language comparisons (c++/rust/go against c, byte for byte) | **289,090,134** |
| **cross-language mismatches** | **0** |

Inputs per operand: every edge value — zero, one, minus one, the signed and
unsigned extremes, the value just inside and just outside every bit boundary,
and the shift amounts at and either side of both widths (31/32/33, 63/64/65)
and beyond, together with their negations — crossed over every operand; then
200,000 uniform random bit patterns per operand; then 100,000 drawn in eight
bands — zero, all-ones, the sign bit, a shift count in [0,130), a power of two
±1, a small value, a value just below all-ones, and a plain uniform draw — so
**divisors of zero, shift counts at and above the width, and the most-negative
over minus one are all reached repeatedly**. All six programs draw the
identical sequence from the same xorshift64 seed in the same order.

## Six genuine divergences, all real and none hidden

**1. C leaves division undefined where RISC-V defines it.** 32 arch-units
(c's `/` and `%`). RISC-V does not trap; C 6.5.5p5 leaves both a zero divisor
and the signed most-negative over minus one undefined, and the host *faults*
on both, so the native reference has no answer at all. The emulation writes
the RISC-V answer out explicitly in all four languages; the reference flags
those inputs, they are excluded from the comparison against the native
operator (**1,512,854 per language**) and counted apart, and they are still
compared across the four languages, where they agree exactly.

**2. clang folds `a / (bool)b` to the identity.** 8 arch-units. A `_Bool` is
0 or 1 and dividing by 0 is undefined, so clang concludes `b == 1` and emits
*nothing at all* for `a / b` (`c.jr ra`) and a constant 0 for `a % b`. The
arch-unit is therefore not the RISC-V `div` instruction: at `b == 0` it
answers `a`, where a raw `div` would answer all-ones. Emulated exactly as the
arch-unit is.

**3. go panics where RISC-V does not.** 18 arch-units. go's `/` and `%` panic
on a zero divisor and its shifts panic on a negative count; the compiler wraps
the arch-opcode in a guard branch to `runtime.panicdivide` /
`runtime.panicshift`. Each of these is emitted as two functions — the
fall-through value and a `_trap` predicate — and the go reference observes the
real panic with `recover()` rather than assuming the condition.
**7,302,152 trap comparisons, 0 disagreements.**

**4. A RISC-V shift is not a go shift, and is undefined in C.** 18 arch-units.
`sll`/`srl`/`sra` use the low 6 bits of the count (`sraw` the low 5), so a
count of 64 shifts by 0. go defines a shift at or above the width as zero, or
a full sign fill for an arithmetic right shift. C and C++ leave it undefined
outright (C 6.5.7p3). The three do not agree — which is exactly why each of
these arch-units is four or more arch-opcodes rather than one. The
`sltiu`/mask idiom the compiler emitted is composed as written, and every
shift count in the emitted source is masked first, so nothing in any of the
four languages is ever undefined. (There are no c shift arch-units in the
population.)

**5. go leaves a 32-bit answer non-canonical in the register.** 6 arch-units,
**measured, not assumed**, by `scripts/probe_answer_width.py`, which recomposes
every arch-unit with the final mask removed:

| arch-unit | go expression | body | non-canonical inputs |
|---|---|---|---:|
| `au_414_go_neg_i32` | `-a` on `int32` | `sub a0, zero, a0` | 12,716 / 300,066 |
| `au_434_go_shl_i32_i32` | `a << b` | `... and a0, t0, t1` | 6,451 / 304,356 |
| `au_435_go_shl_i32_i64` | `a << b` | `... and a0, t0, t1` | 6,019 / 305,544 |
| `au_436_go_shl_i32_u64` | `a << b` | `sll · sltiu · sub · and` | 6,019 / 305,544 |
| `au_458_go_add_i32_i32` | `a + b` | `c.add a0, a1` | 60,436 / 304,356 |
| `au_461_go_sub_i32_i32` | `a - b` | `c.sub a0, a1` | 63,355 / 304,356 |

The RISC-V psABI wants a 32-bit value sign-extended into the register, and
clang does it — c's `-a` on `int32_t` is `subw a0, zero, a0`. go's register
ABI does not require it of a *result*: go emits plain `sub`/`c.add`/`c.sub`
and leaves the bits above 32 as they fall. **All 141 arch-units with a narrow
result were probed; only these 6 are non-canonical, and every one of them is
go with an `int32` result.** This is why the comparison is made at the
result's own width.

**6. `&a` answers an address.** 5 arch-units (c on `bool`, go on `int32`,
`int64`, `uint64`, `bool`). The answer is the address of a stack slot or a
heap cell from `runtime.newobject`, which is not a function of the operand
bits. Emulated and verified under the stated reduction `*(&a)`, with the same
reduction as the reference — as in the float layer. The blocking arch-opcode
is named per unit in `arch_units.json`: `addi a0, sp, 0xf` for c,
`jal ra, <runtime.newobject>` for go.

Signed overflow in `+`, `-`, `*`, `++` and `--` is also undefined in C, and
those inputs *are* in the stream. They are not excluded: the host compiler
wrapped on every one of them and the emulation agreed, so they are reported as
observed agreement over undefined behaviour, not as a verified claim.

---

# The 770 rows with no arch-unit here

## 737 `BUILDFAIL` — there is no arch-unit

The probe source did not compile for riscv64 at all, so no body was ever
produced. **The compiler-operator does not exist** in that language on those
operand types; there is nothing to decompose and nothing to emulate. All 737
also have no x86 body in the corpus's store, so the two builds agree exactly
on which probes are refused.

**637 go, 100 c.** The reasons, from the compilers' own diagnostics:

| what the compiler said | rows |
|---|---:|
| go: `mismatched types` — go has no implicit conversions, so `int32 + int64`, `uint64 & int32` and every other unequal pair is simply not an operator | 510 |
| go: `shifted operand a … must be integer` / `shift count b … must be integer` — `<<` and `>>` on or by `float32`, `float64`, `bool` | 54 |
| go: `operator … not defined on a` — `^`, `&&`, `\|\|`, `!`, `+`, `-`, `%`, `&^` on a type that does not have them | 43 |
| go: `unexpected ++ / -- / ... at end of statement` — in go these are statements, not expressions | 18 |
| go: `<-` on a non-channel | 6 |
| go: other `invalid operation` | 6 |
| **go total** | **637** |
| c: `invalid operands to binary expression` — `%`, `\|`, `^`, `&`, `*` with a `float` or `double` operand | 80 |
| c: `call to undeclared function 'alignof' / '_alignof'` — those spellings are not C | 12 |
| c: `indirection requires pointer operand` — unary `*a` on a scalar | 6 |
| c: `invalid argument type 'float' to unary expression` — `~` on a float | 2 |
| **c total** | **100** |

## 33 `WALK_REFUSED` — a body, but the walker's table is short

These compiled and a body **was** carved. What failed is the RISC-V reference
walker: it has no entry in its opcode table for one arch-opcode in the body, so
task rv2 would not call the body lifted. So they are not "not emulable" — the
body is right there — they are **outside the attested `LIFTED` population**.

| missing from the walker's table | rows | what it is |
|---|---:|---|
| `c.mul a0, a1` | 8 | c's `*` on the 64-bit type pairs — the compressed `mul` |
| `andn a0, a0, a1` | 8 | c's `&&` with a `float` / `double` operand — Zbb and-not |
| `c.not a0` | 4 | c's `~` — the compressed one's-complement |
| `c.addi4spn a0, sp, N` | 5 | c's `&a` — a stack address |
| `fsgnjn.s` / `fsgnjn.d` | 4 | c's and go's `-a` on a float — the sign splice |
| `fli.s` / `fli.d` | 4 | c's `++a` / `--a` on a float — the Zfa constant table |

**18 of the 33 contain a float instruction and are already emulated** in the
float layer, which selected on "has a body" rather than on the outcome. The
other **15** (`c.mul` ×8, `c.not` ×4, `c.addi4spn` ×3) are not emitted here.

---

# These are TESTED, not PROVED

Nothing here is a proof and no prover has seen it. The chain is
compiler-operator → arch-unit → arch-opcodes → emulation, and every link is
established by differential testing on the host, not by derivation. In
particular:

- the mapping from a float arch-opcode to a SoftFloat operation is read off
  Sail's own clause list (`float_clauses.json`); it has not been checked
  against Sail's definition of the instruction.
- the mapping from an **integer** arch-opcode to the language's operator is
  read off the RISC-V unprivileged spec by hand, not off Sail. What
  establishes it is the 379,402,096 comparisons against the native operator,
  not a derivation.
- the go **stack-growth prologue and frame bookkeeping are elided by argument**
  — the prologue re-enters the function with the same arguments, the frame
  slots are never read back into the answer — not by a memory model. Nothing
  in the population contradicts it, but it is an argument, not a proof.
- the emulations under `emul_rm0/` are verified at rounding mode 0 only by the
  comparisons against the native operator, not against SoftFloat.
- the nine `&a` units are emulated only under the stated reduction.

# Files

| | |
|---|---|
| `c/` `cpp/` `rust/` `go/` | one source file per arch-unit (492 each), plus the module wiring |
| `c/au_int.h` `cpp/au_int.hpp` `rust/au_int.rs` `go/helpers_int.go` | the RV64 integer arch-opcode vocabulary, one function per arch-opcode |
| `c/arch_units.h` `cpp/arch_units.hpp` `rust/lib.rs` | the float layer's declarations |
| `c/arch_units_int.h` `cpp/arch_units_int.hpp` `rust/lib_int.rs` | the integer layer's declarations |
| `emul_rm0/` | the 67 SoftFloat operations as integer source at RNE, in all four languages |
| `arch_units.json` | all 492: per (arch-unit, language) the source file, the arch-opcodes it was composed from with what each mapped to, inputs tested, mismatches, cross-language mismatches; plus both layers' totals, the divergences, and the census of the 770 rows with no arch-unit |
| `_units.json` `_index.json` `_nofloat.json` | the float builder's and probe's own records |
| `_units_int.json` `_index_int.json` `_answer_width.json` | the integer builder's and probe's own records |

Entry points:

```
c/au_000_c_not_f32.c            uint64_t au_000_c_not_f32(uint64_t)
cpp/au_000_c_not_f32.cpp        archunits::au_000_c_not_f32
rust/au_000_c_not_f32.rs        archunits::au_000_c_not_f32::au_000_c_not_f32
go/au_000_c_not_f32.go          archunits.Au_000_c_not_f32

c/au_443_go_shr_i32_i32.c       uint64_t au_443_go_shr_i32_i32(uint64_t, uint64_t)
                                uint64_t au_443_go_shr_i32_i32_trap(uint64_t, uint64_t)
```

# Re-running

```sh
cd Research/oracle/riscv/softfloat_slices

# --- layer 1, the float arch-units ---
EMUL_OUT=arch_units/emul_rm0 python3 scripts/emit_emulations.py 0 value
cp emulations/c/sfemul.h     arch_units/emul_rm0/c/
cp emulations/cpp/sfemul.hpp arch_units/emul_rm0/cpp/
cp emulations/rust/helpers.rs arch_units/emul_rm0/rust/
cp emulations/go/helpers.go   arch_units/emul_rm0/go/
python3 scripts/build_arch_units.py       # compose the 174 x 4 sources
python3 scripts/verify_arch_units.py      # build the 6 programs, run them
python3 scripts/nofloat_probe.py          # machine-level no-float attestation
python3 scripts/report_arch_units.py      # writes arch_units.json (float only)

# --- layer 2, the integer arch-units ---
python3 scripts/build_arch_units_int.py   # compose the 318 x 4 sources
python3 scripts/verify_arch_units_int.py  # build the 6 programs, run them
python3 scripts/probe_answer_width.py     # the answer-register probe
python3 scripts/report_arch_units_int.py  # merges BOTH layers into arch_units.json
```

`report_arch_units_int.py` reads the float layer's records back out of
`arch_units.json` and carries them across untouched, so it must run after
`report_arch_units.py`; it is idempotent and can be re-run on its own output.
Both verifiers read `NRAND`, `NBAND` and `AU_ONLY` from the environment for a
quicker pass, and `AU_SCRATCH` for where to build. Everything they write goes
to the scratch directory; `SOURCES` is never touched, and nothing
outside `arch_units/` and `scripts/` is written.

Toolchains: clang 21.1.8, clang++ 21.1.8, rustc 1.96.1, go 1.26.0, x86-64.
This is emulation testing, not lowering, so nothing is cross-compiled.
