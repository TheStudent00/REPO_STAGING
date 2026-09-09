---
id: pcv5.tools.ledgerer.ur.connector
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: connector
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/node_0_0_0_0_1_connector/CORE_0_0_0_0_1_connector.md
super_node:
    name: ur
    path: ../CORE_0_0_0_0_ur.md
sub_nodes:
    - name: kind
      designation: code (attribute)
      realize: false
    - name: from_id
      designation: code (attribute)
      realize: false
    - name: to_id
      designation: code (attribute)
      realize: false
    - name: payload
      designation: code (attribute)
      realize: false
    - name: provenance
      designation: code (attribute)
      realize: false
---

# CORE 0_0_0_0_1 — connector

## sub_nodes

- kind — code (attribute) *(realize: false)*
- from_id — code (attribute) *(realize: false)*
- to_id — code (attribute) *(realize: false)*
- payload — code (attribute) *(realize: false)*
- provenance — code (attribute) *(realize: false)*

## definition

the static graph object joining two nodes by id — the typed node-edge
entry of the owner's carrying capacity, made first-class. every writer that
extends a ledger after its build writes THESE, against existing ids,
which is what makes late arrival uniform rather than special-cased.

## components

```
class Connector
	attributes:
		kind             # from the connector-kind vocabulary below
		from_id          # positional-path id
		to_id            # positional-path id, or an abstract node's id
		payload          # kind-specific data
		provenance       # which writer, when, from what evidence
```

## the connector-kind vocabulary, as drafted

open set by design — the carrying capacity is that new kinds are data,
not schema. the kinds already named by settled material:

- **definition↔instance** — a use joined to its in-corpus definition
  (the owner's worked instance; `tags.scm` gives the syntactic halves).
- **instance→abstract** — a use whose definition is out of corpus,
  joined to an ABSTRACT NODE standing for the to-be wrapper (the
  ledgerer does not decide what is a wrapper; it holds the node —
  the owner, log_002 §8.1).
- **invocation→macro-definition** and **produced→producer** — the
  meta-programming connectors of
  `PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_metaprogramming.md`:
  an invocation to the macro it names, and generated structure to the
  site that generated it.
- **runtime** — the tracer's late connections, `<id>#<rank>` instance
  observations joined on id equality.
- **expansion** — the late expansion pass's upgrade connectors
  (log_005 §2: expansions extend a ledger "the same way the tracer's
  runtime connections do").

## notes

- named `connector` per the owner's reserved use of the word for the static
  graph object ("i like referring to graph objects using the words
  `node` and `connector`"); `ur_to_ledger`'s naming note records the
  reservation this fulfils.
- `provenance` is drafted here because every kind above has a
  different writer (ts_to_ur never writes these; ur_to_ledger, the
  tracer, and the expansion pass all do), and a connector that cannot
  say which writer produced it cannot be re-derived when the
  toolchain version moves (log_003 §6's churn finding). unruled;
  strike if it belongs in `ledger`'s record mechanics instead.
