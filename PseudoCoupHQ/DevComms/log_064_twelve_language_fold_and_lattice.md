# log 064 — the twelve-language fold and the operator-dominance lattice

2026-08-23. Folds the completed cartesian run for the ten new languages
(python, go, php, typescript, java, kotlin, cpp, swift, dart, csharp)
in beside rust (debug), rust_release and ruby into
`matrices_cart_v2/` / `matrices_full_v2/`, and re-runs
`l3_operator_dominance.py` over the extended `matrices_full_v2/`.
Answers the two open questions of
`DevComms/log_056_operator_dominance_and_modes.md` §3 and §4.

**A state correction before anything else.** The task brief's "verified
2026-08-23" note said `matrices_cart_v2/` and `matrices_full_v2/` held
only rust + rust_release + ruby. On inspection the twelve-language fold
was already present on disk (built 2026-08-23 02:33–02:36, by
`l3_cart_read_v2.py --only=... --merge` in stages, `l3_cart_full_v2.py`,
and `l3_operator_dominance_v2_twelve.py`), with `operator_dominance_v2.json`
already written. `matrices_cart_v2/index.json` records
`"verification": {"skipped": "format verification deferred by
--no-verify; run verify(OUT_DIR) over the finished directory"}` — the
chunked build's own format pass was never run over the finished
directory. Nothing here assumes the fold is correct because it exists;
everything below is independently re-derived and checked. `git diff`
against the last commit touching `matrices_cart_v2/`/`matrices_full_v2/`
(`3884342`, rust+ruby only) shows **zero byte difference** on every
`rust.*.csv` / `ruby.*.csv` file in both directories — the fold
disturbed nothing already there.

---

## 1. fold verification

Two independent checks, neither reusing `l3_cart_read.py`'s or
`l3_interval_read.py`'s canon functions:

**(a) raw lane text → cart cell, freshly reimplemented.** A
standalone script
(`Research/kind_fuzz_clustering/log064_independent_verify.py`)
reimplements `INT:` / `UINT:` / `BIGINT:` / `FLOAT:` decode and the
31-fractional-digit `[sign, mant, expo]` canon rule from the CLAUDE.md
spec, with no import of the project's own canon code. For each of the
ten new languages plus `rust_release`, it samples cells across two
operators (an arithmetic op and a comparison op) at L1, and one
operator at L2 for the largest families:

| check | cells sampled | matched | mismatched |
| --- | --- | --- | --- |
| L1 (10 languages + rust_release, 20 op/lang pairs) | 2,362 | 2,362 | 0 |
| L2 (go, cpp, php, kotlin, typescript, rust_release) | 526 | 526 | 0 |

**(b) `matrices_cart_v2` → `matrices_full_v2`, probe-index rule,
reimplemented independently** (the log_055 verifier pattern, written
fresh rather than calling `l3_cart_full.py`'s `map_positions`): for six
sampled profiles across go, php, cpp, csharp, kotlin, typescript
(truth, whole and bigint holders, one L2 profile) every full-grid cell
was recomputed from the cart row's `x_set` and compared to the full
row on disk — **0 mismatches over 862 cells checked**, including the
`UNREPRESENTABLE` fills at positions the cart row's holder-narrower
`x_set` doesn't reach.

`l3_cart_full.py`'s own `main()` (unconditional, no `--no-verify` path
exists for it) additionally asserts rectangularity and one grid size
per `(form_pair, level)` across all blocks at build time; the directory
would not exist in its current state had that assertion failed.

**Verdict: the fold is correct** by two independent re-derivations, and
rust/rust_release/ruby are untouched (byte-identical to the pre-fold
commit, confirmed by `git diff`, and — for `rust_release`, which was
never separately committed — independently re-derived from
`SandboxDesign/agent/out/ct_rust_release_l{1,2}.txt` directly).

## 2. per-language profile and cell counts

| language | cart profiles | cart cells | full profiles | full cells | full values | full declines | full UNREPRESENTABLE |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cpp | 1512 | 2,619,400 | 1512 | 6,172,216 | 2,297,447 | 321,953 | 3,552,816 |
| csharp | 638 | 715,367 | 638 | 2,593,544 | 685,647 | 29,720 | 1,878,177 |
| dart | 358 | 1,057,905 | 358 | 1,281,144 | 934,619 | 123,286 | 223,239 |
| go | 208 | 519,757 | 208 | 917,036 | 430,281 | 89,476 | 397,279 |
| java | 1230 | 1,525,882 | 1230 | 5,120,069 | 1,439,926 | 85,956 | 3,594,187 |
| kotlin | 357 | 611,002 | 357 | 1,620,224 | 592,497 | 18,505 | 1,009,222 |
| php | 468 | 1,485,640 | 468 | 1,487,642 | 1,326,155 | 159,485 | 2,002 |
| python | 3200 | 13,212,225 | 3200 | 13,914,500 | 7,289,216 | 5,923,009 | 702,275 |
| ruby | 2352 | 9,396,120 | 2352 | 9,972,504 | 5,108,255 | 4,287,865 | 576,384 |
| rust | 249 | 646,659 | 249 | 1,147,420 | 428,564 | 218,095 | 500,761 |
| rust_release | 249 | 646,659 | 249 | 1,147,420 | 618,783 | 27,876 | 500,761 |
| swift | 70 | 45,063 | 70 | 79,740 | 26,973 | 18,090 | 34,677 |
| typescript | 162 | 601,214 | 162 | 654,838 | 571,758 | 29,456 | 53,624 |
| **total** | **11,053** | **33,082,893** | **11,053** | **46,108,297** | — | — | — |

11,053 profiles, 46,108,297 full-grid cells — matches the count
`l3_operator_dominance_v2_twelve.py` reports reading, independently
confirmed by summing the CSVs directly rather than trusting that
script's own count.

**Observation, not classified:** swift and dart carry a visibly smaller
L1 operator set than the other ten languages — neither has `plus` or
`minus` rows in `matrices_cart_v2` at all (swift L1: `ampamp, gt, gteq,
lt, pipepipe, star` only; dart L1 has comparison/bitwise ops and `qq` /
`tildeslash` but no `plus`/`minus`). This predates this fold (log_062/063
built these lanes) and is carried forward unchanged; flagged here
because it means swift and dart cannot appear in the `+` mode-partition
evidence below.

## 3. operator dominance, re-run

`operator_dominance_v2.json`, written by
`l3_operator_dominance_v2_twelve.py` (a composition of the settled
`l3_operator_dominance.py` functions, unmodified, over `matrices_full_v2/`
— `operator_dominance_v1.json`, the log_056 audit product, is untouched).

| | v1 (log_056, rust+ruby) | v2 (twelve languages) |
| --- | --- | --- |
| profiles | 2,601 | 11,053 |
| operators | 43 | 248 |
| containment pairs | 23 | 872 |
| mode families (≥2 languages) | 76 | 437 |

**Correction to the task brief:** it stated "before = 24" containment
pairs. The audit file `operator_dominance_v1.json` itself contains 23
pairs, matching log_056's own prose ("23 containment pairs over 43
operators"). 23 is the verified before-count; 24 does not match either
the JSON or the log it was drawn from.

Shape of the new 872: still concentrated in comparison/bitwise
operators (`python.amp`/`pipe` and `ruby.amp`/`pipe` each contain 15
narrower operators; `dart`, `rust`, `rust_release` `.amp`/`.pipe` each
contain 13), the same pattern log_056 described for ruby alone, now
shared by every dynamically-accepting language. 192 of the 872
pair-instances are mutual (A contains B and B contains A) — the
equal-operator-spelling case (`&&`/`and`, `==`/`===`, etc.) seen at
operator grain, same as log_056 §1.

## 4. the two open questions

### 4a. log_056 §3 — does a WRAP mode part now exist?

**Yes.** Queried directly against `operator_dominance_v2.json`'s own
mode partition for `plus` in `whole|whole/L1` (94 profiles, 30 parts,
13 cross-language parts — see §5 below) and cross-checked by hand
against the raw cells for the key `(2^63-1, 42)`:

| language | holder(s) | canon at `(i64max, 42)` |
| --- | --- | --- |
| rust (debug) | `i64 i64` | `RAISE:panic` |
| rust_release | `i64 i64` | `[-1, 1.9999999999999999911095421856189, 62]` |
| go | `int64 int64`, `int int` | `[-1, 1.9999999999999999911095421856189, 62]` |
| java | `long`/`Long` × `short,int,long,Integer,Long` (9 combos) | `[-1, 1.9999999999999999911095421856189, 62]` |
| kotlin | `Long Int`, `Long Long` | `[-1, 1.9999999999999999911095421856189, 62]` |
| csharp | `long`×`int,long,short` | `[-1, 1.9999999999999999911095421856189, 62]` |
| cpp | `int64_t int32_t`, `int64_t int64_t` | `[-1, 1.9999999999999999911095421856189, 62]` |

`[-1, 1.9999999999999999911095421856189, 62]` is exactly the canon of
`-9223372036854775767`, the value two's-complement bit pattern
`0x8000000000000029` names as a signed 64-bit int — the census's
predicted `INT:64:8000000000000029`, confirmed independently
(`canon_num_independent(Fraction(-9223372036854775767))` reproduces the
string byte-for-byte). All six named languages land in ONE part in
`operator_dominance_v2.json`'s partition of `plus`/`whole|whole/L1`
(part 2: `languages: [cpp, csharp, go, java, kotlin, rust_release]`,
256/289 value cells, agreeing over the full grid including
`UNREPRESENTABLE` fills). rust (debug) is confirmed absent from this
part — it panics instead (part 28, singleton, `RAISE:panic` at this
key), exactly the debug-vs-release split log_056 §3 asked the release
lane to resolve.

The wider/unbounded holders sharing the same languages (`u64`/`uint64`/
`ulong`, `i128`/`__int128`, `bigint`) do NOT wrap — they land in the
exact-sum part instead, because their range covers `i64max+42` without
truncation. This is expected and consistent, not a fracture.

### 4b. log_056 §4 — python's unbounded int vs ruby's Integer, and ctypes.c_int64

**Python's `int` and ruby's `Integer` land in the same part — yes.**
Directly compared over the full `whole|whole` L1 grid (289 cells,
`matrices_full_v2/python.plus.L1.csv` `int int` vs
`matrices_full_v2/ruby.plus.L1.csv` `Integer Integer`):
`output_canon_vector` is **byte-identical**, 0 declines, 0
`UNREPRESENTABLE` on either side. The same vector is also
byte-identical to rust's `i128 i128` and typescript's `bigint bigint`.
This is `operator_dominance_v2.json`'s mode-partition part 1 for
`plus`/`whole|whole/L1`: 18 members, 6 languages (`cpp, python, ruby,
rust, rust_release, typescript`), 289/289 value cells, full agreement —
the exact-arithmetic part.

**Python's `ctypes.c_int64` lands elsewhere — yes, but the reason
needs a correction the codebase already recorded (log_061 §2), not a
new one.** `c_int64 c_int64` is its own singleton part (part 25,
256/289 value cells, `UNREPRESENTABLE` on the 33 cells whose operand
`2^64-1` a signed 64-bit holder cannot construct) — its vector is NOT
identical to `int int`'s. But cell-by-cell, **everywhere `c_int64`
answers (all 256 non-`UNREPRESENTABLE` cells), it agrees with `int`
exactly — 256/256, 0 disagreements.** log_061 already diagnosed this:
the log_031 census's "contradicts python's own int" (on `u64max + 42`,
giving `41` vs the unbounded `18446744073709551657`) is a WRAP AT
CONSTRUCTION — `2^64-1` is simply out of `c_int64`'s representable
range and the value is never built, not a wrapping `+`. Once
constructed, `ctypes.c_int64(x).value` is a plain python int and the
arithmetic afterward is python's ordinary unbounded arithmetic. So the
holder differs from `int` **by window (representability), not by
value** — log_056 §4's own caution ("width is a holder property, not a
guarantee") arriving a second time, now confirmed at cell grain across
the full grid rather than asserted from one probe.

## 5. the `+` mode partition, twelve languages

`whole|whole/L1`, before (log_056, rust+ruby only) vs now:

| | before | now |
| --- | --- | --- |
| profiles | 13 | 94 |
| parts | 6 | 30 |
| cross-language parts | 1 | 13 |

The new cross-language parts, beyond the wrap part (§4a) and the
exact-arithmetic part (§4b): a 32-bit wrap part (`cpp, csharp, go,
java, kotlin, rust_release` — `i32 i32` / `int int` / `Int Int` /
`Integer Integer`, 81/289 values); two 32-into-64-widening parts split
by argument order (`int Long` vs `Long int`, `cpp/csharp/java/kotlin`,
144/289 values each — order matters because these languages promote
the narrower side, so `int+Long` and `Long+int` share a VALUE but the
declared holder pair differs, and the partition is on cells not
holders so they still land together *within* an order); a `u64`/
`uint64`/`ulong` wrap-around-unsigned part (`csharp, go, rust_release`,
121/289); five `csharp`/`java` `short`-involving parts; and one
python-only residue (`Decimal + Fraction` / `Fraction + Decimal`, both
directions `RAISE:TypeError`, 0 value cells).

## 6. containment pair count and anomalies

**Containment pairs: 23 before (log_056/`operator_dominance_v1.json`,
NOT 24 as the task brief stated — see §3 correction) → 872 after.**

**Anomaly check 1 — the log_057 float-canon fault shape, searched for
recurrence.** All ten new languages read floats through raw BITS
(`f64::to_bits`-equivalent), not printed text, so the log_057 fault
(reading a printed decimal as an exact decimal) has no obvious way to
recur in them. Checked directly: `f64`/`float64`/`double`/`Double`/
`number`/`float` holders for `plus` on `fractional|fractional/L1`
across rust, rust_release, go, java, csharp, cpp, kotlin, typescript,
php are **byte-identical to rust's `f64 f64`, 256/256 cells, 0
mismatches**. Ruby `Float + Float` vs rust `f64 + f64`, the pair
log_056 §5 flagged with 157/256 disagreements pre-fix, now shows **0
disagreements** — the fix holds under the twelve-language re-fold.
**No instance of this fault shape found among the new languages.**

**Anomaly check 2 — PHP integer overflow, not a fault, a third
arithmetic behaviour.** `php int int` at `(i64max, 42)` answers
`[1, 1.0, 63]` — neither the exact sum (`[1,
1.0000000000000000044452289071906, 63]`) nor the two's-complement wrap
(`[-1, 1.9999999999999999911095421856189, 62]`). `[1, 1.0, 63]` is
exactly `2^63`: PHP silently promotes an overflowing int to float, and
`2^63+41` is inside one double ULP (2048 at this magnitude) of `2^63`,
so it rounds there. This is genuine PHP behaviour (float-fallback
overflow), correctly measured, not an instrument artefact — flagged
because it is a candidate THIRD arithmetic mode alongside exact and
wrap, not because anything is wrong with it.

**Anomaly check 3 — swift/dart's missing `plus`/`minus` at L1** (§2).
Cause not investigated here (out of scope: pure data work, no probes
re-run); flagged for whoever next touches the swift/dart emitters.

---

## decided, recorded for audit

- The fold's correctness was independently re-derived twice (raw text
  → cart, cart → full) with fresh, non-reused code, rather than
  accepted because the files were present and dated after the wrapper
  scripts.
- `operator_dominance_v1.json` (log_056, 23 pairs) is unmodified;
  `operator_dominance_v2.json` (872 pairs, twelve languages) is a new
  file, written by `l3_operator_dominance_v2_twelve.py`.
- `matrices_cart/`, `matrices_full/` (pre-057), and the rust/ruby rows
  inside `matrices_cart_v2/`/`matrices_full_v2/` are confirmed
  untouched (git diff, byte-for-byte, both generations).
- The task brief's "containment pairs before = 24" is corrected to 23
  against the audit file itself; recorded as a correction, not a
  silent substitution.
- PHP's float-fallback overflow and swift/dart's narrower L1 operator
  set are recorded as observations, not classified into the mode or
  guarantee vocabulary — that reading is the owner's.

## awaiting the owner

1. **Is PHP's float-fallback overflow a THIRD candidate arithmetic
   mode** (exact / wrap / float-fallback), or does it belong inside
   "declines and casts" rather than the guarantee taxonomy log_056 §4
   opened? Anomaly check 2 above is descriptive only.
2. **Which scoring is THE weight** (log_055/056, still open) — the
   twelve-language mode partition (§5) sharpens the same argument
   log_056 §4 made: the VALUE reading finds `c_int64` and `int` as one
   operation seen through different windows; the ALL reading (used by
   `mode_partition` here) correctly keeps them as separate parts
   because a guarantee reading needs the window difference visible.
   Still not decided which is THE weight.
