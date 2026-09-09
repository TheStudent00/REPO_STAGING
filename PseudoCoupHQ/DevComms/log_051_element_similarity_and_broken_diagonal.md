# log 051 — element similarity, no scoring of declines, and the broken diagonal, 2026-08-21

Five updates to the interval pilot. Two RAN probes (rust, ruby); three
are rescoring and rendering. Scope unchanged and the owner's: **rust and ruby
ONLY** — the other ten still wait.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

the owner's rulings A–E of 2026-08-21 are recorded verbatim in
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/
SUPPORT_conversion_spec.md`, section "rulings A–E", as SETTLED.

## 1 — ruling A: similarity is PER ELEMENT and NUMERIC

`l3_row_sim.py`. A canonical numeric answer is `[sign, mant, expo]` and
two of them are compared element by element, AS NUMBERS, never as bytes:

| element | distance | similarity |
|---|---|---|
| sign | `abs(s0 - s1)`, which is 0 or 2 | `1 - d/2` → {1.0, 0.0} |
| mant | `abs(m0 - m1)`, already bounded by 1 because mants live in [1,2) | `1 - d`, clamped at 0 |
| expo | `abs(e0 - e1)`, an unbounded integer | **the decay knob**: `1/(1 + d)` |

A sign flip costs real distance — the owner's call, and the reason is that
across a 32-point interval closeness that survives a sign flip is
coincidence. The mant clamp is not decoration: zero canonicalizes to
mant `0.0` and a mant that rounds up at the 31st digit spells `2.0`, so
`d` can reach 2; both are real distance and both floor at 0.

The three combine into one per-sample similarity by the owner's sketch,
EUCLIDEAN: the distance from the perfect point `(1,1,1)` in
element-similarity space, normalised by `sqrt(3)`, subtracted from 1.
Every knob is a single named constant in `l3_row_sim.py` —
`EXPO_DECAY`, `EXPO_DECAY_K`, `COMBINE`, `COMBINE_WEIGHTS`,
`SIGN_MAX_DISTANCE` — and they are copied into the graph JSON as
`scoring_knobs` so a reader never has to guess which setting produced a
number. `COMBINE = "weighted_mean"` is implemented as the documented
alternative and is one word away.

A worked position, `rust.+ / V0_4_4 / i64 + i64` against
`rust.- / V1_4_4 / i64 - i64` on the diagonal, sample 6:

```
  +  ->  [1, 1.375, 5]        -  ->  [1, 0.0, 0]
  sign distance 0    -> sign_sim 1.0
  mant distance 1.375 -> mant_sim 0.0        (clamped)
  expo distance 5    -> expo_sim 0.1666666666666667
  var_sim (euclidean) = 0.248458
```

Byte identity called that position a flat 0. It is not a flat 0: the
signs agree, the magnitudes do not.

### 1.1 the FORM CLASSIFIER, not cast-and-catch

Every `output_canon` declares its form in its own prefix, so the
classifier is total and nothing is ever cast and caught:

| prefix | form | rule |
|---|---|---|
| `[` | numeric | the element rule above; a NON-FINITE (`[1, inf]`, `[-1, inf]`) has no mant and no expo to difference, so within the numeric form it compares by identity |
| `nan` | numeric | the one special word the canon keeps; identity, same reason |
| `t\|` | text | identical NFC bytes → 1.0, else euclidean over the three length similarities. NOT exercised by the pilot (numeric forms only) and flagged as such |
| `c\|` | container | identity. Not exercised |
| `true` / `false` | truth | identity |
| `opaque:` | opaque | identity — a value the canon does not decompose (rust `Range`, ruby `Complex`) |
| `REFUSE` / `RAISE:<kind>` / `ABORT` | an outcome token | **not scored at all** — see ruling B |

Same form → that form's rule. Different form → similarity 0. No
exceptions, no casting errors.

## 2 — ruling B: declines are NOT SCORED AT ALL

the owner: "lets only do matching on similarity of actual objects now. lets
avoid things like REFUSE/RAISE/whatever-else."

A sample position where EITHER row's output is `REFUSE`, `RAISE:*` or
`ABORT` is excluded from the comparison entirely — out of the numerator
AND out of the denominator. If two rows share an input ladder and have
ZERO comparable positions left, there is **no connector between them at
all**, not a zero-weight one.

Every connector records `n_comparable`, `n_excluded_declines` and the
weight. The old byte-identity number rides along as `weight_byte` /
`n_matched_byte`, SECONDARY, over all 32 positions so it is directly
comparable with log 050.

**63,467 cross-operator row pairs share an input ladder and have zero
comparable positions after the exclusion. None of them has a
connector.** That single number is what retires the all-decline
clusters; §6 counts what actually went.

## 3 — ruling C: the lanes that broke the diagonal

`l3_interval_c.py` emits both lanes; `l3_interval_c_read.py` folds them.
The diagonal rows are NOT overwritten — `matrices_interval/` is opened
for reading only, and the new rows live in `matrices_interval_c/` under
the SAME ten columns, the same canon rules and the same `;` separator.

- **C1 SHIFTED**, `interval_id` `IV32:<a>|<b>:shift`. `x_k OP x_{(k+1)
  mod 32}`. No new values: the ladder already carries every point, only
  the pairing moved, so `lhs_canon_vector` is the ladder in order and
  `rhs_canon_vector` is the ladder rotated by one.
- **C2 ONE-LEVEL COMPOSITION**, `IV32:<a>|<b>:comp1`.
  `op(op(x_k, x_k'), op(x_k, x_k'))` — each operator's own outputs fed
  back through itself. The composed operands are OUTPUT values, which
  mostly do not land on ladder points, so this is a real probe run at
  the composed points. A comp1 row's `lhs_canon_vector` and
  `rhs_canon_vector` are BOTH the diagonal row's `output_canon_vector`;
  `lhs_holder`/`rhs_holder` still name the SOURCE operand holders so the
  row traces back to the diagonal row it composes.

Two mechanical points worth recording rather than hiding.

**Type validity of the composition is decided from data, not guessed.**
`op(y, y)` has to typecheck in rust. `y`'s type is read out of the
diagonal lane output (`raw/iv_rust_00.txt`, whose answered lines carry
`std::any::type_name`), and the composition is emitted only where
`(op, ty, ty)` is an ACCEPT cell in `acceptance_rust_A2.json`. **110 of
the 116 accepted numeric cells compose**; the 6 that do not are the `..`
cells, whose output is a `Range` and not a holder in the table at all.
Nothing was speculatively compiled, and there were **0 build failures**.
ruby is route C and has no such question — everything is `eval`'d.

**Where an operand of the composition declines, the composed probe is
NOT RUN and the position is excluded.** ruby detects this itself and
reports the operand's own outcome under the kinds `RAISEOP` /
`REFUSEOP`, so the count is visible instead of inferred; rust gets the
same effect for free, because a panic while computing the operand
unwinds the whole probe function and is caught as `RAISE:panic`. The
reader cross-checks the claim against the diagonal rows: **rust 996
positions, ruby 6,782 positions, 0 of them disagreeing with the
diagonal.** (ruby's own count is 6,763; the other 19 are the log-049
`**`/`BigDecimal` ABORTs, which stop the process rather than raising.)

The rust driver also gained BUILD-FAILURE BISECTION — the log-049 driver
condemned all 1,500 probes of a failed chunk to `BUILDFAIL`, which is
too blunt once a chunk carries a composed expression. It never fired.

### 3.1 what ran, and where the time went

the owner asked how many files get compiled and why a run takes the time it
does, so both drivers now print it and write a `__TIMING__` line into
their lane output.

**rust — `lanes/iv_rust_c0.sh`, 7,232 probes** (116 shifted cells + 110
composed cells × 32 samples):

| | |
|---|---|
| chunk FILES compiled | **5** (cap 1,500 probes per file: 1500, 1500, 1500, 1500, 1232) |
| compile invocations | **5** (bisection never fired; 0 build failures) |
| per-chunk build | 0.38, 0.34, 0.37, 0.39, 0.34 s |
| **compile total** | **1.821 s — 98.3 % of the run** |
| **execution total** | **0.018 s — 1.0 %** |
| driver overhead | 0.014 s |
| **wall** | **1.853 s** compute, 2.0 s lane |
| outcome | 5,016 answers, 2,216 `RAISE:panic`, 0 ABORT, 0 BUILDFAIL, 0 restarts |

So the rust lane's cost is `rustc`, essentially in full. 7,232 probes
execute in eighteen milliseconds; compiling the five files they live in
takes a hundred times that. The chunk cap is therefore the only lever
that matters on this route, and 1,500 is what the pilot set.

**ruby — `lanes/iv_ruby_c0.sh`, 50,688 probes** (792 cells × 32 samples
× 2 variants) in ONE process, as the pilot ran one process:

| | |
|---|---|
| files compiled | **0** — route C is `eval`, nothing is compiled |
| ruby processes | **56** — 1, plus 55 restarts past a probe that stopped it |
| **stall budget** | **550.00 s — 98.8 % of the run** (55 stalls × the 10 s inactivity budget) |
| **actual evaluation** | **6.80 s — 1.2 %** |
| **wall** | **556.80 s** |
| outcome | 31,734 answers, 12,136 raises, 6,763 operand-declines (composed probe not run), 55 ABORT, 0 refusals, 0 missing |

The shape is exactly log 049's, scaled: **all 55 ABORTs are operation
`**`** (ruby op index 18), **and every one of them carries a
`BigDecimal` holder on at least one side** — 21 in the shifted rows, 34
in the composed rows — stopped by the 10 s inactivity budget at the
large ladder magnitudes. 55 of 50,688 probes, 0.11 %. Log 049 asked the owner whether to keep
that budget and got no answer, so it was kept unchanged at 10 s — and it
is again ~99 % of the ruby wall clock. §8 asks again with a bigger
number attached.

## 4 — the tensor extension

`matrices_interval_c/`, 39 CSVs, `index.json`, `README.md`.

| check | number |
|---|---|
| files | 39 |
| rows | **1,810** (rust 116 shift + 110 comp1; ruby 792 shift + 792 comp1) |
| samples inside those rows | 57,920 |
| non-rectangular lines | **0** — column count 10 everywhere |
| rows with a wrong vector length | **0** |
| empty vector slots | **0** — padding NOTHING |
| dirty canon cells | **0** |
| outcome tokens in vectors | 36,726 |

## 5 — the graph, rebuilt

`l3_row_graph_v2.py` → `row_graph_v2.json` (23.84 MB) and
`row_graph_explorer_v2.html` (23.85 MB, self-contained). The log-050
builder `l3_row_graph.py` and its products are UNTOUCHED and still stand
as the byte-identity audit trail.

```
nodes by kind: 2718 row, 39 central, 2757 total
  by language: rust 342, ruby 2376
  by variant:  diagonal 908, shift 908, comp1 902
edges by kind: 2718 internal, 70362 external, 73080 total
distinct input ladder pairs: 224   (was 25 on the diagonal alone)
comparable universe: 143027 row pairs share an identical input ladder
  of which SAME operator (carried by internal connectors):     9198
  of which CROSS operator with ZERO comparable positions
    after ruling B -> NO CONNECTOR AT ALL:                    63467
  of which CROSS operator with a comparable position:         70362
external weight distribution: 38746 at exactly 0.0,
                              25542 strictly between,
                               6074 at exactly 1.0
cross-language external connectors: 9782 of 70362
```

Internal connectors (ruling E — rescored under A/B like everything
else): 2,718, exactly one per row node, mean weight 0.9829, 2,324 at
exactly 1.0, **1,116 flagged `no_comparison`** — either no co-row shares
their inputs, or every shared position is a decline. A `no_comparison`
internal connector is 1.0 by convention and says so in its tooltip.

External connectors by threshold, components counted EXTERNAL-ONLY
(ruling D):

| threshold | external | same-lang | cross-lang | components | multi-node | largest | mixes operators |
|---|---|---|---|---|---|---|---|
| 1.00 | 6,074 | 4,145 | 1,929 | 1,935 | 99 | 62 | yes (6 lang.op) |
| 0.95 | **6,272** | 4,297 | 1,975 | **1,867** | 109 | **62** | yes (6 lang.op) |
| 0.85 | **6,574** | 4,508 | 2,066 | **1,824** | 119 | **86** | yes (12 lang.op) |
| 0.70 | **7,825** | 5,508 | 2,317 | **1,684** | 125 | **131** | yes (23 lang.op) |

(The component count includes the 39 central nodes, which carry no
external connector and so stand alone in that view.)

By variant, at t=0.85: comp1 2,678, diagonal 2,203, diagonal↔comp1 622,
shift 1,071. (`diagonal/comp1` is a mixed pair — one row of each — which
happens when an operator's diagonal outputs happen to equal another
operator's ladder inputs.)

**The largest component is no longer a decline family.** At t=0.85 it is
86 nodes over 12 `lang.op` — `ruby.&`, `ruby.&&`, `ruby.*`, `ruby.+`,
`ruby.<<`, `ruby.|`, `ruby.||`, `rust.&`, `rust.*`, `rust.+`,
`rust.<<`, `rust.|` — cross-language and value-carrying. Log 050's
largest component at every threshold was the 39 ruby rows that agreed by
refusing identically. That family is gone from the top of the scale.

## 6 — the sanity numbers the owner asked for, verbatim

```
  rust.+ ~ ruby.+   (before: 0.9062 byte-identity max on 13 row pairs (log 050 s4.1))
      diagonal          13 connectors  weight max 1.0000 mean 0.9909 min 0.9195  | n_comparable mean 29.9, excluded mean 2.1  | old byte-identity max 0.9062 mean 0.7428
      shift             13 connectors  weight max 1.0000 mean 0.9982 min 0.9769  | n_comparable mean 29.2, excluded mean 2.8  | old byte-identity max 0.9375 mean 0.7212
  rust.+ ~ rust.-   (before: 0.0312 byte-identity on 6 row pairs (log 050 s4.2))
      diagonal           6 connectors  weight max 0.2352 mean 0.1699 min 0.1417  | n_comparable mean 30.2, excluded mean 1.8  | old byte-identity max 0.0312 mean 0.0312
      shift              6 connectors  weight max 1.0000 mean 0.5177 min 0.3567  | n_comparable mean 24.8, excluded mean 7.2  | old byte-identity max 0.1250 mean 0.0729
  ruby.<=> ~ rust.-   (before: 1.0000 byte-identity on 13 row pairs (log 050 s4.3))
      comp1             84 connectors  weight max 1.0000 mean 1.0000 min 1.0000  | n_comparable mean 32.0, excluded mean 0.0  | old byte-identity max 1.0000 mean 1.0000
      diagonal          13 connectors  weight max 1.0000 mean 1.0000 min 1.0000  | n_comparable mean 32.0, excluded mean 0.0  | old byte-identity max 1.0000 mean 1.0000
      shift             13 connectors  weight max 0.4055 mean 0.3976 min 0.3942  | n_comparable mean 32.0, excluded mean 0.0  | old byte-identity max 0.0938 mean 0.0841
  all-decline ruby family (ruby.&, ruby.<<, ruby.=~, ruby.>>, ruby.^, ruby.| on Float/Rational/BigDecimal): 11805 comparable cross-operator row pairs under the OLD byte-identity rule, 0 connectors under rulings A/B  -- GONE
  all-decline ruby family (ruby.&, ruby.<<, ruby.=~, ruby.>>, ruby.^, ruby.| on Integer/Rational/BigDecimal): 10269 comparable cross-operator row pairs under the OLD byte-identity rule, 81 connectors under rulings A/B  -- NOT GONE
```

Read plainly, and not flattered:

**`rust.+ ~ ruby.+` went UP, from 0.9062 to 0.9909 mean, max 1.0000.**
That is ruling B doing exactly what it says. Log 050 §4.1 found the
29/32 pairs disagreeing at precisely three positions, and all three were
overflow points where `i128` panics and ruby's unbounded `Integer` keeps
going. Ruling B excludes a position where either side declined, so those
three positions leave the denominator and the remaining 29 agree. The
two additions are now recorded as agreeing on every position where both
of them answer, which is the true statement; the place where they differ
is a decline, and the owner has ruled declines out of scoring.

**`rust.+ ~ rust.-` went UP too, from 0.0312 to 0.1699 mean on the
diagonal**, and the shifted rows do NOT separate them further — they
bring the two operators CLOSER, to 0.5177 mean. This is the honest
result and it is the opposite of what breaking the diagonal was expected
to do. The reason is ruling A: on the shifted pairing `x_k + x_{k+1}`
and `x_k - x_{k+1}` are two numbers of the same sign and a similar
magnitude wherever `x_{k+1}` is small against `x_k`, and per-element
numeric similarity pays for magnitude closeness where byte identity paid
nothing. Byte identity said 1/32; the elements say the two answers are
in the same neighbourhood. Both are true statements about different
questions. **Ruling A and ruling C pull in opposite directions here and
the owner should see that before the other ten languages run** (§8).

**`ruby.<=> ~ rust.-` on the DIAGONAL is still 1.0000, and that is
correct, not a failure.** On the diagonal both operators really do
answer 0 at all 32 points; `v <=> v` is `0` and `v - v` is `0`. No
scoring rule can or should separate two functions that returned the same
value at every point measured. What separates them is the measurement,
which is what ruling C added: **the SHIFTED rows read 0.3942–0.4055**,
because `x_k <=> x_{k+1}` is one of {-1, 0, 1} while `x_k - x_{k+1}` is
the difference. So the answer to "must now differ" is: the diagonal does
not differ and should not; the shifted rows differ, and they are in the
graph as their own nodes with their own connectors. The comp1 rows are
also 1.0000 (84 of them) for the same structural reason — both
operators' diagonal outputs are all-zero, so both compose over the same
all-zero operands, and `0 <=> 0` and `0 - 0` are both `0`.

**The all-decline ruby cluster is GONE on Float/Rational/BigDecimal:
11,805 comparable cross-operator row pairs under the old rule, 0
connectors now.** `ruby.=~` has NO connector anywhere in the graph — it
declines on every sample of every row, so under ruling B it is
comparable with nothing. That is the retirement the owner asked for.

**81 connectors survive among those operators on
Integer/Rational/BigDecimal, and they are not decline artefacts.** They
were checked one at a time: `n_comparable` runs 9 to 32, weights spread
0.138 to 1.0, and `ruby.=~` appears in none of them. The four that sit at
exactly 1.0 are `ruby.& ~ ruby.|` on `Integer & Integer` with **32
comparable positions and 0 excluded** — which is a true identity, since
`v & v` and `v | v` are both `v`. The example connector `ruby.& ~
ruby.<<` on `Integer` reads weight 0.4469 over 21 comparable positions
where its old byte-identity number was 0.0625. These are real numeric
agreements on real values, which is what was wanted.

## 7 — the explorer and the headless verify

`row_graph_explorer_v2.html`, self-contained, data embedded, no CDN, no
`<script src`. Everything log 050's explorer had, plus a **variant
filter** (all / diagonal only / shifted only / composed only), a **colour
by variant** mode, and tooltips that show `n_comparable`,
`n_excluded_declines` and the secondary `weight_byte` on every external
connector.

**Ruling D is implemented in two places and checked in both.**

- The internal spring constant is **0.0008 against 0.006 for external** —
  near zero. Internal connectors tether a row to its `lang.op` central
  node visually and do nothing else; external connectors carry the
  layout.
- **Component counting is EXTERNAL-ONLY, always**, whether or not
  internal connectors are drawn. The rule line under the toolbar says
  so.
- The clamped linear springs, velocity clamp, gravity to centre, hard
  boundary, grid repulsion and periodic autofit are unchanged from the
  log-050 page, which does not explode.

`node verify_row_graph_v2.js`. The new thing worth naming: **ruling A is
RE-IMPLEMENTED in the verifier**, in JavaScript, straight from the canon
strings in `matrices_interval/` and `matrices_interval_c/` — the form
classifier, the three element similarities and the euclidean combine —
and every one of the 70,362 external weights is recomputed and compared.
Two implementations, one answer.

```
  [script] the page's one inline script ran with no throw
  [embed] 2757 nodes, 73080 connectors, identical to row_graph_v2.json
  [kinds] 2718 row nodes (comp1 902, diagonal 908, shift 908) + 39 central nodes; 2718 internal + 70362 external connectors; header counts agree
  [refs] every connector endpoint is a node, every weight in [0,1]
  [internal] exactly one internal connector per row node (2718), each to its OWN lang.op central node; no_comparison == (n_co_rows_comparable == 0) and always weight 1.0 (ruling E)
  [rows] all 2718 row nodes re-read from 2 interval matrix directories
  [external A] all 70362 weights recomputed from the canon strings by an INDEPENDENT ruling-A implementation; worst disagreement 5.00e-7 (byte-identity secondary 0.00e+0), tolerance 0.000001
  [external B] 70362 cross-operator pairs share an input ladder AND have a comparable position -- all present; 63467 share a ladder but have ZERO comparable positions -- none of them has a connector, as ruling B requires
  [counters] 72 threshold x internal-toggle x draw-cap x variant settings: the page's live row/central/external/internal/component counts equal an independent union-find, every one
  [ruling D components] t=0.85 with internal connectors: "2718 row nodes | 39 central nodes | 6574 external | 2718 internal | 1824 components"; without: "... 6574 external | 0 internal | 1824 components" -- the internal count moves, the COMPONENT count does not (external-only, as ruled)
  [threshold cuts external only] t=1.00 -> 6074 external, t=0.00 -> 10000 external, internal unchanged at 2718 both times
  [draw cap stated] "70362 external connectors clear 0.00, the top 1000 BY WEIGHT are drawn, 69362 are not."
  [ruling D springs] internal spring constant 0.0008 against external 0.006; over 2718 internal and 6574 external connectors the internal springs carry 3.44% of the total spring impulse -- a tether, not the layout
  [autofit] the periodic fit ran with no throw
  [physics] after 800 steps every one of 2757 nodes is finite and inside the hard boundary (grid repulsion, clamped linear springs, velocity clamp, gravity, boundary)
  [settle] 60 further steps move the busiest node 0.000 px; the picture spans 1344 px from centre -- settled, not drifting
  [self-contained] data embedded, placeholder gone, no external script, no CDN
HEADLESS VERIFY: all checks pass
```

The builder's own python-side verify passes the same ground
independently.

## 8 — decided vs awaiting

### decided, recorded for audit (reversible, each one line)

1. Element similarities as in §1; `EXPO_DECAY = reciprocal` and
   `COMBINE = euclidean`, both single constants in `l3_row_sim.py` and
   both copied into the graph JSON as `scoring_knobs`.
2. A non-finite numeric (`[±1, inf]`, `nan`) compares by identity
   INSIDE the numeric form, because it carries no mant and no expo to
   difference.
3. Truth, container and opaque forms compare by identity; text has a
   defined rule that the pilot does not exercise. The classifier is
   total: every canon string lands in exactly one form and nothing
   raises.
4. `weight_byte` / `n_matched_byte` kept on every connector as the
   SECONDARY record, over all 32 positions so it is directly comparable
   with log 050.
5. The ruling-C rows live in `matrices_interval_c/`, a second directory
   with the identical ten-column schema; `matrices_interval/` is opened
   for reading only, so log 049/050 stand unchanged.
6. `SHIFT = 1` — the shifted pairing is `x_k OP x_{(k+1) mod 32}`, one
   constant in `l3_interval_c.py`.
7. A comp1 row's input vectors ARE the diagonal row's output vector;
   `lhs_holder`/`rhs_holder` keep naming the source operand holders so
   the row traces back.
8. rust composition validity decided from the diagonal lane's recorded
   `type_name` plus `acceptance_rust_A2.json`; nothing speculatively
   compiled. Chunk cap 1,500 unchanged; build-failure bisection added
   and never needed.
9. The 10 s ruby inactivity budget kept unchanged from log 049, pending
   the owner's answer to log 049's question 1.
10. Internal spring 0.0008 against external 0.0060; components counted
    external-only at every threshold and with the internal toggle in
    either position.

### awaiting the owner

1. **Ruling A and ruling C pull against each other on `+` versus `-`
   (§6).** Byte identity said `rust.+ ~ rust.-` was 1/32; per-element
   similarity says 0.17 on the diagonal and 0.52 on the shifted
   pairing, because `a+b` and `a-b` are numerically close whenever `b`
   is small against `a`. Breaking the diagonal made two different
   operators look MORE alike, not less. Is that intended — similarity
   is about magnitude and these two operators genuinely answer nearby
   numbers — or should the expo decay be sharpened, or the mant given
   more weight, so magnitude closeness stops paying? The knob is one
   constant and the run is two seconds for rust.
2. **Ruling B lets a weight of 1.0 rest on a single comparable
   position.** `rust.+ ~ rust.-` on `u64` shifted reads **1.0000 on
   n_comparable = 1**: unsigned subtraction underflows and panics at 31
   of the 32 shifted positions, so ruling B excludes them, and the one
   surviving position happens to agree. **64 connectors have
   n_comparable = 1, and 41 of those sit at weight 1.0.** The number is
   recorded on every connector and shown in the tooltip, so nothing is
   hidden — but should there be a MINIMUM n_comparable below which no
   connector is emitted (or below which it is emitted and flagged, the
   way the log-049 criterion was)?
3. **The ruby `**` stall budget is now 98.8 % of the ruby wall clock.**
   55 ABORTs at 10 s each is 550 s of the 556.80 s run; the actual
   evaluation is 6.80 s. Log 049 asked this with 19 ABORTs and 190 s;
   the shifted and composed pairings roughly tripled it. Keep 10 s and
   pay it, lower it (the probes are stuck, not slow — every one is `**`
   at bignum magnitudes), or drop `**` from the interval menu and leave
   its edge rows alone? Before the other ten languages run, this is the
   single largest cost in the pilot.
4. **comp1 comparability is narrow by construction.** Two comp1 rows
   are comparable only where the two operators' DIAGONAL outputs
   coincide, which is exactly the case the composition was meant to
   disambiguate — so `ruby.<=> ~ rust.-` composes over the same all-zero
   operands and stays at 1.0. Is one level enough, or should C2 compose
   across operators (`op_a` applied to `op_b`'s outputs) so the
   composition can separate rather than only confirm?

## 9 — products

- `Research/kind_fuzz_clustering/l3_row_sim.py` — rulings A and B as one
  scoring module, with the knobs as named constants.
- `l3_interval_c.py` — the ruling-C lane generator (C1 shifted, C2
  composed), with the rust type-validity plan and the timing
  instrumentation.
- `l3_interval_c_read.py` — the ruling-C rows and their format verify.
- `lanes/iv_rust_c0.sh`, `lanes/iv_ruby_c0.sh` — as dropped.
- `raw/iv_rust_c0.txt`, `raw/iv_ruby_c0.txt` and the two lane logs
  `raw/iv_rust_c0.lane.log`, `raw/iv_ruby_c0.lane.log` — kept.
- `matrices_interval_c/` — 39 CSVs, `index.json`, `README.md`.
- `l3_row_graph_v2.py` — the v2 builder, with the explorer template
  embedded.
- `row_graph_v2.json` (23.84 MB), `row_graph_explorer_v2.html`
  (23.85 MB, self-contained).
- `verify_row_graph_v2.js` — the headless verify, carrying its own
  independent ruling-A/B implementation.
- Spec: `Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/
  SUPPORT_conversion_spec.md`, section "rulings A–E", recorded as
  SETTLED.

`l3_row_graph.py`, `row_graph.json`, `row_graph_explorer.html`,
`verify_row_graph.js`, `l3_agreement_graph_interval.py`,
`agreement_graph_interval_pilot.json`,
`graph_explorer_interval_pilot.html` and `matrices_interval/` are all
untouched and still stand as logs 049 and 050 left them.
