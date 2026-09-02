---
id: pcv6.tools.t2_ledger
level: 2
status: settled
settled_by: the owner
supersedes: null
decision: ../../../AgentMemory/02_decisions.md
---

# CORE 0_0_1 — T2: Ledger

An independent tool (PseudoCoup is a module of tools; centralized
control comes later when ontology reveals itself). The per-program
record across **three axes** — semantic (drives emission),
structural (verifies shape/wiring), runtime (observations from
executing the output) — one record per source node, everything
joined by one id.

Settled design (the owner-aligned 2026-07-28): ONE record schema, not
joined ledgers; the ledger id is a **runtime-observable signal**
emitted into every transpiled side; ingest records `unresolvable`
honestly, consumers halt on it; minimal core ships first, slots
grow additively. Composition sources and evidence:
[ledger survey](../../../../PseudoCoup_v5/DevComms/ledger_survey_2026-07-27.md),
[R4 runtime survey](../../../Research/r4_runtime_ledger_survey/REPORT.md).

Acceptance (tool-level): `--check` invariants on a pinned corpus;
dump/load byte-fidelity; consumer-halt refusal test; id-emission
test (emitted output carries the ledger id, recoverable by a
runtime probe).

## Nodes

- [node_0_0_1_0_schema](node_0_0_1_0_schema/CORE_0_0_1_0_schema.md)
  — the record: fields, slots, serialization, unresolvable
  markers.
- [node_0_0_1_1_keying](node_0_0_1_1_keying/CORE_0_0_1_1_keying.md)
  — identity: call-site id + instance key, the emission contract,
  secondary indexes.
- [node_0_0_1_2_integrity](node_0_0_1_2_integrity/CORE_0_0_1_2_integrity.md)
  — the check harness: invariants, refusal semantics, growth
  gates.
- [node_0_0_1_3_growth](node_0_0_1_3_growth/CORE_0_0_1_3_growth.md)
  — the deepening: later slots (semantic/connectivity/ui/
  divergence/runtime) under the growth gate, and the
  assembler-scale storage decision. *(planning added 2026-07-29)*
