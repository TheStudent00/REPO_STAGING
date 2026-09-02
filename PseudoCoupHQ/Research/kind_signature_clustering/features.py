#!/usr/bin/env python3
"""features.py — first clustering pass, feature extraction.

Reads raw/<lang>.node-types.json for the five languages rust, python, dart,
c, cpp (kotlin deliberately excluded: it declares no roles/supertypes and
will be evaluated against the validated clusters later) and emits
features.json: one feature record per (language, named kind), built from
grammar-shipped data ONLY.

Vocabulary: tree-sitter's JSON key `children` is quoted only as its key name;
in this codebase that construct is the "sub-node spec". Kinds admitted by a
slot are its input kinds; the positions a kind may occupy are its output
types. We never use tree-terminology other than super-node / sub-node /
co-node / sub-tree.

FEATURES (each is one or more elements of a flat weighted feature set; the
weight of an element is fixed per feature family and drives the weighted
Jaccard distance in cluster.py):

1. role:<r>            (weight 3)  — the kind has a slot with shared role r.
   Shared role vocabulary (present in all five languages, from log_008):
   alternative, arguments, body, condition, consequence, left, name,
   operator, parameters, right, value. Non-shared roles are bucketed as the
   single boolean feature has_other_roles (weight 1) because their names are
   not language-comparable.
2. role:<r>:mult / role:<r>:req  (weight 1 each) — the slot's arity flags
   `multiple` / `required` as shipped in the grammar.
3. in:<r>:<sig>        (weight 1)  — per-slot input types, ABSTRACTED to be
   language-comparable: every concrete kind name in the slot's allowed list
   is collapsed to its derived output-type signature (see 5); a supertype in
   the list contributes sup:<aliased-name>; an unnamed token contributes the
   bucket element "tok". Concrete names never survive into features.
4. anon:mult / anon:req (weight 1), in:anon:<sig> (weight 0.5) — the same
   for the sub-node spec, at half input weight since anonymous positions are
   noisier.
5. out:<sig>           (weight 2)  — output-type memberships, declared AND
   derived. Declared: membership in a grammar-declared supertype, run
   through a small alias table (e.g. _expression/expression/
   primary_expression -> expression) because supertype spelling differs by
   language. DERIVED, purely mechanically, by inverting the grammar: for
   each kind, collect every position that admits it — pos:<r> for each
   shared role r under whose slot it may appear (expanding supertype
   references in type lists recursively), pos:other_role if admitted under
   any non-shared role, pos:anon if admitted in any sub-node spec.
6. is_leaf             (weight 3)  — no fields, no sub-node spec, not a
   supertype.
7. has_subnode_spec    (weight 1)  — the kind carries a sub-node spec.
8. has_other_roles     (weight 1)  — see 1.

features.json layout: {lang: {kind: {"features": {element: weight},
"readable": {...decomposed view for inspection...}}}}
"""
import json
import os
import sys
import collections

# Hold-out flag (the owner's ruling 2a, 2026-08-12): when set, declared supertype
# MEMBERSHIPS are dropped so tree-sitter's own declarations can serve as
# held-out validation targets. Declared memberships are entangled: out_sig()
# feeds both out:* features and the input-signature abstraction, so a flag
# here (rather than a post-hoc filter on out:sup:*) is the only clean cut.
# Supertype REFERENCES inside slot type lists are kept: they are input-side
# grammar structure, not membership assertions about the kind being featured.
HOLD_OUT_DECLARED = False

# Decision-6 fix (v2, 2026-08-12): derived output positions carry COUNTS.
# In v1 a kind "appears under `condition`" was a set element regardless of
# whether 1 or 50 host kinds admit it there. In v2 the count of DISTINCT
# host kinds admitting the kind under each position tag is bucketed on a
# log2 scale and emitted as an ADDITIONAL feature element next to the
# presence element:
#     out:pos:<tag>          (weight W_OUT, as before  -> backward signal)
#     out:pos:<tag>:xb<k>    (weight W_OUT_COUNT, new  -> count resolution)
# with bucket k = min(4, floor(log2(count))): b0=1 host, b1=2-3, b2=4-7,
# b3=8-15, b4=16+. Sub-decisions, ruled here and reported in log_013:
#   (a) BUCKETED log2, not raw or continuous counts — the distance function
#       (weighted Jaccard over set elements) is reused AS IS, so counts must
#       be discretized to participate; log2 buckets make 1-vs-2 hosts a
#       difference but 40-vs-50 not, matching how coarse grammar-shipped
#       admission counts really are.
#   (b) presence element KEPT alongside the bucket element — two kinds
#       admitted under `condition` by 1 vs 20 hosts still share the
#       presence element and differ on the bucket, a graded (not cliff)
#       separation; this is also what keeps v2 backward-compatible in
#       spirit with v1 (v1 features are a subset of v2 features).
#   (c) counts count DISTINCT HOST KINDS, not slots — a host with two
#       slots admitting the same kind under the same tag counts once.
#   (d) input-signature abstraction stays presence-based — pushing buckets
#       through abstract_input() would explode in:* cardinality and change
#       decision 5, which is not on the table here.
# Output is VERSIONED (features_v2.json / features_v2_holdout.json); v1
# outputs are untouched, so everything downstream of features.json is
# backward compatible.
V2_COUNTS = False
W_OUT_COUNT = 1.0
COUNT_BUCKET_CAP = 4


def count_bucket(c):
    b = 0
    while c >= 2 and b < COUNT_BUCKET_CAP:
        c //= 2
        b += 1
    return b

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LANGS = ["rust", "python", "dart", "c", "cpp"]

SHARED_ROLES = [
    "alternative", "arguments", "body", "condition", "consequence",
    "left", "name", "operator", "parameters", "right", "value",
]

# Supertype alias table: language-specific supertype spellings mapped to a
# shared name. This is the one manual table in the pipeline (log_008 SS7
# called for it); everything else is mechanical.
SUPER_ALIAS = {
    "_expression": "expression", "expression": "expression",
    "primary_expression": "expression",
    "statement": "statement", "_statement": "statement",
    "_compound_statement": "statement", "_simple_statement": "statement",
    "_declaration_statement": "statement",
    "_literal": "literal", "_literal_pattern": "literal",
    "_pattern": "pattern", "pattern": "pattern",
    "_type": "type", "type_specifier": "type",
    "_declaration": "declaration",
    "_declarator": "declarator", "_abstract_declarator": "declarator",
    "_field_declarator": "declarator", "_type_declarator": "declarator",
    "parameter": "parameter",
}

# Feature-family weights (the inspectable knobs of the distance function).
W_ROLE = 3.0
W_ARITY = 1.0
W_IN = 1.0
W_IN_ANON = 0.5
W_OUT = 2.0
W_LEAF = 3.0
W_SUBNODE = 1.0
W_OTHER_ROLES = 1.0


def load(lang):
    with open(os.path.join(RAW, lang + ".node-types.json")) as f:
        return json.load(f)


def slot_iter(entry):
    """Yield (role-or-None, spec) for field slots and the sub-node spec.
    `children` below is tree-sitter's key name for the sub-node spec."""
    for name, spec in (entry.get("fields") or {}).items():
        yield name, spec
    if "children" in entry:
        yield None, entry["children"]


def build_language(lang):
    return build_features(load(lang))


def build_features(data):
    by_name = {e["type"]: e for e in data if e.get("named")}
    supertypes = {e["type"]: [s["type"] for s in e.get("subtypes", [])]
                  for e in data if "subtypes" in e}

    def expand(type_list, seen=None):
        """Expand supertype references in a slot's allowed list to the
        concrete kinds they cover (recursively), keeping the supertype
        names too."""
        seen = seen or set()
        out = set()
        for t in type_list:
            n = t["type"] if isinstance(t, dict) else t
            if n in seen:
                continue
            seen.add(n)
            out.add(n)
            if n in supertypes:
                out |= expand(supertypes[n], seen)
        return out

    # --- Mechanical inversion of the grammar: derived output positions ---
    # pos_index[kind] = set of position tags where the kind may appear.
    # pos_counts[kind] = Counter of tag -> number of DISTINCT host kinds
    # admitting the kind under that tag (v2 decision-6 fix, sub-decision c).
    pos_index = collections.defaultdict(set)
    pos_counts = collections.defaultdict(collections.Counter)
    for e in data:
        if not e.get("named"):
            continue
        host_tags = collections.defaultdict(set)  # kind -> tags in THIS host
        for role, spec in slot_iter(e):
            admitted = expand(spec.get("types", []))
            if role is None:
                tag = "pos:anon"
            elif role in SHARED_ROLES:
                tag = "pos:" + role
            else:
                tag = "pos:other_role"
            for k in admitted:
                host_tags[k].add(tag)
        for k, tags in host_tags.items():
            for tag in tags:
                pos_index[k].add(tag)
                pos_counts[k][tag] += 1

    # Declared supertype memberships (aliased).
    declared = collections.defaultdict(set)
    for sup, subs in supertypes.items():
        alias = SUPER_ALIAS.get(sup, sup)
        for s in subs:
            declared[s].add("sup:" + alias)
    if HOLD_OUT_DECLARED:
        declared = collections.defaultdict(set)

    def out_sig(kind):
        """Derived output-type signature of a kind: declared supertype
        memberships (aliased) plus every position tag that admits it."""
        return declared.get(kind, set()) | pos_index.get(kind, set())

    def abstract_input(spec):
        """Collapse a slot's allowed list to language-comparable signatures:
        supertype -> its alias; named concrete kind -> its output signature;
        unnamed token -> the bucket 'tok'."""
        sig = set()
        for t in spec.get("types", []):
            n = t["type"]
            if not t.get("named"):
                sig.add("tok")
            elif n in supertypes:
                sig.add("sup:" + SUPER_ALIAS.get(n, n))
            else:
                sig |= out_sig(n)
        return sig

    result = {}
    for name, e in by_name.items():
        if name in supertypes:
            continue  # supertype entries are categories, not clusterable kinds
        feats = {}
        readable = {"roles": [], "other_roles": [], "out": [], "inputs": {}}

        def add(el, w):
            feats[el] = max(feats.get(el, 0.0), w)

        has_other = False
        for role, spec in slot_iter(e):
            if role is None:
                key = "anon"
                if spec.get("multiple"):
                    add("anon:mult", W_ARITY)
                if spec.get("required"):
                    add("anon:req", W_ARITY)
                for s in abstract_input(spec):
                    add("in:anon:" + s, W_IN_ANON)
                readable["inputs"][key] = sorted(abstract_input(spec))
            elif role in SHARED_ROLES:
                add("role:" + role, W_ROLE)
                if spec.get("multiple"):
                    add("role:%s:mult" % role, W_ARITY)
                if spec.get("required"):
                    add("role:%s:req" % role, W_ARITY)
                for s in abstract_input(spec):
                    add("in:%s:%s" % (role, s), W_IN)
                readable["roles"].append(role)
                readable["inputs"][role] = sorted(abstract_input(spec))
            else:
                has_other = True
                readable["other_roles"].append(role)
        if has_other:
            add("has_other_roles", W_OTHER_ROLES)
        if "children" in e:  # tree-sitter's key for the sub-node spec
            add("has_subnode_spec", W_SUBNODE)
        if not e.get("fields") and "children" not in e:
            add("is_leaf", W_LEAF)
        for s in out_sig(name):
            add("out:" + s, W_OUT)
            if V2_COUNTS and s in pos_counts.get(name, {}):
                add("out:%s:xb%d" % (s, count_bucket(pos_counts[name][s])),
                    W_OUT_COUNT)
        readable["out"] = sorted(out_sig(name))
        if V2_COUNTS:
            readable["out_counts"] = dict(pos_counts.get(name, {}))
        result[name] = {"features": feats, "readable": readable}
    return result


def main():
    global HOLD_OUT_DECLARED, V2_COUNTS
    fname = "features.json"
    if "--v2" in sys.argv:
        V2_COUNTS = True
        fname = "features_v2.json"
    if "--hold-out-declared" in sys.argv:
        HOLD_OUT_DECLARED = True
        fname = ("features_v2_holdout.json" if V2_COUNTS
                 else "features_holdout.json")
    out = {lang: build_language(lang) for lang in LANGS}
    path = os.path.join(HERE, fname)
    with open(path, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for lang in LANGS:
        print(lang, len(out[lang]), "kinds")
    print("wrote", path)


if __name__ == "__main__":
    main()
