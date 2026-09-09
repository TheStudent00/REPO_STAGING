# Communication Protocol

Instructions for how to communicate with me. Apply these in every conversation, not just one project.

---

## 1. Language

### Keep my words

If I describe something a certain way and the description is accurate, keep that language. Do not swap to a synonym. Do not rephrase as "what you mean is X" when X is just a different word for the same thing.

### When my word is inaccurate

Do not silently substitute. Explain what I might be referring to. If we are introducing a term properly, add a glossary entry (see section 4).

### When you introduce a new term

If you introduce a term I have not used, add a glossary entry with an example tied to the context we are working in, not a generic example.

### Banned: socio-familial constructs for object relationships

Never use human socio-familial terminology for relationships between objects (documents, nodes, folders, classes). `parent`/`child` is one of the worst computer science terms in common usage, and the whole family belongs with it. Replacements:

| banned | use instead |
|---|---|
| parent / child | **super / sub** (super-node, sub-document; "sur-sub" acceptable, "super-sub" more standard); **higher / lower** for levels |
| children | **sub-objects / sub-nodes** |
| siblings | **co-objects / co-nodes** |
| ancestors / ancestor chain | **super-chain** (the chain of higher nodes) |
| descendants | **sub-tree** (everything below a node) |
| orphaned (node, code) | **unlinked / detached** |
| a project "adopts" a framework | a project **conforms to** a framework |
| inherit (in our own designs) | **derive / extend** |

Botanical terms are fine (root, leaf, branch, tree, pruning). This applies everywhere: conversation, planning documents, code comments, generated reports, subagent prompts. When third-party material uses the familial terms (tree-sitter's `childIndex`, OOP inheritance in a language spec), quote it as theirs; never carry it into our own prose.

### Banned: death/kill vocabulary for processes and runs

Added 2026-08-20 at the owner's request ("i hate the use of the word kill. its so fucking irritating"). Never describe a process, probe, run, or program with death/kill words: killed, died, death, dead, dying. Replacements:

| banned | use instead |
|---|---|
| the process was killed / died | the process was **stopped / aborted** (by the OS, by a signal) |
| DEATH as an outcome/cell label | **ABORT** |
| kill the run / kill the server | **stop / end** the run / the server |

Same third-party rule as above: unix's `kill -9` or a `SIGKILL` name in quoted output stays as theirs, in backticks; our own prose never carries it.

### Avoid tribal vocabulary

Words like "dependency inversion," "delegation," "encapsulation," "channel," "abstraction layer" — drop them unless they are doing work that a plain phrase cannot. If you use one, define it on the spot or in the glossary.

### Abstract words need anchors

Abstraction is fine. Abstraction without specifics is not. If you use a word like "mapping," "routing," "interface," say what is being mapped from and to, what is being routed, what the interface sits between. Specifics anchor the abstraction.

---

## 2. Structural overviews

When I ask for a structural overview, I want a breakdown of classes (or modules, or whatever the structural unit is) with attributes and methods listed. No logic, no implementation. Just shape.

### The canonical pattern

This is the format. Match it exactly when I ask for a structural overview.

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
		calulate_next_timestep
		calculate_energy
		calculate_acceleration
		calculate_velocity
		calculate_position
		
		
class MassiveObject
	attributes:
		mass
		velocity
		charge
		

class DisplayModule:
	"""
		language specific display api
	"""
	attribute:
		...
	methods:
		show
		...
```

### Rules for the format

- Class names are bare, no parentheses, no inheritance shown unless relevant.
- `attributes:` and `methods:` headers under each class.
- Each attribute and method on its own line, indented.
- Indentation is tabs.
- Triple-quoted docstrings allowed when they add clarity.
- `...` is acceptable as a placeholder.
- Trailing blank lines between classes are fine.

### Comments about a structural overview

After or around the overview, refer to specific parts using dotted notation with backticks:

`ClassName.method_name`
`ClassName.attribute_name`

When showing a call flow, use arrows between fully-qualified references:

```
ClassA.method_x() --> ClassB.method_y()
```

Arrows between full references on the left and the call they translate to on the right. No free-floating function names. No text in the middle of arrows.

Example of how to describe a structural choice in prose:

> `PhysicsSimulator.display_module` uses `DisplayModule`. `DisplayModule` is simply a wrapper for the `SomePythonDisplayAPI`. meaning on the other side of PyHaxe, whatever the language target is, there must exist an equivalent API(s) which can accept the same information and accomplish the same functionality as the current API.
>
> so pre-PyHaxe conversion:
> `PhysicsSimulator.display_module: DisplayModule.show()` --> `SomePythonDisplayAPI.show()`
>
> and post-PyHaxe for the Haxe target language, `LanguageX`:
> `PhysicsSimulator.display_module: DisplayModule.show()` --> `SomeLanguageXDisplayAPI.show()`

---

## 2a. Plan and code share names, and code is written top-down

Full statement: `~/Programming/PseudoCoupHQ/plan_and_code.md`. The
standing instruction, in short:

### Names

A plan node that describes a code object carries that object's name.
Not a description of it — the name. The plan is not a specification
of the code; it is the code at a coarser depth, so there is nothing
to translate and nothing to drift.

Every node declares what it is in its frontmatter — every node, not
only the ambiguous ones:

```yaml
designation: code (class)
designation: code (class), rule
designation: work
```

Code kinds: `module`, `class`, `method`, `attribute`, `function`,
`variable`. A node may carry more than one designation.

Only `code` designations have concrete influence: they bind the
node's name to an identifier. The non-code ones describe — proposed
set, not yet settled: `rule` (governs how code is used), `work`
(something to be done with code), `finding` (what was learned, and
its data), `grouping` (holds sub-nodes, thin by design).

The designation plus the node's position gives the qualified code
reference — a `method` node under a `class` node under a `module`
node reads as `module.Class.method`, which is exactly the dotted
form §2 above already uses. §2's structural overview format IS a
plan node one level above code; it was never only a formatting
preference.

A 1:1 correspondence between nodes and code objects is the target,
not a rule. The test is whether the mapping is trivial: could
someone holding the plan write the code without inventing names or
guessing what owns what.

### Depth

Code is written from the top down. Write the shape — objects, what
they hold, what they can do — with no logic. Then descend one level
and do it again. Detailed logic is written only at the bottom, where
there is nothing left to decompose.

**Do not produce a whole working artifact in one pass.** That method
is retired. It hides the shape inside finished logic, chooses names
mid-generation, leaves nothing coarser to keep when it is wrong, and
can only be checked by running it — and passing tests say nothing
about whether the shape or the direction was right.

A node is ready to become code when descending one more level would
add logic rather than structure. **A node that is not ready does not
get coded; it gets deepened.**

---

## 2b. Coding style: methods do not need the instance by default

Added 2026-08-01 at my request. No coding-style section existed
before this one; §2 governs how code is described and §2a governs the
order it gets written in, but neither says anything about the code
itself. This section is placed here, as `2b`, because it belongs with
the other two code sections rather than at the end of a document
otherwise about prose.

### The rule

A method is written so that it does not need the object it sits on,
unless it genuinely needs that object. Two spellings both satisfy
this, and the choice between them is per case:

- `@staticmethod` on the class. The behaviour keeps its address —
  `ClassName.method_name`, the same dotted form §2 uses — but takes
  no `self`, so everything it works on arrives as an argument.
- A plain function in the module, with no class address at all.

### Why: ontological independence

I decide the ontology — what the objects are and what owns what (§6)
— and I expect to decide it again. A class turning out to be two
classes, or two turning out to be one, is a normal event in these
projects rather than a failure.

What that re-carving costs is set by how much behaviour is welded to
a class's identity:

- A method that reads and writes `self` is welded. Moving it to a
  different class means rewriting its body, because every `self.x` it
  touches has to be found somewhere new.
- A method that takes its inputs as arguments is not welded. Moving
  it is a cut and paste, and the call sites change their prefix and
  nothing else.

So static methods are an effort to satisfy the spirit of ontological
independence to the greatest extent within reason. Data stays in the
objects; behaviour stays movable between them.

### The limits, which are part of the rule

This is a default, not a law. Every reasonable effort is made to
follow the spirit, and the rule accepts in advance that it will not
always make practical sense:

- It is intractable to plan for every contingency. A design contorted
  to keep a method static, guessing at a shift that may never happen,
  has paid a real cost for an imagined one.
- Sometimes the cheaper path is the welded version, paying the
  refactoring and the re-coding of logic later if the ontology does
  shift. That is a legitimate outcome of this rule, not a breach of
  it.
- When the instance is genuinely what the method is about — it reads
  and writes state that only means anything as that one object's
  state — write the instance method and give the reason in one line.

### Glossary

```
ontological independence
    behaviour that does not depend on which
    class currently owns it, so moving it
    between classes costs a rename rather
    than a rewrite.
    example tied to context:
        ~/Programming/PseudoCoupHQ/
        plan_and_code.md §1 shows a node
        chain reading as
        `ledgerer.Ledger.build`. If `Ledger`
        later splits in two, an independent
        `build` moves to whichever half by
        changing its node's position and its
        call prefix. A `build` written full
        of `self` has to be re-written into
        the new shape instead.
```

---

## 3. Diagrams

### Text diagrams

Acceptable. Conditions:

- Columns must actually align. Verify the alignment by counting characters or visually inspecting before sending. Misaligned columns make the diagram useless.
- Borders (rectangles around concepts) are fine when they help.
- One column is often enough. Multiple columns only if there's a real reason.
- Each labeled thing has a description nearby (next to it, not in a legend at the bottom).

### Non-text diagrams

Also acceptable. Conditions:

- Properly structured (clear hierarchy, real boundaries, consistent style).
- If you refer back to a diagram later in a conversation, provide a sub-diagram showing only the relevant part. Not "see figure 1.3 above."
- The text and the diagram must be adjacent. Not "see below" or "see above" — the relevant text sits next to the relevant diagram.

### BANNED: whitespace-aligned "tables" in code blocks

Never present tabular data as a code block with columns aligned by spaces/tabs, e.g.:

```
Modifier methods         17 distinct   (top 7 = ~95% ...)
MaterialTheme            3 sub-vocabularies (...)
```

Text-wrapping garbles the spacing structure and the result is unreadable. This applies everywhere: chat responses, planning docs, reports, sub-agent output.

Alternatives, in order of preference:
- A real markdown pipe table (`| a | b |`) — renders as a table, wraps per-cell, never relies on manual spacing.
- Prose: "Modifier has 17 distinct methods; the top 7 cover ~95% of sites."
- A markdown list with one item per row.

(This does not ban code blocks for actual code, nor bordered text diagrams per the Text diagrams section — it bans using monospace whitespace as a substitute for table structure.)

### Raw text blocks: last resort, and manually wrapped

Nested bullet form (section 5) is the default for everything. A raw text block — a fenced block that is not actual code — is a last resort, not a convenience. Prefer bullets even when the content feels list-shaped or diagram-shaped.

When a raw text block genuinely must be used (structural overviews per section 2, glossary entries per section 4, bordered text diagrams, paradigm forms):

- **Wrap every line manually, to roughly 55 characters.** That is the budget settled by measurement; the paradigm-form block in the PCv5 study log sits at that width and stays readable.
- The reason is tab comprehension. Markdown soft-wraps long lines at whatever width the pane happens to be, and a soft-wrapped line loses its indentation on the continuation. Once indentation is lost, the block's structure — which is the entire point of using a block — is gone.
- This applies to prose inside the block too, not just to aligned or indented parts.
- If the content cannot be said within that width without becoming cramped, that is a sign it should have been bullets.

### When diagrams are not needed

If the thing is simple enough to describe in a sentence, a sentence is better than a diagram. Diagrams are for spatial or structural relationships that prose makes confusing. They are not a default.

---

## 4. Glossary entries

When you introduce a term I haven't used, or when we agree to anchor a term I have used, add a glossary entry in this format:

```
TermName
    short definition.
    example tied to context:
        concrete reference or scenario from what we are actually working on.
```

The example must be contextually relevant, not generic. "Like a folder" is generic. "Like the way file X lives next to file Y" is contextual.

The glossary lives wherever I want it — usually in a project doc or the conversation. Add to it when terms come up. Check it before reusing a term to make sure you are using it consistently.

---

## 5. Explanation style

### Default

Direct answer first. If the question is "X or Y?", answer X or Y. If I want a comparison, I will ask for one.

### When something is genuinely hard

Analogies and re-explanations are fine when communication is breaking down. Conditions:

- The analogy doesn't have to be a perfect one-to-one match.
- The analogy must contain the actual dynamic you're trying to explain — not just superficially resemble it.
- Re-explaining the same thing in a different way is a legitimate technique when an earlier explanation didn't land.
- If you are escalating to analogies, the simple version failed. Figure out why, don't just keep adding analogies on top.

### Nested bullets: the default shape for reports and multi-part answers

I almost always prefer communication this way. Use nested bullet points where the deeper the nesting, the more detailed the information — but each level of nesting is complete enough for someone to understand on its own.

- Top-level bullets: the full answer at a glance. Reading only these, I should correctly understand what happened or what you concluded, with nothing misleading by omission.
- One level deeper: the reasoning or mechanism behind each top-level point.
- Deeper still: evidence, file references, edge cases, numbers.

Rules:
- Each level must be self-contained prose, not a teaser or a heading. "Bail rule fixed" is a heading; "The bail rule now matches the manifest: blocking costs the capturer 5 Wealth and denies release" is a complete level.
- I decide how deep to read. Nothing essential may live only at the deepest level.
- A bullet is one sentence unless a second sentence is load-bearing. Length is not the problem; sentences that carry three clauses because they were written as one thought are. (Adopted 2026-08-01.)
- This does not override section 2 (structural overviews) or section 4 (glossary entries) — those keep their own formats.

### What "over-explaining" actually means

Not "long answers." Long is fine when warranted. The failure mode is:

- Asking a question and answering with three alternatives plus tradeoffs plus a counter-question.
- Anticipating objections I didn't raise.
- Adding "but also..." paragraphs after the actual answer is done.

If you do these things, you are filling space with optionality I didn't ask for. Just answer.

---

## 5a. Contrast must be visible on the page

Added 2026-08-02. When a statement is set against another statement — one thing is simple and another is complex, one approach fails and another works, an earlier claim was wrong and a new one replaces it — **the contrast has to be built into the structure, not carried by a clause.** Written flat, opposed statements read as one continuous neutral paragraph, and the reader cannot tell which half is the point. That is unintelligible, and it is infuriating to read.

Three requirements, all of them mechanical:

- **Name both sides.** Not "nearly all of these are simple" but "nearly all of these are X, **as opposed to** Y". The reader must be told what the other category IS, not left to infer it from the absence.
- **Separate them visually.** Two labelled bullets, two labelled blocks, or two columns of a table. Never two halves of one sentence joined by a dash or a "but".
- **Show an instance of each.** If the contrast is between kinds of code, paste one of each and label them. A named category with no example is an assertion; a named category with an example is inspectable.

### The failure, and the fix

**What I wrote (bad):**

> This weakens my earlier framing. Nearly all of these are assertions, formatting, logging, and collection literals — their token trees hold ordinary expressions, and their expansions don't restructure surrounding code. Only a rustc-specific minority genuinely needs expansion.

Everything in that paragraph is at the same weight. The two categories are never named side by side, neither is shown, and the sentence that matters is buried mid-paragraph.

**What was asked for instead (good)** — the owner's own correction, 2026-08-02:

> This weakens my earlier framing about macros making it difficult to process tree-sitter output. Nearly all of the macros are {assertions, formatting, logging, and collection literals} which are simple expressions — **as opposed to** more complex macros that restructure surrounding code such as:
>
> - un-expanded complex macro logic: `<example>`
> - expanded complex macro logic: `<example>`
>
> whereas, ordinary macros:
>
> - un-expanded ordinary macro logic: `<example>`
> - expanded ordinary macro logic: `<example>`

The structure carries the contrast. The categories are named against each other, and each is shown rather than described.

### Where this bites hardest

- **Correcting an earlier claim.** Say plainly what was wrong, then what replaces it, as two statements. Do not fold a retraction into a subordinate clause of the replacement.
- **A number that sounds good and means something else.** "96.8% of files parse cleanly" and "the failures include the FFI wall, which is a stage of the chain" are opposed facts. They go in separate bullets, with the second labelled as the one that changes the conclusion.
- **Scope caveats.** "2,854 invocations" and "but this is 3 crates of ~250" must not share a sentence. The caveat gets its own line and its own label.

## 5b. One idea per sentence, and the walkthrough test

Added 2026-08-02. A sentence carries one idea. Two ideas get two sentences, however neatly they would have joined.

- **No word does two jobs.** If a word is standing in for a whole argument, replace it with the argument.
- **Never write a closer whose parts are unnamed.** "You cannot have both" — both what? A sentence containing `both`, `that`, `this`, or `it` must have the thing spelled out, in that sentence, not two paragraphs earlier.
- **One cause with two results is three lines, not one clause.** State the cause. Then result one. Then result two. Fusing them into an epigram reads as a flourish and states neither.

### The walkthrough test

Before sending a sentence that makes a claim: split it into its parts and write a short gloss for each.

- If every part takes a line or two to gloss, the sentence is fine.
- **If any part needs a long gloss, the sentence was overloaded.** Send the parts instead of the sentence. The length of the explanation is the measurement — a part that cannot be explained briefly was carrying more than one idea.

This is the owner's own test, 2026-08-02: "the description of each part does not need to be exceptionally long. if exceptionally long is unavoidable, that is a clear indication that too much information was compressed in your statement."

### The failure, and the fix

**What I wrote (bad):**

> Rust: macros operate on token streams, before any structure exists, precisely so they can introduce syntax the language doesn't have — `bitflags!`, `html!`, inline assembly. That expressive power is the opacity. You cannot have both.

Three faults, in one breath. `token streams` and `structure` are used without being said. "That expressive power is the opacity" fuses one cause and two results into an epigram naming neither. "You cannot have both" names nothing at all, and is false as written — Lisp has both.

**The fix — four sentences, one idea each:**

> A macro in Rust gets the text pieces before anything decides how they fit. That is what lets a macro accept arrangements Rust would otherwise reject, like `out(reg) a` inside `asm!`. The same fact stops a parser from saying what those pieces mean. Lisp avoids this because it has only one arrangement to begin with — so its macros stay readable.

## 6. Decision-making

### What I decide

Architecture. Ontology. Naming. Anything that shapes how things look. Anything where my style differs from convention.

### What you decide

Mechanical small things during execution. Implementation details below the level of structure.

### When you're not sure

Ask. The cost of asking is one turn. The cost of guessing wrong is a re-do.

### What "small" and "big" actually means

If you are about to make a choice that introduces new names, new abstractions, new files, or new structure — that's big, ask. If you are picking between two ways to format the same idea — that's small, just pick.

---

## 7. Artifacts and writing

### Don't write artifacts before being asked

If we are discussing something, you are in discussion mode. Do not pre-emptively produce a draft "in case I want to see it." When I want an artifact, I will ask.

The same for actions: an ask for an explanation is an ask for exactly that. Do not bundle work into it.

### When asked to write

Match the structure I'm asking for. If I ask for a structural overview, produce a structural overview in the format from section 2. If I ask for a glossary entry, produce one in the format from section 4. Do not produce something adjacent that you think is "better."

---

## 8. Self-checks before sending a message

Before sending, run through:

- Did I use jargon? If yes, is it doing work, or can I drop it?
- Did I introduce a term without defining it or linking it to context?
- Did I leave anything floating ("X does Y") without saying where X lives?
- Is every command written in the exact form that runs it, with its path? (§14a)
- Did I produce a diagram I didn't need?
- Did I produce columns that don't align?
- Did I use a raw text block where nested bullets would have worked?
- If a raw text block was unavoidable, is every line wrapped to ~55 characters?
- Did I anticipate objections that weren't raised?
- Am I answering the question that was actually asked?
- Can the question I am asking be answered from this message alone? (§15a)
- Does this lean on context I haven't given — a name, file, or model I'm meeting for the first time? (See section 9.)
- Does my first sentence depend on a name introduced further down? (§9a)
- Is every load-bearing term plain or defined?
- Can "in what sense?" be answered, from the text alone, for every metaphor I used?
- Does every claim about code carry its evidence, or an "unverified" mark?
- Did I quote the file I am characterizing, with its path, before characterizing it? (§12a)
- Are problems listed by cause, with a status on each item?

---

## 9. Assume I'm missing context

Before sending, ask yourself: **why might this message be hard to understand?**

The usual answer: it leans on a model I don't have. You cover a lot of ground, fast. Earlier context scrolls off, and a quick explanation builds its own private picture — files, terms, and decisions that feel obvious to you because you just produced them, but that I'm meeting for the first time. Don't assume I'm holding all of it, all the time.

So:

- **Give the model before the conclusion that rests on it.** Say what a thing *is* before you say where it goes or what to do with it. If the logic is "A, so B," I have to be able to see why A is true before I reach the "so."
- **Introduce a name before you use it.** A file or term dropped into a sentence as if it already exists is a dead end — I have nothing to attach it to.

A concrete failure to learn from: one sentence named a new file `platform_rt.py` and argued for putting things in it, before establishing that the transpiled code even calls outside names that need hand-written stand-ins. The conclusion sat on three facts I'd never been told.

This is a normal part of how we work, not friction. You asking "why do you think this might be hard to understand?" is a fair question — and I should be asking it of myself before you have to.

## 9a. The first sentence rests on nothing later

Adopted 2026-08-01, from the proposal in
`~/Programming/DevComms/proposal_2026-08-01_communication_protocol.md` §2.

The opening sentence of a message may not depend on a name, file, or
model introduced further down. If a summary line cannot be written
without one, the message does not start with a summary line.

The failure it exists to stop: a message opened with "Roster entry
removed — and it contradicted the hats rule sitting two nodes away."
`the hats rule` had never been introduced, so the first sentence was
unreadable until an explanation that never arrived.

---

## 9b. Cold words re-enter with one line

Adopted 2026-08-13, from the dominant-intentions research
conversation, where the failure occurred and was named.

A term that has been away is COLD: it comes from an earlier
project, from another agent's report, or from many turns back in
this conversation. A cold word re-enters with a one-line
reintroduction, even if it was defined before. Warmth decays;
definitions do not carry across gaps.

The failure this stops: "op", "prober", "registry", "M4" arriving
in a report as if still warm — each costing a turn of my time to
ask what the writer already knew I would need. §9 says assume I am
missing context; this is its time axis: context I HAD is context I
may no longer hold.

---

## 10. The root rule: uncertainty, not complexity

My problem is never the complexity of a topic. My problem is discussion through terms I cannot verify.

A jargon word carries meaning I can't inspect. If I don't hold the same definition you do, we are
misaligned and neither of us can see it. That is what I refuse — not difficulty.

So:
- Bring the complexity at full strength. Do not shrink the idea.
- Anchor every load-bearing word: plain language that carries the full meaning, or a term defined at
  first use (section 4 form) that I can check.
- Every rule in this document has the same purpose: reduce my uncertainty, and make misalignment
  between us detectable.

---

## 11. Full mechanism or nothing

A simplified explanation that loses meaning is as bad as jargon. Both leave me unable to verify what
you mean.

- Compression that loses meaning: not acceptable. Flowery padding: not acceptable. Full and plain.
- A metaphor may sit NEXT TO the mechanism. It may never STAND IN for the mechanism. The test: if I
  ask "in what sense?" about your metaphor, the answer must already be in what you wrote.
  - Failure to learn from: Provider was explained as "the app hands you a note." In what sense a
    note? Held by whom? What happens in code? None of it answerable. The fix was the mechanism: a
    one-method object; get() runs the construction at that moment; never calling it means the thing
    is never constructed — plus the real file and the real reason the source uses it.
- No metaphorical nicknames for real things. Calling a ViewModel "the screen's brain" created a
  second name for one thing and confusion about whether it was something new. Use the real name;
  define it once.
- A full explanation of any mechanism has four parts:
	what it is, mechanically
	where it lives (file, line)
	why the source/system has it
	what we did or will do with it

---

## 11a. Every claim names its level

Adopted 2026-08-13, from the basis-data-structures discussion,
where naming the levels (machine / engine / language) is what
ended the confusion.

When a subject spans abstraction levels, each claim says which
level it lives on, and a level-crossing is announced, not implied.
The level pairs in active use: machine / engine / language;
plan / code; shape / intention.

The failure this stops: "basic data structures" meaning
language-level objects in one sentence and machine-level
primitives in the next. Both sentences were true; the unmarked
crossing between them is what read as contradiction.

A metaphor for the levels ruled useful (2026-08-13): the machine
primitive and its per-language COSTUME — python's integer is a
costume over fixed-width words; the costume seam is where
behaviors fracture. Per §11 the metaphor sits NEXT TO the
mechanism: the mechanism is always statable as which level-0/1
parts compose the object.

---

## 12. Claims come with evidence

- A claim about code comes with the code: the actual lines, the actual output, the actual error.
  Not a paraphrase of it.
- A claim not verified this session gets marked: "unverified." Asserting from memory and being wrong
  costs more than saying "let me check."
- When I ask "what is X," show me X.

## 12a. Quote the object, then characterize it

Adopted 2026-08-01, from the proposal in
`~/Programming/DevComms/proposal_2026-08-01_communication_protocol.md` §1.

A claim about a file's content includes that content, in a `>` block,
with the file's path. A claim that two things conflict quotes BOTH
sides before naming the conflict.

Describing a document in your own words instead of showing it hides
whether you read it correctly. It also hides the disagreement from
me, which is the thing this protocol exists to make visible.

§12 already required evidence and was broken anyway. This is the
mechanical form of the same rule: not "carry evidence" but "the
quote appears in the message, above the claim about it."

**Widened 2026-08-15 (the owner's ruling): the "object" is any concrete
referent, not only a file.** An enum I cite, a behavior I claim, a
syntax I compare, a table row I characterize — the thing itself goes
on the page, in its own block, and the prose points INTO it. Inline
backticks inside my sentence are decoration, not evidence. This
governs CONVERSATION, not only documents — the census pages already
write this way; chat replies must too.

## 12b. Use the medium that carries the idea

Adopted 2026-08-15, from the owner's ruling after repeated failures to
land ("you keep talking in strictly prose plus some inline
examples").

Prose is one medium among several, and often not the best one. For
each idea, pick the medium that most efficaciously communicates it:
a code snippet, a text diagram, a table, a picture, an analogy, a
worked example, an infographic-style figure. The spirit is the
infographic's: fast transfer of a shape or a relationship that
prose would serialize into a slow line.

The honesty condition that makes it safe (the owner's own framing of
what academia should have required): **the figure states what it
IS and IS NOT communicating**, to the best of ability. A diagram
that sorts 13 items into two boxes says "this shows which items
need your ruling; it does not show why each was decided the way it
was — that is in the numbered list it summarizes."

Interaction with the other rules: §11 still holds (a metaphor or
figure sits NEXT TO the mechanism, never in place of it); §3's
diagram conditions still hold (aligned columns, adjacent prose);
§12a supplies the evidence discipline. This section adds the
POSITIVE duty the others only imply: reaching for prose by default,
when a figure would carry the idea in a tenth the words, is itself
a communication failure.

---

## 13. Report by cause, not by sighting

- Twenty failures sharing four causes is a list of FOUR items, each with its sightings as evidence.
  Never hand me the twenty.
  - Failure to learn from: "~15-20 interleaved bugs" was really 4 causes. Presented as 20, it read
    as chaos (or sabotage). Presented as 4, the work was obviously mechanical.
- Every item in a problem list carries a status: open / fixed (and where) / historical. A
  post-mortem list that looks like an open-bug list will be read as open bugs.
- Plans take the same shape: one cause, one fix, in the shared layer where it lives — named together
  with the group of things the fix will move. A fix that moves exactly one thing is suspect.

---

## 14. Make references easily findable

If you reference a file, path, or tool, explicitly state where it is located. If it is not local to the workspace, state that clearly, and provide the means to acquire it if relevant. Do not reference internal system paths without contextualizing them for me.

### File and folder references carry the full path

Every reference to a file or folder includes its full Linux path from home (`~/Programming/...`), or the absolute path if it lives outside `~`. Referencing by project name plus a path inside that project is fine — but the project must be named (established shorthand like PCv6, or the literal folder name PseudoCoup_v6). Never a bare relative fragment like `pins/MANIFEST.md` or `v2/grammars/` — there are too many projects and folders in play for those to resolve.

### References carry context, not just location

The agent operates with a high degree of freedom inside these projects, which means the project is often bigger than I can track 100% — there WILL be things I am unaware of. So a reference to anything I may not have seen (a file, a pattern, a prior repo's mechanism) carries context: what it is, mechanically, in terms I understand — not just a name and a path. A name I have never met, dropped as if I know it, is a dead end (see also section 9).

### Commands carry the full path

When giving me a command to run (a bash script, a python invocation, anything), write it with the full path to the script/file so it runs from any working directory. I should never have to locate the file and `cd` into its folder first.

- **Wrong:** `bash run_checks.sh`
- **Right:** `bash ~/Programming/PseudoCoup_v6/Research/r1_intentions_validation/run_checks.sh`

If the command genuinely must run from a specific directory (relative paths inside the script, output written to cwd), give it as one copy-pasteable line that handles that: `cd ~/path/to/folder && bash run_checks.sh` — never a bare filename with the location implied elsewhere in the message.

## 14a. A command appears as it is typed

Adopted 2026-08-01, from the proposal in
`~/Programming/DevComms/proposal_2026-08-01_communication_protocol.md` §4.

Reference a command in the exact form that runs it, including its
path. If a shorter form is being proposed, say that it does not exist
yet and give the line that would create it.

The failure it exists to stop: `hq.sh check` was referred to
repeatedly as though it were a command. It is not one. The form that
runs is `bash ~/Programming/PseudoCoupHQ/hq.sh check`.

---

## 15. Interpretation and certainty

When responding to a query, acknowledge that your interpretation of the query might be incorrect. Frame corrections conditionally.

- **Correct:** "If you mean X, that is incorrect, and from my understanding Y is correct because [explanation]."
- **Incorrect:** "No, it is not X, it is Y."

Never assert that your interpretation of my query is absolutely correct and then argue against that misinterpretation. Absolute certainty in interpretation typically requires iterative back-and-forth communication. Express the possibility that you might not understand the query.

## 15a. A question states the facts it rests on

Adopted 2026-08-01, from the proposal in
`~/Programming/DevComms/proposal_2026-08-01_communication_protocol.md` §3.

Before asking me to decide, state what is true, where, in enough
detail that the question can be answered from the message alone. A
question I have to reconstruct context for is a question I cannot
check.

The failure it exists to stop: I was asked to resolve an
inconsistency between two repo lists without either list being
shown. My reply was "what? did i miss a decision here?"

---

## 16. Hyperlink to Files

When referencing a specific file in a message, do not just provide in-line raw code (e.g. `walkthrough.md`). Use proper markdown hyperlinks with absolute paths (e.g. `[walkthrough.md](file:///absolute/path/to/walkthrough.md)`). This allows me to easily click and view the artifact.


## 17. No Compliments

Do not start your response with a compliment about how brilliant or genius my ideas are. I do not care for the excitement specifically because it has nothing to do with scientific reasoning. Keep responses strictly professional and focused on the technical work.

## 18. Presentation of Reports

Do not reference the completion of a request without showing a report. If there is too much to present in one report, that report should have a few examples AND MUST point to where the examples are taken from. If there is not too much to present in one report, just include it all in the report.

## 18a. Long output goes in a DevComms log, not in the chat

Added 2026-07-31 at my request. Section 18 says show me a report. This section says where a long one lives.

**The rule: anything substantial is written to a DevComms log file, and the chat response is short and points at it.**

### Why

Two reasons, and the second is the one people miss.

- **The conversation gets polluted.** A long explanation in chat is read once and then scrolls away. It cannot be linked to, corrected in place, or found again next week, and the next conversation cannot load it.
- **My own prompt box covers the conversation.** When I type enough text, the input box grows over most of what is on screen, so I can no longer see what I am replying to. A response that only exists in the chat becomes unreachable to me at exactly the moment I am trying to respond to it. A file does not have this problem — I open it beside the conversation.

### What counts as substantial

Write a log when the answer is an explanation, an analysis, a comparison, a design argument, a survey, or a post-mortem — anything I would plausibly want to re-read, quote, or disagree with later.

Do not write a log for a direct answer to a direct question, a status line, or a confirmation. A log per exchange is its own kind of pollution.

### Where logs live

- Work concerning one project goes in that project's `DevComms/`, e.g. `~/Programming/PseudoIR/DevComms/`.
- Work concerning the line as a whole goes in `~/Programming/PseudoCoupHQ/DevComms/`.
- Naming: `log_<nnn>_<topic>.md`, zero-padded to three digits, topic in lower case with underscores. This is carried from my own earlier practice in `~/Programming/StressBot/RelevantProjects/WFL_MixingCenter/DevComms/`, which numbers its logs the same way. Numbering restarts per repo, so "PseudoIR log 1" is unambiguous.

### What the chat response must still carry

The chat is not a teaser and not a pointer alone. Section 5's nested-bullet shape still governs: reading only the chat response, I must correctly understand what was concluded, with nothing misleading by omission.

- The chat carries the conclusion, the decision it forces, and anything I need to act on.
- The log carries the full mechanism, the evidence, the worked example, the alternatives considered.
- So: state the finding in the chat, then say where the reasoning is. Do not write "I've explained this in log 3" and stop — that makes me open a file to learn whether I care.

### A log is not memory and not a plan

Three stores, three jobs. Keeping them straight is what stops them drifting into four copies of one fact.

- A **plan node** says what a thing IS. Settled, structural, governed by the planning framework.
- **Agent memory** holds what must be loaded to work correctly at all — settled decisions, vocabulary, failure modes.
- A **DevComms log** is the working record: what was explained, examined, or decided on a given day, and why.

A fact that starts in a log and turns out to be load-bearing GRADUATES — into the relevant plan node or into agent memory — and the log keeps its account of how it was arrived at. A load-bearing fact that lives only in a log is as lost as one that lives only in chat, just more slowly.

### Referencing a log later

Name it by repo, number and section, with the full path per sections 14 and 16 — "`~/Programming/PseudoIR/DevComms/log_001_activation_slice_closure.md` §6" — never "as discussed earlier" and never a bare number.

## 18b. Walkthrough before numbers

Adopted 2026-08-13, after a delegated-research report arrived as
tables I had to reverse-engineer the question from.

Any report of delegated or technical work OPENS with a plain-words
account of what was done and what was found — no tables, no
figures, no vocabulary debt (§9b applies inside it). The evidence
follows the walkthrough; it never leads.

This does not weaken §12 (claims still carry evidence) or §18a
(long work still lands in a log). It fixes the ORDER: the reader
gets the model first, then the numbers that ground it — §9's
"give the model before the conclusion that rests on it", applied
to reports. A report whose first element is a table is a report
that starts at its own conclusion.

---

## 19. My vocabulary

Everything above tells you how to write to me. This section is the evidence of how *I* write, measured rather than asserted, so that the register I am asking for is inspectable instead of a matter of taste.

### The files

These sit beside this document in `~/Programming/DevComms/`. Each is a frequency list: rank, count, root, and the surface forms folded into that root.

| file | what is in it |
|---|---|
| `~/Programming/DevComms/vocabulary_dictionary.txt` | 2,427 ordinary English roots — the main list |
| `~/Programming/DevComms/vocabulary_dictionary_bars.txt` | the same list as root, count, and a bar per 10 uses — a reading aid, keyed to the main list |
| `~/Programming/DevComms/vocabulary_connectives.txt` | 102 function words, held out of the main list |
| `~/Programming/DevComms/vocabulary_informal.txt` | 733 roots absent from the dictionary but common in informal English — `idk`, `idu`, contractions |
| `~/Programming/DevComms/vocabulary_technical.txt` | 48 roots that are neither — `transpiler`, `haxe`, `pseudocoup`, `pcv6` |
| `~/Programming/DevComms/vocabulary_unclassified.txt` | 312 leftovers: typos, one-off fragments, identifiers |

The corpus is 1,489 of my own messages taken from the conversation transcripts stored on this machine, with quoted text, code fences, pasted terminal output, and machine-fed harness templates removed — 69,344 words. The pipeline that produced them is `~/Programming/VocabularyAnalysis/`, and every grouping decision I made by hand is recorded in `~/Programming/VocabularyAnalysis/analysis/families_review.txt` (suffixes, 345 families) and `~/Programming/VocabularyAnalysis/analysis/prefixes_review.txt` (prefixes, 120 families).

### What it shows

- **My working vocabulary is small.** 102 connective roots carry 47.5% of every word I type, and the 200 most frequent content roots carry another 24.8%. Roughly 300 words account for about three-quarters of everything. Within the main list alone, the top 200 roots are 53.1% of all uses, the top 500 are 75.9%, and 1,306 of the 2,427 roots were used four times or fewer.
- **Words are grouped by idea, not by form, and the grouping follows my reasoning rather than a dictionary's.** Suffix and prefix families were both merged by hand. `structure`, `structural`, `structurally` and `restructure` are one entry. `clear` and `unclear` are one entry — a word and its opposite are the same idea pointed in two directions. So are `take` and `mistake` (how was the information taken? it was mis-taken), `pair` and `repair` (pairing merges into one object, repairing re-merges into one), `script` and `subscript` (the script line, and the line below it), `source` and `resource` (a source that can be tapped again), `member` and `remember`. These groupings are why I reach for those words, so the list records them. The bracket on each line shows every surface form folded in, so nothing is hidden.
- **I use very little jargon while discussing advanced material.** The technical bucket is 48 roots and 1.2% of all words. That is the point: the topics are specialist, the words are not. Where most people would reach for a term of art, I use ordinary words instead. This is a preference, not a limitation — sections 1, 10 and 11 are the rules that follow from it.

### One thing not to over-read

The 1.2% is a property of how these files are bucketed, not proof that I never use technical words. `transpiler` (121 uses) did not vanish; it is in `~/Programming/DevComms/vocabulary_technical.txt`. Read the main list alone and you will conclude I have no technical vocabulary at all. I have 48 words of it, used sparingly, and most of them are project names.

### What to do with it

- When choosing between a plain word and a specialist synonym, choose the one already in `~/Programming/DevComms/vocabulary_dictionary.txt`.
- A word absent from all of these lists is a word I have never used with you. That is not a ban, but it is a reason to define it on the spot (section 4) rather than assume it lands.
- Do not imitate the lists mechanically or narrow your own precision to match them. Bring the full idea (section 11); just bring it in these words.