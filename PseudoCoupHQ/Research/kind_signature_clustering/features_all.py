#!/usr/bin/env python3
"""features_all.py — archetype measurement over ALL fetched grammars.

Answers the owner's question (log_013): "is the cardinality of all potential
vectors so great that we cannot simplify the pair-wise comparisons? ...
I would imagine that 411 information sources would create a lot of
identical vectors or present other computational shortcuts."

For every grammar in raw_all/ (inventory: grammar_inventory.json), build
counts-fixed (v2, decision-6 fix) feature vectors for every named kind
using features.build_features UNCHANGED, canonicalize each vector by a
stable hash, and measure deduplication.

Canonical hash: sha1 over the JSON of the feature dict with sorted keys
and weights rendered via repr — identical feature sets (elements AND
weights) collapse to one archetype; nothing else does.

Outputs (both under this directory):
  features_all.json — COMPACT format (documented sub-decision: ~31k kinds
    with full per-kind vectors would run ~100 MB of redundant JSON; the
    archetype table stores every distinct vector ONCE):
      {"format": ..., "n_kinds": N, "n_archetypes": A,
       "vectors": {hash: {element: weight}},
       "members": {grammar: {kind: hash}}}
    Every kind's full vector is recoverable as vectors[members[g][k]].
  archetypes.json — archetype -> member list plus size/category summary:
      {hash: {"size": n, "categories": {cat: n}, "members": ["g:kind", ...]}}

Vocabulary: super-node / sub-node / co-node / sub-tree only; third-party
JSON keys in backticks only.
"""
import collections
import hashlib
import json
import os
import sys

import features

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_ALL = os.path.join(HERE, "raw_all")

features.V2_COUNTS = True  # counts-fixed vectors (decision-6 fix)

# --hold-out-declared (step-3 validation at scale, mirrors features.py's
# flag): drop declared supertype MEMBERSHIPS at the source so the grammars'
# own declarations can serve as held-out validation targets. Writes
# features_all_holdout.json / archetypes_holdout.json; main outputs untouched.
HOLD_OUT = "--hold-out-declared" in sys.argv
if HOLD_OUT:
    features.HOLD_OUT_DECLARED = True
SUFFIX = "_holdout" if HOLD_OUT else ""


def canon(feats):
    s = json.dumps({k: repr(v) for k, v in sorted(feats.items())},
                   sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(s.encode()).hexdigest()[:16]


def main():
    inv = json.load(open(os.path.join(HERE, "grammar_inventory.json")))
    cat_of = {}
    for entry in inv:
        for g in entry.get("grammars", []):
            cat_of[g["file"]] = entry.get("category", "unknown")

    vectors = {}
    members = {}
    arch_members = collections.defaultdict(list)
    n_kinds = 0
    failed = []
    files = sorted(os.listdir(RAW_ALL))
    for fn in files:
        if not fn.endswith(".node-types.json"):
            continue
        gname = fn[:-len(".node-types.json")]
        try:
            data = json.load(open(os.path.join(RAW_ALL, fn)))
            built = features.build_features(data)
        except Exception as e:  # report, never silently drop
            failed.append((fn, repr(e)))
            continue
        members[gname] = {}
        for kind, rec in built.items():
            h = canon(rec["features"])
            vectors.setdefault(h, rec["features"])
            members[gname][kind] = h
            arch_members[h].append(gname + ":" + kind)
            n_kinds += 1

    out = {"format": "see module docstring; vectors[hash] holds each "
                     "distinct v2 feature vector once; members[grammar]"
                     "[kind] -> hash",
           "feature_version": "v2 (decision-6 counts fix, log2 buckets)",
           "n_grammars": len(members), "n_kinds": n_kinds,
           "n_archetypes": len(vectors),
           "failed": failed,
           "vectors": vectors, "members": members}
    with open(os.path.join(HERE, "features_all%s.json" % SUFFIX), "w") as f:
        json.dump(out, f, separators=(",", ":"), sort_keys=True)

    arch = {}
    for h, mem in arch_members.items():
        cats = collections.Counter(cat_of.get(m.split(":")[0] +
                                              ".node-types.json", "unknown")
                                   for m in mem)
        arch[h] = {"size": len(mem), "categories": dict(cats),
                   "members": sorted(mem)}
    with open(os.path.join(HERE, "archetypes%s.json" % SUFFIX), "w") as f:
        json.dump(arch, f, separators=(",", ":"), sort_keys=True)

    # ---- measurement report ----
    print("grammars: %d   kinds: %d   archetypes: %d   dedup ratio: %.2fx"
          % (len(members), n_kinds, len(vectors), n_kinds / len(vectors)))
    if failed:
        print("FAILED grammars:", failed)
    sizes = sorted((v["size"], h) for h, v in arch.items())
    singles = sum(1 for s, _ in sizes if s == 1)
    print("singleton archetypes: %d (%.1f%%)" %
          (singles, 100.0 * singles / len(vectors)))
    print("\ntop 20 archetypes:")
    for s, h in sizes[-20:][::-1]:
        v = arch[h]
        ex = ", ".join(v["members"][:6])
        print("  size %5d  cats %s  e.g. %s" % (s, v["categories"], ex))

    # per-category dedup
    cat_kinds = collections.Counter()
    cat_arch = collections.defaultdict(set)
    for g, kk in members.items():
        c = cat_of.get(g + ".node-types.json", "unknown")
        for kind, h in kk.items():
            cat_kinds[c] += 1
            cat_arch[c].add(h)
    print("\nper-category dedup:")
    for c in sorted(cat_kinds):
        print("  %-16s kinds %6d  archetypes %6d  ratio %.2fx" %
              (c, cat_kinds[c], len(cat_arch[c]),
               cat_kinds[c] / len(cat_arch[c])))

    n, a = n_kinds, len(vectors)
    print("\npairwise matrix: kinds %d -> %s pairs; archetypes %d -> %s "
          "pairs (%.1fx fewer)" %
          (n, "{:,}".format(n * (n - 1) // 2), a,
           "{:,}".format(a * (a - 1) // 2),
           (n * (n - 1)) / max(1, a * (a - 1))))


if __name__ == "__main__":
    main()
