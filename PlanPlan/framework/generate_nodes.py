#!/usr/bin/env python3
"""Generate sub-node folders from the frontmatter `nodes` register.

PROTOCOL §1 (the owner, 2026-08-01): every CORE's frontmatter carries the
sub-node REGISTER — `nodes: [a, b]`, titles only, address order — and
the register is the generation seed. This tool walks a planning tree,
diffs each CORE's register against the sub-node folders actually on
disk, and creates what is registered but not yet realized: the node
folder, a skeleton CORE, a PROGRESS, and a CHECK.

    python3 generate_nodes.py <planning root> [<root> ...]           # dry run
    python3 generate_nodes.py <planning root> [<root> ...] --apply   # write

    python3 generate_nodes.py <root> [...] --projections             # dry run
    python3 generate_nodes.py <root> [...] --projections --apply     # write

Dry run is the DEFAULT: the tool prints exactly what it would create
and touches nothing until --apply is given. Loud over silent.

    python3 generate_nodes.py <root> [...] --adopt                   # dry run
    python3 generate_nodes.py <root> [...] --adopt --apply           # write

--adopt is the one-off for trees that predate the register: it reads
the sub-node folders already on disk and writes the register that
describes them, then rebuilds the projections. It never overwrites a
register that exists. Everything after adoption runs the normal
direction, register -> folders -> projection (the owner, 2026-08-01: "i
want the generation to be markdown-YAML --> `## nodes`. however, we
can build supporting tools to bring current planning into
conformance.")

--projections generates nothing; it rebuilds every CORE's `## sub_nodes`
section (writing the current heading form, so it is also the migration
from the superseded `## nodes`) from its register, tree-wide. This is the refresh for the
known one-run lag: a skeleton enters its super's projection as a bare
link, and its description (its CORE's definition line) can only be
projected after a person writes it — run --projections then.

One existing thing it DOES rewrite, and only one: the `## sub_nodes`
section of a CORE it just generated under. That section is a
PROJECTION of the register (PROTOCOL §1) — generated content, same
contract as DASHBOARD.md — so after realizing new sub-nodes the tool
rebuilds it from the register: one entry per realized sub-node, name
from the register, description from that sub-node's own definition
line. The section scan is fence-aware: a `## ` line inside a fenced
code block is code, not a section.

What it will never do:
  - edit any OTHER part of an existing file, or any file it did not
    just generate under. Prose is the author's.
  - invent a `designation`. That is a judgement per node (PROTOCOL
    §3a), so the skeleton omits the field and `check_plans.py`'s
    missing-designation WARN names it as awaiting that judgement.
  - fix a register/folder disagreement. A folder whose index or title
    disagrees with the register is `check_plans.py`'s ERROR to
    report and a person's to resolve; generating alongside a
    disagreement would build on top of it.

DASHBOARD.md is generate_dashboards.py's job — run it (or plain
`bash ~/Programming/PseudoCoupHQ/hq.sh`, which does) after applying,
or check_plans will correctly report the new folders' dashboards
missing.

Standard library only, like every tool here.
"""

import importlib.util
import os
import re
import sys
from datetime import date

FRAMEWORK_DIR = os.path.dirname(os.path.abspath(__file__))


def _load(name):
    path = os.path.join(FRAMEWORK_DIR, name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_planning_model = _load("planning_model")
read_frontmatter = _planning_model.PlanningNode.read_frontmatter
parse_nodes_register = _planning_model.PlanningNode.parse_nodes_register
# `sub_nodes` when present, the superseded `nodes` when not.
register_of = _planning_model.PlanningNode.register_of
register_entries_of = _planning_model.PlanningNode.register_entries_of
_schema = _load("schema")
# `## sub_nodes` (was `## nodes` until 2026-08-02); rewrite_projection
# writes the current form and absorbs the superseded one, so running
# --projections IS the heading migration for a tree.
SUB_NODES_HEADING = _schema.Sections.SUB_NODES
METADATA_HEADING = _schema.Sections.METADATA
SUPER_NODE_HEADING = _schema.Sections.SUPER_NODE
SUB_NODES_HEADINGS = _schema.Sections.SUB_NODES_FORMS

CORE_RE = re.compile(r"^CORE_.*\.md$")
TITLE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
FOLDER_RE = re.compile(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$")

CORE_SKELETON = """\
---
id: {id}
level: {level}
status: draft
settled_by: the owner
supersedes: null
designation: pending
node:
    name: {title}
    path: {node_path}
super_node:
    name: {super_name}
    path: {super_path}
sub_nodes: []
---

# CORE {chain} — {title}

## metadata

*(pending)*

## super_node

*(none)*

## sub_nodes

*(none yet)*

## definition

*(pending — generated {today} from the register in
{super_core}; the definition and `designation` are the owner's to
write.)*
"""

PROGRESS_SKELETON = """\
---
id: {id}.progress
status: living
---

# PROGRESS — {title}

- {today}: node folder generated by
  `~/Programming/PlanPlan/framework/generate_nodes.py` from the
  `nodes` register of `{super_core}`. Skeleton only — definition,
  designation, and content pending.
"""

CHECK_SKELETON = """\
---
id: {id}.check
---

# CHECK — {chain}_{title}

Node `{id}`. Status `draft`.

## check 1 — completeness

> a node being complete means its sub-nodes are complete. if a node is
> a leaf with no sub-nodes, it is complete.
>
> there is a difference between an intentionally empty list vs a list
> that wont be empty eventually. but we have things like "draft"
> codifications to indicate an incomplete node.
>
> — the owner, 2026-07-31

So the rule has two parts, and the second is what stops it being
vacuous:

    complete(node) = status is `settled` AND every sub-node complete

Without the status clause every leaf is complete by definition and the
recursion bottoms out at "the whole tree is complete", which is true of
any tree and therefore says nothing. `draft` versus `settled` carries
the difference between a node that is a leaf on purpose and one that
simply has not been decomposed yet.

**Is this node settled?** **no** — `status: draft`

**Sub-nodes:**

*none — this is a leaf.*

A leaf is complete when its status is `settled`. There is
nothing beneath it to be incomplete.

### verdict

**NOT COMPLETE** — status is not `settled`.

## check 2 and beyond

None yet. the owner, 2026-07-31: "we can figure out better checks later."
"""


def disp(path):
    home = os.path.expanduser("~")
    ap = os.path.abspath(path)
    if ap.startswith(home + os.sep):
        return "~" + ap[len(home):]
    return ap


def chain_of(dirpath, root):
    """The address chain of a node folder: 'node_0_0_tools' -> '0_0'.
    The planning root itself is chain '0' (its children are
    node_0_0_*, node_0_1_*, ... in every conforming tree).

    The root was chain '1' until 2026-08-05, which made it the only
    node numbered differently in its own filename (`CORE_0`, level 0)
    and in its children's addresses (`node_1_...`). the owner asked why;
    there was no reason. The leading segment is a constant, and level
    has always been `segments - 1`. Renumbered tree-wide by
    `migrate.py renumber-root`."""
    if os.path.abspath(dirpath) == os.path.abspath(root):
        return "0"
    m = FOLDER_RE.match(os.path.basename(dirpath))
    return m.group(1) if m else None


def plan_generation(root):
    """Walk one tree; return (to_create, problems). to_create is a list
    of dicts, one per registered-but-unrealized sub-node."""
    to_create = []
    problems = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        core = next((f for f in filenames if CORE_RE.match(f)), None)
        if core is None:
            continue
        full = os.path.join(dirpath, core)
        with open(full, encoding="utf-8", errors="replace") as fh:
            fields, _ = read_frontmatter(fh.read())
        if "nodes" not in fields and "sub_nodes" not in fields:
            continue  # unconformed tree branch; check_plans reports it
        register = register_entries_of(fields)
        if register is None:
            problems.append(f"{disp(full)}: malformed register — skipped")
            continue
        chain = chain_of(dirpath, root)
        if chain is None:
            problems.append(f"{disp(dirpath)}: folder name does not "
                            f"match the node_<chain>_<title> grammar — "
                            f"skipped")
            continue
        existing = {}
        for d in dirnames:
            m = FOLDER_RE.match(d)
            if m:
                existing[m.group(2)] = d
        for i, entry_ in enumerate(register):
            title = entry_["name"]
            if entry_.get("realize") is False:
                continue  # in-file structure; consumes slot i, no folder
            if not TITLE_RE.match(title):
                problems.append(
                    f"{disp(full)}: register entry “{title}” is not a "
                    f"valid identifier (lower case, underscores) — "
                    f"refused")
                continue
            if title in existing:
                continue  # realized; agreement is check_plans' business
            sub_chain = f"{chain}_{i}"
            folder = f"node_{sub_chain}_{title}"
            # The place-in-the-tree edges the skeleton carries (PROTOCOL
            # §1, 2026-08-02): the super's NAME is its folder title (or,
            # at a tree root, the `node.name`/`id` its CORE states);
            # `node.path` is repo-relative like every `node.path`;
            # `super_node.path` is relative, and a generated folder sits
            # directly under its super, so it is always `../<core>`.
            m = FOLDER_RE.match(os.path.basename(dirpath))
            if m:
                super_name = m.group(2)
            else:
                node_field = fields.get("node")
                super_name = (node_field or {}).get("name") \
                    if isinstance(node_field, dict) else None
                super_name = super_name or fields.get("id", "?")
            repo_dir = os.path.dirname(os.path.abspath(root))
            core_abs = os.path.join(dirpath, folder,
                                    f"CORE_{sub_chain}_{title}.md")
            to_create.append({
                "root": root,
                "dirpath": dirpath,
                "folder": folder,
                "title": title,
                "chain": sub_chain,
                "id": f"{fields.get('id', '?')}.{title}",
                "level": sub_chain.count("_") ,
                "super_core": disp(full),
                "node_path": os.path.relpath(core_abs, repo_dir),
                "super_name": super_name,
                "super_path": f"../{core}",
            })
    return to_create, problems


def iter_body_lines_with_sections(body):
    """Yield (line, section) where section is the current `## ` heading
    or None above the first one. FENCE-AWARE: a line starting ```
    toggles fenced-code mode, and headings inside a fence are code —
    the exact case (the owner, 2026-08-01) that made markdown untrustworthy
    as the register."""
    section = None
    fenced = False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            yield line, section
            continue
        if not fenced and line.startswith("## "):
            section = line.strip()
        yield line, section


def definition_line(core_path):
    """A sub-node's one-line description for the projection: the first
    SENTENCE of its CORE's `## definition` section (PROTOCOL §1, the owner,
    2026-08-01 — the definition moved there when the title-to-nodes
    gap was closed; prose above the first section is also still read,
    so a CORE mid-migration keeps its description). The definition
    wraps across physical lines, so the whole first paragraph is
    joined before clipping at the first sentence boundary; a
    paragraph with no terminal period is used whole. A pending
    placeholder (starts with `*(`) yields no description."""
    with open(core_path, encoding="utf-8", errors="replace") as fh:
        _, body = read_frontmatter(fh.read())
    para = []
    in_placeholder = False
    for line, section in iter_body_lines_with_sections(body):
        if section not in (None, "## definition"):
            if para:
                break
            continue
        s = line.strip()
        if s.startswith("#"):
            continue
        if not s:
            if para:
                break  # first paragraph complete
            in_placeholder = False  # a placeholder ends at its paragraph
            continue
        if not para and s.startswith("*("):
            # pending placeholder: skip its WHOLE paragraph, not just
            # this line — the skeleton's placeholder wraps, and taking
            # its continuation lines as a description projected garbage
            # into the super's `## sub_nodes` (caught 2026-08-02).
            in_placeholder = True
            continue
        if in_placeholder:
            continue
        para.append(s)
    if not para:
        return None
    text = " ".join(para)
    dot = text.find(". ")
    if dot != -1:
        text = text[:dot]
    return text.rstrip(".")


def rewrite_projection(dirpath, root, write=True):
    """Rebuild the `## sub_nodes` section of the CORE in dirpath from its
    register, linking every REALIZED sub-node. Returns
    (core_path, changed, why): core_path is None with a reason in
    `why` if it refused; `changed` says whether the projection
    differed from what was on disk. With write=False nothing is
    written — the dry form of the same computation."""
    core = next((f for f in sorted(os.listdir(dirpath))
                 if CORE_RE.match(f)), None)
    if core is None:
        return None, False, f"{disp(dirpath)}: no CORE file"
    full = os.path.join(dirpath, core)
    with open(full, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    fields, body = read_frontmatter(text)
    # The frontmatter block, captured BEFORE `body` is rewritten below.
    # Deriving it later from len(text) - len(body) silently slices the
    # wrong number of characters once body has changed length, which
    # corrupts the head of every file it touches.
    head = text[:len(text) - len(body)]
    register = register_entries_of(fields)
    chain = chain_of(dirpath, root)
    entries = []
    for i, entry_ in enumerate(register or []):
        title = entry_["name"]
        if entry_.get("realize") is False:
            # In-file structure (PROTOCOL §1): listed unlinked — there
            # is no CORE to link — with its designation if stated.
            desig = entry_.get("designation")
            entries.append(f"- {title}" + (f" — {desig}" if desig else "")
                           + " *(realize: false)*")
            continue
        folder = f"node_{chain}_{i}_{title}"
        sub_core = os.path.join(dirpath, folder,
                                f"CORE_{chain}_{i}_{title}.md")
        if not os.path.isfile(sub_core):
            continue  # unrealized stays out of the projection
        desc = definition_line(sub_core)
        link = f"- [{title}]({folder}/CORE_{chain}_{i}_{title}.md)"
        entries.append(link + (f" — {desc}." if desc else ""))
    super_node = fields.get("super_node")
    super_node_block = "*(none — tree root)*"
    if isinstance(super_node, dict) and "name" in super_node and "path" in super_node:
        super_node_block = f"- [{super_node['name']}]({super_node['path']})"

    nodes_block = "\n".join(entries) if entries else "*(none yet)*"
        
    metadata_entries = []
    for field in ("id", "level", "status", "designation", "settled_by", "supersedes"):
        if field in fields:
            metadata_entries.append(f"- **{field}:** {fields[field]}")
    metadata_block = "\n".join(metadata_entries) if metadata_entries else "*(none)*"

    # The canonical CORE body (PROTOCOL §1, the owner, 2026-08-01: "after
    # the yaml and after the title, the first thing is `## nodes`.
    # not prose. nothing between the core title and nodes section"):
    # (Updated 2026-08-23: `## metadata` now precedes `## sub_nodes`)
    #
    #     # CORE <address> — <title>
    #     ## nodes          (the projection, rebuilt here)
    #     ## definition     (where stranded pre-section prose is moved)
    #     ...every other section, in its original order
    #
    # Parse the body into title / pre-section prose / sections,
    # fence-aware, then reassemble in that order. Prose found between
    # the title and the first section is MOVED into `## definition`,
    # merged ahead of any existing `## definition` content.
    title_lines, pre_prose = [], []
    sections = []  # (heading, [lines]), in document order
    fenced = False
    current = None
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("## "):
            current = [line.strip(), []]
            sections.append(current)
            continue
        if current is not None:
            current[1].append(line)
        elif line.startswith("# "):
            title_lines.append(line)
        else:
            pre_prose.append(line)

    def section_body(heading):
        got = [b for h, b in sections if h == heading]
        return got[0] if got else []

    def trimmed(lines):
        while lines and not lines[0].strip():
            lines = lines[1:]
        while lines and not lines[-1].strip():
            lines = lines[:-1]
        return lines

    definition = trimmed(pre_prose)
    existing_def = trimmed(section_body("## definition"))
    if definition and existing_def:
        definition = definition + [""] + existing_def
    elif existing_def:
        definition = existing_def

    out = []
    out += title_lines or ["# CORE ? — ?"]
    out += ["", METADATA_HEADING, "", metadata_block]
    out += ["", SUPER_NODE_HEADING, "", super_node_block]
    out += ["", SUB_NODES_HEADING, "", nodes_block]
    if definition:
        out += ["", "## definition", ""] + definition
    for heading, sec_body in sections:
        # Both projection heading forms are absorbed here: the rebuild
        # emits the current form above, so a superseded `## nodes` on
        # disk is replaced rather than kept as a stray second section.
        if heading in SUB_NODES_HEADINGS or heading == "## definition" or heading == METADATA_HEADING or heading == SUPER_NODE_HEADING:
            continue
        while sec_body and not sec_body[-1].strip():
            sec_body = sec_body[:-1]
        out += ["", heading] + sec_body
    new_text = (head.rstrip("\n") + "\n\n"
                + "\n".join(out).rstrip("\n") + "\n")
    if new_text == text:
        return full, False, None
    if write:
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(new_text)
    return full, True, None


def adopt_registers(roots, apply_mode):
    """--adopt: bring a tree that predates the register into
    conformance, the direction the owner settled 2026-08-01 — "as a
    PlanPlan generalized policy, i want the generation to be
    markdown-YAML --> `## nodes`. however, we can build supporting
    tools to bring current planning into conformance."

    Generation runs register -> folders -> projection. Adoption runs
    the other way ONCE, for trees that already have folders: it reads
    the sub-node folders on disk and writes the register that
    describes them, in folder-index order. That is a DESCRIPTION of
    what exists, not a judgement — which is why it can be mechanical
    where `designation` cannot.

    It never overwrites a register that is already there (a
    hand-written register is truth; disagreements with disk are
    check_plans' ERROR and a person's to settle). After writing, the
    projections are rebuilt so the markdown follows the YAML, never
    the reverse."""
    wrote, skipped = [], []
    for root in roots:
        for dirpath, dirnames, _ in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames
                                 if not d.startswith("."))
            core = next((f for f in sorted(os.listdir(dirpath))
                         if CORE_RE.match(f)), None)
            if core is None:
                continue
            full = os.path.join(dirpath, core)
            with open(full, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            fields, body = read_frontmatter(text)
            if register_of(fields) is not None:
                continue  # already conformant
            if not text.startswith("---"):
                skipped.append(f"{disp(full)}: no frontmatter block")
                continue
            found = []
            for d in dirnames:
                m = FOLDER_RE.match(d)
                if m:
                    found.append((int(m.group(1).split("_")[-1]),
                                  m.group(2)))
            register = [t for _i, t in sorted(found)]
            line = f"nodes: [{', '.join(register)}]"
            head_end = text.find("\n---", 3)
            head = text[:head_end]
            # replace a malformed `nodes:` line, else append to the block
            head_lines = [l for l in head.splitlines()
                          if not l.startswith("nodes:")]
            head_lines.append(line)
            new_text = "\n".join(head_lines) + text[head_end:]
            wrote.append((full, line))
            if apply_mode:
                with open(full, "w", encoding="utf-8") as fh:
                    fh.write(new_text)
    for s in skipped:
        print(f"!!! {s}")
    verb = "wrote" if apply_mode else "would write"
    for full, line in wrote:
        print(f"{verb} register: {disp(full)}  ->  {line}")
    if not wrote:
        print("every CORE already has a register.")
        return 1 if skipped else 0
    if apply_mode:
        print()
        refresh_projections(roots, True)
    else:
        print(f"\ndry run — nothing written. Re-run with --apply to "
              f"write the {len(wrote)} register(s) above and rebuild "
              f"the projections.")
    return 1 if skipped else 0


def refresh_projections(roots, apply_mode):
    """--projections: rebuild every CORE's `## sub_nodes` from its
    register, tree-wide — the standalone refresh for descriptions
    written after their skeleton was generated. Same dry-run contract
    as generation: report without --apply, write with it."""
    changed, problems = [], []
    for root in roots:
        for dirpath, dirnames, _ in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames
                                 if not d.startswith("."))
            core = next((f for f in sorted(os.listdir(dirpath))
                         if CORE_RE.match(f)), None)
            if core is None:
                continue
            full = os.path.join(dirpath, core)
            with open(full, encoding="utf-8", errors="replace") as fh:
                fields, _b = read_frontmatter(fh.read())
            if register_of(fields) is None:
                continue  # no/malformed register; check_plans' business
            path, did_change, why = rewrite_projection(
                dirpath, root, write=apply_mode)
            if why:
                problems.append(why)
            elif did_change:
                changed.append(path)
    for p in problems:
        print(f"!!! {p}")
    verb = "rebuilt" if apply_mode else "would rebuild"
    for c in changed:
        print(f"projection {verb}: {disp(c)} (`{SUB_NODES_HEADING}`)")
    if not changed:
        print("every projection already matches its register.")
    elif not apply_mode:
        print(f"\ndry run — nothing written. Re-run with --apply to "
              f"rebuild the {len(changed)} projection(s) above.")
    return 1 if problems else 0


def apply_one(entry, today):
    d = os.path.join(entry["dirpath"], entry["folder"])
    os.makedirs(d, exist_ok=False)
    fmt = dict(entry, today=today)
    core = os.path.join(d, f"CORE_{entry['chain']}_{entry['title']}.md")
    check = os.path.join(d, f"CHECK_{entry['chain']}_{entry['title']}.md")
    progress = os.path.join(d, "PROGRESS.md")
    for path, skel in ((core, CORE_SKELETON),
                      (progress, PROGRESS_SKELETON),
                      (check, CHECK_SKELETON)):
        if os.path.exists(path):
            raise SystemExit(f"refusing to overwrite {disp(path)}")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(skel.format(**fmt))
    return [core, progress, check]


def rename_field(roots, old, new, apply_mode):
    """--rename-field: change one frontmatter key across whole trees.

    The half of centralization YAML cannot do. `schema.py` names the
    fields once for the TOOLS, but every CORE still contains the
    literal key text and no YAML construct lets one file take its keys
    from another. So a rename is one edit in `schema.py` plus one run
    of this.

    It is the case §6c allows a script for — genuinely uniform and high
    count — and it keeps §6c's other requirement: it enumerates every
    site first, prints them, and writes nothing without `--apply`, so
    the diff is read rather than trusted.

    Matches a key at the start of a line, optionally after a `- ` for a
    sequence entry, so `description:` and `- description:` both move."""
    pat = re.compile(rf"^(\s*)(-\s+)?{re.escape(old)}:", flags=re.M)
    if old == new:
        print(f"!!! old and new are the same name: {old}")
        return 2
    sites, files = 0, 0
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            for fn_ in sorted(filenames):
                if not fn_.endswith(".md"):
                    continue
                full = os.path.join(dirpath, fn_)
                with open(full, encoding="utf-8") as fh:
                    text = fh.read()
                if not text.startswith("---"):
                    continue
                end = text.find("\n---", 3)
                if end == -1:
                    continue
                head, rest = text[:end], text[end:]
                found = pat.findall(head)
                if not found:
                    continue
                files += 1
                sites += len(found)
                for line in head.splitlines():
                    if pat.match(line):
                        print(f"{'rename' if apply_mode else 'would rename'}: "
                              f"{disp(full)}   {line.strip()}")
                if apply_mode:
                    new_head = pat.sub(
                        lambda m: f"{m.group(1)}{m.group(2) or ''}{new}:", head)
                    with open(full, "w", encoding="utf-8") as fh:
                        fh.write(new_head + rest)
    if not sites:
        print(f"nothing to rename: no frontmatter key `{old}` in these trees.")
        return 0
    print(f"\n{sites} site(s) in {files} file(s).")
    if not apply_mode:
        print("dry run — nothing written. Re-run with --apply.")
    else:
        print("now read the diff, per PROTOCOL §6c — grep confirms your "
              "hypothesis, the diff shows what happened.")
    return 0


def git_origin(repo_dir):
    """The `origin` url from a repo's own `.git/config`, or None.

    Read rather than shelled out to: this tool is standard library
    only, and the file is a plain ini."""
    cfg = os.path.join(repo_dir, ".git", "config")
    if not os.path.isfile(cfg):
        return None
    in_origin = False
    with open(cfg, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            s = line.strip()
            if s.startswith("["):
                in_origin = s.replace(" ", "") == '[remote"origin"]'
            elif in_origin and s.startswith("url"):
                return s.split("=", 1)[1].strip()
    return None


def repo_root_of(path):
    """The nearest ancestor holding `.git`, else None."""
    here = os.path.abspath(path)
    while True:
        if os.path.isdir(os.path.join(here, ".git")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            return None
        here = parent


def adopt_conformance(roots, apply_mode, do_edges=True, do_checks=True):
    """--adopt-edges / --adopt-checks: fill in the PROTOCOL §1 place
    fields and the §3 CHECK id, for trees that predate them.

    This is TRANSCRIPTION, not judgement, which is what makes a
    tree-wide pass appropriate here where §6c warns against sweeps.
    Every value written is already true on disk:

      node        name from the folder (or the id, at a root), path
                  from where the file actually sits
      super_node  the folder above, or null at a tree root
      sub_nodes   the sub-node folders present, in index order
      CHECK id    the node's own id with `.check`

    Nothing existing is overwritten. A node that already states a field
    keeps what it says, so a hand-written cross-repo edge survives.
    The superseded inline `nodes:` register IS replaced when
    `sub_nodes` is written, per PROTOCOL §1's "deleted from a node when
    that node is brought over"."""
    edits, check_edits, problems = [], [], []
    for root in roots:
        repo = repo_root_of(root)
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            core = next((f for f in sorted(filenames) if CORE_RE.match(f)), None)
            if core is None:
                continue
            full = os.path.join(dirpath, core)
            with open(full, encoding="utf-8") as fh:
                text = fh.read()
            fields, _body = read_frontmatter(text)
            if not text.startswith("---"):
                problems.append(f"{disp(full)}: no frontmatter block")
                continue
            node_id = fields.get("id", "")
            is_root = os.path.abspath(dirpath) == os.path.abspath(root)
            m = FOLDER_RE.match(os.path.basename(dirpath))
            name = (node_id.split(".")[-1] if is_root
                    else (m.group(2) if m else None))
            if name is None:
                problems.append(f"{disp(dirpath)}: folder name off-grammar")
                continue

            add = []
            if do_edges and "node" not in fields:
                rel = (os.path.relpath(full, repo) if repo
                       else os.path.basename(full))
                block = f"node:\n    name: {name}\n    path: {rel}\n"
                # A tree root also states which repo it is in, and that
                # repo's remote (PROTOCOL §1): below the root both are
                # derivable by walking `super_node` upward, so they are
                # written ONLY here. Both are read off disk, not asked
                # for — the directory name and `.git/config`'s origin.
                if is_root and repo:
                    block += f"    repo: {os.path.basename(repo)}\n"
                    remote = git_origin(repo)
                    if remote:
                        block += f"    remote: {remote}\n"
                add.append(block)
            if do_edges and "super_node" not in fields:
                if is_root:
                    add.append("super_node: null\n")
                else:
                    up = os.path.dirname(dirpath)
                    up_core = next((f for f in sorted(os.listdir(up))
                                    if CORE_RE.match(f)), None)
                    um = FOLDER_RE.match(os.path.basename(up))
                    if up_core is None:
                        problems.append(f"{disp(up)}: no CORE above {name}")
                        continue
                    with open(os.path.join(up, up_core), encoding="utf-8") as fh:
                        up_fields, _ = read_frontmatter(fh.read())
                    up_name = (um.group(2) if um
                               else up_fields.get("id", "?").split(".")[-1])
                    add.append(f"super_node:\n    name: {up_name}\n"
                               f"    path: ../{up_core}\n")

            new_text = text
            if do_edges and "sub_nodes" not in fields:
                kids = []
                for d in dirnames:
                    km = FOLDER_RE.match(d)
                    if km:
                        kc = next((f for f in sorted(os.listdir(
                            os.path.join(dirpath, d))) if CORE_RE.match(f)), None)
                        if kc:
                            kids.append((int(km.group(1).split("_")[-1]),
                                         km.group(2), d, kc))
                kids.sort()
                if kids:
                    block = "sub_nodes:\n" + "".join(
                        f"    - name: {n}\n      path: {d}/{c}\n"
                        for _i, n, d, c in kids)
                else:
                    block = "sub_nodes: []\n"
                # the superseded inline register goes when this arrives
                if "nodes" in fields:
                    new_text = re.sub(r"^nodes: \[.*\]\n", block, new_text,
                                      count=1, flags=re.M)
                else:
                    add.append(block)

            if add:
                head_end = new_text.find("\n---", 3)
                new_text = (new_text[:head_end + 1] + "".join(add)
                            + new_text[head_end + 1:])
            if new_text != text:
                edits.append((full, new_text))

            if do_checks:
                chk = next((f for f in sorted(filenames)
                            if f.startswith("CHECK_")), None)
                if chk and node_id:
                    cp = os.path.join(dirpath, chk)
                    with open(cp, encoding="utf-8") as fh:
                        ctext = fh.read()
                    if not ctext.startswith("---"):
                        check_edits.append(
                            (cp, f"---\nid: {node_id}.check\n---\n\n{ctext}"))

    for p in problems:
        print(f"!!! {p}")
    verb = "wrote" if apply_mode else "would write"
    print(f"{verb} place fields into {len(edits)} CORE(s)")
    print(f"{verb} frontmatter into {len(check_edits)} CHECK file(s)")
    if apply_mode:
        for path, new in edits + check_edits:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)
        print("\nnow run --projections --apply, then generate_dashboards.")
    else:
        for path, _ in (edits + check_edits)[:6]:
            print(f"    {disp(path)}")
        print("\ndry run — nothing written. Re-run with --apply.")
    return 1 if problems else 0


def main():
    flags = {"--apply", "--projections", "--adopt",
             "--adopt-edges", "--adopt-checks"}
    args = [a for a in sys.argv[1:] if a not in flags]
    apply_mode = "--apply" in sys.argv[1:]
    if "--rename-field" in args:
        i = args.index("--rename-field")
        if len(args) < i + 3:
            print("--rename-field needs <old> <new>")
            return 2
        old_name, new_name = args[i + 1], args[i + 2]
        roots = [os.path.expanduser(r) for r in args[:i] + args[i + 3:]]
        roots = [r for r in roots if os.path.isdir(r)]
        return rename_field(roots, old_name, new_name, apply_mode)
    if not args:
        print(__doc__)
        return 2
    if "--adopt-edges" in sys.argv[1:] or "--adopt-checks" in sys.argv[1:]:
        roots = [os.path.expanduser(r) for r in args
                 if os.path.isdir(os.path.expanduser(r))]
        return adopt_conformance(
            roots, apply_mode,
            do_edges="--adopt-edges" in sys.argv[1:],
            do_checks="--adopt-checks" in sys.argv[1:])
    if "--adopt" in sys.argv[1:]:
        roots = [os.path.expanduser(r) for r in args
                 if os.path.isdir(os.path.expanduser(r))]
        return adopt_registers(roots, apply_mode)
    if "--projections" in sys.argv[1:]:
        roots = [os.path.expanduser(r) for r in args]
        missing = [r for r in roots if not os.path.isdir(r)]
        for r in missing:
            print(f"!!! {disp(r)}: no such directory")
        return refresh_projections(
            [r for r in roots if os.path.isdir(r)], apply_mode) \
            or (1 if missing else 0)
    today = date.today().isoformat()
    total, all_problems = [], []
    for root in args:
        root = os.path.expanduser(root)
        if not os.path.isdir(root):
            all_problems.append(f"{disp(root)}: no such directory")
            continue
        to_create, problems = plan_generation(root)
        total += to_create
        all_problems += problems
    for p in all_problems:
        print(f"!!! {p}")
    if not total:
        # Say which of the two silences this is. Reporting "every
        # registered sub-node has a folder" after refusing an entry
        # names the wrong reason for generating nothing.
        if all_problems:
            print(f"nothing generated: {len(all_problems)} register "
                  f"problem(s) above, and nothing else to do.")
            return 1
        print("nothing to generate: every registered sub-node has a "
              "folder.")
        return 0
    for e in total:
        print(f"{'created' if apply_mode else 'would create'}: "
              f"{disp(os.path.join(e['dirpath'], e['folder']))}/  "
              f"(id {e['id']}, level {e['level']})")
        if apply_mode:
            for f in apply_one(e, today):
                print(f"    {disp(f)}")
    if apply_mode:
        touched = []
        for e in total:
            key = (e["dirpath"], e.get("root"))
            if key not in touched:
                touched.append(key)
        for dirpath, root in touched:
            core, _changed, why = rewrite_projection(dirpath, root)
            if core:
                print(f"projection rebuilt: {disp(core)} (`{SUB_NODES_HEADING}`)")
            else:
                print(f"!!! {why}")
        print(f"\n{len(total)} node(s) generated. Now regenerate "
              f"dashboards (generate_dashboards.py or hq.sh), or "
              f"check_plans will report them missing.")
    else:
        print(f"\ndry run — nothing written. Re-run with --apply to "
              f"create the {len(total)} node(s) above.")
    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main())
