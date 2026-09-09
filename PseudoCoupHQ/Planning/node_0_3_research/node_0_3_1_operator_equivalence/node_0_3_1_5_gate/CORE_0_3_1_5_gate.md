---
id: hq.research.compiler_graph.gate
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class), rule
node:
    name: gate
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/CORE_0_3_1_5_gate.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: verdict
      path: node_0_3_1_5_0_verdict/CORE_0_3_1_5_0_verdict.md
    - name: prove_wrapped
      designation: code (method)
      realize: false
    - name: prove_term_against_ship
      designation: code (method)
      realize: false
    - name: prove_term_against_text
      designation: code (method)
      realize: false
    - name: structural_checks
      path: node_0_3_1_5_4_structural_checks/CORE_0_3_1_5_4_structural_checks.md
    - name: zero_regression
      path: node_0_3_1_5_5_zero_regression/CORE_0_3_1_5_5_zero_regression.md
    - name: lean
      path: node_0_3_1_5_6_lean/CORE_0_3_1_5_6_lean.md
---

# CORE 0_3_1_5 — gate

## metadata

- **id:** hq.research.compiler_graph.gate
- **level:** 3
- **status:** draft
- **designation:** code (class), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- [verdict](node_0_3_1_5_0_verdict/CORE_0_3_1_5_0_verdict.md) — What a gate returns about one unit: an outcome, the reason for it, the solver's counterexample when there is one, which route produced it, and the solver time limit that was in force.
- prove_wrapped — code (method) *(realize: false)*
- prove_term_against_ship — code (method) *(realize: false)*
- prove_term_against_text — code (method) *(realize: false)*
- [structural_checks](node_0_3_1_5_4_structural_checks/CORE_0_3_1_5_4_structural_checks.md) — The six mechanical checks that carry a unit when the solver cannot — used only where the reference has no model for a mnemonic the body spells.
- [zero_regression](node_0_3_1_5_5_zero_regression/CORE_0_3_1_5_5_zero_regression.md) — The before-and-after check run over a whole population after any change: every unit that was PROVED before must still be PROVED, or its loss must carry a named cause that was checked mechanically rather than asserted.
- [lean](node_0_3_1_5_6_lean/CORE_0_3_1_5_6_lean.md) — The operator-mapping proof system: the complete mapping model of every arch opcode (level 0, DERIVED from the reference simulator by a translator, never written twice), the term algebra over it, the equivalence proofs between terms, and the translation to each target language with its preservation theorem — held in Lean 4, whose kernel checks every proof — with z3 kept in the gate as the per-instance check on the unverified compiler's output.

## definition

The proof obligations and the object that discharges them. Nothing in
this research is counted unless it passed a gate: a wrapped text is
counted when it provably computes what the unit's own ship code
computes, for every value of every input row; a term is counted when
it provably equals the reference's answer for that same body, and
independently when a walk of the body in text order rebuilds it.
Every verdict is one of PROVED / DISPROVED / UNDECIDED / REFUSED with
its reason, and a lost proof must carry a named, proved cause.

## design

```
class Gate
	methods:
		prove_wrapped
			"""
			(wrapped_text, unit) -> Verdict.
			OUT-0 of the wrapped text == the
			reference's answer for the unit's
			own ship body, inputs bound row-i <->
			arrival-register-i. Falls to
			structural_checks only when the
			reference has no model for a
			mnemonic the body spells
			"""
		prove_term_against_ship
			"""
			(term, unit) -> Verdict. Route one:
			term == Reference.answer_of(unit)
			"""
		prove_term_against_text
			"""
			(term, unit) -> Verdict. Route two:
			term == the body walked in text order
			with the same opcode_table; evidence
			about the LEDGER'S WIRING, not the
			meanings
			"""
		structural_checks
			"""
			sub-node: C1..C6 — body verbatim and
			in order; prelude writes only arrival
			registers; epilogue before every ret;
			no body line names the ledger; the
			epilogue's pointer is not the result
			register; the label rewrite touched
			only targets
			"""
		zero_regression
			"""
			sub-node: before/after over a
			population; every lost proof carries
			a mechanically checked cause
			"""


class Verdict
	attributes:
		outcome
			"""
			PROVED_ON_SHIP / PROVED_BY_CONSTRUCTION
			/ DISPROVED / UNDECIDED / REFUSED
			"""
		reason
		counterexample
			"""
			the z3 model, when DISPROVED
			"""
		route
		solver_timeout_ms
```

## settled rules

- **Prove against the unit's OWN ship code**, never against another
  unit and never against a rendering. Decision: AgentMemory
  "ground-truth-anchored gate" (round 3).
- **Proved-is-counted.** A unit the gate proved is a counted unit;
  a unit it did not is not, whatever its text looks like. Decision:
  AgentMemory "PROVED UNIT IS A COUNTED UNIT".
- **Zero regressions in the ruled sense**: no unit loses PROVED
  without a named, proved cause; text change is not regression.
  Decision: log_129 header (round 8).
- **Two routes never contradict**: a unit proved on one and
  disproved on the other is a defect to be found, not a tie to be
  broken. Decision: log_147 §1.2 consistency line.
- **A solver timeout is UNDECIDED**, never DISPROVED, and the
  timeout is recorded on the verdict (3,000 ms today). Decision:
  log_147 §13.5.
- **The reference is [reference](../node_0_3_1_4_reference/CORE_0_3_1_4_reference.md)**;
  the gate carries no simulator of its own. Decision: this CORE,
  2026-09-03.

## realization (what exists on disk, 2026-09-03)

| part | current file | status |
|---|---|---|
| prove_wrapped, structural_checks | `canon37_gate.py` (Sim47, C1–C5), `canon38_gate.py` (+C6) | done: 30,436 proved (17,379 PROVED_EQUAL, 1,168 ON_SHIP, 11,889 BY_CONSTRUCTION) |
| prove_term_against_ship | `gate48.py` → `canon10` Sim10 | in use; carries the reference's defects (wrong remainder, no stack/x87, floats uninterpreted) |
| prove_term_against_text | `textwalk48.py` | done; 0 disproofs after the fallback removal (log_153 §4.2) |
| zero_regression | `canon37_zero_regression.py`, `canon38_zero_regression.py`, `zero_regression48/49/53.py` | done per round; one module planned |
| verdicts today | terms: 23,132 proved / 415 disproved / 5,602 undecided / 1,287 no term (log_153) | the 415 are the reference's remainder; the 5,602 are the missing stack/x87 model |

Next lap: `gate.py` importing `reference.py`; the 415 re-gated; the
5,602 re-gated once the reference models STACK and X87.
