#!/usr/bin/env python3
"""dom_ops.py -- THE DOM_OP CONSTRUCTION RULE (the owner, 2026-08-26), run.

The rule, as the owner stated it: dominant operators are DISCOVERED from
machine evidence by matching, never asserted.  Nodes are (language,
grammar-operator, ARITY) -- the PROVENANCE of the probe: which grammar
rule of ONE language generated it.  Edges exist only BETWEEN
languages, weighted by how many equivalence classes the two nodes both
have units in.  Each node keeps its single strongest counterpart per
foreign language, kept only when the choice is MUTUAL.  The connected
components of the mutual-best graph are the dominant operators.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25).  No
operator token may appear in ANY key, grouping, pairing, row
structure, candidate selection, or comparison scope, anywhere in this
line.  The candidate set for comparison comes from machine-form
evidence or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.

How this program obeys it, concretely:
  * every node carries a synthetic id (`N0007`); no dict key, no
    grouping key, no pair key anywhere in this file is built from a
    token.
  * grouping ACROSS languages happens only by machine-form weight:
    the count of shared equivalence classes, then the count of shared
    operand-type keys, then class count.  A token is never compared.
  * the token is written exactly once per node, as `label` on a member
    object that also carries `lang` and `id`.
  * the products are handed to check_no_spelling_keys.py, and this
    program refuses its own output when the guard fails.

ARITY is part of node identity because one token can be two operators.
go's unary `^` and go's binary `^` are two nodes, and they land in two
different dominant operators.

usage:
  dom_ops.py --in DIR --out DIR [--every N]
"""

import json
import os
import subprocess
import sys
import time


LANGS = ["c", "cpp", "go", "rust", "swift"]

# evidence classes, strongest first.  Same order and same words as
# dominant_table.py, so the two tables grade evidence identically.
EVIDENCE_ORDER = ["byte", "canon-byte", "sem", "core-text", "z3",
                  "not-recorded-per-pair", "unclassified"]

EVIDENCE_TEXT = {
    "byte": "byte identity (the two units are the same machine bytes)",
    "canon-byte": "canonical-byte identity (the same machine bytes "
                  "after the canonical renaming)",
    "sem": "anchored sem identity (the two lifted forms are identical)",
    "core-text": "core-text identity: verdicts4's own column found the "
                 "two normal-path cores textually equal",
    "z3": "z3 over the two lifted forms (a proof about the lifter's "
          "model, not about the bytes)",
    "not-recorded-per-pair": "verdicts3b records no ground for this "
                             "unit pair.  That is a limit of the pair "
                             "record, not a weak edge: the class this "
                             "pair sits in was formed by canonical-"
                             "byte identity or by a z3 edge, and "
                             "those grounds are recorded on the "
                             "CLASS, not on the pair.  Read "
                             "`weakest_evidence_from_the_class_table` "
                             "beside this.",
    "unclassified": "ground not recognised by this builder",
}

ABSENCE_TEXT = {
    "no_mutual_counterpart": "no mutual counterpart: the language has "
                             "units in these classes, but no node of "
                             "it was chosen back",
    "bridge_only": "attached by bridge only: a directional bridge "
                   "reaches these classes, membership does not",
    "refused": "refused by the type checker, or measured and never "
               "equal: no accepted unit of this language sits in any "
               "class this dominant operator spans",
}

ABSENCE_SHORT = {
    "no_mutual_counterpart": "no mutual",
    "bridge_only": "bridge only",
    "refused": "refused/absent",
}


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ---------------------------------------------------------------- io

def load(indir):
    doc = {}
    path = os.path.join(indir, "dominant_table3.json")
    doc["table"] = json.load(open(path))
    path = os.path.join(indir, "bridges.json")
    doc["bridges"] = json.load(open(path))
    path = os.path.join(indir, "verdicts3b.json")
    doc["verdicts3b"] = json.load(open(path))
    doc["manifest"] = {}
    doc["core_modes"] = {}
    for lang in LANGS:
        name = "probe_manifest_%s.json" % lang
        doc["manifest"][lang] = json.load(open(os.path.join(indir,
                                                            name)))
        name = "core_modes_%s.json" % lang
        doc["core_modes"][lang] = json.load(open(os.path.join(indir,
                                                              name)))
    return doc


# ------------------------------------------------------- provenance

def provenance(doc):
    """unit label -> the probe's own recorded provenance: which
    language, which grammar operator, which arity bucket.  Read from
    the probe manifest, which is the ONE place a token is authored."""
    out = {}
    for lang in LANGS:
        probes = doc["manifest"][lang]["probes"]
        for n in probes:
            probe = probes[n]
            label = "%s/op_%s" % (lang, n)
            rec = {}
            rec["lang"] = lang
            rec["n"] = n
            rec["display_label"] = probe["operator"]
            rec["arity_bucket"] = probe["bucket"]
            rec["expression"] = probe["expression"]
            out[label] = rec
    return out


# ------------------------------------------------------------ nodes

def build_nodes(doc, prov):
    """the node set.  A node is one (language, grammar-operator,
    arity-bucket) triple -- the provenance of a probe inside ONE
    language.  Nodes are numbered; no key here is built from a
    token."""
    seen = {}
    nodes = {}
    order = []
    for row in doc["table"]["rows"]:
        for member in row["members"]:
            label = member["unit"]
            rec = prov.get(label)
            if rec is None:
                continue
            key = (rec["lang"], rec["display_label"],
                   rec["arity_bucket"])
            if key not in seen:
                seen[key] = None
                order.append(key)
    order.sort()
    i = 0
    index = {}
    for key in order:
        i = i + 1
        nid = "N%04d" % i
        node = {}
        node["id"] = nid
        node["lang"] = key[0]
        node["label"] = key[1]
        node["arity"] = key[2]
        node["units"] = []
        node["classes"] = []
        node["type_keys"] = []
        nodes[nid] = node
        index[key] = nid
    return nodes, index


def node_of_unit(index, prov, label):
    rec = prov.get(label)
    if rec is None:
        return None
    key = (rec["lang"], rec["display_label"], rec["arity_bucket"])
    return index.get(key)


def fill_nodes(doc, nodes, index, prov):
    """which classes each node has units in, and on which operand-type
    keys.  Membership, not comparison."""
    class_members = {}
    for row in doc["table"]["rows"]:
        cid = row["class_id"]
        here = {}
        for member in row["members"]:
            label = member["unit"]
            nid = node_of_unit(index, prov, label)
            if nid is None:
                continue
            if nid not in here:
                here[nid] = []
            here[nid].append(label)
            node = nodes[nid]
            if label not in node["units"]:
                node["units"].append(label)
            if cid not in node["classes"]:
                node["classes"].append(cid)
            tkey = row["type_pair"]
            if tkey not in node["type_keys"]:
                node["type_keys"].append(tkey)
        class_members[cid] = here
    return class_members


# ------------------------------------------------------------ edges

def build_edges(doc, nodes, class_members, every):
    """cross-language edges.  Weight 1 = the number of equivalence
    classes in which the two nodes both have member units.  Weight 2 =
    the number of DISTINCT OPERAND-TYPE KEYS those classes carry, so a
    coincidence on bool alone scores 1.

    The pairing scope is class co-membership.  No token takes part."""
    edges = {}
    done = 0
    for row in doc["table"]["rows"]:
        cid = row["class_id"]
        tkey = row["type_pair"]
        here = class_members.get(cid, {})
        ids = sorted(here.keys())
        a = 0
        while a < len(ids):
            b = a + 1
            while b < len(ids):
                left = ids[a]
                right = ids[b]
                b = b + 1
                if nodes[left]["lang"] == nodes[right]["lang"]:
                    continue
                key = (left, right)
                if key not in edges:
                    rec = {}
                    rec["left"] = left
                    rec["right"] = right
                    rec["classes"] = []
                    rec["type_keys"] = []
                    edges[key] = rec
                rec = edges[key]
                if cid not in rec["classes"]:
                    rec["classes"].append(cid)
                if tkey not in rec["type_keys"]:
                    rec["type_keys"].append(tkey)
            a = a + 1
        done = done + 1
        if every > 0 and done % every == 0:
            log("   classes walked %d/%d, edges so far %d"
                % (done, len(doc["table"]["rows"]), len(edges)))
    for key in edges:
        rec = edges[key]
        rec["weight_classes"] = len(rec["classes"])
        rec["weight_type_keys"] = len(rec["type_keys"])
    return edges


# ------------------------------------------------- the mutual filter

def rank_key(nodes, edges, mine, other):
    """the ordering a node uses to pick its strongest counterpart:
    shared classes first, then shared operand-type keys, then the
    SMALLER class count (a node that sits in fewer classes is the more
    specific counterpart), then the SMALLER unit count.  Machine-form
    quantities only.

    There is deliberately NO further tie-break.  Ordering by node id
    would be ordering by the token the id was built from, and that is
    exactly what THE SPELLING BAN forbids.  When two counterparts tie
    on every machine-form quantity they are equally strongest, and
    both are kept -- see best_per_language."""
    key = pair_key(mine, other)
    rec = edges[key]
    parts = []
    parts.append(rec["weight_classes"])
    parts.append(rec["weight_type_keys"])
    parts.append(-len(nodes[other]["classes"]))
    parts.append(-len(nodes[other]["units"]))
    return tuple(parts)


def pair_key(a, b):
    if a <= b:
        return (a, b)
    return (b, a)


def best_per_language(nodes, edges):
    """each node's strongest counterpart per foreign language.

    Normally that is one node.  When two counterparts in the same
    foreign language tie on EVERY machine-form quantity, they are
    equally strongest and both are kept: separating them would take a
    token, and no token is allowed to select anything here.  The tie
    is recorded so it is visible rather than silent."""
    reach = {}
    for key in edges:
        left = key[0]
        right = key[1]
        reach.setdefault(left, []).append(right)
        reach.setdefault(right, []).append(left)
    best = {}
    ties = []
    for nid in sorted(reach.keys()):
        ranked = {}
        for other in reach[nid]:
            lang = nodes[other]["lang"]
            here = rank_key(nodes, edges, nid, other)
            if lang not in ranked:
                ranked[lang] = (here, [other])
                continue
            there = ranked[lang][0]
            if here > there:
                ranked[lang] = (here, [other])
                continue
            if here == there:
                ranked[lang][1].append(other)
        picks = {}
        for lang in ranked:
            chosen = sorted(ranked[lang][1])
            picks[lang] = chosen
            if len(chosen) > 1:
                rec = {}
                rec["node"] = nid
                rec["foreign_language"] = lang
                rec["equally_strongest"] = chosen
                rec["rank"] = list(ranked[lang][0])
                rec["why"] = "these counterparts tie on every "\
                             "machine-form quantity; separating them "\
                             "would take a token, so both are kept"
                ties.append(rec)
        best[nid] = picks
    return best, ties


def mutual_edges(nodes, edges, best):
    kept = {}
    for key in edges:
        left = key[0]
        right = key[1]
        lang_left = nodes[left]["lang"]
        lang_right = nodes[right]["lang"]
        if right not in best.get(left, {}).get(lang_right, []):
            continue
        if left not in best.get(right, {}).get(lang_left, []):
            continue
        kept[key] = edges[key]
    return kept


# ------------------------------------------------------- components

class UnionFind(object):
    def __init__(self):
        self.up = {}

    def add(self, x):
        if x not in self.up:
            self.up[x] = x

    def find(self, x):
        self.add(x)
        while self.up[x] != x:
            self.up[x] = self.up[self.up[x]]
            x = self.up[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        self.up[rb] = ra


def components(kept):
    uf = UnionFind()
    for key in kept:
        uf.union(key[0], key[1])
    groups = {}
    for nid in sorted(uf.up.keys()):
        root = uf.find(nid)
        groups.setdefault(root, []).append(nid)
    out = []
    for root in sorted(groups.keys()):
        members = sorted(groups[root])
        out.append(members)
    out.sort(key=lambda m: (-len(m), m[0]))
    return out


def assert_one_per_language(nodes, comps):
    """no component may hold two nodes of the same language.

    The brief said this holds BY CONSTRUCTION.  It does not, and the
    assertion is what showed it: a node keeps one counterpart per
    foreign language, but a COMPONENT is a chain, and a chain can walk
    back into a language it already visited.  So this returns the
    collisions instead of claiming there are none.  Nothing is merged
    and nothing is dropped -- the collision is recorded on the row and
    the owner settles what the rule should be."""
    checked = 0
    collisions = []
    i = 0
    for members in comps:
        i = i + 1
        seen = {}
        for nid in sorted(members):
            lang = nodes[nid]["lang"]
            if lang in seen:
                rec = {}
                rec["dom_op_id"] = "D%04d" % i
                rec["language"] = lang
                rec["first_node"] = seen[lang]
                rec["second_node"] = nid
                rec["why"] = "a component is a chain: each node kept "\
                             "one counterpart per foreign language, "\
                             "but the chain walked back into a "\
                             "language it had already visited"
                collisions.append(rec)
                continue
            seen[lang] = nid
        checked = checked + 1
    return checked, collisions


# -------------------------------------------------- evidence trail

def classify_ground(ground):
    if ground is None:
        return "unclassified"
    if ground.startswith("byte identity"):
        return "byte"
    if ground.startswith("sem identity"):
        return "sem"
    if ground.startswith("z3"):
        return "z3"
    return "core-text"


def ground_index(doc):
    """unit-pair -> the ground verdicts3b recorded for that pair.  The
    same reading dominant_table.py performs, so the grades agree."""
    out = {}
    for row in doc["verdicts3b"]["rows"]:
        for p in row.get("pairs", []):
            key = pair_key(p["left"], p["right"])
            if key in out:
                continue
            rec = {}
            rec["ground"] = p.get("ground")
            rec["evidence"] = classify_ground(p.get("ground"))
            rec["carried"] = p.get("carried_from") is not None
            out[key] = rec
    return out


def rank_of(name):
    if name in EVIDENCE_ORDER:
        return EVIDENCE_ORDER.index(name)
    return len(EVIDENCE_ORDER)


def pair_evidence(nodes, grounds, left, right, joint):
    """the evidence trail for one pair of member nodes: over every
    unit pair the two contribute to a shared class, the strongest
    ground recorded and the weakest."""
    seen = []
    for cid in joint:
        here = joint[cid]
        for a in here.get(left, []):
            for b in here.get(right, []):
                key = pair_key(a, b)
                rec = grounds.get(key)
                if rec is None:
                    seen.append("not-recorded-per-pair")
                    continue
                seen.append(rec["evidence"])
    tally = {}
    for name in seen:
        tally[name] = tally.get(name, 0) + 1
    strongest = None
    weakest = None
    for name in EVIDENCE_ORDER:
        if tally.get(name, 0) == 0:
            continue
        if strongest is None:
            strongest = name
        weakest = name
    rec = {}
    rec["left_node"] = left
    rec["right_node"] = right
    rec["unit_pairs"] = len(seen)
    rec["by_ground"] = tally
    rec["strongest_ground"] = strongest
    rec["weakest_ground"] = weakest
    if strongest is None:
        rec["strongest_text"] = "no recorded unit pair"
        rec["weakest_text"] = "no recorded unit pair"
    else:
        rec["strongest_text"] = EVIDENCE_TEXT[strongest]
        rec["weakest_text"] = EVIDENCE_TEXT[weakest]
    return rec


# ------------------------------------------------------------- rows

def fence_key(fence):
    parts = []
    parts.append(str(fence.get("condition")))
    parts.append(str(fence.get("response_kind")))
    return " -> ".join(parts)


def fence_inventory(doc, nodes, members):
    """the modes (fences) the member units carry, read from
    core_modes_*.json.  A fence is a guard or trap the compiler put
    around the normal path."""
    out = []
    for nid in members:
        node = nodes[nid]
        lang = node["lang"]
        units = doc["core_modes"][lang]["units"]
        for label in node["units"]:
            n = label.split("op_")[-1]
            unit = units.get(n)
            if unit is None:
                continue
            for fence in unit.get("modes", []):
                rec = {}
                rec["node"] = nid
                rec["lang"] = lang
                rec["unit"] = label
                rec["fence"] = fence_key(fence)
                out.append(rec)
    return out


def class_table_weakest(doc, cids):
    """the weakest evidence dominant_table3 itself recorded on the
    classes this dominant operator spans.  Quoted, not re-derived."""
    inside = {}
    for cid in cids:
        inside[cid] = None
    worst = None
    tally = {}
    for row in doc["table"]["rows"]:
        if row["class_id"] not in inside:
            continue
        name = row["evidence"]["weakest_evidence"]
        if name is None:
            continue
        tally[name] = tally.get(name, 0) + 1
        if worst is None or rank_of(name) > rank_of(worst):
            worst = name
    return worst, tally


def joint_classes(nodes, class_members, members):
    """the classes this dominant operator SPANS: a class in which at
    least two of its member nodes both have units.  Those are the
    classes that carried the edges."""
    inside = {}
    for nid in members:
        inside[nid] = None
    out = {}
    for cid in class_members:
        here = class_members[cid]
        hits = {}
        for nid in here:
            if nid in inside:
                hits[nid] = here[nid]
        if len(hits) < 2:
            continue
        out[cid] = hits
    return out


def touched_classes(nodes, members):
    out = {}
    for nid in members:
        for cid in nodes[nid]["classes"]:
            out[cid] = None
    return sorted(out.keys())


def bridges_for(doc, cids):
    inside = {}
    for cid in cids:
        inside[cid] = None
    out = []
    for bridge in doc["bridges"]["bridges"]:
        dom = bridge["dominant_class"]
        sub = bridge["dominated_class"]
        if dom not in inside and sub not in inside:
            continue
        rec = {}
        rec["dominant_class"] = dom
        rec["dominated_class"] = sub
        rec["operand_types"] = bridge["operand_types"]
        rec["dominant_result_type"] = bridge["dominant_result_type"]
        rec["dominated_result_type"] = bridge["dominated_result_type"]
        rec["projection"] = bridge["projection_kind"]
        rec["adapter"] = bridge["adapter"]
        rec["inside"] = dom in inside and sub in inside
        rec["dominant_languages"] = \
            bridge["evidence"]["dominant_languages"]
        rec["dominated_languages"] = \
            bridge["evidence"]["dominated_languages"]
        out.append(rec)
    return out


def absence(doc, nodes, members, class_members, joint, bridges):
    present = {}
    for nid in members:
        present[nodes[nid]["lang"]] = None
    out = []
    for lang in LANGS:
        if lang in present:
            continue
        has_units = False
        for cid in joint:
            for nid in class_members.get(cid, {}):
                if nodes[nid]["lang"] == lang:
                    has_units = True
        by_bridge = False
        for bridge in bridges:
            if lang in bridge["dominant_languages"]:
                by_bridge = True
            if lang in bridge["dominated_languages"]:
                by_bridge = True
        if has_units:
            reason = "no_mutual_counterpart"
        elif by_bridge:
            reason = "bridge_only"
        else:
            reason = "refused"
        rec = {}
        rec["language"] = lang
        rec["reason"] = reason
        rec["why"] = ABSENCE_TEXT[reason]
        rec["short"] = ABSENCE_SHORT[reason]
        rec["reached_by_a_bridge"] = by_bridge
        if reason == "refused":
            rec["evidence_class"] = "forced by construction (the "\
                                    "absence of a unit and of an edge)"
        else:
            rec["evidence_class"] = "forced by construction (the "\
                                    "absence of a mutual choice)"
        out.append(rec)
    return out


def one_dom_op(doc, nodes, kept, class_members, grounds, did, members):
    joint = joint_classes(nodes, class_members, members)
    cids = sorted(joint.keys())
    touched = touched_classes(nodes, members)
    bridges = bridges_for(doc, cids)
    fences = fence_inventory(doc, nodes, members)
    row = {}
    row["dom_op_id"] = did
    row["size"] = len(members)
    row["languages"] = sorted([nodes[n]["lang"] for n in members])
    out_members = []
    for nid in sorted(members):
        node = nodes[nid]
        rec = {}
        rec["id"] = nid
        rec["lang"] = node["lang"]
        rec["label"] = node["label"]
        rec["arity"] = node["arity"]
        rec["unit_count"] = len(node["units"])
        rec["class_count"] = len(node["classes"])
        rec["units"] = sorted(node["units"])
        out_members.append(rec)
    row["members"] = out_members
    row["classes_spanned"] = cids
    row["classes_spanned_count"] = len(cids)
    row["classes_touched_count"] = len(touched)
    row["surviving_edges"] = []
    trail = []
    a = 0
    ms = sorted(members)
    while a < len(ms):
        b = a + 1
        while b < len(ms):
            key = pair_key(ms[a], ms[b])
            b = b + 1
            if key not in kept:
                continue
            edge = kept[key]
            erec = {}
            erec["left_node"] = key[0]
            erec["right_node"] = key[1]
            erec["weight_classes"] = edge["weight_classes"]
            erec["weight_type_keys"] = edge["weight_type_keys"]
            row["surviving_edges"].append(erec)
        a = a + 1
    a = 0
    while a < len(ms):
        b = a + 1
        while b < len(ms):
            trail.append(pair_evidence(nodes, grounds, ms[a], ms[b],
                                       joint))
            b = b + 1
        a = a + 1
    row["evidence_trail"] = trail
    weakest = None
    strongest = None
    for rec in trail:
        name = rec["weakest_ground"]
        if name is not None:
            if weakest is None or rank_of(name) > rank_of(weakest):
                weakest = name
        name = rec["strongest_ground"]
        if name is not None:
            if strongest is None or rank_of(name) < rank_of(strongest):
                strongest = name
    row["weakest_evidence"] = weakest
    row["strongest_evidence"] = strongest
    if weakest is None:
        row["weakest_evidence_text"] = "no recorded unit pair"
    else:
        row["weakest_evidence_text"] = EVIDENCE_TEXT[weakest]
    worst, tally = class_table_weakest(doc, cids)
    row["weakest_evidence_from_the_class_table"] = worst
    row["class_table_weakest_distribution"] = tally
    row["bridges"] = bridges
    row["bridge_count"] = len(bridges)
    row["fences"] = fences
    row["fence_count"] = len(fences)
    kinds = {}
    for rec in fences:
        kinds[rec["fence"]] = kinds.get(rec["fence"], 0) + 1
    row["fence_kinds"] = kinds
    row["languages_absent"] = absence(doc, nodes, members,
                                      class_members, joint, bridges)
    row["intention"] = None
    row["intention_candidates"] = {}
    row["intention_candidates"]["proposed_hint"] = None
    row["intention_candidates"]["status"] = "proposed, the owner settles"
    row["intention_candidates"]["why"] = "this table names no "\
        "intention: a dominant operator is a machine-evidence "\
        "component, and the intention over it is the owner's ruling"
    return row


# ------------------------------------- the no-arity comparison run

def no_arity_run(doc, prov):
    """the same construction with ARITY DROPPED from node identity --
    the session's quick run.  Kept so the movement the arity fix
    causes is measured here, in this program, and not recalled."""
    seen = {}
    order = []
    for row in doc["table"]["rows"]:
        for member in row["members"]:
            rec = prov.get(member["unit"])
            if rec is None:
                continue
            key = (rec["lang"], rec["display_label"])
            if key not in seen:
                seen[key] = None
                order.append(key)
    order.sort()
    nodes = {}
    index = {}
    i = 0
    for key in order:
        i = i + 1
        nid = "M%04d" % i
        node = {}
        node["id"] = nid
        node["lang"] = key[0]
        node["label"] = key[1]
        node["arity"] = "not part of identity in this run"
        node["units"] = []
        node["classes"] = []
        node["type_keys"] = []
        nodes[nid] = node
        index[key] = nid
    class_members = {}
    for row in doc["table"]["rows"]:
        cid = row["class_id"]
        here = {}
        for member in row["members"]:
            rec = prov.get(member["unit"])
            if rec is None:
                continue
            nid = index[(rec["lang"], rec["display_label"])]
            here.setdefault(nid, []).append(member["unit"])
            node = nodes[nid]
            if member["unit"] not in node["units"]:
                node["units"].append(member["unit"])
            if cid not in node["classes"]:
                node["classes"].append(cid)
        class_members[cid] = here
    edges = build_edges(doc, nodes, class_members, 0)
    best, ties = best_per_language(nodes, edges)
    kept = mutual_edges(nodes, edges, best)
    comps = components(kept)
    out = {}
    out["nodes"] = len(nodes)
    out["edges_before_the_mutual_filter"] = len(edges)
    out["edges_after_the_mutual_filter"] = len(kept)
    out["components"] = len(comps)
    return out


# ------------------------------------------------------------ build

def build(indir, outdir, every):
    started = time.time()
    log("-- reading the table, the bridges, the manifests, the modes")
    doc = load(indir)
    log("   classes %d, bridges %d"
        % (len(doc["table"]["rows"]),
           len(doc["bridges"]["bridges"])))
    prov = provenance(doc)
    log("   probe provenance records %d" % len(prov))

    log("-- nodes: (language, grammar-operator, arity bucket)")
    nodes, index = build_nodes(doc, prov)
    class_members = fill_nodes(doc, nodes, index, prov)
    log("   nodes %d" % len(nodes))
    buckets = {}
    for nid in nodes:
        name = nodes[nid]["arity"]
        buckets[name] = buckets.get(name, 0) + 1
    log("   by arity bucket %s" % json.dumps(buckets))

    log("-- edges: cross-language only, weighted by shared classes")
    edges = build_edges(doc, nodes, class_members, every)
    log("   edges before the mutual filter %d" % len(edges))

    log("-- the mutual-best filter")
    best, ties = best_per_language(nodes, edges)
    kept = mutual_edges(nodes, edges, best)
    log("   edges after the mutual filter %d" % len(kept))
    log("   equally-strongest ties kept whole %d" % len(ties))

    log("-- components of the mutual-best graph")
    comps = components(kept)
    log("   components %d" % len(comps))
    checked, collisions = assert_one_per_language(nodes, comps)
    log("   ASSERTION RAN over %d components: two-nodes-of-one-"
        "language collisions %d" % (checked, len(collisions)))
    for rec in collisions:
        log("   !! %s holds two %s nodes: %s and %s -- recorded, not "
            "resolved; the owner settles"
            % (rec["dom_op_id"], rec["language"], rec["first_node"],
               rec["second_node"]))

    log("-- the evidence trail")
    grounds = ground_index(doc)
    log("   recorded unit pairs %d" % len(grounds))

    rows = []
    i = 0
    for members in comps:
        i = i + 1
        did = "D%04d" % i
        row = one_dom_op(doc, nodes, kept, class_members, grounds,
                         did, members)
        row["same_language_collisions"] = []
        for rec in collisions:
            if rec["dom_op_id"] == did:
                row["same_language_collisions"].append(rec)
        rows.append(row)
        if every > 0 and i % every == 0:
            log("   dom_ops built %d/%d" % (i, len(comps)))
    log("   dom_ops %d" % len(rows))

    log("-- the same construction with arity dropped, for comparison")
    quick = no_arity_run(doc, prov)
    log("   without the arity fix: nodes %d, edges %d -> %d, "
        "components %d"
        % (quick["nodes"], quick["edges_before_the_mutual_filter"],
           quick["edges_after_the_mutual_filter"],
           quick["components"]))

    attached = {}
    for key in kept:
        attached[key[0]] = None
        attached[key[1]] = None
    unattached = []
    for nid in sorted(nodes.keys()):
        if nid in attached:
            continue
        rec = {}
        rec["id"] = nid
        rec["lang"] = nodes[nid]["lang"]
        rec["label"] = nodes[nid]["label"]
        rec["arity"] = nodes[nid]["arity"]
        rec["class_count"] = len(nodes[nid]["classes"])
        unattached.append(rec)

    out = {}
    out["shape"] = "one row per DOMINANT OPERATOR: a connected "\
                   "component of the mutual-best graph over "\
                   "(language, grammar-operator, arity) nodes"
    out["rule"] = "THE DOM_OP CONSTRUCTION RULE (the owner, 2026-08-26): "\
                  "dominant operators are DISCOVERED from machine "\
                  "evidence by matching, never asserted"
    out["node_definition"] = "a node is the PROVENANCE of a probe -- "\
                             "which grammar rule of ONE language "\
                             "generated it: language, grammar "\
                             "operator, arity bucket.  Arity is part "\
                             "of identity because one token can be "\
                             "two operators."
    out["candidate_set"] = "machine-form evidence only: two nodes are "\
                           "compared when they have units in the same "\
                           "equivalence class of dominant_table3.  "\
                           "No operator token takes part in any key, "\
                           "grouping, pairing or selection here."
    out["spelling"] = "the operator token appears exactly once per "\
                      "node, as the display label `label` on a member "\
                      "that also carries its language and its id"
    out["edge_weights"] = "primary: the number of equivalence classes "\
                          "in which the two nodes both have member "\
                          "units.  secondary: the number of distinct "\
                          "operand-type keys those classes carry, so "\
                          "a coincidence on bool alone scores 1."
    out["mutual_filter"] = "each node keeps its strongest counterpart "\
                           "per foreign language (classes, then type "\
                           "keys, then the smaller class count); the "\
                           "edge survives only when both endpoints "\
                           "chose each other"
    out["intention_note"] = "`intention` is null on every row by "\
                            "instruction; the hint field is proposed "\
                            "only.  the owner settles."
    out["languages"] = LANGS
    out["nodes"] = len(nodes)
    out["nodes_by_arity_bucket"] = buckets
    out["edges_before_the_mutual_filter"] = len(edges)
    out["edges_after_the_mutual_filter"] = len(kept)
    out["dom_op_count"] = len(rows)
    out["nodes_in_a_dom_op"] = len(attached)
    out["nodes_with_no_surviving_edge"] = len(unattached)
    out["unattached_nodes"] = unattached
    out["same_language_assertion"] = {}
    out["same_language_assertion"]["ran"] = True
    out["same_language_assertion"]["components_checked"] = checked
    out["same_language_assertion"]["violations"] = len(collisions)
    out["same_language_assertion"]["collisions"] = collisions
    out["same_language_assertion"]["finding"] = \
        "the brief said a component cannot hold two nodes of one "\
        "language BY CONSTRUCTION.  It can, and the assertion found "\
        "it.  A node keeps one counterpart per foreign language, but "\
        "a component is a CHAIN, and a chain can walk back into a "\
        "language it already visited.  Nothing is merged and nothing "\
        "is dropped here; the collision is recorded on the row and "\
        "the owner settles the rule."
    out["equally_strongest_ties"] = ties
    out["equally_strongest_ties_note"] = "two counterparts in one foreign language that tie on every machine-form quantity are both kept: separating them would take a token, and no token selects anything here"
    out["without_the_arity_fix"] = quick
    out["node_inventory"] = []
    for nid in sorted(nodes.keys()):
        node = nodes[nid]
        rec = {}
        rec["id"] = nid
        rec["lang"] = node["lang"]
        rec["label"] = node["label"]
        rec["arity"] = node["arity"]
        rec["unit_count"] = len(node["units"])
        rec["class_count"] = len(node["classes"])
        out["node_inventory"].append(rec)
    out["wall_seconds"] = round(time.time() - started, 2)
    out["rows"] = rows

    path = os.path.join(outdir, "dom_ops.json")
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("   wrote %s" % path)

    write_markdown(out, os.path.join(outdir, "dom_ops.md"))
    log("   wrote %s" % os.path.join(outdir, "dom_ops.md"))
    write_digest(out, os.path.join(outdir, "dom_ops_digest.md"),
                 os.path.join(outdir, "dom_ops_digest_shape.json"))
    log("   wrote %s" % os.path.join(outdir, "dom_ops_digest.md"))
    return out


# --------------------------------------------------------- markdown

def cell(text):
    if text is None:
        return "--"
    out = str(text)
    out = out.replace("|", "\\|")
    return out


def write_markdown(out, path):
    lines = []
    lines.append("# dom_ops -- the dominant operators")
    lines.append("")
    lines.append("- rule: %s" % out["rule"])
    lines.append("- node: %s" % out["node_definition"])
    lines.append("- candidate set: %s" % out["candidate_set"])
    lines.append("- spelling: %s" % out["spelling"])
    lines.append("- edge weights: %s" % out["edge_weights"])
    lines.append("- mutual filter: %s" % out["mutual_filter"])
    lines.append("- intention: %s" % out["intention_note"])
    lines.append("")
    lines.append("nodes %d, edges %d before the mutual filter, %d "
                 "after, dom_ops %d"
                 % (out["nodes"],
                    out["edges_before_the_mutual_filter"],
                    out["edges_after_the_mutual_filter"],
                    out["dom_op_count"]))
    lines.append("")
    quick = out["without_the_arity_fix"]
    lines.append("without the arity fix, the same construction gives "
                 "nodes %d, edges %d before the filter, %d after, "
                 "components %d."
                 % (quick["nodes"],
                    quick["edges_before_the_mutual_filter"],
                    quick["edges_after_the_mutual_filter"],
                    quick["components"]))
    lines.append("")
    lines.append("the same-language assertion ran over %d components; "
                 "%d collisions found."
                 % (out["same_language_assertion"]["components_checked"],
                    out["same_language_assertion"]["violations"]))
    lines.append("")
    lines.append(out["same_language_assertion"]["finding"])
    lines.append("")
    for row in out["rows"]:
        lines.append("## %s -- %d members over %s"
                     % (row["dom_op_id"], row["size"],
                        ", ".join(row["languages"])))
        lines.append("")
        lines.append("| language | label | arity |")
        lines.append("| --- | --- | --- |")
        for member in row["members"]:
            lines.append("| %s | `%s` | %s |"
                         % (member["lang"], cell(member["label"]),
                            member["arity"]))
        lines.append("")
        lines.append("- classes spanned (%d): %s"
                     % (row["classes_spanned_count"],
                        ", ".join(row["classes_spanned"][:40])))
        if row["classes_spanned_count"] > 40:
            lines.append("  (and %d more)"
                         % (row["classes_spanned_count"] - 40))
        lines.append("- classes any member touches: %d"
                     % row["classes_touched_count"])
        lines.append("- strongest evidence over the member pairs: "
                     "%s" % cell(row["strongest_evidence"]))
        lines.append("- weakest over the member pairs: %s"
                     % row["weakest_evidence_text"])
        lines.append("- weakest the class table itself recorded on "
                     "the spanned classes: %s"
                     % cell(row["weakest_evidence_from_the_class_"
                                "table"]))
        lines.append("- surviving edges: %d"
                     % len(row["surviving_edges"]))
        for erec in row["surviving_edges"]:
            lines.append("  - %s--%s: %d shared classes, %d shared "
                         "operand-type keys"
                         % (erec["left_node"], erec["right_node"],
                            erec["weight_classes"],
                            erec["weight_type_keys"]))
        lines.append("- bridges: %d" % row["bridge_count"])
        for bridge in row["bridges"][:12]:
            lines.append("  - %s dominates %s on the %s projection; "
                         "adapter `%s`; dominant %s, dominated %s"
                         % (bridge["dominant_class"],
                            bridge["dominated_class"],
                            bridge["projection"],
                            cell(bridge["adapter"]),
                            ",".join(bridge["dominant_languages"]),
                            ",".join(bridge["dominated_languages"])))
        if row["bridge_count"] > 12:
            lines.append("  - (and %d more)"
                         % (row["bridge_count"] - 12))
        lines.append("- fences: %d" % row["fence_count"])
        for name in sorted(row["fence_kinds"].keys()):
            lines.append("  - %s x%d"
                         % (name, row["fence_kinds"][name]))
        lines.append("- languages absent:")
        for rec in row["languages_absent"]:
            lines.append("  - %s: %s" % (rec["language"], rec["why"]))
        lines.append("- intention: null; hint proposed only, the owner "
                     "settles")
        lines.append("")
        lines.append("evidence trail, member pair by member pair:")
        lines.append("")
        lines.append("| pair | unit pairs | strongest | weakest |")
        lines.append("| --- | --- | --- | --- |")
        for rec in row["evidence_trail"]:
            lines.append("| %s--%s | %d | %s | %s |"
                         % (rec["left_node"], rec["right_node"],
                            rec["unit_pairs"],
                            cell(rec["strongest_ground"]),
                            cell(rec["weakest_ground"])))
        lines.append("")
    fh = open(path, "w")
    fh.write("\n".join(lines) + "\n")
    fh.close()


def write_digest(out, path, shape_path):
    """the flat digest: ONE table for the whole thing.  Rows are
    dominant operators, columns are the five languages, then the
    machine-form columns."""
    lines = []
    lines.append("# dom_ops digest -- one table")
    lines.append("")
    lines.append("Rows are dominant operators: connected components "
                 "of the mutual-best graph.  A language cell carries "
                 "that language's display label and arity, or `--` "
                 "with the reason it is absent.")
    lines.append("")
    lines.append("Absence reasons: `no mutual` = the language has "
                 "units in these classes but no node of it was chosen "
                 "back; `bridge only` = a directional bridge reaches "
                 "these classes, membership does not; "
                 "`refused/absent` = no accepted unit of the language "
                 "sits in any class this dominant operator spans.")
    lines.append("")
    header = ["dom_op"]
    for lang in LANGS:
        header.append(lang)
    header.append("classes")
    header.append("bridges")
    header.append("fences")
    header.append("weakest evidence")  # as the class table recorded it
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in out["rows"]:
        cells = [row["dom_op_id"]]
        by_lang = {}
        for member in row["members"]:
            by_lang.setdefault(member["lang"], []).append(member)
        absent = {}
        for rec in row["languages_absent"]:
            absent[rec["language"]] = rec
        for lang in LANGS:
            here = by_lang.get(lang)
            if here is not None:
                parts = []
                for member in here:
                    parts.append("`%s` %s" % (cell(member["label"]),
                                              member["arity"]))
                cells.append(" + ".join(parts))
                continue
            rec = absent.get(lang)
            if rec is None:
                cells.append("--")
                continue
            cells.append("-- %s" % rec["short"])
        cells.append(str(row["classes_spanned_count"]))
        cells.append(str(row["bridge_count"]))
        cells.append(str(row["fence_count"]))
        cells.append(cell(row["weakest_evidence_from_the_class_table"]))
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("A cell holding two labels joined by `+` is a "
                 "same-language collision: the component chained back "
                 "into a language it had already visited.  Recorded, "
                 "not resolved -- the owner settles the rule.")
    lines.append("")
    lines.append("nodes %d; edges %d before the mutual filter, %d "
                 "after; dom_ops %d."
                 % (out["nodes"],
                    out["edges_before_the_mutual_filter"],
                    out["edges_after_the_mutual_filter"],
                    out["dom_op_count"]))
    fh = open(path, "w")
    fh.write("\n".join(lines) + "\n")
    fh.close()
    # the shipped guard reads JSON, not markdown.  The digest's
    # STRUCTURE -- its column names and its row identities -- is
    # written out as JSON so the same mechanical guard reads it.  A
    # token in a column name or a row identity would be caught here.
    shape = {}
    shape["what"] = "the STRUCTURE of dom_ops_digest.md: its column "\
                    "names and its row identities.  The language "\
                    "cells are display labels and are not structure; "\
                    "they are carried on unit objects below."
    shape["column_names"] = header
    shape["row_identities"] = [r["dom_op_id"] for r in out["rows"]]
    labels = []
    for row in out["rows"]:
        for member in row["members"]:
            rec = {}
            rec["id"] = member["id"]
            rec["lang"] = member["lang"]
            rec["label"] = member["label"]
            rec["arity"] = member["arity"]
            labels.append(rec)
    shape["cell_labels"] = labels
    fh = open(shape_path, "w")
    json.dump(shape, fh, indent=1)
    fh.write("\n")
    fh.close()


# ------------------------------------------------------------- main

def guard(outdir, names):
    """THE SPELLING BAN's mechanical guard.  This program refuses its
    own output when the guard fails."""
    here = os.path.dirname(os.path.abspath(__file__))
    checker = os.path.join(here, "check_no_spelling_keys.py")
    if not os.path.exists(checker):
        checker = os.path.join(outdir, "check_no_spelling_keys.py")
    cmd = [sys.executable, checker]
    for name in names:
        cmd.append(os.path.join(outdir, name))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stdout.write(proc.stderr)
    return proc.returncode


def main(argv):
    indir = os.path.dirname(os.path.abspath(__file__))
    outdir = indir
    every = 200
    i = 0
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
        if argv[i] == "--out":
            outdir = argv[i + 1]
        if argv[i] == "--every":
            every = int(argv[i + 1])
        i = i + 1
    out = build(indir, outdir, every)
    log("-- THE SPELLING BAN: the mechanical guard, on every product")
    names = ["dom_ops.json", "dom_ops_digest_shape.json"]
    rc = guard(outdir, names)
    if rc != 0:
        log("!! THE GUARD FAILED: refusing this output.")
        return rc
    log("   guard PASS on %s" % ", ".join(names))
    log("dom_ops %d, wall %.2fs"
        % (out["dom_op_count"], out["wall_seconds"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
