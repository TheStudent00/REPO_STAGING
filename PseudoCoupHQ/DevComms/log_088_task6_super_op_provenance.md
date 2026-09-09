# log 088 — TASK 6: join the graph to the miner (super-op provenance)

Date: 2026-08-31. Session: Claude Code, log_083 TASK 6. Depends on
TASK 1 (log_086, `compiler_graph/build_graph2.py`,
`compiler_graph/graph_cpp2.json`).

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

Two files exist already and this task's job was to connect them,
not to build either from scratch:

- `idiom_candidates.json` — a list of 2,144 rows, each one a short
  run of instructions ("the idiom") that the miner found REPEATING
  across several probe units, plus how many units it repeats in
  (`support`) and which languages it repeats across.
- `graph_cpp2.json` — Task 1's graph over four LLVM source files
  (the compiler's own X86 code-generation source). Each node is one
  function; each function carries an `emits` list — the LLVM
  opcodes (`ISD::FADD`, `ISD::XOR`, ...) that function's own source
  text constructs.

The question this task answers, per idiom: WHICH FUNCTION in that
graph is the one that would emit this idiom's instructions? An
answer converts a recurring PATTERN (found by counting) into a
recurring PATTERN WITH A NAMED SOURCE (found by reading the
compiler's own code) — that promotion is "super-op provenance."

**How the search key was chosen, and why not the obvious one.** The
instructions themselves are x86 assembly (`addsd`, `punpckldq`,
...); the graph's emits are LLVM opcode names (`ISD::FADD`). These
are two different vocabularies belonging to two different pipeline
stages, so nothing about them lines up by spelling, and nothing
should — THE SPELLING BAN forbids keying on either token anyway.
`idiom_candidates.json` already carries a bridge field, computed by
an earlier lap and marked in its own file as **forced by
construction**: `names_within_own_lifted_form`. This is the set of
VEX lifter names (a third vocabulary, from the instrumentation
layer) that an idiom's OWN instruction text was checked against,
exact-token, no guessing. Example: idiom_0001's instructions
contain `addsd`, which the file's own `vex_name_to_mnem` table maps
from `Add64F0x2` — so `Add64F0x2` sits in that idiom's
`names_within_own_lifted_form`.

This lap adds exactly ONE new mapping on top of that: VEX lifter
name → LLVM ISD opcode root (`VEX_TO_ISD_ROOTS` in
`build_super_ops.py`, 17 entries, one per name
`idiom_candidates.json`'s own `vex_name_to_mnem` already carries —
`Add64F0x2` → `FADD`, `XorV128` → `XOR`, `CmpEQ64F0x2` →
`SETCC`/`FCMP`/... and so on). This mapping is **human
interpretation of stated design**: the LLVM ISD naming convention
(float add is always spelled `FADD`, bitwise xor is always spelled
`XOR`), not a fact forced out of any artifact. It is the weakest of
the three evidence classes in play here, and every resolved record
says so on itself.

**Matching, and the honesty correction made mid-lap.** A candidate
resolves to a graph node when that node's emit list shares an ISD
opcode ROOT COMPONENT with the idiom's derived roots (component-
exact matching — split each opcode on `::` and `_` and require an
exact component match, specifically so `"OR"` never matches inside
`"XOR"`). The first version of this script broke ties between
equally-scoring nodes by graph list order — and when checked
against idiom_0001 (support 44, the SAME flagship idiom Task 1
hand-verified lands in `SelectionDAGLegalize::ExpandLegalINT_TO_FP`),
it landed on a DIFFERENT function, `lowerToAddSubOrFMAddSub`, because
that idiom's only derived root (`FADD`) is shared by ten different
functions in this region and `lowerToAddSubOrFMAddSub` merely
happened to be first in the graph's node list. That is a wrong
answer stated with false confidence — caught by re-checking against
Task 1's own known answer, not by code review. The fix: a candidate
resolves ONLY when exactly one node holds the maximum overlap size;
a tie among several nodes is recorded as an **ambiguous-match
frontier**, naming every tied function, rather than picked by list
order. Re-run, idiom_0001 now correctly reports itself as an
unresolved ambiguous 10-way tie — with `ExpandLegalINT_TO_FP` named
among the ten candidates, exactly where Task 1 found it, instead of
a confidently wrong single answer.

## instances (real super_ops.json rows, real query output, verbatim)

### a resolved super-op (idiom_0107, support 6)

```json
{
  "idiom_id": "idiom_0107",
  "instructions": [
    "mov %P0,%P2", "shr $1,%P2", "and $0x1,%P3", "or %P2,%P0",
    "cvtsi2ss %P0,%P1", "addss %P1,%P1", "cmpneqss %P1,%P4",
    "movd %P4,%P5", "and $0x1,%P5", "ret"
  ],
  "support": 6,
  "languages": ["c", "cpp"],
  "sample_unit_ids": ["c/op_513", "c/op_518", "cpp/op_513",
                       "cpp/op_518", "cpp/op_981", "cpp/op_986"],
  "names_within_own_lifted_form": ["Add32F0x4", "CmpEQ32F0x4"],
  "emitting_function": {
    "id": "LegalizeDAG.cpp::SelectionDAGLegalize::ExpandNode",
    "file": "LegalizeDAG.cpp",
    "qualified_name": "SelectionDAGLegalize::ExpandNode",
    "start_line": 3084,
    "end_line": 4553
  },
  "stage": "legalization",
  "extent": ["... 57 distinct opcodes/values this function emits,
              including ISD::FADD and ISD::SETCC ..."],
  "carrier_units": ["c/op_513", "c/op_518", "cpp/op_513",
                     "cpp/op_518", "cpp/op_981", "cpp/op_986"],
  "match_basis": {
    "derived_isd_roots": ["FADD", "FCMP", "SETCC", "SETOEQ", "SETONE"],
    "matched_isd_components": ["FADD", "SETCC"],
    "unmapped_vex_names": [],
    "evidence_class": "names_within_own_lifted_form is forced by
      construction ...; the VEX-name -> ISD-root map and the
      component-overlap match are human interpretation of stated
      design -- weakest evidence class, stated here so it is never
      read as forced"
  }
}
```

`ExpandNode` is a large multi-opcode switch function (3,084 to
4,553 — nearly 1,500 lines, 57 distinct emitted opcodes/values in
its own `extent`). It is the UNIQUE function with both `FADD` and
`SETCC` in its emit list in this four-file region, so the match is
correctly unresolved-to-one-answer... resolved to one answer with
no tie — but "unique" here means unique among four files, not
unique in the whole compiler; it is a coarse, catch-all landing
spot, named as such rather than presented as a narrow answer.

### the flagship idiom, correctly reported as ambiguous (idiom_0001, support 44)

```json
{
  "idiom_id": "idiom_0001",
  "instructions": [
    "movq %P0,%P1",
    "punpckldq 0x0(%P2),%P1 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4",
    "subpd 0x0(%P2),%P1 !!reloc=R_X86_64_PC32:.LCPI0_1-0x4",
    "movapd %P1,%P3", "unpckhpd %P1,%P3", "addsd %P1,%P3"
  ],
  "support": 44,
  "languages": ["c", "cpp"],
  "names_within_own_lifted_form": ["Add64F0x2"],
  "frontier_reason": "ambiguous match: 10 functions tie at the same
    overlap size against derived ISD roots (FADD, from Add64F0x2)
    -- picking one by list order would be unfounded, so this idiom
    is refused rather than resolved. tied candidates: LowerFROUND,
    LowerUINT_TO_FP_i64, SelectionDAGLegalize::ExpandLegalINT_TO_FP,
    SelectionDAGLegalize::ExpandNode, TargetLowering::expandUINT_TO_FP,
    X86TargetLowering::ReplaceNodeResults, combineFMA,
    lowerINT_TO_FP_vXi64, lowerToAddSubOrFMAddSub,
    lowerUINT_TO_FP_vXi32"
}
```

`SelectionDAGLegalize::ExpandLegalINT_TO_FP` — Task 1's own
hand-verified answer for this exact idiom — is named in that tied
list. This is the honest result: a single VEX name gives only one
derived ISD root, and one root is not enough to distinguish ten
functions that all touch `FADD` somewhere in a ~2,700-line and a
~200-line source file. Resolving this one for real needs either a
second forced-by-construction signal (there isn't one on this row)
or a narrower per-branch emit extraction (Task 1's own named
frontier #1: sub-block emit extraction is not built).

### spelling guard

```
$ python3 op_pipeline/check_no_spelling_keys.py op_pipeline/super_ops.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS super_ops.json -- no operator token in any key, grouping,
pairing or row structure
```

(One violation was found and fixed before this pass: the first
draft's `graph_source` field read `"../compiler_graph/..."` — the
literal `..` is one of the 91 banned tokens, Rust's range operator.
Reworded, not exempted.)

## numbers

- `idiom_candidates.json`: 2,144 candidate rows total. Candidates
  with `support >= 4` (this task's floor): 494.
- of those 494: **96 resolved** to a single emitting function (all
  96 land on the SAME function, `SelectionDAGLegalize::ExpandNode`
  — a large dispatcher, not 96 distinct emitters); **398 frontier**,
  broken down:
  - 189 ambiguous ties (multiple functions share the maximum
    overlap — the flagship idiom above is one of these)
  - 135 rows carry no `names_within_own_lifted_form` at all (no
    forced-by-construction key to search on — refused rather than
    searched on the weaker co-occurrence field)
  - 64 rows are go/rust/swift-only — Task 1's graph has no reader
    for those languages (named frontier #2 in log_086, reused here
    rather than re-declared)
  - 10 rows have derived ISD roots that overlap NO node's emit list
    in this four-file region at all
- distinct emitting functions found across all 96 resolved rows:
  **1** (`SelectionDAGLegalize::ExpandNode`, `LegalizeDAG.cpp`,
  stage: legalization).
- `graph_pins` carried through unchanged from `graph_cpp2.json`:
  `tree-sitter` 0.25.2, `tree-sitter-cpp` 0.23.4, LLVM tag
  `llvmorg-21.1.8` (commit `2078da43e25a4623cab2d0d60decddf709aaea28`,
  Task 1's pin-correction note reproduced verbatim on this file too).

## honest remainders (named, not silently dropped)

1. **96 super-ops all name the same one function.** This is a real
   measured result, not padding — `ExpandNode`'s huge multi-opcode
   switch is a genuine catch-all in this region, and a single-root
   ISD match cannot select a sub-branch of it. A real distinct
   super-op catalogue needs either sub-block emit extraction (Task
   1's remainder #1) or a second independent search signal per
   idiom; neither exists yet.
2. **189 of 494 candidates are ambiguous ties**, including the
   flagship idiom. The mechanism is honest about this rather than
   guessing — but it means the majority of the "should resolve"
   population does not resolve this lap.
3. **The VEX→ISD root map is human interpretation**, not forced.
   It covers exactly the 17 names `idiom_candidates.json`'s own
   `vex_name_to_mnem` carries; any candidate whose
   `names_within_own_lifted_form` holds a name outside those 17
   would report `unmapped_vex_names` rather than guess (0 rows hit
   this in the actual run — every name seen was one of the 17).
4. **The four-file region is Task 1's, unexpanded.** A candidate
   whose true emitter lives outside `X86ISelLowering.cpp` /
   `LegalizeDAG.cpp` / `TargetLowering.cpp` / `X86InstrSSE.td`
   cannot be found by this query regardless of match quality — it
   will show as "no overlap" or, worse, tie-out against
   in-region functions that merely share an opcode. This is the
   same scope boundary Task 1 named, not a new one.
5. **No runtime-library stage was reached.** All 96 resolved rows
   are `legalization`; `selection` and `runtime-library` are named
   stage categories in the classifier but no candidate landed
   there this lap (`selection` did appear before the tie-honesty
   fix, on the now-corrected wrong answer — after the fix, zero).

## stop rule check

No new ontological category was needed or invented. `stage` uses
the three categories the brief itself names
(selection/legalization/runtime-library); the fourth value the
classifier can produce, `"unclassified:<file>"`, never fired
(every emitting function found this lap sits in one of the four
named region files) and is a defensive fallback, not a new category
in use.

## files

- `Research/op_pipeline/build_super_ops.py` — new, the query script.
- `Research/op_pipeline/super_ops.json` — new, its output (96
  resolved, 398 frontier, passes `check_no_spelling_keys.py`).
- this log.
