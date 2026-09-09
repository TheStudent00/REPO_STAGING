#!/usr/bin/env python3
"""A card explorer for a planning tree — click a node to open it.

    python3 PlanPlan/framework/explorer.py <root> -o view.html
    python3 PlanPlan/framework/explorer.py <root> --serve 8800

WHAT IT IS. One card per node. A card shows the node's name, its
designation and status, and its definition line. Clicking it opens the
card in place: the files in that node's folder, then its sub-node cards
indented beneath. Closed, the page is a list of top-level cards; opened
all the way down, it is the whole tree.

`realize: false` register entries get cards too, marked — they are
structure the register states, and a view that omitted them would show
less than the plan says.

WHY IT IS NOT AUTO-UPDATING BY ITSELF. A page opened from a `file://`
URL cannot run a program on the machine showing it; browsers forbid
that, and no amount of embedded script changes it. So freshness comes
one of two ways:

  -o FILE      write a snapshot. Self-contained: the data is embedded,
               the script is inline, nothing is fetched. Re-run to
               refresh.
  --serve PORT re-scan the tree on EVERY request and serve the result.
               Refreshing the page in the browser is then the same act
               as re-running the analysis.

Standard library only, like every tool here — `http.server` and
`json`. No CDN, no framework, no build step.
"""
import argparse
import html
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import planning_model  # noqa: E402

NAME_RE = re.compile(r"^node_(?:\d+_)*\d+_([a-z0-9_]+)$")


def node_name(node):
    m = NAME_RE.match(os.path.basename(node.path))
    return m.group(1) if m else node.frontmatter.get("id", "?")


def first_sentence(text, limit=160):
    t = " ".join(text.split())
    if not t:
        return ""
    dot = t.find(". ")
    if dot != -1:
        t = t[:dot + 1]
    return t if len(t) <= limit else t[:limit - 1] + "…"


def node_files(node):
    """Every file in the node's own folder, by role, in reading order."""
    out = []
    try:
        entries = sorted(os.listdir(node.path))
    except OSError:
        return out
    for e in entries:
        full = os.path.join(node.path, e)
        if not os.path.isfile(full):
            continue
        if e.startswith("CORE_"):
            role = "CORE"
        elif e == "PROGRESS.md":
            role = "PROGRESS"
        elif e.startswith("CHECK_"):
            role = "CHECK"
        elif e.startswith("SUPPORT_"):
            role = "SUPPORT"
        elif e == "DASHBOARD.md":
            role = "DASHBOARD"
        else:
            role = "other"
        try:
            size = os.path.getsize(full)
        except OSError:
            size = 0
        out.append({"name": e, "role": role, "path": full, "bytes": size})
    order = {"CORE": 0, "PROGRESS": 1, "CHECK": 2, "SUPPORT": 3,
             "DASHBOARD": 4, "other": 5}
    out.sort(key=lambda f: (order[f["role"]], f["name"]))
    return out


def to_data(node):
    fm = node.frontmatter
    kids = [to_data(k) for k in node.sub_nodes]
    for e in node.sub_edges:
        if e.get("realize") is False:
            kids.append({
                "name": e.get("name", "?"),
                "designation": e.get("designation", ""),
                "status": "", "definition": "",
                "unrealized": True, "files": [], "children": [],
                "id": "", "address": "",
            })
    return {
        "name": node_name(node),
        "id": fm.get("id", ""),
        "address": node.address,
        "designation": fm.get("designation", ""),
        "status": fm.get("status", ""),
        "definition": first_sentence(node.definition),
        "unrealized": False,
        "files": node_files(node),
        "children": kids,
    }


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>%(title)s</title>
<style>
 :root { color-scheme: light dark; }
 body { font: 14px/1.5 ui-sans-serif, system-ui, sans-serif;
        margin: 0; padding: 24px; max-width: 1100px; }
 h1 { font-size: 18px; margin: 0 0 4px; }
 .meta { opacity: .65; margin-bottom: 20px; font-size: 13px; }
 .card { border: 1px solid rgba(128,128,128,.35); border-radius: 8px;
         padding: 10px 12px; margin: 6px 0; cursor: pointer;
         background: rgba(128,128,128,.05); }
 .card:hover { border-color: rgba(128,128,128,.7); }
 .card.open { background: rgba(128,128,128,.11); }
 .card.leaf { cursor: default; }
 .row { display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap; }
 .name { font-weight: 650; }
 .tag { font-size: 11px; padding: 1px 7px; border-radius: 10px;
        border: 1px solid rgba(128,128,128,.4); opacity: .85; }
 .def { opacity: .75; margin-top: 4px; }
 .kids { margin-left: 22px; border-left: 2px solid rgba(128,128,128,.25);
         padding-left: 12px; }
 /* One file per line. A wrapping row re-flows as the window narrows,
    which moves every entry and makes the list unreadable at small
    widths; a stacked list stays put. */
 .files { margin: 8px 0 4px; display: flex; flex-direction: column; gap: 2px; }
 .file { font-size: 12px; text-decoration: none; padding: 2px 6px;
         border-left: 2px solid rgba(128,128,128,.35);
         display: flex; gap: 8px; align-items: baseline; }
 .file:hover { background: rgba(128,128,128,.12); }
 .file .role { flex: 0 0 5.5em; opacity: .6; font-size: 11px;
               text-transform: lowercase; }
 .file .fname { overflow-wrap: anywhere; }
 .ghost { opacity: .6; border-style: dashed; }
 .caret { width: 12px; display: inline-block; opacity: .6; }
 button { font: inherit; margin-right: 8px; padding: 3px 10px;
          border-radius: 6px; border: 1px solid rgba(128,128,128,.5);
          background: transparent; cursor: pointer; }
</style>
<h1>%(title)s</h1>
<div class="meta">%(count)s nodes &middot; %(root)s%(live)s</div>
<div><button id="all">expand all</button><button id="none">collapse all</button></div>
<div id="tree"></div>
<script>
const DATA = %(data)s;

function el(tag, cls, text) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined) n.textContent = text;
  return n;
}

function card(node) {
  const wrap = el('div');
  const c = el('div', 'card' + (node.unrealized ? ' ghost' : ''));
  const hasMore = node.children.length || node.files.length;
  if (!hasMore) c.classList.add('leaf');

  const row = el('div', 'row');
  const caret = el('span', 'caret', hasMore ? '\\u25B8' : '');
  row.append(caret, el('span', 'name', node.name));
  if (node.designation) row.append(el('span', 'tag', node.designation));
  if (node.status) row.append(el('span', 'tag', node.status));
  if (node.unrealized) row.append(el('span', 'tag', 'realize: false'));
  if (node.children.length)
    row.append(el('span', 'tag', node.children.length + ' sub'));
  c.append(row);
  if (node.definition) c.append(el('div', 'def', node.definition));

  const body = el('div');
  body.style.display = 'none';
  if (node.files.length) {
    const fl = el('div', 'files');
    for (const f of node.files) {
      const a = el('a', 'file');
      a.append(el('span', 'role', f.role), el('span', 'fname', f.name));
      a.href = 'file://' + f.path;
      a.title = f.path + '  (' + f.bytes + ' bytes)';
      a.onclick = e => e.stopPropagation();
      fl.append(a);
    }
    body.append(fl);
  }
  if (node.children.length) {
    const kids = el('div', 'kids');
    for (const k of node.children) kids.append(card(k));
    body.append(kids);
  }

  if (hasMore) {
    c.onclick = e => {
      e.stopPropagation();
      const open = body.style.display === 'none';
      body.style.display = open ? 'block' : 'none';
      c.classList.toggle('open', open);
      caret.textContent = open ? '\\u25BE' : '\\u25B8';
    };
  }
  wrap.append(c, body);
  return wrap;
}

document.getElementById('tree').append(card(DATA));
function setAll(open) {
  document.querySelectorAll('.card').forEach(c => {
    const body = c.nextSibling;
    if (!body || c.classList.contains('leaf')) return;
    body.style.display = open ? 'block' : 'none';
    c.classList.toggle('open', open);
    const caret = c.querySelector('.caret');
    if (caret) caret.textContent = open ? '\\u25BE' : '\\u25B8';
  });
}
document.getElementById('all').onclick = () => setAll(true);
document.getElementById('none').onclick = () => setAll(false);
</script>
"""


def count_nodes(d):
    return 1 + sum(count_nodes(k) for k in d["children"])


def build(roots, live=False, title=None):
    """One page for one tree, or one page for several.

    Several is the normal case: a project is more than one repo, and a
    view that shows one at a time makes the reader hold the rest in
    their head."""
    if isinstance(roots, str):
        roots = [roots]
    trees = []
    for r in roots:
        d = to_data(planning_model.PlanningTree.load(r).root_node)
        d["repo"] = os.path.basename(os.path.dirname(r))
        trees.append(d)

    if len(trees) == 1:
        data = trees[0]
        heading = title or f"{trees[0]['repo']} — plan"
    else:
        data = {
            "name": title or "the line",
            "id": "", "address": "", "designation": "",
            "status": f"{len(trees)} repos", "definition": "",
            "unrealized": False, "files": [], "children": trees,
        }
        heading = title or "planning — all repos"
        # A repo card shows the repo name rather than the root's id,
        # because that is the name a reader navigates by on disk.
        for t in trees:
            t["name"] = t["repo"]

    return PAGE % {
        "title": html.escape(heading),
        "root": html.escape(", ".join(
            os.path.basename(os.path.dirname(r)) for r in roots)),
        "count": count_nodes(data),
        "data": json.dumps(data),
        "live": " &middot; live: refresh to re-scan" if live else "",
    }


def serve(roots, port):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = build(roots, live=True).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    print(f"serving {len(roots)} tree(s)\n"
          f"  http://127.0.0.1:{port}/   (refresh = re-scan)")
    print("  ctrl-c to stop")
    try:
        HTTPServer(("127.0.0.1", port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("roots", nargs="+",
                    help="one or more planning roots (node_0 folders)")
    ap.add_argument("-o", "--out", help="where to write; defaults to "
                                        "plan_explorer.html beside the first root's repo")
    ap.add_argument("--title", help="page heading")
    ap.add_argument("--serve", type=int, metavar="PORT",
                    help="serve on 127.0.0.1:PORT, re-scanning per request")
    args = ap.parse_args()

    roots = []
    for r in args.roots:
        p = os.path.abspath(os.path.expanduser(r))
        if not os.path.isdir(p):
            sys.exit(f"not a directory: {p}")
        roots.append(p)

    if args.serve:
        return serve(roots, args.serve)

    # Default output sits beside the first root's repo, not in the
    # planning tree — an .html inside a node folder is a stray by the
    # grammar (§1) and would break the checks.
    default = os.path.join(os.path.dirname(os.path.dirname(roots[0])),
                           "plan_explorer.html")
    out = os.path.abspath(os.path.expanduser(args.out or default))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build(roots, title=args.title))
    print(f"-> {out}")


if __name__ == "__main__":
    main()
