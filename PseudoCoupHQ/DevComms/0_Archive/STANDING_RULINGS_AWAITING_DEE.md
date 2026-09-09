# Awaiting the owner — every open ruling, one by one

2026-08-23. A living index, written because the open items were
scattered across logs 054 to 066 and could only be reassembled by
reading all of them. Each item states what is true, what the choice
is, and what changes either way — so it can be answered from this
file alone, without opening the logs.

Ordered by what they block. Section 1 blocks the dominant-operator
work; section 2 blocks nothing but is owed; section 3 is the older
PseudoCoup_v5 ledgerer walk, paused where it was paused.

---

## 1. blocks the dominant-operator construction

### 1.1 the two readings — CLOSED-BY-DISSOLUTION 2026-08-23

**The question had no answer because it was the wrong question.** the owner
ruled the **disagreement-kind classifier** on 2026-08-23 ("looks good!
lets do it"), and it replaces the choice rather than making it.

Both readings asked *how much* two profiles disagree. The useful
question is *what kind* of disagreement it is — a WINDOW difference
(one side declines where the other answers: a representability fact) or
a VALUE clash (both answer, values differ: a behaviour fracture).

| pair kind | verdict | measured over the 4,371 `plus` `whole\|whole` L1 pairs |
| --- | --- | --- |
| WINDOW-only | SAME family; the window is the profile's RANGE, never a mode | 1,317 |
| VALUE-only | DIFFERENT modes; the disagreeing cells ARE the boundary | 58 |
| MIXED | apply the region test; undescribable → flag, do not decide | 2,691 |
| identical | the CONTRACT case, already settled | 305 |

ALL-CELLS treated window differences as disagreement and split rust's
`i32`/`i64`/`u64` into three false modes; VALUE ignored them and
produced a cover, not a partition. **Neither could get both cases
right; the classifier gets both.** The agreement distribution was also
measured and is a CONTINUUM with no gap
(184/170/472/606/638/602/390/490/251/263 across the ten bands), so no
threshold was ever available to either reading.

The item has moved out of this file, per "how to use this file", into
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_ontology.md`
(new section, ADDED, nothing above it rewritten), with the reasoning
attached. Recorded in
`DevComms/log_069_disagreement_kind_classifier.md`; applied across every
probed operator in `DevComms/log_070_dominant_operators_all.md`.

**Two sub-questions the classifier opened, now tracked as §1.5 and
§1.6 below.**

The historical statement of the closed item is kept below the line so
the record of what was decided against is not lost.

---

<details>
<summary>the question as it stood before 2026-08-23</summary>

**What is true.** Every profile cell holds either a value or an
outcome token (`REFUSE`, `RAISE:<kind>`, `ABORT`, `UNREPRESENTABLE`).
Two ways to compare two profiles:

- **VALUE reading** — a cell where either side holds an outcome token
  is dropped from numerator AND denominator.
- **ALL-CELLS reading** — outcome tokens count as answers;
  byte-identical token = agreement; the denominator is the full grid.

**Measured, over `matrices_full_v2/` (log 065):**

| | containment pairs | `plus` whole\|whole L1 parts |
| --- | --- | --- |
| VALUE | 1,046 | 3 by components, **14 by maximal cliques** |
| ALL-CELLS | 368 | 30 (13 cross-language) |

ALL-CELLS is a strict subset of VALUE — 368 shared, 678 only in
VALUE, **zero** only in ALL-CELLS. So ALL-CELLS is never the
disagreeing reading, only the more conservative one.

**What each reading gets right, and wrong:**

- VALUE gets the mode partition right. Under ALL-CELLS, rust's
  `i32`, `i64` and `u64` split into three parts purely because they
  decline at different WIDTHS — and width is a holder property, not
  a guarantee. Measured: all three agree with ruby's `Integer` at
  every cell where they answer, zero disagreements.
- ALL-CELLS gets fracture detection right. Under VALUE,
  `rust.+ i32` against `ruby.+ Integer` scores a perfect 1.000 while
  differing at all 14 overflow keys — the fracture vanishes exactly
  where it matters.

**The consequence nobody should choose blind.** Choosing VALUE also
means choosing CLIQUE semantics for the partition. Dropping declines
can leave two profiles with zero comparable cells — never compared —
which then merge through a third. That is the chaining hazard
`SUPPORT_ontology.md` already rules against for GROUP ("never a
connected component... measured: 7,212 such triples"), and it is why
the same data gives 3 parts by components and 14 by cliques.

**The lean on record (Claude, not a ruling):** state it as two jobs
rather than one choice — *the mode partition uses the VALUE reading
with clique semantics; containment and fracture detection use
ALL-CELLS.* Recorded as a rule so the two never get mixed up in code.

**Needed from the owner:** one reading per job, or a single reading for
both, and clique-versus-component if VALUE is chosen anywhere.

**New evidence, 2026-08-23** (`DevComms/log_068_dominant_plus_worked_example.md`
§3–§4, dominant `+` on `whole|whole` L1, 98 profiles). Under VALUE the
mode partition is **not a partition at all** — it is a COVER: 39 of 98
profiles sit in 2 to 11 maximal cliques at once, and **7 of the 14
cliques cannot be named** against `wrapping`/`growing`/`approximating`
because their members fit DIFFERENT adds. Under ALL-CELLS every profile
is in exactly one of 30 parts and 23 of them name exactly one add, at
the known cost that `wrapping` appears as 6 parts split by width,
signedness and argument order. This is the one open item that actually
blocked the construction.

</details>

---

### 1.5 a fourth disagreement kind, or not

**What is true.** The classifier ruled in §1.1 sorts a disagreeing cell
into WINDOW (decline against answer) or VALUE (answer against different
answer). A cell can also hold a decline against a DIFFERENT decline.
Across the eighteen gate blocks of `matrices_full_v2/`, **482 pairs
disagree only in that way** and have no kind under the rule as ruled.

Witness: `cpp.% int32_t x int32_t` against `csharp.% int x int` — they
agree at all 71 keys where both answer, and differ only in which
decline they gave at the other 10.

**Needed from the owner:** a third cell kind (and a rule for it), or a ruling
that a decline-vocabulary difference is not a disagreement at all.
Measured in `DevComms/log_069_...md` §7 and `log_070_...md` §4.

---

### 1.6 is WINDOW-only merging transitive?

**What is true.** "WINDOW-only → SAME family" is a PAIRWISE verdict.
Closing it transitively has a measured counterexample: on
`whole|whole` L1 the WINDOW-only components merge `add wrapping`,
`add growing` and `add approximating` into one group of 96 profiles,
in two hops, through `csharp.+ short x short` — a profile whose holder
never reaches its own fracture inside the X set. The two ends clash at
35 value cells when compared directly.

Measured both ways (`DevComms/log_070_dominant_operators_all.md` §5):
by connected component, `whole|whole` L1 gives 61 groups with a largest
of 72; by maximal clique it gives 42,324 — a cover, not a partition.

**Needed from the owner:** component, maximal clique, or pairwise-only. The
identity (CONTRACT) families underneath are unaffected either way and
are what log_070 names.

---

### 1.2 the name for php's mode — ANSWERED 2026-08-23, CLOSED

the owner ruled the name: **`approximating`** ("approximating is fine").
The three guaranteed adds are `wrapping`, `growing`, `approximating`.
The item has moved out of this file, per "how to use this file", into
`Research/dominant_intentions/census_integer.md` (the php third-add
ruling block), with the reasoning attached. Recorded in
`DevComms/log_067_three_relations_alignment.md`.

---

### 1.3 which scoring is THE weight, and at what cut

**What is true.** Every connector in the row graph carries two
weights: exact-match rate, and graded per-element similarity. Both
ride on every connector; the explorer toggles; neither was chosen
(open since log 054, item 4).

For orientation, external connector counts at three cuts:

| cut | value scoring | all scoring |
| --- | --- | --- |
| 0.95 | 287 | 202 |
| 0.85 | 522 | 703 |
| 0.70 | 780 | 1,536 |

**Needed from the owner:** which weight is THE weight, and the cut — or a
ruling that both stay and the explorer's toggle is the answer.

---

### 1.4 how `rust_release` sits in the ontology

**What is true.** rust appears twice: `rust` (debug, panics on
overflow) and `rust_release` (wraps). They are the same language and
the same source text, differing only by build mode — and the
record-both-modes ruling says both are kept.

**What is open.** Whether `rust_release` is its own operator node in
the lattice, or a mode annotation on `rust`'s. Today it is a
separate node, which is why it appears as a distinct member of the
wrap part.

**Needed from the owner:** its place in the ontology. Structural, so it is
his.

**How much turns on it, measured 2026-08-23** (log_068 §6, §8): `rust`
and `rust_release` supply 8 of the 98 `+` profiles on `whole|whole`,
and **3 of the 16 residue singletons** are rust-debug profiles that are
alone only because they panic where their co-members answer.

---

## 2. owed, but blocking nothing

### 2.1 swift and dart carry no `plus`/`minus` rows at L1

Found in log 064, cause not investigated, flagged only. Until it is
explained, any conclusion drawn about those two languages'
arithmetic rests on absent data. **Needed:** whether to investigate
now or defer.

### 2.2 the six unmeasured chunk caps

log 063 raised cpp's chunk cap 2,000 → 8,000 by measuring host g++.
The other six compiled languages kept their existing caps because no
toolchain was available to measure them, and `l3_exec.CHUNK` names
real per-language risks (swift's superlinear type checker;
java/kotlin/c#'s 64KB method limit). **Needed:** whether to measure
them, or leave them until a lane is slow.

### 2.3 python's stall budget beside ruby's

python L2 runs at `PYTHON_STALL_S = 0.5`; ruby's recorded budget is
2.0s. Both are in force. **Needed:** one shared constant, or two
per-language ones — and if two, that fact recorded rather than
implicit.

### 2.4 where the older run products live

17 files under `PseudoCoupHQ/Research/` read from
`SandboxDesign/agent/out/`, which holds 480 products. Airlock's
`out/` is empty by design. Repointing them breaks them against their
own data. **Needed:** whether those products move, are copied, or
the readers keep pointing at the old tree.

### 2.5 whether to retire SandboxDesign

Airlock is derived and working; SandboxDesign is untouched and also
working. The two cannot run at the same time — they share container
names deliberately, which is what keeps migration down to "the
command name changes, nothing else does". **Needed:** retire, or
keep both.

### 2.6 the Airlock public repo, after the leak

Two sub-items, both from log 002 of Airlock's DevComms:

- Whether `DevComms/` belongs in a PUBLIC repo at all. It is clean
  now, and it is also the file class that leaked.
- Whether to delete and recreate the GitHub repo. A force-push makes
  the old commits unreachable but does not guarantee removal:
  unreferenced objects may resolve by hash until GitHub's collection
  runs, forks keep their own objects, and caches are outside anyone's
  control. Deleting and recreating is the only certain removal, and
  it drops stars, watchers, issues and the URL's history with it.

### 2.7 co-project names inside Airlock

`MIGRATING.md` and the logs still name PseudoCoupHQ and four other
projects. They carry no disc layout, but Airlock's own contract says
it should name no project. **Needed:** anonymise them, or accept
bare names as harmless.

---

## 3. the PseudoCoup_v5 ledgerer walk, paused

These are log_017's open questions, in the state the walk left them.

- **q1 — the rust kind map.** 163 rows drafted in log 008; the owner's
  later rulings (coupled, the three constructs, the three form
  buckets) were never applied back to the rows. One ratification pass
  makes it the mapper's data. Until then `mint_node` refuses an
  unmapped `ts_kind` by name.
- **q3 — the macro cluster.** The shape table is unratified (20
  shapes → 83%; a seventh would close most of the residue), the
  kind-one engine's placement beside the mapper is undrawn, and the
  injected sub-address's concrete spelling is unpicked.
- **q5 — pinning and census.** Designed, never ratified: `ts_to_ur`
  as owner of the vendored pinned grammars, the runtime pin check,
  and the census discipline (unknown kind at ingest → refuse, or a
  justified baseline).
- **q6 — what a language pack IS on disk.** Its CONTENTS are ruled;
  its file layout is not.
- **the documentation node.** Doc comments stored as data, emitted
  per-target through that target's comment protocol, possibly
  pointing at a file holding the documentation. Recorded as planned
  in `node`'s CORE; not designed.

---

## how to use this file

Answer any item by number in conversation. Answered items move out of
here and into the record that governs them — a census page, a CORE, a
SUPPORT rule — with the reasoning attached, per §18a. This file is an
index of what is open, never the place a settled thing lives.
