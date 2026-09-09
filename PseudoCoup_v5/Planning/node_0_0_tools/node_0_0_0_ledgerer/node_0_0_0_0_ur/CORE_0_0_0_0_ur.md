---
id: pcv5.tools.ledgerer.ur
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: ur
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/CORE_0_0_0_0_ur.md
super_node:
    name: ledgerer
    path: ../CORE_0_0_0_ledgerer.md
sub_nodes:
    - name: node
      path: node_0_0_0_0_0_node/CORE_0_0_0_0_0_node.md
    - name: connector
      path: node_0_0_0_0_1_connector/CORE_0_0_0_0_1_connector.md
    - name: id
      path: node_0_0_0_0_2_id/CORE_0_0_0_0_2_id.md
    - name: tree
      designation: code (class)
      realize: false
    - name: kinds
      designation: code (variable)
      realize: false
---

# CORE 0_0_0_0 — ur

## metadata

- **id:** pcv5.tools.ledgerer.ur
- **level:** 3
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledgerer](../CORE_0_0_0_ledgerer.md)

## sub_nodes

- [node](node_0_0_0_0_0_node/CORE_0_0_0_0_0_node.md) — the UR node — one node shape in four layers, each layer owned by a different writer, none replacing the one beneath it (drafted in `PseudoCoup_v5/DevComms/log_002_ur_brainstorm.md` §7.1).
- [connector](node_0_0_0_0_1_connector/CORE_0_0_0_0_1_connector.md) — the static graph object joining two nodes by id — the typed node-connector entry of the owner's carrying capacity, made first-class.
- [id](node_0_0_0_0_2_id/CORE_0_0_0_0_2_id.md) — the identity value — the third form beside `node` and `connector` (registered 2026-08-05, the owner: "we are aligned.
- tree — code (class) *(realize: false)*
- kinds — code (variable) *(realize: false)*

## definition

Universal Rich AST definitions — the abstraction of the FORM of a
parsed source, as `ledger` is the abstraction of the stored data
structure (the owner, 2026-08-02).

this node is THE vocabulary: node forms, edge forms, the registration
forms. `ledger` instantiates these forms and adds mechanics; it
defines no second vocabulary (settled 2026-08-04). "universal" names
the destination, not the road — the mappers into it are per-language;
consumers of it never require the source language, which is carried
as data (`language`, `ts_kind` in the substrate), not as a
precondition of any interface.

intended to be strictly richer than tree-sitter's tree: nothing
tree-sitter knows about a node is lost by becoming a UR node. the
prior implementation did not achieve that (survey addendum §2.3 —
richer in semantics, poorer in identity: no id, no span, no link back
to the source node); closing that gap is this node's design work, not
a transplant.

## design

the two `realize: false` entries in the register, designed here since
they have no folder:

- **`tree`** — `code (class)`, the per-file container: `language`,
  grammar `semantic_version`, root `node`. holds NO source copy
  (ruled 2026-08-07, superseding the earlier retained-bytes design:
  content lives on the nodes as `TsOrigin.text`, form tokens in the
  pack's stencils). the grammar version on it is what makes pinning
  checkable at runtime (log_002 §6.0).
  serialization RULED 2026-08-06: UR is in-memory only, rebuilt by
  re-parsing; the ledger is the durable store (log_002 §8.3's lean,
  confirmed by the owner). so `tree` stays folderless and grows no
  format. `Builder.ur` is an instance of this class.
- **`kinds`** — `code (variable)`, the neutral `ur_kind` vocabulary:
  DATA, derived from the target grammars (rust's five supertypes and
  the suffix families, log_002 §3), not inherited from the old
  thirty (the owner, log_002 §8.4: building fresh). checked for totality
  against `node-types.json` by the census. **append-only in
  spirit**, like the built-in macro table: a kind that vanished
  would orphan `ur_kind` tags in existing ledgers, so kinds are
  superseded by addition, never removed. the per-language
  ts_kind→ur_kind MAPS are `ts_to_ur`'s, not here — this is the
  destination vocabulary only.
  - **organizing principle, RULED 2026-08-06 (the owner: COUPLED)** — the
    label vocabulary follows the minimum set's verdicts: a construct
    the intentions audit ruled derived gets no bucket of its own;
    the label says the DOMINANT object, the substrate keeps what it
    was (`ts_kind` is lossless either way). the owner's own words carried
    the ruling: "one part is ensuring that the source intention is
    saved but also properly classified into the dominant intention."
    the decision is unpacked in
    `PseudoCoup_v5/DevComms/log_015_coupled_or_decoupled.md`.
  - **the ecosystem additions, RULED 2026-08-12** (the kind-
    clustering research, PCHQ logs 008–016 — 411 grammars, 31,212
    kinds; adoption walk in PCHQ log_016 §6 and the P1–P9 rulings):
    objects gain `import` (155-language family, ends the
    import/namespace strain), `try` (the error-clause family;
    absorbs G's grammar-visible remnant), `pair` (152-language
    key-with-value association), `interpolation` (121 languages);
    forms gain `container-form` (body-lists and document roots —
    retires the NONE question). names per the owner's Python-naming rule
    (no universal claim → Python's word). two standing facts ruled
    with them: classification is TWO-LAYERED (shape from grammar
    evidence now; intention from resolution later — one ruling
    replacing the 42 DUAL tie-breaks), and A/B/C/E/G/H/I are
    shape-invisible ecosystem-wide (ledger-resolved, never
    grammar-resolved). sum types stay refuted as a shape (the
    record-dual-choice ruling now rests on measurement). mapping
    strategy is split by grammar discipline (P9): roled grammars
    via clusters; zero-role/outlier grammars (kotlin, ruby,
    c-sharp) via nearest-counterpart + name evidence.
  - **the three constructs, per the ruling and log_014's brief**:
    sum types → `record` dual `choice` (no `sum` bucket); error
    propagation (`try_expression`) → `choice` dual `function` (no
    `error-flow` bucket, and not C); borrowing → no bucket at
    intention tier; `reference_expression` refuses `name` and takes
    a non-object tag from the form tier. tiers RULED 2026-08-06
    (the owner: "yes to your recommendations and leanings"): the 11
    minimum-set objects + categories A–J (intention tier), plus the
    form tier — `type-form` and `declarative-form` (log_008's
    proposal, now ruled in). the third form bucket for proof
    apparatus (`reference_expression`, `lifetime`) is RULED
    `proof-form` (the owner, 2026-08-06: "`proof-form` sounds good to
    me") — the design walk's last open name.

### the identity system — graduated 2026-08-05

settled and moved to its own node,
[id](node_0_0_0_0_2_id/CORE_0_0_0_0_2_id.md) — the third form beside
`node` and `connector`. the spacetime id, the logical two-level
clock, the frame axis at merge, the fingerprint-as-attribute, and
the wall-clock provenance stamp are all stated there. this section
held the discussion while it was open; the record of how it settled
is in this file's git history.

## harvest

which Frankenstein parts land here. part numbers are
`PseudoCoup_v5/DevComms/log_001_ledgerer_harvest_findings.md`
§2; "addendum" is
`PseudoCoup_v5/DevComms/ledger_survey_2026-08-02_tree_sitter_ur_ast.md`.
placements are draft commentary, not settled.

- **no part transplants here whole.** every surveyed implementation
  is either store-side or tree-sitter-side; the UR layer is the one
  place the survey found NOTHING best-in-class to take. what it
  absorbs is definitional:
  - **the id as a node FIELD** — part 2.1's positional-path id
    (`childIndex:nodeKind` along the path from the root, v0
    `idgen.py`). the GENERATION of ids is `ts_to_ur`'s work;
    what belongs here is the definition that every UR node CARRIES
    one, plus span and source-node linkage — the fields whose absence
    made the prior UR-AST poorer than the tree it came from (addendum
    §2.3). that absence is also what made the survey's "re-key the
    registries onto ids" plan impossible against the old UR-AST
    (addendum §2.5); these fields are the fix.
  - **the metadata side-channel precedent** — the prior `ur_ast.py`'s
    `metadata` dict, written by ingestors and read by emitters. kept
    as precedent, not ported: the "hydrated from the Ledger" intent
    it recorded was never implemented (addendum §2.4), and how UR
    facts relate to ledger entries is settled between this node and
    `ledger`, not inherited.
  - **registration forms for connections** — the node-edge form
    vocabulary the ledger accepts entries in (the owner, 2026-08-02, see
    `ledger`'s notes). no existing code; design work of this node.

## notes

- the owner, 2026-08-02, at the node's founding: "i think this is where a
  significant number of the surveyed pieces will reside but maybe im
  wrong about that." — revised the same day, on the survey's part
  placement (most parts are store-side): "i would have thought the
  formalism would have absorbed all of the components but i suppose
  it makes sense that mechanisms and structures would be spread
  across components."
- the prior implementation is
  `PseudoCoup/pseudocoup/core/ur_ast.py` and its two
  diverged copies (v3, WFL) — see
  `PseudoCoup_v5/DevComms/ledger_survey_2026-08-02_tree_sitter_ur_ast.md`
  §2.2. no copy is the authority; this node supersedes rather than
  ports.
