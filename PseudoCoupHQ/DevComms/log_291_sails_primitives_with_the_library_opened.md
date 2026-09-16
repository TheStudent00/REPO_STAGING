# log 291 — Sail's primitives with the library opened: the operators and operand types every RISC-V definition is built from

2026-09-15, evening. the owner: "the Sail compiler uses primitives to define
its model of RISCV. i want a list of those primitives. not the Lean
stuff. i want the operators and operand types that are used to construct
the entire RISCV definitions."

This is the Sail level, read from Sail's own sources. Log 289 counts the
names in Sail's LEAN OUTPUT; log 290 counts the model's own `val`
declarations with Sail's library unopened, and says so ("Sail's compiler
and its library are NOT on this machine ... anything below that rests on
the library file is marked unverified"). This log opens that library.
Every rendering is LITERAL (quoted, with its path) or GLOSS.

## 1. In plain words, before any number

An arch-opcode is a RISC-V instruction. Its definition in Sail is one
clause of the function `execute`. That clause is written with operator
symbols and function calls. Follow any of them down and you reach, in
four layers:

| layer | what it is | example | where |
|---|---|---|---|
| 1. the clause | one arch-opcode's definition | `execute RTYPE(rs2, rs1, rd, op)` | `model/extensions/I/base_insts.sail:237` |
| 2. the model's own helpers, written in Sail | `X`, `zero_extend`, `bool_to_bit`, `shift_bits_right_arith`, `<_s`, `<_u` | `model/prelude/prelude.sail`, `model/core/regs.sail:235` |
| 3. Sail's library functions, written in Sail | the library's own definitions over the atoms | `lib/*.sail` |
| 4. **the atoms** | a `val` with NO Sail body: every backend writes its own | `add_bits`, `and_vec`, `tdiv_int`, `lt_int` | `lib/vector.sail`, `lib/arith.sail`, `lib/flow.sail`, `lib/smt.sail` |

Layer 4 is the answer to the owner's question. Nothing under it exists in
Sail. A backend (C, Lean, Rocq, Isabelle, SMT) implements exactly these
and gets the whole RISC-V model for free.

## 2. The object, so the vocabulary is visible before it is counted

**LITERAL**, `SOURCES/sail-riscv/model/extensions/I/base_insts.sail`
lines 237 to 251 (commit `3243f93`, 2026-09-09):

```
function clause execute RTYPE(rs2, rs1, rd, op) = {
  X(rd) = match op {
    ADD  => X(rs1) + X(rs2),
    SLT  => zero_extend(bool_to_bit(X(rs1) <_s X(rs2))),
    SLTU => zero_extend(bool_to_bit(X(rs1) <_u X(rs2))),
    AND  => X(rs1) & X(rs2),
    OR   => X(rs1) | X(rs2),
    XOR  => X(rs1) ^ X(rs2),
    SLL  => X(rs1) << X(rs2)[log2_xlen - 1 .. 0],
    SRL  => X(rs1) >> X(rs2)[log2_xlen - 1 .. 0],
    SUB  => X(rs1) - X(rs2),
    SRA  => shift_bits_right_arith(X(rs1), X(rs2)[log2_xlen - 1 .. 0]),
  };
  RETIRE_SUCCESS
}
```

**GLOSS.** Ten arch-opcodes in one clause, chosen by the field `op`.
The vocabulary in it: the symbols `+ - & | ^ << >> <_s <_u`, the slice
`[hi .. lo]`, the `match`, and the calls `X`, `zero_extend`,
`bool_to_bit`, `shift_bits_right_arith`. Of those calls, all four are
the model's own Sail, layer 2. `X` is an overload:
`overload X = {rX_bits, wX_bits, rX, wX}` (`model/core/regs.sail:235`).
`<_s` and `<_u` are the model's too, declared `infix 4 <_s`
(`model/prelude/prelude.sail:146`) and written on top of `signed`,
`unsigned` and integer comparison. So this clause, the most-used one in
RISC-V, reaches the atoms only through the model's own prelude.

## 3. How this was counted, and what was read

| | |
|---|---|
| the model | `SOURCES/sail-riscv/model/`, commit `3243f93`, 170 `.sail` files, 34,181 lines |
| Sail's library | `/opt/opam/default/share/sail/lib/` inside the tower's `lp3-runner`, sail 0.20.2, copied out whole: 60 `.sail` files, 5,735 lines |
| the parser | every `val` declaration in both trees, joined across continuation lines, classified by whether its body is an extern or a Sail definition |
| the check | 0 declarations left unclassified; 156 wrap across lines, and 13 have their `=` on a continuation line, which any line-based grep misses |

Spellings of an external declaration found, so the rule's completeness
is visible:

| spelling | count |
|---|---|
| `val <n> = pure {backend: "..."} : T` | 208 |
| `val <n> = pure "..." : T` | 181 |
| `val <n> = impure "..." : T` | 31 |
| `val "<n>" : T` (old style, the name is the extern symbol) | 21 |
| `val <n> = impure {...} : T` | 16 |
| `val <n> = {...} : T` (no purity word) | 2 |

No `monadic`, no `$[extern]` attribute, in either tree.

## 4. The count

| | Sail's library | the model | total |
|---|---|---|---|
| `val` declarations | 485 | 285 | 770 |
| of them, external (a backend name, not Sail code) | 341 | 118 | 459 |
| of those, ALSO carrying a Sail body as a fallback | 34 | 33 | 67 |
| **true atoms: no Sail body anywhere** | **307** | **85** | **392** |

Where the 392 atoms live:

| file | atoms | what they are |
|---|---|---|
| `lib/float.sail` | 149 | IEEE floats, guarded by `!_FLOATING_POINT` |
| `model/core/softfloat_interface.sail` | 67 | the model's own SoftFloat hooks |
| `lib/vector.sail` | 46 | **bit vectors** |
| `lib/arith.sail` | 27 | **unbounded integers** |
| `lib/real.sail` | 19 | reals |
| `lib/string.sail` | 14 | strings |
| `lib/flow.sail` | 11 | **booleans and integer comparison** |
| `lib/regfp.sail` | 11 | register footprints |
| `model/prelude/prelude.sail` | 11 | the model's own platform hooks |
| `lib/concurrency_interface/emulator_memory.sail` | 7 | memory |
| `lib/mono_rewrites.sail` | 6 | monomorphisation rewrites |
| `lib/mapping.sail` | 5 | mappings |
| `model/sys/sys_reservation.sail` | 4 | the atomic reservation |
| `lib/smt.sail` | 3 | **flooring division** |

The four bold rows are the arithmetic and logic alphabet: **87 atoms**
(46 + 27 + 11 + 3). Everything an integer instruction computes is one of
those. The rest is float, string, real, memory and platform.

## 5. The atoms, with their operand types

### 5.1 Bit vectors — `lib/vector.sail`

| primitive | operand types | result |
|---|---|---|
| `add_bits` | `bits('n), bits('n)` | `bits('n)` |
| `add_bits_int` | `bits('n), int` | `bits('n)` |
| `sub_bits` | `bits('n), bits('n)` | `bits('n)` |
| `and_vec` | `bits('n), bits('n)` | `bits('n)` |
| `or_vec` | `bits('n), bits('n)` | `bits('n)` |
| `xor_vec` | `bits('n), bits('n)` | `bits('n)` |
| `not_vec` | `bits('n)` | `bits('n)` |
| `sail_shiftleft` | `bits('n), int` | `bits('n)` |
| `sail_shiftright` | `bits('n), int` | `bits('n)` |
| `sail_arith_shiftright` | `bits('n), int` | `bits('n)` |
| `bitvector_concat` | `bits('n), bits('m)` | `bits('n + 'm)` |
| `append_64` | `bits('n), bits(64)` | `bits('n + 64)` |
| `subrange_bits` | `bits('n), int('m), int('o)` | `bits('m - 'o + 1)` |
| `update_subrange_bits` | `bits('n), int('m), int('o), bits(...)` | `bits('n)` |
| `bitvector_access` | `bits('n), int('m)` | `bit` |
| `bitvector_update` | `bits('n), int('m), bit` | `bits('n)` |
| `slice` | `bits('m), int('o), int('n)` | `bits('n)` |
| `sail_sign_extend` | `bits('n), int('m)` | `bits('m)` |
| `sail_zero_extend` | `bits('n), int('m)` | `bits('m)` |
| `truncate` | `bits('n), int('m)` | `bits('m)` |
| `truncateLSB` | `bits('n), int('m)` | `bits('m)` |
| `replicate_bits` | `bits('n), int('m)` | `bits('n * 'm)` |
| `sail_zeros` | `int('n)` | `bits('n)` |
| `sail_mask` | `int('len), bits('v)` | `bits('len)` |
| `eq_bits` | `bits('n), bits('n)` | `bool` |
| `neq_bits` | `bits('n), bits('n)` | `bool` |
| `eq_bit` | `bit, bit` | `bool` |
| `unsigned` | `bits('n)` | `range(0, 2^'n - 1)` |
| `signed` | `bits('n)` | `range(-2^('n-1), 2^('n-1) - 1)` |
| `bitvector_length` | `bits('n)` | `int('n)` |
| `count_leading_zeros` | `bits('N)` | `int('n)`, `0 <= 'n <= 'N` |
| `count_trailing_zeros` | `bits('N)` | `int('n)`, `0 <= 'n <= 'N` |
| `get_slice_int` | `int('w), int, int` | `bits('w)` |
| `set_slice_int` | `int('w), int, int, bits('w)` | `int` |
| `set_slice_bits` | `int('m), bits('n), int, bits('m)` | `bits('n)` |
| `vector_length` | `vector('n, 'a)` | `int('n)` |
| `vector_init` | `int('n), 'a` | `vector('n, 'a)` |
| `plain_vector_access` | `vector('n, dec, 'a), int('m)` | `'a` |
| `plain_vector_update` | `vector('n, dec, 'a), int('m), 'a` | `vector('n, dec, 'a)` |
| `to_bytes_le` | `bits(8 * 'n)` | `vector('n, bits(8))` |
| `from_bytes_le` | `vector('n, bits(8))` | `bits(8 * 'n)` |

### 5.2 Unbounded integers — `lib/arith.sail` and `lib/smt.sail`

| primitive | operand types | result |
|---|---|---|
| `add_int` | `int, int` | `int` |
| `add_atom` | `int('n), int('m)` | `int('n + 'm)` |
| `sub_int` | `int, int` | `int` |
| `sub_atom` | `int('n), int('m)` | `int('n - 'm)` |
| `sub_nat` | `nat, nat` | `nat` |
| `mult_int` | `int, int` | `int` |
| `mult_atom` | `int('n), int('m)` | `int('n * 'm)` |
| `negate_int` | `int` | `int` |
| `negate_atom` | `int('n)` | `int(-'n)` |
| `tdiv_int` | `int, int` | `int`, toward zero |
| `_tmod_int` | `int, int` | `int`, toward zero |
| `_tmod_int_positive` | `int, int('n)` | `nat` |
| `ediv_int` | `int('n), int('m)` | `int(div('n,'m))`, flooring |
| `emod_int` | `int('n), int('m)` | `int(mod('n,'m))` |
| `pow2` | `int('n)` | `int(2^'n)` |
| `_shl_int` | `int, int('n)` | `int` |
| `_shr_int` | `int, int('n)` | `int` |
| `_shl1`, `_shl8`, `_shl32`, `_shr32` | `int('k), int('n)` | `int`, in a named set |
| `abs_int_plain` | `int` | `int` |
| `abs_int_atom` | `int('n)` | `int(abs('n))` |
| `max_int` | `int('x), int('y)` | `int('z)` |
| `min_int` | `int('x), int('y)` | `int('z)` |

**LITERAL**, the one every divide instruction reaches,
`/opt/opam/default/share/sail/lib/arith.sail` (copied to this session's
scratchpad), and the model's own wrapper,
`SOURCES/sail-riscv/model/prelude/prelude.sail:44`:

```
val quot_round_zero = pure {interpreter: "quot_round_zero", lem: "hardware_quot",
  c: "tdiv_int", cpp: "tdiv_int", rocq: "Z.quot", lean: "Int.tdiv"}
  : forall 'm, 'm != 0 . (int, int('m)) -> int
```

**GLOSS.** One primitive, six backend spellings. The C simulator calls
GMP's truncating division; Lean gets `Int.tdiv`; Rocq gets `Z.quot`.
Nothing here is a machine instruction: the width enters later, at
`to_bits_truncate`.

### 5.3 Booleans and integer comparison — `lib/flow.sail`

| primitive | operand types | result |
|---|---|---|
| `and_bool` | `bool('p), bool('q)` | `bool('p & 'q)` |
| `or_bool` | `bool('p), bool('q)` | `bool('p \| 'q)` |
| `not_bool` | `bool('p)` | `bool(not('p))` |
| `and_bool_no_flow` | `bool, bool` | `bool` |
| `eq_bool` | `bool, bool` | `bool` |
| `eq_unit` | `unit, unit` | `bool(true)` |
| `eq_int` | `int('n), int('m)` | `bool('n == 'm)` |
| `neq_int` | `int('n), int('m)` | `bool('n != 'm)` |
| `lt_int` | `int('n), int('m)` | `bool('n < 'm)` |
| `gt_int` | `int('n), int('m)` | `bool('n > 'm)` |
| `lteq_int` | `int('n), int('m)` | `bool('n <= 'm)` |
| `gteq_int` | `int('n), int('m)` | `bool('n >= 'm)` |

## 6. The operators, and what each one resolves to

119 bindings, 59 distinct symbols, from `overload operator X = {...}`
and `infix N <sym>` in both trees. The ones an integer instruction uses:

| symbol | resolves to | operand types |
|---|---|---|
| `+` | `add_bits` | `bits('n), bits('n)` |
| | `add_bits_int` | `bits('n), int` |
| | `add_int` / `add_atom` | `int, int` |
| | `regidx_offset` (model, Sail) | a register index and a number |
| `-` | `sub_vec` | `bits('n), bits('n)` |
| | `sub_vec_int` | `bits('n), int` |
| | `sub_int` / `sub_atom` | `int, int` |
| `*` | `mult_int` / `mult_atom` | `int, int` |
| `/` | `quot_positive_round_zero` | `int('n), int('m)` |
| `%` | `rem_positive_round_zero` | `int('n), int('m)` |
| `&` | `and_vec` | `bits('n), bits('n)` |
| | `and_bool` | `bool, bool` |
| `\|` | `or_vec` | `bits('n), bits('n)` |
| | `or_bool` | `bool, bool` |
| `^` | `xor_vec` | `bits('n), bits('n)` |
| | `concat_str` | `string, string` |
| `~` | `not_vec` | `bits('n)` |
| | `not_bool` | `bool` |
| `<<` | `shift_bits_left` | `bits('n), bits('m)` |
| | `sail_shiftleft` | `bits('n), int` |
| `>>` | `shift_bits_right` | `bits('n), bits('m)` |
| | `sail_shiftright` | `bits('n), int` |
| `<<<` / `>>>` | `rotate_bits_left` / `rotate_bits_right` (model, Sail) | `bits('n), bits('m)` |
| `==` | `eq_bits`, `eq_int`, `eq_bool`, `eq_anything`, `eq_string`, `eq_unit`, `eq_real` | by type |
| `!=` | `neq_bits`, `neq_int`, `neq_anything`, `neq_bool` | by type |
| `<`, `<=`, `>`, `>=` | `lt_int`, `lteq_int`, `gt_int`, `gteq_int` | `int('n), int('m)` |
| `<_s`, `<=_s`, `>_s`, `>=_s` | the model's own, `infix 4`, on `signed` + integer compare | `bits('n), bits('n)` |
| `<_u`, `<=_u`, `>_u`, `>=_u` | the model's own, `infix 4`, on `unsigned` + integer compare | `bits('n), bits('n)` |
| `@` | the model's own append | `bits('n), bits('m)` |

The signed and unsigned bit-vector comparisons are NOT atoms. They are
written in the model's prelude over `signed`/`unsigned` and integer
comparison. So `SLT` and `SLTU` reach the atoms as an integer question,
not a bit-vector one, which is why they were the last cells to close at
the fixed width (log 278 §7.5).

## 7. What the 412 arch-opcode definitions actually use

Measured over every `function clause execute` body: 412 clauses, 61
files, 8,805 lines.

| operator | in the clauses | in the whole model |
|---|---|---|
| `\|` | 480 | 947 |
| `-` | 361 | 620 |
| `==` | 281 | 1,303 |
| `+` | 273 | 458 |
| `*` | 226 | 390 |
| `^` | 196 | 2,963 |
| `..` (a slice) | 185 | 805 |
| `&` | 103 | 1,451 |
| `<=` | 91 | 382 |
| `>>` | 72 | 92 |
| `@` | 59 | 2,946 |
| `>=` | 50 | 222 |
| `<<` | 49 | 69 |
| `<` | 47 | 172 |
| `!=` | 43 | 227 |
| `/` | 41 | 62 |
| `>` | 37 | 144 |
| `>>>` | 30 | 52 |
| `~` | 18 | 35 |
| `<<<` | 14 | 34 |
| `<_u` | 5 | 14 |
| `<_s` | 5 | 8 |
| `%` | 3 | 30 |
| `>_s` | 2 | 5 |

31 distinct operator symbols in the whole of RISC-V. The control forms,
16 of them: `let` 2,245, `if`/`then` 498 each, `match` 235, `else` 220,
`return` 204, `assert` 183, `foreach` 153, `var` 142, `struct` 2.

The most-called functions, which are layer 2 and 3, not atoms:

| function | in the clauses |
|---|---|
| `not` | 358 |
| `X` (a register read or write) | 345 |
| `read_vreg` | 241 |
| `Illegal_Instruction` | 210 |
| `zeros` | 190 |
| `unsigned` | 170 |
| `zero_extend` | 131 |
| `sign_extend` | 114 |
| `signed` | 88 |

336 distinct functions are called across the clauses. The vector
extension dominates the list (`read_vreg`, `get_sew`, `get_lmul_pow`,
`valid_reg_group`), which is why the count is 336 and not 50.

## 8. The operand types

Every operand type in the model bottoms out in a small closed set:
`bits('n)`, `bit`, `int`, `int('n)`, `nat`, `range(a, b)`, a set type
like `{1, 2, 4, 8}`, `bool`, `unit`, `string`, `real`, and
`vector('n, T)`. On top of those the model declares:

| kind | count | examples |
|---|---|---|
| type aliases | 57 | `type xlenbits = bits(xlen)`, `type regtype = xlenbits`, `type word = bits(32)`, `type word_width = {1, 2, 4, 8}` |
| enumerations | 299 | `enum rop = {ADD, SUB, SLL, SLT, SLTU, XOR, SRL, SRA, OR, AND}` |
| newtypes and structs | 19 | `newtype regidx`, `struct mul_op` |

The types that appear most often in the clause parameter lists:

| type | in the clauses |
|---|---|
| `regidx` | 355 |
| `vregidx` | 278 |
| `bits('n)` | 235 |
| `vector('n, bits('m))` | 230 |
| `fregidx` | 204 |
| `bits(1)` | 91 |
| `bool` | 55 |
| `bits(5)` | 45 |
| `bits(32)` | 43 |
| `bits(12)` | 35 |
| `xlenbits` | 25 |
| `int` | 25 |
| `bits(64)` | 21 |

**The widths are not literals.** LITERAL,
`SOURCES/sail-riscv/model/core/xlen.sail:13` and `:16`:

```
type xlen : Int = config base.xlen
type log2_xlen  : Int = if xlen == 32 then 5 else 6
```

**GLOSS.** The register width is a type-level integer read from the
configuration file, and every width in the model is an expression over
it. That is why one clause serves RV32 and RV64, and why a proof about
a clause is a proof for every width the configuration allows.

## 9. What this changes for the line

- The alphabet an arch-opcode's definition is built from is **87 atoms**
  for integer work: 46 bit-vector, 27 integer, 11 boolean, 3 flooring.
  A backend that implements those 87 has every integer instruction.
- `<_s` and `<_u` are the model's own Sail, not atoms. Anything that
  wants them at the bit level must unfold through `signed`/`unsigned`
  into an integer comparison first.
- The float wall is structural, not incidental: 216 of the 392 atoms
  are float (149 in Sail's library, 67 in the model's SoftFloat hooks).
  They are more than half the alphabet and none of them is arithmetic
  we can decide.

## 10. Two lists

Decided, recorded for audit:

- Sail's library was copied out of the tower's `lp3-runner` whole (60
  files, sail 0.20.2) into this session's scratchpad; nothing was
  written into `SOURCES` or into the repo but this log;
- the parse left 0 declarations unclassified, and the 13 whose `=` sits
  on a continuation line are counted, which a line-based grep misses;
- this log is the Sail level; log 289 is the Lean level; log 290 is the
  model half with the library unopened.

Awaiting the owner:

- whether Sail's library belongs in the repo as a reference copy, so a
  later session does not have to reach into a container for it.

## 11. Pointers

- the model: `SOURCES/sail-riscv/model/`, commit `3243f93`
- Sail's library, as copied: `/opt/opam/default/share/sail/lib/` in the tower's `lp3-runner`, sail 0.20.2
- the extraction: `primitives.json` (459 records, each with its type, its backend map, whether it has a Sail fallback, and its `$ifdef` guard), `operator_bindings.json` (119), `usage_execute_clauses.json`, `usage_whole_model.json`, `execute_clauses.json` (all 412 bodies), and the two parsers, in this session's scratchpad
- the clause quoted in §2: `SOURCES/sail-riscv/model/extensions/I/base_insts.sail:237`
