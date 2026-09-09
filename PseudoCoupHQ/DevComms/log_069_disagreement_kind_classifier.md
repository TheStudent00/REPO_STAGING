# log 069 — the disagreement-kind classifier, and the dissolution of §1.1

2026-08-23. **RULED BY DEE TODAY** — "looks good! lets do it". This log
records a settled decision and the measurement behind it. Every number
below was re-measured from `matrices_full_v2/` for this log, not carried
over.

Read first: `PseudoCoupHQ/CLAUDE.md`,
`DevComms/log_065_spelling_gaps_and_reading_comparison.md`,
`DevComms/log_067_three_relations_alignment.md`,
`DevComms/log_068_dominant_plus_worked_example.md`,
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_ontology.md`.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

Scope of the measurement, stated so it is not mistaken for more: the
`plus` profiles on `whole|whole`, level 1, in `matrices_full_v2/` — the
94 profiles that live in the twelve `*.plus.L1.csv` files, 4,371 pairs.
(swift's `&+` lives in `swift.ampplus.L1.csv` and is outside this
particular count; log_068's 98-profile set is that 94 plus swift's 4.)

Scripts: the Job-1 measurement is reproduced inside
`Research/kind_fuzz_clustering/log070_dominant_operators.py`, which
applies the same classifier to every gate block; the standalone
verification snippets are quoted in place below. No probe was run; no
lane was submitted; `matrices_full_v2/` is read-only to this log.

---

## 1 — the classifier

**Every non-identical pair sorts by WHAT KIND of disagreement it has.
There is no threshold anywhere in it.**

A cell holds either a VALUE or an outcome token (`REFUSE`, `RAISE:*`,
`ABORT`, `UNREPRESENTABLE`). For a pair of profiles at one key, a
disagreement is therefore one of:

| cell-level kind | what it is |
| --- | --- |
| WINDOW | one side answers a value, the other holds a token — the holders have different ranges |
| VALUE | both answer values, and the values differ — a behaviour clash |

Sorting each PAIR by which kinds appear in it:

| kind | pairs | meaning |
| --- | --- | --- |
| WINDOW only — one side declines where the other answers, never a value-vs-value clash | 1,317 | same behaviour, narrower holder. **A representability fact, NOT a guarantee fact.** |
| VALUE only — both answer, values differ | 58 | a genuine behaviour fracture; the disagreeing cells ARE the mode boundary |
| MIXED — both kinds present | 2,691 | needs the region test, then human eyes if the region cannot be described |
| identical (zero disagreements) | 305 | the CONTRACT case, already settled |
| **all pairs** | **4,371** | |

Non-identical total: **4,066**.

## 2 — THE RULE, as ruled

- **WINDOW-only → SAME family.** Record the window as the profile's
  RANGE, never as a mode.
- **VALUE-only → DIFFERENT modes.** The disagreeing cells define and
  name the boundary.
- **MIXED → apply the region test.** Are the disagreeing keys a
  describable region — one operand negative, magnitude past a limit,
  one side declining? *A fracture has a boundary; noise does not.*
  **Undescribable → flag for the owner, do not decide.**

## 3 — the evidence rows, as objects

### WINDOW-only: `java short×short` against `java short×int`

Agreement 0.952 over all 289 cells; 14 disagreements; **all 14 are
decline-vs-answer, zero value clashes.** Same add, narrower holder.

| position | kind | `java.+ short x short` | `java.+ short x int` |
| --- | --- | --- | --- |
| 71 | WINDOW | `UNREPRESENTABLE` | `[1, 1.99999996088445186614990234375, 30]` |
| 79 | WINDOW | `UNREPRESENTABLE` | `[1, 1.999999959953129291534423828125, 30]` |
| 88 | WINDOW | `UNREPRESENTABLE` | `[1, 1.999999999068677425384521484375, 30]` |
| 96 | WINDOW | `UNREPRESENTABLE` | `[1, 1.99999999813735485076904296875, 30]` |

### VALUE-only: `python c_int64×c_int64` against `php int×int`

Agreement 0.910; 26 disagreements; **all 26 are value-vs-value, zero
window differences.** Wrapping against approximating — a real fracture.

| position | kind | `python.+ c_int64 x c_int64` | `php.+ int x int` |
| --- | --- | --- | --- |
| 1 | VALUE | `[-1, 1.9999999999999999998915797827514, 63]` | `[-1, 1.0, 64]` |
| 2 | VALUE | `[-1, 1.0009765625000000001084202172486, 63]` | `[-1, 1.0009765625, 63]` |
| 4 | VALUE | `[-1, 1.0000000000000000045536491244391, 63]` | `[-1, 1.0, 63]` |
| 5 | VALUE | `[-1, 1.0000000000000000001084202172486, 63]` | `[-1, 1.0, 63]` |

### MIXED, for contrast

`cpp.+ int32_t x int32_t` against `cpp.+ int32_t x int64_t`: agreement
0.734, 77 disagreements, **14 value clashes and 63 window differences**
— the pair log_065 and log_068 both used as their witness. Under the
classifier it is not a tie between two readings; it is one pair carrying
both kinds, and the region test is what it needs.

---

## 4 — WHY IT MATTERS: it DISSOLVES standing ruling §1.1

**The VALUE-vs-ALL-CELLS argument was always about this one thing.**

| reading | what it does with a window difference | what that costs |
| --- | --- | --- |
| ALL-CELLS | treats it as disagreement | splits rust's `i32`/`i64`/`u64` into three false "modes" — width is a holder property, not a guarantee |
| VALUE | ignores it entirely | produces a COVER, not a partition — 39 of 98 profiles in 2 to 11 parts (log_068 §3) |

**Both asked "HOW MUCH do they disagree" when the useful question is
"WHAT KIND of disagreement is it".** Neither reading could get both
cases right. The classifier gets both: the window difference is
recorded as a RANGE (so rust's three widths stay one family) and the
value clash is recorded as a mode boundary (so the fracture does not
vanish).

`STANDING_RULINGS_AWAITING_DEE.md` §1.1 is therefore
**CLOSED-BY-DISSOLUTION**, not answered — the question it asked has no
answer because it was the wrong question. That file is updated in place
with a pointer here.

---

## 5 — the supporting measurement: different operators do NOT look alike

the owner's standing worry is coincidental matches between different
operators. Measured on ONE holder pair so the holder cannot be the
cause — `ruby Integer x Integer`, `whole|whole` L1, 289 cells:

| pair | ALL-CELLS agreement | VALUE-cell agreement | comparable value cells |
| --- | --- | --- | --- |
| `*` vs `+` | 0.003 | 0.003 | 289 |
| `*` vs `-` | 0.003 | 0.003 | 289 |
| `-` vs `/` | 0.003 | 0.004 | 272 |
| `+` vs `/` | 0.010 | 0.011 | 272 |
| `**` vs `+` | 0.014 | 0.014 | 283 |
| `**` vs `-` | 0.017 | 0.018 | 283 |
| `%` vs `*` | 0.055 | 0.059 | 272 |
| `+` vs `-` | 0.059 | 0.059 | 289 |
| `%` vs `-` | 0.066 | 0.070 | 272 |
| `*` vs `**` | 0.090 | 0.092 | 283 |
| `%` vs `**` | 0.100 | 0.109 | 266 |
| `%` vs `/` | 0.125 | 0.070 | 272 |
| `**` vs `/` | 0.145 | 0.158 | 266 |
| `*` vs `/` | 0.166 | 0.176 | 272 |
| `%` vs `+` | 0.225 | 0.239 | 272 |

**Range 0.3% to 22.5%.** Form-signature gating plus cell values
separates `+`, `-`, `*`, `/` and `%` cleanly, with no risk of mixing —
the closest two arithmetic operators ever come on identical holders is
`%` against `+` at 0.225, and the two adds-and-subtracts sit at 0.059.

## 6 — the negative finding: the distribution is a CONTINUUM

Agreement over the 4,066 non-identical pairs, ten bands from 0.0 to
1.0:

| band | 0.0–0.1 | 0.1–0.2 | 0.2–0.3 | 0.3–0.4 | 0.4–0.5 | 0.5–0.6 | 0.6–0.7 | 0.7–0.8 | 0.8–0.9 | 0.9–1.0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pairs | 184 | 170 | 472 | 606 | 638 | 602 | 390 | 490 | 251 | 263 |

Plus **305 identical pairs** at exactly 1.0, counted separately.

**There is NO natural gap.** The distribution is not bimodal, so no cut
falls anywhere defensible — which is exactly why a threshold approach
fails and why the classifier is needed. This is the most useful negative
result in the log: it retires the search for a number.

---

## 7 — one thing the ruled classifier does not yet cover, flagged

A cell can also disagree TOKEN against DIFFERENT TOKEN — both sides
declined, but not with the same outcome. That is neither a window
difference nor a value clash.

- Inside the `plus` `whole|whole` L1 block: **0 pairs are token-kind
  ONLY**, so the ruled three-way classifier is complete there. **563 of
  the 4,066 non-identical pairs carry at least one such cell**, and
  under the rule as ruled those cells ride inside WINDOW-only or MIXED
  without changing the verdict.
- Across all 18 gate blocks of `matrices_full_v2/` (log_070's run):
  **482 pairs disagree ONLY in which decline they gave.** The ruled
  classifier has no bucket for them.

Witness, and it is the clean case:

| pair | disagreements | value clashes | window | token-vs-token | comparable cells |
| --- | --- | --- | --- | --- | --- |
| `cpp.% int32_t x int32_t` vs `csharp.% int x int` | 10 | 0 | 0 | 10 | 71 |

Two profiles that agree at every one of the 71 keys where both answer,
and differ only in HOW they decline the other 10 — a decline-vocabulary
difference, not a behaviour difference. **Flagged, not decided.**

---

## decided, recorded for audit

- The classifier is the owner's ruling of 2026-08-23 and is recorded, not
  re-derived. Every number was re-measured from `matrices_full_v2/`
  and reproduces exactly: 1,317 WINDOW-only, 58 VALUE-only, 2,691
  MIXED, 305 identical, 4,371 pairs over 94 profiles.
- The two evidence rows are quoted as OBJECTS — real canon strings at
  real positions — not described.
- The agreement histogram reproduces band for band
  (184/170/472/606/638/602/390/490/251/263), and it is a continuum with
  no gap. No threshold was applied anywhere in this log.
- The cross-operator control was measured on ONE holder pair so the
  holder could not explain the separation.
- `STANDING_RULINGS_AWAITING_DEE.md` §1.1 marked
  **CLOSED-BY-DISSOLUTION** with a pointer here; the reasoning moved
  into `SUPPORT_ontology.md` as a new section, ADDED, with nothing
  above it rewritten.
- The location note repeated from log_065: `SUPPORT_ontology.md` lives
  under `Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/`,
  not under `Research/kind_fuzz_clustering/`. The section was added
  there.

## awaiting the owner

1. **A fourth disagreement kind, or not.** 482 pairs across the run
   disagree ONLY in which decline they gave (`REFUSE` against
   `RAISE:DivideByZeroException`, and so on). Under the classifier as
   ruled they have no kind. Witness above. Structural, so it is his.
2. **What the region test's catalogue IS.** The rule says "a
   describable region"; log_070 §6 implements a catalogue (one operand
   negative, magnitude past a limit, exact result outside a width, and
   a general product-region test) and measures how far it reaches.
   Whether that catalogue is THE catalogue is the owner's.
