#!/usr/bin/env python3
"""validate_holdout.py — the owner's ruling 2a (2026-08-12): full-population
hold-out validation against tree-sitter's OWN declarations.

Protocol: features were rebuilt WITHOUT declared supertype memberships
(features.py --hold-out-declared) and the merge-tree spectrum re-derived
from them (similarity_matrix_holdout.npz). This script then measures, per
language and per declared supertype, how well the HELD-OUT similarities
separate within-supertype pairs from across-supertype pairs:

  - mean within  : mean spectrum similarity over pairs of kinds both
                   declared members of the supertype (same language);
  - mean across  : mean similarity over pairs (member, non-member) of the
                   same language;
  - AUC          : Mann-Whitney rank statistic — probability that a random
                   within pair is more similar than a random across pair
                   (0.5 = no signal, 1.0 = perfect separation).

This is a REFERENCE FRAME, not an oracle (the owner's words): tree-sitter does
not know cross-language truths, and its supertypes are per-language design
choices. Agreement is reported as evidence, not as a score to maximize.

The 15-row hand key from validate.py is kept as a SECONDARY check only,
clearly labeled hand-picked: mean within-row similarity vs the background
mean over all cross-language pairs.

Output: holdout_validation.json + printed pipe tables.
Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""
import json
import os
import numpy as np

import spectrum
from validate import GROUND_TRUTH

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LANGS = ["rust", "python", "dart", "c", "cpp"]


def declared_supertypes(lang):
    data = json.load(open(os.path.join(RAW, lang + ".node-types.json")))
    return {e["type"]: sorted(s["type"] for s in e.get("subtypes", []))
            for e in data if "subtypes" in e}


def auc(within, across):
    """Mann-Whitney AUC: P(random within pair > random across pair),
    ties counted half."""
    w = np.asarray(within)
    a = np.asarray(across)
    allv = np.concatenate([w, a])
    order = allv.argsort(kind="mergesort")
    ranks = np.empty(len(allv))
    ranks[order] = np.arange(1, len(allv) + 1)
    # average ranks for ties
    vals, inv, cnt = np.unique(allv, return_inverse=True, return_counts=True)
    csum = np.cumsum(cnt)
    avg = (csum - (cnt - 1) / 2.0)
    ranks = avg[inv]
    u = ranks[:len(w)].sum() - len(w) * (len(w) + 1) / 2.0
    return u / (len(w) * len(a))


def main():
    import sys
    v2 = "--v2" in sys.argv  # decision-6 counts fix spectrum
    npz = "similarity_matrix_v2_holdout.npz" if v2 \
        else "similarity_matrix_holdout.npz"
    labels, Z, S = spectrum.load_spectrum(os.path.join(HERE, npz))
    idx = {l: i for i, l in enumerate(labels)}
    lang_idx = {lg: [i for i, l in enumerate(labels)
                     if l.startswith(lg + ":")] for lg in LANGS}

    out = {"per_supertype": [], "hand_key_secondary": {}}
    print("| language | supertype | n members | mean within | mean across "
          "| AUC |")
    print("|---|---|---|---|---|---|")
    for lg in LANGS:
        li = lang_idx[lg]
        for sup, subs in sorted(declared_supertypes(lg).items()):
            mem = [idx[lg + ":" + s] for s in subs if (lg + ":" + s) in idx]
            non = [i for i in li if i not in set(mem)]
            if len(mem) < 2:
                continue
            m = np.array(mem)
            within = S[np.ix_(m, m)][np.triu_indices(len(m), 1)]
            across = S[np.ix_(m, np.array(non))].ravel()
            row = {"language": lg, "supertype": sup, "n": len(mem),
                   "mean_within": round(float(within.mean()), 3),
                   "mean_across": round(float(across.mean()), 3),
                   "auc": round(float(auc(within, across)), 3)}
            out["per_supertype"].append(row)
            print("| %s | %s | %d | %.3f | %.3f | %.3f |" %
                  (lg, sup, len(mem), within.mean(), across.mean(),
                   row["auc"]))

    # Secondary check, HAND-PICKED 15-row key (kept per ruling 2, labeled).
    within_rows = []
    for row, members in GROUND_TRUTH.items():
        ids = [idx[m] for m in members if m in idx]
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                within_rows.append(S[ids[a], ids[b]])
    # background: all cross-language pairs
    cross = []
    for a, la in enumerate(labels):
        for lg in LANGS:
            pass
    lang_of = np.array([l.split(":")[0] for l in labels])
    iu = np.triu_indices(len(labels), 1)
    cross_mask = lang_of[iu[0]] != lang_of[iu[1]]
    bg = S[iu][cross_mask]
    out["hand_key_secondary"] = {
        "label": "HAND-PICKED 15-row key, secondary check only",
        "mean_within_row_similarity": round(float(np.mean(within_rows)), 3),
        "background_cross_language_mean": round(float(bg.mean()), 3),
        "auc_vs_background": round(float(auc(within_rows, bg)), 3),
    }
    print()
    print("hand-picked 15-row key (secondary): mean within-row sim %.3f vs "
          "background cross-language mean %.3f, AUC %.3f" %
          (np.mean(within_rows), bg.mean(),
           out["hand_key_secondary"]["auc_vs_background"]))

    oname = "holdout_validation_v2.json" if v2 else "holdout_validation.json"
    with open(os.path.join(HERE, oname), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", oname)


if __name__ == "__main__":
    main()
