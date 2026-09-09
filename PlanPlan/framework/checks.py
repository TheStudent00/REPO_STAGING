#!/usr/bin/env python3
"""Consistency checks for one or more planning trees.

Each check is one class with a `run` method: given the roots in view
(as `(root_path, label)` pairs — "trees/labels") and the Programming
root, it returns a list of `Finding`s. `Checker` runs every check and
prints the report in `check_plans.py`'s format: grouped by category,
then the CONFORMANCE GAPS banner.

Imports `planning_model` only. No dependencies beyond the standard
library.
"""
import fnmatch
import os
import re

import planning_model
import schema

# The generated sections a CORE may carry ahead of its sub-node listing.
# PROTOCOL §407 (2026-08-23) projects `## metadata` first, always, then
# `## super_node`, then `## sub_nodes`. These are PROJECTIONS of the
# register, not prose, so they do not stand between a reader and what is
# beneath a node. Anything else appearing first does.
PROJECTION_SECTIONS = {"metadata", "super_node", "super node"}


def is_projection_section(heading):
    """Is this heading one of the generated projections?

    `sections_of` answers headings with their markdown prefix intact
    ('## metadata'), so the prefix is stripped before comparing.
    """
    return heading.lstrip("#").strip().lower() in PROJECTION_SECTIONS

PATH_RE = re.compile(r"~/Programming/[^\s`)]*")

# A line carrying this marker is exempt from the dangling-path check.
# It exists because the project's rule is to ANNOTATE a reference to
# something that has gone, not delete it — a fallen position keeps its
# record and its reason. Without an exemption, writing "it used to
# live at X" is indistinguishable from a stale pointer at X, and the
# check would push writers toward deleting the history instead.
#
# Put the marker anywhere on the line:
#     `~/Programming/PseudoCoup_v6/Tools/slicer/` (historical)
#
# Keep it to lines where the path is genuinely being described in the
# past tense. A marker used to silence a real stale pointer turns the
# check off exactly where it was working.
HISTORICAL_RE = re.compile(r"\(historical\)", re.I)
WORD_SPLIT_RE = re.compile(r"\s+")


class Finding:
    """One reported cause, with every place it was sighted."""

    def __init__(self, severity, category, summary, sightings=None, detail=None):
        self.severity = severity  # "ERROR" or "WARN"
        self.category = category
        self.summary = summary
        self.sightings = sightings or []
        self.detail = detail or []


class Check:
    """Base for one framework-wide consistency check."""

    PROGRAMMING_ROOT = os.path.expanduser("~/Programming")
    name = ""
    severity = "ERROR"

    def run(self, roots, programming_root):
        """roots is a list of (root_path, label) pairs already confirmed
        to exist. Returns a list of Finding."""
        raise NotImplementedError

    @classmethod
    def disp(cls, path):
        """Render an absolute path under ~/Programming in that short form,
        for readable diagnostics. Purely cosmetic — resolution always uses
        the real absolute path."""
        ap = os.path.abspath(path)
        if ap == cls.PROGRAMMING_ROOT or ap.startswith(cls.PROGRAMMING_ROOT + os.sep):
            return "~/Programming" + ap[len(cls.PROGRAMMING_ROOT):]
        return ap

    @staticmethod
    def walk_nodes(root):
        """Yield every node folder under a planning root, root included.

        A node folder is one holding a CORE file. Dotted folders (.archive
        and friends) are not nodes and are not walked into."""
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            if any(planning_model.CORE_RE.match(fn) for fn in filenames):
                yield dirpath, sorted(filenames)


class ArchiveNameCheck(Check):
    """Archive folders are named `.archive`, lower case (PROTOCOL §1c).

    Any dotted folder is skipped by every walk, so a mis-cased one does
    no harm to the grammar checks — but `StaleArchiveCheck` looks for
    `.archive` BY NAME, so a `.ARCHIVE` is invisible to it and
    references into it are never reclassified as archived. The folder
    then half-works: hidden from the checks that should ignore it, and
    also hidden from the one check that should read it.

    WARN rather than ERROR: the content is safe either way, and the fix
    is a rename."""

    name = "archive-name"
    severity = "WARN"

    def run(self, roots, programming_root):
        wrong = []
        for root, label in roots:
            for dirpath, dirnames, _ in os.walk(root):
                for d in dirnames:
                    if d.startswith(".") and d.lower() == ".archive" \
                            and d != ".archive":
                        wrong.append(f"{self.disp(os.path.join(dirpath, d))}"
                                     f" — rename to `.archive`")
                dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        if not wrong:
            return []
        return [Finding(
            "WARN", "archive-name",
            f"{len(wrong)} archive folder(s) not named `.archive` "
            f"(PROTOCOL §1c) — the stale-archive check cannot read them",
            sightings=wrong)]


class GrammarCheck(Check):
    """Per-node folder grammar: exactly one CORE, a PROGRESS, any SUPPORT
    files, and sub-node folders — nothing else. Ported verbatim from
    `render_plan.py`'s old `scan_node` — the grammar-checking half of it;
    `render_plan.py` now holds no checking logic of its own and gets
    these same problems from `GrammarCheck.scan` for its own display."""

    name = "grammar"
    severity = "ERROR"

    def run(self, roots, programming_root):
        items = []
        for root, label in roots:
            for address, dirpath, problems in self.scan(root, os.path.basename(root)):
                for p in problems:
                    items.append(Finding(
                        "ERROR", "grammar",
                        f"{label}: {address} — {p}",
                        sightings=[self.disp(dirpath)],
                    ))
        return items

    @classmethod
    def scan(cls, dirpath, address):
        """Walk one node folder and its sub-nodes. Yields
        (address, dirpath, problems) for dirpath, then for every
        sub-node beneath it. A node folder holds exactly one CORE, a
        PROGRESS, any SUPPORT files, and sub-node folders — nothing
        else."""
        problems, cores, supports, subdirs, strays = [], [], [], [], []
        checks_ = []
        has_progress = False

        for entry in sorted(os.listdir(dirpath)):
            full = os.path.join(dirpath, entry)
            if entry.startswith("."):
                continue
            if os.path.isdir(full):
                (subdirs if planning_model.NODE_RE.match(entry) else strays).append(entry)
                continue
            if planning_model.CORE_RE.match(entry):
                cores.append(entry)
            elif entry == "PROGRESS.md":
                has_progress = True
            elif planning_model.SUPPORT_RE.match(entry):
                supports.append(entry)
            elif entry == "DASHBOARD.md":
                # generated by generate_dashboards.py — a legitimate node file,
                # not hand-written and not a stray (framework §1).
                continue
            elif planning_model.CHECK_RE.match(entry):
                checks_.append(entry)
            else:
                strays.append(entry)

        if len(cores) == 0:
            problems.append("no CORE file")
        elif len(cores) > 1:
            problems.append(f"{len(cores)} CORE files: {', '.join(cores)}")
        if not has_progress:
            problems.append("no PROGRESS.md")
        for s in strays:
            problems.append(f"stray: {s}")

        core = planning_model.PlanningNode.read_core(
            os.path.join(dirpath, cores[0])) if cores else None
        if core is not None and not core["fields"]:
            problems.append("CORE has no frontmatter")

        # --- checks learned the hard way, 2026-07-31. Each of these caught a
        # real defect during the PseudoCoup/PseudoIR split, where a bulk rename
        # changed filenames and left everything inside them stale.
        node_id = core["fields"].get("id") if core else None
        core_body = ""
        if cores:
            with open(os.path.join(dirpath, cores[0]), encoding="utf-8") as fh:
                core_body = fh.read()

        # the address in the folder name decides the level; segments minus one,
        # since every level-1 node shares the leading "1"
        if core is not None:
            m = re.match(r"^node_((?:\d+_)*\d+)_", os.path.basename(dirpath))
            depth = 0 if m is None else len(m.group(1).split("_")) - 1
            declared = core["fields"].get("level")
            if declared is not None and declared != str(depth):
                problems.append(f"level {declared} but folder depth {depth}")
            head = re.search(r"CORE\s+([0-9_]+)", core["title"] or "")
            if m and head and head.group(1) != m.group(1):
                problems.append(
                    f"heading says CORE {head.group(1)}, folder says {m.group(1)}")

        # A CHECK file mirrors its CORE's name with any extension. Getting
        # that wrong is the same defect class as a SUPPORT file whose name
        # and id disagree: the file survives a rename of the thing it
        # belongs to and then describes something else.
        if len(checks_) > 1:
            problems.append(f"{len(checks_)} CHECK files: {', '.join(sorted(checks_))}")
        if checks_ and cores:
            want = os.path.splitext(cores[0])[0][len("CORE"):]   # "_1_0_tools"
            got = os.path.splitext(checks_[0])[0][len("CHECK"):]
            if want != got:
                problems.append(
                    f"{checks_[0]}: name does not mirror {cores[0]} "
                    f"(expected CHECK{want}.<ext>)")

        for s in supports:
            sfields, stext = planning_model.PlanningNode.read_frontmatter(open(
                os.path.join(dirpath, s), encoding="utf-8").read())
            sid = sfields.get("id", "")
            want = f"{node_id}.support." if node_id else None
            if want and not sid.startswith(want):
                problems.append(f"{s}: id {sid or '(none)'} not under {want}")
            elif want and s != "SUPPORT_" + sid[len(want):] + ".md":
                problems.append(f"{s}: filename does not match its id {sid}")
            hm = re.search(r"^# SUPPORT — (.*)$", stext, re.M)
            if hm and hm.group(1).replace(" ", "_").replace(":", "").lower() \
                    != s[len("SUPPORT_"):-3]:
                problems.append(f"{s}: heading says '{hm.group(1)}'")
            if f"({s})" not in core_body:
                problems.append(f"{s}: present but not listed in the CORE")

        linked = set(re.findall(r"\((node_[^/)]+)/", core_body))
        for d in subdirs:
            if d not in linked:
                problems.append(f"sub-node {d} not listed in the CORE")
        for d in linked - set(subdirs):
            problems.append(f"CORE lists sub-node {d}, which is not here")

        # The sub-node listing comes before any PROSE section (framework §1,
        # the owner 2026-07-31). A reader should not have to scroll past prose to
        # find out what is beneath a node. Checked by section rather than by
        # heading word, so a project may call the section what it likes.
        #
        # The other PROJECTIONS may precede it. PROTOCOL §407, updated
        # 2026-08-23, projects `## metadata` "first, always", immediately
        # ahead of `## super_node` and `## sub_nodes` — so requiring the
        # sub-node listing in absolute first position contradicted the
        # protocol the moment the metadata projection shipped, and failed
        # every CORE in every conforming tree at once. Projections are not
        # prose: scrolling past them is not what the rule guards against.
        if subdirs and core is not None:
            sections = core["sections"]
            if not sections:
                problems.append("sub-nodes exist but the CORE has no sections")
            else:
                lead = []
                for heading, body in sections:
                    lead.append((heading, body))
                    if set(re.findall(r"\((node_[^/)]+)/", "\n".join(body))):
                        break
                scanned = "\n".join(
                    line for _, body in lead for line in body)
                lead_links = set(re.findall(r"\((node_[^/)]+)/", scanned))
                missing = set(subdirs) - lead_links
                prose = [h for h, _ in lead[:-1]
                         if not is_projection_section(h)]
                if missing:
                    problems.append(
                        f"sub-node listing is not among the leading sections "
                        f"(first is '{sections[0][0]}'; "
                        f"{', '.join(sorted(missing))} listed later)")
                elif prose:
                    problems.append(
                        f"prose section '{prose[0]}' precedes the sub-node "
                        f"listing; only projections "
                        f"({', '.join(sorted(PROJECTION_SECTIONS))}) may")

        yield address, dirpath, problems
        for d in subdirs:
            yield from cls.scan(os.path.join(dirpath, d), d)


class DanglingPathCheck(Check):
    """~/Programming/... references that do not resolve on disk. Also
    feeds the stale-.archive reclassification: a subset of these where
    the referenced thing turns out to be archived."""

    name = "dangling-path"
    severity = "ERROR"

    TRAILING_PUNCT = ".,;)`"

    @staticmethod
    def iter_markdown_files(root):
        """Every non-hidden .md file under root, sorted for determinism."""
        out = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            for fn in sorted(filenames):
                if fn.startswith("."):
                    continue
                if fn.lower().endswith(".md"):
                    out.append(os.path.join(dirpath, fn))
        return sorted(out)

    @classmethod
    def strip_trailing_punct(cls, p):
        was_dir = p.endswith("/")
        s = p
        while s and s[-1] in cls.TRAILING_PUNCT:
            s = s[:-1]
        if was_dir and not s.endswith("/"):
            s += "/"
        return s

    @staticmethod
    def repo_root_for(path_text, programming_root):
        """The top-level project directory a `~/Programming/<X>/...` path
        names, e.g. `~/Programming/PseudoCoup_v6` for anything under it."""
        rel = os.path.relpath(os.path.expanduser(path_text), programming_root)
        if rel.startswith(".."):
            return None
        first = rel.split(os.sep)[0]
        return os.path.join(programming_root, first)

    def run(self, roots, programming_root):
        # cause path-text -> list of (file, line_no)
        sightings = {}
        for root, label in roots:
            for md in self.iter_markdown_files(root):
                with open(md, encoding="utf-8", errors="replace") as fh:
                    lines = fh.read().splitlines()
                for lineno, line in enumerate(lines, start=1):
                    if HISTORICAL_RE.search(line):
                        # A deliberately historical reference: the path is
                        # named BECAUSE it no longer exists. This is the owner's
                        # "annotate rather than remove" rule (the
                        # PCv5-archived-research annotation) made
                        # mechanical — see HISTORICAL_RE for the marker.
                        continue
                    for m in PATH_RE.finditer(line):
                        raw = m.group(0)
                        cleaned = self.strip_trailing_punct(raw)
                        if not cleaned:
                            continue
                        real = os.path.expanduser(cleaned)
                        if os.path.exists(real):
                            continue
                        sightings.setdefault(cleaned, []).append((md, lineno))

        dangling_items = []
        stale_items = []
        for path_text in sorted(sightings):
            sites = sightings[path_text]
            basename = os.path.basename(path_text.rstrip("/"))
            suggestion = None
            if basename:
                repo_root = self.repo_root_for(path_text, programming_root)
                if repo_root and os.path.isdir(repo_root):
                    for dirpath, dirnames, filenames in os.walk(repo_root):
                        dirnames[:] = [d for d in dirnames if not d.startswith(".") or d == ".archive"]
                        if os.path.basename(dirpath) == ".archive" or \
                           f"{os.sep}.archive{os.sep}" in dirpath + os.sep:
                            candidates = fnmatch.filter(filenames, basename)
                            for c in candidates:
                                suggestion = os.path.join(dirpath, c)
                                break
                            if not candidates and basename in dirnames:
                                suggestion = os.path.join(dirpath, basename)
                            if suggestion:
                                break

            site_strs = [f"{self.disp(md)}:{ln}" for md, ln in sorted(sites)]
            if suggestion:
                stale_items.append(Finding(
                    "ERROR", "stale-archive",
                    f"{path_text} does not exist, but a matching name was "
                    f"found archived at {self.disp(suggestion)} — repoint or restore",
                    sightings=site_strs,
                ))
            else:
                dangling_items.append(Finding(
                    "ERROR", "dangling-path",
                    f"{path_text} does not exist",
                    sightings=site_strs,
                ))
        return dangling_items + stale_items


class DuplicateProseCheck(Check):
    """Prose duplicated across trees.

    DASHBOARD.md and CHECK_* are excluded from the CONTENT comparison.
    Both are templated — a dashboard's header and a check's question
    are identical in every node by construction — so comparing them
    reports the tool's own boilerplate rather than a real duplicate,
    on every run, forever.

    Excluded here does NOT mean unchecked. Both are checked for
    EXISTENCE in RequiredFilesCheck, which is the check that actually
    matters for them (the owner, 2026-07-31: "the check can be for
    existence: does DASHBOARD, CHECK, ... exist?"). Content-sameness
    is the expected state for a generated or templated file; absence
    is the defect."""

    name = "duplicated-prose"
    severity = "WARN"

    @staticmethod
    def normalize_line(line):
        return WORD_SPLIT_RE.sub(" ", line.strip())

    @classmethod
    def qualifying_runs(cls, text):
        """Maximal runs of >=3 consecutive non-blank, non-heading lines of
        40+ characters. Returns [(start_line_1indexed, [normalized_lines])]."""
        runs = []
        cur_start = None
        cur_lines = []
        for i, line in enumerate(text.splitlines(), start=1):
            s = line.strip()
            qualifies = bool(s) and not s.startswith("#") and len(s) >= 40
            if qualifies:
                if cur_start is None:
                    cur_start = i
                cur_lines.append(cls.normalize_line(line))
            else:
                if cur_start is not None and len(cur_lines) >= 3:
                    runs.append((cur_start, cur_lines))
                cur_start, cur_lines = None, []
        if cur_start is not None and len(cur_lines) >= 3:
            runs.append((cur_start, cur_lines))
        return runs

    @staticmethod
    def lcs_substrings(a, b, min_len=3):
        """All maximal contiguous common substrings of two line lists, each
        at least min_len long. Returns [(a_start0, b_start0, length)]."""
        la, lb = len(a), len(b)
        dp = [[0] * (lb + 1) for _ in range(la + 1)]
        matches = []
        for i in range(1, la + 1):
            for j in range(1, lb + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = 0
        for i in range(1, la + 1):
            for j in range(1, lb + 1):
                length = dp[i][j]
                if length < min_len:
                    continue
                # only report at the maximal (non-extendable) point
                extends = i < la and j < lb and dp[i + 1][j + 1] == length + 1
                if extends:
                    continue
                matches.append((i - length, j - length, length))
        return matches

    def run(self, roots, programming_root):
        # gather all runs: (root_label, file, start_line, lines)
        all_runs = []
        for root, label in roots:
            for md in DanglingPathCheck.iter_markdown_files(root):
                base = os.path.basename(md)
                if base == "DASHBOARD.md" or base.startswith("CHECK_"):
                    continue
                with open(md, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
                for start, lines in self.qualifying_runs(text):
                    all_runs.append((label, md, start, lines))

        # group[key] -> set of (file, start_line, length) ; key -> (root set)
        groups = {}  # key text -> {"sites": set((md,line,length)), "roots": set()}
        for idx_a in range(len(all_runs)):
            label_a, md_a, start_a, lines_a = all_runs[idx_a]
            for idx_b in range(idx_a + 1, len(all_runs)):
                label_b, md_b, start_b, lines_b = all_runs[idx_b]
                if label_a == label_b:
                    continue
                for a0, b0, length in self.lcs_substrings(lines_a, lines_b):
                    key = " ".join(lines_a[a0:a0 + length])
                    g = groups.setdefault(key, {"sites": set(), "roots": set()})
                    g["sites"].add((md_a, start_a + a0, length))
                    g["sites"].add((md_b, start_b + b0, length))
                    g["roots"].add(label_a)
                    g["roots"].add(label_b)

        items = []
        for key in sorted(groups):
            g = groups[key]
            if len(g["roots"]) < 2:
                continue
            snippet = key[:200]
            sites = sorted(g["sites"])
            site_strs = [f"{self.disp(md)}:{ln} ({length} lines)" for md, ln, length in sites]
            items.append(Finding(
                "WARN", "duplicated-prose",
                f"shared by {len(set(s[0] for s in sites))} files across "
                f"{len(g['roots'])} roots: “{snippet}”",
                sightings=site_strs,
            ))
        return items


class IdCollisionCheck(Check):
    """A frontmatter `id` declared more than once."""

    name = "id-collision"
    severity = "ERROR"

    def run(self, roots, programming_root):
        # id -> [(root_label, core_path)]
        ids = {}
        for root, label in roots:
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
                for fn in sorted(filenames):
                    if planning_model.CORE_RE.match(fn):
                        full = os.path.join(dirpath, fn)
                        with open(full, encoding="utf-8", errors="replace") as fh:
                            fields, _ = planning_model.PlanningNode.read_frontmatter(fh.read())
                        nid = fields.get("id")
                        if nid:
                            ids.setdefault(nid, []).append((label, full))

        items = []
        for nid in sorted(ids):
            entries = ids[nid]
            if len(entries) < 2:
                continue
            roots_involved = sorted(set(r for r, _ in entries))
            cross_root = len(roots_involved) > 1
            kind = "across different roots" if cross_root else "within one root"
            items.append(Finding(
                "ERROR", "id-collision",
                f"id '{nid}' declared {len(entries)} times, {kind}",
                sightings=[f"{r}: {self.disp(p)}" for r, p in sorted(entries)],
            ))
        return items


class RequiredFilesCheck(Check):
    """Every node folder carries a CHECK and a DASHBOARD.

    Added 2026-07-31 at the owner's request: "should check_plans check for
    checks? yeah. if checks dont exist in nodes, how will it check
    sub-nodes?"

    That reasoning is the point. A node's completeness check is
    answered by its sub-nodes' checks, so one missing CHECK does not
    fail one node — it makes every node above it unanswerable.

    DASHBOARD is checked the same way for a different reason: it is
    generated, so a missing one does not mean somebody forgot to write
    it, it means the generator was not run. Both are ERRORs: the first
    breaks the rollup, the second means the tree on disk and the tree
    described do not match.

    Note this is EXISTENCE only. It says nothing about whether a check
    passes — that is the check's own business, and for a by-hand check
    it is a person's."""

    name = "missing-check"
    severity = "ERROR"

    def run(self, roots, programming_root):
        missing_check = {}
        missing_dash = {}
        for root, label in roots:
            for dirpath, filenames in self.walk_nodes(root):
                if not any(f.startswith("CHECK_") for f in filenames):
                    missing_check.setdefault("check", []).append(self.disp(dirpath))
                if "DASHBOARD.md" not in filenames:
                    missing_dash.setdefault("dash", []).append(self.disp(dirpath))

        items = []
        if missing_check:
            sites = missing_check["check"]
            items.append(Finding(
                "ERROR", "missing-check",
                f"{len(sites)} node(s) have no CHECK file — every node above "
                f"them is unanswerable, since a node's completeness is read "
                f"off its sub-nodes' checks",
                sightings=sites))
        if missing_dash:
            sites = missing_dash["dash"]
            items.append(Finding(
                "ERROR", "missing-dashboard",
                f"{len(sites)} node(s) have no DASHBOARD.md — run "
                f"generate_dashboards.py; it is produced, not written",
                sightings=sites))
        return items


class NodesRegisterCheck(Check):
    """The `nodes` register versus the folders on disk.

    - register missing or malformed: WARN, the `designation`
      precedent — pre-existing trees conform branch by branch as they
      are deepened, not by a sweep.
    - folder the register does not name: ERROR — unreachable
      top-down.
    - registered entry with no folder: INFO — planned, not yet
      generated. This is the generation seed, not a defect.
    - registered entry whose folder exists under a different index
      than its register position: ERROR — address and register
      disagree."""

    name = "nodes-register"
    severity = "WARN"

    def run(self, roots, programming_root):
        missing = []       # CORE with no/malformed nodes field
        unrealized = []    # registered entry with no folder
        unlisted = []      # folder the register does not name
        misindexed = []    # folder index disagrees with register order
        for root, label in roots:
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
                core = next((f for f in filenames if planning_model.CORE_RE.match(f)), None)
                if core is None:
                    continue
                full = os.path.join(dirpath, core)
                with open(full, encoding="utf-8", errors="replace") as fh:
                    fields, _ = planning_model.PlanningNode.read_frontmatter(fh.read())
                entries = planning_model.PlanningNode.register_entries_of(fields)
                if entries is None:
                    missing.append(
                        f"{self.disp(full)} (no readable register: neither "
                        f"`sub_nodes` nor the superseded `nodes`)")
                    continue
                register = [e["name"] for e in entries]
                folders = [d for d in dirnames if d.startswith("node_")]
                # folder -> (index, title): node_<addr>_<i>_<title>
                by_title = {}
                for d in folders:
                    m = re.match(r"node_(?:\d+_)*(\d+)_([a-z0-9_]+)$", d)
                    if m:
                        by_title[m.group(2)] = (int(m.group(1)), d)
                for i, entry_ in enumerate(entries):
                    title = entry_["name"]
                    if entry_.get("realize") is False:
                        # In-file structure (PROTOCOL §1): never a
                        # folder, so "unrealized" would be noise — but
                        # a folder appearing under its name IS a
                        # defect: the entry says in-file, the disk says
                        # folder, and only one can be right.
                        if title in by_title:
                            misindexed.append(
                                f"{self.disp(full)}: {title} is "
                                f"`realize: false` but folder "
                                f"{by_title[title][1]} exists")
                        continue
                    if title not in by_title:
                        unrealized.append(f"{self.disp(full)}: {title}")
                    elif by_title[title][0] != i:
                        misindexed.append(
                            f"{self.disp(full)}: {title} is register entry {i} "
                            f"but folder {by_title[title][1]}")
                for title, (_, d) in by_title.items():
                    if title not in register:
                        unlisted.append(f"{self.disp(full)}: {d}")
        items = []
        if missing:
            items.append(Finding(
                "WARN", "nodes-register",
                f"frontmatter `nodes` register missing or malformed on "
                f"{len(missing)} CORE(s) (required on every CORE per "
                f"PROTOCOL §1, 2026-08-01; `[]` for a leaf)",
                sightings=missing))
        if unlisted:
            items.append(Finding(
                "ERROR", "nodes-register",
                f"{len(unlisted)} sub-node folder(s) not in their CORE's "
                f"`nodes` register — unreachable top-down",
                sightings=unlisted))
        if misindexed:
            items.append(Finding(
                "ERROR", "nodes-register",
                f"{len(misindexed)} sub-node folder(s) whose index "
                f"disagrees with register order",
                sightings=misindexed))
        if unrealized:
            items.append(Finding(
                "INFO", "unrealized-nodes",
                f"{len(unrealized)} registered sub-node(s) have no folder "
                f"yet (planned, not generated — the generation seed)",
                sightings=unrealized))
        return items


class ProjectionCheck(Check):
    """The `## sub_nodes` section (superseded form `## nodes` still
    accepted while trees migrate) versus the register it projects.

    the owner, 2026-08-01: "we can still automate checks that `## nodes`
    match the YAML. i just dont want `## nodes` to be ground truth."
    So the section is never READ FOR TRUTH — the register is — but it
    is checked for existence, for first-section position, and for
    agreeing with the register it is derived from.

    A disagreement is an ERROR and its fix is mechanical:
    `generate_nodes.py <root> --projections --apply`. Same contract as
    DASHBOARD.md — generated content that disagrees with its source
    means the generator was not re-run."""

    name = "projection"
    severity = "ERROR"

    @staticmethod
    def node_chain(dirpath, root):
        """The address chain of a node folder ('node_0_0_tools' -> '0_0');
        the planning root itself is '0' (renumbered 2026-08-05, see
        `generate_nodes.chain_of`)."""
        if os.path.abspath(dirpath) == os.path.abspath(root):
            return "0"
        m = re.match(r"^node_((?:\d+_)*\d+)_[a-z0-9_]+$",
                     os.path.basename(dirpath))
        return m.group(1) if m else "?"

    def run(self, roots, programming_root):
        missing, misplaced, disagreeing = [], [], []
        for root, label in roots:
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
                core = next((f for f in filenames if planning_model.CORE_RE.match(f)), None)
                if core is None:
                    continue
                full = os.path.join(dirpath, core)
                with open(full, encoding="utf-8", errors="replace") as fh:
                    fields, body = planning_model.PlanningNode.read_frontmatter(fh.read())
                register = planning_model.PlanningNode.register_of(fields)
                if register is None:
                    continue  # no register yet; NodesRegisterCheck reports it
                secs = planning_model.PlanningNode.sections_of(body)
                # `## sub_nodes` since 2026-08-02; the superseded
                # `## nodes` is still accepted while trees migrate —
                # same contract as the `nodes` frontmatter key. Either
                # form counts as "the projection"; --projections
                # rewrites the heading to the current form.
                heading_forms = schema.Sections.SUB_NODES_FORMS
                present = next((h for h in secs if h in heading_forms), None)
                if present is None:
                    missing.append(self.disp(full))
                    continue
                if secs[0] not in heading_forms:
                    misplaced.append(f"{self.disp(full)} (first section is "
                                     f"“{secs[0]}”)")
                else:
                    # Nothing between the title and the projection (the owner,
                    # 2026-08-01: "not prose. nothing between the core
                    # title and nodes section").
                    for ln in body.splitlines():
                        if ln.startswith("## "):
                            break
                        if ln.strip() and not ln.startswith("# "):
                            misplaced.append(
                                f"{self.disp(full)} (prose between the title "
                                f"and `{present}`: “{ln.strip()[:50]}”)")
                            break
                # projected names, in order, versus the register's realized
                # entries — the only comparison made against the markdown
                projected, in_nodes, fenced = [], False, False
                for line in body.splitlines():
                    if line.lstrip().startswith("```"):
                        fenced = not fenced
                        continue
                    if not fenced and line.startswith("## "):
                        in_nodes = line.strip() in heading_forms
                        continue
                    if in_nodes:
                        m = re.match(r"^\s*-\s*\[([^\]]+)\]", line)
                        if m:
                            projected.append(m.group(1).strip())
                realized = [t for i, t in enumerate(register)
                            if os.path.isdir(os.path.join(
                                dirpath, f"node_{self.node_chain(dirpath, root)}"
                                         f"_{i}_{t}"))]
                if projected != realized:
                    disagreeing.append(
                        f"{self.disp(full)}: projects {projected or '[]'}, "
                        f"register realizes {realized or '[]'}")
        items = []
        heading = schema.Sections.SUB_NODES
        if disagreeing:
            items.append(Finding(
                "ERROR", "projection",
                f"`{heading}` disagrees with the register on "
                f"{len(disagreeing)} CORE(s) — rerun "
                f"`generate_nodes.py <root> --projections --apply`",
                sightings=disagreeing))
        if missing:
            items.append(Finding(
                "WARN", "projection",
                f"`{heading}` section absent on {len(missing)} CORE(s) that "
                f"have a register (required on every CORE per PROTOCOL §1)",
                sightings=missing))
        if misplaced:
            items.append(Finding(
                "WARN", "projection",
                f"`{heading}` is not the first section on {len(misplaced)} "
                f"CORE(s)", sightings=misplaced))
        return items


class DesignationCheck(Check):
    """Missing `designation`, plus the settle-guard: a settled node may
    not still carry the coarse kind `code (object)`."""

    name = "missing-designation"
    severity = "WARN"

    def run(self, roots, programming_root):
        total = 0
        missing = 0
        per_root = {}
        unresolved = []
        for root, label in roots:
            r_total = 0
            r_missing = 0
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
                for fn in sorted(filenames):
                    if planning_model.CORE_RE.match(fn):
                        full = os.path.join(dirpath, fn)
                        with open(full, encoding="utf-8", errors="replace") as fh:
                            fields, _ = planning_model.PlanningNode.read_frontmatter(fh.read())
                        r_total += 1
                        if not fields.get("designation"):
                            r_missing += 1
                        # The settle-guard (PROTOCOL §3a): `code (object)`
                        # is the coarse kind — deferral is allowed, but a
                        # node may not SETTLE still carrying it.
                        elif (fields.get("status") == "settled"
                              and "code (object)" in fields["designation"]):
                            unresolved.append(full)
            total += r_total
            missing += r_missing
            per_root[label] = (r_missing, r_total)

        items = []
        if unresolved:
            items.append(Finding(
                "ERROR", "unresolved-object",
                "settled node still carries the coarse kind `code (object)` "
                "(PROTOCOL §3a settle-guard: refine to a specific kind "
                "before settling)",
                sightings=unresolved,
            ))

        if missing == 0:
            return items
        detail = [f"{label}: {m} of {t}" for label, (m, t) in sorted(per_root.items())]
        items.append(Finding(
            "WARN", "missing-designation",
            f"designation missing on {missing} of {total} nodes "
            f"(not enforced until the conformance pass)",
            sightings=detail,
        ))
        return items


class CompletenessCheck(Check):
    """Report how much of each tree is complete. Never an error.

    the owner's rule, 2026-07-31: "a node being complete means its sub-nodes
    are complete. if a node is a leaf with no sub-nodes, it is
    complete", plus the part that makes it bite — "there is a
    difference between an intentionally empty list vs a list that wont
    be empty eventually. but we have things like 'draft' codifications
    to indicate an incomplete node."

    So `status` carries the difference, and completeness is:

        complete(node) = status is settled AND every sub-node complete

    A settled leaf is complete. A draft leaf is not, whether it is a
    leaf on purpose or has simply not been decomposed yet — which is
    what stops the recursion bottoming out at "everything is complete".

    Being incomplete is a STATE, not a defect. A tree mid-construction
    is supposed to be incomplete, so this reports and never fails."""

    name = "completeness"
    severity = "INFO"

    def run(self, roots, programming_root):
        lines = []
        for root, label in roots:
            status_of = {}
            subs_of = {}
            for dirpath, filenames in self.walk_nodes(root):
                core = next(f for f in filenames if planning_model.CORE_RE.match(f))
                with open(os.path.join(dirpath, core), encoding="utf-8",
                          errors="replace") as fh:
                    fields, _ = planning_model.PlanningNode.read_frontmatter(fh.read())
                status_of[dirpath] = fields.get("status", "")
                subs_of[dirpath] = [
                    os.path.join(dirpath, d) for d in sorted(os.listdir(dirpath))
                    if d.startswith("node_")
                    and os.path.isdir(os.path.join(dirpath, d))]

            def complete(node):
                if status_of.get(node) != "settled":
                    return False
                return all(complete(s) for s in subs_of.get(node, []))

            done = sum(1 for n in status_of if complete(n))
            total = len(status_of)
            leaves = sum(1 for n in status_of if not subs_of.get(n))
            lines.append(f"{label}: {done} of {total} complete "
                         f"({leaves} leaves)")

        return [Finding("INFO", "completeness",
                     "complete = settled AND all sub-nodes complete",
                     sightings=lines)]


class EdgeRegisterCheck(Check):
    """`super_node` and `sub_nodes` — the fields that state where a node
    sits (PROTOCOL §1, the owner, 2026-08-02).

    Before these fields existed, a node's place inside its own tree was
    computed from its folder position, and its place relative to ANY
    OTHER tree was a sentence. A sentence resolves or does not resolve;
    it cannot be wrong in an interesting way. These fields make the
    edge a statement, and a statement can be checked.

    What is reported, and why each severity:

    - field absent: WARN. Every tree predates the fields, so erroring
      would refuse every commit until 52 nodes were rewritten at once
      — the sweep §6c warns against. Conformance comes chain by chain.
    - field malformed: ERROR. A malformed edge is not a node waiting
      to conform; it is a node claiming something unreadable.
    - an edge naming a file that does not exist: ERROR.
    - an edge stated at one end only: ERROR. `A.sub_nodes` naming B
      obliges `B.super_node` to name A, and the reverse.
    - the two ends naming different files: ERROR. This is the case
      nothing could catch before — a node attached to the wrong place,
      with both halves individually resolving."""

    name = "edge-register"
    severity = "WARN"

    @staticmethod
    def resolve(entry_path, core_path):
        """An edge's `path`, as an absolute path. Relative entries are
        relative to the folder holding the CORE that states them;
        `~/Programming/...` entries are absolute already. Cross-tree
        edges must use the absolute form, per §6a — the two trees move
        independently, so a relative path between them breaks the first
        time either one moves."""
        if entry_path.startswith("~"):
            return os.path.abspath(os.path.expanduser(entry_path))
        return os.path.abspath(os.path.join(os.path.dirname(core_path), entry_path))

    @classmethod
    def read_edges(cls, core_path):
        """(super_status, super_entry, sub_status, sub_entries) for one
        CORE, read straight from disk. Deliberately not limited to the
        roots in view: the far end of a cross-tree edge is usually in a
        tree nobody passed on the command line, and refusing to look at
        it would leave exactly the edge these fields exist for
        unchecked."""
        try:
            with open(core_path, encoding="utf-8", errors="replace") as fh:
                fields, _ = planning_model.PlanningNode.read_frontmatter(fh.read())
        except OSError:
            return "unreadable", None, "unreadable", []
        node = planning_model.PlanningNode
        sup_status, sup = node.parse_edge(fields.get(schema.Fields.SUPER_NODE))
        sub_status, subs = node.parse_edge_register(fields.get(schema.Fields.SUB_NODES))
        return sup_status, sup, sub_status, subs

    def run(self, roots, programming_root):
        absent = {}        # label -> [absent count, total]
        malformed = []
        unresolved = []
        one_ended = []
        disagreeing = []

        for root, label in roots:
            n_absent = n_total = 0
            for dirpath, filenames in self.walk_nodes(root):
                core = next((f for f in filenames
                             if planning_model.CORE_RE.match(f)), None)
                if core is None:
                    continue
                core_path = os.path.join(dirpath, core)
                n_total += 1
                sup_st, sup, sub_st, subs = self.read_edges(core_path)
                with open(core_path, encoding="utf-8", errors="replace") as fh:
                    fields_of, _ = planning_model.PlanningNode.read_frontmatter(fh.read())

                if sup_st == "absent" or sub_st == "absent":
                    n_absent += 1
                for field, st, raw in (("super_node", sup_st, sup),
                                        ("sub_nodes", sub_st, subs)):
                    if st == "malformed":
                        malformed.append(f"{self.disp(core_path)}: `{field}`")

                # While both fields exist, they must agree. `nodes` is
                # superseded but still present on every tree that has
                # not been brought over, so for a while one fact is
                # stored twice — the drift case this framework exists
                # to prevent. Comparing them is what makes the overlap
                # safe until `nodes` is retired.
                #
                # Only the IN-TREE entries are compared. `nodes` never
                # meant anything but sub-node folders in this same
                # tree, so a cross-repo entry in `sub_nodes` is not a
                # disagreement with it — `hq.projects` carries
                # `nodes: []` and three cross-repo edges, and both are
                # correct.
                register = planning_model.PlanningNode.parse_nodes_register(
                    fields_of.get(schema.Fields.NODES_SUPERSEDED, "")) if fields_of else None  # the OLD field, on purpose
                if register is not None and sub_st == "ok":
                    in_tree = [e[schema.EdgeKeys.NAME] for e in subs
                               if not e.get(schema.EdgeKeys.PATH,
                                            "").startswith("~")]
                    if in_tree != register:
                        disagreeing.append(
                            f"{self.disp(core_path)}: `nodes` says "
                            f"{register} but `sub_nodes` in-tree entries "
                            f"say {in_tree}")

                # Downward: every entry must exist and must point back.
                for entry in subs:
                    if entry.get(schema.EdgeKeys.REALIZE) is False:
                        continue  # in-file structure: no file, no edge
                    target = self.resolve(entry[schema.EdgeKeys.PATH], core_path)
                    if not os.path.isfile(target):
                        unresolved.append(
                            f"{self.disp(core_path)}: sub_nodes "
                            f"`{entry['name']}` -> {self.disp(target)}")
                        continue
                    t_sup_st, t_sup, _, _ = self.read_edges(target)
                    if t_sup_st != "ok":
                        one_ended.append(
                            f"{self.disp(core_path)} names "
                            f"`{entry['name']}`, but "
                            f"{self.disp(target)} has no `super_node` "
                            f"({t_sup_st})")
                        continue
                    back = self.resolve(t_sup["path"], target)
                    if back != os.path.abspath(core_path):
                        disagreeing.append(
                            f"{self.disp(core_path)} names "
                            f"`{entry['name']}`, but that node's "
                            f"`super_node` points at {self.disp(back)}")

                # Upward: the node above must name this one back.
                if sup_st == "ok":
                    target = self.resolve(sup["path"], core_path)
                    if not os.path.isfile(target):
                        unresolved.append(
                            f"{self.disp(core_path)}: super_node -> "
                            f"{self.disp(target)}")
                    else:
                        _, _, t_sub_st, t_subs = self.read_edges(target)
                        named = any(
                            self.resolve(e[schema.EdgeKeys.PATH], target) == os.path.abspath(core_path)
                            for e in t_subs
                            if e.get(schema.EdgeKeys.REALIZE) is not False)
                        if not named:
                            one_ended.append(
                                f"{self.disp(core_path)} hangs under "
                                f"{self.disp(target)}, which does not name "
                                f"it in `sub_nodes` ({t_sub_st})")
            absent[label] = (n_absent, n_total)

        items = []
        gaps = [(lbl, a, t) for lbl, (a, t) in absent.items() if a]
        if gaps:
            tot_a = sum(a for _, a, _ in gaps)
            tot_t = sum(t for _, _, t in gaps)
            items.append(Finding(
                "WARN", "edge-register",
                f"`super_node`/`sub_nodes` missing on {tot_a} of {tot_t} "
                f"nodes (PROTOCOL §1, 2026-08-02; brought in chain by "
                f"chain, not by a sweep)",
                sightings=[f"{lbl}: {a} of {t}" for lbl, a, t in gaps]))
        for cat, sites, text in (
                ("edge-malformed", malformed,
                 "edge field(s) that could not be read — expected a "
                 "mapping with `name` and `path`"),
                ("edge-unresolved", unresolved,
                 "edge(s) naming a file that does not exist"),
                ("edge-one-ended", one_ended,
                 "edge(s) stated at one end only — every edge is written "
                 "at both of its ends per PROTOCOL §1"),
                ("edge-disagreement", disagreeing,
                 "edge(s) whose two ends name different files — a node "
                 "attached somewhere other than where it says")):
            if sites:
                items.append(Finding("ERROR", cat,
                                     f"{len(sites)} {text}", sightings=sites))
        return items


class NodeSelfCheck(Check):
    """The `node` field — what a CORE says about itself (PROTOCOL §1,
    the owner, 2026-08-02).

    It was added because a CORE could name the repo ABOVE it, through
    `super_node.repo`, and say nothing about the repo it was in. Every
    value in it is checked against something already true on disk, so
    the field is redundant in the same self-policing way the two ends
    of an edge are: a CORE copied from another node, or moved and not
    re-homed, stops agreeing with its own folder.

    `repo` and `remote` sit on a TREE ROOT only. Below the root they
    are derivable by walking `super_node` upward, and the rule against
    storing a derivable fact is the same one that keeps them off
    in-repo edges. Carrying them lower down is reported."""

    name = "node-self"
    severity = "WARN"

    @staticmethod
    def git_remote(repo_dir):
        """The `origin` url from a repo's `.git/config`, or None. Read
        rather than shelled out to: the sandbox has no guarantee of a
        git binary, and the file is a fixed, tiny format."""
        cfg = os.path.join(repo_dir, ".git", "config")
        if not os.path.isfile(cfg):
            return None
        in_origin = False
        try:
            with open(cfg, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    s = line.strip()
                    if s.startswith("["):
                        in_origin = s.replace(" ", "") == '[remote"origin"]'
                    elif in_origin and s.startswith("url"):
                        return s.partition("=")[2].strip()
        except OSError:
            return None
        return None

    def run(self, roots, programming_root):
        absent = {}
        malformed, wrong_path, wrong_name, wrong_repo, misplaced = [], [], [], [], []

        for root, label in roots:
            repo_dir = self.repo_dir_of(root, programming_root)
            n_absent = n_total = 0
            for dirpath, filenames in self.walk_nodes(root):
                core = next((f for f in filenames
                             if planning_model.CORE_RE.match(f)), None)
                if core is None:
                    continue
                core_path = os.path.join(dirpath, core)
                n_total += 1
                with open(core_path, encoding="utf-8", errors="replace") as fh:
                    fields, _ = planning_model.PlanningNode.read_frontmatter(fh.read())
                status, entry = planning_model.PlanningNode.parse_edge(
                    fields.get(schema.Fields.NODE))
                if status == "absent":
                    n_absent += 1
                    continue
                if status != "ok":
                    malformed.append(f"{self.disp(core_path)}: `node` ({status})")
                    continue

                # `node.path` LOCATES the file, and it is relative to
                # the REPO root — not to the node's own folder the way
                # `super_node.path` and `sub_nodes[].path` are.
                #
                # Corrected 2026-08-02, after the owner: "bug: `path` is the
                # document file name, instead its file path." It held a
                # bare filename, which locates nothing, inside the one
                # field whose purpose is a node saying where it is.
                #
                # Repo-relative rather than absolute because `repo` and
                # `remote` on the tree root exist so that a reference
                # survives the repo being cloned somewhere other than
                # ~/Programming. An absolute path here would undo that.
                want_path = (os.path.relpath(os.path.abspath(core_path), repo_dir)
                             if repo_dir else core)
                if entry[schema.EdgeKeys.PATH] != want_path:
                    wrong_path.append(
                        f"{self.disp(core_path)}: `path: "
                        f"{entry[schema.EdgeKeys.PATH]}` but the file sits at "
                        f"{want_path} within its repo")

                folder = os.path.basename(dirpath)
                m = re.match(r"^node_(?:\d+_)*\d+_([a-z0-9_]+)$", folder)
                is_root = os.path.abspath(dirpath) == os.path.abspath(root)
                got_name = entry[schema.EdgeKeys.NAME]

                # `name` is the LAST SEGMENT OF THE ID, at every level.
                # Corrected 2026-08-02 after the owner spotted that a tree
                # root's name was checked by nothing: a root's folder is
                # `Planning`, which carries no name segment, so the
                # folder comparison below silently skipped roots and
                # `name: banana` passed clean. The id holds everywhere —
                # `pcv5` -> pcv5, `pcv5.tools` -> tools,
                # `pcv5.tools.ledgerer` -> ledgerer — so the field stops
                # meaning one thing at a root and another below it.
                node_id = fields.get(schema.Fields.ID)
                if node_id and got_name != node_id.split(".")[-1]:
                    wrong_name.append(
                        f"{self.disp(core_path)}: `name: {got_name}` but "
                        f"`id: {node_id}` ends in {node_id.split('.')[-1]}")
                # Below a root the folder must agree too. Both run: the
                # id says what the node is called, the folder says where
                # it lives, and a name matching one but not the other is
                # the moved-and-not-re-homed case this field exists for.
                elif m and got_name != m.group(1):
                    wrong_name.append(
                        f"{self.disp(core_path)}: `name: {got_name}` "
                        f"but the folder says {m.group(1)}")

                has_repo = schema.EdgeKeys.REPO in entry or schema.EdgeKeys.REMOTE in entry
                if is_root:
                    if not has_repo:
                        wrong_repo.append(
                            f"{self.disp(core_path)}: a tree root's `node` "
                            f"carries `repo` and `remote`")
                    elif repo_dir:
                        want_repo = os.path.basename(repo_dir)
                        want_remote = self.git_remote(repo_dir)
                        if entry.get(schema.EdgeKeys.REPO) != want_repo:
                            wrong_repo.append(
                                f"{self.disp(core_path)}: `repo: "
                                f"{entry.get('repo')}` but the tree is in "
                                f"{want_repo}")
                        if want_remote and entry.get(schema.EdgeKeys.REMOTE) != want_remote:
                            wrong_repo.append(
                                f"{self.disp(core_path)}: `remote: "
                                f"{entry.get('remote')}` but git says "
                                f"{want_remote}")
                elif has_repo:
                    misplaced.append(
                        f"{self.disp(core_path)}: carries `repo`/`remote` "
                        f"below a tree root, where they are derivable by "
                        f"walking `super_node` up")
            absent[label] = (n_absent, n_total)

        items = []
        gaps = [(lbl, a, t) for lbl, (a, t) in absent.items() if a]
        if gaps:
            tot_a = sum(a for _, a, _ in gaps)
            tot_t = sum(t for _, _, t in gaps)
            items.append(Finding(
                "WARN", "node-self",
                f"`node` missing on {tot_a} of {tot_t} nodes (PROTOCOL §1, "
                f"2026-08-02; brought in chain by chain)",
                sightings=[f"{lbl}: {a} of {t}" for lbl, a, t in gaps]))
        for cat, sites, text in (
                ("node-self-malformed", malformed,
                 "`node` field(s) that could not be read"),
                ("node-self-path", wrong_path,
                 "`node.path` value(s) that do not name their own file"),
                ("node-self-name", wrong_name,
                 "`node.name` value(s) that disagree with the folder — a "
                 "CORE copied or moved and not re-homed"),
                ("node-self-repo", wrong_repo,
                 "tree root `node` repo/remote problem(s)"),
                ("node-self-misplaced", misplaced,
                 "`node` field(s) carrying repo/remote below a tree root")):
            if sites:
                items.append(Finding("ERROR", cat,
                                     f"{len(sites)} {text}", sightings=sites))
        return items

    @staticmethod
    def repo_dir_of(root, programming_root):
        """The top-level repo directory a planning root sits in.

        Found by walking UP from the planning root to the nearest `.git`,
        which is what a repo actually is. Falls back to the old rule —
        first path segment under `~/Programming` — for a tree that is not
        in git at all.

        Corrected 2026-08-05. The old rule assumed every tree lives under
        `~/Programming`, so a repo read from anywhere else returned None,
        `want_path` degraded to the bare filename, and EVERY `node.path`
        was reported wrong. Measured: 64 false errors when the same trees
        were checked through a container bind-mount at /projects, against
        0 on the same trees at their usual paths. Anyone cloning these
        repos to another directory would have hit it too."""
        here = os.path.abspath(root)
        while True:
            if os.path.isdir(os.path.join(here, ".git")):
                return here
            parent = os.path.dirname(here)
            if parent == here:
                break
            here = parent
        rel = os.path.relpath(os.path.abspath(root), programming_root)
        if rel.startswith(".."):
            return None
        return os.path.join(programming_root, rel.split(os.sep)[0])


class CheckFrontmatterCheck(Check):
    """A CHECK file carries frontmatter with `id: <node id>.check`
    (PROTOCOL §3, the owner, 2026-08-02).

    CHECK files were written before the rule and carry none, so a
    missing one is a WARN on the `designation` precedent. An id that is
    PRESENT and wrong is an ERROR: it means the CHECK was copied from
    another node and now silently claims to be that node's test, which
    is the same failure the mirrored-filename rule exists to stop."""

    name = "check-frontmatter"
    severity = "WARN"

    def run(self, roots, programming_root):
        missing = {}
        wrong = []
        for root, label in roots:
            n_missing = n_total = 0
            for dirpath, filenames in self.walk_nodes(root):
                core = next((f for f in filenames
                             if planning_model.CORE_RE.match(f)), None)
                chk = next((f for f in filenames
                            if f.startswith("CHECK_")), None)
                if core is None or chk is None:
                    continue
                n_total += 1
                with open(os.path.join(dirpath, core),
                          encoding="utf-8", errors="replace") as fh:
                    core_fields, _ = planning_model.PlanningNode.read_frontmatter(fh.read())
                node_id = core_fields.get("id")
                chk_path = os.path.join(dirpath, chk)
                with open(chk_path, encoding="utf-8", errors="replace") as fh:
                    chk_fields, _ = planning_model.PlanningNode.read_frontmatter(fh.read())
                got = chk_fields.get("id")
                if not got:
                    n_missing += 1
                elif node_id and got != f"{node_id}.check":
                    wrong.append(f"{self.disp(chk_path)}: `id: {got}` "
                                 f"(expected `{node_id}.check`)")
            missing[label] = (n_missing, n_total)

        items = []
        gaps = [(lbl, m, t) for lbl, (m, t) in missing.items() if m]
        if gaps:
            tot_m = sum(m for _, m, _ in gaps)
            tot_t = sum(t for _, _, t in gaps)
            items.append(Finding(
                "WARN", "check-frontmatter",
                f"CHECK frontmatter missing on {tot_m} of {tot_t} nodes "
                f"(PROTOCOL §3, 2026-08-02; `id: <node id>.check`)",
                sightings=[f"{lbl}: {m} of {t}" for lbl, m, t in gaps]))
        if wrong:
            items.append(Finding(
                "ERROR", "check-frontmatter",
                f"{len(wrong)} CHECK file(s) whose `id` names a different "
                f"node — a check that survived a copy and now tests "
                f"something else",
                sightings=wrong))
        return items


class Checker:
    """Runs every check and prints the report in `check_plans.py`'s
    format."""

    def __init__(self, checks):
        self.checks = checks

    def run_all(self, roots, programming_root):
        items = []
        for check in self.checks:
            items.extend(check.run(roots, programming_root))
        return items

    def report(self, items, roots, quiet):
        """Print the grouped report and the CONFORMANCE GAPS banner.
        Returns the error count (the exit-code driver)."""
        n_errors = self._group_and_print(items, quiet)
        # Last, so it is the thing left on screen (the owner: "it should be loud
        # about that gap"). It does not touch the exit code: these trees
        # predate the rule, and refusing every commit until they conform
        # would be the sweep the owner ruled against.
        if not quiet:
            print()
            self._print_conformance_banner(self._conformance_gaps(roots))
        return n_errors

    @staticmethod
    def _group_and_print(items, quiet):
        errors = [i for i in items if i.severity == "ERROR"]
        warns = [i for i in items if i.severity == "WARN"]

        if not quiet:
            order = {"grammar": 0, "dangling-path": 1, "stale-archive": 2,
                      "id-collision": 3, "missing-check": 4,
                      "missing-dashboard": 5, "nodes-register": 6,
                      "projection": 7,
                      "edge-malformed": 8, "edge-unresolved": 9,
                      "edge-one-ended": 10, "edge-disagreement": 11,
                      "node-self-malformed": 11.1, "node-self-path": 11.2,
                      "node-self-name": 11.3, "node-self-repo": 11.4,
                      "node-self-misplaced": 11.5, "node-self": 14.5,
                      "unresolved-object": 12, "missing-designation": 13,
                      "edge-register": 14, "check-frontmatter": 15,
                      "duplicated-prose": 16, "unrealized-nodes": 17,
                      "completeness": 18}
            for item in sorted(items, key=lambda i: (order.get(i.category, 9), i.summary)):
                print(f"[{item.severity}] {item.category}: {item.summary}")
                for s in item.sightings:
                    print(f"    - {s}")
            print()
        print(f"summary: {len(errors)} error(s), {len(warns)} warning(s)")
        return len(errors)

    @staticmethod
    def _conformance_gaps(roots):
        """Per-tree counts of the three §1 gaps, printed as a BANNER.

        the owner, 2026-08-01: "if they dont have either YAML.nodes or
        `## nodes` or `## nodes` section first, then it should be loud
        about that gap." A line among a dozen warnings is not loud, so the
        gaps get their own block at the end of the report with the command
        that closes them."""
        rows = []
        for root, label in roots:
            no_register = no_section = not_first = total = 0
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
                core = next((f for f in filenames if planning_model.CORE_RE.match(f)), None)
                if core is None:
                    continue
                total += 1
                with open(os.path.join(dirpath, core),
                          encoding="utf-8", errors="replace") as fh:
                    fields, body = planning_model.PlanningNode.read_frontmatter(fh.read())
                if planning_model.PlanningNode.register_of(fields) is None:
                    no_register += 1
                secs = planning_model.PlanningNode.sections_of(body)
                forms = schema.Sections.SUB_NODES_FORMS
                if not any(h in secs for h in forms):
                    no_section += 1
                else:
                    # Only PROSE ahead of the sub-node listing is a gap.
                    # The other projections legitimately precede it since
                    # PROTOCOL §407 (2026-08-23) put `## metadata` first,
                    # always — counting them made the banner report every
                    # CORE in every tree as non-conformant on the day the
                    # metadata projection shipped.
                    ahead = secs[:next(i for i, h in enumerate(secs)
                                       if h in forms)]
                    if any(not is_projection_section(h) for h in ahead):
                        not_first += 1
            no_edges = no_chk_fm = 0
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
                core = next((f for f in filenames
                             if planning_model.CORE_RE.match(f)), None)
                if core is None:
                    continue
                node = planning_model.PlanningNode
                with open(os.path.join(dirpath, core),
                          encoding="utf-8", errors="replace") as fh:
                    fields, _ = node.read_frontmatter(fh.read())
                if node.parse_edge(fields.get(schema.Fields.SUPER_NODE))[0] == "absent" \
                        or node.parse_edge_register(fields.get(schema.Fields.SUB_NODES))[0] == "absent":
                    no_edges += 1
                chk = next((f for f in filenames if f.startswith("CHECK_")), None)
                if chk:
                    with open(os.path.join(dirpath, chk),
                              encoding="utf-8", errors="replace") as fh:
                        cf, _ = node.read_frontmatter(fh.read())
                    if not cf.get("id"):
                        no_chk_fm += 1
            if no_register or no_section or not_first or no_edges or no_chk_fm:
                rows.append((label, total, no_register, no_section, not_first,
                             no_edges, no_chk_fm))
        return rows

    @staticmethod
    def _print_conformance_banner(rows):
        if not rows:
            print("conformance: every CORE carries its register, its "
                  "`super_node`/`sub_nodes` edges and a `## sub_nodes` section "
                  "in first position, and every CHECK carries its id.")
            return
        bar = "=" * 68
        print(bar)
        print("CONFORMANCE GAPS — PROTOCOL §1 and §3")
        print(bar)
        for label, total, no_reg, no_sec, not_first, no_edges, no_chk in rows:
            print(f"  {label}   ({total} COREs)")
            if no_reg:
                print(f"      {no_reg} with no `nodes` register in the "
                      f"frontmatter")
            if no_sec:
                print(f"      {no_sec} with no `## sub_nodes` section")
            if not_first:
                print(f"      {not_first} with `## sub_nodes` out of first "
                      f"position")
            if no_edges:
                print(f"      {no_edges} with no `super_node`/`sub_nodes` "
                      f"edges   (§1, 2026-08-02)")
            if no_chk:
                print(f"      {no_chk} CHECK file(s) with no frontmatter "
                      f"id   (§3, 2026-08-02)")
        print()
        print("  the edge fields and CHECK frontmatter are brought in CHAIN "
              "BY CHAIN as")
        print("  a branch is descended into (the owner, 2026-08-02), not by a "
              "sweep over the")
        print("  whole tree. for the older register gap, adoption is "
              "mechanical:")
        print("      python3 ~/Programming/PlanPlan/framework/"
              "generate_nodes.py \\")
        print("          <planning root> --adopt --apply")
        print("  which writes each register FROM the folders already on "
              "disk, then")
        print("  rebuilds the projections. `designation` stays a person's "
              "judgement.")
        print(bar)
