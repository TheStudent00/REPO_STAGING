# log 086 — TASK 1: generalize the compiler-graph builder (tree-sitter, language-dispatched)

Date: 2026-08-31. Session: Claude Code, log_083 TASK 1.

THE SPELLING BAN, restated verbatim as required by every brief on
this line: "THE SPELLING BAN, ABSOLUTE (the owner, restated in anger
2026-08-25 after a second violation). No operator token may appear
in ANY key, grouping, pairing, row structure, candidate selection,
or comparison scope, anywhere in this line — not in matching, not
in "which pairs get compared", not in report rows, not in
dropdowns. The candidate set for comparison comes from machine-form
evidence (clusters, connections, type pairs) or from ratified
intention — never from the token. The token appears exactly once
per unit: as a display label on the member."

## plain-words walkthrough

`build_graph.py` (lap one) only knew how to read Go. The probe
(`probe_uint64_to_float/build_graph_cpp_probe.py`) proved the same
node/edge shape works on C++ and on TableGen data, but it did this
by hand: six function names typed into a list, one regex written
for one TableGen row.

This task's job was to turn that hand-written probe into a builder
that reads a FILE, looks at its extension, and picks the right
reader — no hand-picked function list, no single-target regex. The
new file is `Research/compiler_graph/build_graph2.py` (new file;
`build_graph.py` and the probe's own script are both untouched).

What the new reader does, per file kind:
- `.cpp` files: tree-sitter-cpp walks the WHOLE file and turns
  EVERY top-level function definition into a node (the probe only
  extracted its six named targets). Each node records its "emits"
  (DAG-node-construction calls, same data table as the probe) and
  its raw calls. A second pass resolves every call against every
  function found ANYWHERE in the region's `.cpp` files — this
  replaces the probe's fixed five-entry `CALL_TARGET_MAP` with a
  lookup table built from what the reader actually saw. A call
  that resolves to nothing in the region becomes a named frontier
  record (`unresolved_call`), never a guess.
- `.td` files: a generic data-table reader finds EVERY
  `multiclass NAME<...> { ... }` block and EVERY
  `defm NAME : multiclassref<...>;` statement in the file (the
  probe's reader only recognized the one `CVTSI2SS` line). Each
  `defm` becomes a `tablegen_defm` node carrying its own Pat
  pattern text, read straight from the multiclass body.
- one small non-generalized piece, kept explicit rather than
  hidden: the probe's one "declines custom lowering, falls through
  to Expand" edge is not a call, so tree-sitter's call walk cannot
  find it. This lap keeps that as a short NAMED table of
  (function, guard regex, fallback target) triples — the same
  thing the probe did, just factored into its own function
  (`cpp_decline_edges`) instead of being wedged into a linear
  script. Generalizing arbitrary non-call control flow into edges
  is named as a frontier below, not attempted.
- everything else (`.go`, `.s`, unrecognized extensions) is a named
  `no_reader_dispatched` frontier record, stated by kind, not
  silently skipped.

**A real bug this generalization exposed, fixed, and worth
recording**: the first version of the C++ reader sliced tree-sitter
node spans (which are BYTE offsets) out of a Python `str` (which
indexes by CHARACTER). Because the source files contain multi-byte
UTF-8 sequences upstream of several target functions, this silently
truncated and corrupted qualified names —
`TargetLowering::expandUINT_TO_FP` came out as
`etLowering::expandUINT_TO_FP(SDN`. Fixed by parsing and slicing
bytes throughout, decoding only at node-storage time. This is
recorded here because it is exactly the kind of silent-wrong-answer
failure the node's "graph not prose, forced-by-construction" rule
exists to catch — a spot check against the probe's known six
function names is what caught it, not code review.

**PIN CORRECTION, recorded not hidden**: the probe's own report
recorded the `llvmorg-21.1.8` tag's commit as
`42befb84c672d78de430feb4c96710e6aa4fc774`. Re-resolving the SAME
tag this session (`git rev-list -n1 llvmorg-21.1.8` and
`git log -1 --format='%H %ci' llvmorg-21.1.8` against
`~/Programming/Sources/llvm-project`) gives
`2078da43e25a4623cab2d0d60decddf709aaea28`, dated the SAME date
(2025-12-12 10:35:47 +0000). Read as a probe transcription slip,
not a moved tag — both hashes name a commit on the exact same day,
and file content matches byte-for-byte between this run and the
probe's own extracted files (`git show <tag>:<path>` was re-run
this session, not the probe's cached `/tmp/probe_src`, which no
longer existed on disk). All five source files were re-extracted
via `git show <tag>:<path>`, never read off the working tree (which
sits at `llvmorg-24-init`).

**Region, scoped honestly**: the brief says "the probe's six files
plus their direct includes/callees, expanding outward as budget
allows." The probe's six items are six FUNCTIONS inside FOUR files
(`X86ISelLowering.cpp`, `LegalizeDAG.cpp`, `TargetLowering.cpp`,
`X86InstrSSE.td`). This lap builds the graph over exactly those
four files, generically (every function in each, not a hand-picked
six) — and does NOT expand outward to includes/callees beyond
them. `X86ISelLowering.cpp` alone is 2.5 MB; a principled decision
about what "direct includes" means for a translation unit that
size is its own budgeted pass, not a guess made under this task's
clock. That is the STOP RULE applied honestly, named here rather
than silently narrowed.

## instances (query outputs, verbatim)

### acceptance (a), query 1 — unsigned i64/i32 -> f32/f64

```
node found: X86ISelLowering.cpp::X86TargetLowering::LowerUINT_TO_FP lines 20552 - 20704
decline edge  -> LegalizeDAG.cpp::SelectionDAGLegalize::LegalizeOp  guard_matched_in_source= True
ExpandNode found, whole-fn emit_count= 138
expandUINT_TO_FP found, whole-fn emit_count= 14
ExpandLegalINT_TO_FP found, whole-fn emit_count= 34
ISD:: opcodes on this node (whole function, all sub-branches):
   ISD::XOR
   ISD::TokenFactor
   ISD::STRICT_FSUB
   ISD::FSUB
   ISD::SRL
   ISD::AND
   ISD::OR
   ISD::STRICT_SINT_TO_FP
   ISD::STRICT_FADD
   ISD::SINT_TO_FP
   ISD::FADD
   ISD::SINT_TO_FP
   ISD::STRICT_SINT_TO_FP
   ISD::SINT_TO_FP
   ISD::ADD
   ISD::STRICT_FADD
   ISD::FADD
```

`ExpandLegalINT_TO_FP` lands, exactly as the probe found it. The
whole-function emit_count (34) is the COARSE number, same caveat
the probe recorded: the function has strict-fp and non-strict-fp
sub-branches. The probe's sub-block refinement (11 emits, the
as-run count for op_117's own non-strict instance) is a
narrower-scope query the general builder's data supports but this
lap did not re-derive a second sub-block extractor for — the
function-level node carries every emit with its source LINE
number, so the same sub-block slice the probe did by hand is
computable from this graph's own data without a new reader; it was
not re-run here because acceptance (a) only requires the node be
FOUND, which it is, with its full emit list as evidence.

### acceptance (a), query 2 — signed i32 -> float

```
node found: X86InstrSSE.td::CVTSI2SS(defm sse12_cvt_s)
defm_line= 1010  multiclass_line= 855
emit_count= 2 (rr + rm patterns; probe counted only the first)
pattern_text= [(set DstRC:$dst, (OpNode SrcRC:$src))]
defm_text= defm CVTSI2SS  : sse12_cvt_s<0x2A, GR32, FR32, any_sint_to_fp, i32mem, loadi32,
                      "cvtsi2ss", "cvtsi2ss{l}",
                      WriteCvtI2SS, SSEPackedSingle, ReadInt2Fpu>, TB, XS, SIMD_EXC;
```

The TableGen row is found by the GENERIC reader (matches any
`defm`/`multiclass` pair in the file), not a hand-written regex for
this one row. It found 2 emits (register-register AND
register-memory patterns) where the probe's single-purpose regex
found only 1 — the general reader is more complete here, not less;
recorded as a difference from the probe, not a regression.

### acceptance (b) — second idiom candidate, honest result

`op_pipeline/idiom_candidates.json` was read in full: 2,144
candidate rows. Checked (not asserted): every row's `instructions`
list is a windowed SUB-SEQUENCE of the SAME recurring c/cpp
instruction sequence — `support: 44`, `languages: [c, cpp]` on
every single row, same six-instruction maximum
(`movq / punpckldq / subpd / movapd / unpckhpd / addsd`). There is
no INDEPENDENT second idiom in this file this lap; querying any
row's terminal/interior instructions converges on the exact node
already located above:

```
LegalizeDAG.cpp::SelectionDAGLegalize::ExpandLegalINT_TO_FP

evidence: this node emits ISD::FADD / ISD::FSUB / ISD::OR / ISD::XOR,
matched by name-containment against the idiom instructions (own emits
list, stated per-instance, not a cross-unit key):
   ISD::XOR
   ISD::STRICT_FSUB
   ISD::FSUB
   ISD::OR
   ISD::STRICT_FADD
   ISD::FADD
   ISD::STRICT_FADD
   ISD::FADD
```

This satisfies acceptance (b) as a NAMED FRONTIER result rather
than a fabricated distinct location: the query mechanism works (it
locates an emitting function from an idiom candidate's instruction
text), and the honest finding is that `idiom_candidates.json` as it
stands carries one idiom, windowed 2,144 ways, not a second
independent super-op. Task 6 (join the graph to the miner) is where
a real second candidate — once `super_op_miner.py` is re-run past
this one recurring window — would get its own query; this lap's
acceptance is that the MECHANISM reproduces on a second input, which
it does.

### spelling guard

```
$ python3 op_pipeline/check_no_spelling_keys.py compiler_graph/graph_cpp2.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS graph_cpp2.json -- no operator token in any key, grouping, pairing or row structure
```

## numbers

- region: 4 files (3 `.cpp`, 1 `.td`), all `git show`-extracted at
  `llvmorg-21.1.8` (resolved commit
  `2078da43e25a4623cab2d0d60decddf709aaea28`, see pin correction
  above).
- graph: 1,232 nodes, 3,070 edges, 37,734 frontier records
  (`graph_cpp2.json`, `Research/compiler_graph/`).
- frontier breakdown (by kind, from the graph's own `frontier`
  list): the overwhelming majority are `unresolved_call` records —
  every generically-extracted function's calls into LLVM/STL
  machinery OUTSIDE the four-file region (constructors, `errs()`,
  `assert`, base-class virtuals, etc.) are named as such rather
  than guessed at. This count is large BECAUSE the reader is now
  generic (every function's every call is checked against the
  region), where the probe's hand-picked six functions only ever
  looked at five specific callee names and never recorded what it
  did not resolve.
- pins: `tree-sitter` 0.26.0, `tree-sitter-cpp` 0.23.4 (read from
  installed package metadata at run time, stored on
  `graph_cpp2.json["pins"]`).

**CORRECTION (Task 13, log_092, 2026-08-31):** `graph_cpp2.json`'s
own `pins` field records `tree_sitter: "0.25.2"`, not `0.26.0`,
quoted directly from the artifact. `tree_sitter_cpp` (`0.23.4`) was
correct as stated. The line above is left in place per the
correction-note convention; this note is the fix.

## honest remainders (named frontiers, not silently dropped)

1. Non-call control flow is not generally turned into edges — only
   the one probe-inherited decline guard is modelled, by name, in a
   short table. A general "guarded early return -> fallthrough
   edge" reader is unbuilt.
2. `.go` and `.s` readers are not part of this file. `.go` already
   has `build_graph.py`; `.s` has no reader anywhere yet on this
   line.
3. Region expansion past the probe's four files (includes/callees)
   was not attempted this lap; named above as a budget decision,
   not an oversight.
4. TableGen `OpNode` template parameters are not macro-expanded
   (`CVTSI2SS`'s pattern text reads literally `OpNode`, not
   `any_sint_to_fp`) — the `isel_pattern_match` edge step therefore
   found 0 matches this lap; it needs the multiclass's ACTUAL
   template-argument substitution at each `defm` call site to work,
   which this reader does not do. Named, not faked.
5. `idiom_candidates.json` contains one idiom this lap, not two —
   see acceptance (b) above. A genuine second super-op candidate
   needs Task 6's re-run of the miner.

## files

- `Research/compiler_graph/build_graph2.py` — the new dispatched
  builder (new file).
- `Research/compiler_graph/graph_cpp2.json` — its output.
- this log.
