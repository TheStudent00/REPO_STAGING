---
id: hq.research.compiler_graph.gate.verdict
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: verdict
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_0_verdict/CORE_0_3_1_5_0_verdict.md
super_node:
    name: gate
    path: ../CORE_0_3_1_5_gate.md
sub_nodes:
    - name: outcome
      designation: code (attribute)
      realize: false
    - name: reason
      designation: code (attribute)
      realize: false
    - name: counterexample
      designation: code (attribute)
      realize: false
    - name: route
      designation: code (attribute)
      realize: false
    - name: solver_timeout_ms
      designation: code (attribute)
      realize: false
---

# CORE 0_3_1_5_0 — verdict

## metadata

- **id:** hq.research.compiler_graph.gate.verdict
- **level:** 4
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [gate](../CORE_0_3_1_5_gate.md)

## sub_nodes

- outcome — code (attribute) *(realize: false)*
- reason — code (attribute) *(realize: false)*
- counterexample — code (attribute) *(realize: false)*
- route — code (attribute) *(realize: false)*
- solver_timeout_ms — code (attribute) *(realize: false)*

## definition

What a gate returns about one unit: an outcome, the reason for it, the
solver's counterexample when there is one, which route produced it, and
the solver time limit that was in force. The five outcomes are
PROVED_ON_SHIP (the solver showed equality against the unit's own ship
code), PROVED_BY_CONSTRUCTION (the form applies no transformation, so
the structural checks carry it), DISPROVED (the solver found a value
where the two differ), UNDECIDED (the solver could not answer, or the
reference has no model for something the body spells), and REFUSED (the
unit could not be put into canonical form at all). A solver timeout is
UNDECIDED and never DISPROVED.

## design

```
class Verdict
	attributes:
		outcome
			"""
			PROVED_ON_SHIP /
			PROVED_BY_CONSTRUCTION / DISPROVED /
			UNDECIDED / REFUSED
			"""
		reason
			"""
			plain words: which obligation was
			discharged, or what stopped it
			"""
		counterexample
			"""
			the z3 model, when DISPROVED: the
			seed values at which the two answers
			differ
			"""
		route
			"""
			which obligation produced this
			verdict — wrapped text, term against
			ship, or term against text
			"""
		solver_timeout_ms
			"""
			the limit in force, 3,000 ms today,
			recorded so an UNDECIDED can be
			re-read later
			"""
```

## settled rules

- **A solver timeout is UNDECIDED, never DISPROVED**, and the timeout
  is recorded on the verdict. Decision: log_147 §13.5.
- **Proved-is-counted.** A unit the gate proved is a counted unit; a
  unit it did not is not, whatever its text looks like. Decision:
  AgentMemory "PROVED UNIT IS A COUNTED UNIT".
- **Two routes never contradict.** A unit proved on one route and
  disproved on the other is a defect to be found, not a tie to be
  broken. Decision: log_147 §1.2.
- **A DISPROVED verdict carries the solver's own counterexample**,
  quoted rather than summarized. Decision: log_153 §5.3.
- **UNDECIDED is a statement about the reference, not about the
  unit.** 5,602 of today's UNDECIDED verdicts are the missing stack
  and x87 model. Decision: log_153 §4.3.

## realization (what exists on disk, 2026-09-03)

Home: `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| verdicts on wrapped texts | `canon37_gate.py`, `canon38_gate.py` — 30,436 proved (17,379 PROVED_EQUAL, 1,168 ON_SHIP, 11,889 BY_CONSTRUCTION) | done |
| verdicts on terms | `gate48.py` — 23,132 proved / 415 disproved / 5,602 undecided / 1,287 no term | done (log_153) |
| verdicts on the text walk | `textwalk48.py` — 0 disproofs | done |
| the 415 disproofs | the reference's wrong remainder | **re-gated** (task 91): **415 of 415 prove**, 0 disprove, 0 stay undecided. `t91_audit_printed.txt` |
| the 5,602 undecided | the missing STACK and X87 model | **re-gated** (task 91): **2,356 prove**, 2,969 disprove, 277 stay undecided. The 2,969 are the ledger's own gap, not the reference's: canon38 holds no row for a transfer into the compiler's runtime, so the term asserts the transfer changed nothing while the reference now walks the callee's body. `t91_audit_printed.txt` |
| the wall clock on a verdict | `gate.SOLVER_MILLISECONDS`, 3,000 ms | **measured** (task 91): running the SAME code twice moves 17 of 30,436 verdicts (0.06%) with the callees attached and 8 of 30,436 (0.03%) without, every one of them between UNDECIDED and DISPROVED at the solver's own margin. `t91_audit_printed.txt`, "THE WALL-CLOCK CONTROL" |
