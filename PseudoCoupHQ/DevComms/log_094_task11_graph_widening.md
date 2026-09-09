# log 094 — TASK 11: widen graph coverage so super-op provenance resolves

Date: 2026-08-31. Session: Claude Code, log_091 TASK 11. Depends on
TASK 1 (log_086, `compiler_graph/build_graph2.py`, `graph_cpp2.json`)
and TASK 6 (log_088, `op_pipeline/build_super_ops.py`, `super_ops.json`).

THE SPELLING BAN, restated verbatim as required by every artifact on
this line: "THE SPELLING BAN, ABSOLUTE (the owner, restated in anger
2026-08-25 after a second violation). No operator token may appear in
ANY key, grouping, pairing, row structure, candidate selection, or
comparison scope, anywhere in this line — not in matching, not in
"which pairs get compared", not in report rows, not in dropdowns. The
candidate set for comparison comes from machine-form evidence
(clusters, connections, type pairs) or from ratified intention — never
from the token. The token appears exactly once per unit: as a display
label on the member."

## plain-words walkthrough

Two new files, both new artifacts (nothing from lap two overwritten):

- `compiler_graph/build_graph3.py` — same reader/resolver machinery as
  `build_graph2.py` (imported by copy, not re-implemented), with
  `REGION_FILES` widened from the probe's original four files to
  eleven: the four unchanged, plus the rest of the SelectionDAG
  legalization family that already sits beside `LegalizeDAG.cpp` in
  the same source directory — `SelectionDAG.cpp`, `LegalizeTypes.cpp`,
  `LegalizeFloatTypes.cpp`, `LegalizeIntegerTypes.cpp`,
  `LegalizeVectorOps.cpp`, `LegalizeVectorTypes.cpp`,
  `LegalizeTypesGeneric.cpp`. This is the "functions those calls
  reach" widening the brief asked for, bounded to one directory
  rather than the whole compiler (named stop rule, not a silent
  narrowing).
- `op_pipeline/build_super_ops2.py` — the same join
  `build_super_ops.py` performs, pointed at the new graph
  (`graph_cpp3.json`), with exactly one new rule added:
  **dispatcher demotion**. Among functions tied at the same maximum
  ISD-root overlap, if the graph's own `calls` edges (the SAME
  `tree_sitter_call_expression` edges the builder already produces —
  nothing new asserted) show one tied function CALLS another tied
  function, the caller is dropped from the tie. A dispatcher that
  only relays to a more specific tied sibling is demoted in favor of
  the sibling whose own body holds the emit. This is graph-structural
  (call edges only) — no operator token is read or compared anywhere
  in the rule.

**Before widening the file set, the "37,733 unresolved calls" number
was checked against what it actually is, not assumed.** Counting the
`unresolved_call` frontier by callee name shows the top entries are
`DAG.getNode` (3,331), `SDValue` (1,397), `NODE_NAME_CASE` (463),
`SDLoc` (239) — constructors and member calls the reader's node model
does not resolve regardless of region size — and local lambdas such
as `CanonicalizeShuffleInput` (43), confirmed by `git show`-reading
`X86ISelLowering.cpp` directly: it is declared
`auto CanonicalizeShuffleInput = [&](MVT VT, SDValue Op) {` at line
39956, a local lambda, never a candidate for cross-file resolution no
matter how wide the region gets. Widening the file set can only ever
fix the OTHER kind of frontier entry — a real call into a function
defined in a sibling file the graph had not read — so the fix target
was named honestly before writing `build_graph3.py`, not guessed.

## instances (real query outputs, verbatim)

### widening's real effect on the call graph

```
old (graph_cpp2.json, 4 files): 1232 nodes, 3070 edges
new (graph_cpp3.json, 11 files): 2280 nodes, 18331 edges

unresolved calls FROM the original 4 files:
  old: 37733
  new: 28156
```

9,577 calls that originate in the four original files now resolve to
a real node, because their callee is defined in one of the seven newly
read sibling files. This is the honest, measured effect of widening —
real, but it does not by itself change how many super-ops resolve
(below).

### the concrete test — `SelectionDAGLegalize::ExpandNode` dispatcher through to the specific expander

`idiom_0001` (support 44, the flagship idiom, Task 1's own
hand-verified target `ExpandLegalINT_TO_FP`) re-run against
`graph_cpp3.json` through `build_super_ops2.py`, verbatim:

```json
{
  "idiom_id": "idiom_0001",
  "names_within_own_lifted_form": ["Add64F0x2"],
  "frontier_reason": "ambiguous match: 10 functions tie at the same overlap size against derived ISD roots (FADD, from Add64F0x2) -- picking one by list order would be unfounded, so this idiom is refused rather than resolved. tied candidates: DAGTypeLegalizer::ExpandFloatRes_XINT_TO_FP, LowerFROUND, LowerUINT_TO_FP_i64, SelectionDAGLegalize::ExpandLegalINT_TO_FP, TargetLowering::expandUINT_TO_FP, X86TargetLowering::ReplaceNodeResults, combineFMA, lowerINT_TO_FP_vXi64, lowerToAddSubOrFMAddSub, lowerUINT_TO_FP_vXi32 (dispatcher demotion applied and reduced this tie but did not break it)"
}
```

Verified directly: `graph_cpp2.json`/`graph_cpp3.json` both carry a
real `calls` edge
`LegalizeDAG.cpp::SelectionDAGLegalize::ExpandNode` ->
`LegalizeDAG.cpp::SelectionDAGLegalize::ExpandLegalINT_TO_FP` at line
382 (`tree_sitter_call_expression` evidence) — this is the exact
dispatcher-to-expander edge the brief names. Dispatcher demotion used
this edge and correctly dropped `ExpandNode` itself from the tie (it
calls a tied sibling, so it is a relay, not the emitting site). But
the widened region's new files supplied a REPLACEMENT tenth
candidate, `DAGTypeLegalizer::ExpandFloatRes_XINT_TO_FP` (defined in
`LegalizeFloatTypes.cpp`, one of the seven newly-read files, itself
touching `ISD::FADD`), so the tie stayed at 10 members net — one
demoted, one gained.

**THE CONCRETE TEST: FAIL, reported plainly.** The idiom does not land
uniquely on `ExpandLegalINT_TO_FP`. `ExpandLegalINT_TO_FP` is named
among the ten tied candidates (as it was in lap two), which is the
correct honest position for it given the evidence in hand — a single
derived ISD root (`FADD`) is not selective enough to distinguish ten
functions that all touch `FADD` somewhere in an eleven-file region,
and widening the file set can add new tied candidates as fast as it
removes dispatchers. Breaking this specific tie needs a second
forced-by-construction signal (sub-block emit extraction per
function, or matching against the SPECIFIC switch-case that reaches
each callee rather than whole-function emit lists) — named here as
the frontier, not attempted this lap; this refusal instead of a
forced pick is the same posture Task 6 took when it caught its own
list-order bug.

### spelling guard, both new artifacts

```
$ python3 op_pipeline/check_no_spelling_keys.py compiler_graph/graph_cpp3.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS graph_cpp3.json -- no operator token in any key, grouping, pairing or row structure

$ python3 op_pipeline/check_no_spelling_keys.py op_pipeline/super_ops2.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS super_ops2.json -- no operator token in any key, grouping, pairing or row structure
```

## pins (quoted from `graph_cpp3.json`'s own `pins` object, not from notes)

```json
{
  "tree_sitter": "0.25.2",
  "tree_sitter_cpp": "0.23.4",
  "llvm_tag": "llvmorg-21.1.8",
  "llvm_commit_resolved_this_run": "2078da43e25a4623cab2d0d60decddf709aaea28"
}
```

Sources extracted with `git show llvmorg-21.1.8:<path>` against
`Sources/llvm-project`, never the working tree (which is
checked out at `llvmorg-24-init` — verified again this session,
unchanged from lap two's finding).

## numbers

- `graph_cpp3.json`: 2,280 nodes (was 1,232), 18,331 edges (was
  3,070), 11 region files (was 4). `unresolved_call` frontier: 40,385
  total (up from 37,733 — the wider region has more raw call sites
  overall), but calls FROM the original four files specifically drop
  37,733 -> 28,156 (9,577 newly resolved).
- `super_ops2.json` re-join, same 494 candidates at `support >= 4`:
  - **96 resolved** (same count as lap two, same landing function,
    `SelectionDAGLegalize::ExpandNode` — unchanged)
  - **398 frontier**, broken down IDENTICALLY to lap two:
    - **189 ambiguous ties** — same count. **0 of the 189 broke.**
      157 of the 189 had their tied-candidate SET changed by
      dispatcher demotion (a member dropped, sometimes a new one
      gained from the widened region) but every one stayed above
      one candidate.
    - **64 no-graph-coverage** — same count, unchanged. This bucket
      is language coverage (go/rust/swift have no reader in either
      graph), not file coverage inside c/cpp — file widening cannot
      touch it by construction, so it staying at 64 exactly is the
      expected honest result, not a missed opportunity.
    - 135 no-search-key, 10 no-overlap-in-region — both unchanged.
  - **Concrete test (SelectionDAGLegalize::ExpandNode dispatcher ->
    specific expander): FAIL.** `ExpandLegalINT_TO_FP` remains one
    of ten tied candidates, not the unique answer.

## honest assessment

Widening the region measurably reconnected the call graph (9,577
calls resolved from the original four files) and the dispatcher-
demotion rule is real and correctly removes true relay functions from
ties using only graph structure — verified on `ExpandNode` itself,
which dropped out of idiom_0001's tie exactly as its call edge to
`ExpandLegalINT_TO_FP` predicts. But the ambiguity in the 189 tied
idioms is not caused by MISSING call edges or by dispatchers polluting
ties — it is caused by whole-function emit lists being too coarse: many
sibling functions in the legalization/lowering family emit the same
single ISD opcode root (`FADD`, `XOR`, ...) somewhere in a large body,
and one root is not a selective enough signal to choose among them.
Widening the file set does not fix that, and in idiom_0001's case
supplied a same-sized replacement tie. The named frontier from log_086
and log_088 — sub-block / per-branch emit extraction instead of
whole-function emit lists — is the mechanism that would actually
break these ties; it is not built this lap, stated here rather than
attempted under this task's clock.

## files written this lap, all named

- `compiler_graph/build_graph3.py` (new; widened builder)
- `compiler_graph/graph_cpp3.json` (new; 2,280 nodes / 18,331 edges /
  11 region files)
- `op_pipeline/build_super_ops2.py` (new; re-join with dispatcher
  demotion)
- `op_pipeline/super_ops2.json` (new; 96 resolved / 398 frontier)

No file from lap one or lap two (`build_graph2.py`, `graph_cpp2.json`,
`build_super_ops.py`, `super_ops.json`) was modified.
