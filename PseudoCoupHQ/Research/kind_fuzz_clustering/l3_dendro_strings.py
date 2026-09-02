#!/usr/bin/env python3
"""l3_dendro_strings.py -- THRESHOLD-SPECTRUM clustering over the v2
CANONICAL STRINGS.  Assembly only; no probe runs.

Built 2026-08-20 from the v2 per-operator matrices (the owner's final
canonical-form rulings; see l3_per_op_matrices_v2.py and the dated
section of SUPPORT_conversion_spec.md).

Similarity between two lang.op matrices (the owner's rule):
  - align rows by the input pair (lhs_canon, rhs_canon);
  - where BOTH matrices carry the same input pair, score 1 if the
    output_canon strings are byte-identical, else 0;
  - similarity = mean over the shared input pairs;
  - input pairs present in only one matrix are EXCLUDED (no padding);
  - a column pair with no shared input pairs scores 0, and every
    column stays as its own leaf regardless.

DECISION (overturnable): a matrix can carry SEVERAL rows with the same
(lhs_canon, rhs_canon) -- different holders reading to the same canon.
The aligned value is the sorted SET of that pair's DISTINCT
output_canon strings; two matrices score 1 on the pair only when the
sets are byte-identical.  (A multiset would make holder COUNT a
disagreement, which the rule does not ask for -- go's three int
holders against python's four would zero every pair.)  Nothing is
averaged inside a pair.

Merge machinery: UPGMA average linkage with the Lance-Williams running
mean, imported from l3_dendro_extended.py (the precedent), along with
its sweep, tree build, and explorer HTML (single self-contained file,
data embedded; icicle + threshold slider + search).

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.
"""

import csv
import json
import os
import sys
import time

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from l3_dendro_extended import upgma, sweep, build_tree, \
    HTML_TEMPLATE                                                  # noqa

MAT_DIR = os.path.join(HERE, "matrices")


# --------------------------------------------------------------------
# load the v2 matrices -> column -> {(lhs_canon, rhs_canon): tuple}
# --------------------------------------------------------------------

def load_columns():
    idx = json.load(open(os.path.join(MAT_DIR, "index.json")))
    cols = {}
    for key, meta in idx["matrices"].items():
        per = {}
        for r in csv.DictReader(open(os.path.join(MAT_DIR,
                                                  meta["file"]))):
            per.setdefault((r["lhs_canon"], r["rhs_canon"]),
                           []).append(r["output_canon"])
        cols[key] = {k: tuple(sorted(set(v))) for k, v in per.items()}
    return cols


def sim(fa, fb):
    shared = fa.keys() & fb.keys()
    if not shared:
        return 0.0
    return sum(1 for k in shared if fa[k] == fb[k]) / len(shared)


def clusters_at(keys, hist, t):
    """union-find over the merges with similarity >= t."""
    parent = {}

    def find(x):
        while parent.get(x, x) != x:
            parent[x] = parent.get(parent[x], parent[x])
            x = parent[x]
        return x

    members = {i: [i] for i in range(len(keys))}
    node_members = dict(members)
    for h in hist:
        a, b, n = h["left"]["id"], h["right"]["id"], h["node"]
        node_members[n] = node_members[a] + node_members[b]
        if h["similarity"] >= t:
            parent[a] = n
            parent[b] = n
    groups = {}
    for i in range(len(keys)):
        x = i
        while x in parent:
            x = parent[x]
        groups.setdefault(x, []).append(keys[i])
    return list(groups.values())


COMPARE_OPS = {"==", "!=", "<", ">", "<=", ">=", "<=>", "===", "!==",
               "eq", "ne", "lt", "gt", "le", "ge", "equal?", "eql?",
               "not_eq"}


def is_compare(col):
    return col.partition(".")[2] in COMPARE_OPS


def main():
    print("string-clustering dendro -- v2 canonical strings, assembly "
          "only")
    t0 = time.time()
    cols = load_columns()
    keys = sorted(cols)
    print("  %d columns loaded (%.1f s)" % (len(keys), time.time() - t0))

    hist = upgma(keys, lambda a, b: sim(cols[a], cols[b]))
    rows, plats, sims = sweep(len(keys), hist)
    tree = build_tree(keys, hist)
    print("  %d merges (%.1f s)" % (len(hist), time.time() - t0))

    # ---------------------------------------------- headless verify
    print("HEADLESS VERIFY")
    assert tree["n_leaves"] == len(keys)
    print("  [leaves] %d leaves == %d columns" % (tree["n_leaves"],
                                                  len(keys)))
    for x in range(1, len(sims)):
        assert sims[x] <= sims[x - 1] + 1e-9
    print("  [monotone] %d merge similarities non-increasing" % len(sims))
    byid = {n["id"]: n for n in tree["nodes"]}

    def walk_count(t):
        c = 0

        def g(n):
            nonlocal c
            if n["birth"] >= t:
                c += 1
                return
            for sid in n["subs"]:
                g(byid[sid])
        g(byid[tree["root_id"]])
        return c

    bad = 0
    for step in range(101):
        t = step / 100.0
        a = walk_count(t)
        b = len(keys) - sum(1 for s in sims if s >= t)
        if a != b:
            bad += 1
    print("  [band-walk] tree walk vs merge history over 101 "
          "thresholds: %d disagreements" % bad)

    # ---------------------------------------------- sanity numbers
    print("SANITY")
    s_gr = sim(cols["go.+"], cols["rust.+"])
    s_gp = sim(cols["go.+"], cols["python.+"])
    print("  go.+ ~ rust.+   = %.4f  (shared input pairs: %d)"
          % (s_gr, len(cols["go.+"].keys() & cols["rust.+"].keys())))
    print("  go.+ ~ python.+ = %.4f  (shared input pairs: %d)"
          % (s_gp, len(cols["go.+"].keys() & cols["python.+"].keys())))
    go_cluster = {}
    for t in (0.95, 0.85, 0.70):
        for grp in clusters_at(keys, hist, t):
            if "go.+" in grp:
                go_cluster[t] = sorted(grp)
                ar = [c for c in grp if not is_compare(c)]
                cm = [c for c in grp if is_compare(c)]
                print("  go.+ cluster at t=%.2f (%d members, %d "
                      "arithmetic-side, %d comparison): %s"
                      % (t, len(grp), len(ar), len(cm),
                         ", ".join(sorted(grp))))
                break
    # does an arithmetic group form DISTINCT from comparisons?
    for t in (0.95, 0.85, 0.70):
        grp = go_cluster[t]
        cm = [c for c in grp if is_compare(c)]
        print("  at t=%.2f the go.+ cluster %s comparison columns"
              % (t, "is FREE of" if not cm
                 else "still holds %d" % len(cm)))

    out = dict(
        status="STRING-CLUSTERING DENDRO, v2 CANONICAL STRINGS, "
               "ASSEMBLY ONLY",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        design="similarity = mean per-shared-input-pair byte-identity "
               "of output_canon; input pairs in only one matrix are "
               "excluded; no padding; UPGMA average linkage",
        source="matrices/ (v2, the owner's final canonical forms)",
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        family_order=["strings"],
        families=dict(strings=dict(
            name="strings", n_leaves=len(keys), leaves=keys,
            merge_history=hist, cluster_count_curve=rows,
            stability_plateaus=plats, tree=tree, crosslinks=[])),
    )
    jp = os.path.join(HERE, "dendro_strings.json")
    json.dump(out, open(jp, "w"), separators=(",", ":"), default=str)
    print("  wrote %s (%.2f MB)" % (jp, os.path.getsize(jp) / 1e6))

    html = HTML_TEMPLATE.replace(
        "__DENDRO__", json.dumps(out, separators=(",", ":"),
                                 default=str))
    html = html.replace(
        "Extended clustering &mdash; threshold spectrum, per "
        "coordinate family",
        "String clustering &mdash; threshold spectrum over the v2 "
        "canonical strings")
    hp = os.path.join(HERE, "dendrogram_strings.html")
    with open(hp, "w") as f:
        f.write(html)
    print("  wrote %s (%.2f MB)" % (hp, os.path.getsize(hp) / 1e6))


if __name__ == "__main__":
    main()
