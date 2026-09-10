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
sub_nodes: []
---

# CORE 0_0_0_0_0 — node

## metadata

- **id:** pcv5.tools.ledgerer.ur.node
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

the UR node — one node shape in four layers, each layer owned by a
different writer, none replacing the one beneath it (drafted in
`PRIVATE/PseudoCoup_v5/DevComms/log_002_ur_brainstorm.md` §7.1).

## design

settled 2026-08-05 (the owner: "yes ... and yes", then "i think i agree
with everything, except i want to talk about the identifier system"):
**origin is an attachment, not baked-in fields.** the node carries
only what is true of every node, whatever produced it; the
origin-specific facts live in an origin object held by the node, one
class per origin, helper classes in the same file.

```
class Node
	attributes:
		id             # universal; see `ur`'s identity design
		ur_kind        # universal
		sub_nodes      # universal — generated nodes have structure too
		semantic       # universal annotation slot
		connectors     # universal annotation slot
		origin         # instance of one origin class below
	methods:
		text           # answers via origin; honestly absent for abstract
		walk


class TsOrigin
	"""
		the tree-sitter facts, for nodes whose
		origin is a parse
	"""
	attributes:
		ts_kind
		named
		fields         # the grammar's role names
		span
		language
		text           # content leaves only (identifiers, literals)
		variant        # varying token(s), read from the tree at mint
		path           # source file; set on each file's root node
```

- `path` added 2026-08-06 (the owner: "file name is needed"): without a
  source file name on the row, merge's same-source triage has no
  flag to raise — a double ingestion merges SUCCESSFULLY and sits in
  the ledger twice, unnoticed. optional; the mapper sets it on each
  file's root node at least. intentional re-ingestion (the owner's
  file-history-through-time case) is served by the already-ruled
  wall-clock stamp + the supersedes-style connector; an
  allow-multi-ingest flag is noted as a possible builder option,
  unruled.
- co-shapes as needed, each carrying only what is true of that
  origin: a `GeneratedOrigin` (producer's id, which template) for
  macro-expansion output, an `AbstractOrigin` (declared-by) for the
  to-be-wrapper nodes. names SETTLED as drafted, 2026-08-06.
- why: `ur.node` is not strictly a tree-sitter object (the owner) — the
  macro-extraction system produces nodes tree-sitter never saw, and
  abstract nodes have no text at all. the strictly-richer rule stays
  intact but correctly scoped: for PARSED nodes, everything
  tree-sitter knows lives in `TsOrigin`, nothing lost.
- `Node.origin` and `Connector.provenance` are the same idea seen
  from the two graph objects: everything can say what produced it.

- **no source copy, ruled 2026-08-07** (the owner: "definitely drop
  `source_bytes`... i have no interest in that solution"): the
  ledger stores the FACTS a file states, never the file. content
  leaves carry `text` (measured on the corpus: 14 leaf kinds,
  37.6% of leaf instances); kind-determined tokens (62.4%) are the
  pack's stencils' to rebuild; whitespace is stored nowhere.
  unparse is therefore **faithful convergence** (the owner's word), not
  reproduction: the first pass normalizes to the pack's canonical
  formatting, every later pass is a fixed point — which is the
  log_015 round-trip principle, now grounded at token level.
- **`variant`, ruled 2026-08-07**: for the ~dozen kinds whose
  anonymous tokens vary by instance (operator, trailing `;`,
  turbofish), the varying token is READ from the tree at mint time
  and stored — never inferred, no compiler needed at token level.
  the owner's deeper reason recorded: emission into ANY target needs the
  proper tokens, and this field is where an emitter finds them.
  the per-language varying-kind table is GRAMMAR-AUTHORED (ruled
  2026-08-11, superseding "census-generated and human-reviewed"):
  the pinned `grammar.js` enumerates every admissible token inside
  the rule that admits it, so the table is complete by
  construction; the corpus census stays as frequency and oracle
  material only. see `ts_to_ur`'s design
  (../../node_0_0_0_2_ts_to_ur/CORE_0_0_0_2_ts_to_ur.md).
- **planned, 2026-08-07 (the owner): the documentation node.** doc
  comments are stored as data so they can be inserted into any
  target using that target's comment protocol — a special comment
  node whose content may point to the file holding the respective
  documentation. not yet designed; recorded here as the planned
  home.

## rules

- **the opacity form.** a `token_tree` (or any region the grammar
  declares opaque) becomes ONE node marked opaque — the refusal
  posture applied to form: never silently empty, so a consumer halts
  or skips knowingly. re-parsed content (via `injections.scm`) hangs
  BENEATH the opaque node, marked injected, so direct and recovered
  structure are never confusable.
- **RULED 2026-08-06 (the owner: "yes to your recommendations and
  leanings"): injected nodes' ids form a sub-address space under the
  token_tree's path.** byte offsets stay true to the original file
  (the arithmetic remap of log_010), and direct vs injected stays
  distinguishable by the address itself.

## notes

- named `node` over `ur_node` (the owner, 2026-08-05): the module already
  says whose node it is — `ur.node`, not `ur.ur_node`. the owner's stated
  graph vocabulary is "node and connector", and this class is the
  node half. the overload against planning nodes and tree-sitter
  nodes is carried by qualification (`ur.node` in plans, `ur.Node` in
  code).
