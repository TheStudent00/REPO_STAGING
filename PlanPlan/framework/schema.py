#!/usr/bin/env python3
"""The field vocabulary of the planning grammar, named once.

Added 2026-08-02 at the owner's request: "im also wondering if there is a
way to centralize the document fields according to PlanPlan. like if
we want to change `description` we just need to change it once."

**What this file does and does not give you.** It centralizes the
names for the TOOLS: `planning_model.py`, `checks.py`,
`generate_nodes.py` and `render_plan.py` all ask here rather than
carrying their own string literals, so renaming a field is one edit
instead of four.

It cannot centralize the names for the DOCUMENTS. YAML's anchors and
aliases (`&x` / `*x`) resolve only inside a single document; there is
no include across files. So every CORE will always contain the literal
key text, and a rename still has to rewrite every file. That half is
handled by a migration command rather than by a reference:

    python3 <WORKSPACE_DIR>/PlanPlan/framework/generate_nodes.py \\
        <root>... --rename-field <old> <new> --apply

One place for the behaviour, one command for the documents. Two
mechanisms, because the format will not give us one.

Standard library only; imports nothing, not even the rest of the
framework, so anything may import it.
"""


class Fields:
    """Top-level frontmatter keys on a CORE (PROTOCOL §3)."""

    ID = "id"
    LEVEL = "level"
    STATUS = "status"
    SETTLED_BY = "settled_by"
    SUPERSEDES = "supersedes"
    DECISION = "decision"
    DESIGNATION = "designation"

    # The place-in-the-tree fields (PROTOCOL §1, the owner, 2026-08-02).
    NODE = "node"
    SUPER_NODE = "super_node"
    SUB_NODES = "sub_nodes"

    # Superseded 2026-08-02 by SUB_NODES. Still read, because trees are
    # brought over chain by chain and both forms exist meanwhile. When
    # no tree carries it, this constant and the fallback in
    # `PlanningNode.register_of` go together.
    NODES_SUPERSEDED = "nodes"

    # On a PROGRESS or a CHECK rather than a CORE.
    PROGRESS_ID_SUFFIX = "progress"
    CHECK_ID_SUFFIX = "check"
    SUPPORT_ID_SEGMENT = "support"


class Sections:
    """Markdown section headings inside a CORE body (PROTOCOL §1).

    SUB_NODES was `## nodes` until 2026-08-02, renamed at the owner's request
    to match the frontmatter key it projects (`Fields.SUB_NODES`) —
    the heading and the register it is a projection of should carry one
    name. The superseded form follows the same migration contract as
    `Fields.NODES_SUPERSEDED`: still recognized while trees are brought
    over, and the projection rebuild REWRITES it to the current form,
    so running `generate_nodes.py <root> --projections --apply` is the
    whole migration for a tree."""

    METADATA = "## metadata"
    SUPER_NODE = "## super_node"
    SUB_NODES = "## sub_nodes"
    SUB_NODES_SUPERSEDED = "## nodes"
    # Either form is "the register projection" while both exist.
    SUB_NODES_FORMS = (SUB_NODES, SUB_NODES_SUPERSEDED)

    DEFINITION = "## definition"


class EdgeKeys:
    """Keys inside a `node`, `super_node` or `sub_nodes` entry.

    NAME was called `description` until 2026-08-02. It was renamed
    because the segment is an identifier, not a description —
    `plan_and_code.md` §1: "a plan node that describes a code object
    carries that object's name. Not a description of it, not a synonym
    — the name." `title` was rejected because `read_core` already
    returns `title` for the `# CORE 0_0 — tools` heading."""

    NAME = "name"
    PATH = "path"
    REPO = "repo"
    REMOTE = "remote"

    # `realize: false` (the owner, 2026-08-02) marks a register entry whose
    # structure stays inside the super's own file — an attribute or
    # method planned as structure but not worth a folder. The entry
    # consumes its address slot (so realizing it later renumbers
    # nothing), the generator skips it, and the projection lists it
    # unlinked. It carries NAME and optionally DESIGNATION, and no
    # PATH — there is no file to locate. Deleting the key and running
    # the generator is the whole graduation to a folder. The word is
    # the framework's own verb for register -> folders ("realized",
    # "unrealized"), chosen over `inline` because it names the rule
    # rather than a metaphor.
    REALIZE = "realize"
    # DESIGNATION is allowed ONLY on a `realize: false` entry: a
    # realized sub-node states its designation in its own CORE, and
    # stating it in the register too would be one fact in two places.
    DESIGNATION = "designation"

    REQUIRED = (NAME, PATH)
    # REPO and REMOTE appear on an edge that leaves the repo, and on a
    # tree root's own `node`. Anywhere else they state a fact already
    # derivable by walking `super_node` upward.
    OPTIONAL = (REPO, REMOTE)
    ALL = REQUIRED + OPTIONAL
    # The shape of a `realize: false` entry.
    UNREALIZED_REQUIRED = (NAME,)
    UNREALIZED_OPTIONAL = (REALIZE, DESIGNATION)


class Statuses:
    """`status` values (PROTOCOL §3). `blocked` is deliberately absent:
    it is a PROGRESS status, not a CORE status — a CORE says what a
    node IS, being stuck is where it STANDS."""

    DRAFT = "draft"
    SETTLED = "settled"
    SUPERSEDED = "superseded"
    LIVING = "living"          # PROGRESS files
    ALL_CORE = (DRAFT, SETTLED, SUPERSEDED)


class EdgeStatuses:
    """What `PlanningNode.parse_edge` and `parse_edge_register` return
    as their first value. `ABSENT` and `EMPTY` are kept apart on
    purpose: a leaf that says `sub_nodes: []` has stated something, and
    a CORE with no such field has not."""

    OK = "ok"
    ABSENT = "absent"
    NULL = "null"
    EMPTY = "empty"
    MALFORMED = "malformed"
    UNREADABLE = "unreadable"
