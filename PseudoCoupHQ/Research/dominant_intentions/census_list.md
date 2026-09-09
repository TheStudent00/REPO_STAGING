# feature census — list (where sharing arrives in force)

2026-08-13, hand-drafted in the owner format under the standing
rules (guarantees; record-both modes; origin naming; staged
mutability). Fresh work. EVERY FACT UNVERIFIED — harness work
order.

Scope note: "list" here is the growable ordered container (Python
naming). Languages that ALSO have fixed-size arrays (java, go,
rust, cpp) contribute their growable object (ArrayList, slice,
Vec, vector); the fixed array is a co-object noted where it leaks
into the growable one's behavior.

---

## structure facts — FRACTURED (three ways)

**F-l1 — what the elements may be.**

- **one declared type**: rust (Vec<T>), go ([]T), java
  (List<T>), csharp, kotlin, dart, cpp, typescript (T[] under
  the type checker).
- **anything, mixed freely**: python, ruby, php (and typescript
  at runtime — its discipline is compile-time only, a
  mode-flavored fact: record both faces).

**F-l2 — what the container fundamentally IS.**

- a growable buffer of values/references: python, ruby, java,
  csharp, go, rust, kotlin, cpp, dart.
- an ordered hash wearing list syntax: php (the impostor,
  carried from the basis brainstorm).
- an object with integer-named properties: typescript/js —
  which is why HOLES are possible (`[1, , 3]`, sparse arrays) —
  no other language's list can have a missing middle.

**F-l3 — capacity model**: all growable (in scope by
construction); go's slice is a WINDOW onto a shared backing
array — structure fact with operation consequences (F-l6).

## operation facts

Universal candidates (believed 11/11):

- append/push at the end exists and preserves order.
- indexed read of an existing position answers the element.
- iteration visits elements in index order.
- length answers the element count (no unit ambiguity here —
  the one mercy lists have over strings).

Fractures (list's own — all guarantees):

- **F-l4 — reading past the end.**
  - throw/panic: python (IndexError), java, csharp, kotlin,
    dart, rust (panic), go (panic).
  - answer a nothing-value: ruby (nil), typescript/js
    (undefined), php (null + notice).
  - undefined behavior: cpp `[]` (while `.at()` throws — BOTH
    exist, per-spelling guarantees, origin-named cheaply).
- **F-l5 — negative indexing**: python and ruby count from the
  end (`a[-1]`); everyone else refuses or misbehaves. A view,
  cheap, origin-named if kept.
- **F-l6 — what slicing answers.**
  - a COPY: python, ruby, js/ts (.slice), kotlin, dart, csharp,
    **php, cpp** (both measured `1` — editing the slice/subrange
    does not touch the original). (measured, log_020 run
    2026-08-14; ruled by the owner 2026-08-14)
  - a WINDOW sharing storage: go (slice of a slice edits the
    same cells), rust (&[a..b] — a borrow, compiler-supervised),
    **java** (`subList` is a view; measured `99` — editing through
    it is visible in the original). (measured, log_020 run
    2026-08-14; ruled by the owner 2026-08-14)
  - the sharing camp is a guarantee with sharp consequences:
    editing through the window is VISIBLE through the original.
    Files under the staged-mutability ruling.
- **F-l7 — what `==` does between lists.**
  - content: python, ruby, kotlin, rust, php, **cpp** (measured
    `true` on vectors). (measured, log_020 run 2026-08-14; ruled
    by the owner 2026-08-14)
  - identity: java (== on references; .equals is content), js/ts,
    dart, csharp (SequenceEqual for content).
  - not comparable at all: go (slices refuse ==; only nil-check).
  - origin naming applies (.java_equals precedent extends).
- **F-l8 — sort: in place or copy, and the default order.**
  - in place: python (.sort; sorted() copies — both exist),
    ruby (.sort! vs .sort), js/ts (in place, and the default
    order is LEXICOGRAPHIC even for numbers — [10,9,1] sorts to
    [1,10,9] — the census's single most surprising guarantee),
    java (Collections.sort), go, rust, cpp, dart, csharp.
  - record-both applies where a language ships both spellings.

## assignment and sharing — the staged-mutability workout

**F-l9 — what `b = a` means for a list.** THREE camps:

- **share the object**: python, ruby, java, kotlin, csharp,
  dart, js/ts, go (the slice header copies but the backing
  array is shared — window semantics again).
- **copy the value**: php — assignment copies the whole array
  (copy-on-write under the hood; observably a copy). **cpp** joins
  this camp (measured `1` — `b = a` copies the vector; carries to
  dict's F-l9-dict the same way). (measured, log_020 run
  2026-08-14; ruled by the owner 2026-08-14)
- **move**: rust — `b = a` ENDS a's usability; the compiler
  enforces single ownership. A third semantics entirely, and
  still a guarantee, readable at ingress.

Per the staged ruling: the ledger records origin intent
(share/copy/move) per assignment; PCv5 approximates by polyfill;
v6/v7 get native treatment via slices. Nothing here blocks
dominance — but F-l9 is the single richest source of test
vectors so far (edit-through-one-name-read-through-another, in
three camps).

## border facts — filed away

- **→ (list, string)**: join/split — conversion machinery.
- **→ (list, dict)**: php's impostor makes its "list" page and
  its dict page one object — resolved on dict's page.
- **→ (list, pattern/destructuring)**: billed to D/pattern
  machinery.

## reading — dominance analysis

- the dominant list is REFERENCE-semantics with mixed elements
  (the union costume: python's list), carrying origin-named
  variant operations for the guarantee camps: `.cpp_at` vs raw
  index, `.go_slice` window vs copy slice, `.rust_move` vs
  share-assign, `.php_assign` copy — the pay-per-feature
  principle covers the cost (a program never using windows never
  builds the aliasing machinery).
- js/ts sparse holes and lexicographic sort are guarantees too —
  ugly ones, but computable, so modeled not fought.
- the genuinely-hard residue REMAINS EMPTY after four pages:
  everything found is a guarantee or files under staged
  mutability. dict is the last seed object; if it holds, the
  phase-2 conclusion is: dominance is a mechanical table +
  origin-named variants + the staged sharing plan, with zero
  contradictions.

---

## layer-3 findings, folded back 2026-08-19

Everything above was hand-drafted 2026-08-13 and marked UNVERIFIED:
the page was the harness's work order. The layer-3 campaign has since
run — logs 024 through 037 in
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
        `[1,2,3] + ['a','b']` in python, ruby
        and php is three probes.

holder
    the typed slot a value is put into before
    an operation is applied to it.  one census
    camp can own several holders.
    example tied to context:
        python's `list`, `tuple` and `deque`
        are three holders of the ordered
        container.

form
    the census-level kind of a value, above
    the holder: sequence, keyed, text, whole,
    truth, fractional, nesting, nothing.
    example tied to context:
        `list` and `tuple` are two holders of
        ONE form, sequence.

subscript
    the `[ ]` operation: reading a position or
    a name out of a container.
    example tied to context:
        `[1,2,3][0]` and `{'a':1}['a']` are
        the same token doing two jobs.
```

### F-l2 — php's `+` is a union by KEY, measured

The page calls php's array "the impostor" carried from the basis
brainstorm. Here is the run that shows the impostor at work, on
`+ sequence|base | sequence|strs` *(measured, log_031 §5.4)*:

```
python  sequence:[1,2,3,'a','b']
ruby    sequence:[1,2,3,'a','b']
        keyed:{1,2,3,'a','b'}
php     sequence:[1,2,3]
```

- **Python and ruby concatenate.** Both answer the five-element joined
  sequence.
- **Php answers the LEFT OPERAND.** Php's `+` on arrays is a union by
  key, so the right operand's entries are discarded wherever the keys
  collide — and for two positionally-keyed arrays, every key collides.
  *(measured, log_031 §5.4)*
- This promotes the page's F-l2 reading from an analogy to a
  measurement: php's list is not a list that behaves oddly under `+`,
  it is a keyed container whose `+` is the keyed operation. The dict
  page's resolution of the impostor is the correct filing, and this is
  the evidence for it.
- Ruby's second token is its `Set` holder answering the same input as a
  keyed grouping. *(measured, log_031 §5.4)* One form, two holders, two
  answer kinds — the same holder lesson the string page's e-acute
  finding carries.

### F-l4 (reading past the end) — the two refusal KINDS are different, and the difference is meaningful

The page's F-l4 sorts languages by whether they throw. The runs found a
distinction one level finer, inside python. *(measured, log_024 §4 item
4)*

- **A sequence given a name index refuses with a TYPE complaint**:
  `[1,2,3]['a']` raises `TypeError`.
- **A keyed grouping given a position index refuses with a MISSING-KEY
  complaint**: `{'a':1}[0]` raises `KeyError`.
- The reason is worth carrying: a whole number is a perfectly good key
  that simply is not present. The keyed container did not reject the
  KIND of the index; it looked the index up and did not find it.
- Consequence for the dominant: "refuses" is not one answer. An ingress
  that records only "raised" loses which of the two happened, and the
  two mean different things about the program that ran.

### F-l4 — the index kinds that are not whole numbers

All python, all *(measured, log_024 §4 item 5)*:

| index | answer | what it says |
|---|---|---|
| `[1,2,3][True]` | `int:2` | the truth costume again — True indexes as 1 |
| `[1,2,3][1.5]` | `<raise:TypeError>` | a fractional is not an index |
| `[1,2,3][9223372036854775807]` | `<raise:IndexError>` | a RANGE complaint, not a WIDTH complaint |

- The last row is the one the page has no place for. Python's whole
  number has no width, so an out-of-range index is out of the
  CONTAINER's range rather than out of the index type's range. In a
  fixed-width language the same probe can fail for the other reason,
  and the two failures are not the same fact.

### F-l7 (`==` between lists) — python's containers do not agree across holders, though its numbers do

- `list == tuple` is False. `list == deque` is False. *(measured,
  log_024 §4 item 7)*
- `bytes == bytearray` is True, and `dict == OrderedDict` is True.
  *(measured, log_024 §4 item 7)*
- Against that: `int 42 == Decimal 42 == Fraction 42 == c_int64 42` are
  all True. *(measured, log_024 §4 item 7)*
- The page's F-l7 asks whether `==` compares content or identity ACROSS
  languages. This is a third axis it does not have: whether `==`
  compares content across HOLDERS of one form, inside one language.
  Python answers yes for numbers and mostly no for containers, and the
  exceptions are not obviously principled.

### the `*` and `+` tokens do different jobs on a sequence

- `[1,2,3] * 42` answers a 126-element list — repetition, not
  multiplication. `"hello" * 42` repeats the text. `42 * 42` is
  `int:1764`. `list * list` raises `TypeError`. *(measured, log_024 §4
  item 10)*
- The page's operation universals list append, indexed read, iteration
  and length. Repetition is a fifth operation the ordered container
  owns in some languages, it is spelled with an arithmetic token, and
  it has no row above.

### iteration — what a `for` actually collects

- Over a python `list`, `[1, 2, 3]`. Over a `frozenset`, `[1, 2, 3]`.
  Over a `dict`, `['a', 'b', 'c']` — the KEYS. Over an `int` or a
  `None`, `TypeError`. *(measured, log_024 §4 item 9)*
- The page's "iteration visits elements in index order" universal holds
  for the ordered holders. The frozenset row is the caveat: it iterates
  and it has no index at all, so "in index order" is not checkable
  there.

### sequences in the if-condition slot, across twelve languages

- **Python and php split a sequence by value** — empty goes to the else
  arm. **Ruby sends every sequence to the then arm**, because only
  `nil` and `false` are false. **Typescript accepts and sends every
  sequence to the then arm.** **C++ is PART refused** — some holders of
  sequence convert to bool and some do not. The remaining seven
  languages refuse a sequence in a condition outright. *(measured,
  log_037 §4)*
- A border fact, billed to `choice` per the format ruling, recorded
  here because it gives the list page its first measured
  twelve-language row.
