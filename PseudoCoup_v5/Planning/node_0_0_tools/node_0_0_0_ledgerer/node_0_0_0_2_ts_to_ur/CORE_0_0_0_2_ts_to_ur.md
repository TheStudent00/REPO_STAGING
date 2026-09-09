---
id: pcv5.tools.ledgerer.ts_to_ur
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: ts_to_ur
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_2_ts_to_ur/CORE_0_0_0_2_ts_to_ur.md
super_node:
    name: ledgerer
    path: ../CORE_0_0_0_ledgerer.md
sub_nodes:
    - name: mapper
      designation: code (class)
      realize: false
    - name: language_pack
      designation: code (class)
      realize: false
---

# CORE 0_0_0_2 — ts_to_ur

## metadata

- **id:** pcv5.tools.ledgerer.ts_to_ur
- **level:** 3
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledgerer](../CORE_0_0_0_ledgerer.md)

## sub_nodes

- mapper — code (class) *(realize: false)*
- language_pack — code (class) *(realize: false)*

## definition

maps Tree-Sitter to UR. made up of language-specific sub-modules;
leverages Tree-Sitter vocabularies; lossless; type-aware (the owner,
2026-08-02).

lossless is what makes `ur`'s strictly-richer intent real: every
fact of the tree-sitter node — kind, position, span, bytes —
survives the mapping, so a UR node can always answer for the source
node it came from.

per-language here, universal there: the mappers are per-language;
the TARGET is universal. "universal" names the destination, not the
road (the owner, 2026-08-04).

## design

the two `realize: false` entries in the register, designed here
since they have no folder. shapes RULED 2026-08-11 (the owner: "yeah
those look good"), settled at shape level; skepticism recorded —
robustness is to be VERIFIED (stubs → logic → tests), not assumed.

```
class Mapper
	"""
		walks one tree-sitter parse, mints
		ur.Node per named node; anonymous
		tokens are never materialized —
		positions count them (id arithmetic),
		the pack's tables rebuild them
	"""
	attributes:
		language_pack
		sequencer
	methods:
		map_file
		mint_node
		read_variant
		mark_opaque


class LanguagePack
	"""
		per-language DATA, no per-language
		code: pinned grammar, kind map,
		token tables, query files, census
		baseline
	"""
	attributes:
		grammar_version
		kind_map
		stencils
		variant_roles
		queries
	methods:
		check_pin
```

- `Mapper.map_file` — parse one file with the pack's pinned grammar,
  walk the real tree (anonymous tokens counted in positions, per the
  constitutive id arithmetic), and answer a `ur.Tree`.
- `Mapper.mint_node` — one named tree-sitter node → one `ur.Node`:
  id from the sequencer, `ur_kind` from the pack's kind map,
  `TsOrigin` filled (kind, named, fields, span, language; `text` on
  content leaves; `path` on the root).
- `Mapper.read_variant` — for kinds whose anonymous tokens vary by
  instance: ask the parse by the grammar's role name where one is
  assigned (verified 2026-08-11: tree-sitter's `child_by_field_name`
  — their name — answers anonymous tokens, e.g. `binary_expression`'s
  role `operator` → `'+'`), else scan the anonymous sub-tokens.
  the result lands in `TsOrigin.variant`.
- `Mapper.mark_opaque` — the opacity rule executed: a `token_tree`
  becomes ONE opaque node; injected re-parses hang beneath with
  sub-addressed ids (`node`'s rules section).
- `LanguagePack` is data-only by intent: adding language two means
  writing a pack, not code. `check_pin` compares the runtime
  grammar's version against the manifest (refusal on mismatch).

### the token tables — grammar-authored, RULED 2026-08-11

- **the author is the grammar source, not the corpus and not the
  compiler.** the pinned `grammar.js` is a closed, finite,
  human-written enumeration: every anonymous token appears inside
  the rule that admits it (e.g. `binary_expression`'s operator
  table), so stencils and variant-role lists derived from it are
  complete BY CONSTRUCTION. this supersedes the earlier
  "census-generated, human-reviewed" design: the corpus census
  (`PseudoCoup_v5/Research/census_stencils.py`)
  remains as frequency measurement and oracle test material only —
  it proves nothing about completeness and is not asked to.
- **judges, not authors:** the reconstruction oracle (faithful
  convergence over the corpus) verifies the tables miss nothing —
  a missing bit fails convergence loudly, naming its kind; and
  compile-as-oracle (rustc accepting emitted source) is the
  differential judge where the pinned grammar drifts from the
  language (the 5 ERROR files are the observed divergence).
- the human role is ruling on refusals, not a planned review gate.

### open edges, by log_017 number

- **q3 (macros)** — the shape table is unratified, the kind-one
  engine's placement beside the mapper is undrawn, and the injected
  sub-address's concrete spelling is unpicked. stubs carry these as
  documented edges, not guesses.
- **q4 (error files)** — unruled: refuse / admit-as-opaque / patch
  the grammar.
- **q5 (pinning + census ratification)** — designed, awaiting one
  yes; `check_pin` implements the runtime half.
- **q6 (pack shape on disk)** — the contents list above is ruled by
  this design; the FILE layout of a pack is not yet.

## harvest

which Frankenstein parts land here. part numbers are
`PseudoCoup_v5/DevComms/log_001_ledgerer_harvest_findings.md`
§2; "addendum" is
`PseudoCoup_v5/DevComms/ledger_survey_2026-08-02_tree_sitter_ur_ast.md`.
placements are draft commentary, not settled.

- **2.1 primary key — the generation half.** ids are minted during
  the tree-sitter walk, and this node owns that walk. source: v0
  `idgen.py`
  (`StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/idgen.py`,
  294 lines) — the top-down walk over "tree-sitter's own
  `node.children`, named AND anonymous alike", with
  `check_uniqueness` asserted at build. the id FIELD the walk fills
  is defined in `ur`; the split is generation here, carriage there.
- **the single-owner parsing frontend** — nothing else constructs a
  parser. source: v0 `parse.py` (addendum §1b, ~40 lines:
  Language/Parser construction, API shim, `named_kinds()`
  enumerating the routing surface live from the grammar). the
  N-language generalization of it is the archived `tree_sitter_base`
  design (grammars commit-pinned with provenance manifest; census
  byte-compared for deterministic regeneration; coverage partition
  total) — projected at
  `PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_tree_sitter.md`.
  grammar pinning is upstream of id stability (addendum §1a) and
  this node is its natural owner.
- **the ingress-writer precedent** — type-aware mapping means this
  node is where semantic facts are first in hand. source precedent:
  `PseudoCoup/pseudocoup/ingress/kotlin.py` (the
  tree-sitter walk that wrote both URNodes and ledger registries in
  one pass). settled 2026-08-02, on the definition/instance distinction: this
  node does NOT write ledger entries — it produces UR. the UR →
  ledger derivation is `ur_to_ledger`'s, and the `builder`
  sequences the two through instances it holds as attributes. the
  addendum's one-moment observation (§2.5: the ingest walk is the
  only moment the tree-sitter node and the UR node are both in
  hand) is answered by `ur` carrying the source linkage as node
  fields, so nothing is lost by the hand-off.
- **coverage discipline** — WFL `ingress/coverage.py` recorder +
  justified baseline, v0 `classify.py` total-partition strictness
  (via the `tree_sitter_base` design). per-language sub-modules make
  this the node where "which node kinds does language X produce and
  which do we handle" is measured.

## notes

- renamed from `ts_to_ur_mapper` 2026-08-04 (the owner: "the `x_to_y` is
  fairly descriptive without the need for `x_to_y_<mapping_type>`").
  the co-node lost its suffix the same day, resolving the
  mapper/deriver asymmetry by removing it.
- the working precedent for the single-owner parsing layer is v0's
  `parse.py` frontend (one place constructs parsers; survey addendum
  §1b) and the archived `tree_sitter_base` design (pinned vendored
  grammars, provenance manifest, coverage census). grammar pinning —
  which the addendum names as upstream of id stability (§1a) — has
  no owner in this tree yet; this node is the natural candidate.
