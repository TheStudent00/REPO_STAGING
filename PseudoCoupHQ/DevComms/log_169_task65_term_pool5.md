# log 169 — task 65: term, pool, census on the round-13 gate

Date: 2026-09-03. Nodes: `node_0_3_5_6_term` (with `transcribe`,
`normalize`, `census`, `render_back`) and `node_0_3_5_7_pool` (with
`entry`, `merge_grounds`, `representative`, `families`,
`exception_families`), under
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/`.

Population line, said once and carried on every figure below: **the
30,432 arch-units canon39 records as `WRAPPED_TEXT_PROVED`**, split
1,763 original / 9 interpreter / 28,660 regenerated. The 646 units
canon39 refused have no wrapped text and are not transcribed.

Gate of record for this round: **task 64** (`regate64_store/`, log_168).

---

# 0. What was done, in plain words before any figure

- The term walk was re-run over all 30,432 units with the round-13
  `reference.py` — the one that follows branches and steps into an
  attached runtime callee. Task 64's verdicts were CARRIED, not
  re-derived, because task 64 is this round's gate of record and
  re-asking the same solver the same question is not evidence.
- What term65 added on top of them is what the pool and the census
  need: the transcription detail (holes, cascades, slot
  disagreements) and, for a proved term only, the layer-5 normalized
  text.
- The four states reproduce **exactly**, per population, with the
  consistency line at 0.
- The census was rebuilt (`name_census6`) and its delta taken against
  census5 on the reason sentence.
- The pool was rebuilt on three grounds (`the_pool5`), with families,
  exception families, and a delta against pool4 whose every split and
  merge carries a computed cause.
- **Two findings came out of the delta.** The first is the one the
  brief predicted: entries that were resting on a layer-5 key task 64
  has since withdrawn come apart. The second was not predicted and is
  the more serious of the two: **the layer-5 text is not a function
  of the unit** — a second walk of the same rule over the same units
  prints a different text for 1,479 of 26,594. It is written into the
  normalize CORE as a correction and planned for round 14; the ruled
  rule was NOT edited on a partial fix.

---

# 1. The term run

## 1.1 What was reused and what was re-derived, said mechanically

LITERAL — `term65_run.py`, the paragraph that states it:

```
2. THE VERDICT IS NOT RE-DERIVED.  Task 64 is the GATE OF RECORD for
   this round: `regate64_store/` already holds, per unit, the ship-route
   verdict, the text-route verdict, the outcome, the route and the
   reason, produced by the same `gate.py` over the same reference.
   This run READS that verdict and re-derives only what term65 adds --
   the transcription detail the census needs (holes, cascades, slot
   disagreements) and, for a PROVED term, the layer-5 normalized text.
```

GLOSS: `term65_run.py` walks each unit's ledger itself (it must, to
get the holes the census filters and the term the normalizer prints),
then takes `proved` / `outcome` / `route` / `reason` off task 64's
record for that unit rather than calling the gate again. Where a unit
has no banked record it gates it here and says so in
`verdict_source`; that path was never taken.

## 1.2 The check that makes the reuse honest

Reusing a verdict is only sound if this run's transcription agrees
with task 64's about whether the unit has a term at all. Every record
carries that comparison.

LITERAL — `audit65_printed.txt`:

```
-- WHY they reproduce, said mechanically rather than claimed
   verdicts carried from the gate of record  30432
   verdicts gated by this run                0
   units where this run's transcription and task 64's disagree about whether a term exists  0
```

## 1.3 The four states, per arrival population

LITERAL — `audit65_printed.txt`:

```
   population     state         task 64    term65    move
   original       proved           1665      1665      +0
   original       disproved          49        49      +0
   original       undecided          14        14      +0
   original       no term            35        35      +0
   interpreter    proved              9         9      +0
   interpreter    disproved           0         0      +0
   interpreter    undecided           0         0      +0
   interpreter    no term             0         0      +0
   regenerated    proved          24920     24920      +0
   regenerated    disproved        3085      3085      +0
   regenerated    undecided         271       271      +0
   regenerated    no term           384       384      +0

   ALL            proved          26594     26594      +0
   ALL            disproved        3134      3134      +0
   ALL            undecided         285       285      +0
   ALL            no term           419       419      +0
   ALL            TOTAL           30432     30432

   the brief's line from task 64: 26,594 proved / 3,134 disproved / 285 undecided / 419 no term over 30,432
   term65 reproduces:            26594 / 3134 / 285 / 419 over 30432
   states that differ from task 64: 0
```

GLOSS: **zero differences**, so there is no finding to report here.
The brief asked that any difference be a finding with its cause;
there is none.

## 1.4 The consistency line

LITERAL — `audit65_printed.txt`:

```
   units proved on one route and disproved on the other: 0
```

## 1.5 Layer 5

LITERAL — `audit65_printed.txt`:

```
   proved terms                       26594
   of them, a normalized text exists  26594
   of them, normalization refused     0
   distinct layer-5 texts             1267
```

## 1.6 The 3,134 disproved, carried with their cause

The disproved are NOT dropped and NOT layer-5 eligible: a term that
does not prove is withdrawn, not kept as a weaker key, so each enters
the pool as a member that cannot merge on layer 5 and carries its
reason.

The bucketing test is machine form: does the body transfer, did the
ledger make a `runtime_callee` row for the transfer, and what SHAPE is
the transfer's target — a positional label, a named routine, or an
indirect read through memory. No name we chose and no token enters it.

LITERAL — `audit65_printed.txt`:

```
     2860  log_168 section 5.3: the body transfers into a routine the toolchain's archive defines and canon39's ledger carries no row for it, so the stored term asserts the transfer changed nothing.  FIX PLANNED ROUND 14 -- the canon rebuild with the archive index's own runtime set.
      259  the body does not transfer and the walk left a hole; the disproof has another cause
       13  the body transfers to a NAMED routine that is not a lowering -- a panic or abort path reached on a guard, so the disproof is about the guard's response, not about a missing runtime row
        2  the body transfers INDIRECTLY through memory, so the target is not statically named and no runtime row could be made for it
```

GLOSS, and how it joins log_168's own figure. log_168 §5.3 measured
**2,862** units for its cause, partitioned by which state each unit
moved OUT of (2,860 out of undecided, 2 out of no-term). This table
partitions differently — by the SHAPE of the transfer's target — and
its first and fourth rows sum to **2,860 + 2 = 2,862**. The two
partitions agree on the total; the identity of the members was not
checked member by member, and the agreement is stated as a total, not
as a claim about which units they are. The 13 that transfer to a named
panic path and the 259 with a hole are separated out here rather than
folded in, because they are different facts and the round-14 canon
rebuild will not touch them.

---

# 2. The census

## 2.1 The tally

LITERAL — `name_census6_printed.txt`:

```
-- the census over canon39
   producers 49
   rows blocked 1637
   units blocked 1185
   cascades (not census entries) 686
```

against census5's **52 producers, 1,877 rows**.

## 2.2 The delta, matched on the reason sentence

The census CORE's rule is that comparison between rounds is grouped on
the recorded REASON SENTENCE, never on a producer's spelling.

LITERAL — `name_census6_printed.txt`, the head of each list:

```
   causes CLOSED 27
       -164 rows | arch opcode 'jae' is a census row, not a silent gap: a transfer or trap, and this reference walks a body in text order
       -425 rows | arch opcode 'js' is a census row, not a silent gap: a transfer or trap, and this reference walks a body in text order
       -154 rows | the shared opcode table refused: an address computation over base register '%rip': this reference has no model for the address that register holds, only for the value a read through it returns
       -88 rows | the shared opcode table refused: a division at width 16 is not modeled
       -88 rows | the shared opcode table refused: a division at width 8 is not modeled
       -9 rows | the shared opcode table refused: operand '%ah' is neither an immediate, a register nor a memory operand this file reads
       -74 rows | the attached body of the runtime callee '__divti3' spells 'endbr64', which the shared opcode table refused: arch opcode 'endbr64' has no entry in the opcode table -- no body in the corpus this table was built over spells it
   causes APPEARED 11
       +1174 rows | this row names no place its value resides, and its body line names no destination register
       +77 rows | the attached body of the runtime callee '__udivti3' spells '', which the shared opcode table refused: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read
       +73 rows | the attached body of the runtime callee '__divti3' spells '', which the shared opcode table refused: this body's control flow has a cycle (a transfer back to a block already on the walk), and no loop invariant is invented here
   causes that MOVED 1
       2 -> 15 | the shared opcode table refused: this opcode reads the signed-overflow bit and no flag-setting arch opcode precedes it in this body
```

(the full 27 / 11 / 1 are in the artifact)

GLOSS, in three statements:

- **What closed is exactly what tasks 63 and 64 fixed.** Every
  conditional-transfer opcode closes because the reference now walks a
  body as a graph rather than in text order. `endbr64` closes because
  task 63 added it to the opcode table. The rip-relative address, the
  8- and 16-bit divisions, the widening multiplies and the high-byte
  operand close because task 64 modelled them.
- **What appeared was behind them.** The largest new cause, 1,174
  rows, is a flag-pair row that names no place its value resides — the
  walk now reaches those rows, so they can block; before, it stopped
  earlier. The four runtime callees appear with a NEW reason: the walk
  now enters their bodies and finds a control-flow cycle (or a body
  every path of which leaves the unit), where before it refused at
  `endbr64` and never got that far.
- **The row sums do not add up to the tallies, by construction.** A
  reason sentence can be shared by several producers, so the
  per-reason sums double-count. The authoritative totals are the
  tally block in §2.1.

---

# 3. The pool

## 3.1 The two pools side by side

LITERAL — `pool_delta65_printed.txt`:

```
   quantity                                                pool4    pool5
   entries                                                  1961     1831
   members                                                 30432    30432
   entries_spanning_more_than_one_language                   573      490
   entries_spanning_compiled_and_interpreted                   3        3
   entries_under_the_brief_strict_rule                      5668     5095
   entries_carrying_more_than_one_wrapped_text               480      527
   distinct_layer3_wrapped_texts                            2993     2993
   distinct_layer5_texts_among_eligible_units               1286     1267
   layer3_identity_merges                                  27439    27439
   layer5_identity_merges                                  24754    25327
   proved_edges_applied                                      118      118
   members_with_a_proved_term                              26040    26594
   members_whose_term_was_withdrawn                            0     3134
   members_whose_term_was_undecided                         3865      285
   members_with_no_term                                      527      419
   members_not_layer5_eligible                              4392     3838
   families                                                   34       34
```

The brief-strict count — what the pool would be on layer-5 identity
and proved edges alone — is **5,095**, recorded on the artifact as
`summary.entries_under_the_brief_strict_rule` and used for nothing.

## 3.2 The delta: 35 splits, 89 merges

LITERAL — `pool65_run.log`:

```
   splits 35, merges 89, units gone 0, units new 0
```

## 3.3 THE FINDING THE BRIEF ASKED FOR: merges resting on a withdrawn key

The brief's question, restated: how many pool4 merges rested on a
layer-5 identity that task 64 has since DISPROVED?

The machine-form test, stated before it is applied — LITERAL,
`pool_delta65.py`:

```
  a pool4 member LOST ITS KEY when its record in pool4 says
  `layer5_merge_eligible` true and its record in `term65_store` says
  the term was DISPROVED.  Nothing about a token, a name or an
  operator enters the test.
```

LITERAL — `pool_delta65_printed.txt`:

```
-- THE MEMBERS THAT LOST THEIR LAYER-5 KEY
   pool4 members that were layer-5 eligible and whose term task 64 DISPROVED   233
   pool4 members that were NOT layer-5 eligible and whose term task 64 PROVED  801

-- THE SPLITS: 35, and how many rest on a withdrawn layer-5 key
   splits containing at least one member that lost its layer-5 key   26
   withdrawn-key members inside those splits                        155
   splits with NO such member                                       9

-- THE MERGES: 89, and how many rest on a layer-5 key task 64 GAVE
   merges containing at least one member that GAINED a layer-5 key   74
   newly-keyed members inside those merges                          756
   merges with NO such member                                       15
```

GLOSS, and the number that must not be misread: **233, not 3,134.**
Task 64 disproved 3,134 terms, but most of those units were UNDECIDED
under the round-12 gate and therefore already had no layer-5 key —
nothing they held together can come apart. The 233 are the ones that
DID hold a key and lost it. **26 of the 35 splits contain at least
one of them**, and those splits are the finding: the entry was resting
on evidence that has since been refuted, and it comes apart correctly.

## 3.4 Why the pool got SMALLER while 3,134 keys were withdrawn

LITERAL — `pool_delta65_printed.txt`:

```
   of the 233 members that LOST a layer-5 key, the entry's member set is
       unchanged (the layer-3 text still joins them) 78
       changed  (the entry came apart)               155
   of the 801 members that GAINED a layer-5 key, the entry's member set is
       unchanged (the new key joined nothing new)    45
       changed  (the new key joined an entry)        756
   layer-5 identity merges  pool4 24754 -> pool5 25327  (+573)
```

GLOSS: the two movements pull opposite ways and the second is larger.
78 of the 233 withdrawals cost nothing because those members' layer-3
text still joins them to the same entry; 756 of the 801 new keys
actually joined an entry that the text alone did not reach. Net: 1,961
entries become 1,831.

## 3.5 E00029's successor, printed

Found by MEMBER SET, never by number, so a renumbering is not read as
a change.

LITERAL — `pool_delta65_printed.txt`:

```
   pool4 E00029: 158 members, 7 languages, representative go/op_319
   pool5 successor E00029: 166 members, 8 languages, representative go/op_319
   members shared with pool4 E00029: 158
   members pool4 E00029 had that the successor does not: 0
   members the successor has that pool4 E00029 did not: 8
```

LITERAL — `the_pool5_entry_E00029_successor_printed.txt`, one member
and one of the entry's cross-language grounds:

```
{
 "arrival_annotation": "plain",
 "lang": "c",
 "layer5_merge_eligibility_reason": "the layer-4 term was proved equal to this unit's own machine code, so its layer-5 text is proved evidence",
 "layer5_merge_eligible": true,
 "layer5_normalized_text": "v0 + v1",
 "operator": "+",
 "out_row": "OUT-0",
 "population": "original",
 "result_width": 64,
 "term_outcome": "PROVED_ON_SHIP",
 "term_state": "TERM",
 "unit": "c/op_109",
 "wrapped_text": "mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi; mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi; lea (%rdi,%rsi,1),%rax; mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret"
}
```

```
  {
   "detail": "these members carry the SAME wrapped text, character for character -- the same machine code twice",
   "ground": "layer-3 text identity",
   "languages_it_joins": ["php", "ruby"],
   "wrapped_text": "mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi; mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi; mov %rdi,%rax; add %rsi,%rax; mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret"
  }
```

GLOSS: the entry's members by language are c 68, cpp 68, go 7, rust 8,
**swift 8**, cpython 1, php 4, ruby 2 — swift is the eighth language,
and it is new this round. `operator` is a display label on the member
and is read by nothing.

## 3.6 Families and exception families

LITERAL — `pool65_run.log`:

```
-- the families (the dom_op rule, imported from dom_ops.py)
   nodes (language, grammar-operator, arity) 197
   cross-language edges, raw 1334
   edges surviving the mutual filter 345
   families 34
```

```
-- the exception families, rebuilt over this pool
   guard rows read 314
   rows considered 128
   rows excluded (continue-with-a-different-answer) 186
   rows about units outside this pool 0
   exception families 40
```

GLOSS: the dom_op rule is imported unchanged from `dom_ops.py`, so it
cannot drift between builds. **34 families over 197 nodes**, the same
counts as pool4's build (also 34 / 197), over a pool with 130 fewer
entries. The raw cross-language edge count moved — 1,014 in pool4's
build, **1,334** here — and the mutual filter kept more of them (322
-> **345**), but the connected components still number 34.
The exception families take the next free number
(`exception_families5.json`) because a superseded record is never
edited.

## 3.7 The representative rule

LITERAL — `pool65_run.log`:

```
   entries carrying more than one wrapped text 527
   distinct texts to assemble 1689
   texts newly assembled 288, would not assemble 120, cache holds 1800
```

GLOSS: bytes are MEASURED with `as --64` then `objdump -d`, never
estimated; a text that will not assemble falls back to character
length with the substitution written on the entry rather than hidden.

---

# 4. The collapse, layer 5 against layer 3, per population

LITERAL — `collapse65_printed.txt`:

```
-- THE COLLAPSE, over the units that HAVE a layer-5 text
   population      units  L5 text  L3 text   L3 all    L5 x    L3 x
   original         1665      404      618      657     4.1     2.7
   interpreter         9        3        7        7     3.0     1.3
   regenerated     24920     1219     2010     2972    20.4    12.4
   ALL             26594     1267     2023     2993    21.0    13.1

-- TASK 66's RENDERED TEXT, beside them, over the units it reached
   population      units   render  L5 text  L3 text     R x
   original          371       55       33       59     6.7
   interpreter         8        2        2        6     4.0
   regenerated      5499      102       38      158    53.9
   ALL              5878      102       38      164    57.6
```

GLOSS, with every population named:

- The first block counts over the **26,594 units with a proved layer-5
  text**. Those units carry 2,023 distinct wrapped texts and print
  1,267 distinct normalized terms — layer 5 collapses them 21.0-fold,
  layer 3 13.1-fold. `L3 all` (2,993) is the wrapped-text count over
  the whole 30,432, printed beside it so the two are not confused.
- The second block counts over the **5,878 units task 66 rendered
  back** — a subset of the proved set, not the whole. Over exactly
  those units the ordering is **38 layer-5 texts < 102 rendered texts
  < 164 layer-3 texts**: the return path's text collapses further than
  the compilers' own text and less than the key, which is what a
  fixed-rule re-render should do.

---

# 5. THE SECOND FINDING: the layer-5 text is not a function of the unit

This was not predicted by the brief. It came out of reading the nine
splits that §3.3's test could not explain.

## 5.1 Where it showed up

Nine of the 35 splits contain no member that lost its layer-5 key.
Reading their members' texts side by side, the whole difference is the
ORDER of the arguments of one commutative operator.

LITERAL — the two texts pool5 printed for `c/regen_16844` and
`c/regen_16900`, which pool4 had in one entry, differing only inside
one `Or`:

```
... If(Or(Not(fpEQ(fpToFP(Extract(31, 0, v0)), +0.0)),
          fpIsNaN(fpToFP(Extract(31, 0, v0)))), 1, 0) ...

... If(Or(fpIsNaN(fpToFP(Extract(31, 0, v0))),
          Not(fpEQ(fpToFP(Extract(31, 0, v0)), +0.0))), 1, 0) ...
```

GLOSS: `Or(p, q)` and `Or(q, p)` are the same value. Two units
computing the same thing printed different strings, which is exactly
what the normalize CORE's definition says the rule exists to prevent.

## 5.2 Values in motion: the same unit, walked twice

The defect is not between two units. It is between two walks of the
SAME unit.

LITERAL — `normalize_stability65_printed.txt`, `c/op_105`:

```
   first walk : Concat(Extract(63, 32, v1), fp.to_ieee_bv(fpToFP(Extract(31, 0, v1)) + fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0))))))
   second walk: Concat(Extract(63, 32, v1), fp.to_ieee_bv(fpToFP(fp.to_ieee_bv(fpToFP(RNE(), Extract(31, 0, v0)))) + fpToFP(Extract(31, 0, v1))))
```

Walk it through, one step at a time:

1. The unit's ledger is transcribed to a z3 term. Same ledger, same
   builders, same term both times.
2. `z3.simplify` runs. For the `+` node it must choose an order for
   its two arguments, and it chooses by the solver's INTERNAL NODE
   IDENTITY — a number the solver assigns when a node is first
   created. That number depends on **what the process built before**,
   which is a different set of terms in the two runs.
3. So walk one puts `fpToFP(Extract(31, 0, v1))` first and walk two
   puts `fpToFP(fp.to_ieee_bv(...))` first. Same value; different
   string.
4. It then propagates into the NAMES. Step 2 of the rule renames free
   symbols `v0`, `v1`, … in FIRST-MET order. When the argument order
   moves, the first symbol met moves with it. LITERAL, `c/op_121`,
   the same two walks:

   ```
   first walk : Concat(Extract(63, 32, v0), ... v1 ...)
   second walk: Concat(Extract(63, 32, v1), ... v0 ...)
   ```

   The numbering itself swapped.

## 5.3 How big it is

LITERAL — `normalize_stability65_printed.txt`:

```
-- THE INSTABILITY, over the whole population
   units whose text DIFFERS between the two walks   1479
   as a share of the units walked                   5.6%
   distinct texts, first walk (term65_store)        1267
   distinct texts, second walk                      1294

   by language
       c             525
       cpp           916
       go             13
       rust           10
       swift          15
```

GLOSS: over the 26,594 units with a proved term, **1,479 (5.6%)**
print a different layer-5 text on a second walk of the same rule. It
is concentrated in c and cpp, which is where the float units are. The
consequence for this round's figures is stated plainly: the pool's
layer-5 merge ground carries this noise, and the 1,267 distinct texts
in §1.5 are one walk's count, not a property of the corpus.

## 5.4 The partial repair was tried, MEASURED, and NOT shipped

The obvious repair is a further printing step: put the arguments of a
commutative operator in a fixed order that depends only on the
arguments themselves. It was implemented in a probe that changes
nothing (`normalize_order_probe65.py`) and measured.

LITERAL — `normalize_order_probe65_printed.txt`:

```
-- DISTINCT LAYER-5 TEXTS, the rule as it stands beside the rule with the step
   as ruled (simplify, rename, print)        1292
   with the arguments of a commutative       993
     operator sorted by their printed text
   texts the step collapses                  299
   units whose printed text the step changes 10850
```

and, applying the step BEFORE the renaming (so the numbering is fixed
too) and re-walking the `c` shard in forward and reversed order:

```
units: 582   differ between forward and reversed order: 39
distinct texts (corrected rule): 248
distinct texts (rule as it stands, from the store): 264
```

GLOSS, and the decision: the step helps a great deal — 299 of 1,292
texts collapse — but it **does not make the key a function of the
unit**: 39 of 582 `c` units still print differently when the walk
order is reversed. A repair that does not achieve the rule's stated
purpose is not the repair. So the ruled three steps were NOT edited
on it. The correction is written into the normalize CORE as a settled
correction with its provenance, and the fix is **planned, round 14**.

This is a flag, not a redesign: the round's figures are reported as
measured, with the defect named on them.

## 5.5 Recorded honestly

Like log_168 §5.3's correction, this one was written into the CORE
AFTER the measurement that produced it, which is the reverse of the
binding rule's order. It could not have gone first — it was not known
until the pool delta was read. It is a finding of the run, not a
shape the work needed in advance.

---

# 6. The standing requirements

## 6.1 The unmodified guard, one process

The guard file was not edited. LITERAL:

```
$ git -C ~/Programming/PseudoCoupHQ status --porcelain Research/op_pipeline/check_no_spelling_keys.py
(no output)
$ md5sum check_no_spelling_keys.py
1d6aba67cbcdb021c3bdfd7f40fd2020  check_no_spelling_keys.py
```

`guard65.py` runs it as ONE separate process over every artifact this
task writes, adding nothing to any field set and declaring no
exemption. LITERAL:

```
$ python3 guard65.py
TASK 65: 343 paths  PASS 343  FAIL 0  exempt 0  exit 0
EXIT=0
$ grep -c exempt guard65_transcript.txt
0
```

LITERAL — head of `guard65_transcript.txt`:

```
guard65.py -- every artifact task 65 writes, unmodified guard, ONE process.  Nothing was added to any field set, and no artifact was declared out of the walk.
$ python3 check_no_spelling_keys.py <343 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
PASS audit65.json -- no operator token in any key, grouping, pairing or row structure
PASS name_census6.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool5.json -- no operator token in any key, grouping, pairing or row structure
```

## 6.2 One process

Every run in this task is a single interpreter with no worker pool:
`term65_run.py`, `audit65.py`, `name_census6.py`, `pool65_run.py`,
`pool_delta65.py`, `collapse65.py`, `normalize_order_probe65.py`,
`normalize_stability65.py`, `guard65.py`. `term65_run.py` is resumable
through `term65_state.json`.

## 6.3 Which files were edited rather than added

**None of the round's live modules were edited.** LITERAL:

```
$ git -C ~/Programming/PseudoCoupHQ status --porcelain Research/op_pipeline/term.py Research/op_pipeline/pool.py Research/op_pipeline/gate.py Research/op_pipeline/reference.py
(no output)
```

`term.py` and `pool.py` were available to be edited where a fix was
needed. §5 is the one place a fix was indicated, and the measurement
showed the available fix insufficient, so the ruled rule was left as
it is and the correction went into the tree instead.

Plan files edited: the ten PROGRESS files and ten COREs of §7.3.

## 6.4 The spelling ban

No operator token appears in any key, grouping, pairing, row structure,
candidate selection or comparison scope of anything this task wrote.
`operator` on a pool member and `label` on a family node are display
fields read by nothing; the check above is the mechanical proof.

---

# 7. File inventory

## 7.1 Written by this task — code

| file | what it is |
|---|---|
| `term65_run.py` | the term/normalize run over canon39 on task 64's verdicts |
| `audit65.py` | the four states per population, consistency, layer-5 tally, disproved causes |
| `name_census6.py` | the census over `term65_store`, delta vs census5 |
| `pool65_run.py` | the pool, families, exception families, delta vs pool4 |
| `pool_delta65.py` | the delta read for its cause; E00029's successor |
| `collapse65.py` | the layer-5 / layer-3 / rendered collapse per population |
| `normalize_order_probe65.py` | MEASUREMENT of the partial repair; changes nothing |
| `normalize_stability65.py` | MEASUREMENT of the layer-5 instability; changes nothing |
| `guard65.py` | the unmodified guard over every artifact, one process |

## 7.2 Written by this task — artifacts

| file | what it is |
|---|---|
| `term65_store/` (332 shards, 42 MB) | one layer-4 / layer-5 record per unit, 30,432 |
| `term65_state.json` | resume state for `term65_run.py` |
| `term65_run.log` | the run transcript |
| `audit65.json`, `audit65_printed.txt` | the four states, consistency, causes |
| `name_census6.json`, `name_census6_printed.txt` | the census and its delta |
| `the_pool5.json` (33 MB) | 1,831 entries / 30,432 members |
| `the_pool5_bytes.json` | the measured assembled bytes |
| `the_families5.json` | 34 families / 197 nodes |
| `exception_families5.json` | 40 exception families over pool5 |
| `pool4_pool5_delta.json` | 35 splits, 89 merges, every cause computed |
| `pool_delta65.json`, `pool_delta65_printed.txt` | the delta read for its cause |
| `the_pool5_entry_E00029_successor_printed.txt` | E00029's successor, verbatim |
| `collapse65.json`, `collapse65_printed.txt` | the collapse per population |
| `normalize_order_probe65.json`, `normalize_order_probe65_printed.txt`, `normalize_order_probe65_run.log` | the partial-repair measurement |
| `normalize_stability65.json`, `normalize_stability65_printed.txt`, `normalize_stability65_run.log` | the instability measurement |
| `pool65_run.log` | the pool run transcript |
| `guard65.json`, `guard65_transcript.txt` | the guard result and its transcript |

All under `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

## 7.3 Plan files touched

Under
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/`:

PROGRESS (all ten):

- `node_0_3_5_6_term/PROGRESS.md`
- `node_0_3_5_6_term/node_0_3_5_6_2_transcribe/PROGRESS.md`
- `node_0_3_5_6_term/node_0_3_5_6_3_normalize/PROGRESS.md`
- `node_0_3_5_6_term/node_0_3_5_6_4_census/PROGRESS.md`
- `node_0_3_5_6_term/node_0_3_5_6_5_render_back/PROGRESS.md`
- `node_0_3_5_7_pool/PROGRESS.md`
- `node_0_3_5_7_pool/node_0_3_5_7_1_entry/PROGRESS.md`
- `node_0_3_5_7_pool/node_0_3_5_7_2_merge_grounds/PROGRESS.md`
- `node_0_3_5_7_pool/node_0_3_5_7_4_representative/PROGRESS.md`
- `node_0_3_5_7_pool/node_0_3_5_7_5_families/PROGRESS.md`
- `node_0_3_5_7_pool/node_0_3_5_7_6_exception_families/PROGRESS.md`

COREs — realization tables extended with the round-13 files:

- `node_0_3_5_6_term/CORE_0_3_5_6_term.md`
- `node_0_3_5_6_term/node_0_3_5_6_2_transcribe/CORE_0_3_5_6_2_transcribe.md`
- `node_0_3_5_6_term/node_0_3_5_6_4_census/CORE_0_3_5_6_4_census.md`
- `node_0_3_5_7_pool/CORE_0_3_5_7_pool.md`
- `node_0_3_5_7_pool/node_0_3_5_7_1_entry/CORE_0_3_5_7_1_entry.md`
- `node_0_3_5_7_pool/node_0_3_5_7_2_merge_grounds/CORE_0_3_5_7_2_merge_grounds.md`
- `node_0_3_5_7_pool/node_0_3_5_7_4_representative/CORE_0_3_5_7_4_representative.md`
- `node_0_3_5_7_pool/node_0_3_5_7_5_families/CORE_0_3_5_7_5_families.md`
- `node_0_3_5_7_pool/node_0_3_5_7_6_exception_families/CORE_0_3_5_7_6_exception_families.md`

CORE — a settled correction added, not only a realization row:

- `node_0_3_5_6_term/node_0_3_5_6_3_normalize/CORE_0_3_5_6_3_normalize.md`
  — §5's finding, with its provenance and its round-14 plan.

---

# 8. Resume state

Nothing is part-done. Every run in §7.1 completed and wrote its
artifacts; `term65_state.json` lists all 332 shards as done. There is
no partial store, no partial pool, and no half-written plan file.

If work resumes on this line, the two live items are:

1. **The canon rebuild with the archive index's own runtime set**
   (log_168 §5.3, planned round 14). It is what turns 2,862 of the
   3,134 disproofs into proofs. Until it happens, pool5 should be read
   as covering the units whose bodies do not transfer into the
   compiler's own runtime.
2. **The normalize repair** (§5, planned round 14). The layer-5 key
   must become a function of the unit alone. The measured starting
   point is in `normalize_order_probe65.json` and
   `normalize_stability65.json`; the partial fix is necessary and not
   sufficient, and the remaining 39-of-582 residue on the `c` shard is
   where the next measurement should start.

# 9. Open calls for the owner

None. Everything decided here was decided against the tree or against
AgentMemory.
