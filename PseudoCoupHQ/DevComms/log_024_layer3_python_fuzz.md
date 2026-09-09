# log 024 — layer 3, python: the kind fuzz generated, run, and read

Date: 2026-08-17. Node:
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PseudoCoupHQ/Research/kind_fuzz_clustering/`.
Phases 1 and 2 of that node's plan of record. Python only — generalising to
the other ten is gated on the owner's review, as the node's own plan requires.

---

## §1 — walkthrough, in plain words

Four cold words first, because each has been away long enough that its
earlier definition does not survive the gap.

- **Layer 1** is the DATA: fixed content with no language attached —
  nothing, truth, whole number, fractional number, text, sequence, keyed
  grouping, nesting, identity marks. Ruled 2026-08-15, written down as
  `Research/data_representation/data_layer1.json`.
- **Layer 2** is the REPRESENTATIONS: per language, the ways a running
  program can HOLD that content. One (form, representation) pair is a
  CELL. Reported in log 023.
- **Layer 3**, which this log reports, is the OPERATIONS: what the
  COMPILER can do to a loaded cell. Never builtins, never
  standard-library calls — those are library names, and the node's
  definition puts them out of scope.
- A **KIND** is what tree-sitter's grammar declares: a named construct
  such as `binary_operator` or `subscript`, or an anonymous token such as
  `+` or `is not`. Kinds are what this node clusters.

What was done, in order.

First, the design was written down before anything was generated, so that
it could be argued with rather than reverse-engineered from output. It
says which kinds get probed, what goes into each probe position, what a
probe prints, how a kind that needs an enclosing construct gets one, and
which calls are judgment rather than measurement. It is
`Research/kind_fuzz_clustering/probe_design.md` and §2 below is its
decision list.

Second, the generator ran. It reads the grammar's own legal-slot table —
the pruning instrument phase 0 built — and takes the operand for every
slot from the layer-2 cells that actually loaded: python's 23 LOADS cells
plus its 3 PARTIAL cells with their refused values dropped, 26 cells and
117 distinct values in all. Values are baked in as literals, base values
and edge values alike, so no probe reads a data file at run time. Where a
probe's operands can be spelled as bare literals it is generated twice —
once through a variable, where the compiler cannot fold anything, and
once with the literal standing in the operator's own slot, where it can.
That doubling is the calibration lesson from log 019 made routine: the
difference between the two spellings is a finding about the compiler.
**20,024 probes** came out.

Third, the run. One lane script carrying its own probe payload went
through the SandboxDesign agent lane and came back in **64.5 seconds**.
Inside the sandbox the driver makes two passes. It compiles each probe on
its own first — python's compiler is reachable at run time, so a refusal
isolates to its exact probe and the bisect batching the node designed for
the compiled languages is simply not needed here. Then it runs each
compiled probe in a fresh namespace inside its own catch, under a
two-second clock and a two-gigabyte memory ceiling. Catching is how a
raise is READ; it is harness machinery and never a probed operation.

What came back: **7,868 answers, 11,736 raises, 388 compile refusals, 32
budget exhaustions, nothing lost** — every one of the 20,024 probes has a
line. That the raises outnumber the answers is not a fault. Two thirds of
the probe space is deliberately made of operations applied where they do
not belong — subtracting a keyed grouping from a whole number, indexing a
float — because the boundary of what a kind accepts is exactly half of
what the node compares kinds on. The node's rule is that two kinds relate
by the pair {domain accepted, answer per input}, and a raise is how the
edge of a domain gets located.

Those results were folded into **100 behavior signatures** — one per
probed kind, and, under the R2 ruling, one per operator on a grammar
menu, so `+` and `*` are two signatures and not one host. A signature is
the map from (form, representation, value class) to answer, together with
the domain the kind accepted. That map is what phase 4 will cluster.

Three things the census did not already know came out of it. Two holders
of one layer-1 form can be arithmetically incompatible: `Decimal(42) +
Fraction(42)` raises, though each adds happily to a plain 42 and all
three compare equal. An augmented operator can accept strictly more than
the plain operator it looks like: `list += tuple` answers where `list +
tuple` raises, so the augmented form DOMINATES the plain one inside a
single language — the node's "nests" relation, discovered in the place it
was least expected. And the grammar carries kinds that the language no
longer has: `<>`, `print` as a statement, and `exec` as a statement are
all in python's declared vocabulary and all refuse to compile, 382 of the
388 refusals between them.

---

## §2 — the design decisions, numbered, for the owner

Verbatim from `Research/kind_fuzz_clustering/probe_design.md` §(e). Any of
these can be overturned and the generator re-run; the loop costs about a
minute.

1. **The input is a layer-2 CELL, not a dominant.** Phase 0 counted probes
   against six dominants; layer 3 replaces each dominant with the cells
   that hold that form — python's whole number has four holders, its
   sequence five. This is what makes the run bigger than phase 0's 686 and
   it is the whole point of the three-layer split; without it a probe
   cannot tell `int` from `Decimal`.
2. **Operand pairs are chosen by four rules, not enumerated.** 200 of the
   13,689 possible ordered pairs. The rules are: same-cell (X op X, 26),
   cross-representation within one form (60), cross-form among the seven
   canonical holders (42), and an edge lane putting every non-base value
   of a canonical cell against itself and both ways against a plain 42
   (72). Each rule is there to answer a question; the cross product
   answers none of them better.
3. **A cell classified REFUSES-behavioral is not an input.** python has one
   — `sequence.array.array` — and two of its five values did load. Dropping
   the whole cell is the literal reading of the hand-off rule and it costs
   the run a measured holder. Overturnable: admit the cell with only its
   loaded values, exactly as PARTIAL cells are admitted.
4. **Catching is harness mechanics.** The runner wraps each probe in its
   own try/except so one raise cannot kill a batch, and a `raise`
   PLACEMENT probe is wrapped so the raise can be read. Catching is never
   itself a probed operation.
5. **Python needs no bisect.** Its compiler is reachable at run time, so
   the driver compiles each probe on its own and a refusal isolates
   exactly. The bisect crux in the CORE is a cost of the ten compiled
   languages, not of this one — it is deferred, not solved.
6. **A budget is enforced, and exceeding it is a result.** Two seconds of
   wall clock and 2 GB of address space per probe. `42 ** i64max` is a
   legitimate probe of `**` whose honest answer is "did not finish".
7. **A pattern slot gets only the direct spelling.** In `case {X}:` a
   variable name is not an opaque spelling of a literal — it is a capture
   pattern, a different construct. So the four pattern hosts are probed
   with literals only.
8. **The depth-3+ tail is written up front, not grown from refusals.** The
   CORE left this open; nine wrappers is small enough that writing them
   costs less than a second pass.
9. **Identity atoms are hand-built.** The layer-2 identity probes end in a
   verdict word rather than in the object, so layer 3 spells the three
   identity shapes itself, once per holder. Their construction uses an
   append — layer-2 mechanics for building the operand, never a probed
   operation.
10. **`await` is deferred.** Driving a coroutine needs an event runner,
    which is a standard-library call, and the CORE rules those out of
    scope. It is recorded as deferred rather than silently dropped.
11. **Tier B asks a smaller question than tier A.** One representative
    value per cell, not the full matrix. Overturnable at the cost of about
    a fivefold run, which python can afford and the ten may not.

Two further design points are not judgment calls but are worth stating,
because a reader will look for them. The nine depth-3+ wrappers are
**hand-written** and marked `wrap: "hand"` in the probe file:
`complex_pattern`, `default_parameter`, `dict_pattern`,
`format_expression`, `keyword_argument`, `keyword_pattern`,
`typed_default_parameter`, `union_pattern`, `with_item`. Seventeen
depth-2 kinds get **generated** wrappers — `elif` gets its `if`, `except`
gets its `try`, a comprehension clause gets its comprehension — exactly
the case the CORE names as "`break` needs `for`".

---

## §3 — results overview

Probe space, as generated. Phase 0 predicted 686 python probes under R2
against six dominants; substituting layer-2 cells for dominants multiplies
that by the number of holders and value classes per form.

| | count |
|---|---|
| input cells (LOADS + PARTIAL-minus-refused) | 26 |
| input values (form, representation, value class) | 117 |
| of those, spellable as a bare literal | 43 |
| operand pairs | 200 |
| kinds probed | 62 |
| signatures (R2: one per menu token) | 100 |
| probes generated | 20,024 |
| — opaque spelling / direct spelling | 13,068 / 6,956 |
| — no wrapper / generated wrapper / hand-written wrapper | 18,081 / 1,723 / 220 |
| probes run | 20,024 |
| results returned | 20,024 (none missing) |
| lane runtime | 64.5 s |

By kind family:

| family | signatures | probes | answered | raised | refused | timeout |
|---|---|---|---|---|---|---|
| augmented_assignment | 13 | 4,459 | 1,018 | 3,425 | 0 | 16 |
| binary_operator | 13 | 4,251 | 947 | 3,288 | 0 | 16 |
| comparison_operator | 11 | 3,597 | 2,072 | 1,198 | 327 | 0 |
| placement (44 kinds) | 44 | 1,604 | 1,231 | 312 | 61 | 0 |
| subscript | 1 | 1,600 | 213 | 1,387 | 0 | 0 |
| iteration | 6 | 1,071 | 586 | 485 | 0 | 0 |
| slice | 1 | 960 | 315 | 645 | 0 | 0 |
| delete_statement | 1 | 702 | 56 | 646 | 0 | 0 |
| boolean_operator | 2 | 654 | 654 | 0 | 0 | 0 |
| truth_test | 3 | 480 | 480 | 0 | 0 | 0 |
| unary_operator | 3 | 480 | 130 | 350 | 0 | 0 |
| not_operator | 1 | 160 | 160 | 0 | 0 | 0 |
| concatenated_string | 1 | 6 | 6 | 0 | 0 | 0 |
| **total** | **100** | **20,024** | **7,868** | **11,736** | **388** | **32** |

Truth-testing, `not`, `and` and `or` accept EVERY input the run has: 1,294
probes, no raise, no refusal. That is a domain measurement in its own
right — python has no value its condition slot will reject.

### the operator menus, measured per R2

`binary_operator`, 13 tokens, 327 probes each:

| token | answered | raised | timeout | commonest answer types |
|---|---|---|---|---|
| `*` | 147 | 180 | 0 | int 47, float 36, str 28 |
| `+` | 131 | 196 | 0 | int 47, float 36, list 13 |
| `-` | 96 | 231 | 0 | int 47, float 36, Decimal 6 |
| `%` | 89 | 238 | 0 | int 39, float 32, Decimal 6 |
| `/` | 83 | 244 | 0 | float 71, Decimal 6, Fraction 6 |
| `//` | 83 | 244 | 0 | int 45, float 32, Decimal 6 |
| `**` | 80 | 231 | 16 | float 37, int 33, Decimal 7 |
| `\|` | 64 | 263 | 0 | int 43, dict 13, bool 4 |
| `&` | 48 | 279 | 0 | int 43, bool 4, frozenset 1 |
| `^` | 48 | 279 | 0 | int 43, bool 4, frozenset 1 |
| `>>` | 47 | 280 | 0 | int 47 |
| `<<` | 31 | 296 | 0 | int 31 |
| `@` | 0 | 327 | 0 | — |

`comparison_operator`, 11 tokens, 327 probes each:

| token | answered | raised | refused |
|---|---|---|---|
| `==` | 327 | 0 | 0 |
| `!=` | 327 | 0 | 0 |
| `is` | 327 | 0 | 0 |
| `is not` | 327 | 0 | 0 |
| `<` `<=` `>` `>=` | 138 each | 189 each | 0 |
| `in` | 106 | 221 | 0 |
| `not in` | 106 | 221 | 0 |
| `<>` | 0 | 0 | 327 |

`augmented_assignment`, 13 tokens, 343 probes each; `boolean_operator`,
`and` and `or`, 327 each, both total; `unary_operator`, `+` 54, `-` 54,
`~` 22 answered of 160 each.

### the 388 compile refusals

| refused | count | what it says |
|---|---|---|
| `comparison_operator` `<>` | 327 | the grammar keeps python 2's inequality; python 3 has removed it |
| `exec_statement` | 29 | `exec` is a name in python 3, not a statement |
| `print_statement` | 26 | `print` is a name in python 3, not a statement |
| `dict_pattern` key | 6 | a mapping pattern's key takes a scalar literal only — which is what the grammar declares for that slot; the six container literals fed to it are refused by the compiler |

---

## §4 — first behavior signatures: ten worked examples

Each is read straight off `behavior_python.json`; the probe id is given so
it can be found in `raw/l3_python.txt`.

**1. `+` over the same form in the same holder.** The operator is one
token; what it MEANS is set by the holder.

| left x right | answer |
|---|---|
| (whole, int, 42) x (whole, int, 42) | `int:84` |
| (fractional, float, 1.5) x same | `float:3.0` |
| (text, str, "hello") x same | `str:'hellohello'` |
| (sequence, list, [1,2,3]) x same | `list:[1, 2, 3, 1, 2, 3]` |
| (sequence, tuple, (1,2,3)) x same | `tuple:(1, 2, 3, 1, 2, 3)` |
| (truth, bool, True) x same | `int:2` |
| (keyed, dict, {a:1,b:2,c:3}) x same | `<raise:TypeError>` |
| (nothing, NoneType, None) x same | `<raise:TypeError>` |

Arithmetic for numbers, joining for sequences and text, arithmetic again
for truth values — python's truth value answers as a whole number, which
the census recorded and this confirms from the operator side. The keyed
grouping and the absent value have no `+` at all. Both spellings agree
throughout.

**2. `+` over ONE form in DIFFERENT holders — the cross-representation
lane.** This is the measurement layer 2 exists to make possible.

| left x right | answer |
|---|---|
| (whole, int, 42) x (whole, Decimal, 42) | `Decimal:Decimal('84')` |
| (whole, int, 42) x (whole, Fraction, 42) | `Fraction:Fraction(84, 1)` |
| (whole, int, 42) x (whole, c_int64, 42) | `int:84` |
| (whole, Decimal, 42) x (whole, Fraction, 42) | `<raise:TypeError>` |

Three holders of one layer-1 form. Each mixes with the plain whole number
and answers in its own type — the wider holder wins. But `Decimal` and
`Fraction` do not mix with EACH OTHER, though both hold exactly 42 and
both compare equal to it. Same form, same value, no shared arithmetic.

**3. `+` across forms.** `(whole, int, 42) + (text, str, "hello")` →
`<raise:TypeError>`, and reversed, also `<raise:TypeError>`. `(sequence,
list) + (text, str)` → `<raise:TypeError>`. But `(truth, bool, True) +
(whole, int, 42)` → `int:43`: truth is not a separate arithmetic form in
python, it is a whole number wearing a costume.

**4. subscript over sequence versus keyed versus text.** One token, `[`,
five different meanings.

| container x index | answer |
|---|---|
| (sequence, list) `[0]` | `int:1` |
| (sequence, tuple) `[0]` | `int:1` |
| (sequence, deque) `[0]` | `int:1` |
| (sequence, frozenset) `[0]` | `<raise:TypeError>` |
| (keyed, dict) `[0]` | `<raise:KeyError>` |
| (keyed, dict) `['a']` | `int:1` |
| (keyed, dict) `['absent']` | `<raise:KeyError>` |
| (sequence, list) `['a']` | `<raise:TypeError>` |
| (text, str, "hello") `[0]` | `str:'h'` |
| (text, bytes, "hello") `[0]` | `int:104` |
| (whole, int, 42) `[0]` | `<raise:TypeError>` |

Position for the ordered holders, name for the keyed one — and the two
refuse each other's index in DIFFERENT ways, the sequence with a type
complaint and the keyed grouping with a missing-key complaint, because a
whole number is a perfectly good key that simply is not present. Text
indexes by position like a sequence but its encoded holder answers with a
number where the codepoint holder answers with text. A sequence held as a
frozenset has no index at all.

**5. index kinds that are not whole numbers.** `(sequence, list)[True]` →
`int:2` — the truth costume again, True indexing as 1.
`(sequence, list)[1.5]` → `<raise:TypeError>`; `(sequence,
list)[9223372036854775807]` → `<raise:IndexError>`, a range complaint and
not a width complaint, because python's whole number has no width.

**6. the mixed-form comparisons — where equality and ordering part.**

| pair | `==` | `<` |
|---|---|---|
| (whole, int, 42) x (text, str, "hello") | `bool:False` | `<raise:TypeError>` |
| (whole, int, 42) x (nothing, NoneType) | `bool:False` | `<raise:TypeError>` |
| (sequence, list) x (keyed, dict) | `bool:False` | `<raise:TypeError>` |
| (sequence, list) x (sequence, tuple) | `bool:False` | `<raise:TypeError>` |
| (whole, int, 42) x (fractional, float, 1.5) | `bool:False` | `bool:False` |

Equality is TOTAL in python — 327 of 327 probes answered for each of `==`,
`!=`, `is`, `is not`, none raised. Ordering is not: 138 of 327. The two
sit on the same grammar menu and have visibly different domains, which is
the R2 ruling earning its keep. Numbers order across their forms; nothing
else orders across a form boundary, and two sequence holders do not order
against each other either.

**7. equality ACROSS holders of one form — where two spellings are one
thing.** `int 42 == Decimal 42 == Fraction 42 == c_int64 42` — all
`bool:True`, and `Decimal 42 == Fraction 42` is `bool:True` too, though
they will not add. `dict == OrderedDict` → `bool:True`. But `list ==
tuple` → `bool:False`, `list == deque` → `bool:False`, `str == bytes` →
`bool:False`, `dict == SimpleNamespace` → `bool:False`, while `bytes ==
bytearray` → `bool:True`. Python's numbers agree across holders; its
containers mostly do not.

**8. NaN, read through the operators rather than through printing.**
`nan == nan` → `bool:False`; `nan != nan` → `bool:True`; `nan is nan` →
`bool:False` even for one built value; `nan + 42` → `float:nan`; and
`if nan:` takes the TRUE branch, while `if -0.0:` takes the false one. The
census established what NaN IS; this establishes what every operator does
with it, which is the layer-3 half of the same fact.

**9. iteration — what a `for` sees.**

| holder | `for` collects |
|---|---|
| (sequence, list) | `[1, 2, 3]` |
| (sequence, frozenset) | `[1, 2, 3]` |
| (keyed, dict) | `['a', 'b', 'c']` — the KEYS, not the values |
| (text, str, "hello") | `['h', 'e', 'l', 'l', 'o']` |
| (text, bytes, "hello") | `[104, 101, 108, 108, 111]` |
| (keyed, SimpleNamespace) | `<raise:TypeError>` |
| (whole, int, 42) | `<raise:TypeError>` |
| (nothing, NoneType) | `<raise:TypeError>` |

Text iterates as a sequence of one-character texts; the same text held as
bytes iterates as a sequence of whole numbers. A keyed grouping iterates
over its keys, which is a choice python made and other languages did not.

**10. `*` and `%` — one token, arithmetic in one form and something else
in another.** `(sequence, list) * (whole, int, 42)` answers a 126-element
list: repetition, not multiplication. `(text, str) * 42` repeats the text.
`42 * 42` → `int:1764`. `list * list` → `<raise:TypeError>`. `42 % 42` →
`int:0`; `"hello" % 42` → `<raise:TypeError>` — the old text-formatting
meaning of `%` is not reachable from a text that carries no placeholder,
so this probe locates the boundary rather than the operation. And `42 /
42` → `float:1.0` while `42 // 42` → `int:1`: python's plain division
LEAVES the whole-number form, which is exactly the sort of thing that will
split the eleven languages into camps at phase 4.

---

## §5 — surprises

Six, in the sense of §12: things the census and the layer-2 audit did not
already contain.

1. **Two holders of one form can be arithmetically incompatible.**
   `Decimal(42) + Fraction(42)` raises TypeError. Both hold exactly 42,
   both add to a plain 42, and they compare EQUAL to each other. Equality
   and arithmetic disagree about whether these are the same thing —
   precisely the "overlaps compatibly" case in the CORE's trichotomy, and
   the first one measured.
2. **The augmented operator has a WIDER domain than the plain one, in the
   same language.** `list += tuple` answers `[1, 2, 3, 1, 2, 3]` where
   `list + tuple` raises; `list += "hello"` answers `[1, 2, 3, 'h', 'e',
   'l', 'l', 'o']` where `list + "hello"` raises. Across the whole run
   `+=` answered 156 of 343 against `+`'s 131 of 327, `*=` 153 against
   `*`'s 147, `|=` 70 against `|`'s 64. This is the node's **nests**
   relation — same answers where both work, wider domain — found INSIDE
   one language rather than between two. It also means a clustering that
   treats `+` and `+=` as one kind would be wrong on the evidence.
3. **`|` and `|=` on keyed groupings return different holders.**
   `dict | OrderedDict` answers an `OrderedDict`; `dict |= OrderedDict`
   answers a `dict`. The plain operator takes the right side's holder, the
   augmented one keeps the left's. Same menu token, different answer type.
4. **The grammar carries three constructs python 3 has deleted**, and all
   three refuse to compile: `<>` (327 refusals), `exec` as a statement
   (29), `print` as a statement (26). This is the CORE's "refusal is a
   first-class result" doing real work — it dates the grammar against the
   runtime. One caution for the reader: `print (42)` is not refused,
   because in python 3 the same text parses as a CALL to a name. The
   probe measures the refusal of the python-2 statement form, and the
   direct-spelling twin measures the call it turns into. That is the
   single largest group among the 22 spellings that disagreed.
5. **`@` is a token with no data behind it.** Matrix multiplication is on
   python's `binary_operator` menu and 0 of its 327 probes answered.
   Nothing in layer 1 can reach it — it needs a holder no python
   installation provides without a package. It is a measured hole, and it
   is what a token that only a library can satisfy looks like from here.
6. **`**` is the one operator whose honest answer is sometimes "no
   answer".** 16 of its probes, and 16 of `**=`'s, exhausted the two-second
   budget: `42 ** 9223372036854775807` in a language whose whole number has
   no width has no result to reach. In a fixed-width language the same
   probe will answer instantly, wrapped or saturated — so this timeout is
   itself the discriminating measurement, not a failure of the run.

Two smaller ones, recorded because they will matter to the ten. The
sandbox runner is on python 3.13 while the session's own interpreter is
3.10, and the two disagreed on six compile refusals — the version a lane
runs is part of the measurement and is now captured in the lane log. And
`sequence.array.array`, the one cell python's audit called
REFUSES-behavioral, is absent from this run by decision 3, which is the
cheapest decision on the list to overturn.

---

## §6 — readiness for the ten

The loop is proven end to end on python: design written, probes generated
from the grammar's own legal-slot table, run through the agent lane,
results folded into signatures, nothing lost. What the owner should review
before saying go on the other ten:

- **Decisions 1, 2 and 11** set the size of every remaining run. Layer-2
  cells instead of dominants multiplied python's 686 into 20,024. The ten
  have more representations each and, unlike python, most must COMPILE,
  so the same rules will not cost the same minute. If the answer is that
  phase 3 must fit a budget, the place to cut is the operand-pair rules
  and the tier-B matrix, and it should be cut deliberately here rather
  than discovered at run time.
- **Decision 5 is the one thing python could not test.** Its compiler is
  reachable at run time, so per-probe isolation was free and no bisect was
  written. The bisect crux is real for the other ten and is still
  unimplemented; it needs building and proving on ONE compiled language —
  rust or go, whichever compiles fastest — before all ten are attempted.
- **Decision 3** should be settled once for all eleven, not per language.
  Several languages will have more REFUSES-behavioral cells than python's
  one, and excluding them all could remove a language's only holder for a
  form.
- **Decision 10, `await`,** and with it the whole question of kinds whose
  probe needs a driver, will be much larger in the ten. So will log 021
  §6.2 — the dict gap in java, c-sharp, rust, cpp and kotlin and the
  boolean gap in kotlin — which layer 2 has since answered with
  representations that need a constructor call. Whether those count as
  builtins for layer-3 purposes is unresolved and blocks five languages'
  keyed-grouping lane.
- **The finding in §5.2 changes what phase 4 clusters.** `+` and `+=`
  measured as different kinds with a nesting relation between them. The
  clustering machinery must be able to express "nests" within a language,
  not only across languages, and that should be confirmed before more data
  is generated in a shape that cannot say it.
- **Nothing here is a ruling on the other ten's probe design.** Python's
  tier-A list was chosen from python's own grammar; the equivalent list
  per language is a phase-3 step, and the honest thing is that it will
  need the same eyes on it that this one is getting.

---

## record

Everything is in
`PseudoCoupHQ/Research/kind_fuzz_clustering/`:

- `probe_design.md` — phase 1, the rules, written before generation.
- `probe_generate.py` -> `probes_python.json` — every probe with its
  source, operands, mode and wrapper provenance.
- `lane_build.py` -> `lanes/l3_python.sh` — the self-contained lane; the
  runner cannot see this repo, so the payload travels inside the script,
  as the layer-2 audit lane's did.
- `raw/l3_python.txt` — 20,024 lines of `PROBE_ID|RESULT`;
  `raw/l3_python.lane.log` — the run's own log, including the runner's
  python version.
- `signatures.py` -> `behavior_python.json` + `behavior_python.md` — the
  first behavior signatures and their readable slice.

To reproduce:
`bash -c "cd PseudoCoupHQ/Research/kind_fuzz_clustering && python3 probe_generate.py && python3 lane_build.py"`,
copy `lanes/l3_python.sh` into `SandboxDesign/agent/drop/`,
poll `agent/status/l3_python.sh.status`, copy `agent/out/l3_python.txt`
back to `raw/`, then `python3 signatures.py`.
