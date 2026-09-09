# log 062 — the remaining eight emitters: php, typescript, java, kotlin, c++, swift, dart, c#

2026-08-22. log_052 ran rust and ruby. log_061 added python (the
interpreted shape) and go (the compiled shape). This log adds the
**remaining eight**, on those same two patterns, and leaves every lane
generated, validated and ready to submit so the run needs no agent.

**Nothing about the design changes.** Same `X` / `X'` sets, same
canonical form, same probe-index rule, same outcome vocabulary
(`REFUSE`, `RAISE:<kind>`, `ABORT`, `UNREPRESENTABLE`), level 1
`y = op(x0,x1)` over all ordered pairs of `X`, level 2
`z = op(op(x0,x1), op(x2,x3))` over `X'`. Eight emitters are added and
nothing else moves.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

**No language was skipped.** All eight are emitted. That is the
headline, because the brief expected c# to be blocked — see section 1.

---

## 1 — TOOLCHAIN REALITY, verified rather than trusted

The brief said Airlock's image inventory records `.NET` as absent and
that this would block c#. **The inventory is correct and the conclusion
is wrong**, and the reason is worth recording because it applies to four
languages at once.

`Airlock/README.md`'s "image inventory" is verified line by line against
`Airlock/Containerfile`, and that Containerfile genuinely installs no
.NET, no Kotlin, no Swift and no Dart. But the image is not the whole
filesystem the runner sees. **`up.sh` line 118 and
`quadlet/sandbox-runner.container` line 50 both mount the named podman
volume `sandbox-persist` at `/persist`** — and so do SandboxDesign's,
identically, so the two installs share it. The layer-2 and layer-3
campaigns installed four toolchains into that volume (log_018, log_019,
log_020, log_023) and every lane since has reached them by putting
`/persist/...` on `PATH`.

Inspected directly on the host, at
`~/.local/share/containers/storage/volumes/sandbox-persist/_data/`:

| language | where it actually is | evidence |
|---|---|---|
| c++ | the image | `Containerfile`: `gcc-15 g++-15 clang-21` |
| java | the image | `Containerfile`: `openjdk-25-jdk-headless` |
| php | the image | `Containerfile`: `php-cli` |
| typescript | node in the image; the checker in the volume | `Containerfile`: `nodejs npm`; `/persist/tv/ts5/node_modules/typescript/lib/tsc.js` present |
| kotlin | **the volume** | `/persist/kotlinc/lib/kotlin-stdlib.jar` and the whole `lib/` tree present |
| swift | **the volume** | `/persist/swift/usr/bin/swift-frontend`, `swift-driver`, `clang-17` present |
| dart | **the volume** | `/persist/dart-sdk/bin/dart` present |
| **c#** | **the volume** | `/persist/dotnet/dotnet` and `/persist/dotnet/sdk/10.0.400/` present, plus `/persist/dotnet-csc-build.sh` and `/persist/dotnet-csc-run.sh` from log_023 |

So `.NET` is absent from the **image** and present in the **volume**,
at SDK **10.0.400**. c# is not blocked, and no c# emitter is skipped.

**What is unverified, stated as unverified.** `podman` is not on this
session's `PATH`, so nothing above was confirmed from *inside* a running
container; it is confirmed from the volume's own directory on the host
plus the mount lines in `up.sh` and the quadlet unit. Two further
caveats:

- `swiftc` and `swift` themselves are symlinks and a directory listing
  does not show them; what is confirmed present is `swift-frontend` and
  `swift-driver` in the same `usr/bin`. The exact path the lanes use,
  `/persist/swift/usr/bin/swiftc`, is the path `l3_exec_lanes.py` used
  for the execution campaign that log_032 measured at 3.02 ms/probe, so
  it resolved then.
- the **libncurses symlink does not persist** — it lives in the image's
  own `/usr/lib`, not in the volume — so every generated lane re-makes
  it in its preamble, exactly as `l3_exec_lanes.PRELUDE` has since
  log_027.

**The dart egress question, settled.** `.googleapis.com` was needed to
**install** the dart SDK (log_019, log_020), not to run it. These lanes
call `dart compile exe` on one self-contained file with no `pubspec`, no
package resolution and no download, so they need no allowlist entry.
Airlock currently has no `proxy/allowlist.txt` at all and that blocks
none of these eight.

**Every lane refuses itself in seconds if its toolchain is missing.**
Each compiled lane runs a one-line probe (`test -x
/persist/kotlinc/bin/kotlinc`, `/persist/dotnet/dotnet --version`, …)
before it unpacks anything, prints the exact path it tried and where
that toolchain lives, and exits **4**. A missing toolchain therefore
costs seconds, not an hour.

---

## 2 — the holders, and what is deliberately left out

Every holder is the layer-2 census's own `rep`
(`Research/data_representation/representations_<lang>.json`). Nothing is
invented, widened or renamed.

| language | form | holder | L1 points | L2 points |
|---|---|---|---|---|
| php | truth | `bool` | 6 | 6 |
| php | whole | `int` | 16 | 10 |
| php | fractional | `float` | 16 | 10 |
| typescript | truth | `boolean` | 2 | 2 |
| typescript | whole | `number` | **12** | **8** |
| typescript | whole | `bigint` | 17 | 10 |
| typescript | fractional | `number` | 16 | 10 |
| java | truth | `boolean` | 2 | 2 |
| java | truth | `Boolean` | 2 | 2 |
| java | whole | `short` | 7 | 4 |
| java | whole | `int` | 9 | 5 |
| java | whole | `long` | 16 | 10 |
| java | whole | `Integer` | 9 | 5 |
| java | whole | `Long` | 16 | 10 |
| java | fractional | `double` | 16 | 10 |
| java | fractional | `float` | 7 | 4 |
| kotlin | truth | `Boolean` | 2 | 2 |
| kotlin | whole | `Int` | 9 | 5 |
| kotlin | whole | `Long` | 16 | 10 |
| kotlin | fractional | `Double` | 16 | 10 |
| kotlin | fractional | `Float` | 7 | 4 |
| c++ | truth | `bool` | 2 | 2 |
| c++ | whole | `int32_t` | 9 | 5 |
| c++ | whole | `int64_t` | 16 | 10 |
| c++ | whole | `uint64_t` | 11 | 8 |
| c++ | whole | `__int128` | 17 | 10 |
| c++ | fractional | `double` | 16 | 10 |
| c++ | fractional | `float` | 7 | 4 |
| swift | truth | `Bool` | 2 | 2 |
| swift | whole | `Int` | 16 | 10 |
| swift | whole | `Int32` | 9 | 5 |
| swift | whole | `Int64` | 16 | 10 |
| swift | whole | `UInt64` | 11 | 8 |
| swift | fractional | `Double` | 16 | 10 |
| swift | fractional | `Float` | 7 | 4 |
| dart | truth | `bool` | 2 | 2 |
| dart | whole | `int` | 16 | 10 |
| dart | whole | `BigInt` | 17 | 10 |
| dart | whole | `double (whole number)` | **12** | **8** |
| dart | fractional | `double` | 16 | 10 |
| dart | fractional | `num` | 16 | 10 |
| c# | truth | `bool` | 2 | 2 |
| c# | whole | `short` | 7 | 4 |
| c# | whole | `int` | 9 | 5 |
| c# | whole | `long` | 16 | 10 |
| c# | whole | `ulong` | 11 | 8 |
| c# | fractional | `double` | 16 | 10 |
| c# | fractional | `float` | 7 | 4 |

**A NEW REPRESENTABILITY RULE, and why it is not a design change.** Two
of the census's WHOLE-form holders are binary64 — typescript `number`
and dart `double (whole number)`. Neither has an integer range, so the
existing range test says nothing about them. Their representability is
**exactness as a double**, tested by `float(v) == v`, which is an exact
comparison in python between an int and a float and therefore an
exactness test rather than a rounding test. `2^63` and `2^31` are
present; `2^53+1`, `2^63-1`, `2^64-1`, `-2^63+1` and `-2^53-1` are
**absent**, which is why those two holders carry 12 points and not 17.
This is the settled "representable means EXACTLY representable" rule
reaching a holder shape it had not met, not a new rule.

**Truth is two-of-six in seven of the eight.** php is route C and holds
all six truth points as themselves, like ruby and python. The other
seven declare a real boolean TYPE, so `0`, `1`, `""` and `nil` are
absent from every truth row over them — the same two-of-six rust and go
already carry.

### left out, with the reason and the reversal

A missing column is a finding, so each exclusion is named:

| holder | why it is not carried | how to reverse it |
|---|---|---|
| java `BigDecimal`, kotlin `BigDecimal`, c# `decimal` | `RT_JAVA` / `RT_KOTLIN` fall through to `OPAQUE:<hex of toString>` and `RT_CSHARP` emits `DEC128:<4 words>`; `l3_per_op_matrices.decode_enc` decodes neither. Emitting a column the fold cannot read is worse than not emitting it | add the branch to the runtime, re-emit |
| java `BigInteger`, kotlin `BigInteger` | `RT_JAVA`/`RT_KOTLIN` spell `BIGINT:` as the hex of `toByteArray()`, which is **two's complement**, while `decode_enc` reads a `BIGINT:` payload as signed **magnitude**. `-1` would fold as `255` | correct that one encoding, re-emit |
| c# `System.Numerics.BigInteger` | `RT_CSHARP` has no `BigInteger` case at all; it falls to `OPAQUE:` | add the case, re-emit |
| kotlin `ULong` | `RT_KOTLIN.enc` has no `ULong` branch (it is an inline class over `Long`, not a `Long`), so every answer is `OPAQUE:` | add the branch, re-emit |
| php `GMP`, php `BCMath` | `php-cli` is the only php package in the image, so neither extension is verified present; and BCMath's holder is a **string** carrying a number, so `$a . $b` would measure text concatenation and not arithmetic | install the extension, or model BCMath as a function-call grain, which is a different design |

dart `BigInt` and typescript `bigint` **are** carried: `RT_DART` and
`RT_TS` both spell `BIGINT:` as signed magnitude, which is exactly what
`decode_enc` reads. The unbounded-whole column therefore exists for two
of the eight and is honestly absent for the rest.

---

## 3 — THE FLOAT PATH, per language, with the round-trip proof

log_057's fault: ruby's lane emitted floats as printed text and the
reader read that text as an exact decimal, naming a different real
number than the double — **157 disagreements out of 256 against rust's
`f64`, every one of them ours**. log_061 closed it for python and go by
emitting BITS.

**All eight emit BITS. Not one of them prints a float.**

| language | call that produces the bits | token |
|---|---|---|
| c++ | `memcpy` of the object's bytes, byte-reversed (`RT_CPP._bits`) | `FLOAT:64:<hex>` / `FLOAT:32:<hex>` |
| java | `Double.doubleToRawLongBits` / `Float.floatToRawIntBits` | `FLOAT:<w>:<hex>` |
| kotlin | the same two JDK calls | `FLOAT:<w>:<hex>` |
| swift | `Double.bitPattern` / `Float.bitPattern`, byte-reversed | `FLOAT:<w>:<hex>` |
| dart | `ByteData.setFloat64` (big-endian by default) | `FLOAT:64:<hex>` |
| c# | `BitConverter.GetBytes(double)`, byte-reversed | `FLOAT:64:<hex>` |
| typescript | `DataView.setFloat64(0, v, false)` | `FLOAT:64:<hex>` |
| **php** | **`bin2hex(pack("E", $v))`** — php's own big-endian IEEE-754 double | `FLOAT:64:<hex>` |

The first seven are the **settled `l3_exec.RT_*` runtimes, unmodified** —
the same instruments log_032's execution campaign used. php has no
runtime of its own, so its serialiser is written here and is the only
new float path in this log.

### 3a — the INPUT side, measured for all eight

The declaration each emitter writes is re-parsed and compared bit for
bit against the double it is meant to name. Five witnesses, including
the one at the double's precision limit and the one at `1.0 + 1ulp`:

| witness | the double's bits | php | typescript | java | kotlin | c++ | swift | dart | c# |
|---|---|---|---|---|---|---|---|---|---|
| `+min_subnormal` = `5e-324` | `0000000000000001` | ok | ok | ok | ok | ok | ok | ok | ok |
| `1.0+1ulp` | `3ff0000000000001` | ok | ok | ok | ok | ok | ok | ok | ok |
| `-0.0` | `8000000000000000` | ok | ok | ok | ok | ok | ok | ok | ok |
| `0.1` | `3fb999999999999a` | ok | ok | ok | ok | ok | ok | ok | ok |
| `-max_finite` | `ffefffffffffffff` | ok | ok | ok | ok | ok | ok | ok | ok |

**40 checks, 0 mismatches.** The literals are, verbatim:
`$a = 5e-324;`, `let a: number = 1.0000000000000002;`,
`double a = -0.0;`, `val a: Double = 0.1`,
`let a: Double = -1.7976931348623157e+308`. python's `repr`
round-trips and is a legal double literal in all eight; `-0.0` keeps its
sign in all eight (go was the exception, and go is already handled).

### 3b — the OUTPUT side, measured end to end where a toolchain existed

A lane whose only cell is `double * double` was generated and **run**,
and the emitted `FLOAT:64:` hex compared against
`struct.pack(">d", x).hex()` computed independently. `x * 1.0` is exact
for every finite `x`, including `-0.0` and the min subnormal, so any
disagreement would be the encoding and nothing else.

| witness | c++ emitted | typescript emitted | expected |
|---|---|---|---|
| `+min_subnormal` | `FLOAT:64:0000000000000001` | `FLOAT:64:0000000000000001` | `FLOAT:64:0000000000000001` |
| `1.0+1ulp` | `FLOAT:64:3ff0000000000001` | `FLOAT:64:3ff0000000000001` | `FLOAT:64:3ff0000000000001` |
| `-0.0` | `FLOAT:64:8000000000000000` | `FLOAT:64:8000000000000000` | `FLOAT:64:8000000000000000` |
| `0.1` | `FLOAT:64:3fb999999999999a` | `FLOAT:64:3fb999999999999a` | `FLOAT:64:3fb999999999999a` |
| `-max_finite` | `FLOAT:64:ffefffffffffffff` | `FLOAT:64:ffefffffffffffff` | `FLOAT:64:ffefffffffffffff` |
| `max_finite` | `FLOAT:64:7fefffffffffffff` | `FLOAT:64:7fefffffffffffff` | `FLOAT:64:7fefffffffffffff` |

**12 end-to-end checks, 0 mismatches**, through the real generated lane
source, the real compiler and the real binary.

**java's output call, measured separately.** `javac` is not in this
session's sandbox but `java` is, and a JDK runs a single source file
directly. `Double.doubleToRawLongBits(x * 1.0)` formatted `%016x` —
which is exactly `RT_JAVA.enc` plus `RT_JAVA.ih` — answered:

| witness | measured |
|---|---|
| `5e-324` | `0000000000000001` |
| `1.0000000000000002` | `3ff0000000000001` |
| `-0.0` | `8000000000000000` |
| `0.1` | `3fb999999999999a` |
| `-1.7976931348623157e+308` | `ffefffffffffffff` |

**kotlin's output path is the identical JDK call**, so that measurement
covers kotlin too.

### 3c — corroboration from the products already on disk

kotlin, dart, c# and typescript's own answer products from log_032 —
taken inside this container image, through these same runtimes — already
carry `FLOAT:64:` bit tokens, and they decode correctly:
`4008000000000000` = `3.0`, **`8000000000000000` = `-0.0`**,
`7ff0000000000000` = `+inf`, `7ff8000000000000` = `nan`. The signed zero
surviving the encoding is the sharpest of these, because it is exactly
what a printed-text path loses.

### 3d — what is NOT measured, stated plainly

swift's `Double.bitPattern` and php's `pack("E", ...)` are **not**
executed here — neither toolchain is in this session's sandbox. Both are
single documented bit-extraction calls (`bitPattern` is the raw 64-bit
pattern; php's `E` is documented as big-endian IEEE-754 double), and
both are byte-reversed or big-endian by construction, so no printed
decimal exists anywhere on those paths. Marked **unverified by
execution**, verified by construction and by the input-side table above.

---

## 4 — the operator menus and the accepted-profile sets

Menus are `ops(lang)` in `l3_cart_gen.py`, unchanged: the grammar's own
positioned anonymous tokens intersected with the candidate binary
vocabulary. Nothing was added to any menu — `and`/`or` remain a ruby-only
addition, and it stays ruby-only.

Acceptance is the census's own measurement, read out of the
`acceptance_<lang>_A{1,2}.json` files. Nothing here re-decides
acceptance; php has no such file because it is route C, where execution
is the only acceptance evidence php has.

| language | route | holders | operators | candidate cells | accepted L1 cells | rate |
|---|---|---|---|---|---|---|
| php | C, execution | 3 | 26 | 234 | **234** | 100.0% |
| typescript | A1, static | 4 | 23 | 368 | **81** | 22.0% |
| java | A1, static | 9 | 20 | 1,620 | **713** | 44.0% |
| kotlin | A1, static | 5 | 17 | 425 | **192** | 45.2% |
| c++ | A2, static | 7 | 19 | 931 | **774** | 83.1% |
| swift | A2, static | 7 | 6 | 294 | **62** | 21.1% |
| dart | A2, static | 6 | 17 | 612 | **223** | 36.4% |
| c# | A1, static | 7 | 20 | 980 | **383** | 39.1% |
| *(rust, for scale)* | A2, static | 7 | 19 | 931 | *128* | *13.7%* |
| *(go, for scale)* | A2, static | 7 | 19 | 931 | *116* | *12.5%* |

**The pruning is real data, and it is not uniform.** c++ accepts 83% of
its candidate cells because it converts implicitly between every
arithmetic type; go accepts 12.5% because it refuses every implicit
conversion. rust and go are the hard pruners this line has seen so far,
and c++ is the opposite extreme. swift's 21% is a different story again:
its **menu** is only six operators, because swift's grammar declares
only `* < > >= && ||` as positioned anonymous tokens, so swift
contributes few cells for a reason that has nothing to do with its type
system.

---

## 5 — probe counts, projections, lanes and shards

Probe counts are **exact and deterministic** — the product of the
accepted cells and the X-set sizes, not estimates.

Wall times are **projections**. They are NOT taken at rust's rate: rust
compiles 1,500 probes in 0.31 s and kotlinc compiles 2,000 in about
twenty seconds, so one number for both would be a fiction. Each language
is projected at **its own measured milliseconds-per-probe from log_032's
smoke lanes**, taken inside this same container image. rust appears in
both instruments — 0.30 ms/probe there against log_052's 0.25 ms/probe
on the cartesian run — and the two agree, which is what makes the table
usable. php is route C and is projected at log_052's measured
interpreted rate, 4,003 probes/s.

### level 1 — generated, validated, ready

| lane | cells | probes | rate used | projected wall | shards |
|---|---|---|---|---|---|
| `ct_php_l1.sh` | 234 | 37,544 | 4,003 probes/s | 0m 09s | 1 |
| `ct_typescript_l1.sh` | 81 | 16,238 | 0.24 ms/probe | 0m 03s | 1 |
| `ct_java_l1.sh` | 713 | 89,430 | 0.60 ms/probe | 0m 53s | 1 |
| `ct_kotlin_l1.sh` | 192 | 25,486 | 5.60 ms/probe | 2m 22s | 1 |
| `ct_cpp_l1.sh` | 774 | 96,934 | 1.63 ms/probe | 2m 38s | 1 |
| `ct_swift_l1.sh` | 62 | 10,054 | 3.02 ms/probe | 0m 30s | 1 |
| `ct_dart_l1.sh` | 223 | 46,305 | 0.72 ms/probe | 0m 33s | 1 |
| `ct_csharp_l1.sh` | 383 | 45,011 | 0.76 ms/probe | 0m 34s | 1 |
| **phase 1 total** | **2,662** | **367,002** | | **about 8m** | **8 lanes** |

### level 2 — php generated; the other seven are one command away

| family | probes (upper bound) | projected wall (upper bound) | shards (upper bound) | state |
|---|---|---|---|---|
| php | 1,448,096 | 6m 01s | 1 | **generated** (`ct_php_l2.sh`) |
| typescript | 584,976 | 2m 20s | 1 | awaits `ct_typescript_l1.txt` |
| java | 2,020,148 | 20m 12s | 1 | awaits `ct_java_l1.txt` |
| kotlin | 650,541 | 60m 43s | **2** | awaits `ct_kotlin_l1.txt` |
| c++ | 2,686,491 | 72m 58s | **2** | awaits `ct_cpp_l1.txt` |
| swift | 316,340 | 15m 55s | 1 | awaits `ct_swift_l1.txt` |
| dart | 1,678,096 | 20m 08s | 1 | awaits `ct_dart_l1.txt` |
| c# | 1,023,776 | 12m 58s | 1 | awaits `ct_csharp_l1.txt` |
| **phase 2 total** | **10,408,464** | **under 3h** | | |

The level-2 numbers are **upper bounds**: they assume every level-1 cell
survives the type rule. The real set can only be smaller.

**Why the seven cannot be emitted yet, and why that is not a
formality.** A level-2 cell exists only where `op(y, y)` typechecks, and
`y`'s type is read out of the level-1 lane output — the discipline
`rust_cells_l2` has applied since log_052 and `go_cells_l2` since
log_061. There is no cast-and-catch and no speculative compile. So
"every level-1 lane before any level-2 lane" is a **dependency**, and
the generator names it rather than failing obscurely:

```
ct_java_l2.sh  NOT EMITTED -- level-1 java lane output not found
      (ct_java_l1.txt); run lanes/ct_java_l1.sh first
```

`ct_php_l2.sh` is generated now because php is route C and has no such
question. It is deliberately **not** submitted with phase 1, so that
every level-1 lane finishes before any level-2 lane starts.

**Sharding is derived, not chosen.** `SHARD_TARGET_S = 2400.0`; any
family projecting past forty minutes is cut until no single lane does.
Nothing here projects past the daemon's 3,600 s per-lane ceiling once
sharded, and nothing approaches the ~2 h line.

Whole run: **10,775,466 probes, about three hours of compute** — well
inside a fifteen-hour window.

### the batch

`Airlock/agent/batch.json` already carries
**`pygo-emitters-log061`** with log_061's three queued lanes. Every
command in the runbook **joins** that batch rather than replacing it, so
those three keep their denominator. `--new-batch` is never used.

Two manifests are also written beside the lanes, in Airlock's own
byte-shape (one lane object per line — `progress.sh`'s parser is
line-based, and a manifest that wraps a lane across several lines reads
as no lane at all):

- `Research/kind_fuzz_clustering/lanes/batch_eight-l1-log062.json` —
  8 lanes, weight 367,002
- `Research/kind_fuzz_clustering/lanes/batch_eight-l2-php-log062.json` —
  1 lane, weight 1,448,096

They are a record of what was generated. The manifest Airlock reads is
the one `airlock submit` maintains.

---

## 6 — validation done without the container

Nothing below is a substitute for the Airlock run, and **nothing
produced here is folded into any matrices generation**.

| what | result |
|---|---|
| `python3 -m py_compile l3_cart_gen.py l3_cart_values.py` | clean |
| `l3_cart_values.py` self-check and per-holder table | rust, ruby, python and go point counts **unchanged** (`i32` 9/17, `i64` 16, `u64` 11, `f32` 7, `bool` 2, ruby `Rational` 15) — the new rules touched nothing that existed |
| `sh -n` on all nine generated lanes | all parse |
| `airlock submit --dry-run` on all nine, `--batch pygo-emitters-log061` | **zero refusals, zero warnings** — so every lane has a shebang, no CRLF, an `.sh` name, and a `[n/total]`-style progress line |
| **c++ lane, end to end on the host** | 3 cells, 54 probes, one `g++ -std=c++20` build, **54 answers, 0 raises, 0 aborts, 0 buildfail** |
| **typescript lane, end to end on the host** | 3 cells, 549 probes, one `transpileModule` + `node` run, **549 answers, 0 raises, 0 aborts, 0 buildfail** |
| float round trip, input side | 8 languages x 5 witnesses, **0 mismatches** (section 3a) |
| float round trip, output side | c++ and typescript end to end, 6 witnesses each, **0 mismatches**; java's exact call measured separately (section 3b) |
| generated source, read line by line | kotlin, swift, dart, c# chunk sources inspected: markers present, dispatch tables well formed, start index read from `argv`, `__END__` printed |
| the batch-order hazard | `sorted(os.listdir(drop))` would place `ct_php_l2.sh` **before** `ct_python_l1.sh`, `ct_swift_l1.sh` and `ct_typescript_l1.sh` on a startup sweep — which is why php level 2 is held for phase 2 rather than submitted with phase 1 |

**Not validated by execution:** php, kotlin, swift, dart and c# lanes.
Those five toolchains are not in this session's sandbox. Their sources
were read and their build and run invocations are copied unchanged from
`l3_exec_lanes.build_cmds`, which is what the log_032 execution campaign
actually ran inside this image. They are **written and unverified by
execution**, and each one's first two seconds are a toolchain probe that
says so if it is wrong.

---

## 7 — how the eight fold, and why no reader branch is added

**Every one of the eight emits the RUST line shape** —
`pid|<type>|<ENCODING>`, `pid|-|RAISE:<kind>`, `pid|-|ABORT:<why>`,
`pid|-|BUILDFAIL` — so all eight read through
`l3_cart_read.read_rust` with **no reader change anywhere**. php's
driver emits that shape rather than ruby's `pid|KIND|payload` for
exactly this reason, and its `-|BUILDFAIL` covers both php 7's
`eval`-returns-false and php 8's `ParseError`, because both are the
language refusing the source rather than raising on a value — and
`read_rust` already folds `-|BUILDFAIL` to **REFUSE**.

The holder exclusions of section 2 are what keeps this true: every
holder carried emits a token `decode_enc` already decodes. (An
occasional *operator result* still lands outside that vocabulary —
c++'s `<=>` gives `ORD:LT`, kotlin's `..` gives a range — exactly as
rust's `..` already did in the run of record, and the fold handles those
the way it always has.)

---

## 8 — products

| file | what changed |
|---|---|
| `Research/kind_fuzz_clustering/l3_cart_values.py` | 47 holder entries for the eight; `INT_RANGE["i16"]`; per-language `INT_RANGE_BY_LANG` tables; `DOUBLE_WHOLE`; `STATIC_TRUTH` and `F32_HOLDERS` extended; `_named_int`, `_f_suffixed`, `_decl_eight` and the `decl()` dispatch |
| `Research/kind_fuzz_clustering/l3_cart_gen.py` | `STATIC8*` config, `MS_PER_PROBE`, `accepted_static`, `static_cells_l1/l2`, `static_l1_output_types`, `STATIC8_SH`, `STATIC8_DRIVER`, `emit_static8`; `PHP_SH`, `PHP_DRIVER`, `PHP_RUNNER`, `php_cells`, `emit_php`; `project8`, `shards_for`, `announce8`, `batch_manifest`, `main_eight`, `--eight` and `--manifest` |
| `Research/kind_fuzz_clustering/lanes/ct_{php,typescript,java,kotlin,cpp,swift,dart,csharp}_l1.sh` | the eight level-1 lanes |
| `Research/kind_fuzz_clustering/lanes/ct_php_l2.sh` | php level 2 |
| `Research/kind_fuzz_clustering/lanes/batch_eight-l1-log062.json`, `batch_eight-l2-php-log062.json` | the manifests |
| `Research/kind_fuzz_clustering/RUN_ALL_LANGUAGES.md` | the runbook, for the owner alone |
| `Research/kind_fuzz_clustering/run_all_languages.sh` | the one-command wrapper: submits phase 1, waits, generates phase 2, submits it, waits. Never touches podman |

**rust, ruby, python and go are untouched.** No emitter, constant, stall
budget, shard count or lane of theirs was edited, and `l3_cart_read.py`,
`l3_per_op_matrices*.py`, `matrices_cart*/`, `matrices_full*/` and both
`operator_dominance_*.json` were not written to at all.

---

## decided, recorded for audit

- **No language of the eight was skipped.** c# is not blocked: `.NET`
  is absent from Airlock's **image** and present in the
  **`sandbox-persist` volume** at `/persist/dotnet` (SDK 10.0.400),
  which both `up.sh` and the quadlet unit mount. The same is true of
  kotlin, swift and dart. Verified from the volume's own contents on the
  host plus the mount lines; **not** verified from inside a running
  container, because podman is not on this session's `PATH`.
- Holders are the layer-2 census's own `rep` entries, unaltered. The
  decimal and bignum holders named in section 2 are **excluded**, each
  with its reason and its one-line reversal, because the settled reader
  cannot decode what the settled runtimes emit for them. dart `BigInt`
  and typescript `bigint` are kept because those two encodings are
  already signed-magnitude `BIGINT:`.
- A WHOLE-form holder that is a binary64 (typescript `number`, dart
  `double (whole number)`) is decided by **double-exactness**, so it
  carries 12 of the 17 whole spellings. That is the settled "exactly
  representable" rule reaching a new holder shape, not a new rule.
- Seven of the eight are `STATIC_TRUTH` (two of six truth points); php
  is route C and holds all six.
- **All eight emit binary floats as BITS**, never printed text. php's
  path is `bin2hex(pack("E", $v))`; the other seven reuse the settled
  `l3_exec.RT_*` runtimes unmodified. The round trip is proved on the
  input side for all eight and end to end for c++, typescript and java.
  swift's and php's output calls are unverified by execution and are
  marked so.
- **Every lane emits the RUST line shape**, so all eight fold through
  `read_rust` with no reader branch added anywhere.
- The compiled driver **repairs before it bisects**: a chunk the
  compiler refuses is retried without the probes the compiler's own
  error lines name (up to 16 rounds), and bisected only when the
  compiler names no line. That is `l3_exec_lanes`' settled instrument,
  and it matters most for swift, whose constant folder refuses
  overflows its type checker accepted.
- `PHP_STALL_S = 2.0` — **ruby's recorded number, carried, not
  measured for php.** php has no unbounded integer, so the `**` stall
  that forced python to 0.5 s cannot arise (an oversized power becomes
  INF at once). The budget is a safety net, not a throughput control.
- Chunk caps are `l3_exec.CHUNK`, imported rather than restated.
- Shard counts are **derived** from each language's own measured
  ms-per-probe against `SHARD_TARGET_S = 2400.0`; none was chosen by
  hand.
- php's string length is `strlen` in both slots of the `STR` token —
  php's own length notion is bytes, and `mbstring` is deliberately not
  called because it is not verified present.
- Lanes are written to `lanes/` and **not** auto-dropped: `write()`'s
  auto-drop targets SandboxDesign's tree, and a drop into the wrong tree
  is invisible and looks exactly like a hung queue (log_061 section 0).
- Submission **joins** the existing batch `pygo-emitters-log061` rather
  than replacing it, so log_061's three queued lanes keep their
  denominator. `--new-batch` is never used.
- php level 2 is generated but held for phase 2, because a startup
  `sweep()` sorts names and `ct_php_l2.sh` would otherwise run before
  three level-1 lanes.
- Did not run any lane. Did not start, stop or restart podman. Did not
  fold anything, choose a scoring, set a threshold, or rule anything
  structural.

## awaiting the owner

1. **Restart Airlock, then run the one command.**
   `bash Airlock/down.sh && bash Airlock/up.sh`,
   then
   `bash PseudoCoupHQ/Research/kind_fuzz_clustering/run_all_languages.sh`.
   Everything else in this log follows from that.
2. **The excluded decimal and bignum holders** (section 2). Restoring
   them means correcting four encodings in the shared `l3_exec.RT_*`
   runtimes — which are the instruments of the log_032 run of record —
   and that is a change to a settled instrument, not a mechanical fix.
