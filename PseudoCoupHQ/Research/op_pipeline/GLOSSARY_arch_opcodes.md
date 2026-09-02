# Glossary — the arch opcodes that appear in our units

Scope: the **93 distinct mnemonics** that actually occur in the ship
builds of `op_units_{c,cpp,go,rust,swift}.json`. Nothing here is
general x86 reference material for its own sake; every entry is an
opcode our corpus contains, with its counted occurrences.

Purpose: make the **implicit** parts explicit. An instruction's
written operands are not its full input list. `idiv %esi` names one
register and reads three. This file exists so reading a canonical
runnable unit needs no held-in-mind conditionals.

---

## 1. Four reading rules that apply everywhere

These four facts explain most of what looks hidden.

- **Operand order is source-then-destination.** `mov %edi,%eax`
  moves *from* `%edi` *into* `%eax`. The last operand written is
  the one modified. (This is AT&T order, which is what `objdump`
  prints and what our canonical form stores.)
- **Register names encode width, and they overlap.** `%rax` is 64
  bits; `%eax` is the low 32 bits of that same register; `%ax` the
  low 16; `%al` the low 8. `mov %edi,%eax` and `mov %rdi,%rax`
  touch the same two registers at two widths.
- **The flags register is an invisible operand.** A comparison
  writes it; a `set`/`jump`/`cmov` reads it. Neither writes the
  flags register's name. Any time two instructions seem
  unconnected — a `cmp` then a `setl` — the flags are the wire
  between them.
- **Suffix letters name the width or the number shape.** `b`=8
  bits, `w`=16, `l`=32, `q`=64. On float instructions, `ss`=one
  32-bit float, `sd`=one 64-bit float, `ps`/`pd`=several packed
  into one register at a time.

---

## 2. The genuinely hidden-operand instructions

These are the ones that read or write registers their text never
names. This section is the reason the file exists.

| written | also reads (unwritten) | writes | what it is |
|---|---|---|---|
| `idiv %esi` (36) | `%edx:%eax` as one 64-bit dividend | quotient→`%eax`, remainder→`%edx` | signed divide; **both** answers produced at once |
| `div %esi` (34) | `%edx:%eax` | quotient→`%eax`, remainder→`%edx` | same, unsigned |
| `cltd` (10) | `%eax` | `%edx` | fills `%edx` with copies of `%eax`'s sign bit, building the 64-bit dividend `idiv` needs |
| `cqto` (18) | `%rax` | `%rdx` | the same, one width up (`%rdx:%rax`) |
| `imul %esi` one-operand form (26 total incl. two-operand) | `%eax` | `%edx:%eax` | full-width signed multiply |
| `mul %esi` (1) | `%eax` | `%edx:%eax` | same, unsigned |
| `sbb %eax,%eax` (19) | the carry flag | destination | subtract-with-borrow; used as a trick to spread a flag across a whole register |
| `shl %cl,%eax` / `shr` / `sar` (56/73/28) | `%cl` when the count is a register | destination | the shift count may only live in `%cl` — the hardware allows no other register |
| `ret` (1783) | the stack pointer `%rsp`, and the return address it points at | `%rsp` | leaves the function |
| `call` (40) | `%rsp` | `%rsp`, pushes a return address | enters another function |

**Answering the two questions that prompted this file:**

- **`idiv %esi` is binary, and its second input is implicit.** The
  divisor is written (`%esi`). The dividend is not: it is the
  64-bit value formed by `%edx` (high half) and `%eax` (low half).
  So the operator's two operands are `(%edx:%eax, %esi)`.
- **`cltd` is not attached to the return register by coincidence.**
  It reads `%eax` and writes `%edx`, purely to build that dividend.
  It is a preparation step for `idiv` and appears nowhere else in
  our corpus — every `cltd`/`cqto` in the whole corpus is
  immediately followed by an `idiv` (measured, 100%).

---

## 3. Comparison, and the flag wire

An operator like `a < b` compiles into two instructions that share
the invisible flags register.

- **Writers of the flags** (they compute, discard the number, and
  keep only the flags):
  - `cmp %rsi,%rdi` (338) — subtracts, keeps flags only.
  - `test %edi,%edi` (311) — bitwise-ands, keeps flags only; the
    common use `test x,x` asks "is x zero?".
  - `ucomiss` (169) / `ucomisd` (191) — the same for floats, with
    an extra flag meaning "one of these was NaN".
- **Readers of the flags** — the `set` family writes 1 byte, `1`
  or `0`, into a byte register:

| written | true when |
|---|---|
| `sete` (61) / `setne` (400) | equal / not equal |
| `setl` (30) / `setle` (26) | signed less / less-or-equal |
| `setg` (30) / `setge` (26) | signed greater / greater-or-equal |
| `setb` (20) / `setbe` (18) | unsigned below / below-or-equal |
| `seta` (111) / `setae` (116) | unsigned above / above-or-equal |
| `sets` (8) / `setns` (8) | sign bit set / clear |
| `setp` (138) / `setnp` (2) | parity flag set / clear — after a float compare this means **"a NaN was involved"** |

  The pairing `setp` + `setne` + `or` (support 122 in
  `components2.json`) is the standard "unordered comparison" idiom:
  true if either the values differ or one was NaN.

- **Also flag readers:** the conditional jumps `je jne jl jb jbe ja
  jae js jo` (same condition names as above) and the conditional
  moves `cmove cmovne cmovb cmovbe` (32 total), which copy only if
  the condition holds.

---

## 4. Moving values (mostly bookkeeping, not computation)

These are the instructions the moves-erased ruling treats as
calling-rule bookkeeping rather than mathematics.

- `mov` (844) — copy. The single most common instruction, and
  almost never the operator's substance.
- `movq` (106) / `movd` (64) — copy between a general register and
  a float register, 64 or 32 bits.
- `movabs` (4) — load a constant too large for a normal `mov`.
- `movb` (5) — copy one byte.
- `movzbl` (88) — copy a byte into a 32-bit register, filling the
  rest with **zeros**. This is how a `set` byte becomes a full
  integer result.
- `movslq` (154) — copy a 32-bit value into a 64-bit register,
  filling the rest with **copies of its sign bit**. This is
  widening a signed number.
- `lea` (64) — computes an address expression but stores the
  *number* instead of loading from it. Compilers use it as a free
  add: `lea (%rdi,%rsi,1),%eax` **is** `a + b`. Treating `lea` as a
  move rather than arithmetic is a known trap.
- `push` (30) / `pop` (28) — save to / restore from the stack.
- `nop` (19) / `nopl` (7) — do nothing; padding.

---

## 5. Integer arithmetic and bit work

- `add` (44), `sub` (51), `neg` (22) — add, subtract, negate.
- `imul` two-operand form — signed multiply into the destination.
- `and` (375), `or` (380), `xor` (336), `not` (35) — bitwise. Note
  `xor %eax,%eax` is the standard way to write zero, not a
  computation of anything.
- `shl` (56) left shift, `shr` (73) right shift filling with
  zeros, `sar` (28) right shift filling with the sign bit — so
  `sar` is the signed one.

---

## 6. Float instructions

The `s` in the middle means **scalar** — one number, even though
the register is wide enough for several.

- Arithmetic: `addss`/`addsd` (73/73), `subss`/`subsd` (23/25),
  `mulss`/`mulsd` (25/25), `divss`/`divsd` (23/25) — `ss` for
  32-bit floats, `sd` for 64-bit.
- Conversion: `cvtsi2ss` (218) / `cvtsi2sd` (130) — integer to
  float; `cvtss2sd` (44) — 32-bit float to 64-bit float.
- Copying: `movss` (8) / `movsd` (8) — one float;
  `movaps`/`movapd` (16/60) — a whole register.
- Bit tricks used on floats: `xorps` (77) / `xorpd` (69) — usually
  either zeroing a register or flipping the sign bit;
  `andps`/`andpd` (3/3) — usually clearing the sign bit, i.e.
  absolute value; `orps`/`orpd` (3/3); `pxor` (2) — zeroing.
- Compare-producing-a-mask: `cmpeqss`/`cmpeqsd` (23/27),
  `cmpneqss`/`cmpneqsd` (41/47) — unlike `ucomiss`, these write a
  result of all-ones or all-zeros into the register rather than
  setting flags.
- Rearranging halves of a register: `punpckldq` (44),
  `unpckhpd` (44), `subpd` (44) — these three appear together as
  one recognizable sequence, the standard way of converting a
  64-bit **unsigned** integer to a float when the hardware has no
  direct instruction for it.

---

## 7. Ending, and deliberate failure

- `ret` (1783) — return. Present in essentially every unit.
- `jmp` (58) — unconditional jump.
- `ud2` (31) — an instruction defined to be invalid, so it always
  faults. Swift uses it as its trap response; where Go calls
  `runtime.panicdivide` and Rust calls a panic function, Swift
  simply executes an instruction that cannot execute.
- `call` (40) — in our units, almost always a call into a
  language's panic or error path, which is why it shows up as a
  mode rather than as the normal path.

---

## 8. Terms used about these instructions

```
implicit operand
    a register an instruction reads or
    writes without naming it in its text.
    example tied to context:
        `idiv %esi` in c/op_246 names only
        the divisor; `%edx:%eax` (the
        dividend) and `%edx` (where the
        remainder lands) are implicit.

flags register
    a small set of bits recording facts
    about the last arithmetic result —
    was it zero, negative, did it carry,
    was a NaN involved.
    example tied to context:
        in the `<` units, `cmp %rsi,%rdi`
        writes it and `setl %al` reads it;
        neither instruction names it.

welded pair
    two opcodes that cannot be separated
    because one exists only to prepare the
    other.
    example tied to context:
        `cltd ; idiv` — measured at 100%
        co-occurrence across the corpus, so
        component_mine2.py fuses them into
        one alpha.

scalar (the `s` in `addsd`)
    operating on one number in a register
    wide enough to hold several.
    example tied to context:
        `addsd %xmm1,%xmm0` adds one 64-bit
        float, leaving the register's upper
        half alone.
```
