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
