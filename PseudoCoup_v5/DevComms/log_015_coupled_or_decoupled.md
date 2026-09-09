# log 015 — the coupled/decoupled decision, and the round-trip principle recovered

2026-08-06. Two things, both at the owner's request. §1 is the chat
response of 2026-08-06 copied VERBATIM (the owner: "this feels like an
inflective decision point... keep your response as is and place it
in a log document"), with a glossary appended in §3. §2 records the
round-trip faithfulness principle the owner recalled in the same exchange,
verbatim, because he asked that a note be made somewhere.

---

## 1. The decision, as put to the owner (verbatim from chat)

First up is the one question that sits above all three
recommendations. Here it is, unpacked slowly.

**You have two lists that could easily be mistaken for one list.**

List one — the minimum set (your 11 objects). It answers: *what must
the hub be able to RUN?* Your old audit's "derived, not in the set"
verdicts belong to this list. "Sum types are derived" meant: the hub
needs no 12th object, because record + choice can already run
everything a sum type does.

List two — the coarse buckets of `ur_kind`. It answers a different
question: *what LABEL does a source node get*, so tools can group
nodes without knowing the language.

The upstream question is: **do list one's verdicts automatically
decide list two?** "The hub doesn't need a sum-type *object*" is a
fact about capability. It does not automatically mean "a sum-type
*node* deserves no label of its own" — a label costs the hub
nothing; it's a word on a record, not a new thing the hub must run:

```python
# the hub RUNS Rust's  enum Shape  as a tagged record — settled:
shape = ("circle", 2.0)

# but the ledgerer LABELS the source node. two candidate labels:
{"ts_kind": "enum_item", "ur_kind": "record"}   # what it becomes
{"ts_kind": "enum_item", "ur_kind": "sum"}      # what it was
```

If you rule the lists are **coupled** (labels follow the hub's
objects), the three recommendations stand as briefed: record+choice,
choice+function, no borrow bucket. If you rule them **decoupled**
(labels may be finer than the hub's objects), the guard reading
gains everywhere, because nothing stops a `sum` label.

And here's the observation that I think makes the ruling easy — look
at the example again. **The node carries both fields either way.**
`ts_kind: enum_item` is already there, permanently, because the
substrate layer is lossless. "What it was" is never lost, whichever
label you pick. So a separate `sum` bucket buys almost nothing that
`ts_kind` doesn't already give — the guard reading's fear (losing
the distinction, wrongly merging with Java's enum) is a fear the
strictly-richer design already answered at a lower layer. Which is
why I lean coupled: let the label say the dominant object, and let
the substrate keep the source's exact form, as it always does.

That's the decision. Coupled or decoupled — and if you want, I can
show what one real ledger record would look like under each before
you call it.

---

## 2. The round-trip principle, recovered by the owner in the same exchange

the owner, 2026-08-06, verbatim (recalling "a key PC principle established
since the early versions of PC (i think maybe as far back as v1)
that may have been lost in the fray"):

> faithful multiple round-trip transpilation through all 12
> languages and back to the original source (with the exception that
> the first return to the original source might be slightly
> different but every return after that is identical). another
> similar requirement is that transpiling back-and-forth between two
> languages is identical after the first cycle (similar to the first
> but not requiring a full round-trip through all 12 languages).

And the oracle consequence, verbatim:

> regarding the round-trip faithfulness, i think we should make a
> note somewhere about how that principle could be exceptionally
> useful as a self-contained oracle since source code provides
> ground-truth via round-trips.
>
> speaking of oracles, the re-construction of source code also
> naturally contains its own oracle. we can rely on the same idea.
> we would do: original source --> ledger; ledger --> equivalent
> source (but not identical to original source); equivalent source
> --> ledger; ledger --> equivalent source (identical to the first
> equivalent source)

The principle has receipts in the lineage — it was practiced, not
only stated: v3 kept "12 roundtrip artifacts" as its verification
(transpiler survey §2); exp09 in the archives is "a 4-language
dynamic-oracle round-trip harness (egress -> ingress -> run -> diff
vs canonical)" (survey §3); and the standing determinism rule
("regeneration byte-identical") is the same demand made of the
tools' own outputs.

This is a `finding`-grade note today. It graduates into the ledgerer
chain's planning (likeliest homes: `ledger`'s mechanics or the
builder's `check`) when the owner places it; nothing is registered by this
log.

---

## 3. Glossary

```
coupled / decoupled (this decision)
    coupled: the kinds vocabulary's labels
    must follow the minimum set's verdicts —
    a construct ruled "derived" gets no
    label of its own. decoupled: labels may
    be finer than the hub's object list,
    because a label is a word on a record,
    not a new thing the hub must run.
    example tied to context:
        coupled tags rust's enum_item
        `record`; decoupled may tag it
        `sum`. either way ts_kind stays
        `enum_item` in the substrate.

minimum set (list one)
    the 11 objects the hub must be able to
    RUN so every intention of the 12
    languages can execute there. membership
    is a capability question.
    example tied to context:
        "exception" was ruled derived —
        choice + early return — so it is
        not a 12th object.

kinds vocabulary (list two)
    the coarse labels ur_kind draws from,
    so tools can group source nodes without
    knowing the language. labeling is a
    classification question, not a
    capability question.
    example tied to context:
        function_item carries `function`;
        the decision is whether enum_item
        carries `record` or `sum`.

label vs object
    an object is something the hub must
    implement and run. a label is a word
    written on a ledger record. adding a
    label costs nothing at run time; adding
    an object costs hub capability.
    example tied to context:
        a `sum` LABEL needs no code; a
        12th minimum-set OBJECT would.

substrate
    the layer of a UR node that keeps
    exactly what the parser said — ts_kind,
    span, bytes, position — lossless,
    whatever labels are added above it.
    example tied to context:
        `ts_kind: enum_item` survives on
        the record under either ruling,
        which is why the stakes of the
        label choice are small.

dominant intention
    the owner's term: the object whose
    capabilities cover another object's
    entirely, so the lesser can hot-swap
    into it with zero loss, unused
    capability inert.
    example tied to context:
        tagged record is dominant over sum
        type — it can even hold states the
        sum type forbids; Rust adds only a
        compile-time proof.

round-trip faithfulness (the recovered principle)
    transpiling out and back converges:
    the first return may differ from the
    original, every later return is
    identical. holds for the full
    12-language circle and for any
    two-language back-and-forth.
    example tied to context:
        original source -> ledger ->
        equivalent source -> ledger ->
        equivalent source, where the
        second equivalent equals the
        first.

fixed point (why "identical after the first
cycle" works)
    a value a process maps to itself. the
    first pass normalizes (formatting,
    sugar) and lands on the fixed point;
    every later pass reproduces it exactly.
    example tied to context:
        the "equivalent source" in the owner's
        chain is the fixed point of
        ledger -> source -> ledger.

oracle
    a source of ground truth a test can
    compare against without a human
    judging. the round-trip principle makes
    the system SELF-oracling: the original
    source is the ground truth, and
    convergence is the pass/fail.
    example tied to context:
        v0's oracle.py compared Kotlin
        behavior to transpiled Python;
        the owner's reconstruction oracle needs
        no second language at all.

polyfill
    code supplied in a target language to
    stand in for a capability the target
    lacks. anticipated in targets so
    dominant intentions can always land.
    example tied to context:
        a target without sum types
        receives the tagged-record form;
        if the polyfill is already there
        for the dominant intention, the
        sub-dominant origin need not
        matter — the owner's own observation in
        this exchange.
```
