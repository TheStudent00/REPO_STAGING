# log 116 — TASK 29: the extracted type inventory

Date: 2026-09-01. Session: Claude Code, TASK 29 of
`DevComms/log_115_claude_code_task_briefs_round6.md`.
Population every number on this page counts: the FIVE COMPILED
LANGUAGES' probe corpus (c, cpp, go, rust, swift) as it stands on
disk today — 4,440 candidate probes, 1,779 the compiler accepted,
2,661 it refused. No interpreter/JIT unit is counted anywhere here.

---

# 1. What was done, in plain words

`probe_gen.py` is the program that writes every candidate probe of
the compiled five. It holds two inventories. The OPERATOR inventory
it does not own — it reads it from
`../kind_fuzz_clustering/operator_arity.json`, where every operator
spelling is attributed to the tree-sitter grammar rule that admits
it, at a pinned grammar version. The TYPE inventory it does own, and
owns badly: a table called `HOLDERS`, six rows per language, typed
in by hand.

the owner's ruling of 2026-09-01: the type inventory is EXTRACTED, NEVER
HAND-WRITTEN. This session did the extraction, measured what the
hand-written six missed, and stopped there — no probe was
regenerated, because that decision is the owner's and §5 hands it over
with numbers.

Three things came out of it.

- An extracted inventory exists now (`type_inventory.json`), built
  from grammar sources and the compilers' own type tables, pinned,
  each row attributed to the file that admits it.
- The extraction succeeds for three of the five languages and FAILS
  for two, for a reason that is a property of those languages, not
  of the extractor: go and swift have no grammar-level type tokens
  at all. Go is rescued by go/types' own table; swift has no
  reachable authority on this machine and comes out with nothing.
- The validation found ZERO holes in one direction (every spelling
  the corpus used is admitted by some authority) and a large gap in
  the other (the six hand-written types are a small corner of what
  the authorities admit), plus one thing neither direction predicts:
  the compiler refuses combinations for reasons no type inventory
  can express.

## 1.1 The vocabulary this log uses

- **holder** — the typed slot an operand sits in before an operator
  is applied. `rust i64` is a holder; so is `c int32_t`. `HOLDERS`
  is probe_gen.py's name for its per-language list of them.
- **candidate probe** — one compiled function applying one operator
  to parameters only, written by `probe_gen.py`. A candidate becomes
  an ACCEPTED unit if the compiler compiles it and a REFUSED row if
  the compiler rejects it; the refusal text is stored as testimony.
- **witness** — a source that admits a type spelling. This log uses
  exactly three, defined in §2.2.
- **cell** — in §4.3, the set of candidate probes sharing one ORDERED
  TYPE PAIR, e.g. every candidate whose left operand is `i32` and
  whose right operand is `f64`. Cells are the grouping used
  throughout; no grouping anywhere in this work is keyed by an
  operator spelling.

---

# 2. The extraction (TASK 29a)

## 2.1 The thing being replaced, quoted

> `PseudoCoupHQ/Research/op_pipeline/probe_gen.py`,
> lines 76–92
>
> ```
> HOLDERS = {
>     "c": [
>         ("i32", "int32_t"),
>         ("i64", "int64_t"),
>         ("u64", "uint64_t"),
>         ("f32", "float"),
>         ("f64", "double"),
>         ("bool", "bool"),
>     ],
> ```

Six rows. No source named. Its own header calls them "the reps the
arch campaign used" — a decision recorded, not an authority read.

Against it, the precedent the ruling points at:

> `PseudoCoupHQ/Research/kind_fuzz_clustering/operator_arity.json`
>
> ```
> "authority": "tree-sitter grammar sources; every operator is
>  attributed to the grammar rule that admits it"
> ```

## 2.2 The three witnesses, and the fourth that was refused

- **grammar** — a tree-sitter grammar rule admits the spelling as a
  literal token. A grammar is a closed, human-written enumeration: a
  spelling absent from it cannot parse as a primitive type. This is
  the ratified route, the same one the operator inventory came down.
- **compiler_table** — the compiler's own type table, at a pinned
  revision.
- **corpus_accepted** — a probe carrying this exact spelling was
  accepted by the corpus's own compiler. This witness can only
  CONFIRM: it can never admit a spelling the generator never asked
  about, so its silence about a type is not evidence against it.
- **dwarf_observed — REFUSED.** The brief named DWARF base types
  observed in the corpus as a third witness. It is refused with a
  checked reason, re-checked at run time by
  `type_inventory.py :: dwarf_refusal()` and written into the output:
  the corpus's DWARF records carry parameter LOCATIONS only, and the
  binaries they were read from live under `/persist`, absent here.

  ```
  $ /tmp/reconnect_venv/bin/python3 -c "...op_units_<lang>.json dwarf entry keys..."
  c     dwarf entry keys: ['location', 'name']
  cpp   dwarf entry keys: ['location', 'name']
  go    dwarf entry keys: ['location', 'name']
  rust  dwarf entry keys: ['location', 'name']
  swift dwarf entry keys: ['location', 'name']
  $ ls -d /persist
  ls: cannot access '/persist': No such file or directory
  ```

  Evidence class: forced by construction (the field is not in the
  artifact; the file is not on the disk). The route itself works —
  `dwarf_typed_key.json` did follow `DW_AT_type` on the interpreter
  track — it has simply never been run over the compiled five's
  probe binaries.

## 2.3 The pins, quoted from the artifacts

| what | pin | quoted from |
|---|---|---|
| `c.js` | `tree-sitter/tree-sitter-c@v0.24.2 :: grammar.js` | `operator_arity.json :: grammar_versions` |
| `c_for_cpp.js` | `tree-sitter/tree-sitter-c@v0.23.6 :: grammar.js` | same |
| `rust.js` | `tree-sitter/tree-sitter-rust@v0.24.2 :: grammar.js` | same |
| `go.js` | `tree-sitter/tree-sitter-go@v0.25.0 :: grammar.js` | same |
| `swift.js` | `alex-pinkus/tree-sitter-swift@0.7.3 :: grammar.js` | same |
| clang type table | `clang/include/clang/AST/BuiltinTypes.def` @ `llvmorg-21.1.8`, read by `git show` | the working tree is at `llvmorg-24-init` and is NOT read |
| go tree | `golang_src` commit `9f1012d9a1aa0831ff44ac9c767e96f9943d13fe` | `git -C Sources/golang_src log -1` |
| rust tree | `rust` commit `7c329d6c76e11ca40c5673818ab0439c1be8962c` | `git -C Sources/rust log -1` |

Two pin caveats are recorded IN the artifact rather than smoothed
over:

- The go tree is `goversion.Version = 28` (go 1.28-dev); the corpus's
  go probes were compiled by the container's `go1.26.0`. The table is
  read from the tree on disk because that is the tree on disk.
- The rust tree is a PARTIAL checkout: `Sources/rust/compiler`
  holds three crates (`rustc_codegen_cranelift`, `rustc_codegen_llvm`,
  `rustc_codegen_ssa`) and nothing else, so rustc's own
  `ty::IntTy/UintTy/FloatTy` definitions are not on disk.

## 2.4 What each language's extraction actually did, with the text

### 2.4.1 c and cpp — the grammar carries a literal token list

The rule, quoted from the pinned cache:

> `PseudoCoupHQ/Research/kind_fuzz_clustering/grammar_cache/c.js`,
> line 640
>
> ```
> primitive_type: _ => token(choice(
>   'bool', 'char', 'int', 'float', 'double', 'void',
>   'size_t', 'ssize_t', 'ptrdiff_t', 'intptr_t', 'uintptr_t',
>   'charptr_t', 'nullptr_t', 'max_align_t',
>   ...[8, 16, 32, 64].map(n => `int${n}_t`),
>   ...[8, 16, 32, 64].map(n => `uint${n}_t`),
>   ...[8, 16, 32, 64].map(n => `char${n}_t`),
> )),
> ```

The extractor reads the quoted literals AND expands the three
spread-maps. 26 spellings for c; cpp takes the same rule through
`c_for_cpp.js` (the C base tree-sitter-cpp derives from), also 26.

The compiler table adds classes the grammar does not carry:

> `clang/include/clang/AST/BuiltinTypes.def` @ llvmorg-21.1.8
>
> ```
> // 'unsigned long'
> UNSIGNED_TYPE(ULong, UnsignedLongTy)
> ```

The comment line above each macro states the C spelling, in quotes.
That comment is the .def file's OWN join between builtin id and
source spelling, so the join is extracted, not written by me. 58
rows.

### 2.4.2 rust — the grammar carries a const list

> `grammar_cache/rust.js`, lines 26–58
>
> ```
> const primitiveTypes = numericTypes.concat(['bool', 'str', 'char']);
> ```

`numericTypes` is the 14-row list `u8 i8 … isize usize f32 f64`; the
concat adds three. 17 spellings, and the grammar's OWN split is the
class marking: numeric versus not.

The compiler table for rust is the cranelift back end's exhaustive
match over rustc's scalar enums:

> `Sources/rust/compiler/rustc_codegen_cranelift/src/common.rs`
>
> ```
> UintTy::U8 => types::I8,
> IntTy::I8 => types::I8,
> FloatTy::F32 => types::F32,
> ```

An exhaustive match over an enum is a complete enumeration of that
enum's variants by construction, which is what makes it usable as
the table. 16 rows. The variant names join to the source spellings
by a case fold (`IntTy::I32` is the type written `i32`), and the
join is ACCEPTED ONLY when the grammar witness already admits the
folded spelling — so the fold can never invent a type.

### 2.4.3 go — the grammar admits nothing, the compiler table admits everything

> `grammar_cache/go.js`, line 862
>
> ```
> _type_identifier: $ => alias($.identifier, $.type_identifier),
> ```

Go's grammar has no primitive-type rule. `int32` parses as an
ordinary identifier. The extractor searched for seven rule names
(`primitive_type`, `builtin_type`, `predeclared_type`, `basic_type`,
`scalar_type`, `numeric_type`, `simple_type`), found none, and
recorded the refusal with the list of names searched.

The authority is go/types' universe:

> `Sources/golang_src/src/go/types/universe.go`, line 41
>
> ```
> var Typ = []*Basic{
>   Bool:    {Bool, IsBoolean, "bool"},
>   Int32:   {Int32, IsInteger, "int32"},
>   Uint64:  {Uint64, IsInteger | IsUnsigned, "uint64"},
>   Float64: {Float64, IsFloat, "float64"},
> ```

26 rows, each carrying go/types' own class flags — which is where
go's scalar classification in this work comes from, rather than from
anyone reading names.

### 2.4.4 swift — no enumerating witness exists here

Swift's grammar spells types through `user_type` /
`_simple_user_type`, so nothing is admitted there. `Int32`, `Double`
and `Bool` are STDLIB DECLARATIONS, and no swift compiler or stdlib
source is on this machine:

```
$ ls Sources
clif_probe  encoder  golang_src  graal  jdk  llvm-project  runtime  rust  sdk
```

Nine entries, none of them swift (`sdk` is the dart sdk; `runtime`
is dotnet). Swift therefore has SIX types in the inventory and all
six come from the confirming witness only — the corpus. That is a
gap, not a result. It is finding F5 in §5.

## 2.5 The output, and the shape it had to take

`type_inventory.json` mirrors `operator_arity.json`: a top-level
`authority` line, a `pins` block, per-language witness records with
their refusals, and the type rows.

One structural point, because it is the SPELLING BAN doing real work
rather than ceremony. The first version keyed the rows by spelling
(`types: {"void": {...}}`). The guard refused it:

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py type_inventory.json
operator inventory: 91 tokens read from probe_manifest_*.json
FAIL type_inventory.json -- 3 spelling-keyed place(s)
     $.languages.c.types.void
         dict key is the operator token 'void'
     $.languages.cpp.types.void
         dict key is the operator token 'void'
     $.pins.grammar_cache.quoted_from
         operator token '..' on a structure field
```

`void` is a c type spelling AND an operator token elsewhere in the
91-token inventory; `..` arrived inside a relative path. The guard
cannot tell a coincidence from a violation and should not have to.
The fix was structural, not an exemption: every type is now a UNIT
OBJECT carrying its own `language` and `id`, with the spelling in the
`spelling` field — the one place a token-shaped string is allowed, a
display label on a member. Paths are absolute.

---

# 3. Both validations (TASK 29b)

The measurements live in `type_inventory_validation.json`, written by
`type_inventory_validate.py`. What is being compared: the extracted
inventory against `op_units_<lang>.json`, which is the acceptance
record — every candidate probe with either a `ship` build (accepted)
or a `refused` string holding the compiler's own words.

## 3.1 Direction one — what the hand-written six missed

The scalar-core rule is stated once and applied mechanically: a type
is in the scalar core when an EXTRACTED class marking calls it an
integer, a float or a truth value (clang's
`SIGNED_TYPE`/`UNSIGNED_TYPE`/`FLOATING_TYPE` macro, go/types'
`IsInteger`/`IsFloat`/`IsBoolean` flags, rust.js's `numericTypes`
split). A type with no extracted marking is NOT guessed — it is
listed as undecided, and the gap is reported as a range.

| language | extracted scalar core | two-authority core | undecided | hand-written | never probed | corpus candidates | predicted at two-authority core | predicted at full core |
|---|---|---|---|---|---|---|---|---|
| c | 56 | 8 | 18 | 6 | 53 | 750 | 1,288 | 57,400 |
| cpp | 56 | 8 | 18 | 6 | 53 | 1,002 | 1,736 | 79,352 |
| go | 14 | not defined | 0 | 6 | 8 | 744 | — | 3,864 |
| rust | 14 | 14 | 3 | 6 | 9 | 858 | 4,466 | 4,466 |
| swift | 0 | not defined | 6 | 6 | 0 | 1,086 | — | 0 |
| **total** | | | | **30** | | **4,440** | **7,490** | **145,082** |

"Two-authority core" is the narrower, still fully extracted subset:
the spellings BOTH a grammar rule and the compiler's own table admit.
It is `not defined` for go and swift because those languages have
fewer than two enumerating witnesses at all — writing `0` there
would read as "no type qualifies", which is a different claim.

### 3.1.1 The growth number, walked with values

The multiplier is computed from the corpus's own candidate counts and
never touches an operator list. Rust, step by step:

```
op_units_rust.json                      candidates = 858
  of which arity == "unary"                          = 66
  of which arity == "binary"                         = 792
h = len(HOLDERS["rust"])                             = 6

unary_operator_count  = 66  / 6      = 11.0
binary_operator_count = 792 / (6*6)  = 22.0

at h' = 14 (the extracted rust scalar core):
  11.0 * 14        =    154   unary candidates
  22.0 * 14 * 14   =  4,312   binary candidates
                     -------
                      4,466   candidate probes
```

858 becomes 4,466: five times the rust lane. The same arithmetic on c
at h' = 56 gives 57,400 against 750 — seventy-six times, because
clang's table admits the fixed-point `_Accum`/`_Fract` family and the
128-bit and 16-bit floats. At the two-authority core (8 spellings:
`bool char char8_t char16_t char32_t double float int`) c is 1,288.

### 3.1.2 The nine rust types never probed

`i8 i16 i128 isize u8 u16 u32 u128 usize`. The hand-written six
carried `i32 i64 u64 f32 f64 bool`, so every narrow width, both
128-bit widths and both pointer-sized widths were never asked about
at all. Go's eight: `int int8 int16 uint uint8 uint16 uint32 uintptr`.

### 3.1.3 The one place the hand-written table is AHEAD of the extraction

For c and cpp, `int32_t`, `int64_t` and `uint64_t` — the three the
probes actually use — are NOT in the extracted scalar core. They are
in `undecided`: the grammar admits the SPELLING (they are literal
tokens in `primitive_type`) and the corpus confirms the compiler
accepted them, but no authority ON THIS MACHINE states their CLASS,
because they are `stdint.h` typedefs whose expansion is the target's
business. Finding F3 in §5.

## 3.2 Direction two — spellings the corpus used that no authority admits

| language | accepted probes | operand spellings used | spellings no authority admits |
|---|---|---|---|
| c | 610 | 6 | 0 |
| cpp | 770 | 6 | 0 |
| go | 107 | 6 | 0 |
| rust | 125 | 6 | 0 |
| swift | 167 | 6 | 0 |
| **total** | **1,779** | | **0** |

Zero holes: every spelling on every one of the 1,779 accepted probes
is admitted by at least one authority. Computed as the set difference
of the accepted rows' `lhs_type`/`rhs_type` values against the
inventory's spellings, per language, all five breakdowns pasted
above. This is the extraction's correctness check and it passes
cleanly — with the honesty note that for swift the admitting witness
IS the corpus, so swift's row is a tautology and proves nothing. The
four real rows are c, cpp, go, rust.

## 3.3 Direction three — the refused combinations, and what a cross product cannot do

A type cross product predicts CANDIDATES. It cannot predict
ACCEPTANCE. This measurement asks how much of the refusal mass a
type pair alone explains: a CELL where every candidate was refused is
type-pair-explained; a cell that is part accepted and part refused is
not, because within one cell the type pair is constant and the
operator's own rules decide.

| language | refused | cells | all-refused | mixed | all-accepted | refusals a type pair alone explains |
|---|---|---|---|---|---|---|
| c | 140 | 42 | 0 | 26 | 16 | 0 of 140 (0.0%) |
| cpp | 232 | 42 | 0 | 36 | 6 | 0 of 232 (0.0%) |
| go | 637 | 42 | 24 | 18 | 0 | 456 of 637 (71.6%) |
| rust | 733 | 42 | 24 | 18 | 0 | 528 of 733 (72.0%) |
| swift | 919 | 42 | 24 | 18 | 0 | 648 of 919 (70.5%) |
| **total** | **2,661** | | | | | **1,632 of 2,661 (61.3%)** |

42 cells per language: 36 ordered pairs of the six holders plus the
six one-operand cells.

### 3.3.1 The contrast, walked with values

Take one cell — left operand `i32`, right operand `f64` — in two
languages.

Rust, cell `i32,f64`: 0 accepted, 22 refused.

```
n=70   a && b   error[E0308]: mismatched types
n=106  a || b   error[E0308]: mismatched types
n=142  a & b    error[E0277]: no implementation for `i32 & f64`
n=214  a ^ b    error[E0277]: no implementation for `i32 ^ f64`
n=250  a == b   error[E0308]: mismatched types
```

Every candidate in the cell dies on the type pair. Rust has no
implicit conversion between an integer and a float, so the pair alone
decides, and 24 of rust's 42 cells behave this way — every mixed-type
pair, plus the pairs where one side is `bool`.

C, the same cell `i32,f64` (spelled `int32_t`, `double`): 12
accepted, 6 refused.

```
n=106  a + b    ACCEPTED
n=142  a - b    ACCEPTED
n=178  a * b    ACCEPTED
n=214  a / b    ACCEPTED
n=250  a % b    refused: invalid operands to binary expression
                ('int32_t' (aka 'int') and 'double')
n=286  a || b   ACCEPTED
```

The same type pair, and now the answer depends entirely on which
operator is applied: C's usual arithmetic conversions promote the
integer to double for four of them and the remainder operator refuses
because it is integer-only. C and cpp have ZERO all-refused cells —
no type pair in the entire c lane is refused outright.

The conclusion this forces, and it is the load-bearing one for the
regeneration decision: **for c and cpp, a type inventory predicts
100% of candidates and 0% of refusals; for go, rust and swift it
predicts about 71% of refusals.** A cross product is a candidate
generator, never an acceptance model, and c/cpp are where that bites
hardest.

### 3.3.2 The refusal causes, by cause and not by sighting

2,661 refusals across five languages, bucketed by a cause family read
off the compiler's own words (family names are named for the SHAPE of
the diagnostic; none is named after an operator):

| cause family | count |
|---|---|
| operand types are not compatible | 1,745 |
| expression is not well formed at all | 192 |
| unclassified refusal text | 173 |
| the form wants something that is not a value operand | 168 |
| form needs a generic bound the scalar does not have | 156 |
| operand type is not allowed here | 92 |
| shift position has its own operand rule | 54 |
| operand is not a pointer or a reference | 36 |
| this form is withdrawn or restricted for this operand | 21 |
| no such trait or protocol conformance | 18 |
| result type does not match the stated signature | 6 |

Residue 173 of 2,661 (6.5%) is a genuine long tail — each remaining
text is distinct — and is reported as unclassified rather than forced
into a family.

---

# 4. The gap size, and the regeneration decision (TASK 29c)

Nothing was regenerated. The numbers the decision needs:

| option | candidate probes | vs today (4,440) |
|---|---|---|
| today (hand-written six) | 4,440 | — |
| two-authority core, c/cpp/rust only, go+swift unchanged | 7,490 + 744 + 1,086 = 9,320 | x2.1 |
| full extracted scalar core, all five | 145,082 | x32.7 |

Three things the owner should weigh, stated as facts rather than as a
recommendation:

- The x32.7 figure is dominated by clang's extension-only rows —
  the `_Accum`/`_Fract` fixed-point family, `__float128`, `__ibm128`,
  `__fp16`. They are genuinely in clang's table and genuinely
  compilable with the right flags; whether they are IN SCOPE for
  scalar operator equivalence is a scope question, not an extraction
  question.
- Swift cannot be regenerated from an extracted inventory at all
  today. Its six types have no enumerating authority on this machine
  (§2.4.4).
- A regeneration at any size does NOT need the acceptance question
  answered first: the lane's whole design is that the compiler is the
  acceptance oracle and a refusal is testimony. What §3.3 changes is
  the EXPECTED YIELD, not the method — at rust's 72% type-pair
  refusal rate, most new candidates in mixed-type cells will refuse,
  and refusals are cheap (seconds, per `lane_gen.py`'s fast path).

---

# 5. Findings, by cause, each with a status

- **F1 — the hand-written six are a narrow corner. OPEN, sized.**
  30 hand-written rows across five languages; the authorities admit
  56/56/14/14/0 scalar types. 53 c types, 53 cpp, 8 go and 9 rust are
  never probed. Evidence: §3.1, computed breakdown pasted.
- **F2 — go and swift have no grammar-level type inventory.
  OPEN, structural.** Both grammars spell every type name as an
  identifier. Go is rescued by go/types' `Typ` table; swift has no
  reachable authority and its six inventory rows rest on the
  confirming witness alone. Evidence: §2.4.3, §2.4.4, with the
  searched rule names recorded in the artifact.
- **F3 — the c/cpp fixed-width spellings have no CLASS authority on
  this machine. OPEN.** `int32_t`, `int64_t`, `uint64_t` are admitted
  as spellings by the grammar and confirmed by the corpus, but their
  integer-ness is a `stdint.h` typedef expansion that no on-disk
  source states. They sit in `undecided`. A fourth authority (the
  target's typedef expansion, or a DWARF read) would close it.
- **F4 — a type cross product cannot predict acceptance, and in c
  and cpp it predicts none of it. OPEN, measured.** 0.0% of c/cpp
  refusals are type-pair-explained against ~71% for go/rust/swift.
  Evidence: §3.3, per-language table.
- **F5 — the stored refusal text has one systematic alteration.
  OPEN, not fixed this round.**
  `lane_gen.py :: firstline()` applies `text.replace("|", "/")` to
  every stored diagnostic (lines 192, 365, 368, 371, 373). The
  compiler's own words are therefore altered wherever a diagnostic
  quotes the `|` spelling: rust probe 178 is stored as
  ``error[E0277]: no implementation for `i32 / f64` `` when the
  expression is `a | b`. Refusal text is TESTIMONY, so an alteration
  in it matters. Nothing was changed — zero regressions was binding —
  and the fix belongs to whoever next touches the lane.
- **F6 — DWARF base types are not available for the compiled five.
  OPEN.** §2.2. The route exists and works on the interpreter track;
  it has not been run here.

---

# 6. Guards and regression checks

## 6.1 The spelling-key check, both artifacts

```
$ cd PseudoCoupHQ/Research/op_pipeline
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py \
      type_inventory.json type_inventory_validation.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS type_inventory.json -- no operator token in any key, grouping, pairing or row structure
PASS type_inventory_validation.json -- no operator token in any key, grouping, pairing or row structure
EXIT=0
```

Both programs also REFUSE THEIR OWN OUTPUT on failure: each calls
`refuse_own_output_on_spelling_failure()` after writing, which runs
the guard, removes the written file and exits nonzero if it fails. So
a spelling-keyed artifact cannot be left on disk for a later stage to
inherit.

## 6.2 Zero regressions

```
$ cd PseudoCoupHQ && git status --porcelain
 M Research/op_pipeline/type_inventory.py
 M Research/op_pipeline/type_inventory_validate.py
?? Research/compiler_graph/graph_cpp2.json
?? Research/compiler_graph/graph_cpp3.json
```

The two `M` rows are this session's own new files, already
auto-committed by the daemon and then edited again — a file's current
state is not its history, and the vcs shows they were ADDED by this
session, never pre-existing. The two `??` rows are not this session's:
their timestamps are 19:16 and 21:43 against a session that started at
16:19 today, i.e. yesterday evening, from the compiler-graph line.

`probe_gen.py` was NOT touched:

```
$ git log -1 --format='%h %ad %s' --date=short -- probe_gen.py
8dda5af 2026-08-25 update
```

Last change 2026-08-25, seven days before this session.

## 6.3 Evidence class per claim

| claim | evidence class |
|---|---|
| every inventory row's authority (§2.4) | forced by construction — the row is read out of the named file at the named pin |
| the class markings | forced by construction — the source's own macro/flag/const split |
| the rust case-fold join | derived, gated — accepted only where the grammar already admits the folded spelling |
| the 1,779 / 2,661 / 4,440 counts | forced by construction — `op_units_<lang>.json`'s own `tally` |
| the growth multipliers (§3.1.1) | derived arithmetic from the corpus's own candidate counts |
| the cause families (§3.3.2) | interpreted — a regex over the compiler's words; the 6.5% residue is left unclassified rather than forced |
| the dwarf refusal (§2.2) | forced by construction — field absent, directory absent, both re-checked at run time |
| F5, the altered refusal text | forced by construction — the substitution is on five named lines of `lane_gen.py` |

---

# 7. Complete file inventory

Created this session, all new, nothing existing modified:

| path | what it is |
|---|---|
| `PseudoCoupHQ/Research/op_pipeline/type_inventory.py` | the extractor (TASK 29a) |
| `PseudoCoupHQ/Research/op_pipeline/type_inventory.json` | the extracted inventory, pinned, per language, per type, with the authority that admits it |
| `PseudoCoupHQ/Research/op_pipeline/type_inventory.md` | the readable rendering of the same |
| `PseudoCoupHQ/Research/op_pipeline/type_inventory_validate.py` | the two-direction validation (TASK 29b/c) |
| `PseudoCoupHQ/Research/op_pipeline/type_inventory_validation.json` | the measurements, per language, with the cells and the cause families |
| `PseudoCoupHQ/Research/op_pipeline/type_inventory_validation.md` | the readable rendering of the same |
| `PseudoCoupHQ/DevComms/log_116_task29_type_inventory.md` | this log |

Modified this session: one line appended under the single
`# PROGRESS` heading of
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`.

Read but not modified: `probe_gen.py`, `check_no_spelling_keys.py`,
`lane_gen.py`, `op_units_<lang>.json` (five),
`probe_manifest_<lang>.json` (five),
`../kind_fuzz_clustering/operator_arity.json`,
`../kind_fuzz_clustering/operator_arity.py`,
`../kind_fuzz_clustering/grammar_cache/{c,c_for_cpp,go,rust,swift}.js`,
`Sources/golang_src/src/go/types/universe.go`,
`Sources/rust/compiler/rustc_codegen_cranelift/src/common.rs`,
`Sources/llvm-project` at `llvmorg-21.1.8` via `git show`.

---

# 8. Awaiting the owner

One decision, with the numbers it rests on in §4:

- Regenerate probes over the extracted inventory, and at which
  width — the two-authority core (9,320 candidates, x2.1) or the full
  extracted scalar core (145,082, x32.7)? Swift cannot participate in
  either until it has an enumerating authority (F2).

Decided and recorded for audit, no ruling needed: the witness set and
its refusals (§2.2), the scalar-core rule and its undecided bucket
(§3.1), the unit-object row shape forced by the spelling guard
(§2.5), the cause-family names (§3.3.2).
