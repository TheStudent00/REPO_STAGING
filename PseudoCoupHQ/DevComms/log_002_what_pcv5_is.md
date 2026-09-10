# log 002 — a proposal for what PseudoCoup version 5 is

2026-07-31. the owner asked for a proposed `CORE_0` definition for the
rebuilt PCv5, derived from what he has already said rather than
invented.

**This is Claude's proposal. Nothing here is settled.** Section 2
shows the derivation so the reasoning can be checked rather than
taken, and section 5 names the one thing that cannot be derived and
needs the owner.

---

## 1. The proposed definition line

> **PseudoCoup version 5 — the PseudoCoup that serves PseudoIR.**
>
> it transpiles a source COMPILER into hub source, so PseudoIR has
> something to slice. it is built by Frankensteining all the
> PseudoCoup research into one transpiler and one ledgerer, and it
> runs before a hub exists.

And the co-statement it implies, for the tree above:

> **PseudoCoup version 6 — the PseudoCoup that serves applications.**
> it transpiles ordinary PROGRAMS in the 12 languages into the
> finished hub.

Same machinery, two consumers. That is the "decent amount of overlap"
the owner predicted, and it is not accidental — it is the *generalize then
specialize* rule showing up as two version-states of one lineage.

---

## 2. Where each part comes from

Nothing above is new. Each clause traces to something recorded.

- **"Serves PseudoIR" / holds the Frankensteins.** the owner, 2026-07-31:
  "PseudoIR is meant to use the most advanced Frankenstein transpiler
  and ledgerer. we will make that Frankenstein transpiler and
  ledgerer part of PCv5."
- **"Built by Frankensteining all the PseudoCoup research."** the owner,
  same day: "we will gather all the PseudoCoup research and
  Frankenstein them together to build version 5." The parts list
  already exists as the harvest maps in
  `PRIVATE/PseudoCoup_v6/AgentMemory/03_lineage_and_harvest.md`.
- **"Precursor" and "runs before a hub exists."** the owner: "we can safely
  commandeer it to be the pre-cursor to PCv6." And the cycle recorded
  at
  `PRIVATE/PseudoCoupHQ/Planning/node_0_1_exchange/CORE_0_1_exchange.md`
  opens: "a hub-less PseudoCoup builds the first PseudoIR." **That
  hub-less PseudoCoup had no name until now.** This proposal is that
  it is version 5.
- **"Transpiles a source COMPILER."** Follows from the two above
  rather than being asserted. The exchange node says PseudoCoup gives
  PseudoIR a transpiler because "PseudoIR has to get a compiler's
  source into hub source before it can slice it." If PCv5 is the
  PseudoCoup that gives PseudoIR its transpiler, then compiler source
  is what that transpiler eats.
- **Version 6 as the application half.** The capability ladder in the
  archived dashboard already separated these as rows 4 and 5 —
  "Transpile COMPILER source into the hub" and "Transpile APPLICATION
  source into the hub", the latter marked "not started in PCv6 ... the
  actual 'convert the 12 languages' scripts' capability". The split
  this proposal makes is that same line, drawn between two repos
  instead of two rows.

### Why this reading rather than "before the hub / after the hub"

Both fit the word precursor. They turn out to be the same split, so
the choice does not matter: the transpiler PseudoIR needs is the one
that runs with no hub AND the one that eats compiler source. One
tool, described two ways. Recording it as the compiler/application
split is preferred only because it says what the thing DOES rather
than when it runs.

---

## 3. What this makes the overlap, concretely

the owner: "its a pre-cursor so it is going to have a decent amount of
overlap."

Shared, and deliberately so — this is the *generalize then
specialize* rule:

- tree-sitter parsing and the pinned grammars
- the ledgerer, node identity, the UR-AST
- polyfill, since both halves need source behaviour matched

Different:

- **What is eaten.** A compiler's source versus an ordinary program.
- **Whether calls are followed.** Already a settled distinction:
  compiler transpiling chases callees across files under the
  follow-the-calls rule; application-script transpiling does NOT
  chase imported modules, because that is "often logically and/or
  legally impossible" (the owner, 2026-07-28, recorded in
  `PRIVATE/PseudoCoup_v6/AgentMemory/02_decisions.md`). **That
  one recorded rule is the sharpest line between the two versions,
  and it was written before this split was proposed.**
- **What is targeted.** A stub hub surface versus the finished hub.

---

## 4. What it would mean for the repos

- PCv5 gets a `Planning/` tree it currently lacks, and becomes the
  home of the Frankenstein transpiler and Frankenstein ledgerer.
- PseudoIR's borrow re-points at PCv5. Its
  `PSEUDOCOUP_ROOT` currently defaults to
  `PRIVATE/PseudoCoup_v6` — under this proposal it would come
  to mean version 5. That was already flagged as unsettled in
  `PRIVATE/PseudoIR/Agent_Memory.md` §4 and this would settle
  it.
- PCv6 keeps the goal it already states — the 12 languages into the
  hub — and stops being the place compiler ingestion lives.

---

## 5. RULED 2026-07-31 — parts come from anywhere

the owner: "PCv5 Frankenstein parts can be from anywhere."

So the question below is answered: PCv6's existing tools are eligible
like anything else in `~/Programming`. There is no privileged source
and no excluded one — the harvest maps range over the whole lineage,
and version 6's tools are simply its newest entries rather than a
special case.

What this does NOT license, and the distinction matters because the
two rules look contradictory at a glance:

- **Harvesting a component is moving code IN**, with a provenance
  header and its own acceptance test, after which the source repo is
  irrelevant to whether it runs. Recorded method: "T3 fresh spine,
  mining the lineage — no wholesale port of any version-base;
  components transplant with provenance headers and acceptance tests
  (precedent: WFL 'mine, don't resurrect')."
- **Building on a past project is leaving code THERE** and depending
  on it — calling into it, anchoring a test on it, treating it as a
  live component. That is banned outright (02_decisions, Direction,
  first entry).

The test between them: **after the harvest, can the source repo be
deleted without anything breaking?** If yes it was a transplant. If
no it was a dependency, and it is not allowed.

That test also names the one live violation, which predates this
ruling: PCv6's suite currently cannot pass without PCv5 on disk,
because six tests resolve vendored rustc source through `PCV5_ROOT`.
By the test above that is a dependency, not a transplant, and it is
already on the administrative list to fix by vendoring those sources
in.

### The original question, kept for the record

**What happens to PCv6's existing tools.**

`PRIVATE/PseudoCoup_v6/Tools/` holds `ledgerer` (with
`tree_sitter` inside it), `transpiler`, and `polyfill`, green at 95
tests. All of that is compiler-facing: the transpiler's live ingestor
is the LLVM C++ encoder, which eats compiler source.

Under this proposal that work belongs in version 5. Three ways to
take it, and this is exactly the kind of thing that should not be
guessed:

- **They ARE the Frankenstein seed** — move to PCv5 and get composed
  with the harvested parts. PCv6 empties out and refills with
  application ingress. Most consistent with the proposal; largest
  move.
- **They stay, and PCv5 is built fresh** from the harvest maps. Two
  ledgerers exist for a while. Least disruption now, most
  duplication later, and duplication of exactly the kind this line
  keeps getting hurt by.
- **The split is wrong** and version 5 is something else — in which
  case sections 1 to 4 fall with it.

---

## 6. Confidence

The definition line in §1 is a reading of things the owner has said, and
every clause is traceable in §2 — but the join between them is mine.
He has never said "PCv5 eats compilers and PCv6 eats applications" in
those words. If that sentence is wrong, say so plainly and the rest
comes apart cleanly, because nothing has been built on it.
