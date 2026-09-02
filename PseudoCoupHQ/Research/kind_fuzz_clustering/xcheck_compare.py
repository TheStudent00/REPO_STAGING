#!/usr/bin/env python3
"""xcheck_compare.py — CHECK item 4j, the comparison itself.

Reads xcheck_mapping.json (the mapping, built by xcheck_signature.py)
plus both sources' cluster artifacts, builds a SIGNATURE tree over
exactly the mapped leaves, and compares it against the BEHAVIOUR tree
at MATCHED cluster counts across the whole sweep.

Products: xcheck_signature.json, xcheck_sigdist_<population>.json.
"""
import json
import os
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
SIG = os.path.join(os.path.dirname(HERE), "kind_signature_clustering")
GRAMMAR = {
    "go": "go", "rust": "rust", "cpp": "cpp", "csharp": "c-sharp",
    "java": "java", "kotlin": "kotlin", "swift": "swift", "dart": "dart",
    "typescript": "typescript__typescript", "python": "python",
    "ruby": "ruby", "php": "php__php",
}
# the behaviour side's own widest stability plateau, per artifact
REFERENCE_K = {"operators": 21, "constructs": 12}


def wjac(a, b):
    inter = 0.0
    for e, w in a.items():
        if e in b:
            inter += max(w, b[e])
    union = sum(a.values()) + sum(b.values()) - inter
    return 1.0 - inter / union if union > 0 else 1.0


def upgma(D, n):
    act = {i: [i] for i in range(n)}
    dist = {}
    for i in range(n):
        for j in range(i + 1, n):
            dist[(i, j)] = D[i][j]

    def g(a, b):
        return dist[(a, b)] if a < b else dist[(b, a)]
    merges = []
    nxt = n
    while len(act) > 1:
        ks = sorted(act)
        best = None
        for x in range(len(ks)):
            for y in range(x + 1, len(ks)):
                v = g(ks[x], ks[y])
                if best is None or v < best[0]:
                    best = (v, ks[x], ks[y])
        v, a, b = best
        ma, mb = act.pop(a), act.pop(b)
        for c in list(act):
            da = g(a, c) if a != c else 0.0
            db = g(b, c) if b != c else 0.0
            dist[(min(nxt, c), max(nxt, c))] = (
                (len(ma) * da + len(mb) * db) / (len(ma) + len(mb)))
        act[nxt] = ma + mb
        merges.append((v, a, b, nxt))
        nxt += 1
    return merges


def partition_at_k(merges, n, k):
    parent = list(range(n + len(merges)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i, (v, a, b, nw) in enumerate(merges):
        if i >= n - k:
            break
        parent[find(a)] = nw
        parent[find(b)] = nw
        parent[nw] = nw
    return [find(i) for i in range(n)]


def pair_stats(pa, pb, idx):
    tt = ta = at = aa = 0
    for x in range(len(idx)):
        for y in range(x + 1, len(idx)):
            i, j = idx[x], idx[y]
            a, b = pa[i] == pa[j], pb[i] == pb[j]
            if a and b:
                tt += 1
            elif a:
                ta += 1
            elif b:
                at += 1
            else:
                aa += 1
    tot = tt + ta + at + aa
    return dict(n_pairs=tot, both_together=tt, both_apart=aa,
                sig_together_behaviour_apart=ta,
                behaviour_together_sig_apart=at,
                agreement=round((tt + aa) / tot, 4) if tot else None)


def ari(pa, pb, idx):
    ca = collections.Counter(pa[i] for i in idx)
    cb = collections.Counter(pb[i] for i in idx)
    cc = collections.Counter((pa[i], pb[i]) for i in idx)

    def c2(x):
        return x * (x - 1) / 2
    sij = sum(c2(v) for v in cc.values())
    sa = sum(c2(v) for v in ca.values())
    sb = sum(c2(v) for v in cb.values())
    n = len(idx)
    exp = sa * sb / c2(n)
    mx = (sa + sb) / 2
    return round((sij - exp) / (mx - exp), 4) if mx != exp else 1.0


def main():
    mp = json.load(open(os.path.join(HERE, "xcheck_mapping.json")))
    feats = json.load(open(os.path.join(SIG, "features_all.json")))
    members, vectors = feats["members"], feats["vectors"]
    hosts, fam = mp["hosts"], mp["family"]

    docs = {
        "operators": json.load(open(os.path.join(HERE,
                                                 "clusters_all12.json"))),
        "constructs": json.load(open(os.path.join(
            HERE, "clusters_constructs.json"))),
    }
    out = {"built": "2026-08-20", "check_item": "4j",
           "mapping_report": mp["report"], "populations": {}}

    for popname, doc in docs.items():
        names = sorted(k for k in doc["signatures"]
                       if k not in set(doc.get("empty_domain") or []))
        n = len(names)
        assert n == doc["n_leaves"]
        # leaf-order verification against the artifact's own member lists
        lab = {i: [names[i]] for i in range(n)}
        checked = 0
        for h in doc["merge_history"]:
            mm = lab[h["left"]["id"]] + lab[h["right"]["id"]]
            lab[h["node"]] = mm
            if "members" in h:
                assert sorted(h["members"]) == sorted(mm), h["node"]
                checked += 1
        bmerges = [(1.0 - h["similarity"], h["left"]["id"], h["right"]["id"],
                    h["node"]) for h in doc["merge_history"]]

        kn = [nm for nm in names if nm in hosts]
        m = len(kn)
        vecs = [[vectors[members[GRAMMAR[nm.split('.')[0]]][h]]
                 for h in hosts[nm]] for nm in kn]
        D = [[0.0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                D[i][j] = D[j][i] = min(wjac(a, b)
                                        for a in vecs[i] for b in vecs[j])
        smerges = upgma(D, m)

        classes = collections.defaultdict(list)
        for i, nm in enumerate(kn):
            classes[tuple(sorted(hosts[nm]))].append(nm)
        zero = [(kn[i], kn[j]) for i in range(m) for j in range(i + 1, m)
                if D[i][j] == 0.0]
        zero_same = [p for p in zero
                     if p[0].split(".")[0] == p[1].split(".")[0]]

        # ---- the full matched-K sweep ---------------------------------
        curve = []
        for k in range(2, m):
            pbf = partition_at_k(bmerges, n, k)
            pb = {names[i]: pbf[i] for i in range(n)}
            psf = partition_at_k(smerges, m, k)
            ps = {kn[i]: psf[i] for i in range(m)}
            pa = [ps[x] for x in kn]
            pv = [pb[x] for x in kn]
            idx = list(range(m))
            st = pair_stats(pa, pv, idx)
            st["k"] = k
            st["ari"] = ari(pa, pv, idx)
            curve.append(st)
        best = max(curve, key=lambda r: r["ari"])

        # ---- the reference cut: the behaviour side's widest plateau ----
        ref = REFERENCE_K[popname]
        pbf = partition_at_k(bmerges, n, ref)
        pb = {names[i]: pbf[i] for i in range(n)}
        psf = partition_at_k(smerges, m, ref)
        ps = {kn[i]: psf[i] for i in range(m)}
        pa = [ps[x] for x in kn]
        pv = [pb[x] for x in kn]
        byfam = collections.defaultdict(list)
        for i, nm in enumerate(kn):
            byfam[fam[nm]].append(i)
        famrows = {}
        for f, ii in sorted(byfam.items()):
            if len(ii) < 2:
                continue
            r = pair_stats(pa, pv, ii)
            r["n_leaves"] = len(ii)
            r["ari"] = ari(pa, pv, ii)
            famrows[f] = r
        overall = pair_stats(pa, pv, list(range(m)))
        overall["ari"] = ari(pa, pv, list(range(m)))
        overall["n_leaves"] = m

        # ---- permutation null: shuffle the signature labels ------------
        import random
        rng = random.Random(7)
        obs = overall["ari"]
        null = []
        for _ in range(2000):
            q = pa[:]
            rng.shuffle(q)
            null.append(ari(q, pv, list(range(m))))
        null.sort()
        nullrow = {
            "draws": len(null),
            "mean": round(sum(null) / len(null), 6),
            "p95": round(null[int(0.95 * len(null))], 4),
            "p99": round(null[int(0.99 * len(null))], 4),
            "max": round(null[-1], 4),
            "observed": obs,
            "p_value": sum(1 for r in null if r >= obs) / len(null),
        }

        typeA, typeB = [], []
        for i in range(m):
            for j in range(i + 1, m):
                a, b = pa[i] == pa[j], pv[i] == pv[j]
                if a and not b:
                    typeA.append({"pair": [kn[i], kn[j]],
                                  "sig_distance": round(D[i][j], 6),
                                  "hosts": [hosts[kn[i]], hosts[kn[j]]],
                                  "class": ("blind-same-declaration"
                                            if D[i][j] == 0.0
                                            else "near-declaration")})
                elif b and not a:
                    typeB.append({"pair": [kn[i], kn[j]],
                                  "sig_distance": round(D[i][j], 6),
                                  "hosts": [hosts[kn[i]], hosts[kn[j]]]})

        out["populations"][popname] = {
            "behaviour_leaves": n,
            "mapped_leaves": m,
            "leaf_order_merges_verified": checked,
            "unmapped_leaves": sorted(set(names) - set(kn)),
            "signature_resolution_classes": len(classes),
            "largest_signature_class": max(
                (len(v), k[0] if k else "") for k, v in classes.items()),
            "signature_zero_distance_pairs": len(zero),
            "signature_zero_distance_pairs_same_language": len(zero_same),
            "total_pairs": m * (m - 1) // 2,
            "reference_k": ref,
            "reference_overall": overall,
            "reference_families": famrows,
            "permutation_null": nullrow,
            "best_ari": best,
            "sweep": [{"k": r["k"], "agreement": r["agreement"],
                       "ari": r["ari"]} for r in curve],
            "type_a_count": len(typeA),
            "type_a_blind": sum(1 for t in typeA
                                if t["class"] == "blind-same-declaration"),
            "type_a": typeA,
            "type_b_count": len(typeB),
            "type_b": typeB,
        }
        json.dump({"leaves": kn, "D": [[round(x, 6) for x in r] for r in D]},
                  open(os.path.join(HERE,
                                    "xcheck_sigdist_%s.json" % popname), "w"))

    json.dump(out, open(os.path.join(HERE, "xcheck_signature.json"), "w"),
              indent=1)
    for p, v in out["populations"].items():
        print(p, v["mapped_leaves"], "of", v["behaviour_leaves"],
              "| sig classes", v["signature_resolution_classes"],
              "| ref k", v["reference_k"],
              "agree", v["reference_overall"]["agreement"],
              "ari", v["reference_overall"]["ari"],
              "| bestARI", v["best_ari"]["k"], v["best_ari"]["ari"],
              "| null p", v["permutation_null"]["p_value"],
              "| A", v["type_a_count"], "(blind", v["type_a_blind"], ")",
              "B", v["type_b_count"])
        for f, r in v["reference_families"].items():
            print("    %-11s n=%-3d agree %.4f  A=%-5d B=%-5d" %
                  (f, r["n_leaves"], r["agreement"],
                   r["sig_together_behaviour_apart"],
                   r["behaviour_together_sig_apart"]))


if __name__ == "__main__":
    main()
