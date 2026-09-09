# log 013 — history of the three gap-questions: sum types, error flow, aliasing

2026-08-06. ARCHIVE RESEARCH FOR DEE'S REVIEW. Nothing here is a
decision, a correction, or an amendment. Nothing was edited; one file
was written, this one.

**The question.** the owner, 2026-08-05, on the three gap-questions raised in
`~/Programming/PseudoCoup_v5/DevComms/log_011_uncertain_families_evidence.md`
§"do the five families expose gaps in the intentions data itself?" (G1
sum types, G2 error flow, G3 aliasing), all three absent from
`~/Programming/PseudoIR/Tools/intentions/pc_intentions.json`:

> "i think error flow was included at one point. i vaguely remember
> something about aliasing. i dont recall sum types at all."

**What was searched.** The artifact's own provenance chain
(`pc_intentions.json` `meta`, `intentions_data.py` provenance header,
`README.md`); the full git history of the deleted
`~/Programming/PseudoCoup_v5/Designing/` folder (four commits, all nine
files reconstructed and grepped); the git history of
`~/Programming/PseudoIR/Tools/intentions` (three commits);
`~/Programming/PseudoCoup_v5/DevComms/language_divergence_study_log.md`,
`dev_plan_log.md`, `open_issues.md`, `project_state.md`, `log_008`;
`~/Programming/PseudoCoup_v6/Research/r1_intentions_validation/REPORT.md`;
and `~/Programming/0_Archive/` (PseudoCoup_v1–v4, PseudoIR,
PseudoIR_(retired), WFL_PseudoCoup_Briefing). Search terms: error,
exception, propagat, alias, borrow, sum type, variant, enum, tagged
union, Result, Option, Either.

**Quote-first protocol (§12a).** Every claim below leads with the
verbatim text and characterizes afterward. Every quote carries a
re-findable ref: an absolute path, or a `git show <sha>:path` form.

---

## the provenance chain, established first

All three questions turn on one event, so it is worth fixing before the
per-gap sections. The current artifact is a copy-forward, and the
copy-forward was PARTIAL BY DESIGN.

`~/Programming/PseudoIR/Tools/intentions/intentions_data.py`, lines
588–591 (the comment introducing the field that carries the 11 objects):

> ```
> # Extension field 3: MINIMUM_SET
> # The 11-object minimum intention set, lifted by reading
> # minimum_intention_set.md ("The set" section, post-audit form).
> ```

And the same file's `README.md` provenance section
(`~/Programming/PseudoIR/Tools/intentions/README.md`):

> - minimum_set: `~/Programming/PseudoCoup_v5/Designing/minimum_intention_set.md`
>   (the 11 objects, post-audit).

The source document has SIX sections, not one: "The set", "Why the set
stops here", "Derived (not in the set)", "Relation to the divergence
study", "Audit: the 12 languages' signature intentions, derived",
"Non-object finding", "Audit verdict", "Open". Only "The set" was
lifted. Two of the three items the owner is asking about live in the sections
that were not lifted — and, as §2 and §3 below show, they live there as
POSITIVE RULINGS OF EXCLUSION, not as omissions.

Dates for the whole chain:

| date | event | ref |
| --- | --- | --- |
| 2026-07-17 | earliest error-propagation discussion found | file mtime, `~/Programming/0_Archive/PseudoIR_(retired)/v4/.planning/GeminiDiscussions/low_level_dependencies.md` |
| 2026-07-22 | divergence log lists "exception semantics" as an uninvestigated candidate class | `language_divergence_study_log.md:182`, under the `## Entry 2026-07-22` headings |
| 2026-07-24 15:57 -0400 | `Designing/minimum_intention_set.md` first appears in PCv5 git | `git -C ~/Programming/PseudoCoup_v5 show 866ee4d` ("PCv5 initial: migrate theory docs…") |
| 2026-07-24 21:15 -0400 | `pc_verdicts.json` + `build_verdicts.py` added | `git show 9eec26c` |
| 2026-07-27 13:04 -0400 | last PCv5 commit holding `Designing/` | `git show 7efb6e6` |
| 2026-07-28 | R1 verification; copy-forward into PseudoIR | `~/Programming/PseudoCoup_v6/Research/r1_intentions_validation/REPORT.md` (dated in its own header); `intentions_data.py` header "Copied forward: 2026-07-28" |
| 2026-07-31 11:44 -0400 | first PseudoIR commit containing `Tools/intentions/intentions_data.py` | `git -C ~/Programming/PseudoIR show 9abc927` |
| 2026-08-01 07:51 -0400 | `Designing/` deleted | `git -C ~/Programming/PseudoCoup_v5 show 21cef81` ("Gutting: 550 MB -> 55 MB.") — note the commit timestamp is 08-01, not 07-31 as the gutting is usually dated |
| 2026-08-05 | log_008 and log_011 raise the three as questions | file headers |

`minimum_intention_set.md` is BYTE-IDENTICAL across all three PCv5
commits that contain it (md5 `9e28bd047dde7f7641f44c6999d6f6f9` at
866ee4d, 9eec26c and 7efb6e6). It was never revised. And `MINIMUM_SET`
in `intentions_data.py` is 11 objects in all three PseudoIR commits
(9abc927, 2682a16, 049a8e3) — it never shrank there either. So there is
exactly one transition point for all three questions: the 2026-07-28
lift, which took one section of one document.

---

## 1 — sum types

### 1.1 every appearance found, chronological

| # | date | ref | quote |
| --- | --- | --- | --- |
| S1 | 2026-07-24 (first in git; document undated internally) | `git show 866ee4d:Designing/minimum_intention_set.md`, §"Audit", lines 152–155 | "optionals, null safety<br>(Swift, Kotlin, TS, Rust)<br>= record with a tag field<br>+ choice on the tag." |
| S2 | same file, lines 50–51 | `git show 866ee4d:Designing/minimum_intention_set.md` | "8. record<br>values grouped under named fields" |
| S3 | 2026-07-24 | `git show 866ee4d:Designing/intention_tables_gen.py:73` (T1["C"]["Rust"]) | "Option&lt;T&gt; pure sum type; no null exists at all — strongest form" |
| S4 | 2026-07-24 | `git show 866ee4d:Designing/intention_tables_gen.py:72` (T1["C"]["Swift"]) | "Optional IS an enum — sum type with ? ! sugar" |
| S5 | 2026-07-24 | `git show 866ee4d:Designing/intention_tables_gen.py:198` (T2 C/D) | `("coexist", "designed together: option is a sum type, match consumes it")` |
| S6 | 2026-07-24 | `git show 866ee4d:Designing/intention_tables_gen.py:231` (DIAG["C"]) | "internal merge: sum type is the canonical; null is the legacy spelling" |
| S7 | 2026-07-24 | `git show 866ee4d:Designing/intention_row_satisfiers.md:17` | "\| C optionals \| **Rust** \| `Option<T>` with no null in the language; every other cell is it weakened (sugar removed, enforcement removed, or null retained alongside) \|" |
| S8 | 2026-07-24 | `git show 866ee4d:Designing/intention_row_satisfiers.md:40` | "`Option` = tagged record + choice; `match` = if-chains + field access" |
| S9 | 2026-08-05 | `~/Programming/PseudoCoup_v5/DevComms/log_008_kinds_coarse_tagging_draft.md:337` | "Sum types are not in the minimum set. the owner to rule whether `record` stretches to cover them or an object is missing." |
| S10 | 2026-08-05 | `log_011_uncertain_families_evidence.md`, §G1 | "`minimum_set` has `record` ("values grouped under named fields") and no sum." |

S3–S8 all survive verbatim into the present artifact
(`~/Programming/PseudoIR/Tools/intentions/pc_intentions.json`:
`t1_realizations.C.Rust`, `t1_realizations.C.Swift`,
`t2_compatibility` C/D, `t2_diagonal.C`, `row_satisfiers.C`).

### 1.2 did it ever vanish?

No. Nothing was removed. The phrase "sum type" is in the CURRENT
artifact three times over and always has been — but never as a row of
`minimum_set`, `intent_categories`, `primitives`, or `basis_audit`.

The nearest thing to a ruling is S1, and it is worth reading closely.
`minimum_intention_set.md` states its own governing rule at lines 12–15:

> "Rule for this document: entries earn their<br>place by being
> underivable from the others.<br>Anything derivable is listed as
> derived, or<br>left out."

S1 sits in the audit section, whose preamble (lines 131–134) says:

> "Each entry: the feature people choose the<br>language for, and its
> composite. A feature<br>survives the audit if its derivation is a
> known compiler technique, not hand-waving."

So the audit put optionals — the intent whose satisfier the research
elsewhere calls a "pure sum type" (S3) and a "tagged record + choice"
(S8) — through the derivability test and passed it as DERIVED: record +
choice. Under the document's own rule, a derived thing does not earn a
place. The mechanism was examined and ruled out of the set; the WORDS
"sum type" simply never appear anywhere in `minimum_intention_set.md`.
The audit verdict at lines 214–218 records the outcome of the whole
pass:

> "No 12th object found. One amendment<br>(function IS a value, item 7).
> One<br>non-object identified (static proof<br>grammars). The 11 stand,
> pending the<br>services-grain question."

### 1.3 where I looked and did not find it

No occurrence of "sum type", "tagged union", "variant", "Either" as a
CANDIDATE OBJECT or CANDIDATE CATEGORY anywhere in: the four PCv5
`Designing/` commits; `PCv7_policy_decisions.md`; `BEJ_expansion.md`;
`two_layer_program.md`; `language_divergence_study_log.md`;
`dev_plan_log.md`; the R1 REPORT; `~/Programming/0_Archive/` (all of
PseudoCoup_v1–v4 and both PseudoIR trees). `enum` appears in the
archive only as English, never as a proposed tier member.

### 1.4 verdict

**MY READING: "was discussed but never a row" — confidence high.** The
mechanism was examined by name in the audit (S1) and passed as derived
under the document's stated derivability rule; the term "sum type" was
in the tables from the beginning and is still there. There is no
version of any artifact in which a sum object was a row of any tier and
was later removed. the owner's memory ("i dont recall sum types at all") is
consistent with the evidence in the specific sense that matters: it was
never a candidate object, only a description of what optionals are made
of. the owner rules on whether "derived, therefore excluded" answers G1.

---

## 2 — error flow (error propagation)

### 2.1 every appearance found, chronological

| # | date | ref | quote |
| --- | --- | --- | --- |
| E1 | 2026-07-17 (file mtime 17:31) | `~/Programming/0_Archive/PseudoIR_(retired)/v4/.planning/GeminiDiscussions/low_level_dependencies.md:53` | "Now that the core pipeline strategy is clear, how do you want to handle exception and error propagation primitives? For example, if a Python dependency throws a runtime dynamic exception, should it be translated first into a Go-style dual return values primitive, or a Rust-style Result<T, E> enum lookup?" |
| E2 | same file, line 76 (the reply, reporting the owner's answer back to him) | same path | "I was over-complicating things by treating exceptions as a special "magic" compiler feature. You corrected that by applying your core principle consistently: an exception system is just code." |
| E3 | same file, lines 92–99 | same path | "By treating exceptions, memory allocation, and type built-ins not as "magic built-ins" but as standard graph dependencies to be translated in order, your custom IR stays incredibly lean." |
| E4 | 2026-07-22 | `~/Programming/PseudoCoup_v5/DevComms/language_divergence_study_log.md:182` | "Are there classes not yet listed? Candidates to investigate: exception semantics (what is catchable), recursion limits, integer hashing, default float formatting in print." |
| E5 | 2026-07-24 | `git show 866ee4d:Designing/minimum_intention_set.md`, §"Derived (not in the set)", lines 97–99 | "exception<br>choice + early return through<br>call layers" |
| E6 | 2026-07-24 | same file, lines 174–176 | "defer (Go), RAII (C++), using (C#)<br>= sequence + choice, same<br>derivation as exception." |
| E7 | 2026-07-24 | `git show 866ee4d:Designing/PCv7_policy_decisions.md`, policy 15 | "Objects outside the Ledger<br>(borrowed native packages): defined Fail — dev-time error where<br>provable, declared error at run-time otherwise. Never a raw<br>key error." |
| E8 | 2026-07-24 | `git show 866ee4d:Designing/PCv7_policy_decisions.md`, policy 19 | "Border grammar: three-way verdict … identical (free) / convertible (visible coercion, run-time cost) / incompatible (Fail loudly)." |
| E9 | 2026-07-24 | `git show 866ee4d:Designing/intention_tables_gen.py:347` (O7 verdict) | "PC: checked with error; opt-in Option-returning .get; from-end by explicit marker (C# ^), not bare negative" |
| E10 | 2026-08-05 | `log_008_kinds_coarse_tagging_draft.md:385–387` | "**Error propagation** (`try_expression`, `try_block`) — provisionally C, but C is "null safety, absence in types" and `?` over `Result` is error flow, which is a related but distinct thing." |
| E11 | 2026-08-05 | `log_011_uncertain_families_evidence.md`, §G2 | "No row in `intent_categories` mentions error, exception, failure or Result, and no cell of `t1_realizations.C` uses the word "error" — C is consistently about absence." |

E7, E8 and E9 survive into the present artifact (`policy_refs` /
`operators.O7.pc_verdict`) — so "error" is in `pc_intentions.json`
today, but only as a verdict about what indexing does and what a border
failure looks like, never as an intention.

### 2.2 last version containing it, first without

This is the one where the owner's memory is straightforwardly correct: error
flow WAS an entry in the minimum-set document, and it is not in the
artifact built from it.

| | |
| --- | --- |
| last version containing it | `git show 7efb6e6:Designing/minimum_intention_set.md` (2026-07-27 13:04 -0400), §"Derived (not in the set)", lines 97–99: "exception / choice + early return through / call layers" — byte-identical to 866ee4d |
| first version without it | `git show 9abc927:Tools/intentions/intentions_data.py` in `~/Programming/PseudoIR` (2026-07-31 11:44 -0400), `MINIMUM_SET`, 11 dicts, no `exception` entry; and its build product `~/Programming/PseudoIR/Tools/intentions/pc_intentions.json` `minimum_set` |
| recorded reasoning for the exclusion FROM THE SET | E5's own placement: it is under the heading "Derived (not in the set)", governed by lines 12–15 "Anything derivable is listed as derived, or left out". The derivation given is "choice + early return through call layers" |
| recorded reasoning for the exclusion FROM THE COPY-FORWARD | `intentions_data.py:588–591`: "lifted by reading minimum_intention_set.md ("The set" section, post-audit form)". The scope of the lift is stated; the reason for that scope is not |

Two further points on what the copy-forward was authorized to be. The
R1 report (`~/Programming/PseudoCoup_v6/Research/r1_intentions_validation/REPORT.md`,
2026-07-28) names what needed lifting:

> "3. **Minimum intention set membership** — the 11 objects
> (`minimum_intention_set.md`); not represented in the JSON."

R1 asked for MEMBERSHIP of the 11. It did not ask for the derived list,
and it did not say the derived list was out of scope — it did not
mention it. R1's own scope statement is:

> "Overall: **no context-corruption artifacts found.** … What it lacks
> for the slicer was never claimed to be there — it is missing
> structure, not corrupted content."

So the derived list was never in `pc_verdicts.json` either (R1's Check 2
enumerates its fields; no derived-list field exists). The loss is not a
deletion — it is a document section that was never converted to data,
in either generation.

E4 is a separate thread and a separate near-miss: exception semantics
was nominated as a candidate NINTH DIVERGENCE CLASS on 2026-07-22 and, so
far as this search found, never investigated. `border_lattice` in the
present artifact has 11 entries spanning classes 1–8 plus J3 — no class
9. The divergence log's own note on this
(`language_divergence_study_log.md:310`) says the crossing table "converts
"are there classes 9+?" from speculation into a checklist"; that
checklist was not found anywhere.

### 2.3 verdict

**MY READING: "was present" — confidence high, with one qualification.**
Error flow was present under the name `exception`, in
`minimum_intention_set.md`'s "Derived (not in the set)" block, from the
document's first appearance in git (2026-07-24) to its last
(2026-07-27), and it vanished at the 2026-07-28 copy-forward that lifted
only "The set". The qualification: it was present AS AN EXPLICIT
NON-MEMBER with a stated derivation, not as a row of the set. the owner's "i
think error flow was included at one point" matches a real entry in a
real list. the owner rules on whether "included in the derived list" is what
his memory was reaching for, and on whether the derived list should have
travelled with the 11.

---

## 3 — aliasing (borrowing)

### 3.1 every appearance found, chronological

| # | date | ref | quote |
| --- | --- | --- | --- |
| A1 | 2026-07-14 (the owner decision quoted in a later file) | `~/Programming/0_Archive/PseudoIR_(retired)/pseudoir/registry/data/ops.json:688` and `~/Programming/0_Archive/PseudoIR_(retired)/v2/registry/ops.json:688` | "…NEVER an in-place mutation of `a`. This keeps user types value-like and avoids aliasing surprises. The ban stands; the rebind rule is the pre-decided answer for the day it is lifted, so no future re-litigation." |
| A2 | 2026-07-22 | `~/Programming/PseudoCoup_v5/DevComms/language_divergence_study_log.md:287` | "\| 2 copy-model \| Discipline rule: one aliasing convention (Python's) + explicit `.copy()` at borders \|" |
| A3 | 2026-07-22 | same file, line 340 | "Class 2 border — value-copy struct entering a reference-model frame: convertible via copy, or incompatible if aliasing is load-bearing." |
| A4 | 2026-07-24 | `git show 866ee4d:Designing/minimum_intention_set.md`, §"Non-object finding", lines 198–210 | "ownership / borrowing (Rust)<br>NOT an object at any level.<br>a dev-time grammar restricting<br>aliasing and lifetime (classes<br>2 and 4 of the divergence study).<br>the run-time behavior it permits<br>is fully expressible in the set;<br>what Rust adds is a PROOF about<br>that behavior, checked before<br>running. lives beside the border<br>grammar of PCv7, not in this set." |
| A5 | 2026-07-24 | same file, "Audit verdict", lines 214–218 | "One<br>non-object identified (static proof<br>grammars)." |
| A6 | 2026-07-24 | `git show 866ee4d:Designing/intention_tables_gen.py:285` (P9 verdict) | "PC.list = single-owner Vec semantics (no aliasing surprises); go.slice / php.array as borrows" |
| A7 | 2026-07-24 | `git show 866ee4d:Designing/BEJ_expansion.md:95` | "sender keeps no live alias to `x`. A Ledger judgment. Free." |
| A8 | 2026-07-24 | `git show 866ee4d:Designing/PCv7_policy_decisions.md`, policy 17 | "Qualified (`j.//`, `go.interface`) = explicit,<br>greppable borrow. Abolishes implicit uniqueness at the surface." |
| A9 | 2026-07-24 | `git show 866ee4d:Designing/two_layer_program.md:125` | "layers uniformly: basis borrows and derived borrows use the same" |
| A10 | 2026-07-24 (via `build_verdicts.py`, added 9eec26c) | present in `pc_intentions.json` `border_lattice` class 2 | `"crossing": "aliasing is load-bearing across the border"`, `"spelling": null`, `"verdict": "incompatible"` |
| A11 | 2026-08-05 | `log_008_kinds_coarse_tagging_draft.md:379–384` | "**Borrowing** … — no object covers aliasing. The artifact's `border_lattice` has a copy-model class that turns on exactly this, so the concept is present in the research but not in the 21 buckets." |
| A12 | 2026-08-05 | `log_011_uncertain_families_evidence.md`, §G3 | "`border_lattice` has two entries with `verdict` = "incompatible" and both are aliasing" |

A6, A7 (via `row_satisfiers.B.in_hub`), A8 (via `policy_refs`) and A10
all survive into the present artifact.

### 3.2 last version containing it, first without

| | |
| --- | --- |
| last version containing the "Non-object finding" | `git show 7efb6e6:Designing/minimum_intention_set.md` (2026-07-27 13:04 -0400), lines 196–210 — byte-identical to 866ee4d |
| first version without it | `git show 9abc927:Tools/intentions/intentions_data.py` (2026-07-31 11:44 -0400); the `MINIMUM_SET` block carries the 11 objects and no non-object finding |
| recorded reasoning | A4 itself, which is the most explicit exclusion ruling found anywhere in this research: "NOT an object at any level … lives beside the border grammar of PCv7, not in this set." A5 records it as a formal audit outcome |

Unlike error flow, aliasing did not vanish entirely — it was RELOCATED
by the ruling in A4 to the border grammar, and the border grammar DID
travel: `border_lattice` class 2 (A10) is in `pc_intentions.json` today
and carries the only unspellable incompatibility in the whole lattice.
What was lost at the 2026-07-28 lift is the RULING, not the concept: the
artifact no longer records that aliasing was considered for the tiers
and positively excluded. That is exactly the ambiguity G3 is written
around. log_011 §G3 already guessed the answer without having seen A4:

> "I lean toward the first reading being the intended one (a border
> property is a different kind of thing from an intention), which is why
> family 3's recommendation is medium rather than high."

A4 is the document saying that in the owner's own words, three months of
project-time earlier.

### 3.3 verdict

**MY READING: "was present" — confidence high.** Ownership/borrowing had
its own named section, "Non-object finding", in
`minimum_intention_set.md` from 2026-07-24 to 2026-07-27, with an
explicit exclusion ruling and an explicit relocation to the border
grammar; it was carried into the audit verdict as "One non-object
identified". It left the data at the 2026-07-28 lift of "The set" alone.
the owner's "i vaguely remember something about aliasing" matches a whole
section. the owner rules on whether the relocation ruling should be readable
from the artifact.

---

## 4 — summary table

| gap | ever a row/object? | strongest historical text | last version containing | first version without | my verdict | confidence |
| --- | --- | --- | --- | --- | --- | --- |
| sum types | no | "optionals, null safety … = record with a tag field + choice on the tag" (S1) | n/a — never removed; still in `t1_realizations`/`t2_*` today | n/a | was discussed but never a row | high |
| error flow | no, but an explicit derived entry | "exception / choice + early return through / call layers" (E5) | `git show 7efb6e6:Designing/minimum_intention_set.md` (2026-07-27) | `git show 9abc927:Tools/intentions/intentions_data.py` in PseudoIR (2026-07-31) | was present | high |
| aliasing | no, but an explicit non-object ruling | "ownership / borrowing (Rust) NOT an object at any level … lives beside the border grammar of PCv7, not in this set." (A4) | `git show 7efb6e6:Designing/minimum_intention_set.md` (2026-07-27) | `git show 9abc927:Tools/intentions/intentions_data.py` in PseudoIR (2026-07-31) | was present | high |

One shape runs through all three: `minimum_intention_set.md` is not a
list of 11 things, it is an ARGUMENT that ends in 11 things, and the
copy-forward took the conclusion and left the argument. All three of
log_011's gap-questions are questions the argument already answers —
two of them explicitly (E5, A4), one of them implicitly (S1). None of
the three answers is readable from `pc_intentions.json`.

Two absences-of-evidence, stated plainly:

- **No reasoning was recorded for the SCOPE of the 2026-07-28 lift.**
  `intentions_data.py:588–591` states that only "The set" was taken; no
  file found says why the derived list and the non-object finding were
  not also taken. Searched: the PseudoIR `Tools/intentions` README and
  all three of its commits, the R1 REPORT and PLAN, PCv5 `open_issues.md`,
  `project_state.md`, `dev_plan_log.md`, and every PCv5 commit message.
- **No class-9 investigation of "exception semantics" was found**
  anywhere (E4's candidate). `border_lattice` stops at class 8 plus J3,
  and R1 Check 3 confirms "11 entries cover classes 1–8 plus J3".

---

## open questions for the owner

1. **Does E5 answer G2?** "exception / choice + early return through
   call layers" is an explicit derivation under a rule that excludes
   derivables. If that is the answer, G2 closes and log_011's family-4
   recommendation (a distinct `error-flow` bucket) has to be re-argued
   against a ruling rather than against silence — or withdrawn.
2. **Does A4 answer G3?** It is the exact reading log_011 leaned toward
   and could not source. If it is authoritative, family 3's confidence
   goes from medium to high in the direction of "border property, not
   intention" — which is an argument AGAINST log_011's proposed `borrow`
   bucket at the intention tier, not for it.
3. **Does S1 answer G1?** "record with a tag field + choice on the tag"
   is a derivation of sums, offered under the same rule. If yes, G1
   closes the same way; but sums differ from the other two in that the
   research elsewhere makes a sum the SATISFIER of row C
   (`row_satisfiers.C.basis`), which is a load-bearing role that
   `exception` and `borrowing` never had. This is the one of the three
   where I would not assume the parallel holds.
4. **Should the derived list and the non-object finding become data?**
   They exist only as prose in a deleted folder, recoverable solely from
   PCv5 git. They are, on the evidence above, the answers to three of the
   four questions log_011 asked. A `derived` and a `non_objects` field
   alongside `minimum_set` would make the artifact answer them without a
   git archaeology pass. That is a suggestion about shape, not a claim
   that the artifact is wrong.
5. **Was the scope of the 2026-07-28 lift a decision or a default?** No
   record was found either way. If it was a decision, the reasoning is
   worth capturing before it is lost the way these three were.
6. **Class 9 — exception semantics.** Nominated 2026-07-22 (E4), never
   investigated as far as this search reaches. It is the only candidate
   class from that list that bears on G2. Worth a ruling on whether it is
   dead or merely unstarted.
7. **Is E1/E2 (2026-07-17, PseudoIR-retired) in scope as project
   history at all?** It predates PCv5 and belongs to a retired IR line,
   but "an exception system is just code" is the earliest statement of
   the position E5 later encodes. I include it as evidence of continuity;
   the owner may regard the retired line as not binding on this one.

---

## sources

- `~/Programming/PseudoIR/Tools/intentions/pc_intentions.json` —
  `minimum_set`, `intent_categories`, `border_lattice`, `t1_realizations`,
  `t2_compatibility`, `t2_diagonal`, `row_satisfiers`, `primitives`,
  `operators`, `basis_audit`, `policy_refs`, `meta`. Read 2026-08-06.
- `~/Programming/PseudoIR/Tools/intentions/intentions_data.py` (provenance
  header lines 1–22; `MINIMUM_SET` comment lines 588–591) and
  `README.md`.
- `git -C ~/Programming/PseudoIR log --oneline -- Tools/intentions` →
  9abc927 (2026-07-31), 2682a16 (2026-08-01), 049a8e3 (2026-08-05); all
  three inspected.
- `git -C ~/Programming/PseudoCoup_v5 log --oneline --all -- Designing/`
  → 866ee4d (2026-07-24 15:57), 9eec26c (2026-07-24 21:15), 7efb6e6
  (2026-07-27 13:04), 21cef81 (2026-08-01 07:51, the deletion). All nine
  files at each of the first three commits were extracted and searched.
- `~/Programming/PseudoCoup_v5/DevComms/` —
  `language_divergence_study_log.md`, `dev_plan_log.md`,
  `open_issues.md`, `project_state.md`,
  `log_008_kinds_coarse_tagging_draft.md`,
  `log_011_uncertain_families_evidence.md`.
- `~/Programming/PseudoCoup_v6/Research/r1_intentions_validation/REPORT.md`
  (2026-07-28).
- `~/Programming/0_Archive/` — PseudoCoup_v1 through v4, PseudoIR,
  PseudoIR_(retired), WFL_PseudoCoup_Briefing. Hits: the two `ops.json`
  copies (A1) and
  `PseudoIR_(retired)/v4/.planning/GeminiDiscussions/low_level_dependencies.md`
  (E1–E3). One false positive discarded:
  `PseudoIR_(retired)/v4/.planning/GeminiDiscussions/design.md:23`
  "minimum set of token chains which activates every node in compiler
  checks" — a test-coverage sense of "minimum set", unrelated to the
  intention set.
