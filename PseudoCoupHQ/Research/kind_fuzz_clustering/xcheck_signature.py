#!/usr/bin/env python3
"""xcheck_signature.py — CHECK item 4j.

Cross-check the MEASURED-BEHAVIOR clusters of kind_fuzz_clustering
against the DECLARED-SIGNATURE clusters of kind_signature_clustering.

Neither source wins by default. Everything that cannot be mapped is
counted and named rather than dropped.

Products: xcheck_signature.json (the whole comparison).
"""
import json
import os
import sys
import collections
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))
SIG = os.path.join(os.path.dirname(HERE), "kind_signature_clustering")

# --- decision 1: the twelve target languages and their grammar ids ----
GRAMMAR = {
    "go": "go", "rust": "rust", "cpp": "cpp", "csharp": "c-sharp",
    "java": "java", "kotlin": "kotlin", "swift": "swift", "dart": "dart",
    "typescript": "typescript__typescript", "python": "python",
    "ruby": "ruby", "php": "php__php",
}

# --- decision 9: family of an operator spelling -----------------------
ARITH = set("+ - * / % ** // @".split())
CMP = set("== != < <= > >= <=> === !== is is_not eq ne".split()) | {
    "is not", "not_eq", "instanceof", "in", "is", "as"}
LOGIC = {"&&", "||", "!", "and", "or", "not", "xor", "??", "?:"}
SHIFT = {"<<", ">>", ">>>", "<<<", ">>=", "<<="}
BITS = {"&", "|", "^", "&^", "bitand", "bitor"}


def family(op):
    if op.startswith("Kaccess."):
        return "access"
    if op.startswith("Kflow."):
        return "flow"
    if op.startswith("Kbinding."):
        return "binding"
    if op in SHIFT:
        return "shift"
    if op in LOGIC:
        return "logical"
    if op in BITS:
        return "bitwise"
    if op in CMP:
        return "comparison"
    if op in ARITH:
        return "arithmetic"
    return "other"


# --- the signature side: features and weighted-Jaccard ----------------
def load_features():
    d = json.load(open(os.path.join(SIG, "features_all.json")))
    return d["members"], d["vectors"]


def wjac(a, b):
    """distance = 1 - shared weight / union weight (cluster.py formula)."""
    if not a or not b:
        return 1.0
    inter = 0.0
    for e, w in a.items():
        if e in b:
            inter += max(w, b[e])
    union = sum(a.values()) + sum(b.values()) - inter
    if union <= 0:
        return 1.0
    return 1.0 - inter / union


# --- the mapping ------------------------------------------------------
def operator_hosts(lang):
    """token -> sorted list of host kinds declaring it in an operator slot.

    decision 2: an operator token maps to the NAMED kind whose declared
    operator slot lists it, read off the grammar's own node-types data
    as phase 0 already flattened it into legal_pairs_<lang>.json.
    """
    p = os.path.join(HERE, "legal_pairs_%s.json" % lang)
    d = json.load(open(p))
    out = collections.defaultdict(set)
    for host, slot, filler, kind in d["declared_triples"]:
        if kind != "anon":
            continue
        if slot not in ("operator", "operators"):
            continue
        out[filler].add(host)
    return {k: sorted(v) for k, v in out.items()}


def construct_kind(lang, op, catalogue):
    """decision 4: a construct leaf carries its role; the catalogue
    already resolved role -> declared kind, so no name is guessed."""
    fam, role = op.split(".", 1)
    fam = fam[1:].lower()            # Kflow -> flow
    role = role.split("*")[0]
    for suffix in ("+=", "-=", "*=", "/=", "%="):
        if role.endswith(suffix):
            role = role[: -len(suffix)]
    entry = catalogue.get(lang, {}).get(fam, {}).get(role)
    if not entry or not entry.get("present"):
        return None
    return [entry["kind"]]


def main():
    members, vectors = load_features()
    catalogue = json.load(open(os.path.join(HERE, "construct_catalogue.json")))
    ops_cl = json.load(open(os.path.join(HERE, "clusters_all12.json")))
    con_cl = json.load(open(os.path.join(HERE, "clusters_constructs.json")))

    hosts = {L: operator_hosts(L) for L in GRAMMAR}

    report = {"decisions": [], "populations": {}, "unmapped": {}}

    def build(pop_name, cluster_doc, is_construct):
        leaves = [m for h in cluster_doc["merge_history"]
                  for m in ([] )]  # placeholder
        # leaf ids: reconstruct from merge_history leaf ids + signatures
        sigs = cluster_doc["signatures"]
        names = sorted(k for k, v in sigs.items()
                       if k not in cluster_doc.get("empty_domain", []))
        return names

    # ---- leaf name lists, exactly as the artifacts hold them ----------
    def leaf_names(doc):
        """leaf id -> name, recovered from the merge history's members."""
        n = doc["n_leaves"]
        name_of = {}
        for m in doc["merge_history"]:
            if "members" in m and m["size"] == len(m["members"]):
                pass
        return n

    # merge_history in clusters_all12 carries member names; constructs do
    # not, so leaf ids come from the sorted signature order both files
    # were built from.
    def leaves_of(doc, empty_key="empty_domain"):
        sigs = doc["signatures"]
        empty = set(doc.get(empty_key) or [])
        if isinstance(empty, dict):
            empty = set(empty)
        names = [k for k in sigs if k not in empty]
        # non-empty domain only, in the artifact's own sorted order
        return sorted(names)

    op_leaves = leaves_of(ops_cl)
    con_leaves = leaves_of(con_cl)

    # verify against the recorded leaf counts
    report["leaf_count_check"] = {
        "operators_recorded": ops_cl.get("n_leaves"),
        "operators_rebuilt": len(op_leaves),
        "constructs_recorded": con_cl.get("n_leaves"),
        "constructs_rebuilt": len(con_leaves),
    }

    # ---- map every leaf ----------------------------------------------
    mapping = {}
    unmapped = collections.defaultdict(list)
    for name in op_leaves:
        lang, op = name.split(".", 1)
        g = GRAMMAR[lang]
        hs = hosts[lang].get(op)
        if not hs:
            unmapped["operator_not_declared_in_any_operator_slot"].append(name)
            continue
        vecs = []
        missing = []
        for h in hs:
            hsh = members.get(g, {}).get(h)
            if hsh is None:
                missing.append(h)
            else:
                vecs.append((h, vectors[hsh]))
        if not vecs:
            unmapped["host_kind_absent_from_feature_population"].append(
                name + " -> " + ",".join(hs))
            continue
        mapping[name] = {"lang": lang, "op": op, "hosts": [h for h, _ in vecs],
                         "vecs": [v for _, v in vecs],
                         "dropped_hosts": missing,
                         "family": family(op), "population": "operator"}

    for name in con_leaves:
        lang, op = name.split(".", 1)
        g = GRAMMAR[lang]
        ks = construct_kind(lang, op, catalogue)
        if not ks:
            unmapped["construct_role_absent_from_catalogue"].append(name)
            continue
        vecs = []
        for h in ks:
            hsh = members.get(g, {}).get(h)
            if hsh is not None:
                vecs.append((h, vectors[hsh]))
        if not vecs:
            unmapped["host_kind_absent_from_feature_population"].append(
                name + " -> " + ",".join(ks))
            continue
        mapping[name] = {"lang": lang, "op": op, "hosts": [h for h, _ in vecs],
                         "vecs": [v for _, v in vecs], "dropped_hosts": [],
                         "family": family(op), "population": "construct"}

    report["unmapped"] = {k: sorted(v) for k, v in unmapped.items()}
    report["unmapped_counts"] = {k: len(v) for k, v in unmapped.items()}

    # ---- what the signature side has that the behavior side has not ---
    mapped_kinds = collections.defaultdict(set)
    for name, m in mapping.items():
        for h in m["hosts"]:
            mapped_kinds[m["lang"]].add(h)
    sig_only = {}
    for L, g in GRAMMAR.items():
        allk = set(members.get(g, {}))
        sig_only[L] = sorted(allk - mapped_kinds[L])
    report["signature_only_kinds_count"] = {L: len(v) for L, v in
                                            sig_only.items()}
    report["signature_only_kinds_total"] = sum(
        len(v) for v in sig_only.values())
    report["mapped_kind_count"] = {L: len(v) for L, v in mapped_kinds.items()}

    json.dump({"mapping_names": sorted(mapping),
               "report": report,
               "hosts": {n: m["hosts"] for n, m in mapping.items()},
               "family": {n: m["family"] for n, m in mapping.items()},
               "population": {n: m["population"] for n, m in mapping.items()},
               },
              open(os.path.join(HERE, "xcheck_mapping.json"), "w"), indent=1)

    print("mapped %d of %d leaves" % (len(mapping),
                                      len(op_leaves) + len(con_leaves)))
    print(json.dumps(report["unmapped_counts"], indent=1))
    print("sig-only kinds", report["signature_only_kinds_total"])


if __name__ == "__main__":
    main()
