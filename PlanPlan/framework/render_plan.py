#!/usr/bin/env python3
"""Render any planning tree conforming to the framework as one HTML page.

Reads a planning root (a node_0 folder: CORE_0.md plus node_* folders)
and writes a single self-contained HTML file showing the tree, each
node's frontmatter and definition line, and every place the folder
grammar is broken.

It knows nothing about any particular project. Anything conforming to
`<WORKSPACE_DIR>/PlanPlan/framework/PROTOCOL.md` renders.

Usage:
    python3 <WORKSPACE_DIR>/PlanPlan/framework/render_plan.py <root> [-o out.html]

    python3 <WORKSPACE_DIR>/PlanPlan/framework/render_plan.py \
        <WORKSPACE_DIR>/PseudoCoup_v6/Scratch -o /tmp/scratch.html

Builds its tree from `planning_model.PlanningTree` and gets the grammar
problems it displays from `checks.GrammarCheck` — this file holds the
HTML renderer only, no checking logic of its own.

No dependencies beyond the standard library.
"""
import argparse
import html
import os
import re
import sys
from datetime import datetime, timezone

import checks
import planning_model

LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
CODE_RE = re.compile(r"`([^`]+)`")


class PlanRenderer:
    """Renders a `planning_model.PlanningTree` (plus its grammar
    problems) as one self-contained HTML page."""

    CSS = """
:root { color-scheme: light dark; }
body { font: 14px/1.5 ui-sans-serif, system-ui, -apple-system, sans-serif;
       margin: 0; padding: 32px; max-width: 1000px;
       background: Canvas; color: CanvasText; }
h1 { font-size: 19px; margin: 0 0 4px; }
.sub { color: GrayText; font-size: 13px; margin: 0 0 16px; }
.row { display: flex; align-items: baseline; gap: 10px; padding: 6px 0; }
.nm { font-weight: 600; }
.id { color: GrayText; font-size: 12px; font-family: ui-monospace, monospace; }
.def { color: GrayText; margin: 0 0 2px 0; font-size: 13px; }
.pill { font-size: 11px; padding: 1px 7px; border-radius: 9px; white-space: nowrap;
        border: 1px solid color-mix(in srgb, CanvasText 25%, transparent); }
.thin { color: GrayText; font-style: italic; }
.prog { border-color: #b3261e; color: #b3261e; }
@media (prefers-color-scheme: dark) { .prog { border-color: #f2b8b5; color: #f2b8b5; } }
.wc { color: GrayText; font-size: 12px; margin-left: auto; white-space: nowrap; }
.prob { color: #b3261e; font-size: 12px; margin: 2px 0; }
@media (prefers-color-scheme: dark) { .prob { color: #f2b8b5; } }
.box { border: 1px solid color-mix(in srgb, CanvasText 15%, transparent);
       border-radius: 8px; padding: 8px 16px 14px; margin-bottom: 24px; }
.hdr { font-weight: 600; margin: 16px 0 8px; }
.ok { color: GrayText; }

/* the tree: nested <details>, so collapsing is native and needs no script */
details > summary { cursor: pointer; list-style: none; border-radius: 5px;
                    padding-left: 4px; }
details > summary::-webkit-details-marker { display: none; }
details > summary:hover { background: color-mix(in srgb, CanvasText 6%, transparent); }
details > summary .nm::before { content: "\\25B8 "; color: GrayText;
                                display: inline-block; width: 1em; }
details[open] > summary .nm::before { content: "\\25BE "; }
.leaf { padding-left: 4px; }
.leaf .nm::before { content: ""; display: inline-block; width: 1em; }
.kids { margin-left: 20px;
        border-left: 1px solid color-mix(in srgb, CanvasText 12%, transparent);
        padding-left: 10px; }
.btn { font: inherit; font-size: 12px; padding: 3px 10px; margin-right: 6px;
       border-radius: 6px; cursor: pointer; background: Canvas; color: CanvasText;
       border: 1px solid color-mix(in srgb, CanvasText 25%, transparent); }

/* what a CORE says about itself, below the folder tree: its sections,
   and the bullet trees inside them. deliberately lighter than a node
   row so a component is never read as a node folder. */
.sech { font-size: 12px; color: GrayText; font-variant: small-caps;
        letter-spacing: .04em; }
details.sec > summary .sech::before,
details.cmpfold > summary .cmp::before { content: "\\25B8 "; color: GrayText;
        display: inline-block; width: 1em; }
details.sec[open] > summary .sech::before,
details.cmpfold[open] > summary .cmp::before { content: "\\25BE "; }
.cmp { font-size: 13px; }
.leafcmp { padding-left: calc(1em + 4px); }
.prose { font-size: 13px; color: GrayText; margin: 3px 0; max-width: 72ch;
         padding-left: 4px; }
"""

    SCRIPT = """
<script>
function setAll(open) {
  document.querySelectorAll('details').forEach(d => d.open = open);
}
// depth counts node folders only, so component nesting does not shift
// what "level 2" means
function setDepth(n) {
  document.querySelectorAll('details.nodefold').forEach(d => {
    let depth = 0, p = d.parentElement;
    while (p) {
      if (p.matches && p.matches('details.nodefold')) depth++;
      p = p.parentElement;
    }
    d.open = depth < n;
  });
}
function setDetail(open) {
  document.querySelectorAll('details.sec, details.cmpfold')
          .forEach(d => d.open = open);
}
</script>
"""

    # `## sub_nodes` (and its superseded form `## nodes`) just relists the
    # sub-node folders, which the tree already draws. `## design` is the
    # node's own structure and is worth seeing without a click; every other
    # section opens on demand.
    #
    # `## components` was here until 2026-08-05 and was never in PROTOCOL —
    # it existed only as this special case, which then invited COREs to use
    # a section the grammar had never defined. the owner: "`## components` is
    # awkwardly close to `## sub_nodes`." Renamed to `## design`, and the
    # grammar now states it (PROTOCOL §1b) rather than the renderer
    # implying it.
    SKIP_SECTIONS = {"sub_nodes", "nodes"}
    OPEN_SECTIONS = {"design"}

    def __init__(self, thin_words):
        self.thin_words = thin_words

    @staticmethod
    def esc(s):
        return html.escape(s or "")

    @classmethod
    def inline(cls, s):
        """CORE text is markdown, so a bullet can carry bold, backticks, or a
        link. Escape first, then convert — the markers survive escaping. Link
        targets are relative paths that would not resolve from wherever this
        page is written, so only the link text is kept."""
        s = cls.esc(s)
        s = LINK_RE.sub(r"\1", s)
        s = BOLD_RE.sub(r"<strong>\1</strong>", s)
        s = CODE_RE.sub(r"<code>\1</code>", s)
        return s

    @staticmethod
    def parse_bullets(lines):
        """Turn an indented markdown bullet list into a tree.

        A line starting `- ` or `* ` opens an item; its indent decides how
        deep it sits. A non-bullet line that is not blank continues the
        text of the item above it, which is how a wrapped bullet reads.

        Returns [{"text": ..., "subs": [...]}, ...]."""
        root, stack = [], []
        for line in lines:
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip())
            s = line.strip()
            if s.startswith("- ") or s.startswith("* "):
                item = {"text": s[2:].strip(), "subs": []}
                while stack and stack[-1][0] >= indent:
                    stack.pop()
                (stack[-1][1]["subs"] if stack else root).append(item)
                stack.append((indent, item))
            elif stack:
                stack[-1][1]["text"] += " " + s
            else:
                root.append({"text": s, "subs": []})
        return root

    def node_body(self, node, problems):
        """The visible line(s) for one node: the row, its definition, and any
        grammar problems. Emitted inside <summary> for a node that has
        sub-nodes, so it stays on screen when that node is collapsed."""
        f = node.frontmatter
        status = f.get("status", "—")
        nid = f.get("id", "—")
        words = node.words
        thin = node.core_path is not None and words < self.thin_words

        out = ["<div class='row'>",
               f"<span class='nm'>{self.esc(os.path.basename(node.path))}</span>",
               f"<span class='id'>{self.esc(nid)}</span>",
               f"<span class='pill'>{self.esc(status)}</span>"]
        if thin:
            out.append("<span class='pill thin'>definition only</span>")
        ps = node.progress_status
        if ps and ps not in ("living",):
            out.append(f"<span class='pill prog'>{self.esc(ps)}</span>")
        out.append(f"<span class='wc'>{words} words</span>")
        out.append("</div>")

        if node.core_path and node.definition:
            d = node.definition
            d = d if len(d) <= 150 else d[:150] + "…"
            out.append(f"<p class='def'>{self.esc(d)}</p>")
        for p in problems:
            out.append(f"<p class='prob'>{self.esc(p)}</p>")
        return out

    def render_bullets(self, items):
        """A bullet with sub-bullets folds; a bullet without one does not."""
        out = []
        for it in items:
            if it["subs"]:
                out.append("<details open class='cmpfold'><summary>"
                           f"<span class='cmp'>{self.inline(it['text'])}</span>"
                           "</summary><div class='kids'>")
                out.extend(self.render_bullets(it["subs"]))
                out.append("</div></details>")
            else:
                out.append(f"<div class='cmp leafcmp'>{self.inline(it['text'])}</div>")
        return out

    def render_section_body(self, lines):
        """Blocks separated by blank lines. A block whose first line is a
        bullet renders as a bullet tree; anything else renders as a
        paragraph. This is what lets one section hold prose, then a list,
        then more prose."""
        out, block = [], []

        def flush():
            if not block:
                return
            first = block[0].strip()
            if first.startswith("- ") or first.startswith("* "):
                out.extend(self.render_bullets(self.parse_bullets(list(block))))
            else:
                out.append(f"<p class='prose'>{self.inline(' '.join(' '.join(block).split()))}</p>")
            block.clear()

        for line in lines:
            if line.strip():
                block.append(line)
            else:
                flush()
        flush()
        return out

    def render_sections(self, node):
        """The CORE's own depth — everything the file says below its
        definition line. Without this the view shows only folders, and a
        node whose detail lives in `## design` looks empty."""
        if not node.core_path:
            return []
        out = []
        for heading, lines in node.sections:
            if heading.lower() in self.SKIP_SECTIONS:
                continue
            body = self.render_section_body(lines)
            if not body:
                continue
            openness = " open" if heading.lower() in self.OPEN_SECTIONS else ""
            out.append(f"<details{openness} class='sec'><summary>"
                       f"<span class='sech'>{self.esc(heading)}</span>"
                       "</summary><div class='kids'>")
            out.extend(body)
            out.append("</div></details>")
        return out

    def render_node(self, node, problems_by_address):
        """One node and everything under it — its sub-node folders, then its
        own sections. A node with neither is a plain div, so nothing
        pretends to be foldable when there is nothing inside it."""
        problems = problems_by_address.get(node.address, [])
        body = self.node_body(node, problems)
        secs = self.render_sections(node)
        if not node.sub_nodes and not secs:
            return ["<div class='leaf'>"] + body + ["</div>"]

        out = ["<details open class='nodefold'><summary>"] + body + \
              ["</summary><div class='kids'>"]
        for s in node.sub_nodes:
            out.extend(self.render_node(s, problems_by_address))
        out.extend(secs)
        out.append("</div></details>")
        return out

    def render(self, tree, all_problems, problems_by_address):
        rows = list(tree.walk())
        max_depth = max(d for d, _ in rows)

        parts = [
            "<!doctype html><html><head><meta charset='utf-8'>",
            f"<title>plan — {self.esc(os.path.basename(tree.root_path))}</title>",
            f"<style>{self.CSS}</style></head><body>",
            f"<h1>{self.esc(os.path.basename(tree.root_path))}</h1>",
            f"<p class='sub'>{self.esc(tree.root_path)} · {len(rows)} nodes · "
            f"depth {max_depth} · "
            f"generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>",
            "<p><button class='btn' onclick='setAll(true)'>expand all</button>",
            "<button class='btn' onclick='setAll(false)'>collapse all</button>",
        ]
        # one button per level, so a deep tree can be opened to a chosen depth
        for lvl in range(1, max_depth + 1):
            parts.append(f"<button class='btn' onclick='setDepth({lvl})'>"
                         f"level {lvl}</button>")
        parts.append("<button class='btn' onclick='setDetail(true)'>all detail</button>")
        parts.append("<button class='btn' onclick='setDetail(false)'>no detail</button>")
        parts.append("</p>")

        parts.append("<div class='box'>")
        parts.extend(self.render_node(tree.root_node, problems_by_address))
        parts.append("</div>")

        parts.append("<div class='hdr'>grammar</div><div class='box'>")
        if all_problems:
            for addr, p in all_problems:
                parts.append(f"<p class='prob'>{self.esc(addr)} — {self.esc(p)}</p>")
        else:
            parts.append("<p class='ok'>every node has one CORE, a PROGRESS, "
                         "and nothing stray.</p>")
        parts.append("</div>")
        parts.append(self.SCRIPT)
        parts.append("</body></html>")
        return "\n".join(parts)


def render_tree_text(tree, show=()):
    """The tree as plain text, for pasting into a message or a log.

    Added 2026-08-05. The HTML view is for reading a plan; this is for
    QUOTING one. Until it existed, a tree in conversation was drawn
    from memory, and one drawn from memory was wrong — `node` and
    `connector` were put beside their parent instead of under it, which
    is exactly the error a generated diagram cannot make.

    `show` names optional columns: "designation", "status", "id".
    """
    lines = []
    rows = list(tree.walk())
    root_depth = rows[0][0] if rows else 0

    def label(node):
        name = os.path.basename(node.path)
        m = re.match(r"^node_(?:\d+_)*\d+_([a-z0-9_]+)$", name)
        text = m.group(1) if m else (node.frontmatter.get("id", name))
        extra = []
        if "designation" in show:
            extra.append(node.frontmatter.get("designation", "—"))
        if "status" in show:
            extra.append(node.frontmatter.get("status", "—"))
        if "id" in show:
            extra.append(node.frontmatter.get("id", "—"))
        return text + (f"   [{'; '.join(extra)}]" if extra else "")

    def walk(node, prefix, is_last, depth):
        if depth == root_depth:
            lines.append(label(node))
        else:
            lines.append(prefix + ("└── " if is_last else "├── ") + label(node))
        kids = node.sub_nodes
        # `realize: false` register entries have no folder, so they are
        # not in sub_nodes. Show them, marked, or the picture silently
        # omits structure the register states.
        unrealized = [e for e in node.sub_edges
                      if e.get("realize") is False]
        child_prefix = prefix if depth == root_depth else \
            prefix + ("    " if is_last else "│   ")
        total = len(kids) + len(unrealized)
        for i, k in enumerate(kids):
            walk(k, child_prefix, i == total - 1, depth + 1)
        for j, e in enumerate(unrealized):
            last = (len(kids) + j) == total - 1
            lines.append(child_prefix + ("└── " if last else "├── ")
                         + e.get("name", "?") + "   (realize: false)")

    walk(tree.root_node, "", True, root_depth)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", help="the planning root (a node_0 folder)")
    ap.add_argument("-o", "--out", default="plan_view.html",
                    help="output html (default: plan_view.html in cwd)")
    ap.add_argument("--thin", type=int, default=60,
                    help="word count at or below which a CORE is marked "
                         "'definition only' (default 60)")
    ap.add_argument("--tree", action="store_true",
                    help="print the tree as plain text and exit; writes "
                         "no html")
    ap.add_argument("--with", dest="columns", default="",
                    help="extra columns for --tree, comma separated: "
                         "designation, status, id")
    args = ap.parse_args()

    root = os.path.abspath(os.path.expanduser(args.root))
    if not os.path.isdir(root):
        sys.exit(f"not a directory: {root}")

    tree = planning_model.PlanningTree.load(root)

    if args.tree:
        cols = tuple(c.strip() for c in args.columns.split(",") if c.strip())
        print(render_tree_text(tree, cols))
        return

    grammar_scan = list(checks.GrammarCheck.scan(root, os.path.basename(root)))
    problems_by_address = {address: problems for address, _, problems in grammar_scan}
    all_problems = [(address, p) for address, _, problems in grammar_scan for p in problems]

    renderer = PlanRenderer(args.thin)
    out = os.path.abspath(os.path.expanduser(args.out))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(renderer.render(tree, all_problems, problems_by_address))

    rows = list(tree.walk())
    problem_count = sum(len(p) for p in problems_by_address.values())
    print(f"{len(rows)} nodes, {problem_count} grammar problems -> {out}")


if __name__ == "__main__":
    main()
