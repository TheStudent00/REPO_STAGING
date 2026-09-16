# log 285 — discovering primitive kinds from arch-unit meanings

2026-09-15, on the laptop (local, no tower, no lane). the owner: DISCOVERY of
primitive kinds. How much of the by-hand declaration of the kinds
(unsigned n, signed n, bool, IEEE (e, m), fixed-point, each a
constraint on the one numeric type (sign, mant, expo)) can be read off
the arch-units' Lean expressions alone, by a rule over the expression,
never by a name. Another session writes the kinds by hand in Lean. This
log is the other half: what the meanings already say.

## 1. walkthrough

Compiler-operators lower to arch-units. Arch-units are made of
arch-opcodes (RISC-V instructions). RISC-V instructions are expressed
in Lean via Sail, and so are arch-units: each certified walk row's
`proposal` is the unit's Lean expression over the argument registers
`a`, `b`, written with Sail's pure forms.

The rule does two things.

First it applies Sail's own definitions to the expression:

- each pure form's parameters are substituted
- its `match` takes the arm whose constructor is the argument's own text
- its lets are substituted
- any emitted definition the rule has no rule for (`zopz0zI_s`,
  `mult_to_bits_half`) is unfolded

It stops when only Sail's primitive vocabulary is left: `sign_extend`,
`zero_extend`, `extractLsb`, `to_bits_truncate`, `BitVec.toInt`,
`BitVec.toNatInt`, `bool_to_bit`, the three shifts, `Int.tdiv`,
`Int.tmod`.

Then it walks that expression from the top and carries one question
down every branch: how many low bits of this value does the context
read, and does it read the top bit as a sign? At every argument the
answer is written down. What an argument met is its kind. What the top
produces is the result's kind. Only after that is the kind set beside
the manifest's declared holder.

One unit end to end, go's `<` on int32:

| step | the text |
|---|---|
| meaning | `(pure_RTYPE ((pure_ADDIW (a) (0x000#12))) ((pure_ADDIW (b) (0x000#12))) (LeanIM.rop.SLT))` |
| Sail's definitions applied | `zero_extend (m := 64) (bool_to_bit ((BitVec.toInt (sign_extend (m := 64) (extractLsb a 31 0))) <b (BitVec.toInt (sign_extend (m := 64) (extractLsb b 31 0)))))` |
| `a`, `b` | a comparison reads a signed integer, the `sign_extend` takes bit 31 as the sign, the slice keeps 32 bits: `("signed", 32)` |
| result | one bit, zero-extended: `("bool",)` |
| declared | int32, int32, result bool: all three agree |

The rule never reads the unit's declared holders, its language, its
operator token or its instruction words. It reads only the meaning and
Sail's definitions.

## 2. the declared names

- `kind` is data, one of:
  - `("unsigned", n)`
  - `("signed", n)`
  - `("bool",)`
  - `("ieee", e, m)`
  - `("width", n)`: n bits, signedness undetermined
  - `None`: the meaning never reads it

  One mantissa bit, however it is reached, is `("bool",)`.
- `discover(meaning_text, pure_forms) -> {param: kind, "result": kind}`,
  in `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/leanpath/kinds.py`.
  `pure_forms` is a `Forms`, built with `strip.clauses_of` and
  `strip.propose` over the emit at
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM`
  (42 pure forms).
- `compare(found, declared) -> (verdict, cause)` compares in two
  coordinates: width and signedness class.
- The command is
  `python3 -m leanpath kinds <units.json> <walk.json[,...]> <out.json> [LeanIM dir]`,
  registered in `__main__.py`. It writes `runs/<corpus>/kinds.json`.

The rule at each edge:

| edge in the expression | what it says |
|---|---|
| `extractLsb x (k-1) 0` | x is read in its low k bits, and no more than the context reads |
| `x &&& (2^k - 1)` | x is read in its low k bits; `&&& 1` is one bit |
| `sign_extend (m := 64) x`, x of width w | x's w bits are read with bit w-1 as the sign; the value made is `("signed", w)` |
| `zero_extend (m := 64) x`, x of width w | read unsigned; the value made is `("unsigned", w)`; w = 1 is `("bool",)` |
| `BitVec.toInt x` / `BitVec.toNatInt x` | x is read signed / unsigned, **counted only if** an exact integer operation lies above it (`Int.tdiv`, `Int.tmod`, a comparison, a condition) or the final truncation is wider than x |
| `to_bits_truncate (l := n) e` | the result wraps at n; its sign is the counted sign of the readings below |
| `shift_bits_right_arith x s` / `shift_bits_right x s` | x is read signed / unsigned; s is read unsigned at its own width |
| `shift_bits_left x s`, `+ - * \|\|\| ^^^` | congruent mod 2^n: the width passes down, no sign; `&&&` also keeps the smaller significant width |
| `x <u 1`, `0 <u x`, `x == 0` on a bare argument | a truth reading: x is `("bool",)` |
| a Sail function that takes a `rounding_mode` | its operands are `("ieee", e, m)` by width; keyed by Sail's type, never by a function name |
| no argument anywhere | a constant meaning: the result is `None` |

The counting clause is why the multiply comes out right without a name.
Told `Signed`, Sail's `mult_to_bits_half` reads both operands with
`toInt`. But the low half truncates the product back to 64 bits, so
those readings do not count, and `a`, `b` are `("width", 64)`. Sail's
divide goes through `Int.tdiv`, so there the same readings do count.

The verdict for each parameter:

- **agree**: the same kind
- **undetermined**: the width agrees and the meaning never reads a
  sign; or the meaning never reads the parameter; or the holder is IEEE
  and the meaning never reaches a float edge
- **disagree**: the widths differ, or the meaning reads the opposite
  sign

## 3. the tables

### 3.1 parameters (units with a certified meaning only)

| language | units | with a certified meaning | parameters | agree | disagree | undetermined |
|---|---|---|---|---|---|---|
| c | 750 | 346 | 628 | 96 | 310 | 222 |
| cpp | 1002 | 418 | 796 | 96 | 425 | 275 |
| rust | 858 | 90 | 162 | 25 | 68 | 69 |
| go | 744 | 21 | 30 | 13 | 3 | 14 |

By cause:

| cause | c | cpp | rust | go |
|---|---|---|---|---|
| disagree: reads wider than the holder | 239 | 321 | 50 | 3 |
| disagree: reads narrower than the holder | 59 | 92 | 18 | 0 |
| disagree: reads the opposite sign | 12 | 12 | 0 | 0 |
| undetermined: width agrees, sign never read | 177 | 251 | 57 | 12 |
| undetermined: never read | 37 | 18 | 6 | 0 |
| undetermined: IEEE holder, no float edge | 8 | 6 | 6 | 2 |

What each disagreement is made of (declared holder, then what the
meaning reads):

| inside the cause | c | cpp | rust | go |
|---|---|---|---|---|
| wider: bool read as a 5 to 64-bit value (an `and`, `or`, `+`, a comparison at 64, a shift count) | 136 | 181 | 28 | 0 |
| wider: int32 read at 64 (the language's conversions, the calling convention's extension) | 103 | 140 | 22 | 3 |
| narrower: a truth reading of int32 / int64 / uint64 | 35 | 68 | 0 | 0 |
| narrower: a shift count read in its low 5 or 6 bits | 24 | 24 | 18 | 0 |
| opposite sign: int64 read unsigned beside a uint64 (C's usual arithmetic conversions) | 12 | 12 | 0 | 0 |

Where it agrees:

| declared | c | cpp | rust | go |
|---|---|---|---|---|
| int32 | 10 | 10 | 3 | 4 |
| int64 | 38 | 38 | 11 | 4 |
| uint64 | 48 | 48 | 11 | 4 |
| bool | 0 | 0 | 0 | 1 |

The width found right (agree plus sign never read): c 273 of 628, cpp
347 of 796, rust 82 of 162, go 25 of 30.

### 3.2 results

| language | results | declared as a primitive | agree | disagree | undetermined |
|---|---|---|---|---|---|
| c | 346 | 0 (the manifest leaves it to the compiler: `__typeof__`) | 0 | 0 | 346 |
| cpp | 418 | 0 (`auto`) | 0 | 0 | 418 |
| rust | 90 | 26 (the other 64 are 45 trait output projections and 19 ranges) | 18 | 8 | 64 |
| go | 21 | 21 | 8 | 3 | 10 |

- rust's 8 disagreements: bool results computed as a 64-bit `and`,
  `or` or `xor` of bool holders
- go's 3: int32 results the meaning leaves at 64 with no re-extension
  (unary `+`, `-`, `^`)
- go's 10 undetermined: int64 and uint64 results of congruent
  operations (8), and 2 float results never reached

Result kinds where nothing is declared:

| discovered result | c | cpp |
|---|---|---|
| bool | 117 | 159 |
| signed 32 | 30 | 30 |
| signed 64 | 12 | 12 |
| unsigned 64 | 16 | 16 |
| width 64 | 142 | 191 |
| constant meaning | 29 | 10 |

IEEE edges met: 0 units in all four corpora. The 64 distinct certified
meanings use eleven pure forms, and none of them is a float operation.
The rule could not read 0 units. `check_no_spelling_keys.py` passes on
all four `kinds.json`.

### 3.3 what discovery recovers, and what it cannot in principle

Recovered from the meaning alone:

- the width of a holder the operation slices or re-extends: 32 from
  `sign_extend (extractLsb x 31 0)`; 5 or 6 for a shift count
- the signedness of a holder read by an exact operation: divide,
  remainder, an ordered comparison, an arithmetic or logical right shift
- bool, from a truth reading of an argument, and from a comparison as a
  result
- the wrap width of a result: `to_bits_truncate (l := n)`, or a
  `sign_extend` of an n-bit value

Cannot be recovered, in principle:

- the signedness of a holder under a congruent operation (`+`, `-`, the
  low half of `*`, `&`, `|`, `^`, `<<`, negation). The meaning is the
  same function either way (c 177, cpp 251, rust 57, go 12).
- the SOURCE holder, where the language or the calling convention
  converts before the arch-unit's first instruction. An int32 or a bool
  arrives as a 64-bit register value. The meaning describes the holder
  the operation consumes, not the one written in the source.
- a parameter the meaning never reads: `sizeof`, a range's second bound,
  a float in a register the walk does not read
- a fixed-point scale. A fixed-point holder is an integer of the same
  width with an implied binary point, and no bit-level meaning carries
  the point. No rule was written, and none of the four corpora declares
  such a holder.

IEEE is missing in this run only, not in principle. The rule exists, but
no certified arch-unit reaches a float edge: the walk refuses the float
probes at decode, because the pruned decoder does not know their
instructions (log 284 §2: c 248, cpp 326, rust 24, go 22).

## 4. decided, recorded for audit

- The rule reads Sail's primitive vocabulary and the shape of the
  expression. An instruction's constructor is used only to pick Sail's
  own match arm, by textual identity. No table is keyed by a mnemonic or
  a token.
- Discovery reads `proposal` only. The walk row's `instructions` were
  allowed as an input and were not needed.
- A `toInt` / `toNatInt` reading sets the sign only under an exact
  integer operation or a wider truncation (the counting clause).
- `&&&` keeps the smaller significant width. A mask by `2^k - 1`
  narrows to k.
- One mantissa bit becomes `("bool",)`; `("width", 1)` is included.
- The truth reading is the owner's rule as stated: `sltiu x 1`, `0 <u x` and
  `x == 0` on a bare argument say `("bool",)`.
- A meaning with no argument in it is a constant, and its result is
  `None`.
- An IEEE holder whose meaning never reaches a float edge is undetermined
  (`ieee_not_reached`), not a disagreement, because the walk's meanings
  are over the integer registers.
- When both the width and the sign differ, the cause recorded is the
  width.
- The declared result is the manifest's `result_type`, read through the
  manifest's own holder table (type to rep). A trait output projection,
  a range or a pointer is not a primitive and is not compared. The c and
  cpp manifests declare no result.
- The IEEE rule is keyed by Sail's `rounding_mode` type.
- The parser fixes live in `kinds.py`; `lean_tree.py` is untouched:
  - a record literal `{ f := e, ... }` parses
  - an application stops at a keyword (`let`, `match`, ...)
  - a bare `=` is read as `==`
  - emitted bodies are joined line by line, because `strip.one_line`
    puts commas between `let` lines
- The outputs are
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/{handful_c,corpus_cpp,corpus_rust,corpus_go}/kinds.json`.

## 5. awaiting the owner

1. Re-extended 32-bit arguments. `sign_extend (extractLsb (a + b) 31 0)`
   reads `a` and `b` at 32 bits with no sign, so those int32 parameters
   stay undetermined (c 17, cpp 17, rust 10, go 2). The calling
   convention would call them signed 32; the meaning does not. Keep them
   undetermined, or add the convention as a rule?
2. The truth reading. As the rule stands, `!` and `&&` on int32, int64
   and uint64 discover bool and disagree (c 35, cpp 68). Keep it as a
   kind, or record a truth reading as its own finding that leaves the
   holder undetermined?
