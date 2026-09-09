# log_026 — where the `+` acceptance decision literally lives (compiler source shape check)

- scope: one question — "which operand-type pairs does binary `+` accept?" — traced to the literal
  source location in every compiler reachable inside the sandbox container.
- purpose: LAYER 3 (operation) planning. Testing the owner's intuition ("there is a branch that would
  catch an error, that logic must exist where it has literal code with something like
  `if var0==i64 and var1==f64: error`") against the counter-hypothesis (long nested call chains).
- method: SandboxDesign lane, four serial scripts (`recon_compilers.sh`, `extract_plus.sh`,
  `extract_plus2.sh`, `extract_plus3.sh`, `extract_plus4.sh`); all quotes are `cat -n` / `javap`
  output from files inside the container, not recalled.
- evidence levels used throughout: **measured** (quoted from a file or a run in the container),
  **derived** (computed from measured material), **estimate**, **unverified**.

---

## §1 — plain words, verdict per compiler in one line each

- the owner's intuition is **right for some compilers and wrong for others, and the split is not random**
  — it tracks whether the language's `+` rule is *closed* (a fixed set of primitive types) or
  *open* (user types can join in).
  - **go** — data-shaped. One map literal, one line for `+`, plus a bitmask predicate.
    `binaryOpPredicates` at `expr.go:760-774` says `token.ADD: allNumericOrString`. Extractable
    mechanically. *(measured)*
  - **java** — data-shaped: a literal 23-entry table of `(lhs, rhs, result, opcode)` built in
    `Operators.initBinaryOperators()`. Source file itself unreachable (dangling `src.zip` symlink),
    but the table is fully readable from the shipped bytecode via `javap -c`. *(measured)*
  - **typescript** — chain-shaped and the worst case: the `PlusToken` case is a flat branch, but
    every branch condition calls into the full structural-assignability engine, which is recursive
    and open. 9 named hops from "checker sees `a + b`" to verdict, and the tail is unbounded.
    *(measured)*
  - **rust** — data-shaped, but *the data is in the library, not the compiler*: `add_impl!` at
    `arith.rs:113` lists 16 primitive types; 12 `Add` impls total across `core`+`alloc`. The
    decision procedure (trait selection) is in rustc, whose source is **not** present. *(measured)*
  - **python** — source unreachable (no CPython C tree in the container); the acceptance set is
    observable from the running interpreter (20 accepted of 100 sampled pairs) and the slot
    mechanism (`__add__`/`__radd__`/`NotImplemented`) is directly observable. *(measured, runtime only)*
  - **kotlin / swift / c++** — no source present in the container (kotlinc/swiftc binaries only,
    no compiler sources); not reached. *(measured absence)*
- The one-line synthesis: **the flat extractable branch the owner expects exists, verbatim, in exactly
  the languages where `+` is closed over primitives (go, java, rust-the-library). It does not exist
  in the languages where `+` participates in an open subtype or protocol system (typescript,
  python).** *(derived)*

---

## §2 — per compiler: the quote, the shape, the chain, the extractability verdict

### §2.1 go — go1.26.0, `GOROOT=/usr/lib/go-1.26`

- **THE QUOTE** — `/usr/lib/go-1.26/src/go/types/expr.go:756-775` *(measured)*

  ```
  756: var binaryOpPredicates opPredicates
  757:
  758: func init() {
  759: 	// Setting binaryOpPredicates in init avoids declaration cycles.
  760: 	binaryOpPredicates = opPredicates{
  761: 		token.ADD: allNumericOrString,
  762: 		token.SUB: allNumeric,
  763: 		token.MUL: allNumeric,
  764: 		token.QUO: allNumeric,
  765: 		token.REM: allInteger,
  766:
  767: 		token.AND:     allInteger,
  768: 		token.OR:      allInteger,
  769: 		token.XOR:     allInteger,
  770: 		token.AND_NOT: allInteger,
  771:
  772: 		token.LAND: allBoolean,
  773: 		token.LOR:  allBoolean,
  774: 	}
  775: }
  ```

- the two accompanying halves of the rule, also literal *(measured)*
  - the *same-type* requirement, `expr.go:809-825`:

    ```
    809: 	if !Identical(x.typ, y.typ) {
    ...
    818: 			check.errorf(posn, MismatchedTypes, invalidOp+"%s (mismatched types %s and %s)", e, x.typ, y.typ)
    ...
    823: 		x.mode = invalid
    824: 		return
    825: 	}
    826:
    827: 	if !check.op(binaryOpPredicates, x, op) {
    828: 		x.mode = invalid
    829: 		return
    830: 	}
    ```
  - the refusal site itself, `expr.go:73-84`:

    ```
    73:  func (check *Checker) op(m opPredicates, x *operand, op token.Token) bool {
    74:  	if pred := m[op]; pred != nil {
    75:  		if !pred(x.typ) {
    76:  			check.errorf(x, UndefinedOp, invalidOp+"operator %s not defined on %s", op, x)
    77:  			return false
    78:  		}
    ```
  - the predicate bottoms out in a bitmask, `predicates.go:52,57-62,37-40` and `basic.go:63-65`:

    ```
    52:  func allNumericOrString(t Type) bool { return allBasic(t, IsNumeric|IsString) }
    57:  func allBasic(t Type, info BasicInfo) bool {
    58:  	if tpar, _ := Unalias(t).(*TypeParam); tpar != nil {
    59:  		return tpar.is(func(t *term) bool { return t != nil && isBasic(t.typ, info) })
    60:  	}
    61:  	return isBasic(t, info)
    62:  }
    37:  func isBasic(t Type, info BasicInfo) bool {
    38:  	u, _ := t.Underlying().(*Basic)
    39:  	return u != nil && u.info&info != 0
    40:  }
    64:  	IsNumeric   = IsInteger | IsFloat | IsComplex
    ```

- **THE SHAPE — (a) data-shaped, with a 3-line branch wrapper.** *(measured)*
  - the full `+` rule for named (non-generic, non-untyped) operands is exactly:
    `Identical(a, b) AND (a.info & (IsNumeric|IsString)) != 0`. Two literal predicates, one map entry.
  - chain trace, "checker sees `a + b`" → verdict, N = 6 named hops:

    | # | function | file:line | what it decides |
    |---|---|---|---|
    | 1 | `(*Checker).binary` | expr.go:779 | entry; evaluates both operands |
    | 2 | `(*Checker).matchTypes` | expr.go:875 | untyped-constant conversion only |
    | 3 | `Identical` | expr.go:809 | refuse if operand types differ |
    | 4 | `(*Checker).op` | expr.go:73 | look the operator up in the map, apply predicate |
    | 5 | `allNumericOrString` → `allBasic` | predicates.go:52,57 | type-param spread, else `isBasic` |
    | 6 | `isBasic` | predicates.go:37 | `u.info & info != 0` — verdict |
  - hops 2 and 5 are the only non-trivial ones and both are self-contained (~50 lines and ~6 lines).
    Nothing here re-enters the checker. *(measured)*

- **EXTRACTABILITY VERDICT — yes, mechanically, low cost.** *(derived)*
  - a lifter needs: (i) the `binaryOpPredicates` map literal, (ii) the `BasicInfo` bit constants
    from `basic.go:55-65`, (iii) the `Typ[...]` table of basic kinds and their `info` masks,
    (iv) the hard-coded `Identical` same-type rule.
  - a cross-check run inside the container reproduced the acceptance set from the lifted rule alone,
    without invoking the type-checker's expression path: 6 accepted pairs out of 8×8 sampled basic
    kinds (`int+int`, `int64+int64`, `uint8+uint8`, `float64+float64`, `complex128+complex128`,
    `string+string`; `bool` and `unsafe.Pointer` refused). *(measured)*
  - caveat: the lifted rule covers *typed, non-generic, non-defined* operands. Untyped constants
    (hop 2) and type parameters (hop 5, `tpar.is(...)`) each add a rule the lifter must also carry.

### §2.2 java — javac 25.0.3, OpenJDK 25

- **reachability**: `/usr/lib/jvm/java-25-openjdk-amd64/lib/src.zip` is present as a **dangling
  symlink** → `../../openjdk-25/src.zip`, target absent; a filesystem-wide `find / -name src.zip`
  returned only the dangling link. So **javac's Java source is not readable in this container**.
  The compiled classes are, in `lib/modules` and `jmods/jdk.compiler.jmod`. *(measured)*
- **THE QUOTE** — `javap --module jdk.compiler -p -c com.sun.tools.javac.comp.Operators`,
  method `initBinaryOperators()`, first entries *(measured)*

  ```
    private void initBinaryOperators();
      Code:
           2: getfield      #39   // Field binaryOperators:Ljava/util/Map;
           5: bipush        23
           7: anewarray     #385  // class com/sun/tools/javac/comp/Operators$BinaryOperatorHelper
          12: new           #387  // class com/sun/tools/javac/comp/Operators$BinaryStringOperator
          17: getstatic     #389  // Field com/sun/tools/javac/tree/JCTree$Tag.PLUS
          23: getstatic     #393  // Field ...Operators$OperatorType.STRING
          26: getstatic     #377  // Field ...Operators$OperatorType.OBJECT
          29: getstatic     #393  // Field ...Operators$OperatorType.STRING
          37: sipush        256
          41: invokevirtual #396  // Method ...BinaryStringOperator.addBinaryOperator:(OperatorType;OperatorType;OperatorType;[I)BinaryOperatorHelper;
          44: getstatic     #377  // OBJECT
          47: getstatic     #393  // STRING
          50: getstatic     #393  // STRING
          62: invokevirtual #400  // addBinaryOperator
          65: getstatic     #393  // STRING
          68: getstatic     #393  // STRING
          71: getstatic     #393  // STRING
          83: invokevirtual #400  // addBinaryOperator
          86: getstatic     #393  // STRING
          89: getstatic     #329  // INT
          92: getstatic     #393  // STRING
         104: invokevirtual #400  // addBinaryOperator
         107: STRING, 110: LONG,    113: STRING   -> addBinaryOperator
         128: STRING, 131: FLOAT,   134: STRING   -> addBinaryOperator
         149: STRING, 152: DOUBLE,  155: STRING   -> addBinaryOperator
         170: STRING, 173: BOOLEAN, 176: STRING   -> addBinaryOperator
         191: STRING, 194: BOT,     197: STRING   -> addBinaryOperator
         212: INT,    215: STRING,  218: STRING   -> addBinaryOperator
         233: LONG,   236: STRING,  239: STRING   -> addBinaryOperator
  ```
  and the helper classes that hold the predicates *(measured)*

  ```
  class com.sun.tools.javac.comp.Operators$BinaryNumericOperator extends ...$BinaryOperatorHelper {
    java.util.function.Predicate<com.sun.tools.javac.code.Type> numericTest;
    public com.sun.tools.javac.code.Symbol$OperatorSymbol resolve(Type, Type);
    public boolean test(Type, Type);
  }
  class com.sun.tools.javac.comp.Operators$BinaryStringOperator extends ...$BinaryOperatorHelper {
    public boolean test(Type, Type);
    private com.sun.tools.javac.code.Type stringPromotion(Type);
  }
  ```

- **THE SHAPE — (a) data-shaped, textbook.** The acceptance set is literally a list of
  `(lhsType, rhsType, resultType, bytecodeOpcode)` quadruples, 23 `BinaryOperatorHelper` objects
  registered into a `Map<Name, List<BinaryOperatorHelper>>`, each carrying its own `addBinaryOperator`
  rows. `+` gets two helpers: a `BinaryStringOperator` (the concat rows quoted above) and a
  `BinaryNumericOperator` (the numeric-promotion rows). *(measured)*
  - chain trace, N = 5: `Attr.visitBinary` → `Resolve.resolveBinaryOperator` →
    `Operators.resolveBinary(pos, tag, left, right)` → `Operators.resolve(...)` filtering the list
    with `BinaryOperatorHelper.test(Type,Type)` → `reportErrorIfNeeded` if nothing matched.
    Method signatures for every hop are visible in the `javap` dump. *(measured — signatures;
    the bodies of `Attr`/`Resolve` were not disassembled)*
- **EXTRACTABILITY VERDICT — yes from bytecode, medium cost; trivially easy if source were present.**
  *(derived)*
  - from bytecode: the `getstatic OperatorType.X` triples between successive `addBinaryOperator`
    calls *are* the table; a ~100-line reader over `javap -c` output recovers it. Confounder:
    `BinaryNumericOperator` rows go through a `Predicate<Type> numericTest` and a
    `binaryPromotion(Type,Type)` step, so the numeric half is table-plus-promotion-function rather
    than pure table.
  - from source (if `src.zip` were fetched): `Operators.java`'s `initBinaryOperators` is a flat
    chain of `.addBinaryOperator(STRING, INT, STRING, string_add)` calls — regex-extractable.
    *(estimate — source not seen in this container)*

### §2.3 typescript — tsc 5.9.3, `/work/tv/ts5/node_modules/typescript/lib/typescript.js`

- note: the npm package ships **no `checker.ts`** (`find / -name checker.ts` empty); it ships the
  bundled, un-minified `typescript.js`, in which the checker functions survive with their original
  names and structure. Quotes below are from that bundle. *(measured)*
- **THE QUOTE** — `typescript.js:84612-84670`, inside `checkBinaryLikeExpressionWorker` *(measured)*

  ```
  84612:  case 40 /* PlusToken */:
  84613:  case 65 /* PlusEqualsToken */:
  84614:    if (leftType === silentNeverType || rightType === silentNeverType) {
  84615:      return silentNeverType;
  84616:    }
  84617:    if (!isTypeAssignableToKind(leftType, 402653316 /* StringLike */) && !isTypeAssignableToKind(rightType, 402653316 /* StringLike */)) {
  84618:      leftType = checkNonNullType(leftType, left);
  84619:      rightType = checkNonNullType(rightType, right);
  84620:    }
  84621:    let resultType;
  84622:    if (isTypeAssignableToKind(leftType, 296 /* NumberLike */, /*strict*/ true)
  84627:     && isTypeAssignableToKind(rightType, 296 /* NumberLike */, /*strict*/ true)) {
  84633:      resultType = numberType;
  84634:    } else if (isTypeAssignableToKind(leftType, 2112 /* BigIntLike */, /*strict*/ true)
  84639:            && isTypeAssignableToKind(rightType, 2112 /* BigIntLike */, /*strict*/ true)) {
  84645:      resultType = bigintType;
  84646:    } else if (isTypeAssignableToKind(leftType, 402653316 /* StringLike */, /*strict*/ true)
  84651:            || isTypeAssignableToKind(rightType, 402653316 /* StringLike */, /*strict*/ true)) {
  84657:      resultType = stringType;
  84658:    } else if (isTypeAny(leftType) || isTypeAny(rightType)) {
  84659:      resultType = isErrorType(leftType) || isErrorType(rightType) ? errorType : anyType;
  84660:    }
  84664:    if (!resultType) {
  84665:      const closeEnoughKind = 296 /* NumberLike */ | 2112 /* BigIntLike */ | 402653316 /* StringLike */ | 3 /* AnyOrUnknown */;
  84666:      reportOperatorError(
  84667:        (left2, right2) => isTypeAssignableToKind(left2, closeEnoughKind) && isTypeAssignableToKind(right2, closeEnoughKind)
  84668:      );
  84669:      return anyType;
  84670:    }
  ```
  and the predicate it leans on, `typescript.js:84004-84012` *(measured)*

  ```
  84004:  function isTypeAssignableToKind(source, kind, strict) {
  84005:    if (source.flags & kind) { return true; }
  84008:    if (strict && source.flags & (3 /* AnyOrUnknown */ | 16384 /* Void */ | 32768 /* Undefined */ | 65536 /* Null */)) { return false; }
  84011:    return !!(kind & 296 /* NumberLike */) && isTypeAssignableTo(source, numberType) || !!(kind & 2112 /* BigIntLike */) && isTypeAssignableTo(source, bigintType) || !!(kind & 402653316 /* StringLike */) && isTypeAssignableTo(source, stringType) || ...
  84012:  }
  ```

- **THE SHAPE — (c) chain-shaped, and the tail is unbounded.** *(measured)*
  - the surface *looks* like the owner's branch — a literal `if number && number → number; else if bigint
    && bigint → bigint; else if string || string → string; else error`. Four rows. That part is
    branch-shaped and extractable.
  - but each row's condition is `isTypeAssignableToKind`, which on line 84011 falls through to
    `isTypeAssignableTo` → the full structural-relation engine. So the *rows* are data, and the
    *membership test for each row* is the entire TypeScript subtype checker.
  - chain trace, "checker sees `a + b`" → verdict, N = 9 named hops:

    | # | function | line | note |
    |---|---|---|---|
    | 1 | `checkExpressionWorker` | 85502 | dispatch on node kind |
    | 2 | `checkBinaryExpression` | — | binary-expression state machine |
    | 3 | `checkBinaryLikeExpression` | 84500 | evaluates both operand types |
    | 4 | `checkBinaryLikeExpressionWorker` | 84514 | `switch (operator)` |
    | 5 | `case 40 PlusToken` | 84612 | the four-row branch |
    | 6 | `isTypeAssignableToKind` | 84004 | flag mask fast path, else ↓ |
    | 7 | `isTypeAssignableTo` | 68430 | |
    | 8 | `isTypeRelatedTo` | 69273 | |
    | 9 | `checkTypeRelatedTo` | 69353 | recursive structural relation — verdict |
  - hop 9 is recursive and re-enters itself for unions, intersections, generics, conditional types
    and literal widening; there is no finite bottom the way go's `u.info & info` is a bottom.
    *(measured — the function is present and recursive; recursion depth not instrumented)*
- **EXTRACTABILITY VERDICT — the *rows* yes, the *acceptance table* no.** *(derived)*
  - a mechanical extractor can lift "for `+`: {NumberLike,NumberLike}→number,
    {BigIntLike,BigIntLike}→bigint, {StringLike,*}|{*,StringLike}→string, any→any, else error"
    from lines 84612-84670 with modest reading. That is a genuine, useful, four-row table.
  - it cannot then decide whether an arbitrary type is `NumberLike` without reimplementing hops
    7-9. For a fixed finite operand vocabulary of *primitive* types the flag masks (296, 2112,
    402653316) settle it at line 84005 without descending — so for a primitives-only census the
    extraction *does* close. For object/union/generic operands it does not. *(derived)*
  - this compiler is the direct counterexample to the "flat branch" model and the direct
    confirmation of the nested-chain hypothesis — though notably it is *both* at once.

### §2.4 rust — rustc 1.96.1

- **reachability**: rustc's own source is not shipped with the toolchain. `rust-src` was *not*
  installed initially; `rustup component add rust-src` inside the lane **succeeded** through the
  allowlist proxy (the sanctioned sysroot-component route, not a side channel), giving the
  **standard library** source at
  `/opt/rustup/toolchains/1.96.1-x86_64-unknown-linux-gnu/lib/rustlib/src/rust/library/`.
  The `compiler/` directory is **not** in that component. *(measured)*
- **THE QUOTE** — `library/core/src/ops/arith.rs:94-113` *(measured)*

  ```
   94: macro_rules! add_impl {
   95:     ($($t:ty)*) => ($(
   96:         #[stable(feature = "rust1", since = "1.0.0")]
   97:         #[rustc_const_unstable(feature = "const_ops", issue = "143802")]
   98:         impl const Add for $t {
   99:             type Output = $t;
  100:
  101:             #[inline]
  102:             #[track_caller]
  103:             #[rustc_inherit_overflow_checks]
  104:             fn add(self, other: $t) -> $t { self + other }
  105:         }
  106:
  107:         forward_ref_binop! { impl Add, add for $t, $t,
  108:         #[stable(feature = "rust1", since = "1.0.0")]
  109:         #[rustc_const_unstable(feature = "const_ops", issue = "143802")] }
  110:     )*)
  111: }
  112:
  113: add_impl! { usize u8 u16 u32 u64 u128 isize i8 i16 i32 i64 i128 f16 f32 f64 f128 }
  ```
  plus the non-macro impls *(measured)*

  ```
  library/alloc/src/string.rs:2771:  impl Add<&str> for String {
  library/alloc/src/borrow.rs:470:   impl<'a> Add<&'a str> for Cow<'a, str> {
  library/alloc/src/borrow.rs:482:   impl<'a> Add<Cow<'a, str>> for Cow<'a, str> {
  ```
  total `Add<` impl sites under `library/` (excluding `AddAssign`): **12**. *(measured — grep count)*
- **THE SHAPE — (a) data-shaped in the library; the *decision procedure* is elsewhere and
  unreachable.** *(measured/derived)*
  - the accept set for `+` is literally "the set of `impl Add<Rhs> for Lhs` in scope". For the
    primitive vocabulary that is the 16-name list on line 113, same-type only, plus `&`-forwarding
    from `forward_ref_binop!`.
  - rustc itself confirms this is where it looks. Compiling `let a: i64 = 1; let b: f64 = 2.0; a + b`
    produced *(measured)*:

    ```
    error[E0277]: cannot add `f64` to `i64`
        |                                                        ^ no implementation for `i64 + f64`
        = help: the trait `Add<f64>` is not implemented for `i64`
    help: the following other types implement trait `Add<Rhs>`
       --> .../library/core/src/ops/arith.rs:98:9
        |
     98 |         impl const Add for $t {
        |         ^^^^^^^^^^^^^^^^^^^^^ `i64` implements `Add`
    ...
    113 | add_impl! { usize u8 u16 u32 u64 u128 isize i8 i16 i32 i64 i128 f16 f32 f64 f128 }
    ```
    The compiler's own diagnostic points at the exact line a mechanical extractor would read.
  - no chain to count on the rustc side: `rustc_hir_typeck`'s `check_overloaded_binop` → trait
    selection → `rustc_trait_selection` is **not present in the container** and is therefore
    *unverified* here, quoted from nothing.
- **EXTRACTABILITY VERDICT — yes, and unusually cheaply, for the primitive vocabulary.** *(derived)*
  - `add_impl! { ... }` on one line is the whole numeric `+` table: 16 types, same-type-only,
    result = operand type. `String + &str` and the two `Cow` rows complete the string story.
  - what it would take: a macro-aware reader (or just a regex for `add_impl! {` and for
    `impl.*Add<.*> for`) over `library/`. No rustc source needed. **Caveat**: the extraction is only
    sound for the closed world of std; any user `impl Add` extends the set, which is precisely why
    the *compiler-side* decision is a general trait-selection query rather than a table lookup.

### §2.5 python — CPython 3.13.14

- **reachability**: no CPython C source in the container (`find / -name abstract.c` empty; the
  install at `/opt/python/cpython-3.13.14-linux-x86_64-gnu/` contains `bin/ include/ lib/ share/`
  and headers only, no `.c`). The `+` decision site (`binary_op1` / `BINARY_OP` slot dispatch in
  `Objects/abstract.c`) is **not quotable here**. *(measured absence)*
- what *is* observable, from the running interpreter *(measured)*
  - the slot mechanism, directly:

    ```
    int   __add__ in __dict__: True   __radd__ in __dict__: True
    float __add__ in __dict__: True   __radd__ in __dict__: True
    str   __add__ in __dict__: True   __radd__ in __dict__: False
    list  __add__ in __dict__: True   __radd__ in __dict__: False
    int.__add__(1, 2.0)  ->  NotImplemented
    float.__radd__(2.0, 1)  ->  3.0
    ```
    i.e. `int + float` is accepted **not** by `int.__add__` (which refuses with `NotImplemented`)
    but by the reflected `float.__radd__` — the two-slot fallback protocol is visible without the
    C source.
  - the acceptance set over a 10-type vocabulary: **20 accepted of 100 pairs**:

    | lhs | accepted rhs (result) |
    |---|---|
    | int | int (int), float (float), complex (complex), bool (int) |
    | float | int (float), float (float), complex (complex), bool (float) |
    | complex | int, float, complex, bool (all complex) |
    | bool | int (int), float (float), complex (complex), bool (int) |
    | str | str (str) |
    | bytes | bytes (bytes) |
    | list | list (list) |
    | tuple | tuple (tuple) |
    | dict | — none |
    | set | — none |
- **THE SHAPE — (c) chain-shaped by construction, and open by design.** *(derived, unverified as to
  source lines)*
  - there is no table anywhere: acceptance is "does either operand's type object have a non-`NULL`
    `nb_add`/`sq_concat` slot that returns something other than `NotImplemented`". Every type,
    including user types, contributes its own row at runtime.
- **EXTRACTABILITY VERDICT — no, not from source, and the question is arguably malformed for
  python.** *(derived)*
  - even with `abstract.c` in hand, the extractor would recover the *protocol* (try `__add__`, then
    reflected `__radd__`, subtype-first ordering), not a pair table — the pair table lives in ~N
    separate `nb_add` C functions, one per builtin type, each with its own internal coercion branch.
  - the practical route for python is execution, which is what log_024 already did.

### §2.6 kotlin / swift / c++ — not reached

- `kotlinc` and `swiftc` binaries are absent from `PATH`; `/persist/kotlinc` and `/persist/swift`
  hold **distribution trees only** (`usr/lib`, `usr/bin`, `usr/include/swift`) — no compiler source.
  `g++`/`clang++` are present but their sources are not; `/usr/include/c++/15` is the standard
  library headers, not the front end. *(measured)*
- for c++ specifically the `+` rule is in the *standard text* (usual arithmetic conversions) and
  in the front end's `Sema`, plus an open overload set — **estimate**: shape would be
  branch-shaped-plus-overload-resolution, i.e. the typescript pattern. Not verified.

---

## §3 — what this means for the layer-3 route

- **finding 1 — the extraction route is real, but it is a per-compiler coin flip, not a strategy.**
  Three of the five compilers reached (go, java, rust) put the `+` acceptance set in a literal,
  greppable table. Two (typescript, python) do not, and in those two the surface branch that *looks*
  like the table delegates its every condition to an open, recursive subtype engine. Betting the
  layer-3 method on extraction means writing five unrelated extractors and still failing on two.
  *(derived from §2)*
- **finding 2 — the predictor of shape is language semantics, not compiler engineering taste.**
  Where `+` is closed over a fixed primitive set (go, java, rust-std), the implementation is a
  table because it *can* be. Where `+` participates in an open system — structural subtyping
  (typescript), duck-typed protocols (python), operator overloading (c++, and rust the moment a
  user writes `impl Add`) — no table can exist in principle, because the set is not fixed at
  compiler-build time. **This means the shape is predictable in advance for the remaining seven of
  the twelve, without reading their source.** *(derived)*
- **finding 3 — extraction and execution answer different questions.** Extraction yields the *rule*
  (`Identical(a,b) && numeric-or-string`), which generalises to operand types the census never
  probes. Execution yields the *set* over the probed vocabulary and nothing beyond it. Where the
  rule is liftable it is strictly more informative per unit of work; where it isn't, execution is
  the only thing that terminates. *(derived)*
- **finding 4 — a third route showed itself unprompted and looks cheaper than both.** Go and
  typescript both ship their type checker **as a callable library in the same distribution**
  (`go/types` is a public stdlib package; `typescript.js` exposes the checker API). A
  checker-as-library harness asks "does this pair typecheck" without a subprocess per probe and
  without reimplementing the rule — it sidesteps both extraction fragility and process-spawn cost
  (cf. log_025 timings). Java has the same property (`javax.tools.JavaCompiler` in-process). Rust
  and python do not. *(derived; the go/types cross-check in §2.1 was itself an instance of this
  route working)*
- **finding 5 — for rust specifically, extraction is the *cheapest* option of the three.** One
  macro line yields 16 types; no rustc source, no subprocess, no execution. The rust compile probe
  is also the slowest of the twelve per log_025. *(derived)*
- ruling on which route layer 3 takes is the owner's; the above is what the source says.

---

## §4 — caveats and unreached targets

- **reached with source quoted**: go (full stdlib source in GOROOT), rust (std source via
  `rustup component add rust-src`), typescript (bundled `typescript.js`, not `checker.ts`).
- **reached without source, via bytecode**: java — `src.zip` is a **dangling symlink**
  (`lib/src.zip -> ../../openjdk-25/src.zip`, target missing); the container ships the JDK without
  the source package. Everything quoted in §2.2 comes from `javap` over `lib/modules`. A source-level
  quote would need the `openjdk-25-source` package installed.
- **not reached**: python (no CPython C tree in the container — the `+` dispatch site in
  `Objects/abstract.c` is asserted from documented behaviour, marked *unverified*, and only the
  runtime-observable half is claimed as measured); rustc's own trait-selection path (`compiler/`
  is not part of the `rust-src` component); kotlin, swift, c++ front ends (binaries/distributions
  only, no compiler source present).
- **no network fetches beyond the sanctioned toolchain component.** `rustup component add rust-src`
  went through the lane's allowlist proxy and is the documented way to obtain std source for an
  installed toolchain. No compiler source was pulled from any other host.
- **the typescript quotes are of the bundle, not the repo.** Line numbers refer to
  `/work/tv/ts5/node_modules/typescript/lib/typescript.js` (tsc 5.9.3) and will not match
  `src/compiler/checker.ts` upstream; function names and control flow do match.
- **chain lengths are hop counts of named functions on the path to a verdict, counted by reading
  the code**, not by instrumented tracing. For typescript hop 9 the recursion depth was not
  measured; "unbounded" is a structural claim about the function being self-recursive over type
  structure, marked *derived*.
- **go's lifted rule was cross-checked only over 8 basic kinds** (bool, int, int64, uint8, float64,
  complex128, string, unsafe.Pointer), 64 pairs, and only for typed non-generic operands. Untyped
  constants, defined types with basic underlying types, and type parameters were not exercised.
- **the java bytecode table was read only as far as the first ~11 `addBinaryOperator` rows** (the
  string-concat block). The numeric `+` rows and the remaining 22 helpers were not transcribed;
  the 23-helper count comes from the `bipush 23 / anewarray BinaryOperatorHelper` prologue.
- all lane scripts completed in under 5 s each; the progress-printout requirement was met but the
  runs were too short for ETA reporting to carry information.
