# log 049 — interval sampling, the two-language pilot, 2026-08-21

Two lanes RAN (rust, ruby). Everything downstream is assembly.
Vocabulary held throughout: super-node / sub-node / co-node /
sub-tree; the OS-stopped outcome is ABORT.

Scope, the owner's ruling: **rust and ruby ONLY**. The other ten follow later
if the pilot verifies. Nothing in this session touched them; the graph
here carries 43 nodes, all of them rust or ruby, asserted in the
headless verify.

## 1 — why

Today's value classes are EDGE values, six per form. Six points per
side let coincidental agreement survive: two operators can match on
every shared input pair and still be different functions. The extension
adds INTERVAL sampling — N samples per side spanning each holder's own
representable range — **in addition to** the edge classes, never
replacing them. Pilot: N = 32 per side, numeric forms only (whole,
fractional). Text and containers keep their edge sets untouched.

Acceptance was NOT re-run. Every interval sample lives inside its own
holder's range by construction, so the verdicts in
`acceptance_rust_A2.json` still hold and the rust lane simply reads the
ACCEPT cells out of it.

## 2 — the ladder (deterministic, closed-form, documented)

No random draw, no seed, no per-run variation. Every magnitude is an
exact integer root of a power of two computed in integer arithmetic, so
a re-run reproduces the same 32 values bit for bit.

**Whole, signed, width `W`** (range `-2^(W-1) .. 2^(W-1)-1`):

- 6 near-boundary anchors `[min, min+1, -1, 0, 1, max]`
- 13 log-spaced magnitudes `m_k = floor(2^(k*(W-1)/14))`, `k = 1..13`,
  as the exact integer 14th root of `2^(k*(W-1))`
- the same 13 NEGATED — both signs, the holder is signed
- 6 + 13 + 13 = 32

**Whole, unsigned, width `W`** (range `0 .. 2^W-1`):

- 4 anchors `[0, 1, max-1, max]`
- 28 magnitudes `m_k = floor(2^(k*W/29))`, `k = 1..28`
- 4 + 28 = 32, one sign only

**Unbounded whole holders** (ruby `Integer`, `Rational`, `BigDecimal`)
use a NOMINAL 128-bit window and the signed rule. That window is a
recorded choice, not a measurement: it matches the widest bounded whole
holder in the pilot (rust `i128`) so the two languages' ladders overlap
where they can.

**Fractional, binary floating, normal exponent range `[emin, emax]`:**

- 10 anchors: `+0.0`, `-0.0`, `+minsubnormal`, `-minsubnormal`,
  `minnormal`, `1.0`, `nextafter(1,2)`, `nextafter(1,0)`,
  `+maxfinite`, `-maxfinite`
- 11 magnitudes `1.5 * 2^e_k`,
  `e_k = emin + round(k*(emax-emin)/12)`, `k = 1..11`
- the same 11 NEGATED
- 10 + 11 + 11 = 32

The interval ladder carries **finite values only**. `inf` and `nan`
stay in the edge classes, where they already are — a ladder that spans
a range has no business inventing points outside it.

Seven ladders, one per distinct range: `w_s32`, `w_s64`, `w_u64`,
`w_s128`, `w_big128`, `f_b64`, `f_b32`. Every one was asserted
32-long and collision-free at build time (`l3_interval_values.py`).

## 3 — the lanes, and what they measured

Lane mechanics reused, not reinvented: the log-027 §3 agent lane
(gzip+base64 payload inside a self-contained `/bin/sh`, dropped into
`SandboxDesign/agent/drop/`, status polled at
`agent/status/<name>.status`, products in `/out`). rustc flags copied
verbatim from `l3_exec.py`.

| lane | route | cells | probes | wall | outcome |
|---|---|---|---|---|---|
| `iv_rust_00.sh` | A2 static, `rustc -C debug-assertions=on -C opt-level=0`, 3 chunks of ≤1500 | 116 accepted numeric holder pairs × op | 3,712 | **0.85 s** compute, 0.9 s lane | 2,716 answers, 996 `RAISE:panic`, 0 ABORT, 0 build failures |
| `iv_ruby_00.sh` | C, `eval` per sample | 792 (36 ordered numeric pairs × 22 operations) | 25,344 | **191.93 s** lane, of which 190 s is the stall budget → **≈2 s of actual evaluation** | 18,562 answers, 6,763 raises, 19 ABORT, 0 refusals, 0 missing, 19 restarts |

**Against the estimates.** rust's measured acceptance cost was 62.7 s
for 9,196 probes; the interval sweep costs **0.85 s** because it reuses
those verdicts and compiles three chunks instead of enumerating
acceptance again — the static path is cheap precisely because
acceptance is not repeated. ruby's route-C full value matrix ran at
2.8 s; the interval sweep's own evaluation is ≈2 s, the same order, and
the 191.93 s wall is almost entirely the 19 × 10 s inactivity budget
described below, not computation.

Three chunk builds: 0.3 s, 0.3 s, 0.2 s. Zero restarts on the rust
side.

### 3.1 two hazards the edge-value runs never met

An interval sample reaches `2^127`. That is new, and it broke things
the first time, which is worth recording rather than hiding.

**Hazard one — unbounded allocation.** `a ** b` and `a << b` at that
magnitude are allocations, not slow loops. The ruby driver caps its
address space at 2 GB so such a probe stops fast instead of swapping
the host, and the runner restarts the driver past whatever stopped it
— the same discipline `l3_exec.py` already uses for the compiled
languages. Whether ruby recovers with `NoMemoryError` (a RAISE) or the
VM stops outright (an ABORT) is itself part of what the probe measured;
both are recorded. A bignum computation is a C-level loop no
in-language alarm reaches, so the runner also carries a **10 s
inactivity watchdog**.

All **19 ABORTs are the same shape**: operation `**`, the whole
`BigDecimal` holder, ladder indices 7 and 20 (`±289430`). Each carries
its reason — `stalled>10s` where the harness stopped it,
`rc<n>` where the VM stopped itself. 19 of 25,344 probes, 0.07 %.

**Hazard two — a truncated literal is a WRONG number.** An answer can
be an exact integer of millions of digits. Printing it costs minutes,
and the earlier route-C driver's `inspect[0,120]` would have been
silently re-read as a smaller number — a correctness fault, not a
cosmetic one, and one the edge values never triggered because they
stopped at `2^64`. So an oversized answer now travels as a DECLARED
token — `BIGNUM` / `BIGRAT` / `BIGDEC`, carrying sign, exact bit length
and the leading 512 bits. 512 bits is 154 decimal digits against the 31
the canonical mant shows, so the printed canon is the true one; the
drop is declared in the token instead of hidden inside a literal.
**67 cells took that path** and the count is written into
`matrices_interval/index.json`, so the reliance is visible rather than
assumed.  One such cell, from `matrices_interval/ruby.gtgt.csv`
row `V15_2_2` (`Integer >> Integer`, sample 21):
`[-1, 1.16012938320636749267578125, 155709957]` — an exact integer of
about 47 million decimal digits, canonicalized correctly and printed in
40 characters.

## 4 — the tensor

the owner's row shape, his words: "each set of interval inputs and outputs to
be contained within in their own respective row." So the interval
results are NOT one row per sample. One row = one
`(operator, lhs holder, rhs holder, interval spec)`, carrying the input
sample VECTOR and the output result VECTOR. Own files,
`matrices_interval/<lang>.<op>.csv`; `matrices/` untouched.

    probe_id, lhs_holder, rhs_holder, interval_id, n_samples,
    lhs_canon_vector, rhs_canon_vector, output_canon_vector,
    n_values, n_declines

Vectors are semicolon-separated canonical strings under the v2 rules
unchanged.

**Format verification (`l3_interval_read.py` prints it):**

| check | number |
|---|---|
| files | 39 (17 rust operators, 22 ruby) |
| rows | 908 (rust 116, ruby 792) |
| samples inside those rows | 29,056 |
| non-rectangular lines | **0** — column count 10 everywhere |
| rows with a wrong vector length | **0** — all three vectors are `n_samples` long |
| empty vector slots | **0** — padding NOTHING; a slot with no value carries its outcome token |
| dirty canon cells (fractions, `~`, retired words, non-ascii minus) | **0** |
| outcome tokens in vectors | 7,778, all `REFUSE` / `RAISE:<kind>` / `ABORT` |
| oversized cells rebuilt from leading bits | 67 |

Three verbatim rows, `matrices_interval/rust.eqeq.csv` (the shortest
rows in the set; the header is the file's own first line):

```
probe_id,lhs_holder,rhs_holder,interval_id,n_samples,lhs_canon_vector,rhs_canon_vector,output_canon_vector,n_values,n_declines
V9_6_6,i128,i128,IV32:w_s128|w_s128,32,"[-1, 1.0, 127];[-1, 2.0, 126];[-1, 1.0, 0];[1, 0.0, 0];[1, 1.0, 0];[1, 2.0, 126];[1, 1.048828125, 9];…","[-1, 1.0, 127];…",true;true;…;true,32,0
V9_7_7,f64,f64,IV32:f_b64|f_b64,32,"[1, 0.0, 0];[-1, 0.0, 0];[1, 1.0, -1074];[-1, 1.0, -1074];[1, 1.0, -1022];[1, 1.0, 0];[1, 1.0000000000000002220446049250313, 0];…","[1, 0.0, 0];…",true;true;…;true,32,0
V9_8_8,f32,f32,IV32:f_b32|f_b32,32,"[1, 0.0, 0];[-1, 0.0, 0];[1, 1.0, -149];[-1, 1.0, -149];[1, 1.0, -126];[1, 1.0, 0];[1, 1.00000011920928955078125, 0];…","[1, 0.0, 0];…",true;true;…;true,32,0
```

(The three rows are 1,272–1,305 bytes each; the ellipses above stand
for the remainder of the 32-entry vectors, which are on disk verbatim.
`V9_7_7` reads correctly: the fractional ladder carries `+0.0` and
`-0.0` as DISTINCT samples — `[1, 0.0, 0]` and `[-1, 0.0, 0]` — and
`==` answers true for both, which is the right answer and not a
collision.)

## 5 — the graph, with the owner's edge criterion

`agreement_graph_interval_pilot.json` /
`graph_explorer_interval_pilot.html`. Nodes: 43 (19 rust, 24 ruby
operator matrices; 39 of them carry interval rows — `ruby.and`,
`ruby.or` and two rust operators have edge rows only). Edge rule
unchanged from log 048 (row-grain best-match). An interval row
contributes one `(lhs_canon, rhs_canon) -> output_canon` entry per
sample, so the sweep and the edge values share ONE pair space. That is
the whole mechanism.

Input pairs: **32,320 on the edge values alone → 41,315 with the sweep
(+8,995)**.

**the owner's criterion, settled 2026-08-21:** an edge counts only when
`input_overlap >= weight`, `input_overlap = shared / union`. Applied as
a FILTER, not a deletion: every edge is still emitted with `n_shared`,
`n_matched`, `n_union`, `input_overlap`, `value_weight` and the
EDGE-ONLY numbers, plus a `criterion_pass` flag, so the filter is
inspectable and reversible. The explorer has a checkbox for it, and the
headless verify asserts `criterion_pass == (input_overlap >= weight)`
on every edge.

714 edges; **567 pass, 147 filtered out**.

### 5.1 rust.+ ~ ruby.+ before and after

| | weight | n_shared | n_matched |
|---|---|---|---|
| edge values alone | **0.4024** | 169 | 68 |
| with the sweep | **0.5439** | 228 | 124 |

`input_overlap = 0.1413`, `value_weight = 0.7561`. The edge therefore
**FAILS** the owner's criterion and is filtered out.

The weight ROSE, which is the honest result and not the one the pilot
was aiming at: `rust.+` and `ruby.+` share only same-holder numeric
pairs, and on those the sweep mostly agrees. The coincidence-culling
shows up elsewhere — see below.

### 5.2 the coincidence cull — the point of the pilot

Counted where it shows, at the drawn threshold:

| threshold | edges reaching it on the edge values alone | still there with the sweep | **COINCIDENTAL, removed** |
|---|---|---|---|
| 0.95 | 127 | 52 | **75** |
| 0.85 | 164 | 61 | **103** |
| 0.70 | 329 | 220 | **109** |

Counted at the node-pair grain: **496 node pairs lost weight** once the
sweep ran. Counted at the input-pair grain: the sweep manufactured
89,861 (node pair, input pair) instances that did not exist before —
12,716 agree and **77,145 DISAGREE**.

Worked examples of what fell:

| node pair | edge values alone | with the sweep | drop |
|---|---|---|---|
| `rust.<` ~ `rust.<=` | 0.8626 | 0.4777 | 0.3849 |
| `rust.>` ~ `rust.>=` | 0.8626 | 0.4777 | 0.3849 |
| `rust.+` ~ `rust.^` | 0.8283 | 0.3832 | 0.4451 |
| `rust.+` ~ `rust.\|` | 0.8283 | 0.3832 | 0.4451 |
| `rust.-` ~ `rust.<<` | 0.8485 | 0.3925 | 0.4560 |
| `rust.&` ~ `rust.*` | 0.7475 | 0.3505 | 0.3970 |

On six values per side, `<` and `<=` look like the same operator 86 %
of the time. Sweep 32 values across the holder's range and they agree
48 %. That is exactly the artefact the owner said the edge classes were
letting through.

**The positive control passes.** Six node pairs sat at weight 1.0000 on
the edge values alone, and **all six are still 1.0000 after the sweep**:

- `ruby.&&` ~ `ruby.and`, `ruby.or` ~ `ruby.||` — genuine spellings of
  one operator
- `ruby.==` ~ `ruby.===` — on numerics, one operator
- `ruby.<<` ~ `ruby.>>` — agree on 1,483 of 1,483 shared pairs;
  decline-dominated (`RangeError` / `NoMemoryError` on both sides at
  these magnitudes)
- `rust.&` ~ `rust.&&`, `rust.|` ~ `rust.||` — 67 shared pairs, all
  REFUSE

So the strict "perfect agreement that turned out coincidental" count is
**0**, and that is the result we want: the sweep destroys 103 edges at
t=0.85 and leaves every genuine alias standing.

### 5.3 components

| threshold | with the criterion | without it |
|---|---|---|
| 0.95 | **35** components (4 multi-node, largest 6) | 18 |
| 0.85 | **27** components (8 multi-node, largest 6) | 11 |
| 0.70 | **12** components (7 multi-node, largest 24) | 1 |

Without the criterion the graph collapses to a single component by
t=0.70. With it, structure survives at every threshold. The criterion
is doing real work.

## 6 — headless verify

`node verify_graph_interval.js` — `domstub.js` cannot carry this page
(the explorer draws on a `<canvas>` and domstub's elements have no
`getContext`), so this verifier supplies a canvas-shaped stub, RUNS the
page's own script verbatim, and checks it:

- the one inline script runs with no throw;
- the embed equals `agreement_graph_interval_pilot.json` (43 nodes,
  714 edges);
- every edge endpoint is a node, no 0-weight edge, and
  `criterion_pass == (input_overlap >= weight)` on every edge;
- **10 threshold × criterion settings**: the page's live "n edges | c
  components" counter equals an INDEPENDENT union-find computed in the
  verifier — two methods, one answer, every time;
- the criterion checkbox actually changes the picture (t=0.70:
  188 edges / 12 components with it, 234 edges / 1 component without);
- the autofit interval runs, and after a physics step every node is
  finite and inside the hard boundary — the clamped springs, velocity
  clamp, gravity and boundary copied from the fixed
  `graph_explorer.html` do not explode.

The builder's own python-side verify also passes: JSON well-formed,
counts consistent, no 0-weight edges, every endpoint a node, every node
rust or ruby, HTML self-contained with no `<script src`.

## 7 — products

- `Research/kind_fuzz_clustering/l3_interval_values.py` — the ladder.
- `l3_interval_gen.py` + `l3_interval_ruby.py` — the two lanes.
- `lanes/iv_rust_00.sh`, `lanes/iv_ruby_00.sh` — as dropped.
- `raw/iv_rust_00.txt`, `raw/iv_ruby_00.txt` — the lane output, kept.
- `l3_interval_read.py` — the tensor + format verification.
- `matrices_interval/` — 39 CSVs, `index.json`, `README.md`.
- `l3_agreement_graph_interval.py` — the pilot graph.
- `agreement_graph_interval_pilot.json` (0.23 MB),
  `graph_explorer_interval_pilot.html` (0.24 MB, self-contained).
- `verify_graph_interval.js` — the headless verify.
- Spec: `Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/
  SUPPORT_conversion_spec.md`, section "interval sampling — the tensor
  extension", recorded as SETTLED.

## 8 — decided vs awaiting

### decided, recorded for audit (reversible, each one line)

1. Ladder as in §2; unbounded ruby whole holders take a nominal 128-bit
   window; the ladder is finite-only, `inf` and `nan` stay in the edge
   classes.
2. Row shape and columns as in §4; `;` as the vector separator; nothing
   padded; a valueless slot carries its outcome token.
3. Oversized ruby answers travel as declared `BIGNUM` / `BIGRAT` /
   `BIGDEC` tokens with 512 leading bits, never a truncated literal.
   67 cells relied on it; the count is in `index.json`.
4. Ruby address space capped at 2 GB; restart-past-what-stopped-it;
   10 s inactivity watchdog; a harness stop is ABORT and carries its
   reason.
5. rustc flags, chunking and the `catch_unwind` → `RAISE:panic`
   convention copied unchanged from `l3_exec.py`. A rust `BUILDFAIL`
   reads REFUSE, a `MISSING` reads ABORT.
6. the owner's edge criterion applied as a reversible filter with every raw
   number retained and a checkbox in the explorer.
7. Acceptance not re-run; `acceptance_rust_A2.json` reused as-is.

### awaiting the owner

1. **The 19 ABORTs are all `ruby **` on the whole `BigDecimal` holder
   at ±289430**, stopped by the 10 s inactivity budget. Keep the 10 s
   budget, raise it and pay the wall-clock, or drop `**` from the
   interval menu and leave its edge rows alone? (The 190 s of the
   ruby lane's 192 s is this budget.)
2. **The criterion cuts most cross-language edges**, including
   `rust.+ ~ ruby.+` (overlap 0.1413 against weight 0.5439). 101 of
   267 cross-language edges fail it. Cross-language nodes span
   different holder vocabularies, so their union is large by
   construction and the overlap is structurally small. Is that the
   intent — cross-language neighbourhood must earn a wide overlap — or
   should `input_overlap` be measured over the pairs the two nodes
   COULD share rather than the full union?
