# log 061 — the python and go emitters: built, validated, and BLOCKED at the sandbox

2026-08-22. the owner's staging of the same day: extend the cartesian probe
run from rust + ruby to **two** more languages — python for the
interpreted shape, go for the compiled shape — and prove both before
eight more emitters are written. No other language is emitted here.

**Nothing about the design changes.** Same `X` / `X'` sets, same
canonical form, same probe-index rule, same outcome vocabulary
(`REFUSE`, `RAISE:<kind>`, `ABORT`, `UNREPRESENTABLE`), level 1
`y = op(x0,x1)` over all ordered pairs, level 2
`z = op(op(x0,x1), op(x2,x3))` over `X'`. Two emitters are added, one
on each existing pattern, and nothing else moves.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

---

## 0 — THE BLOCK, first, because it gates section 5 onward

**The running container is not bound to Airlock's agent folders.** Three
lanes were submitted through the validating CLI and sat in
`~/Programming/Airlock/agent/drop/` for 21 minutes with
`~/Programming/Airlock/agent/status/`,
`~/Programming/Airlock/agent/logs/` and
`~/Programming/Airlock/agent/out/` **all still empty** — no
lane has ever run in this tree.

| evidence | reading |
| --- | --- |
| `airlock status` → "queued: ct_go_l1.sh, ct_python_l1.sh, kfz_pygo_ping.sh" and "running: (nothing running)" | the queue is real, the daemon is not consuming it |
| `agent/status/` holds 0 status files | a bound daemon writes one the instant it starts a lane |
| `~/Programming/SandboxDesign/agent/status/` newest entry is `ct_rust_release_l2.sh.status`, 2026-08-22 03:46 | the other tree is idle too, so this is not a lane queued behind a long run |
| `daemon/watcher.py` `main()` calls `sweep()` **once at startup** and is otherwise purely inotify-driven — there is no periodic rescan | a lane dropped while the daemon is bound elsewhere is never picked up, and a restart's startup `sweep()` WILL pick it up |

`airlock doctor` cannot decide it from this session — podman is not on
this session's `PATH`, so every container check is skipped (it says so
itself, severity NOTE). The file evidence is decisive on its own.

**the owner must run, exactly this, and not me:**

```
bash ~/Programming/Airlock/down.sh && bash ~/Programming/Airlock/up.sh
```

The three lanes are already queued, so `up.sh`'s startup `sweep()` runs
them **in the required order** — `sorted(os.listdir(drop))` gives
`ct_go_l1.sh`, `ct_python_l1.sh`, `kfz_pygo_ping.sh`, both level-1 lanes
before anything else.

`airlock doctor` also reports one unrelated FAULT worth fixing while the
sandbox is down: there is no `proxy/allowlist.txt`, so the proxy
default-denies everything. **These lanes need no network** (`GOPROXY=off`,
`GOTOOLCHAIN=local`, no downloads anywhere), so it does not block them.

Everything in sections 1–4 and 6 was done and verified without the
container. Section 5 (the run) and section 7 (the fold) are what the
block costs.

---

## 1 — what was built

| file (all under `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/`) | change |
| --- | --- |
| `l3_cart_values.py` | 15 holder entries added (8 python, 7 go); `INT_RANGE_BY_LANG`, `STATIC_TRUTH`, `NO_SIGNED_ZERO`, `F32_HOLDERS`; `decl()` branches for both; `canon_point` decimal branch widened to python's `Decimal` |
| `l3_cart_gen.py` | `emit_go` + `GO_SH` + `GO_DRIVER`; `emit_python` + `PYTHON_SH` + `PYTHON_DRIVER` + `PYTHON_RUNNER`; `accepted_go` / `go_cells_l1` / `go_l1_output_types` / `go_cells_l2`; `python_cells`; `--pygo` in `main()`; the projection printer |
| `l3_cart_read.py` | `fast_python_canon`, `go_canon`, `read_python`, `shard_lane_files`, `_selfcheck_float_bits`; go and python added to the fold plan; `AIRLOCK_OUT` added as a search directory |
| `lanes/ct_go_l1.sh`, `lanes/ct_python_l1.sh`, `lanes/ct_python_l2_s{0,1,2,3}.sh`, `lanes/kfz_pygo_ping.sh` | the lanes |

**Rust and ruby are untouched.** Proved rather than asserted — the
generator was re-run and its output compared to the lanes of record:

| lane of record | regenerated today | identical |
| --- | --- | --- |
| `lanes/ct_ruby_l1.sh` | — | **YES**, byte for byte |
| `lanes/ct_ruby_l2.sh` | — | **YES**, byte for byte |
| `lanes/ct_rust_release_l1.sh` | — | **YES**, byte for byte |
| `lanes/ct_rust_release_l2.sh` | — | **YES**, byte for byte |
| `lanes/ct_rust_l1.sh` | — | differs, **pre-existing** |
| `lanes/ct_rust_l2.sh` | — | differs, **pre-existing** |

The two rust-debug differences are log_057 Job B's own, not today's:
the payload gained the key `rustc_flags` and the driver gained the
`LANG` tag. Checked key by key — **every payload key present in both is
identical**, cells and holders and operand sets included, and the only
key added is `rustc_flags`.

And the fold was re-run end to end into a scratch directory: **all 85
CSVs come out byte-identical to `matrices_cart_v2/`**, 2,601 rows,
10,042,779 probes, with the four new families named and skipped. The
audit products' hashes are unchanged on disk.

---

## 2 — the holders, and why these and not others

Both holder sets are the **layer-2 census's own** `rep` entries
(`~/Programming/PseudoCoupHQ/Research/data_representation/representations_python.json`
and `…_go.json`). Nothing is invented here.

### python — 8 holders

| form | holder | declaration | L1 points | L2 points |
| --- | --- | --- | --- | --- |
| truth | `bool` | `a = True` / `0` / `""` / `None` | 6 | 6 |
| whole | `int` | `a = 42` | 17 | 10 |
| whole | `decimal.Decimal` | `a = Decimal("42")` | 17 | 10 |
| whole | `fractions.Fraction` | `a = Fraction(42, 1)` | 17 | 10 |
| whole | `ctypes.c_int64` | `a = ctypes.c_int64(42).value` | **16** | 10 |
| fractional | `float` | `a = 0.1` | 16 | 10 |
| fractional | `decimal.Decimal` | `a = Decimal("0.1")` | 16 | 10 |
| fractional | `fractions.Fraction` | `a = Fraction(0.1)` | **15** | **9** |

**`ctypes.c_int64` behaves differently here than the census found, and
the reason is the design, not a fault.** log_031 recorded
`ctypes.c_int64` contradicting python's `int` on `u64max + 42` — but
that contradiction comes from a WRAP AT CONSTRUCTION, and this design
forbids coercion: `2^64-1` is out of `c_int64`'s range, so it is
**ABSENT** from the row and is never constructed. Over the 16 points
`c_int64` does hold, `ctypes.c_int64(x).value` yields a plain unbounded
`int`, so the arithmetic afterwards is python's unbounded arithmetic.
The holder therefore differs from `int` **by window, not by value** —
which is exactly log_056 §4's caution ("width is a holder property, not
a guarantee") arriving in a second language. Recorded as a finding, not
patched away.

`Fraction` drops `-0.0` (no signed zero), the same absence ruby's
`Rational` carries.

### go — 7 holders

| form | holder | declaration | L1 points | L2 points |
| --- | --- | --- | --- | --- |
| truth | `bool` | `var a bool = true;` | **2** | 2 |
| whole | `int32` | `var a int32 = -2147483648;` | 9 | 5 |
| whole | `int64` | `var a int64 = …;` | 16 | 10 |
| whole | `uint64` | `var a uint64 = …;` | 11 | 8 |
| whole | `int` | `var a int = …;` | 16 | 10 |
| fractional | `float64` | `var a float64 = 0.1;` | 16 | 10 |
| fractional | `float32` | `var a float32 = 1.5;` | **7** | 4 |

go's `bool` holds two of the six truth points, exactly as rust's does.
go's `int` is a **distinct holder** from `int64` even though both are
64-bit on this platform — they are distinct types to the compiler, and
`int64 + int` does not compile.

**GO'S NEGATIVE-ZERO HAZARD, found and handled.** Go's untyped constants
have no signed zero at all: the source text `-0.0` is the constant zero,
and `var v float64 = -0.0` stores **+0.0**. The layer-2 census already
spells the point `math.Copysign(0, -1)` (and
`float32(math.Copysign(0, -1))` for the narrow holder), and that
spelling is reused verbatim rather than reinvented. Without it every go
fractional row would have silently carried `+0.0` twice and the signed
zero would have vanished from go's column.

---

## 3 — THE FLOAT PATH, per language, with the round-trip proof

log_057's fault: ruby's lane emitted floats as printed text
(`Float#inspect`) and the reader converted that text as an **exact
decimal**, naming a different real number than the double — 157
disagreements out of 256 against rust's `f64`, all of them ours.

**Both new languages emit BITS. Neither emits a printed float at all.**

| language | path chosen | how it travels | where it is decoded |
| --- | --- | --- | --- |
| **python** | **BITS** | `struct.pack(">d", r).hex()` → `FLOAT:64:<hex>` | `l3_cart_read.fast_python_canon` → `decode_enc` → `canon_output_value` |
| **go** | **BITS** | `math.Float64bits` / `math.Float32bits` → `FLOAT:<w>:<hex>` (RT_GO `_enc`, already in `l3_exec.py`) | `l3_cart_read.go_canon`, which **is** `IR.rust_canon` — go's payload shape is byte-for-byte rust's |
| rust | BITS (unchanged) | `f64::to_bits()` | unchanged |
| ruby | TEXT (unchanged) | `Float#inspect`, converted by the READER through the double | the log_057 fix, unchanged |

python's `Decimal` and `Fraction` keep the **printed** grain on purpose:
a decimal type's printed text already IS its exact value, and a
rational's `n/d` is exact by construction. That is the same split
log_057 settled for ruby, and it is why `Decimal("0.1")` and
`Fraction(0.1)` are two different, both-correct holders.

### the proof, measured

The canon is recomputed **independently** from the double the bits name,
and compared **by string at the canon's own 31-digit precision** — a
double-precision round-trip would be vacuous here for exactly the reason
log_057 proved it vacuous there.

| value | the TEXT path (the log_057 fault) | the BITS path (python, go) | the double, recomputed independently |
| --- | --- | --- | --- |
| `-DBL_MAX` (log_057's own witness) | `[-1, 1.9999999999999997688934766870555, 1023]` | `[-1, 1.9999999999999997779553950749687, 1023]` | `[-1, 1.9999999999999997779553950749687, 1023]` |
| `+min_subnormal` = `5e-324` — **at the double's precision limit** | `[1, 1.0120112665365530917624767335946, -1074]` | `[1, 1.0, -1074]` | `[1, 1.0, -1074]` |
| `1.0 + 1ulp` | `[1, 1.0000000000000002, 0]` | `[1, 1.0000000000000002220446049250313, 0]` | `[1, 1.0000000000000002220446049250313, 0]` |
| `0.1` | `[1, 1.6, -4]` | `[1, 1.6000000000000000888178419700125, -4]` | `[1, 1.6000000000000000888178419700125, -4]` |
| `-0.0` | — | `[-1, 0.0, 0]` | `[-1, 0.0, 0]` |

The `5e-324` row is the sharpest: the text path expands the printed
decimal `5e-324` to a 31-digit mantissa that is **not any double**,
while the bits path answers `1.0` — the min subnormal is exactly
`1.0 × 2^-1074`.

### the instrument is kept, not just the fix

`l3_cart_read._selfcheck_float_bits()` runs **at import**, so every
future fold re-proves it and fails loudly (`AssertionError`, never a
warning). It checks:

- all 16 fractional `X` points, plus `±inf` and both signed zeros;
- **2,000 random doubles** over the full 64-bit space (seeded, so it is
  reproducible), through BOTH `fast_python_canon` and `go_canon`;
- 7 `float32` points through go's narrow holder;
- and that the TEXT reading of `-DBL_MAX` is **still not** the double's
  canon — the fault stated as a live fact rather than a memory.

All pass.

---

## 4 — the operator menus and the accepted profiles

Menus are `ops(lang)` in `l3_cart_gen.py`, which is the grammar's own
positioned anonymous tokens intersected with the candidate binary
vocabulary. `and`/`or` are added to **ruby only** (the design's own
sanity control); python's grammar declares them itself, go declares
neither.

| language | operators | menu |
| --- | --- | --- |
| rust | 19 | `+ - * / % < <= > >= == != & \| ^ << >> && \|\| ..` |
| ruby | 24 | 22 + `and` `or` |
| **python** | **25** | `+ - * / % < <= > >= == != & \| ^ << >> // ** and or in not-in is is-not @` |
| **go** | **19** | `+ - * / % < <= > >= == != & \| ^ << >> && \|\| &^` |

### accepted profiles

| language | route | candidate `(op, lhs, rhs)` | **accepted** | rate |
| --- | --- | --- | --- | --- |
| rust | A2, static | 931 | 128 (L1) | 13.7% |
| **go** | **A2, static** | **931** | **116 (L1)** | **12.5%** |
| ruby | C, execution | — | 2,352 profiles over both levels | — |
| **python** | **C, execution** | — | **1,600 per level, 3,200 over both** | — |

go's accepted set, from the census's own
`acceptance_go_A2.json`, recorded the way the existing
`acceptance_*.json` files are:

| holder pair | ops accepted | which |
| --- | --- | --- |
| `bool × bool` | 4 | `== != && \|\|` |
| `int × int`, `int32 × int32`, `int64 × int64`, `uint64 × uint64` | 17 each | `+ - * / % < <= > >= == != & \| ^ << >> &^` |
| `float32 × float32`, `float64 × float64` | 10 each | `+ - * / < <= > >= == !=` |
| every mixed whole pair (12 of them) | 2 each | `<< >>` only |

**The pruning is real data, not a shortcut.** go refuses every implicit
conversion, so `int64 + int` does not compile and `%` on a float does
not compile; the only cross-holder cells that survive are the shifts,
where go allows a differently-typed shift count. That is the acceptance
grain the census measured, and it is why a statically typed language
contributes ~116 profiles where a dynamically dispatched one contributes
thousands.

---

## 5 — probe counts, projections, lanes and batch

Probe counts are **exact and deterministic** — they are the product of
the accepted cells and the X-set sizes, not an estimate. Wall times are
**projections** from log_052's measured rates (rust 646,659 probes in
162 s, 98% compile → 3,992 probes/s; ruby 9,396,120 probes in 2,347 s →
4,003 probes/s) and are not measurements.

| lane | level | cells / profiles | **probes** | projected wall | status |
| --- | --- | --- | --- | --- | --- |
| `ct_go_l1.sh` | 1 | 116 | **19,184** | 0m 04s | **queued, never ran** |
| `ct_python_l1.sh` | 1 | 1,600 | **360,000** | 1m 29s | **queued, never ran** |
| `ct_go_l2.sh` | 2 | — | — | — | **cannot be emitted yet** |
| `ct_python_l2_s0.sh` | 2 | 400 | 3,182,046 | 44m 12s | written, not submitted |
| `ct_python_l2_s1.sh` | 2 | 400 | 3,227,934 | 44m 23s | written, not submitted |
| `ct_python_l2_s2.sh` | 2 | 400 | 3,227,934 | 44m 23s | written, not submitted |
| `ct_python_l2_s3.sh` | 2 | 400 | 3,214,311 | 44m 20s | written, not submitted |
| **python total** | | **3,200** | **13,212,225** | | |
| **go total (L1 only so far)** | | **116** | **19,184** | | |

Batch: **`pygo-emitters-log061`**, id `batch-20260822T151140Z`, manifest
`~/Programming/Airlock/agent/batch.json`, 3 lanes, weight
379,185. All submitted through the validating CLI
(`python3 ~/Programming/Airlock/airlock submit … --batch
pygo-emitters-log061 --weight <probe count>`) — **zero refusals, zero
warnings**, so every lane carries its `[n/total]` progress line. The
four level-2 shards were `--dry-run` validated identically and are held
back deliberately (see below).

**Why `ct_go_l2.sh` cannot exist yet, and why it is not a formality.**
go's level-2 cells are derived from the **measured TYPE of each level-1
answer** — `op(y, y)` has to typecheck, and `y`'s type is read out of
`ct_go_l1.txt`'s `reflect.TypeOf` field, exactly the discipline
`rust_cells_l2` applies. There is no cast-and-catch and no speculative
compile. So "both level-1 lanes before either level-2 lane" is a
**dependency**, not a preference, and the generator now says so by name
instead of failing obscurely.

**Why the level-2 shards are held back.** No lane has yet run in this
tree at all. Queueing three hours of level-2 work behind a level-1 lane
that has never been observed to succeed would spend the machine on an
unvalidated instrument. They are on disk, validated, and one command
each.

### python's level-2 wall clock is dominated by `**`, and that is MEASURED

python stalls where ruby does not, and the difference is a language
fact: **ruby's `Integer#**` refuses an oversized exponent** (it warns
"in a\*\*b, b may be too big" and answers Infinity), while **python's
just tries**. Sampled at level 2:

| cell | probes sampled | ABORT | rate |
| --- | --- | --- | --- |
| `**` `int` × `int` | 1,406 | 834 | **59.3%** |
| `**` `c_int64` × `c_int64` | 1,398 | 833 | **59.6%** |
| `**` `Fraction` × `Fraction` | 1,106 | 837 | **75.7%** |
| `**` `Fraction` × `int` | 1,125 | 845 | **75.1%** |
| `**` `Decimal` × `Decimal` | 10,000 (the whole cell) | 0 | **0.0%** |
| `**` `int` × `Decimal` | 10,000 (the whole cell) | 0 | **0.0%** |

About **74,300 of python's 12,852,225 level-2 probes (0.58%) stall**.
At ruby's 2.0 s budget those alone would cost **29,720 s of wall clock —
90% of the run — for cells that are excluded from every score anyway**.

**Decision, on the owner's own recorded principle.** log_052 §2:
"a stall is recorded as ABORT and an ABORT is excluded from scoring in
the numerator AND the denominator, so the shorter budget **loses no
measurement — only wall clock**." `PYTHON_STALL_S = 0.5` — python's own
constant; **ruby's 2.0 s is not touched**.

**Control, so the budget is not merely assumed safe:** `Decimal **
Decimal` ran **all 10,000** of its level-2 probes at a **0.10 s** budget
with **zero** aborts. A budget five times shorter than the one chosen
already produces no false stop on 10,000 legitimate probes.

Unsharded, python level 2 projects **177m 20s** — past the daemon's
3,600 s per-lane ceiling and past the ~2 h line — so it is cut across
**4** shards at ~44 min each.

### go's chunk cap is NOT settled — it could not be measured

`GO_CHUNK` is left at rust's 1,500 (13 chunk files for level 1). The
task asked for it to be measured and adjusted; **that measurement needs
a build inside the image and the container never ran**. The ping lane
`lanes/kfz_pygo_ping.sh` exists precisely to take it — it times a
200-function `go build`, checks the negative-zero and constant rules
against the real compiler, and is already queued.

---

## 6 — validation done without the container

Everything below was run and passed. None of it is a substitute for the
Airlock run, and **nothing produced here is folded into any matrices
generation**.

| what | result |
| --- | --- |
| `l3_cart_values.py` self-check and per-holder table | rust and ruby point counts **unchanged** (`i32` 9/17, `i64` 16, `u64` 11, `f32` 7, `bool` 2, ruby `Rational` 15) — the `representable()` refactor preserved behaviour exactly |
| python driver, executed directly on a 6-cell payload | 216 probes, correct ids, `True + True` → `Integer:2`, `True + ""` → `RAISE|TypeError` |
| python driver on float / Decimal / Fraction / c_int64 cells | floats emerge as `FLOAT:64:<hex>`; `-max_finite + -max_finite` → `fff0000000000000` (−inf); `-2^63 × +0.0` → `FLOAT:64:8000000000000000`, **the signed zero survives** |
| python **runner**, 5 workers, 1,318 probes including the `**` cell | 1,194 answers, 40 raises, **84 ABORTs, 84 restarts** — the restart-past-a-stall discipline fires and costs one probe each; `[n/total]` progress line printed; per-worker part files written |
| go source generation, inspected | header imports all used by RT_GO; `defer _guard(id)`; `var a int64 = -9223372036854775808;`; `var a float32 = float32(math.Copysign(0, -1));`; `main()` reads a **start index** from `os.Args` |
| `fast_python_canon` / `go_canon` on the full token vocabulary | `INT:64:8000000000000029` → `[-1, 1.9999999999999999911095421856189, 62]`; `Integer:42` → `[1, 1.3125, 5]` (matches SUPPORT_ontology's own example); `String:` → `t\|\|0\|0\|0` |
| `_selfcheck_float_bits()` | 2,019 doubles + 7 float32 + the log_057 witness, both languages — **PASS** |
| operator filenames | 25 python + 19 go, no dots, no collisions — `l3_operator_dominance.read_profiles`'s `name.split(".")` stays a clean 3-way split |
| full fold re-run into a scratch directory | 85 CSVs, 2,601 rows, 10,042,779 probes, **all 85 byte-identical to `matrices_cart_v2/`**; go and python named and skipped; `matrices_cart_v2/` and `matrices_full_v2/` hashes unchanged |

`l3_cart_full.py` needs no change at all — it is driven entirely by
`matrices_cart/index.json` and names no language.

---

## 7 — the fold and the dominance re-run: BASELINE ONLY

The corrected generation is `matrices_cart_v2/` → `matrices_full_v2/`
(log_057). **Neither was written to.** The superseded `matrices_cart/`
and `matrices_full/` were not touched either.

The baseline was re-derived read-only from `matrices_full_v2/`, so the
"before" numbers below are measured today, not quoted:

| | value |
| --- | --- |
| profiles | 2,601 |
| operators (`lang.op` nodes) | 43 |
| **containment pairs, BEFORE** | **24** |
| mode families (cross-language) | 76 |
| profiles by language | ruby 2,352, rust 249 |

`+` in `whole|whole` at L1 — log_056 §4's table, exactly as it still
stands:

| part | languages | members | value cells | example holders |
| --- | --- | --- | --- | --- |
| 1 | ruby, rust | 8 | 289/289 | `BigDecimal BigDecimal`, `BigDecimal Integer`, `Integer BigDecimal` |
| 2 | ruby | 1 | 289/289 | `Rational BigDecimal` |
| 3 | ruby | 1 | 289/289 | `BigDecimal Rational` |
| 4 | rust | 1 | 67/289 | `i32 i32` |
| 5 | rust | 1 | 221/289 | `i64 i64` |
| 6 | rust | 1 | 102/289 | `u64 u64` |

**Containment pairs AFTER: not measured.** It needs the lane output.

**Whether python's unbounded `int` lands in ruby's `Integer` part: not
measured.** It is a cell-by-cell equality question over the full grid
and only the run answers it.

**Whether go produces the WRAP part log_056 §3 said had no instance:
not measured, but it is now the one thing most likely to.** go's
integer arithmetic **wraps by definition** — there is no debug/release
split and no overflow check to switch off — so `int64` and `uint64` are
expected to answer `INT:64:8000000000000029` where rust-debug answers
`RAISE:panic` and ruby answers the unbounded value. That is a
prediction, and it is stated here **as a prediction** so the run either
confirms or refutes it.

After the fold the graph will carry **87** `lang.op` nodes (rust 19,
ruby 24, python 25, go 19) against 43 today.

---

## decided, recorded for audit

- python's holders and go's holders are the **layer-2 census's own**
  `rep` entries, unaltered; no holder was invented, widened or dropped.
  go's `int` is kept DISTINCT from `int64` because the compiler keeps
  them distinct.
- **Both new languages emit binary floats as BITS**, never as printed
  text. python: `struct.pack(">d", r).hex()`. go: `math.Float64bits` /
  `math.Float32bits`, already present in `l3_exec.RT_GO`. python's
  `Decimal` and `Fraction` keep the printed/exact grain, on the same
  split log_057 settled for ruby.
- `l3_cart_read._selfcheck_float_bits()` runs at import and fails loudly
  (`AssertionError`) — the log_057 instrument, kept pointed at the new
  languages.
- go's negative zero is spelled `math.Copysign(0, -1)` (and
  `float32(math.Copysign(0, -1))`), reusing the census's own spelling,
  because go's untyped constant `-0.0` is `+0.0`.
- `PYTHON_STALL_S = 0.5`, python's own constant, from the measured
  `**` stall table in §5 and on log_052 §2's recorded principle.
  **Ruby's 2.0 s is unchanged.** The control run (10,000 legitimate
  probes at a 0.10 s budget, zero false aborts) is recorded beside it.
- `PYTHON_L2_SHARDS = 4`: unsharded python level 2 projects 177m 20s,
  past both the 3,600 s daemon ceiling and the ~2 h line.
- `PYTHON_RUNNER` is a SEPARATE constant from `RUBY_RUNNER` rather than
  a parameterisation of it, so the generated bytes of
  `ct_ruby_l{1,2}.sh` — the scripts of the run of record — cannot move.
  Verified: they do not.
- `shard_lane_files` is separate from `lane_files` on purpose:
  `raw/` still holds `ct_ruby_l2_s*.txt` from an abandoned sharding
  attempt whose cell partition is NOT the run of record's, and widening
  the ruby glob would silently pull those back in.
- `AIRLOCK_OUT` was ADDED as a search directory in the generator and the
  reader. `LANE_OUT` still points at `SandboxDesign/agent/out` and is
  unchanged — repointing this line wholesale is the owner's call (log_060), so
  nothing moved.
- `--pygo` forces `drop=False`: these lanes go to Airlock through
  `airlock submit`, never through `write()`'s auto-drop, which targets
  SandboxDesign's tree. A drop into the wrong tree is invisible and
  looks exactly like a hung queue.
- The generator now REFUSES to emit `ct_go_l2.sh` without
  `ct_go_l1.txt`, and says why, because go's level-2 cells are derived
  from measured level-1 answer types.
- The four python level-2 shards were validated (`--dry-run`, no
  refusals, no warnings) and **deliberately not submitted** while no
  lane has been observed to run.
- Did not start, stop or restart podman. Did not touch
  `matrices_cart/`, `matrices_full/`, `matrices_cart_v2/`,
  `matrices_full_v2/`, `operator_dominance_v1.json` or
  `operator_dominance_v2.json`. Did not emit any language other than
  python and go. Did not choose which scoring is THE weight, set a
  threshold, or rule anything structural.

## awaiting the owner

1. **Restart Airlock so the queued lanes run** — `bash
   ~/Programming/Airlock/down.sh && bash ~/Programming/Airlock/up.sh`.
   The three lanes are queued in the right order and `up.sh`'s startup
   `sweep()` will take them. Everything in §5's "not measured" and all
   of §7's "AFTER" numbers follow from that one command. (While it is
   down: `cp ~/Programming/Airlock/proxy/allowlist.txt.example
   ~/Programming/Airlock/proxy/allowlist.txt` clears `doctor`'s one
   FAULT; these lanes do not need it.)
2. **python's stall budget, 0.5 s against ruby's 2.0 s.** Decided on
   the owner's own recorded principle and measured, but the ruby budget is a
   recorded ruling and this is a second number beside it — say if it
   should instead be one shared constant.

---

## 2026-08-23 addendum — LEVEL 2, generated and RUN to completion

The block in section 0 is gone: both level-1 lanes ran (`ct_python_l1.sh`
exit 0 in 171.5 s, `ct_go_l1.sh` exit 0 in 6.9 s — the ping lane
`kfz_pygo_ping.sh` also ran, exit 0, 3.3 s). This addendum covers what
followed: emitting, projecting, sharding, submitting and watching level 2
for the last two of the twelve languages to completion. Ten of twelve
have now run level 2; python and go are the ones this addendum closes
out.

### the go driver correction, checked against log_063 before touching anything

log_063 (today, the cpp throughput fix) reads as if it might also cover
go — "go uses that compiled driver" was the framing this session started
from. Reading `l3_cart_gen.py` and log_063 directly says otherwise: the
watchdog (`STATIC8_STARTUP_S` / `STATIC8_STALL_S`, the queue+thread
`run_binary`) was added ONLY to `STATIC8_DRIVER`, the template shared by
cpp/java/kotlin/swift/dart/csharp/typescript. `GO_DRIVER` is a SEPARATE
template (`l3_cart_gen.py` line 771) with its OWN `run_binary` (line
867), and log_063 section 1 says plainly: "Rust and go's `run_binary`
have the identical unconditional-block shape and are not touched here:
their operand set is plain machine arithmetic that panics or traps
rather than looping, so nothing in the run of record has ever produced a
hang there." Confirmed by reading the generated `ct_go_l2.sh` after
emission: no `STARTUP`, `STALL`, `queue.Queue` or `q.get(timeout=...)`
anywhere in it — the START-INDEX restart discipline is present (an
uncatchable stop still costs one probe, never a chunk) but there is no
execution-side watchdog, because log_063 deliberately did not put one
there. **Nothing was changed in `GO_DRIVER`** — the correct action was to
verify the settled decision held, not to invent a watchdog log_063 chose
not to add. Recorded here as a correction to the framing this session
opened with, not as a fault in log_063 itself.

### the projection, redone against TODAY's measured python rate, not ruby's

`l3_cart_gen.py`'s own `project()` sizes the "interpreted" rate from
ruby's cartesian run of record (9,396,120 probes / 2,347.3 s = 4,003/s)
and applies it to python too. That was the only number available when
`PYTHON_L2_SHARDS = 4` was set. Today python's own level-1 lane gives a
real, python-specific number: 360,000 probes in 171.5 s = **2,100
probes/s** — roughly half ruby's rate — and python L1's own worker log
shows why: 740 s of the run's 855.5 s of aggregate worker-time was spent
inside the 0.5 s stall budget (1,480 restarts), so the stall bill is
already a measured, non-trivial share of python's throughput at level 1,
not a level-2-only concern.

Redone with python's own rate plus the level-2 stall bill log_061 §5
already measured (`PYTHON_L2_STALL_PROBES = 74,300`,
`PYTHON_STALL_S = 0.5`, `PYTHON_WORKERS = 5`):

```
12,852,225 / 2,100 + 74,300 * 0.5 / 5 = 6,120.1 + 7,430.0 = 13,550.1 s
                                        = 225.8 min = 3.76 h
```

At 4 shards that is ~56.5 min each — past this run's ~30 min restart-
granularity target. `PYTHON_L2_SHARDS` was changed **4 → 8** in
`l3_cart_gen.py` (13,550.1 / 8 ≈ 1,694 s ≈ 28.2 min projected per shard).
This is a sharding/administrative change only: cells are still assigned
to shards round-robin by cell index (`n % nshard`), so it touches nothing
in the probe design, X sets, canonical form, probe-index rule or outcome
vocabulary. **Verified directly**: the union of the 1,600 cells across
the new 8 shards was decoded from each generated lane's embedded
`table.json` and compared byte-for-byte (as a set) against the union of
the old 4-shard generation's cells — identical, 1,600 cells both ways.

go's level-2 cells are now derivable (level-1 answer types exist):
**92 cells, 500,573 probes** — small, `MS_PER_PROBE["go"]` (0.29 ms,
log_032) or the actual measured go L1 rate (19,184 probes / 6.9 s =
2,780/s) both project under 3 minutes, so go is **not sharded**, matching
`emit_go`'s own signature (no shard parameter) and the task's own
"shard only if the projection says so."

### submission

All 9 lanes joined the LIVE manifest under the existing label — no new
label created:

```
python3 ~/Programming/Airlock/airlock submit <lane.sh> \
    --batch pygo-emitters-log061 --weight <probe count>
```

| lane | cells | probes (weight) | dry-run | submit |
| --- | --- | --- | --- | --- |
| `ct_go_l2.sh` | 92 | 500,573 | clean | accepted |
| `ct_python_l2_s0.sh` | 200 | 1,568,079 | clean | accepted |
| `ct_python_l2_s1.sh` | 200 | 1,613,967 | clean | accepted |
| `ct_python_l2_s2.sh` | 200 | 1,613,967 | clean | accepted |
| `ct_python_l2_s3.sh` | 200 | 1,613,967 | clean | accepted |
| `ct_python_l2_s4.sh` | 200 | 1,613,967 | clean | accepted |
| `ct_python_l2_s5.sh` | 200 | 1,613,967 | clean | accepted |
| `ct_python_l2_s6.sh` | 200 | 1,613,967 | clean | accepted |
| `ct_python_l2_s7.sh` | 200 | 1,600,344 | clean | accepted |

Batch `pygo-emitters-log061` (id `batch-20260822T214906Z`) grew from 21
lanes/weight 379,185 to **30 lanes / weight 22,393,456** — the 8
eight-language STATIC8 lanes and their level-2 shards already in the
manifest were untouched, only extended.

### outcomes — every lane ran to completion, exit 0, no ABORTs, no BUILDFAILs

All 9 lanes ran serially (the daemon runs one script at a time) and
finished before this addendum was written:

| lane | probes | answers | raises | aborts (stall) | wall | exit |
| --- | --- | --- | --- | --- | --- | --- |
| `ct_go_l2.sh` | 500,573 | 412,761 | 87,812 | 0 | 121.7 s (2.0 min) | 0 |
| `ct_python_l2_s0.sh` | 1,568,079 | 852,951 | 706,214 | 8,914 | 976.4 s (16.3 min) | 0 |
| `ct_python_l2_s1.sh` | 1,613,967 | 855,399 | 758,072 | 496 | 67.4 s (1.1 min) | 0 |
| `ct_python_l2_s2.sh` | 1,613,967 | 810,817 | 779,398 | 23,752 | 2,828.8 s (47.1 min) | 0 |
| `ct_python_l2_s3.sh` | 1,613,967 | 899,990 | 713,977 | 0 | 12.8 s (0.2 min) | 0 |
| `ct_python_l2_s4.sh` | 1,613,967 | 985,624 | 602,740 | 25,603 | 3,049.7 s (50.8 min) | 0 |
| `ct_python_l2_s5.sh` | 1,613,967 | 931,945 | 658,289 | 23,733 | 2,645.5 s (44.1 min) | 0 |
| `ct_python_l2_s6.sh` | 1,613,967 | 863,685 | 750,279 | 3 | 33.3 s (0.6 min) | 0 |
| `ct_python_l2_s7.sh` | 1,600,344 | 871,506 | 728,822 | 16 | 298.6 s (5.0 min) | 0 |
| **python L2 total** | **12,852,225** | **7,071,917** | **5,697,791** | **82,517** | **9,914.0 s (2.75 h, serial)** | all 0 |

Cross-check: `answers + raises + aborts` equals `probes` exactly for
every python shard and for go (e.g. s2: 810,817 + 779,398 + 23,752 =
1,613,967). go: 412,761 + 87,812 = 500,573, 0 aborts — no stall, no
BUILDFAIL, consistent with go's arithmetic panicking/trapping rather
than hanging (§ above), so the absent watchdog cost nothing here.

**Actual python abort rate: 82,517 / 12,852,225 = 0.642%**, against the
0.58% (74,300) sampled and projected in log_061 §5 — close, on the same
order, the small gap being sampling variance rather than a modelling
error.

**The per-shard wall-clock variance the ~28 min/shard projection did not
capture, recorded plainly:** actual shard walls ranged from 12.8 s
(`s3`, a lucky cell assignment with zero `**`-type stalls) to 3,049.7 s /
50.8 min (`s4`). The round-robin cell assignment does not evenly spread
the handful of heavily-stalling cells across shards in practice — three
shards (`s2`, `s4`, `s5`) each ran 44–51 minutes, well past the ~28 min
projection and past this run's own ~30 min target, because they drew a
larger share of the `**`-stall cells than the mean. **None came close to
the daemon's 3,600 s ceiling** (worst case 3,049.7 s, 85% of the
ceiling) — the 8-way sharding decision held under real variance where
the original 4-way sharding (which would have concentrated roughly twice
the stall load per shard, ~56.5 min projected mean with the same
variance) would plausibly not have. This was watched live rather than
assumed: `s2` and `s4` were tracked through `airlock status` while their
`[n/total]` progress line showed sustained near-zero throughput
(as low as 250–600 probes/s against a ~19,000 probes/s burst rate on
cheap cells) for several-hundred-second stretches, consistent with a
worker grinding through a contiguous run of `**` probes each costing the
full 0.5 s stall budget before restart.

Every lane printed its `[n/total]` progress line throughout, per the
standing requirement.

### products

`~/Programming/Airlock/agent/out/ct_go_l2.txt` and
`~/Programming/Airlock/agent/out/ct_python_l2_s{0..7}.txt` now exist
alongside the level-1 outputs and the other eight languages' level-2
products. **Nothing here was folded into any matrices generation, no
dominance script was run, no containment-pairs or WRAP-family question
from log_061 §7 was answered** — that fold is the owner's to run.

## decided, recorded for audit (2026-08-23 addendum)

- Verified, did not invent: `GO_DRIVER`'s `run_binary` carries no
  watchdog, matching log_063's own explicit decision not to touch
  rust/go's driver. No code change made to `GO_DRIVER`.
- `PYTHON_L2_SHARDS` changed from 4 to 8 in `l3_cart_gen.py`, justified
  by python's own measured L1 rate (2,100 probes/s, not ruby's 4,003)
  plus the already-measured level-2 stall bill. Verified the cell SET is
  unchanged (1,600 cells, identical before and after, checked by
  decoding both generations' `table.json`s) — only shard granularity
  moved.
- go level 2 emitted unsharded (92 cells, 500,573 probes) — the
  projection at go's own measured rate is under 3 minutes, well inside
  every ceiling, matching `emit_go`'s no-shard signature.
- All 9 lanes validated `--dry-run` clean, then submitted under the
  existing `pygo-emitters-log061` label / `batch-20260822T214906Z` id —
  no new batch created. Batch grew from 21 lanes / weight 379,185 to 30
  lanes / weight 22,393,456.
- All 9 lanes ran to completion: **exit 0, zero ABORTs at the
  script/daemon level, zero BUILDFAILs, zero missing lines.** python's
  per-probe ABORT (the stall-and-restart outcome, excluded from scoring
  by design) totalled 82,517 of 12,852,225 probes (0.642%), close to the
  0.58% sampled projection. go: zero stalls, zero raises beyond the
  87,812 catchable panics/traps recorded as `RAISE:<kind>`.
- Did not fold anything into `matrices_cart_v2/` / `matrices_full_v2/`,
  did not run the dominance script, did not touch any other language's
  lane or product. Did not start, stop or restart podman — the running
  container's watcher picked up all 9 lanes by inotify, as designed.

## awaiting the owner

1. **The fold.** Level 2 is now complete for all twelve languages (ten
   already folded per log_062/063, python and go's level-2 products now
   sitting in `agent/out` unfolded). Folding python and go into
   `matrices_cart_v2/` → `matrices_full_v2/` and re-running the
   containment/WRAP-family questions log_061 §7 left open is the owner's next
   step, not done here.
2. **The per-shard wall-clock variance** (12.8 s to 50.8 min across 8
   python shards, all safely under the 3,600 s ceiling but well past the
   ~28 min mean projection) is worth knowing about if this sharding
   scheme is reused for a future language with a similar stall-prone
   operator — the round-robin-by-cell-index split does not guarantee an
   even stall load per shard.
