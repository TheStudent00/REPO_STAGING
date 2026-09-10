# log 056 — operator-level dominance, the mode partition, and one suspected instrument fault

2026-08-22. the owner's correction of the same day: dominance is an OPERATOR
relation — "operator `A` dominates operator `B` if `A` contains all the
same profiles as `B` and more" — one level above the profile relation
built in log 055. This log carries the operator relation, the mode
partition the guarantees rule calls for, and a measurement that should
be checked before it is believed.

No probes were run. Everything is a re-read of `matrices_full/`.
Script: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/l3_operator_dominance.py`
(2.5 s, run under `nice`). Product:
`PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/operator_dominance_v1.json`.

---

## 1. the relation, at the operator level

Rule as implemented: **A contains B when, for every profile of B, some
profile of A in the same gate block dominates it** — where one profile
dominates another when at every key the lower one answers a VALUE, the
higher one answers the identical value.

- **23 containment pairs** over 43 operators and 2,601 profiles.
- Reading the shape rather than the list: containment is concentrated
  in the comparison and bitwise operators, where ruby's dynamic
  acceptance gives it 98 profiles against rust's 2 to 32.

| A contains B | A profiles | B profiles |
| --- | --- | --- |
| `ruby.&` ⊇ `rust.&` | 98 | 10 |
| `ruby.==` ⊇ `rust.==` | 98 | 14 |
| `ruby.!=` ⊇ `rust.!=` | 98 | 14 |
| `ruby.>>` ⊇ `rust.>>` | 98 | 32 |
| `ruby.\|` ⊇ `rust.\|` | 98 | 10 |
| `ruby.^` ⊇ `rust.^` | 98 | 10 |
| `rust.&` ⊇ `rust.&&` | 10 | 2 |
| `ruby.&&` ⊇ `ruby.and` (and the reverse) | 98 | 98 |

The mutual pairs (`&&`/`and`, `==`/`===`, `||`/`or`) are the equal case:
each contains the other, which is the contract relation seen from the
operator level.

**The arithmetic operators contain nothing.** `ruby.+` does NOT contain
`rust.+`, and the reason is worth stating precisely, because it is not
the reason one would guess.

## 2. why arithmetic fails containment — and it is NOT overflow

Every rust WHOLE profile of `+` is dominated by ruby's `Integer +
Integer`. Measured, zero disagreements:

| rust holder | value cells | disagreements with `ruby Integer + Integer` |
| --- | --- | --- |
| `i32 + i32` | 67 of 289 | 0 |
| `i64 + i64` | 221 of 289 | 0 |
| `u64 + u64` | 102 of 289 | 0 |
| `i128 + i128` | 289 of 289 | 0 |

So the whole-number side nests perfectly: rust answers a narrower
region, ruby answers the same values there and more. Containment fails
only on the FRACTIONAL profiles:

| rust profile | covered by some ruby profile |
| --- | --- |
| `f64 + f64` [L1 and L2] | **no** |
| `f32 + f32` [L1] | **no** |
| every whole profile, both levels | yes |

## 3. the wrap camp is ABSENT from this data, and that matters

The census records five languages wrapping to the identical bit
pattern `INT:64:8000000000000029` on `i64max + 42`, with rust joining
them when built with `-O`. **None of that appears here.** Every rust
overflow cell in `matrices_cart` / `matrices_full` is `RAISE:panic` —
the debug build's behaviour.

- Consequence for the mode work: with only rust-debug and ruby in the
  data, there is exactly ONE arithmetic mode visible — *exact, or
  decline* — and the wrapping-add guarantee has no instance at all.
- The record-both-modes ruling therefore has a concrete owner now: the
  cartesian run needs a rust RELEASE column before the mode partition
  can propose wrapping-add as a mode. That is a run, not a re-read.

## 4. the mode partition

Inside one gate block, one operator SPELLING's profiles are partitioned
by total agreement over the full grid. Each part is a CANDIDATE mode;
no classification into guarantee-vs-no-guarantee is made here, because
that reading is the owner's under the guarantees rule.

`+` in `whole|whole` at L1 — 13 profiles, 6 parts:

| part | languages | members | value cells | example holders |
| --- | --- | --- | --- | --- |
| 1 | ruby, rust | 8 | 289/289 | `BigDecimal BigDecimal`, `Integer Integer`, `i128 i128` |
| 2 | ruby | 1 | 289/289 | `Rational BigDecimal` |
| 3 | ruby | 1 | 289/289 | `BigDecimal Rational` |
| 4 | rust | 1 | 67/289 | `i32 i32` |
| 5 | rust | 1 | 221/289 | `i64 i64` |
| 6 | rust | 1 | 102/289 | `u64 u64` |

**A caution the table makes visible.** Parts 4, 5 and 6 are separate
parts only because the holders DECLINE at different widths — they agree
with part 1 at every value cell (§2). Width is a holder property, not a
guarantee, so a partition by raw full-grid equality proposes modes that
are not modes.

- Under scoring (b) — declines as answers — `i32` and `i64` are
  different.
- Under scoring (a) — declines excluded — they are the same operation
  seen through narrower windows.
- **So the mode partition wants the VALUE reading, and the fracture
  detection wants the ALL reading.** That is a concrete argument for
  keeping both weights rather than choosing one, and it is the first
  thing in this line that gives the two-scoring design a job rather
  than a choice.

## 5. suspected instrument fault — ruby `Float` against rust `f64`

Both are IEEE 754 doubles, so `Float + Float` and `f64 + f64` should
agree wherever both answer. Measured: **157 disagreements** out of 256
cells. A sample, same key, ruby on the left:

> `[-1, 1.9999999999999997688934766870555, 1023]`
> `[-1, 1.9999999999999997779553950749687, 1023]`

The two mantissas agree to about the 17th significant digit and diverge
after it. 17 significant digits is what ruby's `Float#to_s` emits, and
the canonical form specifies 31 fractional digits — so the shape of
this is a canon built from a PRINTED decimal on the ruby side and from
exact bits on the rust side, rather than a real arithmetic difference.

- **Unverified.** This is a hypothesis from the digit position, not a
  measurement of the canon pipeline.
- If it holds, every fractional cross-language comparison in this line
  is affected, and `f64 + f64` failing containment (§2) is an artefact
  rather than a finding.
- Same shape as two faults this line has already caught: swift's
  `-typecheck` accepting what the compiler refuses (log 032), and
  dart's severity fault (log 030). The instrument answered a slightly
  different question than the one asked.

---

## decided, recorded for audit

- Operator containment computed from profiles rather than from cells
  directly: A's covering profile may be any profile in the same gate
  block, since holder pairs need not correspond across languages.
- Mode partition restricted to families with at least two languages
  present; a spelling only one language has cannot exhibit a mode split.
- Parts sorted by language breadth, then member count.
- The residue flag (a part with one language) is recorded but NOT
  classified as `unspecified` — that classification needs the
  guarantees reading.

## awaiting the owner

1. **The ruby-Float canon question (§5)** — should this be verified
   before anything fractional is read as a finding? It is a small,
   cheap check.
2. **A rust RELEASE column (§3)** — without it the wrapping-add
   guarantee cannot appear, so the mode work on arithmetic is
   incomplete. One extra lane, not a new design.
3. **Which scoring is THE weight** — still open, but §4 argues the
   answer may be "both, with different jobs" rather than one.
