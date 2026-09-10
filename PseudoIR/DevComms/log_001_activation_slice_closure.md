# log 001 — does an activation-derived slice close?

2026-07-31. Written because the owner asked for the closure objection to be
explained, after it was recorded in one line in
`PRIVATE/PseudoIR/Planning/node_0_0_tools/node_0_0_1_slice/SUPPORT_brainstorm.md`.

This log explains the objection and proposes a fix. Nothing here is
settled.

---

## 1. The model first

Three things have to be on the table before the objection makes
sense.

- **What a slice is meant to be.** All the code in a source compiler
  that implements one intention. For Rust's signed integer division,
  that is every arm, guard, and helper rustc uses to decide what
  `a / b` does for two signed integers — including the arms for the
  cases that almost never happen.
- **What the detector approach measures.** Run a test module; each
  detector that fires records that its node executed; the nodes that
  fired become the slice. So the definition is:

      slice = { nodes that activated while test module T ran }

- **What a test suite is.** A finite set of cases the compiler's
  authors thought to write. It is not a proof of coverage, and no
  test suite claims to be. rustc's test suite is very good; "very
  good" is not "every path".

---

## 2. The objection in one sentence

If a path implements part of the intention but no test in T drives
it, that path never activates, so it is not in the slice — and the
obvious test for the slice is T, which cannot detect its absence,
because the slice was defined as exactly what T exercises.

---

## 3. The mechanism, step by step

Worked on a case this project has already had to reason about by
hand: `i64::MIN / -1`.

1. **The intention**: Rust's signed integer division. In rustc's
   source this is a routing decision with several arms — normal
   division, division by zero, and the overflow case where
   `MIN / -1` has no representable answer.
2. **Suppose the test module does not cover MIN / -1.** This is not
   a strawman: it is the exact case that is easy to leave untested,
   which is why this project ended up ruling on it by hand rather
   than reading it off a suite. The ruling is recorded at
   `PRIVATE/PseudoCoup_v6/AgentMemory/02_decisions.md` — "T4
   MIN/-1 — RESOLVED (the owner, 2026-07-28): TRAP", with the note that
   PCv5's `srem(MIN,-1)=0` was a machine-level guard rather than
   Rust surface semantics. Two different systems disagreed about this
   case; that is what a hard edge case looks like.
3. **Run the tests.** Every arm the tests drive lights up. The
   overflow arm does not, because nothing drove it.
4. **The slice is cut.** It contains normal division and
   division-by-zero. It does not contain the overflow arm. Nothing
   announces this — a detector that never fires produces no record,
   and an absent record looks exactly like a node that was correctly
   excluded.
5. **The hub now has Rust division that is right for every input the
   tests covered and silently wrong for MIN / -1.**
6. **Check the slice with T.** All green. Necessarily green.

---

## 4. Why step 6 is the real problem

An ordinary gap is found by testing. This gap cannot be, as long as
the test is T.

- **The slice was defined as what T exercises.** Every node T needs
  is in the slice by construction. So T passing tells you nothing
  you did not already know the moment you cut the slice — it is the
  same measurement run twice.
- **This is not a weak test. It is structurally incapable of
  failing** in this way. Strengthening it is not available: any case
  you add to T changes the slice rather than testing it, because the
  new case activates nodes and those nodes join the slice.
- **The failure is silent at every stage.** No detector reports, no
  test fails, no warning prints. The first symptom is a wrong answer
  in an application, with nothing anywhere pointing at division.

The general shape: **the selection criterion and the acceptance
criterion are the same measurement.** A ruler made out of the thing
being measured always reports that the thing is the right length.

This is why the objection is worth raising against an idea that is
otherwise very attractive. The proposal's biggest strength — the
slice is observed, not judged — is exactly what creates the
circularity, because an observation of a run can only ever see what
that run did.

---

## 5. What already guards against it

One recorded rule covers the acceptance half, and it was written
before this idea existed.

`PRIVATE/PseudoCoup_v6/AgentMemory/02_decisions.md`,
"Past-project oracles INFORM, never ANCHOR (the owner, 2026-07-28)":
legitimate anchors are "expectations written from the compiler
source / CPU manual, execution-based semantic results, and the live
source compiler itself (rustc)".

Read against this proposal: **T may select the slice, but T may not
be what accepts it.** Acceptance has to come from a source that did
not participate in the selection — the language reference, the CPU
manual, or live rustc run differentially against the hub. That rule
already forbids the circular arrangement.

It does not, however, solve the problem. It means the wrong slice
fails its acceptance test instead of passing it — which is a real
improvement, and still leaves you holding a slice with a hole and no
information about where the hole is.

---

## 6. Proposed fix: diff the two graphs

This is Claude's proposal, 2026-07-31, not part of the owner's idea.

The ledgerer produces a **structural flow graph** — derived from the
code without running it. The detector run produces a **live flow
graph** — what actually executed. The proposal so far uses only the
second. Both exist.

Subtract one from the other:

    reachable-but-never-activated =
        (structural graph, bounded to the region) − (live graph)

That difference is a **named list of every arm the tests did not
take**. It converts the hole from invisible into an item on a review
queue.

What that buys, concretely:

- **The MIN / -1 arm appears on the list.** It is structurally
  present in the routing region and never fired. A human — or a
  later automated step — looks at a short list of unexercised arms
  instead of at the whole compiler.
- **The slice's shape becomes a claim that can be argued with.**
  "These 4 arms were not exercised; 3 are error-reporting paths we
  deliberately exclude, 1 is the overflow case and belongs in."
- **The automation boundary stays where it was ruled.** The recorded
  position is imprecise-but-safe by default: "cut generously +
  asserted stubs". A never-activated arm can be cut IN generously
  and given an assertion, rather than cut out silently.
- **It is a coverage measurement, which is a thing with prior art**,
  rather than a new invention.

So the reframing is: **what lit up is the slice; what did not light
up is the review queue.** The live graph alone is dangerous. The live
graph diffed against the structural graph is a coverage report, and
a coverage report is exactly the artifact whose absence makes step 4
silent.

---

## 7. Still open

- **How is the structural region bounded?** The subtraction needs a
  boundary or the "never activated" list is the entire compiler minus
  the slice. This may be where the retired seam declaration comes
  back, in a weaker form — not "where does the slice start" but
  "what region are we measuring coverage over".
- **Who rules on an unexercised arm, and by what standard?** The list
  is only useful if there is a way to decide each item. That decision
  looks like the human judgment the proposal was trying to remove,
  though over a far smaller surface.
- **Can generated inputs drive the uncovered arms?** Naming the
  unexercised arms is less than reaching them. the owner's answer, and his
  own design for it, is in
  `PRIVATE/PseudoIR/DevComms/log_002_directed_input_generation.md`.

## 8. CORRECTION, 2026-07-31

This section originally ended by pointing at a past project's fuzzer
as a component to build this on. **That was wrong and is retracted.**

the owner, 2026-07-31: "past project oracles are for verify correctness.
they absolutely will not be used to develop things around ... dont
ever suggest the use of past projects to build dependencies on ever
again."

The recorded rule quoted in §5 above says past-project oracles inform
and never anchor an acceptance test. Today's ruling is stronger and
governs: a past project may be checked AGAINST, and nothing may be
BUILT ON. Naming one as a source of machinery is the error, whatever
the wording around it. The hardened rule is recorded at
`PRIVATE/PseudoCoup_v6/AgentMemory/02_decisions.md` under
Direction.

The retracted text is not restored here because the point of the rule
is that the suggestion should not have been made; §5's citation of
the older rule stands, since it is an accurate quote of what was
recorded then and is now superseded by the harder form.
