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
sub_nodes: []
---

# CORE 0_0_0_0_1 — connector

## metadata

- **id:** pcv5.tools.ledgerer.ur.connector
- **level:** 4
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ur](../CORE_0_0_0_0_ur.md)

## sub_nodes

*(none yet)*

## definition

the static graph object joining two nodes by id — the typed node-connector
entry of the owner's carrying capacity, made first-class. every writer that
extends a ledger after its build writes THESE, against existing ids,
which is what makes late arrival uniform rather than special-cased.

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
  `PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_metaprogramming.md`:
  an invocation to the macro it names, and generated structure to the
  site that generated it.
- **runtime** — the tracer's late connections, `<id>#<rank>` instance
  observations joined on id equality.
- **expansion** — the late expansion pass's upgrade connectors
  (log_005 §2: expansions extend a ledger "the same way the tracer's
  runtime connections do").
