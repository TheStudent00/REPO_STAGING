---
id: pcv5.tools.ledgerer.progress
status: living
---

# PROGRESS — ledgerer

- 2026-08-04 (the owner: "the `x_to_y` is fairly descriptive without the
  need for `x_to_y_<mapping_type>`"): **the two boundary modules
  renamed** — `ts_to_ur_mapper` → `ts_to_ur`, `ur_to_ledger_mapper` →
  `ur_to_ledger`. The rename resolved the mapper/deriver asymmetry
  raised the same day by removing suffixes entirely; the deriver
  framing (UR → ledger is DERIVATION, not format conversion) moved
  into `ur_to_ledger`'s definition text. `deriver` was the candidate
  name; `connector` was rejected because that word is reserved for
  the static graph object.
  - Same-day sharpening from the merge questions the owner raised (recorded
    in `<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/log_005_session_state_macros_and_sequencing.md`
    §3): one DATA MODEL — `ur` is the vocabulary, `ledger` is the
    mechanics over it (keying, durability, merge), and the ledger
    defines no second vocabulary. The nodes stay separate because
    lifecycle differs, not representation.
  - Mechanics note: the folder renames ran just before the session's
    shell died, so only their output was lost — verified 2026-08-05
    through the podman lane, which found exactly the five expected
    folders, one CORE and one CHECK in each, ids matching folders, and
    the register agreeing with disk. No host cleanup was needed.
    Checks re-run the same day: **0 errors** across all five trees.

- 2026-08-02: **metaprogramming settled as a design direction**, written
  to this node's `SUPPORT_metaprogramming.md`, with the measurements and
  the wrong turns in
  `<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/log_003_metaprogramming_model.md`.
  - **The position**: meta-programming is code, held losslessly like any
    other code. REPRESENTATION is always possible; EVALUATION —
    computing what one call produces — is a separate operation the
    ledger does not require. A ledger holding the invocation, the
    definition, and the connector is already a complete record of the
    source; expansion is a derived view.
  - **Rust is the tip of the spear** because it is the most opaque of
    the targets, not merely the first. A model that holds Rust's macros
    holds the C preprocessor and Python's decorators, which operate on
    parsed material rather than raw tokens.
  - **The selection rule for when evaluation is needed**: does the
    expansion create names other code refers to. Not how often the
    macro appears. Measured: `assert_eq!` is invoked 427 times and
    creates nothing nameable, while `math_builder_methods!` is invoked
    twice and creates ~27 methods including `sdiv` — the operation the
    rust_routing work traces. A frequency ranking puts the one that
    matters at the bottom.
  - Two runnable demonstrations were written and kept:
    `<WORKSPACE_DIR>/PseudoCoup_v5/Research/macro_demo.py` (what a macro
    is) and `<WORKSPACE_DIR>/PseudoCoup_v5/Research/macro_engine.py` (the
    operator itself — one engine, macros supplied as data).
  - Four open items are recorded in the SUPPORT file's §8, the sharpest
    being that toolchain expansion is per crate while the ledgerer is
    per file.

- 2026-08-02 **done**, third revision of the day (the owner: "ah yeah
  attribute. youre right! yeah the definition of the module doesnt
  make sense to be within a class"): **the definition/instance
  distinction settled, and the tree reshaped by it.** definitions
  are nodes; instances are attributes. so: `ts_to_ur_mapper` moved
  back up from under the builder to `ledgerer` level (the
  definition site), a new sibling `ur_to_ledger_mapper` extracted
  from the builder (symmetric mappers, one per boundary), and the
  builder became a LEAF `code (class)` whose CORE carries a
  `## components` structural overview — `Builder`'s attributes are
  instances of the four siblings' classes; no `code (instance)`
  designation was invented, because `attribute` (settled 2026-07-31)
  already names a held instance.
  - the overview-as-section was chosen over attribute sub-nodes
    (both conform, per the "either" precedent for rules inside code
    nodes); switching later is cheap.
  - addresses now: ur 0, ledger 1, ts_to_ur_mapper 2,
    ur_to_ledger_mapper 3, builder 4. the owner pushed before the
    restructure, so the previous shape is in version control.
- 2026-08-02 **done**, later the same day (the owner: "we are in agreement
  include `builder`. proceed"): **the flat four restructured to
  three, with the mapper nested** — `ur`, `ledger`, `builder`, and
  `ts_to_ur_mapper` now the builder's sub-node. `ledger_master` was
  renamed `builder` (the `ledgerer.ledger_master` repetition was the
  awkwardness; `builder` is the harvest's own verb —
  `ledger_unified.build`) and refined to `code (class)`: ledgerer
  calls funnel through it, so it holds the ledger-under-construction
  as state. the funnel dissolved one open placement — who writes
  ledger entries during the walk is now internal sequencing of the
  builder, a code-depth decision — and leans the second (`--check`)
  toward the builder, where it is placed.
- 2026-08-02: **the node deepened to four sub-nodes, from the owner's rough
  draft** ("not stuck on the names, just rough drafts"): `ur`,
  `ledger`, `ts_to_ur_mapper`, `ledger_master`, in that address
  order, all `designation: code (module)`, all `status: draft`.
  Registered in this CORE's `sub_nodes`, realized by
  `generate_nodes.py --apply`, definitions written from the owner's
  descriptions with his founding notes kept in each CORE's
  `## notes`.
  - Names were lower-cased from the draft's `UR` and
    `TS_to_UR_mapper` per `plan_and_code.md` §1 (node names are valid
    identifiers, lower case) — the tool refuses uppercase register
    entries.
  - The draft's note on `ledger` ends mid-sentence ("the ledger has
    carrying capacity beyond with the ability to "); the fragment is
    kept verbatim in that CORE's notes, marked as awaiting the owner's
    completion. Nothing is built on it.
  - Material behind the shape: the 2026-08-02 survey addendum
    `<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/ledger_survey_2026-08-02_tree_sitter_ur_ast.md`
    (tree-sitter enters at identity and ingestion, not storage; the
    UR-AST/ledger join exists in spec, not code) and
    `<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/log_001_ledgerer_harvest_findings.md`
    (the nine harvested parts).
- 2026-08-01: node founded, definition only, as one of the four
  sub-nodes the owner ruled for under `pcv5.tools` (ledgerer, transpiler,
  polyfill, tracer — tracer a sibling, not a part of this node).
  designation `code (object)` per the coarse kind added to PROTOCOL
  §3a the same day; refines to module or class before this node
  settles.
- 2026-08-02 **done** (the owner: "we can change it to module and change it
  later if we need"): designation refined from `code (object)` to
  `code (module)`, which clears the §3a settle-guard that would have
  blocked this node from ever reaching `status: settled` while it
  carried the coarse kind.
  - The refinement is allowed to be revisited. §3a calls this
    refinement rather than contradiction, so §2's governance rule is
    not strained by changing it again later.
  - The supporting statement, found in
    `<WORKSPACE_DIR>/PseudoCoupHQ/plan_and_code.md` §1, is an
    ILLUSTRATION rather than a ruling: its worked example shows
    `node_0_0_0_ledgerer` as `code (module)` holding a `Ledger` class
    with a `build` method, reading as `ledgerer.Ledger.build`. It
    carries no date and no attribution, unlike the rulings around it.
