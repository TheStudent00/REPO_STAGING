# log 082 — state of the research, and an audit of the parallel language branch

Date: 2026-08-31. Written at the owner's request after the two-axis
table completed. Part 1 is the measured line's state. Part 2 is a
read-only audit of the parallel work extending to the remaining
languages, with findings that need his ruling.

---

# PART 1 — the measured line

## 1.1 What the line set out to answer

Which operators, across languages, are THE SAME operator — decided
by machine evidence rather than by their spelling. The deliverable
is the dominant-operator table, which feeds ur_kind and the ledger
in PCv5.

## 1.2 Current numbers

| quantity | value |
|---|---|
| languages measured | 5 (c, cpp, go, rust, swift) |
| ship units in the corpus | 1,779 |
| units with canonical form | 1,415 |
| classes | 919 |
| operator-nodes | 139 |
| dominant-operator families | 26 |
| nodes with no surviving edge | 23 |
| guard rows | 305 (1,511 units recorded with zero guards) |
| exception families | 34 |

Population note that must travel with every figure: 1,641 is the
0-branch population the table was built over until the branching
lap; 1,779 is the full corpus and the current table's population.
The two were conflated once and the discrepancy is recorded.

## 1.3 What was built, in the order it became necessary

- THE CANONICAL FORM, enforced. Arch opcodes, standardized
  designated registers, one call per line, runnable with its
  standardized context. Text and assembled bytes verified a
  bijection (508 <-> 508, zero violations either way), so the two
  are one thing in two printings.
- THE TRANSFORM-AND-RETURN STEP. A tool may take the canonical
  text elsewhere (lift, simplify) only with a return path; a
  result that cannot return is an intermediate, not a result.
- THE CONTEXT RECORD. The expression travels with operand widths,
  answer width and return convention, entry contract including
  hardware pins, and the temp pool. This was the root fix for four
  separate renderer failures.
- THE GROUND-TRUTH-ANCHORED GATE. Every rendering is proved
  against the unit's OWN real ship code, never against a previous
  rendering. Re-anchoring exposed two real defects immediately.
- THE CROSS-UNIT PROVER. Pairs sharing a class key, expressions
  not identical, proved by z3 (FPA at bit level for floats).
  Float-comparison slice exhausted: 14 proved, ~1,158 disproved,
  ~552 undecided, 96 refused. The high disprove rate is the
  evidence it does not over-merge.
- SEEDED GROUPING UNDER CONDITIONS. Seed = the normal-path graph;
  guarded containment records "contains seed S under condition C";
  two axes, never merged — operator families by seed, exception
  families by guard.
- THE REPRESENTATIVE RULE. Proved-equivalent units take the
  fewest-bytes member as the group's canonical form; raw
  extractions kept.

## 1.4 The three results worth naming

- MODULO IS ONE FAMILY ACROSS FIVE LANGUAGES. go's seed
  (`mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret`) landed in
  the same class as c's whole unit, with its guards carried as
  data.
- GO'S FLOAT EQUALITY JOINED cpp/rust/swift BY PROOF. go's
  `ucomiss`+`sete`/`setnp`+`and` idiom never text-matches the
  others' single `cmpeqss`; the prover showed them equal on all
  inputs.
- THE CROSS-AXIS TABLE ANSWERS THE DESIGN QUESTION AT A GLANCE:

```
D0015 (modulo)
   c      NONE
   cpp    NONE
   go     [EF0003, EF0016]           zero-divide panic-call + int-min inline
   swift  [EF0004, EF0015, EF0022]   zero-divide trap + in1==-1 trap + int-min inline
```

## 1.5 Named remainders in the measured line

- 34 c/cpp branching units whose seeds are unresolved (their
  guards are overflow/NaN shapes, not divide guards).
- rust's 2 resolved seeds matched no class (rendering not yet
  converged with c/cpp).
- 6,401 cross-language non-float prover pairs never budgeted.
- The super-op candidate list, ranked and unactioned: 305 of 364
  unconverged units carry one of 17 unmodelled lifter names; the
  top candidate blocks 44 units.

---

# PART 2 — the parallel branch, audited read-only

## 2.1 Where it lives

There is no separate directory. The work sits inside
`PRIVATE/PseudoCoupHQ/Research/op_pipeline` alongside the
five-language line, plus raw output in
`PUBLIC/Airlock/agent/out/`, plus new empty planning nodes.

- Written pilots: `interp_cpython.{md,json}` and
  `interp_jvm.{md,json}`, both 2026-08-26, each with pins,
  evidence classes, an explicit "what was NOT done", and a
  recorded guard pass.
- Join machinery: `add_java.py/json`, `jvm_canon.py/json`,
  `dom_ops_java.py`, `core_modes_java.json`.
- A later retrofit, 2026-08-30: `interp_feeder.py`,
  `run_java_pipeline.sh`, `op_units_{java,cpython}.json`,
  `sem_anchored_spill_{java,cpython}.json`.
- Un-folded runs from 2026-08-31 in Airlock only: ruby and php.

## 2.2 What has actually been run

| language | probes | middle form | handler / arch-unit | in HQ artifacts |
|---|---|---|---|---|
| java | 2 | javap bytecode | yes, 104 bytes, canonicalised | yes, but dropped from current tables |
| cpython | 4 | BINARY_OP_ADD_INT | 7 handler slices | 1 unit reaches tree_units2, dropped after |
| ruby | 4 | opt_plus captured | none | nothing in HQ |
| php | 3 | none captured | none | nothing in HQ |
| kotlin, csharp, v8, dart | 0 | — | — | — |

The two pilots are good work: the JVM warm-up recipe is measured
(at least 7000 calls, tiering off, dontinline) and it records a
disagreement with the VM's own reported threshold rather than
smoothing it; the CPython pilot names its gaps plainly ("No diary.
Order is unmeasured.").

## 2.3 SIX FINDINGS THAT NEED DEE

- FINDING 1 — JAVA HAS SILENTLY FALLEN OUT OF THE TABLES.
  `dominant_table9.json` still holds `java/op_1` in a class whose
  languages read `["c","cpp","go","java","rust","swift"]`. Every
  table built since 2026-08-29 has `java=0`. Cause: every
  downstream stage hardcodes `LANGS = ["c","cpp","go","rust",
  "swift"]`. PROGRESS still claims "JAVA ENTERED THE TABLE" —
  true on 2026-08-26, false today.
- FINDING 2 — THE CPYTHON UNIT'S TYPE KEY IS FABRICATED.
  `interp_feeder.py` hardcodes `"lhs_rep": "i32"` for `long_add`,
  whose real signature takes two PyLongObject POINTERS. Its own
  lifted expression shows the pointer dereferences
  (`ld64/g0(Add64(16:64,in0:64))`) while its type key reads
  `i32,i32`. A pointer-taking handler is sitting in the integer
  class key. This is exactly the kind of unratified equation the
  int32_t ruling exists to forbid.
- FINDING 3 — THE RETROFIT RAN INTO A SUPERSEDED BRANCH.
  `run_java_pipeline.sh` ends at `tree_match2.py`. The adopted
  selection is `tree_match3` (ret-block-first), and
  `tree_units3.json` was written BEFORE the two extra languages
  were added. The java/cpython work has never been run under the
  adopted pipeline.
- FINDING 4 — THE ONE MEASURED DEOPT GUARD NEVER REACHED THE
  EXCEPTION AXIS. `interp_jvm.md` records a
  `deopt-continue-elsewhere` response, forced by construction.
  `core_modes_java.json` holds one unit with empty modes, so
  `guards2.json` carries zero java guard rows. The 34 exception
  families were built without the only non-C-family deopt
  evidence in the corpus.
- FINDING 5 — RUBY AND PHP ARE MEASURED AND ORPHANED. Real gcov
  deltas exist from today (ruby: 1,050 lines with positive delta
  across 27 files; php: 344 across 9). No fold script, no HQ
  artifact, no guard run, no PROGRESS entry, no log. The php pin
  is a compromise forced by build failures — 7.4.33 after 8.3.0
  and 8.2.13 both failed — and that choice is recorded only
  inside a lane script.
- FINDING 6 — THE NEW PLANNING NODES ARE AUTO-DERIVED, NOT
  AUTHORED. `node_0_3_6_interp_feeder`'s eight sub-nodes are the
  function and variable names inside `interp_feeder.py`
  (`feeder_config`, `parse_interp`, `format_canon`,
  `invoke_normalizer`, `run_pipeline`, `run_jvm`, `target`,
  `output`) promoted to planning nodes with definitions like
  "Formatting logic". Nine PROGRESS files say only "Initialized."
  Neither new node is referenced by SUPPORT_scaling_design.md,
  which still describes the road as living in node_0_3_5.

## 2.4 What is NOT wrong with it

- The canonical form matched: java's canonical text
  `lea (%rdi,%rsi,1),%eax; ret` is byte-identical to c/op_102's,
  and its normalized expression is character-identical too. Java
  would still match today if it were carried through.
- Provenance was marked honestly: `add_java.json` carries
  `"provenance_is_weaker": true` with an instruction that it be
  marked wherever the unit appears.
- The spelling ban was restated verbatim and the guard was run
  and recorded passing on both pilots.

## 2.5 The choice this puts to the owner

The parallel branch is not a competing line — it uses the same
canonical form, the same guard, the same solver stack, and it
marks its own weaker provenance. What it lacks is CONNECTION: the
five-language line moved fast for two days and left it behind at
three specific joints (the LANGS lists, the tree_match3 adoption,
the guards sweep).

Two shapes for the next move, stated without preference:

- RECONNECT FIRST: fix the three joints, re-run java and cpython
  under the adopted pipeline, fix the cpython type key by machine
  fact rather than assertion, fold ruby and php into HQ artifacts
  with their pins and evidence classes. Outcome: one table, seven
  languages, provenance marked.
- ADVANCE FIRST: continue the five-language line's remainders
  (super-op candidates, the 34 c/cpp branching seeds, the
  unbudgeted prover pairs) and reconnect once the method stops
  moving. Outcome: a stable method, then one reconnection instead
  of repeated ones.

The audit's own reading, offered as a lean and not a decision: the
three joints are small and mechanical, while the cpython type key
is a correctness defect that will silently corrupt a class if the
branch is reconnected without fixing it first.
