# log 125 — TASK 35: swift's extracted type authority

Date: 2026-09-01. Session: Claude Code, TASK 35 of
`DevComms/log_123_claude_code_task_briefs_round7.md`.

POPULATION, said once and applying to every figure below: the FIVE
COMPILED LANGUAGES' probe corpus as it stands on disk today —
4,440 candidate probes, 1,779 the compiler accepted, 2,661 it
refused; swift's slice of that is 1,086 candidates, 167 accepted,
919 refused. Same corpus log_116 measured, unchanged by this task.
No interpreter unit is counted anywhere on this page.

---

# 1. What was done, in plain words

Log 116 extracted a type inventory for five languages and got
nothing for swift: no swift source was on the machine, so swift's
six rows rested on the corpus alone — the corpus confirming the six
spellings the corpus itself had used, which proves nothing. Log 122
then put the source on disk at the toolchain pin. This task read
swift's scalar type authority out of it.

Three routes were run, and they agree.

- The PINNED SOURCE. Swift's concrete scalar types are not written
  down anywhere in the stdlib as a list; they are produced by two
  `.gyb` templates that loop over a generator. So the templates'
  own generation loops were read out of the templates as data — the
  loop line, the variable binding, and the `public struct ${...}`
  declaration that consumes it — and then the generator named on
  that loop line was imported from the same pinned tree and called.
  The list is the template's own. Three types are declared plainly
  rather than generated (`Bool`, `Int128`, `UInt128`) and were read
  from their declaration lines.
- The INSTALLED MODULE INTERFACE (the brief's route (a)). The
  toolchain's own `Swift.swiftinterface` for this target, copied
  byte-identical out of the Airlock container, read for its
  top-level `public struct` declarations and their protocol
  conformances.
- The COMPILER ITSELF (the tool the brief's route (b) names). Each
  extracted spelling was handed to `swift-frontend -typecheck` in a
  one-parameter declaration, with a control spelling that no
  authority admits, to show the check can say no.

The result: 17 swift scalar types, every one of them admitted by
BOTH enumerating routes and typechecked by the compiler, against
the 6 corpus-only rows log 116 had. Validation against the corpus
was then run by log_116's own validator, unmodified, over the new
inventory: zero holes, and swift's row is no longer the tautology
log 116 flagged. The other four languages' numbers are byte-for-byte
what log 116 recorded.

One thing the brief asked about is missing from the disk: log_121
does not exist. §9 records that.

## 1.1 The vocabulary this page uses

- **witness** — a source that admits a type spelling. This page adds
  two enumerating witnesses (`compiler_source`,
  `installed_module_interface`) and one confirming witness
  (`compiler_typecheck`) to log 116's three.
- **enumerating witness** — one that can produce the whole list on
  its own. A confirming witness can only answer about a spelling it
  is handed, so its silence is not evidence.
- **scalar core** — log 116's rule, unchanged and applied by log
  116's own code: a type is in the core when an EXTRACTED class
  marking calls it an integer, a float or a truth value; an unmarked
  type is not guessed, it is listed as undecided.
- **gyb** — swift's stdlib template preprocessor. A `.gyb` file is
  swift source with embedded python; lines starting `%` are the
  python, `${...}` interpolates a python value.

---

# 2. Route one — the pinned source, with the values moving

## 2.1 The pin, quoted from the repository itself

The brief named `Sources/swift-6.0.3-RELEASE` and
noted that `Sources/swift` also exists. Both were
checked. The second is the stale, unusable clone log 122 described:

```
$ git -C Sources/swift log -1 --format='%H %s'
fatal: your current branch 'master' does not have any commits yet

$ git -C Sources/swift-6.0.3-RELEASE log -1 --format='%H %s'
6a862d2eb7128ff1f317b07e8ad1a6da939775f3 Change version string to 'swift-6.0.3-RELEASE'

$ git -C Sources/swift-6.0.3-RELEASE describe --all
tags/swift-6.0.3-RELEASE
```

Nothing was read from `Sources/swift`. The commit matches the one
log 122 recorded, and the extractor re-checks that equality at run
time and writes the answer into its output
(`matches_log_122_recorded_commit: true`).

Evidence class: quoted from the artifact (the repository's own git).

## 2.2 The integer template, walked

### 2.2.1 What is quoted out of the template

```
IntegerTypes.swift.gyb:1066  % for self_type in all_integer_types(word_bits):
IntegerTypes.swift.gyb:1070  %   Self = self_type.stdlib_name
IntegerTypes.swift.gyb:1088  public struct ${Self}
```

Read as data: the loop variable is `self_type`, the generator is
`all_integer_types`, its argument is `word_bits`, the template
variable holding the spelling is `Self`, and the attribute it is
bound to is `stdlib_name`. Nothing here is a guess about swift; it
is four strings lifted off three lines.

### 2.2.2 The generator, called from the same pinned tree

`utils/SwiftIntTypes.py` is imported by path out of the pinned
checkout and `all_integer_types` is called. Its own body:

```
_all_integer_type_bitwidths = [8, 16, 32, 64]

def all_integer_types(word_bits):
    for bitwidth in _all_integer_type_bitwidths:
        for is_signed in [False, True]:
            yield SwiftIntegerType(is_word=False, bits=bitwidth, is_signed=is_signed)
    for is_signed in [False, True]:
        yield SwiftIntegerType(is_word=True, bits=word_bits, is_signed=is_signed)
```

and the spelling is derived inside the class, not by me:

```
self.stdlib_name = ('' if is_signed else 'U') + 'Int' + ('' if is_word else str(bits))
```

Values moving, first two turns of the loop and the last:

```
bitwidth=8,  is_signed=False -> stdlib_name = 'U' + 'Int' + '8'  = UInt8
bitwidth=8,  is_signed=True  -> stdlib_name = ''  + 'Int' + '8'  = Int8
...
is_word=True, is_signed=True -> stdlib_name = ''  + 'Int' + ''   = Int
```

Ten spellings: `UInt8 Int8 UInt16 Int16 UInt32 Int32 UInt64 Int64
UInt Int`.

### 2.2.3 The one parameter that had to be supplied, and why it is not a guess

`word_bits` is the template's own line
`word_bits = int(CMAKE_SIZEOF_VOID_P) * 8` — gyb takes the pointer
size from the build. It is set to 8 here, and recorded in the output
as a TARGET parameter (`x86_64-unknown-linux-gnu`), not as a claim
about swift. It changes no spelling: `Int` and `UInt` are word-sized
whatever the width, and the width rides in the row as `bits`.

### 2.2.4 The class marking

From the generator's own object: `SwiftIntegerType.is_signed` →
`integer_signed` / `integer_unsigned`, the two strings log 116's
validator already recognises.

## 2.3 The floating-point template, walked

```
FloatingPointTypes.swift.gyb:27  % for self_type in all_floating_point_types():
FloatingPointTypes.swift.gyb:29  Self = self_type.stdlib_name
FloatingPointTypes.swift.gyb:77  public struct ${Self} {
```

`utils/SwiftFloatingPointTypes.py :: floating_point_bits_to_type()`
is a four-entry table keyed by bit width, and
`all_floating_point_types()` returns its values: `Float16` (16),
`Float` (32), `Double` (64), `Float80` (80). Class marking: the
template's subject is floating-point types, so all four are `float`.

The template wraps two of the four in a target guard, and the guard
is captured VERBATIM rather than evaluated by me:

```
% if bits == 80:
#if !(os(Windows) || os(Android) || ($Embedded && !os(Linux) && !(os(macOS) || os(iOS) || os(watchOS) || os(tvOS)))) && (arch(i386) || arch(x86_64))
% elif bits == 16:
#if !((os(macOS) || targetEnvironment(macCatalyst)) && arch(x86_64))
```

Whether those two survive on THIS target is not decided by reading
the guard — it is answered by routes two and three, which look at
what the installed toolchain for `x86_64-unknown-linux-gnu`
actually carries. Both say yes (§3, §4).

## 2.4 The three plain declarations

| spelling | declaration read | class marking read |
|---|---|---|
| `Bool` | `Bool.swift:64 public struct Bool: Sendable {` | `Bool.swift:142 extension Bool: _ExpressibleByBuiltinBooleanLiteral, ExpressibleByBooleanLiteral {` |
| `Int128` | `Int128.swift:18 public struct Int128: Sendable {` | `Int128.swift:461 extension Int128: FixedWidthInteger, SignedInteger {` |
| `UInt128` | `UInt128.swift:18 public struct UInt128: Sendable {` | `UInt128.swift:521 extension UInt128: FixedWidthInteger, UnsignedInteger {` |

## 2.5 Integers.swift declares no concrete type — counted, not assumed

The brief named `Integers.swift` as an authority file. It is the
protocol file; the concrete integers come from
`IntegerTypes.swift.gyb`. Computed at run time and written into the
output as finding F35-1:

```
top_level_public_struct_lines   = 0
top_level_public_protocol_lines = 8
```

Evidence class: computed over the pinned file.

---

# 3. Route two — the installed module interface (the brief's route (a))

## 3.1 Which side of the container wall this ran on

The toolchain is INSIDE the Airlock container, not on the host:

```
$ ls -d /persist                       # on the host
ls: cannot access '/persist': No such file or directory
$ which swift swiftc                   # on the host
(no output)
$ podman exec sandbox-runner ls /persist/swift/usr/bin/swift
/persist/swift/usr/bin/swift
```

So a host-side absence check proves nothing about the toolchain —
it only proves the host is not the container. Every route-two and
route-three command below ran inside `sandbox-runner`.

## 3.2 The file, copied byte-identical, and its own pin

```
$ podman exec sandbox-runner sha256sum /persist/swift/usr/lib/swift_static/linux/Swift.swiftmodule/x86_64-unknown-linux-gnu.swiftinterface
f23b753be474a57c7df8af76353522046092d515d8a9c3c937237fe5c776a466  /persist/...
$ sha256sum swift_stdlib_x86_64-unknown-linux-gnu.swiftinterface
f23b753be474a57c7df8af76353522046092d515d8a9c3c937237fe5c776a466  swift_stdlib_x86_64-unknown-linux-gnu.swiftinterface
```

Its first two lines carry its own pin, and the pin is the SAME
release as the source clone — which is why the two routes are
comparable at all:

```
// swift-interface-format-version: 1.0
// swift-compiler-version: Swift version 6.0.3 (swift-6.0.3-RELEASE)
```

Evidence class: quoted from the artifact.

## 3.3 What is read, with the lines that carry it

Top-level `public struct` declarations, plus top-level
`extension Swift.<T> : ...` lines for conformances declared away
from the struct. Four examples, verbatim:

```
36187:@frozen public struct Int32 : Swift.FixedWidthInteger, Swift.SignedInteger, Swift._ExpressibleByBuiltinIntegerLiteral {
32349:@frozen public struct Double {
32372:extension Swift.Double : Swift.BinaryFloatingPoint {
 2332:@frozen public struct Bool : Swift.Sendable {
 2350:extension Swift.Bool : Swift._ExpressibleByBuiltinBooleanLiteral, Swift.ExpressibleByBooleanLiteral {
```

The class marking is the conformance, not the name:
`Swift.SignedInteger` → `integer_signed`, `Swift.UnsignedInteger` →
`integer_unsigned`, `Swift.BinaryFloatingPoint` → `float`,
`Swift.ExpressibleByBooleanLiteral` → `truth_value`. A declaration
carrying none of those is not in the scalar reading at all, which is
what excludes `String`, `Character`, `Duration`, `Hasher` and the
rest of the 78 structs the file declares.

---

# 4. Route three — the compiler's own answer (the tool route (b) names)

## 4.1 What was asked, and the negative control

For each of the 17 spellings, a one-parameter declaration was
typechecked by the installed frontend:

```
$ podman exec -i sandbox-runner bash -lc \
    'cat > /tmp/t35_one.swift && /persist/swift/usr/bin/swift-frontend \
       -typecheck -target x86_64-unknown-linux-gnu /tmp/t35_one.swift 2>&1'
  <<< 'func probe(x: Float80) {}'
(no diagnostic; exit 0)
```

This is finding F35-4 in the artifact. 17 of 17 accepted. The control, a spelling no authority admits,
is refused — so the check has teeth:

```
func probe(x: Int13) {}
/tmp/t35_one.swift:1:15: error: cannot find type 'Int13' in scope
1 | func probe(x: Int13) {}
  |               `- error: cannot find type 'Int13' in scope
exit 1
```

That diagnostic is stored verbatim in `swift_type_authority.json`,
including its `|` characters — the substitution defect log 121
recorded for `lane_gen.py` is not in this path, and nothing here
passes through `firstline()`.

The version, quoted from the tool:
`Swift version 6.0.3 (swift-6.0.3-RELEASE)`.

## 4.2 Why this is a confirming witness and not a third enumeration

A typecheck answers only about a spelling it is handed. It cannot
produce the list, so it can never contradict the two enumerating
routes by omission — only by refusing one of their rows, which it
did not do.

## 4.3 What route (b) as literally written could not do

`swiftc -emit-module-interface` would emit the interface of a module
compiled here, not the stdlib's; the stdlib's interface is not
rebuilt on this machine, and route (a) already carries it. Separately
the driver binaries cannot start in this container at all:

```
$ podman exec sandbox-runner /persist/swift/usr/bin/swiftc --version
/persist/swift/usr/bin/swiftc: error while loading shared libraries: libncurses.so.6: cannot open shared object file: No such file or directory
```

`swift-frontend` has no such dependence and runs, which is the route
§4.1 used. Evidence class: the tool's own testimony.

---

# 5. Agreement, and the rows that came out

## 5.1 The acceptance bar, computed

```
route_source     admitted 17
route_installed  admitted 17
in both          17
route_source only     []
route_installed only  []
class-marking disagreements  []
```

All 17 are admitted by both enumerating routes and typechecked by
the compiler — computed, not asserted:

```
$ /tmp/reconnect_venv/bin/python3 -c "...type_inventory2.json..."
rows total 17 two-route admitted 17 two-route scalar core 16
```

Findings F35-2 and F35-3 in the output record the agreement. Had
either differed, the difference would stand as the finding; no
preference was available to resolve one.

## 5.2 The 17 rows

| swift type | class | source | interface | typecheck | corpus |
|---|---|---|---|---|---|
| Bool | truth_value | yes | yes | yes | yes |
| Double | float | yes | yes | yes | yes |
| Float | float | yes | yes | yes | yes |
| Float16 | float | yes | yes | yes | - |
| Float80 | float | yes | yes | yes | - |
| Int | integer_signed | yes | yes | yes | - |
| Int8 | integer_signed | yes | yes | yes | - |
| Int16 | integer_signed | yes | yes | yes | - |
| Int32 | integer_signed | yes | yes | yes | yes |
| Int64 | integer_signed | yes | yes | yes | yes |
| Int128 | integer_signed | yes | yes | yes | - |
| UInt | integer_unsigned | yes | yes | yes | - |
| UInt8 | integer_unsigned | yes | yes | yes | - |
| UInt16 | integer_unsigned | yes | yes | yes | - |
| UInt32 | integer_unsigned | yes | yes | yes | - |
| UInt64 | integer_unsigned | yes | yes | yes | yes |
| UInt128 | integer_unsigned | yes | yes | yes | - |

The two target-guarded floats, `Float16` and `Float80`, are on this
target: the installed interface declares both and the compiler
typechecks both.

## 5.3 Where the rows were written, and why not into type_inventory.json

The brief's outer instruction is new files only, and the task text
says "add swift's rows in type_inventory.json's exact style". Those
are reconciled by SUPERSEDING rather than editing:
`type_inventory2.json` is `type_inventory.json` with the four
extracted languages copied verbatim and swift's record rebuilt, in
the same row shape (a unit object per type carrying `language`,
`id`, `spelling`, `admitted_by`, `class`, `class_source`).
`type_inventory.json` is untouched on disk (§7). A companion file
holding swift alone was the alternative and was not taken: a later
stage reading one inventory and getting four languages' worth of
truth would be a trap.

---

# 6. Validation against the corpus, run by log_116's own validator

## 6.1 How "exactly as log_116 did" was met

Not re-implemented — the same program. `type_inventory_validate.py`
hard-codes its input and output names, so
`type_inventory2_validate.py` makes a scratch directory, symlinks
the validator, the spelling guard and every input into it, symlinks
`type_inventory2.json` under the name the validator expects, runs it
there, and copies its two outputs back under new names. The
validator itself is byte-identical (§7), and everything it writes
lands in the scratch directory.

## 6.2 Direction two — spellings the corpus used that no authority admits

| language | accepted probes | operand spellings used | spellings no authority admits |
|---|---|---|---|
| c | 610 | 6 | 0 |
| cpp | 770 | 6 | 0 |
| go | 107 | 6 | 0 |
| rust | 125 | 6 | 0 |
| swift | 167 | 6 | 0 |
| **total** | **1,779** | | **0** |

Same zero as log 116 — but swift's zero has changed meaning. Log 116
stated the honesty note that swift's admitting witness WAS the
corpus, so the row was a tautology. It is not one now: the six
spellings the accepted probes use (`Bool Double Float Int32 Int64
UInt64`) are each admitted by the pinned source and by the installed
interface independently of the corpus. Finding F35-5.

## 6.3 Direction one — what the hand-written six missed, swift's row filled in

| language | extracted scalar core | undecided | hand-written | never probed | corpus candidates | predicted at full core |
|---|---|---|---|---|---|---|
| c | 56 | 18 | 6 | 53 | 750 | 57,400 |
| cpp | 56 | 18 | 6 | 53 | 1,002 | 79,352 |
| go | 14 | 0 | 6 | 8 | 744 | 3,864 |
| rust | 14 | 3 | 6 | 9 | 858 | 4,466 |
| swift | **16** | **1** | 6 | **11** | 1,086 | **7,216** |
| **total** | | | **30** | | **4,440** | **152,298** |

Swift's row was `0 / 6 / 6 / 0 / 1,086 / 0` in log 116. The four
other rows are unchanged, and the total moves by exactly swift's
contribution: 145,082 + 7,216 = 152,298.

### 6.3.1 The growth number, walked with values

The multiplier comes from the corpus's own candidate counts and
never touches an operator list:

```
op_units_swift.json                     candidates = 1,086
  of which arity == "unary"                        =   114
  of which arity == "binary"                       =   972
h = len(HOLDERS["swift"])                          =     6

unary_operator_count  = 114 / 6      = 19.0
binary_operator_count = 972 / (6*6)  = 27.0

at h' = 16 (the extracted swift scalar core):
  19.0 * 16        =    304   unary candidates
  27.0 * 16 * 16   =  6,912   binary candidates
                     -------
                      7,216   candidate probes
```

1,086 becomes 7,216: 6.64 times the swift lane. With `Bool` counted
(see L125-1 below) h' = 17 and the figure is 8,126.

### 6.3.2 The eleven swift types never probed

`Float16 Float80 Int Int8 Int16 Int128 UInt UInt8 UInt16 UInt32
UInt128`. The hand-written six carried `Int32 Int64 UInt64 Float
Double Bool`, so both 128-bit widths, both word-sized widths, every
narrow width and both edge-precision floats were never asked about.

## 6.4 Direction three — unchanged, and why

Swift's refusal breakdown is untouched by this task: 919 refused,
42 cells, 24 all-refused, 18 mixed, 0 all-accepted, 70.5% of
refusals a type pair alone explains. Cells are built from the SIX
probed holders, and no probe was regenerated here, so the cell
structure cannot move. Log 116's reading stands.

## 6.5 The two findings this validation produced about the RULE, not about swift

- **L125-1 — the truth-value marking has no seat in `NUMERIC_MARKS`.**
  (Recorded in this log, not in the artifact's finding list: it is a
  property of the shared rule, not of swift.)
  Log 116's stated rule counts "an integer, a float or a truth
  value" as scalar core, but its code's `NUMERIC_MARKS` tuple is
  `("integer_signed", "integer_unsigned", "float",
  "numeric_grammar_marked")` with no truth-value entry, so a boolean
  reaches a core only through go's separate `IsBoolean` flag path.
  Swift's `Bool` therefore lands in `undecided` — exactly as rust's
  `bool` does. The rule was NOT widened here to make swift's number
  bigger; the divergence is reported and both figures are given
  (core 16 → 7,216 candidates; core plus `Bool` 17 → 8,126).
  Whether the shared rule gains a truth-value mark is the owner's call.
- **L125-2 — the two-authority column reads `not defined` for swift
  although swift now has two enumerating routes.** The validator
  tests for witnesses literally named `grammar` and
  `compiler_table`; swift's are named `compiler_source` and
  `installed_module_interface`. Computed here instead, in the same
  shape: swift's two-route admitted set is 17 and its two-route
  scalar core is 16 — the same 16, because both routes admit every
  row. So the number the column would show is 7,216, identical to
  the full-core figure. Nothing is hidden by the `not defined`; it
  is a witness-naming mismatch, and widening the validator's tuple
  would have meant editing log_116's file, which was refused.

---

# 7. Zero regressions, verified programmatically

Baseline taken before any file was written, re-checked after
everything was written:

```
$ sha256sum type_inventory.json type_inventory_validation.json type_inventory.py \
            type_inventory_validate.py type_inventory.md type_inventory_validation.md \
  | diff - /tmp/.../log116_baseline.sha && echo "IDENTICAL - zero regressions"
IDENTICAL - zero regressions
```

The baseline hashes, for the record:

```
6ccde6783976a43008495e8e4b31f15bc691886231a6eee7aac2ec926bac3751  type_inventory.json
a10a891e043fbc6d5d2e63e09ba71c35d3a993d702c9599e8cd28562055df8b5  type_inventory_validation.json
f5f01ccace0e2f612d09a6f3635d9bc665cf19469cf084fe826e8e5836f3b853  type_inventory.py
360b6256445cd68b2d2fd711d2ccbf36a647a7dae2ec6d67cfe3d65f77f5bde5  type_inventory_validate.py
182b4de25fe40ab1a0ab9e4aef31de5f2724dd3726ad794543c510ad2e411580  type_inventory.md
07bc9298ca89a521c2007c8b2bac8eae746a80eec703f529d875e801c271ed38  type_inventory_validation.md
```

`type_inventory2_validate.py` also carries this check internally: it
hashes those six before and after its run and aborts with
`REGRESSION:` if any moved. It printed
`log_116 artifacts unchanged: 6 checked`.

`probe_gen.py` was not touched either; nothing was regenerated.

---

# 8. The spelling ban, and the guard's PASS lines

Every output JSON was run through `check_no_spelling_keys.py`, by
the producing program itself, which removes its own output and exits
nonzero on failure. Pasted verbatim:

```
$ /tmp/reconnect_venv/bin/python3 swift_type_authority.py
operator inventory: 91 tokens read from probe_manifest_*.json
PASS swift_type_authority.json -- no operator token in any key, grouping, pairing or row structure
PASS type_inventory2.json -- no operator token in any key, grouping, pairing or row structure

$ /tmp/reconnect_venv/bin/python3 type_inventory2_validate.py
operator inventory: 91 tokens read from probe_manifest_*.json
PASS type_inventory_validation.json -- no operator token in any key, grouping, pairing or row structure
operator inventory: 91 tokens read from probe_manifest_*.json
PASS type_inventory2_validation.json -- no operator token in any key, grouping, pairing or row structure
log_116 artifacts unchanged: 6 checked
```

Two notes on the ban doing real work in this task, rather than
ceremony:

- `utils/SwiftIntTypes.py` in the pinned tree carries operator-name
  lists (`all_integer_binary_operator_names()` and three more). They
  are never called and never read; only the type generators are.
- Every type spelling in every output rides on a unit object with
  its own `language` and `id`, with the spelling in the `spelling`
  field — the display-label seat. No grouping, pairing or row
  structure anywhere in these files is keyed by a spelling.

---

# 9. The missing log, checked before it was reported

The brief cites "log 121 routes (a)/(b)". There is no log_121 in
this line's DevComms, and none anywhere under `~/Programming` except
an unrelated file in a different project:

```
$ find ~/Programming -name "*log_121*"
StressBot/RelevantProjects/PseudoCoup_v0/DevComms/log_121_reactivity_model.md
$ podman exec sandbox-runner find / -maxdepth 6 -name "log_121*"
(no output)
```

Both sides of the container wall were checked; the file is on
neither. `PseudoCoupHQ/DevComms/` listed 128 entries at the moment of the
check and log_121 was not among them. The routes were therefore taken from the brief's own
inline descriptions — "(a) installed stdlib interface files, (b)
`swiftc -emit-module-interface`" — and both are answered in §3 and
§4. Log 122 §3 independently names the same two routes, which is the
only corroboration available.

Evidence class: verified absence, both sides of the wall.

---

# 10. Complete file inventory

Created by this task, all of them new, all under
`PseudoCoupHQ/Research/op_pipeline/` except the last
two:

| file | bytes | what it is |
|---|---|---|
| `swift_type_authority.py` | 35,546 | the extractor: three routes, agreement, findings; refuses its own output on a guard failure |
| `swift_type_authority.json` | 61,762 | all three routes with their pins, the agreement, the five findings, the 17 rows |
| `swift_type_authority_typecheck.swift` | 186 | the one-file form of the typecheck route, kept as evidence |
| `swift_stdlib_x86_64-unknown-linux-gnu.swiftinterface` | 2,007,304 | the installed stdlib interface, copied byte-identical out of the container (hash in §3.2) |
| `type_inventory2.json` | 204,153 | the superseding inventory: four languages copied verbatim, swift rebuilt |
| `type_inventory2.md` | 1,634 | its readable rendering |
| `type_inventory2_validate.py` | 5,406 | the driver that runs log_116's validator unmodified over the new inventory |
| `type_inventory2_validation.json` | 90,700 | that validator's output, stamped with which inventory it measured |
| `type_inventory2_validation.md` | 1,213 | its readable rendering |
| `DevComms/log_125_task35_swift_authority.md` | this file | the report |

Modified: `Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`
— one dated entry appended under the single `# PROGRESS` heading.
Nothing else on disk was written.

The daemon commits; no commit was made by hand.

---

# 11. For the owner — the two calls this raises

Listed, not asked as a forced choice; the work above does not wait
on either.

1. **Does the shared scalar-core rule gain a truth-value mark?**
   Today `Bool` (swift) and `bool` (rust) sit in `undecided` while
   `bool` (c/cpp) sits in the core, because clang's table happens to
   mark it `UNSIGNED_TYPE`. Swift's figures both ways: 16 core →
   7,216 predicted candidates; 17 → 8,126.
2. **Probe regeneration sizing now includes swift.** Log 120 recorded
   the sizing as "Swift excluded either way". It is no longer
   excluded: swift's lane predicts 7,216 candidates at its extracted
   core against 1,086 today, and the five-language total at extracted
   cores is 152,298 against 4,440. Task 36's reduction report is the
   next input to that decision.
