"""Data source for build_intentions.py: the copied-forward verdict data plus the four slicer-steering extensions.

PROVENANCE (vendored, copy-forward):
    Source 1: ~/Programming/PseudoCoup_v5/Designing/intention_tables_gen.py
              (LANGS, CATS, T1, T2, DIAG, PRIMS, OPS -- verbatim data;
               the HTML rendering half of that file is NOT vendored)
    Source 2: ~/Programming/PseudoCoup_v5/Designing/build_verdicts.py
              (BASIS, LATTICE -- BASIS expanded from its row() helper
               to literal dicts, value-identical)
    Copied forward: 2026-07-28. Maintained in PCv6 from now on;
    PCv5 is archived research and is never written back to.

EXTENSION DATA (the four fields of CORE 0_0_4_0), lifted by reading:
    ROW_SATISFIERS  from ~/Programming/PseudoCoup_v5/Designing/intention_row_satisfiers.md
                    and  ~/Programming/PseudoCoup_v5/Designing/BEJ_expansion.md
    CANON           from the pc_verdict strings in Source 1 (explicit
                    entries; each cites the verdict string it came from)
    MINIMUM_SET     from ~/Programming/PseudoCoup_v5/Designing/minimum_intention_set.md
    POLICIES and POLICY_REFS
                    from ~/Programming/PseudoCoup_v5/Designing/PCv7_policy_decisions.md
                    and the "policy N" mentions in the pc_verdict strings
"""

# ---------------------------------------------------------------
# Copied-forward data (Source 1)
# ---------------------------------------------------------------

LANGS = ["Python", "Dart", "Go", "Kotlin", "Java", "C#",
         "TypeScript", "Swift", "Rust", "C++", "Ruby", "PHP"]

CATS = [
    ("A", "suspension", "async/await, coroutines, generators"),
    ("B", "channels", "message-passing concurrency"),
    ("C", "optionals", "null safety, absence in types"),
    ("D", "pattern matching", "structural choice"),
    ("E", "dispatch", "interfaces, traits, protocols"),
    ("F", "generics", "parameterization by type"),
    ("G", "scoped cleanup", "defer, RAII, using, with"),
    ("H", "events", "callbacks, delegates, streams"),
    ("I", "operator overloading", "user meanings for operators"),
    ("J", "metaprogramming", "reflection, macros, codegen"),
]

# ---- table 1 cells: T1[cat_key][lang] ----
T1 = {
"A": {
 "Python": "async/await + generators; cooperative event loop (asyncio); interpreted, not compiled transform",
 "Dart": "async/await + async* generators; one event loop per isolate; compiler state-machine",
 "Go": "— (goroutines subsume the intent; see channels row)",
 "Kotlin": "suspend functions; compiler state-machine; adds structured concurrency scopes",
 "Java": "— as syntax; virtual threads instead: make blocking cheap, hide suspension rather than spell it",
 "C#": "origin of async/await; Task as first-class handle; the reference state-machine transform",
 "TypeScript": "async/await lowered to promises/generators; single-threaded event loop",
 "Swift": "async/await + actors; structured concurrency like Kotlin",
 "Rust": "async fn compiles to a state-machine VALUE (Future); inert until polled; runtime is a library choice",
 "C++": "C++20 coroutines: rawest form — transform exposed as customization points; no standard runtime",
 "Ruby": "Fibers: explicit resume, no async syntax; scheduler hook since 3.0",
 "PHP": "Fibers since 8.1; no async syntax; rare under request-per-process model",
},
"B": {
 "Python": "library queues (queue, asyncio, multiprocessing); GIL limits parallelism",
 "Dart": "isolates + ports: messaging is the ONLY concurrency; purest actor stance",
 "Go": "channels + goroutines are the language identity; select is syntax-level",
 "Kotlin": "Channel/Flow in the coroutines library",
 "Java": "BlockingQueue library; virtual threads make thread-per-message viable",
 "C#": "System.Threading.Channels library",
 "TypeScript": "postMessage between workers; structured clone — no shared objects",
 "Swift": "actors at language level; AsyncStream",
 "Rust": "std mpsc; unique: Send trait — transfer safety proven at compile-time",
 "C++": "— in std; third-party libraries",
 "Ruby": "Ractors (experimental), isolate-like",
 "PHP": "—",
},
"C": {
 "Python": "None + Optional hint; unenforced",
 "Dart": "sound null safety in the type system (T?)",
 "Go": "nil + (value, ok) multiple-return idiom; no type-level option",
 "Kotlin": "T? enforced in the type system",
 "Java": "Optional&lt;T&gt; as a library object; null remains everywhere else",
 "C#": "nullable reference types, opt-in annotations; Nullable&lt;T&gt; for values",
 "TypeScript": "union types T | null | undefined; strictNullChecks flag",
 "Swift": "Optional IS an enum — sum type with ? ! sugar",
 "Rust": "Option&lt;T&gt; pure sum type; no null exists at all — strongest form",
 "C++": "std::optional for values only; raw pointers still null",
 "Ruby": "nil object; no static story",
 "PHP": "?T in declarations; loosely enforced",
},
"D": {
 "Python": "match/case (3.10), structural; no exhaustiveness check",
 "Dart": "patterns (Dart 3); exhaustive over sealed types",
 "Go": "type switch only",
 "Kotlin": "when + smart casts; sealed exhaustiveness; shallow destructuring",
 "Java": "switch patterns + record deconstruction; sealed exhaustive",
 "C#": "rich patterns in switch expressions",
 "TypeScript": "— native; discriminated unions + narrowing carry the intent",
 "Swift": "switch patterns; exhaustiveness enforced",
 "Rust": "match is central: exhaustive, deep destructuring — reference realization",
 "C++": "— native; std::visit as workaround",
 "Ruby": "case/in (3.0), structural",
 "PHP": "match expression (8.0): value-only, no destructuring",
},
"E": {
 "Python": "duck typing; Protocols structural but unenforced; ABCs",
 "Dart": "every class IS an implicit interface — unique",
 "Go": "structural interfaces, implicit satisfaction — no conformance declaration",
 "Kotlin": "nominal interfaces + default methods",
 "Java": "nominal interfaces; the archetype",
 "C#": "nominal + default impls; explicit implementation option",
 "TypeScript": "structural everywhere — interfaces are shapes, not contracts",
 "Swift": "protocols + extensions + associated types; protocol-oriented identity",
 "Rust": "traits with coherence (orphan rule); monomorphized by default, dyn opt-in",
 "C++": "— as such; virtual classes or templates; concepts (C++20) are structural constraints",
 "Ruby": "duck typing + modules as mixins",
 "PHP": "nominal interfaces + traits (mixins)",
},
"F": {
 "Python": "hints only; erased, unenforced",
 "Dart": "reified — run-time visible",
 "Go": "type parameters (1.18), constraint interfaces; deliberately minimal",
 "Kotlin": "erased on JVM; reified-inline trick",
 "Java": "erasure — the canonical erased generics",
 "C#": "reified in the CLR — run-time knows T",
 "TypeScript": "fully erased; types vanish at run-time",
 "Swift": "witness tables; associated types",
 "Rust": "monomorphization: compile-time copy per type; zero-cost",
 "C++": "templates — monomorphization origin; compile-time duck typing until concepts",
 "Ruby": "— (RBS external annotations only)",
 "PHP": "— (docblocks for analyzers only)",
},
"G": {
 "Python": "with + context managers (__exit__)",
 "Dart": "try/finally only",
 "Go": "defer — fires at FUNCTION exit, not scope exit (unique gotcha)",
 "Kotlin": "use { } extension function",
 "Java": "try-with-resources (AutoCloseable)",
 "C#": "using statement/declaration + IDisposable",
 "TypeScript": "using declarations (recent TC39)",
 "Swift": "defer blocks — scope exit",
 "Rust": "Drop trait: automatic, ownership-driven — no spelling at use site",
 "C++": "RAII destructors — the origin; deterministic",
 "Ruby": "ensure + block-form idiom (File.open { })",
 "PHP": "try/finally; destructors semi-deterministic via refcount",
},
"H": {
 "Python": "callables everywhere; no language construct",
 "Dart": "Streams as the core idiom",
 "Go": "function values; channels often replace callbacks",
 "Kotlin": "lambdas + Flow",
 "Java": "functional interfaces + SAM conversion — function-as-value encoded as interface",
 "C#": "delegates + event ARE language constructs; multicast — unique",
 "TypeScript": "first-class functions; EventEmitter/DOM idioms",
 "Swift": "closures + AsyncSequence/Combine",
 "Rust": "closures with TYPED capture modes (move) — capture is part of the type",
 "C++": "lambdas with explicit capture lists — capture spelled manually",
 "Ruby": "blocks/procs/lambdas — three callable kinds; implicit block argument unique",
 "PHP": "closures + legacy string/array callables",
},
"I": {
 "Python": "dunder methods; open set",
 "Dart": "operator methods; fixed set",
 "Go": "— deliberately forbidden",
 "Kotlin": "operator fun; fixed conventions",
 "Java": "— forbidden",
 "C#": "static operator methods",
 "TypeScript": "— (none in JS)",
 "Swift": "can define NEW operator symbols + precedence — most permissive",
 "Rust": "trait-based (Add, Mul): overloading IS trait implementation",
 "C++": "origin; all existing operators, no new symbols",
 "Ruby": "operators are ordinary methods; open",
 "PHP": "—",
},
"J": {
 "Python": "maximal run-time: metaclasses, __getattr__, decorators, full introspection",
 "Dart": "— run-time (mirrors dead in Flutter); dev-time codegen instead",
 "Go": "reflect package (clunky run-time); go:generate dev-time",
 "Kotlin": "JVM reflection + KSP dev-time processing",
 "Java": "reflection + annotations + bytecode-manipulation ecosystem",
 "C#": "reflection + source generators + expression trees (code as data) — unique",
 "TypeScript": "metaprograms in the TYPE system (mapped/conditional types), erased — unique",
 "Swift": "Mirror read-only; macros (recent) dev-time",
 "Rust": "no run-time reflection; macros — powerful dev-time syntax transforms",
 "C++": "templates: accidentally Turing-complete dev-time metaprogramming; constexpr; no reflection",
 "Ruby": "maximal: method_missing, define_method, open classes — the language's identity",
 "PHP": "run-time reflection API + attributes + magic methods",
},
}

# ---- table 2: pairs. verdict in {"coexist","tension","conflict"} ----
T2 = {
 ("A","B"): ("coexist", "complementary; Kotlin ships both"),
 ("A","C"): ("coexist", "orthogonal"),
 ("A","D"): ("coexist", "orthogonal"),
 ("A","E"): ("tension", "async functions in interfaces (Rust's long pain); resolvable, now shipped there"),
 ("A","F"): ("tension", "generic async fns produce unnameable state-machine types; resolvable"),
 ("A","G"): ("tension", "suspension decouples scope exit from time; async cleanup still unsolved in Rust; needs async-aware scopes"),
 ("A","H"): ("tension", "overlapping intent: both push values later; canonicalize to streams"),
 ("A","I"): ("coexist", "orthogonal"),
 ("A","J"): ("tension", "the async transform IS dev-time metaprogramming; run-time reflection sees transformed code, not source; stage it"),
 ("B","C"): ("coexist", "orthogonal"),
 ("B","D"): ("coexist", "synergy: select is matching over channels"),
 ("B","E"): ("coexist", "orthogonal"),
 ("B","F"): ("coexist", "synergy: typed channels need generics"),
 ("B","G"): ("tension", "handoff moves cleanup responsibility across executors; ownership (Send) resolves"),
 ("B","H"): ("coexist", "two spellings of messaging; canonicalizable"),
 ("B","I"): ("coexist", "orthogonal"),
 ("B","J"): ("coexist", "orthogonal"),
 ("C","D"): ("coexist", "designed together: option is a sum type, match consumes it"),
 ("C","E"): ("tension", "optional interface members reopen null holes (Swift @objc); forbid them"),
 ("C","F"): ("coexist", "synergy: Option&lt;T&gt; requires generics"),
 ("C","G"): ("coexist", "orthogonal"),
 ("C","H"): ("coexist", "unset-handler nullability is a minor rule"),
 ("C","I"): ("coexist", "orthogonal"),
 ("C","J"): ("conflict", "run-time attribute synthesis (method_missing) breaks null-safety proofs; only staging metaprogramming to dev-time saves both"),
 ("D","E"): ("tension", "exhaustiveness needs closed sets, interfaces are open; sealed hierarchies resolve"),
 ("D","F"): ("coexist", "orthogonal"),
 ("D","G"): ("coexist", "orthogonal"),
 ("D","H"): ("coexist", "orthogonal"),
 ("D","I"): ("tension", "custom equality can lie to the matcher (Python __eq__ in match); rule needed"),
 ("D","J"): ("conflict", "run-time class mutation invalidates exhaustiveness proofs; stage to dev-time"),
 ("E","F"): ("tension", "structural vs nominal conformance both needed; constraint systems differ; origin qualifiers resolve"),
 ("E","G"): ("coexist", "synergy: Disposable IS an interface"),
 ("E","H"): ("coexist", "synergy: listener interfaces"),
 ("E","I"): ("coexist", "synergy: trait-based operators (Rust) is the clean resolution"),
 ("E","J"): ("tension", "reflection over structural/erased types is ill-defined; stage it"),
 ("F","G"): ("coexist", "orthogonal"),
 ("F","H"): ("coexist", "orthogonal"),
 ("F","I"): ("coexist", "generic operators are fine"),
 ("F","J"): ("tension", "reified-vs-erased decides what reflection sees; C++ templates are BOTH generics and metaprogramming — split into parametric generics + staged macros"),
 ("G","H"): ("conflict", "a callback capturing a resource outlives the owning scope; deterministic cleanup vs escaping closures (divergence class 4); ownership or GC must arbitrate"),
 ("G","I"): ("coexist", "orthogonal"),
 ("G","J"): ("tension", "generated code must join the cleanup discipline; minor"),
 ("H","I"): ("coexist", "orthogonal"),
 ("H","J"): ("coexist", "synergy: event wiring is metaprogramming's favorite use"),
 ("I","J"): ("tension", "both let one spelling mean new things; compounds implicit-uniqueness risk; origin qualifiers mitigate"),
}

DIAG = {
 "A": "internal merge: event-loop vs polled-future models — pick canonical",
 "B": "internal merge: channel vs actor vs port — pick canonical",
 "C": "internal merge: sum type is the canonical; null is the legacy spelling",
 "D": "internal merge: exhaustive deep matching is the canonical superset",
 "E": "internal merge: structural vs nominal — both kept, qualifier-selected",
 "F": "internal merge: reified vs erased vs monomorphized — pick canonical",
 "G": "internal merge: scope-exit is canonical; function-exit (Go defer) is the variant",
 "H": "internal merge: streams as canonical superset",
 "I": "internal merge: fixed operator set is safer; new symbols (Swift) at own risk",
 "J": "internal merge: dev-time macros canonical; run-time mutation forbidden",
}

# ---- table 3: primitive data structures. (id, name, 12 cells, PC verdict) ----
PRIMS = [
("P1","bool",
 ["native; truthiness in conditions","native","native, strict","native","native","native",
  "native; truthy/falsy","native","native, strict","native + int conversion",
  "native; only nil/false falsy","native; loose truthiness"],
 "type uniform; PC.bool. condition-truthiness legislated: bool only"),
("P2","fixed-width signed int",
 ["— (bigint only)","int64; web target: JS number caveat","int8–64; silent wrap","Int/Long; silent wrap",
  "int/long; silent wrap","wrap default; checked opt-in","— (number + bigint)","traps on overflow",
  "debug trap / release wrap; explicit wrapping_* ops","signed overflow is UB","— (auto bigint)",
  "— (overflow becomes float)"],
 "PC.int64: trap on overflow; wrapping only by explicit spelling (Swift/Rust canon)"),
("P3","unsigned int",
 ["—","—","uint8–64","UInt family","— (helper methods)","full family","—","full family",
  "full family; explicit conversions","full family; permissive mixing","—","—"],
 "PC.uint*: Rust canon — explicit conversions, no implicit mixing"),
("P4","big int",
 ["native, seamless literals","— (removed)","math/big library","java BigInteger","BigInteger",
  "BigInteger","BigInt native","— (libraries)","— (crates)","— (libraries)","native, seamless",
  "GMP extension"],
 "PC.bigint = Python/Ruby seamlessness; polyfilled elsewhere"),
("P5","float64",
 ["IEEE754","IEEE754","IEEE754","IEEE754","IEEE754","IEEE754","IEEE754 — the ONLY number type",
  "IEEE754","IEEE754","IEEE754; x87/FMA edge cases","IEEE754","IEEE754"],
 "already uniform; PC.float64; legislate printing + NaN edges"),
("P6","decimal",
 ["decimal module","— libs","— libs","java BigDecimal","BigDecimal","native decimal type","— libs",
  "Foundation Decimal","— crates","— libs","BigDecimal stdlib","bcmath"],
 "intent from C# (language-level); PC.decimal as self-hosted polyfill"),
("P7","string",
 ["code-point sequence","UTF-16 units","UTF-8 bytes + runes","UTF-16","UTF-16","UTF-16","UTF-16",
  "grapheme clusters + explicit views (utf8/utf16/scalars)","UTF-8; byte-explicit; String/&amp;str",
  "bare bytes, encoding-blind","per-string encoding tag","bytes + mbstring"],
 "PC.string = Swift view model: no default indexing unit; explicit view per access — subsumes every cell"),
("P8","bytes",
 ["bytes/bytearray","Uint8List","[]byte","ByteArray","byte[]","byte[]","Uint8Array","Data",
  "Vec&lt;u8&gt;","vector&lt;uint8_t&gt;","String with BINARY encoding (conflated)",
  "string doubles as bytes (conflated)"],
 "uniform; PC.bytes distinct type; Ruby/PHP string-conflation rejected"),
("P9","list",
 ["list","List","slice: shared backing array; append aliasing hazard","List/MutableList read-write split",
  "ArrayList","List&lt;T&gt;","Array; sparse holes hazard","value semantics, copy-on-write",
  "Vec: single owner","vector","Array","array = ordered map, not a list"],
 "PC.list = single-owner Vec semantics (no aliasing surprises); go.slice / php.array as borrows"),
("P10","map",
 ["dict: insertion-ordered","Map default insertion-ordered","deliberately randomized order",
  "mapOf preserves order","HashMap unordered; LinkedHashMap opt-in","Dictionary order undefined",
  "Map insertion-ordered","unordered","HashMap unordered; BTreeMap sorted","map sorted; unordered_map",
  "Hash insertion-ordered","insertion-ordered"],
 "PC.map = insertion-ordered (majority + determinism); unordered as explicit perf borrow"),
("P11","set",
 ["set: unordered","Set default insertion-ordered","— (map-keys idiom)","setOf preserves order",
  "HashSet unordered","HashSet unordered","Set insertion-ordered","unordered",
  "HashSet unordered; BTreeSet sorted","set sorted","Set insertion-ordered","— (array-keys idiom)"],
 "PC.set = insertion-ordered (JS/Dart canon)"),
("P12","record / struct",
 ["class: reference","class: reference","struct: VALUE — copies on assignment","data class: reference",
  "record: reference, shallow-immutable","class ref AND struct value — both","object: reference",
  "struct value (COW) AND class ref — both","struct + ownership (move)","value by default",
  "Struct: reference","class: reference"],
 "PC.record = reference + explicit .copy() (policy 6); value structs as go.struct / swift.struct borrows"),
]

# ---- table 4: primitive operators. (id, name, 12 cells, PC verdict) ----
OPS = [
("O1","integer division / modulo",
 ["// floor; % sign follows divisor","~/ truncates","truncates","truncates; floorDiv in stdlib",
  "truncates; Math.floorDiv","truncates","no int div; Math.trunc(a/b)","truncates",
  "truncates; div_euclid available","truncates","floor (like Python)","intdiv truncates"],
 "PC: named family floor_div / trunc_div / euclid_div; bare / on ints requires qualifier"),
("O2","equality",
 ["== value (__eq__); is = identity","== value, overridable; identical()","== structural on comparable types",
  "== value / === identity — cleanest split","== is IDENTITY; .equals value (hazard)",
  "== varies by type (hazard)","== coerces / === strict (hazard)","Equatable protocol","PartialEq trait",
  "overloadable","== value","== coerces / === strict (hazard)"],
 "PC: Kotlin split — == trait-based value, === identity; coercive equality rejected"),
("O3","ordering comparisons",
 ["chaining a&lt;b&lt;c; mixed types error","Comparable","ordered on ordered types","Comparable",
  "Comparable","IComparable","coerces mixed types (hazard)","Comparable","Ord trait: total order",
  "overloadable; spaceship &lt;=&gt;","&lt;=&gt; combined operator","coerces (hazard)"],
 "PC: Ord-trait total order; no cross-type comparison; chaining kept as sugar (lowers to and)"),
("O4","shifts",
 ["arbitrary precision shift","arithmetic","arithmetic on signed","shr / ushr named ops",
  "&gt;&gt; arith / &gt;&gt;&gt; logical extra op","type decides",
  "&gt;&gt; / &gt;&gt;&gt;; 32-bit truncation (hazard)","type decides + masking ops",
  "type decides: signed arith, unsigned logical","type decides; UB edges","arbitrary precision",
  "arithmetic"],
 "PC: Rust canon — shift meaning from operand type; no extra operator"),
("O5","boolean and/or",
 ["short-circuit; returns OPERAND value","strict bool","strict bool","strict bool; ?: elvis for defaults",
  "strict bool","strict bool; ?? for defaults","returns operand; ?? added to fix it",
  "strict bool; ?? for optionals","strict bool","strict bool (converts)","returns operand value",
  "strict-ish; ?? added"],
 "PC: strict bool result; the x-or-default intent gets the dedicated ?? spelling"),
("O6","concatenation / coercion",
 ["+ no coercion; str() required","no implicit coercion; interpolation","+ strings only, no coercion",
  "\"s\" + any coerces via toString","\"s\" + any coerces (hazard)","coerces via ToString",
  "\"1\"+1 coerces (hazard)","no coercion; interpolation","no + coercion; format!",
  "std::string + limited","no coercion; interpolation",". operator; numeric strings coerce in + (hazard)"],
 "PC: no implicit coercion (Python/Go/Swift canon); interpolation as the ergonomic spelling"),
("O7","indexing",
 ["checked (IndexError); negative = from-end; slices","checked","checked (panic)","checked; getOrNull opt-in",
  "checked (exception)","checked; ^i from-end index — unique","out-of-range returns undefined (hazard)",
  "checked (precondition)","checked (panic); .get returns Option","[] UNCHECKED UB; .at checked",
  "out-of-range returns nil (hazard)","notice + null (hazard)"],
 "PC: checked with error; opt-in Option-returning .get; from-end by explicit marker (C# ^), not bare negative"),
]

# ---------------------------------------------------------------
# Copied-forward data (Source 2): basis audit matrix and border
# lattice, exactly as build_verdicts.py assembles them.
# ---------------------------------------------------------------

BASIS = {
    "bool": {lang: "native" for lang in LANGS},
    "int64": {
        "Python": "cheap:bigint-mask-trap", "Dart": "native",
        "Go": "native", "Kotlin": "native+trap", "Java": "native+trap",
        "C#": "native+trap", "TypeScript": "solved:BigInt.asIntN",
        "Swift": "native+trap", "Rust": "native+trap", "C++": "native+trap",
        "Ruby": "cheap:bigint-mask-trap", "PHP": "cheap:float-drift",
    },
    "float64": {lang: "native" for lang in LANGS},
    "bytes": {
        "Python": "native", "Dart": "native", "Go": "native",
        "Kotlin": "native", "Java": "native", "C#": "native",
        "TypeScript": "native", "Swift": "native", "Rust": "native",
        "C++": "native", "Ruby": "cheap:conflated", "PHP": "cheap:conflated",
    },
    "list": {
        "Python": "native", "Dart": "native", "Go": "cheap:slice-alias-detach",
        "Kotlin": "native", "Java": "native", "C#": "native",
        "TypeScript": "cheap:unchecked-idx", "Swift": "cheap:cow-value-copy",
        "Rust": "native:move", "C++": "cheap:value-copy",
        "Ruby": "cheap:nil-idx", "PHP": "cheap:value-copy",
    },
    "record": {
        "Python": "native", "Dart": "native", "Go": "cheap:value-copy",
        "Kotlin": "native", "Java": "native", "C#": "native",
        "TypeScript": "native", "Swift": "native", "Rust": "native:move",
        "C++": "cheap:value-copy", "Ruby": "native", "PHP": "native",
    },
    "function_value": {
        "Python": "native", "Dart": "native", "Go": "native",
        "Kotlin": "native", "Java": "cheap:functional-interface",
        "C#": "native", "TypeScript": "native", "Swift": "native",
        "Rust": "native", "C++": "native", "Ruby": "native", "PHP": "native",
    },
    "hashing": {
        "Python": "native:insertion", "Dart": "native:insertion",
        "Go": "cheap:randomized", "Kotlin": "native:insertion",
        "Java": "cheap:LinkedHashMap", "C#": "cheap:undefined-order",
        "TypeScript": "native:insertion", "Swift": "cheap:unordered",
        "Rust": "cheap:unordered", "C++": "cheap:order",
        "Ruby": "native:insertion", "PHP": "native:insertion",
    },
    "executor": {
        "Python": "exposed", "Dart": "withheld", "Go": "exposed",
        "Kotlin": "exposed", "Java": "exposed", "C#": "exposed",
        "TypeScript": "withheld", "Swift": "exposed", "Rust": "exposed",
        "C++": "exposed", "Ruby": "exposed", "PHP": "withheld",
    },
}

LATTICE = [
    {"class": 1, "name": "value-model",
     "crossing": "declared width/semantics differs (e.g. int64 -> bigint)",
     "verdict": "convertible", "spelling": "widen / explicit mask+trap"},
    {"class": 2, "name": "copy-model",
     "crossing": "value-semantics object -> reference-model frame",
     "verdict": "convertible", "spelling": ".copy() at the border"},
    {"class": 2, "name": "copy-model",
     "crossing": "aliasing is load-bearing across the border",
     "verdict": "incompatible", "spelling": None},
    {"class": 3, "name": "evaluation-order",
     "crossing": "none — egress rule (temporaries), no border object",
     "verdict": "identical", "spelling": None},
    {"class": 4, "name": "lifetime",
     "crossing": "resource object -> frame with different cleanup regime",
     "verdict": "convertible", "spelling": "explicit scope wrapper"},
    {"class": 5, "name": "dispatch",
     "crossing": "structurally-conforming type -> nominal slot",
     "verdict": "convertible", "spelling": "as <Interface>"},
    {"class": 6, "name": "collection-order",
     "crossing": "unordered (perf-borrow) collection -> ordered frame",
     "verdict": "convertible", "spelling": "explicit ordering step"},
    {"class": 7, "name": "concurrency",
     "crossing": "mutable object across spawn boundary",
     "verdict": "incompatible", "spelling": "freeze() or .copy() instead"},
    {"class": 7, "name": "concurrency",
     "crossing": "immutable / ownership-transferred object across spawn",
     "verdict": "convertible", "spelling": "send (transfer proof at dev-time)"},
    {"class": 8, "name": "encoding",
     "crossing": "string between view expectations",
     "verdict": "convertible", "spelling": "explicit view (utf8/utf16/points)"},
    {"class": "J3", "name": "dynamic-mode",
     "crossing": "object leaving a mode-dynamic frame",
     "verdict": "convertible", "spelling": "re-validate (proofs stripped)"},
]

# ---------------------------------------------------------------
# Extension field 1: ROW_SATISFIERS
# Lifted by reading intention_row_satisfiers.md (per-row verdicts
# table + status section) and BEJ_expansion.md (the in-hub solutions
# for the winner-less rows B, E, J). One entry per category A-J.
# "native": languages whose realization satisfies the row natively.
# "in_hub": how the row is solved in-hub when no language satisfies
# it (or how the satisfier is narrowed); null when the native
# satisfier is adopted whole.
# ---------------------------------------------------------------

ROW_SATISFIERS = {
 "A": {"satisfier": "Rust", "kind": "single", "native": ["Rust"],
       "in_hub": None, "status": "preliminarily solved",
       "basis": "state-machine-as-value is the row's lowest form; every other cell is it plus a bundled runtime choice (event loop = executor atop polled futures; Java's hidden suspension = a scheduler service decision)",
       "policies": [8]},
 "B": {"satisfier": None, "kind": "none", "native": [],
       "in_hub": "three-virtue composite: Go's ergonomics (channel/spawn/select spellings, scheduler polyfill) + Dart's isolation guarantee (dev-time border check: no mutable object crosses spawn) + Rust's transfer proof (send checked at dev-time, a Ledger judgment)",
       "in_hub_from": ["Go", "Dart", "Rust"],
       "status": "open — solved in-hub",
       "basis": "virtues don't co-occur: Go has ergonomics + select; Dart has the isolation guarantee; Rust has the transfer proof (Send). No language holds all three",
       "policies": [12]},
 "C": {"satisfier": "Rust", "kind": "single", "native": ["Rust"],
       "in_hub": None, "status": "preliminarily solved",
       "basis": "Option<T> with no null in the language; every other cell is it weakened (sugar removed, enforcement removed, or null retained alongside)",
       "policies": [8]},
 "D": {"satisfier": "Rust", "kind": "single", "native": ["Rust"],
       "in_hub": None, "status": "preliminarily solved",
       "basis": "exhaustive + deep destructuring subsumes the row; C#'s pattern richness reduces to guards",
       "policies": [8]},
 "E": {"satisfier": None, "kind": "none", "native": [],
       "in_hub": "dual conformance regimes, qualifier-selected (go.interface structural, java.interface nominal); run-time residue identical (map from type to function); structural-into-nominal requires explicit `as` spelling",
       "in_hub_from": ["Go", "TypeScript", "Java", "Kotlin"],
       "status": "open — solved in-hub",
       "basis": "structural (Go/TS) and nominal (Java/Kotlin) conformance are different intentions; no language offers both first-class. The row origin qualifiers exist for",
       "policies": [13]},
 "F": {"satisfier": "C#", "kind": "single-with-reassignment", "native": ["C#"],
       "in_hub": "restricted below C#: dev-time parameterization only, no run-time type queries (reification is a permission and egresses hard)",
       "status": "preliminarily solved",
       "basis": "reified subsumes erased; C++ template computation reassigned to row J, leaving pure parameterization, which C# covers",
       "policies": [9]},
 "G": {"satisfier": "Rust", "kind": "single", "native": ["Rust"],
       "in_hub": None, "status": "preliminarily solved",
       "basis": "Drop is automatic; every explicit spelling (with, using, defer, ensure) is a drop-guard value; Go's function-exit variant reproducible",
       "policies": [8]},
 "H": {"satisfier": "composite", "kind": "composite", "native": ["C#", "Dart"],
       "in_hub": "streams as the canonical superset, built as the derived object (collection of function-values + suspension); born as a polyfill, egress is its definition",
       "status": "preliminarily solved",
       "basis": "streams subsume callbacks/delegates/multicast; best native versions in C#/Dart, but the true satisfier is the derived object (collection of function-values + suspension)",
       "policies": [10]},
 "I": {"satisfier": "Swift (power) / Rust (mechanism)", "kind": "dual",
       "native": ["Swift", "Rust"],
       "in_hub": "trait-based operator overloading (Rust mechanism); novel symbols (Swift) at-own-risk",
       "status": "preliminarily solved",
       "basis": "Swift: new symbols + precedence, everything else a subset. Rust: overloading-as-trait, the cleanest mechanism for a merged language",
       "policies": [11]},
 "J": {"satisfier": None, "kind": "none-deliberate", "native": [],
       "in_hub": "the row is truncated, not satisfied: J1 dev-time codegen unrestricted; J2 run-time read as closed-world reflection over the Ledger (egress emits metadata tables); J3 run-time write gated by the egress-coverage analyzer (narrow target set + voided proofs, knowingly accepted)",
       "in_hub_from": ["Python", "Ruby"],
       "status": "open — truncated in-hub",
       "basis": "the row spans three stages (run-time mutation, dev-time transforms, type-level); table 2's conflicts show run-time mutation destroys the proofs everything else depends on. The row must be truncated (dev-time only), not satisfied",
       "policies": [14, 15, 16]},
}

# ---------------------------------------------------------------
# Extension field 2: CANON
# One explicit entry per primitive/operator verdict, extracted by
# reading the pc_verdict strings above (no regex guessing). Each
# entry cites the exact verdict string it came from; the builder
# refuses if the citation drifts from the vendored verdict.
# kind: "language"/"languages" = verdict names canon language(s);
# "uniform" = row already uniform; "legislated" = verdict states a
# rule with no single canon language (the statement says what the
# verdict actually says).
# ---------------------------------------------------------------

CANON = {
 "P1": {"kind": "uniform", "canon_languages": [],
        "statement": "type uniform; condition-truthiness legislated: bool only",
        "cites": "type uniform; PC.bool. condition-truthiness legislated: bool only"},
 "P2": {"kind": "languages", "canon_languages": ["Swift", "Rust"],
        "statement": "trap on overflow; wrapping only by explicit spelling (Swift/Rust canon)",
        "cites": "PC.int64: trap on overflow; wrapping only by explicit spelling (Swift/Rust canon)"},
 "P3": {"kind": "language", "canon_languages": ["Rust"],
        "statement": "Rust canon — explicit conversions, no implicit mixing",
        "cites": "PC.uint*: Rust canon — explicit conversions, no implicit mixing"},
 "P4": {"kind": "languages", "canon_languages": ["Python", "Ruby"],
        "statement": "Python/Ruby seamlessness; polyfilled elsewhere",
        "cites": "PC.bigint = Python/Ruby seamlessness; polyfilled elsewhere"},
 "P5": {"kind": "uniform", "canon_languages": [],
        "statement": "already uniform; legislate printing + NaN edges",
        "cites": "already uniform; PC.float64; legislate printing + NaN edges"},
 "P6": {"kind": "language", "canon_languages": ["C#"],
        "statement": "intent from C# (language-level); realized as self-hosted polyfill",
        "cites": "intent from C# (language-level); PC.decimal as self-hosted polyfill"},
 "P7": {"kind": "language", "canon_languages": ["Swift"],
        "statement": "Swift view model: no default indexing unit; explicit view per access",
        "cites": "PC.string = Swift view model: no default indexing unit; explicit view per access — subsumes every cell"},
 "P8": {"kind": "uniform", "canon_languages": [],
        "statement": "uniform; distinct bytes type; Ruby/PHP string-conflation rejected",
        "cites": "uniform; PC.bytes distinct type; Ruby/PHP string-conflation rejected"},
 "P9": {"kind": "language", "canon_languages": ["Rust"],
        "statement": "single-owner Vec semantics (Vec is Rust's realization, per the Rust cell); go.slice / php.array as borrows",
        "cites": "PC.list = single-owner Vec semantics (no aliasing surprises); go.slice / php.array as borrows"},
 "P10": {"kind": "legislated", "canon_languages": [],
         "statement": "insertion-ordered by majority + determinism; no single canon language; unordered as explicit perf borrow",
         "cites": "PC.map = insertion-ordered (majority + determinism); unordered as explicit perf borrow"},
 "P11": {"kind": "languages", "canon_languages": ["TypeScript", "Dart"],
         "statement": "insertion-ordered (JS/Dart canon; JS is represented by the TypeScript column in the 12)",
         "cites": "PC.set = insertion-ordered (JS/Dart canon)"},
 "P12": {"kind": "legislated", "canon_languages": [],
         "statement": "reference + explicit .copy(), legislated by policy 6; no single canon language; value structs as go.struct / swift.struct borrows",
         "cites": "PC.record = reference + explicit .copy() (policy 6); value structs as go.struct / swift.struct borrows"},
 "O1": {"kind": "legislated", "canon_languages": [],
        "statement": "named family floor_div / trunc_div / euclid_div; bare / on ints requires qualifier; no single canon language",
        "cites": "PC: named family floor_div / trunc_div / euclid_div; bare / on ints requires qualifier"},
 "O2": {"kind": "language", "canon_languages": ["Kotlin"],
        "statement": "Kotlin split — == trait-based value, === identity; coercive equality rejected",
        "cites": "PC: Kotlin split — == trait-based value, === identity; coercive equality rejected"},
 "O3": {"kind": "language", "canon_languages": ["Rust"],
        "statement": "Ord-trait total order (Ord trait is Rust's realization, per the Rust cell); no cross-type comparison; chaining kept as sugar",
        "cites": "PC: Ord-trait total order; no cross-type comparison; chaining kept as sugar (lowers to and)"},
 "O4": {"kind": "language", "canon_languages": ["Rust"],
        "statement": "Rust canon — shift meaning from operand type; no extra operator",
        "cites": "PC: Rust canon — shift meaning from operand type; no extra operator"},
 "O5": {"kind": "legislated", "canon_languages": [],
        "statement": "strict bool result; the x-or-default intent gets the dedicated ?? spelling; no single canon language",
        "cites": "PC: strict bool result; the x-or-default intent gets the dedicated ?? spelling"},
 "O6": {"kind": "languages", "canon_languages": ["Python", "Go", "Swift"],
        "statement": "no implicit coercion (Python/Go/Swift canon); interpolation as the ergonomic spelling",
        "cites": "PC: no implicit coercion (Python/Go/Swift canon); interpolation as the ergonomic spelling"},
 "O7": {"kind": "legislated", "canon_languages": ["C#"],
        "statement": "checked with error, legislated; opt-in Option-returning .get; from-end marker adopted from C# (^) — C# is cited only for the marker",
        "cites": "PC: checked with error; opt-in Option-returning .get; from-end by explicit marker (C# ^), not bare negative"},
}

# ---------------------------------------------------------------
# Extension field 3: MINIMUM_SET
# The 11-object minimum intention set, lifted by reading
# minimum_intention_set.md ("The set" section, post-audit form).
# ---------------------------------------------------------------

MINIMUM_SET = [
 {"n": 1, "object": "value",
  "desc": "number, boolean, byte, text"},
 {"n": 2, "object": "name",
  "desc": "a binding from a written identifier to a value"},
 {"n": 3, "object": "operation",
  "desc": "arithmetic, comparison, logic on values"},
 {"n": 4, "object": "sequence",
  "desc": "do this, then that"},
 {"n": 5, "object": "choice",
  "desc": "if"},
 {"n": 6, "object": "repetition",
  "desc": "while"},
 {"n": 7, "object": "function",
  "desc": "a parameterized block; call and return. a function IS a value: it can be named, passed, stored (amendment from the audit)"},
 {"n": 8, "object": "record",
  "desc": "values grouped under named fields"},
 {"n": 9, "object": "collection",
  "desc": "list (ordered many); map (keyed many)"},
 {"n": 10, "object": "mutation",
  "desc": "assignment to a name or field after creation"},
 {"n": 11, "object": "service call",
  "desc": "request to the platform: read, write, clock, display, network, spawn executor"},
]

# ---------------------------------------------------------------
# Extension field 4: POLICIES + POLICY_REFS
# POLICIES: the numbered entries of PCv7_policy_decisions.md
# (bold lead sentence of each). POLICY_REFS: explicit machine links
# from a verdict to the policy entries its pc_verdict string cites.
# One "policy N" mention exists in the verdict strings today (P12);
# the builder refuses if a mention appears without a ref, or a ref
# points at a policy number not listed here.
# ---------------------------------------------------------------

POLICIES = {
 "1": "Discipline assumed.",
 "2": "Proofs live in the hub, once.",
 "3": "Restriction egresses trivially; permission egresses hard.",
 "4": "One canonical semantics per declared type.",
 "5": "Machine-model classes (value-model, encoding): bit-exact simulators.",
 "6": "Language-model classes: legislated, not polyfilled.",
 "7": "Concurrency is a per-target capability flag.",
 "8": "A/C/D/G canonicalize on Rust.",
 "9": "F: generics restricted below C#.",
 "10": "H: streams as the canonical superset of events/callbacks.",
 "11": "I: trait-based operator overloading (Rust mechanism); novel symbols (Swift) at-own-risk.",
 "12": "B: the three-virtue composite.",
 "13": "E: dual conformance regimes, qualifier-selected.",
 "14": "J1 dev-time codegen: unrestricted.",
 "15": "J2 run-time read: closed-world reflection.",
 "16": "J3 run-time write: egress-coverage analyzer, not a ban.",
 "17": "Origin qualifiers.",
 "18": "Modes are coarse qualifiers.",
 "19": "Border grammar: three-way verdict.",
 "20": "Roundtrip is load-bearing.",
}

POLICY_REFS = [
 {"verdict_id": "P12", "policy": 6, "mention": "policy 6",
  "cites": "PC.record = reference + explicit .copy() (policy 6); value structs as go.struct / swift.struct borrows"},
]
