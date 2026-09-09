---
id: pp.framework.progress
status: living
---

# PROGRESS — framework

- 2026-08-05 **done and exercised** (the owner: "i just dont like calling
  python functions in the terminal because ive found very often issues
  with environment and whatever else. bash call is preferable"):
  **`PlanPlan/plan.sh` — one bash entry point** for every
  framework tool.
  - It holds two things only: which interpreter to use, and which tool
    a word maps to. `check`, `dash`, `nodes`, `project`, `adopt`,
    `tree`, `view`, `explore`, `serve`, `migrate`, `which`, `help`.
    Unrecognized flags pass straight through, so a tool gaining an
    option needs no change here.
  - **Interpreter selection is the point.** The framework is standard
    library only, so ANY python3 runs it — which is exactly why "any"
    goes wrong when a machine has several and PATH decides. `plan.sh`
    tries `PLANPLAN_PYTHON`, then `python3`, `python3.13`,
    `python3.12`, `/usr/bin/python3`, `~/anaconda3/bin/python3`, and
    verifies each RUNS at 3.8+ before choosing it. `plan.sh which`
    reports the one selected.
  - **A broken override fails loudly.** First cut let an unusable
    `PLANPLAN_PYTHON` fall through to the next candidate, which would
    silently run a different interpreter than the one asked for and
    hide a typo. Now it stops with the value it was given. That is the
    same half-working failure this framework keeps finding elsewhere,
    caught in its own tooling this time.
  - `hq.sh` gained `tree`, `explore` and `serve`, which call `plan.sh`
    with the line's roots and take a repo NAME rather than a path —
    `hq.sh tree PseudoCoup_v5`. Unknown names are refused with the
    known list printed. HQ still holds sequencing only; the
    interpreter question lives in one place, PlanPlan's.

- 2026-08-05 **done and exercised** (the owner: "can we please resolve it?",
  of the CONFORMANCE GAPS banner): **`generate_nodes.py --adopt-edges`
  and `--adopt-checks`** — the §1 place fields and the §3 CHECK id,
  filled in for trees that predate them.
  - **Why a tree-wide pass is right here**, when §6c warns against
    sweeps and the banner itself says "chain by chain": every value
    written is TRANSCRIPTION of something already true on disk — name
    from the folder, path from where the file sits, super from the
    folder above, sub_nodes from the folders present, CHECK id from
    the node's own id. Nothing is judged. The rule against sweeps
    aims at EDITORIAL passes, where bulk prose edits hide decisions.
    `designation` stays excluded for exactly that reason: it is a
    judgement, and it is still 28 of 60.
  - **Nothing existing is overwritten.** PCv5's hand-written
    cross-repo `super_node` pointing at HQ survived untouched, which
    was the property that had to hold.
  - The superseded inline `nodes:` register is REPLACED when
    `sub_nodes` is written, per §1's "deleted from a node when that
    node is brought over" — not left beside it.
  - Roots additionally get `repo` and `remote`, read off the directory
    name and `.git/config`'s origin url by a small ini reader
    (`git_origin`), keeping the tool standard-library only.
  - **Applied across all five trees**: 60 COREs gained place fields,
    55 CHECK files gained ids. The CONFORMANCE GAPS banner is now
    empty. Warnings fell from 8 to 5.
  - **One real defect surfaced by the adoption, left for the owner**: three
    PseudoIR nodes have ids disagreeing with their folders —
    `pir.rust_llvm_transpile` under `node_0_2_0_0_0_transpile`, and
    the same for `slice` and `insert`. The chain already says
    `rust_llvm`, so the id says it twice. Renaming is a naming call,
    and PseudoIR is deferred until that tree is restructured (the owner,
    2026-08-05: "we can just leave PseudoIR and PCv6 for now").

- 2026-08-05 **done and exercised** (the owner: "we should probably have
  something to make mass updates to all PlanPlan infrastructure"):
  **`migrate.py` built — the first tool for changes that span every
  repo using the framework.**
  - **The gap it fills.** `generate_nodes.py --rename-field` handles
    ONE frontmatter key. Anything wider — an address scheme, a
    filename grammar, a heading — had no tool, so it meant hand
    editing hundreds of files across five repos. That is how a
    migration ends up half-applied, and a half-applied migration is
    worse than none: the checks then describe a state nobody intended.
  - **Four surfaces, in a fixed order**, so a partial run leaves
    something the checks can describe: text inside files, then
    filenames, then folders deepest-first (a parent rename cannot
    orphan a child), then nothing else.
  - **Dry run is the default**, matching every other tool here.
  - **Patterns are anchored to the grammar prefixes** — `node_`,
    `CORE_`, `CHECK_`, `SUPPORT_`, or a `CORE <chain>` heading. Tested
    on a synthetic tree: prose reading "version 1_0 of the spec is
    unrelated" was left untouched while every real address moved.
  - **Code is reported, not rewritten, by default**; `--include-code`
    folds it in once a person has read the list. On the first real run
    that list was 18 files, and reading four of them was what showed
    they were all planning-path references — including
    `PseudoCoup_v5/hub/__init__.py`'s `_HUB_PLAN` constant, which
    would have dangled silently under a hand migration.
  - **Bare constants never match, in either mode** — `return "1"`,
    `CHAIN = "1_0"`. Those need a human decision, so they stay
    invisible to the tool on purpose, and the docstring says to grep
    for them separately when a migration changes what they mean.

- 2026-08-05 **done and exercised** (the owner: "why does node indexing start
  at 1? CORE_0. its sub_nodes start their indexing at `node_1_0`
  instead of `node_0_0`"): **the leading address segment is now 0**,
  so the root's own numbering and its children's addresses agree.
  - **There was no reason for the 1.** Measured before changing
    anything: every node folder in all five trees began with `1` — the
    segment carried no information. The tools derive level as
    `segments - 1` (`sub_chain.count("_")` in `generate_nodes.py`,
    `len(chain.split("_")) - 1` in `checks.py`), so the leading
    segment existed only to make that arithmetic work.
  - **What was actually wrong:** the root was numbered by LEVEL in its
    own filename (`CORE_0`, level 0) and by POSITION in its children's
    addresses (`node_1_...`, root = 1). Two schemes meeting at one
    node. PROTOCOL §1 stated the shape and the intent ("the same
    positional-path identity design as idgen's node ids") but never
    the reason for the mismatch, and no ruling existed.
  - **Executed by `migrate.py renumber-root`** over all five repos:
    310 text files edited, 144 files renamed, 88 folders renamed, in
    one dry-run-then-apply. `chain_of` and `node_chain` now return
    `"0"` for the root; both docstrings carry the reason.
  - Verified after: 0 errors across all five trees, 59 dashboards
    regenerated, projections already matching their registers. The
    only remaining `node_1_` strings are inside `__pycache__`
    binaries, which regenerate.
  - Ids are untouched, as PROTOCOL §1 promises — addresses are
    navigation, `id` is identity. Nothing joined on an address.

- 2026-08-05 **done** (the owner: "`## components` is awkwardly close to
  `## sub_nodes`. i dont even know what purpose `## components`
  serves"): **`## components` removed; `## design` stated in the
  grammar as PROTOCOL §1b.**
  - **How it got used at all, which is the part worth keeping.** The
    name was never in PROTOCOL. It existed only as a special case in
    `render_plan.py` (`OPEN_SECTIONS = {"components"}`) — and that was
    enough for a CORE to be written using a section the grammar had
    never defined. A tool implying grammar is how vocabulary enters
    without a ruling.
  - §1b now states the three section names a tool relies on —
    `## sub_nodes`, `## definition`, `## design` — and says what
    `## design` is FOR: a node's own internal structure, one level
    below its definition, sitting BESIDE the `realize: false` register
    entries rather than instead of them. The register says what the
    parts are; `## design` says how they fit.
  - `render_plan.py` opens `## design` and no longer knows the word
    "components". Two PCv5 COREs using it —
    `pcv5.tools.ledgerer.builder` and `pcv5.tools.ledgerer.ur` — were
    renamed.
  - **NOT swept**: three PCv6 COREs still carry `## components`
    (`node_0_2_api`, `node_0_0_tools/node_0_0_1_transpiler`,
    `node_0_0_tools/node_0_0_0_ledgerer`), as do two archived draft
    copies under PCv5's `ur`. Per §6c the rename happens when those
    chains are descended into, not by a pass over the tree. Nothing
    breaks meanwhile — the section renders closed instead of open.

- 2026-08-05 **done and exercised** (the owner: "does PlanPlan include an
  archive folder protocol? i want to be able to temporarily place
  files in an archive folder"): **`.archive/` is now stated grammar,
  PROTOCOL §1c**, with a check behind it.
  - The behaviour already worked — every folder walk drops dotted
    directories, so an archived file is not a stray, not a second
    CORE, not a node. What was missing was the RULE: name, scope,
    purpose, and the case.
  - **Lower case `.archive`**, matching the convention already on disk
    in PseudoCoup_v6 and PlanPlan.
  - **New `ArchiveNameCheck` (WARN).** Case matters to exactly one
    other check: `StaleArchiveCheck` finds archived material by the
    name `.archive`, so a `.ARCHIVE` is skipped by every walk AND
    invisible to the check that should read it — half-working in the
    worst way. The new check names it rather than letting it pass.
  - Exercised: fires on a planted `.ARCHIVE`, silent on `.archive`,
    and the five real trees stay at 0 errors with no new warning.
  - Two `.ARCHIVE` folders under `pcv5.tools.ledgerer.ur`'s new
    sub-nodes were renamed to `.archive`; their contents (draft CORE
    copies) were preserved.

- 2026-08-05 **done and exercised**: **`repo_dir_of` now finds the repo
  by walking up to the nearest `.git`**, falling back to the old rule
  (first path segment under `~/Programming`) for a tree not in git.
  - **The defect it fixes, and it was not cosmetic.** The old rule
    ASSUMED every planning tree lives under `~/Programming`. Read from
    anywhere else it returned `None`, `want_path` degraded to the bare
    filename, and **every** `node.path` in the tree was reported wrong.
  - Found by running the checks through the podman sandbox, where the
    repos are bind-mounted at `/projects`: **64 errors there against 0
    on the same trees at their usual paths.** Anyone cloning these
    repos to a different directory would have hit the same wall, which
    is why this belongs in PlanPlan rather than in a caller — it is
    wrong for any project, not just this line.
  - Verified three ways: real paths still report 0 errors, 4 warnings
    (unchanged); the same tree reached through a symlink at `/tmp/mnt`
    reports no `node-self-path` errors; in the container the count went
    64 -> 0.
  - The 63 errors still reported inside the container are
    `dangling-path` on `...` prose references, which
    genuinely do not resolve there because only four directories are
    mounted. That is the `$HOME`-mapping limitation already recorded in
    the toolchain notes, not this defect.

- 2026-08-02 **done and exercised** (the owner: "yes, that works!", settling
  the key's name): **`realize: false` register entries** — structure
  of a node that stays inside the node's own file (attributes,
  methods), registered in `sub_nodes` without becoming a folder.
  PROTOCOL §1 carries the rule; the word is the framework's own
  register->folders verb, chosen over `inline` because it names the
  rule rather than a metaphor (alternatives weighed: `in_file`,
  `folder: false`).
  - Semantics: the entry consumes its address slot (graduation —
    delete the key, run the generator — renumbers nothing); carries
    `name` and optionally `designation`, never `path`; the generator
    skips it; the projection lists it unlinked with a
    `*(realize: false)*` marker; `designation` is allowed only on
    these entries, since a realized node states its own. A register
    does not nest inside an entry — an unrealized entry is a leaf,
    and needing children IS the graduation moment.
  - Enforced both ways: a `path` on an unrealized entry is malformed
    (as is `realize:` set to anything but false), and a folder
    existing under an unrealized entry's name is a nodes-register
    ERROR — the entry says in-file, the disk says folder.
  - Exercised on a synthetic tree: the entry consumed slot 0 and the
    realized sibling generated at slot 1; a planted folder under the
    unrealized name was reported by name; a planted `path` on the
    entry read back malformed. One reader fact surfaced:
    `read_frontmatter` keeps scalars as raw strings, so `false`
    arrives as `"false"` — normalized to the boolean once, in
    `parse_edge`, not at call sites.
  - First real instance: `pcv5.tools.ledgerer.builder` registers its
    four attributes and two methods as unrealized entries.
- 2026-08-02 **done and exercised** (the owner: "which im just realizing is
  still named `## nodes` instead of `## sub_nodes` to match the
  YAML"): **the projection heading renamed `## nodes` →
  `## sub_nodes`**, so the heading carries the same name as the
  register it projects. Passed the hats test: right for any project
  using PlanPlan, not only this line.
  - Both names live in `schema.py` (`Sections`); the superseded form
    follows the same contract as the `nodes` frontmatter key — still
    recognized while trees migrate, and the projection rebuild WRITES
    the current form, so `--projections --apply` is the whole
    migration for a tree. PROTOCOL §1 updated; the owner's quoted rulings
    keep the word he used, annotated.
  - Migration run the same day over all five trees (HQ, PCv5, PCv6,
    PseudoIR, PlanPlan): 56 COREs now carry `## sub_nodes` first;
    `check_plans.py` after: 0 errors.
  - Two defects found and fixed in `generate_nodes.py` on the way:
    the CORE skeleton still emitted the superseded frontmatter
    (`nodes: []`, no `node`/`super_node`/`sub_nodes` edges) — it now
    emits the §1 edges; and `definition_line` skipped only the FIRST
    line of a wrapped pending placeholder, so a fresh skeleton's
    placeholder continuation was projected into its super's listing
    as a garbage description. Caught live on the ledgerer chain's
    four new nodes; the placeholder's whole paragraph is now skipped.
- 2026-08-02 **done and exercised**: four changes the owner settled in one
  exchange, taken in the order that stopped each from invalidating the
  next.
  - **`description` renamed to `name`** in every edge entry — 26 keys
    across 14 COREs, plus the tools and the PROTOCOL examples. `name`
    rather than `title` because `plan_and_code.md` §1 settles that a
    node carries the object's NAME, and because `read_core` already
    returns `title` for the `# CORE 0_0 — tools` heading, so `title`
    would have meant two things in one parser. The canonical folder
    grammar was restated from `node_0_0_<description>` to
    `node_0_0_<name>` at the same time; the one survivor is the owner's
    quoted ruling in §3b, which keeps his word with a note beside it.
  - **`node` added** — what a CORE says about itself, in an edge's
    shape. Every value is checked against something already true on
    disk, so a CORE copied or moved and not re-homed stops agreeing
    with its own folder. `repo` and `remote` sit on a tree root only,
    because below it they are derivable by walking `super_node` up —
    the same rule that keeps them off in-repo edges. Exercised with
    four planted defects: a wrong `name`, a `path` naming another
    node's file, a root `repo`/`remote` disagreeing with the directory
    and with `.git/config`, and `repo` carried below a root. All four
    reported; the real files were restored and diffed.
  - **Corrected the same day, and the correction is the interesting
    part.** The first version checked `name` against the folder's name
    segment. A tree root's folder is `Planning` and has no such
    segment, so the comparison skipped roots — the owner read `name: pcv5`
    beside `path: CORE_0.md` and said it looked like a bug, and
    `name: banana` on PCv5's root did in fact pass with 0 errors.
    - The field had also been given two meanings without anyone
      writing that down: the folder segment below a root, the `id` at
      one, because there was nothing else to use.
    - The rule now is `name` == the last segment of `id`, which holds
      at every level (`pcv5` -> pcv5, `pcv5.tools` -> tools,
      `pcv5.tools.ledgerer` -> ledgerer), with the folder comparison
      still run below a root. Two comparisons, one meaning.
    - Re-exercised on both halves: `name: banana` on a root is now an
      ERROR naming the id it should have ended in, and a node whose
      `id` and `name` agree with each other but not with the folder is
      still caught by the folder half.
  - **`node.path` corrected the same day, from a filename to a path.**
    the owner: "bug: `path` is the document file name, instead its file
    path." It held `CORE_0.md`, which locates nothing, in the one
    field whose purpose is a node saying where it is.
    - It is now relative to the REPO root —
      `Planning/node_0_0_tools/CORE_0_0_tools.md` — which is a
      different convention from `super_node.path` and
      `sub_nodes[].path`, both relative to the stating node's folder.
      The difference is not an oversight: an edge points at another
      document from where it stands, while `node.path` answers "where
      is this document" and has no standpoint to be relative to.
    - Repo-relative rather than absolute because `repo` and `remote`
      exist so a reference survives the repo being cloned somewhere
      other than `~/Programming`; an absolute path would undo that.
    - Exercised: the old bare-filename form is now reported, and so is
      a wrong-but-plausible path — `Planning/node_0_1_research/CORE_0_0_tools.md`
      for a file that sits in `node_0_0_tools`.
  - **`nodes` retired on the conformed chain.**
    `PlanningNode.register_of` is now the single place anything asks
    what a CORE registers — `sub_nodes` when present, `nodes` when not
    — so the five chain COREs could drop the old field with the
    register still resolving to the identical lists.
  - **`schema.py` written**, naming every field once for the tools,
    with `--rename-field` in `generate_nodes.py` for the documents.
    Exercised on a copy of PCv5's tree: dry run listed 18 sites in 8
    files and wrote nothing; `name` was renamed to `label` and back
    with `--apply`, and the result diffed byte-identical to the
    original.
  - The honest limit is recorded in `schema.py`'s own docstring and in
    PROTOCOL §3: YAML anchors resolve inside one document only, so a
    document can never take its keys from a central file. One place
    for the behaviour, one command for the files.

- 2026-08-01: node folder generated by
  `PlanPlan/framework/generate_nodes.py` from the
  `nodes` register of `PlanPlan/Planning/CORE_0.md`. Skeleton only — definition,
  designation, and content pending.
- 2026-08-01: deepened to four sub-nodes — protocol, planning_model,
  checks, tools — with the four entry points under tools. structure
  approved by the owner ("yeah sure, great"), names placeholders.
- 2026-08-01 **done: the restructure.** `planning_model.py` and
  `checks.py` built; `check_plans.py` is a thin entry point;
  `render_plan.py` renders and is imported by nobody; the two
  generators import parsing from the model.
  - behaviour pinned: 18 planted-defect variants captured before and
    after — identical output modulo two pre-existing sources of
    randomness (a tmpdir basename and the renderer's live timestamp),
    both normalized, neither introduced by the change.
  - also verified after: combined five-tree check 0 errors 6 expected
    warnings; `--projections` dry reports nothing to rebuild;
    `--check` says 52 dashboards current and a double run is
    byte-identical; renderer HTML byte-identical modulo timestamp;
    no file imports `render_plan`.
