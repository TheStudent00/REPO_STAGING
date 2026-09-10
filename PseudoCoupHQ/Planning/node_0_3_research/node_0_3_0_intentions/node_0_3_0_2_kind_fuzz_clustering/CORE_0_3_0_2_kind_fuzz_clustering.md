---
id: hq.research.kind_fuzz_clustering
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: kind_fuzz_clustering
    path: Planning/node_0_3_research/node_0_3_0_intentions/node_0_3_0_2_kind_fuzz_clustering/CORE_0_3_0_2_kind_fuzz_clustering.md
super_node:
    name: intentions
    path: ../CORE_0_3_0_intentions.md
sub_nodes: []
---

# CORE 0_3_0_2 — kind_fuzz_clustering

## metadata

- **id:** hq.research.kind_fuzz_clustering
- **level:** 3
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [intentions](../CORE_0_3_0_intentions.md)

## sub_nodes

*(none yet)*

## definition

**Cluster KINDS by measured behavior, using an automated fuzzer.**
the owner's naming, 2026-08-14: "oh kinds. thats what i was looking for.
to cluster kinds using an automated fuzzer."

The method he stated the same day:

> "i was thinking about establishing the basic data structures so
> that we can fuzz the rest of the vocabulary. without having to
> have a corpus. we generate the scripts based on vocab tokens
> (that we know what it wants for input and its output type) in
> order to observe how it processes data structures. and then use
> those changes to cluster across languages."

Generate a minimal script per kind, applying it to the verified
dominant data structures; run it; record what came back; cluster
kinds across the 11 languages by what they DID.

## support

- [SUPPORT_conversion_spec.md](SUPPORT_conversion_spec.md) — the
  settled cell-decomposition design (canonical numeric / container /
  text forms, per-operator matrices), ruled by the owner 2026-08-20.
- [SUPPORT_ontology.md](SUPPORT_ontology.md) — the settled ontology of
  the objects: language → operator → profile → cell, what a key is,
  what contract means, and what merging is NOT. Settled with the owner
  2026-08-21.

## the symmetry that gives this node its point

The co-node `kind_signature_clustering` already clusters **the same
population** — every language's kinds — but on a different
evidence source:

| | kind_signature_clustering | kind_fuzz_clustering (this node) |
|---|---|---|
| evidence | what the GRAMMAR SAYS about a kind (arity, slot types, supertypes — declared, static) | what a kind DOES to known inputs (measured, executed) |
| corpus | none needed (grammar files) | none needed (generated scripts) |
| population | 31,212 kinds, 411 languages | the 11 target languages' kinds |
| output | similarity spectrum over declared features | similarity over measured behavior |

Two independent readings of one population. That makes them
**mutually checkable**: where feature-clusters and behavior-clusters
agree, the grouping is strongly evidenced; where they disagree, the
disagreement is itself the finding (a kind that LOOKS like its
counterpart but behaves differently, or the reverse). Neither node
subsumes the other and neither was wasted.

## why it works — the calibrated-instruments argument

A probe's output is only readable if its input is known exactly.
`+` answering 9223372036854775808 is a bignum, a wrap, or a float
that lost precision — distinguishable ONLY because
`dominant_intentions` verified, by execution across 11 languages,
what each language's integer IS (467 confirmed / 7 refuted /
residue empty, 2026-08-14). The six dominants (boolean, float,
integer, string, list, dict) are the calibrated instruments of this
node.

This is why the owner's phase order was right: hand-build the instruments
first, then point them at everything else.

## what gets fuzzed

The grammar's kind set, per language, as tree-sitter knows it:

- **named kinds** — constructs (rust: 163; `binary_expression`,
  `for_expression`, `integer_literal`).
- **anonymous tokens** — operators and keywords (rust: 115; `+`,
  `==`, `..=`, `fn`).

NOT included: **builtins**. `len`, `push`, `map`, `sorted` are
library names; a grammar knows syntax, not the standard library.
They would need a separate per-language harvest — OUT of scope
until the owner opens it.

## the method, as designed 2026-08-14

1. **generate** — per kind, a minimal script applying it to
   dominant-typed inputs. Generation, never collection; there is no
   corpus and none is wanted.
2. **run** — through the Airlock agent lane
   (`python3 PUBLIC/Airlock/airlock submit <lane.sh> --batch
   <label> --weight <n>`; `airlock status` to poll), on the 11 target
   languages installed 2026-08-14 (+ swift bonus). Record the
   answer, the raise, or the **compile refusal** — refusal is a
   first-class result (ruled 2026-08-14; 34 measured instances in
   the census run).
3. **compare by RELATION, not flat signature** (the owner's correction,
   2026-08-14: "one language's builtin might accept more arguments
   than its equivalent in another"). Per kind, compare the pair
   {domain accepted, answer per input}. Two kinds then relate in
   exactly three ways — the trichotomy this line already uses:
   - **nests** — same answers, wider domain. This IS dominance,
     DISCOVERED rather than assumed: the wider kind dominates.
   - **overlaps** compatibly — union candidate.
   - **contradicts** — same input, different answer; a split,
     justified by measurement.
     RULED 2026-08-19 (the owner): contradicts is defined
     BEHAVIORALLY — two kinds whose domains coincide but
     whose answers disjoint. The earlier same-SPELLING
     reading (log_029 decision 6, a stand-in from before
     answers existed) is retired: name-collision pairs
     (cpp.xor vs php.xor and kin) stay on the record as
     data, but no further work is done on them. the owner:
     "i dont see when naming contradictions will ever be
     blocking or needs direct solving" — the time they
     may matter is after clustering, at intention
     unification.
4. **cluster** those relations across languages — the spectrum
   machinery from `kind_signature_clustering`, pointed at measured behavior.

## the layer-3 design — RULED 2026-08-18

the owner settled layer 3 in conversation on 2026-08-18. These rulings
GOVERN everything below them in this document; where an earlier
section disagrees it is marked superseded, not deleted.

### 1. the probe input is a layer-2 HOLDER

RULED: a probe's operand is a layer-2 **holder**, not a layer-1
form. the owner, 2026-08-18: *"yeah per holder"*.

- the layers are the co-node's anchor
  ([CORE_0_3_0_4_data_representation.md](../node_0_3_0_4_data_representation/CORE_0_3_0_4_data_representation.md)):
  layer 1 is the data, layer 2 the per-language holders of
  that data, layer 3 — this node — what the compiler can do
  to a holder.
- every result row carries the triple **(form, holder, value
  class)**. Form-level views stay DERIVABLE by projection, so
  ruling at holder grain costs no coarser reading; the reverse
  would have lost the distinctions the python run already found
  (`Decimal(42) + Fraction(42)` raises though both hold one
  form — log_024 §5).

### 2. FULL ENUMERATION of ordered operand pairs

RULED: no pruning rules. the owner, 2026-08-18: *"full enumeration...
its proof vs potentially biased rules"*.

- ordered pairs, both orders kept: an operator is not assumed
  commutative, and log_024 §5 already measured asymmetry in one
  language.
- sizing is MEASURED, not estimated away
  ([log_025 §1, §4](../../../../DevComms/log_025_probe_timing_measurements.md)):
  **~5.79M probes across the twelve**, **6.2 h batched**,
  **18.1 d worst case** at one probe per file with no batching
  (435 h total).
- what this supersedes: the **four-rule pair selection** of
  phase 1 (`Research/kind_fuzz_clustering/probe_design.md`, log_024
  §2 decisions 1/2/11), which cut python's 13,689 cross product
  to 200 pairs. Dated rationale: the rules were a cost
  compromise taken before any cost was measured; log_025
  measured the cost and it is affordable, and a selected pair
  set cannot prove the absence of an acceptance it never
  probed. The 200-pair result stands as a valid measurement of
  what it covered; it is no longer the plan.

### 3. FULL VALUE MATRIX everywhere

RULED: every value of every holder, everywhere, not a sampled
placement. the owner, 2026-08-18: *"if its within reason, we can just
brute force it"*.

- log_025 §4 measured the cost of adding it to full pair
  enumeration at **under 1 percent** (python 0.86 percent,
  derived), because placement probes grow LINEARLY in values
  while the pair families already grow quadratically.
- what this supersedes: the **tier-B sampled placement** text —
  the split where tier A enumerated pairs and tier B probed one
  placement per slot over a sample of values. Dated rationale
  2026-08-18: the measurement removed the reason for the split;
  a tier that costs under one percent is not worth designing a
  sampling rule for. Tier B survives only as the NAME of the
  per-slot placement probe, no longer as a sampling policy.

### 4. progress print-outs are a STANDING REQUIREMENT

the owner, 2026-08-18: *"for fuck sakes please include runtime
print-outs on progress and maybe even time estimates"*.

Every generation phase and every run phase prints, as it works:
**[done/total]**, **elapsed**, and **ETA**. This is a
requirement on the harness, not a nicety, and it applies to
every phase of this node from here on.

### 5. the evidence ROUTES — all pursued, none dropped

RULED: the owner, 2026-08-18: *"i want to pursue all of them as
solutions where they dont overlap"*. log_026 §3 laid out three
routes and asked which to take; the ruling is all of them.
Assignments per compiler below are log_026 §1/§2's measured
shapes.

- **ROUTE A — acceptance via the compiler's own code
  running.** No transcription and no interpretation anywhere on
  the path; the owner's standard is a *"logical match -- not
  interpretation"*.
  - **A1, in-process** — import the compiler's own shipped
    checking module and CALL it with our operand pairs. Named
    by log_026 §3 finding 4: go (`import "go/types"`, a public
    stdlib package), typescript (the require-able checker in
    the shipped `typescript.js`), java (`javax.tools`).
  - **A2, check-only binary invocation** — the real compiler
    front end, full type check, codegen and linking skipped:
    `rustc --emit=metadata`, c++ `-fsyntax-only`. For
    **kotlin, swift, dart, csharp** the check-only flag or API
    route is **UNVERIFIED** and must be verified before it is
    assigned (open item below).
- **ROUTE B — acceptance DATA lifted where it exists as
  literal data.** log_026 §2 measured three: go's
  `binaryOpPredicates` map (`expr.go:760-774`), java's
  **23-row** `Operators` table (readable via `javap -c`),
  rust's `Add` impl lists via `rust-src` (`arith.rs:113`, 16
  primitive types).
  - extraction OF DATA is mechanical and allowed.
  - **certification gate**: any lifted rule is certified by
    DIFFING its verdicts against route A or route C on the
    same pairs before it enters any table. An uncertified lift
    is a **draft** and is labelled one.
- **ROUTE C — execution.** The runtime ANSWERS — what an
  accepted operation returns — always come from executed
  probes; no route reads them off source. And for the
  **open-dispatch** languages (python, ruby, php, where `+`
  resolves at run time through `__add__`-style slots) execution
  is the ONLY acceptance evidence that exists — log_026 §1 and
  §3 finding 2: no table can exist in principle where the
  accepting set is not fixed at compiler-build time.
- **overlap discipline.** Where two routes answer the SAME
  cell, BOTH run. Agreement certifies the cell; disagreement is
  itself a finding and is recorded as one. This is the same
  two-source posture the signature-versus-fuzz symmetry above
  already gives this line.

### 6. the anti-interpretation rule

the owner's standard, 2026-08-18, verbatim anchor: an acceptance
verdict must come from **the compiler's own logic running**, or
from **its literal data matching** — NEVER from an agent's
reading of the compiler source re-assembled by hand.

The counter-example is recorded, and it is ours: the go
cross-check in [log_026 §2.1](../../../../DevComms/log_026_compiler_acceptance_shape.md)
reproduced go's acceptance set "from the lifted rule alone,
without invoking the type-checker's expression path" — a
hand-re-assembled rule. It agreed with go, which is exactly why
it is the instructive case: agreement does not make a
transcription evidence. Under this rule such a step is a
route-B draft awaiting certification, never a verdict.

### 7. the kotlin cost note

log_025 §4 measured **206 h of the 435 h worst case as kotlin
cold compiler start** (2,397 ms per probe, against cpp's 173
and rust's 36) — 47 percent of the bill for 5 percent of the
probes. The mitigation — compile daemon, batching, or route A2
— is CHOSEN AT PHASE-3 BUILD TIME and **measured, not
assumed**. No daemon was measured in log_025 (excluded by
instruction), so nothing yet quantifies that option.

## what prunes the probe space

**SUPERSEDED 2026-08-18 by ruling 2 above** for the operand
pair space: pairs are now fully enumerated and nothing prunes
them. This section still governs the KIND and CHAIN space —
which kinds exist and what must enclose them — which is
unaffected by the ruling. Kept whole, per the framework's
supersede-do-not-delete rule.

the owner's estimate: kind dependency chains are mostly length two
(`break` needs `for`; `else` needs `if`; `case` needs `switch`;
`catch` needs `try`; `await` needs `async fn`), giving n^2 pairs.
Two refinements, recorded 2026-08-14:

- **a short tail exceeds two** — java's `super(...)` needs class +
  extends + constructor (four); a labelled `continue` needs label +
  loop + continue (three). the owner: "some things might need to be by
  hand" — the tail is that hand list.
- **n^2 is a large overestimate: the grammar already says which
  pairs are LEGAL.** `node-types.json` enumerates, per slot,
  exactly which kinds may fill it — the same data `kind_clustering`
  ran on, already downloaded for all 411 languages
  (`Research/kind_signature_clustering/raw_all/`). Reading legal pairs off the
  grammar replaces blind enumeration: hundreds of probes per
  language rather than 163^2 ~ 26,000. The grammar prunes before a
  single probe is written.

## the engineering crux

In typed languages one bad probe kills the whole program, so probes
cannot simply be batched into one file; and one compile per probe is
unaffordable (kotlinc ~1 min; thousands of probes). **Bisect**:
compile a batch, on refusal split and recompile. Valid probes cost
log-many compiles, and each refusal isolates to its exact kind —
which is the measurement wanted anyway.

## plan of record (walked at the owner's pace)

0. **kind extraction** — pull each target language's named kinds and
   anonymous tokens from its pinned grammar; pull the legal-pair
   table from `node-types.json`. Measurement only; emits the probe
   space and its SIZE — the first number the owner should see before any
   probe runs.
1. **probe design** — the generation rules: which dominant-typed
   inputs each kind position takes, what a probe prints, how a
   refusal is recorded. Hand-written tail for depth-3+ chains. ONE
   language first (proposal: python — no compile step, fastest
   loop), reviewed by the owner before the generator generalises.
2. **generate + run, one language** — prove the loop end to end;
   report probe count, runtime, first behavior signatures.
3. **generate + run, ALL TWELVE, under the 2026-08-18 design.**
   Rewritten that date; the one-line "with bisect batching" it
   replaces is kept in PROGRESS. Phase 3 now means:
   - operands are layer-2 **holders** (ruling 1); every emitted
     row carries (form, holder, value class).
   - **full ordered-pair enumeration** and the **full value
     matrix** (rulings 2 and 3) — ~5.79M probes, 6.2 h batched,
     18.1 d worst case, per log_025 §4.
   - **all evidence routes run together** (ruling 5): A1
     in-process checker calls (go, typescript, java), A2
     check-only invocation (rust, c++; the other four to be
     verified first), B lifted data under the certification
     gate (go, java, rust), C execution — for the runtime
     answers everywhere, and as the only acceptance evidence in
     python, ruby and php. Overlapping cells run twice and the
     comparison is kept.
   - **progress print-outs** — [done/total], elapsed, ETA — on
     both generation and run (ruling 4).
   - **bisect/batching** for compiled-language execution probes
     is BUILT here (the engineering crux above, still unbuilt),
     and kotlin's mitigation is chosen here on measurement
     (ruling 7).
4. **relate + cluster** — unchanged by the 2026-08-18 design.
   nests / overlaps / contradicts across
   languages; output is the discovered kind map: which kinds are one
   thing in different spellings, which dominate which, which are
   private to their language. Cross-check against
   `kind_signature_clustering`'s signature-clusters (the symmetry above).

## record

- artifacts: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`
  (created at phase 0). The harness skeleton to reuse is
  `Research/dominant_intentions/harness/` (vectors → runners → lane
  → compare), with GENERATED probes replacing hand-written vectors.
- instruments: the verified census in
  `Research/dominant_intentions/` + `verified/`.
- co-nodes: `kind_signature_clustering` supplies the grammar data, the legal-
  pair table and the clustering machinery;
  `dominant_intentions` supplies the calibrated inputs.

## the CONSTRUCT families — RULED 2026-08-19

the owner blessed three construct families in conversation on 2026-08-19.
Layer 3 up to that date meant OPERATIONS only — what `+` and `==` do
to a holder. It now also means CONSTRUCTS: what `if`, `for`,
`break`, `a[b]` and `x = a` do to a holder. These rulings GOVERN
everything below them; where an earlier section disagrees it is
marked replaced, not deleted.

### 8. the three families, blessed

RULED: **access**, **flow**, **binding**. the owner, 2026-08-19, on the
naming: *"blessed"*.

- **access** — reaching into a value: index access, slice,
  member reach.
- **flow** — choosing, repeating, or leaving: if, for, while,
  break, continue, try.
- **binding** — attaching a value to a name: assignment,
  augmented assignment, unpacking.

Twelve construct roles over the three families. The list per
language is DERIVED from that language's own kinds file, never
hand-written; a role that resolves to no declared kind is ABSENT
and absence is a FINDING. Measured 2026-08-19: **130 of 144 role
slots resolved, 14 ABSENT**
(`Research/kind_fuzz_clustering/construct_catalogue.json`).

### 9. the SCAFFOLD principle

RULED: each construct gets **one fixed minimal enclosing scaffold**
per language, and it makes the construct legal while contributing
no behaviour. the owner's words for what the scaffold is, 2026-08-19:
inert code *"used to connect logical operations of interest"*.

Three properties are demanded of it, each for a reason.

- **minimal** — the least code that makes the construct legal.
  Every extra line is a second thing that could have caused what
  was observed.
- **inert** — it computes nothing, branches on nothing, and holds
  no state the construct can see.
- **fixed** — byte-identical across every probe of that construct
  in that language. Only the slot fillers change.

Together they give the property the pass rests on: **anything
observed is the construct's doing**, because the only thing that
varied between two probes was what went into the slots.

### 10. the TRACE — the observation standard for flow

RULED: a flow construct is observed by its **trace** — the
sequence of values at each joint. The loop variable at each
iteration, which branch ran, where a break stopped iteration.

The trace is recorded in the **same bits and type encoding as
`answers_encoding.md`**, so traces compare across languages
exactly as `+`'s bits did. The trace row reuses the answer row's
three-field shape:

```
PROBE_ID|TYPE_NAME|TRACE:<n>[<step>,...]
```

with joints `BR=`, `IT=`, `STOP=`, `SKIP=`, `BIND=` and `THROW=`.
Every `<enc>` is an `answers_encoding.md` payload verbatim. No new
encoding is invented and none of the old one is changed. The spec
is `Research/kind_fuzz_clustering/construct_design.md` §e.

### 11. slot discipline and routes CARRY OVER

RULED: nothing about the operand discipline changes. Each
construct slot is fed the layer-2 holders and, through them, the
layer-1 values — ruling 1 already settled that a probe's operand
is a holder, and a construct slot is an operand position like any
other.

- an **if-condition slot** run over all holders and all values IS
  the cross-language **TRUTHINESS table**. It is one-operand, so
  it is an 8-form vector per language and not a 64-cell grid.
- the **routes** are ruling 5's, unchanged: acceptance through
  each language's own proven instrument — the in-process checkers,
  the check-only invocations, the FULL swift compiler per log 034,
  and route-C execution for python, ruby and php; answers and
  traces through single-file execution of probes already known
  legal.

### 12. what this cost, derived and printed before it ran

**647,190 probes** across the twelve — about a ninth of the
operator pass's 5.79M, for the other half of what a compiler can
do to a value. Printed by `construct_space.py` before anything
ran, as the plan of record requires of every phase.

Measured 2026-08-19 (log 036): four languages complete —
python 59,797 probes in 16.9 s, ruby 48,297 in 0.8 s, php 33,660
of 33,680 in 10.4 s (twenty uncatchable fatals), go 1,710 in
26.8 s. Eight languages UNBUILT; instructions in
`Research/kind_fuzz_clustering/HARVEST_constructs.md`.

## open items — recorded 2026-08-18

Open under the settled design, and open is what they are:

- **bisect/batching is still UNBUILT** for compiled-language
  execution probes. log_025's batched 6.2 h assumes it and
  measured amortisation on batches known in advance to
  compile; treat the batched figure as a lower bound, not a
  schedule.
- **route A2 is UNVERIFIED for kotlin, swift, dart, csharp** —
  whether each has a check-only flag or an in-process API is
  not yet established. Verify before assigning.
- **log_024 decision 3** — whether a holder that partially
  refused loading gets probed on the values it DID load. the owner's
  default is **yes**. **RATIFIED BY SILENCE 2026-08-19** (log
  034): the default was put in front of the owner with the two JOB
  rulings and left standing. It is now the settled behaviour
  and it remains OVERTURNABLE — one flag in the generator, and
  every affected cell is already recorded per value class, so
  overturning it costs a re-read and not a re-run.
- **decision 43, the word-spelled operator criterion**
  (2026-08-19, log 034) — the operator vocabulary is no longer
  a hand-written candidate list intersected with the grammar;
  a word is first class iff the grammar declares it in a
  binary operator slot AND the checker refuses it as an
  identifier. Recorded here because it changes what the node
  MEASURES, not only how. Open in the sense that leg G is
  instrument-bound: three grammars spell operators in a way
  tree-sitter node types do not expose, and for those leg G is
  silent rather than negative.

## open for the owner

- phase 1's first language (python proposed).
- whether builtins come into scope later, and from what source.
- whether the depth-3+ hand list is written up front or grown as
  refusals expose the need.
