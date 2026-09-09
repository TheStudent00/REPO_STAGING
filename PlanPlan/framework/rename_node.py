#!/usr/bin/env python3
"""Rename a node in one pass: folder, CORE/CHECK filenames, the
renamed node's own frontmatter, the super-node's register entry and
projection link, every sub-node's `super_node` edge, and every OTHER
document in the planning root that still references the old folder
path, the old CORE filename, or the old dotted id.

    python3 rename_node.py <planning_root> <old_name> <new_name> \\
        [--apply] \\
        [--also-artifacts <old_dir>=<new_dir>] \\
        [--scan-root <dir>]

Dry run is the DEFAULT: prints exactly what it would touch and writes
nothing until --apply is given. `--also-artifacts` is repeatable (rare,
but a rename sometimes carries more than one artifact directory along
with it); `--scan-root` is repeatable too and adds extra places to
search for references to a renamed artifact directory (co-nodes in
another repo, DevComms logs in a sibling repo, ...). With no
`--scan-root` given, the artifact-reference sweep defaults to the repo
that holds `<planning_root>` (found by walking up to the nearest
`.git`, same rule `checks.NodeSelfCheck.repo_dir_of` already uses).

REFUSES LOUDLY AND WRITES NOTHING if:
  - the new node name collides with an unrelated node already at that
    name, or the destination folder already exists on disk;
  - an `--also-artifacts` destination already exists;
  - the planning root does not check clean first — this tool reuses
    every check `check_plans.py` runs (`checks.Checker`) and refuses
    if any of them reports an ERROR. A rename should not be the thing
    that makes a broken tree harder to read.

If the node already carries the NEW name (no folder found under the
old name, but one exists under the new name), the node-level steps are
reported as already done rather than as an error — the tool still runs
the reference sweep and, if given, the `--also-artifacts` rename. This
is the shape a partially-finished manual rename needs: pick up exactly
where it stopped, touch nothing that is already correct.

## rename provenance

PROTOCOL §3: "renames and moves keep the id, so ontology warping is
traceable through time." But `checks.py`'s `node-self-name` check
enforces the opposite — the id's last dotted segment must equal the
node's `name` (and the folder's name segment below a tree root) — so a
folder renamed without changing its id fails that check immediately,
and `check_plans.py` reports it as an ERROR. Framework tension recorded
by the owner, 2026-08-14, at
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/
node_0_3_0_kind_signature_clustering/PROGRESS.md`: "one of the two
rules should give; the owner's call."

Until that call is made, this tool takes the side that keeps the tree
CHECKING CLEAN: the id's last dotted segment is changed to the new
name, same as `node.name` and the folder. That is a real loss — §3's
whole reason for keeping the id stable is so the id alone is enough to
trace a node across a rename — so the tool pays for it twice, in the
two places §3 asked the id itself to cover:

  1. it PRINTS the old id, unmissably, in both the dry-run report and
     the applied report — "provenance: id changed <old> -> <new>";
  2. it APPENDS a dated line naming the old id to the node's own
     `PROGRESS.md`, so the record survives in the one file every
     reader of that node already checks for its history.

A rename is therefore still traceable — just not by the id alone
anymore, until the owner rules which of the two framework rules gives.

Standard library only, like every tool in this framework. Imports
`planning_model`, `schema` and `checks` from this same directory.
"""
import argparse
import os
import re
import shutil
import sys
from datetime import date

import checks
import planning_model
import schema

read_frontmatter = planning_model.PlanningNode.read_frontmatter

NODE_FOLDER_RE = re.compile(r"^node_((?:\d+_)*\d+)_([a-z0-9_]+)$")
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
TEXT_EXTS = {".md", ".py", ".js", ".json", ".log", ".txt", ".sh",
             ".yaml", ".yml", ".gitignore"}


def disp(path):
    home = os.path.expanduser("~")
    ap = os.path.abspath(path)
    return "~" + ap[len(home):] if ap.startswith(home + os.sep) else ap


# --------------------------------------------------------------- locating


def find_node_dirs(root, name):
    """Every node folder under root whose name segment is exactly `name`.
    A conforming tree has at most one; more than one is a collision this
    tool refuses to guess at."""
    out = []
    for dirpath, dirnames, _ in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        m = NODE_FOLDER_RE.match(os.path.basename(dirpath))
        if m and m.group(2) == name:
            out.append(dirpath)
    return out


def core_file_of(dirpath):
    return next((f for f in sorted(os.listdir(dirpath))
                 if planning_model.CORE_RE.match(f)), None)


def check_file_of(dirpath):
    return next((f for f in sorted(os.listdir(dirpath))
                 if planning_model.CHECK_RE.match(f)), None)


def support_files_of(dirpath):
    return [f for f in sorted(os.listdir(dirpath))
            if planning_model.SUPPORT_RE.match(f)]


# ------------------------------------------------------------- preflight


def tree_checks_clean(root):
    """Run every check `check_plans.py` runs, over this one root. Returns
    the list of ERROR-severity findings (empty means clean). Reused
    rather than reimplemented, per the framework's own rule that a tool
    asks `checks.py` rather than carrying its own opinion."""
    programming_root = os.path.expanduser("~/Programming")
    label = os.path.relpath(root, programming_root)
    if label.startswith(".."):
        label = root
    checker = checks.Checker([
        checks.GrammarCheck(), checks.ArchiveNameCheck(),
        checks.DanglingPathCheck(), checks.IdCollisionCheck(),
        checks.RequiredFilesCheck(), checks.NodesRegisterCheck(),
        checks.EdgeRegisterCheck(), checks.NodeSelfCheck(),
        checks.CheckFrontmatterCheck(), checks.ProjectionCheck(),
    ])
    items = checker.run_all([(root, label)], programming_root)
    return [i for i in items if i.severity == "ERROR"]


# ------------------------------------------------------------- text edit


class Edit:
    """One planned change to one file: a literal old substring becoming
    a literal new substring. `label` says what the change IS (id,
    node.name, a register entry, a stray reference, ...), which is what
    the report prints beside the file so a person can tell a structural
    edit from the tree-wide reference sweep without opening anything."""

    def __init__(self, path, label, old, new):
        self.path = path
        self.label = label
        self.old = old
        self.new = new

    def line_count(self):
        return self.old.count("\n") + 1 if self.old else 1


def apply_edits(edits):
    """Group edits by file and write each file once, in the order its
    edits were recorded. A file with no net change (old == new, or the
    old text already gone) is left untouched."""
    by_file = {}
    for e in edits:
        by_file.setdefault(e.path, []).append(e)
    for path, es in by_file.items():
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        for e in es:
            if e.old not in text:
                continue
            text = text.replace(e.old, e.new, 1)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)


def field_line_edit(text, path, label, key, old_value, new_value, indent=""):
    """A `<indent><key>: <old_value>` line, matched exactly and replaced
    with the new value. Returns an Edit or None if the line is not
    present in this exact form (reported by the caller as a miss rather
    than silently skipped)."""
    old_line = f"{indent}{key}: {old_value}"
    new_line = f"{indent}{key}: {new_value}"
    if old_line not in text:
        return None
    return Edit(path, label, old_line, new_line)


# ---------------------------------------------------------- the rename


class Plan:
    def __init__(self):
        self.edits = []          # [Edit]
        self.file_renames = []   # [(old_path, new_path, label)]
        self.dir_renames = []    # [(old_path, new_path, label)]
        self.problems = []       # [str] -- refusal reasons
        self.notes = []          # [str] -- informational, not refusals

    def refuse(self, reason):
        self.problems.append(reason)


def plan_node_rename(root, old_name, new_name):
    """Everything JOB 1 owns for the node itself: folder, CORE/CHECK
    filenames, this node's own frontmatter, the super's register entry
    and projection link, and every direct sub-node's `super_node` edge.
    Returns (Plan, mode) where mode is "rename", "already-renamed", or
    "not-found"."""
    plan = Plan()

    old_dirs = find_node_dirs(root, old_name)
    new_dirs = find_node_dirs(root, new_name)

    if len(old_dirs) > 1:
        plan.refuse(f"{len(old_dirs)} node folders already named "
                     f"`{old_name}` — ambiguous, refusing to guess which "
                     f"one to rename: {', '.join(disp(d) for d in old_dirs)}")
        return plan, "ambiguous"
    if len(new_dirs) > 1:
        plan.refuse(f"{len(new_dirs)} node folders already named "
                     f"`{new_name}` — the destination name is already "
                     f"ambiguous on disk: {', '.join(disp(d) for d in new_dirs)}")
        return plan, "ambiguous"

    if not old_dirs and not new_dirs:
        plan.refuse(f"no node folder named `{old_name}` or `{new_name}` "
                     f"under {disp(root)}")
        return plan, "not-found"

    if not old_dirs and new_dirs:
        # Already renamed (or never had the old name). Nothing to do at
        # the node level; the caller still runs the reference sweep and
        # any --also-artifacts work.
        plan.notes.append(
            f"node already at `{new_name}` ({disp(new_dirs[0])}) — no "
            f"folder named `{old_name}` found. Skipping the node-level "
            f"rename; the sweep below still runs.")
        return plan, "already-renamed"

    old_dir = old_dirs[0]
    m = NODE_FOLDER_RE.match(os.path.basename(old_dir))
    addr = m.group(1)
    new_folder_name = f"node_{addr}_{new_name}"
    new_dir = os.path.join(os.path.dirname(old_dir), new_folder_name)

    if os.path.exists(new_dir) or new_dirs:
        plan.refuse(f"collision: {disp(new_dir)} already exists — "
                     f"refusing to overwrite it")
        return plan, "collision"

    old_core_name = core_file_of(old_dir)
    if old_core_name is None:
        plan.refuse(f"{disp(old_dir)}: no CORE file — refusing to rename "
                     f"a node with no CORE")
        return plan, "no-core"
    old_core_path = os.path.join(old_dir, old_core_name)
    new_core_name = f"CORE_{addr}_{new_name}.md"

    with open(old_core_path, encoding="utf-8") as fh:
        core_text = fh.read()
    fields, _ = read_frontmatter(core_text)
    old_id = fields.get(schema.Fields.ID)
    if not old_id:
        plan.refuse(f"{disp(old_core_path)}: no `id` in frontmatter — "
                     f"refusing to invent one")
        return plan, "no-id"
    segments = old_id.split(".")
    new_id = ".".join(segments[:-1] + [new_name])

    repo_dir = checks.NodeSelfCheck.repo_dir_of(root, os.path.expanduser("~/Programming"))
    new_core_path_after = os.path.join(new_dir, new_core_name)
    new_node_path_value = (os.path.relpath(new_core_path_after, repo_dir)
                            if repo_dir else new_core_name)

    # --- this node's own CORE: id, node.name, node.path, H1 title
    e = field_line_edit(core_text, old_core_path, "id", "id", old_id, new_id)
    if e:
        plan.edits.append(e)
    else:
        plan.notes.append(f"{disp(old_core_path)}: `id: {old_id}` not "
                           f"found in the exact expected form — id left "
                           f"unchanged, reported rather than guessed at")
    e = field_line_edit(core_text, old_core_path, "node.name", "name",
                         old_name, new_name, indent="    ")
    if e:
        plan.edits.append(e)
    node_field = fields.get(schema.Fields.NODE)
    if isinstance(node_field, dict) and schema.EdgeKeys.PATH in node_field:
        e = field_line_edit(core_text, old_core_path, "node.path", "path",
                             node_field[schema.EdgeKeys.PATH],
                             new_node_path_value, indent="    ")
        if e:
            plan.edits.append(e)
    title_m = re.search(r"^# CORE ([\d_]+) — (.+)$", core_text, re.M)
    if title_m and title_m.group(2).strip() == old_name:
        old_title_line = title_m.group(0)
        new_title_line = f"# CORE {title_m.group(1)} — {new_name}"
        plan.edits.append(Edit(old_core_path, "H1 title",
                                old_title_line, new_title_line))

    # --- PROGRESS.md: id, plus the provenance line
    progress_path = os.path.join(old_dir, "PROGRESS.md")
    if os.path.isfile(progress_path):
        with open(progress_path, encoding="utf-8") as fh:
            ptext = fh.read()
        pfields, _ = read_frontmatter(ptext)
        old_pid = pfields.get(schema.Fields.ID)
        want_old_pid = f"{old_id}.{schema.Fields.PROGRESS_ID_SUFFIX}"
        if old_pid == want_old_pid:
            new_pid = f"{new_id}.{schema.Fields.PROGRESS_ID_SUFFIX}"
            plan.edits.append(Edit(progress_path, "PROGRESS id",
                                    f"id: {old_pid}", f"id: {new_pid}"))
        today = date.today().isoformat()
        provenance = (
            f"\n- {today}: node renamed `{old_name}` -> `{new_name}` "
            f"by `rename_node.py`. id changed with it "
            f"(PROTOCOL §3 vs. `node-self-name` — see rename_node.py's "
            f"own docstring): `{old_id}` -> `{new_id}`.\n")
        plan.edits.append(Edit(progress_path, "provenance line",
                                "", provenance))
    else:
        plan.notes.append(f"{disp(old_dir)}: no PROGRESS.md — provenance "
                           f"not recorded there")

    # --- CHECK file: rename + id
    old_check_name = check_file_of(old_dir)
    new_check_path = None
    if old_check_name:
        stem, ext = os.path.splitext(old_check_name)
        want_stem = f"CHECK_{addr}_{old_name}"
        if stem == want_stem:
            old_check_path = os.path.join(old_dir, old_check_name)
            new_check_name = f"CHECK_{addr}_{new_name}{ext}"
            new_check_path = os.path.join(old_dir, new_check_name)
            plan.file_renames.append(
                (old_check_path, new_check_path, "CHECK file"))
            with open(old_check_path, encoding="utf-8") as fh:
                ctext = fh.read()
            cfields, _ = read_frontmatter(ctext)
            old_cid = cfields.get(schema.Fields.ID)
            want_old_cid = f"{old_id}.{schema.Fields.CHECK_ID_SUFFIX}"
            if old_cid == want_old_cid:
                new_cid = f"{new_id}.{schema.Fields.CHECK_ID_SUFFIX}"
                plan.edits.append(Edit(old_check_path, "CHECK id",
                                        f"id: {old_cid}", f"id: {new_cid}"))
        else:
            plan.notes.append(
                f"{disp(os.path.join(old_dir, old_check_name))}: name "
                f"does not mirror the CORE ({want_stem} expected) — left "
                f"as is")

    # --- SUPPORT files: id prefix only (their own name is unaffected)
    for sname in support_files_of(old_dir):
        spath = os.path.join(old_dir, sname)
        with open(spath, encoding="utf-8") as fh:
            stext = fh.read()
        sfields, _ = read_frontmatter(stext)
        sid = sfields.get(schema.Fields.ID, "")
        prefix = f"{old_id}.{schema.Fields.SUPPORT_ID_SEGMENT}."
        if sid.startswith(prefix):
            suffix = sid[len(prefix):]
            new_sid = f"{new_id}.{schema.Fields.SUPPORT_ID_SEGMENT}.{suffix}"
            plan.edits.append(Edit(spath, "SUPPORT id",
                                    f"id: {sid}", f"id: {new_sid}"))

    # --- the CORE file rename itself, and the folder rename
    plan.file_renames.append(
        (old_core_path, os.path.join(old_dir, new_core_name), "CORE file"))
    plan.dir_renames.append((old_dir, new_dir, "node folder"))

    # --- direct sub-nodes beneath this one: their super_node edge moves
    for entry in os.listdir(old_dir):
        full = os.path.join(old_dir, entry)
        if not os.path.isdir(full) or not planning_model.NODE_RE.match(entry):
            continue
        sub_core_name = core_file_of(full)
        if not sub_core_name:
            continue
        sub_core_path = os.path.join(full, sub_core_name)
        with open(sub_core_path, encoding="utf-8") as fh:
            sub_text = fh.read()
        sub_fields, _ = read_frontmatter(sub_text)
        sup = sub_fields.get(schema.Fields.SUPER_NODE)
        if isinstance(sup, dict):
            if sup.get(schema.EdgeKeys.NAME) == old_name:
                plan.edits.append(field_line_edit(
                    sub_text, sub_core_path, "sub-node super_node.name",
                    "name", old_name, new_name, indent="    "))
            old_sup_path = sup.get(schema.EdgeKeys.PATH, "")
            if old_sup_path == f"../{old_core_name}":
                new_sup_path = f"../{new_core_name}"
                plan.edits.append(field_line_edit(
                    sub_text, sub_core_path, "sub-node super_node.path",
                    "path", old_sup_path, new_sup_path, indent="    "))
    plan.edits = [e for e in plan.edits if e is not None]

    # --- the super-node: register entry + projection link
    super_dir = os.path.dirname(old_dir)
    super_core_name = core_file_of(super_dir)
    if super_core_name:
        super_core_path = os.path.join(super_dir, super_core_name)
        with open(super_core_path, encoding="utf-8") as fh:
            super_text = fh.read()
        super_fields, super_body = read_frontmatter(super_text)
        status, entries = planning_model.PlanningNode.parse_edge_register(
            super_fields.get(schema.Fields.SUB_NODES))
        old_rel_path = f"{os.path.basename(old_dir)}/{old_core_name}"
        new_rel_path = f"{new_folder_name}/{new_core_name}"
        if status == "ok":
            for entry in entries:
                if entry.get(schema.EdgeKeys.NAME) == old_name and \
                        entry.get(schema.EdgeKeys.PATH) == old_rel_path:
                    e = field_line_edit(super_text, super_core_path,
                                         "super sub_nodes[].name", "name",
                                         old_name, new_name, indent="      - ")
                    if e is None:
                        e = field_line_edit(super_text, super_core_path,
                                             "super sub_nodes[].name",
                                             "- name", old_name, new_name,
                                             indent="    ")
                    if e:
                        plan.edits.append(e)
                    e2 = field_line_edit(super_text, super_core_path,
                                          "super sub_nodes[].path", "path",
                                          old_rel_path, new_rel_path,
                                          indent="      ")
                    if e2:
                        plan.edits.append(e2)
                    break
            else:
                plan.notes.append(
                    f"{disp(super_core_path)}: no `sub_nodes` register "
                    f"entry named `{old_name}` pointing at {old_rel_path} "
                    f"— register left unchanged, reported rather than "
                    f"guessed at")
        else:
            plan.notes.append(
                f"{disp(super_core_path)}: `sub_nodes` register is "
                f"{status} — cannot update the register entry "
                f"mechanically")
        # the `## sub_nodes` (or superseded `## nodes`) projection link
        link_re = re.compile(
            r"^(\s*-\s*\[)" + re.escape(old_name) + r"(\]\()"
            + re.escape(old_rel_path) + r"(\))", re.M)
        lm = link_re.search(super_text)
        if lm:
            old_link = lm.group(0)
            new_link = f"{lm.group(1)}{new_name}{lm.group(2)}{new_rel_path}{lm.group(3)}"
            plan.edits.append(Edit(super_core_path, "super projection link",
                                    old_link, new_link))
        else:
            plan.notes.append(
                f"{disp(super_core_path)}: no `[{old_name}]({old_rel_path})` "
                f"link found in the projection — left unchanged")
    else:
        plan.notes.append(f"{disp(super_dir)}: no CORE — cannot update a "
                           f"super-node register that is not there")

    return plan, "rename"


def sweep_stray_references(root, old_name, addr, old_core_name,
                            new_name, new_core_name, old_id, new_id,
                            already_touched):
    """Every OTHER markdown document in the planning root that still
    names the old folder token, the old CORE filename, or the old
    dotted id — co-node links, stray mentions, anything the structural
    edits above did not already reach. Conservative on purpose: it
    matches only these three exact, compound tokens (never a bare
    `old_name`), so a prose sentence using the word for something else
    is never touched — the §6c lesson about bulk find-and-replace."""
    old_folder = f"node_{addr}_{old_name}"
    new_folder = f"node_{addr}_{new_name}"
    tokens = [(old_folder, new_folder, "folder token")]
    if old_core_name and new_core_name:
        tokens.append((old_core_name, new_core_name, "CORE filename"))
    if old_id and new_id:
        tokens.append((old_id, new_id, "dotted id"))

    edits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for fn in sorted(filenames):
            if not fn.lower().endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            if full in already_touched:
                continue
            with open(full, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            for old_tok, new_tok, label in tokens:
                if old_tok and old_tok in text:
                    # id token: refuse to match a LONGER id that merely
                    # starts with this one (e.g. this id plus a stray
                    # extra segment) by requiring the next character,
                    # if any, to not continue an identifier.
                    for m in re.finditer(re.escape(old_tok), text):
                        end = m.end()
                        if label == "dotted id" and end < len(text) \
                                and (text[end].isalnum() or text[end] == "_"):
                            continue
                        edits.append(Edit(full, f"stray {label}",
                                           old_tok, new_tok))
                        break
    return edits


def run_node_rename(root, old_name, new_name, apply_mode):
    print(f"planning root: {disp(root)}")
    print(f"node rename:   {old_name!r} -> {new_name!r}")
    print()

    clean_errors = tree_checks_clean(root)
    if clean_errors:
        print(f"!!! REFUSING: {disp(root)} does not check clean — "
              f"{len(clean_errors)} ERROR(s) before this tool touched "
              f"anything:")
        for f in clean_errors[:20]:
            print(f"    [{f.severity}] {f.category}: {f.summary}")
            for s in f.sightings[:3]:
                print(f"        - {s}")
        if len(clean_errors) > 20:
            print(f"    ... and {len(clean_errors) - 20} more")
        print("\nnothing written. Fix the tree first — a rename tool is "
              "not the place to also absorb pre-existing defects.")
        return 2

    plan, mode = plan_node_rename(root, old_name, new_name)
    if plan.problems:
        print("!!! REFUSING:")
        for p in plan.problems:
            print(f"    {p}")
        print("\nnothing written.")
        return 2

    for n in plan.notes:
        print(f"note: {n}")
    if plan.notes:
        print()

    touched_by_structural = {e.path for e in plan.edits}
    old_id = new_id = None
    old_core_name = new_core_name = None
    addr = None
    if mode == "rename":
        m = NODE_FOLDER_RE.match(os.path.basename(plan.dir_renames[-1][0]))
        addr = m.group(1)
        for old_p, new_p, label in plan.file_renames:
            if label == "CORE file":
                old_core_name = os.path.basename(old_p)
                new_core_name = os.path.basename(new_p)
        for e in plan.edits:
            if e.label == "id":
                old_id, new_id = e.old[len("id: "):], e.new[len("id: "):]

    sweep_edits = []
    if mode == "rename":
        sweep_edits = sweep_stray_references(
            root, old_name, addr, old_core_name, new_name, new_core_name,
            old_id, new_id, touched_by_structural)

    all_edits = plan.edits + sweep_edits
    verb = "would edit" if not apply_mode else "edited"
    vrename = "would rename" if not apply_mode else "renamed"

    print(f"=== structural changes ({len(plan.edits)}) ===")
    for e in plan.edits:
        detail = e.new.strip() if e.label != "provenance line" else \
            e.new.strip().splitlines()[-1]
        print(f"  {verb}: {disp(e.path)}  [{e.label}]")
        print(f"      {e.old.strip()[:90] or '(new line)'}")
        print(f"      -> {detail[:90]}")
    for old_p, new_p, label in plan.file_renames:
        print(f"  {vrename}: {disp(old_p)}")
        print(f"      -> {os.path.basename(new_p)}  [{label}]")
    for old_p, new_p, label in plan.dir_renames:
        print(f"  {vrename}: {disp(old_p)}/")
        print(f"      -> {os.path.basename(new_p)}/  [{label}]")

    if sweep_edits:
        print(f"\n=== stray references elsewhere in the tree "
              f"({len(sweep_edits)}) ===")
        for e in sweep_edits:
            print(f"  {verb}: {disp(e.path)}  [{e.label}]")
            print(f"      {e.old!r} -> {e.new!r}")

    if not plan.edits and not plan.file_renames and not plan.dir_renames \
            and not sweep_edits:
        print("  nothing to do.")

    if old_id and new_id:
        print(f"\nprovenance: id changed {old_id} -> {new_id} "
              f"(node-self-name forces the tail to match the new folder "
              f"name; the old id is recorded above in PROGRESS.md and "
              f"here, per this tool's own docstring)")

    if not apply_mode:
        print("\ndry run — nothing written. Re-run with --apply.")
        return 0

    apply_edits(all_edits)
    for old_p, new_p, _ in plan.file_renames:
        os.rename(old_p, new_p)
    for old_p, new_p, _ in plan.dir_renames:
        os.rename(old_p, new_p)
    print("\napplied.")
    return 0


# ------------------------------------------------------------- artifacts


def run_artifact_rename(old_dir, new_dir, scan_roots, apply_mode):
    old_dir = os.path.abspath(os.path.expanduser(old_dir))
    new_dir = os.path.abspath(os.path.expanduser(new_dir))
    print(f"\nartifact rename: {disp(old_dir)}  ->  {disp(new_dir)}")

    if not os.path.isdir(old_dir):
        print(f"!!! REFUSING: {disp(old_dir)} is not a directory")
        return 2
    if os.path.exists(new_dir):
        print(f"!!! REFUSING: collision — {disp(new_dir)} already exists")
        return 2

    old_base = os.path.basename(old_dir.rstrip("/"))
    new_base = os.path.basename(new_dir.rstrip("/"))
    # Matched only when preceded by a path separator, so a bare mention
    # of the artifact's name in prose (not naming the directory) is
    # never touched — the same conservative rule as the node sweep.
    pat = re.compile(r"(?<=[/\\])" + re.escape(old_base) + r"\b")

    def sweep(scan_dir):
        found = []
        for dirpath, dirnames, filenames in os.walk(scan_dir):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in sorted(filenames):
                ext = os.path.splitext(fn)[1]
                if ext not in TEXT_EXTS and fn != ".gitignore":
                    continue
                full = os.path.join(dirpath, fn)
                try:
                    with open(full, encoding="utf-8") as fh:
                        text = fh.read()
                except (OSError, UnicodeDecodeError):
                    continue
                if pat.search(text):
                    new_text = pat.sub(new_base, text)
                    n = sum(1 for a, b in zip(text.splitlines(),
                                               new_text.splitlines())
                            if a != b)
                    found.append((full, text, new_text, n))
        return found

    # Self-references inside the artifact directory, swept BEFORE the
    # move (paths are still valid there), so the moved directory lands
    # already internally consistent.
    self_hits = sweep(old_dir)
    external_hits = []
    for sroot in scan_roots:
        external_hits += [h for h in sweep(sroot) if not h[0].startswith(old_dir + os.sep)]

    verb = "would edit" if not apply_mode else "edited"
    vrename = "would rename" if not apply_mode else "renamed"
    print(f"  {vrename}: {disp(old_dir)}/  ->  {os.path.basename(new_dir)}/")
    print(f"\n  self-references inside the directory ({len(self_hits)}):")
    for full, _t, _n, n in self_hits:
        print(f"    {verb}: {disp(full)}  [{n} line(s)]")
    print(f"\n  references in the scanned roots ({len(external_hits)}):")
    for full, _t, _n, n in external_hits:
        print(f"    {verb}: {disp(full)}  [{n} line(s)]")

    if not apply_mode:
        print("\n  dry run — nothing written.")
        return 0

    for full, _t, new_text, _n in self_hits + external_hits:
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(new_text)
    shutil.move(old_dir, new_dir)
    print("\n  applied.")
    return 0


# ------------------------------------------------------------------ main


def main():
    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("planning_root")
    ap.add_argument("old_name")
    ap.add_argument("new_name")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--also-artifacts", action="append", default=[],
                     metavar="OLD_DIR=NEW_DIR")
    ap.add_argument("--scan-root", action="append", default=[],
                     metavar="DIR")
    args = ap.parse_args()

    root = os.path.abspath(os.path.expanduser(args.planning_root))
    if not os.path.isdir(root):
        print(f"!!! not a directory: {disp(root)}")
        return 2

    rc = run_node_rename(root, args.old_name, args.new_name, args.apply)
    if rc:
        return rc

    if not args.also_artifacts:
        return 0

    if args.scan_root:
        scan_roots = [os.path.abspath(os.path.expanduser(r))
                      for r in args.scan_root]
    else:
        repo_dir = checks.NodeSelfCheck.repo_dir_of(
            root, os.path.expanduser("~/Programming"))
        scan_roots = [repo_dir or os.path.dirname(root)]
    for r in scan_roots:
        if not os.path.isdir(r):
            print(f"!!! not a directory, dropped from scan roots: {disp(r)}")
    scan_roots = [r for r in scan_roots if os.path.isdir(r)]
    print(f"\nscan roots for artifact references: "
          f"{', '.join(disp(r) for r in scan_roots)}")

    for spec in args.also_artifacts:
        if "=" not in spec:
            print(f"!!! --also-artifacts needs OLD_DIR=NEW_DIR, got: {spec}")
            return 2
        old_dir, new_dir = spec.split("=", 1)
        rc = run_artifact_rename(old_dir, new_dir, scan_roots, args.apply)
        if rc:
            return rc
    return 0


if __name__ == "__main__":
    sys.exit(main())
