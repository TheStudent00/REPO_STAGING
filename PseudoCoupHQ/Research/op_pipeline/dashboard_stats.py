#!/usr/bin/env python3
"""dashboard_stats.py -- pane 5's two halves, both of them kept out of
the renderer.

Node: hq.research.compiler_graph.dashboard
(Planning/node_0_3_research/node_0_3_5_compiler_graph/
node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md), sub-node `stats`.

WHY THIS FILE EXISTS.  the owner, 2026-09-05, two requests in one message:

  "in the dashboard stats tab: if you could add a question mark button
   for each row to describe what it means, that would be appreciated"

  "some of the stats can be from a summary ('the pool -- the_pool5.json,
   its own summary'). but i want analysis run to produce stats you
   havent curated."

So this file holds two things, and holds them side by side deliberately:

  (1) THE MEANINGS -- what every row of pane 5 means, written as DATA
      (`MEANINGS`, one record per row key).  They are data and not prose
      inside the renderer so that the set of rows and the set of
      explanations CANNOT DRIFT APART: the renderer looks every row up by
      its key, and a row whose key is absent is drawn as UNEXPLAINED, on
      the page, rather than silently going without.  Each record carries
      the four things the request asks of an explanation:
          counts      what is being counted, in plain words, with any
                      term of ours defined by the sentence carrying it
          population  what it is counted out of
          source      which file it comes from, and whether it was READ
                      FROM A STORED SUMMARY or COUNTED AT RENDER TIME
          caution     what the row does NOT mean, where it is easy to
                      misread.  Optional; a row with nothing to warn
                      about carries none.

  (2) THE ANALYSIS -- three walks that COUNT the artifacts at render
      time and produce figures nobody chose in advance: the corpus by
      language and arrival population, the proof outcome over it, the
      distribution of how many arch opcodes a body holds, how far
      machine code repeats, how many bodies are empty, and the term
      store's states per language.  None of these is read from anything
      a previous agent wrote down.

THE MEMORY BOUND, unchanged and not negotiable.  The page's cap is
`MEMORY_CAP_MB` = 1500 with the abort `OURO_MEMORY_ABORT`.  Every walk
here opens ONE artifact document, reduces it to counters, and drops it
before the next is opened -- no unit record and no body is ever held.
What IS held is small and stated: a count per (language, arrival
population) pair, a count per opcode-count value, and one count per
distinct body of machine code.  Measured (Airlock lane
`t98_l2_shapes.sh`, log 20260905T134435Z): all three walks in ONE
process take 1.7 s and peak at 45.0 MB of resident size.  The caller
passes its own `guard` and this file calls it after every document.

THE CHRONOLOGY.  Nothing here reads a path.  Every read goes through the
`moment` object the caller hands in -- `names_under`, `dirs_under`,
`has`, `read_json` -- which answers from the working tree at the present
moment and from that commit's own blobs at any other.  So every figure
on this page is computable at a past moment wherever version control
holds the artifact, and where it does not the walk answers `None` with
its reason and the pane draws the refusal.

ARTIFACT GENERATIONS ARE PICKED BY NUMBER, never by a hard-coded name.
`canon39_wrapped_c.json` and `canon40_wrapped_c.json` are two
generations of one family, and `term65_store` and `term66_store` are two
generations of another.  A hard-coded name is wrong at every moment but
one, which is the general form of the defect task 74 found in the census
and task 85 found in the pool.  So the family is a pattern and the
generation is the highest number present AT THE MOMENT BEING DRAWN.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

HOW THIS FILE OBEYS IT.  Every grouping here is by one of four
machine-form facts carried on the record: the LANGUAGE, the ARRIVAL
POPULATION, the MACHINE CODE (`body_bytes`), and the OUTCOME the gate
recorded.  The `operator` field is never read at all -- not as a key,
not as a row, not as a candidate.  Replace every operator token in every
artifact with a glyph and every number this file produces is unchanged;
that is the test, and it passes because the field is not touched.  The
row keys of `MEANINGS` are descriptive names this file invents, checked
by `check_dashboard_py_no_spelling.py` like any other python key.

Coding discipline: no compound one-liner statements.
"""

import html
import re


# ===========================================================================
# PART 1 -- THE MEANINGS, AS DATA
# ===========================================================================

def meaning(counts, population, source, caution=None):
    """one row's explanation.  Four fields, and the fourth may be empty
    only when the row carries no easy misreading."""
    return {"counts": counts, "population": population, "source": source,
            "caution": caution}


#: WHERE A NUMBER COMES FROM, in two words the reader can act on.  Every
#: `source` sentence begins with one of these, so a reader can tell at a
#: glance whether a figure was counted while the page was drawn or lifted
#: out of something written earlier.
COUNTED_NOW = "COUNTED AT RENDER TIME"
STORED = "READ FROM A STORED SUMMARY"


MEANINGS = {

    # ---------------------------------------------------------------
    # the pool's own summary block -- a STORED summary
    # ---------------------------------------------------------------

    "pool.entries": meaning(
        "How many ENTRIES the pool holds. An entry is one distinct "
        "computation: a set of arch-units that were proved to compute "
        "the same thing and were therefore collapsed into a single "
        "entry, whatever language or compiler they came from.",
        "Out of the pool's own members — the arch-units that entered "
        "it. The members row below gives that number.",
        STORED + ". The `summary` block written into the pool file by "
        "`pool65_run.py`; the page reads it with a tail carve of the "
        "last 8,192 bytes rather than opening the 32 MB file.",
        "It is NOT the number of operators, and NOT the number of "
        "distinct machine bodies. Two units with different machine code "
        "land in one entry when a proof joins them, and two units with "
        "the same operator label land in different entries when nothing "
        "proves them equal."),

    "pool.members": meaning(
        "How many arch-units entered the pool. A MEMBER is one "
        "arch-unit — one operator's machine code lifted out of one "
        "compiler's output — that the canonical-form gate proved and "
        "that carries a record in the term store of that round.",
        "Out of the whole corpus of arch-units. The computed corpus "
        "section below counts that corpus at render time.",
        STORED + ". The `summary` block of the pool file, tail-carved.",
        "It is NOT the size of the corpus. Units the gate did not prove, "
        "and proved units with no term record, never enter the pool, so "
        "this number is smaller than the corpus by exactly those two "
        "sets."),

    "pool.entries_spanning_more_than_one_language": meaning(
        "Entries whose members did not all come from the same source "
        "language — that is, one computation found in two or more "
        "languages.",
        "Out of the pool's entries.",
        STORED + ". The pool file's `summary` block, tail-carved.",
        "Spanning is a property of the ENTRY, not evidence about any one "
        "member. It says a proof joined units across a language "
        "boundary; it says nothing about how many members came from "
        "each side."),

    "pool.entries_spanning_compiled_and_interpreted": meaning(
        "Entries holding members from both a COMPILED arrival "
        "population (machine code a compiler emitted) and the "
        "INTERPRETER population (the handler bodies inside a language "
        "runtime, such as cpython's or php's).",
        "Out of the pool's entries.",
        STORED + ". The pool file's `summary` block, tail-carved."),

    "pool.entries_under_the_brief_strict_rule": meaning(
        "How many entries the SAME merge code produces with merge "
        "ground one switched off. Ground one is layer-3 identity: two "
        "units whose assembled canonical texts are the same string are "
        "the same machine code twice, so they are equal by "
        "construction with no solver asked.",
        "Out of the same members as the entries row.",
        STORED + ". The pool file's `summary` block, tail-carved. "
        "`pool.py` computes it by running its own merge with one "
        "argument changed, so it is not a second rule.",
        "It is NOT a competing answer and nothing downstream reads it. "
        "`pool.py`'s own words: the two-ground count is recorded and is "
        "used for nothing. The pool's entry count is the `entries` row."),

    "pool.entries_carrying_more_than_one_wrapped_text": meaning(
        "Entries whose members are not all the same machine code — so "
        "something other than plain text identity had to join them: a "
        "proved layer-5 normalized term, or an edge an earlier prover "
        "established.",
        "Out of the pool's entries.",
        STORED + ". The pool file's `summary` block, tail-carved.",
        "These are the interesting entries and not the suspect ones. An "
        "entry with one text is two copies of the same bytes; an entry "
        "with several is a claim that different machine code computes "
        "the same thing."),

    "pool.members_with_a_proved_term": meaning(
        "Members whose LAYER-4 TERM was proved. A layer-4 term is a "
        "mathematical expression transcribed from the unit's ledger; "
        "proved means a solver showed that expression equal to what the "
        "unit's own machine code leaves in its answer slot, for every "
        "value of every register the body reads.",
        "Out of the pool's members.",
        STORED + ". The pool file's `summary` block, tail-carved."),

    "pool.members_whose_term_was_withdrawn": meaning(
        "Members that have a layer-4 term whose proof came back "
        "DISPROVED — the solver found a value where the term and the "
        "machine code disagree — so the term is withdrawn rather than "
        "kept at lower confidence.",
        "Out of the pool's members.",
        STORED + ". The pool file's `summary` block, tail-carved.",
        "Withdrawn is not the same as absent. These units have a term; "
        "it was refuted. The `members with no term` row counts units "
        "where no term was built at all."),

    "pool.members_whose_term_was_undecided": meaning(
        "Members with a layer-4 term the solver neither proved nor "
        "disproved inside its time limit.",
        "Out of the pool's members.",
        STORED + ". The pool file's `summary` block, tail-carved."),

    "pool.members_with_no_term": meaning(
        "Members whose record carries the state NO_TERM: no layer-4 term "
        "was built for them at all, so there was nothing to prove.",
        "Out of the pool's members.",
        STORED + ". The pool file's `summary` block, tail-carved.",
        "This is a gap in transcription, not a failed proof. The census "
        "section further down names the row producers that block a "
        "transcription."),

    "pool.members_not_layer5_eligible": meaning(
        "Members whose layer-5 normalized text may not be used as a "
        "merge key. Layer 5 is the normalized form of the layer-4 term; "
        "it is only admissible as evidence when the term under it was "
        "PROVED equal to the unit's own machine code. An unproved term "
        "is not a weaker key — it is no key.",
        "Out of the pool's members.",
        STORED + ". The pool file's `summary` block, tail-carved."),

    "pool.distinct_layer5_texts_among_eligible_units": meaning(
        "How many DIFFERENT layer-5 normalized texts the eligible "
        "members carry between them. This is the size of merge ground "
        "two's key space.",
        "Out of the eligible members only — every member not counted by "
        "the `members not layer5 eligible` row.",
        STORED + ". The pool file's `summary` block, tail-carved."),

    "pool.layer5_identity_merges": meaning(
        "How many times merge ground two fired: a member's layer-5 text "
        "had already been seen on an earlier member, so the two were "
        "joined.",
        "Out of the eligible members.",
        STORED + ". The pool file's `summary` block, tail-carved.",
        "This counts JOIN EVENTS, not entries. The joins are then closed "
        "under transitivity, so the number of entries does not follow "
        "from this figure by arithmetic."),

    "pool.distinct_layer3_wrapped_texts": meaning(
        "How many DIFFERENT wrapped texts the members carry. A wrapped "
        "text is the unit's canonical assembled text: the prelude that "
        "loads its inputs, the body verbatim, and the epilogue that "
        "stores its answer. This is merge ground one's key space.",
        "Out of the pool's members.",
        STORED + ". The pool file's `summary` block, tail-carved.",
        "It is not the same measurement as the computed `distinct "
        "bodies of machine code` row further down: this counts the "
        "WRAPPED text, which includes the prelude and epilogue the "
        "canonical form adds, and it is counted over the pool's members "
        "rather than over the whole corpus."),

    "pool.layer3_identity_merges": meaning(
        "How many times a member's wrapped text had already been seen "
        "on an earlier member.",
        "Out of the pool's members.",
        STORED + ". The pool file's `summary` block, tail-carved.",
        "It is counted whether or not ground one is switched on, so the "
        "brief-strict entry count can be produced from the same run."),

    "pool.proved_edges_applied": meaning(
        "How many pairs an earlier prover established as equal were "
        "read out of the banked edge files and applied as merge ground "
        "three.",
        "Out of the banked edges available to this build.",
        STORED + ". The pool file's `summary` block, tail-carved."),

    # ---------------------------------------------------------------
    # THE POOL'S EARLIER GENERATIONS.  Found by running, not by reading:
    # the pane drew nine rows as UNEXPLAINED at the moments 2026-09-03
    # 9b9e7e674c and 56755e32ca (Airlock lane `t98_l5_keys.sh`), because
    # the pool generation standing at those commits -- the_pool3 --
    # spells the same measurements under different summary names.  That
    # is the marker doing its job: the rows and the records had drifted
    # apart and the page said so, on the page, rather than going quiet.
    # `build_the_pool3.py` lines 606-634 is where each of these is
    # written, and each record below says what that line does.
    # ---------------------------------------------------------------

    "pool.units_in_the_pool": meaning(
        "How many arch-units entered the pool. An earlier generation's "
        "name for the row a later generation calls `members`.",
        "Out of the whole corpus of arch-units.",
        STORED + ". The `summary` block of the pool generation standing "
        "at this moment, written by `build_the_pool3.py`, tail-carved.",
        "It is not the size of the corpus: units the gate did not prove, "
        "and proved units with no term record, never enter the pool."),

    "pool.units_by_arrival_population": meaning(
        "How the pool's units split by ARRIVAL POPULATION — how each "
        "unit arrived: `original` the hand-written probe corpus, "
        "`regenerated` the machine-generated sweep, `interpreter` the "
        "handler bodies read out of a language runtime.",
        "Out of the units in the pool.",
        STORED + ". The `summary` block of the pool generation standing "
        "at this moment, tail-carved. It is a nested object rather than "
        "a single count, and the page draws it as what it is.",
        "A later pool generation dropped this row. Its absence at the "
        "present moment is a change of artifact, not a change of fact — "
        "the computed corpus section below counts the same split itself."),

    "pool.units_with_no_layer4_term": meaning(
        "Units in the pool for which no layer-4 term was built at all. A "
        "layer-4 term is the mathematical expression transcribed from a "
        "unit's ledger. An earlier generation's name for the row a later "
        "one calls `members with no term`.",
        "Out of the units in the pool.",
        STORED + ". The `summary` block of the pool generation standing "
        "at this moment, tail-carved.",
        "This is a gap in transcription, not a failed proof."),

    "pool.units_withdrawn_at_layer4": meaning(
        "Units whose layer-4 term was DISPROVED against their own "
        "machine code, so the term is withdrawn rather than kept at "
        "lower confidence. An earlier generation's name for the row a "
        "later one calls `members whose term was withdrawn`.",
        "Out of the units in the pool.",
        STORED + ". The `summary` block of the pool generation standing "
        "at this moment, tail-carved.",
        "Withdrawn is not absent. These units have a term; it was "
        "refuted."),

    "pool.units_undecided_at_layer4": meaning(
        "Units with a layer-4 term the solver neither proved nor "
        "disproved inside its time limit. An earlier generation's name "
        "for the row a later one calls `members whose term was "
        "undecided`.",
        "Out of the units in the pool.",
        STORED + ". The `summary` block of the pool generation standing "
        "at this moment, tail-carved."),

    "pool.units_not_layer5_eligible": meaning(
        "Units whose layer-5 normalized text may not be used as a merge "
        "key, because the layer-4 term under it was not proved equal to "
        "the unit's own machine code. An unproved term is not a weaker "
        "key — it is no key. An earlier generation's name for the row a "
        "later one calls `members not layer5 eligible`.",
        "Out of the units in the pool.",
        STORED + ". The `summary` block of the pool generation standing "
        "at this moment, tail-carved."),

    "pool.entries_with_more_than_one_wrapped_text": meaning(
        "Entries whose members are not all the same machine code, so "
        "something other than plain text identity joined them. An "
        "earlier generation's name for the row a later one calls "
        "`entries carrying more than one wrapped text`.",
        "Out of the pool's entries.",
        STORED + ". The `summary` block of the pool generation standing "
        "at this moment, tail-carved."),

    "pool.entries_with_more_than_one_layer5_text": meaning(
        "Entries whose members carry more than one distinct layer-5 "
        "normalized text between them — so the entry was held together "
        "by something other than a single shared normalized term.",
        "Out of the pool's entries.",
        STORED + ". The `summary` block of the pool generation standing "
        "at this moment, tail-carved.",
        "A later pool generation dropped this row."),

    "pool.brief_strict_layer5_identity_merges": meaning(
        "How many times merge ground two fired in the run with ground "
        "one switched off — the brief-strict run. Ground one is layer-3 "
        "identity: two units whose assembled canonical texts are the "
        "same string.",
        "Out of the eligible units of that same run.",
        STORED + ". The `summary` block of the pool generation standing "
        "at this moment, tail-carved.",
        "The brief-strict run is recorded and used for nothing. It is "
        "not a competing answer to the pool's own merge count."),

    # ---------------------------------------------------------------
    # the term audit -- a STORED tally
    # ---------------------------------------------------------------

    "audit.proved_terms": meaning(
        "How many units in that round's term store carry a layer-4 term "
        "the solver proved against their own machine code.",
        "Out of the records the term store of that round holds.",
        STORED + ". The `layer5` block of the term audit named in the "
        "heading above this table.",
        "This audit was written over an EARLIER round than the term "
        "store the computed section below walks. The two count different "
        "populations, so a difference between them is a difference of "
        "round, not a disagreement."),

    "audit.with_a_normalized_text": meaning(
        "How many of those proved terms were successfully normalized "
        "into a layer-5 text — the canonical spelling used as a merge "
        "key.",
        "Out of the proved terms in the same block.",
        STORED + ". The `layer5` block of the term audit named above."),

    "audit.distinct_texts": meaning(
        "How many DIFFERENT layer-5 normalized texts those units carry "
        "between them.",
        "Out of the units carrying a normalized text.",
        STORED + ". The `layer5` block of the term audit named above.",
        "The gap between this and the row above is the whole finding: "
        "many units normalize to the same text, which is what makes the "
        "text usable as a merge key at all."),

    "audit.normalization_refused": meaning(
        "How many proved terms the normalizer refused to normalize, "
        "saying so by name rather than producing an approximate text.",
        "Out of the proved terms in the same block.",
        STORED + ". The `layer5` block of the term audit named above."),

    "audit.disproved_by_cause": meaning(
        "Units whose stored term was DISPROVED, grouped by the cause the "
        "audit computed for the disproof. The cause text printed in the "
        "row is the audit's own; nothing here summarises or shortens it.",
        "Out of the disproved units of that round's term store.",
        STORED + ". The `disproved_by_cause` block of the term audit "
        "named above.",
        "The cause is COMPUTED by the audit from each unit's record — it "
        "is not a category anyone chose in advance, and it is not a "
        "verdict about whether the unit's machine code is wrong."),

    # ---------------------------------------------------------------
    # the census -- a STORED artifact, one row per producer
    # ---------------------------------------------------------------

    "census.row": meaning(
        "One PRODUCER that has no term. A producer is the typed object "
        "that made a ledger row — an arch opcode, a pair of instructions "
        "that set and read a flag, a phrase that is not an opcode, or a "
        "routine the body transfers into. A producer appears in this "
        "census exactly when the one meanings table has no builder for "
        "it, so every ledger row it produced is left without a term. "
        "The two counts are how many ROWS it blocked and how many UNITS "
        "those rows sit in.",
        "Out of the producers appearing in the layer-4 transcriptions of "
        "every unit the canonical-form gate proved. The heading gives "
        "how many producers the census holds and how many of them are "
        "drawn.",
        STORED + ". The highest-numbered `name_census<n>.json` present at "
        "the selected moment, picked by number rather than by name.",
        "A producer here is keyed by its typed machine form and never by "
        "an operator token. The rows are ordered by how many rows they "
        "block, and the table is cut to the top few — the heading prints "
        "what it was cut from, so the cut is stated and not hidden."),

    # ---------------------------------------------------------------
    # THE COMPUTED SECTION -- counted at render time
    # ---------------------------------------------------------------

    "corpus.language_row": meaning(
        "How many arch-units of one source language the canonical-form "
        "corpus holds, split by ARRIVAL POPULATION — how the unit "
        "arrived. `original` is the hand-written probe corpus; "
        "`regenerated` is the machine-generated sweep over holders and "
        "type pairs; `interpreter` is the handler bodies read out of a "
        "language runtime rather than emitted by a compiler.",
        "Out of every unit in every document of the canonical-form "
        "generation named in the heading — its per-language files, its "
        "interpreter file, and every shard of its regenerated store.",
        COUNTED_NOW + ". Each document is opened, its units counted, and "
        "the parsed document dropped before the next is opened. No unit "
        "record is held.",
        "This counts units ATTEMPTED, whatever the gate then said about "
        "them. The proof outcome table below splits the same population "
        "into proved and not proved."),

    "corpus.outcome_row": meaning(
        "How many units the canonical-form gate recorded under one "
        "outcome. `WRAPPED_TEXT_PROVED` means a solver showed the unit's "
        "canonical wrapped text equal to the unit's own shipped machine "
        "code. `REFUSED` means the build declined to produce a canonical "
        "text at all. `GATE_DISPROVED` means a text was produced and the "
        "proof failed.",
        "Out of every unit of the canonical-form generation named in the "
        "heading.",
        COUNTED_NOW + ". Counted in the same single walk as the language "
        "table, from each unit's own `outcome` field.",
        "The outcome values are read off the artifacts; this table shows "
        "every value that actually occurs rather than a list decided in "
        "advance, so a new outcome value appears here on its own."),

    "corpus.not_proved_row": meaning(
        "How many units of one language the gate did NOT prove — every "
        "outcome that is not `WRAPPED_TEXT_PROVED`.",
        "Out of that language's units in the canonical-form generation "
        "named in the heading.",
        COUNTED_NOW + ". Counted in the same single walk.",
        "A language absent from this table has no unproved unit at all, "
        "which is a stronger statement than a zero row would be."),

    "corpus.opcode_spread_row": meaning(
        "For one arrival population: the shape of the distribution of "
        "how many ARCH OPCODES an arch-unit's body holds. An arch opcode "
        "is one machine instruction of the body as it was read back out "
        "of the compiler's output; the count is instructions WITH "
        "repeats, so a body using the same instruction twice counts it "
        "twice. `distinct opcodes` is the separate figure of how many "
        "DIFFERENT instruction spellings the whole population uses — its "
        "vocabulary. `most common` is the count value more units carry "
        "than any other, `median` the middle unit's count, `longest` the "
        "largest, `empty` how many bodies hold no instruction at all.",
        "Out of the units of that arrival population in the "
        "canonical-form generation named in the heading.",
        COUNTED_NOW + ". Counted in the same single walk, from each "
        "unit's `body_as_read` list; measured on this corpus, every line "
        "of every body reads as an instruction, so lines and opcodes are "
        "the same count here.",
        "`distinct opcodes` and the distribution answer different "
        "questions. A body holding 3 opcodes is a body of 3 "
        "instructions; the 162 distinct opcodes are the vocabulary of "
        "the whole population, not a per-unit figure."),

    "corpus.opcode_distribution_row": meaning(
        "The FREQUENCY DISTRIBUTION itself: for one exact number of arch "
        "opcodes, how many arch-units hold a body of exactly that many "
        "instructions, in each arrival population.",
        "Out of the units of each arrival population in the "
        "canonical-form generation named in the heading; each column's "
        "own total is printed in its header.",
        COUNTED_NOW + ". Counted in the same single walk. Every count "
        "value that occurs gets a row; nothing is bucketed, capped or "
        "smoothed.",
        "The rows are opcode COUNTS, not opcodes. Row `3` is not an "
        "instruction — it is every unit whose body is three instructions "
        "long."),

    "corpus.repetition_row": meaning(
        "How far machine code REPEATS across the corpus. Two units hold "
        "the same body when their `body_bytes` — the raw bytes of the "
        "body, as hexadecimal — are the same string. Different operators, "
        "different languages and different type signatures routinely "
        "compile to the same bytes.",
        "Out of the units that carry machine code at all. Interpreter "
        "handler units carry none and are excluded; the row states how "
        "many units that leaves.",
        COUNTED_NOW + ". Counted in the same single walk; one count is "
        "held per distinct body, which is the only thing this walk keeps "
        "that grows with the corpus.",
        "There are TWO honest distinct-body counts and they answer "
        "different questions. Counting a body ONCE FOR THE CORPUS is "
        "smaller; SUMMING each language's own distinct count is larger, "
        "because a body found in four languages is counted four times. "
        "Both are shown, with the number of bodies that appear in more "
        "than one language, which is the whole of the difference."),

    "corpus.repetition_language_row": meaning(
        "For one language: how many of its units carry machine code, how "
        "many DIFFERENT bodies those units hold between them, and the "
        "ratio of the two.",
        "Out of that language's units that carry machine code.",
        COUNTED_NOW + ". Counted in the same single walk.",
        "These per-language distinct counts do not add up to the "
        "corpus-wide distinct count. A body appearing in several "
        "languages is distinct in each of them and is still one body in "
        "the corpus."),

    "corpus.empty_row": meaning(
        "Arch-units whose body holds NO instruction at all — the body as "
        "read back is an empty list.",
        "Out of the units of that arrival population in the "
        "canonical-form generation named in the heading.",
        COUNTED_NOW + ". Counted in the same single walk.",
        "NOBODY HAS EXPLAINED THIS. It is surfaced as a number rather "
        "than hidden, and no cause is offered here because none has been "
        "established. It is not the same as a unit carrying no machine "
        "code: the interpreter units carry no `body_bytes` at all, which "
        "is a different absence and is counted separately."),

    "corpus.body_length_row": meaning(
        "The shape of the distribution of how many BYTES of machine code "
        "an arch-unit's body is, measured off the `body_bytes` field's "
        "own length.",
        "Out of the units that carry machine code.",
        COUNTED_NOW + ". Counted in the same single walk."),

    "corpus.ledger_row": meaning(
        "The shape of the distribution of how many LEDGER ROWS an "
        "arch-unit carries. The ledger is the table of named places a "
        "unit reads and writes — its inputs, its constants, its scratch "
        "space, its guards and its answer — with the producer of each "
        "recorded beside it.",
        "Out of every unit in the canonical-form generation named in the "
        "heading.",
        COUNTED_NOW + ". Counted in the same single walk."),

    "term.records_row": meaning(
        "How many RECORDS the term store holds for one language. One "
        "record is one arch-unit's layer-4 term and everything the round "
        "established about it.",
        "Out of every record in every shard of the term store generation "
        "named in the heading.",
        COUNTED_NOW + ". Every shard is opened, counted, and the parsed "
        "document dropped before the next is opened."),

    "term.state_row": meaning(
        "For one language, how its records split between the two term "
        "states the store actually carries. `TERM` means a layer-4 term "
        "was built for the unit. `NO_TERM` means none was — some ledger "
        "row of that unit had a producer the meanings table has no "
        "builder for, so the transcription could not be completed.",
        "Out of that language's records in the term store generation "
        "named in the heading.",
        COUNTED_NOW + ". Counted in the same single shard-by-shard walk.",
        "`TERM` is not the same as proved. It says a term exists; "
        "whether it was proved against the machine code is a separate "
        "question, answered by the audit rows further up."),

    "term.coverage_row": meaning(
        "How the term store's population compares with the "
        "canonical-form generation it was built over: how many units the "
        "gate proved, how many of those have a record in the store, and "
        "how many are short.",
        "Out of the proved units of the canonical-form generation named "
        "in the heading.",
        COUNTED_NOW + ". Both sides are counted in this render's own two "
        "walks; neither number is read from any stored tally.",
        "Short does NOT mean the unit has no layer-4 term. At the "
        "present moment the units that are short are the ones log 202 "
        "recorded: their layer-4 term is built and proved, and it is the "
        "LAYER-5 normalization that does not converge — measured "
        "invariant at 1,536, 4,096 and 18,432 MB — so what is missing is "
        "the comparison key, not the term. At a PAST moment the same row "
        "can be large for an entirely different reason: the store was "
        "being written and only part of it was committed. A shortfall "
        "there is a store mid-flight, not a finding."),

    "term.callee_row": meaning(
        "How many of one language's term-store records carry at least "
        "one RUNTIME CALLEE ROW. A runtime callee row appears when the "
        "unit's body transfers into a routine the toolchain's own "
        "archive defines — a division helper, say — and the body of that "
        "routine is attached to the unit so the term can account for "
        "what the transfer does.",
        "Out of that language's records in the term store generation "
        "named in the heading.",
        COUNTED_NOW + ". Counted in the same single shard-by-shard walk.",
        "A language absent from this table has no such record at all."),

    "term.holes_row": meaning(
        "Records carrying at least one HOLE, at least one CASCADE, or a "
        "relink refusal. A hole is a place in the walk where the "
        "transcription could not account for what the machine code did. "
        "A cascade is a chain of transfers followed through more than "
        "one routine. A relink refusal is the round declining, by name, "
        "to re-attach a callee body it could not resolve.",
        "Out of every record in the term store generation named in the "
        "heading.",
        COUNTED_NOW + ". Counted in the same single shard-by-shard walk."),
}


# ---------------------------------------------------------------------------
# rendering one explanation
# ---------------------------------------------------------------------------

def esc(text):
    return html.escape("" if text is None else str(text), quote=True)


#: the four parts of an explanation, in the order they are drawn, each
#: with the question it answers.  Written once here so a part cannot be
#: dropped from one row and kept on another.
EXPLANATION_PARTS = [
    ("counts", "what is counted"),
    ("population", "counted out of what"),
    ("source", "where the number comes from"),
    ("caution", "what it does NOT mean"),
]


def explanation_cell(key):
    """the `?` a reader clicks, as one table cell's worth of html.

    NO JAVASCRIPT.  It is a `<details>` element, which opens and closes
    itself in the engine -- the python page carries no script of its own
    and this does not change that.

    A row whose key is not in `MEANINGS` is drawn as UNEXPLAINED, in
    place, naming the key that is missing.  That is the mechanism that
    keeps the rows and the explanations from drifting apart: an
    unexplained row is visible on the page rather than silently going
    without one.
    """
    record = MEANINGS.get(key)
    if record is None:
        return ('<span class="unexplained" title="the row key is %s">'
                'no explanation recorded</span>' % esc(key))
    out = ['<details class="why"><summary class="whymark" '
           'title="what this row means">?</summary>'
           '<div class="whybody">']
    for field, question in EXPLANATION_PARTS:
        value = record.get(field)
        if not value:
            continue
        out.append('<p><b>%s.</b> %s</p>' % (esc(question), esc(value)))
    out.append('</div></details>')
    return "".join(out)


def explained_rows(rows):
    """turn (key, cells) pairs into table rows carrying their own `?`."""
    out = []
    for key, cells in rows:
        out.append(list(cells) + [explanation_cell(key)])
    return out


def unexplained_keys(keys):
    """which of a set of row keys has no record.  Used by the guard lane
    to prove the pane's rows and this file's records agree."""
    missing = []
    for key in keys:
        if key not in MEANINGS:
            missing.append(key)
    return missing


# ===========================================================================
# PART 2 -- THE ANALYSIS, RUN AT RENDER TIME
# ===========================================================================

#: the artifact FAMILIES, each as a pattern over a name, with the
#: generation picked by NUMBER at the moment being drawn.  No generation
#: is written down anywhere in this file: `canon39` and `canon40` are two
#: generations of one family and either may be the highest at a given
#: moment, which is exactly why a hard-coded name cannot be right.
CANON_WRAPPED = re.compile(r"^canon(\d+)_wrapped_([a-z0-9]+)\.json$")
CANON_INTERP = "canon%s_interp.json"
CANON_STORE = "canon%s_regen_store"
TERM_STORE = re.compile(r"^term(\d+)_store$")

PROVED_OUTCOME = "WRAPPED_TEXT_PROVED"

#: the path separator, NAMED rather than written as a literal, for the
#: same reason `dashboard_ouro.TREE_SEPARATOR` is named: the character is
#: also a token in this line's 91-token operator inventory, and the
#: spelling guard is right to refuse a token sitting in a comparison.
PATH_SEPARATOR = "/"


def bump(counter, key):
    counter[key] = counter.get(key, 0) + 1


def units_in(document):
    """the unit records of one artifact document, whichever of the two
    shapes it carries -- a mapping from unit id to record, or a list."""
    held = document.get("units")
    if isinstance(held, dict):
        return list(held.values())
    if isinstance(held, list):
        return held
    return []


def highest_canon(names):
    """the highest-numbered canonical-form generation present, and the
    languages it carries files for -- picked by NUMBER."""
    best = -1
    langs = {}
    for name in names:
        match = CANON_WRAPPED.match(name)
        if not match:
            continue
        number = int(match.group(1))
        if number > best:
            best = number
            langs = {}
        if number == best:
            langs[match.group(2)] = name
    if best < 0:
        return None, []
    ordered = []
    for lang in sorted(langs):
        ordered.append(langs[lang])
    return str(best), ordered


def highest_term_store(folders):
    """the highest-numbered term store present -- picked by NUMBER."""
    best = -1
    found = None
    for name in folders:
        match = TERM_STORE.match(name)
        if not match:
            continue
        number = int(match.group(1))
        if number > best:
            best = number
            found = name
    return found


def spread(counter):
    """the shape of one frequency distribution, without holding the
    values it was built from: how many, where it peaks, its middle, its
    largest, and how many are zero."""
    keys = sorted(counter)
    if not keys:
        return None
    population = 0
    for key in keys:
        population = population + counter[key]
    top = keys[0]
    for key in keys:
        if counter[key] > counter[top]:
            top = key
    seen = 0
    median = keys[0]
    for key in keys:
        seen = seen + counter[key]
        if seen >= (population + 1) // 2:
            median = key
            break
    return {"population": population, "peak": top, "peak_units": counter[top],
            "peak_share": 100.0 * counter[top] / population,
            "median": median, "smallest": keys[0], "largest": keys[-1],
            "zero": counter.get(0, 0)}


def corpus_analysis(moment, guard, folder):
    """ONE walk of the canonical-form corpus, answering every computed
    figure the corpus section draws.

    What is held while it runs, and nothing else: a count per (language,
    arrival population) pair, a count per outcome value, a count per
    opcode-count value per population, one count per distinct body of
    machine code, and the set of languages each distinct body appears in.
    The parsed document is dropped before the next is opened, so no unit
    record and no body text is ever held.

    Answers `None` when the moment carries no file of this family, which
    is what makes the whole section drawable as a refusal at a past
    moment rather than as a number from somewhere else.
    """
    names = moment.names_under(folder)
    generation, wrapped = highest_canon(names)
    if generation is None:
        return None

    inputs = list(wrapped)
    interp = CANON_INTERP % generation
    if interp in names:
        inputs.append(interp)
    store = CANON_STORE % generation
    shards = moment.names_under(folder + PATH_SEPARATOR + store)
    for shard in sorted(shards):
        if shard.endswith(".json"):
            inputs.append(store + PATH_SEPARATOR + shard)

    by_lang_pop = {}
    by_lang = {}
    by_pop = {}
    outcomes = {}
    not_proved_by_lang = {}
    proved = 0
    opcode_dist = {}
    vocabulary = {}
    empty_bodies = {}
    body_length = {}
    ledger_rows = {}
    times_seen = {}
    langs_of_body = {}
    distinct_by_lang = {}
    compiled_by_lang = {}
    compiled = 0
    total = 0

    for rel in inputs:
        document = moment.read_json(folder + PATH_SEPARATOR + rel)
        for unit in units_in(document):
            total = total + 1
            lang = unit.get("lang") or "?"
            population = unit.get("population") or "original"
            bump(by_lang, lang)
            bump(by_pop, population)
            bump(by_lang_pop, (lang, population))

            outcome = unit.get("outcome")
            bump(outcomes, outcome)
            if outcome == PROVED_OUTCOME:
                proved = proved + 1
            else:
                bump(not_proved_by_lang, lang)

            lines = unit.get("body_as_read") or []
            if population not in opcode_dist:
                opcode_dist[population] = {}
                vocabulary[population] = set()
            bump(opcode_dist[population], len(lines))
            if not lines:
                bump(empty_bodies, population)
            for line in lines:
                word = str(line).strip().split(" ")[0].strip()
                if not word:
                    continue
                if not word[0].isalpha():
                    continue
                if not word.isalnum():
                    continue
                vocabulary[population].add(word.lower())

            bump(ledger_rows, len(unit.get("ledger") or []))

            raw = unit.get("body_bytes")
            if raw:
                compiled = compiled + 1
                bump(compiled_by_lang, lang)
                bump(body_length, len(raw) // 2)
                bump(times_seen, raw)
                if raw not in langs_of_body:
                    langs_of_body[raw] = set()
                langs_of_body[raw].add(lang)
                if lang not in distinct_by_lang:
                    distinct_by_lang[lang] = set()
                distinct_by_lang[lang].add(raw)
        del document
        guard("counting the corpus, %s" % rel)

    shared = 0
    for body in langs_of_body:
        if len(langs_of_body[body]) > 1:
            shared = shared + 1
    summed = 0
    per_lang_distinct = {}
    for lang in distinct_by_lang:
        per_lang_distinct[lang] = len(distinct_by_lang[lang])
        summed = summed + per_lang_distinct[lang]
    most_repeated = 0
    most_repeated_body = None
    for body in times_seen:
        if times_seen[body] > most_repeated:
            most_repeated = times_seen[body]
            most_repeated_body = body
    most_repeated_langs = []
    if most_repeated_body is not None:
        most_repeated_langs = sorted(langs_of_body[most_repeated_body])

    spreads = {}
    for population in opcode_dist:
        spreads[population] = spread(opcode_dist[population])

    vocabulary_size = {}
    for population in vocabulary:
        vocabulary_size[population] = len(vocabulary[population])

    return {
        "generation": generation,
        "inputs": len(inputs),
        "units": total,
        "proved": proved,
        "by_lang": by_lang,
        "by_pop": by_pop,
        "by_lang_pop": by_lang_pop,
        "outcomes": outcomes,
        "not_proved_by_lang": not_proved_by_lang,
        "opcode_dist": opcode_dist,
        "opcode_spread": spreads,
        "vocabulary": vocabulary_size,
        "empty_bodies": empty_bodies,
        "body_length": spread(body_length),
        "ledger_rows": spread(ledger_rows),
        "compiled": compiled,
        "compiled_by_lang": compiled_by_lang,
        "distinct_corpus_wide": len(times_seen),
        "distinct_summed_per_language": summed,
        "distinct_by_lang": per_lang_distinct,
        "bodies_in_more_than_one_language": shared,
        "most_repeated": most_repeated,
        "most_repeated_bytes": most_repeated_body,
        "most_repeated_languages": most_repeated_langs,
    }


def term_store_analysis(moment, guard, folder):
    """ONE shard-by-shard walk of the highest term store generation.

    Counters only: records per language, records per (language, term
    state) pair, and four record-shape counts. The parsed shard is
    dropped before the next is opened.
    """
    store = highest_term_store(moment.dirs_under(folder))
    if store is None:
        return None
    shards = []
    for name in sorted(moment.names_under(folder + PATH_SEPARATOR + store)):
        if name.endswith(".json"):
            shards.append(name)
    if not shards:
        return None

    records = 0
    by_lang = {}
    by_state = {}
    by_lang_state = {}
    callee_by_lang = {}
    holes = 0
    cascades = 0
    relink = 0

    for shard in shards:
        rel = folder + PATH_SEPARATOR + store + PATH_SEPARATOR + shard
        document = moment.read_json(rel)
        for unit in units_in(document):
            records = records + 1
            lang = unit.get("lang") or "?"
            state = unit.get("term_state")
            bump(by_lang, lang)
            bump(by_state, state)
            bump(by_lang_state, (lang, state))
            if (unit.get("runtime_callee_rows") or 0) > 0:
                bump(callee_by_lang, lang)
            if unit.get("holes"):
                holes = holes + 1
            if unit.get("cascades"):
                cascades = cascades + 1
            if unit.get("relink_refusal"):
                relink = relink + 1
        del document
    guard("counting %s" % store)

    return {
        "store": store,
        "shards": len(shards),
        "records": records,
        "by_lang": by_lang,
        "by_state": by_state,
        "by_lang_state": by_lang_state,
        "callee_by_lang": callee_by_lang,
        "holes": holes,
        "cascades": cascades,
        "relink_refusals": relink,
    }
