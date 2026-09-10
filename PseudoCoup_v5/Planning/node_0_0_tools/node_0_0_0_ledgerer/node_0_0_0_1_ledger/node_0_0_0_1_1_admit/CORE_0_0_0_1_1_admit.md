---
id: pcv5.tools.ledgerer.ledger.admit
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (function), rule
node:
    name: admit
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_1_ledger/node_0_0_0_1_1_admit/CORE_0_0_0_1_1_admit.md
super_node:
    name: ledger
    path: ../CORE_0_0_0_1_ledger.md
sub_nodes: []
---

# CORE 0_0_0_1_1 — admit

## metadata

- **id:** pcv5.tools.ledgerer.ledger.admit
- **level:** 4
- **status:** draft
- **designation:** code (function), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledger](../CORE_0_0_0_1_ledger.md)

## sub_nodes

*(none yet)*

## definition

`admit(table, node)` — the gate. the one write path into a ledger,
and the mechanical home of the refusal doctrine. dual designation on
purpose: the function is small; the RULES it enforces are the point.

## rules

- **append-only.** admission never rewrites or removes an entry; a
  fallen position keeps its record (supersedes is a connector, not
  an edit).
- **`unresolvable` is a value, never an omission.** an ingestor that
  cannot type a declaration writes the explicit marker; admit
  refuses a record that leaves the slot silently empty. consumers
  halt on the marker knowingly.
- **phase slots are refused before their writer exists.** a record
  claiming a slot its phase does not define is refused by name (the
  R1 refusal pattern) — being loud beats being permissive.
- **admission order is the id order.** admit receives the id from
  the builder's sequencer and appends in sequence; the table's row
  order IS the admission order, which is what makes `dump`
  deterministic for free.

## harvest

- **the refusing write path** — the only one in the lineage:
  `PRIVATE/PseudoCoup_v5/Research/rust_routing/ledger.py`, 56
  lines, "the only rejecting write path and raising `type_of`"
  (ledger survey §2). **the one harvest source inside the material
  the gutting removes** — harvest before gutting or read from
  version control under `PCv5-archived-research`. its posture, not
  its code, is what transplants.
- **the halt-on-unresolvable Discipline Violation rule** — the
  `02_ledger` schema specs
  (`0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/`),
  marked by the survey as more advanced than any implementation.
- **the phase discipline** — the R1 refusal pattern carried through
  `PRIVATE/PseudoIR/Tools/intentions/build_intentions.py`
  ("REFUSES to emit on incomplete data"), the same posture at
  another store.
