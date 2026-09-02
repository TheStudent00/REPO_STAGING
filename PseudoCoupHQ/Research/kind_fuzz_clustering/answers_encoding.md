# answers_encoding.md — how a layer-3 answer is written down

Written 2026-08-19 with the execution runs of log_031. It is the one
place the recording rule lives, so that comparing two languages' answers
is mechanical: read the bits, not a printed form.

## the rule

An answer is recorded at the moment the operation returns, inside the
language, before any formatting the language would choose for itself.
Two things are recorded.

- the **type name the language itself gives the result** — `int64` from
  go's reflect, `i64` from rust's `type_name`, `java.lang.String` from
  java's `getClass`, `System.Boolean` from c#'s `typeof(T)`
- the **content as bits** — integers as two's complement, floats as
  their IEEE bit pattern, text as bytes, containers as a recursive dump
  in the same encoding

No canonicalisation happens at run time. A float is never printed as a
decimal; it is printed as its 64 bits, and the reader decides whether
two languages agree.

## the line

```
PROBE_ID|TYPE_NAME|ENCODING:PAYLOAD
PROBE_ID|-|RAISE:<name>
PROBE_ID|-|DEATH:<rc>
PROBE_ID|-|CODEGEN_REFUSE:<message>
```

`PROBE_ID` is the value matrix's own id, `P<i>_<j>_<x>_<y>_<k>` —
holder i, holder j, value class x of i, value class y of j, operation k.
An answer row therefore joins to its verdict row by id.

## the encodings

| token | payload | meaning |
|---|---|---|
| `INT:<bits>:<hex>` | `bits/4` hex digits, big-endian | two's complement |
| `UINT:<bits>:<hex>` | `bits/4` hex digits, big-endian | unsigned |
| `BIGINT:<hex>` | sign then magnitude, or java's own byte array | arbitrary width |
| `FLOAT:<bits>:<hex>` | `bits/4` hex digits, big-endian | IEEE 754 bit pattern |
| `DEC128:<hex>` | 16 bytes | c# `decimal`, its four words |
| `BOOL:true` / `BOOL:false` | — | canonical token |
| `CHAR:<hex>` | code unit or code point in hex | java/kotlin/c# UTF-16 unit; rust scalar |
| `STR:<len>:<bytes>:<hex>` | the language's own length notion, then UTF-8 byte count, then those bytes | see below |
| `NULL` | — | null, nil, None, nullptr, nullopt |
| `UNDEFINED` | — | javascript only |
| `UNIT` | — | rust `()` |
| `SOME(<enc>)` | — | a present optional |
| `REF(<enc>)` | — | go pointer or interface, dereferenced |
| `PTR` | — | a non-null c++ pointer with no readable content |
| `LIST:<n>[<enc>,…]` | — | ordered container, in its own order |
| `MAP:<n>[<enc>=><enc>,…]` | — | keyed container, entries sorted by their encoded text |
| `TUP:<n>[<enc>,…]` | — | tuple |
| `STRUCT:<n>[<name>=<enc>,…]` | — | fields in declaration order |
| `RANGE[<enc>,<enc>,incl\|excl]` | — | rust and kotlin ranges |
| `ORD:LT\|EQ\|GT\|UN` | — | c++ `<=>` comparison categories |
| `ENUM:<n>` | — | a c++ enumeration's underlying value |
| `OPAQUE:<hex>` | UTF-8 bytes of the language's own `toString` | nothing better was available |

`STR`'s first number is the language's OWN length notion and the second
is always the UTF-8 byte count. They differ on purpose: java, kotlin,
c# and typescript count UTF-16 code units, go counts bytes, rust and
swift count scalar values, dart counts UTF-16 code units. Recording
both is what makes a text answer comparable at all.

`MAP` entries are sorted by their encoded text because several of the
languages' maps have no order of their own. That is the ONE place a
recording choice imposes an order, and it is stated here rather than
buried.

## where the type name comes from, per language

| language | type name | how a primitive keeps its identity |
|---|---|---|
| go | `reflect.TypeOf(v).String()` | go has no boxing; the dynamic type is the static one |
| rust | `std::any::type_name::<T>()` | `T` is inferred from `&_r`, so it is the static type |
| c++ | demangled `typeid(T).name()` | the recorder is a template; `T` is the static type |
| swift | `T.self` in a generic recorder | static type |
| dart | the type argument `T` of a generic recorder | static type |
| c# | `typeof(T).ToString()` | generic recorder, so `int` is not `object` |
| java | overload set: `boolean byte short char int long float double` plus `Object` | overload resolution keeps the primitive |
| kotlin | the same overload set, named `kotlin.Int` and so on | as java |
| typescript | `typeof`, then the constructor name for objects | the static type is erased before run time; this is a fact about the language, recorded, not patched |

## what is NOT an answer

Three non-answers are recorded as themselves and never as a value.

- `RAISE` — the operation was reached and threw. The name is the
  language's own exception class name.
- `DEATH` — the process died and the language could not catch it: a
  c++ `SIGFPE` on integer division by zero, a swift trap. The chunk
  binary takes a start index, so the runner restarts it past the corpse
  and the death costs exactly one probe.
- `CODEGEN_REFUSE` — the probe passed the checker that scored it ACCEPT
  and was then refused later in the same compiler. Swift is the case in
  hand: `swiftc -typecheck` accepts `let b: Int = 9223372036854775808`
  and full compilation refuses the same line. The message is kept
  verbatim.
