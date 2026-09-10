# Plan and code are one thing at two depths

Written 2026-07-31 from the owner's statement. This is a note of intent,
not an implementation. The plan trees at
`PRIVATE/PseudoCoup_v6/Planning/` and
`PRIVATE/PseudoIR/Planning/` do not yet conform to it. Bringing
them into conformance is a separate job for a separate conversation.

---

## The two rules

1. **A plan node that describes a code object carries that object's
   name.** Not a description of it, not a synonym — the name.
2. **Code is written from the top down, and logic is written last.**
   Depth is added a level at a time, exactly the way the planning
   tree is built.

Everything below is these two rules and what follows from them.

---

## 1. Names

### The plan is not a specification of the code

A specification is a separate document that describes something
else. It can drift from what it describes, and it always does. That
is not what these plans are.

**The plan is the code at a coarser depth.** A node names the thing.
Its sub-nodes name the thing's parts. Descend far enough and the
names you are writing are the identifiers in the file. There is no
translation step, because there is nothing to translate — it is the
same tree, seen from further away.

That is why a plan name and a code name are the same name. Two names
for one thing is two places for it to drift, which is the failure
this whole framework exists to prevent.

### Not every node is a code object: the `designation` field

Some nodes describe work, or knowledge, or a decision. `research`,
`lessons`, `intentions` are not classes. `ledgerer`, `transpile`,
`slice`, `insert` are — or will be.

**Every node carries a `designation`** (the owner, 2026-07-31). Not only
the ambiguous ones — every one, so that a missing designation is a
defect the renderer can name rather than a silence someone has to
interpret.

```yaml
designation: code (class)
designation: code (class), rule
designation: work
```

- A comma-separated list. A node can be more than one thing.
- `code (<kind>)` where kind is one of: `object`, `module`, `class`,
  `method`, `attribute`, `function`, `variable`.
- `object` is the COARSE kind, added 2026-08-01: the identifier is
  settled but the kind among the rest is not yet, so "module or
  class?" never blocks a node's creation. the owner: "i view `module` as
  effectively a `class` with a different name. `object` will do." Not
  the OO instance sense. It refines to a specific kind the way a node
  deepens, and a node may not reach `status: settled` still carrying
  it — the settle-guard, enforced by `check_plans.py`. The framework
  definition is `PRIVATE/PlanPlan/framework/PROTOCOL.md`
  §3a.

**Only `code` designations have concrete influence** (the owner). They are
the ones that bind a node's name to an identifier. The rest are
descriptive — but they still have to be accurate, or the field is
noise on three-quarters of the tree.

### The non-code designations

the owner's original word was `meta-logic`, for "something that isn't code
but determines the use of code or development of code", and he is
not attached to it. That sentence splits cleanly, and each half
behaves differently enough to earn its own name:

- **`rule`** — determines the USE of code. Settled policy, not
  scheduled work. Its PROGRESS should not move; if it does, the rule
  changed and that is a decision, not progress.
  - The follow-or-wrap rule. The border lattice. The construction
    grades. "Ingest never guesses; it writes unresolvable."
- **`work`** — determines the DEVELOPMENT of code. Something to be
  done. Its PROGRESS is the file that moves.
  - `construction`, `rust_llvm`, the three run stages. Not code —
    they are performed WITH code.
- **`finding`** — what was learned, and the data it produced. Points
  at evidence outside the tree.
  - `intentions` (the data), `lessons`, `research`'s entries.
- **`grouping`** — exists to hold sub-nodes and say what they have in
  common. Thin by design.
  - `tools`, `research`, `examples`. This one earns its name by
    turning off the "definition only" warning: a grouping node with
    forty words is finished, not neglected.

Four rather than one because each changes what a reader does with
the node. A single umbrella would make the field say "not code" and
nothing more.

**APPROVED by the owner, 2026-07-31.** The set was Claude's proposal
replacing `meta-logic`; the owner approved all four names and the count as
written. `rule` / `work` / `finding` / `grouping` are settled
vocabulary, not a suggestion.

### The designation plus the address gives the qualified name

This is what makes the mapping trivial rather than merely
consistent. A node's designation says what kind of thing it is; its
position says what owns it. Together they give the code reference.

```
node_0_0_0_ledgerer        designation: code (module)
    node_0_0_0_0_ledger    designation: code (class)
        node_0_0_0_0_0_build   designation: code (method)
```

reads as `ledgerer.Ledger.build` without anyone writing that down.
It is also exactly the dotted form the communication protocol §2
already uses for talking about structure — `ClassName.method_name`.
The plan tree produces those references; it does not need a separate
notation for them.

### What follows from rule 1

- **Node names must be valid identifiers.** Lower case, underscores,
  no spaces or punctuation. The existing node folder grammar already
  produces this; the rule makes it load-bearing rather than
  incidental.
- **Renaming a plan node renames code.** Under this rule a rename is
  not tidying — it is a refactor with a blast radius. That raises the
  cost of a casual rename and lowers the cost of a careful one,
  which is the correct trade.
- **A name that is wrong in the plan is wrong in the code.** Getting
  the name right at plan depth, before any logic exists, is the
  cheapest moment to get it right at all.
- **The name is the same; the folder path is not.** A plan node lives
  at `node_0_0_0_ledgerer/`; the code lives at `Tools/ledgerer/`. What
  transfers is the name and the ownership chain, not the location on
  disk.

### Names are settled; shape is aimed at

Rule 1 settles names. It does not settle the tree's shape (the owner,
2026-07-31):

> it might be impractical to enforce a 1:1 for everything. planning
> has some flexibility but yeah trying to match things so that code
> is a trivial mapping from planning is the central idea.

So:

- **A 1:1 correspondence between plan nodes and code objects is the
  target, not a rule.** Planning is allowed structure that has no
  code counterpart, and code is allowed detail that has no node.
- **The test is "is the mapping trivial?"** — could someone holding
  the plan write the code without inventing names or guessing what
  owns what. Not "does every node have exactly one object."
- **Where the two diverge, the divergence should be visible**, not
  discovered later. A node with no code counterpart carries a
  non-code designation and is therefore accounted for. Code with no
  node is the case to watch, because that is structure nobody
  reviewed.

---

## 2. Depth

### How the owner codes

Start at the highest level. Write the shape — what the objects are,
what they hold, what they can do. No logic. Then go one level down
and do it again for each of those. Keep descending. Detailed code
gets written only at the very bottom, where logic is genuinely
required and there is nothing left to decompose.

This is the same shape as the planning framework, deliberately. The
completeness rule of that framework — *a reader who stops at any
level has a correct, just coarser, picture* — is also the rule for
the code.

### The bridge already exists

The structural overview format in
`PRIVATE/DevComms/LLM_communication_protocol.md` §2 — class
name, attributes, methods, no logic — **is a plan node one level
above code.** It was never a separate request format. It is what a
node looks like at the depth where the next descent produces a file.

### The readiness test

A node is ready to become code when descending one more level would
add logic rather than structure.

- Some nodes in the current plans are already there, or close.
- Some are three levels short and would need those levels written
  first.
- **A node that is not ready does not get coded.** It gets deepened.
  Reaching for the editor when the plan is two levels shallow is
  exactly the move this document exists to stop.

### What "logic last" buys

At every level there is a reviewable artifact, and the thing being
reviewed is the thing that is expensive to get wrong: the shape and
the names. If the shape is wrong you find out while the only cost is
a rename. If logic arrived first, you find out after the logic is
written against the wrong shape, and the logic is what you throw
away.

---

## 3. What this replaces, and why

The method being retired is the one an LLM defaults to: produce the
whole working artifact in one pass — structure, names, logic,
imports, tests — and present it finished.

the owner's judgment, stated plainly: this has caused more project failures
than successes, and he cannot recall the last time it worked.

The mechanical reasons, so this is not just a preference:

- **The shape is never reviewed.** It arrives already committed to,
  buried inside working code. Reviewing it means reading the logic
  and inferring the shape back out, which nobody does.
- **The names are never agreed.** They are chosen mid-generation by
  whatever the model reached for, and by the time they are visible
  they are already used in fifty places.
- **When it is wrong, it is wrong all the way down.** There is no
  coarser artifact that survives, because none was ever produced.
  The whole thing is discarded together.
- **It is opaque.** A file that appeared complete cannot be checked
  level by level, so it gets checked by running it — and passing
  tests say nothing about whether the shape or the direction was
  right. This project has already had exactly that failure twice:
  work aimed at a retired backend that passed every test, and a bulk
  rename that broke a data key while the suite stayed green.

None of this is an argument that the fast method produces bad code
in the small. It is an argument that it produces unreviewable
structure in the large, and structure is what the owner decides.

---

## 4. What this means for the current plans

Both trees were written before this was stated, so they were written
to describe rather than to name. Expect:

- Nodes whose names read as descriptions of a thing rather than as
  the thing's identifier.
- Nodes describing code objects that stop several levels above the
  depth where code could begin.
- Nodes that are not code objects at all, currently indistinguishable
  from ones that are.
- Some nodes already at or near coding depth. The rust/llvm slice
  node is close; the three tool nodes in PseudoIR are not.

That update is a separate job with a separate conversation, working
from this document.

---

## 5. Settled, 2026-07-31

- **The `designation` field**, its comma-separated form, and its
  code kinds — module, class, method, attribute, function, variable.
  A seventh, `object`, was added 2026-08-01 as the coarse kind (§1
  above); the six settled here are unchanged by it.
- **Required on every node**, not only the ambiguous ones.
- **Only `code` designations have concrete influence.** They bind a
  name to an identifier; the rest describe.
- **How far the sameness goes** — answered by the same field. A node
  says what kind of code object it is; the tree shape follows from
  the designations rather than from a fixed rule about what a class
  node's sub-nodes must be.
- **Shape is aimed at, not enforced.** Trivial mapping is the target;
  1:1 is not required.
- **The protocol carries the standing instruction**, as card `scope.code-shape` (v1 §2a) of
  `PRIVATE/DevComms/LLM_communication_protocol.md`, beside the
  structural overviews.
- **The four non-code designation names** — `rule`, `work`,
  `finding`, `grouping` — approved by the owner as proposed, names and
  count both. `meta-logic` is retired.
- **A `code (...)` node MAY carry `rule` sub-nodes, and a rule may
  equally be a section inside the code node's CORE.** the owner, when asked
  which: "either. code and non-code designations are first class
  citizens in the PlanPlan spirit." Both spellings conform; the
  choice is per case, on which reads better.
- **Every designation is a first-class citizen.** `code` designations
  are the only ones with concrete influence, but influence is not
  rank — a `rule`, `work`, `finding` or `grouping` node is as
  legitimate as a `class` node. Written into
  `PRIVATE/PlanPlan/framework/PROTOCOL.md` §3a, 2026-07-31,
  because the protocol carried the spirit only by implication and the owner
  asked for it to be stated.

## 6. Still open

- **The renderer does not yet require `designation`.** The check is
  one line, but adding it now would report every node in both trees
  as defective, since none carries the field yet. It goes in with the
  tree update, not before.

## 7. Methods do not need the instance by default (2026-08-01)

Moved here 2026-09-06 from the communication protocol (v2 §6.3),
because it is a rule about how code is shaped, and this file is
where that is stated. The protocol's `scope.code-shape` card points
here.

A method is written so it does not need the object it sits on,
unless it genuinely does. Two legal spellings, chosen per case:
`@staticmethod` on the class (keeps the `ClassName.method_name`
address, takes no `self`), or a plain module function.

Why — **ontological independence**: the owner decides the ontology and
expects to decide it again; a class splitting in two is a normal
event. A method full of `self` is welded to its class and must be
rewritten to move. A method taking its inputs as arguments moves by
cut and paste. Data stays in the objects; behaviour stays movable.

The limits are part of the rule:

- A design contorted to stay static has paid a real cost for an
  imagined one.
- Sometimes the welded version is cheaper now and refactored later.
  That is a legitimate outcome, not a breach.
- When the method genuinely is about that one object's state, write
  the instance method and give the reason in one line.

```
ontological independence
    behaviour that does not depend on which
    class currently owns it, so moving it
    between classes costs a rename rather
    than a rewrite.
    example tied to context:
        a node chain reading as
        `ledgerer.Ledger.build` — if
        `Ledger` later splits in two, an
        independent `build` moves to either
        half by changing its node position
        and call prefix; a `build` full of
        `self` gets re-written instead.
```
