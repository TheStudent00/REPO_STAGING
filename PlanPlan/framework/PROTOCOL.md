---
id: framework.protocol
level: 0
status: draft
settled_by: the owner
supersedes: null
---

# Planning Framework — Protocol

Status: DRAFT — settles by the owner's review. Terminology throughout:
**super-sub** / **higher-lower**, never parent-child.

## 1. Structure: depth is nesting, every level complete

The grammar (the owner, 2026-07-28): a folder at level N contains
`{files and folders}` at level N+1 — and among its files, exactly
ONE core file describing that branch at that level.

- **CORE file** — exactly one per folder, always markdown. It
  describes its branch at its level and hyperlinks down into the
  sub-folders. At level 0 this is `CORE_0.md` (core objectives
  only, readable in a minute).
  - **Three frontmatter fields register a node's place in the tree:
    `node`, `super_node` and `sub_nodes`** (the owner, 2026-08-02). Every
    CORE carries all three. Together they are the only statement of
    where a node sits; no prose sentence is a substitute for any of
    them.
  - **`node` is what the CORE says about ITSELF**, in the same shape
    as an edge. Added because a CORE could name the repo ABOVE it
    through `super_node.repo` and say nothing about the repo it was in
    (the owner, 2026-08-02: "PCv5 seems to lack awareness of its own repo
    but the `super_node` is aware").

    ```yaml
    node:
        name: ledgerer
        path: Planning/node_0_0_tools/node_0_0_0_ledgerer/CORE_0_0_0_ledgerer.md
    ```

    - Every value in it is checked against something already true on
      disk, so the redundancy is self-policing in the same way the two
      ends of an edge are. A CORE copied from another node, or moved
      and not re-homed, stops agreeing with its own surroundings —
      the defect the SUPPORT-file id rule exists to catch, now caught
      for COREs too.
    - **`name` is the last segment of `id`, at every level**, and
      below a tree root it must equal the folder's name segment as
      well. Both comparisons run: the id says what the node is called,
      the folder says where it lives, and a name matching one but not
      the other is precisely the moved-and-not-re-homed case.
      - Corrected 2026-08-02, hours after the field was added, because
        the owner read `name: pcv5` beside `path: CORE_0.md` and said it
        looked like a bug. It was. A tree root's folder is `Planning`,
        which has no name segment, so the folder comparison skipped
        roots entirely — `name: banana` on PCv5's root passed with 0
        errors — and the field silently meant the folder segment below
        a root and the id at one.
    - **`path` LOCATES the file, and it is relative to the REPO
      root** — not to the node's own folder, which is how
      `super_node.path` and `sub_nodes[].path` resolve. Two
      conventions in one file, and the reason for the difference is
      that an edge points at another document from where it stands,
      while `node.path` answers "where is this document" with no
      standpoint to be relative to.
      - Repo-relative rather than absolute because `repo` and `remote`
        exist so a reference survives the repo being cloned somewhere
        other than `~/Programming`. An absolute path in the same field
        would undo that.
      - Corrected 2026-08-02, after the owner: "bug: `path` is the document
        file name, instead its file path." It held a bare filename —
        `CORE_0.md` — which locates nothing, inside the one field
        whose purpose is a node saying where it is.
    - **`repo` and `remote` sit on a TREE ROOT only**, where they are
      checked against the containing directory and the `origin` url in
      that repo's `.git/config`. Below the root they are derivable by
      walking `super_node` upward, and the rule against storing a
      derivable fact is the same one that keeps them off in-repo
      edges. Carrying them lower down is reported.

    ```yaml
    node:
        name: pcv5
        path: Planning/CORE_0.md
        repo: PseudoCoup_v5
        remote: https://github.com/<owner>/PseudoCoup_v5.git
    ```
  - **`sub_nodes` is a sequence of mappings**, in address order — the
    i-th entry IS sub-node `<address>_<i>`. A leaf carries the
    explicit empty form `sub_nodes: []`.

    ```yaml
    sub_nodes:
        - name: ledgerer
          path: node_0_0_0_ledgerer/CORE_0_0_0_ledgerer.md
        - name: transpiler
          path: node_0_0_1_transpiler/CORE_0_0_1_transpiler.md
    ```

  - **A register entry may state `realize: false`** (the owner, 2026-08-02):
    structure of the node that stays inside the node's own file — an
    attribute or method planned as structure, not worth a folder. The
    word is the framework's own verb for register -> folders
    ("realized", "unrealized"), chosen over `inline` because it names
    the rule rather than a metaphor.

    ```yaml
    sub_nodes:
        - name: ts_to_ur_mapper
          designation: code (attribute)
          realize: false
        - name: build
          designation: code (method)
          realize: false
    ```

    - The entry CONSUMES its address slot — the i-th entry is still
      sub-node `<address>_<i>` — so graduating it later renumbers
      nothing. Graduation is mechanical: delete the key, run the
      generator, the folder appears at the reserved address.
    - It carries `name` and optionally `designation`, and **no
      `path`** — there is no file to locate. The pairing is enforced
      both ways: a path on an unrealized entry is malformed, and a
      folder existing under an unrealized entry's name is reported (the
      entry says in-file, the disk says folder; only one can be right).
    - `designation` is allowed ONLY here. A realized sub-node states
      its designation in its own CORE, and stating it in the register
      too would be one fact in two places.
    - The generator skips these entries; the projection lists them
      unlinked, with the designation and a `*(realize: false)*` marker.
    - An unrealized entry is a LEAF by definition. The moment it needs
      children is the graduation moment — a register does not nest
      inside a register entry.
  - **`super_node` is a single mapping**, or `null` at a tree that
    hangs under nothing.

    ```yaml
    super_node:
        name: tools
        path: ../CORE_0_0_tools.md
    ```

  - **An edge that leaves the repo carries `repo` and `remote`
    alongside `path`** (the owner, 2026-08-02: "oh okay yeah that works!").
    A `...` path assumes that layout exists on the
    machine reading it, and cloning one repo alone already produces
    references that resolve nowhere. The repo name and its remote make
    the edge followable without that assumption.

    ```yaml
    super_node:
        name: projects
        path: PRIVATE/PseudoCoupHQ/Planning/node_0_0_projects/CORE_0_0_projects.md
        repo: PseudoCoupHQ
        remote: https://github.com/<owner>/PseudoCoupHQ.git
    ```

    Entries that stay inside the repo carry `path` only. Adding `repo`
    and `remote` to them would state the containing repo on every node
    in every tree, which is the same fact stored several hundred times.
  - **Every edge is therefore written at both of its ends**, and the
    two statements can be compared. When `A.sub_nodes` names B, then
    `B.super_node` must name A; a tool reports it when only one end
    states the edge, or when the two name different files. This is
    what makes a misattached node detectable rather than merely
    wrong.
  - **`co_nodes` is deliberately NOT a field** (the owner, 2026-08-02):
    "co_nodes are discoverable within two steps." Two nodes sharing a
    super-node are co-nodes, and finding them is one step up and one
    step down — `PseudoCoup_v6` and `PseudoIR` are reached from each
    other through `hq.projects`. A field would store what the two
    existing fields already imply.
  - **`super_node` is always writable, because a node is created after
    the node above it** (the owner, 2026-08-02): "a node is created after its
    super_node." So there is no moment in a tree's construction when a
    node exists and cannot state what it hangs under.
  - **Superseded 2026-08-02: the single inline `nodes: [a, b]` field.**
    It held sub-node titles only, with the path derived from position,
    and it could say nothing about what was above a node or about
    anything in another tree. The reason recorded for the inline form
    on 2026-08-01 — one line, no indentation rules, nothing to
    interpret — was never the owner's own preference (2026-08-02: "i didnt
    actually come up with that idea. i didnt like it when i saw it but
    i wanted to move on with other things"). The cost it now carries is
    real and named: **the frontmatter reader must be rewritten**,
    because `PlanningNode.read_frontmatter` splits the block into
    `key: value` lines and would read a multi-line entry as a set of
    unrelated top-level fields, silently and with no error.
    - **How the two are reconciled while both exist.**
      `PlanningNode.register_of` is the one place anything asks a CORE
      what it registers: `sub_nodes` when present, the old `nodes`
      when not, counting only the IN-TREE entries either way. Every
      tool goes through it, so no tool holds an opinion about which
      field is authoritative.
    - **The field is DELETED from a node when that node is brought
      over**, not swept out of every tree at once. The five nodes on
      the first conformed chain no longer carry it; the other 35 still
      do. `register_of`'s fallback goes when the last one does.
    - Where a node carries both, they are compared and a disagreement
      is reported. One fact in two places is the drift this framework
      exists to prevent, and comparing them is what keeps the overlap
      survivable while it lasts.
  - **Why YAML and not the markdown section** (the owner, 2026-08-01):
    markdown headings cannot be trusted without an intelligent
    parser — `## like this` inside a fenced code block is a comment,
    not a section, and there will be other exceptions. The
    frontmatter is a closed little language, and when something is
    wrong in it, it is OBVIOUS.
  - **The entry key is `name`, renamed from `description` 2026-08-02**
    (the owner: "i dont like the use of `description`. do you think title or
    name might be better?"). `name` rather than `title` for two
    reasons. `plan_and_code.md` §1 settles that a node carries the
    object's NAME — "not a description of it, not a synonym — the
    name" — so the segment was never a description in the first place.
    And `title` is already taken: `PlanningNode.read_core` returns
    `title` for the `# CORE 0_0 — tools` heading line, so reusing it
    here would give one word two referents inside one parser.
    - **The folder grammar was restated with it.** The canonical shape
      block in this section wrote `node_0_0_<description>` while the
      register prose and every tool said "title" — one segment with
      two names, which §5 forbids. It is `<name>` in all three places
      now. The one survivor is the owner's quoted ruling in §3b, which keeps
      the word he used, with a note beside it.
  - **Why a sequence of mappings rather than a dictionary.** Address
    order is load-bearing — the i-th entry IS sub-node `<address>_<i>`
    — and a YAML mapping is defined as an UNORDERED set of unique
    keys, so key order is preserved by implementations rather than
    promised by the format. A sequence orders by definition, and it
    also has room for `repo` and `remote`, which a one-key-one-value
    dictionary does not.
  - **Generation runs one way: YAML register -> folders -> `## sub_nodes`**
    (the owner, 2026-08-01, as generalized policy). Nothing derives the
    register from the markdown. The one exception is ADOPTION, a
    supporting tool for trees that predate the rule:
    `generate_nodes.py <root> --adopt` reads the sub-node folders on
    disk and writes the register describing them, once, then rebuilds
    the projections. It refuses to overwrite a register that exists.
    Adoption describes what is already there; it makes no judgement,
    which is why it can be mechanical where `designation` cannot.
  - **A missing register, a missing `## sub_nodes` (either heading
    form), or one out of first position is reported LOUDLY** (the owner, 2026-08-01: "it
    should be loud about that gap"). `check_plans.py` ends its report
    with a per-tree CONFORMANCE GAPS banner naming the counts and the
    adoption command. The banner does not affect the exit code: these
    trees predate the rule, and refusing every commit until they
    conform would be the sweep §6c warns against.
  - This does not put the markdown beyond checking (the owner, 2026-08-01):
    "we can still automate checks that `## nodes` match the YAML. i
    just dont want `## nodes` to be ground truth." `check_plans.py`
    checks the section for existence, for first-section position, and
    for agreeing with the register — it never reads it for truth.
  - **A generated node carries no `designation`** (the owner, 2026-08-01):
    "we are already forced to do work by-hand within the generated
    deeper level anyway, might as well do designation filling then.
    and the analysis of the tree would reveal designations anyway so
    its not opaque." So the skeleton omits the field, the
    missing-designation warning names it, and the judgement is made
    where the definition is written. Deducing it would be guessing at
    the one field §3a says is a judgement.
  - **The register is the generation seed.** `generate_nodes.py`
    reads `sub_nodes`, diffs it against the sub-node folders on disk, and
    generates the folders and skeleton COREs (plus PROGRESS and
    CHECK) for entries not yet realized — dry run by default,
    `--apply` to write. An
    entry with no folder is therefore not a defect — it is a
    sub-node planned and not generated — and the tools report it as
    exactly that. A folder the register does not name IS a defect
    (unreachable top-down).
  - **The `## metadata`, `## super_node`, and `## sub_nodes` sections are PROJECTIONS of the register**,
    kept for the human reader, and they come IMMEDIATELY after the
    title: **nothing sits between the `# CORE` line and
    `## metadata`** (Updated 2026-08-23: to make YAML scalar properties visible in Markdown preview, the generator now projects `id`, `status`, `designation`, etc., into a `## metadata` block which immediately precedes `## super_node` and `## sub_nodes`). This supersedes the 2026-07-31 form, which
    allowed a definition line between title and listing — that
    position fell because the definition was prose in an unmarked
    place a parser could only find by convention.
    - **The heading was renamed from `## nodes` 2026-08-02** (the owner),
      to carry the same name as the `sub_nodes` register it projects
      — the heading and its source should not be two names for one
      thing. Same migration contract as the `nodes` frontmatter key:
      the superseded heading is still recognized while trees are
      brought over, and the projection rebuild WRITES the current
      form, so `generate_nodes.py <root> --projections --apply` is
      the whole heading migration for a tree. Both names live in
      `schema.py` (`Sections`).
    - **It begins with a standalone `## super_node` section** (added 2026-08-23). To make
      tree navigation explorable backward from within the markdown viewer, the
      projection automatically extracts the `super_node` mapping from the
      frontmatter and renders it immediately preceding `## sub_nodes`.
  - **The definition lives in `## definition`**, the section after
    `## sub_nodes` (the owner, 2026-08-01, choosing it over a YAML field
    and over dropping definitions). Each `## sub_nodes` entry's name
    comes from the register; its one-line description is the first
    sentence of that sub-node's `## definition` — so no fact lives
    twice.
  - The projection is generated content (same contract as
    DASHBOARD.md): `generate_nodes.py --apply` rebuilds it for any
    CORE it generates under, `--projections` rebuilds every
    projection in a tree, and a section out of position — or prose
    stranded above `## sub_nodes` — is MOVED to its place rather than
    reported. A skeleton sub-node whose definition is still pending
    appears as a bare link; the description arrives the next time a
    projection rebuild touches that CORE after the definition is
    written.
  - Why it is a rule and not a preference: the tree is how the plan
    is navigated, and a reader who has to scroll past prose to find
    out what is beneath a node is being made to read the branch
    before they can choose it. Putting the listing first means every
    CORE answers "what is under here" in the same place, so
    descending is uniform at every level.
  - `render_plan.py` reports a CORE whose first section is not the
    sub-node listing; `check_plans.py` reports a CORE missing the
    section or holding it out of position, and lists entries whose
    folders do not exist yet (the generation seed).
- **SUPPORT files** — zero or more per folder, any type (markdown,
  Python, HTML, PDF, ...). Supporting material for that branch;
  never the branch's description. Three rules, each of which exists
  because breaking it cost a day (2026-07-31):
  - Its `id` is its node's id plus `.support.<name>`. A SUPPORT file
    whose id names a different node is a file that has been moved
    and not re-homed.
  - Its filename, its id's last segment, and its `# SUPPORT — <name>`
    heading all say the same name. Renaming one and not the others
    is how a title everyone agreed to kill survives inside the file
    that was renamed to kill it.
  - Its node's CORE lists it. A SUPPORT file no CORE mentions is
    unreachable by anyone reading the plan top-down.
- **PROGRESS.md** — exactly one per node folder (added by the owner,
  2026-07-28): a LIVING file recording implementation progress of
  that node's plan, so it is never a mystery where the project
  planning was left off. Uniform literal name `PROGRESS.md` in
  every node. Each planned item carries a status — planned /
  in-progress / done / blocked(on what) / deferred — with dates
  and links to evidence (reports, tool folders, commits). Updated
  AT THE MOMENT progress happens, same rule as agent memory: a
  status that exists only in conversation is lost. CORE says what
  the branch IS; PROGRESS says where its implementation STANDS.
- **CHECK file** — exactly one per node folder (the owner, 2026-07-31).
  It carries frontmatter like every other authored file in the folder,
  with `id: <node id>.check` (the owner, 2026-08-02); see §3.
  The node's test. It sits at the same level as that node's CORE and
  **mirrors its name with any extension**: beside
  `CORE_0_0_tools.md` sits `CHECK_0_0_tools.<ext>`. The extension
  carries what kind of check it is — `.md` for a by-hand check, `.py`
  for a runnable one. Why the name mirrors rather than being free:
  the same reason a SUPPORT file's name, id and heading must agree —
  a check whose name does not track the thing it checks survives a
  rename and then silently checks something else. **Exactly one per
  node folder, and enforced**: `check_plans.py` reports a missing
  CHECK as an ERROR (§3b, settled 2026-07-31; this sentence said
  "zero-or-one, not yet enforced" until 2026-08-01, which §3b had
  already contradicted — the wording lagged the ruling, and the owner
  confirmed the enforced form: "seems like a good check policy to
  have").
- **NODE folders** — sub-folders are the next level down ("node"
  chosen over "level"/"branch": shorter, just as concise — the owner,
  2026-07-28), named with the index path + description.
- **DASHBOARD.md** — zero or one per node folder. GENERATED, not
  hand-written, by
  `PRIVATE/PlanPlan/framework/generate_dashboards.py`: a
  rollup over that node's own sub-tree (status and designation
  breakdowns, anything blocked, PROGRESS bullet-status counts, the
  SUPPORT files present). It is regenerated, never edited — a hand
  edit is silently lost the next time the tool runs, the same
  contract `render_plan.py`'s output already has. Because it is
  produced from the tree rather than authored into it, it is not a
  stray file even though nothing above names it.
- **No stray files**: everything in a folder is its CORE, its
  PROGRESS, its CHECK, a SUPPORT file, a DASHBOARD, or a node folder.

The canonical shape:

```
node_0: folder                       (a project's planning root IS this folder)
    CORE_0.md: file
    CHECK_0.<ext>: file                (the node's test; mirrors the CORE's name)
    PROGRESS.md: file
    SUPPORT_0.md: file
    DASHBOARD.md: file                 (generated — regenerate, do not edit)
    node_0_0_<name>: folder
        CORE_0_0_<name>.md: file
        CHECK_0_0_<name>.<ext>: file
        PROGRESS.md: file
        SUPPORT_0_0_<name>.md: file
        DASHBOARD.md: file             (generated — regenerate, do not edit)
        node_0_0_0_<name>: folder
            ...
        node_0_0_1_<name>: folder
    node_0_1_<name>: folder
    node_0_2_<name>: folder
```

- The index chain (`1_0_2`) is the branch's ADDRESS — the same
  positional-path identity design as idgen's node ids, applied to
  the planning tree. Addresses can shift if branches are inserted
  or pruned; the frontmatter `id` (§3) is the IDENTITY and never
  changes. Analysis joins on `id`; readers navigate by address.
- **The completeness rule** (the load-bearing rule): nothing
  essential lives only at a lower level. A reader who stops at any
  CORE has a correct — just coarser — picture of that branch.

## 1b. A CORE's own sections

After `## sub_nodes` and `## definition`, a CORE may carry whatever
sections its subject needs. Two names are fixed by the grammar so that
tools can rely on them:

- **`## metadata`** — the projection of scalar YAML fields, first, always (§1).
- **`## super_node`** — the projection of the upward hierarchy edge (§1).
- **`## sub_nodes`** — the register's projection, immediately after super_node (§1).
- **`## definition`** — what this node IS, immediately after sub-nodes (§1).

One further name is defined because the renderer treats it specially:

- **`## design`** — the node's OWN internal structure: the shape of the
  thing this node names, one level below its definition. The renderer
  opens it without a click, because a node whose substance lives there
  would otherwise look empty. Every other section opens on demand.

`## design` is where a `code (class)` node states its attributes and
methods in the structural-overview form (§2), and where a node records
internal parts that are structure rather than sub-nodes. It sits
BESIDE the `realize: false` register entries, not instead of them: the
register says what the parts ARE, `## design` says how they fit.

**Superseded 2026-08-05: `## components`.** It was never defined here.
It existed only as a special case inside `render_plan.py` — which was
enough to invite COREs to use a section the grammar had never stated,
and one of them did. the owner: "`## components` is awkwardly close to
`## sub_nodes`. i dont even know what purpose `## components` serves...
`## design` or `## details` would be more accurate." Renamed, and
stated here rather than implied by a tool.

## 1c. Archive folders

**A node folder may contain `.archive/`, and nothing in the framework
looks inside it.**

- **The name is `.archive`, lower case.** The leading dot is what makes
  every tool skip it — folder walks drop dotted directories, so an
  archived file is not a stray, not a second CORE, and not a node.
- **What it is for:** keeping a file that is not live. Superseded
  drafts, an earlier CORE held while a rewrite settles, a document
  moved out of the way. This is the standing annotate-don't-delete
  rule given somewhere to put things.
- **Scope is the node folder it sits in.** An archived CORE stays
  beside the node it belonged to, so the chain is intact and the file
  is where a reader would look for it.
- **Temporary by intent, permanent by permission.** Nothing expires and
  nothing is required to leave.
- **Case matters to exactly one check.** `check_plans.py`'s
  stale-archive check looks for `.archive` by name. A folder named
  `.ARCHIVE` is still skipped by every walk, but that check cannot see
  into it, so a reference into it is not reclassified as archived —
  which is why the mis-cased name is reported rather than silently
  half-working.

Larger archives keep their existing form, unchanged by this: a
superseded tree goes to `.archive/<name>_superseded_<date>/` in the
same repo (§6b), which is this rule at repo scale.

## 2. Governance: higher levels govern lower levels

- A sub-document may refine its super-document, never contradict
  it. If lower-level work discovers the higher level is wrong, the
  higher level is corrected FIRST (correction recorded with why
  the position fell), then the sub-document.
- Change thresholds: `CORE_0.md` and level-1 COREs change only
  through the owner. Lower levels are agent-editable with provenance.
- This is the anti-drift mechanism: project drift is sub-documents
  quietly diverging from a stale higher level.

## 3. Metadata: every document carries a YAML frontmatter header

Prose for humans; metadata for analysis (the PlanPlan study).
Fields:

```yaml
---
id: t2_ledger.keying          # stable dotted id; never reused
level: 2                      # 0 = master
status: draft                 # draft | settled | superseded
                              # NOT blocked — see below
settled_by: the owner               # who settles this node
supersedes: null              # id of the node this replaced, or null
decision: AgentMemory/02_decisions.md#anchor   # when settled
designation: code (class)     # REQUIRED on every node — see §3a
node:                         # statement of itself — see §1
    name: keying
    path: Planning/node_2_0_keying/CORE_2_0_keying.md
super_node:                   # what this node hangs under, or null
    name: ledger       # — see §1
    path: ../CORE_0_0_ledger.md
sub_nodes:                    # address order; [] for a leaf — see §1
    - name: keying
      path: node_2_0_keying/CORE_2_0_keying.md
    - name: storage
      path: node_2_1_storage/CORE_2_1_storage.md
---
```

**The field names live in one file** —
`PRIVATE/PlanPlan/framework/schema.py`, added 2026-08-02 at
the owner's request. Every tool asks it rather than carrying its own string
literals, so renaming a field is one edit instead of four.

- **It centralizes the tools, not the documents.** YAML's anchors and
  aliases resolve only inside a single document; there is no include
  across files. Every CORE will always contain the literal key text.
- **The documents are handled by a migration command instead of a
  reference**:

      python3 PRIVATE/PlanPlan/framework/generate_nodes.py \
          <root>... --rename-field <old> <new> --apply

  It enumerates and prints every site before writing, and writes
  nothing without `--apply` — the shape §6c requires of the one case
  where a script is the right tool.
- So it is one place for the behaviour and one command for the files:
  two mechanisms, because the format will not give us one.

**Every document in a node folder carries frontmatter, in this order:
frontmatter first, then the title, then the sub-node listing (prose
optional), then anything else** (the owner, 2026-08-02). This is why the
whole grammar is markdown — it accommodates many formats and renders
well — and why no fact is moved out into a separate YAML file.

- A CORE carries the full field set above.
- A PROGRESS carries `id` and `status`, where `id` is
  `<node id>.progress`.
- A CHECK carries `id`, where `id` is `<node id>.check` (the owner,
  2026-08-02), the same shape as PROGRESS's. Added because CHECK
  files were written before this rule and carry no frontmatter at
  all.
- A SUPPORT file's `id` is `<node id>.support.<name>`, per §1.
- A DASHBOARD is generated and is exempt: it is produced from the
  tree rather than authored into it.

**`blocked` is a PROGRESS status, not a CORE status** (2026-07-31).
A CORE says what a node IS; being stuck is where it STANDS, so it
belongs in that node's `PROGRESS.md` frontmatter. The renderer reads
it there and shows it beside the node.

A block must name what is blocked AND what is not. "Blocked" alone
stops work that could continue; the useful form is "stage 2 has no
answer so the chain cannot close — stages 1 and 3 are unaffected,
and stage 1 produces the measurement that unblocks stage 2."

- `id` is the analysis key across VCS history: renames and moves
  keep the id, so ontology warping is traceable through time.
- `supersedes` chains preserve why positions fell (superseded
  files move to the local `.archive/` with the chain intact).
- Additional fields may be added per project; never removed.

## 3a. `designation`: what kind of thing a node is

Added 2026-07-31. **The reasoning is not repeated here** — it is in
`PRIVATE/PseudoCoupHQ/plan_and_code.md`, which is the source. This
section is the field's definition and what the grammar owes it.

Required on **every** node, so a missing designation is a defect the
renderer can name rather than a silence a reader has to interpret.
Comma-separated; a node may be more than one thing.

```yaml
designation: code (class)
designation: code (class), rule
designation: work
```

- `code (<kind>)` — kind is one of `object`, `module`, `class`,
  `method`, `attribute`, `function`, `variable`.
  - **`object` is the coarse kind** (the owner, 2026-08-01): a code thing
    whose identifier is settled but whose kind among the others is
    not yet. It exists so that "module or class?" never blocks a
    node's creation — the owner: "i view `module` as effectively a `class`
    with a different name." NOT the OO sense of object; it does not
    mean an instance.
  - It refines later to a specific kind, the same way a node deepens
    — refinement, not contradiction, so §2's governance rule holds.
  - **The settle-guard**: a node may not reach `status: settled`
    while still carrying `code (object)`. Deferral is allowed;
    permanent vagueness is not. `check_plans.py` reports a settled
    node with the coarse kind as an ERROR.
- Non-code designations, **settled by the owner 2026-07-31**, names and
  count both: `rule` (governs how code is used), `work` (something to
  be done with code), `finding` (what was learned, and its data),
  `grouping` (holds sub-nodes; thin by design). These replace the
  earlier `meta-logic`, which is retired.

### Every designation is a first-class citizen

Settled by the owner, 2026-07-31. `code` designations are the only ones
with concrete influence — they bind a node's name to an identifier —
but influence is not rank. A `rule`, `work`, `finding` or `grouping`
node is as legitimate an inhabitant of the tree as a `class` node,
and nothing in this framework treats one as a lesser form of the
other.

What that settles in practice: **a rule governing a code object may
be its own node, or a section inside that code object's CORE.**
Either spelling conforms. The choice is made per case, on which one
reads better, not on a rule about what a code node's sub-nodes are
allowed to be.

The section below reads code-heavy because `code` designations are
the ones that constrain the §1 grammar — an identifier has rules a
prose heading does not. That asymmetry is about mechanical
consequence only, and is not a statement about which nodes matter.

### What follows for the grammar in §1

- **A `code` node's name is the identifier that code will use.** The
  plan is the code at a coarser depth, not a specification of it, so
  the two share one name and there is nothing to drift.
- **Therefore a `code` node's description segment must be a valid
  identifier** — lower case, underscores, nothing else. The node
  folder naming in §1 already produces this; the designation makes it
  load-bearing rather than incidental.
- **The designation plus the address gives the qualified reference.**
  A `method` node under a `class` node under a `module` node reads as
  `module.Class.method` without anyone writing that down.
- **`grouping` suppresses the "definition only" warning.** A grouping
  node with forty words is finished, not neglected, and the renderer
  should stop reporting it as thin.
- **Renaming a `code` node is a refactor**, not tidying. That raises
  the cost of a casual rename and lowers the cost of a careful one,
  which is the correct trade.

### When a node stops being planned and starts being coded

A node is ready to become code when descending one more level would
add logic rather than structure. **A node that is not ready does not
get coded; it gets deepened.** Depth in this tree is the measure of
readiness, which is the whole reason the framework's completeness
rule and the coding method are the same rule.

### Not yet implemented

`render_plan.py` does not require `designation`. The check is one
line, but every node in every conforming tree currently lacks the
field, so it goes in with the trees' update rather than before it.

## 3b. Every node carries a test, and progress is read off the tests

**Policy stated by the owner, 2026-07-31**, to be implemented throughout
PseudoCoupHQ and any project using this framework. The mechanism is
NOT settled — the owner has said he wants to discuss it once the
administrative work is done. What follows is only what he has stated,
recorded so it is not lost, and marked where it stops.

### The policy as stated

- **Progress is tracked through tests.** A node's PROGRESS is not a
  prose claim that something is done; it is backed by a test that
  either passes or does not.
- **"Unit test, especially intermediate kinds."** the owner's words. The
  emphasis is on tests that check a stage part-way through a chain
  rather than only the chain's end result — so a node can report real
  progress before the work it belongs to is finished. *Reading not
  yet confirmed by the owner; the phrase is his, this gloss is not.*
- **Every node gets one, code and non-code alike.**
  - A `code` node gets a test in the ordinary sense, since there is
    an artifact to run.
  - A `rule`, `work`, `finding` or `grouping` node gets a **simpler
    test, mostly a by-hand check** — a stated question with a
    yes-or-no answer that a person can settle by looking — **unless a
    traditional coding test is possible**, in which case it gets one.
  - This follows from §3a: non-code designations are first-class, so
    "has no test" is not a thing a node is allowed to be merely
    because it holds no code.

### Why it belongs in the framework rather than in a project

The same argument as `designation`. A per-project convention drifts
between projects and cannot be checked by a tool that knows nothing
about any particular project. A framework rule can be checked
everywhere at once.

### Where a node's test lives — SETTLED (the owner, 2026-07-31)

> a node check is at the same level as its respective
> `CORE_..._<description>.md`. we can codify it as
> `CHECK_..._<description>.<extension>`

*(The segment this quote calls `<description>` is called `<name>`
everywhere else as of 2026-08-02 — see the rename note at the end of
§1. The quote keeps the word the owner used; the rule it states is
unchanged.)*

So the check is a file in the node folder, beside the CORE, with the
CORE's name and a free extension. `CORE_0_0_tools.md` is checked by
`CHECK_0_0_tools.<ext>`.

- **The extension carries the kind.** `.md` for a by-hand check —
  a written question a person answers by looking. `.py` (or whatever
  the project runs) for a check that executes. Nothing else in the
  grammar has to change to tell the two apart.
- **The name mirrors rather than being free** for the same reason a
  SUPPORT file's name, id and heading must agree: a check whose name
  does not track the thing it checks survives a rename of that thing
  and then silently checks something else.
- Recorded in the §1 grammar and in the canonical shape block.
  `render_plan.py` recognises `CHECK_*` and reports a mismatched name
  or a second CHECK file as grammar problems.

### The first check: completeness

Settled 2026-07-31. Every node's CHECK begins with the same question,
and it is the only one specified so far.

    complete(node) = status is `settled` AND every sub-node complete

Both clauses are load-bearing. Without the first, every leaf is
complete by definition and the recursion bottoms out at "the whole
tree is complete", which is true of any tree and therefore says
nothing. `status` is what distinguishes a node that is a leaf ON
PURPOSE from one that simply has not been decomposed yet — which is
the distinction the check exists to make.

A node's completeness is therefore never answerable by looking at that
node alone. It is read off its sub-nodes' CHECK files, which is why
their existence is enforced below.

Being incomplete is a STATE, not a defect. A tree under construction
is supposed to be incomplete, so `check_plans.py` reports completeness
and never fails on it.

Better checks come later; this one is deliberately crude.

### Existence is enforced

Settled 2026-07-31. `check_plans.py` reports as an ERROR any node
folder missing a CHECK file or a DASHBOARD.md.

- **A missing CHECK** does not fail one node — it makes every node
  above it unanswerable, since completeness is read off sub-nodes'
  checks. One gap breaks the rollup for the whole super-chain.
- **A missing DASHBOARD** does not mean somebody forgot to write one.
  It is generated, so it means the generator was not run and the tree
  on disk disagrees with the tree described.

This is EXISTENCE only. Whether a check PASSES is that check's own
business, and for a by-hand check it is a person's.

Note the asymmetry with `designation`, which is still only a warning:
CHECK and DASHBOARD can be brought into conformance mechanically, so
enforcing them costs nothing. `designation` requires a judgement per
node about what kind of thing it is, so enforcing it before that
judgement has been made would report every node in every tree as
defective.

### Where it still stops

Undecided, and deliberately not invented here:

- What a by-hand check looks like INSIDE the file beyond the
  completeness question, and how it records having been performed and
  when. The location is settled, the first check is settled, the
  artifact's fuller shape is not.
- How per-node checks compose with a project's own rule that every
  tool ships its own acceptance test. The two overlap for a `code`
  node, which has both, and it is not yet stated which governs.

### Related, and also pending discussion

the owner, same message: deepening individual branches of a plan one at a
time, rather than broadening the whole tree, is the intended way to
work — and the per-node tests are what would come with each
deepening. Sequencing to be discussed.

## 4. Links: plain markdown, relative paths

- Standard `[text](relative/path.md)` links ONLY — render on
  GitHub, survive any editor, work in SilverBullet/Obsidian/VS
  Code. No `[[wikilinks]]`.
- File and folder names follow the §1 grammar (level index path +
  description). Descriptions are the owner's domain.

## 5. Prose discipline (what makes the prose analyzable)

- Nested-bullet form per the communication protocol §5: each level
  of a bullet tree self-contained.
- Claims marked measured vs unverified; every settled statement
  links its decision record.
- One concept, one name — checked against the project glossary
  (vocabulary files); new terms get glossary entries at
  introduction.

## 6. Conformance by a project

- The project's planning root plays `node_0`: `CORE_0.md` +
  SUPPORT files + level-1 node folders conforming to §1–§5.
  > **Note on Root Naming:** (the owner, 2026-08-23) The root node's file and `id` should potentially be named after the project itself (e.g., `CORE_0_<project_name>.md` and `id: <project_name>`) rather than generic terms like `CORE_0_planning.md` or `id: root`. This prevents namespace collisions when cross-referencing between trees in a multi-project framework (like `PCHQ`).
- The framework is a template, not a dependency: conforming
  projects copy the conventions; PlanPlan later EXTRACTS
  instances from their VCS histories for the ontology-evolution
  dataset.
- Trees intending to conform, and where each stands (restated
  2026-08-02). None is finished: no node anywhere is `settled`, and
  `designation` is unfilled in most.
  - **NO tree conforms to the 2026-08-02 rules yet** — not one node in
    any of the five carries `super_node`, `sub_nodes`, or frontmatter
    on its CHECK file. That is expected: the rules were written the
    same day, and the reader they depend on has not been rewritten.
  - **Conformance is brought about one chain at a time, not by a
    sweep** (the owner, 2026-08-02): "we are going through chains of nodes
    and diving deeper while doing conformance work on that chain as we
    go." A branch is brought to the current rules when it is descended
    into, which is the same working order §3b already names at its
    close. A tree-wide pass would be the sweep §6c warns against, over
    52 nodes at once.
  - "Mechanical (2026-08-01)" below means the older bar: the inline
    `nodes` register, a `## nodes` section in first position, and a
    CHECK and DASHBOARD in every node folder.
  - `PRIVATE/PseudoCoupHQ/Planning/` — mechanical (2026-08-01).
  - `PRIVATE/PseudoCoup_v5/Planning/` — mechanical (2026-08-01).
  - `PRIVATE/PlanPlan/Planning/` — mechanical (2026-08-01). This
    repo's own tree, founded 2026-08-01.
  - `PRIVATE/PseudoCoup_v6/Planning/` — mechanical (2026-08-01)
    since the register was adopted into all 10 of its COREs. *(This
    entry read "not yet; no register on any of its 10 COREs" until
    2026-08-02; the adoption had been run and the wording lagged it.)*
  - `PRIVATE/PseudoIR/Planning/` — mechanical (2026-08-01) since
    the register was adopted into all 18 of its COREs. *(Same
    correction as the entry above.)* It and PseudoCoup_v6 were one
    tree until 2026-07-31.

## 6a. Splitting one plan into two

Learned by doing it, 2026-07-31. When a project turns out to be two
projects, the split is not a folder move — it is four rules.

- **Each root states what it exchanges with the other, by name.**
  Two artifacts, not a general dependency. If a third thing wants to
  cross, the split is drawn wrong and should be redrawn, not widened.
- **A fact lives in exactly one tree.** The other tree points at it.
  Two descriptions of one thing is the drift this framework exists to
  prevent, and a split doubles the opportunity for it.
- **Each tree must be acyclic on its own.** A bootstrap between two
  projects is fine — one hands the other an artifact and receives a
  different one back. A cycle inside a single tree is not, and is
  usually the reason the split became necessary.
- **Cross-tree references are absolute paths.** Relative paths break
  the first time either tree moves, and the two move independently
  by construction.

## 6b. Retiring a plan, and carrying its content forward

- The old tree is archived, never deleted:
  `.archive/<name>_superseded_<date>/` in the same repo. Its content
  is usually still cited by code and reports, which need re-pointing
  rather than breaking.
- Surviving content is carried as SUPPORT files beside the node that
  now owns it, NOT pasted into COREs. A CORE is the owner's own
  register; a projection must not overwrite it.
- A projected SUPPORT file's header states: the source path(s), the
  word count, a verdict (carried clean / carried with a named
  substitution / not carried), what changed, and **the root the
  source paths are relative to**. A source path with no stated root
  becomes unfindable the moment that root moves — which is exactly
  what archiving it does.
- Carried text keeps its own words. Additions go under their own
  heading above or below it, never interleaved. Appending cannot
  corrupt what it follows; rewriting can.
- A carried list of sub-nodes points backwards, at nodes that no
  longer exist. Add a `## where those nodes went` section giving
  current locations, rather than editing the carried list.
- Content that is NOT carried still gets a file saying so and why.
  A node that silently vanishes reads as an oversight.

## 6c. Editing a plan: read, do not sweep

The single largest source of defects in the 2026-07-31 split was
bulk find-and-replace across files. It produced, in one pass: two
paths that did not exist, a directory name with a doubled suffix
(because the search term was a substring of its replacement), and a
renamed dictionary key in working code — none of which a passing test
suite revealed.

- A script is the right tool when the operation is genuinely uniform
  AND the count is high enough that reading each site is impractical.
  Both conditions, not either.
- Otherwise: open the file, make the edit with its surrounding lines
  visible, move to the next. N files is N decisions, not one sweep.
- When a batch is unavoidable, enumerate every `(file, exact old
  text, exact new text)` triple by hand and assert each old text is
  present, so a miss fails loudly instead of matching something else.
- Verify by reading the diff, not by grepping for what you expect to
  find. Grep confirms your hypothesis; the diff shows what happened.

## 7. Viewing layer

- The vault is the git repo of markdown files — tool-agnostic by
  construction. VS Code (Antigravity) with plain markdown works
  unchanged.
- **`render_plan.py` is the viewer** — reads any conforming tree and
  writes one self-contained HTML page: the collapsible node tree,
  each node's definition line and sections, and every place the
  grammar in §1 and §3 is broken. Standard library only.

      python3 PRIVATE/PlanPlan/framework/render_plan.py \
          <planning root> -o out.html

  It checks, per node: exactly one CORE, a PROGRESS, no strays,
  frontmatter present, `level` against folder depth, heading address
  against folder address, every SUPPORT file's id under its node's id,
  every SUPPORT file's filename against its id and its heading, every
  SUPPORT file listed in the CORE, and the CORE's `## nodes` list
  against the sub-node folders actually present. It also reads each
  `PROGRESS.md`'s status and shows it beside the node, which is how a
  `blocked` node is visible without opening anything.

- **SilverBullet was tried and dropped** (the owner, 2026-07-31). It is a
  markdown wiki with no graph or tree visualization worth the setup;
  its `index.md` and `SETTINGS.md` also violate §1's no-stray-files
  rule in every planning root it touches. `install_silverbullet.sh`
  is archived at
  `framework/.archive/install_silverbullet_superseded_2026-07-31/`
  (moved 2026-08-01, the owner: "if its not already in an archive, put it
  there").

- The viewer's fold UI should someday be foldable cards rather than
  sideways/down arrows (the owner, 2026-08-01). Backseat; not load-bearing.
