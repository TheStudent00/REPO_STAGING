# operator variation breakdown — the arch campaign

Measured 2026-08-24 from `arch_units_{cpp,rust,go,swift}.json` (1652 OK
arch-units). Machine-readable copy: `operator_variation_counts.json`.

A **variation** is one arch-unit: `(operator, lhs type, rhs type)`. There
is no input-value axis — one compiled function covers every input, so a
variation is a shape, not a sample.

## Per language

| language | operator spellings | arch-units | overloaded (>1 variation) | single-variation | median variations per operator |
| --- | --- | --- | --- | --- | --- |
| cpp | 19 | 1157 | 19 | 0 | 65 |
| rust | 19 | 236 | 17 | 2 | 7 |
| go | 19 | 179 | 17 | 2 | 6 |
| swift | 6 | 80 | 4 | 2 | 15 |

Swift's 6 spellings are the whole of what the earlier behaviour census
admitted for it (`*`, `<`, `>`, `>=`, `&&`, `||`), not the whole of
Swift — its grammar admits 28 binary operators. So Swift's rows below
are a 22% sample of its operator surface, and its blanks mean "never
measured", never "does not exist".

## Why C++'s median is 65 and Rust's is 7

C++ permits mixed-type arithmetic through implicit conversion; Rust
refuses it. Measured on `+`:

| language | `+` variations | same-type | mixed-type |
| --- | --- | --- | --- |
| cpp | 83 | 9 | 74 |
| rust | 7 | 6 | 1 |
| go | 7 | 7 | 0 |

`int32_t + int64_t`, `bool + double`, `int32_t + float` all compile in
C++ and all produce their own machine code, because the language
converts one side first. `i32 + i64` does not compile in Rust and
`int32 + int64` does not compile in Go. One language design decision
accounts for the entire gap: 74 of C++'s 83 `+` variations are pairs
the other two languages reject outright.

C++'s `&&` and `||` reach 132 variations each for the same reason
amplified — every scalar and every pointer converts to `bool`, so
almost any pair of holders is a legal operand pair.

## Per operator, per language

| operator | cpp | rust | go | swift |
| --- | --- | --- | --- | --- |
| `!=` | 78 | 30 | 36 | – |
| `%` | 25 | 6 | 4 | – |
| `&` | 25 | 5 | 4 | – |
| `&&` | 132 | 1 | 1 | 1 |
| `&^` | – | – | 4 | – |
| `*` | 49 | 6 | 6 | 6 |
| `+` | 83 | 7 | 7 | – |
| `-` | 65 | 6 | 6 | – |
| `..` | – | 20 | – | – |
| `/` | 49 | 6 | 6 | – |
| `<` | 72 | 19 | 7 | 24 |
| `<<` | 25 | 16 | 16 | – |
| `<=` | 72 | 19 | 7 | – |
| `<=>` | 53 | – | – | – |
| `==` | 78 | 30 | 36 | – |
| `>` | 72 | 19 | 7 | 24 |
| `>=` | 72 | 19 | 7 | 24 |
| `>>` | 25 | 16 | 16 | – |
| `^` | 25 | 5 | 4 | – |
| `\|` | 25 | 5 | 4 | – |
| `\|\|` | 132 | 1 | 1 | 1 |

Operators with a single language column are language-only and can never
yield a cross-language comparison: Go's `&^` (and-not), C++'s `<=>`
(three-way compare), Rust's `..` (range).

## Comparable surface

Only a variation whose `(operator, type pair)` another language also
answers can be compared at all.

| language | arch-units | comparable variations |
| --- | --- | --- |
| cpp | 1157 | 137 |
| rust | 236 | 119 |
| go | 179 | 84 |
| swift | 80 | 40 |

C++ has the widest type coverage, so every other language's comparable
variations pair with C++: the pair totals are 119 (rust), 84 (go), 40
(swift), which is exactly those languages' comparable counts. C++'s own
137 is the deduplicated union of the three, which is why a matrix of
language PAIRS has denominators summing past 137 — one variation can
appear in up to three pair-cells.
