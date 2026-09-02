#!/usr/bin/env python3
"""Step-4 cross-reference: clusters at t=0.40 vs the intentions vocabulary.
Run inside Research/kind_signature_clustering. Writes basis_xref_out.json (scratch).
Vocabulary: super-node/sub-node/co-node/sub-tree only.
"""
import json, os, re, sys
import numpy as np
from scipy.cluster.hierarchy import fcluster

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spectrum_all import load_spectrum_all

T = 0.40

feats = json.load(open(os.path.join(HERE, "features_all.json")))["vectors"]
arch = json.load(open(os.path.join(HERE, "archetypes.json")))
labels, mult, Z, _ = load_spectrum_all()
n = len(labels)
assign = fcluster(Z, t=T, criterion="distance")

# ---- band per cluster: birth = top internal merge height, death = height
# of the merge that dissolves the cluster into a bigger one.
idx = {h: i for i, h in enumerate(labels)}
# build node membership: for each linkage node, the set id
# compute for each archetype leaf its cluster id; then for each cluster,
# find the maximal tree node whose leaves == cluster members.
# Simpler: walk Z; track cluster-of-leaves for each node; a node is "the"
# cluster node if all leaves share one cluster id and its super-node does not.
leaf_cluster = assign  # 1-based ids
node_cluster = {}      # tree node -> cluster id or None(mixed)
node_height = {}
node_leaves = {}
for i in range(n):
    node_cluster[i] = int(leaf_cluster[i]); node_height[i] = 0.0
super_of = {}
for k, (a, b, h, s) in enumerate(Z):
    nid = n + k
    a, b = int(a), int(b)
    super_of[a] = (nid, h); super_of[b] = (nid, h)
    ca, cb = node_cluster[a], node_cluster[b]
    node_cluster[nid] = ca if (ca == cb and ca is not None) else None
    node_height[nid] = h
band = {}   # cluster id -> (birth, death)
for node, c in node_cluster.items():
    if c is None: continue
    sup = super_of.get(node)
    if sup is None or node_cluster[sup[0]] != c:
        death = sup[1] if sup else 1.0
        band[c] = (node_height[node], death)

clusters = {}
for i, c in enumerate(assign):
    clusters.setdefault(int(c), []).append(i)

def cluster_info(c):
    ais = clusters[c]
    members = []
    for i in ais:
        members += arch[labels[i]]["members"]
    langs = sorted({m.split(":", 1)[0] for m in members})
    cats = {}
    for i in ais:
        for k, v in arch[labels[i]].get("categories", {}).items():
            cats[k] = cats.get(k, 0) + v
    b = band.get(c, (0.0, T))
    return {"id": c, "kinds": len(members), "langs": len(langs),
            "lang_list": langs, "members": members, "cats": cats,
            "band": [round(b[0], 3), round(b[1], 3)],
            "width": round(b[1] - b[0], 3),
            "n_arch": len(ais), "arch_idx": ais}

infos = {c: cluster_info(c) for c in clusters}

# ---- bucket name patterns (each an interpretation decision; numbered in report)
PAT = {
 "value": r"literal|number|integer|float|string(?!_interp)|bool|char|true|false|null|nil|none$",
 "name": r"identifier$|^name$|_name$|variable$|path$",
 "operation": r"binary|unary|operator|arith|comparison|logical|cast",
 "sequence": r"^block$|statement_list|compound_statement|^body$|_body$|declaration_list|sequence|source_file|program$",
 "choice": r"^if|_if$|else|conditional|ternary|elif|elsif|unless",
 "repetition": r"while|^for|for_|loop|repeat|do_statement|break|continue|each",
 "function": r"function|method|lambda|closure|call|parameter|argument|return|proc|def$|arrow",
 "record": r"struct|class|field|record|enum|interface_body|object|property",
 "collection": r"array|list(?!_comprehension)|dict|map|tuple|set_|index|subscript|slice|element",
 "mutation": r"assign|augmented|update_expression|increment|decrement",
 "service call": r"extern|foreign|ffi|syscall|asm",
 "A suspension": r"async|await|yield|generator|coroutine|suspend",
 "B channels": r"channel|select_statement|send_statement|go_statement|isolate|actor",
 "C optionals": r"optional|nullable|null_(?!literal)|option_|elvis|safe_navigation|non_null",
 "D pattern matching": r"match|pattern|^case|case_|switch|when_|destructur",
 "E dispatch": r"trait|interface|protocol|impl(?!ort)|implements|extends|virtual",
 "F generics": r"generic|type_parameter|type_argument|template|where_clause|bound|constraint",
 "G scoped cleanup": r"defer|using_|with_statement|finally|ensure|resource|drop",
 "H events": r"event|delegate|signal_|listener|callback|stream",
 "I operator overloading": r"operator_(declaration|definition|function|overload)",
 "J metaprogramming": r"macro|annotation|attribute|decorator|reflect|preproc|pragma|directive|quote|splice",
 "type-form": r"_type$|^type_identifier|primitive_type|type_annotation|predefined_type",
 "declarative-form": r"comment|modifier|visibility|shebang|doc_",
 "proof-form": r"lifetime|borrow|reference_type|ownership|mutable_specifier|ref_",
}

def kindname(m): return m.split(":", 1)[1]

bucket_hits = {}
for bucket, pat in PAT.items():
    rx = re.compile(pat)
    rows = []
    for c, info in infos.items():
        hits = [m for m in info["members"] if rx.search(kindname(m))]
        if not hits: continue
        frac = len(hits) / info["kinds"]
        if len(hits) >= 5 and frac >= 0.4 and info["langs"] >= 5:
            rows.append({**{k: info[k] for k in
                            ("id", "kinds", "langs", "band", "width", "cats", "n_arch")},
                         "match_frac": round(frac, 3),
                         "sample": sorted(hits)[:8]})
    rows.sort(key=lambda r: -r["langs"])
    bucket_hits[bucket] = rows[:6]

# ---- structural (role) evidence per bucket: which role features dominate
def role_profile(c):
    prof = {}
    for i in infos[c]["arch_idx"]:
        for e in feats[labels[i]]:
            if e.startswith("out:") or ":pos:" in e:
                key = e
                prof[key] = prof.get(key, 0) + arch[labels[i]]["size"]
    return sorted(prof.items(), key=lambda kv: -kv[1])[:12]

role_ev = {b: (role_profile(rows[0]["id"]) if rows else [])
           for b, rows in bucket_hits.items()}

# ---- missing vocabulary: many-language clusters with low match to all patterns
allrx = [re.compile(p) for p in PAT.values()]
missing = []
for c, info in infos.items():
    if info["langs"] < 10 or info["kinds"] < 20: continue
    matched = sum(1 for m in info["members"]
                  if any(r.search(kindname(m)) for r in allrx))
    frac = matched / info["kinds"]
    if frac < 0.5:
        from collections import Counter
        names = Counter(re.sub(r"\d+$", "", kindname(m)) for m in info["members"])
        missing.append({**{k: info[k] for k in
                           ("id", "kinds", "langs", "band", "width", "cats")},
                        "match_frac": round(frac, 3),
                        "top_names": names.most_common(10)})
missing.sort(key=lambda r: (-r["langs"], -r["kinds"]))

# ---- the 12 targets
TARGETS = ["python", "typescript__typescript", "java", "c-sharp", "go",
           "rust", "ruby", "php__php", "kotlin", "cpp", "dart", "swift"]
langs_present = sorted({m.split(":", 1)[0] for a in arch.values()
                        for m in a["members"]})
target_report = {}
kind_cluster = {}
for c, info in infos.items():
    for m in info["members"]:
        kind_cluster[m] = c
for lg in langs_present:
    if lg not in TARGETS: continue
    kinds = [m for m in kind_cluster if m.startswith(lg + ":")]
    ge10 = [m for m in kinds if infos[kind_cluster[m]]["langs"] >= 10]
    iso = [m for m in kinds if infos[kind_cluster[m]]["langs"] <= 2]
    target_report[lg] = {
        "n_kinds": len(kinds),
        "frac_ge10": round(len(ge10) / len(kinds), 3) if kinds else None,
        "frac_iso": round(len(iso) / len(kinds), 3) if kinds else None,
        "iso_examples": sorted(iso)[:25]}

# kotlin detail: where its kinds land, biggest few clusters
kot = {}
for m, c in kind_cluster.items():
    if m.startswith("kotlin:"):
        kot.setdefault(c, []).append(kindname(m))
kot_detail = sorted(
    [{"cluster": c, "cluster_langs": infos[c]["langs"],
      "cluster_kinds": infos[c]["kinds"], "band": infos[c]["band"],
      "kotlin_kinds": sorted(v)} for c, v in kot.items()],
    key=lambda r: -len(r["kotlin_kinds"]))

out = {"threshold": T, "n_clusters": len(clusters),
       "targets_present": sorted(target_report),
       "langs_present_sample": [l for l in langs_present if l[0] in "ckd"][:40],
       "bucket_hits": bucket_hits, "role_evidence": role_ev,
       "missing": missing[:30], "target_report": target_report,
       "kotlin_detail": kot_detail}
json.dump(out, open(os.path.join(HERE, "basis_xref_out.json"), "w"), indent=1)
print("clusters:", len(clusters), "targets:", sorted(target_report))
