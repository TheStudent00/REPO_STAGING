---
id: hq.research.compiler_graph.term.normalize
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), rule
node:
    name: normalize
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_6_term/node_0_3_1_6_3_normalize/CORE_0_3_1_6_3_normalize.md
super_node:
    name: term
    path: ../CORE_0_3_1_6_term.md
sub_nodes: []
---

# CORE 0_3_1_6_3 — normalize

## metadata

- **id:** hq.research.compiler_graph.term.normalize
- **level:** 4
- **status:** draft
- **designation:** code (method), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [term](../CORE_0_3_1_6_term.md)

## sub_nodes

*(none yet)*

## definition

The one fixed printing rule that turns a z3 term into a single line of
characters, so that two units computing the same thing print the same
string. Five steps, in order: simplify the term once; put the arguments
of a commutative operator in a fixed order computed FROM THE ARGUMENTS
THEMSELVES; rename every free symbol positionally to `v0`, `v1`, … in
the order the symbols are first met; simplify and re-order once more,
because the renaming is a new term; and print on one line. Renaming
positionally is what removes the register names, which differ between
compilers for the same computation. The ordering step is what removes
the SOLVER's own choice of argument order, which is a function of what
the process built earlier and not of the unit (correction of
2026-09-03, task 79, below). The result is a COMPARISON KEY computed
beside the runnable text, never instead of it: nothing is executed from
it and nothing is proved from it.

## design

The rule, as numbered statements (steps 2 and 5 added 2026-09-03 by
task 79; step 4 was never in the numbered list and has been in the code
since the rule was first written — the correction below records both):

1. Simplify the term ONCE. Not to a fixed point, not repeatedly — one
   pass, so the rule is the same for every unit.
2. ORDER THE ARGUMENTS of every commutative operator, bottom-up, by a
   key computed from the argument sub-term itself. The key is the
   sub-term's own canonical printing: the operator's name WITH ITS
   PARAMETERS (`Extract`'s two bit positions are part of which operator
   it is), the sub-term's sort, and the keys of its own arguments, with
   every free symbol written as its sort alone so that no register name
   can decide an order. Ties — two arguments of identical shape
   differing only in which symbol they read — are broken by the same
   key with the symbols' own names, which is a fact of the unit.
   The table of commutative operators includes the FLOAT ones (`fp.add`,
   `fp.mul`, `fp.eq`); for an operator carrying a rounding mode, the
   rounding mode stays first and only the value arguments are ordered.
3. Rename free symbols positionally `v0`, `v1`, … in first-met order.
4. Simplify the substituted term once, and order it once more. The
   substitution builds a new term, and the solver orders the new term's
   commutative arguments by its own node identity again; ordering it a
   second time is what makes step 4's output a function of the unit.
5. Print on one line.
6. The result is a key, computed only for a unit whose term the gate
   PROVED. A term that did not prove has no key.

```
Term.normalize
	methods:
		simplify_once
			"""
			z3 term -> simplified term, one pass
			"""
		order_commutative
			"""
			term -> term with the arguments of a
			commutative operator in a fixed order,
			keyed on the arguments themselves:
			operator name with its parameters, sort,
			and the arguments' own keys, free symbols
			written as their sort. Never the solver's
			node identity
			"""
		rename_positionally
			"""
			free symbols -> v0, v1, ... in
			first-met order
			"""
		print_one_line
			"""
			term -> normalized_text
			"""
```

Instance: `c/op_109` and `go/op_319` — different compilers, different
register assignments, one normalized text, `v0 + v1`.

## settled rules

- **The rule is simplify once, ORDER THE COMMUTATIVE ARGUMENTS,
  rename positionally, simplify and order again, print on one line.**
  The first, third and last of those are log_147 §8.1's; the ordering
  steps are task 79's repair of the defect the correction below
  measured. Decision: log_147 §8.1; this CORE, 2026-09-03, task 79
  (evidence `log_186`).
- **Layer 5 is a key beside layer 3, never instead of it.** Layer 3,
  the wrapped text, is the runnable record. Decision: log_147 §8.1;
  [term](../CORE_0_3_1_6_term.md) settled rules.
- **Only a PROVED term is normalized.** Decision: log_147 §1.2; the
  pool reads it as `layer5_merge_eligible`.
- **The fixed-rule re-render is a textual normalizer applied AFTER
  proof, never the only route to a text.** Decision: AgentMemory
  "ROUND 10 RULINGS" context; log_142 ruling 4.

- **THE RULE DID NOT ACHIEVE ITS OWN STATED PURPOSE; THE REPAIR WAS
  PLANNED FOR ROUND 14 AND WAS MADE IN ROUND 15** (correction,
  2026-09-03, task 65; ANSWERED the same day by task 79, whose ruling
  is the paragraph after this one — this paragraph is kept unchanged
  below the first line for its record of the measurement).
  This definition says the rule exists "so that two units computing
  the same thing print the same string". MEASURED, over the 26,594
  units the round-13 gate proved, a second walk of the SAME rule over
  the SAME units printed a different string for **1,479 of them
  (5.6%)** — 525 c, 916 cpp, 13 go, 10 rust, 15 swift — and produced
  1,294 distinct texts where the first walk produced 1,267. The cause
  is that `z3.simplify` orders the arguments of a commutative
  operator by the solver's internal node identity, and that identity
  depends on what the process built earlier — so the text is a
  function of the unit AND the walk order. Step 2's positional
  renaming then follows the moved order, so `v0` and `v1` can swap
  as well. CONSEQUENCE: the pool's layer-5 merge ground carries this
  noise, and it is what nine of the 35 pool4 -> pool5 splits are made
  of — entries whose members' texts differ only in the argument order
  of one `Or`. THE REPAIR is a further PRINTING step, applied to the
  simplified term BEFORE the renaming: the arguments of a commutative
  operator put in a fixed order that depends only on the arguments
  themselves. It was tried and measured, and it is NOT SUFFICIENT ON
  ITS OWN — it collapses 299 of 1,292 texts and still leaves 39 of
  582 units on the `c` shard printing differently when the walk order
  is reversed — so the ruled three steps were NOT edited on a partial
  fix. Evidence: `normalize_order_probe65_printed.txt`,
  `normalize_stability65_printed.txt`, log_169. Decision: this CORE,
  2026-09-03, applying its own definition; recorded honestly as a
  correction written AFTER the measurement that produced it, because
  it was not known before the measurement ran.

- **THE REPAIR, RULED AND MEASURED (2026-09-03, task 79).** The
  ordering step of design 2 and 4 is the repair, and it is ruled in
  because it was measured, not because it was the obvious shape. What
  round 14 measured as insufficient was the same idea with two pieces
  missing, and each missing piece was a residue:
  - **The operator's PARAMETERS were not part of the ordering key.**
    `Extract(63, 0, x)` and `Extract(127, 64, x)` read different bits
    and z3 spells both `extract`; two such arguments tied, and a tie
    fell back to the order the term arrived in — the solver's node
    identity, the very thing the step removes. Measured over the `c`
    shard's 582 proved units, walked forward and reversed in one
    process: **11 of 582** still print differently with the parameters
    out of the key; **0 of 582** with them in. Evidence:
    `normalize79_cause_printed.txt`.
  - **The FLOAT operators were not in the table of commutative
    operators.** Round 14's table held the bit-vector and boolean ones
    only, and the residue it recorded — 39 of 582 `c` units — was made
    entirely of float units, whose `fp.add` and `fp.mul` were never
    ordered. Measured this round on the same shard, the ordering step
    with the float operators left out of the table leaves **43 of 582**
    printing differently between a forward and a reversed walk (round
    14's own probe left 39; the two probes differ in how they key the
    ordering, so the counts are close and not the same number), against
    **77 of 582** for the rule as it stood and **0 of 582** for the
    corrected rule. For an operator carrying a rounding mode the
    rounding mode stays first and only the value arguments are ordered.
    Evidence: `normalize79_cause_printed.txt`.
  - **The step is applied TWICE**, once after the first simplification
    and once after the renaming, because the substitution builds a new
    term and the solver orders the new term's commutative arguments by
    node identity again.
  - THE ACCEPTANCE, run and recorded: three walks in three separate
    processes — two in name order and one with the shards and the units
    inside them shuffled (seed 79) — print the SAME text for **26,594
    of 26,594** proved terms; 0 refusals in each walk. The distinct
    layer-5 texts over that population fall from **1,267** (one walk of
    the uncorrected rule, `term65_store`) to **850**, the same 850 in
    all three walks. Evidence: `acceptance79_pre78_printed.txt`,
    `normalize79_walk_pre78_walk1.json` / `..._walk2.json` /
    `..._walk3.json`, log_186. Decision: this CORE, 2026-09-03, task 79.
  - A POPULATION NOTE, because the transcription layer moved under the
    measurement the same day. Task 78 landed a corrected destination
    rule in `ledger.py` (a runtime transfer writes what the attached
    callee's own body writes, not the accumulator) while this walk was
    running. Under the ledger AS IT NOW STANDS, 442 of those 26,594
    units build no OUT-0 term at all, so the three walks print 26,152
    and the acceptance over the current tree reads **26,152 of 26,152
    identical, 442 not printed** (`acceptance79_printed.txt`). The
    26,594-of-26,594 figure above is the same three walks against the
    transcription layer that produced `term65_store`'s 26,594 — the
    only like-for-like comparison there is — with `ledger.py`,
    `canonical_form.py` and `reference.py` pinned to their blobs of
    2026-09-03 23:02. Both figures are the corrected rule printing the
    same text every time; the difference between them is entirely
    task 78's, and it is flagged in log_186 for the ledger node, not
    decided here.
  - **A CONSEQUENCE STATED RATHER THAN HIDDEN: the corrected rule
    UNMAKES five merges that were false.** Predicted over pool5 without
    rebuilding it: 1,831 entries become 1,813 — 50 entries merge in 21
    joins, and 11 entries split. Of the 11, five separate members that
    z3 proves answer DIFFERENTLY for some value of their arrival
    registers (`c/op_555` computes the ordered comparison one way and
    `c/op_663` the other; the uncorrected rule printed one text for
    both because the positional numbering followed an unstable
    argument order). The other six are pairs z3 proves EQUAL whose
    terms are structurally different; a text rule can only ever have
    merged them by accident of numbering, and the ground that carries
    them is the proved edge, not the text. Evidence:
    `normalize79_pool_prediction_printed.txt`,
    `normalize79_split_causes_printed.txt`.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| simplify, rename, print | `layer5.py` | done |
| instance | `v0 + v1` for `c/op_109` and `go/op_319` | done (log_153 §6.1) |
| distinct layer-5 texts among eligible units | 1,104 over the pool's 30,436 members | done (log_154 §2.2) |
| layer 3 against layer 5, per population | counted in log_153 §6.2 | done |
| round-13 layer-5 texts | 1,267 distinct over the 26,594 proved terms; 0 normalization refusals | superseded record (task 65, log_169) |
| the ordering step | `term.py` — `order_commutative`, `ordering_key`, `rebuilt_node`, `operator_name`, `argument_order`, `COMMUTATIVE_OPERATORS`, `ROUNDED_COMMUTATIVE_OPERATORS` | done (task 79, log_186) |
| the three walks, one process each | `normalize79_walk.py`; `normalize79_walk_pre78_walk1/2/3.json` against the pinned pre-task-78 transcription layer, `normalize79_walk_walk1/2/3.json` against the tree as it now stands (walk 3 shuffled, seed 79, in both) | done (task 79) |
| the acceptance test | `acceptance79.py`; `acceptance79_pre78.json` / `_printed.txt` — **26,594 of 26,594** identical, 1,267 texts collapse to 850; `acceptance79.json` / `_printed.txt` — 26,152 of 26,152 identical with the 442 task 78 stopped transcribing named | done (task 79, log_186) |
| the pool prediction task 83 checks | `normalize79_pool_prediction.py` / `.json` / `_printed.txt` — 1,831 entries to 1,813: 50 entries merge in 21 joins, 11 split | done (task 79) |
| the cause of every split | `normalize79_split_causes.py` / `.json` / `_printed.txt` — 5 false merges repaired, 6 proved-equal pairs the text ground stops carrying | done (task 79) |
| what each piece of the repair is worth | `normalize79_cause.py` / `.json` / `_printed.txt` — 77, 11, 43, 0 of the `c` shard's 582 units | done (task 79) |
| the guard | `guard79.py`, `guard79_transcript.txt`, `guard79.json` — 11 artifacts, 11 PASS, 0 FAIL, 0 exempt | done (task 79) |
| the collapse, per population | `collapse65.py`, `collapse65.json`, `collapse65_printed.txt` | done (task 65, log_169) |
