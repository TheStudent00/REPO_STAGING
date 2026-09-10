# Proposal — restructure the communication protocol for an LLM reader

2026-09-06. Written at your request:

> review the LLM communications protocol and determine how to
> restructure it so that it is easier for an LLM to follow. if you
> see the spirit of the content but see how the realization does not
> match the spirit, propose the changes.

**ADOPTED AND CARRIED OUT, 2026-09-06.** the owner: "do what you think is
best." What was done, against §5 and §7 below:

- The rulebook is now v3 at
  `PRIVATE/DevComms/LLM_communication_protocol.md`: 60 cards
  in seven families, a glossary of its own terms, one precedence
  list, and a checklist that is the TEST line of every card.
- The cases file is
  `PRIVATE/DevComms/LLM_communication_protocol_cases.md`:
  every v2 section verbatim under the cards it feeds, with the
  v1 → v2 → card id map at the top. It sits beside the rulebook, not
  in the archive, so a new case can be appended.
- v2 is archived as
  `PRIVATE/DevComms/0_Archive/LLM_communication_protocol_v2.md`.
- §6.3 (static methods) moved to
  `PRIVATE/PseudoCoupHQ/plan_and_code.md` §7; §6.2 was already
  there. The rulebook keeps one pointer card, `scope.code-shape`.
- Precedence is the order in §5.4. Ids are slugs, per §5.5.
- The lost-nothing check ran and passed
  (`PRIVATE/DevComms/0_Archive/build_cases_2026-09-06.py`).
- The §6 size estimate was wrong. The rulebook is 1,146 lines, not
  about 460: each card keeps the whole v2 rule text rather than a
  one-sentence distillation, and the glossary and the 60-line
  checklist are new. What changed is the shape, not the length; the
  stories (the cases file, 1,291 lines) no longer load with it.

---

## 1. The proposal in four sentences

- The protocol is a rulebook and its case history in one file. The
  binding rule text is a minority of the file; the rest is the dated
  account of the failure that produced each rule.
- Split it the way its own §9.2 says to split any record ("three
  stores, three jobs"): a rulebook that says what each rule IS, and a
  case file that keeps every dated failure, quoted, keyed by rule.
  Nothing is dropped; it is moved.
- Inside the rulebook: every rule becomes one card of one fixed
  shape; rules are grouped by cause (its own §5.3); Appendix B
  becomes the first shape rule instead of the last appendix; the
  protocol's own recurring terms get a glossary at the top (its own
  §1.2); one precedence list replaces the four local truces; and the
  send-time checklist is assembled from the cards, so it cannot fall
  behind again.
- The protocol's own rules, applied to the protocol, are the
  justification for each of these moves. Section 4 shows that.

---

## 2. What the file is now

### 2.1 Size and history

| measure | value |
|---|---|
| lines | 1,112 (v1 in `0_Archive/` was 882) |
| rule subsections | 47, under 12 sections and 2 appendices |
| commits since founding 2026-07-31 | 17 |
| rules carrying a date or NEW / REVISED marker | 26 |
| lines naming a failure or quoting you | 27 |

### 2.2 Who reads it, and how

Every task brief from round 2 onward carries this line or one like
it (logs 091, 097, 103, 109, 115, 123, 134 in
`PRIVATE/PseudoCoupHQ/DevComms/`):

> Read AgentMemory.md and the comms protocol in full first

So the whole file is loaded into a fresh context before every
delegated task. Its length and its shape are paid for on every task,
by a reader who did not live the failures it recounts.

---

## 3. Why an LLM finds it hard to follow

Each point: the instance from the file first, then what it costs.

### 3.1 The rule has to be mined out of the story

§1.8 (lines 157–180), the rule in its first sentence:

> When asked what something is, the first sentence names it in
> relation to the things it sits between.

The remaining twenty lines are the account of the hour it took to
reach that sentence, and your quoted question. §4.6 is the same
shape: four rule bullets, then twenty lines on the three attempts.

- For the people who lived the failure, the story IS the rule; it is
  what makes it stick.
- For a fresh context the story is text around the rule, and the
  reader must decide which sentences bind. A rule that has to be
  extracted is a rule that will sometimes be extracted wrong.

### 3.2 No precedence: four local truces, no global order

Where rules pull against each other, the reconciliation is a
paragraph inside one of them:

- §3.1: "Resolution of the apparent conflict with 3.2"
- §2.3: "This does not conflict with §0's 'full mechanism'"
- §4.2: "Scope, stated once: bullets are the default ... §4.1 can
  override"
- §4.1: "Priority among the media rules"

A reader in a hard case needs one list: when two rules disagree,
this one wins. Today the reader must find the right truce, and only
the four foreseen conflicts have one.

### 3.3 The send-time checklist is incomplete

§10 is the part an LLM actually runs before sending. It cites
seventeen section numbers. It does not cite:

| missing | rule |
|---|---|
| §1.7 | one name, one thing |
| §1.8 | what-is-it first — "the most expensive failure in this protocol's history" |
| §3.4a | project vs session; population and as-of on every figure |
| §3.5 | walkthrough before numbers |
| §4.6 | machine state as stepped tables |
| §4.7 | a heading names its content |
| §5.1a | literal / gloss / analogy labelled |
| Appendix B | the target shape |

Every rule added after 2026-08-24 is absent. The checklist is
maintained by hand, and stopped being maintained. The rules the
document itself calls most expensive are the ones the checklist does
not check.

### 3.4 The most important shape rule is an appendix

§3's preamble (line 280):

> THE TARGET SHAPE FOR SUBSTANTIAL REPLIES IS APPENDIX B ...
> Essentially every substantial message should take that shape.

The rule governing essentially every message sits at line 1027,
after the vocabulary statistics, and is reached from §3 by a forward
pointer.

### 3.5 Numbering is out of order and pointers dangle

- §1.8 (line 157) appears before §1.7 (line 182).
- §3.4a and §5.1a are lettered patches. The v2 header says lettered
  patches were merged.
- §1.2 (line 92): "§19's vocabulary lists". There is no §19; the
  lists are §11. This is a v1 number.
- §3 preamble (line 276): "These four rules". §3 has seven.
- Outside the file, citations use three numberings at once: v1
  numbers (§18a, §14a, §5a in HQ logs 007, 039, 072; "protocol §4
  glossary form" in my memory file `explanations-full-mechanism.md`)
  and v2 numbers (§5.1a, §9.1, §1.7). Section numbers as identity
  have already failed once; the next restructure would break them
  again.

### 3.6 Two voices for one person

- §0–§9: "I" and "me" are you.
- §1.8, §4.6, §4.7, Appendices A and B: "the owner" in the third person,
  with "the owner: ..." quotes.

A reader has to work out that "I", "me", "the owner", and "the reader" are
one person, and that "you" is itself. The third-person passages are
the ones I wrote; the first-person ones are yours. The seam shows.

### 3.7 Three kinds of content in one file

| kind | sections |
|---|---|
| how to communicate with you | §0–§5, §8, §10 |
| how to work (code shape, who decides, where logs go) | §6, §7, §9 |
| evidence about your register | §11 |

§6.3 (methods do not need the instance) is a coding rule. It is
loaded every time the protocol is loaded to write a reply.

### 3.8 The protocol's own terms are not held before use

| term | first use | defined |
|---|---|---|
| load-bearing | §0, line 24 | never |
| values in motion | §3 preamble, line 283 | Appendix B, line 1028 |
| cold | §1.5 | §1.5 — then reused in §3.5 as "vocabulary debt" |
| population, as-of | §3.4a | by example only |
| gloss, literal | §5.1a | §5.1a — then "glossed" in B.3 |

These are recurring, weight-carrying words. §1.2 says exactly those
get a glossary entry.

---

## 4. Where the realization contradicts the spirit

The spirit, from §0: reduce the reader's uncertainty; full mechanism
in plain words; every load-bearing word anchored; misalignment
detectable. The document's own rules, applied to the document:

| rule | where the protocol breaks it |
|---|---|
| §2.1 one idea per sentence | §6.3, lines 698–703: "The limits are part of the rule: a design contorted ... ; sometimes the welded version ... ; when the method genuinely is ..." — three ideas, two semicolons, one sentence. §4.4 is one six-clause chain. |
| §1.8 what-is-it first | §3.4a opens "3.2 says assume I am missing context. This sharpens what KIND of context" — motivation first, the rule arrives in the third sentence. §2.3 opens with a negation, "Not long answers". |
| §3.3 the first sentence rests on nothing later | §3's preamble rests on Appendix B. §1.2 rests on a §19 that does not exist. |
| §1.2 recurring load-bearing terms get a glossary | none of the protocol's own terms has one (§3.8 above). |
| §5.3 report by cause, not by sighting | 47 rules are sightings of, by my grouping, seven causes (§5.2 below). §0 says it itself: "Every rule below serves this one purpose." |
| §9.2 three stores, three jobs | what each rule IS and the account of how it was reached share one store. |
| §4.2 every level complete on its own | the top level (the headings plus §10) is not a complete picture, because §10 is missing eight rules (§3.3 above). |
| §1.7 one name, one thing | you are "I", "me", "the owner", and "the reader" (§3.6 above). |

Stated plainly, so it is not misread: none of this says the stories
were a mistake. They are how the rules were won and they are the
evidence a future reader needs to judge a rule. The contradiction is
only that they sit in the same store as the rules, which the
protocol's own §9.2 says to separate.

---

## 5. Proposed shape

### 5.1 Three files, three jobs

| file | job | size |
|---|---|---|
| `PRIVATE/DevComms/LLM_communication_protocol.md` | the rulebook: what each rule IS, one card per rule | about 400 lines |
| `PRIVATE/DevComms/LLM_communication_protocol_cases.md` | the account: every dated failure and quote, verbatim, keyed by rule id; Appendix A and Appendix B entire; the id map v1 § → v2 § → id | unbounded; nothing dropped |
| `PRIVATE/PseudoCoupHQ/plan_and_code.md` (exists) | §6.2 and §6.3 join the file §6.2 already names as their full statement | about 60 lines added |

§11 (vocabulary) becomes a five-line card under NAMES that points at
the six list files. Its analysis paragraphs move to the cases file.

### 5.2 Rulebook order — grouped by cause

0. **Root rule.** §0 as it is, trimmed to its two failure directions.
1. **Glossary of this document's own terms**, in the §1.2 form:
   load-bearing; cold; level; literal, gloss, analogy; instance;
   values in motion; population and as-of; the tree shape.
2. **Precedence.** One list; see §5.4.
3. **Rule families**, each a run of cards. Family = the cause; card =
   one place the cause shows.
   - **NAMES** — one name, one thing, and the reader holds the
     meaning before the name. Cards: keep my words; build on my
     framing; define in the carrying sentence; glossary form; cold
     re-entry; level named; one name one thing; what-is-it first;
     abstract words anchored; banned vocabularies; no nicknames;
     the measured register.
   - **ORDER** — the model before the conclusion. Cards: answer
     first when self-standing; first sentence rests on nothing
     later; name before use; a question states its facts; project
     not session; walkthrough before numbers; interpretation
     conditional.
   - **SHAPE** — one tree, high to low, values in motion. Appendix
     B's four properties become the family's first card. Cards: one
     tree; bullets inside sections, each level complete; one idea
     per sentence and the walkthrough test; contrast visible; a
     heading names its content; no unrequested optionality.
   - **OBJECT** — the thing on the page before the claim about it.
     Cards: quote the object; literal / gloss / analogy labelled;
     unverified marked; instance before mechanism; machine state as
     stepped tables; full mechanism in four parts, metaphor beside
     it; inherited assumptions named; report by cause, with status.
   - **MEDIA** — the mechanics of each form. Cards: pick the medium
     per idea, and the figure says what it is and is not; pipe
     tables only; text diagrams align; raw blocks last resort at
     ~55 characters; the structural-overview form (§6.1).
   - **REFERENCES** — full paths; hyperlinks; commands as typed;
     non-local things said to be so.
   - **SCOPE** — do what was asked, in the form asked; who decides;
     no compliments; completion shows a report; long output to a
     log, with its location and naming.
4. **Send-time checklist.** One line per card: its TEST field,
   copied. Complete by construction, because a card without a TEST
   line is not a finished card.

### 5.3 The card — one shape for every rule

The instance first. §1.8 today is 24 lines; the card that replaces
it in the rulebook:

#### names.what-is-it-first
- **RULE.** When asked what X is, the first sentence names X in
  relation to the things it sits between. Purpose, motivation, and
  construction may follow. They never come first.
- **TEST.** From my first sentence alone, can the reader place X in
  the chain they already hold?
- **BAD.** "A term exists so that z3 can check two arch-units for
  equivalence, which requires..." — purpose first; the noun is
  never placed.
- **GOOD.** "A term is the arch-unit expressed as a z3 expression."
- **CASE.** cases#what-is-it-first, 2026-09-05 — the hour and the
  ten replies, with your question quoted.

A second instance, §3.4a, today 28 lines:

#### order.project-not-session
- **RULE.** Assume I know the project. Do not assume I hold your
  session. Every figure carries its population and its as-of.
- **TEST.** For each number: did I say what it counts and when? Did
  I re-explain anything I already ratified?
- **BAD.** "144 units still unconverged of 1,779"
- **GOOD.** "144 of the 1,779 compiled-language units (five
  languages, as of lap 9) are still unconverged"
- **CASE.** cases#project-not-session, 2026-09-01.

The fields, fixed for every card:

| field | content | bound |
|---|---|---|
| RULE | the imperative | one to three sentences |
| TEST | a yes/no question I can ask of the draft | one sentence |
| BAD / GOOD | one minimal pair | six lines each, at most |
| CASE | pointer into the cases file, with date | one line |

Why one fixed shape: a reader scanning forty cards finds the field
it needs without reading the card. The TEST fields concatenated ARE
§10, so the checklist cannot drift from the rules. And the cards
are markdown headings and bullets, not raw blocks, so §4.5 is
honoured and they render.

### 5.4 Precedence — one list, replacing the four truces

When two rules disagree inside one message, the earlier wins:

1. **Root rule.** The reader's uncertainty goes down and misalignment
   becomes visible. Any rule that would raise uncertainty in the
   case at hand yields.
2. **SCOPE.** Answer what was asked, in the form asked. A perfect
   tree that answers a different question is worth nothing.
3. **NAMES.** Every load-bearing word is held before it is used.
4. **ORDER.** The model before the conclusion.
5. **OBJECT.** The thing on the page before the claim about it.
6. **SHAPE.** One tree, high to low, values in motion.
7. **MEDIA and REFERENCES.** Mechanics.

The four truces then become consequences and are deleted:

| truce today | resolved by |
|---|---|
| §3.1 answer-first vs §3.2 model-first | NAMES above ORDER: if the answer's first sentence needs a name the reader lacks, the name comes first. That is §3.3, and §3.1 no longer needs its own paragraph. |
| §2.3 "no over-explaining" vs §0 "full mechanism" | SCOPE above everything but root: full strength on the thing asked, nothing beside it. |
| §4.2 bullets default vs §4.1 pick the medium | OBJECT above SHAPE above MEDIA: the medium that shows the values wins over the default form. |
| §4.1 metaphor vs mechanism | OBJECT above MEDIA: the mechanism is the object; the metaphor is media, and sits beside. |

This order is my proposal. Where a rule sits is structure, and
structure is yours to rule (§7.1).

### 5.5 Identity — slugs, not numbers

- Each card carries a stable id, `family.slug`:
  `names.one-name-one-thing`, `order.first-sentence`,
  `object.quote-then-characterize`.
- Insertions never renumber and never produce a "3.4a".
- The cases file carries the map v1 § → v2 § → id, so every existing
  citation (§18a, §14a, §5a, §5.1a, §1.7, "§4 glossary form") stays
  resolvable through one table.

### 5.6 Voice

- One voice in the rulebook: you are "I"; the agent is "you".
- The third-person passages ("the owner: ...", "the owner had asked") move to
  the cases file, where an agent's account of an exchange is
  naturally in the third person. The rulebook then obeys §1.7 about
  its own author.

### 5.7 What "nothing dropped" means here

Every dated failure, every quote of yours, Appendix A entire,
Appendix B entire, §11's analysis, and the v2 header's own history
note: moved verbatim to the cases file under the rule id they
motivate. The v2 header promised nothing dropped; this keeps the
promise by the mechanism §9.2 already names — the log keeps the
account of how the rule was reached.

---

## 6. Cost, and the check that nothing was lost

- Rulebook size, estimated: root (12) + glossary (40) + precedence
  (25) + about 42 cards at 8 lines (340) + checklist (45) — about
  460 lines, four tenths of today's 1,112. Each task brief's "read
  in full first" then loads that instead.
- The lost-nothing check: a short script lists every v2 `##` and
  `###` heading and asserts each maps, in the id table, to a card
  in the rulebook and an entry in the cases file. It runs before
  the old file moves to `0_Archive/` as `LLM_communication_protocol_v2.md`.
- Effort: one session to write the cards and move the cases; the
  cards are mostly already-written first sentences.

---

## 7. What needs your ruling before any of it happens

These are structure and naming, which §7.1 puts with you.

- The precedence order in §5.4.
- Slug ids in place of section numbers (§5.5).
- Whether §6.2 and §6.3 move to `plan_and_code.md`, or stay in the
  rulebook as a WORKING family.
- Whether the cases file sits beside the rulebook in `DevComms/`, or
  in `0_Archive/`.

---

## 8. Small fixes worth making even if nothing above is adopted

Each is a one-line edit to the current file.

- §1.2, line 92: "§19's vocabulary lists" → "§11's vocabulary lists".
- §3 preamble, line 276: "These four rules" → "These seven rules".
- Swap §1.7 and §1.8 into numeric order (lines 157–201).
- §10: add lines for §1.7, §1.8, §3.4a, §3.5, §4.6, §4.7, §5.1a, and
  Appendix B.
- My memory file `explanations-full-mechanism.md`: "protocol §4
  glossary form" → "protocol §1.2 glossary form".
