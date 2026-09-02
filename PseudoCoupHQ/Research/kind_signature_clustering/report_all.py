#!/usr/bin/env python3
"""report_all.py — ecosystem-scale structure report (plan step 3, §3-§7 of
log_014). Reads spectrum_all.npz + archetypes.json + grammar_inventory.json
and prints the report tables; machine-readable copy in report_all.json.

Sections computed:
  A. per-category structure at the reference threshold 0.40 (the owner's ruling:
     take everything, tag, report per category, never pre-filter);
  B. widest-band many-language clusters (the empirical-universals table);
  C. category-spanning vs within-category clusters;
  D. the isolated end (archetypes/kinds with no counterpart anywhere);
  E. survival of the log_010 §6 / log_013 §2 stable clusters inside the
     full-ecosystem tree.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""
import collections
import json
import os

import numpy as np
from scipy.cluster.hierarchy import fcluster
from scipy.spatial.distance import squareform

HERE = os.path.dirname(os.path.abspath(__file__))
REF_T = 0.40
CATS = ["general-purpose", "config", "dsl", "notation", "markup", "query",
        "other"]


def lang_of(member):
    return member.split(":")[0]


def main():
    d = np.load(os.path.join(HERE, "spectrum_all.npz"))
    hashes = [str(x) for x in d["labels"]]
    Z = d["Z"]
    n = len(hashes)
    arch = json.load(open(os.path.join(HERE, "archetypes.json")))
    inv = json.load(open(os.path.join(HERE, "grammar_inventory.json")))
    cat_of = {}
    for entry in inv:
        for g in entry.get("grammars", []):
            cat_of[g["file"][:-len(".node-types.json")]] = \
                entry.get("category", "unknown")
    mult = np.array([arch[h]["size"] for h in hashes], dtype=np.int64)
    members = [arch[h]["members"] for h in hashes]
    langs = [set(lang_of(m) for m in mm) for mm in members]
    cats = [collections.Counter(cat_of.get(lang_of(m), "unknown")
                                for m in mm) for mm in members]
    Draw = squareform(np.load(os.path.join(HERE, "dist_all.npy")))
    report = {}

    # ---- tree node bookkeeping ---------------------------------------
    node_leaves = {i: [i] for i in range(n)}
    node_birth = {i: 0.0 for i in range(n)}
    node_death = {}
    for i, (a, b, h, _s) in enumerate(Z):
        a, b = int(a), int(b)
        node_death[a] = node_death[b] = float(h)
        node_leaves[n + i] = node_leaves[a] + node_leaves[b]
        node_birth[n + i] = float(h)
    node_death[n + n - 2] = 1.0

    def node_stats(nid):
        lv = node_leaves[nid]
        ls = set().union(*(langs[i] for i in lv))
        cc = collections.Counter()
        for i in lv:
            cc.update(cats[i])
        return lv, ls, cc

    def cohesion(lv):
        """Multiplicity-weighted mean pairwise kind similarity (within-
        archetype kind pairs are exactly 1.0)."""
        m = mult[lv].astype(np.float64)
        M = m.sum()
        tot_pairs = M * (M - 1) / 2.0
        same = float((m * (m - 1) / 2.0).sum())
        idx = np.array(lv)
        S = 1.0 - Draw[np.ix_(idx, idx)]
        iu = np.triu_indices(len(lv), 1)
        cross = float((np.outer(m, m)[iu] * S[iu]).sum())
        return (same + cross) / tot_pairs if tot_pairs else 1.0

    # ---- A + C: reference-threshold partition, per category ----------
    assign = fcluster(Z, t=REF_T, criterion="distance")
    clusters = collections.defaultdict(list)
    for i, c in enumerate(assign):
        clusters[int(c)].append(i)
    per_cat = {c: {"kinds": 0, "xlang_within_cat": 0, "xcat": 0}
               for c in CATS + ["unknown"]}
    n_clusters = len(clusters)
    span_stats = {"clusters_multi_kind": 0, "clusters_xcat": 0,
                  "clusters_xlang": 0, "clusters_ge10_langs": 0,
                  "kinds_in_ge10_lang_clusters": 0}
    for c, lv in clusters.items():
        ls = set().union(*(langs[i] for i in lv))
        cc = collections.Counter()
        lang_by_cat = collections.defaultdict(set)
        for i in lv:
            for m in members[i]:
                g = lang_of(m)
                ct = cat_of.get(g, "unknown")
                cc[ct] += 1
                lang_by_cat[ct].add(g)
        kinds = int(mult[lv].sum())
        if kinds > 1:
            span_stats["clusters_multi_kind"] += 1
            if len(cc) > 1:
                span_stats["clusters_xcat"] += 1
            if len(ls) > 1:
                span_stats["clusters_xlang"] += 1
        if len(ls) >= 10:
            span_stats["clusters_ge10_langs"] += 1
            span_stats["kinds_in_ge10_lang_clusters"] += kinds
        for ct, cnt in cc.items():
            per_cat[ct]["kinds"] += cnt
            if len(lang_by_cat[ct]) >= 2:
                per_cat[ct]["xlang_within_cat"] += cnt
            if len(cc) > 1:
                per_cat[ct]["xcat"] += cnt
    report["reference_threshold"] = REF_T
    report["n_clusters_at_ref"] = n_clusters
    report["span_stats"] = span_stats
    report["per_category"] = per_cat
    print("== A/C: partition at t=%.2f: %d clusters ==" % (REF_T, n_clusters))
    print(json.dumps(span_stats, indent=1))
    print("\n| category | kinds | merges cross-language within-category | "
          "sits in category-spanning cluster |")
    print("|---|---|---|---|")
    for ct in CATS:
        p = per_cat[ct]
        if not p["kinds"]:
            continue
        print("| %s | %d | %d (%.1f%%) | %d (%.1f%%) |" %
              (ct, p["kinds"], p["xlang_within_cat"],
               100.0 * p["xlang_within_cat"] / p["kinds"],
               p["xcat"], 100.0 * p["xcat"] / p["kinds"]))

    # ---- B: widest-band many-language nodes --------------------------
    MIN_LANGS = 30
    cand = []
    for nid in node_leaves:
        birth = node_birth[nid]
        death = node_death.get(nid, 1.0)
        width = death - birth
        if width < 0.10:
            continue
        lv, ls, cc = node_stats(nid)
        if len(ls) < MIN_LANGS:
            continue
        cand.append((width, nid, lv, ls, cc, birth, death))
    cand.sort(key=lambda x: -x[0])
    top = []
    print("\n== B: widest-band clusters spanning >= %d languages "
          "(top 40) ==" % MIN_LANGS)
    for width, nid, lv, ls, cc, birth, death in cand[:40]:
        names = collections.Counter()
        for i in lv:
            for m in members[i]:
                names[m.split(":", 1)[1]] += 1
        coh = cohesion(lv)
        row = {"node": int(nid), "band": [round(birth, 3), round(death, 3)],
               "width": round(width, 3), "n_langs": len(ls),
               "n_kinds": int(mult[lv].sum()), "n_archetypes": len(lv),
               "cohesion": round(coh, 3),
               "categories": dict(cc),
               "top_names": names.most_common(8),
               "sample_members": sorted(members[lv[0]])[:6]}
        top.append(row)
        print(json.dumps(row))
    report["widest_band_many_language"] = top

    # ---- D: the isolated end -----------------------------------------
    np.fill_diagonal(Draw, np.inf)
    nearest = Draw.min(axis=1)
    iso_mask = nearest > 0.9
    none_mask = nearest >= 1.0
    iso = [(float(nearest[i]), hashes[i]) for i in np.flatnonzero(iso_mask)]
    iso.sort(reverse=True)
    report["isolated"] = {
        "archetypes_nearest_sim_lt_0.1": int(iso_mask.sum()),
        "kinds": int(mult[iso_mask].sum()),
        "archetypes_no_shared_feature_at_all": int(none_mask.sum()),
        "kinds_no_shared_feature": int(mult[none_mask].sum()),
        "examples": [{"nearest_sim": round(1.0 - dd, 3),
                      "members": arch[h]["members"][:4],
                      "size": arch[h]["size"]}
                     for dd, h in iso[:15]]}
    print("\n== D: isolated end ==")
    print(json.dumps(report["isolated"], indent=1))

    # ---- E: log_010/log_013 stable clusters inside the big tree ------
    old_sets = {
        "c/cpp else_clause": ["c:else_clause", "cpp:else_clause"],
        "c/cpp preproc_if family": ["c:preproc_elif", "c:preproc_if",
                                    "cpp:preproc_elif", "cpp:preproc_if"],
        "comments across 4 langs": ["c:comment", "cpp:comment",
                                    "dart:comment",
                                    "dart:documentation_comment",
                                    "python:comment",
                                    "python:line_continuation"],
        "lambda/closure": ["python:lambda", "rust:closure_expression"],
        "conditional_expression + rust:if_expression":
            ["c:conditional_expression", "cpp:conditional_expression",
             "rust:if_expression"],
        "loop family (do/while/for/switch)":
            ["c:do_statement", "c:for_statement", "c:switch_statement",
             "c:while_statement", "cpp:do_statement", "cpp:for_statement",
             "cpp:switch_statement", "cpp:while_statement",
             "dart:do_statement", "dart:switch_statement",
             "dart:while_statement"],
        "body/list family": ["rust:declaration_list",
                             "rust:field_declaration_list",
                             "c:declaration_list", "c:enumerator_list",
                             "c:field_declaration_list",
                             "cpp:declaration_list", "cpp:enumerator_list",
                             "cpp:field_declaration_list",
                             "dart:class_body", "dart:enum_body"],
        "c/cpp case_statement": ["c:case_statement", "cpp:case_statement"],
    }
    feats_all = json.load(open(os.path.join(HERE, "features_all.json")))
    fam = feats_all["members"]
    hidx = {h: i for i, h in enumerate(hashes)}

    def leaf_of(label):
        g, k = label.split(":", 1)
        return hidx[fam[g][k]]

    # union-find replay to find the join height of a leaf set
    print("\n== E: old stable clusters inside the full-ecosystem tree ==")
    esec = []
    for name, labels in old_sets.items():
        try:
            lf = sorted(set(leaf_of(x) for x in labels))
        except KeyError as e:
            print(name, "MISSING", e)
            continue
        # find smallest node containing all leaves
        target = set(lf)
        best = None
        if len(lf) == 1:
            best = lf[0]
        else:
            for i, (a, b, h, _s) in enumerate(Z):
                pass
            # walk: build containment bottom-up
            for nid in sorted(node_leaves, key=lambda q: len(node_leaves[q])):
                if target <= set(node_leaves[nid]):
                    best = nid
                    break
        lv, ls, cc = node_stats(best)
        same_arch = len(lf) == 1
        row = {"set": name, "n_labels": len(labels),
               "n_archetypes": len(lf),
               "joined_at": round(node_birth[best], 3),
               "containing_node_kinds": int(mult[lv].sum()),
               "containing_node_langs": len(ls),
               "containing_node_band": [round(node_birth[best], 3),
                                        round(node_death.get(best, 1.0), 3)],
               "single_archetype": same_arch}
        esec.append(row)
        print(json.dumps(row))
    report["old_stable_clusters"] = esec

    with open(os.path.join(HERE, "report_all.json"), "w") as f:
        json.dump(report, f, indent=1)
    print("\nwrote report_all.json")


if __name__ == "__main__":
    main()
