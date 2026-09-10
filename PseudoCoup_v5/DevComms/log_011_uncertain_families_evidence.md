# log 011 — the five uncertain families: evidence and recommendations

2026-08-05. EVIDENCE FOR DEE'S REVIEW.

**What this is.** For each of the five clusters named at the end of
`PRIVATE/PseudoCoup_v5/DevComms/log_008_kinds_coarse_tagging_draft.md`
(§"every UNCERTAIN row, gathered", items 1-5), one section that: quotes
what the validated intentions artifact at
`PRIVATE/PseudoIR/Tools/intentions/pc_intentions.json` actually
says on the point, cited by field path; lays out the candidate placements
with the strongest argument for each and how two or three of the other
eleven languages in `languages` would classify their equivalent
construct; states the cost asymmetry if the placement is wrong; and ends
with one labelled RECOMMENDATION carrying an explicit confidence and what
would raise it. It serves
`PRIVATE/PseudoCoup_v5/DevComms/log_006_ur_kinds_vocabulary.md`
items 3 (what `ur_kind` classifies) and 5 (the mechanical seed at
language one).

**What this is NOT.** Not a decision, and not an amendment to anything.
Nothing here is applied. The intentions artifact is the owner's own validated
research (`meta.copied_forward_from`: "pc_verdicts.json (R1-verified)")
and is treated throughout as the AUTHORITY on what the buckets mean — my
job is to read what it already implies, not to correct it. Where a
family looks like it exposes a gap in `minimum_set` or
`intent_categories` themselves, that is written as a QUESTION to the owner in
the last-but-one section, never as a correction. Every recommendation is
labelled a recommendation and carries a confidence.

**Provenance marking.** Claims sourced from the artifact are cited by
field path (e.g. `t1_realizations.C.Swift`). Claims about how another
language's grammar spells something, where the artifact does not say, are
marked **[my language knowledge, not in the data]**. The distinction
matters because item 4 of log_006 forbids merges judged on name
resemblance, and my own knowledge is exactly the kind of evidence that
has to be flagged so the owner can discount it.

---

## family 1 — imports and namespacing

Rows: `use_declaration`, `use_list`, `use_wildcard`, `scoped_use_list`,
`extern_crate_declaration`, `mod_item`, and adjacently `crate`, `super`,
`scoped_identifier`, `use_as_clause`.

### 1.1 what the intentions data says

The honest finding is that it says almost nothing, and the silence is
itself the evidence.

| field path | content | bearing |
| --- | --- | --- |
| `minimum_set[1]` | `object` = "name", `desc` = "a binding from a written identifier to a value" | The nearest object. Its wording binds to a VALUE; a `use` binds to an item, which may be a type, a module or a trait. |
| `intent_categories` (all 10) | A suspension, B channels, C optionals, D pattern matching, E dispatch, F generics, G scoped cleanup, H events, I operator overloading, J metaprogramming | No category mentions scope, module, namespace, visibility or import. |
| `basis_audit` (9 keys) | bool, bytes, executor, float64, function_value, hashing, int64, list, record | The audit that produced the minimum-set amendment inspects nine substrate objects. A module/namespace is not among them. |
| `primitives` (12 rows, P1-P12) | bool through record | Same: no namespacing primitive. |
| `border_lattice` (11 classes) | value-model, copy-model, evaluation-order, lifetime, dispatch, collection-order, concurrency, encoding, dynamic-mode | No class turns on name resolution or scope. |

So: namespacing is absent from all four of the artifact's inventories.
It is not a case of the artifact ruling one way; it is a case of the
artifact never having the question put to it. That is a materially
different situation from family 2 or 3 below, where the artifact does
speak.

One near-miss worth putting in front of the owner: `t1_realizations.J.Go` =
"reflect package (clunky run-time); go:generate dev-time", and
`t1_realizations.J["C++"]` = "templates: accidentally Turing-complete
dev-time metaprogramming; constexpr; no reflection". C++'s `#include` is
textual splicing performed before compilation **[my language knowledge,
not in the data]** — which is dev-time code transformation, i.e. J's
territory as `intent_categories[9].desc` defines it ("reflection, macros,
codegen"). The C++ analogue of a Rust `use` therefore lands in a
different bucket from the Rust one under any reading. This is the
sharpest cross-language fact in the family.

### 1.2 candidate placements, argued against each other

**Candidate A — `name` (minimum_set object 2), as log_008 provisionally
assigns.**

Argument for: a `use` really does introduce a written identifier that
subsequent code refers to. `use std::collections::HashMap;` makes the
token `HashMap` resolvable where it was not. The binding is real, is
lexical, and is the thing every consumer of the tag will want to follow.
It is also the cheapest tag: `scoped_identifier` is already `name`
unflagged in log_008, so the whole path machinery stays in one bucket and
the ledger's name resolution has one place to look.

Argument against, made concrete: contrast the two instances.

- Instance of a genuine object-2 binding: `let x = compute();` — a
  written identifier bound to a value that exists at run time.
- Instance of the disputed one: `use std::io::Write;` — the identifier
  `Write` is bound to a trait. There is no value. At run time nothing
  named `Write` exists; the binding is consumed entirely by name
  resolution and then erased.

`minimum_set[1].desc` says "to a value". The second instance has no
value in it. Tagging both `name` asserts they are the same object, and
they differ in whether anything survives to run time.

**Candidate B — the PROPOSED `declarative-form` bucket from log_008
§"the PROPOSED new buckets"/2.**

Argument for: a `use` executes nothing, exactly like
`visibility_modifier`, which log_008 already places there. Both govern
what may reach a name without themselves doing anything. And log_008's
own defence of that bucket — "a positive tag saying 'classified, and the
classification is: carries no intention' keeps the census honest" —
applies verbatim.

Argument against: `declarative-form` was proposed as a bucket for
trivia and modifiers, and an import is not trivia. Deleting every comment
from a file changes nothing; deleting every `use` breaks compilation.
Sweeping imports in there makes the bucket mean "leftovers", which is the
failure mode log_008 was trying to avoid when it argued against NONE.

**Candidate C — a genuinely new coarse bucket, provisionally
`namespace-form`.**

Argument for: it is the only placement that survives the cross-language
test, and the cross-language test is the one log_006 item 4 says decides
merges. Working the other languages:

| language | its equivalent construct | what it would be tagged under candidate A | source |
| --- | --- | --- | --- |
| Go | `import_declaration` / `import_spec`, plus the mandatory `package_clause`; an import binds a package identifier that is then used as a qualifier, and Go's exportedness is carried by identifier CASE, not by any node | `name` would be forced onto `package_clause`, which binds nothing at all — it declares which namespace the file's own declarations join | **[my language knowledge, not in the data]**; the artifact's Go cells (`t1_realizations.E.Go` "structural interfaces, implicit satisfaction") do not address imports |
| TypeScript | `import_statement`, and separately `import type { T }` which is erased entirely | `name` would merge a value import with a type-only import that `t1_realizations.F.TypeScript` describes the general case of as "fully erased; types vanish at run-time" | construct **[my language knowledge]**; the erasure fact is `t1_realizations.F.TypeScript` |
| C++ | `preproc_include`, textual splicing at dev time; also `using_declaration` and `namespace_definition`, which are genuinely different mechanisms in one language | `name` would merge a preprocessor operation with a scope alias. Under `intent_categories[9].desc` ("reflection, macros, codegen"), `#include` has a real claim on J | construct **[my language knowledge]**; the J desc is `intent_categories[9]` |

A single bucket that has to hold Go's `package_clause`, TypeScript's
erased type import and C++'s `#include` is doing no work unless it is
about namespacing specifically. `name` cannot hold all three without
becoming a synonym for "identifier appears here".

Argument against candidate C: log_008 already proposes two new buckets
and admits (§"the PROPOSED new buckets"/1, "Against it") that a bucket
meaning different things per language "is weaker than the other 21".
A third new bucket compounds that. And the artifact's silence is not
positive evidence that a bucket is owed — it may simply be out of scope,
since the artifact is a theory of what a program DOES and namespacing is
about where a program can be SEEN from.

### 1.3 cost asymmetry if wrong

| wrong choice | what breaks | repairable? |
| --- | --- | --- |
| Too coarse — one `namespace-form` covering all six kinds, later found to need splitting | A later refinement adds sub-buckets; existing tags stay valid as super-tags. The `kinds` vocabulary is append-only "in spirit" (log_006 item 1 context), so this is an addition | Yes, append-only |
| Wrong merge — `use_declaration` tagged `name`, then Go's `package_clause` and C++'s `preproc_include` tagged `name` at language two/three on the strength of the Rust precedent | Three unrelated mechanisms become indistinguishable in the neutral layer. Any consumer asking "what binds this identifier" gets a set it cannot re-split, because the distinguishing information was never recorded at the neutral layer — it survives only in the substrate, and only if the substrate is consulted, which defeats the point of the tag | No. Unmerging requires re-deciding every already-tagged corpus |
| NONE | log_008's stated objection applies: the totality check "cannot distinguish 'deliberately unbucketed' from 'not yet done'" | Partially — but only by re-running the classification |

The asymmetry is stark and runs one way: coarse is cheap, merged is
expensive. This is the general shape in all five families and I will not
re-derive it each time, only note where it differs.

### 1.4 RECOMMENDATION

**RECOMMENDATION (family 1):** do NOT tag the import/namespace family
`name`. Tag it with a distinct coarse bucket — provisionally
`namespace-form` — kept separate from both `name` and the proposed
`declarative-form`. `scoped_identifier` and `crate`/`super` should stay
`name`, because a path in expression position genuinely does resolve to a
value; the split falls between paths-that-refer and declarations-that-
bind-into-scope.

**Confidence: medium.** The negative case (it is not `name`) is stronger
than the positive case (it is `namespace-form`). I am confident the merge
is wrong; less confident that one new bucket is the right shape rather
than two, or rather than deferring the whole family to the ledger's name
resolution as log_008 open question 5 contemplates for B/G/I.

**What would raise it:** (a) the owner stating whether the artifact's silence
on namespacing is scope or gap — that single ruling settles the family;
(b) ingest of c/cpp, where `preproc_include` versus `using_declaration`
versus `namespace_definition` in ONE language would show immediately
whether a single bucket can hold them; (c) a count of how many distinct
name-resolution consumers actually want these nodes, since if the answer
is "only the ledger" the bucket may be moot.

---

## family 2 — sum types and enums

Rows: `enum_item`, `enum_variant`, `enum_variant_list`, and adjacently
the whole D pattern-matching set that consumes them.

### 2.1 what the intentions data says

Here, unlike family 1, the artifact speaks — repeatedly, and about sum
types by name, while having no object for them.

| field path | content |
| --- | --- |
| `minimum_set[7]` | `object` = "record", `desc` = "values grouped under named fields" |
| `t1_realizations.C.Rust` | "Option&lt;T&gt; pure sum type; no null exists at all — strongest form" |
| `t1_realizations.C.Swift` | "Optional IS an enum — sum type with ? ! sugar" |
| `row_satisfiers.C.basis` | "Option&lt;T&gt; with no null in the language; every other cell is it weakened (sugar removed, enforcement removed, or null retained alongside)" |
| `t2_compatibility` C/D row | `note` = "designed together: option is a sum type, match consumes it", `verdict` = "coexist" |
| `t1_realizations.D.Rust` | "match is central: exhaustive, deep destructuring — reference realization" |
| `t2_compatibility` D/E row | `note` = "exhaustiveness needs closed sets, interfaces are open; sealed hierarchies resolve", `verdict` = "tension" |
| `row_satisfiers.D.basis` | "exhaustive + deep destructuring subsumes the row" |
| `row_satisfiers.C.satisfier` / `.native` | "Rust" / `["Rust"]`, `status` = "preliminarily solved" |

The phrase "sum type" appears three times in the artifact (C/Rust cell,
C/Swift cell, C/D compatibility note) and the concept is load-bearing in
two of the ten categories — C is *satisfied* by a sum type, and D's
exhaustiveness *requires* the closed set that a sum type is. The
`minimum_set` has "record" for products and nothing for sums.

### 2.2 candidate placements, argued against each other

**Candidate A — `record` (object 8), as log_008 assigns with an
UNCERTAIN flag.**

Argument for: structurally an `enum_variant` with fields is "values
grouped under named fields" — `minimum_set[7].desc` verbatim. And a
`struct_item` and an `enum_item` share almost all their grammar: both
have a name, optional `type_parameters`, and a braced body of field
groups. The tag is cheap and the totality check passes.

**Candidate B — D pattern matching (`intent_categories[3]`, "structural
choice").**

Argument for: `t2_compatibility` C/D says option "is a sum type, match
consumes it", and `row_satisfiers.D.basis` makes exhaustiveness the row's
defining virtue. An enum declaration is precisely the closed set that
makes exhaustiveness computable. On this reading `enum_item` is not data
grouping at all — it is the declaration half of category D.

Argument against B: D is elsewhere assigned to consumption sites
(`match_arm`, `struct_pattern`, `or_pattern`). Putting the declaration in
the same bucket as its consumers makes D mean "anything to do with
matching", which is a topic, not an object.

**Candidate C — a new minimum-set-tier object, provisionally `sum`,
co-ordinate with `record`.**

The contrast, shown with one instance of each side:

- Instance that `record` describes: `struct Point { x: f64, y: f64 }` —
  a value of this type has an `x` AND a `y`. Both fields exist at once.
- Instance in dispute: `enum Shape { Circle(f64), Rect(f64, f64) }` — a
  value of this type has a `Circle` payload OR a `Rect` payload. Never
  both. The count of inhabitants is a sum, not a product, and every
  consumer must branch.

Tagging both `record` asserts they are the same object. They differ in
the one property — and-versus-or — that decides whether a consumer needs
a branch. That is not a fine distinction inside one object; it is the
distinction between two.

Cross-language check, which is where this family gets decisive:

| language | its "enum" | its actual sum type | consequence for candidate A |
| --- | --- | --- | --- |
| Swift | `enum_declaration`, with associated values | the same node — Swift's enum IS a sum type | Agrees with Rust. Supported by `t1_realizations.C.Swift` ("Optional IS an enum — sum type") |
| Java | `enum_declaration` — a fixed set of singleton INSTANCES of one class; every constant has the same field shape | `sealed` interfaces plus records, per `t1_realizations.D.Java` "switch patterns + record deconstruction; sealed exhaustive" | Catastrophic for A. A Java `enum_declaration` really is closer to a record-with-constants; the Rust `enum_item` analogue is a `sealed` hierarchy, an entirely different node. Tagging both `record` on the strength of the shared word "enum" is exactly the name-resemblance merge log_006 item 4 forbids |
| TypeScript | `enum_declaration` (a numeric/string constant bag) | `union_type` — `t1_realizations.D.TypeScript`: "— native; discriminated unions + narrowing carry the intent" | Also bad for A: the sum lives in TYPE position with no declaration node of its own. If `enum_item` is `record`, TS's `union_type` has nowhere to go but the proposed type-form bucket, and the same object lands in two buckets across two languages |

The Java and TypeScript rows are structural facts about those grammars
**[my language knowledge]**; the artifact cells cited alongside them
(`t1_realizations.D.Java`, `t1_realizations.D.TypeScript`) are the
artifact's own corroboration that sealed hierarchies and discriminated
unions are where those languages' D-intent lives.

### 2.3 cost asymmetry if wrong

The general shape of §1.3 holds, with one aggravation specific to this
family: the wrong merge here is *invited by name resemblance*. Three of
the twelve languages have a node literally called `enum_declaration` and
in two of them it means something else. A `record` tag on `enum_item`
does not merely risk a bad merge at language two — it pre-authorises one,
because the next person tagging Java sees `enum_declaration` already
precedented as `record` and agrees.

There is also a downstream consequence the other families do not have:
`row_satisfiers.C.status` is "preliminarily solved" with `satisfier` =
"Rust", and `policy_refs.policies["8"]` = "A/C/D/G canonicalize on Rust".
Rust is the canon language for C and D. If the neutral vocabulary cannot
express the sum type, the canon realization of two rows is the one thing
the vocabulary cannot say.

### 2.4 RECOMMENDATION

**RECOMMENDATION (family 2):** do NOT tag `enum_item` / `enum_variant` /
`enum_variant_list` as `record` alone. Tag them with a distinct bucket —
provisionally `sum`, at minimum-set tier rather than category tier, since
the artifact's own C and D rows depend on it — and keep the DUAL with D
pattern matching only on `enum_item` (the closed set that D consumes),
not on the variants.

**Confidence: high** on the negative claim (not `record`). **Medium** on
the positive claim (a `sum` bucket at minimum-set tier rather than a
category-tier or type-form placement).

**What would raise it:** (a) the owner's answer to gap-question G1 below — if
the minimum set can grow, this is settled; if it is fixed, the question
becomes which existing bucket absorbs the strain, and my answer would
change to D rather than `record`; (b) ingest of one language whose sum
type is spelled in type position (TypeScript) or as a class hierarchy
(Java), which would show whether one bucket can span the three spellings;
(c) a corpus count of how many Rust `enum_item` nodes are consumed
exhaustively versus used as constant bags, which would show how much of
Rust's own enum usage is actually the Java shape.

---

## family 3 — borrowing, references and lifetimes

Rows: `reference_expression`, `reference_type`, `lifetime`,
`lifetime_parameter`, `for_lifetimes`, `mut_pattern`, `ref_pattern`,
`mutable_specifier`, `pointer_type`.

### 3.1 what the intentions data says

This family is the opposite of family 1: the artifact has a great deal to
say, all of it outside the 21 buckets.

| field path | content |
| --- | --- |
| `border_lattice` class 2, first entry | `name` = "copy-model", `crossing` = "value-semantics object -> reference-model frame", `spelling` = ".copy() at the border", `verdict` = "convertible" |
| `border_lattice` class 2, second entry | `name` = "copy-model", `crossing` = "aliasing is load-bearing across the border", `spelling` = null, `verdict` = **"incompatible"** |
| `border_lattice` class 4 | `name` = "lifetime", `crossing` = "resource object -> frame with different cleanup regime", `spelling` = "explicit scope wrapper", `verdict` = "convertible" |
| `border_lattice` class 7, first entry | `name` = "concurrency", `crossing` = "mutable object across spawn boundary", `verdict` = **"incompatible"** |
| `canon.P9.statement` | "single-owner Vec semantics (Vec is Rust's realization, per the Rust cell); go.slice / php.array as borrows" |
| `canon.P12.statement` | "reference + explicit .copy(), legislated by policy 6; no single canon language; value structs as go.struct / swift.struct borrows" |
| `basis_audit.list.Rust` | "native:move" (contrast `basis_audit.list["C++"]` = "cheap:value-copy", `basis_audit.list.Swift` = "cheap:cow-value-copy", `basis_audit.list.Go` = "cheap:slice-alias-detach") |
| `basis_audit.record.Rust` | "native:move" |
| `row_satisfiers.B.in_hub` | "...+ Rust's transfer proof (send checked at dev-time, a Ledger judgment)" |
| `policy_refs.policies["3"]` | "Restriction egresses trivially; permission egresses hard." |

Two observations that I think are the most important evidence in this
whole log.

First: of the eleven `border_lattice` entries, exactly two carry
`verdict` = "incompatible", and both are about aliasing — class 2
"aliasing is load-bearing across the border" and class 7 "mutable object
across spawn boundary". Aliasing is the artifact's hardest wall. It is
the only thing in the lattice that cannot be spelled around (`spelling`
is null for both).

Second: aliasing appears nowhere in `minimum_set` or
`intent_categories`. The concept is in the research at full strength and
absent from the 21 buckets entirely. log_008 §"every UNCERTAIN row"/3
already notices this ("the artifact's `border_lattice` has a copy-model
class that turns on exactly this, so the concept is present in the
research but not in the 21 buckets"); the field paths above are what
backs the observation.

### 3.2 candidate placements, argued against each other

The family splits into a type-side and a value-side, and I argue they
should be split rather than tagged together.

**Type-side: `reference_type`, `pointer_type`, `lifetime`,
`lifetime_parameter`, `for_lifetimes`.**

Candidate A — the PROPOSED `type-form` bucket (log_008's assignment for
`reference_type`, `pointer_type`, `lifetime`). Argument for: these are
`_type` supertype sub-types by the grammar's own table; they spell what a
value is, construct nothing, and log_008's type-form argument ("type
syntax is what a program SAYS about what it does") covers them without
strain.

Candidate B — F generics (log_008's assignment for `lifetime_parameter`,
`for_lifetimes`). Argument for: `intent_categories[5].desc` is
"parameterization by type", and `for<'a>` is literally a binder in the
parameterization machinery.

I do not think these two are in real conflict — log_008 already resolves
them as DUAL where both are present, and that resolution reads correctly
here.

**Value-side: `reference_expression` (`&x`, `&mut x`).** This is the
contested one, and log_008 flags it as "the clearest candidate for a
missing intention".

- Instance of what `name` (object 2) describes: `let x = 5;` then
  `x` — an identifier standing for a value.
- Instance in dispute: `&mut v` — this does not name anything. It
  produces a new thing: a permission to reach `v` without owning it,
  carrying a lifetime the compiler checks. Passing it transfers a
  capability. `border_lattice` class 2's incompatible entry is about
  precisely this thing crossing a boundary.

Candidate A — `name`, as log_008 provisionally assigns. Argument for:
it is the nearest existing object and it keeps the census total. Argument
against: it makes the artifact's only hard wall invisible in the
vocabulary. If `&mut v` reads as `name`, nothing in the tag stream
distinguishes the one construct the lattice says cannot cross a border.

Candidate B — `mutation` (object 10, "assignment to a name or field
after creation"). Argument for: `&mut` grants the object-10 capability;
log_008 already dualises `mutable_specifier` this way. Argument against:
object 10's desc is about *performing* the write; `&mut` performs
nothing, it authorises. `policy_refs.policies["3"]` — "Restriction
egresses trivially; permission egresses hard" — is the artifact drawing
exactly the capability-versus-act distinction, and putting them in one
bucket erases it.

Candidate C — a new bucket, provisionally `borrow` (or `aliasing`).
Argument for: the artifact devotes two lattice classes and two of the
twelve `basis_audit` cells to it, and rules it incompatible at borders.
That is more artifact attention than several of the ten categories get.

Cross-language check:

| language | its equivalent | how it would classify | source |
| --- | --- | --- | --- |
| C++ | `reference_declarator` (`T&`), `pointer_declarator` (`T*`), rvalue reference `T&&`, and `std::move` as an ordinary call | Type-side maps cleanly to type-form. Value-side does NOT: C++'s move is a library function call, so the same intention that Rust spells in the grammar is invisible to the C++ grammar — the same situation log_008 records for B/G/I in Rust | constructs **[my language knowledge]**; corroborated by `basis_audit.list["C++"]` = "cheap:value-copy" and `basis_audit.record["C++"]` = "cheap:value-copy" |
| Swift | `inout` parameter modifier; otherwise copy-on-write value semantics with no borrow spelling at use sites | Swift's borrow analogue is a parameter modifier, i.e. a modifier token, which under log_008's scheme would fall to `declarative-form` — a third bucket for the same intention | construct **[my language knowledge]**; `basis_audit.list.Swift` = "cheap:cow-value-copy" is the artifact's own note that Swift's model differs |
| Go | `&x` unary and `*T` pointer types, no lifetime story; slices alias | Value-side looks superficially identical to Rust's `&x` and means something materially weaker — no aliasing proof | construct **[my language knowledge]**; `basis_audit.list.Go` = "cheap:slice-alias-detach" is the artifact naming the divergence |

Go is the trap here: `&x` in Go and `&x` in Rust are the same three
characters and different objects. `basis_audit.list.Go` versus
`basis_audit.list.Rust` ("cheap:slice-alias-detach" versus "native:move")
is the artifact stating that divergence in its own words.

**Lifetimes specifically.** `lifetime` has no analogue in any of the
other eleven — C++ has none, Swift has none, Go has none **[my language
knowledge, and log_008 §"every UNCERTAIN row" makes the same claim]**.
Under log_006 item 4 that makes it a partial correspondence that stays
language-specific and unmerged, which is *safe by construction*. So the
lifetime sub-question is much less risky than the `&x` sub-question.

### 3.3 cost asymmetry if wrong

| wrong choice | what breaks |
| --- | --- |
| `reference_expression` -> `name`, then Go's `&x` -> `name` at a later ingest | The neutral layer says the two are the same object; the artifact says one of them makes a border crossing "incompatible" (`border_lattice` class 2). A consumer computing border verdicts from `ur_kind` would be wrong in the one place the lattice says wrongness is unrecoverable. Not repairable by refinement, because the tag stream never recorded the distinction |
| `reference_expression` -> new `borrow` bucket, later found unnecessary | The bucket collapses into `name` or `mutation` by a merge rule. Append-only-compatible: the finer tag remains a valid refinement |
| `lifetime` -> type-form, later found to want its own bucket | Cheap. Nothing else in the 12 languages merges into it, so no cross-language damage is possible |

The asymmetry is therefore *not uniform across the family*: it is severe
for `reference_expression` and mild for the type-side rows. That argues
for treating them as two decisions, not one.

### 3.4 RECOMMENDATION

**RECOMMENDATION (family 3), in two parts.**

(3a) Type-side — keep log_008's assignments: `reference_type`,
`pointer_type`, `lifetime` -> type-form; `lifetime_parameter`,
`for_lifetimes` -> F generics, DUAL with type-form where both are
present. **Confidence: medium-high; recorded as medium** because
type-form itself is an unadopted proposal and this inherits its
uncertainty.

(3b) Value-side — do NOT tag `reference_expression` as `name`. Give it a
distinct provisional bucket (`borrow`), on the strength of
`border_lattice` class 2's "incompatible" verdict. **Confidence: medium**
on the placement, **high** on the negative claim that `name` is wrong.

**What would raise it:** (a) the owner's answer to gap-question G3 below;
(b) c/cpp ingest — if C++'s reference/pointer/move triad can be tagged
consistently with Rust's, the bucket is real; if C++'s move turns out to
be invisible to the grammar (as I expect), that is itself the strongest
possible evidence that this intention cannot be carried by `ur_kind` at
all and belongs to the ledger; (c) a statement of whether any downstream
consumer computes `border_lattice` verdicts from `ur_kind` — if none
does, the whole family drops in stakes.

---

## family 4 — error propagation

Rows: `try_expression` (`?`), `try_block`, and adjacently
`return_expression` in its early-return use.

### 4.1 what the intentions data says

| field path | content |
| --- | --- |
| `intent_categories[2]` | `id` = "C", `name` = "optionals", `desc` = **"null safety, absence in types"** |
| `row_satisfiers.C.basis` | "Option&lt;T&gt; with no null in the language; every other cell is it weakened (sugar removed, enforcement removed, or null retained alongside)" |
| `t1_realizations.C.Rust` | "Option&lt;T&gt; pure sum type; no null exists at all — strongest form" |
| `t1_realizations.C.Go` | "nil + (value, ok) multiple-return idiom; no type-level option" |
| `t1_realizations.C.Java` | "Optional&lt;T&gt; as a library object; null remains everywhere else" |
| `t1_realizations.C.Swift` | "Optional IS an enum — sum type with ? ! sugar" |
| `t2_compatibility` C/J row | `note` = "run-time attribute synthesis (method_missing) breaks null-safety proofs; only staging metaprogramming to dev-time saves both", `verdict` = "conflict" |
| `t2_compatibility` C/E row | `note` = "optional interface members reopen null holes (Swift @objc); forbid them", `verdict` = "tension" |
| all of `intent_categories` | no row mentions error, exception, throw, catch, failure or Result |

Every one of C's twelve cells is about ABSENCE. The word "error" does not
occur in the C row anywhere. `Result<T, E>` is not mentioned in the
artifact at all — I checked the full C row and `row_satisfiers.C`.

`t1_realizations.C.Go` is the only cell that arguably reaches toward
error handling, since Go's `(value, ok)` idiom and its `(value, err)`
idiom are the same shape. But the cell names `ok`, not `err`, and calls
it a response to "no type-level option" — the artifact is reading Go's
multi-return as an absence workaround, not as error flow.

### 4.2 candidate placements, argued against each other

**Candidate A — C optionals, as log_008 provisionally assigns.**

Argument for: in Rust, `?` is one operator that works over both `Option`
and `Result`, and both are sum types with a "nothing useful here" variant.
`t1_realizations.C.Rust` names Option's sum-type-ness as the reason Rust
is the C satisfier. Mechanically `?` on `Result` and `?` on `Option` are
the same short-circuit. Splitting them would mean tagging one operator
two ways depending on the type of its operand — which `ur_kind` cannot
see, since it works from the grammar and the grammar does not type-check.
That last point is a strong practical argument: **candidate A is the only
placement `ur_kind` can actually compute.**

**Candidate B — a new bucket, provisionally `error-flow`.**

The contrast, one instance each:

- Instance C describes: `let x: Option<u32> = map.get(k).copied();` —
  there may or may not be a value. Absence is an expected, ordinary
  outcome. Nothing went wrong.
- Instance in dispute: `let f = File::open(p)?;` — something went wrong,
  the failure carries a payload describing what, and `?` propagates that
  payload up the call chain, changing the control flow of the enclosing
  function. The payload and the non-local control transfer are both
  absent from the first instance.

`intent_categories[2].desc` — "null safety, absence in types" — describes
the first instance exactly and the second not at all.

Cross-language check, which is where B gets its strength:

| language | its error-propagation construct | its optional construct | are they the same node? |
| --- | --- | --- | --- |
| Java | `throw_statement`, `try_statement`, `catch_clause`, `throws` in a method signature | `Optional<T>` — a library generic, no dedicated syntax, per `t1_realizations.C.Java` "Optional&lt;T&gt; as a library object" | No, and not even close: one is four grammar constructs, the other is zero |
| Python | `raise_statement`, `try_statement`, `except_clause` | `None` plus an `Optional` hint, per `t1_realizations.C.Python` "None + Optional hint; unenforced" | No. Python's error machinery is grammar; its optional machinery is unenforced annotation |
| Swift | `throws`, `try`/`try?`/`try!`, `do_statement`, `catch_clause` | `Optional`, per `t1_realizations.C.Swift` "Optional IS an enum" | No — and Swift is the sharpest case, because `try?` deliberately CONVERTS the error channel into the optional channel, which only makes sense if they are two channels |

The grammar constructs are **[my language knowledge]**; each optional
cell is quoted from the artifact. The finding: in at least three of the
twelve, error propagation has dedicated grammar and optionals do not, or
vice versa. Tagging Rust's `?` as C sets the precedent that Java's
`throw_statement` is C too — and then C, whose satisfier is "preliminarily
solved" on Rust's Option (`row_satisfiers.C.status`), silently acquires
exception handling, which no cell in its row anticipates.

**Candidate C — `choice` (object 5) plus `function` (object 7).**

Argument for: mechanically `?` is "if the value is the bad variant,
return early". That decomposes into object 5 and object 7's return half,
both of which already exist. No new bucket, no gap claim.

Argument against: that is a description of the LOWERING, not of the
intention. By the same argument `while` is `choice` plus a jump, and the
minimum set keeps `repetition` as object 6 anyway. The artifact clearly
does not consider decomposability sufficient grounds for omission.

### 4.3 cost asymmetry if wrong

| wrong choice | what breaks |
| --- | --- |
| `?` -> C, then Java `throw_statement` / Python `raise_statement` -> C at later ingest | Two intentions merge that three of twelve languages spell with entirely disjoint grammar, and that Swift provides an explicit conversion between (`try?`). Unrepairable at the neutral layer |
| `?` -> C, but with a rule that error constructs in other languages get their own bucket | Rust becomes the odd one out: the same intention is C in Rust and `error-flow` elsewhere. Repairable, but leaves the vocabulary inconsistent in a way that shows up in every cross-language query |
| `?` -> new `error-flow`, later ruled to be C after all | A merge of `error-flow` into C. Append-only-compatible |
| `?` -> `error-flow`, but `?` over `Option` genuinely is C | A small, systematic mis-tag on one operator, correctable by a type-aware pass later. Note this cost is *bounded* and *local* — it affects one kind |

The bounded-versus-unbounded contrast is the decisive part: the cost of
over-splitting here is one operator sometimes tagged too specifically;
the cost of under-splitting is exceptions and optionals fused across
twelve languages.

### 4.4 RECOMMENDATION

**RECOMMENDATION (family 4):** tag `try_expression` and `try_block` with
a distinct bucket — provisionally `error-flow` — rather than C optionals,
and record explicitly in the tag's justification that in Rust the same
operator also serves `Option`, so a type-aware pass may later split it.
Keep the DUAL with C rather than dropping C entirely, since the Option
usage is real.

**Confidence: medium.** The cross-language evidence is strong; what holds
me back is candidate A's practical argument that `ur_kind` cannot see the
operand type, so `error-flow` on `?` will sometimes be tagging an
optional access as an error. That is a real defect in my own
recommendation and the owner should weigh it.

**What would raise it:** (a) a corpus count of Rust `try_expression`
nodes by operand type — if `?` over `Result` dominates `?` over `Option`
by a wide margin, the mis-tag cost is negligible and confidence goes
high; this is measurable today from the pinned corpus plus a shallow type
heuristic; (b) the owner's answer to gap-question G2; (c) ingest of any
language with `throw`/`catch` syntax, which forces the question
immediately rather than deferring it.

---

## family 5 — structural containers

Rows: `source_file`, `declaration_list`, `block`, `unsafe_block`,
`empty_statement`, `parenthesized_expression`, and adjacently
`enum_variant_list`, `field_declaration_list`, `use_list`, `arguments`,
`parameters`, `match_block`.

### 5.1 what the intentions data says

| field path | content |
| --- | --- |
| `minimum_set[3]` | `object` = "sequence", `desc` = **"do this, then that"** |
| `minimum_set[8]` | `object` = "collection", `desc` = "list (ordered many); map (keyed many)" |
| `border_lattice` class 3 | `name` = "evaluation-order", `crossing` = "none — egress rule (temporaries), no border object", `verdict` = "identical" |
| `border_lattice` class 6 | `name` = "collection-order", `crossing` = "unordered (perf-borrow) collection -> ordered frame", `spelling` = "explicit ordering step", `verdict` = "convertible" |
| `canon.P10.statement` | "insertion-ordered by majority + determinism; no single canon language; unordered as explicit perf borrow" |
| `canon.P11.statement` | "insertion-ordered (JS/Dart canon...)" |

Two things stand out. First, `minimum_set[3].desc` is not "a group of
things" — it is "do this, then that", an explicitly TEMPORAL claim about
execution order. Second, the artifact takes order seriously enough to
give it a whole `border_lattice` class (6) and to legislate it twice
(`canon.P10`, `canon.P11`). Order is not treated as incidental anywhere
in this data.

### 5.2 candidate placements, argued against each other

The family is not homogeneous, and I think that is the finding. The
visible contrast, one instance of each:

- Instance where `sequence` is exactly right: the `block` of
  `fn f() { a(); b(); c(); }`. Swapping `a()` and `b()` changes what the
  program does. `minimum_set[3].desc` "do this, then that" is literally
  true of this node.
- Instance where `sequence` is a false claim: the `declaration_list` of
  `mod m { fn a() {} fn b() {} }`. Swapping the two `fn` items changes
  nothing whatever — Rust items are order-independent, mutually visible
  regardless of position. There is no "then". Tagging this `sequence`
  asserts a temporal relation the language does not have.

The same split runs through the family:

| kind | is its content order-bearing? | which side |
| --- | --- | --- |
| `block` | yes — statements execute in written order | sequence, correctly |
| `unsafe_block` | yes — same, plus an obligation with no bucket | sequence, correctly (the obligation is a separate question) |
| `match_block` | partly — arms are tried in order, which is semantic in Rust | sequence, arguably |
| `source_file` | no — items are order-independent | NOT sequence |
| `declaration_list` | no — same | NOT sequence |
| `enum_variant_list` | no — variants have discriminants but no execution order | NOT sequence (and log_008 assigns `record`, not sequence, so this is consistent already) |
| `field_declaration_list` | no | NOT sequence (already `record`) |
| `parenthesized_expression` | n/a — holds exactly one thing | neither |
| `empty_statement` | n/a — holds nothing | neither |

Candidate A — `sequence` for the whole family, as log_008 assigns to
`source_file`, `declaration_list`, `block`, `unsafe_block`,
`empty_statement`. Argument for: it is the only structural object that
fits a container, and log_008 says so explicitly ("Object 4 is the only
structural object that fits a whole-file container"). Simple, total.

Candidate B — split: order-bearing containers `sequence`, order-free
declaration containers get a distinct structural tag (provisionally
`container`, or folded into `declarative-form`). Argument for: it stops
the vocabulary from asserting something false, at the cost of one extra
distinction that is computable from the grammar's own field names without
any semantic analysis.

Cross-language check:

| language | order-free container | order-bearing container | does A's merge hold? |
| --- | --- | --- | --- |
| Go | `source_file` — top-level declarations are order-independent, and Go famously permits use-before-declare at package scope | `block` — statements ordered | No. The same merge would be false in Go for the same reason |
| Java | `class_body` — methods and fields visible regardless of order | `block` | No, same |
| Python | `module` — top-level statements EXECUTE IN ORDER; a `def` at module level is a statement that runs | `block` | Yes, and this is the interesting one: Python's module body genuinely is a sequence. So the split is not the same split in every language |

These are grammar/semantic facts **[my language knowledge]**; the
artifact does not address container nodes. Python's case is what makes me
confident the split is worth making: if `source_file` is tagged
`sequence` in Rust and `module` is tagged `sequence` in Python, the tag
looks like a successful merge while the two nodes differ on exactly the
property the tag names. That is a merge that *passes* a naive check and
is still wrong.

Candidate C — NONE for `empty_statement` and
`parenthesized_expression`. Argument for: they carry position and nothing
else, and log_008 concedes "NONE is defensible" for both. Argument
against: log_008's census argument — a positive tag distinguishes
"classified as carrying nothing" from "not yet done".

### 5.3 cost asymmetry if wrong

This family has the *mildest* asymmetry of the five, and I want that on
the record because it should affect how much of the owner's attention it gets.

| wrong choice | what breaks |
| --- | --- |
| Everything `sequence`, later split | Repairable append-only: the split adds a finer tag under an existing coarse one, and no cross-language information was destroyed, because "is this container ordered" is recoverable from the substrate kind at any time. The Rust `declaration_list` is still a `declaration_list` |
| Split, later merged | Also cheap |
| NONE for the two degenerate kinds | The census defect log_008 names; annoying, not destructive |

The reason this family is cheap and family 2 or 4 is expensive: container
kinds are 1:1 recoverable from the substrate kind name in every language,
so nothing is irreversibly lost. Sum-versus-product and error-versus-
absence are *semantic* distinctions that a substrate kind name does not
carry.

### 5.4 RECOMMENDATION

**RECOMMENDATION (family 5):** split, but treat it as low-priority.
Order-bearing containers (`block`, `unsafe_block`, `match_block`) stay
`sequence`. Order-free declaration containers (`source_file`,
`declaration_list`) get a distinct structural tag rather than `sequence`,
because `minimum_set[3].desc` makes a temporal claim that is false of
them. `empty_statement` and `parenthesized_expression` take a positive
"carries no object" tag rather than NONE, following log_008's census
argument, and I do not think they merit further discussion.

**Confidence: medium-high on the diagnosis** (that `sequence` on
`declaration_list` is a false claim) — recorded as **medium** on the
recommendation, because the cheap repair path means "tag it `sequence`
now, split later" is a perfectly defensible alternative that costs almost
nothing, and the owner may reasonably prefer to spend the decision budget on
families 2 and 4.

**What would raise it:** (a) a statement of whether any consumer will
rely on `sequence` implying execution order — if yes, confidence goes
high immediately; if no consumer cares, the whole question is cosmetic;
(b) c/cpp ingest, where a `translation_unit` has the same order-free
character as Rust's `source_file` and would confirm the pattern.

---

## do the five families expose gaps in the intentions data itself?

Stated as QUESTIONS to the owner, because this artifact is his research and
because a gap finding from a downstream consumer is a hypothesis, not a
correction. Nothing here has been applied anywhere. Three of the five
families produce a question; two do not.

**G1 — sum types.** The artifact names "sum type" three times
(`t1_realizations.C.Rust`, `t1_realizations.C.Swift`, the C/D row of
`t2_compatibility`: "option is a sum type, match consumes it"), makes a
sum type the satisfier of row C (`row_satisfiers.C.satisfier` = "Rust",
`basis` = "Option&lt;T&gt; with no null in the language"), and makes the
closed set a sum type provides the precondition for row D's
exhaustiveness (`row_satisfiers.D.basis`). `minimum_set` has `record`
("values grouped under named fields") and no sum. **Question: is the
absence of a sum object from the minimum set deliberate — because a sum
is derivable from record plus choice, or because it was judged
category-tier rather than minimum-tier — or is it an artefact of the
basis audit's nine keys (`basis_audit`: bool, bytes, executor, float64,
function_value, hashing, int64, list, record) not having included one?**
This is the question I would most want answered, because it is upstream
of family 2 and it touches two of the ten rows.

**G2 — error flow.** No row in `intent_categories` mentions error,
exception, failure or Result, and no cell of `t1_realizations.C` uses the
word "error" — C is consistently about absence. Yet all twelve languages
in `languages` have an error-propagation story, and at least three
(Java, Python, Swift) spell it with dedicated grammar that has nothing to
do with their optional story. **Question: was error propagation
considered and deliberately excluded from the ten categories — perhaps as
already covered by C plus D, or as a library concern rather than a
language intention — or is there an eleventh row that the ten were
distilled from?** I note that `intent_categories` is described in
log_008 as ten "differentiator" categories, which may mean the criterion
was *divergence between languages* rather than *presence*; if error
handling was judged non-divergent, that would answer the question
completely and I would withdraw it.

**G3 — aliasing and ownership.** `border_lattice` has two entries with
`verdict` = "incompatible" and both are aliasing:
class 2 "aliasing is load-bearing across the border" (`spelling` = null)
and class 7 "mutable object across spawn boundary" (`spelling` = null).
Ownership also drives `canon.P9` ("single-owner Vec semantics (no
aliasing surprises)"), `canon.P12` ("reference + explicit .copy()"),
`basis_audit.list.Rust` and `basis_audit.record.Rust` ("native:move"),
and `row_satisfiers.B.in_hub` ("Rust's transfer proof (send checked at
dev-time, a Ledger judgment)"). It appears in neither `minimum_set` nor
`intent_categories`. **Question: is aliasing deliberately scoped to the
border lattice — i.e. it is a property of crossings rather than an
intention an object holds — or does the fact that it is the lattice's
only unspelIable incompatibility argue for it having a place in the
tiers too?** I lean toward the first reading being the intended one
(a border property is a different kind of thing from an intention), which
is why family 3's recommendation is medium rather than high.

**Not gaps, in my reading.** Family 1 (namespacing) and family 5
(containers) do not, I think, expose gaps. The artifact is a theory of
what a program does; namespacing governs what a program can see, and
container nodes are grammar bookkeeping. Their absence looks like scope,
not omission. I raise them here only to say I considered and rejected the
gap reading for both — the owner may disagree, particularly on namespacing,
since `t1_realizations.J["C++"]` shows at least one language where the
import mechanism is a dev-time code transform and therefore does have an
intention.

**One further question, not from the five families but noticed while
reading.** `const_block` (log_008 flags it UNCERTAIN, "the min set has no
compile-time-execution object"): `intent_categories[9]` is "reflection,
macros, codegen", and `row_satisfiers.J.basis` says the J row "spans
three stages (run-time mutation, dev-time transforms, type-level)" and
"must be truncated (dev-time only), not satisfied". **Question: does
"dev-time transforms" in J's staging include compile-time evaluation of
ordinary code (`const fn`, `const { }`, C++ `constexpr` — which
`t1_realizations.J["C++"]` does list under J), or is const evaluation a
different stage again?** The answer settles `const_block` and, at
language two, all of C++'s `constexpr` surface.

---

## open questions for the owner

The five recommendations as a decision list. Each is a recommendation,
not a decision, and each is reversible in the direction stated.

| # | family | RECOMMENDATION | confidence | cheapest thing that would settle it |
| --- | --- | --- | --- | --- |
| 1 | imports / namespacing | Not `name`. A distinct `namespace-form` bucket; `scoped_identifier`, `crate`, `super` stay `name` | medium | the owner ruling whether the artifact's silence on namespacing is scope or gap |
| 2 | sum types / enums | Not `record`. A distinct `sum` bucket at minimum-set tier, DUAL with D on `enum_item` only | high on "not `record`", medium on the placement | Answer to G1 |
| 3a | borrowing — type side | Keep log_008: type-form, DUAL with F where parameterized | medium | Inherits type-form's own adoption question |
| 3b | borrowing — value side | Not `name`. A distinct `borrow` bucket for `reference_expression`, on `border_lattice` class 2's "incompatible" verdict | high on "not `name`", medium on the placement | Answer to G3; c/cpp ingest |
| 4 | error propagation | Not C alone. A distinct `error-flow` bucket, DUAL with C, with the `?`-over-Option caveat recorded | medium | Corpus count of `try_expression` by operand type; answer to G2 |
| 5 | structural containers | Split: order-bearing containers `sequence`; order-free declaration containers a distinct structural tag. LOW PRIORITY — the repair is cheap either way | medium | Whether any consumer relies on `sequence` implying execution order |

Four further questions, in the order I would ask them:

7. **Which of these five is worth a decision now?** Families 2 and 4
   carry unrepairable cost if wrong and both are decided by a single
   ruling each (G1, G2). Family 5 is cheap in both directions. If
   attention is scarce, 2 and 4 are where it pays.
8. **The three gap-questions G1, G2, G3** — each is asked as a question
   about the artifact's intent, not as a claim that it is incomplete.
   None has been acted on.
9. **Does a "not X" recommendation without an agreed "is Y" get
   recorded?** Three of the six rows above are stronger on the negative
   than the positive. If the vocabulary can carry a tag meaning
   "classified, and known NOT to be `name`/`record`/C, placement
   pending", the high-confidence half of each finding is preservable
   while the rest waits. That is a question about the vocabulary's
   shape and it interacts with log_008 open question 1
   (exclusive-versus-primary).
10. **Everything above is Rust-only**, and log_006 item 2 argues against
    guessing ahead of ingest. Three of the five families (1, 3, 5) would
    be substantially settled by c/cpp ingest alone, since C++ contains
    the hard case for each: `#include` versus `using_declaration` versus
    `namespace_definition`; references, pointers and library-level
    `std::move`; and an order-free `translation_unit`.

---

## sources

- `PRIVATE/PseudoIR/Tools/intentions/pc_intentions.json` —
  `minimum_set`, `intent_categories`, `t1_realizations`,
  `t2_compatibility`, `row_satisfiers`, `border_lattice`, `canon`,
  `basis_audit`, `primitives`, `operators`, `policy_refs`, `languages`,
  `meta`. Read 2026-08-05; all quotations are verbatim from those fields.
- `PRIVATE/PseudoCoup_v5/DevComms/log_008_kinds_coarse_tagging_draft.md`
  — the full table, the two PROPOSED buckets, the 37 UNCERTAIN rows and
  the five clusters this log takes as its sections.
- `PRIVATE/PseudoCoup_v5/DevComms/log_006_ur_kinds_vocabulary.md` —
  items 3 and 5 (what `ur_kind` classifies, and the mechanical seed),
  plus item 4's rule that merges are judged on grammar facts and meaning,
  never on name resemblance, which is the standard applied throughout.
- My own knowledge of the grammars of Go, Java, Python, Swift, C++ and
  TypeScript, marked **[my language knowledge, not in the data]** at
  every point of use, and never used to support a merge on its own.
