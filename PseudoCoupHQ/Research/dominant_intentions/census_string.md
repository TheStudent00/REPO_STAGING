# feature census — string (the composite wearing one name)

2026-08-13, hand-drafted in the owner format (structure / operation
/ border), with the guarantees rule and record-both-modes applied.
Fresh work, no old-project artifacts. EVERY FACT UNVERIFIED — the
harness's work order.

Level check before the facts (protocol §11a): at level 1 a string
is a composite — growable buffer of integers plus an encoding
convention. Every fracture below is a disagreement about WHICH
composite the language chose, and each choice is a guarantee, so
ingress always knows which string it was handed.

---

## structure facts — FRACTURED (twice)

**F-s1 — what one position holds (the unit).** Three camps:

- **UTF-16 code unit**: java, csharp, kotlin, typescript, dart.
  (The JVM/CLR/JS engine inheritance — base predicts camp.)
- **byte (UTF-8 by convention)**: go, rust, php, cpp.
- **codepoint**: python, **ruby** (measured: length of "é" is 1,
  of "𝄞" is 1, of "é𝄞" is 2; the first unit of "𝄞" is 119070 —
  matching python cell for cell) (a string is a sequence of
  unicode characters, storage hidden). (measured, log_020 run
  2026-08-14; ruled by the owner 2026-08-14)

The consequence fact, F-s3, is this fracture seen through
`length` — same string, three different lengths ("é" as one
codepoint, one utf16 unit, two utf8 bytes; "𝄞" as one codepoint,
TWO utf16 units, four bytes).

**F-s2 — whether a string can change in place.** Two camps:

- **immutable value**: python, java, csharp, go, kotlin, dart,
  typescript (value semantics via copy-on-write).
- **mutable object**: ruby (`s << "x"` edits s), cpp
  (std::string), rust (String is growable-in-place; &str is the
  immutable view — BOTH exist, by declared type, so rust's
  guarantee is per-declaration, readable at ingress).
- **value semantics between names, mutable in place through one
  name (a fourth position)**: **php** — moved out of the
  immutable-value camp. Measured: assigning into a second name and
  editing through the first leaves the second unchanged (`abc`,
  copy-on-assign confirmed), but assigning into a position through
  the SAME name mutates it in place (`$s[0] = "z"` on `"abc"` gives
  `zbc`). php's guarantee is value semantics between names, but
  mutation within a name. (measured, log_020 run 2026-08-14; ruled
  by the owner 2026-08-14)

## operation facts

Universal candidates (believed 11/11):

- concatenation produces the joined text.
- content equality exists (spelled ==, .equals, or eql —
  spelling aside, a content comparison is available everywhere).
- substring/slice by the language's own unit exists.
- round trip through bytes with a NAMED encoding is exact.

Fractures (string's own operations — these stay):

- **F-s3 — what `length` counts.** utf16-units camp / bytes camp
  / codepoints camp, exactly the F-s1 camps. Each is a
  guarantee; the Hub needs the three length operations, not one
  length with moods.
- **F-s4 — what indexing `s[i]` answers.**
  - a one-character string: python.
  - a utf16 unit (as char): java (charAt), csharp, kotlin,
    typescript, dart (codeUnitAt).
  - a byte: go, php, cpp.
  - REFUSED at the unit level: rust — `s[i]` does not compile;
    you must say `.bytes()`, `.chars()`, or slice by byte range
    (which PANICS off a character boundary — a guarantee too).
- **F-s5 — what the equality OPERATOR does (distinct from
  content equality existing).**
  - `==` compares content: python, go, rust, kotlin, csharp,
    ruby, php, dart, typescript.
  - `==` compares IDENTITY (same object), content is `.equals`:
    java — the classic interview wound, and a real guarantee
    difference the mapper must honor.

## border facts — filed away, for the record

- **→ (string, integer) parsing** — radix, whitespace tolerance,
  error behavior on junk: billed to the conversion machinery.
- **→ (string, float) printing** — already on float's page
  (F-f3).
- **→ (string, ordering)**: locale-aware vs codepoint-order
  comparison — billed to the ordering machinery (and locale is a
  service-call-shaped dependency besides).
- **→ interpolation** — the 121-language family already has its
  own ruled bucket (`interpolation`); string's page only notes
  that its OUTPUT is a string.

## reading — dominance analysis

- **value containment is total**: every camp's string holds any
  unicode text. As values, one dominant string suffices.
- **the unit fractures (F-s1/s3/s4) are guarantees, so the
  division precedent applies directly**: the Hub carries the
  three unit VIEWS as distinct operations (byte-length,
  utf16-length, codepoint-length; likewise indexing), ingress
  stores which view the source guaranteed, the transpiler may
  make a view explicit and never guesses. No contradiction —
  a program using java's length means utf16-length, and
  utf16-length is computable from any faithful representation.
- **pay-per-feature applies to representation**: store one
  canonical encoding; build the other views' index structures
  lazily, on first use — the unused views cost nothing (the V8
  precedent, transplanted).
- **F-s2 (mutability) is the one to watch**: a mutable string is
  observably different when two names share it (edit through one
  name, read through the other). This is not a per-operation
  view; it is an identity semantics difference — the same
  question list/dict will pose loudly. Candidate treatment:
  the dominant string is immutable, and MUTATION is modeled as
  the border where string meets the sharing/aliasing machinery —
  but that machinery has no census page yet, so this files as
  the first OPEN item for the container pages to inherit.
- java's `==` (F-s5) is a guarantee, cheap to honor at ingress
  (map java `==` on strings to identity-compare, `.equals` to
  content-compare); it costs the dominant nothing.

## rulings absorbed (the owner, 2026-08-13, post-draft)

- **origin naming for guarantee-variant operations**: a variant
  operation carries its origin's name — `.java_equals` (or
  `.java.equals`, spelling open) for java's identity-compare;
  most-popular origin when several languages share the variant.
  Verbose but intuitive (the owner). This COMPLEMENTS the Python-naming
  rule: Python names the buckets; origins name the variants.
- **mutability staged, not blocking (F-s2 de-escalated)**: for
  PCv5, a polyfill APPROXIMATION of mutability is fine — PCv5's
  purpose is supporting PseudoIR's compiler transpilation (low
  volume, not user-facing, relaxed efficiency). PCv6/v7 (production
  level) get native mutability in the Hub via compiler slice
  insertion. Either way the ledger knows origin and origin intent,
  which AUTOMATICALLY determines the mode — so shared-mutation
  identity is an implementation stage, not a dominance
  contradiction. (The multi-objective framing recorded with it:
  this research feeds PCv5's relaxed context AND v6/v7's production
  context AND the general ingress/egress discipline; the same
  finding weighs differently per consumer.)

## pattern check, three pages in

bool: featureless after re-filing. float: one operation fracture.
integer: structure + operations fracture, all guarantees. string:
structure fractures twice, operations three times — ALL guarantees
except mutability, which escalates to the sharing question. The
running conclusion holds: fractures are almost always guarantees,
guarantees never contradict (each is computable from a faithful
value), and the genuinely hard residue is narrowing to exactly
two: overflow-behavior selection (integer) and shared-mutation
identity (string, and soon the containers).

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
        `"é" + "hello"` in python, ruby and
        php is three probes.

holder
    the typed slot a value is put into before
    an operation is applied to it.  ONE
    census camp can own several holders.
    example tied to context:
        python's `str` and python's `bytes`
        are two holders for text, and the
        e-acute finding below is entirely
        about which holder was asked.

value class
    a named family of test values, chosen so
    the awkward cases are covered.
    example tied to context:
        `eacute` is the value class holding
        the single character é.

cell
    one combination of operand kinds an
    operation was asked about.
    example tied to context:
        `text|text` is the cell where both
        operands are text.

answer grain
    measuring what an operation RETURNS, as
    against measuring only whether the
    language accepts it.
    example tied to context:
        all three languages accept `==` on
        two e-acutes; the answer grain is
        what shows they agree.
```

### F-s1/F-s3 — the e-acute concatenation is a HOLDER story, not a text story

This is the one predicted text fracture that fractured, and reading it
carelessly gets the wrong lesson. The answers, on
`+ text|eacute | text|base_hello` *(measured, log_031 §5.6)*:

```
python  text:c3a968656c6c6f
ruby    text:c3a968656c6c6f
        sequence:[233,104,101,108,108,111]
php     sequence:[195,169,108,108,111]
```

Two facts, and they point in opposite directions.

- **The string holders AGREE, exactly.** Python's and ruby's string
  holders return the identical bytes, `c3a968656c6c6f`. *(measured,
  log_031 §5.6)* At the cell level `text|text` under `+` scores
  **1.000 python against ruby**, once the reader had decoded both
  languages' printers. *(measured, log_031 §5.6)*
- **The CODEPOINT-ARRAY holders disagree, and that is the whole
  fracture.** Ruby's array carries the codepoint **233**. Php's array
  carries the utf-8 bytes **195** and **169**. *(measured, log_031
  §5.6)*
- So F-s1's three camps are visible inside one language pair by
  changing holder, not by changing language. The page assigns a camp
  per language; the measurement says the camp is a property of the
  HOLDER the program chose, which is the sharper form of the same claim
  and is what makes ingress able to read it.
- A second fault rides along in php's row: php drops a byte. Its array
  answer has five entries where ruby's has six, because `+` on a php
  array is a union by KEY rather than a concatenation — the same
  operation the list and dict pages record. *(measured, log_031 §5.4
  and §5.6)* Php's row is therefore not evidence about php's TEXT at
  all.
- **e-acute EQUALITY did not fracture**: `== text|eacute |
  text|eacute` agrees across all three, with both tokens present in
  each. *(measured, log_031 §5.6)*

### the "concatenation is universal" candidate needs its spelling caveat

- The page lists "concatenation produces the joined text" as a believed
  11/11 universal.
- **Php has no `+` on strings at all** and spells concatenation `.`.
  *(measured, log_031 §5.4)*
- The universal survives as a universal about the OPERATION and not
  about the token. That distinction is already the page's origin-naming
  practice; this is a measured instance of it inside the universals
  list rather than inside the fracture list.

### F-s4 (indexing) — the encoded holder answers a NUMBER, the codepoint holder answers TEXT

- In python, `"hello"[0]` answers `str:'h'` and the same text held as
  `bytes` answers `int:104`. *(measured, log_024 §4 item 4)*
- The page's F-s4 sorts languages into "a one-character string"
  (python) and "a byte" (go, php, cpp). The run shows python sitting in
  BOTH rows depending on holder, so F-s4 is a per-holder fracture in the
  same way F-s1 is.
- Text indexes by position like a sequence, and that is where the
  similarity stops: a sequence refuses a name index with a type
  complaint, and text is refused by neither for the reason the keyed
  camp is. *(measured, log_024 §4 item 4)*

### iteration — a text's unit shows up again in what a `for` sees

- In python, a `for` over `"hello"` collects `['h','e','l','l','o']`,
  and over the same text held as `bytes` collects
  `[104,101,108,108,111]`. *(measured, log_024 §4 item 9)*
- The page has no iteration row. This is F-s1's unit question asked
  through a third operation — length, indexing, and now iteration all
  read the same holder choice — which strengthens the page's reading
  that the Hub needs the unit VIEWS as distinct operations rather than
  one operation with moods.

### text in the if-condition slot, across twelve languages

- Text goes to the else arm when empty and the then arm otherwise in
  **python and php** (recorded as a split by value). In **ruby** every
  text goes to the then arm, because only `nil` and `false` are false.
  In **typescript** text is accepted and split. In **c++** text is
  PART refused — some holders of text convert to bool, some do not.
  The other seven languages refuse a text in a condition outright.
  *(measured, log_037 §4)*
- This is a border fact and it bills to `choice`, per this page's own
  format ruling. It is recorded here because the c++ row is
  per-HOLDER, which is the same shape as F-s1 and is the only place in
  the truthiness table where a static language splits within a form.
