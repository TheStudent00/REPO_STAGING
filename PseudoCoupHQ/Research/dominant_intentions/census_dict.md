# feature census — dict (the last seed object)

2026-08-13, hand-drafted in the owner format under the standing
rules (guarantees; record-both modes; origin naming; staged
mutability). Fresh work. EVERY FACT UNVERIFIED — harness work
order.

Scope note: "dict" is the keyed container (Python naming).
typescript/js has a SPLIT PERSONALITY here — the plain object
(string keys only, keys silently coerced to strings) and Map (any
keys, by identity). Both are in scope, recorded as two columns of
one language; record-both applies.

---

## structure facts — FRACTURED (twice, plus one anti-guarantee)

**F-d1 — what a key may be.**

- **anything hashable/equatable**: python (by __hash__/__eq__),
  ruby, js Map (by object identity), java, kotlin, csharp, dart;
  rust (K: Hash+Eq, declared), go (comparable K, declared), cpp
  (declared + hash provided).
- **strings (and ints) only**: php; js PLAIN OBJECT — and js
  coerces silently (`obj[1]` and `obj["1"]` are the same slot),
  a guarantee with teeth.

**F-d2 — whether iteration order is promised.**

- **insertion order guaranteed**: python (3.7+), ruby, php,
  js Map, dart (default), kotlin (default LinkedHashMap).
- **explicitly NOT promised**: rust HashMap, java HashMap
  (LinkedHashMap is the opt-in), csharp Dictionary (order
  unspecified), cpp unordered_map.
- **actively RANDOMIZED**: go — iteration order is deliberately
  shuffled per run so programs cannot accidentally rely on it.
  An ANTI-GUARANTEE: a promise OF unpredictability, the census's
  first. (js plain object: insertion order EXCEPT integer-like
  keys iterate first in numeric order — the weird cousin;
  recorded as its own row.)

## operation facts

Universal candidates (believed 11/11):

- insert, overwrite-on-duplicate-key (last write wins), delete,
  membership test, length — all present, same meaning.
- value read by an EXISTING key answers the value.

Fractures (dict's own — all guarantees):

- **F-d3 — reading a MISSING key.** Four camps, the widest
  operation fracture in the census:
  - throw: python (KeyError), csharp (indexer throws).
  - answer a nothing-value: ruby (nil), js/ts (undefined),
    kotlin (null), dart (null), java (null — with the null-value
    ambiguity that forces containsKey), php (null + notice).
  - answer the ZERO VALUE of the value type, plus an ok flag as
    the idiom: go (`v, ok := m[k]`).
  - INSERT a default and answer it: cpp `operator[]` — reading
    creates the key. (cpp `.at()` throws — both exist,
    per-spelling guarantees, origin-named: `.cpp_bracket` vs
    `.cpp_at`.)
  - rust: panic on index, Option via .get — both, per-spelling.
- **F-d4 — deleting while iterating.**
  - error/undefined: python (RuntimeError), java
    (ConcurrentModificationException), rust (borrow rules forbid
    it at compile time), csharp (throws).
  - explicitly ALLOWED: go (delete during range is defined and
    safe).
  - tolerated with caveats: ruby, php, js Map (spec'd behavior).
- **F-d5 — key equality fine print**: js Map keys by identity
  (two equal-content objects are different keys) vs python/ruby
  by value-equality; NaN-as-key retrievable in js Map
  (SameValueZero) but a trap in python. Edge rows; vectors
  cheap; billed here, not to the border, because the dict OWNS
  its key-matching rule.

## assignment and sharing

Inherits list's F-l9 wholesale: share (eight languages) /
copy-on-assign (php, **cpp** — measured `1` on the vector,
carried here by the same fact) / move (rust). Same camps, same
staged ruling, one line because it is the same fact. (measured,
log_020 run 2026-08-14; ruled by the owner 2026-08-14)

## border facts — filed away

- **→ the php impostor, RESOLVED here**: php's array is ONE
  structure serving both the list page and this one — an ordered
  hash with integer-and-string keys. Under the dominant, that is
  simply... a dict with insertion order and integer keys, which
  the dominant dict already IS. php's array ingresses as the
  dominant dict wearing a list view — the owner's dict-list instinct
  from the container discussion, arriving as the natural
  resolution rather than an invention.
- **→ (dict, record/object)**: js objects double as records;
  billed to the record page when/if the census extends there.
- **→ (dict, json/serialization)**: conversion machinery.

## reading — dominance analysis, and the seed-tier close

- the dominant dict is insertion-ordered, any-key,
  reference-semantics — python's dict IS this costume, nearly
  exactly — with origin-named variants for the camps:
  `.go_get` (zero-value + ok), `.cpp_bracket` (insert-on-read),
  `.java_get` (null-with-containsKey), js-object string-coercion
  as an ingress mapping fact.
- **go's anti-guarantee is the elegant case**: a correct go
  program CANNOT rely on iteration order, so the dominant's
  order promise is a strict superset — unused, therefore inert,
  therefore free. The dominant may keep order for everyone;
  go-origin programs simply never observe it. the owner's inertness
  principle closing its own loop.
- **residue check: EMPTY.** cpp's insert-on-read, js's key
  coercion, go's randomization — all guarantees, all modeled,
  all origin-named. Nothing on this page contradicts.

## seed tier complete — the phase-2 conclusion

Five pages (boolean, float, integer, string, list, dict — six
objects, five files): fractures are near-always guarantees;
guarantees never contradict; the two apparent hard cases closed
by rulings (overflow: two adds + origin intent; mutability:
staged, origin+intent determines mode); the residue is empty.
Dominance over the basic tier is: ONE mechanical table of
guarantees, a set of origin-named variant operations, the
pay-per-feature representation principle, and the staged sharing
plan. Zero contradictions found. The harness (phase 1) now has
its complete work order: verify every fact on these five pages by
execution, and the verified table IS the basic tier of the
dominant-intentions basis.

---

## layer-3 findings, folded back 2026-08-19

Everything above was hand-drafted 2026-08-13 and marked UNVERIFIED:
the page was the harness's work order, and the last line above says so.
The layer-3 campaign has since run — logs 024 through 037 in
`PseudoCoupHQ/DevComms/`. This section carries what
those runs PROVED that the sections above do not already say. Nothing
stated above is repeated here.

Each item names the log and section it comes from, and its level.
**Measured** means a number a run printed. **Derived** means a number
worked out from measured numbers.

### the words this section uses

```
probe
    one small generated program that asks one
    language one question.
    example tied to context:
        `{'a':1}[0]` in python is one probe.

holder
    the typed slot a value is put into before
    an operation is applied to it.  one census
    camp can own several holders.
    example tied to context:
        python's `dict`, `OrderedDict` and
        `SimpleNamespace` are three holders
        this section separates.

form
    the census-level kind of a value, above
    the holder: keyed, sequence, text, whole,
    truth, fractional, nesting, nothing.
    example tied to context:
        `dict` and `OrderedDict` are two
        holders of ONE form, keyed.

subscript
    the `[ ]` operation: reading a position or
    a name out of a container.
    example tied to context:
        `{'a':1}[0]` raises a missing-key
        complaint and `[1,2,3]['a']` raises a
        type complaint — one token, two
        refusal kinds.
```

### the php impostor, RESOLVED here — now with the measurement

The page resolves php's array as a dict wearing a list view, and calls
that resolution natural rather than invented. The run that proves it is
an operation, not a structure claim.

- On `+ sequence|base | sequence|strs`, python and ruby concatenate and
  answer `sequence:[1,2,3,'a','b']`. Php answers `sequence:[1,2,3]` —
  the LEFT operand — because php's `+` on arrays is a union by KEY, and
  the right operand's entries are discarded wherever the keys collide.
  *(measured, log_031 §5.4)*
- Read the two sides against each other:
  - **The list-page reading**: php's `+` looks like a broken
    concatenation.
  - **The dict-page reading, which is the correct one**: php's `+` is
    not concatenation at all. It is the keyed union, behaving exactly
    as a keyed container's merge should, and the collision rule
    (existing key wins) is its stated guarantee.
- This page's resolution is therefore measured rather than argued: the
  operation php's array carries is the DICT's operation, so the object
  is a dict.

### keyed merge is an operation the dominant needs, and python does not have it

- Python's `dict + dict` raises `TypeError` — the keyed grouping has no
  `+` at all. *(measured, log_024 §4 item 1)*
- Php's `+` on the same form is the key union above. *(measured,
  log_031 §5.4)*
- The page's operation universals list insert, overwrite, delete,
  membership, length and read-by-existing-key. **Merge is not on that
  list and it is not universal**: one language spells it `+`, one
  refuses `+` entirely. Under the page's own origin-naming rule this is
  a `.php_plus` variant with a stated collision guarantee, which costs
  the dominant nothing — but it is a row the page is missing.

### F-d3 (reading a missing key) — the refusal KIND is itself a finding

The page's F-d3 sorts languages by what a missing key produces. The
runs found the distinction one level finer, inside python, and it is
about which complaint arrives. *(measured, log_024 §4 item 4)*

- **The keyed grouping refuses with a MISSING-KEY complaint**:
  `{'a':1}[0]` raises `KeyError`, not `TypeError`.
- **The ordered container refuses with a TYPE complaint**:
  `[1,2,3]['a']` raises `TypeError`.
- The reason matters to F-d1: **a whole number is a perfectly good key
  that simply is not present.** Python's dict did not reject the KIND
  of the index. It looked it up and did not find it. So python belongs
  in F-d1's "anything hashable" camp for a reason the run can show,
  rather than by assertion.
- `{'a':1}['absent']` also raises `KeyError`, which is the page's
  throw-camp row confirmed. *(measured, log_024 §4 item 4)*

### F-d5 (key equality fine print) — holders of one form do not all agree

- `dict == OrderedDict` is True. *(measured, log_024 §4 item 7)*
- `dict == SimpleNamespace` is False. *(measured, log_024 §4 item 7)*
- The page bills key-matching to the dict because the dict OWNS its
  rule. This adds the container-level twin of that fact: whether two
  keyed HOLDERS inside one language compare equal is also the dict's
  own rule, and python answers it differently for two holders that both
  hold names bound to values.

### iteration — a `for` over a keyed grouping visits the KEYS

- Over a python `dict`, a `for` collects `['a', 'b', 'c']` — the keys,
  not the values. Over a `SimpleNamespace` it raises `TypeError`.
  *(measured, log_024 §4 item 9)*
- The page's F-d2 asks whether iteration ORDER is promised. This is the
  prior question F-d2 assumes and the page never states: **what
  iteration yields.** Python's choice of keys is a choice, and the page
  is right that other languages did not all make it — but the page has
  no row recording that the choice exists.

### keyed values in the if-condition slot, across twelve languages

- **Python and php split a keyed value by value** — empty goes to the
  else arm. **Ruby and typescript send every keyed value to the then
  arm.** **C++ flatly REFUSES** a keyed value in a condition: a
  `std::map` has no conversion to bool, and this is the one form where
  c++ refuses outright while accepting whole and fractional.
  *(measured, log_037 §4)* The remaining seven languages refuse it
  along with everything else that is not a boolean.
- A border fact, billed to `choice` per the format ruling. It is
  recorded here because the c++ row is the sharpest evidence that
  coercion-to-bool is a per-STRUCTURE decision inside a language, not a
  per-language camp — which is the reading the boolean page's border
  ledger wanted and could not measure.
