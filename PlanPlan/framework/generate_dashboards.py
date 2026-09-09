#!/usr/bin/env python3
"""Write a DASHBOARD.md rollup into every node folder of a planning tree.

Each node's DASHBOARD.md summarizes that node's OWN SUB-TREE (itself plus
everything beneath it): status and designation breakdowns, anything
blocked, PROGRESS bullet-status counts, and the SUPPORT files present.

Usage:
    python3 ~/Programming/PlanPlan/framework/generate_dashboards.py \
        <root>... [--check]

`--check` writes nothing: exits 1 if any node's DASHBOARD.md would differ
from what is on disk (including a node that has none yet), 0 if every
node is current.

DETERMINISM is the point of this tool: no timestamps, no dates, no
hostnames, no absolute paths outside `~/Programming/...` form. Every
collection is sorted before rendering, so running this twice in a row
produces byte-identical files.

No dependencies beyond the standard library. Imports `planning_model.py`
from the same directory rather than reimplementing its tree walk.
"""
import argparse
import importlib.util
import os
import re
import sys

FRAMEWORK_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_planning_model():
    path = os.path.join(FRAMEWORK_DIR, "planning_model.py")
    spec = importlib.util.spec_from_file_location("planning_model", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


planning_model = _load_planning_model()
PlanningTree = planning_model.PlanningTree

PROGRAMMING_ROOT = os.path.expanduser("~/Programming")

STATUS_WORDS = ["planned", "in-progress", "done", "blocked", "deferred"]
STATUS_RES = {w: re.compile(r"\b" + re.escape(w) + r"\b", re.IGNORECASE)
              for w in STATUS_WORDS}
BLOCKED_RE = re.compile(r"\bblocked\b", re.IGNORECASE)
BULLET_RE = re.compile(r"^\s*[-*]\s")


def disp(path):
    """~/Programming/... form of an absolute path — textual, not
    resolved, so the output is identical regardless of whose machine
    generated it."""
    ap = os.path.abspath(path)
    if ap == PROGRAMMING_ROOT or ap.startswith(PROGRAMMING_ROOT + os.sep):
        return "~/Programming" + ap[len(PROGRAMMING_ROOT):]
    return ap


# ---------------------------------------------------------------- gather

def subtree_nodes(node):
    """This node plus every node beneath it, itself included."""
    def _walk(n):
        yield n
        for s in n.sub_nodes:
            yield from _walk(s)
    return list(_walk(node))


def progress_lines(node):
    """(text) lines of this node's own PROGRESS.md, or [] if absent."""
    if not node.progress_path:
        return []
    with open(node.progress_path, encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


def gather(node):
    """Everything a DASHBOARD.md needs for this node's sub-tree."""
    nodes = subtree_nodes(node)

    status_counts = {}
    designation_counts = {}
    for n in nodes:
        fields = n.frontmatter
        status = fields.get("status") or "(missing)"
        status_counts[status] = status_counts.get(status, 0) + 1
        desig = fields.get("designation")
        if desig:
            parts = [d.strip() for d in desig.split(",") if d.strip()]
        else:
            parts = ["(missing)"]
        for d in parts:
            designation_counts[d] = designation_counts.get(d, 0) + 1

    blocked = []  # (file_disp, line_no, quoted_line)
    bullet_status_counts = {w: 0 for w in STATUS_WORDS}
    supports = []  # file_disp

    for n in nodes:
        lines = progress_lines(n)
        prog_path = n.progress_path or os.path.join(n.path, "PROGRESS.md")
        for i, line in enumerate(lines, start=1):
            if BLOCKED_RE.search(line):
                blocked.append((disp(prog_path), i, line.strip()))
            if BULLET_RE.match(line):
                for w, rx in STATUS_RES.items():
                    if rx.search(line):
                        bullet_status_counts[w] += 1
        for s in n.support_paths:
            supports.append(disp(s))

    return {
        "sub_node_count": len(nodes) - 1,
        "status_counts": status_counts,
        "designation_counts": designation_counts,
        "blocked": sorted(blocked),
        "bullet_status_counts": bullet_status_counts,
        "supports": sorted(supports),
    }


# ---------------------------------------------------------------- render

def render_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return out


def render_dashboard(node, stats):
    fields = node.frontmatter
    nid = fields.get("id", "(none)")
    status = fields.get("status", "(none)")
    designation = fields.get("designation", "(none)")

    lines = []
    lines.append("<!-- GENERATED FILE — do not hand-edit. -->")
    lines.append("<!-- Produced by "
                  "~/Programming/PlanPlan/framework/generate_dashboards.py "
                  "from this node's own sub-tree. Hand edits are lost the -->")
    lines.append("<!-- next time the tool runs; re-run it instead of "
                  "editing this file. -->")
    lines.append("")
    lines.append(f"# DASHBOARD — {node.address}")
    lines.append("")
    lines.append("A rollup over this node's own sub-tree (itself plus "
                  "everything beneath it). Regenerated, not edited.")
    lines.append("")
    lines.append("## this node")
    lines.append("")
    lines.extend(render_table(
        ["field", "value"],
        [["id", f"`{nid}`"], ["status", status], ["designation", designation]],
    ))
    lines.append("")
    lines.append("## sub-tree")
    lines.append("")
    lines.append(f"sub-node count: {stats['sub_node_count']}")
    lines.append("")
    lines.append("### status breakdown")
    lines.append("")
    if stats["status_counts"]:
        rows = [[k, str(v)] for k, v in sorted(stats["status_counts"].items())]
        lines.extend(render_table(["status", "count"], rows))
    else:
        lines.append("(no nodes)")
    lines.append("")
    lines.append("### designation breakdown")
    lines.append("")
    if stats["designation_counts"]:
        rows = [[k, str(v)] for k, v in sorted(stats["designation_counts"].items())]
        lines.extend(render_table(["designation", "count"], rows))
    else:
        lines.append("(no nodes)")
    lines.append("")
    lines.append("## blocked")
    lines.append("")
    if stats["blocked"]:
        for file_disp, lineno, text in stats["blocked"]:
            # path and line number are NOT joined inside one backtick span:
            # `path:N` would read as a single ~/Programming/... reference
            # to check_plans.py's dangling-path scan, which does not know
            # `:N` is a line suffix rather than part of the path.
            lines.append(f"- `{file_disp}` line {lineno} — {text}")
    else:
        lines.append("nothing in this sub-tree mentions \"blocked\".")
    lines.append("")
    lines.append("## PROGRESS bullet statuses")
    lines.append("")
    lines.append("counted by scanning every PROGRESS.md bullet in this "
                  "sub-tree for these words; a bullet mentioning more than "
                  "one word counts toward each.")
    lines.append("")
    rows = [[w, str(stats["bullet_status_counts"][w])] for w in STATUS_WORDS]
    lines.extend(render_table(["status word", "bullet count"], rows))
    lines.append("")
    lines.append("## SUPPORT files in this sub-tree")
    lines.append("")
    if stats["supports"]:
        for s in stats["supports"]:
            lines.append(f"- `{s}`")
    else:
        lines.append("(none)")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------- driver

def all_nodes(root_node):
    return subtree_nodes(root_node)


def build(root):
    tree = PlanningTree.load(root)
    out = {}  # dashboard path -> content
    for node in all_nodes(tree.root_node):
        stats = gather(node)
        content = render_dashboard(node, stats)
        out[os.path.join(node.path, "DASHBOARD.md")] = content
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("roots", nargs="+", help="one or more planning roots")
    ap.add_argument("--check", action="store_true",
                     help="write nothing; exit 1 if any DASHBOARD.md is stale")
    args = ap.parse_args()

    wanted = {}
    for raw in args.roots:
        root = os.path.abspath(os.path.expanduser(raw))
        if not os.path.isdir(root):
            print(f"not a directory: {raw} (resolved {root})", file=sys.stderr)
            sys.exit(2)
        wanted.update(build(root))

    if args.check:
        stale = []
        for path in sorted(wanted):
            want = wanted[path]
            if not os.path.isfile(path):
                stale.append((path, "missing"))
                continue
            with open(path, encoding="utf-8") as fh:
                have = fh.read()
            if have != want:
                stale.append((path, "content differs"))
        if stale:
            for path, why in stale:
                print(f"stale: {disp(path)} ({why})")
            print(f"{len(stale)} stale dashboard(s)")
            sys.exit(1)
        print(f"{len(wanted)} dashboard(s) current")
        sys.exit(0)

    for path in sorted(wanted):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(wanted[path])
    print(f"wrote {len(wanted)} dashboard(s)")


if __name__ == "__main__":
    main()
