# Probe: single-instruction vs super-op, in LLVM's own source graph

Bounded, single-measurement probe. 2026-08-31. Answers the owner's/the
hypothesis paragraph in isolation; does not extend the Go compiler
graph, does not touch AgentMemory/Planning/DevComms/op_pipeline
artifacts. Artifacts of this probe live under
`Research/compiler_graph/probe_uint64_to_float/`:
`build_graph_cpp_probe.py`, `query_hypothesis.py`, `graph_cpp_probe.json`,
`query_output.txt`.

## 1. what was available vs not

- **LLVM/clang source tree: PRESENT**, at
  `<WORKSPACE_DIR>/Sources/llvm-project` (a real git checkout, 3.9G,
  full tag history back to `llvmorg-8.0.0-rc2`). No download was
  needed or performed. Evidence class: **tool's own testimony**
  (`git log`, `git tag`, `du`).
- **Pin mismatch, found and corrected, named here so it is not
  silently repeated.** The repo's checked-out HEAD is
  `6a33b69d8bae737e5e1d60c7b7776a0b1f885bfa` (`llvmorg-24-init-680`,
  dated 2026-07-17 by its own commit) -- a much later dev snapshot
  than what actually built the ship code this probe is about. The
  op_pipeline's own record,
  `Research/op_pipeline/lane_out_ordering/compiler.txt`, states the
  compiler that produced op_117/op_501 is **`Ubuntu clang version
  21.1.8 (6ubuntu1)`** (evidence class: tool's own testimony -- the
  compiler's own version banner, captured by a prior lane run).
  The exact matching tag, `llvmorg-21.1.8`, exists in the same repo
  at commit `42befb84c672d78de430feb4c96710e6aa4fc774` (tagged
  source dated 2025-12-12 per `git log -1` on the tag). This probe
  extracted files with `git show llvmorg-21.1.8:<path>` rather than
  reading the working tree, so the region actually analyzed matches
  the pinned compiler, not the repo's current checkout. **Anyone
  reading files off this tree directly (not through a tag pin) is
  reading five months of drift past the pinned compiler** -- this is
  the dead end named: no LLVM source is pinned to the ship compiler
  by the checkout's default state; the tag has to be selected by
  hand (or by a pin-recording tool that does not yet exist here).
- **`tree-sitter-cpp`: not previously used on this line, installed
  fresh** (`pip install tree-sitter==0.26.0 tree-sitter-cpp` ->
  0.23.4; matches the sandbox this probe ran in, not necessarily any
  other machine). **`tree-sitter-tablegen`: absent from PyPI**,
  confirmed by a failed `pip install` (`ERROR: Could not find a
  version that satisfies the requirement`). This matches
  `log_072_compiler_graph_tracing.md` sec 4a, which already flagged
  the TableGen grammar as unverified. **Named dead end**: no general
  `.td` parser exists in this environment. What would pass it: build
  tree-sitter-tablegen from the upstream grammar repo (not attempted
  -- out of scope for a bounded probe) or write a fuller TableGen
  data-table reader than the one used here (see sec 3).

## 2. pins, exactly as lap-one recorded them

```
tree-sitter        == 0.26.0   (same pin as the Go graph, lap one)
tree-sitter-cpp     == 0.23.4  (new on this line; no prior pin existed)
tree-sitter-tablegen: NOT AVAILABLE (PyPI has no distribution)
LLVM/clang tree tag == llvmorg-21.1.8
LLVM/clang commit   == 42befb84c672d78de430feb4c96710e6aa4fc774
llvm-project repo HEAD (do NOT read this for pinned-compiler work)
                    == 6a33b69d8bae737e5e1d60c7b7776a0b1f885bfa
pinned compiler (op_pipeline's own testimony)
                    == Ubuntu clang version 21.1.8 (6ubuntu1)
```

## 3. scope decision on "build the graph" (recorded, not hidden)

`build_graph.py` (lap one) is hardcoded to Go: `tree_sitter_go`,
region rules keyed to `cmd/compile`'s package layout. It has no
language dispatcher. CORE_0_3_5's own open-items list already names
this gap ("**Second language** -- apply unchanged machinery to a
second compiler ... to prove language-agnosticism by construction
rather than intent" -- still open as of the CORE file read for this
probe). Building that properly over "SelectionDAG legalization + the
target's ISel patterns" as asked -- i.e. the whole region, hundreds
of files -- is a campaign, not a bounded probe.

What this probe did instead, consistent with the node's own
minimality rule ("Model what is easy; beyond that, build ONLY enough
... Completeness of the compiler model is not the objective;
sufficiency of the identity proof is"): a purpose-built graph over
exactly the 5 C++ functions + 1 TableGen defm that source-grepping
located as relevant, dispatched by file extension per the node's own
rule (`.cpp` -> tree-sitter-cpp; `.td` -> a regex data-table reader,
matching CORE_0_3_5 sec 4's own prescription that `.td` "is not
code" and its node is "the table (parsed as data)"). Nodes carry an
`emit_count` = number of SDNode-constructing calls
(`DAG.getNode`/`getSetCC`/`getSelect`/`getConstant`/...) found by
walking each function's own AST -- an operational, mechanical
stand-in for "how many low-level operations does this compiler
region produce", the same register the hypothesis is stated in.

**Honest limitation of this graph, stated plainly**: the five C++
functions and the one TableGen defm were **located by grep**, not by
a graph walk from a fixed entry point (there is no automated
"language mapping" showing that `a + b` for `(u64, f32)` operands
reaches `X86TargetLowering::LowerUINT_TO_FP` in the first place --
that upstream leg, C-source through Clang's CodeGen down to the
first `UINT_TO_FP` SelectionDAG node, was not built or queried here).
The graph proves the CALL/DECLINE/PATTERN-MATCH structure downstream
of that first node; it does not yet prove how that node itself is
reached from `a + b`. That is a real frontier -- see sec 6.

## 4. the graph, and its literal query output

`graph_cpp_probe.json`: 7 nodes, 7 edges, `check_no_spelling_keys.py`
run against it and PASSED ("no operator token in any key, grouping,
pairing or row structure" -- the check is nominally about the
operator-equivalence pipeline's inventory, not this node's own
material, but the instruction was to run it on any JSON artifact
produced, and it is a clean, honest pass: this graph groups nothing
by operator spelling; its nodes are compiler-source declarations,
its labels are C++/TableGen identifiers, not the 12-language
operator tokens the check hunts for).

Full literal output of `query_hypothesis.py` (the query's own
printed nodes/edges, not a paraphrase):

```
=== PINS ===
{
  "tree_sitter": "0.26.0",
  "tree_sitter_cpp": "0.23.4",
  "llvm_tag": "llvmorg-21.1.8",
  "llvm_commit": "42befb84c672d78de430feb4c96710e6aa4fc774",
  "llvm_repo_head_commit_MISMATCH": "6a33b69d8bae737e5e1d60c7b7776a0b1f885bfa",
  "pinned_compiler_per_op_pipeline": "Ubuntu clang version 21.1.8 (6ubuntu1)"
}

=== PATH QUERY: unsigned i64 -> f32 (op_117's case) ===
X86TargetLowering::LowerOperation
  --[calls, forced-by-construction: switch case ISD::UINT_TO_FP]-->
X86TargetLowering::LowerUINT_TO_FP
  --[declines_custom_lowering, guard: is64Bit && SrcVT==i64 &&
     (DstVT==f32||DstVT==f64) -> return SDValue()]-->
SelectionDAGLegalize::LegalizeOp
  --[calls: case TargetLowering::Custom, TLI.LowerOperation
     returned null -> [[fallthrough]] to case Expand]-->
SelectionDAGLegalize::ExpandNode
  --[calls: case ISD::UINT_TO_FP, TLI.expandUINT_TO_FP(...)]-->
TargetLowering::expandUINT_TO_FP
  --[declines: early return false, DstVT.getScalarType() != f64]-->
  (back in ExpandNode, expandUINT_TO_FP returned false)
  --[[fallthrough]] case ISD::SINT_TO_FP: ExpandLegalINT_TO_FP(...)]-->
SelectionDAGLegalize::ExpandLegalINT_TO_FP

=== SUB-BLOCK: the specific unsigned-i64/i32->f32/f64 branch ===
LegalizeDAG.cpp lines 2754-2808 (inside ExpandLegalINT_TO_FP, 55 source lines)
emit_count (SDNode-constructing calls) in this block, ALL sub-branches (strict + non-strict) combined: 14
    DAG.getSetCC('dl')
    DAG.getConstant('0')
    DAG.getConstant('1')
    DAG.getNode('ISD::SRL')
    DAG.getConstant('1')
    DAG.getNode('ISD::AND')
    DAG.getNode('ISD::OR')
    DAG.getSelect('dl')                     [strict-only: InCvt select]
    DAG.getNode('ISD::STRICT_SINT_TO_FP')   [strict-only]
    DAG.getNode('ISD::STRICT_FADD')         [strict-only]
    DAG.getNode('ISD::SINT_TO_FP')          [non-strict: halved-value convert]
    DAG.getNode('ISD::FADD')                [non-strict: double back]
    DAG.getNode('ISD::SINT_TO_FP')          [non-strict: direct/fast convert]
    DAG.getSelect('dl')                     [final: Slow-or-Fast branch]
contains a guard/select (branch-shaped) node: True

as-run emit count for op_117's actual instance (non-strict, i64->f32,
drops the 3 strict-only emits): 11
    DAG.getSetCC, DAG.getConstant(0), DAG.getConstant(1), SRL, DAG.getConstant(1),
    AND, OR, SINT_TO_FP, FADD, SINT_TO_FP, getSelect

=== PATH QUERY: signed i32 -> float (op_501's case) ===
ISD::any_sint_to_fp(GR32:$src)
  --[isel_pattern_match, TableGen Pat, X86InstrSSE.td]-->
defm CVTSI2SS : sse12_cvt_s<0x2A, GR32, FR32, any_sint_to_fp, ...>
  file=X86InstrSSE.td  defm_line=1010  multiclass_line=855  emit_count=1
  pattern: [(set DstRC:$dst, (OpNode SrcRC:$src))]

=== VERDICT INPUTS ===
unsigned i64->f32 sub-block emit_count = 14  (branch present: True)
signed   i32->f32 pattern emit_count   = 1   (branch present: False)
```

(Full run, including every raw node/edge dump, is in
`probe_uint64_to_float/query_output.txt`; the graph itself is
`probe_uint64_to_float/graph_cpp_probe.json`.)

## 5. hypothesis verdict, with evidence

**The hypothesis holds, and the signal is not muddy — it is sharp.**

- **Structural distinguishability, forced by construction from the
  source graph itself:**
  - The super-op case (u64->f32) is reached only after TWO explicit
    DECLINES: `X86TargetLowering::LowerUINT_TO_FP` (custom-lowering,
    target-specific, `X86ISelLowering.cpp:20584-20587`) returns
    `SDValue()` for exactly `(i64, f32|f64)` on 64-bit targets
    without AVX512; then `TargetLowering::expandUINT_TO_FP`
    (target-independent, `TargetLowering.cpp:8560`) also declines
    (`DstVT.getScalarType() != MVT::f64` at line ~8581, and f32 !=
    f64). Only after both refuse does control fall through
    (`[[fallthrough]]`, LegalizeDAG.cpp:3460-3461) into
    `SelectionDAGLegalize::ExpandLegalINT_TO_FP`, a FUNCTION that
    constructs **11 SDNodes for the as-run non-strict instance**
    (14 if both the strict and non-strict sub-branches are counted
    together, which never co-execute), including one `DAG.getSetCC`
    and one `DAG.getSelect` -- i.e. a **guard**. This is legalization/
    expansion exactly as the hypothesis names it: "the target has no
    instruction for the operation, so a FUNCTION emits several
    instructions, usually with a branch, reached only when a
    type/target check fails."
  - The single-instruction case (i32->f32, signed) is a TableGen
    `Pat`, `[(set DstRC:$dst, (OpNode SrcRC:$src))]` inside the
    `sse12_cvt_s` multiclass, instantiated by `defm CVTSI2SS :
    sse12_cvt_s<0x2A, GR32, FR32, any_sint_to_fp, ...>`
    (`X86InstrSSE.td:1010`, multiclass at line 855). This is a
    declarative table row: **1 pattern, 1 opcode (`CVTSI2SSrr`),
    no guard, no branch, no function body to walk** -- exactly
    instruction SELECTION as the hypothesis names it: "one IR
    operation matches one pattern, emits one opcode."
  - The mechanical signal the hypothesis predicted -- **emit count
    per IR operation, and which stage produced it** -- is exactly
    what separates the two: **11 (as-run) vs 1**, and **C++ function
    in the legalizer vs. TableGen pattern row consumed by the
    ISel matcher generator**. Evidence class: forced by construction
    (both counts come from parsing the actual source text at the
    pinned tag, not from reading the assembly or guessing).

- **Extent is readable from the source, and it CONTRADICTS the
  miner's "three two-instruction fragments" framing named in the
  task.** The routine's boundary is not a guess or a post-hoc
  grouping of assembly lines -- it is the literal `{ ... }` body of
  one function, `SelectionDAGLegalize::ExpandLegalINT_TO_FP`'s
  unsigned-conversion `if` block, `LegalizeDAG.cpp:2754-2808`. Every
  one of the 11 as-run SDNode constructions is inside that single
  brace-delimited block; none of them belongs to a neighboring,
  separately-triggered operator. The block is not naturally "three
  two-instruction fragments" at the source level: it is one
  seven-step sequential computation (test/branch, shr, and, or,
  convert, double, convert) plus the branch that selects between the
  doubled and direct results -- eight logical steps, most of which
  the compiler happens to schedule into a two-block CFG with a
  differing instruction count per block ONLY because the "direct"
  (`Fast`) side skips the halving steps entirely. The extent question
  the hypothesis asked ("is EXTENT readable from source") is
  answered **yes**: the source's own brace nesting gives the extent
  directly, forced by construction, with no assembly-side
  segmentation heuristic needed.
  - One nuance the source itself surfaces and prior analysis (reading
    only the assembly) could not: LLVM's own comment at
    `LegalizeDAG.cpp` (just above the block) reads *"TODO: This
    really should be implemented using a branch rather than a
    select. We happen to get lucky and machinesink does the right
    thing most of the time."* -- i.e. at the SelectionDAG level this
    is a `select` (a value-level ternary), and it is a LATER,
    separate pass (`machinesink` / X86's if-conversion) that turns it
    into the `test`/`js`/two-basic-block shape actually observed in
    op_117's ship assembly. The routine's shape in the SOURCE GRAPH
    (one function, one guarded value-select, 11 SDNode emits) and its
    shape in the FINAL ASSEMBLY (a real branch across two blocks) are
    both true, at two different stages -- evidence class: tool's own
    testimony (the comment is LLVM authors' own statement about their
    own code) plus forced-by-construction (the block's brace extent).

- **Where the signal is honestly less clean than the two-line
  hypothesis summary:** `ExpandLegalINT_TO_FP` is not single-purpose
  -- it is one function serving THREE cases (i32/i64->f64 via the
  first branch at line ~2681, unsigned i32|i64->f32/f64 via our
  block, and the strict-fp variant sharing the same block). The
  function-level `emit_count` (34, see `graph_cpp_probe.json`) is
  therefore NOT the right number to quote for "this operation's
  expansion size" -- only the as-run sub-block count (11) is.
  Reporting the function-level number without this refinement would
  have overstated the routine's size by roughly 3x. This refinement
  (sec in `query_hypothesis.py`) is recorded so a future query does
  not have to rediscover it.

## 6. frontier, and what a next probe needs to remove it

Named dead ends and what would pass them, per the node's frontier-
honesty rule:

1. **Upstream leg not built.** This probe starts at
   `X86TargetLowering::LowerOperation`'s switch and `LowerUINT_TO_FP`
   -- it does not show, as a graph path, how Clang's front end turns
   `a + b` (`a: u64, b: f32`) into an `ISD::UINT_TO_FP` node in the
   first place (Clang CodeGen's usual-arithmetic-conversions handling
   in `CGExprScalar.cpp`, then `SelectionDAGBuilder::visitUIToFP` or
   equivalent). Needed to pass it: extend the node set by the same
   grep-then-extract method, or (properly) run `build_graph.py`'s
   approach with a C++ dispatcher over the CodeGen + SelectionDAGBuilder
   region.
2. **TableGen's generated matcher table not built or inspected.** The
   `Pat` in `X86InstrSSE.td` is the SOURCE the ISel table is compiled
   from (`llvm-tblgen -gen-dag-isel` producing
   `X86GenDAGISel.inc`, generated at build time, not checked into the
   tree). This probe treats the `.td` Pat itself as the forced-by-
   construction fact and does not claim to have inspected the
   generated table. Needed to pass it: actually build LLVM at the
   pinned tag (or extract a prebuilt `X86GenDAGISel.inc` from the
   Airlock toolchain if one already exists there) and grep the
   generated matcher for the same opcode.
3. **No general `.td` parser.** `tree-sitter-tablegen` is not on
   PyPI; this probe used a two-regex reader scoped to exactly the one
   multiclass instantiation needed. A second `.td`-sourced case would
   need either a hand-written reader extended per-case (cheap, but
   not general) or building the grammar from source (a real
   dependency-fetch decision, deliberately not made in this bounded
   probe).
4. **No language dispatcher exists yet in `build_graph.py` itself.**
   This probe's `build_graph_cpp_probe.py` is a ONE-OFF, scoped to 5
   functions + 1 defm by hand-location (grep), not a generalization
   of lap one's machinery. CORE_0_3_5's own "Second language" open
   item is still open after this probe; what this probe adds is one
   proof that the case-by-case version of that idea works and gives a
   sharp answer, not that the general dispatcher has been built.

## 7. evidence class summary

| claim | class |
| --- | --- |
| LLVM source present at `<WORKSPACE_DIR>/Sources/llvm-project` | tool's own testimony (`git log`/`git tag`) |
| pinned compiler is clang 21.1.8, tag available at commit 42befb84... | tool's own testimony (compiler.txt banner + git tag lookup) |
| repo HEAD (24-init) is NOT the pinned compiler | forced by construction (date/commit comparison) |
| `X86TargetLowering::LowerOperation` dispatches `ISD::UINT_TO_FP` to `LowerUINT_TO_FP` | forced by construction (source line quoted, singleton switch case) |
| `LowerUINT_TO_FP` declines i64->f32 on 64-bit non-AVX512 | forced by construction (source line quoted) |
| decline falls through to `ExpandNode` via `LegalizeOp`'s Custom-handling | forced by construction (source line quoted, same mechanism as any Custom-lowering node) |
| `TargetLowering::expandUINT_TO_FP` declines for f32 dest | forced by construction (early-return guard quoted) |
| `ExpandLegalINT_TO_FP`'s unsigned block emits 11 SDNodes (as-run, non-strict) | forced by construction (AST walk over the exact brace-delimited block, script + output included) |
| CVTSI2SS is a single TableGen Pat, one opcode | forced by construction (regex-extracted defm + multiclass text, included) |
| the halving-select becomes a real branch in the final assembly via a later pass | tool's own testimony (LLVM's own source comment, quoted verbatim) — NOT independently re-verified against op_117's actual objdump in this probe (that verification was done in a PRIOR op_pipeline measurement, referenced but not re-run here) |
| extent of the routine = the function's brace-delimited block | forced by construction (brace-matching over the source text) |
| no general `.td` parser is available in this environment | forced by construction (failed `pip install`, exit code 1, quoted) |
