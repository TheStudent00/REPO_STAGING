# log 174 — task 71: the compiler graph, four compilers

Date: 2026-09-03. Node: `hq.research.compiler_graph.graph`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/CORE_0_3_5_9_graph.md`).

# 1. What now exists

## 1.1 The class the tree names

`Research/compiler_graph/graph.py` holds `class Graph` with the CORE's
own names: attributes `static_structure`, `dynamic_structure`,
`frontier`; methods `build`, `diary`, `query_path`, `coverage`,
`super_ops`.

- Four compilers are built by that one class, from PINS.
- `build_graph.py`, `build_graph2.py`, `build_graph3.py` each carry
  one added header line marking them superseded records. Nothing else
  in them was edited.

## 1.2 What is implemented and what is stubbed, said once, here

| method | state |
|---|---|
| `build` | implemented, run over four compilers |
| `query_path` | implemented, run once per compiler |
| `diary` | the READER is implemented and run over task 72's 590 go diaries; the PRODUCER (inject, rebuild, replay) is task 72's and is not in this file |
| `coverage` | implemented, joined to those 590 diaries |
| `super_ops` | NOT implemented. It raises `NotYetBuilt` by name rather than returning an empty result that could be read as a measurement. Task 75. |

Nothing else is stubbed.

## 1.3 Language-agnostic by construction, realized as data

The CORE's rule is realized the way the PCv5 ledgerer realizes it
(`PseudoCoup_v5/Tools/ledgerer/ts_to_ur.py`, `class LanguagePack`):
per-language DATA, one universal mapper. A pack is a table of
tree-sitter node type names; the mapper below it never names a
language. Adding a fifth grammar is a pack, not code.

LITERAL — the go pack, from `graph.py`:

```
PACK_GO = LanguagePack(
    language="go",
    extensions=(".go",),
    module="tree_sitter_go",
    def_types=("function_declaration", "method_declaration", "func_literal"),
    name_fields=("name",),
    param_types=("parameter_declaration", "variadic_parameter_declaration"),
    local_types=("var_spec", "const_spec", "short_var_declaration"),
    call_types=("call_expression",),
    ref_types=("identifier", "type_identifier", "field_identifier"),
    member_types=("selector_expression",),
    member_field="field",
    assign_types=("assignment_statement", "short_var_declaration"),
)
```

GLOSS: every field names node types in go's own grammar. `def_types`
says which node declares a callable unit; `param_types` says which
node declares one parameter. The mapper reads these fields and nothing
else.

"Defined in" versus "does" is unchanged: dispatch is by file
extension, to the grammar of the language the file is WRITTEN in. The
X86 backend is about registers and is written in C++, so it is read by
the C++ grammar and sits in the cpp region.

# 2. The four graphs, with their regions and their pins

## 2.1 The region rule per compiler, under the minimality rule

The CORE's rule is "model what is easy; build only enough to prove
which low-level operands are which high-level variables". Each region
is the lowering path — where a named argument becomes a machine
location — and nothing wider.

| compiler | region | pin, quoted from the repository |
|---|---|---|
| go | `src/cmd/compile/internal/{ssagen,abi,amd64,ssa}` | `9f1012d9a1aa0831ff44ac9c767e96f9943d13fe` |
| cpp | `clang/lib/CodeGen` + `llvm/lib/Target/X86` | `llvmorg-21.1.8` → `2078da43e25a4623cab2d0d60decddf709aaea28` |
| rust | `compiler/rustc_codegen_ssa`, `rustc_codegen_llvm`, `rustc_middle/src/mir` | `7c329d6c76e11ca40c5673818ab0439c1be8962c` |
| swift | `lib/SILGen`, `lib/IRGen` | `6a862d2eb7128ff1f317b07e8ad1a6da939775f3` |

Every file is read with `git show <pin>:<path>`. No working tree is
read: all four sit at a different commit than their pin (llvm's tree
is at `llvmorg-24-init-680-g6a33b69d8bae`).

### 2.1.1 CLANG SERVES BOTH c AND cpp — said, not assumed

There is no `graph_c.json` and there should not be one. c and cpp go
through one driver, one CodeGen library and one x86 backend; they
differ in the front end, which this region does not contain. Shipping
a duplicate graph under a second name would be a second copy of one
measurement.

### 2.1.2 THE RUST PIN IS A FRONTIER, recorded rather than papered over

The corpus was compiled by `rustc 1.96.1 (31fca3adb 2026-06-26)`, a
rustup toolchain. The rust source checkout on this machine does not
contain commit `31fca3adb`:

```
$ git cat-file -t 31fca3adb
fatal: Not a valid object name 31fca3adb
```

Its own head is `7c329d6c`, dated 2026-08-03. So `graph_rust.json` is
built from a NEARBY rustc source, not from the source that compiled
the corpus. Every claim read off it is bounded by that gap. Task 72
found the same fact from the other side (log_175: the source commit is
absent from the checkout).

## 2.2 The counts, each with its population

| compiler | files | nodes | edges | frontier | parse errors |
|---|---|---|---|---|---|
| go | 81 | 10,393 | 63,797 | 77,530 | 0 |
| cpp | 269 (incl. 61 data tables) | 112,364 | 386,065 | 523,694 | 2,082 |
| rust | 134 | 13,446 | 60,382 | 101,095 | 49 |
| swift | 230 | 71,106 | 192,655 | 278,245 | 311 |

Population: "files" is files of that region actually read; "nodes" is
file + def + param + local + data_row nodes; "frontier" is the record
count, not a failure count.

Parse errors are NOT zero for three compilers, and each one is named
with its file and line in the `parse_errors` list of the graph file
(2,082 + 49 + 311 = 2,442 records). They are C++ and rust constructs
the pinned grammars do not admit; the ruled response to a grammar
falling behind is a pin bump, which is not this task's work.

## 2.3 Node and edge vocabulary, unchanged from the go lap

Nodes: `file`, `def`, `param`, `local`, `data_row`.
Edges: `contains`, `calls`, `reads`, `writes`.

LITERAL — one def node, from `graph_go.json`:

```json
{"id": "src/cmd/compile/internal/abi/abiutils.go#353#def#0",
 "kind": "def", "language": "go",
 "file": "src/cmd/compile/internal/abi/abiutils.go",
 "label": "ABIAnalyzeFuncType", "start_line": 353, "end_line": 388}
```

LITERAL — one call edge, from `graph_go.json`:

```json
{"src": "src/cmd/compile/internal/abi/abiutils.go#657#def#0",
 "dst": "src/cmd/compile/internal/abi/abiutils.go#197#def#0",
 "rel": "calls", "at_line": 669, "matched_on": "callee_text",
 "evidence": "call_node_in_own_parse_resolved_by_unique_name"}
```

LITERAL — one data-table node, from `graph_cpp.json`:

```json
{"id": "llvm/lib/Target/X86/X86CallingConv.td#442#data_row#0",
 "kind": "data_row", "language": "tablegen_data",
 "file": "llvm/lib/Target/X86/X86CallingConv.td",
 "label": "X86_32_RegCall", "table": "X86_RegCall_base",
 "start_line": 442, "pattern_count": 0}
```

GLOSS on the call edge: `matched_on` records HOW the name resolved
(the whole callee text, or its trailing segment) — it is the name of a
resolution method, not the callee's text. The callee's text itself is
not stored; §6.1 says why.

GLOSS: a `.td` file is a data table, not code, so it gets no grammar
and each row is a node. `X86_32_RegCall` is one calling-convention
table entry; `table` names the multiclass it instantiates.

## 2.4 An unresolved reference is a frontier record with its candidates

LITERAL — one frontier record, from `graph_go.json`:

```json
{"kind": "ambiguous_call",
 "file": "src/cmd/compile/internal/abi/abiutils.go",
 "detail": "clear", "at_line": 660,
 "from_node": "src/cmd/compile/internal/abi/abiutils.go#657#def#0",
 "candidate_count": 7,
 "candidates": ["src/cmd/compile/internal/ssa/biasedsparsemap.go#103#def#0",
                "src/cmd/compile/internal/ssa/debug.go#1184#def#0",
                "src/cmd/compile/internal/ssa/sparsemap.go#73#def#0", ...]}
```

GLOSS: a call at line 660 names `clear`. Seven defs in this region are
called `clear`, so no single edge is evidenced; the candidate set is
carried instead of a guess.

### 2.4.1 This rule was written because the defect was MEASURED

The first version resolved a call by picking the first def carrying
the name. A cpp path query then walked through a call to `size()` that
had landed on an unrelated def of the same name — a connection that
does not exist. Refusing ambiguity changed the counts: cpp `calls`
fell from 61,692 to 35,773, with 26,124 ambiguities recorded. Fewer
edges, none of them manufactured.

Frontier by kind, per compiler:

| kind | go | cpp | rust | swift |
|---|---|---|---|---|
| unresolved_reference | 69,060 | 400,771 | 86,954 | 217,894 |
| unresolved_call | 6,374 | 94,656 | 9,290 | 36,196 |
| ambiguous_call | 2,094 | 26,124 | 4,802 | 23,844 |
| parse_error | 0 | 2,082 | 49 | 311 |
| no_reader_dispatched | 2 | 0 | 0 | 0 |
| data_table_backend_not_built | 0 | 61 | 0 | 0 |

# 3. The go rebuild, diffed against lap one

`build_graph.py` was re-run to `graph_go_lapone.json` so the two could
be compared. Its output is 126,304,023 bytes against the August file's
126,304,049 — lap one reproduces.

## 3.1 What is comparable, and what is not

NODE AND EDGE TOTALS ARE NOT COMPARED. Lap one mints a node per
identifier occurrence (105,367 `ref` nodes of its 182,935); `graph.py`
mints a node per file, def, param and local. Those are two resolutions
of one region, not two measurements of one quantity. Comparing them
would produce a number that means nothing.

What IS comparable is the region's file set and its named function
definitions.

## 3.2 The result

| measure | lap one | graph.py |
|---|---|---|
| files carrying nodes | 114 | 81 |
| named function definitions | 1,514 | 1,500 |
| definitions in BOTH | 1,500 | 1,500 |
| only in lap one | 14 | — |
| only in graph.py | — | 0 |

The 14 that lap one has and graph.py does not are all in generated
files — 10 in `ssa/opGen.go` (`Asm`, `AuxIntType`, `HasSideEffects`,
`IsCall`, `IsTailCall`, `ResultInArg0`, `Scale`, `String`,
`SymEffect`, `UnsafePoint`), 1 in `amd64/simdssa.go`
(`ssaGenSIMDValue`), and 3 in `ssagen/simd{AMD64,ARM64,Wasm}intrinsics.go`. The stated region rule excludes generated
files; lap one recorded their declarations under a `generated_code`
frontier note. That is a REGION RULE difference, stated, not a
resolution failure.

The 33-file gap is the same story plus two rules the new file states
rather than inherits:

- `ssa/_gen/*` — 28 `.rules` files and a vendored library. That is the
  rewrite-rule GENERATOR: tooling that runs before the compiler is
  built, never source a probe's compilation walks. Lap one excluded it
  by not recursing into subdirectories; `graph.py` excludes it by a
  named rule.
- `ssa/testdata/*.go` — go programs that are test INPUT to the
  compiler, not compiler logic.

# 4. The path query: one answered, three named frontiers

## 4.1 The question, in words

Where does a function parameter — a name the programmer wrote — become
a physical machine location? For go the August lap answered it; this
lap asks the same question of all four compilers through
`Graph.query_path`.

## 4.2 The walk shape, and why it is constrained

`query_path` takes the steps it is allowed as (relation, direction)
pairs. THIS IS NOT A CONVENIENCE FILTER. Two looser shapes were run on
this region first and both produced connections that are not
connections:

- allowed to take `contains` in reverse from a def, the walk reaches
  the def's FILE and from there every other def in that file — so any
  two defs in one file sit three hops apart. The go query "answered"
  through that shortcut: `ft` → `ABIAnalyzeFuncType` → the file →
  `allocateRegs`. It proves nothing.
- allowed to take `calls` in reverse, the walk joins two defs merely
  because both call one shared helper. The cpp query "answered" by
  going through `getDecl` and `getFunction`.

The identity shape is lap one's own: leave the parameter for the def
that contains it (`contains`, reversed), then follow `calls` FORWARD.
File nodes are kept out of the walk. Every step in a printed path
records its direction.

## 4.3 go — the August answer, reproduced

LITERAL — from `report_task71.json`:

```
START src/cmd/compile/internal/abi/abiutils.go#353#param#0
 contains (reversed) -> abiutils.go:353 ABIAnalyzeFuncType [def]
 calls (forward)     -> abiutils.go:603 assignParam [def]
 calls (forward)     -> abiutils.go:623 tryAllocRegs [def]
 calls (forward)     -> abiutils.go:514 allocateRegs [def]
```

4 hops, 8 nodes visited.

LITERAL — the August answer, from `acceptance_query.txt`:

```
  [0] .../abiutils.go:362 local_var  param
  [3] .../abiutils.go:367 call       s.assignParam
  [4] .../abiutils.go:603 method     assignParam
  [5] .../abiutils.go:604 call       state.tryAllocRegs
  [6] .../abiutils.go:623 method     tryAllocRegs
  [7] .../abiutils.go:634 call       state.allocateRegs
```

DIFF: the same three functions, in the same order, at the same lines —
`assignParam` at 603, `tryAllocRegs` at 623. Lap one printed 8 hops
because it walks through its `ref` and `call` nodes; `graph.py` prints
4 because its nodes are defs and the call is an edge attribute. Same
path, two resolutions. Lap one's last hop names the CALL SITE of
`allocateRegs` (line 634); `graph.py`'s names its DEFINITION (line
514).

VALUES IN MOTION, so the path is not just a list of names: the go
compiler is compiling a probe. `ABIAnalyzeFuncType` receives `ft`, the
function's type — for a probe with two 64-bit integer parameters, a
type carrying two parameter slots. It hands each slot to
`assignParam`, which asks `tryAllocRegs` whether registers are still
available for a value of that size. `tryAllocRegs` calls
`allocateRegs`, which takes the next entries out of the available
integer-register list — for the first parameter, go's `AX`. The
programmer's first parameter and the machine's `AX` are joined by
those four hops, and the join is a walk over data, not a reading of
source by a person.

## 4.4 cpp — a named frontier: `State.AllocateReg`

The walk starts at a parameter of `CodeGenFunction::EmitFunctionProlog`
(`clang/lib/CodeGen/CGCall.cpp:3060`), visits 219 nodes, and stops.

LITERAL — the frontier record that stops it:

```json
{"kind": "unresolved_call", "callee_text": "State.AllocateReg",
 "file": "llvm/lib/Target/X86/X86CallingConv.cpp", "at_line": 282,
 "from_node": "llvm/lib/Target/X86/X86CallingConv.cpp#237#def#0"}
```

8 such records name a goal. GLOSS: the register assignment is reached
through a callback state object (`CCState`), whose class is defined
outside this region, so the call names a method the region never
declares. This is a REAL structural fact about clang, not a reader
weakness: LLVM's calling-convention code is invoked through generated
callbacks and a state object, and following it needs either the
generated `X86GenCallingConv.inc` (produced by TableGen at build time,
not in the source tree — already a recorded frontier) or the region
widened to `llvm/lib/CodeGen/CallingConvLower.cpp`.

## 4.5 rust — a named frontier: `arg_abi.store` / `llvm::get_param`

The walk starts at a parameter of `arg_local_refs`
(`compiler/rustc_codegen_ssa/src/mir/mod.rs:455`), visits 142 nodes,
and stops.

LITERAL:

```json
{"kind": "ambiguous_call", "callee_text": "arg_abi.store",
 "file": "compiler/rustc_codegen_llvm/src/abi.rs", "at_line": 333,
 "from_node": "compiler/rustc_codegen_llvm/src/abi.rs#327#def#0",
 "candidate_count": 4}
{"kind": "ambiguous_call", "callee_text": "llvm::get_param",
 "file": "compiler/rustc_codegen_llvm/src/abi.rs", "at_line": 296,
 "candidate_count": 2}
```

111 records name a goal. GLOSS: `store` is a trait method with four
implementations in this region, and the reader cannot say which one a
given call reaches without type information it does not have. Refusing
is correct. Note also what rust's stop means beyond the reader: rustc
hands the argument to LLVM and LLVM chooses the register, so the
physical register is not in rustc's source at all.

## 4.6 swift — a named frontier: `F.begin()->createFunctionArgument`

The walk starts at a parameter of `SILGenFunction::emitProlog`
(`lib/SILGen/SILGenProlog.cpp:1398`), visits 113 nodes, and stops.

LITERAL:

```json
{"kind": "unresolved_call",
 "callee_text": "F.begin()->createFunctionArgument",
 "file": "lib/SILGen/SILGenBridging.cpp", "at_line": 2125,
 "from_node": "lib/SILGen/SILGenBridging.cpp#2058#def#0"}
```

56 records name a goal. GLOSS: the callee is reached through a call on
the result of another call (`F.begin()`), whose type is a SIL basic
block declared in `include/swift/SIL/`, outside the region. As with
rust, the physical register is chosen inside LLVM, so swift's walk was
always going to stop at the region boundary; the value of the record
is that it says exactly WHERE.

## 4.7 The honest summary of §4

One of four questions is answered by a path. Three are answered by a
named unresolved reference with its file and line. Frontier honesty is
the deliverable where the answer is not, and none of the three was
turned into a path by loosening the walk.

# 5. Coverage: the go diaries joined through `graph.py`

## 5.1 The join key

Task 72's 590 go diaries are on disk. Their ids are byte spans;
`graph.py`'s are `file#line#kind#ordinal`. Neither can be rewritten
into the other, so the join is on the one coordinate both carry: the
DECLARATION SITE.

LITERAL — one diary line, from `diaries/go/op_0.txt`:

```
1	-	src/.../abiutils.go:12127-13356:method|ABIAnalyzeFuncType|src/.../abiutils.go:353
```

GLOSS: three tab fields — a sequence number, a marker column, and the
unit record. The unit record's three pipe-fields are the byte span,
the unit's name, and the declaration site `abiutils.go:353`. That last
field is the join key, and it is the same 353 the def node above
carries as `start_line`. The join is exact, not approximate.

## 5.2 The result, with its population

| compiler | defs in region | probes | visited by ≥1 probe | visited by none |
|---|---|---|---|---|
| go | 1,859 | 590 | 724 | 1,135 |
| cpp | 10,789 | 0 | 0 | 10,789 |
| rust | 3,313 | 0 | 0 | 3,313 |
| swift | 10,088 | 0 | 0 | 10,088 |

- 7 diary keys fall outside the region, all in `ssa/opGen.go` — the
  generated file the region rule excludes. That is the region rule
  showing its own edge, not a coverage failure.
- cpp, rust and swift: 0 probes. Their whole def population is
  never-visited BY ABSENCE OF MEASUREMENT. That is not the same fact
  as a def no probe reaches, and it is never stated as the latter.
- go's 724 of 1,859 is a DIFFERENT population from task 72's own 731
  of 1,549: that denominator is instrumented function bodies, this one
  is defs of `graph.py`'s region. Neither replaces the other.

## 5.3 The never-visited list is the finding

Top files by defs no probe visits (count / total defs in that file):

| file | never visited | defs in file |
|---|---|---|
| `ssagen/intrinsics.go` | 216 | 225 |
| `ssa/rewrite.go` | 196 | 242 |
| `ssagen/ssa.go` | 105 | 220 |
| `amd64/ssa.go` | 57 | 69 |
| `ssa/magic.go` | 40 | 40 |
| `ssa/merge_conditional_branches.go` | 33 | 33 |
| `ssa/func.go` | 30 | 77 |
| `ssa/html.go` | 30 | 32 |

GLOSS: `ssa/magic.go` is 40 of 40 — the magic-number division helpers
are compiler logic our scalar probes never exercise at all.
`ssagen/intrinsics.go` at 216 of 225 is the intrinsic table; the probes
call no intrinsics. This agrees with task 72's own list, measured on a
different population.

Defs every probe visits (590 of 590): `StringToAux`
(`ssa/rewrite.go:815`), `init` (`ssa/addressingmodes.go:107`), `init`
(`ssa/compile.go:615`), `ssaMarker` (`ssagen/ssa.go:1153`), `Init`
(`amd64/galign.go:14`), `NewSymABIs` (`ssagen/abi.go:33`).

# 6. The guard

`Research/op_pipeline/check_no_spelling_keys.py`, UNMODIFIED, one
process, over all four graph files.

LITERAL — `Research/compiler_graph/guard_task71.txt`, complete:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS graph_go.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_rust.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_swift.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ echo EXIT=$?
EXIT=0
$ grep -c exempt guard_task71.txt
0
```

No exemption was taken; no `role` key exists in any of the four files.

## 6.1 The guard's first run FAILED, and the cause is worth keeping

The first run refused three of four graphs — 126 places in cpp, 3,159
in rust, 749 in swift. The cause: node ids were spelled
`file:line:name`, and COMPILERS CONTAIN FUNCTIONS WHOSE OWN NAMES ARE
OPERATOR TOKENS — `new` in rustc, `consume` in swift and in llvm, `as`
in swift. An id built from a name therefore put an operator token into
every edge's `src` and `dst`, which is a row structure, which is
exactly what the ban forbids.

The fix is general, not a patch on three names:

- A node id is now a MACHINE COORDINATE and carries no name:
  `file#line#kind#ordinal`.
- The name lives only in the node record's `label` field. That record
  carries `language` and `id`, so it is a unit object, and a display
  label on a unit object is the one appearance the ban permits.
- A call edge carries no `callee_text` either. Its file and line
  locate the call in the compiler's own source, which is where the
  text belongs.

Side effect, stated: minting a fresh id per declaration raised node
counts (swift 58,862 → 71,106, cpp 99,362 → 112,364), because two
declarations sharing a line no longer collapse into one node. That is
more faithful, not inflated.

# 7. Pins and environment

- Python: `/tmp/reconnect_venv/bin/python3` (3.13.9). Tree-sitter was
  NOT installed in that venv and was installed for this task, pinned
  to the versions already present system-wide so nothing moved
  underneath earlier laps:

```
tree-sitter 0.25.2
tree-sitter-go 0.25.0
tree-sitter-cpp 0.23.4
tree-sitter-c 0.24.2
tree-sitter-rust 0.24.2
tree-sitter-swift 0.7.3
```

- PIN CORRECTION, recorded: `build_graph3.py`'s header asserts
  `tree-sitter == 0.26.0`. The runtime is 0.25.2. The graphs record the
  version they were actually built with, read from package metadata at
  run time rather than typed in.
- No Airlock instance was used. Everything ran on the host, reading
  pinned git objects. `t71` was never brought up and so needs no
  bringing down.

# 8. File inventory

New:

- `Research/compiler_graph/graph.py` — the class.
- `Research/compiler_graph/report_graph.py` — the diff, the queries,
  the coverage run.
- `Research/compiler_graph/graph_go.json`, `graph_cpp.json`,
  `graph_rust.json`, `graph_swift.json` — the four graphs.
- `Research/compiler_graph/graph_go_lapone.json` — lap one re-run, for
  the diff.
- `Research/compiler_graph/report_task71.json`,
  `query_task71.json`, `coverage_go_summary.json`,
  `guard_task71.txt` — the measurements and the guard transcript.
- `Research/compiler_graph/build_{go,cpp,rust,swift}.log`,
  `build_lapone.log` — run transcripts.
- `DevComms/log_174_task71_compiler_graph_four.md` — this file.

Edited:

- `Research/compiler_graph/build_graph.py`, `build_graph2.py`,
  `build_graph3.py` — one header line each, marking them superseded
  records. Nothing else.
- `Planning/.../node_0_3_5_9_graph/CORE_0_3_5_9_graph.md` — the
  realization table replaced with what is on disk after this task.
- `Planning/.../node_0_3_5_9_graph/PROGRESS.md` — six entries, each
  with its evidence link.

Not touched: `Research/op_pipeline/check_no_spelling_keys.py`;
`Research/compiler_graph/coverage.py` (task 72's).

# 9. Resume state, per compiler

| compiler | graph | diaries | coverage | query | next |
|---|---|---|---|---|---|
| go | built, diffed clean | 590 | 724 of 1,859 | ANSWERED | task 75: `super_ops` over the 590 diaries |
| cpp | built | none | 0 probes | frontier: `State.AllocateReg` | widen to `llvm/lib/CodeGen/CallingConvLower.cpp`, or build TableGen's generated callbacks; instrumented build priced in log_175 |
| rust | built (pin frontier) | none | 0 probes | frontier: `arg_abi.store`, 4 candidates | trait-method resolution needs type information the reader lacks; and the corpus's rustc source commit must be fetched before a diary can join |
| swift | built | none | 0 probes | frontier: `F.begin()->createFunctionArgument` | region boundary at `include/swift/SIL/`; log_175 records that a swift build cannot start on this machine |

# 10. Two lists

DECIDED, RECORDED FOR AUDIT:

- Node ids are machine coordinates, not names. Forced by the guard.
- Ambiguous calls produce a candidate set, not an edge. Forced by a
  measured false path.
- `query_path` takes a constrained step set. Forced by two measured
  false paths.
- `ssa/_gen` and `ssa/testdata` are out of the go region, by stated
  rule.
- No `graph_c.json`: clang serves both c and cpp.
- `coverage.py` (task 72's) was not modified or folded in; `graph.py`
  carries its own reader for the same format.

AWAITING DEE: nothing.
