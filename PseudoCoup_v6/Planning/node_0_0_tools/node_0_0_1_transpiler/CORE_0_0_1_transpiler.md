---
id: pcv6.transpiler
level: 2
status: draft
settled_by: the owner
supersedes: null
nodes: []
---

# CORE 0_0_1 — transpiler

## metadata

- **id:** pcv6.transpiler
- **level:** 2
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

*(none yet)*

## definition

maps from source language to target language while preserving
intentions

## components

- ingress
  - mapping: source (lang x) --> UR-AST --> target (hub)
- egress
  - mapping: source (hub) --> UR-AST --> target (lang x)

## notes

two components, not one. the perspective is the hub. mapping into the
hub is not the same work as mapping out of it.

what the transpiler is really doing: take UR_AST_x from script_x in
language_x, and map each node and edge to its equivalent node and
edge in UR_AST_y for language_y. we do not have UR_AST_y — making it
is the job. sometimes the ledger makes the mapping obvious. when it
is not obvious, we build the logic for it.

the transpiler travels through the levels of depth it is allowed to.
when it meets an object it can follow to its definition, it follows,
as long as that makes sense. if it does not follow, that object
becomes a wrapper on the other side.

reasons to stop following:

- the definition is not logically reachable. found while following.
- the definition is not legally reachable. said up front.
- the goal is the high level logic, not the modules. said up front.

policy for now. the last two are already shaped like data if we want
them to be.

the same script under a different goal gives a different boundary, so
follow-or-wrap belongs to the transpiler, not the ledger.

## support

projected from the previous plan:

- [SUPPORT_ingress.md](SUPPORT_ingress.md) — the pipeline every
  language rides, and what an ingestor may specialize
- [SUPPORT_egress.md](SUPPORT_egress.md) — emission, held until
  ingress stands
