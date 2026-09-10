---
id: pcv5.tools.ledgerer.ur.node
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: node
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/node_0_0_0_0_0_node/CORE_0_0_0_0_0_node.md
super_node:
    name: ur
    path: ../CORE_0_0_0_0_ur.md
sub_nodes:
    - name: ts_kind
      designation: code (attribute)
      realize: false
    - name: named
      designation: code (attribute)
      realize: false
    - name: span
      designation: code (attribute)
      realize: false
    - name: fields
      designation: code (attribute)
      realize: false
    - name: children
      designation: code (attribute)
      realize: false
    - name: language
      designation: code (attribute)
      realize: false
    - name: id
      designation: code (attribute)
      realize: false
    - name: ur_kind
      designation: code (attribute)
      realize: false
    - name: semantic
      designation: code (attribute)
      realize: false
    - name: connectors
      designation: code (attribute)
      realize: false
    - name: text
      designation: code (method)
      realize: false
    - name: field
      designation: code (method)
      realize: false
    - name: walk
      designation: code (method)
      realize: false
---

# CORE 0_0_0_0_0 — node

## sub_nodes

- ts_kind — code (attribute) *(realize: false)*
- named — code (attribute) *(realize: false)*
- span — code (attribute) *(realize: false)*
- fields — code (attribute) *(realize: false)*
- children — code (attribute) *(realize: false)*
- language — code (attribute) *(realize: false)*
- id — code (attribute) *(realize: false)*
- ur_kind — code (attribute) *(realize: false)*
- semantic — code (attribute) *(realize: false)*
- connectors — code (attribute) *(realize: false)*
- text — code (method) *(realize: false)*
- field — code (method) *(realize: false)*
- walk — code (method) *(realize: false)*

## definition

the UR node — one node shape in four layers, each layer owned by a
different writer, none replacing the one beneath it (drafted in
`PRIVATE/PseudoCoup_v5/DevComms/log_002_ur_brainstorm.md` §7.1).

## components

```
class Node
	attributes:
		ts_kind          # substrate
		named            # substrate
		span             # substrate
		fields           # substrate
		children         # substrate
		language         # substrate
		id               # identity
		ur_kind          # normalization
		semantic         # annotation
		connectors       # annotation
	methods:
		text
		field
		walk
```

the four layers, and who writes each:

- **substrate** — what the parser said, kept rather than transformed:
  `ts_kind`, `named`, `span`, `fields` (the grammar's role names),
  `children` (position-ordered, anonymous included), `language`.
  written once at mapping time by `ts_to_ur`, never after.
  losslessness is the substrate plus the retained source bytes, which
  live on `tree` (the `realize: false` container in `ur`'s register);
  `Node.text` resolves the span against them.
- **identity** — `id`, the positional path (harvest part 2.1), minted
  by `ts_to_ur` during the walk. a field on the node because the
  survey addendum found its absence is what broke the prior UR-AST.
- **normalization** — `ur_kind`, the language-neutral tag drawn from
  `ur`'s `kinds` vocabulary. a TAG on the real node, not a class
  replacing it: neutral consumers read `ur_kind`; nothing needing the
  substrate loses it.
- **annotation** — `semantic` and `connectors`, the slots the ledger
  side reads and writes; `ur_to_ledger` fills them, and late writers
  (tracer, expansion pass) extend `connectors` against existing ids.

## rules

- **the opacity form.** a `token_tree` (or any region the grammar
  declares opaque) becomes ONE node marked opaque — the refusal
  posture applied to form: never silently empty, so a consumer halts
  or skips knowingly. re-parsed content (via `injections.scm`) hangs
  BENEATH the opaque node, marked injected, so direct and recovered
  structure are never confusable.
- **open, carried from log_002 §8.1:** whether injected nodes' ids
  form a sub-address space under the token_tree's path. leaning yes
  (byte offsets already stay true to the original file under
  `included_ranges`), unruled.

## notes

- named `node` over `ur_node` (the owner, 2026-08-05): the module already
  says whose node it is — `ur.node`, not `ur.ur_node`. the owner's stated
  graph vocabulary is "node and connector", and this class is the
  node half. the overload against planning nodes and tree-sitter
  nodes is carried by qualification (`ur.node` in plans, `ur.Node` in
  code).
