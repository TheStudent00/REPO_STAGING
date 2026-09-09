# log 047 — final canonical forms + string clustering (2026-08-20)

## what was built

the owner's FINAL canonical-form rulings landed today (settled; they
overrode the earlier forms of log 046 after repeated
miscommunication — integer mants rejected, then rationals/`~`
markers/exact columns rejected too; fractions are banished from every
visible column). Recorded verbatim in the new dated section of
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_conversion_spec.md`.
Two products, both assembly only — no probe runs:

- `Research/kind_fuzz_clustering/l3_per_op_matrices_v2.py` — re-emits
  the **242 per-operator CSVs** in `matrices/` under the final forms.
  It imports the v1 generator (which stays on disk for the audit
  trail) and patches its canonical spellings. 11 columns everywhere:
  `probe_id, lhs_holder, lhs_value_class, lhs_bytes, lhs_canon,
  rhs_holder, rhs_value_class, rhs_bytes, rhs_canon, output_bytes,
  output_canon`. Outcome tokens travel IN `output_canon` (`REFUSE`,
  `RAISE:<kind>`, `ABORT`); the indicator columns are retired. Numeric
  canon `[sign, mant, expo]`, sign ∈ {−1,1}, decimal mant in [1,2) at
  31 significant fractional digits (trailing zeros stripped to a
  one-digit minimum); zero `[±1, 0.0, 0]`; infinities `[±1, inf]`;
  `nan` the only word kept. Text `t|hex|b|cp|g`; containers
  `c|members|key_format|order_flag`. Exact rational mants live in
  `matrices/exact_sidecar.json` (1,151 distinct canon strings), never
  a CSV. `index.json` and `README.md` rewritten to match.
- `Research/kind_fuzz_clustering/l3_dendro_strings.py` — the
  threshold-spectrum clustering over the new canonical strings.
  Similarity = mean per-shared-(lhs_canon, rhs_canon)-pair
  byte-identity of `output_canon`; unshared pairs excluded, no
  padding; UPGMA average linkage (the l3_dendro_extended machinery and
  explorer). Products `dendro_strings.json` +
  `dendrogram_strings.html` (single self-contained file, data
  embedded, icicle + threshold slider + search).

## verification (the approved python.+ slice)

base_42 + i64max_plus1, 16 rows, diffed against the owner's expected
strings, verbatim:

```
MATCH    int+int:                     [1, 1.0000000000000000045536491244391, 63]
MATCH    int+ctypes.c_int64:          [-1, 1.9999999999999999908927017511218, 62] ; rhs_canon [-1, 1.0, 63]
MATCH    decimal.Decimal+fractions.Fraction: RAISE:TypeError
MATCH    fractions.Fraction+decimal.Decimal: RAISE:TypeError
MISMATCH ctypes.c_int64+ctypes.c_int64: [-1, 1.9999999999999999908927017511218, 62] (expected [-1, 1.0, 1])
```

The mismatch is in the DATA, not the conversion:
`behavior_python_C.json` cell `P5_5_base_42_i64max_plus1_+` records
`int:-9223372036854775766` (the same sum every other holder pair
gets), and no reading of −9223372036854775766 yields `[-1, 1.0, 1]`
(= −2). Reported to the owner rather than papered over. Hygiene sweep over
all 242 CSVs: 0 cells with fractions, `~`, or retired words in a
visible canon column; 0 non-rectangular matrices.

## clustering results

Headless verify: 242 leaves = 242 columns; 241 merge similarities
non-increasing; band-walk (tree walk vs merge history) agrees at all
101 thresholds.

- `go.+` ~ `rust.+` = **0.9206** over 189 shared input pairs (high, as
  expected).
- `go.+` ~ `python.+` = **0.0000** over 169 shared input pairs — real,
  not a bug: python.+ carries four heterogeneous holders per input
  pair, so nearly every pair's output SET includes extras
  (`RAISE:TypeError` from Fraction↔Decimal, a 28-digit Decimal
  spelling beside the exact int spelling), and byte-identity of the
  set is never met. The strict string rule measures exactly this.
- `go.+` cluster: t=0.95 → {go.+} alone; t=0.85 → {go.+, rust.+};
  t=0.70 → 62 members, all arithmetic/bitwise/logical
  (go/rust/cpp/java/csharp/kotlin/dart/swift/typescript `+ - * % <<
  >> & | ^ && ||` and kin), **zero comparison columns** at all three
  thresholds — the arithmetic group forms DISTINCT from comparisons,
  which now output truth strings (`true`/`false`) and separate, as
  the design predicted.

## decided vs awaiting

Decided and recorded (overturnable): mant trailing-zero strip to a
one-digit minimum; RAISE kind normalization (package prefixes
stripped, go's message-text raise → `IntegerDivideByZero`); the
duplicate-holder alignment as a SET of distinct output_canon strings;
sidecar keyed by canon string.

Awaiting the owner: the c_int64+c_int64 expected-string discrepancy above —
either the approved example needs a correction or the recorded cell
does.
