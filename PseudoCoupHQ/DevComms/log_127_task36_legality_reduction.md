# log 127 — TASK 36: the legality reduction, measured before any compiling

Date: 2026-09-01. Session: Claude Code, TASK 36 of
`DevComms/log_123_claude_code_task_briefs_round7.md`.

REPORT-ONLY. Nothing was compiled. No probe was written, no lane was
submitted, no existing file was changed (§7).

Two populations are counted on this page and they are never mixed:

- **the corpus** — the five compiled languages' candidate probes as they
  stand on disk today: 4,440 candidates, 1,779 accepted, 2,661 refused,
  six hand-written holder types per language. Every "hit" and "miss"
  number is against this population.
- **the full-core candidate space** — the same operator units crossed with
  each language's EXTRACTED SCALAR CORE from `type_inventory2.json`
  (log 125's current inventory: 56 c, 56 cpp, 14 go, 14 rust, 16 swift):
  152,298 candidates. Every "naive / legal / reduction" number is against
  this population. No probe of it exists; it is arithmetic.

---

# 1. The answer first, in one line each

## 1.1 The reduction, full-core population (152,298 candidates)

The rules the five authorities state about their own operators cut the
candidate space from **152,298 to 129,043** — a factor of **1.18** — and
the cut is wildly uneven by language:

| language | naive cross-product | rules admit | units with no rule (passed through) | would compile | factor |
|---|---|---|---|---|---|
| c | 57,400 | 51,325 | 504 | 51,829 | x1.11 |
| cpp | 79,352 | 67,463 | 3,528 | 70,991 | x1.12 |
| go | 3,864 | 469 | 84 | 553 | **x6.99** |
| rust | 4,466 | 498 | 1,302 | 1,800 | **x2.48** |
| swift | 7,216 | 1,326 | 2,544 | 3,870 | **x1.86** |
| **total** | **152,298** | **121,081** | **7,962** | **129,043** | **x1.18** |

Counting only the operator units the rules actually cover, the factors are
x1.12 / x1.18 / x8.24 / x8.97 / x5.44 and x1.26 overall. The difference
between the two columns is the residue in §4.

## 1.2 The validation, corpus population (4,440 candidates)

The filter was run at the corpus's own six holder types and scored against
what the compilers actually did:

- **99.9% agreement inside rule scope**: 3,584 of 3,588 in-scope
  candidates predicted correctly; 4 misses, all one cause (§5).
- **0 of the 1,779 accepted units would have been dropped.** Not one
  accepted probe is predicted illegal.
- Stated as a compile budget: **2,499 of 4,440 candidates would go to a
  compiler instead of 4,440**, and all 1,779 accepted units are inside
  those 2,499.

## 1.3 The finding that changes log 116's reading

Log 116 measured that a TYPE PAIR alone explains 0.0% of c/cpp refusals
and about 71% of go/rust/swift's (its finding F4). The operator-category
rules close exactly that hole:

| language | refused (corpus) | explained by an extracted rule | log 116's type-pair figure |
|---|---|---|---|
| c | 140 | 122 (87.1%) | 0.0% |
| cpp | 232 | 184 (79.3%) | 0.0% |
| go | 637 | 607 (95.3%) | 71.6% |
| rust | 733 | 489 (66.7%) | 72.0% |
| swift | 919 | 539 (58.7%) | 70.5% |
| **total** | **2,661** | **1,941 (72.9%)** | **61.3%** |

The rest of each row is not a wrong prediction — it is a refusal on an
operator unit for which no rule was extracted at all (§4), which the
filter passes through to the compiler rather than judging.

---

# 2. What was built, and what a "rule" is here

## 2.1 The two new programs

- `legality_rules.py` reads each language's own operand-admissibility
  statement out of its source and writes `legality_rules.json`: **55
  rules** and **185 operator units**.
- `legality_filter.py` applies those rules and writes
  `legality_reduction.json` (§1.1's arithmetic) and
  `legality_validation.json` (§1.2's scoring, with every miss).

## 2.2 A rule, defined by showing one

A RULE is one admissibility statement, read off a named line, expressed in
four classes (`integer_signed`, `integer_unsigned`, `float`,
`truth_value`). This is the whole of go's remainder-and-bitwise rule as
the artifact holds it:

```
{"language": "go",
 "rule_id": "go_binaryOpPredicates_allInteger",
 "source_file": "src/go/types/expr.go",
 "pin": "9f1012d9a1aa0831ff44ac9c767e96f9943d13fe",
 "line": 766,
 "text": "\t\ttoken.REM: allInteger,",
 "shape": {"arity": "binary",
           "lhs_classes": ["integer_signed", "integer_unsigned"],
           "rhs_classes": ["integer_signed", "integer_unsigned"],
           "same_type_required": true}}
```

Line 766 is not typed in: `legality_rules.py :: find_line()` SEARCHES the
file for the quoted fragment and records where it found it. A fragment
that is not found is a hard failure and no output is written — which is
how the first run caught a mis-typed clang fragment (§5.2).

## 2.3 The spelling ban, and how the join is made without a token key

Nothing is keyed, grouped, paired or selected by an operator token.

- A rule is keyed by the AUTHORITY'S OWN NAME for its check
  (`clang_CheckBitwiseOperands`, `go_comparison_ordering`,
  `swift_BinaryInteger_heterogeneous_shift_operands`,
  `rust_codegen_int_binop`).
- An operator unit is a UNIT OBJECT carrying `language`, `id`, `arity`,
  `position` and `rule_ids`; the token sits in its `spelling` field, the
  display-label seat the guard allows. Example row:
  `{"language": "go", "id": "go/opunit_12", "arity": "binary",
  "spelling": "%", "authority_operation": "REM",
  "rule_ids": ["go_binaryOpPredicates_allInteger"]}`.
- The join from a unit to a rule runs through the AUTHORITY'S OWN
  spelling table wherever one exists: clang's
  `OperationKinds.def` (`BINARY_OPERATION(Rem, "%")`), clang's
  `TokenKinds.def` `CXX_KEYWORD_OPERATOR` rows for c++'s alternative
  spellings, go/token's `tokens` array (`REM: "%"`), and for swift the
  declaration itself, which spells the operator in its own signature.
  Rust is the exception and is finding F36-3.
- Guard, on both artifacts, pasted in §6.

---

# 3. Where each rule came from, with the values moving

## 3.1 c and cpp — clang's Sema operator-category checks

`Sema` is clang's semantic-analysis stage; `CreateBuiltinBinOp` is the one
function that decides a built-in binary expression's type, and it does so
by a switch that hands each operation to a category check. Read at
`llvm-project` tag `llvmorg-21.1.8` via `git show` only — the working tree
is at `llvmorg-24-init-680-g6a33b69d8bae` and is never read.

```
$ git -C ~/Programming/Sources/llvm-project rev-parse llvmorg-21.1.8
42befb84c672d78de430feb4c96710e6aa4fc774
$ git -C ~/Programming/Sources/llvm-project describe --tags | head -1
llvmorg-24-init-680-g6a33b69d8bae
```

Ten checks were extracted. Two of them, with the line that carries the
rule:

```
  case BO_Rem:
    ResultTy = CheckRemainderOperands(LHS, RHS, OpLoc);
...
QualType Sema::CheckRemainderOperands(...)
  if (compType.isNull() ||
      (!compType->isIntegerType() &&
       !(getLangOpts().HLSL && compType->isFloatingType())))
    return InvalidOperands(Loc, LHS, RHS);
```

```
inline QualType Sema::CheckBitwiseOperands(...)
  if (LHS.get()->getType()->hasFloatingRepresentation() ||
      RHS.get()->getType()->hasFloatingRepresentation())
    return InvalidOperands(Loc, LHS, RHS);
```

### 3.1.1 The values moving, on the cell log 116 walked

Log 116's contrast case was c's cell `int32_t, double` — 12 accepted, 6
refused, with a type pair that cannot explain the split. Here is the same
cell decided by the rules, candidate by candidate:

```
  a + b   -> clang_CheckAdditionSubtractionOperands
              admits {int_s,int_u,float,truth} x same     LEGAL    (compiler: accepted)
  a - b   -> same rule                                    LEGAL    (accepted)
  a * b   -> clang_CheckMultiplyDivideOperands            LEGAL    (accepted)
  a / b   -> same rule                                    LEGAL    (accepted)
  a % b   -> clang_CheckRemainderOperands
              admits {int_s,int_u,truth} only;
              `double` is class float                     ILLEGAL  (refused:
              "invalid operands to binary expression ('int32_t' and 'double')")
  a || b  -> clang_CheckLogicalOperands (any scalar)      LEGAL    (accepted)
```

All six agree with the compiler. That cell is where log 116 said a type
inventory predicts nothing; the operator-category rule predicts all of it.

## 3.2 go — the spec-implementing type checker's own predicate tables

Go's checker holds two literal tables mapping each token to a predicate
over the operand type; they are the rule, verbatim:

```
src/go/types/expr.go, line 761
	binaryOpPredicates = opPredicates{
		token.ADD: allNumericOrString,
		token.SUB: allNumeric,
		token.REM: allInteger,
		token.LAND: allBoolean,
```

Three more go rules come from the same file: equality
(`case token.EQL, token.NEQ:`), ordering (`case !allOrdered(x.typ()):` —
which is why go refuses `bool < bool`), and the shift rule
(`"shifted operand %s must be integer"`), the one binary rule in go that
does NOT require both sides to be the same type. Go's homogeneity comes
from the line above the predicate call:

```
	if !Identical(x.typ(), y.typ()) { ... MismatchedTypes ... }
```

Pin: `golang_src` at `9f1012d9a1aa0831ff44ac9c767e96f9943d13fe`.

## 3.3 rust — the code generator's exhaustive match over operand kinds

Rust's trait-impl tables (`library/core/src/ops/*.rs`) are NOT on this
machine, and the checked exclusion is in §4.2. What IS on disk is an
exhaustive match over the operand's type kind, which states which classes
each operation is ever generated for, plus an assertion that states
homogeneity:

```
compiler/rustc_codegen_cranelift/src/num.rs
    match in_lhs.layout().ty.kind() {
        ty::Bool  => codegen_bool_binop(...)     // BitXor, BitAnd, BitOr only
        ty::Uint(_) | ty::Int(_) => codegen_int_binop(...)
        ty::Float(_) => codegen_float_binop(...) // Add,Sub,Mul,Div,Rem only
        _ => unreachable!(...)
    }

    if !matches!(bin_op, BinOp::Shl | ... | BinOp::ShrUnchecked) {
        assert_eq!(in_lhs.layout().ty, in_rhs.layout().ty,
            "int binop requires lhs and rhs of same type");
    }
```

The assertion's exemption for shifts is the whole of rust's shift rule:
same-type NOT required, both sides integer. Unary comes from
`base.rs`'s `UnOp::Not` (bool or integer) and `UnOp::Neg`
(`ty::Int(_)` and `ty::Float(_)` — unsigned integers are absent, which is
correct and is not a class-level guess).

Pin: `rust` at `7c329d6c76e11ca40c5673818ab0439c1be8962c`.

## 3.4 swift — the stdlib's own operator declarations

Swift declares its operators as static functions with signatures, so the
signature IS the admissibility rule. Read from the installed module
interface on disk beside the corpus
(`swift_stdlib_x86_64-unknown-linux-gnu.swiftinterface`, the route (a)
witness log 125 established), with the pinned clone
`swift-6.0.3-RELEASE` @ `6a862d2eb7128ff1f317b07e8ad1a6da939775f3` naming
the stdlib sources those declarations come from.

```
  static func % (lhs: Self, rhs: Self) -> Self                        (BinaryInteger)
  static func & (lhs: Self, rhs: Self) -> Self                        (BinaryInteger)
  static func << <RHS>(lhs: Self, rhs: RHS) -> Self
                                     where RHS : Swift.BinaryInteger  (BinaryInteger)
  static func == (lhs: Self, rhs: Self) -> Swift.Bool                 (Equatable)
  @_transparent public static func == <Other>(lhs: Self, rhs: Other) -> Swift.Bool
                                     where Other : Swift.BinaryInteger
  @_transparent prefix public static func - (operand: Self) -> Self   (SignedNumeric)
```

Two of swift's rules are not class-level statements but CONFORMANCE
statements, and they are computed rather than assumed:
`swift_conformance()` reads every declaration head in the interface
(`@frozen public struct Int32 : Swift.FixedWidthInteger, ...`,
`public protocol Strideable : Swift.Comparable`,
`extension Swift.Bool : Swift.Equatable`) and closes over protocol
inheritance. The result decides the comparison rules' admitted classes:

```
Int32 -> FixedWidthInteger -> BinaryInteger -> Strideable -> Comparable   yes
Bool  -> Sendable, Equatable, Hashable, ...                    Comparable no
```

That closure is what makes the filter refuse `Bool < Bool` — and the
compiler agrees: `error: binary operator '<' cannot be applied to two
'Bool' operands`.

---

# 4. The residue: operator units with no extracted rule

## 4.1 What they are, and why they are passed through, not dropped

62 of the 185 operator units have no rule in any authority table read
here. They are not arithmetic operator units: address-of and dereference,
`sizeof` / `_Alignof` / `__extension__`, c++'s three-way comparison,
rust's four range forms and `as`, swift's ranges, `??`, `try` / `try!`,
`consume`, `is` / `as?`.

The filter says NOTHING about them, so their candidates still go to the
compiler. That is why §1.1 has two columns: 121,081 admitted by a rule
plus 7,962 belonging to units with no rule = 129,043 to compile.

Dropping them instead would be a measured loss, and the corpus says
exactly how much:

```
out-of-rule-scope candidates in the corpus   852 of 4,440
  of which the compiler ACCEPTED             136
  of which the compiler REFUSED              716
```

Those 136 accepted units include c's `sizeof` / `_Alignof` family (30),
cpp's `<=>` (22), rust's range constructors (24) and swift's `??` and
range forms (16). They are real accepted units in the corpus today.

## 4.2 The exclusion, checked on the host side of the container wall

The claim "rust's trait-impl tables are not on this machine" is a path
claim, so first: which side of the wall this ran on.

```
$ ls -d /work
ls: cannot access '/work': No such file or directory
$ hostname
<host>
```

`/work` is the container's build root — the corpus's own refusal texts
carry it (`/work/op_cpp/u/n53/unit.cpp:9:12: error: ...`). It is absent
here, so this is the host. On the host:

```
$ ls ~/Programming/Sources/rust/library
ls: cannot access '~/Programming/Sources/rust/library': No such file or directory
$ ls ~/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/rustlib/src
ls: cannot access '.../lib/rustlib/src': No such file or directory
```

The clone is the partial checkout log 116 already recorded (three crates
under `compiler/`), and the installed toolchain has no `rust-src`
component. So rust's `impl Add for i32` tables have no on-disk authority,
and rust's logical-and / logical-or have none either (they are lowered to
control flow before the code generator sees them) — which is why rust has
15 units with no rule, the most of any language after swift.

---

# 5. Every miss, and its cause

## 5.1 The four misses, all one cause

```
$ python3 -c "...legality_validation.json misses..."
cpp ++ ++a bool ['clang_CheckIncrementDecrementOperand_no_truth_value_increment']
    | error: ISO C++17 does not allow incrementing expression of type bool
cpp -- --a bool ['clang_CheckIncrementDecrementOperand_no_truth_value_decrement']
    | error: cannot decrement expression of type bool
cpp ++ a++ bool  (same rule)   | same diagnostic
cpp -- a-- bool  (same rule)   | same diagnostic
```

All four are predicted LEGAL and were REFUSED. The rules themselves are
right — both were read out of clang and both exclude a truth value:

```
    if (S.getLangOpts().CPlusPlus && ResType->isBooleanType()) {
      if (!IsInc) { S.Diag(OpLoc, diag::err_decrement_bool) ...; return QualType(); }
      S.Diag(OpLoc, S.getLangOpts().CPlusPlus17 ? diag::ext_increment_bool ...
```

The cause is one layer down, in the TYPE inventory, and it is a finding
about the shared class vocabulary rather than about this filter:

- **F36-1 — c and cpp have no truth-value class to exclude.** clang's own
  type table declares `bool` with `UNSIGNED_TYPE`, so
  `type_inventory2.json` marks c/cpp `bool` as `integer_unsigned`. A rule
  that turns on truth-value-ness therefore cannot fire in c or cpp,
  and increment/decrement is the only place in the whole corpus where
  that distinction decides anything. Size: 4 of 4,440 (0.09%).
  The remedy is one row in the class normalisation (c/cpp `bool` ->
  `truth_value`, which every other c/cpp rule already admits because they
  all list truth_value alongside the integers) — it was NOT applied,
  because widening a class marking to make a score go to 100% is exactly
  the kind of per-name patch that is banned. the owner's call.

## 5.2 Two misses that were found and fixed DURING the run, recorded so the
## fix is auditable

Both were caught by the corpus and both were fixed by reading MORE of the
authority, never by special-casing a spelling:

- 36 swift candidates (`Int32` against `Int64`, six comparison units)
  were predicted illegal and had been ACCEPTED. Cause: swift declares a
  HETEROGENEOUS comparison for integers
  (`static func == <Other>(lhs: Self, rhs: Other) where Other : BinaryInteger`)
  that the first pass missed. Adding that declaration as its own rule
  fixed all 36 and broke nothing.
- 4 swift candidates (`Bool` against `Bool`, four ordering units) were
  predicted legal and had been REFUSED. Cause: the first pass gave the
  Comparable rule all four classes by assumption. Replacing the
  assumption with the computed conformance closure (§3.4) fixed all 4.
- A third correction was mechanical, not measured: a clang fragment was
  typed with the wrong indentation and `find_line()` refused to write any
  output until it matched the file.

Score before those two fixes: 44 misses, 98.8% in-scope agreement. After:
4 misses, 99.9%.

---

# 6. Guards, and the cross-check against log 116 / log 125

## 6.1 The spelling-key check, all three artifacts

```
$ cd ~/Programming/PseudoCoupHQ/Research/op_pipeline
$ /tmp/reconnect_venv/bin/python3 legality_rules.py
wrote .../legality_rules.json: 55 rules, 185 operator units
operator inventory: 91 tokens read from probe_manifest_*.json
PASS legality_rules.json -- no operator token in any key, grouping, pairing or row structure

$ /tmp/reconnect_venv/bin/python3 legality_filter.py
...
operator inventory: 91 tokens read from probe_manifest_*.json
PASS legality_reduction.json -- no operator token in any key, grouping, pairing or row structure
PASS legality_validation.json -- no operator token in any key, grouping, pairing or row structure
```

Matching-shaped, no exemption claimed: neither program declares
`"role": "generator provenance"`, so both were walked in full. Both
programs REFUSE THEIR OWN OUTPUT on failure —
`refuse_own_output_on_spelling_failure()` runs the guard, deletes the
written file and exits nonzero.

## 6.2 The naive counts reproduce log 116 and log 125 exactly

This is the check that the operator-unit list is the corpus's own and not
a list invented here. Log 116 §3.1 derived each language's operator counts
by dividing candidates by holders; this task instead counted the distinct
units in the acceptance record. The two agree to the unit:

| language | this task's naive at full core | log 116 / log 125's "predicted at full core" |
|---|---|---|
| c | 57,400 | 57,400 |
| cpp | 79,352 | 79,352 |
| go | 3,864 | 3,864 |
| rust | 4,466 | 4,466 |
| swift | 7,216 | 7,216 (log 125) |
| **total** | **152,298** | **152,298** |

Walked for rust: the acceptance record carries 33 distinct operator
units, 11 unary and 22 binary; the extracted rust scalar core is 14
spellings.

```
  11 unary  x 14            =    154
  22 binary x 14 x 14       =  4,312
                              -------
                               4,466   candidates
```

Log 116 reached 11 and 22 by dividing rust's 858 corpus candidates by 6
and 36; this task reached them by counting the distinct units in
`op_units_rust.json`. Two different routes, the same two numbers, and the
same total for all five languages.

## 6.3 Evidence class per claim

| claim | evidence class |
|---|---|
| every rule's admitted classes (§3) | the tool's own testimony — the check is read out of the compiler's/stdlib's source at the named pin, line searched at run time |
| the swift conformance closure (§3.4) | forced by construction — computed from the interface's own declaration heads |
| the spelling/opcode joins for c, cpp, go, swift (§2.3) | the tool's own testimony — the authority's own table |
| rust's spelling/operation join | human interpretation of stated design — no on-disk authority (F36-3, §4.2), stated on every rust unit's `join_evidence` field |
| the 4,440 / 1,779 / 2,661 counts | forced by construction — `op_units_<lang>.json`'s own tally |
| the reduction arithmetic (§1.1) | derived arithmetic over the extracted inventory and the corpus's own unit list |
| the 4 misses (§5.1) | forced by construction — the compiler's own stored diagnostic |
| the rust-source exclusion (§4.2) | forced by construction — directory absent, container wall established first |

---

# 7. Zero regressions, verified programmatically

```
$ cd ~/Programming/PseudoCoupHQ && git status --porcelain
?? Research/compiler_graph/graph_cpp2.json
?? Research/compiler_graph/graph_cpp3.json
```

The two untracked rows are not this session's — they are the same two
log 116 recorded, from the compiler-graph line. This session's own files
are already committed by the daemon. The only files MODIFIED anywhere in
`op_pipeline` since this task's first commit are this task's own new
files, edited after the daemon had already added them:

```
$ git log --diff-filter=M --name-only --pretty=format: b3b3ee8..HEAD -- Research/op_pipeline | sort -u
Research/op_pipeline/legality_filter.py
Research/op_pipeline/legality_reduction.json
Research/op_pipeline/legality_rules.json
Research/op_pipeline/legality_rules.py
Research/op_pipeline/legality_validation.json
```

`probe_gen.py`, `lane_gen.py`, `type_inventory*.json`, `check_no_spelling_keys.py`
and every `op_units_*.json` were read only.

---

# 8. Complete file inventory

Created this session, all new:

| path | what it is |
|---|---|
| `~/Programming/PseudoCoupHQ/Research/op_pipeline/legality_rules.py` | the rule extractor; searches each source for the quoted fragment and refuses to write if it is absent |
| `~/Programming/PseudoCoupHQ/Research/op_pipeline/legality_rules.json` | 55 rules with file+line+pin provenance, 185 operator units with their rule joins |
| `~/Programming/PseudoCoupHQ/Research/op_pipeline/legality_filter.py` | applies the rules; writes the reduction and the validation |
| `~/Programming/PseudoCoupHQ/Research/op_pipeline/legality_reduction.json` | per language and per operator unit: naive, legal, no-rule residue, factor |
| `~/Programming/PseudoCoupHQ/Research/op_pipeline/legality_validation.json` | the corpus scoring, the corpus-sized compile budget, and every miss |
| `~/Programming/PseudoCoupHQ/DevComms/log_127_task36_legality_reduction.md` | this log |

Modified this session: one dated entry appended under the single
`# PROGRESS` heading of
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`.

Read but not modified: `op_units_<lang>.json` (five),
`probe_manifest_<lang>.json` (five), `type_inventory2.json`,
`type_inventory_validate.py`, `check_no_spelling_keys.py`,
`swift_stdlib_x86_64-unknown-linux-gnu.swiftinterface`,
`~/Programming/Sources/llvm-project` at `llvmorg-21.1.8` via `git show`
(`clang/lib/Sema/SemaExpr.cpp`, `clang/include/clang/AST/OperationKinds.def`,
`clang/include/clang/Basic/TokenKinds.def`),
`~/Programming/Sources/golang_src/src/go/types/expr.go`,
`~/Programming/Sources/golang_src/src/go/token/token.go`,
`~/Programming/Sources/rust/compiler/rustc_codegen_cranelift/src/{num.rs,base.rs}`,
`~/Programming/Sources/swift-6.0.3-RELEASE` (pin only).

---

# 9. Findings

- **F36-1 — c and cpp have no truth-value class, so a truth-value
  exclusion cannot be expressed there. OPEN, sized at 4 of 4,440.** §5.1.
  One-row remedy available; not applied, because widening a class marking
  to raise a score is the patch shape this line bans.
- **F36-2 — 62 of 185 operator units have no rule in any authority table
  read here, and 136 corpus-accepted units live on them. OPEN,
  structural.** §4. They are passed through to the compiler; dropping them
  would lose real accepted units.
- **F36-3 — rust has no on-disk operator authority.** §4.2. The trait
  tables are absent (partial checkout, no `rust-src`), so rust's rules
  come from the code generator's exhaustive match — which states type
  classes correctly but says nothing about logical-and / logical-or — and
  rust's spelling/operation join is declared rather than extracted, the
  only such join in the five.
- **F36-4 — the reduction is a go/rust/swift effect, not a c/cpp one.**
  §1.1. c and cpp cut by about a ninth because clang's usual arithmetic
  conversions genuinely admit nearly every scalar pair for nearly every
  operator; the refusals c and cpp DO have are almost all
  operator-category refusals (§1.3), which the filter now predicts.
- **F36-5 — the filter loses no accepted unit on the corpus.** §1.2.
  0 of 1,779.

---

# 10. For the owner — the call this hands over

The brief's step is done: the reduction is measured and nothing was
compiled. What is now decidable, with the numbers on the page:

- **Regenerate at the full extracted core with the filter in front?** That
  is 129,043 compiles instead of 152,298 — the filter saves 23,255 —
  against today's 4,440. The saving is concentrated in go (x6.99), rust
  (x2.48) and swift (x1.86).
- **Or regenerate only where the filter earns its keep** — go, rust and
  swift at full core (553 + 1,800 + 3,870 = 6,223 compiles, against 3,014
  candidates in those three lanes today) and leave c and cpp at the
  current six holders, since filtering them saves about a ninth.
- **F36-1's one-row remedy** — mark c/cpp `bool` as a truth value in the
  class normalisation, taking the corpus agreement from 99.9% to 100%.

No probe was compiled and no CPU-capped Airlock work was started, per the
brief.
