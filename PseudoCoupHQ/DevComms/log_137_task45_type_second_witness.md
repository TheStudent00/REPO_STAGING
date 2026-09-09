# log 137 — TASK 45: the type inventory's second witness

Date: 2026-09-02. Population words used throughout: **the regeneration**
means the 129,553 probes the trickle container compiled on 2026-09-02
(log 131) — 29,288 accepted with full extraction, 100,265 refused. **The
inventory** means `Research/op_pipeline/type_inventory2.json`, the
per-language list of type spellings an authority names. Neither is
changed by this work; inventory 2 is read-only here and the regeneration
was not re-run.

---

# 1. What was done and what it found, in plain words

The inventory was built by asking each toolchain what type names it
KNOWS — clang's builtin-type table, go/types' `Typ` table, the rust
grammar's primitive list, swift's stdlib source and installed module
interface. That is not the same question as what this target ACCEPTS in
a source file. So a second witness was measured: for every type spelling
in the inventory, a source file whose only content is a declaration of
that type was compiled, in the CPU-capped trickle container, at the same
flags the probe lanes use. Two forms per type — the type as a variable,
and the type in the position a probe puts it in, a function parameter.
416 compilations, no operator in any of them.

85 of the 208 spellings that can be written in source were refused by
the compiler that is supposed to know them. The families are the ones
round 9's correction named and a few more: the embedded-C fixed-point
types (`_Accum`, `_Fract`, and every `_Sat` combination) are behind a
flag this target does not set; `char16_t`/`char32_t`/`wchar_t`/`char8_t`
need a header the probe does not include in C; `__ibm128` is refused on
this target by name; `__fp16` compiles as a variable and is refused as a
parameter, which is exactly the distinction the two forms exist to make
visible; go's untyped constants and `invalid type` are type-checker
vocabulary and not writable at all; `str` in rust has no known size.

`type_inventory3.json` is the inventory restricted to what survives.
The scalar core it yields shrinks for c (56 → 25) and c++ (56 → 28) and
does not move for go, rust or swift — which says the over-admission was
entirely clang's table being an inventory of everything clang can
represent, not of everything this Linux x86-64 target compiles.

Then the corrected inventory was checked against what the compilers
actually did in the regeneration, probe by probe. 95,371 of the 100,265
refusals — 95.1% — are probes at least one of whose holder types this
target refuses to declare. Those probes would never have been generated
under the corrected inventory. **Zero** accepted probes carry a demoted
type, which is the check that could have refuted the whole witness. Of
the 4,894 refusals left, 4,614 are on operator units for which no
legality rule was ever extracted (the filter passes those to the
compiler by design), 4 are the ratified c++ truth-value quirk, and 276
are one real miss with one cause: the swift probe emitter attaches
`@_cdecl` by looking at the RESULT type only, and swift cannot export a
128-bit integer PARAMETER to C. The legality oracle's agreement inside
its own scope is 99.0%, and it is 100.0% in c, c++, go and rust.

---

# 2. The second witness, with the values moving

## 2.1 The question the first witness answered

Take `c/type_0`, the row inventory 2 holds for `_Accum`:

```
{"language": "c", "id": "c/type_0", "spelling": "_Accum",
 "admitted_by": [{"witness": "compiler_table",
   "source": "clang/include/clang/AST/BuiltinTypes.def @ llvmorg-21.1.8",
   "declared_as": "SIGNED_TYPE",
   "joined_via": "the .def comment line above the macro, which states the C spelling",
   "builtin_id": "Accum", "verification": "table_row_comment_join"}],
 "class": "integer_signed", "class_source": "SIGNED_TYPE"}
```

Everything in that row is true. clang's own table names `_Accum`, at a
pinned revision, and marks it a signed type. The row's claim is "clang
knows this name".

## 2.2 The question that was never asked

The probe lane does not ask clang what it knows. It writes a file and
runs `clang -std=c17 -O0 -g -c`. `declare_lane.py` writes the smallest
file that asks that question, with no operator anywhere in it:

```
#include <stdint.h>
#include <stdbool.h>

void declared_holder(_Accum a)
{
    (void)0;
}
```

and the compiler answers, in its own words, captured verbatim:

```
/work/decl_c/u/d00002/decl.c:4:22: error: unknown type name '_Accum'
    4 | void declared_holder(_Accum a)
      |                      ^
1 error generated.
```

`_Accum` is behind `-ffixed-point`, which the probe lanes do not pass.
So the type is known and not declarable, and the row is demoted.

## 2.3 Why two forms, shown by the type where they differ

`__fp16` answers the two forms differently, and it is the only spelling
that does (both in c and in c++, so two rows, one behaviour):

| form | source | verdict |
|---|---|---|
| variable | `static __fp16 declared_value;` | ACCEPT |
| parameter | `void declared_holder(__fp16 a) { (void)0; }` | REFUSE |

The refusal, verbatim:

```
error: parameters cannot have __fp16 type; did you forget * ?
```

A probe holder IS a parameter, so the parameter form decides membership
and the variable form is recorded beside it. Had only the variable form
been compiled, `__fp16` would have stayed in the core and gone on
producing refusals.

## 2.4 The compilations, counted

416, which is 208 source spellings × 2 forms. The remaining 122
inventory rows carry a compiler-table identifier with `::` in it rather
than a source spelling — nothing can be written with them, so nothing
was compiled for them, and they are demoted with that reason recorded
(`cause: not_a_source_spelling`). `core_rule2.scalar_core` already
excluded them by the same test, so no core member is affected.

| language | inventory 2 rows | compiled (types × 2) | kept | demoted by the compiler | demoted as not-a-spelling |
|---|---:|---:|---:|---:|---:|
| c | 127 | 148 | 35 | 39 | 53 |
| cpp | 127 | 148 | 38 | 36 | 53 |
| go | 26 | 52 | 17 | 9 | 0 |
| rust | 33 | 34 | 16 | 1 | 16 |
| swift | 17 | 34 | 17 | 0 | 0 |
| **total** | **330** | **416** | **123** | **85** | **122** |

The lane tallies, printed by the lanes themselves:

```
=== declaration lane -- c -- 148 declarations ===
Ubuntu clang version 21.1.8 (6ubuntu1)
done: {"submitted": 148, "accept": 71, "refuse": 77} -> /out/decl_c.txt
done: {"submitted": 148, "accept": 77, "refuse": 71} -> /out/decl_cpp.txt
done: {"submitted": 52, "accept": 34, "refuse": 18} -> /out/decl_go.txt
done: {"submitted": 34, "accept": 32, "refuse": 2} -> /out/decl_rust.txt
done: {"submitted": 34, "accept": 34, "refuse": 0} -> /out/decl_swift.txt
```

(Those tallies count both forms; membership is decided by the parameter
form alone, which is why c keeps 35 and not 71/2.)

## 2.5 The pins, verified in-container before anything was compiled

`bash trickle_up.sh` asks the toolchains rather than assuming them, and
each lane prints its own banner again before it compiles:

```
$ bash trickle_up.sh
  machine cores: 12 ; cap: 6
  trickle-runner already existed; started (bound to .../AirlockTrickle/agent/drop)
  toolchains, asked rather than assumed:
Ubuntu clang version 21.1.8 (6ubuntu1)
Ubuntu clang version 21.1.8 (6ubuntu1)
rustc 1.96.1 (31fca3adb 2026-06-26)
go version go1.26.0 linux/amd64
Swift version 6.0.3 (swift-6.0.3-RELEASE)
```

All five identical to log 131's table, which is identical to the
2026-08-25 originals. The flags are copied from `lane_gen.py ::
compile_probe`, anchor mode: c `-std=c17 -O0 -g -c`; cpp `-std=c++20
-O0 -g -c`; rust `--crate-type=lib --emit=obj -C opt-level=0 -g`; go
`go build -gcflags='-N -l'`; swift `-Onone -g -c`.

## 2.6 Which side of the container wall each step ran on

```
HOST path check:
<user>
ls: cannot access '/persist': No such file or directory
  PseudoCoupHQ exists -> HOST side
```

The generator, the fold and every count ran on the host. Only the 416
compilations ran inside `trickle-runner`, whose `/persist` mount holds
the swift toolchain read-only. Airlock's own containers were up
throughout and were not touched:

```
$ podman ps -a --format '{{.Names}} {{.Status}}' | sort
sandbox-proxy Up 47 hours
sandbox-runner Up 46 hours
trickle-runner Exited (137) Less than a second ago
va-proxy Up 3 days
va-runner Up 3 days
```

The trickle copy was left PAUSED at the end of this work
(`bash trickle_down.sh --pause`), with nothing running inside it first
(the only compiler process present was a stopped `[go] <defunct>` from
88 minutes earlier).

---

# 3. Every demotion, by the compiler's own words

Grouped by diagnostic shape: the message with its `file:line:col`
prefix removed, quoted spans replaced by `<Q>`, digits replaced by `N`.
That normalisation is uniform, so the grouping key is the compiler's own
diagnostic shape and never a token.

## 3.1 c — 39 demotions

| the compiler's words | how many | the spellings |
|---|---:|---|
| `error: unknown type name <Q>` | 25 | `_Accum`, `_Fract`, `_Sat _Accum`, `_Sat _Fract`, `_Sat long _Accum`, `_Sat long _Fract`, `_Sat short _Accum`, `_Sat short _Fract`, `_Sat unsigned _Accum`, `_Sat unsigned _Fract`, `_Sat unsigned long _Accum`, `_Sat unsigned long _Fract`, `_Sat unsigned short _Accum`, `_Sat unsigned short _Fract`, `char16_t`, `char32_t`, `char64_t`, `char8_t`, `charptr_t`, `half`, `max_align_t`, `nullptr_t`, `ptrdiff_t`, `size_t`, `wchar_t` |
| `error: expected <Q>` | 10 | `long _Accum`, `long _Fract`, `short _Accum`, `short _Fract`, `unsigned _Accum`, `unsigned _Fract`, `unsigned long _Accum`, `unsigned long _Fract`, `unsigned short _Accum`, `unsigned short _Fract` |
| `error: parameters cannot have __fp16 type; did you forget * ?` | 1 | `__fp16` |
| `error: __ibm128 is not supported on this target` | 1 | `__ibm128` |
| `error: unknown type name <Q>; did you mean <Q>?` | 1 | `ssize_t` |
| `error: argument may not have <Q> type` | 1 | `void` |

## 3.2 cpp — 36 demotions

Same families, minus the four that C++ has natively (`char8_t`,
`char16_t`, `char32_t`, `wchar_t` are keywords in C++20 and survive),
plus `_Bool`, which is C's spelling and not C++'s:

| the compiler's words | how many | the spellings |
|---|---:|---|
| `error: unknown type name <Q>` | 19 | `_Accum`, `_Bool`, `_Fract`, the twelve `_Sat` combinations, `char64_t`, `charptr_t`, `half`, `max_align_t` |
| `error: expected <Q>` | 10 | the ten `long`/`short`/`unsigned` fixed-point combinations |
| `error: unknown type name <Q>; did you mean <Q>?` | 4 | `nullptr_t`, `ptrdiff_t`, `size_t`, `ssize_t` |
| `error: parameters cannot have __fp16 type; did you forget * ?` | 1 | `__fp16` |
| `error: __ibm128 is not supported on this target` | 1 | `__ibm128` |
| `error: argument may not have <Q> type` | 1 | `void` |

## 3.3 go — 9 demotions

go's table names its own type-checker vocabulary. The nine are
`Pointer`, `invalid type`, and the seven `untyped ...` constants. Two
verbatim:

```
Pointer:        # declprobe
                ./main.go:4:23: undefined: Pointer
                ./main.go:8:19: undefined: Pointer

untyped int:    # declprobe
                ./main.go:4:31: syntax error: unexpected name int in parameter
                list; possibly missing comma or )
```

`Pointer` is `unsafe.Pointer`'s bare table name; the untyped rows are
constant kinds that exist only inside the type checker.

## 3.4 rust — 1 demotion

```
error[E0277]: the size for values of type `str` cannot be known at compilation time
 --> /work/decl_rust/u/d00022/decl.rs:2:27
  |
2 | pub fn declared_holder(a: str) {
  |                           ^^
```

`str` was never in the scalar core, so this demotion moves no candidate.

## 3.5 swift — 0 demotions

All 17 spellings declare. `Int128` and `UInt128` declare fine as plain
Swift parameters; the swift misses in §5.3 are NOT about declarability.

---

# 4. The reduction recomputed on the corrected inventory

`legality_filter3.py` is `legality_filter2.py`'s arithmetic with one
input swapped: the core is read from `type_inventory3.json` instead of
`type_inventory2.json`. The rules are untouched (`legality_rules.json`
is read as it stands) and `core_rule2.scalar_core` is the same
membership test.

```
lang    core2  core3       naive2     naive3     compile2   compile3
c          56     25        57400      11675        51829      10085
cpp        56     28        79352      20076        70991      17364
go         14     14         3864       3864          553        553
rust       15     15         5115       5115         1993       1993
swift      17     17         8126       8126         4187       4187
TOTAL                      153857      48856       129553      34182
```

- `naive` is the cross-product of operator units with the core.
- `compile` is what the filter would send to a compiler: rule-admitted
  candidates plus the candidates of operator units for which no rule was
  extracted.
- The candidate space falls from **129,553 to 34,182** — the same
  129,553 the regeneration actually compiled, against 34,182 it would
  compile now. 29,288 of those were accepted, so the corrected filter's
  compile budget is within 4,894 of the accepted count.
- Only c and c++ move. go, rust and swift do not lose one core member,
  because their authorities are their own type checkers and stdlib
  rather than a compiler-internal representation table.

The 31 spellings c's core loses, and the 28 c++ loses, are listed row by
row in `legality_reduction3.json :: core_sizes_v2_vs_v3[*].left_the_core`.

---

# 5. The re-validation against what the compilers actually did

## 5.1 What was joined to what

`regen_validate1.py` reads the 326 regeneration stores
(`trickle_store/op_units2_*.json`) and nothing else. It compiles
nothing. The 8 re-capture stores (`op_units_recapture_*`) are a
different population — the ORIGINAL corpus re-captured for verbatim
testimony — and are excluded by filename, counted and named in the
output.

Each probe's record already carries what the join needs: its holder
types, whether it was accepted (a `ship` extraction present, no
`refused` text), the filter's own verdict written at generation time
(`meta.filter_verdict`), its rule ids, and its operator UNIT id.

## 5.2 The holder question, which is the witness's own test

```
probes 129553  accepted 29288  refused 100265
  holders all declarable : accepted 29288  refused  4894
  a holder demoted       : accepted     0  refused 95371
```

- **95,371 of the 100,265 refusals (95.1%) are probes carrying a type
  this target refuses to declare.** Round 9's correction estimated
  ~91,000; the measured figure is 95,371.
- **0 accepted probes carry a demoted type.** This is the check that
  could have refuted the second witness: one acceptance would mean the
  declaration lane demoted a type the probe lane can use. There are
  none, over all 29,288 accepted probes.
- Per language, the demoted-holder refusals are c 41,744 of 41,819 and
  cpp 53,627 of 53,921; go, rust and swift have **zero**, which is the
  same fact §4 shows from the other side — their cores never contained
  a non-declarable type.

## 5.3 The operator question, and every remaining miss

Inside the probes whose holders are all declarable, the oracle's own
recorded verdict is scored against accept/refuse. `no_rule` is out of
scope by construction: the filter passes those to the compiler instead
of judging them.

```
oracle scope 28552  hits 28272  quirk agreements 4  misses 276  agreement 99.0%
  c      scope   9860 hits   9860 agree 100.0%  out-of-scope 225
  cpp    scope  16384 hits  16380 agree 100.0%  out-of-scope 980
  go     scope    469 hits    469 agree 100.0%  out-of-scope 84
  rust   scope    508 hits    508 agree 100.0%  out-of-scope 1485
  swift  scope   1331 hits   1055 agree  79.3%  out-of-scope 2856
```

The 28,552 in-scope figure is independently the `filtered_legal` total
in §4's recomputation — the same number reached from the candidate side
and from the compiled side.

The 4,894 declarable-holder refusals account exactly:

| what | how many |
|---|---:|
| on an operator unit with no extracted rule (passed to the compiler by design) | 4,614 |
| the ratified c++ truth-value quirk, scored as agreement | 4 |
| genuine misses: predicted legal, compiler refused | 276 |
| **total** | **4,894** |

### 5.3.1 The 4 quirk agreements, verbatim

```
cpp/probe_452 bool cpp/opunit_32 clang_CheckIncrementDecrementOperand_no_truth_value_increment
   error: ISO C++17 does not allow incrementing expression of type bool [-Wincrement-bool]
cpp/probe_508 bool cpp/opunit_34 clang_CheckIncrementDecrementOperand_no_truth_value_decrement
   error: cannot decrement expression of type bool
cpp/probe_788 bool cpp/opunit_25 clang_CheckIncrementDecrementOperand_no_truth_value_increment
cpp/probe_844 bool cpp/opunit_26 clang_CheckIncrementDecrementOperand_no_truth_value_decrement
```

These are the four `legality_quirks.json` already annotates under the owner's
2026-09-01 ruling ("if c++ allows it and someone can use it with
intention, its valid"), keyed by RULE ID. Scored as agreement, listed
separately, refusal text kept.

### 5.3.2 The 276 misses are one cause, and it is not a legality cause

Every one of the 276 carries the same diagnostic shape, and the example
row, verbatim:

```
swift/probe_375  Int with Int128  swift/opunit_11
/work/regen_swift_c0000/u/n375/unit.swift:3:13: error: method cannot be
marked @_cdecl because the type of the parameter 2 cannot be represented
in Objective-C
```

Walked with values: `probe_gen.py :: emit_swift` decides whether to
attach `@_cdecl` by testing the RESULT type against a six-name set
(`Int32, Int64, UInt64, Float, Double, Bool`). For `a + b` with `a: Int`
and `b: Int128` the result is `Int`, which is in that set, so `@_cdecl`
is attached — and swift then refuses, because the second PARAMETER is a
128-bit integer that cannot be exposed to C. The operand shape is legal
Swift; the export attribute is what fails.

Confirmed mechanically over the whole miss set: 44 distinct holder pairs
carry the 276 misses, and **0 of the 44 lack a 128-bit holder**.

So the legality oracle made no wrong legality prediction in this
population at all. Agreement stated honestly two ways: 99.0% counting
the emitter defect against the oracle, 100.0% in every language whose
probe emitter does not attach an export attribute.

---

# 6. Findings

- **F45-1 — the inventory over-admitted by 85 spellings of 208, and it
  was one authority's fault.** clang's `BuiltinTypes.def` is an
  inventory of everything clang can REPRESENT, including targets and
  language modes this lane never selects. Every demotion outside c/c++
  is a type checker's internal vocabulary (go) or an unsized type
  (rust). Evidence: forced by construction — 416 compilations, each
  refusal in the compiler's own words.
- **F45-2 — the second witness is not refuted by a single accepted
  probe.** 0 of 29,288 accepted probes carry a demoted type. Evidence:
  forced by construction, over the whole accepted population.
- **F45-3 — 95,371 of the 100,265 refusals are type-declaration
  refusals, not operator refusals.** The correction's ~91,000 estimate
  was low by about 4,400. Evidence: forced by construction.
- **F45-4 — the swift probe emitter's `@_cdecl` test reads the result
  type and ignores the parameter types.** 276 refusals, one cause, no
  legality content. The fix is in `probe_gen.py :: emit_swift`: attach
  `@_cdecl` only when the result AND every parameter is C-representable.
  NOT MADE HERE — this task does not re-run the regeneration, and
  changing the emitter changes what a future run generates. Evidence:
  the tool's own testimony (swiftc's diagnostic) plus a whole-population
  holder tally.
- **F45-5 — 4,614 refusals remain on operator units with no extracted
  rule.** rust and swift carry 4,179 of them. This is the same residue
  log 127 §4 named; the second witness does not touch it, and it is the
  next place a reduction can come from.
- **F45-6 — `__fp16` is the one type whose two declaration forms
  disagree**, and the disagreement is exactly the one that matters for
  probes. Recorded in `type_inventory3.json :: forms_disagree`. Had the
  witness compiled only variables, the type would have stayed in the
  core.

---

# 7. Guards, and zero regressions

## 7.1 The spelling-key check on every JSON written

```
$ /tmp/reconnect_venv/bin/python3 type_inventory3.py
operator inventory: 91 tokens read from probe_manifest_*.json
PASS type_inventory3.json -- no operator token in any key, grouping, pairing or row structure
PASS type_demotions1.json -- no operator token in any key, grouping, pairing or row structure

$ /tmp/reconnect_venv/bin/python3 legality_filter3.py
PASS legality_reduction3.json -- no operator token in any key, grouping, pairing or row structure

$ /tmp/reconnect_venv/bin/python3 regen_validate1.py
PASS regen_witness_validation1.json -- no operator token in any key, grouping, pairing or row structure
```

Each program deletes its own output and exits non-zero on failure. That
happened once, and is recorded rather than hidden: the first cut of
`type_inventory3.py` stored compiler words in a field named
`compiler_message`, and the guard refused the file because a go
diagnostic's words contain an operator token on a structure field. The
fix is general, not per-name: every field holding compiler words is
named `refusal`, the name this line already uses for stored compiler
testimony and which the guard already treats as prose.

```
FAIL type_demotions1.json -- 6 spelling-keyed place(s)
     $.demotions[168].compiler_message
         operator token '..' on a structure field
REFUSED OWN OUTPUT: spelling guard failed
```

## 7.2 Nothing existing was modified

```
$ git status --porcelain Research/op_pipeline | grep -c '^ M'
0
$ git diff --stat HEAD -- Research/op_pipeline/type_inventory2.json \
    Research/op_pipeline/legality_reduction2.json \
    Research/op_pipeline/core_rule2.py Research/op_pipeline/legality_rules.json
(empty)
$ ls -la Research/op_pipeline/type_inventory2.json
-rw-rw-r-- 1 <user> <user> 204153 Sep  1 18:22 .../type_inventory2.json
```

Inventory 2 still carries its 2026-09-01 18:22 timestamp. Every artifact
of this task is a new name. The regeneration was NOT re-run: the trickle
state file was not touched and no `regen_*` lane was executed.

The daemon has already committed the work (`git log`: `auto: 2 files
(regen_validate1.py, regen_witness_validation1.json)` and the commits
before it); nothing is held back.

---

# 8. Complete file inventory

Every file this task created, all new:

| path | what it is |
|---|---|
| `Research/op_pipeline/declare_lane.py` | writes the declaration lanes; the source templates for both forms, the probe lanes' own flags, the verbatim codec copied into the driver |
| `Research/op_pipeline/declare_lanes/declare_c.sh` | the exact lane that ran for c |
| `Research/op_pipeline/declare_lanes/declare_cpp.sh` | the exact lane that ran for cpp |
| `Research/op_pipeline/declare_lanes/declare_go.sh` | the exact lane that ran for go |
| `Research/op_pipeline/declare_lanes/declare_rust.sh` | the exact lane that ran for rust |
| `Research/op_pipeline/declare_lanes/declare_swift.sh` | the exact lane that ran for swift |
| `Research/op_pipeline/declare_raw/decl_c.txt` | c's lane product, verbatim-escaped (148 records) |
| `Research/op_pipeline/declare_raw/decl_cpp.txt` | cpp's lane product (148 records) |
| `Research/op_pipeline/declare_raw/decl_go.txt` | go's lane product (52 records) |
| `Research/op_pipeline/declare_raw/decl_rust.txt` | rust's lane product (34 records) |
| `Research/op_pipeline/declare_raw/decl_swift.txt` | swift's lane product (34 records) |
| `Research/op_pipeline/type_inventory3.py` | folds the lane products into the inventory; decides membership on the parameter form |
| `Research/op_pipeline/type_inventory3.json` | extracted AND declarable — 123 rows, inventory-2 row shape plus the `declarable` column |
| `Research/op_pipeline/type_demotions1.json` | every demoted row with the compiler's words verbatim (85 compiler demotions, 122 not-a-spelling) |
| `Research/op_pipeline/legality_filter3.py` | the reduction recomputed over inventory 3 |
| `Research/op_pipeline/legality_reduction3.json` | 48,856 naive / 28,552 legal / 34,182 must-compile, with the per-language core delta |
| `Research/op_pipeline/regen_validate1.py` | joins the corrected inventory to the regeneration's own accept/refuse |
| `Research/op_pipeline/regen_witness_validation1.json` | the 2x2 holder table, the per-language oracle scoring, the quirk agreements, the miss shapes with holder tallies |
| `DevComms/log_137_task45_type_second_witness.md` | this page |

Read, never written: `type_inventory2.json`, `legality_rules.json`,
`legality_quirks.json`, `core_rule2.py`, `legality_filter.py`,
`legality_filter2.py`, `lane_gen.py`, `verbatim_diag.py`,
`trickle_store/*` (326 regeneration stores + 8 excluded re-capture
stores).

---

# 9. Evidence class per claim

| claim | class |
|---|---|
| 85 spellings are not declarable on this target | forced by construction (416 compilations; each refusal is the compiler's own refusal of a file containing only that declaration) |
| the reason each one gives | the tool's own testimony (the diagnostic text, stored verbatim through the escape codec) |
| 0 accepted probes carry a demoted type | forced by construction, exhaustive over 29,288 |
| 95,371 refusals are type-declaration refusals | forced by construction, exhaustive over 100,265 |
| the 276 swift misses are the `@_cdecl` emitter | the tool's own testimony (swiftc's words) + a whole-population holder tally; the emitter's rule is read in `probe_gen.py :: emit_swift` |
| the 4 c++ agreements are a quirk, not a miss | ratified intention (the owner, 2026-09-01), applied by rule id |
| the pins are unchanged | the tool's own testimony, printed by the lanes themselves before compiling |

---

# 10. For the owner — the two calls this raises

1. **F45-4, the swift `@_cdecl` emitter.** Fixing it makes 276 refused
   probes compile, and it changes the probe generator, so a future
   regeneration would differ from the banked one. Not made in this task.
2. **F45-5, the 4,614 no-rule refusals.** rust and swift carry most of
   them. Extracting rules for those operator units is the next available
   reduction; it is a different authority-reading task, not a witness
   task.
