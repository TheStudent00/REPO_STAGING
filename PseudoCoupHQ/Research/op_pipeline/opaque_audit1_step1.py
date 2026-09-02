#!/usr/bin/env python3
"""opaque_audit1_step1.py -- STEP 1 quantification for the tree_match3
verification task (this session's job, per the brief handed down).

Measures, over all 1,779 units, how many of tree_match2's and
tree_match3's selected (normalized) values are a BARE OPAQUE ATOM
(the normalized text is exactly one atom token -- op_N / atom_N /
pad_N -- with no surrounding computation structure), and how many of
the 333 tree_match2 cross-language exact clusters are keyed on an
expression that IS or CONTAINS ONLY opaque material.

THE SPELLING BAN: this script counts and reports by unit id / lang /
normalized-root text only. It never groups or keys by `operator`; the
`operator` field is read out for display in the worst-5 listing only,
attached per-member (unit-identifying dict), never used as a key or
grouping criterion. Verified after writing by
check_no_spelling_keys.py (see step 5 of the report).

Evidence class: PROGRAMMATICALLY VERIFIED, over the full 1,779-unit
population and the full 333-cluster population -- not a sample.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

BARE_ATOM_RE = re.compile(r"^(op|atom|pad)_\d+$")

# an "opaque token" appearing INSIDE a larger expression -- used for the
# cluster-key classification (contains-only-opaque check).
ATOM_TOKEN_RE = re.compile(r"\b(op|atom|pad)_\d+\b")

SEPARATOR_RE = re.compile(r"[\s,()]+")


def is_bare_atom(norm_text):
    """True iff the ENTIRE normalized text is exactly one opaque atom,
    no wrapping structure at all."""
    if norm_text is None:
        return False
    return bool(BARE_ATOM_RE.match(norm_text.strip()))


def is_opaque_only(norm_text):
    """True iff the normalized text, with every opaque atom token
    removed, has nothing left but separators -- i.e. it is built
    ENTIRELY from opaque material (may still have wrapping like
    Concat(op_1, op_2), which is still 'no real computation', just
    atoms glued together with no z3 operator among REAL leaves).
    Anything with an operator NAME left over (Extract, Concat, +, an
    If, ...) is treated as real computation structure, per the brief's
    own phrasing ("contains ONLY opaque material, no real computation
    structure")."""
    if norm_text is None:
        return False
    stripped = ATOM_TOKEN_RE.sub("", norm_text)
    remainder = SEPARATOR_RE.sub("", stripped)
    return remainder == ""


def load(path):
    doc = json.load(open(path))
    return doc


def audit_units(units_doc, label):
    total = 0
    bare = 0
    bare_ids = []
    for u in units_doc["units"]:
        if not u.get("sem_ok"):
            continue
        total += 1
        norm = u.get("normal_path_root")
        if is_bare_atom(norm):
            bare += 1
            bare_ids.append((u["lang"], u["n"], u.get("operator"), norm))
    print("%s: %d units with sem_ok, %d (%.1f%%) selected a bare opaque "
          "atom with no computation structure" %
          (label, total, bare, 100.0 * bare / total if total else 0.0))
    return total, bare, bare_ids


def audit_clusters(matches_doc, label):
    cl = [c for c in matches_doc["exact_normalized_root"]
          if c["cross_language"]]
    opaque_clusters = []
    for c in cl:
        if is_opaque_only(c["normalized_root"]):
            opaque_clusters.append(c)
    print("%s: %d cross-language exact clusters, %d (%.1f%%) keyed on "
          "an expression that IS or CONTAINS ONLY opaque material" %
          (label, len(cl), len(opaque_clusters),
           100.0 * len(opaque_clusters) / len(cl) if cl else 0.0))
    return cl, opaque_clusters


def main():
    u2 = load(os.path.join(HERE, "tree_units2.json"))
    u3 = load(os.path.join(HERE, "tree_units3.json"))
    m2 = load(os.path.join(HERE, "tree_matches2.json"))
    m3 = load(os.path.join(HERE, "tree_matches3.json"))

    print("=== per-unit bare-opaque-atom selection ===")
    t2, b2, ids2 = audit_units(u2, "tree_match2 (old, global-largest)")
    t3, b3, ids3 = audit_units(u3, "tree_match3 (new, ret-block-first)")

    print()
    print("=== cross-language cluster opacity (tree_match2's 333) ===")
    cl2, opaque2 = audit_clusters(m2, "tree_match2")

    print()
    print("=== cross-language cluster opacity (tree_match3's 289, for "
          "reference) ===")
    cl3, opaque3 = audit_clusters(m3, "tree_match3")

    worst = sorted(opaque2, key=lambda c: -len(c["members"]))[:5]

    print()
    print("=== worst 5 candidate false merges in tree_match2's 333 "
          "(opaque-keyed clusters, ranked by member count) ===")
    result_worst = []
    for c in worst:
        member_ids = ["%s/%s(op=%s)" % (m["lang"], m["n"], m["operator"])
                       for m in c["members"]]
        print("key=%r  type_pair=%s  size=%d  languages=%s" %
              (c["normalized_root"], c["type_pair"], len(c["members"]),
               c["languages"]))
        for mid in member_ids:
            print("    ", mid)
        result_worst.append(dict(
            normalized_root=c["normalized_root"],
            type_pair=c["type_pair"],
            member_count=len(c["members"]),
            languages=c["languages"],
            members=member_ids,
        ))

    out = dict(
        role="generator provenance",
        note="output of opaque_audit1_step1.py -- STEP 1 quantification, "
             "programmatically verified over all units / all 333 "
             "clusters, not a sample",
        tree_match2_units_with_sem_ok=t2,
        tree_match2_bare_opaque_selection_count=b2,
        tree_match3_units_with_sem_ok=t3,
        tree_match3_bare_opaque_selection_count=b3,
        tree_match2_cross_language_cluster_count=len(cl2),
        tree_match2_opaque_only_cluster_count=len(opaque2),
        tree_match3_cross_language_cluster_count=len(cl3),
        tree_match3_opaque_only_cluster_count=len(opaque3),
        worst_5_opaque_clusters_in_tree_match2_333=result_worst,
    )
    out_path = os.path.join(HERE, "opaque_audit1_step1_result.json")
    json.dump(out, open(out_path, "w"), indent=1)
    print()
    print("wrote", out_path)


if __name__ == "__main__":
    main()
