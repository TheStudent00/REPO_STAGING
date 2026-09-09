# log 065 — operator-spelling gaps in the run, and the two readings compared

2026-08-23. Two survey jobs for the owner. **No probes run.** Job 1 audits
what the cartesian run's operator menu (`ops(lang)` in
`Research/kind_fuzz_clustering/l3_cart_gen.py`) could never have seen
because a guarantee is spelled as a method or a block, not an operator.
Job 2 builds the comparison log_056 §4 asked for — VALUE reading versus
ALL-CELLS reading, over `matrices_full_v2/` — and tests the owner's specific
worry about coincidental matches. Read first: `PseudoCoupHQ/CLAUDE.md`,
`DevComms/log_064_twelve_language_fold_and_lattice.md`,
`DevComms/log_056_operator_dominance_and_modes.md` §3–§4,
`Research/dominant_intentions/census_integer.md`,
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_ontology.md`
(the actual location — the brief's `Research/.../SUPPORT_ontology.md`
path does not exist; it lives under `Planning/`).

Scripts written for this log:
`Research/kind_fuzz_clustering/log065_readings.py` (Job 2 containment,
both readings), plus inline `python3 -c` snippets recorded verbatim
below for the mode-partition and coincidental-match drill-downs. Every
heavy pass ran under `nice -n 15`; the slowest single block (`plus`
family aside) was 70 s. Total compute across every python invocation
in this log: well under ten minutes.

---

# JOB 1 — guaranteed behaviours the cartesian run never probed

## the method

For each candidate, two questions, answered from files on disk, never
from memory:

1. **Is it an operator or a method/block?** Checked against
   `kinds_<lang>.json`'s `anonymous` token list (`l3_accept.ops`'s own
   source: `have = set(k["anonymous"]) | set(k["anonymous_positioned"])`).
   If the candidate string is not an anonymous grammar token, it is a
   named call (method/function) or, for `checked`/`unchecked`, a
   keyword introducing a block — never a binary operator our probe
   design could spell as `(a) OP (b)`.
2. **Was it in scope for the run?** Checked against `ops(lang)` in
   `Research/kind_fuzz_clustering/l3_cart_gen.py`, which is `COMMON +
   EXTRA[lang]` (from `l3_accept.py`) intersected with the grammar's
   own anonymous tokens.

## the table

| language | spelling | what it guarantees | operator or method/block | in `ops(lang)`? | verification |
| --- | --- | --- | --- | --- | --- |
| rust | `checked_add`/`sub`/`mul`/`div`/`rem` (returns `Option`, `None` on overflow) | detect-and-signal add — a candidate mode never in `ops()` at all | method | no | confirmed: not an anonymous token in `kinds_rust.json`; found in-repo only as harness code (`Research/kind_fuzz_clustering/bnd/bnd_rust.rs:10`, `l3_boundary_gen.py:1426`), used for the harness's OWN boundary bisection, not measured as a census fact |
| rust | `wrapping_add`/`sub`/`mul`/`div`/`rem` (silent wrap) | the wrapping-add guarantee, EXPLICITLY chosen (stable across debug/release, unlike bare `+`) | method | no | confirmed absent from `kinds_rust.json`'s anonymous tokens; **already documented** in `DevComms/log_020_full_census_run.md:142,525,536-537` — "rust source that says `wrapping_add` has CHOSEN the wrapping guarantee" |
| rust | `saturating_add`/`sub`/`mul`/`div`/`rem` (clamps to the type's min/max) | clamp-to-bound — a guarantee with NO existing mode-vocabulary entry (not wrap, not grow, not php's approximating) | method | no | UNVERIFIED beyond grammar-absence — zero hits anywhere else in the repo |
| rust | `overflowing_add`/`sub`/`mul`/`div`/`rem` (returns `(value, did_overflow: bool)`) | same VALUE as `wrapping_*`, packaged with a flag — not a new mode, a new return shape | method | no | UNVERIFIED beyond grammar-absence — zero hits elsewhere |
| swift | `&+`, `&-`, `&*` (wrapping arithmetic) | the wrapping-add/sub/mul guarantee | **operator** (infix, by Swift's own grammar) | **no — confirmed absent, and it is a DOUBLE absence** | see below |
| java / kotlin | `Math.addExact` (throws on overflow) | detect-and-raise, made explicit — contrasts with java's bare `+`, which just wraps silently with no guarantee attached | method | no | confirmed: `addExact` is not an anonymous token in either `kinds_java.json` or `kinds_kotlin.json`; zero hits elsewhere in repo — UNVERIFIED beyond the grammar check |
| java / kotlin | `Math.floorDiv`, `Math.floorMod` | the floor-division/floor-mod guarantee (contrasts with `/`/`%`'s truncating guarantee, census F-i3/F-i4) | method | no | same as above — grammar-absent, zero other hits, UNVERIFIED |
| csharp | `checked { }` / `unchecked { }` | opt-in strict overflow checking (throws) / opt-in explicit wrap | **block form** (keyword, not a binary operator) | n/a — not a candidate binary op at all | confirmed: `checked` and `unchecked` ARE anonymous (keyword) tokens in `kinds_csharp.json` — the grammar sees them, but `l3_accept.py`'s `COMMON`/`EXTRA["csharp"]` candidate list never included them because they aren't binary infix spellings |
| csharp | `Math.BigMul` (128-bit product of two 64-bit values, no overflow) | a widening multiply — avoids overflow for ONE operation via a wider return type, not language-wide unboundedness | method | no | UNVERIFIED — zero hits anywhere in repo beyond this survey |
| go | `math/bits` (`bits.Add64`, `bits.Mul64`, … return `(result, carry)`) | exposes the wrap value plus carry-out — multi-word arithmetic building block | method (package functions) | no | confirmed absent from `kinds_go.json`; zero other hits — UNVERIFIED |
| dart | `~/` (truncating integer division) | **already in scope — NOT a gap.** `ops("dart")` includes `~/` today, and it is actively probed: `matrices_full_v2/dart.tildeslash.L1.csv` and `.L2.csv` exist with real cells | operator | **yes** | the brief's framing of `~/` as a starting point to verify was wrong to treat as a candidate gap; verified directly against `matrices_full_v2/` |
| python | `divmod(a,b)` | returns `(a // b, a % b)` — a packaging of the ALREADY-probed floor-div/floor-mod guarantees (census F-i3/F-i4), not a new arithmetic behaviour | method (builtin function) | no | confirmed absent from `kinds_python.json`'s anonymous tokens |
| python | `math.fsum` (compensated summation) | a FLOAT precision guarantee, not an integer-overflow guarantee — belongs to `census_boolean_float.md`'s territory, not `census_integer.md`'s | method | no | confirmed absent from grammar tokens |
| php | `intdiv(a,b)` | truncating integer division that RAISES on overflow (`INT_MIN / -1`) instead of falling to float — the opposite guarantee from php's native `/`, which always floats, and from php's native `+`, which approximates (see below) | method (builtin function) | no | confirmed absent from `kinds_php.json`'s anonymous tokens; confirmed as a real, used php builtin — the harness's OWN php lane code calls it (`l3_boundary_gen.py:419,441,476`) |
| php | `bcadd()`/`bcmath` family, `gmp_add()`/`gmp` family | the GROWING guarantee (arbitrary precision), same family as python's `int`/ruby's `Integer` — reached via function call, not the native `+` | method (extension functions) | no | confirmed: both extensions are installed and confirmed present in this environment (`php -m` showing `bcmath`, `gmp` — `DevComms/log_023_layer2_representations.md:392-403`; `Planning/.../PROGRESS.md:67`; `DevComms/log_042_boundaries_by_bisection.md:149`) |

### swift's `&+`/`&-`/`&*`, in detail

Confirmed as a genuine, double gap — not merely "not intersected":

1. **`l3_accept.py`'s own candidate list never included them.**
   `EXTRA["swift"] = ["??", "...", "..<"]` (line 54) — `&+`/`&-`/`&*`
   were never even proposed as candidates to intersect against the
   grammar.
2. **The grammar extraction never captured them either.**
   `kinds_swift.json`'s `anonymous` list (109 tokens) contains exactly
   one `&`-token: `&&`. No `&+`, `&-`, `&*`, `&<<`. Checked against the
   archived tree-sitter grammar too
   (`0_Archive/PseudoIR_(retired)/v2/grammars/swift/node-types.json`):
   it declares a node type **`custom_operator`** — Swift's operators
   like `&+` are lexed by a REGEX-matched category, not fixed anonymous
   string tokens, which is mechanically why an anonymous-token
   enumeration can never see them. This is a real Swift infix operator
   (general knowledge, cross-checked against the grammar's own
   `custom_operator` node type, which is the mechanism such operators
   would need); it is UNVERIFIED beyond that — no measured cell exists
   for it anywhere in this repo.

`ops("swift")` today has 6 members: `&&, *, <, >, >=, ||` — no `+`,
`-`, `/`, `%`, or any bitwise operator at all (log_064 §2 already
flagged swift/dart's narrow L1 set as an observation).

## probe cost — OPERATOR-spelling gaps only

**Only one candidate above is a genuine operator-spelling gap:
swift's `&+`/`&-`/`&*`.** Every other candidate is a method or block
form and is scope, not a run-cost question (below).

Estimated from swift's OWN existing holder table
(`l3_cart_gen.table("swift", 1)`, whole form): 4 integer holders —
`Int` (n=16), `Int32` (n=9), `UInt64` (n=11), `Int64` (n=16). Assuming
same-type acceptance only (swift's static typing rarely mixes widths
implicitly, consistent with the existing 6-operator menu's pattern):

| level | cells per operator (sum of `n²` over the 4 holders) | 3 operators (`&+`,`&-`,`&*`) |
| --- | --- | --- |
| L1 | 16² + 9² + 11² + 16² = 714 | 2,142 |
| L2 | 16⁴ + 9⁴ + 11⁴ + 16⁴ = 152,274 | 456,822 |
| **total** | | **~459,000 cells** |

This is an ESTIMATE extrapolated from the existing table, not a
measurement — swift's acceptance pattern for `&+` etc. could differ
from `*`'s (e.g. if cross-width wrapping-add is accepted where plain
`+` isn't declared at all). Against the 46,108,297 cells already in
`matrices_full_v2/` (log_064 §2), this is small — under 1% — and uses
the SAME swiftc `-typecheck` A2 acceptance route already built for the
other 6 swift operators. **Not run.**

## operator vs. method/block — the plain count

- **Operator-spelling gaps (cheap, a run-scope question only):** 1 —
  swift's `&+`/`&-`/`&*` family (one grammar-extraction fix plus one
  small lane).
- **Method/block spellings that raise the scope question the census
  deferred** ("builtins are out of scope until the owner opens it"): 13 —
  rust's `checked_*`/`saturating_*`/`overflowing_*` (3 method
  families), java/kotlin's `Math.addExact`/`floorDiv`/`floorMod` (3),
  csharp's `checked`/`unchecked` block and `Math.BigMul` (2), go's
  `math/bits` (1), python's `divmod`/`math.fsum` (2), php's `intdiv`
  and `bcmath`/`gmp` (2).

---

# JOB 2 — the two readings compared, and the owner's coincidental-match worry tested

Definitions used (my operationalisation of log_056 §4's open question,
not a ruling):

- **VALUE reading** — two profiles are compared only at positions
  where BOTH answer a value (declines and `UNREPRESENTABLE` excluded
  from numerator AND denominator, per `CLAUDE.md`'s own scoring rule:
  "zero comparable keys means NO connector"). A dominates B when at
  least one such position exists and none of them conflict.
- **ALL-CELLS reading** — every position counts; outcome tokens
  (`REFUSE`, `RAISE:*`, `ABORT`, `UNREPRESENTABLE`) ride as literal
  answers, compared by byte identity like any value. Because there is
  no partial credit, "A contains B" collapses to full-vector equality
  under this reading (any surplus information A has already shows as
  a literal mismatch) — this is exactly what
  `l3_operator_dominance.py`'s existing `mode_partition` already does;
  here it is extended to containment too.

Both computed fresh over `matrices_full_v2/` (11,053 profiles, 248
operators, 46,108,297 cells) —
`Research/kind_fuzz_clustering/log065_readings.py`, 12.6 s total.

## 1. containment pair counts, both readings

| reading | containment pairs |
| --- | --- |
| VALUE | 1,046 |
| ALL-CELLS | 368 |
| intersection (both readings agree) | 368 |
| only VALUE | 678 |
| only ALL-CELLS | 0 |

**ALL-CELLS ⊆ VALUE, exactly** — every ALL-CELLS containment pair is
also a VALUE containment pair, and 678 pairs hold only under the
looser VALUE reading. This is the expected shape: full-vector equality
is strictly harder to achieve than value-cell-only agreement, so
nothing new appears under ALL-CELLS that VALUE didn't already find.

Sample of the 678 only-in-VALUE pairs (full list in
`Research/kind_fuzz_clustering/log065_containment_readings.json`):

| A contains B (VALUE only) |
| --- |
| `cpp.amp` ⊇ `go.amp` |
| `cpp.bangeq` ⊇ `csharp.bangeq` |
| `cpp.bangeq` ⊇ `rust.bangeq` |
| `cpp.eqeq` ⊇ `python.eqeq` |
| `cpp.gt` ⊇ `dart.gt` |
| `cpp.gt` ⊇ `java.gt` |
| `cpp.gt` ⊇ `rust.gt` |
| `cpp.caret` ⊇ `go.caret` |

These are cross-language same-spelling pairs (`gt` vs `gt`, `bangeq`
vs `bangeq`) that agree on every VALUE cell but not on every literal
cell — almost certainly differing `UNREPRESENTABLE` footprints from
different holder widths, exactly log_056 §4's "width is a holder
property, not a guarantee" caution, now visible as a reading-dependent
containment count rather than an assertion.

## 2. the `plus`/`whole|whole/L1` mode partition, both readings

94 profiles (matches log_064 §5 exactly).

**ALL-CELLS reading** (full-vector equality — a true partition,
reproduces `operator_dominance_v2.json`'s own numbers exactly):

| parts | cross-language parts |
| --- | --- |
| 30 | 13 |

Top parts:

| langs | members | value cells | example holders |
| --- | --- | --- | --- |
| 6 | 18 | 289/289 | `cpp, python, ruby, rust, rust_release, typescript` — `Integer Integer`, `i128 i128`, `Decimal Decimal`, `bigint bigint` |
| 6 | 10 | 256/289 | `cpp, csharp, go, java, kotlin, rust_release` — `i64 i64`, `int64_t int64_t`, `long long` (64-bit wrap) |
| 6 | 9 | 81/289 | same 6 langs — `i32 i32`, `int32_t int32_t` (32-bit wrap) |
| 4 | 7 | 144/289 | `cpp, csharp, java, kotlin` — `int Long` (32-into-64 widening, one argument order) |
| 4 | 7 | 144/289 | same 4 langs — `Long int` (the other argument order) |

**VALUE reading** — this is where the reading matters. Two ways to
partition, both measured, and they disagree on the count:

**(a) naive connected components** (pairwise: compatible if no
conflict on shared value cells) — **3 components**: sizes 92, 1, 1.
But component 1 (92 members, 11 languages: `cpp, csharp, go, java,
kotlin, php, python, ruby, rust, rust_release, typescript`) is **NOT a
clique** — the exact chaining hazard `SUPPORT_ontology.md` already
flagged ("chaining through never-compared pairs is the hazard,
measured at 7,212 triples," log_053). Concrete witness inside the
92-member blob:

| A | B | conflicting cells (of 289) | sample |
| --- | --- | --- | --- |
| `cpp int32_t×int32_t` | `cpp int32_t×int64_t` | 14 | pos 54: `A=[1, 0.0, 0]` vs `B=[-1, 1.0, 32]` (32-bit wrap disagrees with the exact 64-bit sum) |

So **3 is not a trustworthy VALUE-reading part count** — it is an
artefact of treating pairwise compatibility as if it were transitive,
which `SUPPORT_ontology.md` already says it is not.

**(b) maximal cliques** inside the 92-member blob (the `GROUP` concept
`SUPPORT_ontology.md` actually specifies — "every pair inside must
agree, a maximal clique, never a connected component"), computed by
Bron–Kerbosch: **12 cliques**, sizes `36, 34, 18, 15, 15, 10, 9, 9, 9,
5, 3, 3` (graph density inside the blob: 1,437 of 4,186 possible
edges, 0.34). Plus the 2 singleton components = **14 groups total**
under this operationalisation.

| clique | size | langs | note |
| --- | --- | --- | --- |
| 0 | 36 | cpp, csharp, java, python, ruby, rust, rust_release, typescript | the exact-arithmetic camp, widened out to every holder compatible with it (includes `cpp __int128`, `csharp/java short×short`) |
| 1 | 34 | cpp, csharp, go, java, kotlin, rust, rust_release | 64-into-wider widening camp |
| 2 | 18 | cpp, csharp, go, java, kotlin, rust, rust_release | 32-bit wrap camp |
| 5 | 10 | cpp, csharp, go, java, python, rust, rust_release | unsigned-64 wrap camp, `python c_int64` included |
| 9 | 5 | csharp, java, php, rust | `php int×int` (the approximating guarantee) sits HERE, compatible with `csharp/java short×short` and `rust i32×i32`/`i64×i64` |

**`csharp:short×short` and `java:short×short` appear in 10 of the 12
cliques** — this is the mechanism, shown concretely: `short` never
reaches overflow within the sampled X set, so it agrees with the
wrap camp, the exact camp, AND php's approximating camp simultaneously
— not because it IS any of those operations, but because its narrow
declared range never exercises the fracture. This is the owner's own
"differ by cardinality" pattern, reproduced here at PROFILE grain
inside a single operator's mode family, even though it never rises to
a full cross-OPERATOR match (§4 below).

**So: VALUE-reading part count is reading-dependent on which
operationalisation of "part" is used** — 3 (connected components,
provably not trustworthy here) vs 14 (maximal cliques, consistent with
the settled `GROUP` definition). Flagged, not resolved.

## 3. the owner's specific worry, tested: coincidental matches between DIFFERENT operator spellings

Scope: pairs of DIFFERENT operator NAMES (`amp` vs `ampamp`, not
`cpp.gt` vs `java.gt`) that come out identical or containing.

| reading | differing-name containment pairs (op_id level) | distinct operator-NAME pairs behind them |
| --- | --- | --- |
| VALUE | 227 | 7 |
| ALL-CELLS | 101 | 6 |

The 7 distinct name-pairs (VALUE reading): `(amp, ampamp)`, `(ampamp,
and)`, `(bangeq, bangeqeq)`, `(eqeq, eqeqeq)`, `(or, pipepipe)`,
`(pipe, pipepipe)`, `(qcolon, qq)`. ALL-CELLS drops `(qcolon, qq)` —
6 remain.

**Classification, checked cell-by-cell, not asserted:**

| name pair | classification | evidence |
| --- | --- | --- |
| `(ampamp, and)`, `(or, pipepipe)` | **genuine** | deliberate cross-language synonyms — ruby's own `&&`/`and` sanity control (`l3_cart_gen.py` docstring, "the positive control that says the harness is measuring what it claims to") |
| `(amp, ampamp)`, `(pipe, pipepipe)` | **genuine, domain-restricted** | checked directly: `csharp.amp` vs `csharp.ampamp` on `bool bool` — `true & true = true`, `true & false = false`, `false & true = false`, `false & false = false`, identical to `&&` at every one of these 4 cells. Non-vacuous (varies with input), provably identical for boolean operands with no side effects observed — a real fact, not a sampling accident. Confined to `truth|truth` blocks because `&&`/`\|\|` have no OTHER domain in any of the 12 languages. |
| `(eqeq, eqeqeq)`, `(bangeq, bangeqeq)` | **genuine, type-restricted** | span `whole\|whole`, `fractional\|fractional` AND `truth\|truth` (both L1 and L2) — NOT confined to a narrow corner. When both operands are pinned to the identical static type (which every profile here is, by construction — `lhs_holder`/`rhs_holder` are declared types), `==` and `===` cannot diverge: there is no cross-type coercion for `===` to refuse that `==` would have allowed. Real, not coincidental — though it says nothing about mixed-type operands, which this probe design never declares. |
| `(qcolon, qq)` | **coincidental — confirmed by direct cell inspection** | see below |

### the one confirmed coincidental match: dart `??` vs kotlin `?:`

`dart.qq` contains `kotlin.qcolon` under the VALUE reading, over ALL
12 of `kotlin.qcolon`'s blocks (not just `truth|truth`) — the
strongest-looking match in the whole survey. Investigated because
`??`/`?:` are conceptually DIFFERENT-enough operators (nullish
coalescing vs. Kotlin's Elvis, which also null-checks — plausibly the
same operation) to be worth checking rather than assuming either way.

**The measurement is vacuous.** Neither language's holder table
declares a NULLABLE holder for `qcolon`/`qq` in ANY form:

- `kotlin.qcolon.L1.csv`, `whole|whole`, holder `Int Int` (not `Int?
  Int`): every value cell is the SAME regardless of the right operand
  — `-42 ?: {-42,-1,0,1,7,42,1000}` all answer `[-1, 1.3125, 5]` (the
  canon of −42, unchanged); `1000 ?: {anything}` always answers the
  canon of 1000. **`?:` measures as "always return the left operand,"
  because the left operand is never null in this data.**
- `dart.qq.L1.csv`, `whole|whole`, holders are all non-nullable too:
  `int`, `BigInt`, `double_whole` — no `int?`.
- Even inside `truth|truth`, where `nil` IS a representable X-set
  member, both operators' only holder pair (`bool bool` / `Boolean
  Boolean`) is the non-nullable boolean type, so `nil` lands
  `UNREPRESENTABLE` on both sides at every one of the 32
  nil-involving cells; the only 4 comparable cells are
  `{true,false}×{true,false}`, where BOTH operators are still
  vacuously "return lhs."

**Neither operator's actual null-coalescing branch fires anywhere in
this dataset.** The containment is real (they genuinely agree
everywhere both answer) but it is agreement between two constant
functions, not evidence `??` and `?:` are the same operation — this
traces to a probe-design/holder-table gap (no nullable holder was ever
declared for either language for this operator), not an inherent
semantic question.

**Coincidental op_id-level pairs:**

| reading | coincidental pairs | which |
| --- | --- | --- |
| VALUE | 2 | `dart.qq ⊇ kotlin.qcolon`, `typescript.qq ⊇ kotlin.qcolon` |
| ALL-CELLS | 0 | (the vacuous match doesn't survive full literal equality — `UNREPRESENTABLE` footprints differ) |

## 4. the three-filter stack, applied to the coincidental residue

Applied in order to the 2 VALUE-reading coincidental pairs (ALL-CELLS
already has 0 — nothing to filter):

| step | what it checks | residue after |
| --- | --- | --- |
| start | — | 2 |
| (a) match profile input types | already true by construction — containment only ever compares profiles inside the SAME gate block (`form_pair/level`), so every compared pair already shares its form on both sides | 2 |
| (b) match profile cardinality | also already true by construction — every profile in one block shares the SAME X-set size (`truth` = 6 throughout, `whole` = 17, `fractional` = 16); nothing to remove | 2 |
| (c) match on cells of the same mode (or non-mode) | **my operationalisation, not a ruling**: MODE is defined only for the guaranteed-add family the census actually rules on — `{+, -, *}` get one of `wrapping / growing / php's-approximating / unspecified(rust debug)`; every other operator (`??`, `?:`, and all of §3's comparison/logical operators) has no guarantee to carry and is tagged `non-mode`. The filter's own `(or non-mode)` clause admits non-mode/non-mode pairs. `qq`/`qcolon` are both non-mode → filter passes them | 2 |

**The stack removes nothing.** Residue after all three filters: **2**
(VALUE reading), **0** (ALL-CELLS reading, already empty). Both are
already small enough to sort by hand — and already sorted by hand
above: the surviving pair traces to a specific, nameable, fixable data
gap (no nullable holder was ever probed for `??`/`?:` in dart or
kotlin), not to an unresolved ambiguity. The filters as specified have
no criterion for "the profile is a constant function of one argument,"
which is what actually explains this survivor — worth naming as a
FOURTH candidate filter, not applied here (that would be deciding).

---

## decided, recorded for audit

- `ops(lang)` (`l3_cart_gen.py`) and `kinds_<lang>.json`'s anonymous
  token lists were read directly, not assumed, for every candidate in
  Job 1; every UNVERIFIED marking above means "absent from grammar
  extraction AND absent from every other file in the repo," checked
  both ways.
- dart's `~/` was found ALREADY in scope and already probed
  (`matrices_full_v2/dart.tildeslash.{L1,L2}.csv` exist) — the brief's
  framing of it as a starting point to verify is corrected here, not
  silently dropped.
- swift's `&+`/`&-`/`&*` gap is doubled: absent from `l3_accept.py`'s
  own candidate list AND absent from the grammar extraction, the
  latter explained mechanically by Swift's `custom_operator` grammar
  node (a regex-lexed category, confirmed against the archived
  tree-sitter node-types.json), not merely asserted.
- Job 2's two readings were computed fresh over `matrices_full_v2/`
  (`Research/kind_fuzz_clustering/log065_readings.py`,
  `log065_containment_readings.json`), independent of
  `operator_dominance_v1.json`/`v2.json` (log_056/064's own products,
  which implement a third, hybrid definition and are cited for
  cross-reference only, never overwritten).
- Every classification in §3 (genuine vs. coincidental) is backed by
  cell-level inspection quoted in this log, not asserted from the
  operator name alone — including the one case (`amp`/`ampamp`) that
  looked risky by CLAUDE.md's own precedent (`*`/`&` on `{0,1}`) and
  turned out to be a real, non-vacuous, non-coincidental fact for
  boolean operands specifically.
- The VALUE-reading mode-partition ambiguity (§2: 3 components vs. 14
  cliques) is recorded as a measured fact about the chaining hazard
  `SUPPORT_ontology.md` already named, with a concrete witness pair
  (`cpp int32_t×int32_t` vs `cpp int32_t×int64_t`, 14 conflicting
  cells), not resolved into one number.

## awaiting the owner

1. **Which reading is THE weight for containment/mode work** — still
   open; §1–§2 give the concrete diff (678 pairs, 3-vs-14 parts) to
   decide from, per the owner's request, not a recommendation.
2. **Closing the swift `&+`/`&-`/`&*` gap** — ~459,000 cells estimated,
   cheap, but needs (a) a grammar-extraction fix for
   `kinds_swift.json` (or a bypass using the `custom_operator` node
   type) and (b) adding the three spellings to
   `l3_accept.py`'s `EXTRA["swift"]`. Not run.
3. **Whether to open the method/block scope question** — 13
   method/block candidates found (§ Job 1 close), none run, none
   costed beyond the one operator-spelling exception; "builtins are
   out of scope until the owner opens it" stands unless he opens it.
4. **A fourth filter for the vacuous-profile case** — the owner's 3-filter
   stack does not catch the one confirmed coincidental match (§4);
   the residue is small enough (2) that hand-sorting already found and
   explained it, but the stack itself has a gap if this pattern
   recurs at larger scale.
5. **Is `MODE(profile) = non-mode` for every operator outside `{+, -,
   *}` the right scope for filter (c)?** Recorded as my
   operationalisation (§4), explicitly not a ruling — division/modulo
   have their OWN fracture (F-i3/F-i4, floor/truncate/Euclidean) that
   this operationalisation deliberately did not fold into "mode."
