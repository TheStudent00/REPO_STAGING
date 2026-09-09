# log_234 — arch-opcode mappings as fits: the owner's regression-fitting idea, read against the 162 opcodes

Node: `Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/` (goal
section, added 2026-09-07). Written 2026-09-07 by the coordinator
(Fable). Opinion is marked; the rest is definition. No runs.

the owner, verbatim: "i mean regression-fitting almost literally, perhaps
exactly. since an operator mapping can literally be plotted and
interpolated through. those interpolations could be added/combined/
composed (function-composition f(g(x)) and whatever else) to match
(emulate) the arch-opcode regression-fitting."

## 1. What a plotted mapping is

An arch opcode at width w is a function from 2^w (one input) or
2^(2w) (two inputs) points to 2^w values. Plotting it means: x axis
input a, y axis input b, height the output, every point known
exactly. There is no noise and no missing point, so "regression" here
is interpolation through a complete table: the fit is exact, and the
only question is which family of functions fits with few coefficients.

## 2. The three classes, and the basis in which each is an exact small fit

| opcode class (of the 162) | read as integers 0..2^w-1, the plot is | the basis where the fit is small and exact | fit |
|---|---|---|---|
| `add sub neg imul mul lea` | a plane (or a saddle for `imul`) that wraps at 2^w | integers modulo 2^w | a polynomial of degree 1 or 2 with integer coefficients: `add` = a + b, `imul` = a·b, `lea (a,b,4)` = a + 4b |
| `and or xor not` | not smooth: `xor` at 8 bits is a nested checkerboard, every polynomial over the integers needs ~2^w terms | bits, arithmetic modulo 2 (each output bit as a polynomial in the input bits) | exact and tiny: `xor` = a + b bitwise, `and` = a·b bitwise, `or` = a + b + a·b bitwise, `not` = 1 + a |
| `shl shr sar`, `cmp/set*`, `movzx/movsx`, `cmov` | piecewise: flat regions separated by straight edges (the shift count, the comparison boundary) | piecewise linear over integers, with the pieces named by a condition | `sar` = floor(a / 2^k) on each piece k = b mod 32; `setl` = 1 where a < b else 0 |
| the float ones (`addss` … `cvtsi2sd`) | piecewise over the five float classes, with rounding steps inside | the IEEE field decomposition (log_228 §3): sign, exponent, significand as integers | polynomial in the fields on each piece, plus the rounding rule |

So the idea holds, with one precision: "interpolate" is exact fitting
in the right basis, and there are two bases, integers modulo 2^w and
bits modulo 2. Every opcode is a small fit in one of them, plus a
piece condition.

## 3. Composition of fits IS the term algebra

- f(g(x)) of two fits is a fit. The term the walk produces for an
  arch-unit is exactly this: opcodes composed, each an operation of
  §2. So the fit view and the term view are one object; the fit view
  adds the coefficients and the basis as data, which the term view
  does not carry.
- An emulation of opcode X in language y, in this view: a composition
  of y's operators' fits whose coefficients equal X's fit. Equality of
  two fits in the SAME basis is coefficient comparison, no solver.
  That is the gain the owner is sensing: within one basis, "does this
  composition emulate X" is arithmetic on coefficients, linear in the
  size of the composition.

## 4. The hard region, stated once (opinion, held to known results)

- A composition that mixes the two bases (an `add` followed by an
  `xor`, an `imul` then `and`) has no small fit in either basis: a
  single `add` written bitwise needs the carry chain, degree w; a
  single `xor` written modulo 2^w needs ~2^w terms. This is a known
  fact, the reason ARX ciphers (add, rotate, xor) resist algebra.
- So the fit route decides emulations cheaply inside one basis and
  falls back to the gate (z3, SAT on bits) when the emulation crosses
  bases. z3's bit-blasting is exactly "everything in the bit basis",
  which is why it always works and why it costs 2^w-ish for division.
- Measured today: of the 25 emulated singleton opcodes, every one
  lands in a single basis; the disproved pool-entry emulations (o13's
  95) are mostly mixed compositions. Not yet measured: how many of the
  162 opcodes' emulations across nine languages stay in one basis.

## 5. What the fuzz census already is

The fuzz census's sampled inputs are plotted points of the mapping.
A fit through them, checked against the reference's definition on all
2^w points, is the interpolation the owner describes; where a candidate fit
and the mapping differ, z3 returns the differing point exactly.

## 6. What to run, after the portable Airlock is on the server (no runs now)

1. The 162-row table from `reference.py`: mnemonic | widths | basis |
   the fit LITERAL | piece conditions | flags written | fault region.
   Definition work over existing code; the 2 unmodelled mnemonics named.
2. Per language, the fit of each compiler-operator at each width, from
   its own single-opcode or guarded unit (the same table for y's side).
3. For each of the 162 × 9 cells: search for a composition of y's fits
   equal to X's fit inside one basis (coefficient comparison); record
   FIT_FOUND / CROSSES_BASES / NO_OPERATOR; the CROSSES_BASES cells go
   to the gate as today.

## 7. Awaiting the owner

- Whether "fit" (the coefficients plus basis plus piece condition) is
  the name, and whether the 162-row table is the first artifact after
  the server is up.
