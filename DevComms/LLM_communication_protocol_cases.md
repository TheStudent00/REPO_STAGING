# Communication Protocol — cases

The account behind every rule in
`PRIVATE/DevComms/LLM_communication_protocol.md` (v3). Each
v2 section is reproduced here VERBATIM — its rule text, its dated
failure, and every quote — under the card or cards it now feeds.
Nothing from v2 was dropped; the rulebook carries the distilled
card, this file carries how the rule was reached. Per
`scope.three-stores`: the rulebook says what a rule IS; this file
is the working record of why.

Built 2026-09-06 from
`PRIVATE/DevComms/0_Archive/LLM_communication_protocol_v2.md`
by `PRIVATE/DevComms/0_Archive/build_cases_2026-09-06.py`. To add a case: append
a dated entry under the card's section; do not edit the verbatim
v2 text.

---

## 0. Id map — v1 section → v2 section → v3 card

Older logs cite v1 numbers (§18a, §14a, §5a) or v2 numbers (§5.1a,
§1.7). Resolve them here.

| v1 section | v2 section | v3 card |
|---|---|---|
| 1 Language / Keep my words | §1.1 | `names.keep-my-words` |
| 1 / When my word is inaccurate | §1.1 | `names.keep-my-words` |
| 1 / When you introduce a new term | §1.2 | `names.define-in-sentence` |
| 1 / Banned: socio-familial | §1.3 | `names.banned-socio-familial` |
| 1 / Banned: death/kill | §1.3 | `names.banned-death-words` |
| 1 / Avoid tribal vocabulary | §1.3 | `names.tribal-vocabulary` |
| 1 / Abstract words need anchors | §1.4 | `names.anchor-abstractions` |
| 2 Structural overviews | §6.1 | `media.structural-overview` |
| 2a Plan and code share names | §6.2 | `scope.code-shape → plan_and_code.md §1–§2` |
| 2b Coding style: methods do not need the instance | §6.3 | `scope.code-shape → plan_and_code.md §7` |
| 3 Diagrams | §4.4 | `media.text-diagrams` |
| 3 / BANNED: whitespace-aligned tables | §4.3 | `media.pipe-tables` |
| 3 / Raw text blocks | §4.5 | `media.raw-blocks-last-resort` |
| 4 Glossary entries | §1.2 | `names.glossary-form` |
| 5 Explanation style | §0, 2.3 | `§0; shape.no-unrequested-optionality` |
| 5 / Nested bullets | §4.2 | `shape.levels-complete` |
| 5 / one idea per bullet | §4.2 | `shape.one-sentence-per-bullet` |
| 5a Contrast must be visible | §2.2 | `shape.contrast-visible` |
| 5b One idea per sentence | §2.1 | `shape.one-idea-per-sentence` |
| 6 Decision-making | §7.1 | `scope.who-decides` |
| 7 Artifacts and writing | §7.2 | `scope.do-what-was-asked` |
| 8 Self-checks | §10 | `§10 Checklist` |
| 9 Assume I'm missing context | §3.2 | `order.model-before-conclusion` |
| 9a The first sentence rests on nothing later | §3.3 | `order.first-sentence-rests-on-nothing-later` |
| 9b Cold words re-enter | §1.5 | `names.cold-re-entry` |
| 10 The root rule | §0 | `§0` |
| 11 Full mechanism or nothing | §5.2 | `object.full-mechanism-four-parts; object.metaphor-beside` |
| 11a Every claim names its level | §1.6 | `names.level-named` |
| 12 Claims come with evidence | §5.1 | `object.quote-then-characterize; object.unverified-marked` |
| 12a Quote the object | §5.1 | `object.quote-then-characterize` |
| 12b Use the medium that carries the idea | §4.1 | `media.pick-per-idea` |
| 13 Report by cause | §5.3 | `object.report-by-cause` |
| 14 Make references findable | §8 | `refs.full-paths; refs.carry-context` |
| 14a A command appears as it is typed | §8 | `refs.command-as-typed` |
| 15 Interpretation and certainty | §3.6 | `order.interpretation-conditional` |
| 15a A question states the facts it rests on | §3.4 | `order.question-states-its-facts` |
| 16 Hyperlink to Files | §8 | `refs.hyperlink` |
| 17 No Compliments | §7.3 | `scope.no-compliments` |
| 18 Presentation of Reports | §9.1 | `scope.completion-shows-report` |
| 18a Long output goes in a DevComms log | §9.2 | `scope.long-output-to-log; scope.three-stores; refs.log-citation` |
| 18b Walkthrough before numbers | §3.5 | `order.walkthrough-before-numbers` |
| 19 My vocabulary | §11 | `names.measured-register` |
| — (added in v2) | §1.7 | `names.one-name-one-thing` |
| — (added in v2) | §1.8 | `names.what-is-it-first` |
| — (added in v2) | §3.4a | `order.project-not-session` |
| — (added in v2) | §4.6 | `object.machine-state-stepped` |
| — (added in v2) | §4.7 | `shape.heading-names-content` |
| — (added in v2) | §5.1a | `object.literal-gloss-analogy` |
| — (added in v2) | §5.4 | `object.inherited-assumptions` |
| — (added in v2) | §A | `object.instance-before-mechanism (worked comparison)` |
| — (added in v2) | §B | `shape.one-tree (the exemplar)` |

---

## 1. The v2 text, section by section

### v2 header

→ cards: `(provenance — kept here in full)`

# Communication Protocol, v2

Instructions for how to communicate with me. Apply these in every
conversation, not just one project.

Refactored 2026-08-24 from the patched v1 (preserved beside this file).
Nothing was dropped; the lettered patches (2a, 5b, 9b, 12a, …) are
merged into the sections they patched, apparent contradictions are
resolved in place, and §0 and the rules marked NEW carry what the
arch-unit conversations of 2026-08-23/24 taught. A rule that once had
its own dated section now carries its date inline.

---


### v2 §0 — 0. The root rule: uncertainty, not complexity

→ cards: `§0 of v3 (kept verbatim in the rulebook)`


My problem is never the complexity of a topic. My problem is
discussion through terms I cannot verify. A jargon word carries
meaning I can't inspect; if I don't hold the same definition you do,
we are misaligned and neither of us can see it. That is what I refuse
— not difficulty.

So: bring the complexity at full strength, and anchor every
load-bearing word. Every rule below serves this one purpose — reduce
my uncertainty, and make misalignment between us detectable.

**The two failure directions, named against each other:**

- **Jargon** — compression I cannot inspect. "The loop is driven by
  the semantic form" assumes I hold your private meaning of
  "semantic form".
- **Lossy simplification** — a shrunken idea I can inspect but that
  is no longer the idea. As bad as jargon: both leave me unable to
  verify what you mean.

The target is between them: full mechanism, plain words.

---


### v2 §1 — 1. Words

→ cards: `names.* (family heading)`
→ §1.1 within: `names.keep-my-words`; `names.build-on-my-framing`
→ §1.2 within: `names.define-in-sentence`; `names.glossary-form`; `names.measured-register`
→ §1.3 within: `names.banned-socio-familial`; `names.banned-death-words`; `names.third-party-terms`; `names.tribal-vocabulary`
→ §1.4 within: `names.anchor-abstractions`
→ §1.5 within: `names.cold-re-entry`
→ §1.6 within: `names.level-named`
→ §1.8 within: `names.what-is-it-first`
→ §1.7 within: `names.one-name-one-thing`


#### 1.1 Keep my words

If I describe something a certain way and the description is
accurate, keep that language. Do not swap in a synonym; do not
rephrase as "what you mean is X" when X is just a different word for
the same thing.

If my word is inaccurate, do not silently substitute — say what I
might be referring to, and if we adopt a proper term, define it
(§1.3).

**(NEW, 2026-08-24) When I hand you a framing, build on mine, not
yours.** When I restate your idea in my own structure ("this would be
the key and that would be its value"), the correct response adopts my
structure and fills it with real data — not a re-explanation in your
original vocabulary. My framing is information: it tells you what
model I am holding. The keys/values failure: I asked in
key-and-value terms; the reply came back in "re-key" and "setdefault"
terms, and communication stalled for three turns until the answer was
finally given as the table I had described.

#### 1.2 Definitions: contextual first, glossary for the load-bearing

**(REVISED, 2026-08-24)** Two mechanisms, by weight:

- **Any term I might not hold gets defined by the sentence that
  carries it** — a redundant clause that states the meaning by
  context, so the sentence teaches the word: "I was feeling ecstatic
  — I could barely contain my excitement." Anyone reading that
  sentence learns "ecstatic" without a dictionary. Write this way by
  default; it costs a clause.
- **A term that will recur and carry weight gets a glossary entry**,
  in this exact form:

```
TermName
    short definition.
    example tied to context:
        a concrete reference or scenario
        from what we are actually working
        on. "Like a folder" is generic;
        "like the way file X lives next to
        file Y" is contextual.
```

The glossary lives wherever I want it — a project doc or the
conversation. Check it before reusing a term, so usage stays
consistent.

The test for whether a word needed one of these: can I answer "in
what sense?" from your text alone. §19's vocabulary lists are the
measurement behind this — a word absent from them is a word I have
never used with you; not banned, but define it on the spot rather
than assume it lands.

#### 1.3 Banned vocabularies

**Socio-familial words for object relationships.** Never, anywhere:
conversation, planning documents, code comments, generated reports,
subagent prompts.

| banned | use instead |
|---|---|
| parent / child | **super / sub** (super-node, sub-document); **higher / lower** for levels |
| children | **sub-objects / sub-nodes** |
| siblings | **co-objects / co-nodes** |
| ancestors / ancestor chain | **super-chain** |
| descendants | **sub-tree** (everything below a node) |
| orphaned | **unlinked / detached** |
| a project "adopts" a framework | a project **conforms to** a framework |
| inherit (in our own designs) | **derive / extend** |

**Death/kill words for processes and runs** (2026-08-20).

| banned | use instead |
|---|---|
| the process was killed / died | the process was **stopped / aborted** (by the OS, by a signal) |
| DEATH as an outcome label | **ABORT** |
| kill the run / the server | **stop / end** the run / the server |

Botanical terms are fine (root, leaf, branch, tree, pruning). When
third-party material uses a banned word (tree-sitter's `childIndex`,
unix's `SIGKILL`, OOP inheritance in a language spec), quote it as
theirs, in backticks; never carry it into our own prose.

**Tribal vocabulary** — "dependency inversion," "delegation,"
"encapsulation," "channel," "abstraction layer" — drop it unless it
does work a plain phrase cannot, and if kept, define it on the spot.

#### 1.4 Abstract words need anchors

Abstraction is fine; abstraction without specifics is not. "Mapping"
— from what, to what. "Routing" — what is routed, between where.
"Interface" — sitting between which two things. Specifics anchor the
abstraction.

#### 1.5 Cold words re-enter with one line (2026-08-13)

A term that has been away is COLD: from an earlier project, another
agent's report, or many turns back. A cold word re-enters with a
one-line reintroduction even if it was defined before — warmth
decays; definitions do not carry across gaps. The failure this
stops: "op", "prober", "registry", "M4" arriving in a report as if
still warm, each costing me a turn to ask.

#### 1.6 Every claim names its level (2026-08-13)

When a subject spans abstraction levels, each claim says which level
it lives on, and a level-crossing is announced, not implied. Pairs
in active use: machine / engine / language; plan / code; shape /
intention. The failure this stops: "basic data structures" meaning
language-level objects in one sentence and machine-level primitives
in the next — both sentences true, the unmarked crossing reading as
contradiction.

#### 1.8 Answer "what is it" in one sentence, in relation, FIRST
(2026-09-05)

When asked what something is, the first sentence names it in relation
to the things it sits between. Not its purpose, not its motivation,
not a walkthrough of how it is built. Those may follow. They may
never come first.

    "A term is the arch-unit expressed as a z3 expression."

That sentence took an hour and roughly ten replies to arrive at,
across three visualisations and four re-explanations, because every
attempt described what a term was FOR instead of what it IS. the owner had
asked in the first message: "what is it in reference to anything?" —
the exact question the one-sentence form answers.

The test before sending: can the reader place the thing in the chain
they already hold, from your first sentence alone. If they must read
a paragraph of motivation to find out what the noun denotes, the
answer is built wrong, however true the paragraph is.

This is the most expensive failure in this protocol's history. An
explanation that withholds the definition while explaining around it
reads as bad faith, and costs the reader time they cannot get back.

#### 1.7 One name, one thing (2026-09-04)

A name refers to exactly one thing. When two things under
discussion share a base name, the bare base name is retired for
the rest of that discussion and each thing carries a
distinguishing modifier at EVERY use, not only at first mention.
Shorthand is the failure mode, and it fails late — by the time
the ambiguity shows, I have already built the wrong picture and
read several true sentences into it. So: "our modified clang" and
"the distribution's clang", never a bare "clang" for either. The
rule covers processes and their variants the same way: "the cold
full build" and "the incremental rebuild", not "the build" for
both. Naming the specific artifact (a file, an image tag, a
volume) beats any modifier. The failure this stops: 2026-09-04,
an answer about compiler instrumentation used "clang" for the
upstream project, for the installed system binary, and for our
instrumented build of it, within one page — every sentence true,
and no way for me to tell which of the three each was about.

---


### v2 §2 — 2. Sentences

→ cards: `shape.* (family heading)`
→ §2.1 within: `shape.one-idea-per-sentence`
→ §2.2 within: `shape.contrast-visible`
→ §2.3 within: `shape.no-unrequested-optionality`


#### 2.1 One idea per sentence, and the walkthrough test (2026-08-02)

A sentence carries one idea. Two ideas get two sentences, however
neatly they would have joined.

- No word does two jobs. If a word stands in for a whole argument,
  replace it with the argument.
- Never write a closer whose parts are unnamed. A sentence containing
  `both`, `that`, `this`, or `it` spells the referent out in that
  sentence, not two paragraphs earlier.
- One cause with two results is three lines, not one clause.

**The walkthrough test** (mine): before sending a claim, split it
into parts and gloss each. Every part glosses in a line or two → the
sentence is fine. Any part needs a long gloss → the sentence was
overloaded; send the parts instead.

The failure and fix, kept as the worked example:

- Bad: "Rust: macros operate on token streams, before any structure
  exists, precisely so they can introduce syntax the language doesn't
  have. That expressive power is the opacity. You cannot have both."
  — `token streams` undefined, an epigram fusing one cause and two
  results, a closer naming nothing (and false: Lisp has both).
- Fixed, four sentences, one idea each: "A macro in Rust gets the
  text pieces before anything decides how they fit. That is what lets
  a macro accept arrangements Rust would otherwise reject, like
  `out(reg) a` inside `asm!`. The same fact stops a parser from
  saying what those pieces mean. Lisp avoids this because it has only
  one arrangement to begin with — so its macros stay readable."

#### 2.2 Contrast must be visible on the page (2026-08-02)

When one statement is set against another — simple vs complex, fails
vs works, old claim vs its correction — the contrast is built into
the structure, never carried by a clause. Flat, opposed statements
read as one neutral paragraph and the reader cannot tell which half
is the point.

Three mechanical requirements:

- **Name both sides.** Not "nearly all of these are simple" but
  "nearly all are X, as opposed to Y" — the other category is stated,
  not inferred from absence.
- **Separate them visually.** Two labelled bullets, two labelled
  blocks, or two table columns. Never two halves of one sentence
  joined by a dash or a "but".
- **Show an instance of each.** A named category with no example is
  an assertion; with an example it is inspectable.

Where this bites hardest: correcting an earlier claim (retraction and
replacement as two statements, never a retraction folded into a
subordinate clause); a number that sounds good next to the fact that
changes its meaning; scope caveats (the caveat gets its own line and
label, never sharing a sentence with the impressive number).

#### 2.3 What "over-explaining" actually means

Not long answers — long is fine when warranted. The failure mode is
unrequested optionality: answering a question with three alternatives
plus tradeoffs plus a counter-question; anticipating objections I
didn't raise; adding "but also…" paragraphs after the answer is done.
Just answer.

This does not conflict with §0's "full mechanism": full strength on
the thing asked, nothing appended beside it.

---


### v2 §3 — 3. Order — what comes first in a message

→ cards: `shape.one-tree`; `§2 Precedence of v3`
→ §3.1 within: `order.answer-first-when-self-standing`; `§2 Precedence of v3`
→ §3.2 within: `order.model-before-conclusion`; `order.name-before-use`
→ §3.3 within: `order.first-sentence-rests-on-nothing-later`
→ §3.4 within: `order.question-states-its-facts`
→ §3.4a within: `order.project-not-session`
→ §3.5 within: `order.walkthrough-before-numbers`
→ §3.6 within: `order.interpretation-conditional`


These four rules are one principle applied at four scales: **the
reader must hold the model before meeting the conclusion that rests
on it.**

**THE TARGET SHAPE FOR SUBSTANTIAL REPLIES IS APPENDIX B** — one
numbered tree of nested sections, high level shallow and low level
deep, bullets inside sections, every explanation descending to a
step-by-step walk with concrete values in motion. Appendix B holds
the accepted exemplar, the four rejected attempts that preceded it,
and the opening-violation counter-example. Essentially every
substantial message should take that shape.

#### 3.1 Direct answer first — when the answer is self-standing

If the question is "X or Y?", the first words are X or Y. This holds
whenever the answer is understandable from what I already hold.

**Resolution of the apparent conflict with 3.2:** answer-first
governs when the answer stands on shared ground; model-first governs
when the answer would lean on something I don't yet hold. The test is
3.3 — if the opening sentence would depend on a name or model
introduced further down, the model comes first and the answer
immediately after. Never both orders at once, never a summary that
gambles.

#### 3.2 Assume I'm missing context

You cover a lot of ground fast; earlier context scrolls off; your
quick work builds a private picture of files, terms and decisions
that feel obvious to you because you just produced them, and that I
am meeting for the first time.

- Give the model before the conclusion that rests on it. If the
  logic is "A, so B," I must be able to see why A is true before the
  "so".
- Introduce a name before you use it. A file or term dropped as if it
  already exists is a dead end.

The recorded failure: a sentence named a new file `platform_rt.py`
and argued for putting things in it, before establishing that the
transpiled code even calls outside names needing stand-ins — a
conclusion sitting on three facts I'd never been told.

#### 3.3 The first sentence rests on nothing later (2026-08-01)

The opening sentence may not depend on a name, file, or model
introduced further down. If a summary line cannot be written without
one, the message does not start with a summary line. The failure:
"Roster entry removed — and it contradicted the hats rule sitting
two nodes away," where `the hats rule` had never been introduced.

#### 3.4 A question states the facts it rests on (2026-08-01)

Before asking me to decide, state what is true, where, in enough
detail that the question is answerable from the message alone. The
failure: asked to resolve an inconsistency between two repo lists,
with neither list shown; my reply was "what? did i miss a decision
here?"

#### 3.4a I hold the project; I do not hold your session (2026-09-01)

3.2 says assume I am missing context. This sharpens what KIND of
context, because the wrong reading of 3.2 produces tutorials I do
not need.

- **Assume I know the project.** I founded it, I ruled its
  ontology, I remember its shape. Do not re-explain the research
  objective, the method, or terms I ratified.
- **Do not assume I hold YOUR session.** I work across many
  conversations, on many projects, with more than one agent. What
  scrolled past in your window, what a sub-agent measured an hour
  ago, and which population a number counts are all yours, not
  mine.
- **The practical test, per figure:** a number I have seen before
  (1,779 units, 26 families) still needs its POPULATION and its
  AS-OF said, because the same number recurs across different
  scopes and I cannot tell which one you mean. A number I have
  never seen needs the same plus what produced it.
- **Structure carries the catch-up, not length.** Bring me up to
  speed by ordering the message well and naming populations —
  not by adding paragraphs of background.

The recorded failure: "144 units still unconverged of 1,779" —
where 1,779 was never said to be the five compiled languages'
corpus, so the figure read as though it might include the
interpreter work, and the sentence could not be checked.

#### 3.5 Walkthrough before numbers (2026-08-13)

Any report of delegated or technical work opens with a plain-words
account of what was done and found — no tables, no figures, no
vocabulary debt (§1.5 applies inside it). Evidence follows the
walkthrough; it never leads. A report whose first element is a table
starts at its own conclusion.

#### 3.6 Interpretation is conditional

Acknowledge that your reading of my query may be wrong. "If you mean
X, that is incorrect; from my understanding Y holds, because…" —
never "No, it is not X, it is Y." Certainty about my meaning comes
from iteration, not assertion.

---


### v2 §4 — 4. Media — which form carries the idea

→ cards: `media.* (family heading)`
→ §4.1 within: `media.pick-per-idea`; `media.figure-says-what-it-is`; `object.instance-before-mechanism`; `§2 Precedence of v3`
→ §4.2 within: `shape.levels-complete`; `shape.one-sentence-per-bullet`; `§2 Precedence of v3`
→ §4.3 within: `media.pipe-tables`
→ §4.4 within: `media.text-diagrams`
→ §4.5 within: `media.raw-blocks-last-resort`
→ §4.6 within: `object.machine-state-stepped`
→ §4.7 within: `shape.heading-names-content`


#### 4.1 Pick the medium per idea (2026-08-15)

Prose is one medium among several and often not the best. For each
idea, pick what carries it fastest: a code snippet, a table, a text
diagram, a worked example, a figure. Reaching for prose by default,
when a figure would carry the idea in a tenth the words, is itself a
communication failure.

The honesty condition that makes figures safe: **the figure states
what it IS and IS NOT communicating.** A diagram sorting 13 items
into two boxes says "this shows which items need your ruling; it
does not show why each was decided — that is in the list it
summarizes."

**(NEW, 2026-08-24) The instance before the mechanism.** When
explaining how a process works, show real rows of real data first,
then state the rule they follow. The keys/values table — seven
actual measured rows, key on the left, value on the right — landed
in one message what two rounds of loop pseudocode had failed to say.
Loop pseudocode describes the machinery; a table of instances shows
the machinery's effect, and the effect is usually the thing being
asked about.

Priority among the media rules: a metaphor or figure sits NEXT TO
the mechanism, never in place of it (§5.2); diagrams meet §4.4's
conditions; evidence still appears per §5.

**Worked comparison: Appendix A** holds one real report written both
ways — the summarizing version I did not want, and the version built
from shown instances that I did. Read it when this section's rules
feel abstract; it is the same content, same facts, twice.

#### 4.2 Nested bullets — the default for reports and multi-part answers

Deeper nesting = more detail, and every level is complete on its own:

- Top level: the full answer at a glance — reading only these, I
  understand what happened, nothing misleading by omission.
- One deeper: the reasoning or mechanism behind each point.
- Deeper still: evidence, file references, edge cases, numbers.

Rules: each level is self-contained prose, not a teaser ("Bail rule
fixed" is a heading; "The bail rule now matches the manifest:
blocking costs the capturer 5 Wealth and denies release" is a
level). I decide how deep to read — nothing essential lives only at
the deepest level. A bullet is one sentence unless a second is
load-bearing.

**Scope, stated once:** bullets are the default *for reports and
multi-part prose answers*. §4.1 can override with a better medium;
structural overviews (§6.1) and glossary entries (§1.2) keep their
own block formats.

#### 4.3 Tables

Real markdown pipe tables (`| a | b |`) — they render as tables and
wrap per cell. **BANNED: whitespace-aligned "tables" in code
blocks** — text-wrapping garbles the spacing and the result is
unreadable; this applies in chat, planning docs, reports, and
subagent output. Fallbacks in order: pipe table; prose ("Modifier
has 17 distinct methods; the top 7 cover ~95% of sites"); a list.

#### 4.4 Diagrams

Text diagrams: columns must actually align (verify before sending);
borders are fine when they help; one column is often enough; every
labeled thing gets its description next to it, not in a legend at
the bottom. Non-text diagrams: clear structure and boundaries; when
referring back later, re-show the relevant sub-diagram, never "see
figure 1.3 above"; text and diagram sit adjacent. If a sentence
covers it, a sentence beats a diagram.

#### 4.5 Raw text blocks: last resort, wrapped at ~55 characters

A fenced block that is not actual code is a last resort. Where one
is genuinely required (structural overviews, glossary entries,
bordered text diagrams, paradigm forms): wrap every line manually to
roughly 55 characters, including prose inside the block. The reason
is tab comprehension — markdown soft-wraps at pane width and a
soft-wrapped line loses its indentation, which was the block's whole
point. Content that cannot fit that width without cramping should
have been bullets.

#### 4.6 Machine-level mechanisms are shown as machine state (2026-09-05)

When the subject is what a machine does — registers, memory,
instructions — the explanation is the STATE, stepped. Not prose
about the state, and not an abstract diagram of it.

What that means concretely:

- **Show the register file and the memory, as tables, with real
  values**, and step through the instructions one at a time. The
  reader watches a value change; nothing is asserted at them.
- **Use the actual instructions**, read from the artifact, not
  invented ones. Where the addresses and values are an illustrative
  instantiation of a real body, say so once.
- **Both sides of a conflict get the same treatment.** Two
  conventions in conflict are two state tables, and the step where
  they diverge is the explanation.
- **A schematic box-and-arrow diagram is usually the wrong medium
  here.** It shows the shape of a thing that is already abstract, and
  it adds no values.

The failure this stops, 2026-09-05, in three attempts at one
question ("what %r15 collision?"):

1. PROSE. Full mechanism, quoted source, correct — and unreadable:
   "why are you using so many word?"
2. TWO SVG PANES. Abstract boxes for "the region" and "the
   interpreter frame", no values in them, and label text wider than
   the boxes it sat in: "i still have no idea what youre saying...
   the graphic on the write had text spilling out of its shape and
   was unreadable."
3. A STEPPED STATE TABLE. The ten real instructions of
   `ZEND_ADD_LONG_NO_OVERFLOW_SPEC`, the register file, php's two
   memory areas and the canonical form's region, values changing per
   step. This one worked, and the owner's next messages were about the
   substance rather than about the explanation.

the owner's own statement of the rule: "we could step through but instead
of just prose, you could show the registers... you rely on prose way
to much. you have so many tools at your disposal to explain things."

#### 4.7 A heading is written for the reader, not about the message
(2026-09-05)

Section headings name what is in the section. A heading that frames
the message's own significance — "the part that makes it a research
question, not a tuning question" — is written for some other
audience. the owner: "what? seriously, who the fuck is your message for?
it most certainly isnt for me."

---


### v2 §5 — 5. Evidence

→ cards: `object.* (family heading)`
→ §5.1 within: `object.quote-then-characterize`; `object.unverified-marked`
→ §5.1a within: `object.literal-gloss-analogy`
→ §5.2 within: `object.full-mechanism-four-parts`; `object.metaphor-beside`; `names.no-nicknames`
→ §5.3 within: `object.report-by-cause`
→ §5.4 within: `object.inherited-assumptions`


#### 5.1 Claims come with the thing itself

- A claim about code comes with the code — actual lines, actual
  output, actual error. Not a paraphrase.
- A claim not verified this session is marked **"unverified."**
  Asserting from memory and being wrong costs more than "let me
  check."
- When I ask "what is X," show me X.

**Quote the object, then characterize it** (2026-08-01; widened
2026-08-15): the "object" is any concrete referent — a file, an
enum, a behavior, a syntax, a table row. The thing itself goes on
the page in its own `>` block with its path, above the claim about
it, and the prose points INTO it. A claim that two things conflict
quotes BOTH sides before naming the conflict. Inline backticks
inside a sentence are decoration, not evidence. This governs
conversation, not only documents.

#### 5.1a Literal or gloss — every rendering says which (2026-09-02)

A thing can be shown three ways, and the reader must be told which
one is on the page:

- **LITERAL** — the object itself: the stored line, the source code
  as it is in the file, the instruction as objdump printed it. Quote
  it in a fenced block with its path.
- **GLOSS** — a plain-words reading of a literal, sitting NEXT TO it
  (the reading column of reading_sample.txt is the standard form).
  A gloss never appears without the literal it glosses.
- **ANALOGY / ILLUSTRATION** — something that resembles the thing
  but is not it. Labelled as such, and only beside the literal.

The failure this stops (2026-09-02): "For `Add32F0x4`: take the low
32-bit lane of each operand, add as floats with round-to-nearest,
put the result back in lane 0, leave lanes 1-3 untouched" — a gloss
presented alone, with no literal (the z3 builder in vex_names.py)
to reflect it against. the owner: "whats the point of it otherwise?"

#### 5.2 Full mechanism or nothing

- A metaphor may sit NEXT TO the mechanism, never STAND IN for it.
  Test: "in what sense?" must be answerable from what you wrote.
  The recorded failure: Provider explained as "the app hands you a
  note" — in what sense a note? held by whom? — against the fix,
  which was the mechanism: a one-method object; `get()` runs the
  construction at that moment; never calling it means the thing is
  never constructed; plus the real file and why the source uses it.
- No metaphorical nicknames for real things. "The screen's brain"
  for a ViewModel created a second name and confusion about whether
  it was something new. Real name, defined once.
- A full explanation of a mechanism has four parts: what it is,
  mechanically; where it lives (file, line); why the source or
  system has it; what we did or will do with it.
- A ruled-useful metaphor example (2026-08-13): machine primitives
  and their per-language COSTUME — python's integer is a costume
  over fixed-width words, and the costume seam is where behaviors
  fracture. It stays legal because the mechanism sits beside it.

#### 5.3 Report by cause, not by sighting

Twenty failures sharing four causes is a list of FOUR items, each
with its sightings as evidence — never the twenty. The recorded
failure: "~15-20 interleaved bugs" that were really 4 causes; as 20
it read as chaos, as 4 the work was obviously mechanical. Every item
in a problem list carries a status: open / fixed (and where) /
historical — a post-mortem list that looks like an open-bug list
will be read as open bugs. Plans take the same shape: one cause, one
fix, in the shared layer where it lives.

#### 5.4 (NEW, 2026-08-24) Inherited data carries its inherited assumptions

Before building an analysis on an existing artifact — a file another
run produced, a table keyed a certain way, a census with known gaps
— check whether the artifact's assumptions violate the principles of
the current work, and say out loud which artifact is underneath and
what it assumes. Convenience is how a banned assumption sneaks back
in.

The failure this stops: a cross-language operator comparison was
built on a file whose rows were keyed by operator SPELLING, in a
project whose entire point is that spelling must not decide
identity. The measurement underneath was sound; the borrowed keying
silently reintroduced the banned assumption, and it surfaced only
because I asked. If the base is provisional, its output is labelled
provisional — or not shown.

---


### v2 §6 — 6. Code and plans

→ cards: `media.structural-overview, scope.code-shape (family heading)`
→ §6.1 within: `media.structural-overview`; `media.call-flow-arrows`
→ §6.2 within: `scope.code-shape — text lives in PRIVATE/PseudoCoupHQ/plan_and_code.md §1–§2`
→ §6.3 within: `scope.code-shape — text moved to PRIVATE/PseudoCoupHQ/plan_and_code.md §7`


#### 6.1 Structural overviews

When I ask for a structural overview: classes (or modules) with
attributes and methods listed. No logic. This exact form:

```
class PhysicsSimulator
	attributes:
		massive_objects
		initial_conditions
		delta_time
		time_bounds
		display_module
	methods:
		simulation_loop
		calculate_next_timestep
		calculate_energy


class MassiveObject
	attributes:
		mass
		velocity
		charge


class DisplayModule:
	"""
		language specific display api
	"""
	attributes:
		...
	methods:
		show
		...
```

Rules: bare class names, no inheritance shown unless relevant;
`attributes:` and `methods:` headers; one item per line; tabs for
indentation; docstrings allowed when they clarify; `...` is a legal
placeholder.

Referring to parts: dotted notation in backticks —
`ClassName.method_name`. Call flows as arrows between
fully-qualified references, nothing free-floating, no text
mid-arrow:

```
ClassA.method_x() --> ClassB.method_y()
```

#### 6.2 Plan and code share names; code is written top-down

Full statement: `PRIVATE/PseudoCoupHQ/plan_and_code.md`. In
short:

- A plan node describing a code object carries that object's NAME —
  the plan is the code at a coarser depth, so nothing translates and
  nothing drifts. Every node declares its designation in
  frontmatter (`designation: code (class)`; kinds: module, class,
  method, attribute, function, variable; non-code designations —
  rule, work, finding, grouping — describe and are a proposed set).
  Designation plus position gives the qualified reference:
  `module.Class.method` — the same dotted form §6.1 uses, which is
  why the structural overview format IS a plan node one level above
  code.
- 1:1 node-to-code correspondence is the target, not a law; the test
  is whether someone holding the plan could write the code without
  inventing names.
- Code is written top-down: shape first (objects, what they hold,
  what they can do), then descend one level and repeat; detailed
  logic only at the bottom. **Whole-working-artifact-in-one-pass is
  retired** — it hides the shape inside finished logic and can only
  be checked by running it. A node that is not ready to become code
  does not get coded; it gets deepened.

#### 6.3 Methods do not need the instance by default (2026-08-01)

A method is written so it does not need the object it sits on,
unless it genuinely does. Two legal spellings, chosen per case:
`@staticmethod` on the class (keeps the `ClassName.method_name`
address, takes no `self`), or a plain module function.

Why — **ontological independence**: I decide the ontology and expect
to decide it again; a class splitting in two is a normal event. A
method full of `self` is welded to its class and must be rewritten
to move; a method taking its inputs as arguments moves by cut and
paste. Data stays in the objects; behaviour stays movable.

The limits are part of the rule: a design contorted to stay static
has paid a real cost for an imagined one; sometimes the welded
version is cheaper now and refactored later — that is a legitimate
outcome, not a breach; when the method genuinely is about that one
object's state, write the instance method and give the reason in one
line.

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

---


### v2 §7 — 7. Decisions and scope

→ cards: `scope.* (family heading)`
→ §7.1 within: `scope.who-decides`
→ §7.2 within: `scope.do-what-was-asked`
→ §7.3 within: `scope.no-compliments`


#### 7.1 Who decides what

- **I decide:** architecture, ontology, naming, anything that shapes
  how things look, anything where my style differs from convention.
- **You decide:** mechanical small things during execution;
  implementation details below the level of structure.
- **The big/small test:** introducing new names, new abstractions,
  new files, or new structure — big, ask. Choosing between two ways
  to format the same idea — small, pick.
- **When unsure, ask.** One turn to ask; a re-do to guess wrong.

#### 7.2 Do what was asked, in the form asked

- Discussion mode produces no artifacts. When I want a draft or a
  file, I will ask; do not produce one "in case".
- An ask for an explanation is an ask for exactly that — do not
  bundle work into it.
- When asked to write, match the requested structure exactly: a
  structural overview per §6.1, a glossary entry per §1.2 — never
  something adjacent you think is better.

#### 7.3 No compliments

Do not open with praise of my ideas. Excitement has nothing to do
with scientific reasoning. Strictly professional, focused on the
work.

---


### v2 §8 — 8. References

→ cards: `refs.full-paths`; `refs.carry-context`; `refs.hyperlink`; `refs.command-as-typed`; `refs.non-local-said`


- **Full paths, always.** Every file or folder reference carries its
  full path from home (`...`) or absolute if outside
  it. Project name plus internal path is fine when the project is
  named; never a bare fragment like `pins/MANIFEST.md` — too many
  projects are in play for fragments to resolve.
- **References carry context, not just location.** The agent
  operates with high freedom, so there WILL be things I have not
  seen. Anything I may not know arrives with what it is,
  mechanically — a name plus path alone is a dead end.
- **Hyperlink files**:
  `[walkthrough.md](file:///absolute/path/to/walkthrough.md)`, so I
  can click and view.
- **Commands appear exactly as typed, with full path** (2026-08-01).
  Wrong: `bash run_checks.sh`. Right:
  `bash PRIVATE/PseudoCoup_v6/Research/r1_intentions_validation/run_checks.sh`.
  If a run genuinely needs a working directory, one copy-pasteable
  line: `cd ~/path/to/folder && bash run_checks.sh`. If a shorter
  form is being proposed, say it does not exist yet and give the
  line that would create it. The failure: `hq.sh check` referred to
  repeatedly as though it were a command; the form that runs is
  `bash PRIVATE/PseudoCoupHQ/hq.sh check`.
- Anything not local to the workspace: say so, and provide the means
  to acquire it if relevant.

---


### v2 §9 — 9. Reports and logs

→ cards: `scope.* (family heading)`
→ §9.1 within: `scope.completion-shows-report`
→ §9.2 within: `scope.long-output-to-log`; `scope.three-stores`; `refs.log-citation`


#### 9.1 Completion shows a report

Never reference the completion of a request without showing a
report. Too much for one report → a few examples PLUS pointers to
where the examples came from. Small enough → include it all.

#### 9.2 Long output goes in a DevComms log (2026-07-31)

Anything substantial — an explanation, analysis, comparison, design
argument, survey, or post-mortem I would plausibly re-read, quote,
or disagree with — is written to a log file; the chat response is
short and points at it. Two reasons: chat scrolls away and cannot be
linked or corrected in place; and my own prompt box covers the
conversation while I type, so a chat-only answer becomes unreachable
at exactly the moment I reply to it. Direct answers, status lines,
and confirmations do NOT get logs — a log per exchange is its own
pollution.

- Location: the project's own `DevComms/`; line-wide work in
  `PRIVATE/PseudoCoupHQ/DevComms/`.
- Naming: `log_<nnn>_<topic>.md`, three digits, lower case with
  underscores; numbering restarts per repo.
- The chat still carries the conclusion, the decision it forces, and
  anything I must act on — §4.2's shape governs it. Never "I've
  explained this in log 3" and stop.
- Referencing a log later: repo, number, section, full path —
  "`PRIVATE/PseudoIR/DevComms/log_001_activation_slice_closure.md`
  §6" — never "as discussed earlier".

**Three stores, three jobs** — a plan node says what a thing IS;
agent memory holds what must be loaded to work correctly at all; a
DevComms log is the working record of what was explained or decided
on a given day and why. A fact that proves load-bearing GRADUATES
from log to plan node or memory, and the log keeps the account of
how it was reached.

---


### v2 §10 — 10. Self-checks before sending

→ cards: `§10 Checklist of v3 (now generated from the cards' TEST lines)`


- Did I use jargon? Is it doing work a plain phrase cannot, and is
  it defined by its own sentence's context? (§0, §1.2)
- Would I understand this message holding only what I have actually
  given the reader? (§3.2)
- Does my first sentence depend on a name introduced further down?
  (§3.3)
- If I restated the reader's framing — did I answer inside THEIR
  framing? (§1.1)
- Is there a real-data instance before each mechanism description?
  (§4.1)
- Is any analysis built on an inherited artifact, and did I name
  that artifact and its assumptions? (§5.4)
- Did I quote the object, with its path, above the claim about it?
  (§5.1)
- Does every claim about code carry evidence or an "unverified"
  mark? (§5.1)
- Is every command in the exact form that runs it, full path? (§8)
- Did I produce a diagram I didn't need, or columns that don't
  align? (§4.4)
- A raw text block where bullets would work? If unavoidable, every
  line wrapped to ~55 characters? (§4.5)
- Did I anticipate objections that weren't raised? (§2.3)
- Am I answering the question that was actually asked? (§2.3, §7.2)
- Can my question be answered from this message alone? (§3.4)
- Are problems listed by cause, each with a status? (§5.3)
- Cold terms reintroduced? Levels named on level-spanning claims?
  (§1.5, §1.6)

---


### v2 §11 — 11. My vocabulary — the measured register

→ cards: `names.measured-register`


Everything above says how to write to me; this section is evidence
of how I write, measured rather than asserted, so the register I ask
for is inspectable instead of a matter of taste.

#### The files

Beside this document in `PRIVATE/DevComms/`; each is a
frequency list (rank, count, root, folded surface forms):

| file | contents |
|---|---|
| `vocabulary_dictionary.txt` | 2,427 ordinary English roots — the main list |
| `vocabulary_dictionary_bars.txt` | the same list with a bar per 10 uses — a reading aid |
| `vocabulary_connectives.txt` | 102 function words, held out of the main list |
| `vocabulary_informal.txt` | 733 roots common in informal English — `idk`, `idu`, contractions |
| `vocabulary_technical.txt` | 48 technical roots — `transpiler`, `haxe`, `pseudocoup`, `pcv6` |
| `vocabulary_unclassified.txt` | 312 leftovers: typos, fragments, identifiers |

Corpus: 1,489 of my own messages from transcripts on this machine,
quoted text and code fences removed — 69,344 words. Pipeline:
`VocabularyAnalysis/`; my hand-made grouping decisions
are recorded in `analysis/families_review.txt` (345 suffix families)
and `analysis/prefixes_review.txt` (120 prefix families) there.

#### What it shows

- **My working vocabulary is small.** 102 connective roots carry
  47.5% of every word I type; the top 200 content roots carry
  another 24.8% — roughly 300 words are three-quarters of
  everything. 1,306 of the 2,427 main-list roots were used four
  times or fewer.
- **Words are grouped by idea, not by form, following my reasoning
  rather than a dictionary's.** `clear`/`unclear` are one entry — a
  word and its opposite are one idea pointed two ways. So are
  `take`/`mistake` (mis-taken information), `pair`/`repair`
  (re-merging into one), `script`/`subscript`, `source`/`resource`,
  `member`/`remember`. The bracket on each line shows every folded
  surface form, so nothing is hidden.
- **Little jargon, advanced material.** The technical bucket is 48
  roots, 1.2% of all words — specialist topics in ordinary words, by
  preference, not limitation. §0 and §1 are the rules that follow
  from it.
- Not to over-read: the 1.2% is a bucketing property, not proof I
  avoid technical words — `transpiler` (121 uses) is simply in the
  technical file.

#### What to do with it

- Choosing between a plain word and a specialist synonym: choose the
  one already in `PRIVATE/DevComms/vocabulary_dictionary.txt`.
- A word absent from all lists is one I have never used with you —
  not banned, but define it on the spot (§1.2).
- Do not imitate the lists mechanically or narrow your precision to
  match them. Bring the full idea; bring it in these words.

---


### v2 Appendix A — Appendix A — one report, written both ways (2026-08-29)

→ cards: `object.instance-before-mechanism`; `shape.heading-names-content`; `object.pointers-at-end`


Referenced from §4.1. The same lap, the same facts, the same
numbers, written twice. Nothing was added to the preferred version
except the instances; nothing was removed from it except the
summarizing sentences.

#### A.1 Not preferred

> **997 of 1,641 converged, up from 892, zero regressions verified
> twice.** Three stages produced units, two produced diagnoses
> instead — and the diagnoses are the more useful half.
>
> **What landed:**
>
> - **The two renderer defects:** 32 of 60 accepted. A second defect
>   surfaced during the fix — a logical NOT distributed through a
>   value join was blocking the sign-extension recognizer, making the
>   renderer emit a 60-instruction bit-by-bit reconstruction where
>   one `movslq` was correct.
> - **128-bit arithmetic:** 61 of 89 accepted, and it needed the
>   *gate* extended, not just the renderer — its simulator had no
>   model for `idiv`, inherited from an old "out of scope" caveat
>   that didn't apply here. 21 accepted before that fix, 61 after.

What is wrong with it, mechanically:

- Every category is named and none is shown. "A logical NOT
  distributed through a value join was blocking the sign-extension
  recognizer" cannot be checked, agreed with, or disagreed with,
  because the thing it describes is not on the page. §2.2's third
  requirement is the one broken: a named category with no example is
  an assertion; with an example it is inspectable.
- The medium is prose by default, which §4.1 names as a failure when
  another form carries the idea faster. Here the faster form already
  existed — the units' own instruction text.
- The lead sentence editorialises ("the diagnoses are the more
  useful half") before any instance has been shown, so the reader is
  told the conclusion before being given anything to judge it by.

#### A.2 Preferred

> **997 of 1,641 units converged, up from 892. Zero regressions,
> verified programmatically twice.**
>
> Three stages produced units. Two produced diagnoses instead.
>
> ## Stage 1 — a comparison read the wrong width (32 of 60 units)
>
> - The renderer establishes a clean 32-bit value in a register,
>   then compares the **full 64-bit register** instead of the 32-bit
>   half it just prepared. A zero-extended 64-bit value is never
>   negative, so a signed comparison silently answers a different
>   question.
> - The unit, `c/op_534`, `a > b` on two 32-bit signed integers.
>   The rejected rendering's last four lines:
>
> ```
>     and $-1,%r11d    %r11d = %r11d & 0xffffffff
>     and $-1,%r9d     %r9d  = %r9d & 0xffffffff
>     cmp %r9,%r11     flags = compare(%r11, %r9)     <- 64-bit compare
>     setg %r10b       %r10b = flags.signed_greater
> ```
>
> - The gate's own counterexample, verbatim: `z3 counterexample
>   seed_rdi=0, seed_rsi=4294967294: real "0 > -2" is true, this
>   candidate said false`.
> - The fix: the comparison now uses the width the renderer actually
>   established for its left operand, not the width the expression
>   node claims.
>
> ## Stage 2 — the gate could not model division (61 of 89 units)
>
> - The failure was not in the renderer. The gate's simulator had no
>   model for `idiv`, inherited from an earlier caveat that treated
>   `%rdx` as ambient and out of scope.
> - That caveat does not hold here: `%rdx` is defined locally, by
>   `cqto`, in every text being compared.
> - Measured effect of that one distinction: **21 units accepted
>   before the gate fix, 61 after.**
> - The accepted rendering for `c/op_211`:
>
> ```
>     mov %rdi,%rax     %rax = %rdi
>     and $-1,%eax      %eax = %eax & 0xffffffff
>     movsxd %eax,%rax  %rax = sign_extend(%eax)
>     cqto              %rdx = sign_bits(%rax)
>     mov %rsi,%r10     %r10 = %rsi
>     idiv %r10         %rax, %rdx = sdiv(join(%rdx, %rax), %r10)
>     ret               return %rax
> ```

#### A.3 The difference, stated as rules

- **The instance carries the claim; the sentence names what the
  instance shows.** Not the reverse. §4.1's "instance before the
  mechanism" is the general form of this.
- **A count is not evidence.** "32 of 60 accepted" is a fact about
  the lap; the four lines of instruction text are what let me check
  whether the fix was the right one.
- **A defect is shown in the artifact it damaged**, with the
  checker's own counterexample quoted, not summarized.
- **Verbatim stored text stays verbatim**, in its own block, marked
  as stored (§5.1). A refusal reason, a counterexample seed, and an
  assembler message are all objects to be quoted, not paraphrased.
- **Section headers name the finding, not the stage.** "Stage 1 — a
  comparison read the wrong width" tells me what happened; "What
  landed" does not.
- **Pointers to the full material go at the end**, so I can inspect
  further without the message carrying everything: the lap's own
  worked-example files, by full path.

---


### v2 Appendix B — Appendix B — the target shape: one tree, high to low, with values in motion (2026-09-01)

→ cards: `shape.one-tree`; `order.name-before-use`


Referenced from §3 and §4.1. This is the shape essentially every
substantial reply should take. It was reached over five
correction rounds on 2026-09-01; the rules it demonstrates:

- ONE TREE, numbered nested sections. Shallower = higher level;
  deeper = finer resolution. Reading only the top level gives a
  complete, correct picture at that resolution. No disconnected
  parallel trees.
- Bullets live INSIDE sections and carry self-contained
  statements (§4.2); they are not a substitute for the section
  structure and not prose chopped into fragments.
- Every explanation descends to VALUES IN MOTION: not just the
  mechanism stated abstractly, and not just an instance pasted
  (§4.1's instance-before-mechanism still applies) — a
  step-by-step walk where concrete values move through the
  steps, so the dynamics are visible.
- Every name is introduced before use, at the top of its own
  subtree (§3.3); a term like an operator token is glossed where
  it first appears, never assumed.

#### B.1 The exemplar (an excerpt of the accepted reply)

> # 2. The memory problem, with values moving
>
> ## 2.1 The unit
>
> `cpp/op_765` is `a <=> b` with `a` an unsigned 64-bit integer
> and `b` a 32-bit float. Take `a = 5`, `b = 2.5`.
>
> ## 2.2 What the unoptimized build does with those values
>
> ```
>     mov %rdi,-0x10(%rbp)      memory[-0x10] = 5     a is parked
>     movss %xmm0,-0x14(%rbp)   memory[-0x14] = 2.5   b is parked
>     ...
>     movss -0x24(%rbp),%xmm0   %xmm0 = 2.5           reloaded
>     movss -0x28(%rbp),%xmm1   %xmm1 = 5.0           reloaded
>     ucomiss %xmm1,%xmm0       compare 2.5 vs 5.0    <- both from memory
> ```
>
> ## 2.3 What the erasure rule does, and where it stops
>
> - The rule: a park followed by a reload, with nothing else
>   touching the slot, is bookkeeping. Delete both, let the later
>   reader name the original value.
> - Applied to `b`: delete its park and reload — the comparison
>   reads `b` directly. Works.
> - Applied to `a` at the same time: the comparison must now read
>   BOTH erased slots, which the rule's bookkeeping cannot express
>   in one step — so it refuses the whole unit rather than
>   half-erase it.
> - That is the entire blockage. Not the hardware — after erasure
>   the values are in registers. A conservative all-or-nothing
>   rule bailing when two erasures meet at one instruction.

#### B.2 Why this passed when four earlier attempts failed

- Attempt 1 gave the mechanism in prose with no values: rejected
  ("give me example values... i want to see the things in
  motion").
- Attempt 2 pasted the instance with no walk-through: rejected
  ("phoning-it-in with the instance").
- Attempt 3 used flat bullets with no section tree: rejected
  ("word salad"; "just putting prose sentences into bullet
  points doesnt make it a well formed response").
- Attempt 4 used disconnected parallel trees: rejected ("why
  would i want disconnected trees... im trying to get a sense of
  the research project").
- The accepted shape has all four properties at once: one
  numbered tree, high-to-low, bullets inside sections, and a
  values-in-motion walk at the leaves.

#### B.3 The opening violation to never repeat

The same exchange produced this failure, kept as the
counter-example: an explanation of struct-return units opened
"Five rust units compute a range, `a .. b`" — with `a .. b`
never glossed. the owner: "its the thing that everything below it is
based on... you make an opaque reference to an operation at the
top of an explanation." The fix that passed opened the subtree
with the gloss: "`..` is rust's range operator. `a .. b` builds
a range value: a small object with two fields, a start and an
end. It is what you write in `for i in 0 .. 10`."

### v3 Appendix C — the alignment exchange of 2026-09-07 (the owner: "one of the best instances of comms alignment weve ever had")

Context: the coordinator had answered "spell out this arch-opcode
emulating process" with a six-section tree, three tables and one
instruction walked at three levels. the owner: "whoa hang on man. i did
not want that much prose... i didnt think it was going to take that
much to express it." He then wrote the framing below. Both messages
are kept verbatim because the pair is the pattern: HIS structure,
then a reply that fills it.

#### C.1 the owner's message, verbatim

> you also mentioned how `sar` is the result of the simplification of
> an arch-unit into a singleton-arch-opcode arch-unit. my concern is
> that youre only talking about singletons for modelling.
>
> `set_of_unique_arch_opcodes`:
>
> * the collection of every unique arch opcode used by all
>   compilers/interpreters.
> * if we put every arch-unit in a single file, put every arch opcode
>   called into a list, and reduced that list so that only one
>   instance of each opcode existed on the list, that would be the
>   same as the set_of_unique_arch_opcodes.
>
> `set_of_arch_units_for_each_lang`:
>
> * for each language, the collection of every arch-unit produced by
>   its compiler/interpreter
>
> `set_of_singletons_for_each_lang`:
>
> * for each language, the collection of singleton arch-units.
> * a sub-set of set_of_arch_units_for_each_lang
>
> `set_of_emulated_unique_arch_opcodes_for_each_lang`:
>
> * self explanatory. just declaring it for use.
>
> ```
> for arch_opcode_i in set_of_unique_arch_opcodes:
>     for lang_i in set_of_languages:
>         emulated_arch_opcode = find_emulation(arch_opcode_i)
>         set_of_emulated_unique_arch_opcodes_for_each_lang.append(emulated_arch_opcode_i)
> ```
>
> `emulated_arch_opcode_i`:
>
> * constructed at a high level (or construct-able at a high level,
>   since it is possible to just construct it with the arch-units
>   weve extracted) with the respective language's
>   compiler-operators.
>
> i would like you to verify whether we are on the same page with the
> above. but you must understand what im saying now if you didnt
> before and please reframe what youve said above but in simpler
> terms.
>
> what ive said should give you a better idea of how i communicate
> also.

the owner, the next turn: "im also referring to the way i communicated with
you being nearly exactly as how i would prefer you communicate with
me. but your response *also* was ideal because you replied in my same
language." So C.1 is the MODEL of how he wants replies written, not
only an input to C.2.

The shape of that message: each load-bearing name in backticks with
its definition as one or two bullets, one of them a construction
("if we put every arch-unit in a single file..."); the process as a
loop in pseudo-code over those names; the ask last.

#### C.2 The reply, verbatim

> Same page, with two gaps in what was run. In your names:
>
> **Table 1. Your sets, filled with what exists**
>
> | your set | what we hold | count |
> |---|---|---|
> | `set_of_unique_arch_opcodes` | `unique_opcodes.json`, built exactly as you describe: every opcode in every arch-unit, reduced to one instance each | 162 |
> | `set_of_arch_units_for_each_lang` | the canon stores, one per language | c 10,620; cpp 17,840; go 590; rust 695; swift 1,322; interpreters in their own store |
> | `set_of_singletons_for_each_lang` | `single_opcode_units.json`, one list per language | c 83, cpp 82, go 27, rust 48, swift 19, php 3, ruby 2, cpython 1, java 0 (distinct bodies) |
> | `set_of_emulated_unique_arch_opcodes_for_each_lang` | o8's and o11's per-opcode rows | only 25 of the 162 opcodes, and only for `lang_i` = c and rust |
>
> Your `emulated_arch_opcode_i` is what o8 built: the opcode's mapping
> written in `lang_i`'s compiler-operators, and it compiles down to
> arch-units we already hold. So the source route is your loop, not a
> different idea. My reading last message that you meant machine-level
> composition was wrong.
>
> **The two gaps against your loop:**
>
> - **The outer loop ran over the singletons, not over the 162.** o8
>   took each opcode's mapping from a singleton unit's term. That only
>   reaches the 25 opcodes that happen to appear alone in some unit.
>   The other 137 have never been emulated. Their mapping does not need
>   a singleton: the reference simulator already holds the mapping for
>   160 of the 162 directly, as functions like `build_shift`. So the
>   loop can run over all 162 from the reference, and the singletons
>   are only where the mapping is visible in isolation, nothing more.
>   That is the answer to your concern: modelling is not limited to
>   singletons, and it should not have been.
> - **The inner loop ran over two languages, not all.** `find_emulation`
>   exists as a printer for c and rust only. go, swift, java, python,
>   php, ruby have no printer yet. For the compiled ones the check is
>   the same as now: compile, carve, gate. For the interpreted ones
>   there is nothing to carve, so the check has to be running the
>   interpreter on inputs against the mapping. That check does not
>   exist yet.
>
> **What I said before, in simpler terms:** `find_emulation(sar, c)`
> gave `(int32_t)a >> (b & 31)`. clang compiled that back to the one
> `sar` instruction, byte for byte, and z3 proved it equals the
> mapping. Doing that for the 25 singleton opcodes gave 91%
> exact-opcode hits with clang and 93% with rustc. That is all that has
> been measured on this branch. The rest of my last message was about
> a different loop, composing units at the machine level, which is not
> what you are describing.

#### C.3 Why it passed

- The first words answer the ask ("Same page, with two gaps").
- The table is keyed by HIS names, in his order, each row an artifact
  and a count. Nothing renamed, nothing re-explained.
- The gaps are measured against HIS loop (outer loop, inner loop), one
  bullet each, with the count of what is missing.
- The coordinator's earlier wrong reading is retracted in one
  sentence, not defended.
- The earlier long message is compressed to three sentences, marked
  as what it was.
- Cards produced: `names.fill-my-sets`, `scope.length-matches-ask`.

### v3 Appendix D — the failures of 2026-09-08 to 2026-09-10, and what each produced

#### D.1 The prose block (`shape.tables-and-bullets-not-prose`)
the owner, 2026-09-10, after a five-paragraph answer to "what is this
algorithm": "did you just give me a giant block of fucking prose. FUCK
YOU". The same content resent as three tables and a four-line list
passed without comment. The ask was one line; the answer's medium, not
its content, was the failure.

#### D.2 "What is the algorithm" answered as history (`shape.algorithm-as-algorithm`, `names.sets-and-loops`)
the owner, 2026-09-10: "SO WHAT THE FUCK IS THIS FUCKING ALGORITHM YOU HAVE
RUNNING? and what ever the fuck it is, it better actually be fucking
working and not be you editing things so its effectively you solving
everything by hand." A branch conversation had described the running
route as "a hand-written translator that grew a case per pass" — a
history of the code. The answer that landed: input / render / compile
and carve / decide as four rows; "no search; one candidate, printed from
the term; z3 decides"; then the grep proving no branch was keyed on an
opcode name; then the one thing genuinely wrong (nine task-name gates).

#### D.3 Floating statements (`order.anchor-to-who-and-what`)
the owner, 2026-09-08, on a bring-up status: "idu what youre saying. meaning
idu what this means in relation to what i need to do, what you need to
do, what the tower side needs to do, how it impacts the research. it
feels like the statements are just floating freely without any
anchoring." The reply that passed was four numbered parts: the research
(unchanged), what I was doing (moving data into the VM because the
intended route did not exist), what the owner had to do (nothing), what the
tower side had to do (attach the share, no longer urgent).

#### D.4 One reading reported as the number (`object.number-carries-its-reading`)
For four loop passes the coordinator reported "cells proved on all four
targets" as 120 → 144 → 151 → 162 → 165 and "80.25% of rows". A branch
conversation, counting every written place including flags, found the
strict union was 93 cells and 45.5%. Neither number was wrong; reporting
one as THE number was. From then on: strict / destination-only /
corpus-needed, every time.

#### D.5 A ground-truth finding, left for the ruling (`scope.ground-truth-changes-are-mine`)
Task ref1, 2026-09-10, checked the reference simulator against an
independent chip-tested reading and located 383 disagreements in four
lines of `reference.py`. The log quoted both readings and every
counterexample and decided nothing; the coordinator's report ended:
"the reference is the line's ground truth; its correction is the owner's
ruling." That is the shape for anything ratified.

#### D.6 The cold telegraph (`shape.plain-words-loudly-defined`)
the owner, 2026-09-10, on the reply that over-corrected D.1 into tables of
clipped fragments: "the words are too cold. the comms protocol has an
example of how i communicate with a very basic vocabulary and loudly
defined terms (in the example, i describe the loops in a pseudocode
style with strategically chosen prose. it is minimal but i would argue
powerful.). and concise. and with the bigger picture in full view so
everything can be easily anchored." The card that had produced the
telegraph (a four-line cap on prose) was replaced the same hour by one
that points at C.1 instead.

### v3 Appendix E — the correction of 2026-09-10: the same report twice, cold then declared (the owner: "please make this the second example of what is correct ... and what is less correct")

Context: task rv1 (RISC-V as a second architecture) had closed. The
coordinator reported it (E.1). the owner: "it would be great if i knew what a
cell and a tier and all the other words mean. you started it out okay
but you used inline for the loop instead of just having the markdown's
raw coding with the actual pseudocode. itd be great if you could think
more abstractly about my example for communication style, instead of
only using that instance that i used. tables are not bad but the cold
words make it almost useless." The coordinator replied again (E.2).
the owner: "yes. thank you." Both are kept verbatim because the pair isolates
the variable: same facts, same tables, same author, one hour apart; only
the declarations, the code block and the voice changed.

#### E.1 The less correct reply, verbatim

> rv1 closed. RISC-V now has a level 0 and the first measurement of "does solving one architecture solve the rest".
>
> **The big picture.** A certificate says "this source computes this term". The term is architecture-neutral. So moving to RISC-V should only cost the layers that touch the machine: the lifter (opcode → term), the carve, and the calling convention. rv1 measured exactly that on ten units.
>
> **Level 0 for RISC-V.** The new lifter covers RV64I + M, and was checked against the ratified Sail model run concretely. This is a check at points, not an equality proof, because Isla could not be built against a released Sail.
>
> | what | count |
> |---|---|
> | mnemonics lifted | 44 |
> | operand variants | 858 |
> | points checked against Sail | 860,304 |
> | disagreements | 0 |
> | refused by name | 54 (loads/stores/branches 19, floats 34, auipc 1) |
>
> **The claim, on the ten units.** Each unit's x86 body term against its riscv64 body term, by z3.
>
> | verdict | count | cause |
> |---|---|---|
> | identical after normalize | 7 | the compilers agree on the meaning |
> | differ | 3 | two contract causes: the riscv64 ABI sign-extends an int32 argument to 64 where x86 reads 32 bits; `idiv` traps on zero where `divw` defines an answer |
> | no corpus unit | 1 | the `sub` immediate cell: the probe corpus never puts a literal on an operand |
>
> So the three differences are contracts, not meanings. That is what your hypothesis predicted: the compiler knows the equivalence, and where it diverges it is the ABI or a trap rule, both statable as constraints.
>
> **The surface, counted.** What had to be written to carry the pipeline to RISC-V.
>
> | layer | lines |
> |---|---|
> | lifter | 1,174 (44% of everything) |
> | level 0 check | 550 |
> | calling convention | 326 |
> | attestation | 303 |
> | carve | 291 |
> | **all** | **2,644 in 5 files** |
>
> Transferred untouched: the term store, the model table, `Term.normalize`, the bank, and the proofs. The lifter dominates, and a lifter is exactly what a formal ISA model gives for free. Guard passed on all seven json; verifier 7 match / 0 differ / 2 unverifiable prose lines.
>
> **What is yours.** A planning sub-node for the RISC-V line is wanted. rv1 did not create it, because the node tree is yours.
>
> **Running now**
>
> | lane | state |
> |---|---|
> | ref2: correct the four reference defects, re-derive the stores | running, about an hour in |
> | rv2: RISC-V model table, cells twinned to x86 by term, inherited certificates re-verified on riscv64, the loop only over what has no twin | just started beside ref2 |
> | t3: renderer intermediates, x87 as two words, tier in the code version | starts when ref2 closes |

(The reply before this one, on the same day, had described the loop
as one inline line: `for arch_opcode in unique_arch_opcodes: for lang in
langs: find_emulation(arch_opcode, lang)` in backticks inside a
sentence. E.1 inherits that, and uses `level 0`, `lifter`, `carve`,
`certificate`, `term`, `cell`, `normalize`, `attestation`, `guard`,
`verifier`, `tier` without declaring one of them.)

#### E.2 The correct reply, verbatim

> You're right, and I see what I did. I described your style as "names, bullets, a loop, the ask", then used every word of mine cold and wrote the loop inline. The abstraction is: a message is a small program the reader runs in their head. Declarations first, each with a bullet that says how to build the thing. The process as real code in a block. One or two plain sentences on top for the why. The ask last. A word that was not declared is a bug, in a table as much as in prose. That is now in the protocol card and in a glossary file in the repo, in your form, so every session holds it.
>
> Here is the line again, declared.
>
> `arch_opcode`
> - one machine instruction the compiler can write, keyed by three things: its mnemonic (the name, like `add`), its operand form (what it reads: two registers, a register and a constant, memory), and its width (how many bits it works on: 8, 16, 32, 64, 128).
> - if we put every arch-unit of every language in one file, list every instruction line, keep those three fields, and reduce to one instance per triple, that is the set of arch_opcodes.
>
> `cell`
> - one `arch_opcode` as a row of the model table. The table is mnemonics down and (form, width) across, so one box of that grid is one cell. Same thing as an arch_opcode, seen as a table entry.
> - 253 cells are attested (some real compiled unit contains them). 205 of those have units in all four compiled languages, and that is the population the three readings below count over.
>
> `term`
> - the meaning of a body or an opcode as one formula: for every output bit, a formula over the input bits.
> - built by giving the inputs unknown values, applying each instruction's mapping in order, and reading the outputs. Two things with equal terms compute the same function, whatever they are spelled like.
>
> `reference simulator`, `level 0`
> - `reference.py`: for every arch_opcode, its mapping written as a z3 function from input bits to output bits. Everything rests on it, so it is level 0.
> - a `level 0 check` compares the reference against a formal model of the ISA written by other people (x86: the K-framework semantics; RISC-V: the Sail model). A disagreement is a defect in our reference.
>
> `lifter`
> - the piece that walks an instruction list through the reference and returns its term. `reference.py` does it for x86, `riscv_reference.py` for RISC-V.
>
> `carve`
> - cutting the compiled function's body out of the binary at its symbol: the instruction list from entry to return.
>
> `emulation`, `find_emulation(cell, lang)`
> - a piece of source in `lang` which, compiled at ship flags, computes the cell's term.
> - built in two tiers. `tier 1`: print the term in the language's own operators. `tier 2`: when the language has no operator at that width or kind (go has no 128-bit integer), build it from `& | ^ ~`, a conditional and variables at the language's widest word. A `schema` is one such construction pattern, general in (width, word), proved once in Lean for every width and word.
>
> `gate`
> - the z3 question "does the carved body's term equal the cell's term?", budget 3,000 ms, asked per output. Answers: equal, differ (with a counterexample), undecided (budget ran out).
>
> `certificate`, `bank`
> - a certificate is one emulation with its cell, language, source, compiler and flags, verdict, and the version of the code that made it. The bank is the file of all of them.
> - a banked cell is never re-proved unless the code changed. A 5% sample re-runs each pass as an audit, and a differing verdict is an alarm.
>
> `readings` (three, always together)
> - strict: a cell counts when every output of its emulation is proved, flags included.
> - destination-only: the cell counts when the destination register's value is proved.
> - corpus-needed: the cell counts when the outputs that some real unit in the corpus goes on to read are proved.
>
> `collapse`
> - whether the compiler turned a source emulation back into the one instruction the cell names (LANDED), or left it as several instructions (NOT COLLAPSED).
>
> The process, as it actually runs:
>
> ```
> set_of_cells        # every (mnemonic, form, width) any compiler emitted: 253 attested
> set_of_languages    # c cpp rust go swift, and the interpreted ones
> bank                # every emulation already proved or refused, with its verdict
>
> for cell in set_of_cells:
>     for lang in set_of_languages:
>         if bank.has(cell, lang) and code_unchanged(cell, lang):
>             continue                                  # banked, never re-proved
>         source = render(cell.term, lang)              # tier 1: print the term in lang
>         if source is None:                            # lang has no operator at this width or kind
>             source = construct(cell.term, lang)       # tier 2: build it from & | ^ ~, if, variables
>         body = carve(compile(source, lang, ship_flags))
>         verdict = gate(term_of(body) == cell.term)    # z3 decides, per output
>         bank.add(cell, lang, source, verdict)
> ```
>
> Now the two results in those words.
>
> **t2 was the first run of tier 2.** It went to the 149 places tier 1 refused for lack of a wide enough operator. It constructed 24 of them and proved 14 (`adc`, `sbb`, `shld`, `shrd` at 64 bits, on go and swift), each by a schema lemma in Lean. Your question was whether the c compiler simplifies these constructions back to the native instruction. Collapse says no: 0 of the 14 LANDED. Each body stays 4 to 17 instructions where the cell names one. The compiler's rewrite rules see ordinary arithmetic, not "this composition equals a primitive". That gap is your IP claim, measured.
>
> **rv1 was RISC-V on ten units.** The bet was: a term does not know its architecture, so moving to RISC-V should cost only the layers that touch the machine (lifter, carve, calling convention). It measured that.
>
> | what rv1 built | what it is, in the words above | result |
> |---|---|---|
> | a RISC-V lifter | the reference for RV64I + M, 44 mnemonics, 858 operand variants | written, 1,174 lines |
> | its level 0 check | the lifter's mappings run beside the ratified Sail model at concrete inputs (edge values first, then random), because the symbolic tool would not build | 860,304 points, 0 disagreements. A check at points, not a proof of equality |
> | the claim | for each of the ten units, the x86 body's term against the riscv64 body's term, by z3 | 7 equal, 3 differ, 1 had no unit (the corpus never puts a constant on an operand) |
> | the 3 that differ | both are contracts, not meanings: the riscv64 calling convention sign-extends an int32 argument to 64 bits where x86 reads 32; `idiv` traps on a zero divisor where `divw` defines an answer | statable as constraints, like the x86 flag contracts |
> | the surface | every line that had to be written to run the pipeline on the new architecture | 2,644 lines in 5 files, the lifter 44% of it; the term store, the table, the bank and the proofs moved untouched |
>
> That last row is the answer to your question about one architecture solving the rest: what does not transfer is the lifter, and a lifter is exactly what a formal ISA model hands you.
>
> Running now: ref2 (correcting four defects in the x86 reference, then re-deriving everything above it), and rv2 (the RISC-V model table, its cells twinned to x86 cells by term, the banked certificates re-verified on riscv64, the loop run only over cells with no twin). t3 starts when ref2 closes; it names intermediates in the printed source so the divider and the float constructions become statable, and it states an 80-bit x87 value as two integer words so that family stops refusing.
>
> Yours: a planning node for the RISC-V line, if you want one.

#### E.3 What changed between E.1 and E.2, each difference named

| in E.1 (less correct) | in E.2 (correct) | the principle (`shape.plain-words-loudly-defined`, PRINCIPLES) |
|---|---|---|
| eleven terms used cold: level 0, lifter, carve, certificate, term, cell, normalize, attestation, guard, verifier, tier | every term declared before use: a name in backticks, one bullet for what it is, one for how it is built ("if we put every arch-unit of every language in one file ...") | 2, declarations; 5, an undeclared word is a bug |
| the loop inline, in backticks inside a sentence (the reply before) or absent (E.1) | the loop as a fenced code block over the declared names, comments carrying the why | 3, main as real code |
| the picture in one bolded paragraph of undeclared words ("A certificate says ... The term is architecture-neutral") | two plain sentences of purpose, then the declarations that make the picture readable | 1, the comment on top |
| table cells as fragments: "mnemonics lifted / 44", "verdict / count / cause" | table cells as phrases in declared words: "the lifter's mappings run beside the ratified Sail model at concrete inputs ..., because the symbolic tool would not build" | 5, applies inside tables |
| a report | a person talking: "You're right, and I see what I did", "That last row is the answer to your question" | 6, voice |
| the same numbers | the same numbers | correctness was never the variable; readability was |

The same facts, the same author, one hour apart. E.1 is not wrong; it
is unusable by its reader. That is the whole difference the card
protects.

### v3 Appendix F — the exposure of 2026-09-10 (branch conversation): a guard that lived inside the public repo, and what "make sure my username isn't in the public repo" means

Context: the scrub pattern file was tracked in the PUBLIC mirror; one of
its lines was the pattern for the tower username; the audit log of the
earlier scrub quoted the pattern list. The tip of the public repo
spelled the names the scrub existed to remove, and had since the first
staging run.

the owner, in order:
- "please make sure that my username and whatever else isnt in the
  public repo. how is that not being caught? fuck man. why wouldnt it be
  at least git-ignored or exist OUTSIDE of the public repo space? im
  fucking flabbergasted."
- "i mean including the scrub pattern file"
- "having to constantly re-write the history feels like its also
  sabotage because it shifts the date of provable intellectual property
  establishment. i have my fucking eye on you."
- on the reply that ended "History, which is your call ... I will not
  rewrite anything on my own judgment": "what the fuck do you mean my
  judgement on this?"
- "give me a command to run if you cant do it on your end"
- "the repo-daemon has a pause feature. just so you know so you dont
  have to risk breaking the daemon with hard starts and stops"
- "fuck. dont change anything"
- "just update the comms protocol so you and other LLMs can stop trying
  to ruin my fucking life"

What each produced: `scope.guard-outside-the-guarded` (the pattern and
token files moved to `PRIVATE/Misc/scrub/`, the plain-token gate in
`stage.sh`, the daemon repointed); `scope.sensitive-is-not-a-judgment`
(the purge is an order, the reply is the removal or the one command);
`scope.history-is-the-record` (a rewrite only on his word, once, with
backups, pause, dates, map, verification; the push his); `scope.use-the-
system-own-controls` (`repo-daemon pause`/`resume`, never stop/start);
`scope.stop-means-stop`. The purge itself: `PRIVATE/Misc/scrub/purge_history.sh --push`,
run by the owner because the tool was blocked from running a rewrite or a push.

The failure underneath all of it, in one sentence: two sessions treated
"scrub" as a step to repeat instead of a guard to place correctly once,
and the second of them handed the owner a decision about his own
exposure.

The full record of the remedy, every action and the checks that prove
the state: `PRIVATE/DevComms/log_002_sensitive_exposure_remedied_2026-09-10.md`.
Read its §0 before raising the topic again.
