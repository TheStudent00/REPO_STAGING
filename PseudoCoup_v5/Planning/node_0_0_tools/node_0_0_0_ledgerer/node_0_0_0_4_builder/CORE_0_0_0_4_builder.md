---
id: pcv5.tools.ledgerer.builder
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: builder
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_4_builder/CORE_0_0_0_4_builder.md
super_node:
    name: ledgerer
    path: ../CORE_0_0_0_ledgerer.md
sub_nodes:
    - name: ts_to_ur
      designation: code (attribute)
      realize: false
    - name: ur_to_ledger
      designation: code (attribute)
      realize: false
    - name: ur
      designation: code (attribute)
      realize: false
    - name: ledger
      designation: code (attribute)
      realize: false
    - name: build
      designation: code (method)
      realize: false
    - name: check
      designation: code (method)
      realize: false
    - name: sequencer
      designation: code (attribute)
      realize: false
---

# CORE 0_0_0_4 — builder

## metadata

- **id:** pcv5.tools.ledgerer.builder
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledgerer](../CORE_0_0_0_ledgerer.md)

## sub_nodes

- ts_to_ur — code (attribute) *(realize: false)*
- ur_to_ledger — code (attribute) *(realize: false)*
- ur — code (attribute) *(realize: false)*
- ledger — code (attribute) *(realize: false)*
- build — code (method) *(realize: false)*
- check — code (method) *(realize: false)*
- sequencer — code (attribute) *(realize: false)*

## definition

the ledgerer's operational funnel: ledgerer calls route through the
builder, which runs source → UR → ledger end to end. pure
orchestration — it DEFINES nothing the siblings define; it holds
instances of them as attributes and sequences `ts_to_ur` and
`ur_to_ledger`. lossless (the owner, 2026-08-02).

named for the harvest's own verb — v0's entry point is
`ledger_unified.build`, the integrity check runs at build, and later
ledger-merging is a build-from-many. a class, not a module: it holds
the work-in-progress as state and exposes the call surface (so
`ledgerer.Builder` in code).

## design

draft shape, per the definition/instance ruling (the owner, 2026-08-02):
attributes are INSTANCES whose types are defined in the sibling
modules. each is registered above as a `realize: false` entry — plan
structure, no folder — and graduates to a folder by deleting that
key when it grows rules or design of its own.

```
class Builder
	attributes:
		ts_to_ur
		ur_to_ledger
		ur
		ledger
		sequencer
	methods:
		build
		check
```

- `Builder.ts_to_ur` — instance of `ts_to_ur`'s class.
- `Builder.ur_to_ledger` — instance of `ur_to_ledger`'s class.
- `Builder.ur` — the UR tree under construction, in `ur`'s forms.
- `Builder.ledger` — the ledger under construction, in `ledger`'s
  forms.
- `Builder.sequencer` — the two-level logical clock (batch ordinal,
  in-batch index) that assigns spacetime coordinates at admission
  (settled 2026-08-05; the id VALUE class is `ur.id`). with the
  ledger-under-construction, this is the state the builder holds —
  the correction to “nearly stateless.”
- `Builder.build` — source → UR → ledger, sequencing `ts_to_ur`
  then `ur_to_ledger`.
- `Builder.check` — the integrity harvest (2.5 below) run over the
  built ledger.

## harvest

which Frankenstein parts land here. part numbers are
`~/Programming/PseudoCoup_v5/DevComms/log_001_ledgerer_harvest_findings.md`
§2. placements are draft commentary, not settled.

- **2.5 integrity** — the only `--check` in the lineage: ids
  globally unique, every id exactly once, `entry_count` equals node
  count, nonzero exit on failure. source: `ledger_unified.check()`,
  L243–281 of
  `~/Programming/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger_unified.py`.
  taken "verbatim, extended" with the two invariants that do not
  exist yet: COVERAGE (every emitted node traces to a ledger id) and
  SEMANTIC (every declaration id carries a type or an explicit
  `unresolvable`) — the second is how `ledger`'s refusal posture
  becomes mechanically enforced. placed here because the builder
  owns operations over built ledgers; the alternative placement in
  `ledger` remains defensible.
- **2.7 verification half** — execute, introspect, compare, joined
  on id equality: v0's exec-and-introspect with dropped/relocated
  discrimination
  (`~/Programming/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger.py`,
  370 lines) and `kit_ledger`'s `_lcs` + `_sig_match` comparison
  (`.../kit_ledger.py`, 374 lines). deliberately parser-free — it
  meets the static side only at the id (survey addendum §1c), a
  property to preserve.
- **the instance connection** — the owner's wrapped/followed objects
  connecting to their instances. precedent: the `<id>#<rank>`
  instance key at fire time; the tracer (`pcv5.tools.tracer`, a
  co-node of the ledgerer, not part of it) is the writer that adds
  runtime connections and annotations later. the boundary: the
  tracer OBSERVES and emits; the builder RECORDS what arrives into
  the ledger.
- **ledger merging** — named by the owner at founding as a possible later
  responsibility. no surveyed part corresponds; nothing in the
  lineage ever merged two ledgers.
- *(moved out 2026-08-02: 2.9's writing half went to
  `ur_to_ledger_mapper` with the mapping work when that node was
  extracted.)*

## notes

- the sequencer candidate of 2026-08-05 was settled the same day
  (the owner: "perfect") and is in the register and design above; the id
  VALUE class is `ur.id`
  (`../node_0_0_0_0_ur/node_0_0_0_0_2_id/CORE_0_0_0_0_2_id.md`).
- the owner, 2026-08-02, at the node's founding (as `ledger_master`):
  "objects wrapped/followed can have a special ledger connection to
  its instances (for slicing or whatever other purposes); *master*
  because this module might have more responsibilities later such as
  merging ledgers."
- renamed `ledger_master` → `builder` and refined `code (module)` →
  `code (class)` the same day, when the funnel was settled. briefly
  held `ts_to_ur_mapper` as a sub-node; reversed hours later on the
  definition/instance ruling (the owner: "the definition of the module
  doesnt make sense to be within a class") — definitions live at
  `ledgerer` level, the builder holds instances as attributes.
  *(a section-only spelling was briefly the plan; superseded the
  same day by `realize: false` register entries — PROTOCOL §1 —
  so the structure is registered YAML-truth AND stays in this
  file. the `## design` overview above is its commentary.)*
- the instance connection is the per-instance key of the settled
  keying (`<id>#<rank>` at fire time) seen from the store's side —
  the id joins a call site to every runtime instance of it.
