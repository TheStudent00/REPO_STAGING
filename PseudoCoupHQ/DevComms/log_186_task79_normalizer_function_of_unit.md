# log 186 — TASK 79: the layer-5 text made a function of the unit

Date: 2026-09-03. Node: `hq.research.compiler_graph.term.normalize`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_6_term/node_0_3_5_6_3_normalize/CORE_0_3_5_6_3_normalize.md`).
Interpreter of record for every run pasted below:
`/tmp/reconnect_venv/bin/python3` (python 3.13.9, z3 5.1.0, pyvex 9.3.4).

---

# 1. What was done, in plain words

Round 13 measured that the layer-5 text — the one-line printing of a
unit's proved z3 term, which the pool uses as a merge key — was not a
function of the unit. Walking the same 26,594 units a second time
printed a different text for 1,479 of them. Round 14 tried the obvious
repair, measured it insufficient, and left the ruled steps unedited.

This round the rule was changed in its CORE first and then in the code,
and the repair now holds: **three walks in three separate processes,
one of them with the shards and the units inside them deliberately
shuffled, print the same text for 26,594 of 26,594 proved terms.** The
number of distinct texts over that population falls from 1,267 to 850.

Two things were found on the way that are not the repair itself:

- Round 14's repair failed for two nameable reasons, and each was
  priced on one shard: the ordering key left the operator's PARAMETERS
  out (so two reads of different bit ranges tied), and the table of
  commutative operators left the FLOAT operators out (so the float
  units, which are where the instability lived, were never ordered).
- The corrected rule unmakes five pool merges that were FALSE — pairs
  of units that z3 proves answer differently for some register values,
  which the unstable numbering had printed as one text. Six other pairs
  are proved EQUAL and stop sharing a text; those are equalities a text
  rule could only ever have caught by accident.

One flag, not decided here: task 78's corrected destination rule landed
in `ledger.py` while this work ran, and under the ledger as it now
stands 442 of the 26,594 units build no OUT-0 term at all. Section 6
proves that with the two module versions side by side.

---

# 2. The defect, with values in motion

## 2.1 The unit

`c/op_105` is a `c` unit whose answer is a 64-bit value built from two
arrivals: a 64-bit integer register (`seed_rdi`) and a 128-bit vector
register (`seed_xmm0`). Its term converts the integer to a float, adds
it to the float held in the low 32 bits of the vector register, and
puts the result back beside the vector's untouched high half.

## 2.2 What the old rule printed, twice, for that one unit

LITERAL — `Research/op_pipeline/normalize_stability65_printed.txt`
(round 14's measurement, quoted for the record):

```
   first walk : Concat(Extract(63, 32, v1), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))))
   second walk: Concat(Extract(63, 32, v1), fp.to_ieee_bv(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0)))) + fpToFP(Extract(31, 0, v1))))
```

GLOSS: the two arguments of one addition are in the other order. Same
value, different string, same unit, same rule.

## 2.3 Why the order moved

`z3.simplify` chooses an order for a commutative operator's arguments
by the solver's internal node identity — a number assigned when a node
is first created in that process. Sub-terms are shared between units,
so which units were walked earlier decides which sub-term holds the
smaller number. Walk the shards in a different order and the two
arguments swap.

It then reaches the NAMES, because step 3 of the rule renames free
symbols `v0`, `v1`, … in first-met order: when the arguments swap, the
first symbol met swaps with them, and the numbering itself changes.

---

# 3. The repair, with the same values moving through it

## 3.1 The step that was added

The rule gains an ORDERING step, applied bottom-up to the simplified
term: the arguments of a commutative operator are put in a fixed order
by a key computed FROM THE ARGUMENTS THEMSELVES, never from the
solver's node identity.

The key of a sub-term is its own canonical printing:

- the operator's name WITH ITS PARAMETERS — `extract[31,0]`, not
  `extract`;
- the sub-term's sort;
- the keys of its own arguments;
- every free symbol written as its SORT ALONE (`?(_ BitVec 64)`), so
  that no register name decides an order.

A tie — two arguments of identical shape that differ only in which
symbol they read — is broken by the same key with the symbols' own
names, which is a fact of the unit and not of the process.

## 3.2 The step running on `c/op_105`, printed

LITERAL — the trace, run this session against `term.ordering_key`:

```
the fp add node has 3 arguments (the first is the rounding mode)
  argument 0
    printed : RNE()
    shape key: roundNearestTiesToEven:RoundingMode
  argument 1
    printed : fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, seed_rdi))))
    shape key: (to_fp[8,24] (fp.to_ieee_bv (to_fp[8,24] roundNearestTiesToEven:RoundingMode (extract[31,0] ?(_ BitVec 64)))))
  argument 2
    printed : fpToFP(Extract(31, 0, seed_xmm0))
    shape key: (to_fp[8,24] (extract[31,0] ?(_ BitVec 128)))
  the two value arguments in the order the key puts them:
    fpToFP(Extract(31, 0, seed_xmm0))
    fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, seed_rdi))))
final text: Concat(Extract(63, 32, v1), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))))
```

GLOSS, one step at a time:

1. The rounding mode is argument 0 and stays there; only arguments 1
   and 2 may move.
2. Argument 2's key starts `(to_fp[8,24] (extract` and argument 1's
   starts `(to_fp[8,24] (fp.to_ieee_bv`. Comparing those two strings,
   `e` comes before `f`, so argument 2 is placed first — and it is
   placed first no matter what the process built earlier, because
   neither string mentions anything but the two sub-terms.
3. The renaming then meets `seed_xmm0` first and `seed_rdi` second, so
   `v1` is the vector register in every walk.

## 3.3 The code

LITERAL — `Research/op_pipeline/term.py`, `Term.normalize`, the steps
only:

```python
        simplified = z3.simplify(term)
        simplified = order_commutative(simplified)
        symbols = ordered_symbols(simplified)
        substitution = []
        for index, symbol in enumerate(symbols):
            if symbol.sort().kind() == z3.Z3_BV_SORT:
                fresh = z3.BitVec("v%d" % index, symbol.size())
            else:
                fresh = z3.Const("v%d" % index, symbol.sort())
            substitution.append((symbol, fresh))
        if substitution:
            simplified = z3.substitute(simplified, *substitution)
        simplified = z3.simplify(simplified)
        simplified = order_commutative(simplified)
        return one_line(simplified)
```

GLOSS: the ordering runs TWICE — once on the simplified term, and once
after the renaming, because the substitution builds a new term and the
solver orders that new term's commutative arguments by node identity
again. `order_commutative` walks with an explicit stack, so a deep term
cannot exhaust Python's own call stack.

The helpers are `order_commutative`, `ordering_key`, `rebuilt_node`,
`operator_name`, `argument_order`, and the two tables
`COMMUTATIVE_OPERATORS` and `ROUNDED_COMMUTATIVE_OPERATORS`. Nothing
outside `normalize` and those helpers was touched; task 80's
`RenderBack` work in section 5 of the same file was not disturbed.

---

# 4. Why round 14's repair was not enough, priced piece by piece

The measurement walks the `c` shard's 582 proved units forward and then
in reverse inside ONE process, under four printing rules. A rule whose
text is a function of the unit prints the same text both ways.

LITERAL — `Research/op_pipeline/normalize79_cause_printed.txt`:

```
-- THE SHARD
   the `c` shard's units with a proved term 582

-- EACH PRINTING RULE, WALKED FORWARD AND REVERSED IN ONE PROCESS
   as_ruled_before_task79             differs  77 of 582   distinct 259
   order_without_parameters           differs  11 of 582   distinct 239
   order_without_the_float_operators  differs  43 of 582   distinct 242
   the_corrected_rule                 differs   0 of 582   distinct 229

   peak resident size 73 MB, cap 6144 MB
```

GLOSS, and this is the answer to "why did the obvious repair fail":

- **The operator's parameters.** `Extract(63, 0, x)` and
  `Extract(127, 64, x)` read different bits and z3 spells both
  `extract`. With the parameters out of the key those two arguments tie
  and the tie falls back to the order the term arrived in — the node
  identity again. 11 of 582 units still move without them.
- **The float operators.** Round 14's table of commutative operators
  held the bit-vector and boolean ones only. The instability lives in
  the float units, so leaving `fp.add` and `fp.mul` out leaves 43 of
  582 moving (round 14's own probe recorded 39; the two probes key the
  ordering differently, so the counts are close and not the same
  number).
- With both in, 0 of 582 move.

---

# 5. THE ACCEPTANCE TEST

## 5.1 What was run

Three walks, each its OWN process — two walking the shards and the
units inside them in name order, one walking them shuffled with seed
79 — then a comparison, unit by unit, of the three texts. Two walks
inside one process could not measure this defect at all, since they
would share the node-identity counter that causes it.

Population: the 26,594 units whose term the round-13 gate proved, read
off `term65_store`, the same population log_169 measured.

## 5.2 The figure

LITERAL — `Research/op_pipeline/acceptance79_pre78_printed.txt`:

```
-- THE POPULATION
   units with a proved term and a stored layer-5 text 26594
   units walk1 printed  26594  (refused 0)
   units walk2 printed  26594  (refused 0)
   units walk3 printed  26594  (refused 0)

-- THE ACCEPTANCE FIGURE
   units printed by all three walks                 26594
   units whose three texts are IDENTICAL            26594 of 26594
   units whose texts differ between walks           0
   units of the population no walk printed          0

-- THE DISTINCT-TEXT COLLAPSE, over the same 26594 units
   before, the uncorrected rule, one walk (term65_store) 1267
   after,  walk1                                        850
   after,  walk2                                        850
   after,  walk3 (shuffled construction order)          850
   units whose printed text the correction changes      8091
```

GLOSS: **26,594 of 26,594**, no residue, nothing unprinted. The
distinct-text collapse is 1,267 to 850 — and the "before" figure is one
walk's count under the unstable rule, not a property of the corpus
(log_169 measured a second walk producing 1,294). The "after" 850 is
the same 850 in all three walks, which is the point of the exercise.

## 5.3 The unit of section 2, before and after

LITERAL — the same transcript:

```
   unit c/op_105
     before (term65_store, uncorrected rule): Concat(Extract(63, 32, v1), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))))
     after  (walk1):                          Concat(Extract(63, 32, v1), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))))
     after  (walk2):                          Concat(Extract(63, 32, v1), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))))
     after  (walk3, shuffled):                Concat(Extract(63, 32, v1), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))))
   unit c/op_121
     before (term65_store, uncorrected rule): Concat(Extract(63, 32, v0), fp.to_ieee_bv(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v1))) + fpToFP(Extract(31, 0, v0))))
     after  (walk1):                          Concat(Extract(63, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v1)))))
     after  (walk2):                          Concat(Extract(63, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v1)))))
     after  (walk3, shuffled):                Concat(Extract(63, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), v1)))))
```

GLOSS: `c/op_121` is the unit whose NUMBERING swapped between walks in
log_169 §5.2. Its text changes under the correction — the addition's
arguments are now in the key's order — and it is then the same text in
all three walks, shuffled walk included.

## 5.4 The memory bound, stated and met

- STATED before the run: one shard's JSON at a time plus one short text
  per unit; expected peak under 1.5 GB; hard cap 6 GB with the named
  abort `ABORT_MEMORY_CEILING`, checked every 200 units.
- SAMPLED first, under the named interpreter: 2,000 units, 5.4 s, peak
  resident size 82 MB (`--limit 2000`; the sample file was removed
  after reading, it is not an artifact).
- MEASURED on the three pinned walks of section 5.2, `/usr/bin/time -v`:
  `Maximum resident set size` 85,452 kB / 84,760 kB / 90,944 kB — 83 to
  89 MB against the 6,144 MB cap. The three walks against the current
  tree measured 85,480 kB / 85,224 kB / 90,800 kB. The abort never
  fired.

---

# 6. The population moved under the measurement — task 78, flagged

## 6.1 What happened

Task 78's corrected destination rule landed in `ledger.py` at 23:04 to
23:09, while this task's walks were running. Under the ledger as it now
stands, 442 of the 26,594 units build NO OUT-0 TERM at all — 209 `c`
and 233 `cpp`, every one a regenerated unit — so the three walks print
26,152 and the acceptance over the current tree reads 26,152 of 26,152
identical with 442 unprinted.

## 6.2 The proof that it is task 78's change and not the repair

LITERAL — the diff between the two `ledger.py` blobs, the destination
rule for a transfer into the compiler's own runtime:

```
$ git show 88eb36a:Research/op_pipeline/ledger.py | diff - Research/op_pipeline/ledger.py | head
521c521,523
<     "writes": [(ACCUMULATOR, "the runtime routine's answer")],
---
>     "writes": "every register family the ATTACHED CALLEE's own body "
>               "changes, one row per family, read off that body by "
>               "`answer_registers_of_body`",
```

LITERAL — one of the 442 units transcribed twice, with `ledger.py`,
`canonical_form.py` and `reference.py` taken from their blobs of
23:02 in the first run and from the tree in the second:

```
== modules from .../scratchpad/pre78
   out_term built? True
   layer-5 text: v0
== modules from PRIVATE/PseudoCoupHQ/Research/op_pipeline
   out_term built? False
```

GLOSS: the same unit, the same corrected normalizer, the same
interpreter; the only difference is the transcription layer. This is
the ledger node's to answer, not the normalize node's — it is FLAGGED
here and nothing about it was decided or worked around.

## 6.3 Which figure is the acceptance

Both are reported, and both say the corrected rule prints one text per
unit:

| walks against | units printed | identical across the three walks |
|---|---|---|
| the transcription layer pinned to 23:02, which produced `term65_store`'s 26,594 | 26,594 | **26,594 of 26,594** |
| the tree as it now stands, with task 78's rule | 26,152 | 26,152 of 26,152, 442 not transcribed |

The pinned run is the like-for-like comparison — the population the
brief names, and the only one whose "before" texts exist to compare
against.

---

# 7. The prediction task 83 will check

## 7.1 How it is computed, and its control

`pool.py` closes three grounds under transitivity: layer-5 text
identity among proved units, layer-3 wrapped-text identity, and the
proved edges of the cross-unit prover. Only the first changes here. So
the prediction runs those three grounds twice over pool5's own members
— once with pool5's stored texts, once with the corrected walk's — and
compares the two partitions by member sets.

The control matters more than the prediction: with pool5's own texts
the same code must reproduce pool5.

LITERAL — `Research/op_pipeline/normalize79_pool_prediction_printed.txt`:

```
-- THE POOL AS IT STANDS
   entries 1831, members 30432

-- THE CONTROL: the same three grounds over the same members, with pool5's own texts
   groups the control forms                    1831
   pool5's own entry count                     1831
   the control reproduces pool5 member for member  True

-- THE CORRECTED TEXTS
   units of the pool the corrected walk printed 26594
   groups the corrected rule forms              1813
   distinct layer-5 texts, pool5's own          1267
   distinct layer-5 texts, corrected            850

-- THE PREDICTION task 83 will check
   entries before                               1831
   entries after                                1813
   entries that MERGE (two or more become one)  50 entries in 21 joins
   entries that SPLIT (one becomes two or more) 11
   members                                      30432 before, 30432 after
```

GLOSS: **pool5's 1,831 entries become 1,813** — 50 earlier entries
merge in 21 joins, 11 entries split, and no member enters or leaves.
The pool was NOT rebuilt here; task 83 rebuilds it and this is the
number it should find.

## 7.2 Every split's cause, decided by the solver

A split can be a false merge repaired or a real merge lost, and the
difference is decidable: transcribe one member of each group over the
same free symbols and ask z3 whether the two can answer differently.

LITERAL — `Research/op_pipeline/normalize79_split_causes_printed.txt`:

```
-- THE CAUSE, decided by the solver, one comparison per pair of groups
   comparisons whose two sides are PROVED DIFFERENT (a false merge repaired) 5
   comparisons whose two sides are PROVED EQUAL (a real merge lost)      6
   comparisons the solver left undecided                              0
```

### 7.2.1 A false merge repaired

LITERAL — the same file, the pair `c/op_555` and `c/op_663` (20 members
in one pool5 entry), with the texts trimmed to the part that differs:

```
     c/op_555
       new text: If(And(Not(fpEQ(...v0..., ...v1...)), Not(fpToFP(Extract(31, 0, v0)) < fpToFP(Extract(31, 0, v1))), ...
     c/op_663
       new text: If(And(Not(fpEQ(...v0..., ...v1...)), Not(fpToFP(Extract(31, 0, v1)) < fpToFP(Extract(31, 0, v0))), ...
       verdict : PROVED_DIFFERENT
       at      : seed_xmm0 = 612369407; seed_xmm1 = 2055076864
```

GLOSS: both units arrive in `xmm0` and `xmm1`; one answers 1 when the
first is above the second and the other when the second is above the
first. They are different functions of their arrival registers, and z3
prints the register values at which they disagree. The uncorrected rule
gave both ONE text, because the positional numbering followed an
unstable argument order. That merge was false, and the correction
unmakes it — the same class of error the evidence doctrine records for
the lifter's operand anonymization.

### 7.2.2 A merge the text ground stops carrying

LITERAL — the same file, `swift/regen_1000` and `swift/regen_1077`:

```
     swift/regen_1000
       new text: If(Extract(31, 0, v0) == Extract(31, 0, v1), 0, 1) | If(0 <= Extract(15, 0, v0), 0, 1)
     swift/regen_1077
       new text: If(Extract(31, 0, v0) == Extract(31, 0, v1), 0, 1) | If(0 <= Extract(15, 0, v1), 0, 1)
       verdict : PROVED_EQUAL
```

GLOSS, walked through: the second half of each unit reads a DIFFERENT
register — the first unit's low 16 bits of `rdi`, the second unit's low
16 bits of `rsi`. They are nevertheless equal, and the reason is not
syntactic: the second half only decides the answer when the first half
is false, and the first half is false exactly when the low 32 bits of
the two registers agree, which forces their low 16 bits to agree too.
A text rule cannot see that; it merged them before only because the
unstable numbering happened to name both registers `v0`. Six pairs are
of this kind, each a two-member entry. The ground that carries such a
pair is the proved edge, not the text — and the pool already has that
ground.

---

# 8. The standing requirements

## 8.1 The unmodified guard, one process

LITERAL — `Research/op_pipeline/guard79_transcript.txt`:

```
guard79.py -- every JSON artifact task 79 writes, unmodified guard, ONE process.  Nothing was added to any field set, and no artifact was declared out of the walk.

command: /tmp/reconnect_venv/bin/python3 PRIVATE/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py ... (11 paths)

operator inventory: 91 tokens read from probe_manifest_*.json
PASS normalize79_walk_walk1.json -- no operator token in any key, grouping, pairing or row structure
PASS normalize79_walk_walk2.json -- no operator token in any key, grouping, pairing or row structure
PASS normalize79_walk_walk3.json -- no operator token in any key, grouping, pairing or row structure
PASS normalize79_walk_pre78_walk1.json -- no operator token in any key, grouping, pairing or row structure
PASS normalize79_walk_pre78_walk2.json -- no operator token in any key, grouping, pairing or row structure
PASS normalize79_walk_pre78_walk3.json -- no operator token in any key, grouping, pairing or row structure
PASS acceptance79.json -- no operator token in any key, grouping, pairing or row structure
PASS acceptance79_pre78.json -- no operator token in any key, grouping, pairing or row structure
PASS normalize79_pool_prediction.json -- no operator token in any key, grouping, pairing or row structure
PASS normalize79_split_causes.json -- no operator token in any key, grouping, pairing or row structure
PASS normalize79_cause.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ grep -c exempt guard79_transcript.txt
0
```

The guard file itself is unmodified against the tree; nothing was added
to any field set and no artifact was declared out of the walk.

## 8.2 The spelling ban

No operator token appears in any key, grouping, pairing, row structure,
candidate selection or comparison scope in anything this task wrote.
The comparison scope of section 7.2 is the pool's own member sets. The
one place a unit's display label exists in these artifacts is pool5's
own member records, which this task reads and does not re-key.

## 8.3 Evidence class per claim

- The stability figures, the collapse figures and the split causes are
  **forced by construction**: they compare artifacts this task built,
  by comparisons only the fact itself explains, and the solver
  verdicts rest on the transcribed model.
- The z3 verdicts (`PROVED_EQUAL`, `PROVED_DIFFERENT`) are proofs about
  the MODEL of the machine, which is the lifter's testimony.
- The claim that task 78's change causes the 442 refusals is **forced
  by construction**: the same unit, the same normalizer, two module
  versions, printed in section 6.2.

## 8.4 Coding discipline

No compound one-liner statements in any file written this round. The
banned vocabulary does not appear.

---

# 9. Complete file inventory

## 9.1 The plan tree — changed FIRST, with provenance

| file | change |
|---|---|
| `Planning/.../node_0_3_5_6_3_normalize/CORE_0_3_5_6_3_normalize.md` | definition rewritten to the five steps; design's numbered statements gain the ordering step and the second simplification, and the method block gains `order_commutative`; the first settled rule restated; the round-14 correction marked ANSWERED; a new settled rule **THE REPAIR, RULED AND MEASURED** with the priced pieces, the acceptance figure, the population note about task 78, and the merge/split consequence; realization table rewritten |
| `Planning/.../node_0_3_5_6_term/PROGRESS.md` | five entries: the CORE rule change, the acceptance, the piece-by-piece pricing, the pool prediction with its control, and the guard |

## 9.2 The code

| file | change |
|---|---|
| `Research/op_pipeline/term.py` | `Term.normalize` gains the two ordering steps; new module-level helpers `operator_name`, `ordering_key`, `rebuilt_node`, `argument_order`, `order_commutative` and the tables `COMMUTATIVE_OPERATORS`, `ROUNDED_COMMUTATIVE_OPERATORS`. Nothing else in the file was touched |

## 9.3 New files (all in `Research/op_pipeline/`)

| file | what it is |
|---|---|
| `normalize79_walk.py` | one walk of the corrected rule over the proved population, in its own process |
| `normalize79_walk_walk1.json`, `..._walk2.json`, `..._walk3.json` | the three walks against the tree as it now stands |
| `normalize79_walk_pre78_walk1.json`, `..._walk2.json`, `..._walk3.json` | the three walks against the pinned pre-task-78 transcription layer |
| `normalize79_walk1.log`, `normalize79_walk2.log`, `normalize79_walk3.log`, `normalize79_pre78_walk1.log`, `normalize79_pre78_walk2.log`, `normalize79_pre78_walk3.log` | `/usr/bin/time -v` transcripts, with peak resident size |
| `acceptance79.py` | the three-walk comparison |
| `acceptance79.json`, `acceptance79_printed.txt` | the acceptance against the current tree (26,152 of 26,152, 442 unprinted) |
| `acceptance79_pre78.json`, `acceptance79_pre78_printed.txt` | **the acceptance figure: 26,594 of 26,594** |
| `normalize79_cause.py`, `normalize79_cause.json`, `normalize79_cause_printed.txt` | what each piece of the repair is worth, on the `c` shard |
| `normalize79_pool_prediction.py`, `normalize79_pool_prediction.json`, `normalize79_pool_prediction_printed.txt` | the prediction task 83 checks, with its control |
| `normalize79_split_causes.py`, `normalize79_split_causes.json`, `normalize79_split_causes_printed.txt` | every predicted split, its cause decided by the solver |
| `guard79.py`, `guard79.json`, `guard79_transcript.txt` | the unmodified guard over all eleven JSON artifacts, one process |

## 9.4 Not edited, not imported

`layer4*.py`, `layer5.py`, `canon*` and the round-14 probes
(`normalize_order_probe65.py`, `normalize_stability65.py`) are
superseded records: they were read and quoted, never edited and never
imported.

---

# 10. For the coordinator, not decided here

1. **Task 78's landed rule stops 442 previously-transcribing units from
   building an OUT-0 term** (section 6). It belongs to the ledger node.
   Task 83's rebuild will meet it, and the prediction in section 7 is
   computed against the pre-change transcription layer for exactly that
   reason.
2. **The layer-5 text ground can merge units that compute different
   functions of their arrival registers** — five such merges existed in
   pool5 and the correction unmakes them (section 7.2.1). The ground
   merges terms that are equal UP TO a positional renaming of symbols,
   which is weaker than equality as functions of the registers. That is
   the pool node's rule, not this node's; it is flagged, not changed.
