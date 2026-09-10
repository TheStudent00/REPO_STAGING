# log 158 — task briefs for Claude Code, round 12

Date: 2026-09-03. Point a Claude Code session here. OPUS IS THE
DEFAULT SUB-AGENT. ONE AIRLOCK INSTANCE PER TASK.

## THIS ROUND IS THE FIRST RUN UNDER THE PLAN TREE

the owner, 2026-09-03: "plan out every fucking step … we have completely
drifted away from the use of PlanPlan." The tree now exists:

`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/`

nine level-3 nodes (probes, arch_unit, canonical_form, ledger,
reference, gate, term, pool, guard) and 31 level-4 nodes. EVERY task
below is a node whose PROGRESS.md says **planned**. Read the node's
CORE (definition, design, settled rules, realization) before writing
a line of code. The rules that bind this round:

1. **Code carries the node's name.** The deliverable of a node named
   `reference` is `reference.py` with a class `Reference`; its
   methods are the node's `methods:`; its sub-nodes are its
   attributes / methods / inner classes as the CORE's `## design`
   says. `canon*`, `gate48`, `layer4*`, `build_the_pool*` are
   superseded records and are not edited.
2. **A shape the tree lacks is added to the tree first.** If you find
   the CORE wrong, STOP, write the correction into the CORE with
   provenance (PROTOCOL §2), record it in the node's PROGRESS, then
   code. Never code a shape the tree does not state.
3. **No question reaches the owner that a CORE or AgentMemory already
   answers.** Check both before flagging anything. Flag only ontology
   or naming.
4. **Update the node's PROGRESS.md at the moment progress happens**,
   with the evidence link. The completion log is the narrative; the
   PROGRESS entry is the record.
5. Everything from log_151's standing requirements: spelling ban
   pasted verbatim into every sub-agent brief; unmodified guard, one
   process, `grep -c exempt` = 0; prove against the unit's own ship
   code; zero regressions in the ruled sense; §5.1a labels; Appendix
   B shape; every number with its population.

STATE AT HANDOFF (log_157, verified): canon38 30,436 proved / 642
refused; terms 23,132 proved / 415 withdrawn (reference's remainder)
/ 5,602 undecided (no stack/x87 reference) / 1,287 no term; pool3
2,247 entries / 632 multi-language; census4 54 producers.

---

## TASK 57 — `reference.py` (node 0_3_5_4 reference; Opus; centerpiece)

CORE: `node_0_3_5_4_reference/CORE_0_3_5_4_reference.md` and its two
sub-nodes `opcode_table`, `machine_state`.

WORK: one class `Reference` with `simulate`, `answer_of`; one
`MachineState` with registers / flags / memory / stack / x87; ONE
`opcode_table` (mnemonic -> reads, writes, term builder) built by
folding in `vex_names.py`'s lane builders, `condition_table.py`'s
condition route, `layer4.py`'s producer table, and `canon12`'s
division (`SRem`/`URem`). Acceptance instances, printed with values:
(a) `c/op_246` (`idiv` remainder) — answer term uses `SRem`;
`7, -3` gives `1`; (b) a push/pop unit (`c/regen_11491`) — the stack
round-trips; (c) an x87 compare unit (`cpp/regen_36796`) — both
loads reach the compare. Then: `canon9/10/12_behaviour_check.py`
marked superseded in their headers (one comment line each, nothing
else edited). PROGRESS entries on `reference`, `opcode_table`,
`machine_state`.

## TASK 58 — `gate.py` (node 0_3_5_5 gate; Opus; after 57)

CORE: `node_0_3_5_5_gate/` and sub-nodes `verdict`,
`structural_checks`, `zero_regression`.

WORK: `Gate` with `prove_wrapped`, `prove_term_against_ship`
(imports `Reference`), `prove_term_against_text`,
`structural_checks` (C1–C6), `zero_regression`; `Verdict` per the
CORE. Re-gate ALL 30,436 canon38 terms. EXPECTATION TO TEST: the 415
remainder withdrawals prove; a large part of the 5,602 undecided
decide. Report proved / disproved / undecided / no-term per
population against 23,132 / 415 / 5,602 / 1,287, every movement with
its cause; consistency line = 0. PROGRESS on all four nodes.

## TASK 59 — ledger repairs (node 0_3_5_3 ledger; Opus; parallel with 57)

CORE: `node_0_3_5_3_ledger/` sub-nodes `flag_rules`,
`destination_rules`, `producer`; and
`node_0_3_5_1_arch_unit/node_0_3_5_1_8_runtime_callee/`.

WORK: (a) `sbb`/`adc` as flag SETTERS (699 units, log_153 §4.2) in
the flag-setter table; (b) `runtime_callee`: locate libgcc /
compiler-rt archives on this machine per toolchain (`gcc
-print-libgcc-file-name`, clang's `libclang_rt.builtins-x86_64.a`,
rustc's bundled compiler-builtins, swift's), extract `__divti3`,
`__udivti3`, `__modti3`, `__umodti3` bodies with `ar x` + `objdump
-d`, attach each as an ArchUnit the caller references, and give the
caller's answer row the producer `{"kind": "runtime_callee",
"callee": "__divti3"}` — 308 units listed in
`out_of_scope_library_calls.json` (its verdict superseded; its list
stands); (c) the module is `ledger.py` carrying `Ledger`, `Row`,
`Producer`, `DESTINATION_RULES`, `FLAG_RULES`, importing nothing from
`ledger47/48` (copy what is unchanged, with a header line saying
so). Re-walk all 31,078 units -> `canon39_*` artifacts written by
`canonical_form.py` (task 60) — coordinate: task 59 delivers
`ledger.py`, task 60 consumes it. PROGRESS on the four nodes.

## TASK 60 — `canonical_form.py` (node 0_3_5_2; Opus; after 59)

CORE: `node_0_3_5_2_canonical_form/` and sub-nodes `prelude`,
`epilogue`, `labels`, `refuse`.

WORK: `CanonicalForm` with `wrap`, `assemble`, `refuse`, using
`ledger.Ledger`; the prelude emits IN rows in `arrival_contract`
ORDER (the vector-first defect of log_153 §9 — count the affected
units first, print `c/op_105` before and after). Render all 31,078
-> `canon39_*`; gate with task 58's `gate.py`; zero regressions vs
canon38 with named causes; assemble 2,728 sample; unmodified guard
over every file. PROGRESS on the five nodes.

## TASK 61 — `term.py` and `pool.py` (nodes 0_3_5_6, 0_3_5_7; Opus; after 60)

WORK: `Term` (`transcribe`, `normalize`, `census`; `render_back`
stays planned and is NOT attempted) reading `Reference.opcode_table`
— no second meanings table; `name_census5.json`. `Pool` (`merge` on
the three grounds, `compare`, `representative`, `families`,
`exception_families` REBUILT over the new pool — the round-5
`exception_families2.json` is superseded) -> `the_pool4.json`,
`the_families4.json`, `exception_families3.json`. Delta vs pool3
with computed causes; E00029's successor printed. PROGRESS on all
term and pool nodes.

## TASK 62 — bank round 12 (smaller model acceptable)

WORK: verification transcripts; the one-page state in Appendix B
shape; authoritative count line over pool4; `python3
PRIVATE/PlanPlan/framework/check_plans.py
PRIVATE/PseudoCoupHQ/Planning` pasted (non-dangling lines);
dashboards regenerated; posterity message with `wc -c`.

---

Order: 57 and 59 in parallel; 58 after 57; 60 after 59 (and 58 for
its gate); 61 after 60; 62 last.

NOT IN THIS ROUND (planned in the tree, deliberately deferred): one
`emit` module for probes; the swift re-run; `render_back`. No open
calls for the owner.
