# log 293 — below Sail: GMP, SoftFloat, and the float gap sized

2026-09-16, early. the owner's question, over a long exchange: what actually
defines a RISC-V instruction, how far down does it go, and can the logic
be extracted by machine rather than by a person. This log is the answer,
measured. Every rendering is LITERAL (quoted, with its path) or GLOSS.

## 1. In plain words, first

An arch-opcode is a RISC-V instruction. Sail states what it computes and
stops there. Sail contains no gates and no algorithm: every arithmetic
primitive is a name handed to a backend. Follow the C backend down and
you land in GMP, a big-number library. Follow the float instructions
down and you land in Berkeley SoftFloat, which is already inside the
model's own tree. Both are written in ordinary integer C. So the logic
of every arch-opcode is recoverable by compiling that C and reading it
back through Sail's own decoder, with no person typing anything.

That last step is the pipeline this line already has. The float half of
it needs four pieces of walker engineering and no new theory.

### 1.1 What this log came to hold

It was opened to size the float gap and grew as the gap closed. The
chain, each link measured and each with its own section:

| | section | state |
|---|---|---|
| Sail contains no gates; its arithmetic is a name handed to a backend | 2 | |
| the C backend lands in GMP; the complete path for one instruction, eleven files | 3 | |
| the floats land in Berkeley SoftFloat, inside the model's own tree | 4 | |
| SoftFloat compiled for riscv64 and measured: zero loops anywhere | 5 | |
| each operation sliced to its minimum, all 67 | 6.1, 6.2 | |
| each flattened to ONE branch-free block, verified on 411 M evaluations | 6.3 | |
| a float operation as a Lean expression, by Sail's own definitions | 6.4 | 21 of 43 |
| the 67 operations as source in c, c++, rust, go, 82 M comparisons | 6.5 | 67 of 67 |
| the 174 float ARCH-UNITS emulated across four languages | 6.6 | 174 of 174 |
| the per-arm fix: one clause, `lui` no longer blocks anything | 6.7 | done |
| the remaining 318 arch-units, so every readable one is covered | 6.8 | 474 of 474 |

**The headline.** Every readable RISC-V arch-unit, float and integer, is
emulated in c, c++, rust and go, checked against its own language's
operator and against the other three, with no mismatch in 1.03 billion
comparisons. Six genuine cross-language divergences were found and are
named in 6.8.1; they are places where the same operator legitimately
means different things.

**What this is NOT.** None of it is proved. The emulations are
established by testing against the implementation the Sail C simulator
itself links, and Sail has no clause for a float operation to prove them
against. The proof direction is section 6.4 and it stands at 21 of 43,
blocked now on term size rather than on anything about floats.

## 2. Sail has no gates. What it has instead

**LITERAL**, Sail's declaration of bit-vector addition, from the library
copied out of the tower's `lp3-runner` (sail 0.20.2):

```
val add_bits = pure {
  ocaml: "add_vec", lem: "add_vec", coq: "add_vec",
  lean: "_lean_add", _: "add_bits"
} : forall 'n. (bits('n), bits('n)) -> bits('n)
```

**LITERAL**, what the C backend does with it, from the same library's
`sail.c`:

```c
void and_bits(lbits *rop, const lbits op1, const lbits op2)
{ rop->len = op1.len; mpz_and(*rop->bits, *op1.bits, *op2.bits); }

void add_bits(lbits *rop, const lbits op1, const lbits op2)
{ rop->len = op1.len; mpz_add(*rop->bits, *op1.bits, *op2.bits); }
```

**GLOSS.** A name and a table of spellings. No carry chain exists
anywhere in Sail. `mpz_` is GMP. Two typedefs decide everything:

```c
typedef mpz_t sail_int;     // Sail's `int` IS a GMP heap big-integer
typedef uint64_t fbits;     // fixed-width bits get a machine word
```

So anything routed through Sail's unbounded `int` goes to GMP, and that
is divide, remainder, multiply-high and the sign-extension arithmetic.
Anything staying in `bits(n)` compiles small. The primitive inventory
itself is log 291.

## 3. GMP, fetched and measured

GMP was nowhere on this machine. It is now at
`SOURCES/gmp`, version 6.3.0, with `FETCHED.txt` carrying
the URL, the sha256 `a3c2b8...538898`, and why it is there. 22 MB, 863 C
files, 921 assembly files.

### 3.1 The operators it uses

Tokenised over its portable C path, 189 files (`mpn/generic/*.c` plus
`longlong.h`), comments and string literals stripped: **36 distinct
operator tokens, every one standard C.**

| group | tokens |
|---|---|
| arithmetic | `+ - * / %` |
| bitwise | `& \| ^ ~ << >>` |
| comparison | `== != < > <= >=` |
| logical | `&& \|\| !` |
| conditional | `? :` |
| assignment and step | `= += -= *= /= %= &= \|= ^= <<= >>= ++ --` |
| member | `->` |

Nothing exotic. No intrinsic, no builtin, no wide type. The two places
people expect magic are plain C: the 64×64→128 multiply splits each
operand into halves and does four half-multiplies, three adds and a
carry test; the 128÷64 divide does two rounds of schoolbook long
division with a compare-and-fix-up loop.

### 3.2 The complete path for one arch-opcode

`DIV`, every file named. Sail's runtime calls 72 GMP entry points in
total, across printing, rationals and string parsing; **one instruction
reaches eleven files.**

```
execute DIV                            model/extensions/M/mext_insts.sail:53

├─ signed(rs1), signed(rs2)            sail.c  sail_signed
│    ├─ mpz_set                        mpz/set.c
│    ├─ mpz_tstbit                     mpz/tstbit.c
│    ├─ mpz_set_ui                     mpz/set_ui.c
│    ├─ mpz_mul_2exp                   mpz/mul_2exp.c
│    ├─ mpz_combit                     mpz/combit.c
│    └─ mpz_sub                        mpz/aors.h
│
├─ quot_round_zero                     sail.c  tdiv_int
│    └─ mpz_tdiv_q                     mpz/tdiv_q.c
│         └─ mpn_div_q                 mpn/generic/div_q.c     dn == 1
│              └─ mpn_divrem_1         mpn/generic/divrem_1.c
│                   └─ udiv_qrnnd      longlong.h:2203
│                        = __udiv_qrnnd_c   longlong.h:2147
│
└─ to_bits_truncate                    sail.c  get_slice_int
     ├─ mpz_get_ui                     gmp.h macro
     ├─ mpz_set_ui                     mpz/set_ui.c
     ├─ mpz_tstbit                     mpz/tstbit.c
     └─ mpz_setbit                     mpz/setbit.c
```

**LITERAL**, `longlong.h:2200`: *"If udiv_qrnnd was not defined for this
processor, use `__udiv_qrnnd_c`."* RISC-V has no `udiv_qrnnd`; its only
entry in that file is a wide multiply using `mulhu`. **So on RISC-V,
GMP's divide is pure C and never reaches a divide instruction.**

The 18 rational files in that 72 are dead for RISC-V: the model never
uses Sail's `real` type, and every occurrence of the word in the model
is in an English comment.

### 3.3 Why GMP is the wrong source for divide

It is circular. `__udiv_qrnnd_c` computes `__q1 = n1 / __d1` on 64-bit
words. Compile that for RISC-V and `divu` comes back, so tracing GMP
defines `DIV` in terms of `DIV`.

The escape is measured. Compiling `a / b` for riscv64:

| target | result |
|---|---|
| `-march=rv64im` | `divu a0, a0, a1 ; ret` — one instruction |
| `-march=rv64i` | a call to `__udivdi3` — the instruction does not exist |

And a shift-and-subtract divide, written with no `/` or `%`, compiled
for `rv64i`, is **20 instructions with zero divide or multiply**. The
compiler even made it branchless: `sltu` then `addi -1` builds an
all-ones or all-zeros mask and the subtract and bit-set are masked by
it, leaving only the loop back-edge as a branch.

That construction is the one the owner ruled sufficient on 2026-09-10, and
`build.py` carries the ruling verbatim: "A language with `& | ^ ~`, a
conditional and variables has every gate a processor is built from, so
every opcode's mapping is constructible from them, as a GUARANTEE."

## 4. The float gap: the definition exists, and it is in the tree

GMP is the wrong place to look for floats. `mpf` is GMP's own format,
not IEEE 754. The thing that actually defines RISC-V floats is **Berkeley
SoftFloat**, vendored at
`SOURCES/sail-riscv/dependencies/softfloat/berkeley-softfloat-3/`.
It is what the C simulator links, and it is pure integer C.

**LITERAL**, the opening of `source/f64_div.c`:

```c
signZ = signA ^ signB;
if ( expA == 0x7FF ) { if ( sigA ) goto propagateNaN; ... }
```

No floating-point arithmetic. Sign, exponent and fraction pulled out of
the bit pattern with shifts and masks, then integer work.

So the largest hole in the Lean path has a complete definition on disk,
inside the model's own dependencies, from the authority the simulator
already trusts.

## 5. SoftFloat measured for riscv64

Compiled with the model's own build settings
(`build/Linux-RISCV64-GCC`), `-march=rv64im -O2`. **67 of 67 externals
compiled**, plus 28 internal helpers they reach: 95 functions, 6,490
instructions.

| operation | instructions | branches | back-edges | calls | loads+stores | mul/div |
|---|---|---|---|---|---|---|
| `f64_add` | 8 | 1 | 0 | 2 | 0 | 0 |
| `f64_mul` | 111 | 12 | 0 | 5 | 28 | 2 |
| `f64_div` | 150 | 13 | 0 | 6 | 28 | 7 |
| `f64_sqrt` | 107 | 9 | 0 | 5 | 20 | 4 |
| `f32_div` | 101 | 13 | 0 | 6 | 12 | 2 |
| `f32_mul` | 97 | 12 | 0 | 5 | 10 | 1 |
| `f64_le` | 36 | 5 | 0 | 1 | 2 | 0 |
| `f32_to_f64` | 56 | 5 | 0 | 2 | 6 | 0 |
| `f64_to_i64` | 62 | 5 | 0 | 2 | 12 | 0 |

**The headline: zero loops, in all 95 functions.** Eight have a backward
branch target, but none closes a cycle; every one jumps to a shared
epilogue the compiler laid out early. The detector was checked against a
control case with a real `while` loop and fired correctly.

That matters because a data-dependent loop is the only thing that forces
a symbolic walker to fork and the only thing that needs an induction
proof. There are none here.

Distribution over the 95: 372 branches, 126 calls, 324 loads and stores,
36 multiply or divide. 65 of the 67 externals make calls; only
`i32_to_f64` and `ui32_to_f64` are leaves. 56 touch memory, 11 are
register-only. The round-to-integer family dispatches through a 7-entry
jump table on the rounding mode, the only computed jumps.

### 5.1 Why `-march=rv64i` is a trap for this work

Compiling the float set for the base integer target grows the total by
only three percent, which looks free. It is not. The 36 multiplies and
divides become calls to library routines (`__muldi3`, `__udivdi3`) whose
bodies are outside SoftFloat and were not measured — and those routines
are the shift-and-add and shift-and-subtract loops, the one thing in
this area that needs induction. Compile the float work for `rv64im`,
where multiply and divide are single instructions Sail already defines,
and no loop ever appears.

## 6. The slice, and how to cut it

Summing separate function bodies is an upper bound, not a slice: it
counts every instruction in each helper, including paths the caller can
never reach. The true slice is produced by inlining and dead-code
elimination, and all the tools are on the laptop:

```
clang --target=riscv64-unknown-elf -march=rv64im -O1 <defines> <includes> \
      -emit-llvm -c <source>.c -o <source>.bc          # per source
llvm-link *.bc -o linked.bc
opt -passes='internalize,always-inline,inline,globaldce,instcombine,simplifycfg,dce,globaldce' \
    -internalize-public-api-list=<operation> linked.bc -o slice.bc
llc -march=riscv64 -mattr=+m -O2 -filetype=obj slice.bc -o slice.o
```

On `f64_div` this leaves **one symbol and no calls at all**:

| `f64_div` | instructions |
|---|---|
| own body, helpers left as calls | 150 |
| upper bound, helper bodies in full | 336 |
| **true slice, inlined and dead code cut** | **302** |

The slice is larger than the own-body figure because inlining pulls the
helpers in, which is the honest size of the logic rather than an
artifact of where the source files were split. It is smaller than the
bound because the unreachable arms of the shared helpers are gone.

Slicing removes the second of the four walker blockers outright: a
sliced operation contains no calls, in 61 of 67 cases (§6.1).

### 6.1 Every operation sliced: all 67

All 67 sliced, no failures. `f64_div` reproduced at exactly 302.
`own` is the body compiled alone, `bound` is that plus every transitive
helper's full body, `slice` is what survives inlining and dead-code
elimination. `memory` is loads plus stores. A dot marks an indirect jump.

**arithmetic**

| operation | own | bound | **slice** | branches | calls left | mul/div | memory |
|---|---|---|---|---|---|---|---|
| `f16_add` | 23 | 535 | **373** | 53 | 1 | 2 | 11 |
| `f16_div` | 107 | 293 | **233** | 28 | 0 | 4 | 12 |
| `f16_mul` | 104 | 290 | **235** | 28 | 0 | 3 | 10 |
| `f16_mulAdd` | 16 | 493 | **457** | 54 | 0 | 5 | 15 |
| `f16_sqrt` | 105 | 291 | **221** | 24 | 0 | 7 | 12 |
| `f16_sub` | 23 | 535 | **373** | 53 | 1 | 2 | 11 |
| `f32_add` | 17 | 453 | **299** | 38 | 1 | 2 | 7 |
| `f32_div` | 101 | 276 | **253** | 30 | 0 | 4 | 14 |
| `f32_mul` | 97 | 272 | **243** | 28 | 0 | 3 | 12 |
| `f32_mulAdd` | 13 | 493 | **452** | 55 | 0 | 5 | 13 |
| `f32_sqrt` | 81 | 307 | **236** | 23 | 0 | 9 | 14 |
| `f32_sub` | 17 | 453 | **299** | 38 | 1 | 2 | 7 |
| `f64_add` | 8 | 455 | **317** | 40 | 2 | 2 | 3 |
| `f64_div` | 150 | 336 | **302** | 29 | 0 | 9 | 12 |
| `f64_mul` | 111 | 297 | **254** | 28 | 0 | 4 | 10 |
| `f64_mulAdd` | 3 | 543 | **529** | 61 | 0 | 6 | 15 |
| `f64_sqrt` | 107 | 344 | **260** | 23 | 0 | 11 | 12 |
| `f64_sub` | 8 | 455 | **313** | 39 | 2 | 2 | 3 |

**compare**

| operation | own | bound | **slice** | branches | calls left | mul/div | memory |
|---|---|---|---|---|---|---|---|
| `f16_eq` | 41 | 46 | **38** | 8 | 0 | 0 | 2 |
| `f16_le` | 42 | 47 | **39** | 5 | 0 | 0 | 2 |
| `f16_le_quiet` | 54 | 59 | **51** | 9 | 0 | 0 | 2 |
| `f16_lt` | 40 | 45 | **37** | 5 | 0 | 0 | 2 |
| `f16_lt_quiet` | 52 | 57 | **49** | 9 | 0 | 0 | 2 |
| `f32_eq` | 41 | 46 | **38** | 8 | 0 | 0 | 2 |
| `f32_le` | 41 | 46 | **38** | 5 | 0 | 0 | 2 |
| `f32_le_quiet` | 52 | 57 | **49** | 9 | 0 | 0 | 2 |
| `f32_lt` | 39 | 44 | **36** | 5 | 0 | 0 | 2 |
| `f32_lt_quiet` | 51 | 56 | **48** | 9 | 0 | 0 | 2 |
| `f64_eq` | 43 | 48 | **40** | 8 | 0 | 0 | 2 |
| `f64_le` | 36 | 41 | **33** | 5 | 0 | 0 | 2 |
| `f64_le_quiet` | 50 | 55 | **47** | 9 | 0 | 0 | 2 |
| `f64_lt` | 35 | 40 | **32** | 5 | 0 | 0 | 2 |
| `f64_lt_quiet` | 49 | 54 | **46** | 9 | 0 | 0 | 2 |

**convert**

| operation | own | bound | **slice** | branches | calls left | mul/div | memory |
|---|---|---|---|---|---|---|---|
| `f16_to_f32` | 50 | 99 | **71** | 6 | 0 | 1 | 2 |
| `f16_to_f64` | 55 | 104 | **76** | 7 | 0 | 1 | 2 |
| `f16_to_i32` | 49 | 119 | **85** | 16 | 0 | 0 | 6 |
| `f16_to_i64` | 45 | 115 | **84** | 16 | 0 | 0 | 6 |
| `f16_to_ui32` | 45 | 106 | **71** | 14 | 0 | 0 | 6 |
| `f16_to_ui64` | 46 | 102 | **73** | 17 | 0 | 0 | 6 |
| `f32_to_bf16` | 47 | 166 | **122** | 13 | 0 | 0 | 10 |
| `f32_to_f16` | 46 | 166 | **134** | 17 | 0 | 0 | 10 |
| `f32_to_f64` | 56 | 105 | **78** | 5 | 0 | 1 | 2 |
| `f32_to_i32` | 35 | 105 | **90** | 15 | 0 | 0 | 4 |
| `f32_to_i64` | 64 | 124 | **98** | 19 | 0 | 0 | 6 |
| `f32_to_ui32` | 35 | 96 | **81** | 11 | 0 | 0 | 4 |
| `f32_to_ui64` | 63 | 119 | **90** | 17 | 0 | 0 | 6 |
| `f64_to_f16` | 46 | 166 | **131** | 16 | 0 | 0 | 10 |
| `f64_to_f32` | 41 | 151 | **121** | 16 | 0 | 0 | 10 |
| `f64_to_i32` | 33 | 103 | **88** | 15 | 0 | 0 | 4 |
| `f64_to_i64` | 62 | 122 | **93** | 19 | 0 | 0 | 6 |
| `f64_to_ui32` | 33 | 94 | **79** | 11 | 0 | 0 | 4 |
| `f64_to_ui64` | 61 | 117 | **88** | 18 | 0 | 0 | 6 |
| `i32_to_f16` | 76 | 196 | **134** | 11 | 0 | 1 | 5 |
| `i32_to_f32` | 21 | 196 | **122** | 11 | 0 | 1 | 5 |
| `i32_to_f64` | 47 | 47 | **47** | 1 | 0 | 1 | 0 |
| `i64_to_f16` | 90 | 210 | **148** | 11 | 0 | 1 | 5 |
| `i64_to_f32` | 87 | 197 | **140** | 12 | 0 | 1 | 5 |
| `i64_to_f64` | 15 | 194 | **131** | 10 | 0 | 1 | 5 |
| `ui32_to_f16` | 70 | 190 | **123** | 10 | 0 | 1 | 5 |
| `ui32_to_f32` | 22 | 197 | **136** | 13 | 0 | 1 | 8 |
| `ui32_to_f64` | 41 | 41 | **41** | 1 | 0 | 1 | 0 |
| `ui64_to_f16` | 84 | 204 | **137** | 10 | 0 | 1 | 5 |
| `ui64_to_f32` | 86 | 196 | **130** | 10 | 0 | 1 | 5 |
| `ui64_to_f64` | 15 | 194 | **141** | 12 | 0 | 1 | 8 |

**round to integer**

| operation | own | bound | **slice** | branches | calls left | mul/div | memory |
|---|---|---|---|---|---|---|---|
| `f16_roundToInt` · | 111 | 138 | **114** | 17 | 0 | 0 | 7 |
| `f32_roundToInt` · | 98 | 124 | **99** | 17 | 0 | 0 | 6 |
| `f64_roundToInt` · | 92 | 121 | **103** | 17 | 0 | 0 | 7 |

**Totals over the 67:** slices sum to **9,769 instructions**, against a
12,586 upper bound and a 3,624 own-bodies-only figure. The true slice is
22 percent below the bound and 2.7 times the naive own-body count.
Largest `f64_mulAdd` at 529, smallest `f64_lt` at 32, median 103.

**Zero natural loops**, confirmed a second way: 35 slices contain a
literal backward branch target and a dominator analysis shows none
closes a cycle, agreeing with the separate-compilation measurement of
§5.

Three things the walker still meets:

- **Six operations keep one call**, all of them add or subtract, at 16,
  32 and 64 bits, each to its own rounding helper. After the magnitude
  helpers inline, that helper has two call sites and the cost model
  declines to duplicate it. Forcing it inline gives a call-free body at
  a size cost (`f64_add` 474 rather than 317). These six are also the
  only slices that exceed their upper bound, which is that same genuine
  duplication across two sites, not an error.
- **Three indirect jumps**, the round-to-integer family at 16, 32 and 64
  bits, each one jump through a 6-entry table on the rounding mode.
- **Two lookup tables stay undefined.** Only function definitions were
  linked, so the square-root approximation tables are absent. Linking
  the table source leaves `f64_sqrt` at exactly 260, so the size is
  unaffected, but the walker needs the table contents to have a meaning.

One build note: `f64_sqrt` needs `instcombine<no-verify-fixpoint>`,
because this LLVM build asserts that pass converges in one iteration and
it does not. The variant was checked bit-identical on all 66 others,
`f64_div` included.

### 6.2 Slicing inside the Sail context: the real minimum

The slices of §6.1 were cut without the caller's context, and that was
wrong. Sail does not call these operations generically. The wrapper it
calls, `c_emulator/riscv_softfloat.cpp`, fixes the state first:

```c
void softfloat_init(uint64_t rm) {
  softfloat_exceptionFlags = 0;
  softfloat_roundingMode = uint8_of_rm(rm);
}
```

and the twelve float-to-integer conversions additionally pass a literal:
`f64_to_i64(a, rm8, true)`. So three facts hold at every call: the
exception flags start at zero, the rounding mode is one of five known
values, and `exact` is `true`.

Pinning them and re-slicing, 650 builds:

| | instructions |
|---|---|
| generic, this pipeline | 9,648 |
| **minimum, best mode per operation** | **8,160** |
| the same, also pinning `exact` | 8,147 |
| keeping all five modes per affected operation | 38,762 |

Context is worth 15 percent. The `exact` flag is worth 13 instructions
across all twelve converts, which is a useful negative: per-caller facts
beyond the mode are unlikely to repay the effort.

**Which operations the mode touches was decided by measurement, not by
name.** 47 are affected, 20 are not. The twenty are shown identical by
SHA-256 over the whole object across all five modes, not asserted.

The rounding modes, read from `source/include/softfloat.h`:
`near_even = 0`, `minMag = 1`, `min = 2`, `max = 3`, `near_maxMag = 4`,
`odd = 6`. RISC-V reaches 0 to 4; mode 6 is SoftFloat's own and is never
selected.

**arithmetic**

| operation | generic | **best** | at mode | worst | pinned via |
|---|---|---|---|---|---|
| `f16_add` | 373 | **318** | 0 | 427 | global |
| `f16_div` | 233 | **200** | 4 | 205 | global |
| `f16_mul` | 235 | **202** | 1 | 211 | global |
| `f16_mulAdd` | 457 | **421** | 1 | 428 | global |
| `f16_sqrt` | 221 | **189** | 1 | 199 | global |
| `f16_sub` | 373 | **318** | 0 | 427 | global |
| `f32_add` | 299 | **292** | 2 | 386 | global |
| `f32_div` | 253 | **225** | 1 | 229 | global |
| `f32_mul` | 244 | **214** | 1 | 219 | global |
| `f32_mulAdd` | 452 | **420** | 2 | 424 | global |
| `f32_sqrt` | 239 | **208** | 1 | 214 | global |
| `f32_sub` | 299 | **292** | 2 | 386 | global |
| `f64_add` | 315 | **311** | 0 | 404 | global |
| `f64_div` | 297 | **269** | 1 | 275 | global |
| `f64_mul` | 255 | **225** | 1 | 231 | global |
| `f64_mulAdd` | 507 | **476** | 1 | 482 | global |
| `f64_sqrt` | 257 | **231** | 1 | 236 | global |
| `f64_sub` | 312 | **308** | 0 | 402 | global |

**convert**

| operation | generic | **best** | at mode | worst | pinned via |
|---|---|---|---|---|---|
| `f16_to_i32` | 85 | **62** | 1 | 68 | parameter_wrapper+pinned_global |
| `f16_to_i64` | 84 | **61** | 1 | 67 | parameter_wrapper+pinned_global |
| `f16_to_ui32` | 71 | **44** | 2 | 57 | parameter_wrapper+pinned_global |
| `f16_to_ui64` | 73 | **47** | 2 | 56 | parameter_wrapper+pinned_global |
| `f32_to_bf16` | 118 | **67** | 1 | 91 | global |
| `f32_to_f16` | 134 | **87** | 1 | 104 | global |
| `f32_to_i32` | 90 | **62** | 1 | 72 | parameter_wrapper+pinned_global |
| `f32_to_i64` | 97 | **76** | 4 | 84 | parameter_wrapper+pinned_global |
| `f32_to_ui32` | 81 | **55** | 2 | 62 | parameter_wrapper+pinned_global |
| `f32_to_ui64` | 89 | **63** | 4 | 74 | parameter_wrapper+pinned_global |
| `f64_to_f16` | 131 | **88** | 1 | 104 | global |
| `f64_to_f32` | 121 | **83** | 1 | 96 | global |
| `f64_to_i32` | 88 | **60** | 1 | 70 | parameter_wrapper+pinned_global |
| `f64_to_i64` | 92 | **70** | 1 | 78 | parameter_wrapper+pinned_global |
| `f64_to_ui32` | 79 | **53** | 2 | 60 | parameter_wrapper+pinned_global |
| `f64_to_ui64` | 87 | **62** | 2 | 70 | parameter_wrapper+pinned_global |
| `i32_to_f16` | 136 | **110** | 1 | 119 | global |
| `i32_to_f32` | 104 | **75** | 1 | 80 | global |
| `i64_to_f16` | 150 | **124** | 1 | 134 | global |
| `i64_to_f32` | 123 | **94** | 1 | 100 | global |
| `i64_to_f64` | 114 | **84** | 1 | 90 | global |
| `ui32_to_f16` | 125 | **101** | 1 | 107 | global |
| `ui32_to_f32` | 119 | **58** | 1 | 73 | global |
| `ui64_to_f16` | 139 | **111** | 1 | 122 | global |
| `ui64_to_f32` | 114 | **87** | 1 | 92 | global |
| `ui64_to_f64` | 133 | **72** | 1 | 87 | global |

**round to integer**

| operation | generic | **best** | at mode | worst | pinned via |
|---|---|---|---|---|---|
| `f16_roundToInt` | 114 | **49** | 1 | 77 | parameter_wrapper+pinned_global |
| `f32_roundToInt` | 99 | **49** | 1 | 65 | parameter_wrapper+pinned_global |
| `f64_roundToInt` | 103 | **53** | 1 | 71 | parameter_wrapper+pinned_global |

**mode-independent — identical object across all five modes**

| operation | slice | operation | slice |
|---|---|---|---|
| `f16_eq` | 38 | `f64_eq` | 40 |
| `f16_le` | 39 | `f64_le` | 33 |
| `f16_le_quiet` | 51 | `f64_le_quiet` | 47 |
| `f16_lt` | 37 | `f64_lt` | 32 |
| `f16_lt_quiet` | 49 | `f64_lt_quiet` | 46 |
| `f32_eq` | 38 | `f16_to_f32` | 71 |
| `f32_le` | 38 | `f16_to_f64` | 76 |
| `f32_le_quiet` | 49 | `f32_to_f64` | 78 |
| `f32_lt` | 36 | `i32_to_f64` | 47 |
| `f32_lt_quiet` | 48 | `ui32_to_f64` | 41 |

**What specialising removes.** Over all 650 builds:

- **Indirect jumps: zero.** They existed only in the three generic
  round-to-integer baselines, one 6-entry table each, and every pinning
  deletes them. The computed jump was never a walker problem; it was an
  artifact of slicing without context.
- **Natural loops: zero**, dominator-checked across all 650.
- **Calls: only the six add and subtract**, and not even those at mode
  1, where the rounding helper folds in. Forced inlining clears all six.

Round toward zero (mode 1) is the cheapest in 33 of the 47 affected
operations and is also the mode where the last call disappears. If one
mode is to be done first, that is the one.

One trap, recorded because it silently gives a wrong answer: linking
SoftFloat's unmodified `softfloat_state.c` lets the optimiser fold its
`near_even` initialiser, so the "generic" slice quietly becomes the
mode-0 slice. The generic figures above are measured with that file
left out.

### 6.3 Flattening: every float operation as one block of pure arithmetic

§6.2 left two things in the way of the walker, which reads a FLAT list of
instructions and refuses any body with a branch: branches, and the stack
and flag memory. Both come out by the same kind of mechanical transform
that §6.1 and §6.2 used, and neither needs walker work.

**What flattening is.** A branch chooses between two computations. Flattening
computes BOTH and picks the answer arithmetically:

```
result = (A & mask) | (B & ~mask)
```

with `mask` all-ones when the condition held. Same answer, no control
flow. The cost is that both arms always run.

**Why it is legal here, and only here.** Three preconditions, each
established by an earlier step and none of them true of ordinary
compiled code:

| precondition | established by |
|---|---|
| no loops, so the control-flow graph is a DAG and always flattens | §5, dominator-checked over 650 builds |
| no calls | §6.1 slicing |
| every instruction safe to run unconditionally | localising the flag global, which removed all data memory |

**The chain, measured on `f64_le` at rounding mode 1:**

| stage | instructions | branches | memory |
|---|---|---|---|
| sliced, mode pinned | 33 | 6 | 3 |
| flag global localised | 28 | 6 | 0 |
| DAG flattened to one block | 32 | 2 | 0 |
| selects lowered to mask arithmetic | **34** | **0** | **0** |

The last step is needed because base RISC-V has no conditional move, so
the backend re-introduces a branch for any `select` left in the IR.

**The result over all 67.** Every one became a single basic block with
zero branches, zero jumps, zero calls and zero data memory. All 670
artifacts, five rounding modes by two flag variants.

| | instructions |
|---|---|
| sliced, best mode each | 8,702 |
| **flattened, best mode each** | **11,900** |
| flattened, value plus exception flags | 14,220 |
| flattened, all five modes kept | 63,017 |

Flattening costs 1.37 times. The compare and round-to-integer families
got SMALLER, because their branches cost more than the arithmetic that
replaces them.

A correction to §6.2: the honest baseline is 8,702, not the 8,160
published there, which counted only the entry symbol at a lighter
optimisation level. The 1.37 figure uses the comparable baseline.

**Verification, which is the part that matters.** A smaller instruction
count is worthless if the meaning changed. Every flattened operation was
built for the host as well and run against the original:

| | |
|---|---|
| inputs per pass | 205,443,140 |
| passes | 2 |
| total evaluations | 410,886,280 |
| **mismatches** | **0** |

Inputs were the full edge cross-product (positive and negative zero and
infinity, quiet and signalling NaN, largest and smallest normal and
subnormal, each plus or minus one ulp) plus 300,000 randoms per operand
per mode. Exception flags were compared as well as values.

The second pass exists because the first was not sound evidence: the
host and RISC-V builds are NOT the same IR, only 48 of 670 matched,
since the two datalayouts declare different native integer widths and
`instcombine` narrows differently. The second pass takes the exact IR
handed to the RISC-V backend, rewrites only the datalayout and triple,
and runs that.

**Three transforms were needed beyond the four above**, all mechanical
and none float-specific: the square-root lookup tables lowered into
arithmetic by packing entries into words and selecting with masks;
minimum and maximum lowered to masks, since RISC-V has no instruction
for them and the backend emitted the last remaining branch; and the
backend told not to park large constants in a constant pool.

**Guards went on exactly three instructions**, one divide in each of
`f16_div`, `f32_div` and `f64_div`. A divide is undefined on a zero
divisor in LLVM IR even though RISC-V's own `divu` returns all ones and
never traps, so hoisting one out of a guarded block is invalid. The
divisor is forced away from zero when its path condition is false. No
other unsafe instruction exists in the set.

**What is NOT solved, stated plainly.** "Zero memory" is true of DATA
memory. 284 of the 670 objects spill to the stack, 13,210 instructions
of it, because branch-free code holds every value live at once and
RISC-V has 27 usable registers. So the walker still meets memory on 42
percent of these. It is the easy kind, known stack offsets, local to the
body, dead at return, but it is not nothing.

Artifacts: `Research/oracle/riscv/softfloat_slices/flattened/`, 2,011
files; the flattener is `scripts/flatten_dag.py`.

### 6.4 The step never taken: a float operation as a Lean expression

Lane `lp3_l94`, 2026-09-16, 175 s on instance lp3. The nine flattened
float operations that have zero branches AND zero memory were run
through the walker: Sail's own decoder reads each word, Sail's own
`execute` definitions compose through the registers, and Lean certifies
that running those instructions leaves the composed expression in the
answering register.

**Nine of nine CERTIFIED. None refused, none failed.**

| operation | verdict | Lean |
|---|---|---|
| `f64_eq` | CERTIFIED | 17.5 s |
| `f16_eq` | CERTIFIED | 17.0 s |
| `f64_le` | CERTIFIED | 18.2 s |
| `f64_lt` | CERTIFIED | 18.2 s |
| `f64_le_quiet` | CERTIFIED | 18.2 s |
| `f64_lt_quiet` | CERTIFIED | 18.3 s |
| `f64_to_ui32` | CERTIFIED | 22.1 s |
| `f64_to_i64` | CERTIFIED | 22.2 s |
| `f64_to_ui64` | CERTIFIED | 22.0 s |

**LITERAL**, IEEE double equality as Sail's own RISC-V definitions,
abbreviated (the full term is in the run's `walk.json`):

```
(pure_RTYPE ((pure_RTYPE ((pure_ITYPE ((pure_RTYPE (a) (b) (rop.XOR)))
  (0x001) (iop.SLTIU))) ((pure_ITYPE ((pure_SHIFTIOP ((pure_RTYPE (b) (a)
  (rop.OR))) (0x01) (sop.SLLI))) (0x001) (iop.SLTIU))) (rop.OR))) ...
```

**GLOSS.** `f64_eq` is an exclusive-or of the two operands, tested
against zero; an or of the two, shifted left one to drop the sign, also
tested against zero, which is the both-zeros case; and on each operand a
test that the exponent field is not all ones or the fraction is zero,
which is the not-a-NaN case. Every leaf is a Sail clause: `RTYPE`,
`ITYPE`, `SHIFTIOP`, `ADDIW`. Nothing in it was typed by a person.

This closes the chain from Sail declaring `riscv_f64Eq` with no body to
a Lean expression for what it computes, by machine at every step:

```
Sail declares it external, no body
  -> Berkeley SoftFloat's C, in the model's own dependency tree
  -> compiled for riscv64, sliced, context pinned      (6.1, 6.2)
  -> flattened to one branch-free block                (6.3)
  -> walked through Sail's own definitions             (6.4)
  -> a Lean expression, certified
```

**What is not yet done.** Only 9 of 67 are eligible: the rest are
branch-free but spill to the stack, and the walker refuses memory. And
this is the emulation's meaning, not a proof that it equals anything;
Sail has no clause for a float operation to prove it against, so
SoftFloat is the ground truth, as it is for the C simulator.

One defect found and fixed on the way, recorded because it cost a lane:
the first attempt refused all four units with *"reads x15, outside the
ABI arguments"*. The cause was the word extraction, which tested the
first character of the disassembly's address with `isdigit`, so every
instruction at an address beginning with a hex letter was silently
dropped, including the one initialising that register. The walker was
right and the input was wrong.

### 6.5 Unproven functional emulation, in four languages

the owner, 2026-09-16: "the ultimate goal is to reach arch-unit emulation
across all the languages -- ultimately with proof eventually but first
unproven functional emulation."

Each flattened block of §6.3 was emitted as SOURCE in c, c++, rust and
go, so that a float arch-opcode is computed by ordinary integer
operators of each language. **67 of 67 in every language. Nothing failed
to emit, nothing failed to compile, nothing mismatched.**

| family | ops | c | c++ | rust | go |
|---|---|---|---|---|---|
| f16 arithmetic | 6 | 2,486 | 2,510 | 2,486 | 2,480 |
| f32 arithmetic | 6 | 2,467 | 2,491 | 2,467 | 2,461 |
| f64 arithmetic | 6 | 2,567 | 2,591 | 2,567 | 2,561 |
| compare, three widths | 9 | 294 | 330 | 294 | 285 |
| round to integer | 3 | 137 | 149 | 137 | 134 |
| float to float | 7 | 714 | 742 | 714 | 707 |
| float to integer | 12 | 931 | 979 | 931 | 919 |
| integer to float | 12 | 805 | 853 | 805 | 793 |
| **all 67** | 67 | **10,617** | **10,885** | **10,617** | **10,550** |

Largest is `f64_mulAdd` at about 640 lines; smallest `ui32_to_f64` at
about 22.

**Verification: 20,544,314 inputs per language, 82,177,256 comparisons,
0 mismatches.** The reference is SoftFloat itself, built from the
model's vendored tree with its own settings, called in-process: c and
c++ directly, rust through a foreign-function declaration, go through
cgo. Inputs are the full edge cross-product plus 200,000 uniform randoms
per operand plus 100,000 with banded exponents so subnormals and
overflow are actually reached.

**Two controls, which are what make the zero meaningful.** A count of
zero mismatches says nothing unless the test can detect a difference:

| control | result |
|---|---|
| point the same binaries at an oracle using a DIFFERENT rounding mode | 115,378 mismatches of 645,314, in every language |
| re-emit with the OPPOSITE reading of all three poison don't-cares (over-wide shift, `ctlz(0)`, divide by zero) | still 0 mismatches over the same 20.5 M inputs |

The first shows the harness discriminates. The second shows the three
places where LLVM's semantics are undefined are genuinely unobservable
here, rather than the emulation having been pinned lucky.

**The one real portability obstacle was go's lack of a 128-bit
integer**, needed by exactly two operations, `f64_mul` and
`f64_mulAdd`, for the 64 by 64 to 128 significand product. c, c++ and
rust have one natively. Go gets a two-word pair with the full operation
set written out once, so later rounding modes need no new code.

The eight LLVM intrinsics needed a helper each per language. A built-in
was used only where its edge case is exactly LLVM's: rust's
`leading_zeros` and `saturating_sub`, c++'s `countl_zero`, go's
`bits.LeadingZeros`. Everything else is written out, because the
built-in differs at an edge: c's `__builtin_clz` is undefined at zero
and `std::abs` is undefined at the most negative value.

**What this is and is not.** It is functional emulation, established by
testing against the implementation the Sail C simulator itself links.
It is not proof. No Lean theorem stands behind any of these, and Sail
has no clause for a float operation to prove them against.

Artifacts: `Research/oracle/riscv/softfloat_slices/emulations/`,
`{c,cpp,rust,go}/` plus `emulations.json` and a README; the emitter and
harness in `scripts/`.

### 6.6 Arch-unit emulation across languages: the goal, reached unproven

the owner's target, 2026-09-16: "arch-unit emulation across all the languages
-- ultimately with proof eventually but first unproven functional
emulation."

An arch-unit is a compiler-operator lowered. 174 of the 1,244 RISC-V
arch-units of task rv2 contain a float instruction: 150 from c, 24 from
go. Each was decomposed into its arch-opcodes, every float one mapped to
the emulation of §6.5 and every integer one to the language's own
operator, and composed into one function per language.

**174 of 174, in all four languages. 696 files. No failures.**

170 are pure functions of the operand bits. Four are emulated under a
stated reduction: the address-of units, whose answer is an address
rather than a function of the operand, blocked by `c.addi4spn a0, sp,
0xc` in c and a call to the runtime allocator in go. For those the
reduction is emulated and the reference is reduced identically.

**The float arch-opcodes, 33 distinct, all accounted for:**

| kind | distinct | mapped to |
|---|---|---|
| arithmetic at single and double width | 8 | the §6.5 emulations |
| compares at single and double width | 6 | the §6.5 emulations |
| integer to float, float to float | 9 | the §6.5 emulations |
| bit moves, sign splices, the Zfa constant, loads and stores | 10 | pure bit manipulation, written directly |

23 to an emulation, 10 to bit manipulation, none failed.

**Verification against the ORIGINAL compiler-operator, not against
SoftFloat.** Testing against SoftFloat would have been circular, since
the emulations came from it. Instead each unit's own expression was
compiled natively in its own language at `-O2` with no fast-math, and
both were run on the same inputs.

| | |
|---|---|
| inputs per language | 52,478,900 |
| comparisons against the native operator | 209,915,600 |
| **mismatches** | **0** |
| cross-language comparisons, byte for byte against c's stream | 157,436,700 |
| **mismatches** | **0** |

And the generated code was disassembled and checked: **zero float
instructions, zero vector-register references, in any language.** The
emulation really is integer-only.

**A genuine specification-level divergence was found, and it is the most
valuable thing here.** On 94,744 inputs per language, across 92 of the
174 units, the two answers differ. Both are a NaN of the result type;
they differ only in sign and payload. LITERAL, from the run:

```
au 6   c ++a   0x7f800001               native 0x7fc00001        emul 0x7fc00000
au 26  c a+b   0x0, 0x7ff0000000000001  native 0x7ff8...0001     emul 0x7ff8...0000
au 154 go a*b  0x0, 0x7f800000          native 0xffc00000        emul 0x7fc00000
```

**GLOSS.** c and go both leave a NaN's sign and payload unspecified. So
three implementations legitimately disagree: RISC-V pins every NaN
result to the canonical quiet NaN; x86-64 propagates a quieted input
payload, or returns the negative indefinite for an invalid operation
with no NaN input; our emulation follows RISC-V because SoftFloat does.
Set the payload aside and the difference count is zero.

It reaches exactly the 88 arithmetic units and the 4 increment and
decrement units. Every comparison, every logical operator, every sign
splice and every address-of diverges on nothing.

**This is a portability fact the line needs**, not a defect: a NaN's
payload does not carry across architectures, so any round trip that
claims bit-exactness must either exclude it or pin it deliberately.

**What this is.** Functional emulation, established by testing. It is
not proof: no Lean theorem stands behind any of it, and Sail has no
clause for a float operation to prove it against.

Artifacts: `Research/oracle/riscv/softfloat_slices/arch_units/`,
`{c,cpp,rust,go}/` plus `arch_units.json` and a README; the builder,
verifier and the no-float disassembly probe in `scripts/`.

### 6.7 The per-arm fix: one clause, and what it unblocked

Sail writes several instructions into ONE clause and selects between
them with a match. **LITERAL**, `model/extensions/I/base_insts.sail:29`:

```
X(rd) = match op {
    LUI   => off,
    AUIPC => get_arch_pc() + off
};
```

**GLOSS.** `lui` is "put this constant in a register", a sign-extended
immediate and nothing else. `auipc` adds the program counter, which is
an effect. The strip refused the WHOLE clause over the `auipc` arm, so
every compiled body containing a `lui` was refused over a sibling it
never executes. In the corpus run of log 278 that was 82 units; among
the flattened float slices of §6.3 it was 34 of the 43 that are
otherwise clean.

That the semantics are strippable was never in doubt: Sail's compressed
`C_LUI`, which has only the pure arm, was already certified.

**The change**, in `leanpath/strip.py` and `leanpath/walk.py`, 97 lines:

- an arm with an effect no longer condemns its siblings; it is recorded
  and the clause is certified **per arm**, shape `arms`
- one definition and one certificate per pure arm, each stated with the
  CONCRETE constructor substituted for the case parameter
- **no definition is emitted for an arm that cannot be expressed**, so
  nothing false can be stated about it; this is what makes it sound
- the walk takes the arm the decode actually produced and refuses one
  with no form

**LITERAL**, what the strip now emits for `UTYPE`:

```lean
def pure_UTYPE_LUI (imm : (BitVec 20)) : BitVec 64 :=
  let off : xlenbits := (sign_extend (m := 64) (imm +++ 0x000#12))
  off

theorem strip_UTYPE_LUI (imm : (BitVec 20)) (rd : regidx) :
    execute_UTYPE imm rd .LUI =
    (do
      wX_bits rd (pure_UTYPE_LUI imm)
      pure RETIRE_SUCCESS) := by
  first
  | rfl
  | simp only [execute_UTYPE, pure_UTYPE_LUI, bind_assoc, pure_bind]
```

**Verified, lane `lp3_l95`.** The strip re-run over the whole model
certifies `UTYPE` with `pure_arms = [LUI]` and records
`arms_not_expressible = [UTYPE.AUIPC]`.

**Exactly ONE clause of the 339 benefits.** The leverage is not in the
count but in how common `lui` is: one clause, 82 corpus units and 34
float operations.

**And it moved the wall rather than removing it.** The 34 now compose,
but several fail in Lean with *"(kernel) deep recursion detected"*. That
is the term-size problem log 278 §7.3 named: the compose step
substitutes each register's value into every later use, so a value used
twice is copied twice and the term's nesting depth grows with the body.
The named remedy is one `let` per instruction in compose, so the term is
linear in the instruction count and shared values are shared. That is
now the binding constraint for the larger float slices, and `lui` is
not.

**An accounting note, so no credit is misplaced.** The strip's certified
count went from 93 in the older baseline to 128 in this run. Most of
that gain is NOT this change: the other session added a float-effects
rule on 2026-09-15 that accounts for about 31 of it. This change
accounts for `UTYPE` alone.

### 6.8 Every readable arch-unit, in four languages

The 318 arch-units with no float instruction were emulated the same way
as the 174 float ones, completing the set.

**318 of 318 in c, c++, rust and go. No failures, no blocking
arch-opcode.** 55 distinct integer arch-opcodes across 1,119
occurrences: compares, bitwise, add and subtract, the word forms that
operate on the low 32 bits and sign-extend, shifts, multiply, divide and
remainder, a conditional select, and the stack prologue and frame
traffic which is elided because it is not part of the function.

| | comparisons | mismatches |
|---|---|---|
| against each unit's own native operator | 379,402,096 | **0** |
| cross-language, byte for byte | 289,090,134 | **0** |

**Combined with §6.6: 474 of 474 readable arch-units are emulated in all
four languages**, 156 float and 318 integer. The directory holds 492
including 18 float units the older walker could not read.

#### 6.8.1 Six genuine divergences, all found by the run

These are the valuable part. Each is a place where "the same operator"
means different things, and each was handled in the open rather than by
dropping inputs quietly.

| # | what | units | what was done |
|---|---|---|---|
| 1 | **C's division is undefined** at a zero divisor and at the most negative over minus one; the host faults | 32 c units | those inputs are flagged and excluded from the native comparison, still cross-checked across languages; the emulation writes RISC-V's non-trapping answer out as restoring long division, using no `/` or `%` at all |
| 2 | **clang folds `a / (bool)b` to the identity** | 8 units | at `b == 0` the arch-unit answers `a`, not all ones. A compiler's licence under undefined behaviour, visible in the machine code |
| 3 | **go panics where RISC-V does not** | 18 units | the emulation is split into a value function and a `_trap` predicate, verified against go's real panics through `recover` |
| 4 | **RISC-V's shift is not go's, and is undefined in C** | 18 units | every emitted shift count is masked to 5 or 6 bits first, so nothing is undefined |
| 5 | **go leaves a 32-bit answer non-canonical in the register** | 6 units, found by probing all 141 narrow-result units | comparison is done at the result's own width |
| 6 | **address-of is an address, not a function of the operand** | 5 units | emulated under the stated reduction, reference reduced identically |

6,051,416 comparisons were excluded, all of them case 1, where the C
reference is undefined rather than merely different.

#### 6.8.2 What the probe generator did not reach

**Correction, 2026-09-16.** This section first read "What cannot be
emulated, and why", and said of the 737 `BUILDFAIL` rows that "the
compiler-operator does not exist, so there is nothing to emulate". the owner
challenged it — *"we have emulations for every arch-opcode and every
primitive so how is anything escaping the machinery?"* — and he is
right. The original claim conflated two different things:

1. **that compiler will not lower that spelling** — true, and it is
   what `attest_rv.json` records;
2. **the operation has no meaning** — false, and not what a `BUILDFAIL`
   shows.

A refusal is precisely the case this line exists for: an operator one
language has, carried into a language that lacks it. The original
wording filed the hub's purpose under its exclusions. Corrected below;
the original sentence is named here rather than quietly removed.

| | count | what it is |
|---|---|---|
| `BUILDFAIL` | 737 | no body: the probe asked the compiler for `a OP b` in that compiler's own syntax and the compiler refused the spelling. Sorted below |
| `WALK_REFUSED` | 33 | a body exists but the older walker lacks a table entry. Not unemulable, merely outside the attested set; 18 carry float and were already covered |

Sorting the 737 by what was actually refused, and by whether the
operation is buildable from pieces the corpus already holds:

| n | the refusal | buildable? | out of what |
|---|---|---|---|
| 342 | go: `int32 OP float64` — no implicit mixing | yes | a convert, then the float op |
| 216 | go: `int32 OP int64` — no implicit widening | yes | sign- or zero-extend, then the integer op |
| 98 | c: `%`, `<<`, `&`, `\|`, `^` applied to `float`/`double` | yes | `f64_rem` and kin, or the bit-pattern reading |
| 21 | go: arithmetic on two `bool` | yes | a bool is a one-bit integer |
| 12 | go: `a++` / `a--` in expression position | yes | the same increment; go forbids only the position |
| 2 | c: `~` on a `double` | yes | bit-pattern complement |
| 28 | c: `alignof a` / `_Alignof a` on an expression | **no** | alignment is a property of a type; nothing runs |
| 18 | c, go: unary `*`, `&`, `<-` on a non-pointer, non-channel | **no** | these compute no value |

**691 of 737 are buildable; 46 are not runtime operations at all.**

Two worked concretely:

- go `int32 + int64`. The operation is sign-extend then add. Both are
  arch-opcodes the corpus carries emulations for in all four languages.
  Go's type rule forbids writing it, not performing it.
- c `double % double`. The operation is `f64_rem`, which Berkeley
  SoftFloat defines in full. It is absent from the 67 sliced externals
  only because the slice list was taken from Sail's RISC-V externals
  and RISC-V has no float-remainder instruction. One slice away.

So the 737 are a limit of the **probe generator**, not of
expressibility. Closing them needs a second probe form that asks for
the *emulation* of `a OP b` rather than for the spelling the compiler
rejects — the emulation corpus is already the shape of that answer.
This is open work and is listed as such in §8.

Artifacts: `Research/oracle/riscv/softfloat_slices/arch_units/`,
`{c,cpp,rust,go}/` with 495 files each, `arch_units.json` covering all
492, and the builders and verifiers in `scripts/`.

## 7. What the walker needs, in order

**Correction, 2026-09-16.** The first version of this section was written
from the SoftFloat measurement plus an assumption about the walker's
internals that had not been read. Two things in it were wrong, and the owner
caught both. They are corrected here and the original claims are named
so the error is visible.

- It said "the current walker forks, which is why it fears explosion".
  **It does not fork.** It has no control-flow handling of any kind. A
  body containing a branch is refused outright:
  `arch_unit.branch_rule` returns *"fork-and-join not implemented in
  lp1; the form shows the condition"*, and in the corpus run of log 278
  a `BTYPE` body is a refusal row, not a forked walk.
- It never said that **the walker has two halves**, and that the branch
  work lands in the Lean half first.

### 7.1 The walker is two halves

| half | file | what it does |
|---|---|---|
| composer | `leanpath/walk.py`, `compose` | carries a map from register number to expression along a LINEAR list of decoded instructions; reads become lookups, the write updates the map |
| certifier | `leanpath/walk.py`, `walk_file`, over `lean/Leanpath.lean.in` | states in Lean that running those instructions through Sail's own `execute` leaves the composed expression in the answering register, and lets `simp` check it |

**LITERAL**, the Lean side's walk, from `walk_file`:

```lean
def walk : List instruction → SailM ExecutionResult
  | [] => pure RETIRE_SUCCESS
  | i :: is => do let _ ← step i; walk is
```

**GLOSS.** It executes every instruction in the list, in address order,
and never reads the program counter. That is faithful for straight-line
code and wrong the moment a branch exists, because a branch's whole
effect is to decide which instructions run next. A flat walk would
execute both arms.

So "a branch becomes a conditional in one expression" is not an edit to
the composer. The certifier has to follow control flow, or the theorem
it states does not mean what it says.

### 7.2 The four pieces, restated

| # | piece | size | where the work lands |
|---|---|---|---|
| 1 | control flow: the Lean walk must follow the program counter, and the composer must merge register maps at a join | 372 branches | Lean first, then the composer; this is the architecture decision of §7.3 |
| 2 | calls | 0 after slicing | not walker work; §6 deletes it for 61 of 67 operations |
| 3 | memory | 324 loads and stores | composer; stack traffic only, local to the body, so it can be extra unknowns rather than a memory model |
| 4 | the jump tables | **0 after §6.2** | not walker work at all; pinning the rounding mode deletes every one |

The 64-instruction bound remains an arbitrary guard rather than a
necessity: nothing breaks at 65, and for straight-line code the cost is
linear.

**Row 4 is closed by §6.2, which was measured after this section was
first written.** The three tables came from a `switch` on the rounding
mode. Sail fixes that mode at every call, so slicing inside the caller's
context folds the switch and the table with it: zero indirect jumps in
all 650 specialised builds. Row 2 tightens the same way — at mode 1 even
the six add and subtract operations come out call-free.

So two of the four pieces are gone, and both were removed by slicing
rather than by touching the walker. What remains is control flow and
stack memory.

### 7.3 The architecture decision, open

Two ways to make the certifier follow control flow. This is the owner's call
and nothing is built until it is made.

| | what changes | cost |
|---|---|---|
| **follow the program counter** | the body becomes instructions paired with offsets; the Lean walk reads the program counter, finds the instruction at that offset, executes, repeats, with fuel equal to the instruction count | program-counter arithmetic and an offset lookup in Lean; unfolding terminates because the body is loop-free and the fuel is concrete |
| **blocks plus a join lemma** | today's flat walk is kept per straight-line block, unchanged and sound; blocks are combined in Lean by a lemma saying the machine takes one block when the condition holds and the other otherwise | smaller change to existing code, but one proof obligation per join, forever |

The first removes the branch refusal, the call refusal and the
instruction bound together, because all three follow from the list being
flat. The second preserves more of what exists.

## 8. What this changes

- The float gap is closeable with no new theory: no induction, no
  width-general lemma, nothing of the kind the multiply-high wall
  needed. It is four pieces of engineering over code that is entirely
  straight-line.
- The route is not "abandon Lean". The float hole is Sail's, not
  Lean's: Sail declares those operations with no body for any backend,
  and only the C backend works because it links a library. Rocq,
  Isabelle and SMT have the identical hole.
- Sail's remaining job is narrow and worth keeping: it supplies the
  formula per instruction without a person typing one. That is the
  thing the owner ordered removed on 2026-09-14 when `riscv_reference.py`
  was deleted, and writing a modeller by hand would put it back.
- Bit-blasting is not what extracts logic from code. Blasting takes a
  formula to gates. Code to formula is symbolic execution, which is
  what `walk` already does.
- **Open work, opened by §6.8.2's correction:** 691 arch-units the
  probe generator never reached, because it asked each compiler for a
  spelling that compiler rejects. They need a second probe form that
  asks for the *emulation* — widen-then-operate, convert-then-operate,
  the bit-pattern reading — rather than for `a OP b`. The pieces are
  already in the corpus; what is missing is the generator that
  assembles them. This would take the attested set from 492 to roughly
  1,183 of the 1,244, with 46 genuinely outside it.

## 9. Two lists

Decided, recorded for audit:

- GMP 6.3.0 fetched to `SOURCES/gmp` with provenance and
  checksum; nothing else under `SOURCES` was touched;
- Sail's own library was copied out of the tower's `lp3-runner` into
  this session's scratchpad, 60 files, sail 0.20.2;
- every number above is reproducible by the command beside it; the
  measurement artifacts are in this session's scratchpad;
- §6.8.2 rewritten 2026-09-16 after the owner challenged its claim that the
  737 `BUILDFAIL` rows had "nothing to emulate". The claim was wrong,
  the original sentence is named in place, and the matching passage in
  `PRIVATE/PseudoCoupHQ/README.md` was corrected to match.

Awaiting the owner:

- whether Sail's library belongs in the repo as a reference copy, so a
  later session does not reach into a container for it;
- whether to open a plan node for the float route (slice, walk, prove)
  or fold it into the existing `arch_unit.branch_rule` leaf;
- the two files both numbered `log_292` in `DevComms`, which are
  identical and are chat text rather than logs.

## 10. Pointers

- GMP: `SOURCES/gmp`, and its `FETCHED.txt`
- SoftFloat: `SOURCES/sail-riscv/dependencies/softfloat/berkeley-softfloat-3/`
- the model: `SOURCES/sail-riscv/model/`, commit `3243f93`
- the float externals the model declares: `model/core/softfloat_interface.sail`
- the primitive inventory at the Sail level: log 291
- the construction ruling and its algorithms: `Research/oracle/cross_construction/emulation/construct/general/build.py`
- the gate netlists already generated: `Research/oracle/riscv/primitives_as_gates/`, 72 files, 18 operations at 8/16/32/64
