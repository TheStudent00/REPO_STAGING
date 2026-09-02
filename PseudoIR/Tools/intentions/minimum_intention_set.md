<!-- RECOVERED 2026-08-05 from PseudoCoup_v5 git history
     (`git show 7efb6e6:Designing/minimum_intention_set.md`),
     at the owner's green light, after log_013 found that the
     2026-07-28 copy-forward took only "The set" section:
     the conclusion travelled, the argument did not. This file
     restores the full six-section argument beside the data
     (`intentions_data.py`) so they never separate again.
     Historical content below is verbatim and unedited. -->

# Minimum Intention Set

Question: what is the minimum set of objects
(low level to high level) which would satisfy
all intentions a developer expresses through
any of the 12 PseudoCoup languages?

Scope: the 12. Python, Dart, Go, Kotlin,
Java, C#, TypeScript, Swift, Rust, C++,
Ruby, PHP.

Rule for this document: entries earn their
place by being underivable from the others.
Anything derivable is listed as derived, or
left out.

---

## The set

```
1. value
	number, boolean, byte, text

2. name
	a binding from a written identifier
	to a value

3. operation
	arithmetic, comparison, logic
	on values

4. sequence
	do this, then that

5. choice
	if

6. repetition
	while

7. function
	a parameterized block; call and
	return. a function IS a value:
	it can be named, passed, stored.
	(amendment from the audit below —
	 callbacks, events, comparators
	 are inexpressible otherwise)

8. record
	values grouped under named fields

9. collection
	list (ordered many)
	map (keyed many)

10. mutation
	assignment to a name or field
	after creation

11. service call
	request to the platform:
	read, write, clock, display,
	network, spawn executor
```

---

## Why the set stops here

Items 1-10 are computation. Theory says this
list is already generous: sequence + choice +
repetition express any control flow
(Bohm-Jacopini), and function alone is
Turing-complete (lambda calculus). Items are
kept anyway when removing them would force
unreadable encodings. "Minimum" here means
minimum for expressing intent, not minimum
for a proof.

Item 11 is not computation and not derivable
from 1-10. No arrangement of pure computation
produces a pixel or reads a file. Services
must be primitive.

---

## Derived (not in the set)

```
class
	record + functions + dispatch

module
	record of names, at file scale

exception
	choice + early return through
	call layers

iterator / for-each
	repetition + function

closure
	function + record (captured names)

pointer
	name whose value is a location
	(requires the flat-memory service
	 or a collection to index into)
```

---

## Relation to the divergence study

Every language in the 12 offers spellings of
this same set. A language "enabling an
intention" means: it gives a short spelling
for some composite of these objects. The
divergence classes live in items 3, 10, 9,
and 11 — where identical spellings compute
different results. See
language_divergence_study_log.md.

---

## Audit: the 12 languages' signature
## intentions, derived

Each entry: the feature people choose the
language for, and its composite. A feature
survives the audit if its derivation is a
known compiler technique, not hand-waving.

```
async/await, coroutines, generators
	(C#, Kotlin, Dart, Python, JS/TS)
	= function + record + choice.
	a paused function is a record
	holding its position and locals;
	resume is a call that reads it.
	this is literally how C#/Kotlin
	compilers implement it
	(state-machine transform).

channels, goroutines (Go)
	= collection (queue) + mutation
	+ service call (spawn executor).
	blocking = the scheduler service.

optionals, null safety
	(Swift, Kotlin, TS, Rust)
	= record with a tag field
	+ choice on the tag.

pattern matching (Rust, Swift, C#)
	= choice + record field access.

interfaces, traits, protocols
	(Java, Go, Rust, Swift)
	= dispatch. dispatch itself
	= map from type to function
	+ function-as-value. derived,
	given amendment to item 7.

generics, templates (Java, C++, Rust)
	= dev-time only. a generic
	function is one function checked
	against many declared types;
	types die at compile-time.
	no run-time object needed.

defer (Go), RAII (C++), using (C#)
	= sequence + choice, same
	derivation as exception.

events, delegates, callbacks
	(C#, JS/TS)
	= collection of function-values
	+ repetition (call each).

operator overloading (C++, Python)
	= function + dispatch. spelling
	sugar over a call.

metaprogramming, reflection
	(Ruby, Python, Java)
	= names stored as a map from
	text to value. expressible,
	but run-time self-modification
	is discipline-forbidden; only
	the read side survives.
```

## Non-object finding

```
ownership / borrowing (Rust)
	NOT an object at any level.
	a dev-time grammar restricting
	aliasing and lifetime (classes
	2 and 4 of the divergence study).
	the run-time behavior it permits
	is fully expressible in the set;
	what Rust adds is a PROOF about
	that behavior, checked before
	running. lives beside the border
	grammar of PCv7, not in this set.
```

## Audit verdict

No 12th object found. One amendment
(function IS a value, item 7). One
non-object identified (static proof
grammars). The 11 stand, pending the
services-grain question.

## Open

- is 11 the right grain for services, or
  does it split (file / display / network /
  executor as separate primitives)?
- second audit pass wanted: per-language
  standard libraries (not just language
  features) — do any library intentions
  escape the set? (suspect: no — libraries
  are composites by construction.)
