#!/usr/bin/env python3
"""query_path.py -- path queries over graph_go.json.

BFS over typed edges from a start node to the first node satisfying a goal
predicate. Prints the path (file:line, kind, name) with the edge type taken at
each step -- or, when no branch reaches the goal, the exact nodes where the
search died and the frontier kinds that stopped it.

Vocabulary: super-node / sub-node / co-node / sub-tree; higher / lower.

Examples
--------
  # find candidate start nodes
  python3 query_path.py --graph graph_go.json --find "ABIParamAssignment" --limit 20

  # path query
  python3 query_path.py --graph graph_go.json \
      --start-name paramsOut --start-file ssagen/abi.go \
      --goal-name Reg
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque


def load(path):
    with open(path) as fh:
        return json.load(fh)


def loc(n):
    return "%s:%d" % (n["file"], n.get("start_line", 0))


def matches(n, name=None, kind=None, file_sub=None, exact=False):
    if kind and n["kind"] != kind:
        return False
    if file_sub and file_sub not in n["file"]:
        return False
    if name:
        nm = n.get("name") or ""
        if exact:
            if nm != name:
                return False
        elif name.lower() not in nm.lower():
            return False
    return True


def build_index(doc):
    nodes = {n["id"]: n for n in doc["nodes"]}
    out = defaultdict(list)
    inn = defaultdict(list)
    for e in doc["edges"]:
        out[e["src"]].append(e)
        inn[e["dst"]].append(e)
    return nodes, out, inn


def bfs(nodes, out_edges, in_edges, starts, goal_fn, edge_types=None,
        reverse_types=None, max_nodes=2_000_000):
    """BFS over typed edges.

    `reverse_types` names edge types that may also be walked from lower end to
    higher end (e.g. resolves_to walked backwards turns a declaration into the
    set of references that read it -- needed for forward dataflow, since
    resolves_to is authored reference -> declaration).
    """
    seen = {s: None for s in starts}
    q = deque(starts)
    visited = 0
    dead = []
    while q:
        cur = q.popleft()
        visited += 1
        if visited > max_nodes:
            break
        if cur not in starts and goal_fn(nodes[cur]):
            return reconstruct(seen, cur), visited, dead
        steps = [(e, e["dst"], False) for e in out_edges.get(cur, [])
                 if not edge_types or e["type"] in edge_types]
        if reverse_types:
            steps += [(e, e["src"], True) for e in in_edges.get(cur, [])
                      if e["type"] in reverse_types]
        if not steps:
            dead.append(cur)
            continue
        for e, nxt, rev in steps:
            if nxt in seen or nxt not in nodes:
                continue
            seen[nxt] = (cur, e, rev)
            q.append(nxt)
    return None, visited, dead


def reconstruct(seen, end):
    chain = []
    cur = end
    while seen.get(cur) is not None:
        prev, e, rev = seen[cur]
        chain.append((prev, e, cur, rev))
        cur = prev
    chain.reverse()
    return chain


def render(nodes, chain):
    lines = []
    if not chain:
        return "(start node already satisfies the goal)"
    first = nodes[chain[0][0]]
    lines.append("  [0] %-34s %-18s %s" % (loc(first), first["kind"],
                                           first["name"]))
    for i, (_p, e, dst, rev) in enumerate(chain, 1):
        n = nodes[dst]
        label = e["type"] + ("/" + e["kind"] if e.get("kind") else "")
        if rev:
            label += " (reversed)"
        lines.append("       --%s-->" % label)
        lines.append("  [%d] %-34s %-18s %s" % (i, loc(n), n["kind"],
                                                n["name"]))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True)
    ap.add_argument("--find", help="list nodes whose name contains this")
    ap.add_argument("--find-kind")
    ap.add_argument("--find-file")
    ap.add_argument("--limit", type=int, default=40)

    ap.add_argument("--start-id")
    ap.add_argument("--start-name")
    ap.add_argument("--start-file")
    ap.add_argument("--start-kind")
    ap.add_argument("--start-exact", action="store_true")
    ap.add_argument("--all-starts", action="store_true",
                    help="seed BFS from every node matching the start filter")

    ap.add_argument("--goal-name")
    ap.add_argument("--goal-kind")
    ap.add_argument("--goal-file")
    ap.add_argument("--edge-types", help="comma-separated filter")
    ap.add_argument("--reverse-types",
                    help="comma-separated edge types also walkable backwards "
                         "(typically resolves_to: declaration -> its readers)")
    ap.add_argument("--json-out")
    args = ap.parse_args()

    doc = load(args.graph)
    nodes, out_edges, in_edges = build_index(doc)

    if args.find is not None or args.find_kind or args.find_file:
        hits = [n for n in nodes.values()
                if matches(n, args.find, args.find_kind, args.find_file)]
        hits.sort(key=lambda n: (n["file"], n.get("start_line", 0)))
        for n in hits[:args.limit]:
            print("%-40s %-14s %-30s %s" % (loc(n), n["kind"], n["name"][:30],
                                            n["id"]))
        print("-- %d match(es), showing %d" % (len(hits),
                                               min(len(hits), args.limit)))
        return

    if args.start_id:
        starts = [args.start_id]
    else:
        cand = [n for n in nodes.values()
                if matches(n, args.start_name, args.start_kind,
                           args.start_file, args.start_exact)]
        cand.sort(key=lambda n: (n["file"], n.get("start_line", 0)))
        if not cand:
            print("no start node matched", file=sys.stderr)
            sys.exit(2)
        starts = [n["id"] for n in cand] if args.all_starts else [cand[0]["id"]]

    def goal_fn(n):
        return matches(n, args.goal_name, args.goal_kind, args.goal_file)

    etypes = set(args.edge_types.split(",")) if args.edge_types else None
    rtypes = set(args.reverse_types.split(",")) if args.reverse_types else None
    chain, visited, dead = bfs(nodes, out_edges, in_edges, starts, goal_fn,
                               etypes, rtypes)

    result = {"starts": starts, "visited": visited, "found": chain is not None}
    print("START:")
    for s in starts[:5]:
        print("  %-34s %-18s %s" % (loc(nodes[s]), nodes[s]["kind"],
                                    nodes[s]["name"]))
    if len(starts) > 5:
        print("  ... %d start nodes total" % len(starts))
    print("GOAL: name~%r kind=%r file~%r" % (args.goal_name, args.goal_kind,
                                             args.goal_file))
    print("visited %d nodes" % visited)
    if chain is not None:
        print("\nPATH (%d hops):" % len(chain))
        print(render(nodes, chain))
        result["path"] = [
            {"step": 0, "id": chain[0][0], **{k: nodes[chain[0][0]][k]
                                              for k in ("kind", "name", "file",
                                                        "start_line")}}
        ] + [
            {"step": i, "edge": e["type"], "edge_kind": e.get("kind"),
             "reversed": rev, "id": dst,
             **{k: nodes[dst][k] for k in ("kind", "name", "file",
                                           "start_line")}}
            for i, (_p, e, dst, rev) in enumerate(chain, 1)
        ]
    else:
        print("\nNO PATH. Every branch died. Terminal nodes reached: %d"
              % len(dead))
        bykind = defaultdict(list)
        for d in dead:
            bykind[nodes[d]["kind"]].append(d)
        summary = []
        for k, ids in sorted(bykind.items(), key=lambda kv: -len(kv[1])):
            print("  %-22s %6d   e.g. %s" % (k, len(ids),
                                             " | ".join(
                                                 "%s %s" % (loc(nodes[i]),
                                                            nodes[i]["name"][:40])
                                                 for i in ids[:3])))
            summary.append({"kind": k, "count": len(ids),
                            "examples": [{"id": i, "loc": loc(nodes[i]),
                                          "name": nodes[i]["name"][:80]}
                                         for i in ids[:5]]})
        result["dead_ends"] = summary
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(result, fh, indent=2)
        print("\n(json written to %s)" % args.json_out)


if __name__ == "__main__":
    main()
