# log 044 — the extended clustering matrix and its conversion spec

2026-08-20. Node: `Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering`.
**No probe ran and no lane ran** — everything here is assembly over the
layer-3 answer data already on disk, loaded through `l3_answers12.py`'s
own `load_three`/`load_nine` so the canonical token space is the one
`clusters_all12.json` stands on.

## 1. what was built

the owner ruled the extended-matrix design today; it is recorded as SETTLED
in a new node SUPPORT file and implemented the same day.

- `Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_conversion_spec.md`
  — the design: base 64-row form-pair × lang.op matrix with `refuse`,
  `raise` and `not-applicable` as first-class distinct cell elements;
  three extension layers (numeric [sign | mantissa | exponent |
  special] on an unbounded EXACT cast, container [sorted values | key
  format | order flag] on a dict-list cast, text [utf-8 bytes |
  codepoints | graphemes | NFC]); wrap congruences recorded as
  FEATURES; and the governing rule quoted: *never compare raw answers,
  compare their decompositions, and let WHICH coordinate disagrees be
  the feature.*
- `Research/kind_fuzz_clustering/l3_matrix_extended.py` — the
  assembler, in the l3_* family, reusing the existing loaders rather
  than re-parsing anything.
- `Research/kind_fuzz_clustering/matrix_extended_base.csv` — the base
  matrix, rectangular and spelling-blind: cell = sorted set of answer
  forms joined by `+`, or `REFUSE`.
- `Research/kind_fuzz_clustering/matrix_extended.json` (26.7 MB) — the
  extension coordinates at the value-pair grain, INTERNED: each of the
  6,155 distinct canonical tokens is decomposed once in
  `token_decompositions`, `cells` maps column → input cell → token
  list, and `congruences` lists every detected wrap relation.

## 2. sanity checks, as printed

```
  base matrix: 64 rows x 239 columns -> .../matrix_extended_base.csv
  cells: 6863 filled, 8433 REFUSE, 15296 total
  6155 distinct canonical tokens decomposed in 0.1 s
  63111 congruences (wrap relations) recorded
SANITY CHECKS
  [1] matrix dimensions: 64 rows x 239 columns
  [2] go.+ non-REFUSE cells: 3 -> ['fractional|fractional',
      'text|text', 'whole|whole']
  [3] 2^64 congruence on (i64max, base_42) touching go.+: 9 pairs
      go.+ ~ python.+ : whole:-9223372036854775767 vs
                        whole:9223372036854775849  === mod 2^64
      go.+ ~ go.+     : whole:-9223372036854775767 vs
                        whole:9223372036854775849  === mod 2^64
```

The planned checks read: dimensions PASS at 64 rows, with the column
count at **239 rather than the design conversation's 233** — 233 is
the log-030-era signature count and logs 034/035 admitted the
word-spelled operations since; the matrix follows the data on disk.
`go.+` PASS, exactly 3 non-refuse cells and they are the three named.
The 2^64 congruence between go's int64 and uint64 holders on
(i64max, base_42) PASS — detected both WITHIN `go.+` (the go.+ ~ go.+
line) and against python's `whole:9223372036854775849`.

## 3. worked examples, quoting real cells

- **Wrap as a feature.** `whole|i64max|whole|base_42` under `go.+` is
  the two-token set `{whole:-9223372036854775767,
  whole:9223372036854775849}`; the decomposition reads sign −1 /
  exponent 62 against sign +1 / exponent 63 with exact values
  9223372036854775767 and 9223372036854775849, and the assembler
  records `≡ mod 2^64` nine ways across cpp, csharp, go, kotlin,
  python and ruby instead of nine mismatches.
- **Containers made comparable.** `sequence|empty|sequence|strs`:
  `ruby.<<` on a Set holder answers `keyed:{#<Set:{'a','b'}>}` and
  `python.+` answers `sequence:['a','b']` — canonicalized, BOTH read
  sorted_values `['text:61','text:62']`, and only the order flag
  differs (`unordered` against `as-sorted`). The sort makes them
  comparable; the flag preserves what the sort destroyed.
- **Precision not invented.** `php.+` on the same i64max cell answers
  `fractional:9.2233720368548e+18` beside `raise:Error`; its exact
  cast is 9223372036854800000, which is congruent to nothing mod any
  `2^w` — php's printer destroyed the low digits before recording,
  and the exact cast preserves precision without re-inventing it. The
  disagreeing coordinate is the mantissa at exponent 63, which is
  precisely the feature.
- Three base rows, verbatim (truncated at the page edge):

```
truth|truth,truth,ABORT+whole,whole,truth,whole,whole,whole,ABORT+whole,...
whole|whole,truth,ABORT+whole,whole,truth,whole,whole,whole,ABORT+whole,...
text|text,truth,REFUSE,REFUSE,truth,REFUSE,sequence+text,whole,REFUSE,...
```

## 4. where the data resisted the design

- **239 against 233** — stated above; the design sentence carried a
  stale count and the data won.
- **`abort` is in the data and the design named only refuse and
  raise.** c++'s `SIGFPE` and segfault rows are real answers-in-kind;
  `ABORT` is carried as a first-class cell element beside `RAISE`
  (visible in `truth|truth` above, `cpp.%` = `ABORT+whole`).
- **Ruby's inspect-grain container spellings.** Set tokens
  (`#<Set:{...}>`) and the word spellings `true`/`nil` are normalised
  before the literal parse; ruby's Struct/data inspect forms
  (`#<structa='a',...>`) are LEFT unparsed on purpose, their container
  coordinates reading the unparsed marker — **938 of 2,188 container
  tokens**, almost all Struct/data/opaque-bearing, counted rather than
  papered over.
- **Print-grain floats cannot be exactly decomposed past their
  printer.** The exact cast is exact of the PRINTED form (the php
  example above); 10 numeric tokens did not parse at all and carry an
  `unparsed` special.
- **The congruence floor is a judgment.** `w ≥ 8` keeps a difference
  of 2 or 4 reading as arithmetic; 63,111 congruences survive it,
  dominated by w = 63 (33,552), w = 64 (16,219) and w = 53 (8,337) —
  the two's-complement walls and the double-mantissa wall surfacing
  by themselves. 22 sit at w = 2646, which is bignum `**` territory.
- **Refuse conflates two silences in the base CSV.** A never-probed
  pair and a probed-and-declined pair both read `REFUSE` at the form
  grain; the JSON's cells distinguish them by presence.

## 5. bookkeeping

PROGRESS carries a dated entry. CHECK has no matching open item for
this deliverable (it is today's ruling, not a planned phase item), so
CHECK is untouched.

---

## postscript, 2026-08-20 (same day) — two rulings applied

the owner ruled on the two open items and one wording ban; the assembler
was patched and re-run. Numbers above stand except where restated
here.

- **The word `death`/`DEATH` is banned** (the owner: he hates death/kill
  wording). The cell element is now **`ABORT`**: the operating
  system stopped the probe's process with no language-level error
  (c++ `SIGFPE` on `%` by zero is the standing example). The
  internal token prefix in the answers files remains `death:` —
  third-party-style data, quoted as is; only our vocabulary changed.
- **REFUSE is split from UNPROBED in the base CSV.** First attempt
  found 0 REFUSE — the answers files hold only the ACCEPTED subset,
  so refusal evidence had to come from the acceptance files
  (`acceptance_<lang>_A2/A1.json`), now loaded by
  `load_probed_pairs()`. Result: **8,145 REFUSE / 288 UNPROBED /
  6,863 filled**. REFUSE = the acceptance stage probed the form pair
  and the language declined it (egress-relevant: a measured gap that
  needs polyfill). UNPROBED = no probe ever asked (no claim). The
  288 UNPROBED sit in the three C-route languages, which have no
  acceptance files.
- Congruence floor w >= 8 left as is (the owner reviewing; mass at
  53/63/64 regardless).

---

## postscript 2, 2026-08-20 — wrap detection moved into the owner's coordinates

the owner's correction: the detector compared RAW signed values (difference
= 2^w), which is exactly what the governing rule forbids. In
[sign, mant, expo] space the separation of a signed wrap lives in
the SIGN dimension — the mants stay close (82 apart in the go/python
case) while their SUM is exactly the modulus.

Two spellings now, both inside the decomposition, labeled apart:

- **signed wrap**: sign flip AND |a| + |b| = 2^w
  (go int64 `-9223372036854775767` against python
  `9223372036854775849`: mant sum 2^64).
- **unsigned wrap**: same sign AND | |a| - |b| | = 2^w
  (go uint64 `41` against python `18446744073709551657` on
  `u64max + 42`: mant difference 2^64) — the case a
  sign-flip-only rule would have lost.

Counts: 23,660 signed + 14,255 unsigned = 37,915 relations
(was 63,111 under the raw-difference spelling — the excess was
pairs that satisfied raw-difference without either decomposed
signature). The w >= 8 floor stays as a guard; the sharper
signatures do most of its old job.
