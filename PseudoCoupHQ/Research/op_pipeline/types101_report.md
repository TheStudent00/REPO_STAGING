# types101 — dominant types: the join, over DWARF re-read from the compiler

Task t101b (closing task t101, which stopped correctly at step 1 with
a flag). Node:
`hq.research.compiler_graph.probes.type_inventory`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_0_probes/node_0_3_1_0_1_type_inventory/CORE_0_3_1_0_1_type_inventory.md`).
Master plan step: `CORE_0_3_research` §4.2 step 3.

Written 2026-09-06, superseding this file's 01:52 version, which is
now log_213's record, not this file's. The full account, with the
shell transcripts that reproduce every number here, is
`PRIVATE/PseudoCoupHQ/DevComms/log_217_task_t101b_dominant_types_join.md`.

---

## 1. The objects, one sentence each

- **A dominant type** (research CORE §1, verbatim) is one
  machine-level holder — a class (signed integer, unsigned integer,
  float, truth) at a width — with every language's spellings for it
  hanging off it, so that a language type resolves to the holder the
  machine distinguishes and no further.
- **The language type inventory**
  (`type_inventory2_core2.json`) is the LEFT side of the join: per
  language, per scalar-core spelling, a `normalised_class` and no
  width — c 56, cpp 56, go 14, rust 15, swift 17 spellings.
- **The DWARF parameter/result table** is the RIGHT side: log_213
  found the stored tables carried only `name` and `location`, so
  task t101b re-read `DW_AT_byte_size` and `DW_AT_encoding` straight
  from the compiler — `types101_anchor_dwarf.py` regenerated every
  accepted probe's source from its `meta`, compiled it at anchor
  flags only, walked `DW_AT_type` with pyelftools (the method in
  `dwarf_typed_key.py`, task 24), and deleted the binary — writing
  `types101_dwarf_rows.json` + 294 shards under `types101_dwarf_rows/`
  (92,127 rows: 61,060 parameter, 31,067 result, over 31,067 units).
- **The machine type key** (`type_key` on every pool entry of
  `the_pool5.json`, 88 distinct over 1,831 entries) is what the join
  makes readable: arrival register families and answer width, e.g.
  `rdi,rsi|32`.
- **The join** (`types101_join.py`) reads those DWARF rows, decides
  each holder from the encoding it finds (never from a spelling), and
  writes `types101_holders.json`, `types101_spellings.json`,
  `types101_entry_holders.json`.

## 2. Instance and the two bugs on the way here

- Instance: `PUBLIC/Airlock/instances/t101b.conf` (from
  `t97.conf`, cpus 6 / memory 8g, `ABORT_MEMORY_T101B` at 4 GB in the
  parent). Lanes: `t101b_l1_sample.sh` (sample 60, exit 0),
  `t101b_l2_all.sh` (all 31,067 accepted probes, exit 0, 532.2s),
  `t101b_l3_join.sh` (exit 1 — bug 1), `t101b_l4_join.sh` (exit 1 —
  bug 2, after bug 1's fix), `t101b_l5_join.sh` (exit 0),
  `t101b_l6_guard.sh` (the spelling-ban guard, exit 0).
- **Bug 1** (found by the session that stopped at the join step, fixed
  before this session started): `types101_join.py`'s `holders_table`
  built `off_holder` as `defaultdict(lambda: defaultdict(int))` keyed
  4 deep — `(lang, role, kind, holder)` — while the code that reads it
  back (`for hid, n in c.most_common()`) expects the value at
  `(lang, role, kind)` to itself be a `Counter` over holders. Fixed at
  cause, one line: `off_holder = collections.defaultdict(collections.Counter)`
  keyed 3 deep, matching the read side.
- **Bug 2** (found this session, when lane 4 got past bug 1's fix and
  hit a new stop): `entry_holders()` returned `dict(tot)` where `tot`
  is a `collections.Counter()`. A `Counter` answers a missing key with
  0 (`__missing__`); a plain `dict` raises `KeyError`. Every totals
  key this run actually populated (no compiled probe lacked DWARF
  rows: `members_compiled_without_rows` never got incremented) was
  therefore silently dropped by `dict(tot)`, and `main()`'s summary
  line's read of `ptot["members_compiled_without_rows"]` raised
  `KeyError: 'members_compiled_without_rows'`. Fixed at cause, one
  line: `return entries, keys, wd, tot, pool["meta"].get("generator")`
  — return the `Counter` itself, matching how every other totals
  object in this file is read.
- Both fixes are in `types101_join.py`; no other file changed.

## 3. Three DWARF rows, LITERAL (from `t101b_l1_sample.sh`'s log)

```
{"declared_spelling": "_Bool", "dwarf_byte_size": 1, "dwarf_encoding": "DW_ATE_boolean", "dwarf_encoding_absent_on_the_type": false, "dwarf_spelling": "_Bool", "dwarf_terminal_tag": "DW_TAG_base_type", "dwarf_type_chain": [{"byte_size": 1, "encoding": "DW_ATE_boolean", "name": "_Bool", "tag": "DW_TAG_base_type"}], "language": "c", "param_name": "a", "population": "regenerated", "position": 0, "probe_n": 1, "role": "parameter", "store_file": "op_units2_c_c0000.json", "subprogram_linkage_name": null, "subprogram_name": "op_1", "symbol": "op_1", "unit": "c/regen_1"}
{"declared_spelling": "float32", "dwarf_byte_size": 4, "dwarf_encoding": "DW_ATE_float", "dwarf_encoding_absent_on_the_type": false, "dwarf_spelling": "float32", "dwarf_terminal_tag": "DW_TAG_base_type", "dwarf_type_chain": [{"byte_size": 4, "encoding": "DW_ATE_float", "name": "float32", "tag": "DW_TAG_base_type"}], "language": "go", "param_name": "a", "population": "regenerated", "position": 0, "probe_n": 0, "role": "parameter", "store_file": "op_units2_go_c0000.json", "subprogram_linkage_name": null, "subprogram_name": "main.op_0", "symbol": "main.op_0", "unit": "go/regen_0"}
{"declared_spelling": "Double", "dwarf_byte_size": 8, "dwarf_encoding": null, "dwarf_encoding_absent_on_the_type": true, "dwarf_spelling": "const struct Double", "dwarf_terminal_tag": "DW_TAG_structure_type", "dwarf_type_chain": [{"byte_size": null, "encoding": null, "name": null, "tag": "DW_TAG_const_type"}, {"byte_size": 8, "encoding": null, "name": "Double", "tag": "DW_TAG_structure_type"}], "language": "swift", "param_name": "a", "population": "regenerated", "position": 0, "probe_n": 34, "role": "parameter", "store_file": "op_units2_swift_c0000.json", "subprogram_linkage_name": "$s11unit_anchor5op_34yS2dF", "subprogram_name": "op_34", "symbol": "op_34", "unit": "swift/regen_34"}
```

The third row is the swift finding stated by name: swift's stdlib
scalars (`Double` here) are `DW_TAG_structure_type` under a
`DW_TAG_const_type`, not `DW_TAG_base_type`, and carry a `byte_size`
with no `DW_AT_encoding` — `dwarf_encoding_absent_on_the_type: true`
on every swift row, 2,523 of them (see §6). Anchor flags used, one
compile per accepted probe, no ship build, no objdump:

| language | anchor compile |
|---|---|
| c | `/usr/bin/clang -std=c17 -O0 -g -c unit.c -o unit_anchor.o` |
| cpp | `/usr/bin/clang++ -std=c++20 -O0 -g -c unit.cpp -o unit_anchor.o` |
| go | `go build -gcflags=all=-N -l -o bin_anchor .` |
| rust | `rustc --crate-type=lib --emit=obj -C opt-level=0 -g -o unit_anchor.o unit.rs` |
| swift | `/persist/swift/usr/bin/swiftc -Onone -g -c unit.swift -o unit_anchor.o` |

## 4. Per-language compile counts (`t101b_l2_all.sh`, all 31,067 accepted probes)

| language | accepted | attempted | compiled at anchor | parameters typed | refused | params (rows) | rows carrying `DW_AT_encoding` |
|---|---|---|---|---|---|---|---|
| c | 10,620 | 10,620 | 10,620 | 10,620 | 0 | 20,814 | 20,814 |
| cpp | 17,840 | 17,840 | 17,840 | 17,840 | 0 | 35,296 | 35,296 |
| go | 590 | 590 | 590 | 590 | 0 | 1,108 | 1,108 |
| rust | 695 | 695 | 695 | 695 | 0 | 1,319 | 1,319 |
| swift | 1,322 | 1,322 | 1,322 | 1,322 | 0 | 2,523 | **0** |

Zero refusals in any language, at any of the four stages. Swift is
the one language whose anchor DWARF carries no `DW_AT_encoding` on
any of its base types — every one of its 2,523 parameter rows has
`dwarf_encoding_absent_on_the_type: true` — matching the brief's
named question and answered with the one literal DIE in §3.

## 5. The holder table (all 32 rows: parameter side)

Class × width, per language the spellings that resolve to it with
attesting probe counts (`probes_attesting`, i.e. distinct probes that
declared an operand of that spelling — `parameter_rows` counts rows,
which can exceed probes when a probe has the same spelling on more
than one parameter position).

| holder (`DW_AT_encoding|byte_size`) | class | bits | language: spellings (probes attesting) |
|---|---|---|---|
| `DW_ATE_boolean\|1` | truth | 8 | c: `bool`(1012), `_Bool`(824); cpp: `bool`(1458); go: `bool`(12); rust: `bool`(32) |
| `DW_ATE_signed_char\|1` | signed integer | 8 | c: `char`(824), `signed char`(824); cpp: `char`(1267), `signed char`(1267) |
| `DW_ATE_signed\|1` | signed integer | 8 | go: `int8`(61); rust: `i8`(66) |
| `DW_ATE_signed\|2` | signed integer | 16 | c: `short`(824), `signed short`(824); cpp: `short`(1267), `signed short`(1267); go: `int16`(61); rust: `i16`(66) |
| `DW_ATE_signed\|4` | signed integer | 32 | c: `int`(824), `signed int`(824), `int32_t`(188); cpp: `int`(1267), `signed int`(1267), `wchar_t`(1267), `int32_t`(247); go: `int32`(90); rust: `i32`(96) |
| `DW_ATE_signed\|8` | signed integer | 64 | c: `long`(824), `long long`(824), `signed long`(824), `signed long long`(824), `int64_t`(188); cpp: `long`(1271), `long long`(1271), `signed long`(1271), `signed long long`(1271), `int64_t`(247); go: `int64`(90), `int`(61); rust: `i64`(96), `isize`(66) |
| `DW_ATE_signed\|16` | signed integer | 128 | c: `__int128_t`(824); cpp: `__int128_t`(1275); rust: `i128`(66) |
| `DW_ATE_unsigned_char\|1` | unsigned integer | 8 | c: `unsigned char`(824); cpp: `unsigned char`(1277) |
| `DW_ATE_unsigned\|1` | unsigned integer | 8 | go: `uint8`(61); rust: `u8`(65) |
| `DW_ATE_unsigned\|2` | unsigned integer | 16 | c: `unsigned short`(824); cpp: `unsigned short`(1277); go: `uint16`(61); rust: `u16`(65) |
| `DW_ATE_unsigned\|4` | unsigned integer | 32 | c: `unsigned int`(824); cpp: `unsigned int`(1263); go: `uint32`(61); rust: `u32`(65) |
| `DW_ATE_unsigned\|8` | unsigned integer | 64 | c: `unsigned long`(824), `unsigned long long`(824), `uint64_t`(188); cpp: `unsigned long`(1255), `unsigned long long`(1255), `uint64_t`(245); go: `uint64`(90), `uint`(61), `uintptr`(61); rust: `u64`(94), `usize`(65) |
| `DW_ATE_unsigned\|16` | unsigned integer | 128 | c: `__uint128_t`(824); cpp: `__uint128_t`(1253); rust: `u128`(65) |
| `DW_ATE_float\|2` | float | 16 | c: `_Float16`(601), `__bf16`(601); cpp: `_Float16`(888), `__bf16`(888) |
| `DW_ATE_float\|4` | float | 32 | c: `float`(746); cpp: `float`(1072); go: `float32`(26); rust: `f32`(32) |
| `DW_ATE_float\|8` | float | 64 | c: `double`(746); cpp: `double`(1072); go: `float64`(26); rust: `f64`(32) |
| `DW_ATE_float\|16` | float | 128 | c: `__float128`(601), `long double`(601); cpp: `__float128`(888), `long double`(888) |
| `DW_ATE_UTF\|1` | unicode character (none of the four holder classes) | 8 | cpp: `char8_t`(1277) |
| `DW_ATE_UTF\|2` | unicode character (none of the four holder classes) | 16 | cpp: `char16_t`(1277) |
| `DW_ATE_UTF\|4` | unicode character (none of the four holder classes) | 32 | cpp: `char32_t`(1263) |
| `DW_AT_encoding_absent\|1` | DW_AT_encoding_absent | 8 | swift: `Int8`(177), `UInt8`(176), `Bool`(18) |
| `DW_AT_encoding_absent\|2` | DW_AT_encoding_absent | 16 | swift: `Int16`(177), `UInt16`(176), `Float16`(18) |
| `DW_AT_encoding_absent\|3` | DW_AT_encoding_absent | 24 | (no parameter attests this holder; it appears only as a rust result type — a 3-byte `RangeInclusive<i8/u8/bool>`, see §6) |
| `DW_AT_encoding_absent\|4` | DW_AT_encoding_absent | 32 | swift: `Int32`(230), `UInt32`(176), `Float`(36) |
| `DW_AT_encoding_absent\|6` | DW_AT_encoding_absent | 48 | (no parameter attests this holder; result-only, rust `RangeInclusive<i16/u16>`) |
| `DW_AT_encoding_absent\|8` | DW_AT_encoding_absent | 64 | swift: `Int64`(230), `UInt64`(228), `Int`(177), `UInt`(176), `Double`(36) |
| `DW_AT_encoding_absent\|12` | DW_AT_encoding_absent | 96 | (no parameter attests this holder; result-only, rust `RangeInclusive<i32/u32/f32>`) |
| `DW_AT_encoding_absent\|16` | DW_AT_encoding_absent | 128 | swift: `Int128`(57), `UInt128`(56), `Float80`(18) |
| `DW_AT_encoding_absent\|24` | DW_AT_encoding_absent | 192 | (no parameter attests this holder; result-only, rust `RangeInclusive<i64/u64/isize/usize>`) |
| `DW_AT_encoding_absent\|32` | DW_AT_encoding_absent | 256 | (no parameter attests this holder; result-only, rust `Range<i128/u128>`) |
| `DW_AT_encoding_absent\|48` | DW_AT_encoding_absent | 384 | (no parameter attests this holder; result-only, rust `RangeInclusive<i128/u128>`) |
| `DW_AT_encoding_absent\|no_size` | DW_AT_encoding_absent | none | (no parameter attests this holder; result-only, swift `Optional<T>`/`ClosedRange<T>` structure mangled names, see §6) |

Nine of the 32 holders carry zero parameter rows; every one of them
is attested as a RESULT type instead (rust `Range*<...>` iterator
structures and swift stdlib generics — none is invented: §7's pool
cross-check confirms all 32 appear in at least one pool entry).
`holders_by_class`: `DW_AT_encoding_absent` 12, `unsigned integer` 6,
`signed integer` 6, `float` 4, `unicode character` 3, `truth` 1.

## 6. Per-language coverage

### 6.1 Of the scalar-core spellings (`types101_spellings.json`, per language)

| lang | core spellings | attested | agree | disagree | undecidable | unattested |
|---|---|---|---|---|---|---|
| c | 56 | 25 | 22 | 3 | 0 | 31 |
| cpp | 56 | 28 | 22 | 6 | 0 | 28 |
| go | 14 | 14 | 14 | 0 | 0 | 0 |
| rust | 15 | 15 | 15 | 0 | 0 | 0 |
| swift | 17 | 17 | 0 | 0 | 17 | 0 |

Totals over the 158-row scalar core: 99 attested, 73 agree, 9
disagree, 17 undecidable, 59 unattested. Swift's 17 are all
UNDECIDABLE, not disagreeing — DWARF gives the width, never the class
(§3's third row), so there is nothing to compare its class against.

### 6.2 Of the 88 machine `type_key`s (`types101_entry_holders.json`, per language)

A language "serves" a `type_key` when at least one pool entry lists
that language among its members AND that entry has at least one
member whose DWARF rows were read (`members_with_rows > 0` — true for
every entry this run: 88/88 `type_keys` covered, 0 entries with
`members_compiled_without_rows > 0`).

| lang | type keys the language appears in | of those, served (has DWARF rows) |
|---|---|---|
| c | 57 | 57 |
| cpp | 61 | 61 |
| go | 26 | 26 |
| rust | 19 | 19 |
| swift | 23 | 23 |
| **all 88 keys** | — | **88 covered, 0 uncovered** |

### 6.3 Holders that exist in one language's core and no other's

Eight of the 32 holders (parameter side) have exactly one language
attesting them:

| holder | class | bits | the one language |
|---|---|---|---|
| `DW_ATE_UTF\|1` | unicode character | 8 | cpp (`char8_t`) |
| `DW_ATE_UTF\|2` | unicode character | 16 | cpp (`char16_t`) |
| `DW_ATE_UTF\|4` | unicode character | 32 | cpp (`char32_t`) |
| `DW_AT_encoding_absent\|1` | DW_AT_encoding_absent | 8 | swift |
| `DW_AT_encoding_absent\|2` | DW_AT_encoding_absent | 16 | swift |
| `DW_AT_encoding_absent\|4` | DW_AT_encoding_absent | 32 | swift |
| `DW_AT_encoding_absent\|8` | DW_AT_encoding_absent | 64 | swift |
| `DW_AT_encoding_absent\|16` | DW_AT_encoding_absent | 128 | swift |

Every `DW_AT_encoding_absent` parameter holder is swift-only because
swift is the only compiled language among the five whose stdlib
scalars are structures rather than base types (§3); cpp's three UTF
holders are single-language because c has no distinct UTF character
type in its scalar core.

### 6.4 Holders the pool has no entry for

None. Cross-checking the 32 holders in `types101_holders.json`
against every `distinct_parameter_holder_tuples` / `distinct_result_holders`
entry in `types101_entry_holders.json`'s 1,831 pool entries: all 32
are referenced by at least one entry. (One extra id shows up in the
pool's own tuples, `DW_TAG_pointer_type|no_size` — a pointer role,
excluded from the holder table by design since a pointer is not a
scalar class × width; it is not a 33rd holder.)

## 7. The DWARF-vs-inventory disagreements (9, all LITERAL)

| language | spelling | DWARF class (bits) | inventory `normalised_class` | verdict |
|---|---|---|---|---|
| c | `_Bool` | truth (8) | integer_unsigned | DWARF says truth (truth_value), the inventory says integer_unsigned |
| c | `bool` | truth (8) | integer_unsigned | DWARF says truth (truth_value), the inventory says integer_unsigned |
| c | `char` | signed integer (8) | integer_unsigned | DWARF says signed integer (integer_signed), the inventory says integer_unsigned |
| cpp | `bool` | truth (8) | integer_unsigned | DWARF says truth (truth_value), the inventory says integer_unsigned |
| cpp | `char` | signed integer (8) | integer_unsigned | DWARF says signed integer (integer_signed), the inventory says integer_unsigned |
| cpp | `char16_t` | unicode character (16) | integer_unsigned | DWARF's class is unicode character, none of the inventory's four |
| cpp | `char32_t` | unicode character (32) | integer_unsigned | DWARF's class is unicode character, none of the inventory's four |
| cpp | `char8_t` | unicode character (8) | integer_unsigned | DWARF's class is unicode character, none of the inventory's four |
| cpp | `wchar_t` | signed integer (32) | integer_unsigned | DWARF says signed integer (integer_signed), the inventory says integer_unsigned |

None resolved — brief §3's stop rule: DWARF and the inventory
disagreeing is listed, never adjudicated by this task.

## 8. Verifier tally

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_217_task_t101b_dominant_types_join.md
```

Three passes (lanes `t101b_l7_verify.sh` / `l8_verify2.sh` /
`l9_verify3.sh`), each fixing what the previous pass found (an
absolute host path that doesn't resolve inside the sandbox, and a
`> 0` substring the checker's redirect scanner misread as a shell
write) — never the verifier itself. Final tally, log_217 §7 in full:

**claims 20 | MATCHES 6 | DIFFERS 0 | UNVERIFIABLE 7 | REFUSED 2 |
NOT_RERUNNABLE 5. Zero DIFFERS.**

## 9. Guard

`check_no_spelling_keys.py` run over all 337 json files this task
wrote or re-wrote — the three artifacts, `types101_dwarf_rows.json` +
294 shards, `types101_dwarf_rows_sample.json` + 38 shards (lane
`t101b_l6_guard.sh`): **337 PASS, 0 FAIL**. `grep -c exempt` over
every `types101_*` file (code and json): 0.

## 10. The two lists

### Decided, recorded for audit

- The join ran to completion over all 92,127 DWARF rows re-read from
  the compiler (31,067 accepted probes, 0 refused, 0 members compiled
  without rows): 32 holders, 88/88 type keys covered, 9 class
  disagreements listed and not resolved, 73/99 attested spellings
  agree with the inventory, swift's 17 attested spellings are
  UNDECIDABLE (no `DW_AT_encoding` on any swift stdlib scalar).
- Two bugs were found and fixed at cause in `types101_join.py`, one
  line each (§2); no other file changed; `fold.py`,
  `type_inventory2_core2.json`, and `the_pool5.json` were not touched.
- The spelling-ban guard passes on every json this task produced
  (337/337); `grep -c exempt` is 0 everywhere.

### Awaiting the owner

- (none) — task t101/t101b's open question from log_213 (whether to
  authorize the compiler re-read) is closed by this run; nothing here
  needs a ruling.
