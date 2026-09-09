# log 057 — the ruby Float canon fault, fixed and re-folded; the rust RELEASE column, dropped

2026-08-22. Two jobs from the same session. Job A fixes and re-folds the
fault log_056 §5 flagged as unverified. Job B answers log_056 §3 and
§4's open item: a rust RELEASE column, so the wrapping-add guarantee
has an instance in the data.

---

## JOB A — the ruby Float canon fault

### 1. the fault, confirmed at the code level

`Research/kind_fuzz_clustering/l3_per_op_matrices.py`, `canon_output_printed`,
before this fix: a native binary `float`/`double` payload (ruby
`Float:#{r.inspect}`) and a genuinely decimal payload (`BigDecimal`,
`Rational`, ...) were handled by the SAME branch — `Fraction(text)`,
reading the printed digits as an EXACT DECIMAL. That is correct for a
decimal type (its printed text already IS its exact value) and wrong
for a binary double (its printed text is a SHORTEST ROUND-TRIPPING
DECIMAL of a value stored in binary — treating those digits as exact
names a different real number once you look past ~17 significant
digits).

Reproduced directly, `-DBL_MAX` (`ruby (-1.7976931348623157e+308).inspect`):

| path | canon |
| --- | --- |
| old (`Fraction(text)`, the bug) | `[-1, 1.9999999999999997688934766870555, 1023]` |
| new (`Fraction(float(text))`, the fix) | `[-1, 1.9999999999999997779553950749687, 1023]` |

These are the exact two strings log_056 §5 quoted from ruby vs rust —
confirms the hypothesis was right and pins the fault to this one
function.

### 2. the fix

`canon_output_printed` now splits `FLOAT_TYPES` (`float`, `double`) from
the decimal-ish family (`decimal`, `bigdecimal`, `rational`, `fraction`,
`gmp`, `num`). The float branch parses `float(text)` first, then feeds
`Fraction(that double)` — exact, by construction — to `canon_from_fraction`.
`MANT_DIGITS=31` and the 60-digit decimal context are unchanged; they were
never the problem.

Checked, per the task's own instruction not to assume: the one other
text-printed-float shape in this line, ruby's `BigDecimal((v).to_s)`
INPUT construction (`l3_cart_values.py` `decl`/`canon_point`). Not a
fault — `canon_point` computes the input's canon from the SAME string
(`Fraction(Decimal(repr(v)))`) that `decl` uses to build the actual
ruby `BigDecimal`, so both sides agree by construction: the BigDecimal
holder's value genuinely IS that decimal text, exactly, because
`BigDecimal(str)` is decimal-to-decimal. The fault is specific to
binary-float print-grain, not to every float-adjacent path.

### 3. the self-check

`l3_interval_read.py`'s `ruby_canon` now calls `_check_float_roundtrip`
on every `Float:` payload. A literal "does this canon round-trip to the
double" check turned out to be **vacuous** — proven before writing it:

```
old = "[-1, 1.9999999999999997688934766870555, 1023]"
new = "[-1, 1.9999999999999997779553950749687, 1023]"
both parse back (round-to-nearest, double precision) to ffefffffffffffff
```

Both the buggy and the fixed mantissa round-trip to the identical
double — the fault lives in digits the double's own 52-bit precision
cannot see, only the 31-digit canon can. So the check instead
independently recomputes `v2.canon_num(Fraction(float(text)))` and
compares by STRING to the canon actually produced, raising `SystemExit`
on any mismatch. Verified against both directions:

```
self-check fed the OLD buggy canon -> fired:
  FLOAT CANON ROUND-TRIP FAILURE (the log_057 fault, unfixed): ruby
  Float:'-1.7976931348623157e+308' canonicalised to [-1,
  1.999999999999999768893476687055..., but the double it names
  canonicalises to [-1, 1.99999999999999977795539507496... independently

fed the FIXED canon -> silent (as required)
2,000 random doubles (full 64-bit space, getrandbits) -> all clean
```

It then ran, live, against every `Float:` answer in the real fold below
and raised nothing.

### 4. raw lane output — still on disk, contrary to log_052's worry

`log_052` flagged the 482 MB ruby level-2 lane output as living in the
gitignored `SandboxDesign/agent/out/`, implicitly at risk
of being gone. **It is not gone.** Found in both `agent/out/` and
`Research/kind_fuzz_clustering/raw/`:

| file | size |
| --- | --- |
| `ct_ruby_l1.txt` | 12.3 MB |
| `ct_ruby_l2.txt` | 504.6 MB |
| `ct_rust_l1.txt` | 0.8 MB |
| `ct_rust_l2.txt` | 20.9 MB |

So the FULL re-fold was possible — no probe was re-run for Job A.

### 5. the re-fold — matrices_cart_v2 / matrices_full_v2

Two thin wrappers, reusing the settled generators unmodified and only
repointing their output directories: `l3_cart_read_v2.py` (wraps
`l3_cart_read.py`) and `l3_cart_full_v2.py` (wraps the existing
`l3_cart_full.py`, per the task). `matrices_cart/` and `matrices_full/`
are byte-for-byte untouched on disk (verified `md5sum` before/after).

| generation | files | rows | probes / cells | wall clock |
| --- | --- | --- | --- | --- |
| `matrices_cart_v2/` | 85 | 2,601 | 10,042,779 probes | 36.7 s |
| `matrices_full_v2/` | 85 | 2,601 | 11,119,924 cells (5,536,819 value, 4,505,960 decline, 1,077,145 `UNREPRESENTABLE`) | 10.7 s |

The full-grid totals are byte-identical to log_055's numbers — the
inflation logic did not change, only the source cells did.

### 6. how many cells changed

Cell-by-cell diff, `matrices_cart/` vs `matrices_cart_v2/` (same result
diffing the `_full` pair, since `UNREPRESENTABLE` fills are untouched):

| | value |
| --- | --- |
| total cells | 10,042,779 |
| changed cells | **293,113** (2.9%) |
| changed rows | 179 of 2,601 |
| files touched | 20 of 85 |

The 20 files are every ruby operator whose menu can answer a `Float`
(directly, or by returning a `Float` operand for `&&`/`and`/`\|\|`/`or`):

| operator | L1 rows changed | L2 rows changed |
| --- | --- | --- |
| `&&` / `and` | 7 / 7 | 7 / 7 |
| `\|\|` / `or` | 8 / 8 | 8 / 8 |
| `-` | 9 | 9 |
| `%` | 9 | 9 |
| `+` | 9 | 9 |
| `/` | 9 | 9 |
| `*` | 9 | 9 |
| `**` | 11 | 18 |

Sample cells, `ruby.ampamp.L1.csv` row `A16_1_5` (`&&` returning a Float
operand):

| slot | old (bug) | new (fix) |
| --- | --- | --- |
| 0 | `[-1, 1.9999999999999997688934766870555, 1023]` | `[-1, 1.9999999999999997779553950749687, 1023]` |
| 6 | `[1, 1.0120112665365530917624767335946, -1074]` | `[1, 1.0, -1074]` |
| 12 | `[1, 1.5707963267948965, 1]` | `[1, 1.5707963267948965579989817342721, 1]` |

(Row 6 shows the reverse pattern too: the buggy path can print a
FULL, wrong 31-digit expansion where the true value terminates
cleanly at `1.0` — the decimal happened to have more digits than the
double's true binary value did.)

### 7. ruby Float+Float vs rust f64+f64, before and after

Both are IEEE-754 doubles; log_056 measured 157 disagreements out of
256 cells and called it "unverified — a hypothesis, not a
measurement." Re-measured directly on the full-grid pair
(`rust.plus.L1.csv` `f64`×`f64` vs `ruby.plus.L1.csv` `Float`×`Float`,
same 16-value X set both sides):

| | L1 (256 cells) | L2 (10,000 cells) |
| --- | --- | --- |
| BEFORE (`matrices_full`) | **157 disagreements** | not separately re-measured; same instrument |
| AFTER (`matrices_full_v2`) | **0 disagreements** | **0 disagreements** |

The hypothesis holds exactly: this was the canon-pipeline artefact
log_056 suspected, not a real arithmetic difference. `ruby Float + Float`
and `rust f64 + f64` now agree at every value cell, both levels.

### 8. operator dominance, re-run on the corrected data

`l3_operator_dominance_v2.py` composes the EXISTING
`l3_operator_dominance.py`'s own functions (unmodified) against
`matrices_full_v2/`, writing to `operator_dominance_v2.json` — it never
calls that module's `main()`, because `main()` hard-codes
`operator_dominance_v1.json` and that file is the log_056 audit
product; confirmed untouched (`md5sum` matches before/after).

| | v1 (pre-fix) | v2 (post-fix) |
| --- | --- | --- |
| containment pairs | 23 | **24** |

The one new pair: `ruby.star ⊇ rust.star` (98 ruby `*` profiles contain
12 rust `*` profiles) — `rust f32*f32` turns out to be exactly dominated
by `ruby Float*Float` over this X set (0/49 value-cell disagreements),
which the pre-fix canon fault made unreachable.

**`ruby.+` does NOT contain `rust.+`, even after the fix** — and the
reason has to be stated precisely, because it is not the fault just
fixed. `rust f64+f64` is now perfectly dominated (§7). `rust f32+f32`
is NOT, and never was an instrument question — `f32` is genuinely
lower precision than `Float`/`f64`, so real rounding differences
survive:

| ruby profile | disagreements with `rust f32+f32` (49 value cells) |
| --- | --- |
| `Float + Float` | 6 |
| `BigDecimal + BigDecimal` | 8 |
| `Rational + Rational` | 21 |

No ruby fractional profile in the block dominates `rust f32+f32`, so
`+`'s containment stays blocked — by a real precision fact, not an
artefact. (`*` happened to clear this bar on the sampled 16-value X
set; `+` did not.)

---

## JOB B — the rust RELEASE column

### 1. what changed in `l3_cart_gen.py`

`emit_rust(level, smoke=False, release=False)` — same cells, same
holders, same probe construction. New:

- `RUST_DEBUG_FLAGS = ["-C", "debug-assertions=on", "-C", "opt-level=0"]`
  (unchanged behaviour) and `RUST_RELEASE_FLAGS = ["-O"]` (rustc's
  shorthand for `-C opt-level=2`; with no `debug-assertions=on` /
  `overflow-checks=on` both stay off, which IS the wrapping-add mode).
- The flags travel inside `table.json` as `rustc_flags`; the driver's
  `compile_chunk` reads them instead of a hard-coded list.
- `language` in the payload is `rust_release` when `release=True` — a
  DISTINCT tag, never `rust`, so debug and release rows cannot merge.
  `__SUMMARY__`/`__TIMING__` lines and every progress print carry the
  tag too (`LANG` in the driver), not a literal `"rust"` string.
- `main()` gained a `--release` branch: emits ONLY the two
  `ct_rust_release_l{1,2}.sh` lanes (ruby and debug rust are untouched
  — they already ran, log_052).

Debug-mode lane generation is unchanged byte-for-byte (verified: the
`__LABEL__` placeholder substitutes back to the literal `"rust"` text
that was already there).

### 2. generated and dropped

```
python3 l3_cart_gen.py --release
  ct_rust_release_l1.sh   128 cells,    20531 probes, 12 KB
  ct_rust_release_l2.sh   121 cells,   626128 probes, 12 KB
```

20,531 + 626,128 = **646,659 probes** — matches the task's own count for
the existing rust cartesian run exactly (same cells, same X sets, only
the compile flags differ).

Batch manifest written BEFORE dropping, per the new machinery
(`SandboxDesign/README.md` "Progress, and the batch manifest",
`DevComms/log_001_cpu_cap_and_batch_progress.md`, both added today):

```
bash SandboxDesign/batch.sh rust-release-column \
    ct_rust_release_l1.sh:20531 ct_rust_release_l2.sh:626128
```

Both scripts then written into `SandboxDesign/agent/drop/`.

### 3. the container WAS running — it picked the lanes up immediately

The task briefed me to expect the container might be stopped. It was
not: within seconds of the drop, `agent/status/ct_rust_release_l1.sh.status`
showed `state=running` with a live log
(`[progress] rust L1 chunk 1/14 build 2.15s`). `bash
SandboxDesign/progress.sh` tracked the batch to completion:

```
== batch summary ==
  batch:    rust-release-column  (id batch-20260822T073430Z)
  overall:  2/2 lanes done   weight 646659/646659  (100.0% by weight)
  elapsed:  00:12:25
  status:   batch complete

  ct_rust_release_l2.sh   done  exit=0   693.8s
  ct_rust_release_l1.sh   done  exit=0    22.9s
```

**If the owner finds the container stopped on some other occasion**, the
start command is `bash SandboxDesign/up.sh` — not run
here, since it was not needed and I was told not to start podman
myself.

### 4. the results — wrapping-add now has an instance

`__SUMMARY__` lines, raw lane output in `agent/out/`:

| lane | probes | answers (debug) | panics (debug) | answers (release) | panics (release) |
| --- | --- | --- | --- | --- | --- |
| L1 | 20,531 | 16,082 | 4,449 | **20,421** | **110** |
| L2 | 626,128 | 412,482 | 213,646 | **598,362** | **27,766** |

4,339 (L1) + 185,880 (L2) formerly-panicking cells now WRAP instead —
the guarantee log_056 §3 said had zero instances in the data now has
190,219.

The concrete case log_056 §3 named directly — `i64::MAX + 42`, five
other languages' census bit pattern `INT:64:8000000000000029`:

| build | `2^63-1 i64 + 42 i64` |
| --- | --- |
| debug (`ct_rust_l1.txt`) | `RAISE:panic` |
| release (`ct_rust_release_l1.txt`) | `INT:64:8000000000000029` (signed: `-9223372036854775767`) |

Rust joins the wrap census, exactly as predicted, once built with `-O`.

A `*` example from the same run, `i32 * i32` (op index 2, holder `i32`):

| probe | debug | release |
| --- | --- | --- |
| `A2_3_3_0` | `RAISE:panic` | `INT:32:00000000` |
| `A2_3_3_2` | `RAISE:panic` | `INT:32:80000000` |

**Not folded into `matrices_cart_v2`/`matrices_full_v2`.** The task
scoped Job B as "prepare and drop one small probe lane," and folding a
third rust language column into the compatibility-gate / dominance /
mode-partition machinery is a structural decision (does it join the
existing `rust` operator node, or get its own; does the mode partition
in log_056 §4 gain a fourth part) that belongs to the owner, not decided
here. The raw answers sit in `agent/out/ct_rust_release_l{1,2}.txt`,
ready for that fold when wanted.

### 5. the stray file

`SandboxDesign/agent/drop/.probe_write_test` (0 bytes,
from an earlier write test) still exists and could not be removed from
this sandbox:

```
$ rm -f agent/drop/.probe_write_test
rm: cannot remove '...': Operation not permitted
```

Harmless per the task's own note — the watcher only runs `*.sh` — but
it needs a human `rm` since this sandbox's mount forbids the unlink.

---

## decided, recorded for audit

- `canon_output_printed` (`l3_per_op_matrices.py`): binary float/double
  print-grain text now converts via `Fraction(float(text))`, never
  `Fraction(text)` directly; decimal-ish types (`BigDecimal`,
  `Rational`, `Fraction`, `gmp`, `num`) keep the direct decimal parse,
  because their printed text already IS their exact value.
  `MANT_DIGITS=31` and the 60-digit decimal context unchanged.
- Checked the `BigDecimal`-from-float INPUT construction path
  (`l3_cart_values.py`) for the same shape of fault — it is NOT one;
  `canon_point` and `decl` agree by construction (same string, same
  decimal interpretation, and a `BigDecimal` genuinely equals its own
  decimal text exactly).
- `ruby_canon` (`l3_interval_read.py`) gained `_check_float_roundtrip`:
  fails loudly (`SystemExit`) if a `Float:` payload's canon is not
  independently reproducible from `float(text)`. Designed to compare at
  the canon's OWN 31-digit precision, not double precision — a
  double-precision round-trip check was proven vacuous first (both the
  buggy and fixed mantissa for `-DBL_MAX` round-trip to the identical
  double bits) and rejected before being written.
- New generation `matrices_cart_v2/` + `matrices_full_v2/` written by
  thin wrappers (`l3_cart_read_v2.py`, `l3_cart_full_v2.py`) that reuse
  the settled generators unmodified, only repointing output
  directories. `matrices_cart/` and `matrices_full/` stay on disk
  byte-for-byte unchanged (verified by hash), per the v5-rebuild
  convention.
- `operator_dominance_v2.json` written by composing
  `l3_operator_dominance.py`'s own functions directly, never calling
  its `main()` (which hard-codes the v1 output path) — protects the
  log_056 audit product.
- No probe was re-run for Job A; the raw lane output was found intact.
- `emit_rust` extended with a `release` parameter and `rustc_flags`
  threaded through the lane payload; `language=rust_release` is a
  DISTINCT tag from `language=rust`, never merged. Debug-lane output is
  byte-for-byte unchanged.
- Both rust-release lanes dropped and run to completion; raw answers
  kept in `agent/out/`, NOT folded into any matrices generation here.
- Did not start or stop the container; did not delete the stray
  `.probe_write_test` file (cannot, from this sandbox).
- Did not run the other ten languages. Did not choose which scoring
  (§7 of log_055, still open) is THE weight, or any cut.

## awaiting the owner

1. **Fold `rust_release` into the matrices.** Raw answers exist
   (`agent/out/ct_rust_release_l{1,2}.txt`); whether it becomes its own
   operator node, how it interacts with the compatibility gate,
   containment, and the §4 mode partition (a 4th part per family) is
   structural.
2. **Delete `SandboxDesign/agent/drop/.probe_write_test`**
   — harmless, but this sandbox cannot unlink it.
3. Still open from log_055/log_056, untouched by this session: which
   scoring is THE weight (§7 log_055), and whether the other ten
   languages are gated on the pilot clustering the way the owner expects.
