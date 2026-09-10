# log 025 — what one layer-3 probe costs, measured, and what brute force would cost

Date: 2026-08-18. Node:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`
(`timing_build.py`, `timing_read.py`, `lanes/tm_*.sh`, `raw/tm_*.txt`,
`timing_results.json`).

This log answers one question and no others: **before ruling on the full
value matrix, what does a probe actually cost?** It measures, it does not
propose. Every number below carries its level — **measured**, **derived**,
or **estimate**.

---

## §1 — walkthrough, in plain words

Three cold words first, because each has been away long enough that its
earlier definition does not survive the gap.

- **Layer 1** is the DATA: fixed content with no language attached —
  nothing, truth, whole number, fractional number, text, sequence, keyed
  grouping, nesting, identity marks.
- **Layer 2** is the REPRESENTATIONS: per language, the ways a running
  program can HOLD that content. One (form, representation) pair is a CELL,
  and a cell has several VALUES.
- **Layer 3**, which this log serves, is the OPERATIONS: what the COMPILER
  can do to a loaded cell — operators, subscripting, comparison, unary
  forms. Never builtins, never standard-library calls.

What was done. Twelve lane scripts, one per language, each generating a
random sample of **100 realistic probes** — one operation applied to literal
operands spelled in that language, drawn from the layer-1 forms, half of the
sample predicted-accepting and half predicted-refusing. Each probe got its
own file, its own directory and its own fresh process. Each was timed twice
over: the compile step, where the language has one, and the run step,
separately, in wall clock. No batching, no daemon, no warm process. That is
deliberately the worst case, which is what the owner asked for.

The headline numbers, all **measured**.

- **One probe costs between 12 ms and 2.4 s**, depending entirely on the
  language. PHP is the cheapest at **11.8 ms**; kotlin is the dearest at
  **2,449 ms**. That is a **208-fold spread** across the twelve, and it is
  almost entirely the compile step: kotlin's compiler alone is 2,397 ms of
  its 2,449, because every probe pays a cold JVM start plus a cold kotlinc.
- **Refusing is cheaper than accepting in every compiled language**, because
  a probe refused at compile never runs. Go: 52 ms refusing against 121 ms
  accepting. Swift: 161 against 249. That matters, because under enumeration
  refusals are the majority.
- **Python is the one language where refusing costs MORE** — 25.6 ms against
  13.1 ms — because a python refusal is a raise at run time and the
  interpreter pays to build and print it. Ruby and PHP are flat, refusing and
  accepting within a millisecond of each other.

Then the counting. Python's full count is **derived**, not guessed: the real
generator was re-run with the pair rule replaced by full enumeration of
ordered pairs and the tier-B representative replaced by the full value
matrix, and the probes were counted.

- Python as run in log 024: **20,024 probes** from 200 chosen operand pairs.
- Python under full enumeration of its 117 x 117 = **13,689 ordered pairs**,
  tier B unchanged: **654,411 probes** (derived).
- Python under full enumeration AND the full value matrix in tier B:
  **660,102 probes** (derived). The full value matrix costs only **5,691
  extra probes, under one percent**. Enumerating the pairs is the whole of
  the expense; the value matrix is a rounding error on top of it.

Scaling the other eleven by their phase-0 probe space and the square of
their layer-2 value count gives **about 5.79 million probes across the
twelve** (estimate).

- **Worst case, one probe per file, serial: about 435 hours — 18.1 days** of
  sandbox time (estimate over measured means).
- **Batched at 100 probes per file: about 6.2 hours** (estimate over a
  measured batch). A single 100-probe batch was compiled and run once per
  language, and it amortises the fixed cost by **33x to 103x**.
- The distribution is brutally uneven. **Kotlin alone is 206 of the 435
  hours — 47 percent of the entire bill** for 5 percent of the probes.

So the plain answer to the question the owner asked. The full value matrix is
nearly free — under one percent on top of full pair enumeration. Full pair
enumeration itself is what costs, and even that is affordable everywhere
except kotlin, and affordable in kotlin too the moment probes share a file.

---

## §2 — the measurement method

- **The probe shape.** One operation on literal operands, which is the shape
  layer 3 actually uses.
  - Operations sampled: the binary operators `+`, `-`, `*`, the comparison
    `<`, the equality `==`, the subscript `[0]`, the unary minus, and the
    unary negation.
  - Operands: **17 atoms per language** — the layer-1 forms in that
    language's own spellings, reusing the `spell` tables from
    `representations_<language>.json` where they applied. Nothing, both truth
    values, three whole numbers, three fractional numbers, three texts, two
    sequences, two keyed groupings.
  - Both operands are spelled OPAQUELY — bound to a name first, then the
    operator sees the name. That is the majority mode in the python
    precedent (13,068 of 20,024) and it denies the compiler the folding
    shortcut, so it is the honest cost.
- **The sample.** N = 100 per language, drawn at random from the full
  operation x operand space with a fixed per-language seed, balanced 50
  predicted-accepting and 50 predicted-refusing.
  - The prediction only balances the draw. **What the report classifies on is
    the measured exit code**: a probe is ACCEPTED when both steps exited
    clean and REFUSED otherwise. Measured accept counts ranged from 26
    (rust) to 72 (php) — the static languages refuse more of the same sample
    than the dynamic ones do, which is itself a layer-3 fact.
- **The timing.** Wall clock in nanoseconds around each step, taken inside
  the sandbox by the lane itself. Compile and run recorded separately. Fresh
  process per probe, fresh directory per probe, one probe per file.
  - **N = 100 was reached for all twelve languages.** A 400-second per-lane
    cap was built in and none of the twelve hit it; kotlin came closest at
    251 seconds.
  - Compiled languages measure a compile step and a run step. Python, ruby,
    php and dart have no separate compile invocation in this harness and
    measure a run step only — their compile column is a structural zero, not
    a measurement of zero.
- **An instrument defect found and removed.** The first pass reported every
  step at a suspicious 100-millisecond multiple. A diagnostic lane
  (`raw/tm_diag.txt`, measured) established the cause: the container's
  `timeout` is uutils coreutils 0.8.0, which polls at 100 ms and so rounds
  every step it wraps up into a 100 ms bucket — a bare `/bin/true` measured
  106 ms under it and 3 ms without it. The second pass, which is what this
  log reports, does not wrap a timed step in `timeout`. The residual
  instrument cost is the two `date` forks, which each lane measures for
  itself (3.2 to 4.1 ms) and which `timing_read.py` subtracts from every
  step.
- **The batch measurement.** One extra file per language holding **100
  accepting probes**, each in its own scope, compiled once and run once.
  - It may hold only probes that genuinely compile and run, since one
    refusal refuses the whole file — which is precisely why a batched
    enumeration needs the bisect the CORE records as unbuilt. The members
    were selected by pass 1's measured exit codes.
  - All twelve batches compiled and ran clean.

---

## §3 — the per-language table

Every timing column is **measured** and is a mean over N = 100 with its
sample standard deviation. Means are per probe over the WHOLE sample,
including probes that never reached the run step, since that is the true
cost per probe attempted. The count column is **derived** for python and
**estimate** for the other eleven.

| language | N | compile mean±sd (ms) | run mean±sd (ms) | accept vs refuse (ms) | est. full count | worst-case total | batched total |
|---|---|---|---|---|---|---|---|
| php | 100 | — (no compile step) | 11.8 ± 1.7 | 11.8 vs 11.6 | 541,018 | 1.8 h | 0.02 h |
| python | 100 | — (no compile step) | 17.1 ± 6.0 | 13.1 vs 25.6 | 660,102 | 3.1 h | 0.03 h |
| ruby | 100 | — (no compile step) | 38.4 ± 6.1 | 38.3 vs 38.5 | 757,433 | 8.1 h | 0.08 h |
| rust | 100 | 35.6 ± 11.6 | 0.4 ± 0.7 | 55.5 vs 29.1 | 332,379 | 3.3 h | 0.10 h |
| go | 100 | 71.6 ± 31.7 | 0.6 ± 1.1 | 121.3 vs 52.2 | 224,188 | 4.5 h | 0.09 h |
| dart | 100 | — (no compile step) | 144.6 ± 6.1 | 143.4 vs 146.6 | 506,078 | 20.3 h | 0.20 h |
| cpp | 100 | 173.0 ± 21.4 | 1.0 ± 0.9 | 188.6 vs 150.2 | 747,370 | 36.1 h | 0.54 h |
| swift | 100 | 191.7 ± 41.8 | 1.1 ± 1.5 | 249.4 vs 160.9 | 86,413 | 4.6 h | 0.09 h |
| typescript | 100 | 265.8 ± 9.7 | 34.4 ± 34.0 | 333.5 vs 265.5 | 580,822 | 48.4 h | 0.55 h |
| java | 100 | 298.5 ± 22.4 | 10.9 ± 11.0 | 321.1 vs 297.3 | 443,921 | 38.2 h | 0.57 h |
| csharp | 100 | 348.0 ± 21.9 | 12.0 ± 11.3 | 384.0 vs 332.0 | 607,248 | 60.7 h | 0.81 h |
| kotlin | 100 | 2396.8 ± 182.0 | 52.2 ± 43.0 | 2621.2 vs 2190.7 | 302,796 | 206.0 h | 3.13 h |
| **all twelve** | **1,200** | — | — | — | **5,789,768** | **435.2 h (18.1 d)** | **6.2 h** |

Supporting counts, so the estimates can be argued with:

| language | layer-2 values that load | layer-2 holders | phase-0 R2 probes | measured accept / refuse in sample | batch per-probe (ms) | amortisation |
|---|---|---|---|---|---|---|
| python | 117 | 27 | 686 | 68 / 32 | 0.18 | 97x |
| ruby | 112 | 25 | 859 | 64 / 36 | 0.37 | 103x |
| php | 97 | 22 | 818 | 72 / 28 | 0.12 | 101x |
| typescript | 101 | 26 | 810 | 51 / 49 | 3.38 | 89x |
| dart | 110 | 28 | 595 | 61 / 39 | 1.43 | 101x |
| go | 84 | 23 | 452 | 29 / 71 | 1.39 | 52x |
| java | 131 | 36 | 368 | 51 / 49 | 4.63 | 67x |
| csharp | 116 | 33 | 642 | 54 / 46 | 4.78 | 75x |
| rust | 91 | 25 | 571 | 26 / 74 | 1.09 | 33x |
| cpp | 104 | 27 | 983 | 62 / 38 | 2.59 | 67x |
| swift | 98 | 27 | 128 | 36 / 64 | 3.57 | 54x |
| kotlin | 110 | 29 | 356 | 60 / 40 | 37.16 | 66x |

How the counts were obtained.

- **Python, DERIVED.** `probe_generate.py` was re-run with two rules
  replaced and the output counted.
  - Rule 2 (200 operand pairs chosen by four rules) replaced by full
    enumeration of the 117 x 117 = 13,689 ordered pairs: **654,411 probes**.
  - Decision 11 (tier B takes one representative value per cell) additionally
    replaced by the full value matrix: **660,102 probes**.
  - The delta between them is **5,691 probes, 0.86 percent**.
- **The other eleven, ESTIMATE.** Python's 660,102 scaled by two factors:
  the ratio of phase-0 R2 probe counts, which carries the kinds and the
  operator menus; and the SQUARE of the ratio of layer-2 loading values,
  which carries the operand pairs. The square is the right power because the
  pair families are over 97 percent of the derived python count.

---

## §4 — what the numbers say about brute force

- **The full value matrix is not the expensive decision. It is nearly
  free.** Adding it to full pair enumeration costs python 0.86 percent
  (derived). If the owner is weighing whether to brute-force the values as well as
  the pairs, the cost side of that trade is under one percent and should not
  decide it. The reason is structural and will hold for the other eleven:
  tier B is a per-slot placement probe, so it grows LINEARLY in values, while
  the tier-A pair families already grow quadratically and already dominate.
- **Eight of the twelve are trivially affordable even at the worst case.**
  php 1.8 h, python 3.1 h, rust 3.3 h, go 4.5 h, swift 4.6 h, ruby 8.1 h,
  dart 20.3 h, cpp 36.1 h. Every one of those is an overnight run with one
  probe per file, no batching and no bisect (estimate over measured means).
  Four of them are under five hours.
- **The expensive tail is four languages, and one of them is most of it.**
  java 38 h, typescript 48 h, csharp 61 h, kotlin 206 h. Together they are
  **353 of the 435 hours, 81 percent**. Kotlin alone is **206 hours, 47
  percent of the whole bill**, and it earns that with 5 percent of the
  probes. The cause is measured and specific: 2,397 ms of cold compiler
  start per probe, against cpp's 173 and rust's 36.
- **Batching settles the tail, and the measurement is in hand.** Amortisation
  measured at 33x to 103x. The whole twelve-language brute force drops from
  18.1 days to **6.2 hours**, and kotlin from 206 hours to **3.1 hours** — no
  longer the worst offender in absolute terms and no longer decisive.
  - The catch is stated honestly: a batch may hold only probes that compile.
    The batch measured here was built from pass 1's measured accepts for
    exactly that reason. Batching the real run therefore requires the bisect
    the CORE records as unbuilt, and the bisect's cost is NOT in these
    numbers.
- **The verdict on brute force.** Full enumeration of ordered operand pairs
  plus the full value matrix is **within reason**. At the absolute worst
  case — one probe per file, fresh process, no batching, no daemon, nothing
  clever — it is 18 days of sandbox time for all twelve, and eight of the
  twelve finish overnight on their own. The full value matrix adds under one
  percent to that and should be taken. The only number that argues against
  the worst-case route is kotlin's 206 hours, and it is a single language
  with a single measured cause; it can be paid, deferred, or batched, and
  batching it needs the bisect, which is the same engineering the CORE
  already records as owed for the ten compiled languages. Nothing here says
  do not brute-force. What it says is that the brute force is bounded, that
  the bound is days rather than months, and that the value matrix is not the
  part worth arguing about.

---

## §5 — caveats

- **Sample bias, and it is real.** The 100 probes per language are one
  operation over 17 atoms; the actual enumeration is 39-plus operator menu
  tokens over 117 values, and it includes tier-B placement probes with
  hand-written and generated wrappers that this sample does not contain at
  all. Wrapped probes are longer source and will compile a little slower.
  The measured means are therefore a floor on the compile side, though the
  fixed cost — process start, compiler start — dominates so heavily in every
  compiled language that the source-length term should stay small.
- **The 17 atoms are not the 117 values.** Edge values were deliberately not
  stressed: the whole-number atoms are 0, 42 and 1,000,000, not the width
  boundaries. Layer 3's real run WILL include values that cost more to
  evaluate, and log 024 measured 32 probes that exhausted a two-second budget
  outright. Budget exhaustions are not in these means and would be added on
  top.
- **Sandbox variance is not characterised.** Each language was measured once,
  in one container, on one host, with warm filesystem caches after the first
  few probes. The standard deviations reported are within-lane, not
  between-run. Go's compile sd of 31.7 ms on a 71.6 ms mean is the widest
  relative spread and is the one place where a repeat run is most likely to
  disagree.
- **Run means include structural zeros.** A probe refused at compile has no
  run step, and its run time enters the mean as zero. That is correct for
  cost-per-probe-attempted, which is what the totals need, but it means the
  run column must not be read as "what a run costs when it happens" —
  especially for rust and go, where three quarters of the sample never ran.
- **The estimates are scalings, not counts.** Only python's count is derived
  from its generator. The other eleven have no layer-3 generator yet, so
  their probe counts are a two-factor scaling and could be wrong by a
  substantial factor in either direction — most plausibly too LOW, since
  several languages have more holders than python and the phase-0 R2 count
  predates layer 2 entirely. Swift's 86,413 is the estimate to trust least:
  it rests on a phase-0 R2 count of 128, by far the smallest of the twelve,
  and swift was a bonus language in that phase rather than a target.
- **The batch numbers assume a bisect that does not exist.** Amortisation was
  measured on batches known in advance to compile. In a real run the members
  are not known in advance, and locating a refusal inside a failed batch is
  the unbuilt engineering the CORE names. Treat the batched column as a lower
  bound on a batched run, not as a schedule.
- **No daemon, by instruction.** Kotlin's 2,397 ms is a cold kotlinc every
  time. A compile daemon would very likely collapse it, and the same is true
  of java, csharp and typescript. That route was excluded from the
  measurement on purpose and so nothing here quantifies it.
- **The first pass is discarded but kept.** `raw/tm_pass1_*.txt` holds the
  timeout-quantised first pass. It is retained because it is what the batch
  members were selected from, and because `raw/tm_diag.txt` is the evidence
  for discarding it. Do not read timings out of it.

---

## record

Everything is in `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`:

- `timing_build.py` -> `lanes/tm_<language>.sh` — the twelve self-contained
  timing lanes, one per language; the runner cannot see the repo, so each
  lane carries its 100 probe programs and its batch file inside itself.
- `raw/tm_<language>.txt` — the measurements, one line per probe:
  `<probe id>|<predicted>|<compile rc>|<compile ns>|<run rc>|<run ns>`, plus
  a `__GAP__` line holding that lane's own instrument cost and a
  `__BATCH100__` line holding the batched compile and run.
- `raw/tm_diag.txt` — the diagnostic that convicted `timeout`.
- `raw/tm_pass1_<language>.txt` — the discarded first pass.
- `timing_read.py` -> `timing_results.json` — the statistics, the derived
  python counts and the scaled estimates.

To reproduce: `python3 timing_build.py`, copy `lanes/tm_<lang>.sh` into
`SandboxDesign/agent/drop/` one at a time, poll
`agent/status/tm_<lang>.sh.status`, copy `agent/out/tm_<lang>.txt` back into
`raw/`, then `python3 timing_read.py`.
