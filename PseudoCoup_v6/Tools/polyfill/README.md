# polyfill (T4)

The wrapper layer filling target-behavior gaps so transpiled code matches
source behavior exactly. Plan node:
`PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_2_polyfill/`
(id `pcv6.tools.t4_polyfill`). Governing law, non-negotiable: **uniform
wrapping, no exemptions -- every operator on a polyfilled type routes
through the wrapper, or none do.** Mixed depth is forbidden because an
unwrapped node becomes ambiguous between "proven safe" and "tool missed
it."

- `wrap_fixed_width.py` -- the wrapper layer: fixed-width integer types
  `u8/u16/u32/u64/i8/i16/i32/i64`, both as PCv5-style plain functions
  (`u8(x)`, `i8(x)`, ...) and as classes (`U8`, `I8`, ...) whose dunder
  methods ARE the operator routing (arithmetic wraps silently, `&|^~`
  are signedness-invariant at matched width, `>>` is logical for
  unsigned / arithmetic for signed, `//`/`%` truncate toward zero for
  signed operands, comparisons diverge unsigned-vs-signed on the same
  bit pattern exactly as Rust's do).
- `check_uniformity.py` -- the enforcement check: given a Python module
  (source text or an `ast.Module`), finds every value annotated or
  assigned as one of the eight wrapper types and reports any
  arithmetic/bitwise/shift/comparison operator touching it that is not
  itself directly wrapped (or part of an associative same-operator
  chain whose outermost link is wrapped -- see the docstring for why
  `A | B | C` needs one outer wrap while `(A & B) << C` needs both
  wrapped individually, each traced to a harvested transpile's own style).
- `test_polyfill.py` -- acceptance (this tool's oracle): 68/68 at
  graduation (2026-07-28, sandbox) -- a differential grid (every
  wrapper type x every operator) against an oracle re-derived from
  arbitrary-precision Python ints plus explicit `%`-mask/sign-extend
  written fresh in the test file (never by importing and reusing
  `wrap_fixed_width`'s own `_wrap`/`_trunc_div`), covering type
  max/min, `-1`, `0`, shift-by-0, shift-by-(width-1), signed
  division/remainder truncation, and unsigned wraparound; plus
  `check_uniformity` against a uniform and a deliberately non-uniform
  sample, both modeled on a harvested transpile's real `encode_modrm`.

Run acceptance:

```bash
python3 -m pytest PseudoCoup_v6/Tools/polyfill -q
```

Full stack (with the other three T1-T3 tools):

```bash
python3 -m pytest \
  PseudoCoup_v6/Tools/ledgerer/tree_sitter \
  PseudoCoup_v6/Tools/ledgerer \
  PseudoCoup_v6/Tools/transpiler \
  PseudoCoup_v6/Tools/polyfill -q
```

Both commands measured 2026-07-28 (sandbox): `polyfill` alone 68/68;
the four-tool stack 99/99 in one run.

## Provenance (exact source, per ported/derived semantic)

| Semantic | Source | Note |
|---|---|---|
| `u8(x) = x & 0xFF`, `u32(x) = x & 0xFFFFFFFF`, the nested `u8(u8(u8(...)) ...)` uniform-wrap style, `CodeSink.put1/2/4/8` | a retired reference backend's Rust support-layer transpile (since removed as mis-aimed) | byte-identical at the time of harvest; this is the primary semantic source and the worked positive/negative example both `check_uniformity.py` and `test_polyfill.py` build their fixtures from (`encode_modrm`). |
| `i8(x)` mask-then-sign-extend | the same retired reference backend's transpile (byte-identical body also inlined in the sibling transpiler's `POLYFILLS` template) | byte-identical at the time of harvest. |
| generalized mask+sign-extend at arbitrary bit width (`_wrap(v, bits, signed)`) | `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/runtime/numbers.py:25-29` (`_wrap(v, bits)`) | this is the exact file the T4 plan node cites as harvest ("v0 `runtime/numbers.py` (fixed-width at literals)"). `u8`/`i8`/`u32` above are this formula's `bits=8`/`bits=32` special cases. **Generalization, not a semantic change**: v0's version always sign-extends (its docstring marks unsigned ints/`ushr` as an unimplemented refinement); a `signed` parameter was added so one formula covers both `u*` and `i*`. |
| signed truncating division/remainder (toward zero, dividend's sign) | `StressBot/.../runtime/numbers.py:32-40` (`_tdiv`/`_tmod`), byte-identical formula in `PseudoCoup_v5/Research/divergence_suite/class_1_value_model.py:21-23` (`trunc_div`) | ported formula; divide-by-zero raises Python's native `ZeroDivisionError` here rather than v0's Kotlin-flavoured `ArithmeticException` class (matching `rust_cell.py`'s own precedent of representing a trap as a raised Python exception). |
| arithmetic vs. logical right shift chosen by signedness | doctrine: `PseudoIR/DevComms/compiler_transpilation_experiment.md`, section 3's divergence table (`0xFF00000000000000 >> 60` = 15 logical / -1 arithmetic) and section 5's Map/Wrap/Fail rule | **not present in any harvested PCv5/v0 source** -- v0's `numbers.py` only ever implements arithmetic shift (Kotlin has no unsigned int in that file); the retired reference backend's transpile only ever shifts small non-negative register-encoding ints, never exercising the signed/unsigned divergence. Implemented directly from the doctrine + Rust reference semantics; checked in `test_polyfill.py` against the doctrine's own worked numbers. |
| explicit outbound crossing (`__int__`), refusing silent cross-width/cross-signedness mixing | `PseudoCoup_v5/Research/rust_routing/rust_cell.py` (`RustI64`: `"int(x) outbound: explicit, allowed"`) | border-discipline pattern ported; **deviation**: `rust_cell.py` refuses ALL bare Python operators on its wrapped cell (forcing an explicit `r.+`-style call); here the operator dunder methods themselves ARE the wrapper, so `a + b` between two `U8` instances already satisfies "routes through the wrapper" by CORE_0_0_3's own definition. `check_uniformity.py` exists for the case `rust_cell.py`'s stricter design prevents structurally: a value that carries polyfilled provenance but has escaped into (or never entered) wrapped form. |
| bitwise `&`/`|`/`^`/`~` signedness-invariance at matched width | doctrine section 3 (corrects the original report's claim that `~`/`&` corrupt a `uint64_t` at 64-bit width) | verified directly in `test_polyfill.py::test_bitwise_signedness_invariant_at_matched_width`, not merely assumed from the doctrine text. |

## Recorded deviations

1. **`MIN / -1` does not trap.** Real Rust panics on signed integer
   division overflow (`MIN / -1`) unconditionally, even in release
   builds. No harvested PCv5 or v0 source special-cases this. This
   module's uniform "mask the result of every operator" policy (the
   same policy the retired reference backend's transpile applied
   throughout its own `u8()`/`u32()`) silently wraps that case back to
   `MIN` instead of trapping. Deliberate scope decision, pinned by
   `test_min_over_neg_one_wraps_silently_recorded_deviation` in
   `test_polyfill.py` rather than hidden.
2. **Division by zero raises `ZeroDivisionError`**, not v0's
   `ArithmeticException`. Kotlin's exception hierarchy isn't being
   reproduced here, only the numeric semantics; `ZeroDivisionError` is
   Python's native representation of the same trap, consistent with
   `rust_cell.py`'s own precedent (`OverflowError` on an out-of-range
   literal).
3. **Cross-type mixing is refused, not coerced.** `U8(1) + U16(1)`
   raises `TypeError` rather than silently widening one operand --
   silent cross-width mixing is exactly the ambiguity CORE_0_0_3
   forbids. An explicit `.cast(cls)` method exists for the deliberate
   crossing.
4. **Unary `-` on unsigned types is refused**, matching Rust (no `Neg`
   impl for `u8`/.../`u64`); on signed types it wraps like every other
   operator here (`-I32(I32.MIN)` wraps back to `I32.MIN`, not a trap).

## check_uniformity scope (recorded limitation)

A name is "polyfilled" only if it is annotated with a wrapper type
(`x: u8`), or assigned directly from a wrapper call/another polyfilled
name. Statically inferring that an un-annotated, dynamically-typed
Python variable is "secretly" `u8`-typed by convention alone (PCv5's
own un-annotated style, e.g. `encode_modrm`'s bare `m0d`, `enc_reg_g`,
`rm_e` parameters) is undecidable in general Python and out of scope --
annotate to bring a value under this check. See the module docstring
for the full reasoning, including why an associative same-operator
chain (`A | B | C`) only needs one outer wrap while two different
operators stacked directly (`(A & B) << C`) each need their own.

## What remains open

- Only the eight wrapper types named in the CORE_0_0_3 plan node
  (`u8/u16/u32/u64/i8/i16/i32/i64`) exist. Per that node, "the wrapper
  SET grows per source-grammar need, discovered by T1's census" --
  no ingestor has yet requested a type outside this set.
  `wrap_fixed_width.FUNCS`/`TYPES` are the two registries a future
  ingestor would extend.
  - `u16`/`u64`/`i16`/`i32`/`i64` are not literally present in any
    harvested PCv5 source (only `u8`/`u32`/`i8` are) -- they are the
    same ported formula (`_wrap`) at the widths the doctrine's growth
    rule calls for next, not yet exercised by a live ingestor.
- `check_uniformity.py` is not wired into any ingestor's build path
  yet (T3's Rust/LLVM ingestors do not currently emit
  `wrap_fixed_width`-style code); it is a standalone, independently
  runnable checker until an egress renderer produces polyfilled output
  to check.
