# log 014 — coarse buckets versus derivations: the reduction reading against the guard reading

2026-08-06. DECISION-SUPPORT EVIDENCE FOR DEE. Nothing here is applied.
One file was written, this one. No `Planning/` file was read for edit and
none was touched.

**The decision, in the owner's framing of 2026-08-05.** A coarse bucket in the
`ur_kind` vocabulary can be read two ways, and the two readings disagree
about three constructs.

- **REDUCTION reading** (Karp sense — a reduction is a mapping to a MORE
  GENERAL object, not a shrinking). A construct is tagged by the
  DOMINANT object it reduces to. The dominant object is the more
  general, more capable one: it can hold everything the construct can
  hold, and the capability the construct does not use sits inert.
  the owner's intent-dominance, quoted from
  `~/Programming/PseudoCoup_v5/DevComms/log_006_ur_kinds_vocabulary.md`
  item 3:

  > "the ultimate intention of an object is the greatest amount of
  > intent that object can hold... the dominant intentions cover all the
  > intentions of all other objects... the intent-dominant object can
  > essentially hot-swap with zero loss of functionality — since unused
  > intentions are inert."

  Characterizing: this is a claim about CAPACITY, not about shape. The
  worked example is Rust's `enum_item`, which reduces to a tagged record
  — a record plus a choice on the tag field. The record is dominant
  because it can hold even the states the sum type forbids (both
  payloads present at once, no payload at all). Rust does not add
  run-time behaviour on top of the record; it adds a compile-time PROOF
  that the forbidden states never occur.

- **GUARD reading.** A construct keeps its own bucket when tagging it
  with the shared dominant object would invite a wrong cross-language
  merge. The bucket is not a claim about what the construct IS; it is a
  fence that stops the next language's tagger from following a
  precedent that does not hold. Java's `enum_declaration` is not a sum
  type, and a `record` tag on Rust's `enum_item` is the precedent that
  makes it look like one.

**The three constructs in scope:** sum types, error flow, and
aliasing/borrowing. These are exactly the three that
`~/Programming/PseudoCoup_v5/DevComms/log_013_intentions_gap_history.md`
traced to a single event — the 2026-07-28 copy-forward that took the
conclusion of `minimum_intention_set.md` and left the argument.

**Why the framing matters now.** The recovered argument at
`~/Programming/PseudoIR/Tools/intentions/minimum_intention_set.md` IS the
reduction reading, written down by the owner before the question was asked.
Its governing rule, lines 21–24:

> "Rule for this document: entries earn their place by being
> underivable from the others. Anything derivable is listed as derived,
> or left out."

Characterizing: "derivable" there means exactly what "reduces to a
dominant object" means here. The document is a reduction argument
throughout. That is the first fact of this brief, and it puts
`~/Programming/PseudoCoup_v5/DevComms/log_011_uncertain_families_evidence.md`
— which recommended three new buckets, all on guard grounds — in direct
tension with the owner's own recovered rulings on two of the three, and in
partial tension on the third.

**Provenance marking, carried over from log_011.** Claims from
`~/Programming/PseudoIR/Tools/intentions/pc_intentions.json` are cited by
field path. Claims about how a language spells something, where the
artifact does not say, are marked **[my language knowledge]**. Uncertain
table rows are marked **[UNSURE]** in the row itself.

**Standing fact weighed throughout.** PCv5 is INGRESS-ONLY into a Python
hub. the owner: every major intention will literally exist in the hub; egress
is not his concern. Section 3 of each construct applies this.

---

# construct 1 — sum types

## 1.1 what the owner's recovered argument says

`~/Programming/PseudoIR/Tools/intentions/minimum_intention_set.md`,
§"Audit: the 12 languages' signature intentions, derived", lines 161–165:

> "optionals, null safety
> (Swift, Kotlin, TS, Rust)
> = record with a tag field
> + choice on the tag."

And the audit's own admission standard, lines 140–144:

> "Each entry: the feature people choose the language for, and its
> composite. A feature survives the audit if its derivation is a known
> compiler technique, not hand-waving."

Characterizing: the sum type went through the audit under the name
"optionals, null safety", was given a two-object derivation, and the
derivation is a known compiler technique (a tagged union IS a record
with a discriminant, in every compiler that has ever emitted one). Under
the document's own rule it is derived and therefore does not earn a
place. The audit verdict, lines 222–227:

> "No 12th object found. One amendment (function IS a value, item 7).
> One non-object identified (static proof grammars). The 11 stand,
> pending the services-grain question."

Characterizing: "No 12th object found" is a positive finding, not a
silence. log_013 §1.4 reached the same reading independently:

> "**MY READING: "was discussed but never a row" — confidence high.**
> The mechanism was examined by name in the audit (S1) and passed as
> derived under the document's stated derivability rule".

## 1.2 the 12-language table

Question per row: what is the language's nearest construct to Rust's
`enum_item`, what dominant object does it reduce to, and is that
reduction the SAME as Rust's (record + choice on the tag)?

| language | nearest construct (one phrase) | reduces to | same reduction as Rust's? |
| --- | --- | --- | --- |
| Python | class hierarchy, or `Enum` subclass, or a tagged `dict`/dataclass union | record + choice on the tag — but the tag is a run-time type test, not a declared field | SAME reduction, WEAKER enforcement. No compile-time proof at all. `t1_realizations.C.Python`: "None + Optional hint; unenforced" |
| Dart | `sealed class` with subtypes (Dart 3), exhaustive `switch` | record + choice on the runtime type | SAME reduction, different tag carrier (class identity rather than a field) **[my language knowledge]** |
| Go | struct with a discriminant field, or an interface with a closed set of implementors by convention | record + choice on the tag | SAME reduction, and Go is the language where the reduction is what the programmer literally writes — there is no sugar to see through **[my language knowledge]** |
| Kotlin | `sealed class` / `sealed interface` + `when` | record + choice on the runtime type | SAME reduction, class-identity tag **[my language knowledge]** |
| Java | `enum_declaration` (fixed set of singleton INSTANCES of one class); the real sum is `sealed` interface + records | The `enum_declaration` reduces to record + a name-to-instance map. The `sealed` hierarchy reduces to record + choice on the type | The `enum_declaration` is NOT the same reduction. The `sealed` hierarchy IS. `t1_realizations.D.Java`: "switch patterns + record deconstruction; sealed exhaustive" |
| C# | `enum` (named integer constants); the nearest sum is a `record` hierarchy with a `switch` expression | `enum` reduces to named values over an integer; the record hierarchy reduces to record + choice | The `enum` is NOT the same reduction — it is closer to `minimum_set[0]` value plus `minimum_set[1]` name. The hierarchy IS **[my language knowledge]** |
| TypeScript | `union_type` with a discriminant property (`{kind: "a"} \| {kind: "b"}`); separately `enum_declaration`, a constant bag | The union reduces to record + choice on the tag, with the tag an ordinary property. The `enum_declaration` reduces to named values | The union IS the same reduction — and TypeScript is the clearest case, because the tag field is written out by hand. `t1_realizations.D.TypeScript`: "— native; discriminated unions + narrowing carry the intent" |
| Swift | `enum` with associated values | record + choice on the tag | SAME reduction. `t1_realizations.C.Swift`: "Optional IS an enum — sum type with ? ! sugar" |
| Rust | `enum_item` / `enum_variant` / `enum_variant_list` | record + choice on the tag (`minimum_set[7]` + `minimum_set[4]`) | reference row. `t1_realizations.C.Rust`: "Option&lt;T&gt; pure sum type; no null exists at all — strongest form" |
| C++ | `std::variant` (library, not grammar); `union` + a tag field; `enum class` | `std::variant` reduces to record + choice, but through a template call, so the GRAMMAR shows only a call. Raw `union` + tag is the reduction, written out | SAME reduction, INVISIBLE TO THE GRAMMAR for `std::variant` — this is the same shape log_011 §3.2 found for `std::move` **[my language knowledge]** |
| Ruby | Symbols plus a `case`; or class hierarchy. No sum construct at all | record + choice on the tag, with no declaration site whatsoever | SAME reduction, no node to tag **[UNSURE — Ruby has no construct near enough that "nearest construct" is well defined]** |
| PHP | `enum` (8.1), backed or pure; cases may have methods but not per-case payloads | record + a name-to-instance map, like Java's | NOT the same reduction — PHP enum cases cannot carry distinct payloads, so there is no per-variant record shape **[UNSURE — I am not certain whether PHP 8.1+ enums can carry per-case data through interfaces in a way that changes this]** |

**Reading of the table.** Nine of twelve reduce the same way (record +
choice on the tag), which is strong support for the reduction reading
being TRUE. Three of twelve — Java, C#, PHP — have a construct SPELLED
`enum` that reduces differently. The reduction reading and the guard
reading are therefore not disagreeing about facts. They disagree about
whether a tag should record the true reduction or fence off the false
merge that the shared spelling invites.

## 1.3 what each reading implies for `ts_to_ur` and the `kinds` vocabulary

The per-language mappers live at
`~/Programming/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_2_ts_to_ur/CORE_0_0_0_2_ts_to_ur.md`
("the mappers are per-language"), so both readings cost the same number
of map entries; what differs is the vocabulary they map INTO.

**Reduction reading — worked instance.** `ur_kind` stays at 21 buckets.
The Rust mapper writes:

```python
# ts_to_ur/rust.py  — reduction reading
"enum_item":         {"ur_kind": "record", "dual": "choice"},
"enum_variant":      {"ur_kind": "record"},
"enum_variant_list": {"ur_kind": "record"},
```

and the Java mapper, at language two, is FORCED by the table above to
write something different, because the reduction genuinely is different:

```python
# ts_to_ur/java.py  — reduction reading, language two  [Java]
"enum_declaration":   {"ur_kind": "record", "dual": "name"},   # constant bag
"class_declaration@sealed": {"ur_kind": "record", "dual": "choice"},
```

Characterizing: the reduction reading does not by itself produce the bad
merge. It produces `record` on both nodes, but with different duals, and
the dual is where the and-versus-or lives.

**Guard reading — worked instance.** `ur_kind` gains a 22nd bucket.

```python
# ts_to_ur/rust.py  — guard reading
"enum_item":         {"ur_kind": "sum", "dual": "pattern_matching"},
"enum_variant":      {"ur_kind": "sum"},
```

```python
# ts_to_ur/java.py  — guard reading, language two  [Java]
"enum_declaration":         {"ur_kind": "record"},   # NOT sum: fence holds
"class_declaration@sealed": {"ur_kind": "sum"},
```

Characterizing: the fence is doing real work in the Java mapper — the
tagger who sees `sum` on `enum_item` cannot reach for it on
`enum_declaration` without noticing that Java's enum has no per-case
payload. Under the reduction reading the same tagger sees `record` and
agrees with it for the wrong reason.

**The hub-side illustration**, which is where the two readings can be
compared on equal ground. Both readings lower to the same Python:

```python
# hub, spelled out — this is what Rust's enum Shape { Circle(f64), Rect(f64,f64) } becomes
@dataclass
class Shape:
    tag: str                      # "Circle" | "Rect"
    circle_0: float | None = None
    rect_0: float | None = None
    rect_1: float | None = None
```

Characterizing: the hub object can hold `tag="Circle"` with `rect_0` set
— a state Rust forbids. That is the dominance relation, visible in four
lines: the record holds strictly more states than the sum type does.

## 1.4 the ingress-only argument, applied

In the hub everything becomes spelled-out Python. The four-line dataclass
above is the destination for all twelve languages' sum constructs; the
compile-time proof does not survive ingress because there is nothing in
the hub to check it against and no egress that would need it.

| reading | what ingress-only BUYS it | what ingress-only COSTS it |
| --- | --- | --- |
| reduction | Everything. The hub form IS the reduction. A `record` tag names the thing the hub will actually build, so the tag and the destination agree, and the mapper's job is to fill in the tag field the source language was hiding | Nothing at ingress. The cost is entirely at egress, which the owner has said is not his concern — a `record` tag cannot tell a future egress writer that Rust wants its proof back |
| guard | Cross-language hygiene at language two and after. The fence is not about the hub; it is about the NEXT MAPPER AUTHOR | A 22nd bucket that no hub object corresponds to. Nothing downstream of ingress consumes `sum` differently from `record`, because the hub has one dataclass either way |

Characterizing: ingress-only weakens the guard reading's payoff from
"correctness of the neutral layer" to "correctness of the tagging
process". That is a real benefit but it is a PROCESS benefit, and process
benefits can be bought with a comment instead of a bucket.

## 1.5 RECOMMENDATION — sum types

Where the recovered ruling and log_011 conflict, both quoted.

the owner's recovered argument
(`~/Programming/PseudoIR/Tools/intentions/minimum_intention_set.md`,
lines 161–165, 222–227):

> "optionals, null safety (Swift, Kotlin, TS, Rust) = record with a tag
> field + choice on the tag."
> ... "No 12th object found."

log_011 §2.4:

> "**RECOMMENDATION (family 2):** do NOT tag `enum_item` /
> `enum_variant` / `enum_variant_list` as `record` alone. Tag them with
> a distinct bucket — provisionally `sum`, at minimum-set tier ...
> **Confidence: high** on the negative claim (not `record`)."

Which the evidence favours, and why: **the recovered ruling, on the
substance; log_011, on the operational risk.** log_011's high-confidence
negative claim was made without having seen the audit entry — it was
arguing against silence, and log_013 §4 already says so ("All three of
log_011's gap-questions are questions the argument already answers"). The
audit entry is not silence; it is a derivation that the 12-language table
above independently confirms in nine of twelve rows. log_011's real
finding survives the ruling, but it is narrower than it looked: it is not
that `record` is the wrong reduction, it is that `record` ALONE on
`enum_item` loses the closed-set fact that row D's exhaustiveness depends
on (`row_satisfiers.D.basis`: "exhaustive + deep destructuring subsumes
the row").

**MY RECOMMENDATION (sum types): take the reduction reading, with the
dual carrying the guard.** Tag `enum_item` `record` DUAL `choice`, and
`enum_variant`/`enum_variant_list` `record`. Do NOT add a `sum` bucket.
Record in the Rust mapper's justification the one fact the reduction
loses — that the tag is closed and the states are exclusive — and make
that a MAPPER NOTE, not a bucket.

**Confidence: medium-high.** High that `record` is the correct
reduction (nine of twelve rows, plus the owner's own audit). Medium-high on
"therefore no new bucket", because log_011's name-resemblance argument
is genuinely strong and I am trading a structural guarantee for a
process discipline.

**What would change it:** (a) the owner ruling that `ur_kind` is exclusive
rather than primary-plus-dual — if a node can carry only ONE bucket, the
dual cannot carry the guard and my recommendation flips to log_011's;
this is log_008 open question 1 and it is upstream of everything here.
(b) A demonstration that some consumer computes exhaustiveness from
`ur_kind` alone. (c) Ingest of Java or C# showing that a mapper author
in practice followed the `record` precedent onto `enum_declaration` —
one real instance of the bad merge would settle it against me.

---

# construct 2 — error flow

## 2.1 what the owner's recovered argument says

`~/Programming/PseudoIR/Tools/intentions/minimum_intention_set.md`,
§"Derived (not in the set)", lines 105–107:

> "exception
> choice + early return through
> call layers"

and lines 183–185:

> "defer (Go), RAII (C++), using (C#)
> = sequence + choice, same derivation as exception."

Characterizing: this is the most explicit of the three rulings. Error
flow is not merely absent from the set — it is NAMED in the list of
things positively excluded, with its reduction given. And the second
quote shows the reduction was load-bearing enough to be reused for three
more constructs. log_013 §2.3 dates the loss precisely: present
2026-07-24 to 2026-07-27, gone at the 2026-07-28 lift.

Note what the reduction says and does not say. It reduces exception to
`choice` (`minimum_set[4]`) plus `function`'s return half
(`minimum_set[6]`) — NOT to `record`, and NOT to C optionals. So the
recovered ruling does not endorse log_008's provisional placement of
`try_expression` under C either.

## 2.2 the 12-language table

Question per row: nearest construct to Rust's `?`, what it reduces to,
same reduction as Rust's?

| language | nearest construct (one phrase) | reduces to | same reduction as Rust's? |
| --- | --- | --- | --- |
| Python | `raise` / `try` / `except`, plus implicit propagation through every frame | choice + early return through call layers — but the choice is INVERTED: propagation is the default and catching is the explicit act | SAME objects, OPPOSITE default. `t1_realizations.C.Python`: "None + Optional hint; unenforced" is about absence, not this |
| Dart | `throw` / `try` / `on`-`catch`; all exceptions unchecked | choice + early return, propagation by default | SAME as Python's shape, not Rust's **[my language knowledge]** |
| Go | `if err != nil { return ..., err }` written by hand at every call site | choice + early return through call layers — WRITTEN OUT, no sugar | SAME reduction as Rust's, and Go is the row that proves the reduction, because Go's spelling IS the reduction. `t1_realizations.C.Go`: "nil + (value, ok) multiple-return idiom; no type-level option" |
| Kotlin | `throw` / `try`-`catch`; `Result<T>` in the stdlib but no propagation operator | choice + early return, propagation by default | Python's shape **[my language knowledge]** |
| Java | `throw_statement`, `try_statement`, `catch_clause`, and `throws` in the signature | choice + early return; `throws` adds a compile-time PROOF about which frames must handle | SAME objects; Java's checked-exception `throws` is the closest analogue anywhere to Rust's compile-time obligation. `t1_realizations.C.Java`: "Optional&lt;T&gt; as a library object; null remains everywhere else" |
| C# | `throw` / `try` / `catch`, unchecked | choice + early return, propagation by default | Python's shape **[my language knowledge]** |
| TypeScript | `throw` / `try` / `catch`; `Error` is untyped in the signature | choice + early return, propagation by default | Python's shape **[my language knowledge]** |
| Swift | `throws`, `try` / `try?` / `try!`, `do` / `catch` | choice + early return; `try` at each call site is a REQUIRED marker, so the propagation point is visible | CLOSEST to Rust's of the twelve — `try` marks the same syntactic position `?` does. `try?` converts the error channel into the optional channel, which is the artifact's own evidence that they are two channels |
| Rust | `try_expression` (`?`), `try_block` | choice + early return through call layers (`minimum_set[4]` + `minimum_set[6]`) | reference row |
| C++ | `throw` / `try` / `catch`; also error codes and `std::expected` (C++23) as library | choice + early return; `std::expected` propagation is hand-written or macro'd | Exceptions are Python's shape; `std::expected` is Rust's, and the language has BOTH **[my language knowledge]** |
| Ruby | `raise` / `begin`-`rescue`; also `raise` inside blocks with `retry` | choice + early return, propagation by default | Python's shape **[my language knowledge]** |
| PHP | `throw` / `try` / `catch`; historically also error levels and `@` suppression | choice + early return, propagation by default | Python's shape; the legacy error-level channel is a second mechanism **[UNSURE — I am not confident how much of the legacy channel is still grammar-visible in current PHP]** |

**Reading of the table.** All twelve reduce to the SAME two objects.
The reduction reading is not merely defensible here, it is uniform —
this is the strongest of the three tables. The divergence is entirely in
the DEFAULT (propagate silently versus mark the propagation point) and
in whether the obligation is proved at compile time. Both of those are
proof-and-default facts, not object facts.

## 2.3 what each reading implies for `ts_to_ur` and the `kinds` vocabulary

**Reduction reading — worked instance.** No new bucket; `?` gets the two
objects it reduces to.

```python
# ts_to_ur/rust.py  — reduction reading
"try_expression": {"ur_kind": "choice", "dual": "function"},   # early return through call layers
"try_block":      {"ur_kind": "choice", "dual": "sequence"},
```

```python
# ts_to_ur/java.py  — reduction reading, language two  [Java]
"throw_statement": {"ur_kind": "choice", "dual": "function"},
"catch_clause":    {"ur_kind": "choice"},
```

Characterizing: the merge that log_011 called catastrophic — Rust's `?`
and Java's `throw_statement` in one bucket — is here NOT a defect, it is
the finding. Under the recovered ruling they genuinely are the same two
objects, and the table above says so for all twelve.

**Guard reading — worked instance.** A 22nd or 23rd bucket.

```python
# ts_to_ur/rust.py  — guard reading
"try_expression": {"ur_kind": "error_flow", "dual": "optionals"},  # ? also serves Option
"try_block":      {"ur_kind": "error_flow"},
```

Characterizing: the guard here fences error flow off from C optionals,
which is what log_011 was actually worried about. But note that under the
reduction reading the fence is unnecessary, because the reduction never
sent `?` to C in the first place — it sends it to `choice` + `function`.
log_008's provisional C placement is rejected by BOTH readings.

**Hub-side illustration.** Both readings lower to the same Python. Rust's
`let f = File::open(p)?;`:

```python
# hub, spelled out
_r = file_open(p)
if _r.tag == "Err":
    return Err(_r.err)          # early return through the call layer
f = _r.ok
```

Characterizing: three lines, and both objects are visible in them — the
`if` is the choice, the `return` is the function's return half. This is
the derivation from the recovered argument, executed.

## 2.4 the ingress-only argument, applied

| reading | what ingress-only BUYS it | what ingress-only COSTS it |
| --- | --- | --- |
| reduction | A great deal. The hub has ONE error mechanism, whatever the source. Python's own `raise`/`except` is the hub's native spelling, so the twelve languages converge on it at ingress by necessity, not by choice. The reduction tag names the convergence point | It cannot record the DEFAULT difference — that Python propagates silently and Rust marks every propagation point. But that difference is a property of the source, and the substrate kind (`try_expression` versus `raise_statement`) still carries it losslessly |
| guard | The `error_flow` bucket would let a query ask "where does this program's failure travel" across languages without consulting the substrate | The bucket buys nothing the hub uses. And it has the defect log_011 admitted itself: `ur_kind` works from the grammar and cannot see the operand type, so `error_flow` on `?` will mis-tag every `?` over `Option` |

Characterizing: the ingress-only fact is more decisive here than on sum
types, because Python's hub IS one of the twelve and its error mechanism
is the one everything lands in.

## 2.5 RECOMMENDATION — error flow

the owner's recovered ruling
(`~/Programming/PseudoIR/Tools/intentions/minimum_intention_set.md`,
lines 105–107):

> "exception
> choice + early return through
> call layers"

log_011 §4.4:

> "**RECOMMENDATION (family 4):** tag `try_expression` and `try_block`
> with a distinct bucket — provisionally `error-flow` — rather than C
> optionals ... **Confidence: medium.**"

Which the evidence favours, and why: **the recovered ruling, clearly.**
log_011's own confidence was only medium, its stated reservation was
exactly the operand-type problem, and — decisively — its argument was
framed as "not C". The recovered ruling agrees that it is not C. It just
supplies the positive answer log_011 could not find: `choice` +
`function`. log_011's cross-language table (Java, Python, Swift spell
error and absence with disjoint grammar) is fully compatible with the
reduction reading; those three rows argue against C, not against
`choice`. And my 12-language table above is uniform in a way none of the
other two are.

**MY RECOMMENDATION (error flow): take the reduction reading.** Tag
`try_expression` `choice` DUAL `function`, `try_block` `choice` DUAL
`sequence`. Do NOT add an `error-flow` bucket, and do NOT tag either as
C optionals. The `?`-over-`Option` problem that defeated log_011's
recommendation DISAPPEARS under this reading, because `choice` +
`function` is the correct reduction whichever type the operand has —
which is itself a point of evidence for the reduction reading, not just
a convenience.

**Confidence: high.** This is the strongest of the three: an explicit
recovered ruling, a uniform 12-language table, a hub that natively
speaks the destination, and the elimination of the one defect that held
log_011 back.

**What would change it:** (a) the owner ruling that the "Derived (not in the
set)" list was NOT meant to govern `ur_kind` — the list governs
minimum-set MEMBERSHIP, and `ur_kind` is a different vocabulary; if
buckets and set-membership are decoupled, this whole argument weakens on
all three constructs and I would want that ruling before anything is
applied. (b) A consumer that needs "did this program fail" answerable
from `ur_kind` alone. (c) Class-9 exception semantics turning out to be
a live divergence class (log_013 open question 6) — if error handling
diverges at the border, it is a lattice matter and possibly a bucket
matter too.

---

# construct 3 — aliasing / borrowing

## 3.1 what the owner's recovered argument says

`~/Programming/PseudoIR/Tools/intentions/minimum_intention_set.md`,
§"Non-object finding", lines 207–218:

> "ownership / borrowing (Rust)
> NOT an object at any level.
> a dev-time grammar restricting
> aliasing and lifetime (classes
> 2 and 4 of the divergence study).
> the run-time behavior it permits
> is fully expressible in the set;
> what Rust adds is a PROOF about
> that behavior, checked before
> running. lives beside the border
> grammar of PCv7, not in this set."

Characterizing: this is not a derivation, it is a stronger claim — a
category refusal. Sum types and exceptions were ruled DERIVED (they
reduce to objects in the set). Borrowing is ruled NOT AN OBJECT AT ALL,
and RELOCATED to the border grammar. The sentence "what Rust adds is a
PROOF about that behavior" is the same sentence the owner used in framing this
decision for `enum_item`; it is the reduction reading's own engine, and
here it is applied to reach a different destination.

log_013 §3.3 confirms the relocation held: the border grammar travelled
into `pc_intentions.json` as `border_lattice`; the RULING did not.

## 3.2 the 12-language table

Question per row: nearest construct to Rust's `&x` / `&mut x`, what it
reduces to, same reduction as Rust's?

| language | nearest construct (one phrase) | reduces to | same reduction as Rust's? |
| --- | --- | --- | --- |
| Python | nothing — every name is already a reference; no borrow spelling exists | `name` (`minimum_set[1]`), because the reference IS the ordinary case | NOT the same: Rust's `&x` is a marked departure from a value default; Python has no default to depart from |
| Dart | nothing — reference semantics for objects, value for primitives, no borrow spelling | `name` | NOT the same, same reason as Python **[my language knowledge]** |
| Go | `&x` unary, `*T` pointer type; slices alias implicitly | `name` whose value is a location — exactly `minimum_set`'s "Derived" entry for `pointer` | SAME THREE CHARACTERS, DIFFERENT OBJECT. `basis_audit.list.Go` = "cheap:slice-alias-detach" versus `basis_audit.list.Rust` = "native:move". This is the trap row |
| Kotlin | nothing at use sites; JVM reference semantics throughout | `name` | NOT the same **[my language knowledge]** |
| Java | nothing; JVM reference semantics; `final` restricts rebinding, not aliasing | `name` | NOT the same **[my language knowledge]** |
| C# | `ref` / `out` / `in` parameter modifiers, `ref` locals, `Span<T>` | `name` whose value is a location, plus a dev-time restriction on lifetime for `Span` | PARTIALLY the same — `ref struct` lifetime rules are a genuine compile-time aliasing proof, the nearest thing to Rust outside Rust **[UNSURE — I am not confident how far C# `ref struct` escape analysis goes] [my language knowledge]** |
| TypeScript | nothing; JS reference semantics; `readonly` is erased | `name` | NOT the same. `t1_realizations.F.TypeScript`: "fully erased; types vanish at run-time" |
| Swift | `inout` parameter modifier; copy-on-write value semantics elsewhere; newer `borrowing`/`consuming` modifiers | `name` plus a copy elision the compiler performs invisibly | NOT the same shape — Swift's is a parameter modifier, so the same intention lands on a modifier token rather than an expression. `basis_audit.list.Swift` = "cheap:cow-value-copy" |
| Rust | `reference_expression` (`&x`, `&mut x`), `reference_type`, `lifetime`, `mutable_specifier` | `name` whose value is a location, plus a compile-time PROOF about aliasing and lifetime | reference row. `basis_audit.list.Rust` = "native:move" |
| C++ | `reference_declarator` (`T&`), `pointer_declarator` (`T*`), `T&&`, and `std::move` as an ORDINARY FUNCTION CALL | `name` whose value is a location; the move is a library call, so the grammar shows only a call | Type-side SAME, value-side INVISIBLE TO THE GRAMMAR — the same finding log_011 §3.2 predicted |
| Ruby | nothing; everything is a reference; `dup`/`freeze` at run time | `name` | NOT the same **[my language knowledge]** |
| PHP | `&$x` reference assignment and `&` parameter binding; arrays are copy-on-write values | `name` whose value is a location | SAME THREE CHARACTERS as Go and Rust, and a third distinct meaning — PHP's `&` opts INTO reference semantics for a value type. `canon.P9.statement`: "go.slice / php.array as borrows" |

**Reading of the table.** This is the inverse of the error-flow table.
Seven of twelve have NO construct at all, and among the three that spell
it `&` — Go, PHP, Rust — the three characters mean three different
things. There is no uniform reduction to point at; the only thing all
twelve share is `name`, and `name` is so general here that it stops being
informative. This is the construct where the reduction reading's own
machinery produces a dominant object that carries almost nothing.

## 3.3 what each reading implies for `ts_to_ur` and the `kinds` vocabulary

**Reduction reading — worked instance.**

```python
# ts_to_ur/rust.py  — reduction reading
"reference_expression": {"ur_kind": "name"},        # a name whose value is a location
"reference_type":       {"ur_kind": "name"},
"lifetime":             {"ur_kind": None, "note": "dev-time proof grammar, no object"},
```

Characterizing: the third line is where the recovered ruling bites. Under
"NOT an object at any level", `lifetime` has no bucket at all — it is a
proof grammar, and the vocabulary's honest answer is a positive "carries
no object" tag rather than a stretch.

**Guard reading — worked instance.**

```python
# ts_to_ur/rust.py  — guard reading
"reference_expression": {"ur_kind": "borrow"},
"lifetime":             {"ur_kind": "borrow"},
```

```python
# ts_to_ur/go.py  — guard reading, language two  [Go]
"unary_expression@&":   {"ur_kind": "name"},   # NOT borrow: Go's & has no proof
```

Characterizing: the fence here is doing MORE work than in either other
construct, because the false merge is invited by three literal
characters rather than by a word, and it is invited by two other
languages rather than one.

**Hub-side illustration.** Rust's `fn f(v: &mut Vec<u32>) { v.push(1); }`
called as `f(&mut xs);` becomes, in the hub:

```python
# hub, spelled out
def f(v):        # v is an ordinary Python name bound to the same list object
    v.append(1)
f(xs)            # no marker survives; Python has no borrow spelling
```

Characterizing: four lines, and the `&mut` is GONE. Not lowered —
absent. The proof had nothing to lower to. This is the clearest hub-side
demonstration of the recovered ruling's "NOT an object at any level".

## 3.4 the ingress-only argument, applied

| reading | what ingress-only BUYS it | what ingress-only COSTS it |
| --- | --- | --- |
| reduction | The hub confirms it: the borrow vanishes at ingress with nothing lost at run time, exactly as "the run-time behavior it permits is fully expressible in the set" predicts. Under ingress-only, the proof's disappearance costs nothing, because there is no egress that would have to reconstruct it | It tags `&mut v` as `name`, which is true and uninformative. `border_lattice` class 2's "incompatible" verdict (`spelling`: null) becomes invisible in the tag stream — but see below on whether that matters under ingress-only |
| guard | A `borrow` bucket would keep the one construct the lattice says cannot cross a border visible at the neutral layer | Under ingress-only, border crossings are an EGRESS concern. The lattice's incompatible verdict is about "aliasing is load-bearing across the border" — a crossing that ingress-only never performs. So the guard's strongest evidence, the class-2 verdict, is evidence about a situation PCv5 does not currently reach |

Characterizing: this is the largest swing the ingress-only fact produces
anywhere in this brief. log_011's family-3b recommendation rested almost
entirely on `border_lattice` class 2's "incompatible" verdict, and under
ingress-only that verdict is about a boundary that is not being crossed.
I want to be careful not to overclaim: the verdict is still TRUE, and a
future PCv7 border grammar will need it. But it is stored in
`border_lattice`, where the recovered ruling deliberately put it, and it
is readable there.

## 3.5 RECOMMENDATION — aliasing / borrowing

the owner's recovered ruling (lines 207–218, quoted in full at §3.1):

> "ownership / borrowing (Rust) NOT an object at any level. ... lives
> beside the border grammar of PCv7, not in this set."

log_011 §3.4:

> "(3b) Value-side — do NOT tag `reference_expression` as `name`. Give
> it a distinct provisional bucket (`borrow`), on the strength of
> `border_lattice` class 2's "incompatible" verdict. **Confidence:
> medium** on the placement, **high** on the negative claim that `name`
> is wrong."

Which the evidence favours, and why: **the recovered ruling on
PLACEMENT; log_011 on the specific danger of the Go and PHP rows.**
log_011 itself guessed the ruling's content before finding it —
log_013 §3.2 quotes log_011 §G3: "I lean toward the first reading being
the intended one (a border property is a different kind of thing from an
intention), which is why family 3's recommendation is medium rather than
high." Characterizing: log_011's own hedge was pointed at exactly the
ruling that has now surfaced, and log_013 §"open questions" item 2 draws
the consequence — A4 "is an argument AGAINST log_011's proposed `borrow`
bucket at the intention tier, not for it."

But the 12-language table above is the one place where I do not think the
recovered ruling settles everything. It settles that borrowing is not an
INTENTION. It does not settle what `ur_kind` should write on
`reference_expression`, because `ur_kind` must write something and `name`
is the merge that Go's `&x` and PHP's `&$x` will follow.

**MY RECOMMENDATION (aliasing/borrowing): take the reduction reading for
the tier question and the guard reading for the tag.** Concretely: do NOT
add `borrow` as a minimum-set-tier or category-tier bucket — the
recovered ruling forecloses that, and ingress-only removes the evidence
log_011 leaned on. DO refuse `name` on `reference_expression`, and give
it a positive non-object marking instead — a tag whose meaning is
"classified; carries a dev-time proof grammar, not an object", the same
marking `lifetime` gets. That is not a 22nd intention bucket; it is the
vocabulary's way of saying what the audit verdict already said ("One
non-object identified (static proof grammars)").

**Confidence: medium.** Higher (medium-high) on the negative half — no
`borrow` bucket at intention tier, because the recovered ruling is
explicit and ingress-only guts the counter-evidence. Lower (medium) on
the positive half, because "a positive non-object tag" is a shape the
vocabulary does not yet have, and log_008's `declarative-form` proposal
is the nearest existing candidate and was proposed for trivia, not for
proof grammars.

**What would change it:** (a) the owner ruling on whether `ur_kind` may carry
a NON-OBJECT tag at all — if every node must land in one of the 21
buckets, my split recommendation is unavailable and I would fall back to
`name` with a mapper note, reluctantly. (b) c/cpp ingest: if C++'s
`std::move` is invisible to the grammar as I expect, that is the
strongest evidence that this intention cannot be carried by `ur_kind`
and belongs to the ledger, which strengthens the recommendation. (c) Any
sign that PCv5 will not stay ingress-only — the moment egress is in
scope, `border_lattice` class 2 becomes live and log_011's argument
recovers its full force. (d) the owner ruling that the "Non-object finding"
was scoped to the minimum set only and says nothing about `ur_kind`.

---

# summary

| construct | reduction reading says | guard reading says | RECOMMENDATION | confidence |
| --- | --- | --- | --- | --- |
| sum types | `record` + `choice` on the tag; the record is dominant because it holds even the states the sum forbids; Rust adds a proof, not behaviour. Nine of twelve languages reduce the same way | `sum` as a distinct bucket, because Java's, C#'s and PHP's `enum` reduce differently and share the word, pre-authorising a bad merge at language two | Reduction reading. `enum_item` -> `record` DUAL `choice`; no `sum` bucket; the closed-set fact recorded as a mapper note | medium-high |
| error flow | `choice` + `function`'s return half — "choice + early return through call layers", verbatim from the recovered audit. All twelve reduce identically | `error-flow` as a distinct bucket, because Java, Python and Swift spell error and absence with disjoint grammar | Reduction reading. `try_expression` -> `choice` DUAL `function`; no `error-flow` bucket; not C either. The `?`-over-`Option` defect disappears | high |
| aliasing / borrowing | NOT an object at any level; a dev-time proof grammar; relocated to the border grammar. Seven of twelve languages have no construct at all | `borrow` as a distinct bucket, because Go's `&x`, PHP's `&$x` and Rust's `&x` are three characters with three meanings | Split. No `borrow` bucket at intention tier (reduction reading wins the tier question); but refuse `name` and use a positive non-object tag (guard reading wins the tag question) | medium |

**The single most decision-relevant row in this brief**, extracted from
§2.2 because it is the one row that decides a construct on its own:

| language | nearest construct | reduces to | same as Rust's? |
| --- | --- | --- | --- |
| Go | `if err != nil { return ..., err }` written by hand at every call site | choice + early return through call layers — WRITTEN OUT, no sugar | SAME reduction as Rust's, and Go is the row that proves the reduction, because Go's spelling IS the reduction |

Characterizing: Go writes the derivation out longhand. Rust's `?` and
Go's four-line idiom are the same two objects with different amounts of
sugar over them, and that is visible without any semantic analysis or
appeal to my own language knowledge — it is what the source text says.
No comparable row exists for the other two constructs.

---

## open questions for the owner

1. **Does the "Derived (not in the set)" list govern `ur_kind` at all?**
   The list governs membership of the ELEVEN. `ur_kind` is a different
   vocabulary with a different job (totality against `node-types.json`).
   This brief assumes the reductions carry across. If they do not, all
   three recommendations weaken at once and the guard reading gains
   across the board. This is the single question upstream of everything
   here and I would want it answered first.

2. **Exclusive or primary-plus-dual?** log_008 open question 1. Two of
   my three recommendations put the guard in the DUAL slot. If a node
   carries exactly one bucket, the sum-types recommendation flips to
   log_011's and the error-flow one weakens.

3. **May `ur_kind` carry a positive NON-OBJECT tag?** Needed by the
   aliasing recommendation, and also by `lifetime`, `empty_statement`
   and `parenthesized_expression` (log_011 §5.2 candidate C). The
   recovered audit verdict names a category — "static proof grammars" —
   that the vocabulary currently cannot express.

4. **Is a MAPPER NOTE a durable artefact?** Both my reduction-reading
   recommendations move information out of the bucket and into the
   per-language mapper's justification. That is only safe if mapper
   notes are recorded, greppable and reviewed at language two. If they
   are informal, the guard reading is right for the boring reason that
   only buckets survive.

5. **Does ingress-only hold for the life of `ur_kind`?** §3.4 shows the
   fact swinging the aliasing decision by itself. If egress is even
   possible later, `border_lattice` class 2 becomes live and log_011's
   `borrow` bucket recovers its strongest argument. The vocabulary is
   append-only in spirit, so adding `borrow` later is cheap; UNMERGING
   `name` later is not. That asymmetry is worth weighing against my own
   recommendation.

6. **Is PHP's enum, and C#'s `ref struct`, as I have them?** Two rows in
   this brief are marked **[UNSURE]** and both could move a table's
   count by one. Neither changes a recommendation on its own.

7. **Should the derived list and the non-object finding become data?**
   Carried forward unchanged from log_013 open question 4. This brief is
   the second document in two days to depend on prose recoverable only
   from PCv5 git.

---

## sources

- `~/Programming/PseudoIR/Tools/intentions/minimum_intention_set.md` —
  the recovered six-section argument; §"The set", §"Derived (not in the
  set)" (lines 105–107), §"Audit" (lines 140–144, 161–165, 183–185),
  §"Non-object finding" (lines 207–218), §"Audit verdict" (lines
  222–227). All quotations verbatim.
- `~/Programming/PseudoIR/Tools/intentions/pc_intentions.json` —
  `languages`, `minimum_set`, `intent_categories`, `t1_realizations`,
  `row_satisfiers`, `basis_audit`, `border_lattice`, `canon`. Cited by
  field path throughout.
- `~/Programming/PseudoCoup_v5/DevComms/log_011_uncertain_families_evidence.md`
  — families 2, 3b and 4, and their recommendations, quoted in §1.5,
  §2.5, §3.5.
- `~/Programming/PseudoCoup_v5/DevComms/log_013_intentions_gap_history.md`
  — the recovered rulings S1, E5, A4 and their dating.
- `~/Programming/PseudoCoup_v5/DevComms/log_006_ur_kinds_vocabulary.md` —
  item 3 (the owner's intent-dominance quote), item 4 (merges judged on
  grammar facts, never name resemblance), item 5 (the mechanical seed).
- `~/Programming/PseudoCoup_v5/DevComms/log_008_kinds_coarse_tagging_draft.md`
  — the 21 buckets, the two PROPOSED buckets, open question 1.
- `~/Programming/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_2_ts_to_ur/CORE_0_0_0_2_ts_to_ur.md`
  — read only, for the per-language mapper shape ("the mappers are
  per-language").
- My own knowledge of the grammars of the twelve, marked **[my language
  knowledge]** at every point of use, and never used alone to support a
  merge.
