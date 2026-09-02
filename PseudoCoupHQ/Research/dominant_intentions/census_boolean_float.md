# feature census, draft 2 — boolean and float (the calibration pair)

2026-08-13. Draft 1 refactored after the owner's owner insight ("is it
more of a problem for the `if` operator than it is for `bool`?" —
yes, and the census format now says so). Fresh work, no
old-project artifacts. Languages: the 11 active targets (python,
typescript, java, csharp, go, rust, ruby, php, kotlin, cpp, dart;
swift deferred).

EVERY FACT IS UNVERIFIED — written from language knowledge, to be
confirmed or refuted by execution. The census is the harness's
work order.

## the format (RULED 2026-08-13: every fact names its owner)

Three owners, and a fact files under exactly one:

- **structure** — what values the thing can hold. Nothing else.
- **operation** — what can be done to/with the structure, where
  the operation belongs to this structure (negation belongs to
  bool; division belongs to float).
- **border** — the structure meeting something else: an `if`, an
  `==` against another type, a print, a sort. Border facts have
  TWO owners and are billed to the OTHER party or to the pair —
  they constrain that party's dominant, never this structure's.

Dominance of a data structure is decided by its structure +
operation facts ONLY. Border facts migrate: `choice` (the
if/and/or machinery) inherits its own fracture list, the implicit
conversion operation `truth(x)` likewise, equality likewise. Nothing
is discarded; everything is billed correctly.

---

## boolean

### structure facts (believed 11/11 universal)

- two values, spelled true/false (case aside: python True/False).
- nothing else. bool-the-structure is featureless — the
  calibration expectation, restored once usage facts went home.

### operation facts (believed 11/11 universal)

- negation flips the two values.
- two bools compare equal/unequal correctly.
- storable, passable, returnable like any value.

### fractures: none at structure or operation level (believed).

The dominant boolean is expected to be the cheapest dominant in
the whole program: two values and a flip.

### border facts — filed AWAY from bool, named here for the record

- **→ `choice` (the if machinery): which values `if` accepts.**
  bool-only camp: java, csharp, go, rust, kotlin, dart. coerce
  camp: python, typescript, ruby, php, cpp. A fact about each
  language's `if`, not about bool.
- **→ the implicit conversion `truth(x) -> bool`: which values
  convert to false.** Exists only in the coerce camp, and its
  body differs per language: python (None, 0, "", empties),
  typescript (null, undefined, 0, NaN, ""), ruby (ONLY false and
  nil), php (0, "", "0", empty array), cpp (numeric/pointer
  zero). An unwritten function; the fracture is in ITS body.
- **→ `choice` again: what and/or answer.** Operand-returning:
  python, typescript, ruby (`3 or 5` is 3 — control flow wearing
  operator syntax, works on ANY values). Bool-returning: java,
  csharp, go, rust, kotlin, dart, cpp, php.
- **→ the bool/integer border under equality.** python True == 1
  true (bool is an integer sub-species); typescript and php
  loosely true, strictly false; the strict-typed six: not a legal
  comparison. Billed to the PAIR (bool, integer) — a cross-object
  vector when integer's page exists.
- **→ the type checker: comparing two bool LITERALS.** typescript
  refuses (TS2367, disjoint singleton types — literal types exist
  for tagged-union narrowing; bools inherit the machinery); the
  other ten accept. Only reachable in code that never compiled, so
  ingress never meets it; an egress-discipline row only. (measured,
  log_019; ruled by the owner 2026-08-14)

## float

### structure facts (believed 11/11 universal)

- the value is the same 64-bit IEEE double everywhere (level-0
  float; machine-identical — the one object with no costume on
  its value).
- NaN, +Infinity, -Infinity, -0.0 all exist as values.

### operation facts

Universal candidates (believed 11/11):

- arithmetic (+ - * /) follows IEEE round-to-nearest: same
  inputs, same bits.
- NaN == NaN is false; -0.0 == 0.0 is true; infinities compare
  correctly against finite values.

Fractures (owned by float's own operations — these stay):

- **F-f1 — division by zero.** IEEE-quiet camp (1.0/0.0 is
  Infinity): typescript, java, csharp, go (variables), rust,
  ruby, kotlin, cpp, dart. Refuse camp: python raises
  ZeroDivisionError; php 8 throws DivisionByZeroError (its
  fdiv() gives the IEEE answer). Sub-camp: go refuses CONSTANT
  1.0/0.0 at compile time. Division is a float operation, so
  this fracture is genuinely float's — the first real
  union-or-contradiction ruling the dominant float needs.

### border facts — filed away, for the record

- **→ (float, integer) under equality**: 1 == 1.0 true by
  promotion in most; rust refuses without a cast; typescript
  trivially true (there is only the float).
- **→ (float, text): the printed form.** Shortest-round-trip
  camp: python, typescript, rust, ruby, dart, java (mostly).
  Convention camp: cpp (6 significant digits default), php
  (precision setting), go (format-verb dependent), csharp
  (runtime-version differences). Candidate ruling: printing is
  pure costume, excluded from dominance (the owner to confirm).
- **→ (float, ordering): sorting with NaN present.** rust admits
  floats are not totally ordered (loudly, at compile time); java
  picks a total order (NaN last); python and typescript misbehave
  quietly. Billed to the ordering machinery.

## reading, post-refactor

- bool: featureless at structure+operation level, exactly as the
  seed order assumed. Its apparent complexity was `choice`'s and
  the conversion operation's, misfiled.
- float: structure universal; ONE genuine operation fracture
  (F-f1, division by zero) — the first hard dominant ruling.
- the border ledger is not waste: each filed-away fact is a
  pre-written vector for the construct that owns it (`choice`'s
  page starts with three fractures already found).
- pattern to watch at integer/string/list: if their fractures
  also sort mostly into borders, dominants stay cheap and the
  border ledger becomes the real map of cross-language
  disagreement.

---

## layer-3 findings, folded back 2026-08-19

Everything above was written 2026-08-13 from language knowledge and
marked UNVERIFIED: the page was the harness's work order. The layer-3
campaign has since run — logs 024 through 037 in
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/`. This section carries what
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
        `pi + pi` in a 64-bit float slot, in
        seven languages, is seven probes.

holder
    the typed slot a value is put into before
    an operation is applied to it.
    example tied to context:
        php's string holder and php's
        codepoint-array holder are two holders
        for one piece of text, and they gave
        different answers.

form
    the census-level kind of a value, above
    the holder: truth, whole, fractional,
    text, sequence, keyed, nesting, nothing.
    example tied to context:
        the truthiness table below has one
        column per form.

the if-condition slot
    the one operand position an `if` takes.
    run over every holder and value, that
    single slot IS the truthiness table.
    example tied to context:
        c++ accepts a whole number there and
        refuses a `std::map`.
```

## boolean — the truthiness table, measured over twelve languages

The page above files "which values `if` accepts" as a border fact and
names two camps from language knowledge. The runs put every holder and
every value class through the if-condition slot in all twelve
languages, which turns that border fact into a table. *(measured,
log_037 §4)*

Read the codes like this.

```
T   always then
E   always else
S   splits: some values then,
    some values else
R   refused: the checker would not
    accept a value of that form in
    a condition at all
p   part refused: some holders of
    that form accepted, some not
-   not probed
```

Columns are the first two letters of the form: nothing, truth, whole,
fractional, text, sequence, keyed, nesting.

| language | no | tr | wh | fr | tx | sq | ke | ne |
|---|---|---|---|---|---|---|---|---|
| go | R | T | R | R | R | R | R | R |
| rust | R | T | R | R | R | R | R | R |
| cpp | p | T | T | T | p | p | R | R |
| swift | R | T | R | R | R | R | R | R |
| dart | p | T | R | R | R | R | R | R |
| csharp | R | T | R | R | R | R | R | R |
| kotlin | R | T | R | R | R | R | R | R |
| java | R | T | R | R | R | R | R | R |
| typescript | p | T | T | T | T | T | T | T |
| python | E | S | S | S | S | S | S | T |
| ruby | E | S | T | T | T | T | T | T |
| php | E | S | S | S | S | S | S | T |

What the table adds to the page's two camps:

- **The bool-only camp gains swift and loses nobody**: seven refuse
  everything but truth — go, rust, swift, dart, c-sharp, kotlin, java.
  *(measured, log_037 §4)*
- **The coerce camp is five**: c++, typescript, python, ruby, php.
  *(measured, log_037 §4)*
- **The line is not the static-against-open line.** C++ and typescript
  are statically checked and they coerce, and the coercing five do not
  otherwise group. *(measured, log_037 §4)* The page's two camps are
  right and its implied explanation is not available.
- **The two static coercers coerce DIFFERENTLY.** C++ admits whole and
  fractional, part of text and sequence, and flatly refuses keyed and
  nesting — a `std::map` has no conversion to bool. Typescript admits
  every form, because every javascript value has a truthiness.
  *(measured, log_037 §4)*
- **The open three do not agree with each other.** The one cell all
  three share is `nothing` going to the else arm. They then split: ruby
  sends every other form to the then arm without exception, because in
  ruby only `nil` and `false` are false; python and php both split
  whole, fractional, text, sequence and keyed by value, because zero
  and empty are false in both. *(measured, log_037 §4)* This confirms
  the page's per-language bodies for `truth(x)` and puts the ruby row
  where the page put it.
- **A caveat that changes how a T is read.** The nine statically checked
  languages were measured at the HOLDER grain, so a **T** there means
  the holder was accepted, NOT that every value of that form goes to
  the then arm. The three open languages were measured at the VALUE
  grain and their **S** cells carry counts. *(measured, log_037 §4)*

## float — what the runs proved

### the structure claim, confirmed by bits rather than by print

- `pi + pi` on the 64-bit float holder returns the bit pattern
  `FLOAT:64:401921fb54442d18` in go, rust, c++, java, c-sharp, kotlin
  and typescript — seven languages, one bit pattern, no exceptions.
  *(measured, log_032 §5 surprise four)*
- This is the page's "same inputs, same bits" universal candidate,
  promoted from believed to measured on seven of the eleven.
- The method is the finding's other half: **recording bits rather than
  printed decimals is what makes the statement possible.** Seven
  default float formatters would have produced at least three different
  strings, and a print-grain pass would have reported a fracture that
  does not exist. *(measured, log_032 §5 surprise four)*

### the −0.0 lesson — a fracture that belonged to the reader

This is the sharpest methodological finding on this page's subject, and
it is worth carrying because the page lists −0.0 as a structure fact.

- **What was nearly recorded:** php prints negative zero as `-0`. Read
  back by parsing it as a number first, that becomes `whole:0` — and
  the pass would have reported php fracturing from python and ruby on
  −0.0.
- **What was actually true:** the three agree. The reading rule was
  changed to read php's `-0` back by its SIGN CHARACTER, and the
  fracture went away. *(measured during the build; the pre-fix run is
  what showed it — log_031 §5.6, decision 23)*
- The general form: a fracture reported by a census is a claim about
  two languages AND a claim about the instrument that read them. −0.0
  survives as a value in all three; it did not survive the first
  reader.

### the known fractures that did NOT fracture

Checked across python, ruby and php. Every one of these agrees.
*(measured, log_031 §5.6)*

| fracture the page or its neighbours predicted | input cell | verdict |
|---|---|---|
| 2^53+1 | `+ whole\|p53_plus1 \| whole\|base_42` | all three agree, `whole:9007199254741035` |
| −0.0 | `+ fractional\|negzero \| fractional\|negzero` | agree — php `fractional:-0.0`, python and ruby carry `-0.0` and `0.0` |
| NaN arithmetic | `+ fractional\|nan \| fractional\|nan` | agree, `fractional:nan` |
| NaN equality | `== fractional\|nan \| fractional\|nan` | agree, `truth:false` |
| inf against NaN | `< fractional\|inf \| fractional\|nan` | agree, `truth:false` |

- The page's operation universals — NaN == NaN is false, infinities
  compare correctly against finite values — hold as measured across
  those three.
- 2^53+1 agreeing matters to integer's F-i1, where typescript's 2^53
  limit is a structure fracture: the limit is real and it is not
  reachable by these three.

### F-f1 (division by zero), measured on the statically checked nine

- The page's IEEE-quiet camp is confirmed where it was measured, and
  dart is the row worth reading: dart's `/` answers positive infinity,
  `FLOAT:64:7ff0000000000000`, on INTEGER operands, because dart's `/`
  always returns a `double`. *(measured, log_032 §5 surprise three)*
- The consequence for this page: dart's `/` is a float operation
  wearing an integer-looking spelling, so F-f1 owns it and integer's
  F-i5 does not. The census's own division-by-zero rows for dart sit on
  two pages and the operation is one.

### NaN read through the operators rather than through printing

- In python, `nan == nan` is False, `nan != nan` is True, `nan + 42` is
  `float:nan`, and `nan is nan` is False **even for one built value**.
  *(measured, log_024 §4 item 8)*
- `if nan:` takes the TRUE branch and `if -0.0:` takes the false one.
  *(measured, log_024 §4 item 8)*
- The page established what NaN IS. This is what every operator does
  with it, which is the same fact seen from the operation side — and
  the `if` rows are the truthiness table's float column, arriving from
  the other direction.
