#!/usr/bin/env bash
# t87 lane 12 — every numeric claim in log 193 that is not already a
# literal from an earlier lane, checked against the artifacts. An audit
# whose claims outnumber its tool calls is rejected, so the claims are
# recomputed here rather than asserted.
#
# THE SPELLING BAN, ABSOLUTE (the owner, 2026-08-25). No operator token in any
# key, grouping, pairing, row structure, candidate selection or
# comparison scope. Nothing here groups by a label; labels are only
# COUNTED, to prove the grouping did not use them.
set -u
say() { echo; echo "======== $* ========"; }
cd PseudoCoupHQ/Research/compiler_graph

say "[1/3] variants spanning both source languages of the one compiler"
python3 - <<'PY'
import json
for path in ("variant_connections_c_and_cpp.json",
             "variant_connections_extended.json"):
    d = json.load(open('PseudoCoupHQ/Research/compiler_graph/' + path))
    rows = d["variants"]
    both = [r for r in rows if len(r["languages"]) > 1]
    print("   %-40s %5d variants, %4d span more than one language"
          % (path, len(rows), len(both)))
PY

say "[2/3] member-count distribution, and the singleton share"
python3 - <<'PY'
import json
for path in ("variant_connections_go.json",
             "variant_connections_c_and_cpp.json",
             "variant_connections_extended.json"):
    d = json.load(open('PseudoCoupHQ/Research/compiler_graph/' + path))
    rows = d["variants"]
    sizes = sorted((r["member_count"] for r in rows), reverse=True)
    ones = sum(1 for s in sizes if s == 1)
    print("   %-40s variants %5d  largest %4d  singletons %5d  members total %5d"
          % (path, len(rows), sizes[0], ones, sum(sizes)))
PY

say "[3/3] the eight exclusive transitions of the worked example, backing recounted"
python3 - <<'PY'
import json
d = json.load(open('PseudoCoupHQ/Research/compiler_graph/'
                   'variant_connections_c_and_cpp.json'))
row = d["variants"][0]
ex = row["exclusive_transition_examples"]
backed = sum(1 for e in ex if e["backed_by_a_static_call_edge"])
print("   variant %s: %d examples printed, %d of them backed by a static "
      "call edge" % (row["variant_id"], len(ex), backed))
labels = set(m["operator"] for m in row["members"])
print("   distinct display labels among its members: %d" % len(labels))
print("   go: mixed-label variants and the widest-spread label, recounted")
g = json.load(open('PseudoCoupHQ/Research/compiler_graph/'
                   'variant_connections_go.json'))
mixed = 0
spread = {}
for r in g["variants"]:
    ls = set(m["operator"] for m in r["members"])
    if len(ls) > 1:
        mixed += 1
    for l in ls:
        spread.setdefault(l, set()).add(r["variant_id"])
top = sorted(((len(v), k) for k, v in spread.items()), reverse=True)[:3]
print("      mixed-label go variants: %d of %d" % (mixed, len(g["variants"])))
print("      widest-spread go labels: %s"
      % ", ".join("%s in %d variants" % (json.dumps(k), n) for n, k in top))
PY
echo "DONE t87_l12"
