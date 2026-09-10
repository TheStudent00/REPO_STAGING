# Ledger Survey addendum — tree-sitter and the UR-AST — 2026-08-02

Companion to `ledger_survey_2026-07-27.md`, answering two questions
that survey never asked, at the owner's request:

1. **Which ledger components use the tree-sitter API**, directly,
   indirectly, or not at all — because the new ledgerer will be
   tree-sitter based, and the question is what the harvested parts
   already assume, not a rule that they must.
2. **Where the UR-AST is in all of this** — it was meant as a richer
   AST structure than tree-sitter's, it was part of the advanced
   tools, and it appears nowhere in the ledger survey.

One document, not two, because the answers turn out to be one
finding: the ledger survey's two families that never met are also
**two trees that never met** — the verification family lives on the
raw tree-sitter tree, the semantic family lives on the UR-AST, and
no code anywhere maps one tree's nodes to the other's.

Every path and line cited below was verified on disk 2026-08-02.
The part numbers (§2.1–§2.9) are the nine parts of
`PRIVATE/PseudoCoup_v5/DevComms/log_001_ledgerer_harvest_findings.md`.

---

## 1. tree-sitter usage, part by part

Three modes. **direct** — the file imports and walks the tree-sitter
API. **indirect** — the file never touches tree-sitter, but its data
is produced or consumed by code that does. **none** — no relationship
either way.

| part (log_001 §) | source | mode | evidence |
| --- | --- | --- | --- |
| 2.1 primary key | v0 `idgen.py` | **direct, constitutive** | see §1a |
| 2.2 record shape | v0 `ledger_unified.py` | **direct** | imports `parse` as `_ts_parse` (L75); resolves id → tree-sitter node per file (L93); walks the tree-sitter parent chain (L107) |
| 2.3 semantic payload | `PseudoCoup/pseudocoup/core/ledger.py` | **none in the file, indirect in practice** | imports are `json`, `os`, `typing` only (L1–3). Every writer is tree-sitter code: `ingress/kotlin.py` L1–2 imports `tree_sitter` + `tree_sitter_kotlin` directly and calls `ledger.register_*` from inside its parse walk |
| 2.4 keying specs | `0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/` | **indirect, by stipulation** | `master.md` L61: "As the Ingestor maps `tree-sitter` syntax into `URNodes`, it queries the Ledger's `types` registry" — tree-sitter is the assumed front end, never the API used |
| 2.4 refusal impl | `PseudoCoup_v5/Research/rust_routing/ledger.py` | **none** | sole import is `rust_cell` (L11); a pure refusing dict |
| 2.5 integrity `check()` | v0 `ledger_unified.py` L243–281 | **direct** | same file as 2.2; and the invariants it asserts are properties of tree-sitter-derived ids |
| 2.6 divergence kinds | v0 `ledger.py` `classify_methods` | **half-direct** | the Kotlin side is tree-sitter — "tree-sitter = the source spec" (L15, L43); the Python side is `ast` + `inspect` + exec (L29–30) |
| 2.6 reason vocabulary | `0_Archive/PseudoIR/archive/experiments/` `ledger.json` sidecars | **none** | data files, no API |
| 2.7 verification half | v0 `kit_ledger.py` | **none, deliberately** | imports `importlib`, `types`, `oracle`, `ui_ledger` (L19–27) — it executes and introspects the transpiled Python; it joins the static side on id equality, never re-parsing anything |
| 2.8 layout intent | v0 `ui_ledger.py` | **direct** | "tree-sitter call-tree walk" (L71); imports `parse` (L29) |
| 2.9 registry linkage | no code exists | n/a | — |

### 1a. The primary key is not just tree-sitter-*using* — it is a description *of* the tree-sitter tree

`idgen.py`'s id is `childIndex:nodeKind` composed along the path from
the root, where the child index counts "tree-sitter's own
`node.children`, named AND anonymous alike" (L14–17) and the walk goes
"through the REAL tree-sitter tree (matching the shape tree-sitter
itself produces)" (L43). `nodeKind` is a grammar node kind string.

So the id does not merely come from tree-sitter; **it is a coordinate
in a specific grammar's parse tree**. Two consequences:

- **Grammar version is upstream of id stability.** A grammar update
  that changes node kinds or child arity changes ids without any
  source edit. The keying spec's own note ("re-ingesting changed
  source changes ids") covers source edits; this is the same hazard
  from the grammar side, and no surveyed component owns it. The only
  design that does is the archived `tree_sitter_base` plan node
  (projected into
  `PRIVATE/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_tree_sitter.md`):
  commit-pinned vendored grammars with a provenance manifest and a
  byte-compared census. That node is design, not surveyed code.
- **Every id-consuming part inherits the dependency.** 2.2, 2.5, 2.7
  and the emission contract (`inject_emitid.py`, itself direct —
  `parse` at L153, edits placed at tree-sitter byte offsets, L731)
  are tree-sitter-coupled through the id even where their own logic
  is not.

### 1b. One shared frontend

Every **direct** consumer above routes through a single 40-line
module, `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/parse.py`:
`Language`/`Parser` construction, an old/new py-tree-sitter API
shim, and `named_kinds()` enumerating the routing surface live from
the compiled grammar. Its docstring: "tree-sitter is the TRUTH;
everything downstream routes off the concrete syntax tree it
produces." No tool constructs a parser on its own. This is the
single-owner pattern `tree_sitter_base` generalizes to N languages.

### 1c. Verdict for the new ledgerer

tree-sitter enters the harvested material at exactly two depths, and
is absent at two others:

- **Identity** — constitutive (§1a). The key IS tree-sitter.
- **Ingestion** — all semantic-payload writers are tree-sitter walks.
- **Storage** — none. Both stores (289-line, rust_routing) are
  parser-agnostic dicts and can stay that way.
- **Runtime verification** — none, deliberately. `kit_ledger` and
  the exec side of `classify_methods` introspect executed output and
  meet the static side only at the id.

So "the ledgerer is tree-sitter based" is true of identity and
ingestion, and false of storage and runtime verification — the
latter's independence from the parser is a property to preserve, not
a gap.

---

## 2. The UR-AST

### 2.1 What it is, mechanically

`PseudoCoup/pseudocoup/core/ur_ast.py`, 154 lines. ~30 plain Python
classes under a base:

```python
class URNode:
    """Base class for all Universal Rich AST nodes."""
    def __init__(self):
        self.metadata: dict[str, Any] = {}
        # metadata will hold properties hydrated from the Ledger
```

Language-neutral node kinds (`ModuleNode`, `ClassDefNode`,
`FunctionDefNode`, `BinaryOpNode`, …). No id field, no span field, no
reference to the tree-sitter node it was built from, no
serialization. Ingestors map tree-sitter syntax into URNodes;
emitters traverse URNodes.

### 2.2 Three copies, all different, no authority

| copy | lines | md5 differs | delta |
| --- | --- | --- | --- |
| `0_Archive/PseudoCoup_v3/pseudocoup/core/ur_ast.py` | 124 | yes | the origin |
| `PseudoCoup/pseudocoup/core/ur_ast.py` (v4) | 154 | yes | v3 + `UnaryOpNode`, `CastNode`, `ModifierNode`, `DeclarativeNode` |
| `WFL_Projects/WFL_PseudoCoup/pseudocoup/core/ur_ast.py` | 142 | yes | v4 **minus** `UnaryOpNode` and `CastNode` |

The lineage's most advanced emitter (WFL's `dart.py`) runs on a
UR-AST *missing two node kinds its parent has*. Contrast the
289-line ledger, whose WFL copy is byte-identical to v4's. The
UR-AST drifted where the ledger did not — three stores of one
schema, the exact failure the planning framework names.

### 2.3 The spirit versus what was achieved

The spirit: a **richer** AST than tree-sitter's. What the code
achieves: a *normalized* one — language-neutral kinds plus a
`metadata` side-channel that ingestors write semantic facts into
(`metadata['type']`, `metadata['scope_fn']`, `metadata['range_kind']`
— `ingress/kotlin.py` L161, L381–388) and emitters read
(`node.metadata.get('type', 'dynamic')` across `egress/*.py`).

But positionally it is **poorer** than the tree it came from: a
URNode cannot be addressed. tree-sitter gives every node a path,
span, and byte offsets; the URNode keeps none of them. Richer in
semantics, poorer in identity — and identity is the axis the ledger
survey ranked highest (§2.1's positional-path ids as the
highest-value transplant).

### 2.4 The ledger–UR-AST join exists in spec and comment, not in code

- The `02_ledger` specs define them as one mechanism: the ingestor
  erases in the UR-AST and logs in the Ledger; the emitter traverses
  the UR-AST, consults the Ledger, re-injects (`master.md` L51–52,
  L61, L66).
- The code comment says `metadata` "will hold properties hydrated
  from the Ledger."
- **Neither happens.** `core/ledger.py` and `core/ur_ast.py` never
  import each other; nothing hydrates metadata from the Ledger —
  ingestors write metadata directly at parse time, and emitters that
  want ledger facts call the Ledger themselves by name. The
  hydration is an intent with no implementation.

### 2.5 Why it was absent from the ledger survey — and why that was a real gap

Scoping: the ledger survey inventoried ledger *stores*; the UR-AST
is the IR, which the transpiler survey covered in one table row and
one synthesis line (the two-IR-philosophies decision, still open).
Neither survey examined it as a component.

The gap is real because the survey's own §4 plan crosses the two
trees without saying so. The chosen primary key (§2.1) addresses
**tree-sitter** nodes. The chosen semantic payload (§2.3) is written
and consumed by code that lives on the **UR-AST**, which cannot be
addressed. "Re-key the registries onto ids" therefore requires a
URNode ↔ tree-sitter-node mapping held at ingest time — the one
moment both nodes are in hand (`ingress/kotlin.py` holds the
tree-sitter node while constructing the URNode). **No such mapping
exists in any code surveyed.** It is a tenth part in the same sense
as §2.9's registry linkage: design work, no transplant available.

Restated as the one-line finding: the two families never met because
their trees never met. v0's verification family has no UR-AST at all
— it works the raw tree-sitter tree, which is exactly why its ids
work. The semantic family works the UR-AST, which is exactly why its
keys are bare names. Uniting the families IS uniting the trees.

---

## 3. Source inventory, verified 2026-08-02

Beyond log_001 §5's table, the files this addendum adds:

| source | on disk |
| --- | --- |
| `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/parse.py` | present, tree-sitter frontend, sole parser owner |
| `PseudoCoup/pseudocoup/core/ur_ast.py` | 154 lines |
| `WFL_Projects/WFL_PseudoCoup/pseudocoup/core/ur_ast.py` | 142 lines |
| `0_Archive/PseudoCoup_v3/pseudocoup/core/ur_ast.py` | 124 lines |
| `PseudoCoup/pseudocoup/ingress/kotlin.py` | tree_sitter import at L1–2; ledger writes at L630–979 |
| `0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/master.md` | ledger/UR-AST mechanism at L41–66 |

All paths are `...`.

## 4. Open decisions this addendum creates (the owner's)

1. **Where the new ledgerer's record binds.** To the tree-sitter
   tree only, v0-style, with any UR-AST consumer resolving through
   the id — or carrying the URNode ↔ id mapping as a first-class
   part of the ledgerer. The second is new design (§2.5); the first
   makes the UR-AST optional downstream machinery.
2. **Whether the UR-AST is harvested into PCv5 at all** — and if
   so, which of the three diverged copies is the authority, given
   the newest (WFL) is missing two node kinds its parent has.
3. **Who owns grammar pinning.** Id stability depends on pinned
   grammar versions (§1a). The only design that owns this is the
   archived `tree_sitter_base` node; nothing in PCv5's planning
   tree does yet.
