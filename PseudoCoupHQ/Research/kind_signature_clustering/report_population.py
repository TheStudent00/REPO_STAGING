#!/usr/bin/env python3
"""report_population.py — the owner's rulings 2b and 3 (2026-08-12): whole-
population reporting (all 800 named kinds, none sampled) and the two
presentation artifacts, all computed as QUERIES against the merge-tree
spectrum in similarity_matrix.npz (full features, not the hold-out run).

Emits:
  - best_counterparts.json : for EVERY kind, its nearest counterpart in
    each OTHER language with the spectrum similarity (ties on merge height
    broken by raw weighted Jaccard similarity).
  - best_counterparts.md   : readable slice — per language pair, the
    strongest mutual matches; plus the isolated kinds.
  - cluster_by_language.md : rows = clusters at the stated reference
    threshold 0.40, columns = the five languages, cells = member kind
    names; each row also carries internal cohesion (mean within-cluster
    raw similarity) and the threshold band [birth, death) over which that
    exact member set is a maximal cluster in the merge tree.
  - aggregates.json + printed tables: per-language-pair mean similarity
    (5x5), the 20 highest cross-language pairs, the 10 most isolated
    kinds, and the widest-band multi-language clusters.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""
import json
import os
import numpy as np

import spectrum

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["rust", "python", "dart", "c", "cpp"]
REF_THRESHOLD = 0.40


def main():
    labels, Z, S = spectrum.load_spectrum()
    R = 1.0 - spectrum.load_spectrum.raw  # raw weighted Jaccard similarity
    np.fill_diagonal(R, 1.0)
    lang_of = [l.split(":", 1)[0] for l in labels]
    kind_of = [l.split(":", 1)[1] for l in labels]
    lang_idx = {lg: np.array([i for i, x in enumerate(lang_of) if x == lg])
                for lg in LANGS}

    # ---- 2b: best counterpart of EVERY kind in each other language ----
    best = {}
    for i, lab in enumerate(labels):
        row = {}
        for lg in LANGS:
            if lg == lang_of[i]:
                continue
            cand = lang_idx[lg]
            s = S[i, cand]
            m = s.max()
            tied = cand[s >= m - 1e-9]
            j = tied[np.argmax(R[i, tied])]  # tie-break on raw similarity
            row[lg] = {"kind": kind_of[j], "similarity": round(float(m), 3),
                       "raw_similarity": round(float(R[i, j]), 3)}
        best[lab] = row
    with open(os.path.join(HERE, "best_counterparts.json"), "w") as f:
        json.dump(best, f, indent=1, sort_keys=True)

    # isolation score: best similarity to ANY other-language kind
    iso = {lab: max(v["similarity"] for v in best[lab].values())
           for lab in labels}
    isolated = sorted(iso.items(), key=lambda kv: kv[1])[:10]

    # top cross-language pairs by spectrum similarity, raw as tie-break
    iu = np.triu_indices(len(labels), 1)
    cross = [(S[a, b], R[a, b], labels[a], labels[b])
             for a, b in zip(*iu) if lang_of[a] != lang_of[b]]
    cross.sort(key=lambda t: (-t[0], -t[1]))
    top20 = cross[:20]
    # Two saturation sources push cross pairs to similarity ~1.0 (merge
    # height 0): (a) c and cpp ship near-identical grammars, (b) kinds whose
    # only features are a weak sub-node spec have IDENTICAL feature sets
    # (raw distance 0) and merge at height 0 in one degenerate group. Both
    # drown the informative list; report the saturation count (split by
    # cause) and a second top-20 over non-saturated pairs only.
    saturated = [t for t in cross if t[0] >= 0.999]
    n_saturated = len(saturated)
    n_sat_ccpp = sum(1 for t in saturated
                     if {t[2].split(":")[0], t[3].split(":")[0]} ==
                     {"c", "cpp"})
    top20_nosat = [t for t in cross if t[0] < 0.999][:20]

    # per-language-pair mean similarity (5x5)
    pair_mean = {}
    for a in LANGS:
        for b in LANGS:
            block = S[np.ix_(lang_idx[a], lang_idx[b])]
            if a == b:
                n = len(lang_idx[a])
                v = block[np.triu_indices(n, 1)].mean()
            else:
                v = block.mean()
            pair_mean[(a, b)] = float(v)

    # ---- 3a: cluster_by_language.md at the reference threshold ----
    clusters = spectrum.clusters_at(REF_THRESHOLD)
    bands = spectrum.stability_bands()
    lab_i = {l: i for i, l in enumerate(labels)}
    n_single = sum(1 for c in clusters if len(c) == 1)
    lines = ["# Clusters by language (reference threshold %.2f)" % REF_THRESHOLD,
             "",
             "Rows = clusters discovered at the reference slice of the merge",
             "tree; any other slice is a query (`spectrum.clusters_at(t)`).",
             "Cohesion = mean within-cluster raw weighted-Jaccard similarity.",
             "Band = threshold range [birth, death) over which this exact",
             "member set is a maximal cluster in the merge tree; width in",
             "parentheses. Singleton clusters are omitted (%d of them)."
             % n_single,
             "",
             "| cluster | cohesion | band (width) | " +
             " | ".join(LANGS) + " |",
             "|---|---|---|" + "---|" * len(LANGS)]
    rows_meta = []
    for ci, mem in enumerate(clusters):
        if len(mem) == 1:
            continue
        ids = np.array([lab_i[m] for m in mem])
        coh = R[np.ix_(ids, ids)][np.triu_indices(len(ids), 1)].mean()
        band = bands.get(frozenset(mem))
        btxt = ("%.2f-%.2f (%.2f)" % (band[0], band[1], band[1] - band[0])
                if band else "n/a")
        cells = []
        for lg in LANGS:
            ks = sorted(k.split(":", 1)[1] for k in mem
                        if k.startswith(lg + ":"))
            cells.append(", ".join(ks) if ks else "—")
        lines.append("| s%03d | %.3f | %s | %s |" %
                     (ci, coh, btxt, " | ".join(cells)))
        rows_meta.append({"cluster": "s%03d" % ci, "n": len(mem),
                          "n_langs": len({m.split(":")[0] for m in mem}),
                          "cohesion": round(float(coh), 3),
                          "band": [round(band[0], 3), round(band[1], 3)]
                          if band else None,
                          "members": mem})
    with open(os.path.join(HERE, "cluster_by_language.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

    # widest-band clusters spanning >= 2 languages (the strong assertions)
    stable = sorted([r for r in rows_meta if r["n_langs"] >= 2],
                    key=lambda r: -(r["band"][1] - r["band"][0]))

    # narrow-band clusters (exist only in narrow slices)
    narrow = [r for r in rows_meta
              if r["n_langs"] >= 2 and (r["band"][1] - r["band"][0]) < 0.03]

    # ---- readable best-counterparts slice ----
    md = ["# Best counterparts — readable slice",
          "",
          "Full population is in `best_counterparts.json` (every one of the",
          "800 kinds, its nearest counterpart in each other language).",
          "Similarity = co-cluster fraction across the threshold spectrum.",
          "", "## 20 highest cross-language pairs", "",
          "| similarity | raw | kind A | kind B |", "|---|---|---|---|"]
    for s, r, a, b in top20:
        md.append("| %.3f | %.3f | %s | %s |" % (s, r, a, b))
    md += ["", "%d cross-language pairs saturate at similarity ~1.0 "
           "(%d of them c<->cpp twins from near-identical shipped grammars; "
           "the rest are identical-featured weak-sub-node-spec kinds that "
           "merge at height 0)." % (n_saturated, n_sat_ccpp),
           "", "## 20 highest NON-saturated cross-language pairs", "",
           "| similarity | raw | kind A | kind B |", "|---|---|---|---|"]
    for s, r, a, b in top20_nosat:
        md.append("| %.3f | %.3f | %s | %s |" % (s, r, a, b))
    md += ["", "## 10 most isolated kinds", "",
           "No counterpart above the stated similarity anywhere — reported,",
           "not hidden.", "",
           "| kind | best cross-language similarity | best counterpart |",
           "|---|---|---|"]
    for lab, v in isolated:
        bl, bv = max(best[lab].items(), key=lambda kv: kv[1]["similarity"])
        md.append("| %s | %.3f | %s:%s |" % (lab, v, bl, bv["kind"]))
    with open(os.path.join(HERE, "best_counterparts.md"), "w") as f:
        f.write("\n".join(md) + "\n")

    # ---- aggregates ----
    agg = {"reference_threshold": REF_THRESHOLD,
           "n_kinds": len(labels),
           "n_clusters_at_reference": len(clusters),
           "n_singletons_at_reference": n_single,
           "pair_mean": {a + ":" + b: round(pair_mean[(a, b)], 3)
                         for a in LANGS for b in LANGS},
           "top20_cross_pairs": [[round(s, 3), a, b] for s, _, a, b in top20],
           "n_saturated_cross_pairs": n_saturated,
           "n_saturated_c_cpp": n_sat_ccpp,
           "top20_cross_pairs_non_saturated":
               [[round(s, 3), a, b] for s, _, a, b in top20_nosat],
           "isolated10": [[lab, round(v, 3)] for lab, v in isolated],
           "widest_band_multilanguage": stable[:15],
           "narrow_band_multilanguage": narrow[:15],
           "all_multilanguage_clusters": stable}
    with open(os.path.join(HERE, "aggregates.json"), "w") as f:
        json.dump(agg, f, indent=1, default=float)

    # print for the log
    print("| mean sim | " + " | ".join(LANGS) + " |")
    print("|---|" + "---|" * len(LANGS))
    for a in LANGS:
        print("| %s | " % a +
              " | ".join("%.3f" % pair_mean[(a, b)] for b in LANGS) + " |")
    print()
    print("clusters at %.2f: %d (%d singletons); multi-language non-singleton"
          ": %d" % (REF_THRESHOLD, len(clusters), n_single,
                    len([r for r in rows_meta if r["n_langs"] >= 2])))
    print()
    print("widest-band multi-language clusters:")
    for r in stable[:12]:
        print("  %s width %.2f band %.2f-%.2f coh %.3f n=%d langs=%d: %s" %
              (r["cluster"], r["band"][1] - r["band"][0], r["band"][0],
               r["band"][1], r["cohesion"], r["n"], r["n_langs"],
               ", ".join(r["members"][:12]) +
               ("..." if r["n"] > 12 else "")))
    print()
    print("narrow-band (<0.03) multi-language clusters: %d" % len(narrow))
    for r in narrow[:6]:
        print("  %s band %.2f-%.2f: %s" % (r["cluster"], r["band"][0],
              r["band"][1], ", ".join(r["members"][:8])))
    print()
    print("isolated:", ["%s %.3f" % (l, v) for l, v in isolated])
    print("wrote best_counterparts.json/.md, cluster_by_language.md, "
          "aggregates.json")


if __name__ == "__main__":
    main()
