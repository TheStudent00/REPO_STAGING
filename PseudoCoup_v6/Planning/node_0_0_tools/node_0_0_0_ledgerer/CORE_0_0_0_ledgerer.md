---
id: pcv6.ledgerer
level: 2
status: draft
settled_by: the owner
supersedes: null
nodes: []
---

# CORE 0_0_0 — ledgerer

## metadata

- **id:** pcv6.ledgerer
- **level:** 2
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

*(none yet)*

## definition

the system that tracks all information needed of input script to
preserve intentions. the ledger is what it produces.

a separate tool, because its purpose exists outside of the transpiler
project. the transpiler uses it.

## components

- tree-sitter: core external module of project that allows the
  connection between languages
  - tree-sitter script processing
  - tree-sitter vocabulary for some language
- UR-AST: universal rich syntax tree using tree-sitter CST and
  whatever else
  - identity
  - static record
  - dynamic record: how the static record interacts with itself and
    other external objects. connections that wouldnt be clear from a
    static perspective
- validation

## notes

the ledgerer works on what it is given. it does not follow an object
to its definition. the transpiler does that. the transpiler imports
the ledgerer as a module, so the transpiler decides what the ledgerer
is given.

the ledger says what the script says: this node uses X from module M.
finding M is not the ledgerer's work.

## support

projected from the previous plan:

- [SUPPORT_tree_sitter.md](SUPPORT_tree_sitter.md) — one module owning
  grammars and parsing for every language
- [SUPPORT_ur_ast.md](SUPPORT_ur_ast.md) — the record shape, and how
  each entry gets its identity
- [SUPPORT_validation.md](SUPPORT_validation.md) — the self-check, and
  the rule that ingest never guesses
- [SUPPORT_todos.md](SUPPORT_todos.md) — later slots, and an
  unresolved scale problem
- [SUPPORT_recording_intentions.md](SUPPORT_recording_intentions.md) — recording
  which intention each construct selects
