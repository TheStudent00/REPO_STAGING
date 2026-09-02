---
id: hq.research.kind_fuzz_clustering.support.ontology
level: 3
status: settled
settled_by: the owner
designation: rule
node:
    name: kind_fuzz_clustering
    path: Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md
---

# SUPPORT — ontology

the ontology of the fuzz-clustering objects.

Settled 2026-08-21 with the owner, after the words `row` and `key` were used
loosely enough to cost several turns. Every term below has exactly one
meaning, and no term is reused for two things.

## the containment chain

```
language
  operator            rust.+ , ruby.&& , ruby.and
    profile           operator x lhs holder x rhs holder x level
      cell            one input pair -> one output
```

## the terms

```
value
    one member of an X set, in canonical
    form.
    example tied to context:
        `[1, 1.3125, 5]` is the canonical
        form of 42.

X set
    the sampled interval for one form at one
    level: the list of values probed.  A
    PROFILE CARRIES ITS X SET -- the interval
    is a property of the profile, not
    something outside it.
    example tied to context:
        `whole/L1/17` is the 17 whole values
        from -2^63 to 2^64-1; `truth/L1/6` is
        true, false, 0, 1, "", nil.

key
    the ADDRESS of a cell: the input pair
    `(lhs_canon, rhs_canon)` at level 1, or
    the four-tuple `(x0,x1,x2,x3)` at level 2.
    A key is never merged with anything -- it
    is an address, and addresses are only
    matched or not matched.
    example tied to context:
        `([1, 1.0, 0], [1, 1.0, 0])` is the
        key of the cell where both operands
        are 1.

cell
    one key together with the output it
    produced.  The atom of the whole line:
    everything above is computed from cells
    and nothing else.
    example tied to context:
        in `ruby.* / Integer x Integer`, key
        `([1, 1.75, 2], [1, 1.75, 2])` holds
        output `[1, 1.53125, 5]` -- 7 times 7
        is 49.

profile
    ALL the cells for one (operator, lhs
    holder, rhs holder, level).  Fixed by the
    two INPUT slots; the output slot is
    whatever came back and may differ from
    cell to cell.  Level 1 has |X|^2 cells,
    level 2 has |X|^4.
    example tied to context:
        `ruby.& / TrueFalse x TrueFalse / L1`
        is 36 cells, and its outputs include
        `true`, `false`, `[1, 0.0, 0]`,
        `RAISE:TypeError` and
        `RAISE:NoMethodError` -- five output
        shapes in one profile.

operator
    one SPELLING in one language, together
    with every profile that spelling has.
    Language-qualified: `rust.+` and `ruby.+`
    are two operators, and `ruby.&&` and
    `ruby.and` are two operators that turn
    out to have identical profiles.
    example tied to context:
        `ruby.+` holds 36 level-1 profiles
        (six holders on each side) and 36 at
        level 2.

form
    the census-level kind of a value, above
    the holder: nothing, truth, whole,
    fractional, text, sequence, keyed,
    nesting.

holder
    the typed slot a value sits in before the
    operator is applied.  One form can own
    several holders.
    example tied to context:
        ruby's `Integer`, `Rational` and
        `BigDecimal` are three holders of the
        form whole.
```

## the relations between profiles

```
shared keys
    the INTERSECTION of two profiles' key
    sets.  Two profiles are comparable only
    at their shared keys; the rest of each
    profile is not evidence about the other.
    example tied to context:
        `ruby.& / TrueFalse x TrueFalse` and
        `ruby.* / Integer x Integer` share 4
        keys -- the pairs drawn from {0, 1},
        the only canonical values in both X
        sets -- out of 36 and 289 cells.

comparable key
    a shared key where NEITHER profile
    declined.  A decline (REFUSE, RAISE:*,
    ABORT) drops the key from the numerator
    AND the denominator.

agreement
    over the comparable keys, the fraction
    where the two outputs are byte-identical.
    This is the exact-match weight.  The
    graded weight is the same quantity with
    per-element numeric similarity in place
    of byte identity.

contract
    two profiles with the SAME key set whose
    cells are identical at EVERY key become
    ONE node.  This is plain identity, so it
    is transitive and needs no clique test.
    the owner's words: "the merging is based on
    identical canon lhs, rhs, output.  not a
    few of them.  on all of them."
    example tied to context:
        `ruby.&& / Integer x Integer / L1`
        contracts with
        `ruby.and / Integer x Integer / L1`;
        this happens 32 times across the
        holder pairs and both levels.

group
    contracted nodes that agree at every
    SHARED key but whose key sets DIFFER are
    NOT contracted.  They are drawn inside
    one hull: members stay distinct, the
    group carries each pair's overlap size
    and the minimum overlap as its weakest
    evidence.  Every pair inside must agree
    (a maximal clique) -- never a connected
    component, because chaining through
    never-compared pairs is the hazard
    (measured: 7,212 such triples, log 053).
    example tied to context:
        rust's `f32 * f32` groups with ruby's
        `Float * Float` at 144 shared keys;
        their X sets differ (f32 carries 7
        fractional values, f64 and Float carry
        16), so they are grouped, not
        contracted.
```

## what merging is NOT

- Keys are never merged. A key is an address; two profiles either hold
  the same address or they do not.
- Cells are never merged. A cell belongs to exactly one profile.
- Only PROFILES contract, and only when every cell matches over an
  identical key set.

## the three relations, and which rule governs which

Added 2026-08-23 with the owner (`DevComms/log_067_three_relations_alignment.md`).
**Nothing above is rewritten; this section says which relation each rule
above was written for.**

THREE DISTINCT RELATIONS had been conflated under the word
"dominance". Each has its own license and its own properties.

```
CONTAINMENT  (discovery)
    "does an existing operator already
    contain this one?"
    A dominates B when at every key where B
    answers a VALUE, A answers that identical
    value.
    DIRECTED, and TRANSITIVE.  The proof:
        A dominates B, B dominates C.  Take
        any key where C answers a value v.  B
        must answer v.  Since B answers a
        value there, A must answer v.  So A
        dominates C.
    Nothing is inferred about a never-compared
    pair -- it FOLLOWS.  So the CHAINING
    HAZARD ruled against for GROUP below does
    NOT apply to containment.

ACCUMULATION  (construction)
    "may opA, opB, opC be combined into a
    dominant opD that may not exist in any
    language?"
    A UNION, not containment.  Licensed by
    SHARED INTENTION -- the same minimum-set
    object -- NEVER by measured overlap.  The
    measurement then says HOW they fracture,
    not WHETHER they belong together.
    Overlap is not sufficient:
        dart `??` and kotlin `?:` share an
        edge and are unrelated operations --
        neither language declared a nullable
        holder, so both degenerated to
        "return lhs" (log_065, the one
        confirmed coincidental pair).  Same
        shape as `and`/`mul` agreeing on
        {0, 1}.
    Overlap is not necessary:
        three operators with entirely disjoint
        behaviour profiles, all spelled `+` in
        three languages, still justify one
        dominant `+` -- maximally fractured,
        but one operator.  Requiring a shared
        edge would refuse to build the
        operator most needed.

FRACTURE  (mode accommodation)
    "is x0 a mode of x1, or a different
    behaviour?"
    Neither containment nor equality -- a
    SIMILARITY judgement, decided with the
    graded scoring plus the guarantees rule
    (`Research/dominant_intentions/census_integer.md`).
    This is where the clustering machinery --
    group, clique, connectedness, the two
    readings -- legitimately belongs.
```

**Which relation each rule above governs:**

| rule | written for | still correct there | note |
| --- | --- | --- | --- |
| `contract` | FRACTURE (identity of two profiles) | yes | plain identity; transitive under any relation, so it also survives unchanged as the finest containment step |
| `group` | FRACTURE | yes | a GROUP may legitimately hold objects that were compared and did NOT match: "connected" there means SIMILAR |
| the clique requirement inside `group` ("never a connected component… 7,212 triples") | FRACTURE | yes | it is a fact about a SYMMETRIC similarity relation. **It does NOT transfer to CONTAINMENT**, which is transitive by the proof above |
| `shared keys`, `comparable key`, `agreement` | FRACTURE | yes | measurement machinery, relation-neutral |
| the two readings (VALUE / ALL-CELLS, `DevComms/log_065`) | FRACTURE — the mode partition | open | which reading is THE reading is `STANDING_RULINGS_AWAITING_DEE.md` §1.1, still the owner's |
| the owner's input-overlap criterion (CLAUDE.md) | FRACTURE | yes | it exists to cut 4-shared-key similarity edges; containment has no threshold to defend |
| the decline rule ("declines are never scored") | untagged | — | it changes what CONTAINMENT means as much as what similarity means; that is exactly §1.1 |

**The correction, recorded honestly.** The clustering ontology was
built for a symmetric similarity question, and its vocabulary was
carried into a directed containment problem without checking whether it
transferred. **Every rule here must say WHICH RELATION it governs.**
The rules not tagged in the table above are untagged because that
tagging is structural and is the owner's.

## the disagreement-kind classifier — governs FRACTURE

Added 2026-08-23, **ruled by the owner** ("looks good! lets do it"), recorded
in `DevComms/log_069_disagreement_kind_classifier.md`. **Nothing above
is rewritten.** This section replaces the two-readings question rather
than answering it.

A cell holds either a VALUE or an outcome token (`REFUSE`, `RAISE:*`,
`ABORT`, `UNREPRESENTABLE`). So a disagreement between two profiles at
one key is one of exactly two things, and a PAIR sorts by which of them
appear in it. **There is no threshold anywhere in this rule.**

```
WINDOW disagreement
    one side answers a VALUE where the
    other holds a token.  The two holders
    have different ranges.  A
    REPRESENTABILITY fact, never a
    guarantee fact.

VALUE disagreement
    both sides answer, and the values
    differ.  A BEHAVIOUR fracture.

the three pair kinds
    WINDOW-only  -- no value-vs-value clash
                    anywhere.
    VALUE-only   -- no decline-vs-answer
                    cell anywhere.
    MIXED        -- both kinds present.
```

**THE RULE:**

| pair kind | verdict | what is recorded |
| --- | --- | --- |
| WINDOW-only | **SAME family** | the window is the profile's RANGE, never a mode |
| VALUE-only | **DIFFERENT modes** | the disagreeing cells define and name the boundary |
| MIXED | **apply the region test** | are the disagreeing keys a describable region — one operand negative, magnitude past a limit, one side declining? A fracture has a boundary; noise does not. **Undescribable → flag for the owner, do not decide.** |

Measured over all 4,371 `plus` profile pairs on `whole|whole` L1 in
`matrices_full_v2/`: **1,317 WINDOW-only, 58 VALUE-only, 2,691 MIXED,
305 identical.**

**Why this replaces the two readings.** ALL-CELLS counted a window
difference as disagreement, which split rust's `i32`/`i64`/`u64` into
three false modes; VALUE ignored it entirely, which produced a cover
rather than a partition. Both asked HOW MUCH two profiles disagree. The
useful question is WHAT KIND of disagreement it is. Neither reading
could get both cases right; the classifier gets both.
`STANDING_RULINGS_AWAITING_DEE.md` §1.1 is therefore CLOSED **by
dissolution**, not by a choice between the readings.

**The relation this governs is FRACTURE.** It says nothing about
CONTAINMENT or ACCUMULATION, which keep the licenses recorded above.

**The decline rule still stands and still binds it.** "Zero comparable
keys means NO connector, not a zero-weight one" — so a WINDOW-only pair
with no cell where BOTH answer a value is NOT an edge. Measured
consequence (`DevComms/log_070_dominant_operators_all.md` §5): without
that guard, a profile that declines everywhere is WINDOW-only-compatible
with every profile in its block and every gate block collapses to one
family.

**What the classifier does NOT cover, recorded as a limit.** A cell can
disagree TOKEN against DIFFERENT TOKEN — both sides declined, with
different outcomes. Across the eighteen gate blocks, **482 pairs
disagree only in that way** (witness: `cpp.% int32_t x int32_t` against
`csharp.% int x int`, 10 such cells, 71 comparable cells, zero value
clashes and zero window differences). They have no kind under the rule
as ruled. Open, and it is the owner's.

**Transitivity, measured, NOT assumed.** WINDOW-only is a pairwise
verdict. Closing it transitively is a separate decision and it has a
measured counterexample: on `whole|whole` L1 the WINDOW-only components
merge `add wrapping`, `add growing` and `add approximating` into one
group of 96 profiles, through profiles that never reach their own
fracture. Two hops suffice —

```
php.+ int x int          (approximating, 256 value cells)
  -- WINDOW-only -->
csharp.+ short x short   (49 value cells, reaches no fracture)
  -- WINDOW-only -->
cpp.+ int64_t x int64_t  (wrapping 64 signed, 256 value cells)
```

— while the two ends, compared directly, clash at 35 value cells.
Whether WINDOW-only merging is by component, by maximal clique, or
pairwise only is **not decided here**; both are measured in log_070 §5.

## open, to revisit

- **Output-shape variation as a clustering signal.** A profile whose
  outputs change shape across its cells (`ruby.&` answering `true`,
  a number, and two different raises) is currently scored only cell by
  cell. the owner, 2026-08-21: "i think those are potentially valid
  behaviors to cluster with... we will just make a note about it to
  visit later."
- **Declines as disagreement rather than exclusion.** Today a key where
  one side answers and the other declines is dropped. In
  `rust.+ / i32 x i32` against `ruby.+ / Integer x Integer`, exactly
  the 14 overflow keys are dropped, so the pair scores 1.000 — and the
  overflow fracture, which is the real difference between the two
  operators, is the thing that vanished.
- **the owner's input-overlap criterion** (input-overlap percentage must be
  >= the output-agreement percentage) is ruled but NOT yet applied to
  the v4 graph. It is what kills the 4-shared-key groups.
