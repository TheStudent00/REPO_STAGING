# log 022 — type_vocabulary step A: the twelve compilers' type enumerations, unioned

date: 2026-08-16
node: `PseudoCoupHQ/Planning/node_0_3_research/node_0_3_3_type_vocabulary/CORE_0_3_3_type_vocabulary.md`
artifacts: `PseudoCoupHQ/Research/type_vocabulary/`
status: step A complete — MEASUREMENT ONLY. Nothing here rules on which
entries become instruments; that is step B, and it is the owner's.

---

## §1 — what step A did, in plain words

Five words in this log have been away long enough to need a line each
before they are used.

- An **instrument** is a data structure the fuzzing line measures WITH:
  a shape whose behaviour has been written down per language and then
  confirmed by execution. Six exist — boolean, float, integer, string,
  list, dict — and they live in
  `PseudoCoupHQ/Research/dominant_intentions/`.
- A **dominant** is the one version of such a structure that all twelve
  languages can be made to agree on; "the six verified dominants" and
  "the six instruments" name the same six things from two directions.
- The **harness** is the runner in
  `PseudoCoupHQ/Research/dominant_intentions/harness/`
  that takes a written-down claim and executes it in every language to
  confirm or refute it. It is not used in this log at all.
- **`TyKind`** is the enum inside the Rust compiler that lists every
  form of type rustc understands. It is the model for this whole node:
  a compiler carries its own closed list, so the list can be read
  rather than guessed at.
- The **lane** is the unattended runner at
  `SandboxDesign/agent/` — a session drops a shell script
  into `drop/`, a daemon runs it inside the sandbox container, and the
  session reads the log and the products back out. Every language that
  was executed here was executed through it.

The job was: for each of the twelve target languages, find the
language's OWN list of the types it understands, take that list
verbatim, and union the twelve lists.

**Where the lists came from.** Nine languages handed over a closed
enumeration written by the compiler's own authors — rustc's `TyKind`,
go's `reflect.Kind`, javac's `TypeKind`, the TypeScript checker's
`TypeFlags`, the CLR's `CorElementType`, libstdc++'s type-category
traits, the Kotlin compiler's `PrimitiveType` and `StandardNames`,
swift's `Mirror.DisplayStyle`, php's `gettype()` value set. Three
languages have no such list to hand over, so what they gave instead was
their core type table: CPython's builtin type objects, ruby's core
classes, the Dart SDK's `dart:core` declarations. Swift gave both.

**That difference is a level crossing, and it is the thing everything
else in this log rests on.** A `TyKind` variant is a type FORM — "there
is a thing called a struct". A core-type entry is a NAMED TYPE — "there
is a thing called `Hash`". The union had to be built at one level, so
it was built at the level the instruments already live on: a shape a
running program holds values of. Reading the form level onto that shape
level is the first normalization decision (§4.1) and every other
decision hangs off it.

**The headline number: the union has 59 distinct entries.** Six of them
are already verified instruments. Fifty-three are new. Fifteen of the
59 are single-language.

Two of the 59 are worth naming immediately because they change what
"complete" means.

- **Two of the six verified instruments are barely in the compilers at
  all.** `dict` is present in 6 of 12 and `list` in 7 of 12. In java,
  csharp and cpp neither is a type the compiler knows about — the
  growable list is `ArrayList`, `List<T>`, `std::vector`, all library
  classes, and the map likewise. The instruments were never chosen from
  the compilers' vocabulary, and this measurement is the first time
  that gap has been counted.
- **Twelve of the 59 are not data at all.** They are types the compiler
  manipulates and no running program ever holds a value of: inference
  variables, java's `WILDCARD`, the CLR's `ELEMENT_TYPE_SENTINEL`,
  rustc's `Error`. They are in the table and counted, marked
  `MACHINERY`, so that step B can rule them out in one move instead of
  twelve.

The first-pass expectation written into the CORE guessed "about a
dozen" beyond the six. The measured answer is 53 beyond the six, of
which 41 are data and 12 are machinery. Two entries the expectation
named did not survive: `decimal` produced no row at all (§4.13), and
`complex` produced one, but at 3 of 12 rather than as a single-language
oddity.

Nothing was executed against a program; nothing was verified; no fact
about behaviour was collected. This is a vocabulary count.

---

## §2 — the source used for each language, and how authoritative it is

One row per language. "compiler-enum" means the list was read out of a
closed enumeration the compiler's own authors maintain. "runtime-
enumerated" means the list was read out of a running interpreter, which
is authoritative for that build but is a core-type table rather than a
type-kind enum. "doc-sourced" means it was transcribed from a
specification because nothing executable was available.

| language | what was read | confidence | how |
|---|---|---|---|
| rust | `TyKind` in `compiler/rustc_type_ir/src/ty_kind.rs`, which is what `rustc_middle::ty::TyKind` re-exports; plus `AliasTyKind` and `InferTy` | compiler-enum | fetched verbatim from `raw.githubusercontent.com/rust-lang/rust/master/...` |
| go | `reflect.Kind` iterated from 0 and printed via `String()`; `go/types.BasicKind` read off the `types.Typ` table | compiler-enum (runtime-enumerated); the 14 structural node names are doc-sourced | go 1.26.0 in the lane |
| java | `javax.lang.model.type.TypeKind.values()` and `java.lang.classfile.TypeKind.values()` | compiler-enum (runtime-enumerated from the JDK); the JVMS 4.3.2 descriptor table is doc-sourced | OpenJDK 25.0.3 in the lane |
| typescript | `ts.TypeFlags` and `ts.ObjectFlags` read straight off the compiler package | compiler-enum | typescript 5.9.3 under node in the lane |
| csharp | `CorElementType` in `dotnet/runtime`, `src/libraries/System.Private.CoreLib/src/System/Reflection/CorElementType.cs` | compiler-enum, but NOT executed — no .NET is installed | fetched verbatim from `raw.githubusercontent.com/dotnet/runtime/main/...` |
| python | every name in `builtins` and in `types` for which `isinstance(obj, type)` holds | runtime-enumerated; core-type level, CPython exposes no `TyKind` equivalent | CPython 3.13.14 in the lane |
| ruby | every constant on `Object` whose value is a `Module` | runtime-enumerated; core-type level | ruby 3.3.8 in the lane |
| php | `gettype()`/`get_debug_type()` over one value of each constructible zval shape; core interfaces from `get_declared_interfaces()` | runtime-enumerated for those two; the zval `IS_*` tags and the declaration-position type names are doc-sourced | PHP 8.5.4 in the lane |
| kotlin | `org.jetbrains.kotlin.builtins.PrimitiveType.values()` and the static fields of `StandardNames$FqNames`, read by reflection out of the shipped `kotlin-compiler.jar`; plus the top-level classes in `kotlin-stdlib.jar` | compiler-enum | kotlinc at `/persist/kotlinc` in the lane |
| cpp | the primary and composite type-category traits, and the fundamental integral and floating types, read off the `__is_integral_helper` and `__is_floating_point_helper` specializations | compiler-header-sourced (the implementation's own header, not hand-listed) | libstdc++ `/usr/include/c++/15/type_traits` |
| dart | every top-level nominal declaration in the SDK's own `dart:core` sources | sdk-source-enumerated; core-type level | `/persist/dart-sdk/lib/core/*.dart` |
| swift | the shipped `Swift.swiftinterface` for the stdlib module: column-0 public nominal declarations and typealiases; plus `Mirror.DisplayStyle` from the same file | stdlib-interface-enumerated (the compiler's own module interface) | swift 6.0.3 at `/persist/swift` |

Three things went wrong on the way and are recorded because they change
what a re-run would do.

- **TypeScript 7 no longer exposes `TypeFlags` from JavaScript.** `npm
  install typescript` fetched 7.0.2, whose checker has moved to Go;
  `ts.TypeFlags` came back `undefined` and no `typescript.d.ts` shipped
  at the usual path. The 5.x line was pinned instead, and 5.9.3 gave
  the enum. A later re-run must pin the same way or read the enum from
  the typescript-go source.
- **Swift ships no `TyKind` equivalent in the binary toolchain.** No
  `MetadataKind.def`, no `TypeNodes.def`, no `MetadataValues.h`
  anywhere under `/persist/swift`. The stdlib's module interface is the
  closest closed list available, plus `Mirror.DisplayStyle`, which is a
  real eight-case type-kind enum but a small one.
- **csharp is the one language nothing was run for.** The .NET
  toolchain is not installed. `CorElementType` was read from the
  runtime's own source rather than from prose documentation, so it is
  as good as a compiler-enum in content, but it was never executed and
  is marked accordingly.

The raw extractions, one file per language with the verbatim names, the
source and the confidence, are in
`PseudoCoupHQ/Research/type_vocabulary/raw/`.

---

## §3 — the union

Column heads are the twelve languages in the order python, typescript,
java, csharp, go, rust, ruby, php, kotlin, cpp, dart, swift. Three
markers:

- `x` — the type is in that language's own enumeration.
- `~` — present but qualified. The reason sits in the `raw` field of
  that cell in `type_union.json`; go's `rune` is an alias for `int32`
  rather than a distinct kind, typescript's `Array` is a `lib.d.ts`
  interface rather than a `TypeFlag`.
- `.` — absent from that language's own enumeration.

`n` counts only the `x` cells.

| type entry | py | ts | jv | cs | go | rs | rb | ph | kt | cp | dt | sw | n | instrument | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| boolean | x | x | x | x | x | x | x | x | x | x | x | x | 12 | yes | ruby spells it as two classes with one value each |
| integer (fixed-width whole number) | . | . | x | x | x | x | . | x | x | x | x | x | 9 | yes | python and ruby have no fixed-width integer at all; their whole-number type is arbitrary-precision and sits in the bigint row. typescript has neither: `number` is the double. |
| bigint (arbitrary-precision whole number) | x | x | . | . | . | . | x | . | . | . | x | ~ | 4 | no | swift's StaticBigInt only types a literal, it is not a value type a program computes with |
| unsigned integer | . | . | . | x | x | x | . | . | x | x | . | x | 6 | no | java has no unsigned type at all |
| pointer-sized integer | . | . | . | x | x | x | . | . | . | ~ | . | ~ | 3 | no | the width follows the machine word rather than the source |
| float (IEEE binary floating point) | x | x | x | x | x | x | x | x | x | x | x | x | 12 | yes |  |
| complex number | x | . | . | . | x | . | x | . | . | . | . | . | 3 | no | named in the CORE's first-pass expectation; the measurement confirms it at 3 of 12 |
| rational number | . | . | . | . | . | . | x | . | . | . | . | . | 1 | no | exact fractions; only ruby ships one as a core class |
| char / unicode scalar | . | . | x | x | ~ | x | . | . | x | x | . | x | 6 | no | python, typescript, ruby, php and dart have no character type; a one-element string stands in |
| string / text | x | x | . | x | x | x | x | x | x | . | x | x | 10 | yes | java and cpp are the two whose compiler-level enumeration has no text type: java.lang.String is a DECLARED reference and std::string is a library class template |
| byte buffer / raw bytes | x | . | . | . | ~ | . | ~ | ~ | . | . | . | . | 1 | no | three languages have byte-oriented strings instead of a separate buffer type |
| list (growable ordered sequence) | x | ~ | . | . | x | ~ | x | x | x | . | x | x | 7 | yes | java's ArrayList, csharp's List<T>, cpp's std::vector and rust's Vec are library types; none appears in those four compilers' own type enumerations |
| fixed-size array | . | . | x | x | x | x | . | . | x | x | . | . | 6 | no | length is part of the type |
| slice / view into a sequence | x | . | . | . | ~ | x | . | . | . | . | . | x | 3 | no | borrows storage it does not own |
| dict (key-to-value map) | x | . | . | . | x | . | x | ~ | x | . | x | x | 6 | yes | a verified instrument, yet only 6 of 12 compilers enumerate it; elsewhere it is a library class |
| set | x | . | . | . | . | . | x | . | x | . | x | x | 5 | no | the CORE flags this as a candidate derivation from dict |
| tuple (fixed-arity heterogeneous product) | x | x | . | . | ~ | x | . | . | ~ | . | x | x | 5 | no |  |
| struct / record (named product, no identity) | ~ | . | . | x | x | x | x | . | . | x | . | x | 6 | no |  |
| class / object with identity | x | x | x | x | . | . | x | x | x | x | x | x | 10 | no | go and rust have no class form at all |
| enum / tagged variant | . | x | . | . | . | x | . | ~ | x | x | x | x | 6 | no | java's TypeKind has no enum entry (an enum is a DECLARED class) and csharp's CorElementType has none either (an enum is a VALUETYPE) |
| range / interval | x | . | . | . | . | . | x | . | x | . | . | x | 4 | no |  |
| iterator / sequence | x | . | . | . | . | . | x | x | x | . | x | x | 6 | no | swift's ~40 lazy and adapter sequence types fold here |
| function (a callable value) | x | ~ | x | x | x | x | x | ~ | x | x | x | ~ | 9 | no |  |
| closure / coroutine / generator (callable carrying state) | x | . | . | . | . | x | x | x | . | . | . | . | 4 | no | rustc gives these four TyKind variants of their own, which is why they earn a row separate from function |
| pointer (raw machine address) | . | . | . | x | x | x | . | . | . | x | . | x | 5 | no |  |
| reference (alias for another's storage) | . | . | . | x | . | x | . | ~ | . | x | . | . | 3 | no |  |
| weak reference | ~ | . | . | . | . | . | . | ~ | . | . | x | . | 1 | no | php's WeakReference/WeakMap are core classes, but this measurement does not read presence off php's class list (decision 6), so php is marked qualified |
| channel (typed queue between tasks) | . | . | . | . | x | . | ~ | . | . | . | . | . | 1 | no | the CORE's own example of a single-language type that stays in |
| symbol / interned name | . | x | . | . | . | . | x | . | . | . | x | . | 3 | no |  |
| regular expression | . | . | . | . | . | . | x | . | . | . | x | . | 2 | no |  |
| date-time / duration | . | . | . | . | . | . | x | . | . | . | x | x | 3 | no |  |
| optional wrapper (adds absence to a type) | . | ~ | . | . | . | ~ | . | . | ~ | . | ~ | x | 1 | no | rust's Option is a library enum with no TyKind of its own; three languages spell optionality as a modifier rather than a type |
| the absent value's own type (null/nil/None) | x | x | x | . | x | . | x | x | . | x | x | . | 8 | no | csharp, rust, kotlin and swift give the absent value no type of its own |
| void / unit (no meaningful value) | ~ | x | x | x | ~ | ~ | ~ | ~ | x | x | ~ | x | 6 | no | half the set has a real type here and half fakes it with the absent value or with no return at all |
| never / bottom (the type with no values) | . | x | . | . | . | x | . | ~ | x | . | ~ | x | 4 | no |  |
| any / top (every value belongs to it) | x | x | ~ | x | ~ | . | x | ~ | x | . | x | x | 7 | no |  |
| interface / protocol (dispatch, no storage) | . | x | ~ | ~ | x | x | ~ | ~ | . | . | . | x | 4 | no |  |
| runtime type object (a value denoting a type) | x | . | . | . | . | . | x | . | x | . | x | ~ | 4 | no |  |
| error / exception type | x | . | ~ | . | ~ | . | x | x | x | . | x | x | 6 | no | rust's TyKind::Error is NOT this -- it is the compiler's marker for a type it could not compute, and it is filed under the compiler-placeholder row instead |
| result / either | . | . | . | . | . | ~ | . | . | x | . | . | x | 2 | no |  |
| lazy value (computed on first read) | . | . | . | . | . | . | . | . | x | . | . | . | 1 | no |  |
| atomic cell | . | . | . | . | . | . | . | . | x | . | . | . | 1 | no |  |
| SIMD vector | . | . | . | . | . | . | . | . | . | . | . | x | 1 | no |  |
| key path / property reference | ~ | . | . | . | . | . | . | . | x | . | . | x | 2 | no |  |
| module / package as a type | x | . | x | . | . | . | ~ | . | . | . | . | . | 2 | no |  |
| uri | . | . | . | . | . | . | . | . | . | . | x | . | 1 | no | the weakest data entry: parsed text that only dart puts in its core |
| text builder (mutable text accumulator) | . | . | . | . | . | . | . | . | . | . | x | . | 1 | no | java's StringBuilder and python's io.StringIO are library types; only dart's core declares one |
| union type (a value is one of several) | x | x | x | . | x | . | . | ~ | . | ~ | . | . | 4 | no | MACHINERY. cpp's is_union is overlapping storage, a different thing from a type-level union |
| intersection type | . | x | x | . | . | . | . | ~ | . | . | . | . | 2 | no | MACHINERY. |
| type parameter / generic variable | . | x | x | x | x | x | . | . | . | . | . | . | 5 | no | MACHINERY. |
| wildcard (bounded unknown type argument) | . | . | x | . | . | . | . | . | . | . | . | . | 1 | no | MACHINERY. java alone gives this a type kind |
| applied generic (a generic with its arguments filled in) | . | x | . | x | ~ | ~ | . | . | . | . | . | . | 2 | no | MACHINERY. |
| type alias | . | . | . | . | x | x | . | . | . | . | . | x | 3 | no | MACHINERY. |
| literal type / untyped constant | . | x | . | . | x | ~ | . | . | . | . | . | . | 2 | no | MACHINERY. two compilers carry a whole level between the literal and its eventual type |
| type operator (conditional, keyof, indexed access, mapped) | . | x | . | . | . | . | . | . | . | . | . | . | 1 | no | MACHINERY. typescript alone computes types from other types |
| opaque / foreign type (layout unknown to the language) | . | . | . | ~ | . | x | . | . | . | . | . | ~ | 1 | no | MACHINERY. |
| unsafe binder (lifetime-erased type) | . | . | . | . | . | x | . | . | . | . | . | . | 1 | no | MACHINERY. rust alone |
| pattern-restricted type (values narrowed by a pattern) | . | . | . | . | . | x | . | . | . | . | . | . | 1 | no | MACHINERY. rust alone |
| compiler-internal placeholder (inference var, error, sentinel) | . | x | x | x | x | x | . | ~ | . | . | . | . | 5 | no | MACHINERY. no program ever holds one of these; they exist so the compiler can keep going |

Every cell that reads `x` carries, in `type_union.json`, the raw
spelling it was built from, and `union.py` checks that spelling against
the language's raw file on every run. The check currently reports **0
`x` cells with no matching raw name**. Nine `~` cells fail the same
check by design: their note is prose explaining why the type is
qualified rather than a name from the enumeration ("Option is a library
enum, absent from TyKind").

---

## §4 — the normalization decisions

These are the judgment calls. Each one is a place where the raw
enumerations did not decide the answer and I did. They are the part of
step A that step B is entitled to overturn; overturning any of them
changes the union size, and `union.py` is the one file to edit.

1. **The union is built at the shape level, not the type-kind level.**
   Nine languages gave a type-kind enumeration (a list of type FORMS);
   three gave a core-type table (a list of NAMED TYPES); swift gave
   both. A single table cannot hold two levels, so everything was read
   onto the level the six instruments already occupy — a shape a
   running program holds values of. The cost is that rustc's `Adt` and
   ruby's `Hash` sit in the same table despite being different kinds of
   statement.

2. **`integer` and `bigint` are two rows, not one.** python and ruby
   have no fixed-width whole number at all; their integer is
   arbitrary-precision. typescript has neither — `number` is the
   double, and `BigInt` is a separate flag. Splitting makes `integer`,
   a verified instrument, read 9 of 12, with python and ruby appearing
   only on the bigint row. **Merging them would read 12 of 12 and hide
   the overflow fracture the census already found.** This is the single
   most overturnable decision in the log.

3. **`unsigned integer` is its own row rather than folded into
   `integer`.** rustc's `TyKind` separates `Int` from `Uint`, and the
   CLR separates `ELEMENT_TYPE_I4` from `ELEMENT_TYPE_U4`. The
   compilers made the split; the union kept it. Six of twelve have it,
   and java has no unsigned type at all.

4. **rust's `Adt` splits three ways.** One `TyKind` variant covers
   struct, enum and union. Those are three different shapes in every
   other language in the set, so `Adt` was read onto the `struct`,
   `enum / tagged variant` and `class / object` rows rather than given
   a row of its own.

5. **go `slice`, ruby `Array`, php `array`, kotlin `List`, dart `List`,
   swift `Array` and python `list` all normalize to the one `list`
   row** — the growable-list entry ALREADY VERIFIED as the dominant
   `list`. rust's `Vec`, java's `ArrayList`, csharp's `List<T>` and
   cpp's `std::vector` normalize to the same row but are marked absent
   or qualified, because in those four the type is a LIBRARY type and
   does not appear in the compiler's enumeration at all. That is why
   the row reads 7 rather than 12.

6. **php presence is read from `gettype()` and from php's
   declaration-position type names, never from
   `get_declared_classes()`.** That list reports which extensions this
   build loaded — PDO, Phar, Socket, DateTime, FFI — which is a fact
   about the build, not about the language. The cost is visible and
   accepted: php's `WeakReference` and `WeakMap` are genuine core
   classes, and this rule marks them qualified rather than present.

7. **Families of adapter types fold to one row.** swift's roughly forty
   lazy, drop, prefix, flatten and joined sequence adapters, and
   python's `map`, `filter`, `zip`, `enumerate`, `reversed`, all fold
   into `iterator / sequence`. swift's `SIMD2` through `SIMD64` fold
   into `SIMD vector`. rustc's `Closure`, `Coroutine`,
   `CoroutineClosure` and `CoroutineWitness` fold into one
   `closure / coroutine / generator` row. Without folding, swift alone
   would contribute more entries than the other eleven combined.

8. **Twelve entries are marked MACHINERY and stay in the union.** A
   machinery entry is a type the compiler manipulates that no running
   program ever holds a value of: inference variables, java's
   `WILDCARD`, the CLR's `ELEMENT_TYPE_SENTINEL`, rustc's `Infer`. They
   are counted in the 59 rather than dropped, because dropping them
   would be a scope ruling and scope rulings are step B's. The mark
   lets step B remove all twelve in one stroke.

9. **rustc's `TyKind::Error` is filed under compiler-placeholder, not
   under error/exception.** It is rustc's marker for a type it could
   not compute, so that a broken compile can keep producing useful
   messages. It has nothing to do with a program's exception type, and
   putting the two in one row would have made `error / exception type`
   read 7 instead of 6 on a false match.

10. **cpp's `is_union` is filed two ways.** It counts as present under
    `struct / record`, because a C++ union is a value with storage that
    a program holds; and as qualified under the machinery row `union
    type`, because a type-level union ("a value is one of several
    types") is a different idea that C++ does not have.

11. **Three markers rather than two.** A binary present/absent would
    have forced a lie in roughly forty cells: go's `rune` is an alias
    for `int32` and not a distinct `reflect.Kind`; typescript's `Array`
    is a `lib.d.ts` interface and not a `TypeFlag`; dart's `void` is a
    keyword and not a `dart:core` declaration. `~` records these, and
    every `~` cell carries a one-line reason in `type_union.json`.

12. **Nothing was invented.** An entry exists only where at least one
    language's own enumeration produced it. No row was added because
    the set looked incomplete without it.

13. **`decimal` therefore has no row, and that refutes the CORE's
    first-pass expectation.** The expectation named csharp's decimal as
    a single-language type worth carrying. The measurement says
    otherwise: the CLR's `CorElementType` has no decimal tag —
    `System.Decimal` is an `ELEMENT_TYPE_VALUETYPE` struct in the class
    library — and no other target ships an exact base-10 fractional
    type in its core. Decimal is a library type in all twelve, so it
    never entered the union.

---

## §5 — the fifteen single-language entries

A single-language entry has exactly one `x`. Per the owner's ruling of
2026-08-14 — "if they truly dont have equivalents in other languages,
not a problem. in fact, its those gaps the Hub is trying to fill" —
these stay in the union rather than being pruned as noise. They are
listed here so they are inspectable in one place.

Data entries, ten of them:

- **rational number — ruby.** `Rational`, exact fractions. No other
  target has one in core.
- **byte buffer / raw bytes — python.** `bytes`, `bytearray`,
  `memoryview`. go, ruby and php are marked `~`: their strings are
  byte-oriented, so the shape exists without a type of its own.
- **weak reference — dart.** `WeakReference`, `Expando`, `Finalizer`.
  php is `~` only because of decision 6.
- **channel — go.** `chan`. This is the CORE's own worked example of a
  single-language type. ruby is `~`: `Queue` and `SizedQueue` are core
  classes but thread queues rather than a type form.
- **optional wrapper — swift.** `Optional`. Four other languages have
  optionality without a type for it: rust's `Option` is a library enum
  absent from `TyKind`, and typescript, kotlin and dart all spell it as
  a modifier on another type.
- **lazy value — kotlin.** `Lazy`, `LazyThreadSafetyMode`.
- **atomic cell — kotlin.** `AtomicInt`, `AtomicLong`, `AtomicBoolean`,
  `AtomicReference`, `AtomicArray`. java has these too, but in
  `java.util.concurrent.atomic`, a library, so java reads absent.
- **SIMD vector — swift.** `SIMD2` through `SIMD64`, `SIMDMask`, and
  the `SIMD` and `SIMDScalar` protocols. cpp has vector extensions but
  they are compiler extensions, not part of the standard's type
  categories, so cpp reads absent.
- **uri — dart.** The weakest data row in the table: parsed text that
  only dart puts in its core.
- **text builder — dart.** `StringBuffer`, `StringSink`. java's
  `StringBuilder` and python's `io.StringIO` are library types.

Machinery entries, five of them:

- **wildcard — java.** `WILDCARD`, a bounded unknown type argument.
- **type operator — typescript.** `Conditional`, `Index`,
  `IndexedAccess`, `StringMapping`, `Mapped`, `ReverseMapped`.
  typescript alone computes types from other types.
- **opaque / foreign type — rust.** `Foreign` plus the `Opaque` alias
  kind.
- **unsafe binder — rust.** `UnsafeBinder`.
- **pattern-restricted type — rust.** `Pat`.

rust holds three of the five machinery singles; typescript and java one
each.

---

## §6 — what step B now asks the owner to rule

Six rulings, in the order they unblock the most work. Only the first is
strictly required to start census work.

1. **Which of the 47 data entries become instruments.** The six exist
   already. The remaining 41 are candidates, and the fracture-rich ones
   the CORE flagged in advance — nothing/unit, function — are rows 34
   and 25 of the table.

2. **Which entries are derived from an existing instrument rather than
   new.** Four obvious candidates, each of which would reduce the count
   without losing coverage: `set` as a dict with ignored values;
   `bigint` as integer without the width; `slice / view` as a list that
   does not own its storage; `fixed-size array` as a list that cannot
   grow.

3. **Whether the twelve MACHINERY entries are out of scope wholesale.**
   They are types no program holds a value of. If they are out, the
   union drops from 59 to 47 in one ruling.

4. **Whether the `integer` / `bigint` split stands.** §4 decision 2. If
   it collapses, `integer` reads 12 of 12 and the union drops to 58.

5. **Whether the three weakest data rows stay.** `uri`, `text builder`
   and `date-time / duration` are the rows most likely to be library
   conveniences that happened to land in a core namespace.

6. **The build order.** The CORE already says the fracture-rich pages
   will need longer census pages and a real hand pass; deciding which
   three or four to write first sets what phase 2 of the census does.

---

## §7 — where everything is

- Raw per-language extractions, verbatim names with source and
  confidence: `PseudoCoupHQ/Research/type_vocabulary/raw/`
  — twelve files, `<language>.types.json`.
- The union program, with every mapping written out in one table:
  `PseudoCoupHQ/Research/type_vocabulary/union.py`.
  Run it with
  `python3 PseudoCoupHQ/Research/type_vocabulary/union.py`.
- The union itself:
  `PseudoCoupHQ/Research/type_vocabulary/type_union.json`
  (machine-readable, one entry per row with per-language marker, raw
  spelling, and note) and
  `PseudoCoupHQ/Research/type_vocabulary/type_union.md`
  (the §3 table on its own).
- The lane scripts that did the extraction, archived by the daemon:
  `SandboxDesign/agent/drop/.done/` — `tv_probe.sh`,
  `tv_extract.sh`, `tv_extract2.sh`, `tv_extract3.sh`,
  `tv_extract4.sh`, `tv_extract5.sh`. Their raw text products are in
  `SandboxDesign/agent/out/` as `tv_*.txt`.
