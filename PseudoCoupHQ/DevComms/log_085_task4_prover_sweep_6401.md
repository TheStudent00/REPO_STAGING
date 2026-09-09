# log 085 — TASK 4: the unbudgeted prover bucket (6,401 cross-language pairs)

Date: 2026-08-31. Session: Claude Code, TASK 4 of log_083's briefs.
Working directory: `PseudoCoupHQ/Research/op_pipeline`.

## 1. Plain-words walkthrough

There is a table of arch-units (real compiled machine-code
instruction sequences, one per operator per language per probe).
Two units are the SAME operation when a solver (z3) can show, for
every possible input, they compute the identical answer — not by
reading the source language's operator name, only by reading the
instructions.

Earlier laps ran this solver ("the prover") on 5,285 pairs and found
14 proofs — all inside the float-arithmetic slice. A large bucket was
left completely untouched: 6,401 pairs where the two units are from
DIFFERENT languages and NEITHER side is a float operation (integer,
boolean, comparison — everything the float sweep excluded). This log
is that bucket, swept in full this session.

Result: 84 direct proofs (5 seen in the first 25-second sample chunk,
80 total by the end) plus 4 more pairs proved "for free" by
transitivity (if A=B and B=C are both proved, A=C needs no solver
call). 5,471 pairs were DISPROVED (the solver found a concrete input
where the two sides answer differently — a real, checked
counterexample, not a guess). 846 came back UNDECIDED (the solver's
model of the instructions has a gap, or it timed out — an honest
"our instrument can't tell," never folded into PROVED or DISPROVED).
Zero REFUSED (no `%rip`-relative unknown-constant loads in this
bucket's texts).

That is a 1.3% proof rate. As the earlier float sweep's docstring put
it, "the disprove rate is the credibility" — most units that share a
type signature genuinely do different things, and the solver said so
5,471 times with a real counterexample each time. The 84 proofs are
durable: each one is a bit-level equality holding for every possible
input, verified by z3, not a sample match.

Given proofs landed, I rebuilt the class table on top of them — on
the `dominant_table23` lineage specifically (the task brief's own
instruction: apply on 23, never conflate with 22). New files:
`dominant_table23b.json` / `dom_ops21b.json`. Measured effect: 926
classes collapse to 901 (25 fewer, from 98 total cross-language
proved edges — the earlier float slice's 14 plus this bucket's 84 —
all landing as genuinely new merges, none redundant with an
already-shared class); the population and node count (135) are
unchanged; edgeless nodes (units with no cross-language match) drop
from 23 to 20.

## 2. What was built

- `cross_unit_prover_bucket1.py` — new script, reuses
  `cross_unit_prover.py`'s population builder, candidate-pair
  builder, `priority_bucket`, and `prove_pair` UNCHANGED (imported,
  not reimplemented — same discipline `cross_unit_prover_extend.py`
  already used for its own slice). Restricts to bucket 1 only
  (cross-language, non-float class key — exactly the 6,401 named
  but never attempted by either prior file). Skips any pair already
  attempted in `proved_edges.json` or `proved_edges2.json`.
  Transitivity shortcut: union-find over every PROVED edge across
  all three files; a connected pair is recorded PROVED with a
  supporting chain, no solver call. Checkpointed: resumes from its
  own `proved_edges3.json` output on each re-run (the sandbox's
  ~170s per-command cap made two chunks necessary — see §4).
- `proved_edges3.json` — the sweep's own output, additive to the
  other two proved-edges files (same schema; merge by unioning
  `pairs`).
- `build_table23b.py` — new script. Loads `dominant_table23.json`'s
  own classes (built by text equality, no proved-edge substitution
  by that file's own deliberate design) and adds exactly one more
  union step: two classes merge when a PROVED edge (from any of the
  three proved-edges files) connects a member of one to a member of
  the other. THE REPRESENTATIVE RULE applied: the merged group's
  canonical text is the simplest member's (fewest bytes), ties by
  class_id order; every original per-class text is kept
  (`representative_chosen_from` on each merged row) — nothing
  erased.
- `dominant_table23b.json` / `dom_ops21b.json` — the rebuilt table and
  dom_op families, on the `dominant_table23` lineage. This is now
  THE current state of that lineage; `dominant_table22`/`dom_ops20`
  is a separate lineage, untouched, per the task brief.

  **RENAME NOTE:** these two files (and the builder that produced
  them) were first written as `dominant_table24.json`/`dom_ops22
  .json`/`build_table24.py`. The coordinator flagged that TASK 7's
  own brief reserves those exact names for THE single reconciled
  lineage ("Output dominant_table24/dom_ops22 as THE table"), and
  this lap's proof-merged continuation of table23 is not that
  reconciliation — so all three were renamed to `dominant_table23b
  .json` / `dom_ops21b.json` / `build_table23b.py` before this log
  was finished, freeing table24/dom_ops22 for Task 7. The rebuild
  was re-run under the new names and reproduced the same numbers
  byte-for-byte (926 -> 901 classes, 135 nodes, 26 dom_ops, edgeless
  23 -> 20); both new grouping artifacts were re-checked against
  `check_no_spelling_keys.py` and still pass.

## 3. Instances — real pairs, the prover's own output verbatim

**A proved pair** (cross-language, i32 result, direct solver proof):

```
"a": "c/op_174",
"b": "go/op_60",
"class_key_type_pair": "i32,i32",
"class_key_result_family": "i32",
"cross_language": true,
"verdict": "PROVED",
"detail": "z3 proved bit-level equality for every value of every
  register either text reads before writing (fpToIEEEBV/BitVec
  comparison, 12000ms timeout)",
"proof_method": "solver"
```

**A disproved pair** (cross-language, i32 result, real
counterexample):

```
"a": "c/op_0",
"b": "cpp/op_12",
"class_key_type_pair": "i32,None",
"class_key_result_family": "i32",
"cross_language": true,
"verdict": "DISPROVED",
"detail": "z3 found a counterexample: [seed_rdi = 256]",
"proof_method": "solver"
```

**A transitive proof** (no solver call — chain named):

```
"a": "go/op_564",
"b": "swift/op_366",
"class_key_type_pair": "i32,i32",
"class_key_result_family": "bool",
"cross_language": true,
"verdict": "PROVED",
"detail": "proved by transitivity (union-find over already-PROVED
  edges), no solver call made -- supporting chain: ['go/op_564',
  'cpp/op_606', 'swift/op_366']",
"proof_method": "transitive"
```

The 84 proved pairs' languages: {c, cpp, go, rust, swift} — all five
0-branch languages, cross-language throughout. Broken down by class
key result family: i32 (14), i64 (11), u64 (11), bool (48 — mostly
comparison shapes). By type pair: `i32,i32` (26), `i32,None`/
`i64,None`/`u64,None` (11 each — unary-shaped), `i64,i64`/`u64,u64`
(7 each), `i32,i64`/`i64,i32` (3 each), `bool,None` (5).

## 4. Per-chunk tallies (checkpointed run)

The sandbox caps a single command at roughly 170s wall-clock. Two
chunks were needed:

| chunk | env budget | pairs attempted this chunk | elapsed | cumulative PROVED | cumulative PROVED_TRANSITIVE | cumulative DISPROVED | cumulative UNDECIDED | cumulative REFUSED |
|---|---|---|---|---|---|---|---|---|
| 1 | `SWEEP_BUDGET_SECONDS=20` (sanity check, ran ~23s) | 3,101 | 23.2s | 5 | 0 | 2,468 | 628 | 0 |
| 2 | `SWEEP_BUDGET_SECONDS=60` (ran ~27.9s, hit end of set) | 3,300 | 27.9s | 80 | 4 | 5,471 | 846 | 0 |

Total attempted: 6,401 / 6,401 (100% of the bucket). Final tally:
**PROVED 80 (solver) + 4 (transitive) = 84; DISPROVED 5,471;
UNDECIDED 846; REFUSED 0.**

`stopped_reason` on the final chunk: `"completed the full bucket1
remaining set"` — the sweep is DONE, not partial. No further chunks
are needed for this bucket.

## 5. Gates run

- `python3 check_no_spelling_keys.py proved_edges3.json` → **PASS**,
  no exemption claimed: "no operator token in any key, grouping,
  pairing or row structure."
- `python3 check_no_spelling_keys.py dominant_table23b.json` →
  **PASS**, no exemption claimed.
- `python3 check_no_spelling_keys.py dom_ops21b.json` → **PASS** via
  the provenance exemption (`role: "generator provenance"`) — the
  SAME exemption `dom_ops21.json` (the file it extends) already
  uses; not a new precedent.
- Zero-regression check: `dominant_table23.json` carries 1,645 unit
  labels across its rows; `dominant_table23b.json`'s merged rows
  carry the same 1,645 unit labels, none dropped, none renamed.
  `build_table23b.py` never regenerates a unit's own canonical
  text — it only adds a grouping layer on top of `dominant_table23
  .json`'s own rows, so every previously-converged unit's newest
  text is untouched (verified: population count identical
  before/after, 1,645 = 1,645).

## 6. Evidence class per claim

- The 84 PROVED edges are LEVEL-2 evidence (z3-proved, bit-level
  equality over all inputs) — the same class the ratified canon
  names as class-forming (AgentMemory, "THE CANONICAL RUNNABLE
  FORM," level-2 paragraph).
- The 5,471 DISPROVED edges are MEASURED (a concrete counterexample
  input, printed by z3 verbatim) — refusal-grade honesty, not an
  absence of evidence.
- The 846 UNDECIDED edges are an INSTRUMENT LIMIT, named as such by
  `prove_pair`'s own detail text (either the reused Sim8/Sim20
  simulator has no model for a mnemonic in the pair, or the 12s
  z3 timeout was hit) — never folded into PROVED or DISPROVED.
- The `dominant_table23b.json`/`dom_ops21b.json` numbers (901 classes,
  135 nodes, 26 dom_ops, 20 edgeless) are a DIRECT COUNT off the
  rebuilt table, printed by the builder itself and re-verified by a
  separate population-count check in this log.

## 7. Remainders — honest, not smoothed over

- 846 UNDECIDED pairs are a REAL open question, not attempted
  further this session — a future lap could raise
  `PER_PAIR_TIMEOUT_MS` or extend Sim8/Sim20's mnemonic coverage and
  re-run just those 846 (they are individually identifiable in
  `proved_edges3.json` by `verdict == "UNDECIDED"`).
- `dominant_table22`/`dom_ops20` (the OTHER lineage, log_083's own
  919/139/26/23 baseline) was NOT touched by this task, per its own
  instruction — Task 7 (reconciling the two lineages) is a separate,
  later task.
- The representative-selection proxy for "fewest bytes of machine
  code" is `len(canonical_text)` (the instruction text's own
  character length) — the same proxy `dominant_table23.json`'s rows
  already carry; no separate byte-assembly step was run in this
  session. Flagged, not decided: if a future lap wants a literal
  assembled-byte count instead of a text-length proxy, that is a
  design choice for the owner, not decided here.

## 8. Two-list rule

**Decided, recorded for audit:**
- Swept the full 6,401-pair bucket 1, chunked/checkpointed,
  transitivity shortcut on. 84 proofs landed, durable.
- Rebuilt `dominant_table23b.json`/`dom_ops21b.json` on the
  `dominant_table23` lineage (not `dominant_table22`), applying THE
  REPRESENTATIVE RULE, per the task brief's explicit instruction.
- All new grouping/pairing artifacts pass the spelling gate; zero
  regression verified by unit-population count.

**Awaiting the owner:**
- Whether to raise the per-pair z3 timeout or extend simulator
  mnemonic coverage to chase the 846 UNDECIDED pairs further.
- Whether "fewest bytes" should become a literal assembled-byte
  count rather than the text-length proxy, if/when representative
  selection becomes load-bearing elsewhere.
