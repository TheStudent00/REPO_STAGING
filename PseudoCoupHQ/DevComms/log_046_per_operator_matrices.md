# log 046 — the settled per-operator matrices (2026-08-20)

## what was built

the owner ruled the per-operator-matrix design today (settled, recorded in
the dated section of
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_conversion_spec.md`).
Built the same day, assembly only — no probe runs, no lanes:

- `Research/kind_fuzz_clustering/l3_per_op_matrices.py` — the
  generator, reusing `l3_answers12.py`'s data files and parsing
  (answers_<lang>.json for the nine bit-grain languages;
  behavior_<lang>_C.json + manifest_<lang>.json for python/ruby/php)
  and `l3_matrix_extended.py`'s grapheme fallback and container
  decomposition.
- `Research/kind_fuzz_clustering/matrices/` — **242 CSVs**, one per
  `lang.op`, each rectangular at 19 columns, one PROBE per row;
  inputs (holder, value class, bytes-as-held, canonical, exact mant)
  filled on every row including REFUSE/RAISE/ABORT rows; outputs
  empty on non-value rows; indicator columns REFUSE/RAISE/ABORT plus
  raise_kind.
- `matrices/index.json` — per matrix: file, row count, holder count,
  value-row count, per-indicator counts.
- `matrices/README.md` — the filename escaping and the full reverse
  mapping.

Compile refusals come from `acceptance_<lang>_A2/A1.json` (the
answers files hold only the accepted subset); their inputs are filled
at the acceptance stage's representative value class (`BASE_ORDER` of
`l3_accept.py`). `codegen_refuse` rows in the answers files carry
their own value classes. The stopped-by-OS outcome is ABORT (480 such
rows in c++ alone); the OS return code stays in the answers file, the
matrix row carries the indicator.

## the escaping scheme

A word-spelled operator that is entirely letters keeps its spelling
with spaces as underscores (`python.not_in.csv`). Any other operator
is spelled character by character from a fixed table: `+`→plus,
`-`→minus, `*`→star, `/`→slash, `%`→percent, `<`→lt, `>`→gt, `=`→eq,
`!`→bang, `&`→amp, `|`→pipe, `^`→caret, `~`→tilde, `?`→q, `.`→dot,
`@`→at, `:`→colon. So `go.plus.csv`, `go.ltlt.csv`, `dart.tildeslash.csv`,
`php.ltegt.csv`. The reverse mapping for every one of the 242 files is
written in `matrices/README.md`; no two operators collide.

## sanity outputs (verbatim)

```
SANITY CHECKS
  [1] go.+ rows: 573 (value rows 180, REFUSE 393, RAISE 0, ABORT 0)
  [2] go.+ uint64 base_42+i64max_plus1 -> output 800000000000002a canonical [1, ~1.000000000000000005, 63]
  [2] go.+ uint64 i64max_plus1+base_42 -> output 800000000000002a canonical [1, ~1.000000000000000005, 63]
  [3] python.+ rows for the ordered pair base_42+i64max_plus1: 16 (4 holders x 4), RAISE=1: 2 [('decimal.Decimal', 'fractions.Fraction', 'TypeError'), ('fractions.Fraction', 'decimal.Decimal', 'TypeError')]
      both orderings: 32 rows, RAISE=1: 4
      behavior_python_C.json direct count: 32 cells, 4 RAISE
  [4] python.+ eacute lhs byte spellings in the probe set: ['c3a9'] (canonical ['[c3a9, 2, 1, 1]'])
  [5] rectangularity: 242 matrices, 0 non-rectangular, column count 19 everywhere else
```

Check [3] verified against `behavior_python_C.json` directly, as
ruled: the RAISE pair is exactly Decimal↔Fraction, TypeError, 2 of 16
per ordering. Check [4]: the probe set spells e-acute ONLY as NFC
(`c3a9`); no NFD spelling exists in the data, so the NFD→NFC merge
cannot be demonstrated on a real row — stated rather than invented.
`python: 178 BUDGET cells skipped (not an answer, not a refusal)` —
budget exhaustion is neither a value nor a refusal and gets no row.

## where the data resisted

- **Lone surrogates.** UTF-16 code-unit holders (java/kotlin/c#
  `char`) answer lone surrogate halves that are not encodable text.
  They are spelled `\uXXXX` inside the canonical rather than crashing
  or being dropped (`_desurrogate` in the generator).
- **NUL bytes.** A php printed payload carries a literal NUL, which
  csv cannot quote; it is spelled `\x00` on write.
- **c# `decimal` outputs (DEC128)** are carried as opaque canonical —
  the four-word bit layout's recorded order was not certified, and
  guessing it would invent precision. Inputs of the `decimal` holder
  ARE canonicalized (decimal-string-exact read-rule).
- **java/kotlin `BigDecimal` inputs** were confirmed decimal-string
  built (`new BigDecimal("{V}")` in
  `Research/data_representation/representations_*.json`), so their
  read-rule is decimal-exact (0.1 reads 1/10), while python
  `Decimal(0.1)`/`Fraction(0.1)` and ruby `Rational(0.1)` are built
  FROM the double and read the binary rational. Ruby
  `BigDecimal((v).to_s)` round-trips through the double's shortest
  print and reads decimal-exact.
- **swift carries only 6 operations** (`&& * < > >= ||`) in both its
  acceptance and answers artifacts — 6 matrices is the data, not a
  reader fault.
- **Acceptance REFUSE cells are holder-pair grain** (the verdict is a
  function of the holder pair, not the value — l3_accept.py's own
  ruling), so a REFUSE row's value class is the acceptance stage's
  representative (`BASE_ORDER`), recorded as such in the
  value-class column.

## the mant ruling, plainly

Integer mants were REJECTED because the decomposition is not unique —
`42 = 42×2^0 = 21×2^1 = 84×2^-1`. The settled canon is floating-point
normalization, mant ∈ [1,2), which is single-valued; the readable
decimal mant is rounded to 18 fractional digits and marked `~` when
inexact, with the exact rational mant in the machine column beside it.
