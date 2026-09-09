# log 100 -- TASK 16: provenance tie-breaking by reachability

Date: 2026-08-31. Session: Claude Code, log_097 TASK 16. Depends on
TASK 11 (log_094, `compiler_graph/build_graph3.py`, `graph_cpp3.json`,
`op_pipeline/build_super_ops2.py`, `super_ops2.json`, 96 resolved /
398 frontier / 189 ambiguous ties, 0 of 189 broke) and TASK 6
(log_088, the original join and the flagship idiom idiom_0001).

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.

## plain-words walkthrough

Round 2 (log_094) diagnosed WHY widening the file set could not break
ties: every candidate function in a tie shares one ISD opcode root
(`FADD`, `SETCC`, ...) somewhere in its body, and one shared root is
not selective enough among ten functions in the same source family.
The fix round 2 named but did not build: find WHICH candidate is
actually REACHED for the idiom's specific IR operation kind, by
reading the compiler's own dispatch logic, not by counting opcodes
anywhere in a function body.

This task builds that reachability check, in a new file
`op_pipeline/build_super_ops3.py`, over `super_ops2.json`'s 189
ambiguous ties. Two pieces of real evidence, neither the operator
token:

**1. The idiom's IR kind, from carrier-unit machine-form evidence.**
Every idiom's `sample_unit_ids` point at rows in
`probe_manifest_c.json` / `probe_manifest_cpp.json`. Those rows carry
`lhs_rep` / `rhs_rep` -- machine reps like `u64`, `f64` -- assigned
from the probe's C/C++ TYPE by an earlier lap, not from the token.
When a carrier row shows an INTEGER rep paired with a FLOAT rep, that
carrier's own operation is a `UINT_TO_FP`/`SINT_TO_FP` conversion
(signed iff the integer rep is not `u`-prefixed), with the source/
destination widths read off the reps themselves. This override is
applied ONLY when the idiom's own derived ISD roots are a subset of
`{FADD, FSUB}` -- the two roots every *_TO_FP expansion algorithm in
the pinned source terminates in, verified by reading all three
candidate bodies (below). A compare idiom riding the SAME carrier
units (idiom_0153/0154, `CmpEQ64F0x2`/`CmpEQ32F0x4`, roots `FCMP`/
`SETCC`/...) is a DIFFERENT idiom on a shared carrier and is refused
by this same restriction rather than misclassified as a conversion --
this bug was caught mid-session (see instances below) and fixed
before the final run.

**2. Which function is REACHED for that kind, parsed as data from the
pinned source.** `llvmorg-21.1.8` (never the working tree, which sits
at `llvmorg-24-init` -- reverified this run and recorded in the
output's own `source_pins`), read via `git show` for the same eleven
files `build_graph3.py` already reads. Two dispatch structures are
parsed as plain text, never hand-typed:

- `setOperationAction(ISD::<kind>, MVT::<vt>, <action>)` calls inside
  X86ISelLowering.cpp's constructor -- whether X86 marks a kind+VT
  pair `Custom` (routes through X86's own lowering) or leaves it to
  the generic legalizer.
- `X86TargetLowering::LowerOperation`'s big switch (`case ISD::<kind>:
  return Callee(...)`, one line per case, X86ISelLowering.cpp) and
  `SelectionDAGLegalize::ExpandNode`'s big switch (`case ISD::<kind>:`
  label groups, LegalizeDAG.cpp) -- each gives a first-hop callee
  name or case body text.

A tied candidate resolves when its own (unqualified) name is the
first-hop callee, or appears as a call inside the first-hop callee's
own body (a second, real hop over real call text -- the same kind of
evidence `build_graph3.py`'s `calls` edges already use, followed one
level deeper for this specific kind only). A tie breaks ONLY when
EXACTLY ONE tied candidate is reached this way; more than one, or
zero, stays on the frontier, named honestly -- never picked by list
order.

## instances (real parsed data, real resolution, verbatim)

### the acceptance idiom, resolved -- and a correction to the prior "hand-verified answer"

`idiom_0001` (support 44) carries `c/op_118`: `uint64_t a + double b`
(`lhs_rep: u64`, `rhs_rep: f64` -- a real probe row, quoted below).
That is machine-form evidence of an implicit `UINT_TO_FP` conversion
before the add; the idiom's own derived root is `FADD` alone, inside
the `{FADD, FSUB}` eligibility set, so the override applies:

```
carrier row op_118: lhs_rep=u64 rhs_rep=f64 -> int/float rep
mismatch, machine-form evidence of an implicit UINT_TO_FP
```

Parsed dispatch data (verbatim from the run):

```
setOperationAction(ISD::UINT_TO_FP, ...) rows found:
  {"i64": ["Custom"], "i32": ["Custom"], ...}
X86TargetLowering::LowerOperation case ISD::UINT_TO_FP -> LowerUINT_TO_FP
hop-2 search inside LowerUINT_TO_FP(...)'s own body: found LowerUINT_TO_FP_i64
SelectionDAGLegalize::ExpandNode: no 'case ISD::UINT_TO_FP' label found
```

`idiom_0001` resolves UNIQUELY to `LowerUINT_TO_FP_i64`
(X86ISelLowering.cpp).

**This is NOT the log_097/log_086 "hand-verified" answer
(`SelectionDAGLegalize::ExpandLegalINT_TO_FP`), and the source itself
says why.** `X86ISelLowering.cpp:255` sets
`setOperationAction(ISD::UINT_TO_FP, MVT::i64, Custom)` -- X86 marks
this exact (kind, width) pair Custom, which means the generic
legalizer's `ExpandNode`/`ExpandLegalINT_TO_FP` path is never reached
for it at all; the node is resolved through X86's own `LowerOperation`
-> `LowerUINT_TO_FP` -> `LowerUINT_TO_FP_i64` instead.
`LowerUINT_TO_FP_i64`'s own comment (X86ISelLowering.cpp:20204-20215,
quoted verbatim, under 15 words per line) documents exactly the
idiom's instructions:

```
movq       %rax,  %xmm0
punpckldq  (c0),  %xmm0
subpd      (c1),  %xmm0
pshufd     $0x4e, %xmm0, %xmm1   (or haddpd under SSE3)
addpd      %xmm1, %xmm0
```

against the idiom's own instructions (super_ops2.json, unchanged):

```
movq %P0,%P1
punpckldq 0x0(%P2),%P1
subpd 0x0(%P2),%P1
movapd %P1,%P3
unpckhpd %P1,%P3
addsd %P1,%P3
```

Move, interleave-constant, subtract-packed, shuffle/extract-high,
add -- the same five-step shape, mnemonic for mnemonic. Neither
`SelectionDAGLegalize::ExpandLegalINT_TO_FP` (its unsigned i64/f64
path is a sign-bit-test/select routine -- SetCC, shift, and, or,
select -- with no `punpckldq`/`subpd` anywhere) nor
`TargetLowering::expandUINT_TO_FP` (a scalar bit-fusion routine with
no vector shuffle/extract step) produces this instruction shape.
Reported as a correction, not a silent overwrite: the prior lap's
"hand-verified" claim was itself unverified against the actual
per-candidate instruction text; this lap's answer is the one that
matches the idiom's own bytes.

### the mid-session bug, caught and fixed before the final run

The first version of `derive_kind()` applied the conversion override
to ANY idiom whose carrier units contained an int/float rep mismatch,
regardless of the idiom's own root. Re-run against `idiom_0153`/
`idiom_0154` (support 6, root `CmpEQ64F0x2`/`CmpEQ32F0x4` ->
`FCMP`/`SETCC`/`SETOEQ`/`SETONE` -- a COMPARE, not an add) it wrongly
classified both as `UINT_TO_FP` because their sample carriers happen
to include a `uint64/double` compare probe, then correctly found zero
reachable candidates (an honest zero hiding a wrong kind). Fixed by
restricting the override to idioms whose derived roots are a subset
of `{FADD, FSUB}` -- re-run, `idiom_0153`/`idiom_0154` now correctly
refuse at the kind-derivation step:

```
idiom_0153: refused: no conversion evidence on any carrier row, and 4
derived ISD roots (not exactly one) -- no single forced kind, refused
at the kind-derivation step
idiom_0154: refused: no conversion evidence on any carrier row, and 4
derived ISD roots (not exactly one) -- no single forced kind, refused
at the kind-derivation step
```

A second bug, also caught before the final run: the regex extracting
`derived ISD roots (...)` from `super_ops2.json`'s own text originally
captured the whole parenthetical, including the trailing
`, from Add64F0x2` vex-name clause, as if it were part of the roots
list -- corrupting the `{FADD, FSUB}` subset check for every row.
Fixed by splitting on the literal `, from ` boundary the generator
(`build_super_ops2.py`) itself always writes.

### spelling guard

```
$ python3 op_pipeline/check_no_spelling_keys.py op_pipeline/super_ops3.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS super_ops3.json -- no operator token in any key, grouping,
pairing or row structure
```

## numbers (computed, breakdown pasted per the round-3 rule)

- 189 ambiguous ties in `super_ops2.json`'s frontier (unchanged input,
  re-verified this run: `len([r for r in frontier if
  r['frontier_reason'].startswith('ambiguous match:')]) == 189`).
- **121 of 189 broke** (64.0%). All 121 resolve to the SAME single
  emitting function, `LowerUINT_TO_FP_i64` (X86ISelLowering.cpp) --
  computed: `Counter(r['emitting_function_qualified_name'] for r in
  broken) == {'LowerUINT_TO_FP_i64': 121}`. This is a real, measured
  result, not padding: every one of these 121 idioms is a sub-sequence
  or full instance of the same unsigned-i64-to-double conversion
  routine, mined at different lengths/supports by the recurrence
  miner from the same underlying carrier probes (idiom_0001,
  idiom_0003, idiom_0006, idiom_0007 all share the exact same 8
  `sample_unit_ids`, confirmed by direct comparison).
- **68 of 189 stayed on the frontier**, broken down:
  - 44 refused at the kind-derivation step: either no carrier shows
    an int/float rep mismatch and the idiom has more than one derived
    ISD root (no single forced kind), or the roots are outside the
    `{FADD, FSUB}` eligibility set (a compare/bitwise/other idiom that
    happens to ride a conversion-bearing carrier -- idiom_0153/0154's
    class, above).
  - 24 got a derived kind (`UINT_TO_FP` on 24 of these, checked:
    `sint_to_fp` count among this bucket is 0) but the reachability
    search found ZERO tied candidates -- the true emitter for that
    (kind, width) pair is not in the tied set at all, or the parser's
    two dispatch structures (X86's `LowerOperation`/`ExpandNode`) do
    not cover where it actually lives (e.g. a type-legalization-stage
    expansion in one of the widened `LegalizeFloatTypes.cpp`-family
    files, not directly text-searched by this lap's parser). Named
    frontier, not silently dropped.
  - 0 of 189 landed with MORE than one candidate still reached after
    the reachability check (computed: `len([r for r in
    still_ambiguous_or_refused if 'still ambiguous' in
    r['task16_reachability']['trace'][-1]]) == 0`) -- the mechanism
    never produced a smaller-but-still->1 tie; every attempted row
    landed at exactly 0 or exactly 1.
- 121 + 44 + 24 = 189, verified by direct count.

## honest remainders (named, not silently dropped)

1. **The reachability parser covers two dispatch structures only**
   (`X86TargetLowering::LowerOperation`'s switch and
   `SelectionDAGLegalize::ExpandNode`'s switch), plus one level of
   hop-2 body search. A true emitter reached through a DIFFERENT
   dispatch path -- e.g. the type-legalizer's own promote/expand
   routing inside `LegalizeFloatTypes.cpp`/`LegalizeIntegerTypes.cpp`,
   which `build_graph3.py`'s widened region reads but this lap's
   parser does not specifically dispatch-parse -- is invisible to
   this check and reports as "0 reached" honestly rather than a false
   resolve. This is the named cause behind most of the 24-row bucket
   above, not attempted further this lap.
2. **The hop-2 body-boundary heuristic** (`callee_body()`, bounded by
   the next `\n}\n\n` line, capped at 8000 chars) is a formatting
   heuristic, not a real parser -- checked directly against
   `LowerUINT_TO_FP`'s own body (6,548 chars after the fix, contains
   `LowerUINT_TO_FP_i64`/`LowerUINT_TO_FP_i32` and nothing else from
   the 121 resolved rows' tied sets, verified by direct string
   search) but not proven correct for every function in the region.
3. **The `{FADD, FSUB}` eligibility restriction is itself human
   interpretation of stated design** (read off three function bodies
   by inspection, not derived from a table) -- weaker than the
   forced-by-construction dispatch text, stated here rather than
   claimed as forced.
4. Non-c/cpp idioms (go/rust/swift, the 64-row no-graph-coverage
   bucket from `super_ops2.json`) are untouched by this task --
   out of scope by construction (no reader in this region), unchanged.

## files written this lap, all named

- `op_pipeline/build_super_ops3.py` (new; the reachability tie-break
  script, reads `super_ops2.json` + `probe_manifest_c.json` +
  `probe_manifest_cpp.json` + the eleven pinned llvmorg-21.1.8 source
  files via `git show`)
- `op_pipeline/super_ops3.json` (new; 121 broken / 68 still
  ambiguous-or-refused, `super_ops2.json` and `super_ops.json` both
  left untouched)
- this log

No prior-lap artifact (`build_graph2.py`, `build_graph3.py`,
`graph_cpp2.json`, `graph_cpp3.json`, `build_super_ops.py`,
`build_super_ops2.py`, `super_ops.json`, `super_ops2.json`) was
modified.
