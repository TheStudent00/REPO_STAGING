# SPEC — the reading form

A second column beside the canonical runnable text. One instruction,
one reading line, always — so the two columns line up and either can
be read against the other.

```
mov %edi,%eax       %eax = %edi
cltd                %edx = sign_bits(%eax)
idiv %esi           %eax, %edx = sdiv(join(%edx, %eax), %esi)
mov %edx,%eax       %eax = %edx
ret                 return %eax
```

Ratified by the owner 2026-08-27 (style, two columns, register spelling
kept). **The function NAMES below are proposed, not ratified** —
naming is the owner's; strike and replace freely.

## Rules

- **One line in, one line out.** No instruction is folded into
  another, no instruction is dropped. The correspondence is what
  makes the column trustworthy.
- **Implicit operands are written out.** If the hardware reads a
  register the text does not name, the reading line names it.
- **Registers keep their spelling, `%` included.** `%eax` already
  says 32 bits, so widths are not repeated in function names for
  integer work. Float registers (`%xmm0`) do not carry a width, so
  float function names carry it (`add_f32`, `add_f64`).
- **The reading form adds nothing and decides nothing.** It is a
  rendering of the instruction, not an interpretation of it. Where
  a value's role is known from the recorded evidence rather than
  the instruction (which register holds the result at `ret`), the
  line says so and the field it came from is recorded.

## The function vocabulary (proposed)

| function | means |
|---|---|
| `sign_bits(x)` | a word made of copies of x's sign bit |
| `join(hi, lo)` | two registers read as one double-width value |
| `sdiv(n, d)` / `udiv(n, d)` | divide; answers **two** values, quotient then remainder |
| `smul(a, b)` / `umul(a, b)` | multiply; the one-operand form answers two values, low then high |
| `compare(a, b)` | the flags left by subtracting b from a |
| `bit_compare(a, b)` | the flags left by bitwise-and (this is `test`) |
| `fcompare_f32/f64(a, b)` | the flags left by a float comparison, including the NaN flag |
| `flags.<name>` | one fact read out of the flags — `equal`, `signed_less`, `below`, `carry`, `sign`, `nan`, and their negations |
| `zero_extend(x)` / `sign_extend(x)` | widen, filling with zeros / with copies of the sign bit |
| `shift_left`, `shift_right_zeros`, `shift_right_sign` | the three shifts |
| `int_to_f32/f64(x)`, `f32_to_f64(x)` | number-shape conversions |
| `mask_equal_f32(a,b)`, `mask_unequal_f32(a,b)` (and `_f64`) | float compares that answer all-ones or all-zeros instead of flags |
| `trap()` | an instruction that always faults (`ud2`) |
| `push(x)` / `pop()` | stack save and restore |

## Templates, by family

### Hidden-operand instructions

| instruction | reading line |
|---|---|
| `cltd` | `%edx = sign_bits(%eax)` |
| `cqto` | `%rdx = sign_bits(%rax)` |
| `idiv S` | `%eax, %edx = sdiv(join(%edx, %eax), S)` |
| `div S` | `%eax, %edx = udiv(join(%edx, %eax), S)` |
| `imul S` (one operand) | `%eax, %edx = smul(%eax, S)` |
| `mul S` (one operand) | `%eax, %edx = umul(%eax, S)` |
| `imul S,D` (two operands) | `D = D * S` |
| `sbb D,S` | `D = D - S - flags.carry` |
| `shl %cl,D` | `D = shift_left(D, %cl)` |
| `ret` | `return R` — R is the recorded result register, not named by the instruction |
| `call F` | `call F()` |

### Moves and widening

| instruction | reading line |
|---|---|
| `mov S,D`, `movq`, `movd`, `movb`, `movss`, `movsd`, `movaps`, `movapd` | `D = S` |
| `movabs $K,D` | `D = K` |
| `movzbl S,D` | `D = zero_extend(S)` |
| `movslq S,D` | `D = sign_extend(S)` |
| `lea (A,B,N),D` | `D = A + B*N` — **arithmetic, not a move** |
| `push S` / `pop D` | `push(S)` / `D = pop()` |
| `nop`, `nopl` | `# nothing` |

### Arithmetic and bit work

| instruction | reading line |
|---|---|
| `add S,D` / `sub S,D` | `D = D + S` / `D = D - S` |
| `neg D` | `D = -D` |
| `and S,D` / `or S,D` / `xor S,D` | `D = D & S` / `D = D \| S` / `D = D ^ S` |
| `not D` | `D = ~D` |
| `shr K,D` / `sar K,D` | `D = shift_right_zeros(D, K)` / `D = shift_right_sign(D, K)` |

### Flags: writers, then readers

| instruction | reading line |
|---|---|
| `cmp S,D` | `flags = compare(D, S)` |
| `test S,D` | `flags = bit_compare(D, S)` |
| `ucomiss S,D` / `ucomisd S,D` | `flags = fcompare_f32(D, S)` / `_f64` |
| `sete D` / `setne D` | `D = flags.equal` / `D = flags.not_equal` |
| `setl` / `setle` / `setg` / `setge` | `flags.signed_less` / `.signed_less_equal` / `.signed_greater` / `.signed_greater_equal` |
| `setb` / `setbe` / `seta` / `setae` | `flags.below` / `.below_equal` / `.above` / `.above_equal` |
| `sets` / `setns` | `flags.sign` / `flags.not_sign` |
| `setp` / `setnp` | `flags.nan` / `flags.not_nan` |
| `je L` / `jne L` / `jl` / `jb` / `jbe` / `ja` / `jae` / `js` / `jo` | `if flags.<same name>: goto L` |
| `jmp L` | `goto L` |
| `cmove S,D` etc. | `D = S if flags.<name> else D` |

### Floats

| instruction | reading line |
|---|---|
| `addss S,D` / `addsd S,D` | `D = D + S` (32-bit float) / (64-bit float) |
| `subss` / `subsd` / `mulss` / `mulsd` / `divss` / `divsd` | same shape, with `-`, `*`, `/` |
| `cvtsi2ss S,D` / `cvtsi2sd S,D` | `D = int_to_f32(S)` / `int_to_f64(S)` |
| `cvtss2sd S,D` | `D = f32_to_f64(S)` |
| `xorps S,D` / `xorpd` | `D = D ^ S` — zeroing when S and D are the same register, sign-flip against a constant otherwise |
| `andps` / `andpd` / `orps` / `orpd` / `pxor` | `D = D & S`, `D = D \| S`, `D = D ^ S` |
| `cmpeqss S,D` / `cmpneqss S,D` (and `sd`) | `D = mask_equal_f32(D, S)` / `mask_unequal_f32(D, S)` |
| `punpckldq S,D`, `unpckhpd S,D`, `subpd S,D` | rendered individually, with a note that this trio is the standard unsigned-64-to-float conversion |

### Ending

| instruction | reading line |
|---|---|
| `ud2` | `trap()` |

## What must fail loudly

An instruction with no template is **not** rendered as a guess. The
renderer refuses that unit by name, the way every other stage in
this line refuses, so an unknown opcode can never be silently shown
as something it is not.
