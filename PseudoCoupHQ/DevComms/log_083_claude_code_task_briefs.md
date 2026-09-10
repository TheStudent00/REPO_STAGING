# log 083 — task briefs for Claude Code sessions

Date: 2026-08-31. Written for handoff: the owner will point a Claude
Code session at this file. Each task is self-contained: context
files to read first, the work, acceptance criteria, and standing
requirements. Tasks are ordered by value; they are independent
unless a dependency is named.

## STANDING REQUIREMENTS — every task, every sub-agent

- Read FIRST, in full: `PRIVATE/PseudoCoupHQ/AgentMemory.md`
  (all rulings; especially THE CANONICAL FORM IS ENFORCED,
  CANONICALIZATION INCLUDES THE TRANSFORM-AND-RETURN STEP,
  SEEDED GROUPING UNDER CONDITIONS, THE REPRESENTATIVE RULE,
  TEMP REGISTERS ARE STANDARDIZED NOT LIMITED, FIX A CAUSE AT
  FIRST OBSERVATION, THE SPELLING BAN, the evidence doctrine)
  and `PRIVATE/DevComms/LLM_communication_protocol_v2.md`.
- PASTE THE SPELLING BAN VERBATIM into every sub-agent brief
  (AgentMemory requires this; the paragraph is in AgentMemory
  under "THE SPELLING BAN, ABSOLUTE").
- Every artifact that groups or pairs units runs
  `op_pipeline/check_no_spelling_keys.py`; matching-shaped files
  must pass WITHOUT the provenance exemption.
- Every new rendering is proved by the ground-truth-anchored gate
  against the unit's OWN real ship code (never a prior
  rendering). Zero regressions verified programmatically: every
  previously-converged unit keeps byte-identical newest text.
- New files only; defective artifacts stay on disk as records.
- Update the node PROGRESS
  (`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md`)
  with a dated entry per completed task: what changed, measured
  before/after, honest remainders. One `# PROGRESS` heading only.
- Evidence class stated on every claim. Refuse honestly rather
  than fabricate; a diagnosed dead-end is a valid result.
- Working directory for pipeline tasks:
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline`.
- Current state: 1,457 of 1,779 units converged; table
  926/135/26/23 on the dominant_table23 lineage (also see the
  919/139/26/23 full-population lineage of dominant_table22 —
  the two lineages differ in method and must not be conflated;
  reconciling them is Task 7).

---

## TASK 1 — generalize the compiler-graph builder (tree-sitter,
## language-dispatched), cpp first

CONTEXT: `Research/compiler_graph/build_graph.py` (Go-hardcoded;
lap one built 86 files -> 182,935 nodes, 0 parse errors),
`resolve_dots.py`/`resolve_dots2.py`/`fix_bindings.py` (dot
resolution work), `query_path.py`,
`probe_uint64_to_float/` (the successful bounded probe: purpose-
built cpp graph over 6 files; its build_graph_cpp_probe.py is a
starting point), the node CORE's standing rules (graph not prose;
language-agnostic by construction: extension -> grammar
dispatch), and PCv5's language-pack shape
(`PRIVATE/PseudoCoup_v5/Tools/ledgerer/ts_to_ur.py` —
LanguagePack: per-language DATA, one universal mapper; reuse the
design, not necessarily the code).

WORK: refactor build_graph.py into a dispatched builder:
extension -> tree-sitter grammar (go, c, cpp available; tree-
sitter-cpp confirmed installing cleanly), assembly and data-table
files to their readers per the CORE. Node/edge vocabulary
unchanged from lap one (defined-in vs does). Then build the graph
over the LLVM region that matters: SelectionDAG legalization +
X86 ISel lowering (the probe's six files plus their direct
includes/callees, expanding outward as budget allows). PIN
DISCIPLINE: extract sources at tag llvmorg-21.1.8 by `git show`
from `Sources/llvm-project` (the working tree is at
llvmorg-24-init — do NOT read it directly; the probe caught this).
Record pins in the artifact.

ACCEPTANCE: (a) the probe's two queries reproduce from the
general builder (unsigned-64-to-float lands in
ExpandLegalINT_TO_FP with its 11 emits; signed-32-to-float lands
in the CVTSI2SS TableGen row via the data-table reader); (b) a
query for a SECOND super-op candidate from
`op_pipeline/idiom_candidates.json` locates its emitting function
(or a named frontier); (c) graph JSON passes the spelling guard.

## TASK 2 — the irregular blocking names: 219 + 19 units

CONTEXT: `op_pipeline/name_census.json` (the actionable ranking),
`vex_names.py` (the generic translator + dictionary dispatch),
`condition_table4/8/9.py` (the canonical-context route for
amd64g_calculate_condition — 219 remaining units are the ones
these tables do NOT yet cover; survey which shapes),
`canon24*.py` (newest driver/gate lineage).

WORK: (a) survey the 219 amd64g_calculate_condition units by
flag-setter and condition read — extend the condition tables for
the uncovered shapes (the canonical-context route: read the
condition off the canonical text, value-based pairing, never
positional); (b) amd64g_calculate_rflags_c (19 units): model the
carry-flag reconstruction for the shapes present (survey first);
(c) Mul32/Mul64/DivModS128to64/DivModU128to64 stragglers (a few
units) via the existing widening machinery (canon12_normalize
precedent). Run through render + gate; rebuild
tree_units/clusters; report converged delta from 1,457.

## TASK 3 — the 34 c/cpp branching seeds (overflow/NaN guard
## shapes)

CONTEXT: `seeds1.json` (34 unresolved, reasons recorded
per-unit), `seed_extract1.py` (the resolver: exact-text lookup;
c/cpp units got 0 or 2+ matches), `guards2.json`,
`core_modes_c/cpp.json`, the branching-canonicalization PROGRESS
entry (2026-08-29).

WORK: c/cpp's branching units guard conversions (float-to-int
boundary checks) and the u64->float halving idiom — their
non-trapping alternate paths are not table members, so exact-text
lookup failed. Extend the resolver: (a) when both paths compute
(no trap), the seed is the path whose text (or proved-equal
class) matches a straight-line unit; if NEITHER matches, try the
cross-unit prover (cross_unit_prover.py machinery) between path
text and candidate class representatives — a proved edge resolves
the seed; (b) the halving idiom's units: the idiom is now a named
super-op (Task 1's graph names its extent); the seed is the
operator instruction (addss/subss/...) and the idiom is CONTEXT
(the conversion), not guard and not seed — record it as a third
component kind if needed and FLAG THE DESIGN CHOICE for the owner
rather than silently inventing ontology. Update
dominant_table/dom_ops; report family changes.

## TASK 4 — the unbudgeted prover bucket: 6,401 cross-language
## non-float pairs

CONTEXT: `cross_unit_prover.py`, `cross_unit_prover_extend.py`,
`proved_edges.json`/`proved_edges2.json` (float-comparison slice:
14 proved; widened sweep: 0 new proofs in 5,285 pairs — the
disprove rate is the credibility), the sandbox's ~170s
per-command cap (chunk and checkpoint; the extend script already
does).

WORK: sweep the 6,401 remaining cross-language pairs, chunked,
checkpointed, transitivity shortcut on. Expect mostly disproofs;
every proof is durable. Rebuild representatives/table/dom_ops
only if proofs land. Report tallies per chunk.

## TASK 5 — reconnect the parallel language branch (java,
## cpython, ruby, php)

CONTEXT: `PRIVATE/PseudoCoupHQ/DevComms/log_082_state_of_research_and_parallel_branch.md`
PART 2 — six findings, read all. The three joints and the
correctness defect, in order:

WORK: (a) FIX THE CPYTHON TYPE KEY FIRST (finding 2): the feeder
hardcodes i32,i32 for long_add, which takes two PyLongObject
POINTERS — key it by machine fact (pointer width/encoding from
the unit's own lifted expression or DWARF), never by assertion;
if the honest key makes it incomparable to integer classes, that
is the correct outcome. (b) LANGS lists (finding 1): the
downstream stages hardcode five languages — parameterize (one
LANGS source of truth), re-run java+cpython through the ADOPTED
pipeline (tree_match3 selection, current normalizer — finding 3).
(c) java's deopt guard (finding 4): carry interp_jvm.md's
measured deopt-continue-elsewhere row into guards2/exception
families with its weaker-provenance mark. (d) fold ruby and php
(finding 5): write fold_interp_ruby.py / fold_interp_php.py in
the pilots' own .md+.json format from the Airlock outputs
(`PUBLIC/Airlock/agent/out/interp_ruby_b/`,
`interp_php_b/`), recording pins (ruby 3.3.0; php 7.4.33 — a
compromise pin after 8.3/8.2 build failures, record that), guard
runs, and what was NOT done. (e) the auto-derived planning nodes
(finding 6): do NOT edit Planning — list them in the report for
the owner to rule on (planning is his).

## TASK 6 — join the graph to the miner (super-op provenance)

DEPENDS ON: Task 1.
CONTEXT: `op_pipeline/idiom_candidates.json` (idioms with the
within-form vs co-occurrence split), Task 1's graph.

WORK: for each idiom candidate with support >= 4: query the
graph for its emitting function (the probe's method). Output
`super_ops.json`: idiom -> {emitting function, stage
(selection/legalization/runtime-library), extent (the function's
emit list), carrier units}. This converts recurrence-mined
candidates into provenance-named super-ops. Idioms whose emitter
is not found get a named frontier. Spelling guard applies.

## TASK 7 — reconcile the two table lineages

CONTEXT: dominant_table22/dom_ops20 (full 1,779 population,
seed-joined branching units, representative rule NOT applied) vs
dominant_table23/dom_ops21 (0-branch method rebuilt with canon24,
representative lineage diverged at representatives5 which
predates canon24). The PROGRESS entries of 2026-08-29..31 record
the divergence.

WORK: one builder, one lineage: full population, seed texts for
branching units, representative rule with the corrected ground
(b) (raw expressions, constant values carried, bare placeholders
refused), machine-fact result types, canon24-newest text
fall-through, proved edges as ground (c). Output
dominant_table24/dom_ops22 as THE table. Verify: modulo family
spans c/cpp/go/swift; float comparisons include go via proved
edges; bitwise families span all five; no family loses members
vs either parent lineage without a named cause. State the
population on the artifact.

---

Order recommendation: 2 and 4 are budget-friendly and
independent; 1 unlocks 6; 5 is self-contained; 3 benefits from
1+6 but can start; 7 last, once 2/3/5 have stopped moving the
inputs.
