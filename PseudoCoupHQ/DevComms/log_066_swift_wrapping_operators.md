# log 066 — closing swift's `&+`/`&-`/`&*` gap

2026-08-23. Closes the one genuine operator-spelling gap log_065
diagnosed: Swift's wrapping-arithmetic operators `&+`, `&-`, `&*` are
never seen by `l3_accept.ops()`'s grammar extraction, because Swift
lexes them as a REGEX-MATCHED `custom_operator` grammar node rather than
fixed anonymous tokens. the owner greenlit running these at BOTH levels,
2026-08-23. Read first: `PseudoCoupHQ/CLAUDE.md`,
`DevComms/log_065_spelling_gaps_and_reading_comparison.md` (Job 1, the
diagnosis and cost estimate), `DevComms/log_062_remaining_language_emitters.md`
(the swift emitter), `DevComms/log_063_cpp_lane_throughput_fix.md` (the
stall watchdog every compiled lane now carries).

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

---

## 1 — the extraction workaround, and why it was needed

Confirmed directly (not re-asserted from log_065): `l3_accept.ops("swift")`
intersects a candidate vocabulary against `kinds_swift.json`'s own
`anonymous`/`anonymous_positioned` token lists, and that file's 109-entry
`anonymous` list carries exactly one `&`-token (`&&`). `&+`/`&-`/`&*` are
real swift infix operators (Swift's `FixedWidthInteger` protocol) but are
lexed by Swift's grammar as a `custom_operator` node — a regex-matched
category, not fixed strings — so a fixed-token enumeration structurally
cannot see them, at any candidate-list size. They are OPERATOR spellings,
not library calls, so they belong in the operator data despite the
extraction blindness.

**The fix is a hand-added, clearly-labelled addition, not a change to the
extraction path.** `Research/kind_fuzz_clustering/l3_cart_gen.py` gained a
new section (`SWIFT_WRAP_OPS`, `SWIFT_WRAP_INT_REPS`,
`swift_wrap_cells_l1`, `swift_wrap_l1_output_types`,
`swift_wrap_cells_l2`, `emit_swift_wrap`) kept in a **separate namespace**
from `ops("swift")` / `accepted_static("swift")` / `static_cells_l1/l2`.
`ops("swift")` and `acceptance_swift_A2.json` are the census's own
MEASURED products (a real swiftc `-typecheck` acceptance run); folding a
hand-derived verdict into them would blur measured and hand-derived data
in one file, and would also renumber or commingle probe ids with the
ALREADY-RUN `ct_swift_l1.txt`/`ct_swift_l2.txt` lanes. This is a
mechanical decision (reversible by merging later), not a structural one,
and is flagged as such below.

**Acceptance, not measured by a fresh swiftc pass — derived, and the
derivation is checked, not asserted.** `&+`/`&-`/`&*` are declared in the
Swift standard library only on types conforming to `FixedWidthInteger`
(`static func &+ (Self, Self) -> Self` — same type on both operands and
the result, no promotion). This is a **narrower version of a pattern
already measured** for `*` in `acceptance_swift_A2.json`: read directly,

| operation | ACCEPT pairs (of 576 candidate pairs) |
| --- | --- |
| `*` | `Int Int, Int32 Int32, Int64 Int64, UInt64 UInt64, Double Double, Float Float` — same-type only, 6 pairs |

so same-type-only is a MEASURED fact for this operator family, not a new
assumption. `&+`/`&-`/`&*`'s domain is that same same-type rule
restricted to the four INTEGER holders (`Double`/`Float` do not conform
to `FixedWidthInteger`, so they were taken REFUSE — general Swift-language
knowledge, UNVERIFIED by a swiftc acceptance measurement, but consistent
with every non-`FixedWidthInteger` swift holder already REFUSING `*` for
the identical protocol-conformance reason).

**Safe in both directions by construction, and this ran clean.** An
over-included cell would simply fail to compile and bisect down to
`BUILDFAIL` (which `read_rust` already folds to REFUSE, log_062 §7) —
wasted compile time, not a wrong answer. The actual run: **2,142 of 2,142
L1 probes answered, 0 raises, 0 aborts, 0 buildfail; 74,163 of 74,163 L2
probes answered, 0 raises, 0 aborts, 0 buildfail.** Every hand-derived
ACCEPT cell compiled and ran; nothing was over- or under-included as far
as this run can show.

---

## 2 — real probe counts versus log_065's estimate

log_065 estimated ~2,142 at L1 and ~456,822 at L2, extrapolated from
swift's own 4-holder integer table (`Int` n=16, `Int32` n=9, `UInt64`
n=11, `Int64` n=16).

| level | log_065 estimate | measured (this run) | note |
| --- | --- | --- | --- |
| L1 | 2,142 | **2,142** | exact match |
| L2 | 456,822 | **74,163** | log_065's estimate used L1's `n⁴` per holder (`16⁴+9⁴+11⁴+16⁴=152,274` per op); the REAL level-2 probe count uses the level-2 RESTRICTED `X'` set per holder (`Int` n=10, `Int32` n=5, `UInt64` n=8, `Int64` n=10 — the same narrower set every other STATIC8 language's L2 already uses), giving `(10·10)²+(5·5)²+(8·8)²+(10·10)²=24,721` per op. Cross-checked against swift's own already-run `ct_swift_l2.sh`, whose declared probe count (35,009) matches the identical L2-restricted-set formula exactly, not the L1-`n⁴` one. |
| **total** | ~459,000 | **76,305** | |

**This is a real correction to log_065's own estimate**, caught by
generating for real rather than trusting the extrapolation: the L2 method
log_065 used was the wrong formula for this codebase's level-2 design
(`X'`, not `X` to the 4th power).

Cells: **12 at L1, 12 at L2** (3 operators × 4 same-type integer
holders), both levels — no cell was skipped at L2 (every L1 answer's own
measured swift type was, unsurprisingly, the same holder it started as,
confirmed by reading `ct_swift_wrap_l1.txt` back rather than assumed).

---

## 3 — lanes, submission, wall times

Manifest: the live batch `pygo-emitters-log061` was inspected first
(`python3 PUBLIC/Airlock/airlock status`) and found **complete**
(30/30 lanes, 100% by weight) — not joined. A new manifest was written,
`bash PUBLIC/Airlock/batch.sh swift-wrap-log066
ct_swift_wrap_l1.sh:2142`, then extended for L2 via
`airlock submit --batch swift-wrap-log066 --weight 74163`.

**Container bind check, stated as a limitation.** `python3
PUBLIC/Airlock/airlock doctor` in this session reports `podman is
not on PATH here, so every container check is skipped` — `check_binds`
(the specific check the brief asked for) is nested inside
`check_container` and never runs when podman is absent, so it could not
be positively confirmed from this sandbox before submitting. This was
not a stop condition in practice: both lanes were picked up by the daemon
within seconds of dropping, ran to completion, and their `agent/out`
products decode correctly (§4) — strong indirect evidence the runner IS
bound to this repo's `agent/` folders, but not the direct `check_binds`
confirmation the brief asked for. Flagged, not asserted as verified.

| lane | probes | dry-run | exit | elapsed | notes |
| --- | --- | --- | --- | --- | --- |
| `ct_swift_wrap_l1.sh` | 2,142 | 0 refusals | 0 | 6.8 s | 6 chunk files, cap 400/file (unchanged `STATIC8_CHUNK["swift"]`), stall_s=0.000 throughout |
| `ct_swift_wrap_l2.sh` | 74,163 | 0 refusals | 0 | 244.3 s | 186 chunk files, cap 400/file, stall_s=0.000 throughout, well under the ~30 min shard threshold (projected 224 s at swift's log_062-measured 3.02 ms/probe) so NOT sharded |

L1 ran before L2 was generated, per the brief: `swift_wrap_cells_l2()`
reads `ct_swift_wrap_l1.txt`'s real measured output types (never a
guess), so the L2 lane could not exist before L1 finished.

---

## 4 — fold verification

`Research/kind_fuzz_clustering/l3_cart_read.py`'s shared `build()` gained
a `lang == "swift_wrap"` branch (base holder table = swift's, but its own
op list `G.SWIFT_WRAP_OPS` and its own cells
`G.swift_wrap_cells_l1/l2()`), and `main()`'s `plan` list gained two
entries (`("swift_wrap", 1, ...)`, `("swift_wrap", 2, ...)`) reading
`ct_swift_wrap_l1.txt` / `ct_swift_wrap_l2.txt` through the existing,
UNCHANGED `read_rust` — no new payload branch, exactly log_062 §7's
reasoning (every STATIC8 lane emits the rust line shape). `swift_wrap` is
kept as its own language tag, never merged into `swift`'s own rows, for
the same reason `rust_release` is kept distinct from `rust`: a different
measurement condition (hand-derived acceptance, not the census's swiftc
run) that must never silently blend into the grammar-measured rows.

Folded with the EXISTING readers, exactly as log_064 did:

```
AIRLOCK_OUT=.../Airlock/agent/out python3 l3_cart_read_v2.py \
    --only=swift_wrap.L1,swift_wrap.L2 --merge --no-verify
```

then `nice -n 15 python3 l3_cart_full_v2.py` (unconditional full
re-derivation from `matrices_cart_v2/`, as it always is).

**Byte-identity of everything already there, confirmed both directories,
by full-file SHA-256 before/after (473 pre-existing files each):**

| directory | pre-existing files changed | pre-existing files missing | new files |
| --- | --- | --- | --- |
| `matrices_cart_v2/` | **0** | **0** | 6 (`swift_wrap.{ampplus,ampminus,ampstar}.L{1,2}.csv`) |
| `matrices_full_v2/` | **0** | **0** | 6 (same names) |

Format verification (`l3_cart_read.verify`) over the merged
`matrices_cart_v2/`: 479 files, 11,077 rows, 33,159,198 probes,
**0 non-rectangular lines, 0 wrong vector lengths, 0 empty slots, 0
dirty canon cells.** `l3_cart_full_v2.py`'s own unconditional assertions
(rectangularity, one grid size per `(form_pair, level)`) passed —
otherwise the run would not have completed. New row totals: 12 rows ×
2,142 probes (L1) + 12 rows × 74,163 probes (L2) = 76,305 probes across 6
new operator matrices, matching the lane counts exactly.

**Four independent cell checks, raw lane text → CSV, decoded fresh from
the `INT:`/`UINT:` hex tokens (two's-complement / unsigned, per
`CLAUDE.md`'s spec) rather than trusting the project's own canon code**:

| check | raw lane line | expected (hand-computed) | CSV cell (`matrices_cart_v2`) | match |
| --- | --- | --- | --- | --- |
| `&+`, `Int Int`, `(2^63-1, 42)`, L1 | `A0_3_3_249\|Int\|INT:64:8000000000000029` | two's-complement wrap of `9223372036854775849` = `-9223372036854775767` | `[-1, 1.9999999999999999911095421856189, 62]` | yes |
| `&-`, `Int32 Int32`, `(-2^31, 1)`, L1 | `A1_4_4_4\|Int32\|INT:32:7fffffff` | `Int32.min - 1` wraps to `Int32.max = 2147483647` | (raw hex `0x7fffffff` = `2147483647`, decoded independently) | yes |
| `&*`, `UInt64 UInt64`, `(2^64-1, 42)`, L1 | `A2_5_5_113\|UInt64\|UINT:64:ffffffffffffffd6` | `((2^64-1)*42) mod 2^64 = 18446744073709551574` = `0xffffffffffffffd6` | (raw hex matches independently computed wrap) | yes |
| `&+`, `Int Int`, `(1,1,1,1)`, L2 | `B0_3_3_3333\|Int\|INT:64:0000000000000004` | `(1&+1)&+(1&+1) = 4` | `[1, 1.0, 2]` | yes |

All four raw-hex values were decoded and canonised independently (plain
`Fraction`/`Decimal` arithmetic, two's-complement/unsigned parsing spelled
out inline, no import of the project's canon functions) and matched the
CSV cell in every case, including the full-grid mapping (checked
separately for the first key: `matrices_full_v2/swift_wrap.ampplus.L1.csv`
position 264 of the 17-point full whole/L1 grid also reads
`[-1, 1.9999999999999999911095421856189, 62]`).

---

## 5 — the measured fact the mode work asked for

**At `(2^63-1) + 42` on swift's 64-bit `Int` holder, `&+` gives EXACTLY
the same canon as the wrap part every other language's 64-bit wrapping
holder gives** (log_064 §4a: `cpp, csharp, go, java, kotlin,
rust_release` all answer this at their 64-bit holders):

```
A0_3_3_249|Int|INT:64:8000000000000029
```

decodes (two's-complement, bit pattern `0x8000000000000029`) to
`-9223372036854775767`, whose canon is

```
[-1, 1.9999999999999999911095421856189, 62]
```

— the pasted cell, `matrices_cart_v2/swift_wrap.ampplus.L1.csv`,
`probe_id=A0_3_3` (`Int Int`), position 249 of 256:

| lhs_holder | rhs_holder | cell at `(2^63-1, 42)` |
| --- | --- | --- |
| `Int` | `Int` | `[-1, 1.9999999999999999911095421856189, 62]` |

Swift's `&+` therefore joins the WRAP part with the same canon
`cpp int64_t`, `csharp long`, `go int64`, `java long`, `kotlin Long` and
`rust_release i64` already share at this key. This closes log_065's
statement that swift and dart could not appear in the `+` mode-partition
evidence at all — swift now can, through its hand-added `&+` spelling,
though this fact has NOT been folded into `operator_dominance_v2.json`
or re-run through `l3_operator_dominance_v2_twelve.py` (out of scope
here; flagged below).

---

## products

| file | what changed |
| --- | --- |
| `Research/kind_fuzz_clustering/l3_cart_gen.py` | +191 lines, purely additive: `SWIFT_WRAP_OPS`, `SWIFT_WRAP_INT_REPS`, `swift_wrap_cells_l1`, `swift_wrap_l1_output_types`, `swift_wrap_cells_l2`, `emit_swift_wrap`. Nothing else in the file touched — `ops()`, `accepted_static()`, `static_cells_l1/l2()`, every existing emit function, `STATIC8_*`, `MS_PER_PROBE`, the stall/startup constants: all unchanged, confirmed by diff and by re-running `ops("swift")`/`static_cells_l1("swift")`/`static_cells_l2("swift")` before and after (62 L1 cells, 8 L2 cells, both unchanged) |
| `Research/kind_fuzz_clustering/l3_cart_read.py` | `build()` gained a `lang == "swift_wrap"` branch (mechanical `if`, no existing branch's logic moved or altered); `main()`'s `plan` list gained two entries reading `ct_swift_wrap_l1.txt`/`ct_swift_wrap_l2.txt` through the unchanged `read_rust` |
| `Research/kind_fuzz_clustering/lanes/ct_swift_wrap_l1.sh`, `ct_swift_wrap_l2.sh` | the two new lanes, generated by `emit_swift_wrap`, on the unmodified `STATIC8_SH`/`STATIC8_DRIVER` template |
| `Airlock/agent/batch.json` | new manifest, label `swift-wrap-log066`, 2 lanes, weight 76,305 (the previous batch `pygo-emitters-log061` was complete and is not disturbed — its own record lives in `Airlock/agent/status/*.status`, untouched) |
| `Research/kind_fuzz_clustering/matrices_cart_v2/swift_wrap.{ampplus,ampminus,ampstar}.L{1,2}.csv` | 6 new files, 12 rows / 2,142 probes (L1) + 12 rows / 74,163 probes (L2) |
| `Research/kind_fuzz_clustering/matrices_full_v2/swift_wrap.{ampplus,ampminus,ampstar}.L{1,2}.csv` | 6 new files, full-grid re-derivation of the above |
| both `index.json` | updated additively (`--merge`); every pre-existing entry, and every pre-existing `.csv` byte, confirmed unchanged by SHA-256 |

---

## decided, recorded for audit

- **The extraction workaround is a hand-added, separately-namespaced
  addition** (`SWIFT_WRAP_*`), not a change to `l3_accept.ops()` or to
  `kinds_swift.json`'s grammar extraction — the extraction blindness is
  structural (Swift's `custom_operator` regex-lexed node) and is worked
  around, not fixed, exactly as the brief allowed.
- **Acceptance for the 3 new operators is DERIVED, not measured by a
  fresh swiftc pass** — same-type-only, restricted to swift's 4 integer
  holders, extending a pattern (`*`'s same-type-only ACCEPT set)
  already measured in `acceptance_swift_A2.json`. The run itself
  (2,142/2,142 and 74,163/74,163 answered, 0 buildfail on either level)
  is consistent with this derivation being exactly right, not merely
  safe.
- **log_065's L2 estimate (456,822) is corrected to a measured 74,163**
  — the estimate used L1's holder sizes to the 4th power; the codebase's
  actual level-2 design uses the smaller, level-2-restricted `X'` set
  per holder, cross-checked against swift's own already-run L2 lane's
  declared probe count (35,009, using the identical restricted-set
  formula).
- **Fold verified two ways**: SHA-256 byte-identity of all 473
  pre-existing files in both `matrices_cart_v2/` and `matrices_full_v2/`
  (zero changed, zero missing), and four independent raw-hex-to-canon
  spot checks across L1 and L2, three operators, three different
  holders, matching the CSV cells exactly.
- **The measured fact**: swift's `&+` on `Int Int` at `(2^63-1, 42)`
  answers `[-1, 1.9999999999999999911095421856189, 62]`
  (`INT:64:8000000000000029`), byte-identical to the wrap-part canon
  log_064 §4a already recorded for `cpp/csharp/go/java/kotlin/
  rust_release`'s 64-bit wrapping holders.
- Did not touch `matrices_cart/` or `matrices_full/` (superseded, per
  the brief). Did not re-run `ct_swift_l1.sh`/`ct_swift_l2.sh` (already
  done) or any other already-completed lane. Did not start, stop, or
  attempt to start/stop podman or any container. Did not fold this fact
  into `operator_dominance_v2.json` or re-run
  `l3_operator_dominance_v2_twelve.py`.

## awaiting the owner

1. **Whether `swift_wrap` should stay a separate language tag or be
   merged into `ops("swift")`/`acceptance_swift_A2.json` proper.** A
   mechanical choice made here (kept separate, reversible), not a
   structural ruling — flagged because it affects how downstream
   mode-partition/containment queries will find (or not find) these
   three operators under the name "swift" versus "swift_wrap".
2. **`operator_dominance_v2.json` was not re-run** with `swift_wrap`
   folded in — §5's fact was checked by hand against the raw CSV, not
   through the dominance/containment tooling. Re-running
   `l3_operator_dominance_v2_twelve.py` over the now-larger
   `matrices_full_v2/` would surface whether `swift_wrap`'s `&+` lands
   in log_064 §4a's existing wrap part or forms its own — expected to
   be the former given §5, not yet confirmed through that tooling.
3. **The container-bind check (`check_binds`) could not be run directly**
   in this session (podman absent from `PATH`) — confirmed only
   indirectly, by both lanes being picked up and completing correctly
   against `Airlock/agent/`. If a direct `airlock doctor` bind
   confirmation matters for the record, it needs a session with podman
   on `PATH`.
