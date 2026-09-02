#!/usr/bin/env python3
"""validate_all.py — hold-out validation AT ECOSYSTEM SCALE (plan step 3.2).

Same protocol as log_010 §3 / validate_holdout.py, over ALL 411 grammars:
features rebuilt WITHOUT declared supertype memberships
(features_all.py --hold-out-declared), the multiplicity-weighted merge-tree
spectrum re-derived from them (spectrum_all_holdout.npz), then for every
(grammar, declared supertype) group with >= 3 clusterable members we test
whether held-out spectrum similarities separate within-supertype pairs
from (member, non-member) pairs of the SAME grammar. AUC = Mann-Whitney.

Similarity of two kinds = 1 - merge height of their hold-out archetypes
(1.0 when they share an archetype — exact under the multiplicity-weighted
linkage, which is UPGMA over the full kind population).

Reference frame, not oracle (the owner's ruling): the grammars' own supertype
declarations are per-language design choices; agreement is evidence.

Output: holdout_validation_all.json + pipe-table summary (overall and
per category). Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""
import collections
import json
import os

import numpy as np
from scipy.spatial.distance import squareform

from validate_holdout import auc

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_ALL = os.path.join(HERE, "raw_all")


def main():
    d = np.load(os.path.join(HERE, "spectrum_all_holdout.npz"))
    hashes = [str(x) for x in d["labels"]]
    hidx = {h: i for i, h in enumerate(hashes)}
    S = 1.0 - squareform(d["merge_condensed"])
    np.fill_diagonal(S, 1.0)

    feats = json.load(open(os.path.join(HERE, "features_all_holdout.json")))
    members = feats["members"]          # grammar -> kind -> archetype hash

    inv = json.load(open(os.path.join(HERE, "grammar_inventory.json")))
    cat_of = {}
    for entry in inv:
        for g in entry.get("grammars", []):
            cat_of[g["file"][:-len(".node-types.json")]] = \
                entry.get("category", "unknown")

    rows = []
    for fn in sorted(os.listdir(RAW_ALL)):
        if not fn.endswith(".node-types.json"):
            continue
        g = fn[:-len(".node-types.json")]
        if g not in members:
            continue
        data = json.load(open(os.path.join(RAW_ALL, fn)))
        sups = {e["type"]: [s["type"] for s in e["subtypes"]]
                for e in data if "subtypes" in e}
        if not sups:
            continue
        gm = members[g]
        all_idx = {k: hidx[h] for k, h in gm.items()}
        for sup, subs in sorted(sups.items()):
            mem = sorted(set(k for k in subs if k in all_idx))
            if len(mem) < 3:
                continue
            non = sorted(set(all_idx) - set(mem))
            if not non:
                continue
            mi = np.array([all_idx[k] for k in mem])
            ni = np.array([all_idx[k] for k in non])
            within = S[np.ix_(mi, mi)][np.triu_indices(len(mi), 1)]
            across = S[np.ix_(mi, ni)].ravel()
            rows.append({"grammar": g, "category": cat_of.get(g, "unknown"),
                         "supertype": sup, "n": len(mem),
                         "mean_within": round(float(within.mean()), 3),
                         "mean_across": round(float(across.mean()), 3),
                         "auc": round(float(auc(within, across)), 3)})

    aucs = np.array([r["auc"] for r in rows])
    summary = {"n_groups": len(rows),
               "n_grammars": len(set(r["grammar"] for r in rows)),
               "mean_auc": round(float(aucs.mean()), 3),
               "median_auc": round(float(np.median(aucs)), 3),
               "groups_ge_0.6": int((aucs >= 0.6).sum()),
               "mean_within": round(float(np.mean(
                   [r["mean_within"] for r in rows])), 3),
               "mean_across": round(float(np.mean(
                   [r["mean_across"] for r in rows])), 3)}
    per_cat = {}
    for cat in sorted(set(r["category"] for r in rows)):
        ca = np.array([r["auc"] for r in rows if r["category"] == cat])
        per_cat[cat] = {"n_groups": len(ca),
                        "mean_auc": round(float(ca.mean()), 3),
                        "median_auc": round(float(np.median(ca)), 3),
                        "groups_ge_0.6": int((ca >= 0.6).sum())}

    out = {"summary": summary, "per_category": per_cat, "per_group": rows}
    with open(os.path.join(HERE, "holdout_validation_all.json"), "w") as f:
        json.dump(out, f, indent=1)

    print("overall: %d groups over %d grammars — mean AUC %.3f, median "
          "%.3f, %d/%d >= 0.6; mean within %.3f vs across %.3f" %
          (summary["n_groups"], summary["n_grammars"], summary["mean_auc"],
           summary["median_auc"], summary["groups_ge_0.6"],
           summary["n_groups"], summary["mean_within"],
           summary["mean_across"]))
    print("\n| category | groups | mean AUC | median AUC | >=0.6 |")
    print("|---|---|---|---|---|")
    for cat, s in per_cat.items():
        print("| %s | %d | %.3f | %.3f | %d |" %
              (cat, s["n_groups"], s["mean_auc"], s["median_auc"],
               s["groups_ge_0.6"]))
    print("\nwrote holdout_validation_all.json")


if __name__ == "__main__":
    main()
